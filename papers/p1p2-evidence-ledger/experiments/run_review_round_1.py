#!/usr/bin/env python3
"""P1+P2 M9 — Five-persona review runner.

Reuses the P12 review-runner pattern (5 distinct model_ids via Paratera,
PIT-107 compliance). Reads P1+P2 artefacts (pilot_30.jsonl,
pilot_power.md, baseline_design.md, blocked.md) and asks 5 distinct
reviewers for a score in [1.0, 7.0] plus binding weakness.

Per task_spec §6: median >= 6.5 → continue; otherwise fold into P12.
Per roadmap §11 anti-inflation: first round <= 7.0; +1.5 max per round.
"""
from __future__ import annotations
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P12_ROOT / "experiments"
PAPER = P12_ROOT / "paper"
OUT_REVIEW_MD = PAPER / "review_round_1.md"
OUT_RESULTS = EXPERIMENTS / "review_round_1_results.json"

# 5 distinct model_ids (PIT-107) — all via PARATERA_API_KEY
REVIEWERS = [
    ("R1 experimentalist (methodology rigor)", "deepseek-v4-pro",
     "You are R1, an experimentalist. Score methodology rigor: pre-registration, control conditions, sample size relative to claim strength, statistical test choice. The M3 power analysis found n=30 pilot underpowered (0.48 at d=0.5). M4 pivoted to factor-type-conditional claim. Is this pivot honest, or post-hoc? Are the 6 PIT invariants enforced by the validator robust? Is the unit-test coverage sufficient?"),
    ("R2 theorist (conceptual contribution)", "kimi-k2.5",
     "You are R2, a theorist. Score conceptual contribution: does the 14-field evidence_ledger_entry schema (PIT-201..PIT-206) advance beyond free-text reasoning traces? Is the factor-type taxonomy (precedent/inhibitor/branch/falsifier/authority) theoretically grounded, or ad-hoc? Does the cross-paper bridge to P12 5-protocol design add value, or is it cargo-cult?"),
    ("R3 applied (practical usefulness)", "MiniMax-M3",
     "You are R3, an applied researcher. Score practical usefulness: would a practitioner actually use an evidence_ledger_entry over free-text? Is the 28/30 settleable rate (un_settleable_ratio=0.07) realistic or did we cherry-pick? Does the Gulei 2015 case study generalize, or is it single-incident overfit?"),
    ("R4 skeptical (false-positive hunting)", "deepseek-v4-flash",
     "You are R4, a skeptical reviewer. Hunt for false positives: the M3 power analysis shows pilot_30 is underpowered. Does the M4 pivot to 'factor-type-conditional effect' merely restate known variance, or is there a real signal? The authority factor shows +0.39 confidence delta on n=5 — is that stable, or one lucky entry (C-P1P2-005)? The branch/precedent factors show NEGATIVE delta — is the ledger actively harmful there?"),
    ("R5 systems (engineering quality)", "qwen3.5-122b-a10b",
     "You are R5, a systems reviewer. Score engineering quality: pipeline scripts (build_pilot_10, build_pilot_30, validate_ledger, assemble_partial_runs), manifest validators, unit tests (10/10), schema enforcement, reproducibility. Is the validator's invariant check sufficient, or does it miss subtle bugs (e.g., the build_pilot_10 PIT-201 row-5 violation that initially slipped through)?"),
]

