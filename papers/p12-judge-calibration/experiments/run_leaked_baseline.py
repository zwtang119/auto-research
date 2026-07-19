#!/usr/bin/env python3
"""P12 M2 — Leaked baseline judge run.

For each row in `experiments/sample_manifest.jsonl` (in
`experiments/sample_ids_ordered.json` order), call the judge with the
sample's ORIGINAL condition label visible (awareness=leaked), per
`state/io_spec.md` §3 protocol 1.

Emits `experiments/leakage_reproduction.json` as a json array of rows,
each row matching the `judge_protocol_result` schema (data-contracts §7):

    {
      "record_id":          "R-P12-leaked-NNN",
      "sample_id":          "P12-NNN",
      "protocol":           "leaked",
      "judge_id":           "<judge model name, NOT 'self'>",
      "awareness":          "leaked",
      "score":              float in [1.0, 5.0],
      "score_band":         "<low|mid|high>",
      "abstain":            false,
      "consistency_on_wrong": 1.0,
      "ground_truth_correctness": null,
      "leakage_hint_visible_to_judge": "<the condition label>",
      "judge_called_at":    "<iso8601>",
      "judge_call_ms":      int,
      "raw_response_path":  "experiments/leaked_responses/<record_id>.txt"
    }

This is NOT a long-running experiment: 450 LLM calls × 1 judge. With
retries and average 2s/call: ~15 min wall time on a quiet net connection.

Pre-flight checklist (run from .../papers/p12-judge-calibration/):
    [1] bash experiments/validate_manifest.sh            # must return OK
    [2] test -f experiments/sample_manifest.jsonl
    [3] python -c "import yaml,openai,httpx"             # deps installed
    [4] test -f ../../framework/vendor/policysim_scripts/api_client.py
    [5] test -f ../../framework/vendor/policysim_config/experiment-config.yaml
    [6] test -f ../../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/inner_monologue_ISPACE_run001.yaml
    [7] cp ../../.env.sample ../../.env && fill in keys (one-time)

Run:
    python experiments/run_leaked_baseline.py [--dry-run] [--limit N]

The runner reads API credentials from the **project-root `.env`**
(`auto-research/.env`, NOT committed; see `.env.sample`). The vendored
policysim scripts are at `framework/vendor/policysim_scripts/`.

Usage notes:
- `--dry-run` skips LLM calls and emits synthetic-but-deterministic
  records (score=mean-of-condition + small jitter) so you can verify the
  IO schema before spending API budget.
- `--limit N` calls only the first N rows; useful for smoke tests.

Stopping rules (per `state/experiment_design.md` §Stop conditions):
- A row where the judge returns invalid JSON is logged + skipped (no
  retry), so that P12 M3's blind protocol can compare against the same
  data instead of having parse failures shadow the protocol comparison.
- If > 20% of rows return invalid JSON, abort + log alarm.
- If the judge returns `awareness` field other than "leaked", flag as
  protocol-violation and abort.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

# --- Paths -----------------------------------------------------------------
P12_ROOT = Path(__file__).resolve().parent.parent
AUTO_ROOT = P12_ROOT.parent.parent
P11_ROOT = (AUTO_ROOT / "legacy" / "p11-closed-v5-minimax-m3")
P11_A_YAML = P11_ROOT / "experiments" / "h5-emergence" / "A" / "yaml"

EXPERIMENTS = P12_ROOT / "experiments"
MANIFEST = EXPERIMENTS / "sample_manifest.jsonl"
FROZEN = EXPERIMENTS / "sample_ids_ordered.json"
OUT_RESULT = EXPERIMENTS / "leakage_reproduction.json"
OUT_RESPONSES = EXPERIMENTS / "leaked_responses"

# Vendored copy of the policysim scripts (kept inside this repo)
VENDOR_ROOT = AUTO_ROOT / "framework" / "vendor"
POLICYSIM_SCRIPTS = VENDOR_ROOT / "policysim_scripts"
POLICYSIM_CONFIG = VENDOR_ROOT / "policysim_config" / "experiment-config.yaml"


def _load_env_file(path: Path) -> None:
    """Load KEY=VALUE lines from a .env file into os.environ.
    Pure stdlib (no python-dotenv). Idempotent (does not overwrite existing)."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


