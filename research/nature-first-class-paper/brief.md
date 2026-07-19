# Research Brief: Nature-first-class-paper recalibration

## Refined question
Using the Nature Career "How to write a first-class paper" (Gewin 2018) methodology as an evaluative lens — distilled to 5 选题判据 — evaluate which paper-topic selection strategy the auto-research Topic-5 portfolio should adopt to maximize the odds of producing a first-class paper.

## The 5 选题判据 (from the article)
1. **Single-key-message test** (Mensh): Can the direction be expressed in one sentence = the title? If not, the topic is not focused.
2. **"What's new and compelling" red-thread test** (Murphy): Defensive/data-uniqueness-only framings fail; the answer must be a one-sentence methodological insight.
3. **Global-context + alternative-explanation test** (Borja + Gorsuch): Novelty must be defensible against existing literature; alternative explanations pre-examined.
4. **Human-storytelling + cross-audience clarity test** (Doubleday + Konkiel): Must be stateable to non-specialists; spans citations beyond home subfield.
5. **Reproducibility test** (Gorsuch): No missing methodology → not a dead end.

## Portfolio context (to be verified against arXiv/publisher, not 自媒体)
- **P1+P2 Evidence RAG + Factor Ledger** — ACTIVE mainline. M1 factor ledger schema + M2 settlement mapping (30 claims, Brier via P8). Methodology angle: dual-ledger crosswalk + orthogonal enums + Brier replay for settlement calibration. Scenario: Gulei 2015 petrochemical incident.
- **P8 Market Calibration**: repositioned as P1+P2's external settlement layer (Brier/Log Loss). M1.5 calc_brier.py done.
- **P7 Signal Fusion**: demoted to evidence input layer.
- **P12 Judge Calibration**: CLOSED (blind judge scores HIGHER than leaked — opposite of leakage hypothesis; folded into P1+P2).
- **P11 Inner Monologue**: closed, reused as scenario data.
- **Direction X (harness methodology standalone)**: CLOSED — slot occupied (DeepSeek Harness team 2026-05, Stanford Meta-Harness 2026-03-31, Chinese AHE paper 2026-04, 62-page Harness Engineering survey 2026-05).
- **Direction Y (harness validation benchmark, NeurIPS D&B)**: DOWNGRADED — "boring" pushback; data-uniqueness reads as publication gaming; needs methodological re-frame.
- **Direction Z (G3 + Harness-Evolution Combined, ACL/EMNLP Findings 2027)**: PRIMARY but GATED — G3 dual-ledger crosswalk 92.9% + Brier replay 100% IS methodological (reconciliation methodology), but gated on user confirmation.

## Hard constraints (from project MEMORY.md)
- **D17**: After user "boring" pushback on a paper direction, do NOT (a) defend, (b) restate with new framing, (c) propose 3-5 NEW directions as a defensive gesture. Recommendations must be GATED on user-supplied criteria.
- **"Data-uniqueness ≠ paper-interesting"**: A paper whose novel-point collapses if the data-uniqueness claim is removed is data-driven gaming, not method-driven insight.
- **Slot-occupancy 2-layer check**: any "should we pursue X" must complete (Layer A) arXiv + GitHub + major labs search + (Layer B) 自媒体 fact-verification.
- **Toutiao/WeChat fact-verification**: 自媒体 numbers/titles MUST be marked ⚠️ UNVERIFIED until confirmed by arXiv/publisher/direct x.com URL.

## Angles (Phase 2 decomposition)
- **A1**: Scorecard — apply each 选题判据 from Nature article to {P1+P2, Direction Y reformulated, Direction Z} → per-direction-per-判据 scorecard. (reasoning over the existing portfolio context + article text)
- **A2**: Recent 2024–2026 first-class papers in adjacent spaces (LLM agent harness methodology, prediction-market calibration, evidence-ledger / RAG for settlement, dual-ledger reconciliation) that succeeded with a *methodological* framing (NOT data-uniqueness) — cite arXiv ID + venue + first author + one-sentence key message.
- **A3**: Novelty of G3 dual-ledger crosswalk + Brier replay reconciliation relative to 2024–2026 prior art in calibration / ledger reconciliation — what's the closest prior art, does G3 clear the red-thread test.
- **A4**: Failure-mode signature of rejected "data-uniqueness-as-novelty" papers — articulate the methodological-insight test precisely enough to apply to P1+P2 and Direction Y reformulation; what does a reviewer's reject letter look like.
- **A5**: Adversarial sanity check — verify Direction X is actually CLOSED (re-confirm Stanford Meta-Harness, DeepSeek Harness team, Chinese AHE paper, 62-page Harness Engineering survey are real and slot-occupying) and that re-opening it would be re-treading.

## Depth mode
- **standard** — 5 angles, 0 follow-up rounds by default (research phase 1 in single parallel block, optional reflection).

## Today's date
- 2026-07-16
