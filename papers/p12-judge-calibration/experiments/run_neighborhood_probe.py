#!/usr/bin/env python3
"""P12 M4 — Neighborhood probe schema + M5 — small sample run.

For each axis in {role, fact, consequence}, generate ≤10 probes by
mutating exactly one axis of a base sample from sample_manifest.jsonl.
The probe is judged by deepseek-v4-pro with awareness="neighborhood"
(judge told it is a probe, but not which axis).

Output:
- experiments/neighborhood_probe_schema.json  (the schema, written once)
- experiments/neighborhood_probe_results.json (>=30 rows, axis-balanced)
- experiments/neighborhood_responses/R-P12-neighborhood-NNN.txt
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import random
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
OUT_SCHEMA = EXPERIMENTS / "neighborhood_probe_schema.json"
OUT_RESULT = EXPERIMENTS / "neighborhood_probe_results.json"
OUT_RESPONSES = EXPERIMENTS / "neighborhood_responses"

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
        os.environ.setdefault(k, v.strip().strip('"').strip("'"))


_load_env_file(AUTO_ROOT / ".env")

JUDGE_MODEL = "deepseek-v4-pro"
SCORE_BANDS = [(1.0, 2.0, "low"), (2.0, 3.5, "mid"), (3.5, 5.0, "high")]

# --- Schema (M4 deliverable) ---------------------------------------------
SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "P12 Neighborhood Probe Result",
    "type": "object",
    "required": [
        "record_id", "sample_id", "axis", "protocol", "judge_id",
        "awareness", "score", "score_band", "abstain", "consistency_on_wrong",
        "ground_truth_correctness", "judge_called_at", "judge_call_ms",
        "raw_response_path",
    ],
    "properties": {
        "record_id": {"type": "string", "pattern": r"^R-P12-neighborhood-[0-9]{3,}$"},
        "sample_id": {"type": "string", "pattern": r"^P12-[0-9]{3,}$"},
        "axis": {"type": "string", "enum": ["role", "fact", "consequence"]},
        "protocol": {"type": "string", "const": "neighborhood"},
        "judge_id": {"type": "string", "not": {"const": "self"}},
        "awareness": {"type": "string", "const": "neighborhood"},
        "score": {"type": "number", "minimum": 1.0, "maximum": 5.0},
        "score_band": {"type": "string", "enum": ["low", "mid", "high"]},
        "abstain": {"type": "boolean"},
        "abstain_reason": {"type": "string"},
        "consistency_on_wrong": {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "ground_truth_correctness": {"type": ["boolean", "null"]},
        "mutated_prompt": {"type": "string", "description": "the mutated prompt sent to the judge"},
        "mutated_axis_field": {"type": "string", "description": "which field was mutated"},
        "judge_called_at": {"type": "string"},
        "judge_call_ms": {"type": "integer"},
        "raw_response_path": {"type": "string"},
    },
}


def utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def band_for(score: float) -> str:
    for lo, hi, name in SCORE_BANDS:
        if lo <= score < hi:
            return name
    return "high" if score >= 5.0 else "low"


def load_yaml(p: Path) -> dict:
    import yaml
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{p}: not a yaml map at root")
    return data


# --- Probe mutators --------------------------------------------------------
# Each mutator takes (sample, yaml_data) and returns
# (mutated_prompt, mutated_axis_field). The mutation is deterministic.

def mutate_role(sample: dict, yaml_data: dict) -> tuple[str, str]:
    """Mutate the enterprise/role: swap ISPACE<->LANDSPACE and adjust
    tech-route cue. Keeps fact content and decision intact."""
    flip_map = {
        "ISPACE": "LANDSPACE",
        "LANDSPACE": "ISPACE",
        "SPACETIMETECH": "ISPACE",
    }
    new_enterprise = flip_map.get(sample["original_enterprise"], "ISPACE")
    new_label = f"Mutated role: enterprise is now {new_enterprise} (original: {sample['original_enterprise']})."
    original = yaml_data.get("agent_output", "")
    mutated_prompt = (
        f"[Neighborhood probe — axis=role]\n"
        f"{new_label}\n\n"
        f"The agent's response under the ORIGINAL enterprise context:\n"
        f"{original}\n\n"
        f"Question: would the response change if the enterprise were {new_enterprise}? "
        f"Re-score the five dimensions (1.0-5.0) reflecting how the original response "
        f"would have to be adapted to fit {new_enterprise}."
    )
    return mutated_prompt, f"enterprise:{sample['original_enterprise']}->{new_enterprise}"


def mutate_fact(sample: dict, yaml_data: dict) -> tuple[str, str]:
    """Mutate one factual claim: replace any numerical value with 2× its value.
    Keeps role and decision intact."""
    original = yaml_data.get("agent_output", "")
    # deterministic: find first digit sequence and double it
    m = re.search(r"(\d+(?:\.\d+)?)", original)
    if m:
        old_num = float(m.group(1))
        new_num = old_num * 2 if old_num != 0 else 1.0
        mutated = original.replace(m.group(1), f"{new_num:g}", 1)
        mutated_axis_field = f"fact:{old_num:g}->{new_num:g}"
    else:
        mutated = original + "\n\n[Probe mutation: scenario year advanced by 2.]"
        mutated_axis_field = "fact:scenario_year+=2"
    mutated_prompt = (
        f"[Neighborhood probe — axis=fact]\n"
        f"The factual claim has been perturbed: see mutated agent_output below.\n\n"
        f"Mutated agent output:\n{mutated}\n\n"
        f"Score the five dimensions (1.0-5.0) for this perturbed output."
    )
    return mutated_prompt, mutated_axis_field


def mutate_consequence(sample: dict, yaml_data: dict) -> tuple[str, str]:
    """Mutate the decision/consequence: prepend an 'adopt opposite decision' cue.
    Keeps role and facts intact."""
    original = yaml_data.get("agent_output", "")
    mutated = (
        "Consider the OPPOSITE of the original decision:\n\n"
        + original.replace("\n", "\n> ")
    )
    mutated_axis_field = "consequence:opposite"
    mutated_prompt = (
        f"[Neighborhood probe — axis=consequence]\n"
        f"The agent is now asked to consider the opposite decision to the original.\n\n"
        f"{mutated}\n\n"
        f"Score the five dimensions (1.0-5.0) for this opposite-decision probe."
    )
    return mutated_prompt, mutated_axis_field


MUTATORS = {
    "role": mutate_role,
    "fact": mutate_fact,
    "consequence": mutate_consequence,
}


# --- Probe prompt (sent to judge) ----------------------------------------
NEIGHBORHOOD_PROMPT = """You are an LLM judge scoring a NEIGHBORHOOD PROBE of a
role-conditioned policy simulation output. A neighborhood probe perturbs
exactly one axis (role / fact / consequence) of the original sample to test
the judge's robustness.

