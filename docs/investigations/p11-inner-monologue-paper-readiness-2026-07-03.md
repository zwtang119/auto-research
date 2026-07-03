# Investigation: p1.1 Inner Monologue Paper Readiness

## Summary
Final decision: **take the workshop fallback now, with a 14-day hard stop and no new major experiments**. The most evidence-supported move for a 60-point paper is to package the existing v5.3 data plus the label-leakage finding into a workshop submission, not to continue repair loops or start the v4 CDS Benchmark W2 path.

Rationale: v5 already has 927 runs and 1,824 judge calls; review scores have plateaued across 26 rounds at roughly 5.84-6.60; the original H1 collapsed under blind judging; and the v4 CDS Benchmark is unvalidated with a fallback that itself implies 9,000 runs and 2-3 months. The active problem is path-selection oscillation, not data scarcity.

## Symptoms
- The project contains multiple p1.1 inner-monologue experiment generations: `legacy/p11-legacy-snapshot-2026-07`, `legacy/p11-closed-v5-mimo`, and `legacy/p11-closed-v5-minimax-m3`.
- The most advanced generation appears to include experiment harnesses, logs, paper draft artifacts, and a `ROADMAP-to-8.5.md`, but it is unclear whether the next best step is repair, more experiments, more analysis, or paper-topic reframing.
- User target: a "60-point" publishable paper, with `/Users/tangzw119/Downloads/Towards a Science of Scaling Agent Systems.pdf` as a "100-point" reference ceiling; fallback target is a quickly publishable workshop-level paper.

## Background / Prior Research
### External Reference: "Towards a Science of Scaling Agent Systems"
Explore agent `DA75FF61-61A9-4778-8D60-9E71161942E2` read `/Users/tangzw119/Downloads/Towards a Science of Scaling Agent Systems.pdf` and related Downloads material using the PDF skill.

Key benchmark takeaways:
- The reference paper is a 100-point benchmark because it combines 180 configurations, 3 LLM families, 4 agentic benchmarks, 5 architecture variants, identical prompts/tools/token budgets, a 20-parameter mixed-effects predictive model, and out-of-sample validation on a future model.
- Its core "secret weapon" is not just scale but a prescriptive architecture-selection rule with 87% held-out accuracy.
- A realistic 60-point p1.1 paper should preserve cross-model and cross-prompt-strategy evidence, identical-budget hygiene, and 1-2 mechanism narratives, but should not promise a universal scaling law, an 87%-style predictor, or future-model validation.
- A workshop fallback can be a clean negative/counter-intuitive result: inner monologue does not improve, and may reduce, decision emergence in commercial-space multi-agent scenarios; reuse existing 240 runs plus a small replication if needed.
- The agent recommended repricing the v4 W2 gate in `legacy/p11-closed-v5-minimax-m3/docs/superpowers/specs/2026-07-03-cds-benchmark-design.md` section 6.1: replace a hard 1.5x-from-360-runs trigger with a conjunctive gate around 1.3x baseline, Cliff's delta >= 0.4 in both DeepSeek and Qwen, and a visible ablation gap.

### Project Evolution / Git Archaeology
Explore agent `AB22F9DB-4BAD-4F2A-9F53-BCDCD3F40BAE` investigated the p1.1 workspace evolution and recent git state.

Key chronology:
- G1 `legacy/p11-legacy-snapshot-2026-07`: M1-only DeepSeek-V4-Pro scaffold; abandoned before full evidence.
- G2 `legacy/p11-closed-v5-mimo`: full pipeline to about 7.0/10; closed deliberately because more samples could not fix single-scenario/model/theory limitations.
- G3 `legacy/p11-closed-v5-minimax-m3`: current frontier; despite the directory name, the experiment uses DeepSeek-V4-Flash and Qwen3.5-122B, with "Minimax M3" only as chat LLM context.
- G3 has progressed through H1 failure, label leakage discovery, H1c reasoning-depth pass, H1-continuity pass, H1-auditability fail, v4 CDS Benchmark pivot, v5/v5.3 experiments, and comprehensive synthesis by 2026-07-03.

