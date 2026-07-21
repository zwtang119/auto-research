#!/usr/bin/env python3
"""Direction A 5-persona review runner.

Reads:
  - docs/papers/direction-a-1-page-proposal.md
  - docs/investigations/novelty-depth-check-2026-07-05.md
  - docs/investigations/llm-intelligence-blocker-verdict-2026-07-05-zh.md

Calls 5 distinct reviewers via Paratera (PIT-107 compliance) + 1 cross-validation
reviewer on minimaxi (per the canonical pattern from prior reviews).

Hard gate: median score >= 5.5 → Direction A proceeds.
             < 5.5              → fold into G3 methods paper.

Reviewers (canonical, matching prior P12 M8 + G1 reviews):
  R1 experimentalist → deepseek-v4-pro    (methodology rigor)
  R2 theorist        → kimi-k2.5          (conceptual contribution)
  R3 applied         → MiniMax-M3         (practical usefulness)
  R4 skeptical       → deepseek-v4-flash  (false-positive hunting)
  R5 systems         → qwen3.5-122b-a10b  (engineering quality)

Cross-validation:
  R6 cross           → minimaxi/MiniMax-M3  (distinct provider)
"""
from __future__ import annotations
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

AUTO_ROOT = Path("/Users/tangzw119/Documents/GitHub/auto-research")
POLICYSIM_SCRIPTS = AUTO_ROOT / "framework" / "vendor" / "policysim_scripts"
POLICYSIM_CONFIG = AUTO_ROOT / "framework" / "vendor" / "policysim_config" / "experiment-config.yaml"

PROPOSAL_PATH = AUTO_ROOT / "docs" / "papers" / "direction-a-1-page-proposal.md"
SPEC_PATH = AUTO_ROOT / "docs" / "papers" / "direction-a-mechanism-experiment-spec.md"
NOVELTY_PATH = AUTO_ROOT / "docs" / "investigations" / "novelty-depth-check-2026-07-05.md"
BLOCKER_PATH = AUTO_ROOT / "docs" / "investigations" / "llm-intelligence-blocker-verdict-2026-07-05-zh.md"

OUT_RESULTS_JSON = AUTO_ROOT / "docs" / "papers" / "experiments" / "direction_a" / "results" / "review_round_1.json"
OUT_RESULTS_MD = AUTO_ROOT / "docs" / "papers" / "direction-a-review-round-1.md"

REVIEWERS = [
    ("R1 experimentalist (methodology rigor)", "deepseek-v4-pro",
     "You are R1, an experimentalist. Score methodology rigor: is the cell design (4 anchors × 3 judges × 2 domains × N=30) adequate? Is the pre-registered analysis plan (OLS with anchor + sample fixed effects) sufficient? Are the confounds (parse failures, provider severity offset, domain-specific anchor meaning) properly addressed? Is the G2 N=30 falsification acknowledgment honest?"),
    ("R2 theorist (conceptual contribution)", "kimi-k2.5",
     "You are R2, a theorist. Score conceptual contribution: is the Tversky-Kahneman anchoring-and-adjustment framework genuinely novel given CoBBLEr (Koo et al. arXiv:2309.17012)? Does the 3-axis taxonomy (CONTRAST/ASSIMILATION/INSUFFICIENT-ADJUSTMENT) make testable predictions? Is the sign-asymmetry prediction (Δ_contrast < 0, Δ_assimilation > 0) falsifiable?"),
    ("R3 applied (practical usefulness)", "MiniMax-M3",
     "You are R3, an applied researcher. Score practical usefulness: would an LLM-judge practitioner find the 3-axis anchoring taxonomy actionable? Are the 4 anchor types (leaked-GT / score-tagged-ref / confidence-cue / no-anchor) realistic in real evaluation pipelines? Does the framework survive the G2 N=30 falsification (which showed the contrast effect is smaller than N=6 suggested)?"),
    ("R4 skeptical (false-positive hunting)", "deepseek-v4-flash",
     "You are R4, a skeptical reviewer. Hunt for false positives: is the CONTRAST/ASSIMILATION distinction theoretically clean? Could the leaked-GT anchor manipulation be confounded with the prompt-formatting change (not the content)? Is the cds4worldcup domain (only 2 settlements) credible evidence for cross-domain generalization? Could CoBBLEr's 6 cognitive biases be reframed post-hoc to subsume anchoring effects?"),
    ("R5 systems (engineering quality)", "kimi-k2.6",
     "You are R5, a systems reviewer. Score engineering quality: is the 24-cell × 30-sample × 4-anchor design reproducible? Are the prompts (in build_cells.py) well-isolated between conditions? Are the parse-failure / rate-limit / 429 mitigation strategies adequate? Is the pre-registration lock (spec §3.3) actually enforceable?"),
]

