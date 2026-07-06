# Investigation: AutoResearch Top-Journal Readiness

## Summary
Final judgment: **the current portfolio is not top-journal/main-track ready**. The honest current ceiling is a workshop/findings-style joint methods paper around P12 + P1+P2 + P8 + P7, roughly 6.5-7.0 review territory. A real main-track/top-journal attempt becomes rational only after structural unlocks that tokens alone cannot buy: independent scenario diversity, external validation, and frontier-model baselines.

## Symptoms
- The portfolio asks whether the current research contents can plausibly reach a top journal or top-tier publication if more token budget, experiments, and analysis are invested.
- Existing roadmap explicitly prioritizes a near-term 60-point publishable paper first, with higher-ceiling work only if there is a structural breakthrough.
- P11 has a prior readiness investigation concluding it should not keep chasing a main-conference-level upgrade.
- Active paper lines include P12 judge calibration, P1+P2 evidence ledger, P8 market/settlement calibration, and P7 signal fusion, but their current evidence maturity appears uneven.

## Background / Prior Research

### External Literature: Multi-Agent Decision Evaluation
Explore agent `D3BDEF60-A96E-4B78-81DE-A9E3D8FDC759` checked 2024-2026 multi-agent and decision-evaluation literature.

Key primary-source anchors:
- GAIA: <https://arxiv.org/abs/2311.12983>
- AgentBench: <https://arxiv.org/abs/2308.03688>
- SWE-bench: <https://arxiv.org/abs/2310.06770>
- MetaGPT: <https://arxiv.org/abs/2308.00352>
- AutoGen: <https://arxiv.org/abs/2308.08155>
- PlanBench: <https://arxiv.org/abs/2206.10498>
- Humanity's Last Exam: <https://arxiv.org/abs/2501.14249>
- Clinical decision agent benchmark: <https://www.nature.com/articles/s41746-026-02443-6>

Takeaways:
- Top-tier multi-agent decision papers increasingly require real tasks/scenarios, multiple baselines, statistical rigor, human or external validation, and failure analysis.
- Emergency/disaster LLM-agent benchmarks appear thin at top venues, which creates a real opening for P1+P2 if it becomes a benchmark-grade, externally validated decision-intelligence paper.
- Agent scaffolding alone is not enough; the paper must show that evidence structure, calibration, and settlement add measurable value beyond a strong single-agent / ReAct / multi-agent baseline.

### External Literature: Evidence Ledger / Evidence Topology
Explore agent `1E855CBA-5EFE-4E40-96EC-1C5C12643309` checked RAG, evidence-grounded agents, provenance, claim verification, and evidence graphs.

Key primary-source anchors:
- GraphRAG: <https://arxiv.org/abs/2404.16130>
- Graph RAG survey: <https://arxiv.org/abs/2408.08921>
- HippoRAG: <https://arxiv.org/abs/2405.14831>
- JANUS factored reasoning / evidence-grounded HRI: <https://arxiv.org/abs/2602.00675>
- RAGAS: <https://arxiv.org/abs/2309.15217>
- Faithful chain-of-thought: <https://arxiv.org/abs/2301.13379>
- Claim verification survey: <http://www.copenlu.com/publication/2024_arxiv_dmonte/>
- Automated fact-checking with LLMs: <https://arxiv.org/abs/2502.08909>

Takeaways:
- Novelty cannot rest on "RAG with citations," "knowledge graph," or "claim verification"; those areas are crowded.
- The plausible novelty is a schema-enforced, settlement-aware, multi-relational decision contract: claim -> evidence -> contradiction -> missing prerequisites -> settlement rule -> observed outcome -> calibration update.
- JANUS is the nearest semantic threat because it combines "factored reasoning" and "evidence-grounded" agents; P1+P2 must differentiate as decision trace + settlement discipline, not inner-speech or generic evidence grounding.

### External Literature: LLM Judge Calibration
Explore agent `0FE2FD3D-0B73-473C-A5AA-61C2FEEDF489` checked 2024-2026 LLM-as-a-judge calibration, bias, leakage, pairwise judging, and abstention literature.