Current state per explore agent:
- G3 includes roughly 240 earlier single/group runs plus v5 artifacts around 750 A runs, 90 A1 runs, 72 C runs, 1,500 judge scores, and two paper-draft directions.
- Robust findings include H1 fidelity ceiling/failure, H1c reasoning depth pass, H3 gene-to-behavior pass, low subjective-fidelity judge agreement, high objective/risk-taking agreement, and a counter-intuitive group-emergence result where pure analysis beats inner monologue.
- Open structural issues include non-MECE mode definitions, fidelity ceiling, DeepSeek judge parse failures, low inter-rater agreement for emergence modes, unsupported causal path from reasoning depth to fidelity, and residual spec drift.
- The recent trajectory is not "repair only" or "more experiments only"; it is a path-selection loop. The explore agent's recommended next move is a hard choice between the v4 CDS Benchmark W2-checkpoint path and the workshop-paper fallback, avoiding another v5.4/v6 spec revision.

## Investigator Findings

### F1. v5 Data Completeness — VERIFIED, with one structural caveat

| Check | Status | Evidence (file:line) |
|---|---|---|
| v5 run count (927 = 750+90+72+15 pilot) | ✅ Verified | `experiments/h5-emergence/metadata.json:131-133` (`"total_runs_yaml": 927, "total_judge_calls": 1824`) |
| Pilot 15 runs complete | ✅ | `metadata.json:8-12` (n_runs=15) |
| A 5-condition MECE complete | ✅ | `metadata.json:13-23` (750 runs, 5 conditions, 50/cell, 2 judges) |
| A1 baseline_io negative control complete | ✅ | `metadata.json:24-34` (90 runs, baseline_io × 3 ent × 30) |
| C 4-mode transfer test complete | ✅ | `metadata.json:35-45` (72 runs, 4 modes × 3 ent × 2 models × 3) — `multi_strategic_shift` correctly removed (1-run measurability issue) |
| A2b A inter-rater ICC | ✅ | `metadata.json:46-65` — overall ICC=0.707 moderate, per-dim 0.50-0.794 |
| A2_C C inter-rater Cohen's κ | ✅ | `metadata.json:66-81` — pooled κ=0.183 (slight/poor) |
| A_kw_fdr.json | ✅ | `experiments/h5-emergence/analysis/A_kw_fdr.json:36-40` — `H=54.086, p=0.0, significant=true`; valid_runs_per_judge `{DeepSeek: 551, Kimi: 750}` confirms 199 DeepSeek parse failures |
| A1_baseline_vs_pure.json | ✅ | `experiments/h5-emergence/analysis/A1_baseline_vs_pure.json:1-9` — `t=-3.391, p=0.0008, Cliff's δ=-0.162` |
| C_emergence_freq.json | ✅ | `experiments/h5-emergence/analysis/C_emergence_freq.json:1-15` — 72 paired runs, 4-mode frequency, DS vs QW chi²=2.949 p=0.40 |
| Cost in $25-79 range | ✅ | `metadata.json:134` (matches spec v5.3 §7 estimate $24-76) |
| 2758 yaml files in h5-emergence (includes judge yaml) | ✅ | `find experiments/h5-emergence -name '*.yaml' -o -name '*.json'` |

**Structural caveat (F1.1)**: The 26.5% DeepSeek parse failure (`A_kw_fdr.json:28-29`) leaves only 551/750 valid scores from DeepSeek judge (Kimi 750/750). This is already in `metadata.json:135-137` notes and the A2b `per_dimension_icc.financial_depth=0.50` (`metadata.json:57`) is the most fragile dimension — confirms the known weak point. **Implication**: Analysis is already correctly filtered to valid scores, but any A-paper relying on per-dimension analysis must caveat financial_depth and consider Gold-Calibration rerun (per spec v5.3 §2.4 thresholds 0.5/1.0).

