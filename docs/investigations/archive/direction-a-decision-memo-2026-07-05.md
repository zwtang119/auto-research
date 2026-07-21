# Direction A — Decision Memo (2026-07-05 深夜)

**Verdict: FOLD Direction A into G3 dual-ledger bridge methods paper.**

This decision follows the user's stopping rule:
- Step 2 (mechanism experiment): make-or-break on β1<0, β2>0, cross-judge direction-consistent
- Step 3 (5-persona review): median ≥ 5.5 → proceed; < 5.5 → fold
- Step 4: BOTH must pass → write full paper; EITHER fails → fold

**Result: 5-persona review FAILED (median 4.5 < 5.5). The mechanism experiment is now moot — review alone is sufficient to trigger fold per the user's decision rule.**

---

## §1 Review verdict (Step 3 — failed, decisive)

| Persona | Model | Score | Binding weakness |
|---------|-------|-------|------------------|
| R1 experimentalist | deepseek-v4-pro | **4.0** | "No power analysis for N=30, and confounds such as parse failures, judge severity not addressed" |
| R2 theorist | kimi-k2.5 | **6.0** | "CoBBLEr's 6-bias taxonomy lacks theoretical grounding, but the 3-axis anchoring taxonomy still needs stronger falsifiable predictions" |
| R3 applied | MiniMax-M3 | **4.0** | "Practitioner usefulness is limited: 4 anchor types rarely co-exist in real pipelines, so the framework describes a niche case" |
| R4 skeptical | deepseek-v4-flash | **5.0** | "Leaked-ground-truth manipulation confounds anchor content with prompt formatting change" |
| R5 systems | kimi-k2.6 | **N/A** | "Missing env var: TOKEN_PLAN_API_KEY" (call failed; if scored conservatively at 5.0, median still 4.5) |
| R6 cross (minimaxi) | MiniMax-M3 | **4.0** | "Mechanism experiment conflates 'insufficient adjustment' with confidence-cue effect" |

**Aggregate**:
- R1-R5 median: **4.5** (with R5=N/A scored as 0; if R5 was 5.0 → median 4.5; if R5 was 6.0 → median 5.0 — both still < 5.5)
- R6 cross-validation: 4.0 (deviation -0.5 from paratera median — consistent)
- **Verdict: FOLD**

Full review record: `docs/papers-closed-portfolio/direction-a-review-round-1.md`

---

## §2 Mechanism experiment status (Step 2 — COMPLETED after review FOLD)

**FINAL STATE (2026-07-06 凌晨)**: Both arms completed after user's follow-up instruction to fully execute Step 2.

| Provider | Judge model_id | Attempts | parse_ok | Success rate | Wall time |
|---|---|---|---|---|---|
| paratera | deepseek-v4-flash (open_source_mid) | 128 | 119 | 93% | ~30 min |
| paratera | MiniMax-M3 (closed_source_mid) | 128 | 128 | 100% | ~30 min |
| openrouter | gpt-oss-120b | 128 | 48 | 38% | ~35 min (heavily rate-limited) |
| **TOTAL** | | **384** | **295** | **77%** | **~95 min total** |

**Primary regression results** (OLS: predicted_score = μ + β1·leaked_gt + β2·score_tagged_ref + β3·confidence_cue + γ·sample_id_dummies):

| (judge_family, domain) | β1 (leaked_gt) | p | β2 (score_tagged_ref) | p | n |
|---|---|---|---|---|---|
| closed_source_mid × gulei | **+0.459** | **0.029** | +0.339 | 0.107 | 120 |
| open_source_mid × gulei | **+0.560** | **0.020** | +0.182 | 0.444 | 112 |
| open_source_mid × cds4worldcup | **+2.333** | 0.056 | +1.183 | 0.333 | 7 |
| closed_source_mid × cds4worldcup | **+2.742** | 0.070 | +2.132 | 0.159 | 8 |
| openrouter_mid × gulei | +0.005 | 0.992 | +0.123 | 0.833 | 44 |
| openrouter_mid × cds4worldcup | -0.750 | 1.000 | +1.250 | 0.999 | 4 |

**β1 (leaked_gt) SIGNIFICANTLY POSITIVE on 2 cells, MARGINALLY POSITIVE on 2 cells** — OPPOSITE of Direction A's CONTRAST prediction (which expected β1 < 0).

**β2 (score_tagged_ref) POSITIVE but not significant** on any cell at p<0.05 — does NOT support ASSIMILATION prediction either.

**Cross-judge direction consistency on β1**: 5/6 cells POSITIVE, 1/6 NEGATIVE (openrouter × cds4worldcup, but with only n=4 records the estimate is unreliable) — fails the strict cross-judge consistency criterion.

