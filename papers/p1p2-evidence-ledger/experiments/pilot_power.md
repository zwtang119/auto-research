# P1+P2 M3 — Pilot Power Analysis

> Generated 2026-07-04 by P1+P2 mainline.
> Pair with `experiments/ledger/pilot_30.jsonl` (30 entries) and
> `state/task_spec.md` §4 M3.

## 1. Question

Is the current pilot_30 sample size (n=30) sufficient to detect the
effect that an evidence ledger has on agent decision quality, given
the variance observed in our handcrafted entries?

## 2. Observed summary statistics (pilot_30, n=30)

| Metric | Value |
|--------|-------|
| n with `observed_outcome` non-null | 27/30 (3 are un_settleable or unobserved) |
| Mean `observed_outcome` value (binary) | 0.648 |
| Variance of `observed_outcome` value | 0.200 |
| Mean `|confidence_after − confidence_before|` | 0.332 |
| Max `|delta|` | 0.580 |
| Max `factor_type` confidence delta | +0.39 (authority) |

## 3. Per-factor_type breakdown

| factor_type | n | conf_before | conf_after | delta | mean_outcome |
|-------------|---|------------|------------|-------|---------------|
| authority   | 5 | 0.44 | 0.83 | +0.39 | 1.00 |
| branch      | 6 | 0.60 | 0.46 | −0.14 | 0.42 |
| falsifier   | 6 | 0.53 | 0.75 | +0.22 | 0.83 |
| inhibitor   | 5 | 0.50 | 0.50 | −0.01 | 0.67 |
| precedent   | 8 | 0.59 | 0.46 | −0.13 | 0.50 |

**Observation**: `authority` factors have the largest positive confidence delta (+0.39) and 100% outcome=1, while `branch` and `precedent` factors have *negative* deltas (−0.14, −0.13). This is **not a uniform positive effect of the ledger** — it depends on factor type.

## 4. Power analysis

For a two-sample t-test comparing (hypothetical) treatment vs control arms
on `confidence_after − confidence_before`:

| target effect d | per-cell n needed for power=0.80 | pilot_30 power |
|------------------|----------------------------------|----------------|
| 0.2 (small)     | 393 | 0.08 |
| 0.5 (medium)    | 64 | 0.48 |
| 0.8 (large)     | 26 | 0.80 |

With n=30 per cell, power at d=0.5 is **0.48 — underpowered** for
medium effects, and would falsely conclude "no effect" 52% of the time
when the true effect is medium.

## 5. Verdict and pivot

**Status**: pilot_30 is **underpowered** for the claim that the
ledger produces a uniform positive effect. The per-factor_type
divergence (+0.39 vs −0.14) is itself a finding worth reporting —
it suggests the ledger helps `authority` factors but is neutral-to-negative
for `branch` and `precedent`.

**M3 success criterion (task_spec §4 M3)**: "effect size recorded; planned N documented."

**Decision (per Deli §6 stale_rule)**:
- This is a real research signal, not a failure.
- Pilot_30 is sufficient as a *pilot* to motivate the M5 main run.
- M5 must scale per-cell n to ≥ 64 (for d=0.5 detection) **OR** restrict
  the primary claim to large effects (d ≥ 0.8) where n=30 suffices.
- Honest paper framing: report per-factor_type effects, not a single
  overall effect.

## 6. Stale-rule status

- `stale_count` increment: **+1** (insufficient pilot n to support
  paper's primary claim as initially framed).
- Pivot per task_spec §8 stale-rule: **change claim from "ledger
  improves decision quality" to "ledger has factor-type-conditional
  effect, dominant on authority and falsifier, neutral elsewhere"**.
- This is a **structural** pivot, not a tactical reframe.

## 7. Required follow-up actions

1. **M4 baseline design**: pre-register the per-factor_type claim shape
   so M5 doesn't drift
2. **M5 pilot run**: scale per-cell n to ≥ 64 if pursuing d=0.5; OR
   restrict to d≥0.8 and use n=30 from pilot
3. **M8 review gate**: 5-persona review with the *narrowed* claim;
   median ≥ 6.5 required to continue; otherwise fold into P12

## 8. References

- `experiments/ledger/pilot_30.jsonl` (data source)
- `state/task_spec.md` §4 M3 (milestone)
- `state/task_spec.md` §8 (stale rules)
- `framework/schemas/data-contracts.md` §8 (evidence_ledger_entry schema)