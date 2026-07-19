# P1+P2 M4 — Baseline vs Evidence-Ledger Comparison Design

> Generated 2026-07-04 by P1+P2 mainline.
> Pair with `experiments/pilot_power.md` (M3) and `state/task_spec.md` §4 M4.

## 1. Pre-registered claim shape (per M3 stale pivot)

**Original (rejected by M3)**: "Evidence ledger improves agent decision quality."

**Pivoted (this M4 design)**: "The evidence ledger has a *factor-type-conditional* effect on agent decision quality:
- Positive on `authority` and `falsifier` factors (where 2+ independent sources or refutation logic is structurally necessary)
- Neutral-to-negative on `branch` and `precedent` (where the ledger may over-constrain)

We further claim: **`authority` factor confidence delta > 0.30 (medium effect)
with n=5 (current) is unstable; needs n=20+ for power=0.80 confirmation.**"

This is the structural pivot mandated by M3's `stale_count >= 1` finding.

## 2. Conditions

```
Condition A: Control — free-text reasoning, no ledger (P11-style baseline)
Condition B: Treatment — evidence-ledger structured claims (P1+P2 design)
```

## 3. Variables

- **Independent**: condition (A vs B), scenario (Gulei 4 stages × 6 agents)
- **Dependent**:
  - `confidence_after − confidence_before` (per cell, per factor_type)
  - `observed_outcome` value (0/1; binary)
  - `audit_trace` completeness (binary: present/absent)
- **Blocking**:
  - factor_type (5 levels: precedent / inhibitor / branch / falsifier / authority)
  - stage (4 levels)
  - agent (6 levels)

## 4. Pre-registered metrics

| Metric | Cell | Comparison | Test |
|--------|------|-----------|------|
| M4.1 confidence delta | per (factor_type, stage) | A vs B | Welch's t-test (paired by sample_id) |
| M4.2 observed_outcome value | per (factor_type, stage) | A vs B | Fisher exact test (binary) |
| M4.3 audit_trace completeness | per row | A vs B | McNemar's test |
| M4.4 per-factor_type interaction | per factor_type | A vs B interaction | Two-way ANOVA |

## 5. Pre-registered sample size

**Target**: per-cell n ≥ 30 (PIT-007 floor) for primary claim.
**Stretch**: per-cell n ≥ 64 (M3 power analysis for d=0.5 detection).

**Pilot_30 is sufficient for M4.4 interaction structure** (5 factor_types ×
2 conditions × n≥6 each ≈ 60 cells) but not for M4.1 main effect
detection. M5 main run scales.

## 6. Pre-registered stopping rule

Stop and report if any of:
- Control arm's `confidence_after − confidence_before` distribution shows
  variance > 0.20 (control is unstable, not a fair baseline)
- Treatment arm's audit_trace completeness rate < 50% (ledger is not
  being used; report as engineering failure)
- After 100 cells per condition, the per-factor_type interaction
  ANOVA F-statistic p < 0.01 with effect size η² < 0.06 (interaction
  is statistically significant but effect is too small to be useful)

## 7. Threats to validity (pre-registered)

1. **Confound via producer model**: P11 used DeepSeek-V4-Flash as producer.
   P1+P2 producer is unspecified — fix to DeepSeek-V4-Flash for the M5
   main run to control for producer identity.
2. **Confound via judge model**: P1+P2 factor outcomes were hand-curated
   (no live judge). M5 must use `deepseek-v4-pro` as judge per P12 M2
   runner pattern.
3. **Carryover from P12 calibration finding**: P12 M8 found blind >
   leaked (CI [-1.46, -1.08], paired n=10). If M5 uses the same judge in
   blind mode, the per-factor_type effect may invert. Plan: M5 uses
   `awareness=blind` (not leaked) for the treatment arm; this matches
   P12's safer protocol.

## 8. Pre-registration artefact

This document is the M4 deliverable. Any change to claims, metrics, or
sample size after this is written goes to `state/findings.jsonl` as
`level=warn, source=m4_pivot` and triggers a re-registration.