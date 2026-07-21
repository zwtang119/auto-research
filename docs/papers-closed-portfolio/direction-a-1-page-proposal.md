# Direction A — 1-Page Proposal: A Unified Anchoring-Bias Taxonomy for LLM-as-a-Judge

> **Status**: draft for 5-persona review (NOT yet a paper)
> **Source**: derived from `docs/investigations/first-principles-top-journal-directions-2026-07-05.md` Rank 1 candidate direction + `novelty-depth-check-2026-07-05.md` (3 surveys + 8 method papers + CoBBLEr all checked; theoretical framework gap CONFIRMED; CoBBLEr identified as closest prior art with explicit 3-axis differentiation)
> **Hard gate before any large-token mechanism experiment**: 5-persona review median ≥ 5.5 + method-paper depth-check pass (8 papers COMPLETED 2026-07-05 晚, 0/8 use anchoring framing)
> **Author / Date**: 2026-07-05 (AutoResearch)
> **Target venues (post-honest-ceiling)**: ACL/EMNLP Findings 2027, EMNLP evaluation track, NeurIPS Datasets & Benchmarks — workshop/Findings baseline per `llm-intelligence-blocker-verdict-2026-07-05-zh.md`

---

## 1. Problem

LLM-as-a-judge bias research is data-rich but **theory-poor**: 3 surveys (`Gu et al. 2024 arXiv:2411.15594`, `Li D. et al. 2024 arXiv:2411.16594`, `Li H. et al. 2024 arXiv:2412.05579`) enumerate 7-15 named bias types each, with no shared theoretical lens. Gu et al. **explicitly call for "a more formal theoretical framework"** and "a unified and comprehensive benchmark" to quantify biases — i.e., the field has identified its own missing axis.

## 2. Proposed direction (Direction A)

**A unified anchoring-bias taxonomy for LLM-as-a-judge**, grounded in Tversky-Kahneman (1974) anchoring-and-adjustment theory. Concretely:

