#!/usr/bin/env python3
"""P8 review_round_1 — 5-persona review of P8 M1.5 (calc_brier.py) standalone.

Reuses P12/P1+P2 review-runner pattern: 5 distinct Paratera model_ids
(PIT-107), anti-inflation cap (max ≤ 7.0), produces binary go/no-go.

P8 is NOT a paper project per task_spec — it's a methodology/scaffolding
component. So the review verdict is "is calc_brier.py + 17 unit tests
production-quality?" not "should this paper be published?".

If median < 5.0: calc_brier.py is research-grade, not production-grade;
defer to methods paper or tooling consolidation.
If median >= 5.0: calc_brier.py is reusable; promote to framework/.
"""
from __future__ import annotations
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

P8_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P8_ROOT / "experiments"
WIKI = P8_ROOT / "wiki"
OUT_REVIEW_MD = P8_ROOT / "paper" / "review_round_1.md"
OUT_RESULTS = EXPERIMENTS / "review_round_1_results.json"

REVIEWERS = [
    ("R1 experimentalist (methodology rigor)", "deepseek-v4-pro",
     "You are R1, an experimentalist. Score methodology rigor: is calc_brier.py the right API surface for Brier/Log Loss in the P1+P2 evidence-ledger pipeline? Does the aggregate_scores() portfolio-level summary handle missing-data correctly? Are 17 unit tests sufficient coverage of the Brier math edge cases (perfect prediction, p=0, p=1, multi-class)?"),
    ("R2 theorist (probabilistic-foundation correctness)", "kimi-k2.5",
     "You are R2, a theorist. Score probabilistic-foundation correctness: does compute_brier / compute_log_loss / compute_brier_multiclass correctly implement the standard definitions? Are the clipping (eps=1e-15) and length-mismatch checks correct? Does the 4-band factor_update heuristic (p≥0.7 + o=1 → supported) have a probabilistic justification, or is it an arbitrary cut?"),
    ("R3 applied (P1+P2 pipeline integration)", "MiniMax-M3",
     "You are R3, an applied researcher. Score P1+P2 pipeline integration: given that P1+P2 evidence_ledger_entry has settlement_rule and observed_outcome, can calc_brier.py consume these directly? Is the factor_update heuristic (p≥0.7 + o=1 → supported) a reasonable v0 default for P1+P2's M7 settleability audit, or does it bias the audit?"),
    ("R4 skeptical (data shape mismatch)", "deepseek-v4-flash",
     "You are R4, a skeptical reviewer. Hunt for false positives: the M1 attempt found that cds4polymarket's 17-round AB-test data is judge scores (discrete 1-5) not continuous prediction_p. Does this mean calc_brier.py cannot be USED on existing data, even though it's CORRECT in implementation? Is the 'Brier/Log Loss Python function does not exist' gap from task_spec §Known Gaps actually closed, or only the math?"),
    ("R5 systems (engineering quality)", "qwen3.5-122b-a10b",
     "You are R5, a systems reviewer. Score engineering quality: 262-line calc_brier.py with 17 unit tests, CLI subcommand, --workdir-like flags, --default-baseline option. Is the code production-grade, or research-grade? Is the build_settlement_record heuristic classification (p≥0.7 vs p≤0.3 bands) robust to noisy predictions? Are there missing edge cases in the multiclass compute?"),
]

VENDOR_ROOT = P8_ROOT.parent.parent / "framework" / "vendor"
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
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_score_and_weakness(text: str) -> tuple[float | None, str]:
    if text:
        m = re.search(r"\{[^{}]*\"score\"\s*:\s*([0-9.]+)[^{}]*\"weakness\"\s*:\s*\"([^\"]*)\"[^{}]*\}", text)
        if m:
            return float(m.group(1)), m.group(2)
        m = re.search(r"SCORE:\s*([0-9.]+)", text)
        w = re.search(r"WEAKNESS:\s*(.+)", text, re.DOTALL)
        if m:
            return float(m.group(1)), (w.group(1).strip() if w else "(none)")
    return None, "(unparseable)"