**Caveat (F1.2)**: A2_C pooled κ=0.183 means **judges disagree on emergence-mode attribution** (mode frequency ranking is preserved per chi², but per-run labels are noisy). The 3/4 "transfer" finding rests on ranking not on per-run labels. A C-paper must reframe "transfer" as "rank-preserved" not "label-agreement".

---

### F2. Paper Readiness Plateau — VERIFIED at 5.84-6.60 (26 rounds)

| Check | Status | Evidence (file:line) |
|---|---|---|
| Paper1 (workshop) median 5.2 | ✅ | `wiki/decisions/2026-07-03-comprehensive-synthesis.en.md:60-67` (R2/R5 binding at 4.5) |
| Paper2 (transfer) median 5.0 | ✅ | `wiki/decisions/2026-07-03-comprehensive-synthesis.en.md:69-74` (R4_synthesizer 3.0 binding) |
| 26 review rounds, real median ~6.0 | ✅ | `wiki/annotations/paper-review-rounds.md:64-82` (Round 22-26: 5.84→6.60→6.0→6.24→6.5→6.04; ±0.5 noise dominant) |
| Text-repair loop saturated (6.0-6.6 plateau) | ✅ | `paper/ROADMAP-to-8.5.md:23-28` ("修复 #1+#2+#3+#5...约 1-2 迭代", but 11+ rounds prove text repair saturates) |
| H1 fidelity ceiling (DeepSeek 0.03, Kimi -0.02) | ✅ | `state/progress.json:33`; `wiki/decisions/h1-reformulation.md:23-25` |
| H1 blind (label-leakage corrected): δ=-0.04, p=0.73 | ✅ | `wiki/decisions/blind-judge.md:22-27`; `state/progress.json:43` |
| H1c reasoning depth pass (DS 0.70, QW 0.66) | ✅ | `state/progress.json:34`; `paper/main.tex:27-28` |
| H3 Spearman robust (DS 0.82, Kimi 0.75, QW 0.73, Emergency 0.92, blind 0.76) | ✅ | `state/progress.json:35`; `wiki/concepts/workshop-tier-paper.md:101` |
| Inter-judge fidelity κ=0.19 (low), risk_taking 0.74 (high) | ✅ | `state/progress.json:36-37` |
| main.tex is real workshop-tier paper (not stub) | ✅ | `paper/main.tex:1-99` — full abstract + 3 research questions + RoleDNA 6-dim definition + Related Work, label-leakage headline, H1/H1c/H3/H4 claims |
| Three framing candidates: F1 emergence, F3 Spearman, F2 (planned but unbuilt) | ✅ | `wiki/decisions/h1-reformulation.md:34-95`; F1+F3 data-passed, F2 rejected in synthesis |