Key primary-source anchors:
- MT-Bench / Chatbot Arena judge paper: <https://arxiv.org/abs/2306.05685>
- LLM-as-a-Judge survey: <https://arxiv.org/abs/2411.16594>
- Position bias in LLM judges: <https://arxiv.org/abs/2406.07791>
- Self-preference bias: <https://arxiv.org/abs/2410.21819>
- Time-travel contamination detection: <https://arxiv.org/html/2308.08493v3>
- Benchmark contamination survey: <https://arxiv.org/abs/2406.04244>
- Agent-as-a-Judge: <https://arxiv.org/abs/2410.10934>
- Scoring bias in LLM-as-a-Judge: <https://arxiv.org/abs/2506.22316>

Takeaways:
- P12 is not novel by individual components: leaked/blind/pairwise/neighborhood/abstention all have nearby prior art.
- P12 can still be a credible short paper if framed as a frozen five-protocol decomposition on the same ordered sample list, with `verdict_delta` as the headline metric that identifies the source of judge pathology.
- P12 is unlikely to be an independent top-journal paper unless it becomes a broadly validated judge-side benchmark; it is more valuable as the reliability layer for P1+P2.

### External Literature: Prediction-Market Settlement / Forecast Calibration
The prediction-market explore agent was cancelled after entering a long-running deep-research loop. I replaced it with direct agent-reach Exa searches.

Key primary-source anchors:
- ForecastBench: <https://arxiv.org/pdf/2409.19839>
- Reasoning and Tools for Human-Level Forecasting: <https://arxiv.org/pdf/2408.12036>
- LLM-as-a-Prophet / Prophet Arena: <https://arxiv.org/pdf/2510.17638>
- FORECAST benchmark: <https://proceedings.neurips.cc/paper_files/paper/2025/file/2277c7c3b112fcc6031a6f0d832df2a0-Paper-Datasets_and_Benchmarks_Track.pdf>
- KalshiBench: <https://arxiv.org/html/2512.16030>
- Evaluating LLMs on real-world forecasting against expert forecasters: <https://arxiv.org/pdf/2507.04562>

Takeaways:
- Forecasting work already uses Brier score, log loss, ECE, market returns, and expert/crowd comparisons; P8 cannot claim novelty merely from using Polymarket/Kalshi-style markets.
- P8's value is as an external settlement/calibration layer for factor-level beliefs: it gives P1+P2 hard outcomes instead of pure LLM-judge scores.
- Independent P8 top-tier potential would require a strong result such as factor-level belief updates outperforming market-only or LLM-only baselines across enough resolved events. Current project state does not yet show that.

## Investigator Findings

> **Top-line**: there is **no credible top-tier (NeurIPS/ICLR/ACL main-track) publication route** in the current portfolio. Every active paper line either has been formally CLOSED as a standalone results paper or is a methodology scaffolding artifact without powered executed evidence. The combined methods paper (P12 + P1+P2 + P8 + P7) is the only *plausible* high-ceiling unit, but its ceiling is **workshop / findings-track (≈6.5-7.0)**, not main-conference (≥7.5). Structural blockers — single scenario, no external validation, no frontier baselines, low inter-judge agreement — are not token-bounded; they cannot be bought away with more compute.

### Hypothesis validation

**(H1) CONFIRMED: no current single paper line has top-tier executed evidence.**

