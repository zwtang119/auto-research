# Investigation: AutoResearch Top-Journal Opportunity (Fresh rp-investigate-cli Pass)

Date: 2026-07-05
Method: rp-investigate-cli + Superpowers (verification-before-completion, falsification-first)

## Summary
<!-- Filled after pair investigator + chat synthesis. -->

## Symptoms (User Question)
- 调研目前 auto-research 项目的现状（papers/、framework/、state/），分析是否有机会发表顶刊论文。
- Translation: investigate the current state of the auto-research project and analyze whether there is a credible opportunity to publish a top-tier journal / top-tier conference (NeurIPS/ICLR/ACL/EMNLP main-track) paper.

## Background / Prior Research

This is a **fresh assessment** run on 2026-07-05 evening. It builds on — and explicitly re-verifies — six same-day investigation documents already in `docs/investigations/`:

| Prior doc | Date | Key claim (as written) |
|---|---|---|
| `top-journal-readiness-2026-07-05.md` | 2026-07-05 | Not top-journal ready; ceiling workshop/findings 6.5-7.0; 3 structural unlocks needed. |
| `first-principles-top-journal-directions-2026-07-05.md` | 2026-07-05 | 3 counter-direction candidates (PA-degrades, calibration paradox, dual-ledger bridge); none main-track ready. |
| `orchestrated-progress-assessment-2026-07-05.md` | 2026-07-05 | Joint methods paper outline 6-persona median=4.0; FALLBACK to P11 workshop. |
| `post-gate-and-qlib-assessment-2026-07-05.md` | 2026-07-05 | G1 fail, G3 Brier unfinished, G2 strong signal but n=6 < N=30. |

### Verified current state (re-read against `state/progress.json` + per-paper `progress.json` on 2026-07-05 evening)

The state has **moved beyond** what the `post-gate-and-qlib-assessment` doc captured. Current truth:

| Item | Status as of 2026-07-05T03:25:28Z | Evidence |
|---|---|---|
| **G1 PA-degrades-fidelity** | **FAILED** | `state/progress.json:22` — R1=4.0, R3=4.0 < 5.5 gate; median=4.5. Drop as standalone; keep as P11 workshop pillar. |
| **G2 calibration paradox** | **PARTIAL — strong signal, underpowered** | `state/progress.json:24`; `papers/p12-judge-calibration/state/progress.json:19-36` — 1st judge n=10 delta=-1.284 CI [-1.461,-1.078]; 2nd judge (openrouter gpt-oss-120b, 4th distinct provider) n=6 delta=-3.667 CI [-4.0,-3.0]. Effect **strengthened** across judge families, but n=6 < N=30 paired spec. |
| **G3 dual-ledger crosswalk** | **FULL PASS** (NEW since post-gate doc) | `state/progress.json:23` + recent_events 2026-07-05T03:25:28Z — field coverage 92.9% (AR→CWCUP), enums orthogonal, Brier replay 2/2 settlements matched at correct prediction-card version (v0.1 [0.55,0.27,0.18] not v0.2). The post-gate doc's "G3 Brier unfinished" is now STALE. |
| **PIT-NEW-9** (P7 audit-chain) | **FIXED** | `papers/p07-signal-fusion/state/progress.json:111-121` — `snippet_sha256_prefix` now real `hashlib.sha256`; 14/14 tests GREEN. |
| **P12 standalone** | CLOSED | median 3.0, `fold_into_p1_p2`. |
| **P1+P2 standalone** | CLOSED | median 4.0, `fold_into_p12`; pilot_30 power 0.48 at d=0.5 (underpowered). |
| **P8 standalone** | Scaffolding only | median 5.0 (research_grade_acceptable); **no `predicted_p` data** — AB-test is 1-5 judge scores; Brier math ready (17/17 tests) but cannot run on existing data. |
| **P7 standalone** | Scaffolding only | median 5.0; live SignalFusionEngine import blocked on cds-keyperson repo; cross-paper adapter works on synth signals. |
| **Joint methods paper** | FALLBACK | 6-persona review median=4.0 < 4.5 threshold. |
| **P11 (legacy)** | CLOSED 2026-07-03 | 26-review plateau median 5.84-6.60; inter-judge agreement on subjective fidelity 0.19 (near random); Mimo+v5 integration estimated Gate-4 7.5-8.0 at 7-10 days. |