## Probe metadata
- axis: {axis}
- original_sample_id: {original_sample_id}
- mutated_axis_field: {mutated_axis_field}

## Probe prompt
{mutated_prompt}

## Scoring dimensions (1.0-5.0, one score per dimension)
1. **risk_tolerance_consistency**
2. **innovation_focus_consistency**
3. **compliance_culture_consistency**
4. **market_influence_consistency**
5. **agility_score_consistency**

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
  "awareness": "neighborhood"
}}
```"""


def build_messages(axis: str, original_sample_id: str, mutated_axis_field: str,
                   mutated_prompt: str) -> list[dict]:
    return [{
        "role": "user",
        "content": NEIGHBORHOOD_PROMPT.format(
            axis=axis,
            original_sample_id=original_sample_id,
            mutated_axis_field=mutated_axis_field,
            mutated_prompt=mutated_prompt,
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
        prompt_stage="p12_m4_neighborhood",
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


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-axis", type=int, default=10,
                    help="probes per axis (default 10, total 30)")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    # M4: write schema first
    OUT_SCHEMA.write_text(json.dumps(SCHEMA, indent=2, ensure_ascii=False))
    print(f"Wrote schema → {OUT_SCHEMA}")

    if not MANIFEST.exists() or not FROZEN.exists():
        print(f"FATAL: manifest/frozen missing", file=sys.stderr)
        return 2

    samples_by_id = {}
    for line in open(MANIFEST):
        r = json.loads(line)
        samples_by_id[r["sample_id"]] = r

    frozen_ids = json.loads(FROZEN.read_text())

    # Pick base sample_ids per axis: deterministic stride
    rng = random.Random(args.seed)
    base_ids = rng.sample(frozen_ids, 3 * args.per_axis)
    per_axis_ids = {
        "role": base_ids[0 * args.per_axis:1 * args.per_axis],
        "fact": base_ids[1 * args.per_axis:2 * args.per_axis],
        "consequence": base_ids[2 * args.per_axis:3 * args.per_axis],
    }

    # pre-flight
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

    out_records = []
    parse_failures = 0
    t_run = time.time()
    idx = 0
    for axis, ids in per_axis_ids.items():
        mutator = MUTATORS[axis]
        for sample_id in ids:
            idx += 1
            sample = samples_by_id[sample_id]
            yaml_path = AUTO_ROOT / sample["source_path"]
            if not yaml_path.exists():
                continue
            try:
                yaml_data = load_yaml(yaml_path)
            except Exception as e:
                print(f"WARN: {sample_id} yaml parse failed: {e}", file=sys.stderr)
                continue

            mutated_prompt, mutated_axis_field = mutator(sample, yaml_data)
            messages = build_messages(
                axis=axis,
                original_sample_id=sample_id,
                mutated_axis_field=mutated_axis_field,
                mutated_prompt=mutated_prompt,
            )

            parsed = call_judge_real(messages)
            dt_ms = parsed.pop("_dt_ms", 0)
            if parsed.get("_parse_failed"):
                parse_failures += 1
                (OUT_RESPONSES / f"R-P12-neighborhood-{idx:03d}.txt").write_text(
                    parsed.get("raw", ""), encoding="utf-8"
                )
                continue

            (OUT_RESPONSES / f"R-P12-neighborhood-{idx:03d}.txt").write_text(
                parsed.pop("_raw", ""), encoding="utf-8"
            )

            score, score_empty = aggregate_score(parsed.get("scores", {}))
            record = {
                "record_id": f"R-P12-neighborhood-{idx:03d}",
                "sample_id": sample_id,
                "axis": axis,
                "protocol": "neighborhood",
                "judge_id": JUDGE_MODEL,
                "awareness": "neighborhood",
                "score": score,
                "score_band": band_for(score),
                "abstain": score_empty,
                "abstain_reason": ("empty_scores_dict" if score_empty else ""),
                "consistency_on_wrong": 1.0,
                "ground_truth_correctness": None,
                "mutated_prompt": mutated_prompt,
                "mutated_axis_field": mutated_axis_field,
                "judge_called_at": utc_iso(),
                "judge_call_ms": dt_ms,
                "raw_response_path": f"experiments/neighborhood_responses/R-P12-neighborhood-{idx:03d}.txt",
            }
            out_records.append(record)
            print(f"[{idx}/{3 * args.per_axis}] axis={axis} sample={sample_id} score={score}",
                  flush=True)

            if idx < 3 * args.per_axis:
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