- `papers/p12-judge-calibration/state/progress.json:4-12` — `status: "m8_complete_fold_into_p1_p2"`, `iteration: 6`. M8 closed; carryover into P1+P2 only.
- `papers/p12-judge-calibration/state/progress.json:33-58` — 5-persona review **median 3.0 / mean 2.8 / max 4.0**, **verdict `fold_into_p1_p2`** (median < 6.0 threshold). PIT-107 satisfied (5 distinct models); anti-inflation cap GREEN.
- `papers/p12-judge-calibration/experiments/calibration_metrics.md:9-13,49-67` — Per-protocol n is **leaked=10, blind=10, neighborhood=3, abstention=7**; H1c and F1 hypotheses populated **with zero rows** (n=0 cells); CI [-1.461, -1.078] for the leaked-vs-blind delta = -1.284 — leakage **detected in the OPPOSITE direction** to the hypothesis. Sample sizes below any defensible threshold.
- `papers/p1p2-evidence-ledger/state/progress.json:4-12` — `status: "m9_fold_into_p12_median_4_0_below_6_5"`, `iteration: 4`. M9 closed; standalone paper path abandoned.
- `papers/p1p2-evidence-ledger/state/progress.json:28-36` — 5-persona review **median 4.0 / mean 4.0 / max 5.0**, **verdict `fold_into_p12`** (median < 6.5 threshold).
- `papers/p1p2-evidence-ledger/paper/review_round_1.md:13-29` — All 5 reviewer binding weaknesses name **single-incident overfit (R3)**, **n=5 unstable (R4)**, **PIT-201 row-5 violation missed (R5)**, **no theoretical grounding for factor-type taxonomy (R2)**, **no sample-size justification for per-factor-type claim (R1)**. No reviewer found the standalone paper publishable.
- `papers/p08-market-calibration/state/progress.json:4-12` — `status: "m1_5_review_research_grade_acceptable"`, `iteration: 2`. NOT a results paper; methodology scaffolding only (median 5.0, threshold 5.0).
- `papers/p08-market-calibration/state/progress.json:22-27` — **Critical data-shape blocker**: `m1_ab_test_data_shape_mismatch` — "M1 attempted to parse 17-round AB-test data; data is judge scores (discrete 1-5) not prediction probabilities. Brier cannot be computed without a new round emitting predicted_p." There is currently **zero Brier-able data** in P8.
- `papers/p07-signal-fusion/state/progress.json:4-11` — `status: "m1_review_research_grade_acceptable"`, `iteration: 3`. Methodology scaffolding only (median 5.0).
- `papers/p07-signal-fusion/state/findings.jsonl:5` — **Live engine blocked**: "SignalFusionEngine import blocked: signal_fusion_engine.py uses internal imports that fail when adapter is run from papers/p07-signal-fusion/experiments/." M3+ blocked on engine refactor.
- `papers/p07-signal-fusion/state/findings.jsonl:7` — **Real audit-chain defect detected in M1 review**: `snippet_sha256_prefix` is fabricated via string padding, not a real SHA256. Codified as PIT-NEW candidate 9. Even the scaffolding has a known-broken audit chain.
- `legacy/p11-closed-v5-minimax-m3/state/progress.json:4-12` — `status: "closed_2026-07-03_Mimo_integration_recommended"`. 240+927 runs done, **26 review rounds plateau at median 5.84-6.60** (per `legacy/p11-closed-v5-minimax-m3/wiki/annotations/paper-review-rounds.md:64-82` and the prior readiness investigation F2).

**(H2) PARTIALLY VALIDATED, BUT DOWNGRADED: P1+P2 + P12 with P8/P7 support is the only plausible high-ceiling route — but ceiling is workshop/findings, not main-track.**

