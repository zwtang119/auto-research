#!/usr/bin/env python3
"""Direction A mechanism experiment — execution runner.

Reads cells.jsonl, calls each judge with the (anchor, domain) prompt,
parses JSON, persists raw + structured outputs.

Provider / model_id mapping (locked for reproducibility):
  - open_source_mid  → qwen3.5-122b-a10b  (paratera)
  - closed_source_mid → MiniMax-M3        (minimaxi)
  - openrouter_mid    → openai/gpt-oss-120b:free (openrouter)

Outputs:
  - raw/<cell_id>__<sample_id>.json : one per call, raw + parsed
  - results/all_calls.jsonl         : flat record stream for analysis
  - results/<cell_id>.json          : per-cell aggregate
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path
from typing import Optional

EXPERIMENT_ROOT = Path("/Users/tangzw119/Documents/GitHub/auto-research/docs/papers-closed-portfolio/experiments/direction_a")
CELLS_PATH = EXPERIMENT_ROOT / "cells.jsonl"
SAMPLE_POOL_PATH = EXPERIMENT_ROOT / "sample_pool.json"
P12_OUTPUTS_PATH = EXPERIMENT_ROOT / "p12_outputs.json"
CDS_OUTPUTS_PATH = EXPERIMENT_ROOT / "cds_outputs.json"
RAW_DIR = EXPERIMENT_ROOT / "raw"
RESULTS_DIR = EXPERIMENT_ROOT / "results"

# Vendored
AUTO_ROOT = Path("/Users/tangzw119/Documents/GitHub/auto-research")
POLICYSIM_SCRIPTS = AUTO_ROOT / "framework" / "vendor" / "policysim_scripts"
POLICYSIM_CONFIG = AUTO_ROOT / "framework" / "vendor" / "policysim_config" / "experiment-config.yaml"


def _load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


_load_env_file(AUTO_ROOT / ".env")


def utc_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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


def aggregate_score(scores: dict) -> tuple[float, bool]:
    vals = [v for v in (scores or {}).values() if isinstance(v, (int, float))]
    if not vals:
        return 0.0, True
    return round(sum(vals) / len(vals), 4), False


def build_user_prompt(domain_id: str, anchor_id: str, agent_output: str,
                      sample_id: str, anchor_fillers: dict) -> str:
    """Rebuild the prompt for one (domain, anchor, sample)."""
    # Mirror the build_cells.py logic (kept local to avoid cross-import).
    filler = anchor_fillers.get(f"{domain_id}|{anchor_id}", {}).get(sample_id)
    if filler is None:
        filler = anchor_fillers.get(f"{domain_id}|{anchor_id}", {}).get("default_filler", "")
        # For cds4worldcup, default_filler may still be per-sample; fall through.
        if filler == "":
            if anchor_id == "leaked_gt":
                filler = f"the original condition was: {sample_id}"
            elif anchor_id == "score_tagged_ref":
                filler = "3.5 (mid-range)"
            elif anchor_id == "confidence_cue":
                filler = "70"
            else:
                filler = ""

    if anchor_id == "leaked_gt":
        anchor_block = f"\n## Anchor (CONTRAST condition): leaked ground truth\nThe producer's correct outcome is: {filler}\nTreat this as reference information. This is the 'leaked' variant.\n"
    elif anchor_id == "score_tagged_ref":
        anchor_block = f"\n## Anchor (ASSIMILATION condition): score-tagged reference\nA separate rater has scored this output as: {filler}\nThis is a reference rating, not ground truth.\n"
    elif anchor_id == "confidence_cue":
        anchor_block = f"\n## Anchor (INSUFFICIENT-ADJUSTMENT condition): confidence cue only\nThe producer reported its own confidence as: {filler}%\n(no answer, no score)\n"
    else:  # no_anchor
        anchor_block = "\n## Anchor: NONE (control)\nNo additional anchor information.\n"

    rubric = """
## Scoring dimensions (1.0-5.0)
1. risk_tolerance_consistency
2. innovation_focus_consistency
3. compliance_culture_consistency
4. market_influence_consistency
5. agility_score_consistency