- **Contrast effect**: a high (or low) anchor in the judge prompt causes scoring to be **stricter (or more lenient)** than it would be in isolation. In our own project (P12 G2), the **"leaked ground truth" anchor caused the LLM judge to score STRICTER, not more lenient — opposite the conventional "label-leak bias inflates scores" expectation**. This is a CONTRAST effect: the judge adjusted insufficiently toward the high ground-truth anchor, leaving more room to penalize.
- **Assimilation effect**: a score-tagged reference answer (e.g., Li et al. 2026 arXiv:2506.22316 showed this anchors the judge toward the reference's score) causes the judge to **converge** to the reference. We map this to ASSIMILATION.
- **Adjustment effect** (Tversky-Kahneman's third core mechanism): judges **stop adjusting too early** when an anchor is given — explaining the well-known position bias, verbosity bias, self-preference bias, and "early stopping" of reasoning, all as instances of **insufficient anchor adjustment**.

The taxonomy is a **3-axis mapping** of 12+ LLM-judge bias types (from Li H. et al.'s "Cognitive-Related Biases" bucket) onto 3 anchoring mechanisms. This is the **first formal cognitive-bias framework for LLM-judge bias** — and the framework makes testable predictions (e.g., **assimilation vs contrast should have opposite sign** of bias; in our P12 data we observe strong contrast but weak assimilation).

## 3. Why this is novel

- **The 3 LLM-judge surveys** (checked via Google + Semantic Scholar deep search) do NOT use anchoring/contrast/assimilation/prospect-theory framing. Gu et al. explicitly asks for a theoretical framework.
- **CoBBLEr (Koo et al., arXiv:2309.17012, Sep 2023) — the closest prior art, requires explicit differentiation**:
  - CoBBLEr proposes a 6-cognitive-bias benchmark for LLM-as-evaluator (Egocentric, Position, Bandwagon, Authority, Sentiment, Confusion) — **descriptive taxonomy, no unifying theoretical mechanism**.
  - Direction A's 3-axis differentiators:
    1. **Theoretical grounding**: Tversky-Kahneman (1974) anchoring-and-adjustment theory — CoBBLEr has no unifying theory.
    2. **Mechanism experiment**: pre-registered sign-asymmetry test (Δ_contrast < 0 vs Δ_assimilation > 0) — CoBBLEr measures prevalence, not mechanism.
    3. **Specific anchor types**: leaked-GT (CONTRAST) + score-tagged-ref (ASSIMILATION) — neither is a CoBBLEr category.
- **8 method papers checked (KIEval, OffsetBias, CALM, JudgeDeceiver, Auto-J, CRITIC, JudgeLM, Prometheus-2)**: 0/8 use anchoring/contrast/assimilation framing. CALM (12 named biases) is the most enumerative, but orthogonal to anchoring. See `docs/investigations/novelty-depth-check-2026-07-05.md` Check 3 for the full 8-paper table.
- **External prior art (Li et al. 2026 arXiv:2506.22316)** documents the score-tagged-reference → lenient prior art. We map this onto ASSIMILATION. Their paper does NOT propose a unified taxonomy.

## 4. The mechanism experiment (preview — full spec below)

**Cell design**: 3-way factorial: anchor type × judge family × domain.

- **Anchor types (4)**: ground-truth-leaked / score-tagged-reference / confidence-cue-only / no-anchor (control).
- **Judge families (3)**: open-source (Qwen3.5-122B-A10B, DeepSeek-V4-Flash, MiniMax-M3) + mid-frontier (Claude-Sonnet-4) + frontier (GPT-5, Claude-Opus-4). Frontier per `llm-intelligence-blocker-verdict-2026-07-05-zh.md` §四 row 6 has concrete value for theoretical-grounding validation.
- **Domains (2)**: Gulei 2015 emergency + cds4worldcup match outcome (the latter is now a real external validation source per `rp-investigate-top-journal-2026-07-05.md` Finding 1, which corrected the "24 games" hallucination to 2 unique settlements).

**Per-cell N**: 30 paired samples (per `first-principles §17` G2 spec). Total cells: 4 × 3 × 2 × 2 (control) × 30 = ~1500 judge calls. With ~25s/call serial, ~10 hours wall time on Paratera. Frontier arm adds ~2 hours.

**Headline metrics**:
- Δ_assimilation − Δ_contrast (predicted sign asymmetry, falsifiable)
- per-domain preservation of contrast direction (Gulei shows contrast; cds4worldcup should too)
- cross-judge severity scaling (provider-dependent, per MEMORY.md "Reviewer calibration pattern — provider axis")

## 5. What this proposal does NOT claim

- It is NOT a novel LLM-judge benchmark or new model. It is a **theoretical framework** that explains existing and future biases.
- It is NOT a top-journal main-track claim per `llm-intelligence-blocker-verdict-2026-07-05-zh.md` — honest ceiling is workshop/Findings 6.5-7.0. Even with all gates passed, main-track requires scenario diversity + external validation + frontier baselines (per `post-gate-and-qlib-assessment-2026-07-05.md` §四).
- It does NOT replace the 3 surveys. It explains them with a unifying lens.

## 6. Risks and honest limits

- **P12 G2 N=30 completion FALSIFIED the strong-signal N=6 reading** (per memory, 2026-07-05T04:00:00Z): 1st judge n=17 mean_delta=-0.16 CI [-0.35, +0.02] (CI crosses 0); 2nd judge n=8 mean_delta=+0.34 CI [+0.23, +0.46] (REVERSE direction). The P12 N=10 contrast-effect signal **did not generalize to N=30**. This is a **calibration of my confidence in the contrast hypothesis** — Direction A still proposes it as a theoretical prediction, but the empirical evidence is weaker than the N=6 suggested.
- **3 distinct providers** are needed for PIT-107; we have 3 active (paratera, minimaxi, openrouter) but OpenRouter free tier has 40% parse-failure attrition on structured JSON prompts. Need paid tier or batched retries for the 30-sample/cell target.
- **Method-paper check COMPLETED** (2026-07-05 晚): 0/8 use anchoring framing. **CoBBLEr identified as closest prior art** (Koo et al. arXiv:2309.17012) — handled in §3 with 3-axis differentiation. The "may surface MARGINAL" caveat no longer applies; novelty clearance is closed.
- **Honest ceiling remains workshop/Findings**: even with novelty clearance, the realistic venue is ACL/EMNLP Findings (7.0-7.5), not main track (≥7.5). Main track needs scenario diversity + external validation + frontier baselines beyond what this project can deliver in <6 months.

## 7. Next step

5-persona review on this proposal. If median ≥ 5.5: schedule the 1500-call mechanism experiment (~12 hours wall time on Paratera + frontier arm). If median < 5.5: fold into a methods paper alongside G3 dual-ledger bridge.