- The combined unit is real: the 14-field `evidence_ledger_entry` schema + 6 PIT invariants (PIT-201..PIT-206) from `papers/p1p2-evidence-ledger/wiki/concepts/evidence-ledger-schema.md:11-28`; the 5-protocol P12 judge design (leaked/blind/pairwise/neighborhood/abstention) from `papers/p12-judge-calibration/state/progress.json:12-19`; the `settlement_record` schema from `papers/p08-market-calibration/paper/outline.md:9-29`; the P7 adapter contract from `papers/p07-signal-fusion/state/findings.jsonl:1-2`. Each piece passes `research_grade_acceptable` review (median 5.0) as a scaffolding artifact.
- `papers/p1p2-evidence-ledger/experiments/pilot_power.md:35-44` — Power analysis is explicit: **for d=0.5 detection, need N=64/cell**; **for d=0.8 detection, N=26/cell** suffices. The pilot_30 has 5 cells × ~6 entries per factor_type (range 5-8) — i.e., **N ≈ 5-8 per cell, not 64**. The result is **power = 0.48 at d=0.5**, i.e., a 52% false-negative rate for medium effects. The roadmap's 60-point budget cannot fund N=64/cell × 30 cells × 4 conditions ≈ 30 API hours (`papers/p1p2-evidence-ledger/state/blocked.md:18-24`).
- `papers/p1p2-evidence-ledger/state/blocked.md:81-94` — The closure was deliberate: P1+P2 standalone is closed; the methodology **folds into P12** as a methods paper. The closure narrative (`papers/p1p2-evidence-ledger/state/blocked.md:89-94`) explicitly says "carry the 14-field evidence_ledger_entry schema + 6-PIT-invariants validator + factor-type taxonomy + P12 5-protocol design into a single methods paper (joint P1+P2 + P12 submission). The cross-paper bridge is the contribution; the standalone result is too underpowered."
- The highest-ceiling unit is therefore a **methodology/contract paper** (e.g., "A Structured Contract for Verifiable Agent Decisions: Evidence Ledger + Judge Calibration + Settlement"), not a results paper. Estimated ceiling: **workshop-tier 6.5-7.0** with current scaffolding; main-track ≥7.5 requires the N=64/cell main run plus scenario diversification plus external validation.

**(H3) CONFIRMED: P11 can provide empirical motivation but not headline a top-tier results paper.**

- `legacy/p11-closed-v5-minimax-m3/state/closure.md:11-21` — Closure rationale: H1 fidelity ceiling FAILED under blind judging; label leakage created false positives; pure_analysis > inner_monologue on emergence vocabulary; subjective fidelity judging less stable than objective risk-taking. The closure was a deliberate decision not to chase main-conference-level upgrade.
- `legacy/p11-closed-v5-minimax-m3/state/progress.json:34-37` — H1c reasoning depth PASS, H3 Spearman PASS (0.76-0.82 across 4 judges), but inter-judge agreement on **subjective fidelity is 0.19 (near random)**; only `risk_taking` is robust (0.74). 6D full report has only rt(0.78) strong, 4 others near zero.
- `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/metadata.json:46-65` — A2b ICC 0.707 moderate; per-dimension ICC 0.50-0.794, with `financial_depth=0.50` as the most fragile dimension. 26.5% DeepSeek parse failures (199/750) leave only 551 valid scores for the primary judge.
- `legacy/p11-closed-v5-minimax-m3/wiki/closure/2026-07-03-project-end.md:23-25` — The recommended Mimo+v5 integration path expects **Gate 4 score 7.5-8.0** ("main conf 可能") at 7-10 days of additional work — a non-trivial but bounded Mimo-integration bet, not a token-bounded bet.
- P11 is best repurposed as: (a) a counter-example in P1+P2 ("free-text reasoning traces are not enough"); (b) a sample source for P12 judge calibration; (c) a workshop/findings paper in its own right (per the prior readiness investigation at `docs/investigations/p11-inner-monologue-paper-readiness-2026-07-03.md:212-220`).

**(H4) CONFIRMED: tokens help sample size but structural blockers are scenario diversity, external validation, and frontier baselines.**

Sample-size blockers (token-bounded, partially solvable):
- `papers/p1p2-evidence-ledger/experiments/pilot_power.md:35-44` — Pilot N=30 yields 0.48 power at d=0.5. To reach 0.80 power at d=0.5 needs **N=64/cell** across 30 cells = ~30 API hours, explicitly out of single-session budget (`papers/p1p2-evidence-ledger/state/blocked.md:22`).
- `papers/p12-judge-calibration/experiments/calibration_metrics.md:9-13` — P12's per-protocol n (10, 10, 3, 7) is below any defensible detection threshold; expanding to N=30+ per protocol × 4 conditions = ~1,000 judge calls, feasible but not yet executed.
- `papers/p08-market-calibration/state/progress.json:24-26` — **No probabilities exist** in P8's 17-round AB-test data (judge scores 1-5 instead). Tokens cannot convert 1-5 scores into Brier-compatible probabilities; new rounds must emit `predicted_p` first.
- Sample size IS partially unlockable with compute, but see `papers/p1p2-evidence-ledger/state/blocked.md:30-32` — "M5 main run exceeds single-session budget — needs explicit user sign-off for 30 API hours."