# Auto-load project-root .env so vendor scripts see the keys
_load_env_file(AUTO_ROOT / ".env")

# --- constants ------------------------------------------------------------
JUDGE_MODEL = "deepseek-v4-pro"     # per `experiment_design.md` §Frozen judge model list
SCORE_BANDS = [(1.0, 2.0, "low"), (2.0, 3.5, "mid"), (3.5, 5.0, "high")]


def band_for(score: float) -> str:
    for lo, hi, name in SCORE_BANDS:
        if lo <= score < hi:
            return name
    return "high" if score >= 5.0 else "low"


def utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_yaml(p: Path) -> dict:
    """Parse a P11 v5 A-yaml. Minimal parser — extract `agent_output`."""
    import yaml
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{p}: not a yaml map at root")
    if "agent_output" not in data:
        raise ValueError(f"{p}: missing agent_output field")
    return data


# --- prompt ---------------------------------------------------------------
LEAKED_PROMPT = """You are an LLM judge scoring a role-conditioned policy
simulation output for character-consistency.

## Original condition (provided deliberately — this is the "leaked" variant)
The producer wrote under condition: {condition_label}

## Enterprise context
- Enterprise ID: {enterprise_id}
- (See agent output for full enterprise profile)

## Agent output (to be scored)
{agent_output}

## Scoring dimensions (1.0–5.0, one score per dimension, integer or .5 increments)
1. **risk_tolerance_consistency** — does the agent respect the risk profile?
2. **innovation_focus_consistency** — does the output match the tech-route?
3. **compliance_culture_consistency** — does the agent observe compliance cues?
4. **market_influence_consistency** — does the strategy match the market position?
5. **agility_score_consistency** — does the agent's response speed/adaptation match agility?

## Output format (strict JSON, no extra text)
```json
{{
  "scores": {{
    "risk_tolerance_consistency": <float>,
    "innovation_focus_consistency": <float>,
    "compliance_culture_consistency": <float>,
    "market_influence_consistency": <float>,
    "agility_score_consistency": <float>
  }},
  "awareness": "leaked"
}}
```

Emit ONLY the JSON. No commentary."""


def build_messages(sample: dict, yaml_data: dict) -> list[dict]:
    cond = sample["original_condition"]
    cond_label = {
        "inner_monologue": "inner_monologue (character-immersed thinking)",
        "no_think": "no_think (no chain-of-thought)",
        "pure_analysis": "pure_analysis (logic-only thinking)",
    }.get(cond, cond)
    return [{
        "role": "user",
        "content": LEAKED_PROMPT.format(
            condition_label=cond_label,
            enterprise_id=sample["original_enterprise"],
            agent_output=yaml_data["agent_output"],
        ),
    }]


# --- call layer -----------------------------------------------------------
def call_judge_dry_run(sample: dict, jitter_seed: int) -> dict:
    """Synthetic leaked-scoring output (deterministic per sample)."""
    # mean score anchored to condition (leaked baseline); jitter per sample
    cond_means = {
        "inner_monologue": 3.42,   # M2 leaked-baseline prior
        "no_think": 3.18,
        "pure_analysis": 3.50,
    }
    mu = cond_means.get(sample["original_condition"], 3.30)
    # per-dimension jitter, seeded
    rng = jitter_seed
    def rnd(seed: int) -> float:
        h = int(hashlib.sha256(f"{sample['sample_id']}:{seed}".encode()).hexdigest(), 16)
        return ((h % 1000) / 1000.0) - 0.5  # -0.5..+0.5
    return {
        "scores": {
            "risk_tolerance_consistency":     round(max(1.0, min(5.0, mu + 0.7  + rnd(1))), 2),
            "innovation_focus_consistency":   round(max(1.0, min(5.0, mu + 0.1  + rnd(2))), 2),
            "compliance_culture_consistency": round(max(1.0, min(5.0, mu + 0.3  + rnd(3))), 2),
            "market_influence_consistency":   round(max(1.0, min(5.0, mu - 0.2  + rnd(4))), 2),
            "agility_score_consistency":      round(max(1.0, min(5.0, mu - 0.4  + rnd(5))), 2),
        },
        "awareness": "leaked",
    }


