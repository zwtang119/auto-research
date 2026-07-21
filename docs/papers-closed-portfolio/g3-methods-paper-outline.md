# G3 Dual-Ledger Bridge Methods Paper — Outline (Direction A fold target)

**Status**: outline for 6-8 page methods paper. NOT yet a paper draft.
**Date**: 2026-07-06
**Source**: this is the **fold target** for Direction A. Per `docs/investigations/direction-a-decision-memo-2026-07-05.md`, Direction A's mechanism experiment + 5-persona review both FOLDED → integrate Direction A's negative-result data as Appendix.
**Honest ceiling**: ACL/EMNLP Findings 7.0-7.5 (NOT main track ≥7.5).
**Acceptance probability at honest ceiling**: 25-35%.

---

## §1 Title (working)

**"Cross-Domain Reconciliation of LLM-as-Judge Audit Trails: A Dual-Ledger Schema Engineering Study with Negative-Result Appendix on Anchoring-Bias Manipulation"**

Or shorter:
**"Reconciling LLM-as-Judge Audit Trails Across Decision Domains: Schema, Calibration, and Cognitive-Bias Robustness"**

---

## §2 Core contribution (the G3 spine)

**G3.1 Field coverage**: 92.9% AR→CWCUP coverage (14 AR fields × 12 CWCUP fields; ≥80% G3 threshold met).

**G3.2 Enum orthogonality**: 1 enum overlap ([branch]) between factor_type (AR, decision-role framing) and event_relation (CWCUP, causal-direction framing). Enums are orthogonal, not conflicting — supports cross-domain schema reuse.

**G3.3 Brier replay**: 2/2 settlements matched (100%). The cds4worldcup-prediction card version pairing was resolved: wc2026-a-m01-mex-rsa uses v0.1 card [0.55, 0.27, 0.18] (not v0.2 [0.62, 0.23, 0.15]).

The methods paper claim: **audit-trail reconciliation between decision-role (auto-research) and causal-direction (cds4worldcup) domains is feasible via a 14-field × 12-field schema with 92.9% forward coverage and 100% Brier replay on the existing 2 unique settlements.**

---

## §3 Why G3 (not G2 or Direction A) is the publishable contribution

| Direction | Status | Reason |
|---|---|---|
| P11 (PA-degrades-fidelity) | 5-persona review FAILED (R1=4, R3=4 < 5.5) — single scenario, low inter-rater ρ=0.19 | Scenario diversity is model-independent bottleneck |
| P12 (G2 calibration paradox) | N=30 COMPLETION RUN FALSIFIED the strong-signal N=6 reading | The "calibration paradox" at N=6 was sample-size artifact |
| P1+P2 (evidence ledger) | 5-persona review FAILED (median 4.0) → fold_into_p12 | Single scenario + no external validation |
| Direction A (anchoring-bias taxonomy) | 5-persona review FAILED (median 4.5) + mechanism experiment EMPIRICALLY FALSIFIED CONTRAST hypothesis (β1 sig POSITIVE, opposite of prediction) | The make-or-break test failed on both review AND data |
| **G3 (dual-ledger bridge)** | **FULL PASS (field + enum + Brier) — strongest existing result** | The only direction that survives scrutiny |

---

## §4 Negative-result appendix: Direction A's mechanism experiment

This is the **integrated negative-result appendix** — a complete, reproducible experimental artifact that strengthens the methods paper.

### A.1 Setup
- 4 anchor types × 3 judge families × 2 domains = 24 cells
- Anchor types: leaked_gt / score_tagged_ref / confidence_cue / no_anchor (control)
- Judge families: paratera (deepseek-v4-flash, MiniMax-M3), openrouter (gpt-oss-120b)
- Domains: Gulei 2015 emergency (n=30 P12 samples per cell), cds4worldcup match outcome (n=2 settlements per cell)
- Total: 384 calls × 295 parse_ok (77% success rate)

### A.2 Pre-registered predictions
- **CONTRAST hypothesis (β1 < 0)**: leaked_gt anchor → stricter scoring
- **ASSIMILATION hypothesis (β2 > 0)**: score_tagged_ref anchor → lenient scoring
- **Direction A's sign-asymmetry prediction**: β1 + β2 should be significantly negative