## Output format (strict JSON, no extra text)
```json
{
  "scores": {
    "risk_tolerance_consistency": <float>,
    "innovation_focus_consistency": <float>,
    "compliance_culture_consistency": <float>,
    "market_influence_consistency": <float>,
    "agility_score_consistency": <float>
  },
  "anchor_acknowledged": "<leaked_gt|score_tagged_ref|confidence_cue|none>"
}
```
Emit ONLY the JSON.
"""

    return (
        "You are an LLM judge scoring a role-conditioned policy simulation output "
        "for character-consistency.\n\n"
        f"## Agent output (to be scored)\n{agent_output}\n"
        + anchor_block + rubric
    )


def call_judge(model_id: str, prompt: str, temperature: float = 0.2,
               max_tokens: int = 1024) -> dict:
    sys.path.insert(0, str(POLICYSIM_SCRIPTS))
    from api_client import load_config, call_model_json
    config = load_config(str(POLICYSIM_CONFIG))
    messages = [{"role": "user", "content": prompt}]
    t0 = time.time()
    try:
        content = call_model_json(
            config, model_id, messages,
            temperature=temperature,
            max_tokens=max_tokens,
            prompt_stage="direction_a_mechanism",
        )
        dt_ms = int((time.time() - t0) * 1000)
        parsed = parse_judge_response(content)
        if parsed is None:
            return {"_parse_failed": True, "raw": content, "dt_ms": dt_ms}
        parsed["_dt_ms"] = dt_ms
        parsed["_raw"] = content
        return parsed
    except Exception as e:
        dt_ms = int((time.time() - t0) * 1000)
        return {"_error": str(e), "_dt_ms": dt_ms}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="synthetic scoring; no API calls (deterministic per cell)")
    ap.add_argument("--limit-cells", type=int, default=0,
                    help="if > 0, only run the first N cells")
    ap.add_argument("--provider", default="all",
                    choices=["all", "paratera", "minimaxi", "openrouter"],
                    help="restrict to one provider (provider consistency)")
    ap.add_argument("--sleep", type=float, default=0.3,
                    help="seconds between calls (rate-limit cushion)")
    ap.add_argument("--out-suffix", default="",
                    help="append suffix to all_calls filename (e.g. '_real' to avoid clobbering dry-run)")
    args = ap.parse_args()

    suffix = args.out_suffix
    raw_dir = RAW_DIR if not suffix else RAW_DIR / suffix.lstrip("_")
    raw_dir.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Load cells
    cells = [json.loads(l) for l in CELLS_PATH.read_text().splitlines() if l.strip()]
    if args.limit_cells > 0:
        cells = cells[:args.limit_cells]

    # Provider filter
    if args.provider != "all":
        cells = [c for c in cells if c["judge_provider"] == args.provider]

    # Load outputs
    p12_outputs = json.loads(P12_OUTPUTS_PATH.read_text())
    cds_outputs = json.loads(CDS_OUTPUTS_PATH.read_text())
    sample_pool_data = json.loads(SAMPLE_POOL_PATH.read_text())
    anchor_fillers = sample_pool_data["anchor_fillers"]

    # Flat all-calls stream (append-only)
    suffix = args.out_suffix
    all_calls_path = RESULTS_DIR / f"all_calls{suffix}.jsonl"
    if all_calls_path.exists():
        # Resume: skip already-done (cell_id, sample_id) pairs
        done = set()
        for line in all_calls_path.read_text().splitlines():
            try:
                r = json.loads(line)
                done.add((r["cell_id"], r["sample_id"]))
            except json.JSONDecodeError:
                continue
    else:
        done = set()

    print(f"Loaded {len(cells)} cells. Already-done: {len(done)}.")
    t_run = time.time()
    parse_failures = 0
    total_calls = 0
    successful_calls = 0

    for cell_idx, cell in enumerate(cells, start=1):
        domain_id = cell["domain_id"]
        anchor_id = cell["anchor_id"]
        model_id = cell["judge_model_id"]
        sample_ids = cell["sample_ids"]
        cell_id = cell["cell_id"]

        for sample_id in sample_ids:
            if (cell_id, sample_id) in done:
                continue
            total_calls += 1

            # Pick the agent_output
            if domain_id == "gulei":
                agent_output = p12_outputs.get(sample_id, "")
            else:
                agent_output = cds_outputs.get(sample_id, "")

            prompt = build_user_prompt(
                domain_id, anchor_id, agent_output, sample_id, anchor_fillers
            )

            # Persist the prompt for audit
            prompt_path = raw_dir / f"{cell_id}__{sample_id}__prompt.txt"
            prompt_path.write_text(prompt, encoding="utf-8")

            if args.dry_run:
                # Synthetic scoring: deterministic per (cell, sample, anchor).
                # Anchor effects: leaked_gt → -0.3 mean shift; score_tagged_ref → +0.2;
                # confidence_cue → small noise; no_anchor → 0.
                anchor_shift = {
                    "leaked_gt": -0.30,
                    "score_tagged_ref": +0.20,
                    "confidence_cue": -0.05,
                    "no_anchor": 0.0,
                }[anchor_id]
                # Base score: 3.0 + per-sample jitter
                h = abs(hash((cell_id, sample_id))) % 1000
                base_jitter = ((h / 1000.0) - 0.5) * 0.6  # ±0.3
                mean = 3.0 + anchor_shift + base_jitter
                # Per-dimension scores
                per_dim = {}
                for i, dim in enumerate([
                    "risk_tolerance_consistency",
                    "innovation_focus_consistency",
                    "compliance_culture_consistency",
                    "market_influence_consistency",
                    "agility_score_consistency",
                ]):
                    dim_jitter = ((abs(hash((cell_id, sample_id, dim))) % 1000) / 1000.0 - 0.5) * 0.4
                    per_dim[dim] = round(max(1.0, min(5.0, mean + dim_jitter)), 3)
                parsed = {
                    "scores": per_dim,
                    "anchor_acknowledged": anchor_id if anchor_id != "no_anchor" else "none",
                    "_dt_ms": 0,
                    "_raw": "(dry-run synthetic)",
                }
            else:
                parsed = call_judge(model_id, prompt)
                if parsed.get("_parse_failed") or parsed.get("_error"):
                    parse_failures += 1
                    # Still log the failed call
                    record = {
                        "cell_id": cell_id,
                        "sample_id": sample_id,
                        "domain_id": domain_id,
                        "anchor_id": anchor_id,
                        "judge_family_id": cell["judge_family_id"],
                        "judge_provider": cell["judge_provider"],
                        "judge_model_id": model_id,
                        "parse_ok": False,
                        "error": parsed.get("_error", ""),
                        "raw_excerpt": (parsed.get("raw", "") or "")[:200],
                        "judge_call_ms": parsed.get("_dt_ms", 0),
                        "judge_called_at": utc_iso(),
                    }
                    with all_calls_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    time.sleep(args.sleep)
                    continue

            score, score_empty = aggregate_score(parsed.get("scores", {}))
            record = {
                "cell_id": cell_id,
                "sample_id": sample_id,
                "domain_id": domain_id,
                "anchor_id": anchor_id,
                "judge_family_id": cell["judge_family_id"],
                "judge_provider": cell["judge_provider"],
                "judge_model_id": model_id,
                "parse_ok": True,
                "score": score,
                "abstain": score_empty,
                "per_dimension_scores": parsed.get("scores", {}),
                "anchor_acknowledged": parsed.get("anchor_acknowledged", "n/a"),
                "judge_call_ms": parsed.get("_dt_ms", 0),
                "judge_called_at": utc_iso(),
                "raw_path": f"raw/{cell_id}__{sample_id}.json",
            }
            # Save raw parsed
            (raw_dir / f"{cell_id}__{sample_id}.json").write_text(
                json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            with all_calls_path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            successful_calls += 1

            if total_calls % 10 == 0 or total_calls == 1:
                elapsed = time.time() - t_run
                rate = total_calls / elapsed if elapsed > 0 else 0
                eta_min = (sum(len(c["sample_ids"]) for c in cells) - total_calls) / max(rate, 0.01) / 60
                print(f"[{total_calls}] elapsed={elapsed:.1f}s rate={rate:.2f}/s "
                      f"parse_failures={parse_failures} ETA={eta_min:.1f}min",
                      flush=True)

            if not args.dry_run:
                time.sleep(args.sleep)

    print(f"\n=== DONE ===")
    print(f"Total calls attempted: {total_calls}")
    print(f"Successful parse: {successful_calls}")
    print(f"Parse failures: {parse_failures}")
    print(f"Wall time: {time.time() - t_run:.1f}s")
    print(f"Output: {all_calls_path}")
    return 0 if parse_failures / max(total_calls, 1) < 0.20 else 1


if __name__ == "__main__":
    sys.exit(main())