CROSS_REVIEWER = ("R6 cross (minimaxi provider replication)", "MiniMax-M3",
                   "You are R6, a cross-validation reviewer on a different provider (minimaxi). Repeat R1+R5 in one score: methodology rigor + engineering quality. If your score differs by > 1.0 from the paratera median, flag this as cross-provider deviation.")


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


def parse_score_and_weakness(text: str) -> tuple[float | None, str]:
    m = re.search(r"\{[^{}]*\"score\"\s*:\s*([0-9.]+)[^{}]*\"weakness\"\s*:\s*\"([^\"]*)\"[^{}]*\}", text)
    if m:
        return float(m.group(1)), m.group(2)
    m = re.search(r"SCORE:\s*([0-9.]+)", text)
    w_match = re.search(r"WEAKNESS:\s*(.+)", text, re.DOTALL)
    if m:
        return float(m.group(1)), (w_match.group(1).strip() if w_match else "(none)")
    return None, "(unparseable response)"


def build_prompt(persona_flavor: str, proposal: str, spec: str, novelty: str) -> str:
    # Cap each section to avoid token blowup
    return f"""You are reviewing a paper draft for a workshop / findings-track submission.

# Paper claim (Direction A)
The paper proposes a Unified Anchoring-Bias Taxonomy for LLM-as-a-Judge, grounded in
Tversky-Kahneman (1974) anchoring-and-adjustment theory:
  - CONTRAST effect: leaked ground truth → stricter scoring
  - ASSIMILATION effect: score-tagged reference → lenient scoring
  - INSUFFICIENT-ADJUSTMENT effect: confidence cue → asymmetric adjustment

The framework is validated by a 4 anchor × 3 judge × 2 domain × N=30 mechanism experiment
with a pre-registered OLS regression.

# 1-page proposal (excerpt)
```markdown
{proposal[:5500]}
```

# Mechanism experiment spec (excerpt)
```markdown
{spec[:3500]}
```

# Novelty depth-check summary (excerpt)
```markdown
{novelty[:4000]}
```

# Your persona
{persona_flavor}

# Your task
Return ONLY this JSON (no markdown, no other text):
{{"score": <integer 1-7>, "weakness": "<one sentence, 10-30 words>"}}

Score 1-7 per project anti-inflation cap (first round ≤ 7.0).
Hard gate: median ≥ 5.5 → proceeds to full paper. Median < 5.5 → fold into G3 methods paper.
"""


def call_judge(model_id: str, prompt: str) -> dict:
    sys.path.insert(0, str(POLICYSIM_SCRIPTS))
    from api_client import load_config, call_model
    config = load_config(str(POLICYSIM_CONFIG))
    messages = [{"role": "user", "content": prompt}]
    t0 = time.time()
    try:
        content, _usage = call_model(
            config, model_id, messages,
            temperature=0.3,
            max_tokens=1024,
            prompt_stage="direction_a_review",
        )
        dt = time.time() - t0
        score, weakness = parse_score_and_weakness(content)
        return {
            "model_id": model_id,
            "ok": True,
            "score": score,
            "weakness": weakness,
            "raw_response_preview": content[:300],
            "elapsed_s": round(dt, 2),
            "completion_tokens": len(content),
        }
    except Exception as e:
        return {"model_id": model_id, "ok": False, "error": str(e), "elapsed_s": time.time() - t0}