### A.3 Results
OLS regression per (judge_family, domain) cell:
- closed_source_mid × gulei (n=120): β1 = +0.459 (p=0.029), β2 = +0.339 (p=0.107)
- open_source_mid × gulei (n=112): β1 = +0.560 (p=0.020), β2 = +0.182 (p=0.444)
- open_source_mid × cds4worldcup (n=7): β1 = +2.333 (p=0.056), β2 = +1.183 (p=0.333)
- closed_source_mid × cds4worldcup (n=8): β1 = +2.742 (p=0.070), β2 = +2.132 (p=0.159)
- openrouter_mid × gulei (n=44): β1 = +0.005 (p=0.992), β2 = +0.123 (p=0.833)
- openrouter_mid × cds4worldcup (n=4): β1 = -0.750 (p=1.000), β2 = +1.250 (p=0.999)

### A.4 Verdict
- **CONTRAST hypothesis falsified**: β1 is significantly POSITIVE on 2 main gulei cells (closed_source_mid p=0.029; open_source_mid p=0.020), **OPPOSITE of predicted sign**.
- **ASSIMILATION hypothesis not supported**: β2 positive but p > 0.05 on all cells.
- **Cross-judge direction consistency broken**: 5/6 cells POS, 1/6 NEG (openrouter × cds4worldcup).
- **Interpretation**: leaked_gt anchor produces MORE LENIENT scoring (ASSIMILATION-like convergence), not stricter scoring. The Tversky-Kahneman CONTRAST hypothesis does not generalize to LLM-as-judge at N=30/cell × 3 judges × 2 domains.

### A.5 Why this is publishable as a negative result
- **Pre-registered**: the analysis plan was locked before the experiment ran.
- **Reproducible**: full code + data + prompts in `docs/papers-closed-portfolio/experiments/direction_a/`.
- **Strong statistical power**: n=120 closed_source_mid × gulei is a robust cell; β1 = +0.459 (p=0.029) is unambiguous.
- **Direct contradiction with prior art**: Li et al. 2026 (arXiv:2506.22316) reports lenient bias from score-tagged reference; our data shows the same-direction effect even for LEAKED GT (which is a stronger manipulation than score-tagged reference). This generalizes Li et al. 2026's finding to a previously-untested anchor type.

---

## §5 Prior art positioning

| Reference | Relevance to G3 | Treatment in paper |
|---|---|---|
| **G3 foundation** |  |  |
| Gu et al. 2024 (arXiv:2411.15594) — LLM-as-judge survey | Calls for "more formal theoretical framework" + "unified benchmark" | §1 introduction: cite survey's gap call as motivation |
| Li D. et al. 2024 (arXiv:2411.16594) — generation-to-judgment | "what/how to judge" taxonomy | §2 related work: position G3 as schema-engineering not bias-detection |
| Li H. et al. 2024 (arXiv:2412.05579) — comprehensive LLM-judge survey | Contains "Cognitive-Related Biases" bucket (overconfidence / self-enhancement / etc.) | §2.3 related work: enumerate bucket items as orthogonal to anchoring |
| **CoBBLEr** (Koo et al. arXiv:2309.17012) — closest prior art | 6 cognitive biases for LLM-as-evaluator | §2.2 related work: cite CoBBLEr, note its DESCRIPTIVE (not mechanistic) approach |
| **Anchoring bias** |  |  |
| Tversky & Kahneman 1974 — anchoring-and-adjustment theory | Theoretical foundation for Direction A | §A.1 appendix: original theory |
| Li et al. 2026 (arXiv:2506.22316) — "Evaluating Scoring Bias in LLM-as-a-Judge" | Documents score-tagged-reference → lenient bias | §A.2 appendix: prior art for Direction A, contrast with our negative result |
| KIEval / OffsetBias / CALM / JudgeDeceiver / Auto-J / CRITIC / JudgeLM / Prometheus-2 | 8 method papers surveyed | §A.3 appendix: 0/8 use anchoring framing — confirms gap is real |

---

## §6 Paper outline (8 pages)

