# Experiment Pitfalls & Anti-Patterns

> Created: 2026-07-03
> Scope: shared upstream doc consumed by all four active experiment surfaces —
> P12 (`papers/p12-judge-calibration/`), P1+P2 evidence ledger
> (`papers/p1p2-evidence-ledger/`, new mainline), P1.2 settlement
> (`papers/p08-market-calibration/`), and P2.1 evidence input
> (`papers/p07-signal-fusion/`).
> Read by: smaller worker agents before drafting prompts, scripts, or
> experiment runs. Pair with `data-contracts.md` for the matching IO schemas.

This file is the **trap log** for the four experiment lines. Each pitfall
records: the trap name, the four-line description, a "what to write into
state" line so smaller agents can self-report, and the cross-reference into
the matching contract in `data-contracts.md`. Anti-patterns that have already
bit this portfolio are marked **CONFIRMED**; theoretical ones are marked
**PREVENTIVE**.

Conventions used in this file:

- `pitfall_id` uses the prefix `PIT-` for general / portfolio-wide traps and
  `PIT-<EXP>-` for experiment-specific ones (`EXP` ∈ {`P12`, `EVP`, `P1P2`,
  `P12E`, `P1P2E`, `P12P`, `P1P2P` — see the experiment-id table in
  `data-contracts.md`).
- A `state_log` line is what the work agent appends to
  `state/findings.jsonl` or `state/iteration_log.jsonl` when it falls into or
  avoids the trap.
- `gate` references the AutoResearch paper-writing gate that the trap most
  threatens (G1 Lit, G2 Exp, G3 Structure, G4 Figures, G5 Review, plus
  AutoResearch A1 State / A2 Stall / A3 Watchdog).

---

## 0. How to use this file

| Step | When | Action |
|------|------|--------|
| 1 | Before opening a new experiment dir | Read §1 (universal traps) and the experiment-specific section (§2 P12, §3 P1+P2, §4 P1.2, §5 P2.1). |
| 2 | Before writing a prompt or harness | Re-read §6 (prompt anti-patterns) and §7 (data-shape traps). |
| 3 | At end of each iteration | Walk §8 (pre-flight checklist) once. If any box is unchecked, the iteration is not done. |
| 4 | When `stale_count >= 2` | The orchestrator must cite a pitfall id when injecting a new direction; do not just retune the prompt. |
| 5 | When filing a finding | Reference the `pitfall_id` in `findings.jsonl` so the audit trail is grep-able. |

---

## 1. Universal traps (all four experiments)

### PIT-001 — Hallucinated citations and numbers  **[CONFIRMED]**

Score-history self-rating jumps and ad-hoc LLM-generated tables are notorious
for invented data. The framework cannot remove the error source; it can only
force a mechanical check. Cite a paper, a number, a hash, a path, or a
line — never "approximately". Verification must happen at most every 20
citation-like entries (`framework.html §4`).

- `state_log`: `findings.jsonl` — add a `verified: bool` and `source_path`
  field; refuse to mark a finding "completed" if `verified=false`.
- `gate`: G1 Lit, G4 Figures, A1 State.

### PIT-002 — Score inflation through self-rating  **[CONFIRMED]**

In-framework multi-persona simulated review drifts upward over rounds. The
roadmap enforces an anti-inflation cap: first round ≤ 7.0, +1.5 max per
round, ≥ 1 unresolved weakness must remain, median (not mean) is the
final score. Self-rating 8.5+ claims are equivalent to "Strong Accept"
in venue terms.

- `state_log`: `iteration_log.jsonl` — record the per-reviewer scores and
  the median, plus a one-line "unresolved weakness" string. Do not aggregate
  to a mean.
- `gate`: G5 Review, A1 State.

### PIT-003 — Cognitive loop on a stalled direction  **[CONFIRMED]**

Successive iterations re-try similar directions with diminishing returns.
`stale_count` increments on 0 new findings or a metric drop. At
`stale_count >= 2` you must change a **structural** constraint, not a
tactical parameter. At `stale_count >= 4` you stop and write
`state/blocked.md`. This is the single most important AutoResearch rule
(`framework.html §5`).

- `state_log`: bump `stale_count` in `state/progress.json`; on the
  structural pivot, append a `directions_tried.json` entry whose
  `differs_from_all` flag is `true`; on block, write `state/blocked.md`.
- `gate`: A1 State, A2 Stall.

### PIT-004 — Guardian / worker overstep  **[CONFIRMED]**

A heartbeat patrol that reads worker data, modifies worker state, or
reports on the worker's behalf destroys separation of duties. Patrols may
only liveness-check, restart, or nudge (`framework.html §2 v`).

- `state_log`: `logs/heartbeat.jsonl` entries may only carry fields
  `{ts, source, level, event, target, action}` where
  `action ∈ {liveness, restart, nudge}`.
- `gate`: A3 Watchdog.

### PIT-005 — Sample manifest that does not reference real samples  **[CONFIRMED]**

P12 has a recurrent failure where the manifest lists hypothetical or
fabricated P11 ids. The file is "valid JSONL" but the data does not point
at the real source. Every `sample_id` must resolve to a real file under
the source project, with a hash or sha-prefix recorded in the manifest.

- `state_log`: each manifest row carries `source_path` and
  `source_sha256_prefix` (first 12 chars). Validation in `data-contracts.md`
  §3.
- `gate`: G2 Exp, A1 State.

### PIT-006 — HARKing (hypothesis adjusted after seeing results)  **[PREVENTIVE]**

Changing the metric or the hypothesis once numbers come in is a top reason
for rejected experiments. The statistical plan is fixed *before* the run;
surprise findings become a follow-up experiment, not a re-framing of the
original.

- `state_log`: `state/experiment_design.md` (frozen pre-registration) must
  exist before the run; after the run, `findings.jsonl` may reference it
  but may not modify it.
- `gate`: G2 Exp.

### PIT-007 — Sample size floor for statistical claims  **[PREVENTIVE]`

n < 30 with no bootstrap is not a claim. Any "significantly better than X"
sentence in a paper must point to a row in `results.json` with
`n >= 30` per cell or a documented bootstrap CI.

- `state_log`: `results.json` — each result row carries `n` and
  `statistical_test` and either `p_value` or `ci_low` / `ci_high`.
- `gate`: G2 Exp.

### PIT-008 — Direction diversity loss  **[PREVENTIVE]**

After a stall the default is to keep digging in the same direction. Inject
a perturbation: start from the opposite hypothesis, find a structurally
similar cross-domain case, or shift one axis of the experiment
(`framework.html §7 B Parallel exploration`).

- `state_log`: the new direction in `directions_tried.json` must differ
  on ≥ 1 axis (hypothesis, method, data source, evaluation metric) from
  every prior entry.
- `gate`: A2 Stall.

### PIT-009 — Resume instead of fresh session  **[CONFIRMED]**

Resuming a session accumulates context and is the main cause of cognitive
loops (`framework.html §2 iv`). Each iteration starts with a fresh session
and injects state via files. The `claude-prompt.md` and `mimo-prompt.md` of
each experiment dir are the only correct entry points.

- `state_log`: the prompt's first action is `update state/progress.json
  last_seen`; the second is to read `state/task_spec.md`.
- `gate`: A1 State, A3 Watchdog.

### PIT-010 — Context window collapse  **[PREVENTIVE]**

Long sessions degrade even with file-state discipline. Hard cap is
**~40 rounds** before the agent writes `state/checkpoint.md` and asks for
restart (`p1.2/claude-prompt.md`, `p2.1/claude-prompt.md`). Sub-agents may
read at most 5 large files per iteration; no single file over 300 lines
(`framework.html §8 Engineering constraints 1`).

- `state_log`: when `iteration > 40`, append a `checkpoint_requested`
  entry to `iteration_log.jsonl` and write `state/checkpoint.md` summarising
  progress and current milestone.
- `gate`: A1 State, A2 Stall.

### PIT-011 — Engagement of the user mid-run  **[CONFIRMED]**

`framework.html §2 i` forbids prompting the user during a run. The only
exception in this portfolio is the **single** M2 human checkpoint in
P1.2 (event selection review). All other P12, P1+P2, P2.1 tasks are
zero-interaction.

- `state_log`: any `level=question` event in `logs/work.jsonl` outside the
  P1.2 M2 checkpoint is a violation flag; orchestrator should fire a
  `nudge` and append `pitfall_hit: PIT-011` to the next iteration log.
- `gate`: A2 Stall, A3 Watchdog.

### PIT-012 — Mixing evidence formats  **[PREVENTIVE]**

P2.1's Forecaster emits **text** descriptions of `base/downside/upside`,
not numeric probabilities. P1.2's Brier/Log Loss consumes **numeric**
probabilities. If the two surfaces are wired through P1+P2 evidence
ledger, a text forecast must be converted to a probability distribution
*before* it lands in the settlement record. Treating the text as
"already a number" is a frequent silent error.

- `state_log`: any `factor_ledger_entry` whose `observed_outcome.confidence`
  is a string is rejected by the validator; the worker must resend with
  numeric `confidence` in `[0, 1]`.
- `gate`: G2 Exp, G3 Structure, plus the cross-experiment PIT-027 in §5.

### PIT-013 — Single-judge self-confidence  **[CONFIRMED, P11]**

P11's H1 false positives were driven by a single judge (the producer) and
its confidence score. Every judge-style metric must be either (a) blind,
(b) paired with a peer judge, or (c) abstention-aware. Producer
self-confidence is a confound, not a signal.

- `state_log`: every judgment record carries `judge_id` and
  `awareness: blind|leaked|pairwise` and (if abstained) `abstain: true` +
  `abstain_reason`.
- `gate`: G2 Exp, G5 Review.

---

## 2. P12 Judge Calibration (`papers/p12-judge-calibration/`)

### PIT-101 — Label leakage in judge prompts  **[CONFIRMED, P11 source]**

Any prompt that contains the condition label (`inner_monologue`,
`no_think`, `pure_analysis`) makes the judge see what it should not.
H1's blind failure is the canonical case. P12 must run at least one
**leaked** and one **blind** protocol over the same sample set and
report the delta.

- `state_log`: `experiments/leakage_reproduction.json` carries
  `protocol: leaked|blind|pairwise|neighborhood|abstention` per record;
  the diff table is in `experiments/calibration_metrics.md`.
- `gate`: G2 Exp.

### PIT-102 — Brittle consistency-on-wrong  **[CONFIRMED, P11]**

A judge that gives consistent scores to an obviously wrong answer is
worse than one that gives noisy scores. The "consistency" metric must
be **conditional on correctness**: a paraphrase of a known-bad answer
that scores high is a fail, not a pass.

- `state_log`: `experiments/pairwise_blind_results.json` records
  `paraphrase_id` and `ground_truth_correctness: bool`; the metric
  `consistency_on_wrong` is `mean(score | not correct)`, and a value
  > 0.5 is a fail.
- `gate`: G2 Exp, G5 Review.

### PIT-103 — Abstention collapse  **[PREVENTIVE]**

Allowing the judge to abstain ("insufficient evidence") only works if
abstention is treated as a real outcome. If every hard case is silently
scored instead of abstained, abstention-aware scoring degrades to label
leakage. Track the abstain rate; flag if it is ever 0 on a sample set
that includes ambiguous cases.

- `state_log`: each `neighborhood_probe_results.json` row carries
  `abstain: bool` and `abstain_reason`; aggregate `abstain_rate` per
  probe. If a sample set has `abstain_rate == 0` and
  `ambiguous_count > 0`, log a `pitfall_hit: PIT-103` event.
- `gate`: G2 Exp, G5 Review.

### PIT-104 — Neighborhood probes that are not actually neighbors  **[PREVENTIVE]**

A "neighborhood probe" that is a wholly different question is not a
neighborhood probe; it is a different experiment. The probe must change
exactly one axis (role behavior, factual premise, decision consequence)
relative to the original.

- `state_log`: `experiments/neighborhood_probe_schema.json` carries
  `axis: role|fact|consequence` per probe; each probe must declare
  the original `sample_id` and the single axis it mutates.
- `gate`: G2 Exp.

### PIT-105 — Reusing P11 samples without re-anchoring  **[CONFIRMED]**

P11 samples were collected under label-leakage conditions. Importing
them into P12 "as is" perpetuates the leak unless each sample is
re-anchored: condition label stripped from inputs, condition
membership moved to a separate metadata field that the judge never
sees.

- `state_log`: every imported P11 sample in
  `experiments/sample_manifest.jsonl` has
  `original_condition: string` and `condition_visible_to_judge: false`
  in the row's metadata.
- `gate`: G2 Exp, A1 State.

### PIT-106 — Comparing apples to oranges across protocols  **[PREVENTIVE]**

A common failure is comparing the mean score of the leaked protocol to
the mean score of the blind protocol on different sample subsets. The
delta is meaningless. The two protocols must run on the same sample
set with the same `sample_id` ordering.

- `state_log`: every per-protocol result file lists
  `sample_ids_ordered: [string]`; the orchestrator cross-checks that
  all protocols in the run share the same ordered list.
- `gate`: G2 Exp, G5 Review.

### PIT-107 — Five-persona review without diversity  **[PREVENTIVE]**

The five personas are R1 Experimentalist, R2 Theorist, R3 Perfectionist,
R4 Synthesizer, R5 Newcomer. If all five are run by the same model
with the same prompt template, the median is a measure of one LLM's
bias, not five. Force at least one different LLM per round.

- `state_log`: `paper/review_round_*.md` carries
  `reviewer_models: [string]`; if all entries are the same model, the
  round is invalid.
- `gate`: G5 Review.

---

## 3. P1+P2 Evidence Ledger (`papers/p1p2-evidence-ledger/`, new mainline)

### PIT-201 — Ledger entry without contradicting evidence  **[PREVENTIVE]**

The P1+P2 schema requires `contradicting_evidence[]`. An entry that
records only supporting evidence turns the ledger into a confirmation
log. The validator must reject entries with empty
`contradicting_evidence` *and* empty `missing_prerequisites[]` —
i.e. an entry that pretends to be complete.

- `state_log`: ledger entries failing the contradiction / missing test
  are written to `experiments/rejected_entries.jsonl` with reason
  `pitfall_hit: PIT-201`.
- `gate`: G2 Exp, G3 Structure.

### PIT-202 — Single-source authority claim  **[PREVENTIVE]**

A `factor_type: authority` entry must declare
`source_independence >= 2`. A single source is not authority, it is
opinion. If the same newswire is the only citation, the authority
field is invalid.

- `state_log`: rejected entries list with `pitfall_hit: PIT-202` and the
  observed `source_independence` value.
- `gate`: G2 Exp.

### PIT-203 — Freshness is not just timestamp  **[PREVENTIVE]**

`freshness: "2026-07-03"` on a 24-hour news cycle is not the same as
"2026-07-03" on a 1-year macro indicator. The schema must also carry
`freshness_window` (the natural period of the indicator) and the
validator computes a `freshness_ratio = age / freshness_window`. Ratios
above 1.0 are stale regardless of the absolute date.

- `state_log`: ledger entries store `freshness_ratio`; entries with
  `freshness_ratio > 1.0` are flagged with `stale: true` in
  `experiments/aged_entries.jsonl`.
- `gate`: G2 Exp.

### PIT-204 — Settlement rule that cannot be evaluated  **[PREVENTIVE]**

A `settlement_rule` is a contract for what would prove the factor
right or wrong. If the rule cannot fire on the available event
outcomes, the factor is un-settleable and must be marked
`settleable: false`. The percentage of un-settleable factors must be
reported; > 40% un-settleable is a fail.

- `state_log`: `experiments/settleability_audit.json` records
  `total_factors`, `un_settleable`, `un_settleable_ratio`.
- `gate`: G2 Exp, G5 Review.

### PIT-205 — Confidence before == confidence after  **[PREVENTIVE]**

If the ledger is to be the substrate of belief update, the
`confidence_after` field must differ from `confidence_before` when
new evidence lands. If they are equal across the whole run, either
the evidence has no weight (bad) or the field is being copy-pasted
(bad). Track `confidence_delta_distribution`; flag if the variance
is 0.

- `state_log`: aggregated per-run `confidence_delta` stats in
  `experiments/belief_update_stats.json`.
- `gate`: G2 Exp.

### PIT-206 — Audit trace that is not auditable  **[PREVENTIVE]**

`audit_trace` is supposed to be the reproduction log: which
sources, which tool, which timestamp, which hash. If the field is a
one-line free-text comment, it is not an audit trace. The field must
be an array of structured steps, each with a `tool` and a `sha256`.

- `state_log`: validator rejects entries whose `audit_trace` is not an
  array of objects with `tool` and `sha256` keys.
- `gate`: G2 Exp, A1 State.

### PIT-207 — Reusing the P1.1 / P11 prompt archive as ledger input  **[CONFIRMED, P11]**

P11 produced `inner_monologue / no_think / pure_analysis` free-text
reasoning. These are not evidence; they are process traces. Routing
them into the ledger as `supporting_evidence` without an independent
`source` and `observability` claim perpetuates the P11 label-leakage
problem at the evidence-input layer.

- `state_log`: ledger import script must reject rows whose
  `source_type: free_text_trace` unless paired with an explicit
  `trace_grounded: bool` flag set to true with a justifying
  `grounding_source_id`.
- `gate`: G2 Exp, plus the cross-experiment PIT-027 in §5.

### PIT-208 — Sample-pilot scale-up without effect-size estimate  **[PREVENTIVE]**

The P1+P2 2-week plan asks for a 10-handcrafted-example pilot on
day 1-2. Scaling that to 30 settleable factors on day 3-5 without
computing an effect size is a guaranteed under-powered follow-up.
Effect size is computed before scaling.

- `state_log`: `experiments/pilot_power.md` carries the effect size
  estimate, the planned N for the larger run, and the reasoning.
- `gate`: G2 Exp.

---

## 4. P1.2 Market Calibration / Settlement Layer
(`papers/p08-market-calibration/`)

### PIT-301 — Claiming Factor Ledger exists when 0 lines of code  **[CONFIRMED]**

`p1.2 .../state/task_spec.md` records the fact-check: 81 lines of
design doc, **0 lines of Python**. Do not write paper sentences that
say "we have a Factor Ledger" until `calc_brier.py` or its equivalent
plus a working ledger read/write exist. Keep the claim at "design
complete, implementation in progress" until the validator passes.

- `state_log`: `state/implementation_status.md` — keep a current
  table of `component`, `design_lines`, `code_lines`, `tests`,
  `passing`. Update on every milestone.
- `gate`: G3 Structure, G5 Review.

### PIT-302 — Brier computed from text forecasts  **[CONFIRMED, P2.1 coupling]**

P2.1's Forecaster outputs three text scenarios. Naively taking the
count of words like "likely" as a probability is **not** a Brier input.
If the project reuses a P2.1 forecast, the worker must either
(a) re-extract a numeric probability from a human-anchored table or
(b) declare the factor `un_settleable: true` and exclude it from the
Brier aggregate. Picking (a) and not validating against anchors is
the trap.

- `state_log`: Brier inputs are logged with `source: numeric|anchor|
  text-extract`; only `numeric` and `anchor` are valid for the
  paper's headline Brier.
- `gate`: G2 Exp.

### PIT-303 — Single M2 human checkpoint, then zero  **[CONFIRMED, P1.2 spec]**

M2 (event selection review) is the **only** human checkpoint. After
that the agent must run M3-M9 with no questions. Adding a second
checkpoint, even for a "small" decision, breaks the AutoResearch
zero-interaction rule (`framework.html §2 i`).

- `state_log`: any `level=question` event after M2 is a violation.
- `gate`: A2 Stall.

### PIT-304 — Polymarket API without rate limit handling  **[CONFIRMED, P1.2 spec]**

The current code uses a single `/events` endpoint with a 15 s
timeout and no retry. A "ran for 4 hours" run that silently
returns empty data because of rate limits is a known failure mode.
Either add backoff/retry or scope the run to ≤ 5 events per
domain, but do not claim robust calibration on partial data.

- `state_log`: each event pull records `http_status`, `attempt`, and
  `backoff_ms` in `experiments/event_pull_log.jsonl`.
- `gate`: G2 Exp.

### PIT-305 — Gold-H/M/L as the only judge drift signal  **[CONFIRMED, P1.2 spec]**

`calibration_lib.py:34-38` exposes 3 gold samples. Three is the
absolute minimum to detect a constant offset; it cannot detect
distribution shift. If a paper claim is "judge is calibrated", it
needs more than 3 anchors. Either expand the gold set or weaken
the claim.

- `state_log`: `state/calibration_lib_audit.md` records the gold
  set size, the test it supports, and the limit.
- `gate`: G5 Review.

### PIT-306 — Knowledge writeback "improvement" without a baseline metric  **[CONFIRMED, P1.2 spec]**

The writeback loop only shows improvement if the metric before is
defined and recorded *before* the writeback fires. Defining the
metric after the run is HARKing. The metric and the snapshot are
taken first.

- `state_log`: `experiments/before_after/before.json` is frozen
  before the writeback; `experiments/before_after/after.json` is
  taken after. The diff is the result. The before file's hash
  appears in the after file's `baseline_sha256`.
- `gate`: G2 Exp.

### PIT-307 — "17 rounds" claim vs the actual 27 dirs  **[CONFIRMED, P1.2 spec]**

The current claim says "17 rounds of A/B testing" but the file
count is 27 experiment dirs and the version range is v02-v16 = 15
versions. The paper should not over-claim. Use the count you can
defend from the directory listing.

- `state_log`: `experiments/ab_test_inventory.md` carries the
  exact directory count, version range, and the count of dirs
  that pass the inclusion filter.
- `gate`: G1 Lit, G5 Review.

### PIT-308 — Cross-domain ANOVA with N=2 per cell  **[PREVENTIVE]**

P1.2 has 6 domains. With n = 2 per cell, an ANOVA is meaningless.
Report only directional consistency (≥ 4/6 domains in the same
direction) and label it as such.

- `state_log`: the cross-domain report's stats section carries
  the n per cell next to the test name.
- `gate`: G2 Exp.

---

## 5. P2.1 Signal Fusion / Evidence Input Layer
(`papers/p07-signal-fusion/`)

### PIT-401 — Treating 267 lines as a research contribution  **[CONFIRMED, P2.1 spec]**

The chain is 267 lines (or 427 with the pipeline orchestrator).
The roadmap explicitly says this scale can be dismissed as "thin
engineering". Do not write the paper framing around the algorithm
itself. Frame around the **ablation structure**, the **bias
detection contract**, and the **evidence-topology** output (the
adapter for P1+P2's ledger).

- `state_log`: paper outline section §1 (contributions) must
  contain at least one item phrased as "ablation protocol",
  "bias-detection contract", or "evidence-ledger adapter", not
  "novel fusion algorithm".
- `gate`: G3 Structure, G5 Review.

### PIT-402 — Calibrator's 2.0× ratio as a statistical test  **[CONFIRMED, P2.1 spec]**

`calibrator.py:41-63` raises a flag when one scenario gets ≥ 2× the
weight of another. This is a heuristic, not a test. Do not phrase
"over_optimism detected (p < 0.05)" — phrase "over_optimism
flagged (ratio ≥ 2.0× threshold, no significance test)".

- `state_log`: the bias-detection result rows in
  `experiments/calibrator_results.json` carry
  `method: ratio_threshold` and `significance_tested: false`.
- `gate`: G2 Exp.

### PIT-403 — Polymarket INACTIVE counted as a data source  **[CONFIRMED, P2.1 spec]**

`polymarket` is marked INACTIVE in the source list. The grouping
table in `task_spec.md` has been corrected, but a re-run of the
prompt may still pipe it in. The validator must exclude any row
whose `datasource_status != active`.

- `state_log`: rejected datasource references are logged with
  `pitfall_hit: PIT-403` in `experiments/datasource_filter.jsonl`.
- `gate`: G2 Exp.

### PIT-404 — A/B without a pre-registered metric  **[CONFIRMED, P2.1 spec]**

The 4 conditions (A: no data, B: raw, C: fused, D: fused+diagnose)
need a single pre-registered primary metric. P2.1 spec mentions
"历史吻合度" but does not freeze its computation. Freeze it
before the run.

- `state_log`: `experiments/primary_metric.md` carries the
  formula, range, and the row that will be reported in the paper.
- `gate`: G2 Exp.

### PIT-405 — MC run count claimed vs run count persisted  **[PREVENTIVE]**

The plan is 4 conditions × 100 runs = 400. If the JSONL output has
< 400 records, the run is incomplete. A common silent failure is a
retry loop that overwrites prior results, or a memory cap that
truncates the output. The validator counts records per condition.

- `state_log`: `experiments/mc_inventory.json` records
  `condition, expected, actual, sha256_prefix_of_output`.
- `gate`: G2 Exp, A1 State.

### PIT-406 — Forecaster text → numeric for P1.2 Brier (cross-coupling)  **[CONFIRMED]**

Same trap as PIT-302, but from the producer side. If a P2.1
experiment wants to feed a Brier aggregate, the worker must add
a `numeric_forecast` field — not silently reinterpret the text.

- `state_log`: see PIT-302; cross-reference in
  `experiments/forecast_bridge_log.md`.
- `gate`: G2 Exp, PIT-302, PIT-027.

### PIT-407 — MemoryLayer confusion (5 vs 6)  **[CONFIRMED, P2.1 spec]**

P2.1 spec notes the original claim "5 MemoryLayer implementations"
but the file scan finds 6 concrete classes
(Mem0Memory/Mem0Adapter/Vector/Graph/Hybrid/Mock). If the paper
text says "5" it is wrong; if it says "6" it is right; if it says
"5 active + 1 helper", the paper must justify the split.

- `state_log`: a `state/component_inventory.md` keeps the
  authoritative count, with class names, line counts, and the
  paper-text version.
- `gate`: G3 Structure, G5 Review.

### PIT-408 — `no_think` / `pure_analysis` traces as evidence input  **[CROSS, PIT-207]**

P11's `no_think` and `pure_analysis` traces are not evidence. If
P2.1 ever advertises a "decision trace" feature, it is a process
artifact, not an observable signal. The four observable signal
types are `confirmed_fact / weak_evidence / missing_data /
source_failure`; a free-text trace is none of these.

- `state_log`: signal rows whose `signal_type` is not in the
  enum are rejected with `pitfall_hit: PIT-408`.
- `gate`: G2 Exp.

---

## 6. Prompt-level anti-patterns (all four experiments)

The following show up in `claude-prompt.md` / `mimo-prompt.md`. They are
checked by the orchestrator at every restart.

| id | Anti-pattern | Why it fails | How to fix |
|----|--------------|--------------|------------|
| PAP-1 | "Ask the user before submitting" | Breaks zero-interaction (PIT-011). | "Submit, then re-submit on failure. The user is not a checkpoint." |
| PAP-2 | "Read all 30 result files" | Exceeds 5-large-file cap (PIT-010). | "Read the 3 most recent findings.jsonl entries first." |
| PAP-3 | "Score yourself 8+ to pass" | Score inflation (PIT-002). | "Score per reviewer persona, then take median. Cap first round at 7.0." |
| PAP-4 | "Cite the paper you remember" | Hallucinated citation (PIT-001). | "For each citation, write the path and the verified quote." |
| PAP-5 | "If the result is bad, change the metric" | HARKing (PIT-006). | "If the result is bad, write a follow-up experiment, do not change the metric." |
| PAP-6 | "Use the leaked labels if they help" | Label leakage (PIT-101, PIT-105). | "Strip the condition label before judging. Re-anchor it to metadata only." |
| PAP-7 | "Resubmit the same experiment to be sure" | Cognitive loop (PIT-003). | "Two identical runs = one data point. The third must change an axis." |
| PAP-8 | "Add another gold sample" without freezing the gold set first | Sample drift (PIT-305). | "Freeze the gold set in `state/calibration_lib_audit.md` before any run uses it." |
| PAP-9 | "Decide based on a single judge's confidence" | Single-judge self-confidence (PIT-013). | "Pair the judge, or run blind, or allow abstention. Never trust a single confidence." |
| PAP-10 | "Persist results in chat / not in state files" | State drift (PIT-009, A1). | "Every result is `state/findings.jsonl` or `experiments/*.json`. Chat is ephemeral." |

---

## 7. Data-shape traps (cross-experiment)

These are the shapes that have broken the harness at least once in the
portfolio history, or that are guaranteed to break the upcoming ledger
contract.

| id | Shape | Symptom | Fix |
|----|-------|---------|-----|
| DST-1 | `confidence: "high"` instead of `0.85` | Brier cannot run, ledger validator rejects. | Numeric `confidence` in `[0, 1]`. Use `confidence_band: low\|med\|high` for human labels. |
| DST-2 | `supporting_evidence: ["yes"]` | Not an array of structured refs. | Array of `{source_id, snippet_sha256, observed_at, independence_class}` objects. |
| DST-3 | `audit_trace: "looked at wikipedia"` | Not auditable. | Array of `{tool, input_sha256, output_sha256, ts, agent}`. |
| DST-4 | `sample_id: "P11-001"` without a `source_path` | PIT-005 hit. | Every `sample_id` carries `source_path` and `source_sha256_prefix`. |
| DST-5 | `factor_type: "authority"` with `source_independence: 1` | PIT-202 hit. | Authority factors require `source_independence >= 2`. |
| DST-6 | `forecast: "likely"` going into Brier | PIT-302 hit. | Forecasts must be numeric or explicitly tagged `un_settleable: true`. |
| DST-7 | `freshness: "2026-07-03"` with no `freshness_window` | PIT-203 hit. | Both fields are required; the validator computes `freshness_ratio`. |
| DST-8 | Empty `abstain_reason` when `abstain: true` | PIT-103 hit. | `abstain_reason` is non-empty if `abstain` is true. |
| DST-9 | `condition_visible_to_judge: true` on a P12 sample | PIT-101, PIT-105 hit. | Default false; only true in the explicitly leaked protocol. |
| DST-10 | `judge_id: "self"` for the producer's own output | PIT-013 hit. | The producer cannot be its own judge; `judge_id` must be a distinct agent id. |
| DST-11 | `audit_trace` step missing `tool` | PIT-206 hit. | `tool` is required; allowed values are listed in `data-contracts.md §6`. |
| DST-12 | A `findings.jsonl` row without `verified: bool` | PIT-001 hit. | `verified` is required. |
| DST-13 | A `iteration_log.jsonl` row without `unresolved_weakness` (review rounds) | PIT-002 hit. | `unresolved_weakness` is required on review rows. |
| DST-14 | A P2.1 signal row with `signal_type` outside the 4-value enum | PIT-408 hit. | Enum is `confirmed_fact \| weak_evidence \| missing_data \| source_failure`. |
| DST-15 | A P1.2 Brier input from `text-extract` source being used as the headline metric | PIT-302 hit. | Headline Brier is `numeric` or `anchor` only. `text-extract` is reported separately. |

---

## 8. Pre-flight checklist (run before marking any iteration done)

Tick once, paste a one-liner into `iteration_log.jsonl` as
`preflight_pass: true | false` with the list of failed ids.

### 8.1 Universal (all four experiments)

- [ ] PIT-009 — fresh-session entry point used (not resume).
- [ ] PIT-010 — file budget respected (≤ 5 large files, ≤ 300 lines each).
- [ ] PIT-001 — every numeric / citation claim has a `source_path` and a
  verification flag.
- [ ] PIT-002 — review row carries median score and an
  `unresolved_weakness` string.
- [ ] PIT-003 — `stale_count` and `directions_tried.json` updated.
- [ ] PIT-006 — pre-registration artifact exists for the run.
- [ ] PIT-007 — `n >= 30` per cell or bootstrap CI reported.
- [ ] PIT-011 — no `level=question` outside the P1.2 M2 checkpoint.
- [ ] A1 — `state/progress.json` `last_seen` is current.

### 8.2 P12-specific

- [ ] PIT-101 — leaked + blind + pairwise + neighborhood + abstention
  protocols all run on the same ordered `sample_ids_ordered` list.
- [ ] PIT-103 — `abstain_rate > 0` on any sample set with
  `ambiguous_count > 0`.
- [ ] PIT-104 — neighborhood probes change exactly one axis.
- [ ] PIT-105 — every imported P11 sample has
  `condition_visible_to_judge: false`.
- [ ] PIT-107 — review round uses ≥ 2 distinct models.

### 8.3 P1+P2 evidence-ledger-specific

- [ ] PIT-201 — no ledger entry has both `contradicting_evidence=[]` and
  `missing_prerequisites=[]`.
- [ ] PIT-202 — every `factor_type: authority` entry has
  `source_independence >= 2`.
- [ ] PIT-203 — every entry has `freshness_window` and `freshness_ratio`
  computed.
- [ ] PIT-204 — settleability audit exists, `un_settleable_ratio <= 0.4`.
- [ ] PIT-205 — `confidence_delta_distribution` has non-zero variance.
- [ ] PIT-206 — `audit_trace` is a structured array.
- [ ] PIT-207 — no `source_type: free_text_trace` rows unless
  `trace_grounded: true` with a `grounding_source_id`.
- [ ] PIT-208 — pilot effect size computed before scaling.

### 8.4 P1.2-specific

- [ ] PIT-301 — `state/implementation_status.md` reflects current
  code-vs-design ratio.
- [ ] PIT-302 — Brier inputs are `numeric` or `anchor` for the headline
  number.
- [ ] PIT-303 — no `level=question` after M2.
- [ ] PIT-304 — `event_pull_log.jsonl` carries `http_status` and
  `backoff_ms` for every event.
- [ ] PIT-305 — gold-set audit written; if used, expanded beyond 3.
- [ ] PIT-306 — `before.json` is frozen and its hash appears in
  `after.json`.
- [ ] PIT-307 — `ab_test_inventory.md` matches the directory count.
- [ ] PIT-308 — per-cell n reported next to each statistical test.

### 8.5 P2.1-specific

- [ ] PIT-401 — paper outline contributions do not lead with a "novel
  fusion algorithm" claim.
- [ ] PIT-402 — calibrator results carry `method: ratio_threshold` and
  `significance_tested: false`.
- [ ] PIT-403 — datasource filter excludes `polymarket`.
- [ ] PIT-404 — `experiments/primary_metric.md` is frozen before the run.
- [ ] PIT-405 — `mc_inventory.json` shows 400 records across 4 conditions.
- [ ] PIT-407 — component inventory matches paper text.
- [ ] PIT-408 — signal rows have `signal_type` in the 4-value enum.

### 8.6 Cross-experiment

- [ ] PIT-012 / PIT-302 / PIT-406 — no text-format forecast is silently
  used as a numeric probability.
- [ ] PIT-027 — any P11 free-text trace entering P1+P2 is grounded
  (PIT-207) and not silently treated as a P2.1 observable signal
  (PIT-408).

---

## 9. Quick reference: which pitfalls block which gates

This is the lookup a small worker should do before deciding to ship a
deliverable.

| Gate | Blocking pitfalls |
|------|-------------------|
| G1 Literature | PIT-001, PIT-307, PIT-407 |
| G2 Experiment | PIT-005, PIT-006, PIT-007, PIT-101, PIT-102, PIT-103, PIT-104, PIT-105, PIT-106, PIT-201, PIT-202, PIT-203, PIT-204, PIT-205, PIT-206, PIT-207, PIT-208, PIT-302, PIT-304, PIT-306, PIT-308, PIT-402, PIT-403, PIT-404, PIT-405, PIT-408 |
| G3 Structure | PIT-201, PIT-301, PIT-401, PIT-407, PIT-012 |
| G4 Figures | PIT-001 |
| G5 Review | PIT-002, PIT-103, PIT-107, PIT-204, PIT-301, PIT-305, PIT-307, PIT-401, PIT-407 |
| A1 State | PIT-001, PIT-003, PIT-005, PIT-009, PIT-010, PIT-206, PIT-405 |
| A2 Stall | PIT-003, PIT-008, PIT-010, PIT-011, PIT-303 |
| A3 Watchdog | PIT-004, PIT-009, PIT-011 |

---

## 10. Self-reporting protocol

When a worker recognises it has fallen into a pitfall:

1. Append a row to `state/findings.jsonl` with at least:
   ```json
   {"ts": "...", "source": "work", "level": "warn", "event": "pitfall_hit",
    "pitfall_id": "PIT-XXX", "experiment": "p12|p1p2|p1.2|p2.1",
    "detail": "one-line description of the actual symptom",
    "mitigation": "what the agent did next"}
   ```
2. If the pitfall is in §1 universal or §6 prompt-level, also bump
   `stale_count` only when the same pitfall is hit twice in a row (single
   hit is not a stall).
3. If the pitfall blocks a gate (see §9), the worker must explicitly
   declare the gate-block in the next `iteration_log.jsonl` row and
   refuse to mark the iteration complete until the trap is cleared.

When a worker recognises it has avoided a pitfall:

1. Append a row to `state/findings.jsonl` with
   `event: "pitfall_avoided"` and the `pitfall_id`.
2. After 5 such rows for the same `pitfall_id` across the portfolio,
   the orchestrator may mark the trap as "internalised" and stop
   pre-checking it on the next iteration.

---

## 11. Cross-references

- `data-contracts.md` — matching JSON shapes for sample_manifest,
  leakage_reproduction, pairwise_blind_results, neighborhood_probe_*,
  factor_ledger entries, settlement_record, brier_input, signal row,
  progress.json, findings.jsonl, iteration_log.jsonl, work.jsonl.
- `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` — the
  portfolio-wide anti-inflation, stale-detection, and direction-diversity
  rules.
- `state/task_spec.md` (root) — milestones and stale-count thresholds.
- `docs/autoresearch/2026-07-03-experiment-configuration-plan.md` — the
  per-experiment shared-deliverable checklist.
- `victorchen96.github.io/auto_research/framework.html` — the upstream
  AutoResearch protocol (zero-interaction, guardian/worker split,
  state files, stall detection, heartbeat watchdog).
- `victorchen96.github.io/auto_research/skill/paper-writing.html` — the
  5-gate review and anti-inflation score rules.
