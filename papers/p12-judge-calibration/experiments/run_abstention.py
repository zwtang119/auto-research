#!/usr/bin/env python3
"""P12 M5b — Abstention-aware judge runner.

Mirror of `run_blind_baseline.py` with one difference: the prompt allows
the judge to abstain when it judges the evidence insufficient. The
metric is `abstain_rate` + the residual score on non-abstained items.

Output:
- experiments/abstention_results.json (450 rows, awareness="abstention")
- experiments/abstention_responses/R-P12-abstention-NNN.txt
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

# --- Paths (same as M2/M3) ------------------------------------------------
P12_ROOT = Path(__file__).resolve().parent.parent
AUTO_ROOT = P12_ROOT.parent.parent

EXPERIMENTS = P12_ROOT / "experiments"
MANIFEST = EXPERIMENTS / "sample_manifest.jsonl"
FROZEN = EXPERIMENTS / "sample_ids_ordered.json"
OUT_RESULT = EXPERIMENTS / "abstention_results.json"
OUT_RESPONSES = EXPERIMENTS / "abstention_responses"

VENDOR_ROOT = AUTO_ROOT / "framework" / "vendor"
POLICYSIM_SCRIPTS = VENDOR_ROOT / "policysim_scripts"
POLICYSIM_CONFIG = VENDOR_ROOT / "policysim_config" / "experiment-config.yaml"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = line.strip() if (line := raw.strip()) else ""
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))


_load_env_file(AUTO_ROOT / ".env")

JUDGE_MODEL = "deepseek-v4-pro"
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


# --- ABSTENTION PROMPT -----------------------------------------------------
ABSTENTION_PROMPT = """You are an LLM judge scoring a role-conditioned policy
simulation output for character-consistency. The producer wrote under one
of the standard conditions; the condition label is intentionally hidden.

## Enterprise context
- Enterprise ID: {enterprise_id}

## Agent output (to be scored)
{agent_output}

## Scoring dimensions (1.0–5.0)
1. **risk_tolerance_consistency**
2. **innovation_focus_consistency**
3. **compliance_culture_consistency**
4. **market_influence_consistency**
5. **agility_score_consistency**

## Abstention policy
If you judge that the available evidence is insufficient to score reliably
— for example, the output is too short, off-topic, internally contradictory,
or you cannot tell which scoring dimension is being violated — you MAY
abstain instead of guessing. **Abstaining is preferred over guessing.**
When abstaining, set `"abstain": true` and provide a one-sentence
`abstain_reason`. Otherwise score normally.

## Output format (strict JSON, no extra text)
```json
{{
  "abstain": <bool>,
  "abstain_reason": "<non-empty if abstain=true, else empty string>",
  "scores": {{
    "risk_tolerance_consistency": <float>,
    "innovation_focus_consistency": <float>,
    "compliance_culture_consistency": <float>,
    "market_influence_consistency": <float>,
    "agility_score_consistency": <float>
  }},
  "awareness": "abstention"
}}
```

When `abstain=true`, the `scores` object MAY be omitted or set to null."""


def build_messages(sample: dict, yaml_data: dict) -> list[dict]:
    return [{
        "role": "user",
        "content": ABSTENTION_PROMPT.format(
            enterprise_id=sample["original_enterprise"],
            agent_output=yaml_data["agent_output"],
        ),
    }]


def _extract_first_balanced_json(text: str) -> Optional[str]:
    start = text.find("{")
    if start == -1:
        return None
    depth, in_str, esc = 0, False, False
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
        prompt_stage="p12_m5b_abstention",
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


def make_record(sample: dict, idx: int, parsed: dict, judge_id: str, dt_ms: int) -> dict:
    record_id = f"R-P12-abstention-{idx:03d}"
    abstain = bool(parsed.get("abstain", False))
    scores = parsed.get("scores", {}) or {}
    score, _ = aggregate_score(scores)
    return {
        "record_id": record_id,
        "sample_id": sample["sample_id"],
        "protocol": "abstention",
        "judge_id": judge_id,
        "awareness": "abstention",
        "score": score,
        "score_band": band_for(score),
        "abstain": abstain,
        "abstain_reason": parsed.get("abstain_reason", "") if abstain else "",
        "consistency_on_wrong": 1.0,
        "ground_truth_correctness": None,
        "leakage_hint_visible_to_judge": "",
        "per_dimension_scores": scores,
        "judge_called_at": utc_iso(),
        "judge_call_ms": dt_ms,
        "raw_response_path": f"experiments/abstention_responses/{record_id}.txt",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    if not MANIFEST.exists() or not FROZEN.exists():
        print("FATAL: manifest/frozen missing", file=sys.stderr)
        return 2

    if not POLICYSIM_CONFIG.exists():
        print("FATAL: config missing", file=sys.stderr)
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
        print(f"FATAL: pre-flight: {e}", file=sys.stderr)
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
        yaml_path = AUTO_ROOT / sample["source_path"]
        if not yaml_path.exists():
            continue
        try:
            yaml_data = load_yaml(yaml_path)
        except Exception as e:
            print(f"WARN: {sample_id} yaml parse failed: {e}", file=sys.stderr)
            continue

        messages = build_messages(sample, yaml_data)
        parsed = call_judge_real(messages)
        dt_ms = parsed.pop("_dt_ms", 0)
        if parsed.get("_parse_failed"):
            parse_failures += 1
            (OUT_RESPONSES / f"R-P12-abstention-{idx:03d}.txt").write_text(
                parsed.get("raw", ""), encoding="utf-8"
            )
            continue

        (OUT_RESPONSES / f"R-P12-abstention-{idx:03d}.txt").write_text(
            parsed.pop("_raw", ""), encoding="utf-8"
        )

        record = make_record(sample, idx, parsed, JUDGE_MODEL, dt_ms)

        # PIT-103: abstain=true ⇒ reason non-empty
        if record["abstain"] and not record["abstain_reason"]:
            print(f"WARN: {sample_id} abstained without reason", file=sys.stderr)
            record["abstain_reason"] = "unspecified"

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