### The falsification question for this investigation
The prior docs say "no top-journal opportunity." But two things changed **after** the most conservative doc was written:
1. **G3 is now a full pass** — the dual-ledger schema bridge to `cds4worldcup` is real, with a working Brier replay on version-paired settlement records. This is a genuine cross-domain methods result that did not exist when `top-journal-readiness` was written.
2. **G2's effect strengthened 3× on a 2nd judge family** — the "blind > leaked" calibration paradox is now cross-provider, not single-judge. (Still n=6 < N=30.)

The pair investigator's job is to **falsify "no top-journal opportunity"**: either confirm it with fresh evidence given the updated state, or surface a credible top-journal angle that the updated state enables.

## Investigator Findings

### TL;DR — Verdict

**CONFIRMED: NO NeurIPS/ICLR/ACL/EMNLP main-track opportunity. Honest ceiling remains workshop / Findings 6.0-7.0.** G3 FULL PASS + G2 cross-provider 3× effect strengthening do **not** unlock a top-journal main-track submission. Three of five falsification agents surfaced **new falsifying evidence** that the prior docs did not surface.

### Method

Five read-only explore agents fanned out in parallel (RepoPrompt `agent_explore`), each with an independent scope and a focused deliverable. Reconcile below.

| Agent | Scope | Verdict |
|---|---|---|
| A (G3 novelty) | Does G3 dual-ledger crosswalk survive novelty check vs GraphRAG / HippoRAG / JANUS / RAGAS / PROV-O? | **NO.** Schema engineering dressed as research. 5-15% main-track survival. |
| B (G2 prior art) | Is G2 strict-on-leaked direction novel vs Li et al. 2026 (Ref-k) and Zheng et al. 2023 (MT-Bench)? | **Plausibly novel but unconfirmed.** Li et al. 2026 (5,421 instances, 5 judges) shows opposite direction. Workshop/Findings only. |
| C (N=30 path) | Cheapest path to N=30 paired for G2? Top-journal deadline alignment? | **N=30 reachable in ~3 days for $0.** But no main-track deadline in 30-60 days. |
| D (cds4worldcup) | Does cds4worldcup settlement corpus give enough events for external validation of G3? | **NO.** Only 2 unique settlement records (not 24 as prior docs claim). Internal cross-domain only. |
| E (joint paper) | Is there a credible single-paper package combining G2+G3+P11-negative-result? | **NO.** Strict subset of joint-methods outline that already failed 6-persona review (median=4.0, FALLBACK, 14h before this investigation). Workshop/Findings 6.5-7.0. |

### Finding 1 (Agent D): The "24 games" claim is false

**Claim from prior docs:** `first-principles-top-journal-directions-2026-07-05.md:39` states "cds4worldcup has 24-game settled outcomes." Repeated in `prompt-exports/oracle-plan-2026-07-05-094329-first-principles-top-b9ad.md:150`.

**Falsification:** Exhaustive filesystem enumeration (`find /Users/tangzw119/Documents/GitHub/cds4worldcup -path "*/settlement/*" -type f`) returns **3 files = 2 unique + 1 archive duplicate**:

| # | Path | Tournament | Match | Settled |
|---|---|---|---|---|
| 1 | `cds4worldcup/artifacts/fixtures/cds4polymarket/settlement/wc2022-g-arg-ksa.settlement_record.yaml` | WC 2022 | Argentina vs Saudi Arabia | 2026-06-10 |
| 2 | `cds4worldcup/artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml` | WC 2026 | Mexico vs South Africa | 2026-06-13 |
| 3 | `cds4worldcup/archive/cds4polymarket/worldcup-2026-factor-calibration/settlement/wc2022-g-arg-ksa.settlement_record.yaml` | (duplicate of #1) | — | Archived |

Sanity-checks: every `*_results.csv` file (match_level, factor_level, judge_adjudication, protocol_failure, knowledge_update, baseline_comparison) is **header-only** (1 line, 0 data rows). The "48-team championship probabilities" referenced in prior docs is a `cds_championship.json` simulation output — WC 2026 has not been played, no ground-truth Brier exists for those.

**3 of 6 prediction cards have no settlement record** despite match dates having passed:
- `wc2026-b-m02-qat-sui` (locked 2026-06-13T18:00:00Z)
- `wc2026-c-m01-bra-mar`
- `wc2026-f-m01-ned-jpn`

**Implication:** cds4worldcup cannot serve as external validation. It is **internal cross-domain** (same author `tangzw119`, same `~/Documents/GitHub/`, same git workflow, sibling repo). Per the project's own G5 definition in `docs/investigations/orchestrated-progress-assessment-2026-07-05.md:38-42`, external validation requires "human inter-rater, gold set, or public benchmark tie-in such as ForecastBench, GAIA, AgentBench, or a domain oracle." cds4worldcup meets none.

### Finding 2 (Agent D): No per-match market baseline, no human inter-rater, no public benchmark join

**No per-match market baseline:** Every prediction card declares `baselines.market_or_odds.status: missing_with_reason` (cited for all 4 inspected cards). The `baseline_suite_registry.csv` declares `market_public_baseline` as "populated, 39/48 teams" but this is at the championship level (Polymarket championship futures snapshot), not per-match W/D/L. There is no `polymarket_implied_p` or `betfair_implied_p` to Brier-compare against the 2 settled matches.

**No human inter-rater:** Both settlement rows take `outcome_90m` from authoritative Wikipedia / FIFA links. n_rater = 1 per match. The codability annotation project (`cds4worldcup/artifacts/annotation/codability-v0.2-cn/`, 300 + 100 kappa) scores Kimi agent reasoning on factor rubrics, NOT match outcomes.

**No public benchmark join:** No ties to ForecastBench (arXiv 2409.19839), FORECAST (NeurIPS 2025 D&B), KalshiBench (2512.16030), Tetlock/Mellers IARPA, FiveThirtyEight SPI, or ESPN Brier. `grep -lir "Betfair"` returns 0 hits in `cds4worldcup`.

### Finding 3 (Agent A): G3 is schema engineering dressed as research

**Closest prior art:**

| System | Venue | Year | What it does | Different from G3 |
|---|---|---|---|---|
| **HippoRAG** (Gutiérrez et al.) | NeurIPS 2024 (arXiv 2405.14831) | 2024 | KG-augmented RAG with PageRank; structured claim-evidence bindings (KG triples + source provenance) | G3 has no retrieval/QA arm |
| **GraphRAG** (Edge et al.) | arXiv 2404.16130 (rev Feb 2025) | 2024-25 | Entity KG + community summaries + citation blocks at chunk level; 26-77% token-cost reduction on global summarization | G3 has no empirical evaluation |
| **RAGAS** | arXiv 2309.15217 / EMNLP 2024 industry | 2023-24 | Faithfulness / Context Relevance / Citation Recall LLM-judge metrics with public benchmarks | G3's `confidence_before/after` + `observed_outcome` echoes these with no head-to-head |
| **PROV-O** | W3C Recommendation | 2013 | Domain-agnostic provenance ontology (Entity / Activity / Agent) for cross-domain interchange | Subsumes G3's "crosswalk" with formal semantics |
| **Schema-matching** (COMA / CUPID / iMAP / HOLISSE) | DB community 2001-2024 | 20+ years | Solved subproblem; standard tools exist | G3 is a 1:1 field map exercise, baseline territory |

**Key falsification points:**
- The G3 artifact itself names the future contribution as "schema-reconciliation paper" (`docs/papers/g3-dual-ledger-crosswalk.md:82`).
- Both schemas are owned by same author/team. Documenting that two internal JSON shapes already overlap is documentation, not research.
- The 2/2 Brier match is on a cherry-picked pair. Per `docs/papers/g3-brier-replay-results.md:9`: "hardcoded file list (not directory traversal) due to sandbox Path.rglob restriction." The script was written to match.
- Joint-methods 6-persona review median=4.0 < 4.5 fallback threshold; G3 was the only structural gate that passed because G3 only tests structural fields, not methods. The structural ease is the falsification — a result that can be obtained by trivial schema inspection is not a research contribution.

**Survival estimates:**
- Top-journal mainline track: **5-15%** (without multi-domain experimental arm)
- Workshop position paper (R0-FoMo, ICML GenAI+Law, NeurIPS Eval Workshop): **~70%**
- Methods section in P12 (existing mainline): **~50%** as a sub-contribution
- Top-journal main-track ≥7.5: requires Requirement A (≥3 paired domains with Brier vs unstructured baseline on ≥100 paired claims) — 30-60 day budget **forbids this**

### Finding 4 (Agent B): G2 strict direction is plausibly novel but Li et al. 2026 is the closest counter-example

**Li et al. 2026 (arXiv:2506.22316, Ant Group, Feb 2026) — Reference Answer Score Bias:**
- Datasets: BiGGen Bench (2,780), FLASK (2,001), MT Bench (320), Vicuna Bench (320). **5,421 instances total.**
- Judges: GPT-4o, DeepSeek-V3-671B, Qwen3-32B, Qwen3-8B, Mistral-Small-24B.
- Construct: judge given reference answer tagged with score k ∈ {1,2,3,4,5}.
- **Direction: LENIENT** (pull toward reference score k). Verbatim: "DeepSeek-V3-671B assigns a score of 5 to more than half of the instruction-response pairs when Ref-5 is provided."
- Effect size (Table 3, p. 9): GPT-4o BiGGen Bench Ref-5: Flip Rate **45.54%**, MAD **0.7166** vs No-Pert 23.63% FR / 0.2865 MAD.
- **Critical structural difference from G2:** Li et al. does NOT have paired blind-vs-leaked on identical instances. They compare no-reference vs reference-with-score-k. G2 compares blind vs full leaked GT on identical instances.

**Other prior art scanned:**
- Zheng et al. 2023 (arXiv 2306.05685, NeurIPS 2023 D&B): catalogs position / verbosity / self-enhancement biases — NO claim about GT leakage direction.
- CALM (NeurIPS Safe GenAI Workshop 2024): 12 biases catalogued, direction not headline.
- OffsetBias (EMNLP Findings 2024): debiasing via curated data, not direction-of-leakage.
- JudgeDeceiver (arXiv 2024): prompt-injection attack, direction = lenient (adversarial goal).
- LLM-as-judge survey (arXiv 2411.16594, ASU 2024): catalogs known biases, no strict-on-leaked claim.

**Verdict on novelty:** **Plausibly novel but unconfirmed.** Li et al. 2026 uses score-tagged references (Ref-k explicit numerical anchor); G2 uses unlabeled leaked GT (implicit content anchor). The bias mechanism may differ — but a deeper bibliography chase is warranted before finalizing the novelty claim. The hypothesis to test: contrast effect (Tversky-Kahneman) where GT provides anchor → candidate evaluated as gap below it → lower score. Different from anchor-pull-toward-k because no explicit "this should be 5" tag is provided.

**Verdict on venue:**
- NeurIPS / ICLR main-track: **NO** (n=16 paired total across 2 judges)
- ACL / EMNLP main: **Borderline** (Li et al. 2026 will be cited by reviewers as the closest counter-example)
- ACL / EMNLP Findings: **Plausible**
- Workshop (EMNLP Eval4NLP, ICLR Workshop on LLM Eval): **Realistic**
- Position / short paper (4pp): **Yes, with reframing** as "Observation: leaked-GT produces strict bias in 2 judge families, opposite direction to Li et al. 2026"

### Finding 5 (Agent C): N=30 paired is reachable in ~3 days for $0; top-journal deadlines are not

**Current state:**
- 1st judge (Paratera deepseek-v4-pro): **n=10 paired**, delta=-1.284, CI [-1.461, -1.078], CI width 0.383
- 2nd judge (OpenRouter gpt-oss-120b): **n=6 paired**, delta=-3.667, CI [-4.000, -3.000], CI width 1.000 (2.6× wider)

**Critical data-loss finding:** The 2nd-judge raw scores live ONLY in the markdown report (`docs/papers/g2-p12-calibration-paradox-replication.md` §3). The 6 paired rows are NOT in `experiments/`. To extend, must re-collect all 6. **No partially-stored 2nd-judge data exists.**

**Path to N=30:**
- 1st judge → N=30: +40 API calls × 25s = **17 min wall time, $0, 1 evening session**
- 2nd judge → N=30: +48 API calls, OpenRouter quota 200/day cap → **2 calendar days minimum**
- Full G2 (both at N=30): **~3 days wall-clock, $0**

**Top-journal deadline alignment:**
- NeurIPS 2026 main track: deadline ~May 2026 — **past, 2 months ago**
- ICLR 2026 main track: deadline ~Jan 2026 — **past, 6 months ago**
- ACL 2026 main track: deadline ~May 2026 — **past, 2 months ago**
- EMNLP 2026 main track: deadline ~June 2026 — **past, 1 month ago**
- NeurIPS 2026 workshops: October 2026 (~3 months out, ~mid-Aug submission)
- ACL Rolling Review (ARR): continuous (~2-3 month review cycle, plausible in 30 days)
- NeurIPS 2027 main track: deadline ~May 2027 (~10 months out)

**Brutal truth:** **No main-track top-journal deadline falls in 30-60 days.** Realistic submission targets are NeurIPS 2026 workshop (mid-Aug) or ARR.

### Finding 6 (Agent E): The proposed G2+G3+P11-neg package is a strict subset of an already-rejected joint-methods outline

**Unifying narrative (working title):**

> When LLM agents self-evaluate, three independent measurement pathologies compose: (1) G2 — LLM judges are **stricter, not lenient**, when handed leaked ground-truth (blind > leaked, opposite of standard leakage-bias); (2) G3 — two independently-evolved evidence-ledger schemas reconcile at 92.9% field coverage with orthogonal enums, showing schema drift is the real barrier; (3) P11-negative-result — structured pure-analysis prompting degrades role-fidelity judges under role conflict. Taken together: LLM-agent evaluation infrastructure must be designed as an end-to-end measurement contract.

**Falsification on the package:** The **closest existing artifact** is the joint-methods paper outline that **already bundles G2 + G3 + settlement + audit** (strict superset of the proposed package). It was reviewed by 6 personas with **median=4.0**, verdict FALLBACK, timestamp 2026-07-04T20:06:18Z (`docs/papers/joint-methods-outline-review.md:20-26`) — **14 hours before this investigation.**

The proposed package swaps "joint methods" for "PA-degrades-fidelity" — but PA-degrades-fidelity's 1-page abstract already failed 5-persona review (R1=4.0, R3=4.0, median=4.5; G1 gate R1+R3≥5.5 failed at sum 8.0). All three paper lines have been independently closed for standalone publication (P12 median 3.0; P1+P2 median 4.0; P11 26-review plateau 5.84-6.60).

**Required additional evidence for main-track (none currently present):**

1. G2 powered to N=30 paired with 2nd judge family (~5-8 API hours)
2. P12 H1c / F1 cells populated (currently n=0 across all protocols)
3. Cross-scenario validation of G2 (currently P11-anchored)
4. Dual-ledger replication on a 3rd system (currently 2-system only)
5. Frontier-model baseline arm (GPT-5 / Claude-Opus-4 / Gemini-3 — currently zero)
6. Human inter-rater or external benchmark tie-in (currently zero)
7. Joint-review re-pass on the unified paper itself (must re-pass median≥5.5)

### Finding 7 (Agent E): Honest ceiling and reframe options

**Ceiling assignment:**

| Venue tier | Verdict | Evidence |
|---|---|---|
| NeurIPS / ICLR / ACL / EMNLP main-track (≥7.5) | **NO** | Joint-methods outline 4.0 < 4.5; proposed package is weaker; structural unlocks absent |
| ACL / EMNLP Findings, NeurIPS D&B (7.0-7.5) | **Borderline, only if G2 powered to N=30** | Ceiling ~7.0 per prior assessments |
| Workshop (6.0-7.0) | **YES, plausible target** | Consistent 6.5-7.0 ceiling across all 4 prior same-day assessments |
| Below workshop (≤6.0) | **NO** if framed as joint submission | |

**Alternative framings (ranked by honesty, not optimism):**

| Framing | Ceiling | Best venue | Pros | Cons |
|---|---|---|---|---|
| **E. Empirical-study: "The blind-judge paradox: 3 independent replications of an under-reported leakage direction"** | 6.5-7.5 (workshop/Findings) | EMNLP / ACL Findings on eval methodology | Smallest scope, highest single-finding novelty; G2 2nd judge 3× effect IS publishable | Drops G3+P11; only n=6 on 2nd judge |
| **A. Position paper: "LLM-agent evaluation infrastructure is broken at every layer"** | 6.5-7.5 (workshop/Findings) | ACL/EMNLP Findings, AI eval workshops | No new runs needed; reviewer-noise literature is open | Novel-claim threshold lower for Findings than main-track |
| **D. Methods paper: "An audit contract for LLM-agent evaluation"** | 6.5-7.0 (workshop) | ICSE / FSE / AI engineering workshops | Reframes 14-field ledger + 5-protocol + signal-fusion as audit/provenance contract; novelty lane open | P7 PIT-NEW-9 is a defect, not a contribution |
| **C. Negative-results: "Three counter-intuitive measurements"** | 6.0-7.0 (workshop) | ReScience / ML Reproducibility Challenge / ICLR Failure Modes | Existing venues; lowest novelty ceiling | R4 score 2.0 on G1 abstract suggests at least one reviewer disbelieves the finding |

**Best path within reach:** Framing E + Framing A combined. Lead with G2 calibration paradox (1st judge n=10 + 2nd judge n=6 with 3× effect strengthening), make G3 the cross-domain validation appendix, re-cast P11 negative result as measurement-contract discussion section. This is the joint-methods outline but **stricter** (smaller claim, smaller scope) — must re-pass 6-persona review threshold (median ≥ 5.5) before submission.

**Two structural unlocks needed for main-track ≥7.5:**
1. **Scenario diversification** — ≥3 independent scenarios beyond Gulei 2015 + commercial_space (4-8 weeks of human curation, NOT token-bounded)
2. **Frontier-model baseline** — GPT-5 / Claude-Opus-4 / Gemini-3 arm on at least one cell (1-2 weeks API budget, currently zero)

Without those, no framing reaches main-track ≥7.5.

### Evidence Quality Summary

| Claim from prior docs | New evidence | Honest reassessment |
|---|---|---|
| G3 dual-ledger PASS (post-gate) | 92.9% field + 2/2 Brier match | **STRUCTURAL PASS, EMPIRICALLY TRIVIAL.** 2/2 is on cherry-picked pairs with hardcoded file list. Schema engineering, not research contribution. |
| G2 effect strengthening 3× on 2nd judge | 1st judge n=10 + 2nd judge n=6, both CI<<0 | **DIRECTION PLAUSIBLY NOVEL BUT UNDERPOWERED.** Li et al. 2026 has opposite direction on 5,421 instances × 5 judges. Needs N=30 + 3rd judge + controlled mechanism experiment. |
| 24-game cds4worldcup settled corpus | 2 unique settlement records | **CLAIM FACTUALLY FALSE.** Same author, same git tree, no per-match market baseline, no human inter-rater, no public benchmark join. Internal cross-domain, not external validation. |
| Workshop/Findings 6.0-7.0 ceiling | Joint-methods outline 4.0 < 4.5 (14h ago) | **CEILING CONFIRMED.** Strict subset of failed joint-methods outline. No structural unlocks present. |
| Top-journal main-track opportunity | NeurIPS / ICLR / ACL / EMNLP 2026 main all past | **NO 30-60 DAY MAIN-TRACK DEADLINE EXISTS.** NeurIPS 2026 workshop (~mid-Aug) or ARR are realistic targets. |

### Recommendations (Investigation-Specific)

**Do NOT re-attempt main-track framing.** Instead, sequenced within 30 days:

1. **Tonight:** Run 17-min Paratera extension → 1st judge N=30 paired ($0). Persist raw responses to `experiments/g2_judge_results.json` so they aren't lost this time.
2. **Days 2-3:** OpenRouter 2nd judge → N=30 paired (quota-bound, 2 days). Persist raw responses properly.
3. **Days 4-7:** Draft workshop short paper (4-8 pages) using Framing E + Framing A combined. Lead with G2 paradox, append G3 as cross-domain validation, relegate P11 to discussion. Submit to NeurIPS 2026 workshop on AI Evaluation (or similar) by mid-August.
4. **Parallel:** Submit to ARR for next-cycle main-track evaluation (results land in time for NeurIPS 2027 if accepted first round).
5. **Background (NOT token-bounded):** Begin scenario diversification (≥3 new domains beyond Gulei + commercial_space). This is the only path to ≥7.5 main-track ceiling.

### Final Verdict

**CONFIRM NO TOP-JOURNAL MAIN-TRACK OPPORTUNITY.** Honest ceiling: workshop / Findings 6.0-7.0. Updated state (G3 full pass + G2 cross-provider 3× effect) does not change this. Required for main-track ≥7.5: scenario diversification + frontier-model baseline (weeks-to-months, not token-bounded).

### Citations (every claim file:line or URL)

**Prior investigation docs (referenced but not updated):**
- `auto-research/docs/investigations/post-gate-and-qlib-assessment-2026-07-05.md:13-15` — G3 partial pass, G2 partial pass
- `auto-research/docs/investigations/first-principles-top-journal-directions-2026-07-05.md:39` — "24-game settled outcomes" CLAIM FALSE
- `auto-research/docs/investigations/orchestrated-progress-assessment-2026-07-05.md:36-44` — structural unlocks
- `auto-research/docs/investigations/top-journal-readiness-2026-07-05.md:147-186` — prior ceilings

**State / paper files:**
- `auto-research/state/progress.json:22,23,24,78-80` — G1 fail, G3 FULL PASS, G2 PARTIAL, G3.3 Brier 2/2
- `auto-research/papers/p12-judge-calibration/experiments/calibration_metrics.md:9-13, 28-30, 73-77` — G2 evidence
- `auto-research/docs/papers/g2-p12-calibration-paradox-replication.md:16-17, 38-39` — G2 replication
- `auto-research/papers/p1p2-evidence-ledger/wiki/concepts/evidence-ledger-schema.md` — schema details
- `auto-research/docs/papers/g3-dual-ledger-crosswalk.md:43, 50-58, 82` — G3 claims
- `auto-research/docs/papers/g3-brier-replay-results.md:9, 46-47` — G3 Brier replay
- `auto-research/docs/papers/joint-methods-outline-review.md:11-26` — joint-methods FALLBACK
- `auto-research/papers/p12-judge-calibration/paper/review_round_1.md:25-28` — P12 standalone close
- `auto-research/papers/p1p2-evidence-ledger/paper/review_round_1.md:11-26` — P1+P2 standalone close
- `auto-research/legacy/p11-closed-v5-minimax-m3/paper/main.tex:36-48, 140-148` — P11 evidence
- `auto-research/legacy/p11-closed-v5-minimax-m3/CLAUDE.md:35-43` — P11 PA-degrades-fidelity

**Prior-art URLs:**
- https://arxiv.org/abs/2405.14831 — HippoRAG (NeurIPS 2024)
- https://arxiv.org/abs/2404.16130 — GraphRAG (Edge et al. 2024)
- https://arxiv.org/abs/2309.15217 — RAGAS (EMNLP 2024 industry)
- https://www.w3.org/TR/prov-o/ — PROV-O (W3C Recommendation 2013)
- https://arxiv.org/abs/2506.22316 — Li et al. 2026, "Evaluating Scoring Bias in LLM-as-a-Judge"
- https://arxiv.org/abs/2306.05685 — Zheng et al. 2023, MT-Bench (NeurIPS 2023 D&B)
- https://arxiv.org/abs/2411.16594 — LLM-as-judge survey (ASU 2024)
- https://arxiv.org/abs/2409.19839 — ForecastBench

**cds4worldcup corpus (verified by exhaustive enumeration):**
- `cds4worldcup/artifacts/fixtures/cds4polymarket/settlement/wc2022-g-arg-ksa.settlement_record.yaml`
- `cds4worldcup/artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml`
- `cds4worldcup/archive/cds4polymarket/worldcup-2026-factor-calibration/settlement/wc2022-g-arg-ksa.settlement_record.yaml` (duplicate)
- `cds4worldcup/artifacts/fixtures/cds4polymarket/predictions/mvpa/wc2026-a-m01-mex-rsa.prediction_card.yaml` (v0.1, p=[0.55,0.27,0.18])
- `cds4worldcup/artifacts/fixtures/cds4polymarket/predictions/mvpa/wc2026-a-m01-mex-rsa.v0.2.prediction_card.yaml` (v0.2, p=[0.62,0.23,0.15])
- `cds4worldcup/artifacts/fixtures/cds4polymarket/predictions/phase-minus1/wc2022-g-arg-ksa.prediction_card.yaml`
- `cds4worldcup/artifacts/plan-c/predictions/wc2026-{b-m02-qat-sui,c-m01-bra-mar,f-m01-ned-jpn}.prediction_card.yaml` (no settlement)

## Investigation Log

### Phase 0 - Workspace Verification
**Hypothesis:** auto-research workspace is loaded in RepoPrompt window 3.
**Findings:** `rp-cli -e 'windows'` → window `3` workspace `auto-research` (34 tabs). `rp-cli -w 3 -e 'tree --type roots'` → root `/Users/tangzw119/Documents/GitHub/auto-research` present (plus `cds4worldcup`).
**Evidence:** rp-cli output 2026-07-05.
**Conclusion:** Confirmed.

### Phase 1 - Initial Assessment & State Verification
**Hypothesis:** The 4 prior same-day docs answer the question, but the state has moved since the most conservative one; verify before relying.
**Findings:** Re-read all 4 active-paper `progress.json` + top-level `state/progress.json`. G3 advanced to FULL PASS at 03:25:28Z (after `post-gate-and-qlib-assessment` was written). G2 still partial. PIT-NEW-9 fixed. G1 failed. Joint methods fallback.
**Evidence:** `state/progress.json:1-79`, `papers/p12-judge-calibration/state/progress.json:1-37`, `papers/p1p2-evidence-ledger/state/progress.json:1-176`, `papers/p08-market-calibration/state/progress.json:1-69`, `papers/p07-signal-fusion/state/progress.json:1-122`.
**Conclusion:** Prior "no top-journal" verdict is stale on G3 (it's now a full pass) but still likely directionally correct. Dispatching pair to falsify.

## Root Cause
<!-- Filled after synthesis. -->

## Recommendations
<!-- Filled after synthesis. -->

## Preventive Measures
<!-- Filled after synthesis. -->
