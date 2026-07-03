# P12 Experiment Design (Pre-registration)

> Created: 2026-07-03 · exp_id `P12` · frozen at end of M1 per PIT-006.
> Pair with `state/io_spec.md` §4, `state/task_spec.md`, `wiki/concepts/judge-calibration-protocol.md`.

This file declares the **pre-registered plan** for P12's judge-calibration viability probe.
After the run starts, this file is **read-only** (PIT-006). Surprises go to `state/findings.jsonl`
and become follow-up experiments, not a re-framing of the original.

## §Hypothesis

> **H_cal.** When the same P11 sample is judged under each of the five protocols
> (leaked, blind, pairwise, neighborhood, abstention), the
> `delta_score = leaked_score − blind_score` is non-zero for **at least one** of the
> three standard conditions at α = 0.05. If no condition shows a non-zero delta,
> the protocols are equivalent and the contribution collapses to "rediscovery",
> which is the pre-registered null outcome.

Scope of H_cal is calibration, not the original P11 effect (`H1 / H1c / H3 / F1`).
P12 inherits these hypothesis labels from P11 only as **anchor points** for
`state/io_spec.md` §2.3 (`calibration_metrics.md`).

## §Primary metric

- `delta_score = leaked_score − blind_score` computed **per sample**.
- Reported quantities per condition (n=150 each):
  - `mean(delta_score)`
  - 95% bootstrap CI (10 000 resamples, fixed seed `42`)
  - `abstain_rate` (from `abstention` protocol rows)
  - `consistency_on_wrong` (from `pairwise` protocol rows)
- All scores live in the [1.0, 5.0] band per P11's RoleDNA 5-point scale.

## §n per cell

- **150 per condition** = 3 enterprises × 50 runs/cell, parsed from filenames
  matching `^<condition>_<enterprise>_run<NNN>\.yaml$` where `NNN ∈ 001..050`.
- Conditions covered: `inner_monologue`, `no_think`, `pure_analysis`.
- Total: 3 × 150 = **450 samples** for M2-M5.
- Per-cell n=150 satisfies PIT-007 (≥ 30 for a directional claim).

## §Sample set

**Source**: P11 v5 A-runs at
`../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/`
(post-restructure; see `state/io_spec.md` §1 for the canonical reference).

**Inclusion**: filename `<condition>_<enterprise>_run<NNN>.yaml` where `condition ∈ {inner_monologue, no_think, pure_analysis}`.

**Exclusion (deferred to M3 / M5 as transfer material, NOT in M2)**:
- `output_only` (negative-control condition from P11 v5 §A — 150 yaml)
- `explicit_audit` (probe-condition from P11 v5 §A — 150 yaml)

Total excluded: 300 yaml. Rationale: `state/io_spec.md` §1.1 enum is fixed at the
three standard strings; expanding the enum is an explicit M4/M5 task.

**Producer model**: `DeepSeek-V4-Flash` (P11 v5 producer).

**Gold label `ground_truth_correctness`**: imported from P11's human labels
where present; explicitly absent on P11 v5 runs (P11 did not capture
ground-truth during M2 runs). For M2-M5, `ground_truth_correctness` is recorded
as `null` with the rationale noted in `state/findings.jsonl`. **No invented
labels** (PIT-005).

## §Frozen sample IDs order

```
outer loop  : original_condition in [inner_monologue, no_think, pure_analysis]
inner loop  : original_enterprise in [ISPACE, LANDSPACE, SPACETIMETECH]   # alphabetical
inner-inner : original_run_id ascending as integer 1..50                  # numeric sort
counter     : starts at 1, sample_id = f"P12-{counter:03d}"
```

This guarantees the **identical** `sample_ids_ordered` array in
`experiments/sample_ids_ordered.json` and the **identical** row order in
`experiments/sample_manifest.jsonl`. Both files are byte-stable (other than
`imported_at`) under re-execution, satisfying PIT-106.

The 450-sample sequence is: `P12-001` (inner_monologue/ISPACE/001) →
`P12-150` (inner_monologue/SPACETIMETECH/050) → `P12-151` (no_think/ISPACE/001)
→ ... → `P12-450` (pure_analysis/SPACETIMETECH/050).

## §Frozen judge model list

For M2 (the first non-M1 milestone):

- **Single judge**: `DeepSeek-V4-Flash`.

Rationale (cross-reference `state/directions_tried.json:directions[1]`):
the M2 budget is 450 × 1 = 450 LLM calls (vs 450 × 2 = 900 with two judges).
A two-judge setup (DeepSeek-V4-Flash + Kimi-K2.5) is held for M3, where
pairwise and neighborhood protocols can re-use the same judge pool. Per
`state/task_spec.md` "Stale Rules" and framework §6, M2 deliberately keeps the
cost small to support the 3–6 day viability window.

A `judge_id != "self"` invariant is enforced structurally: the producer
(DeepSeek-V4-Flash) is **not** the judge in `leaked`/`blind`/`pairwise`
calls (DST-10, PIT-013). For M2, M2 invocations use a separate
judge-pool entry stored in `experiments/leakage_reproduction.json:judge_id`
(deferred — do **not** invent the value here).

## §Stop conditions

Three nested exits, in priority order. Trigger of any exit closes the iteration loop.

1. **Effect-size early exit (success path).** Compute `mean(delta_score)` and
   its 95% bootstrap CI per condition (3 conditions). If **all three**
   `|mean(delta_score)| < 0.05` AND the **max** 95% CI width `< 0.10`,
   record `early_exit: no_leakage_effect` in `state/findings.jsonl` and
   close M2 with the verdict "leakage not detected under this protocol
   set; fold into P1+P2 methodology".

2. **Direction pivot (structure).** Framework §6 / `state/task_spec.md`
   "Stale Rules": when `stale_count >= 2` (recorded in `state/progress.json`),
   drop the `pairwise` and `abstention` protocols and run only
   `(leaked, blind, neighborhood)`. The pivoted set is what produced the
   P11 label-leakage finding, so it is the **highest-value truncation** when
   budget is tight. This pivot changes **structure** (the protocol set),
   not tactics (prompt tuning).

3. **Hard stop (failure path).** `stale_count >= 4` ⇒ fold P12 into
   `papers/p1p2-evidence-ledger/` methodology with the verdict
   `not_viable_as_short_paper`, citing the lack of a robust
   `delta_score` signal across the 3 conditions. Stop further P12 runs.

## §Pre-registration lock

This file is **frozen**. After M1 close:

- Edits to add findings → `state/findings.jsonl` (append-only, PIT-003).
- Edits to change direction → create a new design doc in
  `state/experiment_design.<reason>.<sha256-7>.md` (PIT-006 intent:
  surprises do not retroactively rewrite the original plan).
- This file MAY be re-read freely; it is not the place for surprises.

## §Cross-references

- `state/io_spec.md` §3 — frozen protocol set (5 protocols).
- `state/io_spec.md` §4 — pre-registration requirements (PIT-006).
- `state/io_spec.md` §1.1 — sample manifest invariants (PIT-005, PIT-105).
- `state/io_spec.md` §7 — validation commands.
- `state/task_spec.md` — milestones, success criteria, stale rules.
- `state/directions_tried.json` — direction history (current: `reuse_p11_label_leakage`).
- `wiki/concepts/judge-calibration-protocol.md` — the protocol design.
- `wiki/decisions/2026-07-03-p12-configuration.md` — configuration rationale.
- `../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/metadata.json`
  — upstream P11 v5 metadata (`A.n_runs=750`, conditions list, enterprise list).