def main() -> int:
    if not PROPOSAL_PATH.exists():
        print(f"FATAL: {PROPOSAL_PATH} missing", file=sys.stderr)
        return 2
    if not NOVELTY_PATH.exists():
        print(f"FATAL: {NOVELTY_PATH} missing", file=sys.stderr)
        return 2

    proposal = PROPOSAL_PATH.read_text()
    spec = SPEC_PATH.read_text() if SPEC_PATH.exists() else "(spec not yet written)"
    novelty = NOVELTY_PATH.read_text()

    OUT_RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)

    results = []
    for persona_label, model_id, flavor in REVIEWERS:
        print(f"Calling {persona_label} ({model_id})...", flush=True)
        prompt = build_prompt(flavor, proposal, spec, novelty)
        result = call_judge(model_id, prompt)
        result["persona"] = persona_label
        results.append(result)
        score_str = f"{result['score']}" if result.get('score') is not None else 'N/A'
        print(f"  → score={score_str} ({result.get('elapsed_s', 0):.1f}s) ok={result['ok']}")

    # Cross-validation reviewer (R6)
    persona_label, model_id, flavor = CROSS_REVIEWER
    print(f"Calling {persona_label} ({model_id})...", flush=True)
    prompt = build_prompt(flavor, proposal, spec, novelty)
    result = call_judge(model_id, prompt)
    result["persona"] = persona_label
    results.append(result)
    score_str = f"{result['score']}" if result.get('score') is not None else 'N/A'
    print(f"  → score={score_str} ({result.get('elapsed_s', 0):.1f}s) ok={result['ok']}")

    # Persist
    OUT_RESULTS_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2))

    # Compute median + verdict
    scores_r1_r5 = [r["score"] for r in results[:5] if r.get("score") is not None]
    median_5 = statistics.median(scores_r1_r5) if scores_r1_r5 else None
    cross_score = results[5].get("score") if len(results) > 5 else None
    cross_deviation = None
    if cross_score is not None and median_5 is not None:
        cross_deviation = round(cross_score - median_5, 2)

    decision = "PROCEED (median >= 5.5)" if median_5 and median_5 >= 5.5 else "FOLD (median < 5.5)"

    md_lines = [
        "# Direction A — 5-Persona Review Round 1 (2026-07-05)\n",
        f"_Source: docs/papers/direction-a-1-page-proposal.md (67 lines, CoBBLEr 3-axis differentiation in §3)_\n",
        "_Reviewers: 5 paratera (PIT-107) + 1 minimaxi cross-validation_\n",
        f"\n## Results\n",
        "| Persona | Model | Score | Weakness |",
        "|---------|-------|-------|----------|",
    ]
    for r in results:
        score = r.get('score', 'N/A')
        weakness = r.get('weakness', r.get('error', 'N/A'))[:80]
        md_lines.append(f"| {r['persona']} | {r['model_id']} | {score} | {weakness} |")

    md_lines.append(f"\n## Aggregate\n")
    md_lines.append(f"- R1-R5 median: **{median_5}**")
    md_lines.append(f"- R6 cross-validation (minimaxi): {cross_score} (deviation from paratera median: {cross_deviation})")
    md_lines.append(f"\n## Verdict\n")
    md_lines.append(f"**{decision}**\n")

    if median_5 and median_5 >= 5.5:
        md_lines.append("\nDirection A **proceeds** to mechanism experiment execution. The 24-cell × N=30 × 4-anchor design is authorized.\n")
    else:
        md_lines.append("\nDirection A **folds** into a methods paper. Pivot target: G3 dual-ledger bridge (`docs/papers/direction-a-mechanism-experiment-spec.md` §7).\n")

    OUT_RESULTS_MD.write_text("\n".join(md_lines))

    print(f"\n=== AGGREGATE ===")
    print(f"R1-R5 median: {median_5}")
    print(f"R6 cross-validation: {cross_score}")
    print(f"DECISION: {decision}")
    print(f"\nWrote {OUT_RESULTS_JSON}")
    print(f"Wrote {OUT_RESULTS_MD}")

    return 0 if median_5 and median_5 >= 5.5 else 1


if __name__ == "__main__":
    sys.exit(main())