Scenario-diversity blockers (NOT token-bounded, NOT unlockable without fresh scenario acquisition):
- `papers/p1p2-evidence-ledger/paper/review_round_1.md:14` — R3 (applied) binding weakness: "Gulei 2015 is single-incident overfit; 7% un_settleable rate looks cherry-picked and factor-type-conditional framing barely informs practitioners." The 30 handcrafted entries are entirely Gulei 2015 + commercial_space 3ent — two scenarios.
- `papers/p12-judge-calibration/experiments/calibration_metrics.md:18-35` — H1c and F1 hypotheses populated with **n=0 rows**. Four of the six planned condition × protocol cells have no data; this is not a sample-size problem, it is a **scenario coverage problem** (no_think and pure_analysis scenarios were never sampled at the judge-calibration layer).
- `papers/p12-judge-calibration/state/progress.json:50-58` — Calibration explicitly reuses P11's anchors only ("P12 only reuses anchors; P12's primary claim is the leakage effect, not P11's substantive claims"). Top-tier venues require scenarios that are not the project's own anchors.

External validation blockers (NOT token-bounded, requires human/benchmark acquisition):
- All five P12 reviewers are LLMs (deepseek-v4-pro, kimi-k2.5, MiniMax-M3, deepseek-v4-flash, qwen3.5-122b-a10b). No human inter-rater, no human gold set, no public benchmark tie-in.
- `papers/p07-signal-fusion/state/findings.jsonl:9` — R2 (theorist) named "missing_data vs source_failure semantic overlap" — even the schema has unresolved semantic questions that external review would surface.
- `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/metadata.json:66-81` — A2_C pooled κ=0.183 (slight/poor); judges disagree on emergence-mode attribution. Any paper claiming judge-mediated evaluation must report inter-rater, but currently only ICC 0.707 on A and κ 0.183 on C — the latter is too weak to defend.

