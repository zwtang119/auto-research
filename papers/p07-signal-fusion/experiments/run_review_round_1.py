#!/usr/bin/env python3
"""P7 M1 review_round_1 — 5-persona review of P7 M1 (adapter_signal_to_ledger.py).

Per P7 layer-roles separation, P7 is the evidence input layer that
produces signal_evidence_entry rows translated into evidence_ledger_entry
supporting/contradicting refs. The review verdict decides whether the
adapter is reusable for P1+P2 M5 pilot run.
"""
from __future__ import annotations
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

P7_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P7_ROOT / "experiments"
OUT_REVIEW_MD = P7_ROOT / "paper" / "review_round_1.md"
OUT_RESULTS = EXPERIMENTS / "review_round_1_results.json"

REVIEWERS = [
    ("R1 experimentalist (methodology rigor)", "deepseek-v4-pro",
     "You are R1, an experimentalist. Score methodology rigor: does the adapter correctly translate 4 signal types (confirmed_fact / weak_evidence / missing_data / source_failure) into 2 buckets (supporting / contradicting) per data-contracts §8? Is the independence_class resolution (primary/secondary/tertiary) principled or arbitrary? Are the 12 unit tests sufficient coverage?"),
    ("R2 theorist (signal-theory correctness)", "kimi-k2.5",
     "You are R2, a theorist. Score signal-theory correctness: should missing_data be classified as contradicting (negative evidence of completeness) or as a separate gap? Is source_failure semantically distinct from missing_data in this 4-type taxonomy, or is it a duplicate?"),
    ("R3 applied (P1+P2 consumer-side integration)", "MiniMax-M3",
     "You are R3, an applied researcher. Score P1+P2 consumer-side integration: does the grouped_output format match what P1+P2's evidence_ledger_entry.supporting_evidence[] and contradicting_evidence[] fields expect? Are the snippet_summary fields informative enough for downstream audit?"),
    ("R4 skeptical (PIT-302 false-rejection rate)", "deepseek-v4-flash",
     "You are R4, a skeptical reviewer. Hunt for false positives: the PIT-302 rule rejects supporting signals without numeric_forecast. In a real Gulei pipeline, what fraction of supporting signals would lack numeric_forecast? Is the rejection heuristic too strict (over-rejecting useful evidence) or too loose?"),
    ("R5 systems (engineering quality)", "qwen3.5-122b-a10b",
     "You are R5, a systems reviewer. Score engineering quality: 200-line adapter with 12 unit tests, CLI subcommand with --scenario/--claim-id/--grouped-output flags, --workdir handling. Was the source_id double-prefix bug (SIG-SIG-... → SIG-...) a one-off typo, or a sign of weak input validation? Is the rejected-count semantics in the CLI output clear?"),
]

VENDOR_ROOT = P7_ROOT.parent.parent / "framework" / "vendor"
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
    return f"""You are reviewing the P7 M1 deliverable: `experiments/adapter_signal_to_ledger.py`.

# Context
P7 = Multi-Source Signal Fusion for Multi-Agent Decision Support.
P7 M1 = adapter from `signal_evidence_entry` (data-contracts §10) to
`evidence_ledger_entry.supporting_evidence[]` and `contradicting_evidence[]` arrays.
This is the layer-roles bridge: P7 producer → P1+P2 consumer.

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
    _load_env_file(P7_ROOT.parent.parent / ".env")

    artefacts_parts = []
    for path in [
        EXPERIMENTS / "adapter_signal_to_ledger.py",
        EXPERIMENTS / "test_adapter_signal_to_ledger.py",
        EXPERIMENTS / "sample_signals.jsonl",
        EXPERIMENTS / "sample_signals_grouped.json",
        P7_ROOT / "state" / "io_spec.md",
    ]:
        if path.exists():
            artefacts_parts.append(f"=== {path.relative_to(P7_ROOT)} ===\n{path.read_text()[:2500]}")
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
                prompt_stage="p7_m1_review",
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
    lines.append("# P7 M1 Review Round 1 — Five-Persona Review")
    lines.append("")
    lines.append(f"> Generated {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} by `experiments/run_review_round_1.py`.")
    lines.append("> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.")
    lines.append("> Reviewing adapter_signal_to_ledger.py (P7 M1) — layer-roles bridge, not a paper.")
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
    lines.append("## 3. Verdict (P7 is bridge tooling, threshold = 5.0 not 6.5)")
    lines.append("")
    if median_score is None:
        lines.append("- **Verdict**: `inconclusive` — all reviewers errored.")
    elif median_score >= 6.0:
        lines.append(f"- **Verdict**: `production_grade` (median {median_score:.1f} >= 6.0)")
        lines.append("- Action: promote adapter to framework/ as reusable layer-roles bridge.")
    elif median_score >= 5.0:
        lines.append(f"- **Verdict**: `research_grade_acceptable` (5.0 <= median {median_score:.1f} < 6.0)")
        lines.append("- Action: keep as paper-scoped bridge; document PIT-302 strictness; defer live integration until cds-keyperson import refactor.")
    else:
        lines.append(f"- **Verdict**: `not_yet_acceptable` (median {median_score:.1f} < 5.0)")
        lines.append("- Action: revise PIT-302 rule; consider relaxing to allow supporting-without-numeric in specific scenario contexts.")
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
    lines.append("## 6. Calibration context (M2 import-path finding)")
    lines.append("")
    lines.append("Per `state/findings.jsonl` 2026-07-04: M2 attempt to import live")
    lines.append("SignalFusionEngine from cds-keyperson failed with ModuleNotFoundError")
    lines.append("on `from src.backend...` internal imports. Adapter works on synthetic")
    lines.append("5-signal fixture (3 supporting + 2 contradicting) but live engine")
    lines.append("integration requires cds-keyperson cwd or relative-import refactor.")
    lines.append("P7 M2 stale_count += 1.")
    lines.append("")
    lines.append("## 7. Required follow-up actions")
    lines.append("")
    lines.append("1. Record verdict in `state/findings.jsonl` (level=decision, source=p7_m1_review_round_1)")
    lines.append("2. Update `state/progress.json` with M1 review verdict")
    lines.append("3. Promote adapter to framework/ if verdict >= production_grade")
    lines.append("")

    OUT_REVIEW_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_REVIEW_MD.write_text("\n".join(lines))
    OUT_RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {OUT_REVIEW_MD}")
    print(f"Wrote {OUT_RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())