def build_prompt(persona_flavor: str, artefacts: str) -> str:
    return f"""You are reviewing the P8 M1.5 deliverable: `experiments/calc_brier.py`.

# Context
P8 = Prediction Markets as Calibration Field for LLM Agents.
P8 M1.5 = implement `calc_brier.py` (Python Brier/Log Loss calculator).
Per task_spec §Known Gaps, this gap was "Python auto-computation does not exist". calc_brier.py closes that gap.

# Artefacts (excerpt)
```python
{artefacts[:8000]}
```

# Your persona
{persona_flavor}

# Your task
Return ONLY this JSON (no markdown, no other text):
{{"score": <integer 1-7>, "weakness": "<one sentence, 10-30 words>"}}

Score 1-7 per roadmap §11 anti-inflation cap (first round ≤ 7.0).
"""


def main() -> int:
    _load_env_file(P8_ROOT.parent.parent / ".env")

    artefacts_parts = []
    for path in [
        EXPERIMENTS / "calc_brier.py",
        EXPERIMENTS / "test_calc_brier.py",
        P8_ROOT / "state" / "task_spec.md",
        WIKI / "concepts" / "brier-score.md",
        WIKI / "decisions" / "brier-implementation.md",
    ]:
        if path.exists():
            artefacts_parts.append(f"=== {path.relative_to(P8_ROOT)} ===\n{path.read_text()[:2500]}")
    artefacts = "\n\n".join(artefacts_parts)

    sys.path.insert(0, str(POLICYSIM_SCRIPTS))
    from api_client import load_config, call_model
    cfg = load_config(str(POLICYSIM_CONFIG))

    for _, model_id, _ in REVIEWERS:
        provider = cfg["models"][model_id]["provider"]
        api_key_env = cfg["api_endpoints"][provider]["api_key_env"]
        if not os.environ.get(api_key_env):
            print(f"FATAL: env ${api_key_env} not set for {model_id}", file=sys.stderr)
            return 2

    results = []
    for persona_label, model_id, flavor in REVIEWERS:
        prompt = build_prompt(flavor, artefacts)
        t0 = time.time()
        try:
            content, usage = call_model(
                cfg, model_id,
                [{"role": "user", "content": prompt}],
                temperature=0.3, max_tokens=2048,
                prompt_stage="p8_m15_review",
            )
            elapsed = time.time() - t0
            score, weakness = parse_score_and_weakness(content)
            results.append({
                "persona": persona_label, "model_id": model_id,
                "score": score, "weakness": weakness,
                "raw_response_preview": (content or "")[:300],
                "elapsed_s": round(elapsed, 1),
                "completion_tokens": (usage or {}).get("completion_tokens", 0),
                "ok": score is not None,
            })
            print(f"  {model_id:25s} -> score={score} ({elapsed:.1f}s)", flush=True)
        except Exception as e:
            elapsed = time.time() - t0
            results.append({
                "persona": persona_label, "model_id": model_id,
                "score": None, "weakness": f"(API error: {type(e).__name__}: {str(e)[:120]})",
                "raw_response_preview": "", "elapsed_s": round(elapsed, 1),
                "completion_tokens": 0, "ok": False,
            })
            print(f"  {model_id:25s} -> FAIL ({elapsed:.1f}s) {type(e).__name__}", flush=True)

    scores = [r["score"] for r in results if r["score"] is not None]
    median_score = statistics.median(scores) if scores else None
    max_score = max(scores) if scores else None

    lines = []
    lines.append("# P8 M1.5 Review Round 1 — Five-Persona Review")
    lines.append("")
    lines.append(f"> Generated {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} by `experiments/run_review_round_1.py`.")
    lines.append("> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.")
    lines.append("> Reviewing calc_brier.py (P8 M1.5) — methodology/scaffolding component, not a paper.")
    lines.append("")
    lines.append("## 1. Reviewer set")
    lines.append("")
    lines.append("| # | Persona | model_id | score | binding weakness |")
    lines.append("|---|---------|----------|-------|------------------|")
    for r in results:
        score_str = f"{r['score']:.1f}" if r['score'] is not None else "n/a"
        lines.append(f"| {r['persona'].split()[0]} | {r['persona']} | `{r['model_id']}` | "
                     f"{score_str} | {r['weakness']} |")
    lines.append("")
    lines.append("## 2. Aggregate")
    lines.append("")
    if scores:
        lines.append(f"- Median score across R1..R5: **{median_score:.1f}**")
        lines.append(f"- Mean score: {statistics.mean(scores):.2f}")
        lines.append(f"- Max score: {max_score:.1f}")
    else:
        lines.append("- All reviewers errored.")
    lines.append("")
    lines.append("## 3. Verdict (P8 is methodology/scaffolding, threshold = 5.0 not 6.5)")
    lines.append("")
    if median_score is None:
        lines.append("- **Verdict**: `inconclusive` — all reviewers errored.")
    elif median_score >= 6.0:
        lines.append(f"- **Verdict**: `production_grade` (median {median_score:.1f} >= 6.0)")
        lines.append("- Action: promote calc_brier.py to framework/ as reusable tool.")
    elif median_score >= 5.0:
        lines.append(f"- **Verdict**: `research_grade_acceptable` (5.0 <= median {median_score:.1f} < 6.0)")
        lines.append("- Action: keep as paper-scoped tool; document known limitations.")
    else:
        lines.append(f"- **Verdict**: `not_yet_acceptable` (median {median_score:.1f} < 5.0)")
        lines.append("- Action: revise factor_update heuristic; address data-shape blocker before M7 settleability audit can use this.")
    lines.append("")
    lines.append("## 4. Anti-inflation cap compliance (roadmap §11)")
    lines.append("")
    if max_score is not None and max_score <= 7.0:
        lines.append(f"- Max reviewer score = {max_score:.1f} ≤ 7.0 ✓")
    elif max_score is not None:
        lines.append(f"- **WARNING**: max reviewer score = {max_score:.1f} > 7.0. Cap violated.")
    lines.append("")
    lines.append("## 5. `unresolved_weakness` (single most-cited)")
    lines.append("")
    if results:
        sorted_results = sorted(results, key=lambda r: r["score"] if r["score"] is not None else 99)
        lines.append(f"> {sorted_results[0]['weakness']}  *(from {sorted_results[0]['model_id']}, score={sorted_results[0]['score']:.1f})*")
    lines.append("")
    lines.append("## 6. Calibration context (M1 data-shape finding)")
    lines.append("")
    lines.append("Per `state/findings.jsonl` 2026-07-04: M1 attempt to parse cds4polymarket")
    lines.append("ab-test/analysis/ab_test_17rounds_data.xlsx found 9 sheets containing")
    lines.append("judge scores (discrete 1-5) and winner labels — NOT continuous")
    lines.append("prediction_p in [0,1] needed by calc_brier.py. Brier computable;")
    lines.append("upstream data shape is wrong. P8 M1 stale_count += 1.")
    lines.append("")
    lines.append("## 7. Required follow-up actions")
    lines.append("")
    lines.append("1. Record verdict in `state/findings.jsonl` (level=decision, source=p8_m15_review_round_1)")
    lines.append("2. Update `state/progress.json` with M1.5 review verdict")
    lines.append("3. Promote calc_brier.py to framework/ if verdict >= production_grade")
    lines.append("")

    OUT_REVIEW_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_REVIEW_MD.write_text("\n".join(lines))
    OUT_RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {OUT_REVIEW_MD}")
    print(f"Wrote {OUT_RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())