Frontier-baseline blockers (NOT token-bounded, requires API budget for GPT-5/Claude-Opus-4/Gemini-3-Pro):
- All five P12 review models are mid-tier open/closed models. Top-tier multi-agent decision papers (per the prior literature anchors: GAIA, AgentBench, SWE-bench, MetaGPT, AutoGen, PlanBench, Humanity's Last Exam) require frontier-model baselines. None of P7/P8/P12/P1+P2 evidence includes a frontier-model arm.
- `papers/p1p2-evidence-ledger/experiments/baseline_design.md` (referenced in `state/progress.json:60-66`) plans a per-factor-type comparison but does not list which models — this is a documented gap, not an oversight.

Additional structural blocker surfaced by inspection:
- `papers/p07-signal-fusion/state/findings.jsonl:7` — **PIT-NEW-9**: `snippet_sha256_prefix` is fabricated by string padding (`sig_id.replace('SIG-', '')[:12].ljust(12, '_')`), not a real SHA256. This is a real audit-chain defect in P7's M1 scaffolding. Any paper claiming audit-trace integrity must fix this before submission. Fix path documented: compute sha256 of signal_id + scenario + scenario_text + numeric_forecast bytes; truncate to 12 hex chars.

### Ranked investment recommendation

> Honest read: the **credible ceiling is workshop / findings track (≈6.5-7.0)**, not main-conference (≥7.5). All ranked options below are framed as publishable units in that ceiling band. None credibly reaches top-tier main-track with current executed evidence.

**Rank 1 (recommended): Joint P12+P1+P2 methods paper — "A Structured Contract for Verifiable Agent Decisions"** — ceiling 6.5-7.0, ETA 4-6 weeks, low API cost.

- Contribution shape: a 4-page (workshop) or 8-page (findings) methodology paper bundling the 14-field `evidence_ledger_entry` schema, the 5-protocol judge calibration design, the `settlement_record` Brier/Log Loss layer, and the P7 signal→ledger adapter. Each component already passes `research_grade_acceptable` review (median 5.0).
- Investment unlocks: (a) fix PIT-NEW-9 in P7 (1 day); (b) run P12 neighborhood probe to N=30 (2 days, ~3 API hours); (c) write one cross-paper integration doc that ties the four contracts together (3 days); (d) run 5-persona review on the integrated outline (1 day).
- Why it is the only plausible high-ceiling unit: it is the **only configuration where four independently-validated contracts compose into one paper** without requiring powered executed experiments. The contribution is the contract surface, not a result — and that is exactly what a methods paper claims.
- Hard gate: if the integrated outline review median < 5.5, fall back to the P11 workshop paper (Rank 3).

**Rank 2: P8 standalone short paper — "Settling Evidence: A Prediction-Market Settlement Layer for LLM Agent Belief Updates"** — ceiling 5.5-6.0, ETA 3-4 weeks, medium API cost.

- Blockers first: (a) AB-test data must be re-shaped — new rounds must emit `predicted_p`, not 1-5 judge scores (`papers/p08-market-calibration/state/progress.json:24-26`); (b) M2 human checkpoint for event selection is pending (`state/progress.json:18-20`).
- Investment unlocks: (a) re-run AB test with `predicted_p` output (2 weeks); (b) compute Brier/Log Loss on N=30+ resolved events per cell (the calc_brier.py is already implemented and 17/17 tests GREEN — `state/progress.json:14-17`); (c) write a focused 4-page paper (1 week).
- Why Rank 2 not Rank 1: the contribution is plumbing-only ("settlement contract" not "new calibration algorithm", per `papers/p08-market-calibration/paper/outline.md:9-13`); single-layer novelty is below the cross-paper integration novelty of Rank 1.
- Hard gate: if N=30 per cell cannot be reached (Polymarket/Kalshi settlement resolution rate), drop to a workshop demo paper.

**Rank 3: P11 workshop paper — "Inner Monologue as a Process Signal, Not a Fidelity Lever"** — ceiling 6.0-6.5, ETA 14 days, zero new API cost.

- Per `docs/investigations/p11-inner-monologue-paper-readiness-2026-07-03.md:212-220` and the 14-day plan there.
- Uses existing 927 runs + label-leakage finding + 1,824 judge calls. No new experiments.
- Why Rank 3 not Rank 1: it is single-scenario / single-LLM-family / single-judge-architecture — the structural ceilings named in the prior investigation's F4 (R2_theorist binding 4.5, R4_synthesizer binding 3.0-4.5) cannot be moved without scenario diversification.
- Use this as a fallback if Rank 1 stalls, OR run it in parallel as a "guaranteed submit" while Rank 1 matures.

**Rank 4: P7 standalone — NOT RECOMMENDED until engine refactor.**
- `papers/p07-signal-fusion/state/findings.jsonl:5` — Live engine import blocked; M3+ cannot run without cds-keyperson refactor.
- PIT-NEW-9 (fabricated sha256_prefix) is a real audit-chain defect; any audit-claim paper must fix this first.
- The paper outline already commits to "evidence-input adapter of the P1+P2 mainline" (`papers/p07-signal-fusion/paper/outline.md:5`), i.e., P7 is a sub-component, not an independent paper. Investing in P7 standalone is a scope-creep risk.

**Rank 5: P12 standalone — NOT VIABLE.**
- Already closed (median 3.0, fold_into_p1_p2). Do not reopen as standalone; the closure rationale was deliberate.

### Investment summary table

| Rank | Unit | Ceiling | ETA | API cost | Hard gate |
|---|---|---|---|---|---|
| 1 | Joint P12+P1+P2+P8+P7 methods paper | 6.5-7.0 (workshop/findings) | 4-6 wk | ~3-5 hr (P12 N=30 only) | Outline review median ≥ 5.5 |
| 2 | P8 standalone settlement short paper | 5.5-6.0 (workshop) | 3-4 wk | ~5-10 hr (AB re-shape + Brier) | N ≥ 30/cell on Polymarket |
| 3 | P11 workshop paper | 6.0-6.5 (workshop) | 14 d | 0 | Already validated at 5.84-6.60 |
| 4 | P7 standalone | not viable without engine refactor | n/a | n/a | n/a |
| 5 | P12 standalone | closed | n/a | n/a | n/a |

### What would change the answer (top-tier unlock conditions)

For any unit to credibly reach **main-track ≥ 7.5**, three structural gaps must close — none are token-bounded:

1. **Scenario diversification** — at least 3 independent emergency / decision scenarios beyond Gulei 2015 + commercial_space 3ent. Each requires external scenario acquisition (human SMEs, public benchmarks, or dataset licensing). Estimated effort: 4-8 weeks of human curation.
2. **External validation** — at least one arm with human inter-rater, gold-set calibration, or public benchmark tie-in (ForecastBench, GAIA, AgentBench, or a domain-specific oracle). Estimated effort: 3-6 weeks plus benchmark licensing.
3. **Frontier-baseline arm** — GPT-5 / Claude-Opus-4 / Gemini-3-Pro comparisons on at least one cell of the design. Estimated effort: 1-2 weeks of API budget + analysis; current models (DeepSeek-V4-Flash, Kimi-K2.5, Qwen3.5-122B) are mid-tier.

If any two of the three are unlocked, Rank 1's ceiling rises to 7.0-7.5 (findings track, possibly main-track borderline). If all three are unlocked, Rank 1's ceiling rises to 7.5-8.0 (main-track credible). Without at least two unlocks, **no top-tier route exists** in the current portfolio.

## Recommendations

- **Default next move**: invest 1 day fixing PIT-NEW-9 in P7 (cheap, eliminates audit-chain defect), 2 days running P12 neighborhood probe to N=30 (small but impactful sample-size upgrade), then 3 days writing the joint P12+P1+P2+P8+P7 methods-paper outline. Run 5-persona review on the outline at Day 6. If median ≥ 5.5, proceed to full paper (4 weeks); otherwise fall back to Rank 3 (P11 workshop paper, 14-day hard stop).
- **Don't do**: do not reopen P12 standalone; do not invest in P7 standalone without engine refactor; do not promise a main-track NeurIPS/ICLR submission without first closing at least two of the three structural-unlock conditions above.
- **Reserve spend**: do not commit to P8's M5 main run (N=64/cell × 30 cells × 4 conditions ≈ 30 API hours) without explicit user sign-off and a paired P1+P2 main-run commitment — one without the other halves the value of the data.

## Preventive Measures

- **Pre-register the top-journal route** before any new experimental cycle. Top venues penalize post-hoc claim re-shaping; the M4 pivot in `papers/p1p2-evidence-ledger/state/progress.json:32-36` is on-record but must be locked into a fresh pre-registration for the joint methods paper.
- **Cap each paper line's scope before starting**: P12 = judge calibration only; P1+P2 = evidence contract only; P8 = settlement only; P7 = adapter only. The current "everything folds together" posture has worked for scaffolding but will not survive external review unless each piece is independently citable.
- **Hold a hard external-validation gate** before any main-track submission: minimum one human inter-rater study or one public benchmark tie-in. Without it, do not submit to NeurIPS / ICLR / ACL main track — only to workshops or findings tracks.
- **Don't conflate "high-ceiling" with "top-tier"**: high-ceiling in this portfolio means workshop/findings-track ceiling 6.5-7.0; top-tier means main-track ≥7.5 and requires closing the three structural gaps above.

## Root Cause

The 12+-path oscillation from P11's history, the M3→M4 structural pivot that **narrowed** the P1+P2 claim rather than broadening it, the closure of P12 with verdict `fold_into_p1_p2` and P1+P2 with verdict `fold_into_p12`, the absence of Brier-able probabilities in P8, and the audit-chain defect in P7 collectively indicate a **methodology-first / evidence-second** posture. The contracts are good; the executed evidence is small. Top-tier requires the inverse posture: contracts first as scaffolding, executed evidence as the headline. The fastest credible top-tier route is therefore **methodology paper now, powered-experiment follow-up in 3-6 months** — but the follow-up requires scenario diversification, external validation, and frontier baselines, none of which are token-bounded.

### Phase 0 - Workspace Verification
**Hypothesis:** The `auto-research` workspace is loaded in RepoPrompt and can be targeted with rp-cli.
**Findings:** `rp-cli -e 'windows'` showed window `3` with repo `/Users/tangzw119/Documents/GitHub/auto-research`; `rp-cli -w 3 -e 'tree --type roots'` showed roots for `auto-research` and `cds4worldcup`.
**Evidence:** RepoPrompt CLI output on 2026-07-05.
**Conclusion:** Confirmed.

### Phase 1 - Initial Assessment
**Hypothesis:** The portfolio-level top-journal opportunity is not P11 alone, but a possible combined P1+P2/P8/P12 system around evidence-structured agent decision making.
**Findings:** Initial reads of `README.md`, `docs/portfolio/project-index.md`, `papers/README.md`, `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md`, and the prior P11 readiness report support this split.
**Evidence:** `README.md:1-13`, `docs/portfolio/project-index.md:21-45`, `papers/README.md:8-18`, `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md:1-19`, `docs/investigations/p11-inner-monologue-paper-readiness-2026-07-03.md:1-20`.
**Conclusion:** Confirmed; deeper investigation focused on the combined methods-paper route.

### Phase 1.5 - External Literature
**Hypothesis:** The portfolio can only claim top-tier novelty if external literature leaves room for settlement-aware evidence contracts, not generic RAG, LLM-as-judge, or prediction-market calibration.
**Findings:** External checks confirmed the surrounding literatures are crowded. The plausible gap is a schema-enforced, settlement-aware, multi-relational decision contract, not "RAG with citations" or "another judge calibration method."
**Evidence:** Background / Prior Research sections above.
**Conclusion:** Confirmed.

### Phase 2 - Builder Context Gathering
**Hypothesis:** The readiness decision requires cross-paper context across P11, P12, P1+P2, P8, P7, and framework contracts.
**Findings:** Builder selected 42 full files and concluded no individual line is top-tier ready. It identified the joint P1+P2 + P12 methods paper, with P8/P7 as supporting layers, as the only plausible high-ceiling route.
**Evidence:** RepoPrompt builder selection included roadmap, prior P11 investigation, framework schemas, P11 closure/h5 metadata, P12 state/metrics, P1+P2 progress/power/settlement mapping, P8/P7 state and outlines.
**Conclusion:** Confirmed with caveat that builder was more optimistic about main-track probability than later pair/chat synthesis.

### Phase 3 - Pair Investigator
**Hypothesis:** Builder's high-ceiling route may be too optimistic unless active lines have executed evidence.
**Findings:** Pair investigator confirmed that every active standalone line is closed or scaffolding-only. It downgraded the credible current ceiling to workshop/findings unless three structural gaps close: scenario diversity, external validation, and frontier baselines.
**Evidence:** `## Investigator Findings` above.
**Conclusion:** Confirmed; this is the controlling assessment.

### Phase 4 - Final Chat Synthesis
**Hypothesis:** The correct recommendation should reconcile builder optimism with pair conservatism.
**Findings:** Chat synthesis sided with the conservative interpretation: spend small token/API budget to produce a joint methods paper, but do not call it top-journal ready. Main-track becomes rational only after at least two of the three structural unlocks are secured.
**Evidence:** Oracle chat `new-chat-A2C785` over the curated selection.
**Conclusion:** Final recommendation: workshop/findings first; main-track only after structural unlocks.