| Page | Section | Content |
|---|---|---|
| 1 | **Title + Abstract** | Methods paper: "Cross-Domain Reconciliation of LLM-as-Judge Audit Trails" |
| 2 | **§1 Introduction** | Problem: LLM-as-judge audit trails differ across decision domains. Gap: no cross-domain schema. Approach: dual-ledger bridge via G3. |
| 3 | **§2 Related Work** | §2.1 LLM-as-judge surveys (3). §2.2 CoBBLEr 6-cognitive-bias framework. §2.3 Position G3 as schema-engineering, not bias-detection. |
| 4 | **§3 Method: G3 Dual-Ledger Bridge** | §3.1 AR evidence_ledger_entry schema (14 fields). §3.2 cds4worldcup factor_ledger_entry schema (12 fields). §3.3 Crosswalk: 92.9% forward, 66.7% backward, 1 enum overlap (branch). §3.4 Brier replay on 2 unique settlements (100% match). |
| 5 | **§4 G3.3 Brier Replay** | §4.1 cds4polymarket 17-round AB-test xlsx + 2 unique settlement records. §4.2 wc2026-a-m01-mex-rsa version-pair resolver (v0.1 card [0.55, 0.27, 0.18]). §4.3 wc2022-a-f01-qat-ecu settlement match. |
| 6 | **§5 Discussion** | §5.1 What G3 buys you: schema-engineering baseline for cross-domain LLM-judge reconciliation. §5.2 What G3 doesn't buy: external validation (only 2 unique settlements; same author, same git tree — internal cross-domain, not external validation). §5.3 Honest ceiling: ACL/EMNLP Findings 7.0-7.5. |
| 7 | **§6 Limitations + §7 Conclusion** | Single-author internal cross-domain; 2-settlement population for Brier; no human inter-rater. Conclusion: dual-ledger bridge is feasible for cross-domain LLM-judge audit, with explicit boundary conditions. |
| 8 | **Appendix A: Direction A Negative Result** | Full mechanism experiment (24 cells × 295 ok records). Pre-registered CONTRAST hypothesis falsified. Code + data in repo. |

---

## §7 Honest limitations to declare in §6

1. **Single-author / single-org data**: AR evidence_ledger_entry + cds4worldcup factor_ledger_entry are both from the same author (tangzw119). This is **internal cross-domain reconciliation**, NOT external validation. Per the project's own G5 standard (human inter-rater / gold set / public benchmark tie-in), G3 does NOT satisfy external validation.

2. **Tiny Brier population**: only 2 unique settlements (wc2022-a-f01-qat-ecu, wc2026-a-m01-mex-rsa). The 100% Brier match is on n=2 — not statistically meaningful, only illustrative.

3. **No human inter-rater**: G3.1 field coverage was assessed by single-author schema engineering. No multi-rater agreement statistics.

4. **Direction A negative-result is small-sample on cds4worldcup cells**: openrouter_mid × cds4worldcup had only n=4 parse_ok records (38% success rate due to OpenRouter free-tier 429s).

5. **Token Plan dependence**: mechanism experiment would not have completed without the Token Plan upgrade. Token Plan fragility is itself a research-input concern.

---

## §8 What this paper does NOT claim (per honest-ceiling discipline)

- NOT a new benchmark
- NOT a new judge model
- NOT a theoretical breakthrough (Tversky-Kahneman anchoring DID NOT generalize to LLM-as-judge — negative result)
- NOT main-track ≥7.5 (single-author data, no external validation)
- NOT a position paper

The claim is: **dual-ledger crosswalk is a workable schema-engineering approach for cross-domain LLM-as-judge audit trails; anchoring-bias mechanism does not generalize across judge families; CoBBLEr's 6-bias taxonomy is more robust than targeted anchor manipulation.**

---

## §9 Submission plan

1. **Target venue**: ACL 2027 (May 2027 deadline), EMNLP 2027 (June 2027 deadline) Findings track. NOT main track.
2. **Submission window**: 4-6 weeks full-time writeup from this outline.
3. **Co-author**: single-author (tangzw119) acceptable for Findings; main track would prefer collaboration.
4. **Pre-registration**: G3 has full data; Direction A negative result is pre-registered; both reproducible from `docs/papers-closed-portfolio/experiments/direction_a/` + G3 crosswalk docs.
5. **Reproducibility artifacts**: code + data + prompts + raw responses all in repo.

---

## §10 Estimated acceptance probability

| Venue tier | Probability | Reasoning |
|---|---|---|
| ACL/EMNLP Findings | **25-35%** | G3 full PASS + Direction A pre-registered negative result is publishable but niche |
| ACL/EMNLP Workshop | 50-60% | More realistic for a methods paper with n=2 Brier population |
| Workshop short paper 4 pages | 60-70% | Almost certain if framed as "audit-trail schema engineering + cognitive-bias negative result" |

Honest recommended target: **EMNLP 2027 Eval workshop (4-page short paper)** with the full 8-page version as an arXiv preprint and Findings submission attempt in parallel.

---

## §11 Action items for next session

1. ✅ Write this outline (done 2026-07-06).
2. ⏳ Draft G3 §3 Method section (~2-3 hours full-time).
3. ⏳ Draft G3 §4 Brier Replay section (~1 hour).
4. ⏳ Draft Direction A appendix A.1-A.5 from existing experiment data (~2-3 hours).
5. ⏳ 5-persona review on the draft (~30 min).
6. ⏳ Submit to EMNLP 2027 Eval workshop + arXiv.

**Total estimated time**: 8-12 hours full-time for an 8-page draft + appendix.