**Key observation (F2.1)**: The main.tex abstract already front-loads the *methodology* contribution (label-leakage failure mode) and the *counter-intuitive* finding (pure > inner on emergence, 1.5×, Cliff's δ=0.75/0.96, p<0.001) — i.e., the strongest available stories are already in the paper. **The plateau is not from narrative poverty; it is from R2_theorist's binding 4.5 (theorist sees no theory contribution) and R4/R5 binding 3.0-4.5 (single-scenario, single-LLM-family concerns).** Text repair cannot address these structural concerns.

**Key observation (F2.2)**: H1 has been "broken twice" (`h1-reformulation.md:23-28`): first the ceiling artifact, then the label-leakage collapse. The honest paper story is *label-leakage methodology + H1c/H3/F1 robust findings*. The paper already commits to this in `main.tex:23-28`. The plateau is structural, not presentational.

---

### F3. Decision Docs and Specs — VERIFIED, with one inconsistency

| Check | Status | Evidence (file:line) |
|---|---|---|
| Comprehensive synthesis (CN + EN) exists with 3-option recommendation | ✅ | `wiki/decisions/2026-07-03-comprehensive-synthesis.md:1-419`; `...en.md:1-200+` |
| cds-benchmark-design.md v1.1 has W2 hard checkpoint | ✅ | `docs/superpowers/specs/2026-07-03-cds-benchmark-design.md:204-220` (360 runs trigger, fallback to v3.2.1 if hybrid < 1.5× baseline) |
| v5-minimal-plan.md v5.3 with 945→927 runs | ✅ | `docs/superpowers/specs/2026-07-03-paper-v5-minimal-plan.md:1-396` (v5.3: removed multi_strategic_shift, added A2b) |
| Paper1 / Paper2 drafts exist | ✅ (drafts in `paper/`) | `paper/main.tex` (workshop tier) + `paper/results.tex` |
| ROADMAP-to-8.5.md with 7 weaknesses | ✅ | `paper/ROADMAP-to-8.5.md:9-18` |
| h1-reformulation.md with F1/F2/F3 | ✅ | `wiki/decisions/h1-reformulation.md:34-95` |
| blind-judge.md with leakage discovery | ✅ | `wiki/decisions/blind-judge.md:1-77` |
| CDS-Benchmark v4 is designed but UNVALIDATED | ✅ | `cds-benchmark-design.md:1-238` — **no `h5-emergence/cds-benchmark/` data; only 50-pilot + 360-W2 planned, not executed** |

**Inconsistency (F3.1)**: The synthesis doc (`comprehensive-synthesis.md:330-356`) recommends the CDS-Benchmark hybrid path with 3-4% probability of main-conf 7.5-8.0 and ~95% probability of workshop 6.5-7.0 (via fallback to v3.2.1). But the *fallback itself* (v3.2.1) is described as 9,000 runs / 2-3 months (`cds-benchmark-design.md:212-215`). The "95% workshop fallback" timeline is therefore *not* 2-3 weeks — it is 2-3 months of additional work. This misrepresents the time cost of the fallback path.

**Observation (F3.2)**: The cds-benchmark-design v1.1 has been "approved (brainstorming complete, direction 1)" (`cds-benchmark-design.md:6`) but is in the *designed-not-executed* state. The v5 spec (also approved) is the actually-executed v5.3 plan. The v4 plan has no run history. The W2 hard checkpoint (360 runs) is a future commitment, not a current data point.

---

### F4. G2 Closure vs G3 Progress — VERIFIED, confirms structural ceiling

| Check | Status | Evidence (file:line) |
|---|---|---|
| G2 (legacy/p11-closed-v5-mimo) closed at 7.0 | ✅ | `legacy/p11-closed-v5-mimo/state/progress.json:8,10,29-33` (`status: P1.1_CLOSED_7.0`, `current_milestone: CLOSED`) |
| G2 closure_reason: "Marginal gain 7.0→8.0 not justified; core limitations (single scenario/model/theory) not solvable by more samples" | ✅ | `legacy/p11-closed-v5-mimo/state/progress.json:33-34` |
| G2 used different scenario (gulei_petrochemical) | ✅ | `legacy/p11-closed-v5-mimo/state/progress.json:14` |
| G2 had 150 runs, 1050 findings, 4 figures | ✅ | `legacy/p11-closed-v5-mimo/state/progress.json:18-31` |
| G2 trajectory: 5.0→6.0→6.5→7.0 (4 rounds to closure) | ✅ | `legacy/p11-closed-v5-mimo/state/progress.json:30` |
| G3 current median 5.84-6.60 (26 rounds, plateau) | ✅ | `paper-review-rounds.md:64-82` |
| G3 has different scenario + cross-model + label-leakage discovery | ✅ | `state/progress.json:14` (commercial_space_3ent), `:20-22` (DeepSeek+Qwen), `blind-judge.md` |

**Comparison (F4.1)**: G2 closed at 7.0 in 4 rounds; G3 has run 26 rounds and plateaus at 5.84-6.60. The two situations are *not the same*:
- G2 closed because **the marginal gain from another round was small** — 7.0 had reached the structural ceiling for gulei_petrochemical / single-scenario / single-judge work, and the closure_reason explicitly identified the unfixable structural limits.
- G3 is on a *different scenario* (commercial_space_3ent, multi-judge) and has *more evidence* (240 → 927 runs, plus label-leakage finding). G3 should not close at 5.84-6.60 just because G2 did — G3's ceiling appears to be **a different 5.84-6.60 ceiling** driven by **different** structural issues (R2_theorist 4.5 binding on theory, R4_synthesizer 3.0 binding on transfer-claim).

**Implication (F4.2)**: G2's closure rationale (close when 7.0→8.0 marginal not justified) **does not directly transfer** to G3 because (a) G3 has not yet reached 7.0, and (b) G3's structural issues are R2/R4/R5 binding 3.0-4.5, not R1-experimentalist. The honest read: G3 needs *either* a CDS-Benchmark-type structural change to break 6.0, *or* a deliberate decision to stop at 6.0-6.5 and ship a workshop paper.

---

### F5. Cross-cutting observations

**(F5.1) Three loops confirmed and diagnosed**: The synthesis doc (`comprehensive-synthesis.md:209-220`) names three feedback loops. I confirm:
- Loop 1 (text repair): stable at 6.0 — 26 rounds prove it (`paper-review-rounds.md:64-82`).
- Loop 2 (H1): broken by both ceiling and label-leakage. Already pivoted to H1c/H3/F1. **This is no longer a loop, it is a closed finding**.
- Loop 3 (path selection): 12+ paths, no stable attractor. Confirmed in `comprehensive-synthesis.md:222` ("v1 → v2 → v3 → v4 → v3.2.1 → v4 → CDS Benchmark → 12 paths → 决策疲劳"). This loop is the active pathology.

**(F5.2) The 60-point target framing**: The synthesis doc (`comprehensive-synthesis.md:323-355`) frames the 7.0+ as 3-4% likely via hybrid, 95% via fallback. The Mimo reference paper is 100-point. A 60-point paper is more modest — a workshop paper with strong methodology, clean negative result, and open-source tool, scoring 6.0-6.5 median. **The 60-point target is reachable from the current state with 2-3 weeks of focused packaging, without any new experiments**.

**(F5.3) What's actually publishable today**:
- Label-leakage failure mode in LLM-judge role-consistency evaluation (`blind-judge.md:60-66`) — **methodological contribution**, under-elevated in current paper.
- Counter-intuitive emergence finding: pure > inner on emergence, δ=0.75/0.96 dual-generator (`h1-reformulation.md:51-56`) — **novel empirical finding**, well-replicated.
- H1c reasoning-depth result: 874 vs 472 tokens, δ=0.70, no judge (`paper/main.tex:27-28`) — **objective behavioral signal**, immune to label-leakage.
- H3 Spearman: risk_tolerance gene → risk-taking behavior, ρ=0.76 blind (`state/progress.json:35`) — **6-dim framework de-mythologized to 1+5**.

These four findings form a coherent workshop-paper story: *"Inner monologue is a *process signal*, not a *fidelity lever*: it makes reasoning longer, but does not move behavioral fidelity once LLM-judge anchoring is controlled for. In multi-agent groups, structured analytical prompting produces more emergence vocabulary than character immersion."* The story is honest, methodologically careful, and structurally novel — i.e., it is a real contribution, not a "scaffold up to 8.5" exercise.

---

## Recommendation

### Single recommendation: **Workshop-paper fallback path with hard 14-day stop** (Option 2 of comprehensive synthesis, executed in 14 days not 2-3 months)

**Rationale**:
1. **60-point target is reachable today.** Workshop paper with median 6.0-6.5 (Gate 4 from `paper-review-rounds.md:82`, "real stable median 6.0") is consistent with a 60-point target. Main-conf 7.0+ is not reachable in 14 days, given 26 rounds of plateau and an unvalidated 360-run CDS-Benchmark that even its own designer rates 3-4% (`comprehensive-synthesis.md:347`).
2. **The 3+ feedback loops in F5.1 all point to "stop the path-selection cycle"**, not "add another experimental iteration." The G2 closure rationale (`legacy/p11-closed-v5-mimo/state/progress.json:33`) is the correct template: G2 closed at 7.0 because the marginal gain was not justified. G3's honest equivalent is "close at 6.0-6.5 because main-conf 7.0 marginal is not justified, and ship a workshop paper."
3. **The v4 CDS-Benchmark is the wrong next step for 60 points.** It is 1 month of work with 3-4% main-conf success rate and a v3.2.1 fallback that itself takes 2-3 months. The expected-value calculus fails for a 60-point target.
4. **The "do nothing" option (status quo) is unacceptable.** Without an explicit decision, Loop 3 (path-selection oscillation) will continue, and 7-14 days will be consumed without shipping.

### Why NOT the other options
- **Repair** (text iterations on existing paper): Loop 1 is *proven* saturated at 6.0-6.6 over 26 rounds. Continuing this is the high-cost, low-EV option.
- **More experiments** (e.g., CDS-Benchmark W2, or v3.2.1 9,000 runs): 1-3 months of work, ≤5% main-conf probability, and the CDS-Benchmark is *unvalidated* (F3.2). The Mimo 100-point reference is out of reach in 14 days regardless.
- **Paper-topic reframing** (e.g., 18 options list in synthesis): This is *another* path-selection loop iteration. The right reframing was already done in `h1-reformulation.md` (F1+F3 selected, F2 rejected). Re-reframing is a delay tactic.
- **Workshop fallback (immediate, 2-3 weeks)**: This is the *honest* 60-point move. Use existing 927 runs + label-leakage finding.

---

## 7-14 Day Plan for the 60-Point Workshop Paper

**Total duration**: 14 days. **Hard stop**: Day 14 submission. **No new experiments**. **No spec revisions**.

| Day | Task | Output | File:line target |
|---|---|---|---|
| 1 | **Decision lock-in**: write hard-fallback clause in `state/checkpoint.md` and `wiki/decisions/workshop-commit.md` (NEW). Stop all other paths. Update `state/progress.json` status to `WORKSHOP_COMMIT_14D`. | Decision doc | `state/checkpoint.md:2` |
| 2 | **Reframe paper around 4 pillars** (rewrite abstract + intro §1): (1) label-leakage methodology, (2) H1c reasoning-depth signal, (3) F1 counter-intuitive emergence, (4) H3 Spearman (6-dim → 1+5) | Updated `main.tex` | `paper/main.tex:7-43` (abstract) |
| 3 | **Restructure results.tex** to make 4-pillar story explicit; add subsection on label-leakage as primary methodological contribution (currently buried as a fix) | Updated `results.tex` | `paper/results.tex` (full file) |
| 4 | **Generate 4 publication-quality figures**: (a) emergence-vocab bar chart (pure > inner > no_think, dual gen), (b) reasoning-depth boxplot, (c) H3 Spearman scatter with regression line, (d) label-leakage before/after Cliff's-δ plot | 4 figures in `paper/figures/` | `paper/figures/` (currently empty/missing) |
| 5 | **Gold-Calibration rerun on 50-run sample** to address financial_depth ICC=0.50 weak spot — do NOT rerun the full 750, just enough to demonstrate Gold-Cal fix for 1 dimension | Updated A_kw_fdr + add `paper/figures/gold_cal_financial_depth.pdf` | `experiments/h5-emergence/analysis/A_kw_fdr.json:24-29` |
| 6 | **Add Pairwise Blind judge** as second metric (per cds4polymarket borrowing): rerun 30 random runs with pairwise blind vs single blind, report Cohen's d for the 4 pillars | Add `experiments/h5-emergence/analysis/pairwise_blind.json` | NEW analysis file |
| 7 | **Tectonic compile** main.tex; fix any layout issues; add figures; produce main.pdf for round 27 review | `paper/main.pdf` updated | `paper/main.pdf` |
| 8 | **Round 27 automated review** (5 reviewers); record in `experiments/.../review/round_27.json`; compute median | Round 27 review JSON | `experiments/mc-2026-07-01-inner-monologue/review/` (existing path) |
| 9 | **Triage round 27 weaknesses**: keep all 3 "structural" (financial_depth, R2_theorist, R4_synthesizer) as honest limitations; fix presentation/narrative issues only | Updated `main.tex` | `paper/main.tex` |
| 10 | **Re-elevate label-leakage contribution**: promote from "methodology footnote" to §3 dedicated subsection with 1-2 pages, framing as "LLM-judge anchoring failure mode in role-consistency evaluation" | New §3 in `main.tex` | NEW section in `paper/main.tex` |
| 11 | **Round 28 review**; if median ≥6.3, lock abstract and intro | Round 28 JSON; final `main.tex` | `paper/main.tex` |
| 12 | **Final compile + reference cross-check** (104 refs verified, no fabricated citations per ROADMAP hard-constraint) | `main.pdf` final | `paper/main.pdf`, `paper/references.bib` |
| 13 | **Venue selection**: ACL 2027 / EMNLP 2027 / NeurIPS 2027 *workshop* track (not main conf) — pick 1-2 targets, draft cover letter, draft 100-word summary for workshop track | Venue list + cover letter | NEW doc `state/submission_targets.md` |
| 14 | **Submit**. Update `state/checkpoint.md` to `M5_workshop_submitted`. Update `state/progress.json` status. | Submission confirmation | `state/progress.json:3` |

**Hard stop conditions**:
- If at Day 11 round-28 median < 5.8: **abort**, write a 1-page workshop *extended abstract* (2-3 pages, 1 figure), submit that instead at Day 14.
- If at Day 14 submit gate fails (e.g., references incomplete, compile errors): **fix in <2h and submit anyway**. The cost of one more day of delay > the cost of an imperfect submission.

**Things explicitly NOT in this plan** (deliberately):
- ❌ CDS-Benchmark 360-run W2 (unvalidated, 1 month, 3-4% main-conf probability)
- ❌ v3.2.1 9,000-run fallback (2-3 months, low ceiling)
- ❌ New LLM-judge runs (use the existing 1,824 judgments)
- ❌ New scenarios / new models (G2 already proved "more samples won't fix this")
- ❌ Round 29+ on the current paper (text-repair loop is *proven* saturated)

**Acceptance criteria for the 14-day plan**:
- Workshop paper submitted (not "in progress")
- Median ≥ 6.0 (lower bound of current plateau, defensible)
- Median ≥ 6.3 (modest improvement expected from reframing)
- All 4 pillars present in the paper abstract
- Label-leakage finding promoted to primary contribution
- Submission to a *named workshop* (e.g., EMNLP 2027 Workshop on Multi-Agent Systems, or similar)

---

## Root Cause

The 12+ path oscillation is the active pathology. G3 has more and better data than G2 but is stuck in a path-selection loop instead of shipping. A 60-point workshop paper is achievable from the current 927 runs + label-leakage finding in 14 days without any new experiments.

## Preventive Measures

- **Write hard-fallback clauses on Day 1 of any future >2-week project** (per `comprehensive-synthesis.md:384-385`).
- **Cap path-selection to 4-category taxonomy**: fix data / repackage / re-run / restart (`comprehensive-synthesis.md:386`).
- **Distinguish structural vs narrative vs presentation reviewer feedback** and route each to the right actuator (`comprehensive-synthesis.md:387`).
- **Never pick the "do nothing" option** — status-quo is the failure mode (`comprehensive-synthesis.md:388`).

## Investigation Log

### Phase 0 - Workspace Verification
**Hypothesis:** The `auto-research` workspace is loaded in RepoPrompt and can be targeted with rp-cli.
**Findings:** `rp-cli -e 'windows'` showed window `2` with repo `/Users/tangzw119/Documents/GitHub/auto-research`; `rp-cli -w 2 -e 'tree --type roots'` showed roots for `auto-research` and `cds4worldcup`.
**Evidence:** rp-cli window output, 2026-07-03.
**Conclusion:** Confirmed.

### Phase 1 - Initial Triage
**Hypothesis:** The key evidence is concentrated under the three p1.1 directories, with `legacy/p11-closed-v5-minimax-m3` likely the current frontier.
**Findings:** Initial tree scan found paper artifacts, V5 harnesses, H1/H5 experiments, and a roadmap in `legacy/p11-closed-v5-minimax-m3`.
**Evidence:** `rp-cli -w 2 -e 'tree --depth 2'`.
**Conclusion:** Needs deeper investigation.

### Phase 1.5 - External Reference and History
**Hypothesis:** The local PDF reference and git/workspace history can clarify the realistic bar for a 60-point paper.
**Findings:** Explore agents found that the Mimo reference is a 100-point ceiling because it has multi-benchmark, multi-family, predictive, and out-of-sample validation structure. P1.1 cannot credibly promise that kind of scaling law; it can credibly ship a workshop-grade methodological/negative-result paper.
**Evidence:** Explore sessions `DA75FF61-61A9-4778-8D60-9E71161942E2` and `AB22F9DB-4BAD-4F2A-9F53-BCDCD3F40BAE`; summary recorded in `## Background / Prior Research`.
**Conclusion:** Confirmed.

### Phase 2 - Builder Context Gathering
**Hypothesis:** The paper-readiness decision requires cross-file synthesis over progress state, paper drafts, review history, v5 data, and v4/v5 specs.
**Findings:** Builder selected 26 core files and concluded the strongest evidence-supported path was at least to submit v5 workshop papers before any upside bet.
**Evidence:** Selected files included `state/progress.json`, `paper/main.tex`, `paper/results.tex`, `experiments/h5-emergence/metadata.json`, `wiki/annotations/paper-review-rounds.md`, `wiki/decisions/2026-07-03-comprehensive-synthesis*.md`, and v4/v5 specs.
**Conclusion:** Confirmed.

### Phase 3 - Pair Investigator
**Hypothesis:** The final path may be either two-track workshop-plus-W2 or workshop-only.
**Findings:** Pair investigator verified v5 completeness, review plateau, known data-quality caveats, v4 unvalidated status, and G2 closure precedent. It recommended workshop-only with a 14-day hard stop.
**Evidence:** Findings appended under `## Investigator Findings`; key spot checks include `metadata.json:132-139`, `paper-review-rounds.md:65-82`, `cds-benchmark-design.md:206-220`, `legacy/p11-closed-v5-mimo/state/progress.json:32-38`, `blind-judge.md:22-66`, and `h1-reformulation.md:22-56`.
**Conclusion:** Confirmed.

### Phase 4 - Oracle Synthesis
**Hypothesis:** The Builder and pair disagreement should be resolved by the user's stated 60-point target.
**Findings:** Oracle sided with pair: workshop fallback only. A parallel v4 W2 track would recreate the documented path-selection loop and distract from the only near-term publishable deliverable.
**Evidence:** Oracle chat `new-chat-DE2A45` over the curated 75.9k-token selection.
**Conclusion:** Final recommendation is workshop-only for this cycle.