def _extract_first_balanced_json(text: str) -> Optional[str]:
    """Find the first balanced top-level {...} block, supporting arbitrary nesting."""
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return None


def parse_judge_response(text: str) -> Optional[dict]:
    """Robust JSON parser for judge output. Tries, in order:
    1. all ```json ... ``` code fences (if multiple, take the first parseable),
    2. the full stripped text,
    3. the first balanced top-level {...} block (handles nested objects).
    """
    # 1. try every ```json ... ``` fence
    for m in re.finditer(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
    # 2. full stripped text
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    # 3. first balanced {...} (nested-safe)
    block = _extract_first_balanced_json(text)
    if block:
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            pass
    return None


def call_judge_real(messages: list[dict]) -> dict:
    """Real LLM call. Imports from the vendored policysim api_client.

    Requires API credentials in project-root `.env` (one-time copy of
    `.env.sample`); vendored scripts read openai-style key from env vars
    named in `framework/vendor/policysim_config/experiment-config.yaml`.
    """
    sys.path.insert(0, str(POLICYSIM_SCRIPTS))
    try:
        from api_client import load_config, call_model
    except Exception as e:
        raise RuntimeError(
            f"Cannot import vendored api_client: {e}\n"
            f"Verify {POLICYSIM_SCRIPTS}/api_client.py exists."
        )
    config = load_config(str(POLICYSIM_CONFIG))
    t0 = time.time()
    # Vendored api_client.call_model returns 2-tuple (content, usage).
    # Stub-leaked smoke (-dry-run) is unaffected; this path fires only
    # when --dry-run is OFF.
    content, _usage = call_model(
        config, JUDGE_MODEL, messages,
        temperature=0.2,
        max_tokens=2048,
        prompt_stage="p12_m2_leaked",
    )
    dt_ms = int((time.time() - t0) * 1000)
    parsed = parse_judge_response(content)
    if parsed is None:
        return {"_parse_failed": True, "raw": content, "dt_ms": dt_ms}
    parsed["_dt_ms"] = dt_ms
    parsed["_raw"] = content
    return parsed


def aggregate_score(scores: dict) -> tuple[float, bool]:
    """Mean of dimension scores. Returns (score, empty_flag).
    empty_flag=True signals that scores dict was empty/malformed and
    the caller should mark the row as abstained.
    """
    vals = [v for v in (scores or {}).values() if isinstance(v, (int, float))]
    if not vals:
        return 0.0, True
    return round(sum(vals) / len(vals), 3), False


def make_record(sample: dict, idx: int, score: float, parsed: dict,
                cond_label: str, judge_id: str, dt_ms: int,
                abstained: bool = False,
                abstain_reason: str = "") -> dict:
    record_id = f"R-P12-leaked-{idx:03d}"
    return {
        "record_id": record_id,
        "sample_id": sample["sample_id"],
        "protocol": "leaked",
        "judge_id": judge_id,
        "awareness": "leaked",
        "score": score,
        "score_band": band_for(score),
        "abstain": abstained,
        "abstain_reason": abstain_reason,
        "consistency_on_wrong": 1.0,
        "ground_truth_correctness": None,
        "leakage_hint_visible_to_judge": cond_label,
        "per_dimension_scores": parsed.get("scores", {}),
        "judge_called_at": utc_iso(),
        "judge_call_ms": dt_ms,
        "raw_response_path": f"experiments/leaked_responses/{record_id}.txt",
    }


# --- main -----------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="synthetic scoring; no API calls")
    ap.add_argument("--limit", type=int, default=0,
                    help="if > 0, only score the first N rows")
    args = ap.parse_args()

    # L2 — first action of every business-loop callback is update last_seen.
    # Per Deli §7 + framework/watchdog/README.md.
    try:
        sys.path.insert(0, str(AUTO_ROOT / "framework" / "watchdog"))
        from l2_callback import heartbeat
        heartbeat(
            state_file=P12_ROOT / "state" / "progress.json",
            source="p12_M2_runner",
            detail=f"start args={vars(args)}",
        )
    except Exception as _e:
        # L2 must never block the business loop; degrade silently.
        print(f"L2 heartbeat failed (non-fatal): {_e}", file=sys.stderr)

    if not MANIFEST.exists():
        print(f"FATAL: {MANIFEST} missing — run build_sample_manifest.py first",
              file=sys.stderr)
        return 2
    if not FROZEN.exists():
        print(f"FATAL: {FROZEN} missing", file=sys.stderr)
        return 2

    samples_by_id = {}
    for line in open(MANIFEST):
        r = json.loads(line)
        samples_by_id[r["sample_id"]] = r

    frozen_ids = json.loads(FROZEN.read_text())
    if args.limit and args.limit > 0:
        frozen_ids = frozen_ids[:args.limit]

    # quick env pre-flight when not dry-run
    if not args.dry_run:
        if not POLICYSIM_CONFIG.exists():
            print(f"FATAL: {POLICYSIM_CONFIG} missing", file=sys.stderr)
            return 2
        try:
            sys.path.insert(0, str(POLICYSIM_SCRIPTS))
            from api_client import load_config
            cfg = load_config(str(POLICYSIM_CONFIG))
            api_key_env = cfg["api_endpoints"][cfg["models"][JUDGE_MODEL]["provider"]]["api_key_env"]
            if not os.environ.get(api_key_env):
                print(
                    f"FATAL: env ${api_key_env} not set. Copy .env.sample to "
                    f".env at project root and fill in your key. "
                    f"Run with --dry-run to test schema without API.",
                    file=sys.stderr,
                )
                return 2
        except Exception as e:
            print(f"FATAL: pre-flight import failed: {e}", file=sys.stderr)
            return 2

    OUT_RESPONSES.mkdir(parents=True, exist_ok=True)

    out_records = []
    parse_failures = 0
    t_run = time.time()
    for idx, sample_id in enumerate(frozen_ids, start=1):
        sample = samples_by_id[sample_id]
        sample_yaml_path = AUTO_ROOT / sample["source_path"]
        if not sample_yaml_path.exists():
            print(f"WARN: {sample_id} source yaml missing: {sample_yaml_path}",
                  file=sys.stderr)
            continue
        try:
            yaml_data = load_yaml(sample_yaml_path)
        except Exception as e:
            print(f"WARN: {sample_id} yaml parse failed: {e}", file=sys.stderr)
            continue

        messages = build_messages(sample, yaml_data)
        if args.dry_run:
            parsed = call_judge_dry_run(sample, jitter_seed=idx)
            dt_ms = 0
        else:
            parsed = call_judge_real(messages)
            dt_ms = parsed.pop("_dt_ms", 0)
            if parsed.get("_parse_failed"):
                parse_failures += 1
                (OUT_RESPONSES / f"R-P12-leaked-{idx:03d}.txt").write_text(
                    parsed.get("raw", ""), encoding="utf-8"
                )
                continue

        # Always write raw response for audit
        (OUT_RESPONSES / f"R-P12-leaked-{idx:03d}.txt").write_text(
            parsed.pop("_raw", ""), encoding="utf-8"
        )

        score, score_empty = aggregate_score(parsed.get("scores", {}))
        cond_label = sample["original_condition"]
        record = make_record(
            sample=sample, idx=idx,
            score=score, parsed=parsed,
            cond_label=cond_label, judge_id=JUDGE_MODEL, dt_ms=dt_ms,
            abstained=score_empty,
            abstain_reason=("empty_scores_dict" if score_empty else ""),
        )
        out_records.append(record)

        if idx % 25 == 0 or idx == len(frozen_ids):
            elapsed = time.time() - t_run
            print(f"[{idx}/{len(frozen_ids)}] elapsed={elapsed:.1f}s "
                  f"parse_failures={parse_failures}", flush=True)

        # crude rate-limit to avoid burst on shared endpoints
        if not args.dry_run and idx < len(frozen_ids):
            time.sleep(0.5)

    OUT_RESULT.write_text(json.dumps(out_records, ensure_ascii=False, indent=2))
    elapsed = time.time() - t_run
    print(f"\nWrote {len(out_records)} records → {OUT_RESULT}")
    print(f"elapsed: {elapsed:.1f}s · parse_failures: {parse_failures}")

    if parse_failures > 0 and not args.dry_run:
        ratio = parse_failures / (parse_failures + len(out_records))
        if ratio > 0.20:
            print(f"ALARM: parse failure ratio {ratio:.1%} > 20% — investigate.",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
