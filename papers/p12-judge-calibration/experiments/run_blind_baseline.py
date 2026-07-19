#!/usr/bin/env python3
"""P12 M3 — Blind baseline judge run.

Mirror of `run_leaked_baseline.py` but with the condition label STRIPPED
from the judge prompt. The judge is told only that the producer wrote
"under one of the standard conditions" but NOT which one, so
awareness="blind" forces the judge to score without label cue.

Emits `experiments/blind_baseline_results.json` (json array of rows
matching `judge_protocol_result` schema, data-contracts §7).
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

# --- Paths (same as M2) ---------------------------------------------------
P12_ROOT = Path(__file__).resolve().parent.parent
AUTO_ROOT = P12_ROOT.parent.parent
P11_ROOT = (AUTO_ROOT / "legacy" / "p11-closed-v5-minimax-m3")
P11_A_YAML = P11_ROOT / "experiments" / "h5-emergence" / "A" / "yaml"

EXPERIMENTS = P12_ROOT / "experiments"
MANIFEST = EXPERIMENTS / "sample_manifest.jsonl"
FROZEN = EXPERIMENTS / "sample_ids_ordered.json"
OUT_RESULT = EXPERIMENTS / "blind_baseline_results.json"
OUT_RESPONSES = EXPERIMENTS / "blind_responses"

VENDOR_ROOT = AUTO_ROOT / "framework" / "vendor"
POLICYSIM_SCRIPTS = VENDOR_ROOT / "policysim_scripts"
POLICYSIM_CONFIG = VENDOR_ROOT / "policysim_config" / "experiment-config.yaml"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        os.environ.setdefault(k, v)


_load_env_file(AUTO_ROOT / ".env")

# --- constants -----------------------------------------------------------
JUDGE_MODEL = "deepseek-v4-pro"     # same judge as M2, for paired comparison
SCORE_BANDS = [(1.0, 2.0, "low"), (2.0, 3.5, "mid"), (3.5, 5.0, "high")]


def band_for(score: float) -> str:
    for lo, hi, name in SCORE_BANDS:
        if lo <= score < hi:
            return name
    return "high" if score >= 5.0 else "low"


def utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_yaml(p: Path) -> dict:
    import yaml
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{p}: not a yaml map at root")
    if "agent_output" not in data:
        raise ValueError(f"{p}: missing agent_output field")
    return data


# --- prompt (BLIND: condition label stripped) ----------------------------
BLIND_PROMPT = """You are an LLM judge scoring a role-conditioned policy
simulation output for character-consistency.