VENDOR_ROOT = P12_ROOT.parent.parent / "framework" / "vendor"
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
    return f"""You are reviewing a paper draft for P1+P2 (Evidence Ledger) mainline.

# Paper claim (post-M4 structural pivot)
The paper claims the evidence_ledger_entry (14-field schema with 6 PIT invariants) has a FACTOR-TYPE-CONDITIONAL effect on agent decision quality:
- Positive on `authority` and `falsifier` factors
- Neutral-to-negative on `branch` and `precedent` factors
- M3 power analysis found pilot_30 (n=30) underpowered for a uniform-positive claim (0.48 at d=0.5)
- M4 structural pivot: claim re-shaped, not prompt retuned (per task_spec §8 stale rule)

# Available artefacts (excerpt)
```markdown
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
    _load_env_file(P12_ROOT.parent.parent / ".env")

    artefacts_parts = []
    for path in [
        EXPERIMENTS / "ledger" / "pilot_30.jsonl",
        EXPERIMENTS / "pilot_power.md",
        EXPERIMENTS / "baseline_design.md",
        P12_ROOT / "state" / "blocked.md",
        P12_ROOT / "wiki" / "decisions" / "2026-07-04-m2-settlement-mapping.md",
    ]:
        if path.exists():
            artefacts_parts.append(f"=== {path.relative_to(P12_ROOT)} ===\n{path.read_text()[:3000]}")
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
                prompt_stage="p1p2_m9_review",
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
    lines.append("# P1+P2 Review Round 1 — Five-Persona Review")
    lines.append("")
    lines.append(f"> Generated {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} by `experiments/run_review_round_1.py`.")
    lines.append("> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.")
    lines.append("> Reviewing the **post-M4 structural-pivot** claim: factor-type-conditional effect.")
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
    lines.append("## 3. Verdict")
    lines.append("")
    if median_score is None:
        lines.append("- **Verdict**: `inconclusive` — all reviewers errored. Rerun after fixing API issues.")
    elif median_score >= 6.5:
        lines.append(f"- **Verdict**: `go_mainline` (median {median_score:.1f} >= 6.5)")
        lines.append("- Action: continue P1+P2 standalone; M5 main run worth authorizing.")
    else:
        lines.append(f"- **Verdict**: `fold_into_p12` (median {median_score:.1f} < 6.5)")
        lines.append("- Action: stop P1+P2 standalone paper. Carry 14-field evidence_ledger_entry + 5-protocol P12 design into a methods paper.")
    lines.append("")
    lines.append("## 4. Anti-inflation cap compliance (roadmap §11)")
    lines.append("")
    if max_score is not None and max_score <= 7.0:
        lines.append(f"- Max reviewer score = {max_score:.1f} ≤ 7.0 ✓")
    elif max_score is not None:
        lines.append(f"- **WARNING**: max reviewer score = {max_score:.1f} > 7.0. Cap violated; down-weight this round.")
    lines.append("")
    lines.append("## 5. `unresolved_weakness` (single most-cited)")
    lines.append("")
    if results:
        sorted_results = sorted(results, key=lambda r: r["score"] if r["score"] is not None else 99)
        if median_score is not None and median_score < 6.5:
            lines.append(f"> {sorted_results[0]['weakness']}  *(from {sorted_results[0]['model_id']}, score={sorted_results[0]['score']:.1f})*")
        else:
            lines.append(f"> {sorted_results[-1]['weakness']}  *(from {sorted_results[-1]['model_id']}, score={sorted_results[-1]['score']:.1f})*")
    lines.append("")
    lines.append("## 6. Calibration context (M3 power analysis)")
    lines.append("")
    lines.append("Per `experiments/pilot_power.md`:")
    lines.append("- pilot_30 n=30 yields power=0.48 at d=0.5 (underpowered for uniform-positive claim)")
    lines.append("- per-factor_type delta: authority +0.39 / falsifier +0.22 / branch -0.14 / precedent -0.13")
    lines.append("- M4 structural pivot: claim re-shaped to factor-type-conditional, NOT tactical reframe")
    lines.append("- required scale for d=0.5 detection: N=64/cell (~30 API hours)")
    lines.append("")
    lines.append("## 7. Required follow-up actions")
    lines.append("")
    if median_score is not None and median_score >= 6.5:
        lines.append("1. User authorizes M5 main run (N=64/cell, ~30 API hours)")
        lines.append("2. Run M5; M6 coverage audit; M7 settleability audit; M8 paper outline")
        lines.append("3. Schedule Day-14 5-persona review round 2")
    else:
        lines.append("1. Record verdict in `state/findings.jsonl` (level=decision, source=p1p2_m9_round_1)")
        lines.append("2. Update `state/progress.json`: status → `m9_close_no_mainline_paper`")
        lines.append("3. Carry 14-field evidence_ledger_entry + 5-protocol P12 design into a methods paper")
    lines.append("")

    OUT_REVIEW_MD.write_text("\n".join(lines))
    OUT_RESULTS.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\nWrote {OUT_REVIEW_MD}")
    print(f"Wrote {OUT_RESULTS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())