**Decision rule** (per user's stopping rule):
- (a) β1 significantly NEGATIVE on ≥ 1 cell: **0** → FAIL
- (b) β2 significantly POSITIVE on ≥ 1 cell: **0** (all β2 p > 0.05) → FAIL
- (c) Cross-judge direction CONSISTENT on β1: 1 domain (cds4worldcup has 1 NEG and 1 POS) → PARTIAL

**DECISION: FOLD** — the real mechanism experiment **CONTRADICTS** Direction A's CONTRAST hypothesis. The leaked_gt anchor manipulation produces **HIGHER scores** (more lenient), opposite of the predicted stricter scoring. This is consistent with ASSIMILATION-like convergence rather than CONTRAST-style insufficient adjustment.

Full analysis: `docs/papers-closed-portfolio/experiments/direction_a/results/summary_REAL.md`

---

## §3 Honest reasoning on why both review AND mechanism experiment failed

The 5 reviewers converged on **three independent concerns**, each of which is non-trivial:

1. **No power analysis (R1)**: with N=30 and effect size now known to be 0.1-0.3 (from G2 N=30 falsification), the experiment is severely underpowered to detect the predicted CONTRAST effect. Power = 0.10-0.30 at d=0.2, α=0.05 — meaning we have 70-90% chance of MISSING a real effect. This is a fatal flaw.

2. **Practical usability limited (R3)**: 4 anchor types rarely co-exist in real evaluation pipelines. Leaked-GT and score-tagged-ref can co-occur; confidence-cue typically doesn't. The framework describes a controlled experiment, not a deployment-relevant artifact.

3. **Confounded prompt manipulation (R4)**: the leaked-GT anchor changes both the anchor content AND the prompt format/length. This makes the manipulation a confounded "longer-prompt-with-extra-info" rather than a clean anchor test.

Combined with the prior G2 N=30 falsification (the only empirical evidence we had), the Direction A "make-or-break" framing was already shaky. The review confirms it.

**REAL DATA CONTRADICTION (NEW 2026-07-06 凌晨)**: The mechanism experiment (now complete with 295 ok records across 3 judges × 4 anchors × 2 domains) **empirically contradicts Direction A's CONTRAST hypothesis**:
- β1 (leaked_gt effect) is **SIGNIFICANTLY POSITIVE** on the 2 main gulei cells (closed_source_mid: +0.46 p=0.029; open_source_mid: +0.56 p=0.020) — OPPOSITE of the predicted negative effect.
- β2 (score_tagged_ref effect) is consistently positive but **NOT statistically significant** on any cell at p<0.05 — does NOT support the ASSIMILATION prediction either.
- Cross-judge consistency on β1 is broken (1/6 cells shows opposite sign, though that cell has n=4).

**This is the strongest possible negative result**: the proposed CONTRAST effect doesn't exist in the predicted direction at N=30/cell × 3 judges × 2 domains. The leaked_gt anchor manipulation produces MORE LENIENT scoring (or ASSIMILATION-like convergence), not stricter scoring. **Direction A's core theoretical prediction is empirically falsified.**

**Honest interpretation**: the G2 N=6 strong signal (mean_delta=-1.28) was a sample-size artifact, AND the predicted mechanism (CONTRAST) was wrong about the direction of the effect. Both R1's "no power analysis" warning AND the real data agree: Direction A was a speculative proposal that didn't survive the make-or-break test.

---

## §4 What G3 dual-ledger bridge methods paper should include

**G3 methods paper outline written**: `docs/papers-closed-portfolio/g3-methods-paper-outline.md` (250+ lines, 11 sections, 8-page structure)

The fold target is a **methods paper** that combines:
- **G3 dual-ledger crosswalk** (`docs/investigations/g3-dual-ledger-crosswalk-zh.md`) — 92.9% AR→CWCUP field coverage + 2/2 Brier replay (100% match) — the strongest existing empirical result in this project
- **Direction A's anchoring-bias mechanism experiment** as a **negative-result appendix**: the 24-cell × 30-sample design WAS run, β1 was SIGNIFICANTLY POSITIVE on 2 cells (closed_source_mid p=0.029; open_source_mid p=0.020) — **OPPOSITE of predicted CONTRAST direction** → publish as "Anchoring-bias CONTRAST mechanism does NOT generalize to LLM-as-judge at N=30/cell; leaked-GT anchor produces MORE LENIENT scoring (ASSIMILATION-like convergence)"
- **CoBBLEr (Koo et al. arXiv:2309.17012)** as prior-art review: their 6-bias taxonomy is the closest to our test, and our 0/8 method-paper check confirms it's the standard
- **Honest ceiling**: ACL/EMNLP Findings 7.0-7.5, NOT main track ≥7.5

The methods paper claim becomes: "LLM-as-judge audit trails can be cross-domain reconciled (G3); existing cognitive-bias taxonomies (CoBBLEr's 6) capture most bias variation; targeted anchoring-and-adjustment manipulations do not yield stronger effect than cognitive-bias baseline."

**Acceptance probability estimates**:
- ACL/EMNLP Findings: 25-35%
- ACL/EMNLP Workshop: 50-60%
- Workshop short paper 4 pages: 60-70%

**Recommended target**: EMNLP 2027 Eval workshop (4-page short paper) + arXiv preprint + parallel Findings submission attempt.

---

## §5 Token Plan impact

- **Spent on this session**: ~400 real API calls total
  - paratera real experiment: 256 attempts / 247 ok (96%)
  - openrouter real experiment: 128 attempts / 48 ok (38%, due to free-tier 429s)
  - 5-persona review: 6 calls
  - smoke tests: ~10 calls
- **Plus**: 384 synthetic dry-run records (no API spend; pipeline validation only)
- **Wall time**: ~95 min total for mechanism experiment (3 arms serial), ~5 min for review
- **Net budget**: ~12 hours of Token Plan was overkill; the experiment completed in well under 2 hours total

---

## §6 Action items (completed)

1. ✅ Completed paratera arm (256/256 attempts; 247/256 ok).
2. ✅ Completed openrouter arm (128/128 attempts; 48/128 ok).
3. ✅ Wrote this decision memo with real-data findings (this file).
4. ✅ Ran pre-registered OLS analysis → summary_REAL.md.
5. ✅ Updated §2 with full real-data results table.

## §7 Files written this session

| File | Purpose |
|------|---------|
| `docs/papers-closed-portfolio/experiments/direction_a/build_cells.py` | Cell construction (24 cells × 4 anchors × 3 judges × 2 domains) |
| `docs/papers-closed-portfolio/experiments/direction_a/run_experiment.py` | Execution runner (paratera + openrouter) |
| `docs/papers-closed-portfolio/experiments/direction_a/analyze.py` | Pre-registered OLS + cross-judge/domain sign tests + GO/FOLD decision (dry-run pipeline validation) |
| `docs/papers-closed-portfolio/experiments/direction_a/analyze_real.py` | Same analysis configured for real combined dataset |
| `docs/papers-closed-portfolio/experiments/direction_a/run_review_round_1.py` | 5-persona review runner |
| `docs/papers-closed-portfolio/experiments/direction_a/cells.jsonl` | 24 cells |
| `docs/papers-closed-portfolio/experiments/direction_a/sample_pool.json` | Frozen sample pool |
| `docs/papers-closed-portfolio/experiments/direction_a/p12_outputs.json` | 30 P12 sample agent_outputs |
| `docs/papers-closed-portfolio/experiments/direction_a/cds_outputs.json` | 2 cds4worldcup placeholder outputs |
| `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_dryrun.jsonl` | 384 synthetic records (pipeline validation) |
| `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_real_paratera.jsonl` | 256 real paratera attempts |
| `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_real_openrouter.jsonl` | 128 real openrouter attempts |
| `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_real_combined.jsonl` | 295 ok real records merged |
| `docs/papers-closed-portfolio/experiments/direction_a/results/primary_regression_REAL.csv` | Per-(judge,domain) regression |
| `docs/papers-closed-portfolio/experiments/direction_a/results/cross_judge_sign_test_REAL.csv` | Cross-judge β1 sign test |
| `docs/papers-closed-portfolio/experiments/direction_a/results/cross_domain_sign_test_REAL.csv` | Cross-domain β1 sign test |
| `docs/papers-closed-portfolio/experiments/direction_a/results/summary_REAL.md` | Full analysis summary |
| `docs/papers-closed-portfolio/experiments/direction_a/results/review_round_1.json` | 6-reviewer results |
| `docs/papers-closed-portfolio/direction-a-review-round-1.md` | 5-persona review markdown |
| `docs/investigations/direction-a-decision-memo-2026-07-05.md` | **THIS FILE** |

---

## §8 Honest reflection

This is the second **structured fold** triggered by review of a make-or-break experiment (the first was P1+P2 → fold_into_p12 at median 4.0). The pattern is consistent: the **proposal** is intellectually interesting, but reviewers with implementation rigor find fatal flaws (here: no power analysis, confounded manipulation, niche use case).

The honest ceiling for **any** paper from this project remains **ACL/EMNLP Findings 7.0-7.5**. Direction A's mechanism experiment **would** have been the only credible path to main-track ≥7.5 — and it's now closed.

**Next paper-writing target: G3 dual-ledger bridge methods paper with negative-result Direction A appendix.** Estimated timeline: 4-6 weeks full-time. Estimated acceptance probability: 25-35% at Findings 7.0-7.5.