## Original condition (NOT disclosed — blind variant)
The producer wrote under one of the standard conditions. The condition
label is intentionally hidden from you. Score only on the basis of the
agent output below.

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
  "awareness": "blind"
}}
```

Emit ONLY the JSON. No commentary."""


def build_messages(sample: dict, yaml_data: dict) -> list[dict]:
    return [{
        "role": "user",
        "content": BLIND_PROMPT.format(
            enterprise_id=sample["original_enterprise"],
            agent_output=yaml_data["agent_output"],
        ),
    }]


def _extract_first_balanced_json(text: str) -> Optional[str]:
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
    for m in re.finditer(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL):
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass
    block = _extract_first_balanced_json(text)
    if block:
        try:
            return json.loads(block)
        except json.JSONDecodeError:
            pass
    return None


def call_judge_real(messages: list[dict]) -> dict:
    sys.path.insert(0, str(POLICYSIM_SCRIPTS))
    from api_client import load_config, call_model
    config = load_config(str(POLICYSIM_CONFIG))
    t0 = time.time()
    content, _usage = call_model(
        config, JUDGE_MODEL, messages,
        temperature=0.2,
        max_tokens=2048,
        prompt_stage="p12_m3_blind",
    )
    dt_ms = int((time.time() - t0) * 1000)
    parsed = parse_judge_response(content)
    if parsed is None:
        return {"_parse_failed": True, "raw": content, "dt_ms": dt_ms}
    parsed["_dt_ms"] = dt_ms
    parsed["_raw"] = content
    return parsed


def aggregate_score(scores: dict) -> tuple[float, bool]:
    vals = [v for v in (scores or {}).values() if isinstance(v, (int, float))]
    if not vals:
        return 0.0, True
    return round(sum(vals) / len(vals), 3), False


def make_record(sample: dict, idx: int, score: float, parsed: dict,
                cond_label: str, judge_id: str, dt_ms: int,
                abstained: bool = False,
                abstain_reason: str = "") -> dict:
    record_id = f"R-P12-blind-{idx:03d}"
    return {
        "record_id": record_id,
        "sample_id": sample["sample_id"],
        "protocol": "blind",
        "judge_id": judge_id,
        "awareness": "blind",
        "score": score,
        "score_band": band_for(score),
        "abstain": abstained,
        "abstain_reason": abstain_reason,
        "consistency_on_wrong": 1.0,
        "ground_truth_correctness": None,
        "leakage_hint_visible_to_judge": "",  # blind variant: no hint
        "per_dimension_scores": parsed.get("scores", {}),
        "judge_called_at": utc_iso(),
        "judge_call_ms": dt_ms,
        "raw_response_path": f"experiments/blind_responses/{record_id}.txt",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0,
                    help="if > 0, only score the first N rows")
    args = ap.parse_args()

    if not MANIFEST.exists():
        print(f"FATAL: {MANIFEST} missing", file=sys.stderr)
        return 2
    if not FROZEN.exists():
        print(f"FATAL: {FROZEN} missing", file=sys.stderr)
        return 2

    if not POLICYSIM_CONFIG.exists():
        print(f"FATAL: {POLICYSIM_CONFIG} missing", file=sys.stderr)
        return 2
    try:
        sys.path.insert(0, str(POLICYSIM_SCRIPTS))
        from api_client import load_config
        cfg = load_config(str(POLICYSIM_CONFIG))
        api_key_env = cfg["api_endpoints"][cfg["models"][JUDGE_MODEL]["provider"]]["api_key_env"]
        if not os.environ.get(api_key_env):
            print(f"FATAL: env ${api_key_env} not set", file=sys.stderr)
            return 2
    except Exception as e:
        print(f"FATAL: pre-flight import failed: {e}", file=sys.stderr)
        return 2

    OUT_RESPONSES.mkdir(parents=True, exist_ok=True)

    samples_by_id = {}
    for line in open(MANIFEST):
        r = json.loads(line)
        samples_by_id[r["sample_id"]] = r

    frozen_ids = json.loads(FROZEN.read_text())
    if args.limit and args.limit > 0:
        frozen_ids = frozen_ids[:args.limit]

    out_records = []
    parse_failures = 0
    t_run = time.time()
    for idx, sample_id in enumerate(frozen_ids, start=1):
        sample = samples_by_id[sample_id]
        sample_yaml_path = AUTO_ROOT / sample["source_path"]
        if not sample_yaml_path.exists():
            print(f"WARN: {sample_id} source yaml missing", file=sys.stderr)
            continue
        try:
            yaml_data = load_yaml(sample_yaml_path)
        except Exception as e:
            print(f"WARN: {sample_id} yaml parse failed: {e}", file=sys.stderr)
            continue

        messages = build_messages(sample, yaml_data)
        parsed = call_judge_real(messages)
        dt_ms = parsed.pop("_dt_ms", 0)
        if parsed.get("_parse_failed"):
            parse_failures += 1
            (OUT_RESPONSES / f"R-P12-blind-{idx:03d}.txt").write_text(
                parsed.get("raw", ""), encoding="utf-8"
            )
            continue

        (OUT_RESPONSES / f"R-P12-blind-{idx:03d}.txt").write_text(
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

        if idx < len(frozen_ids):
            time.sleep(0.5)

    OUT_RESULT.write_text(json.dumps(out_records, ensure_ascii=False, indent=2))
    elapsed = time.time() - t_run
    print(f"\nWrote {len(out_records)} records → {OUT_RESULT}")
    print(f"elapsed: {elapsed:.1f}s · parse_failures: {parse_failures}")
    if parse_failures > 0:
        ratio = parse_failures / (parse_failures + len(out_records))
        if ratio > 0.20:
            print(f"ALARM: parse failure ratio {ratio:.1%} > 20%", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())