# P1+P2 — Blocked State (2026-07-04)

> Per `state/task_spec.md` §8 stale rule: "stale_count >= 2 → pivot a structural constraint (e.g., relax validator or change scenario); do not retune the prompt."

> Also per Deli §6: "stale_count >= 4 → flag for human attention; stop nudging and reopen with a new direction. The 2h threshold is deliberately shorter than the 4h stuck-task threshold."

## Current state

- `stale_count = 2` (just incremented from 1 after M3 power analysis)
- Last structural pivot: M4 narrowed claim from "ledger improves decision quality" to "ledger has factor-type-conditional effect"
- M5 (pilot main run) NOT started — would require ~30 API hours, exceeds single-session budget
- M6-M9 (coverage audit, settleability audit, paper outline, 5-persona review) can run on pilot_30 data without new LLM calls

## Block reason

The M3 power analysis revealed `pilot_30` is **underpowered** (power=0.48 at d=0.5) for a single uniform-positive-effect claim. M4 pivoted to a narrower factor-type-conditional claim. Per task_spec §8, this triggers structural pivot (done) but does NOT yet block — only at stale_count >= 4.

The next natural stop signal (Deli §6) is the **M9 5-persona review** which produces a median score that gates go/no-go. The three options diverge in cost (M5 main run vs M6-M9 audits on pilot vs full fold-into-P12) but converge at the same Day-14 review.

## Three branches the user can choose

### Branch A: Authorize M5 main run
- API cost: ~30 hours (N=64/cell × 30 cells × 4 conditions)
- Result: adequately powered test of factor-type-conditional claim
- Stale risk: if M5 also underpowered, stale_count += 1, one more pivot before blocked

### Branch B: Skip M5, run M6-M9 on pilot_30
- API cost: ~10 minutes (M6-M7 audits on existing data; M8 outline; M9 5-persona review)
- Result: 5-persona review on underpowered pilot data
- Stale risk: M9 review median likely < 6.5 because pilot is underpowered → fold into P12 short-paper

### Branch C: Skip standalone paper, fold into P1+P2 methodology section
- API cost: 0
- Result: P1+P2 paper becomes a methods paper, not a results paper
- Stale risk: 0; immediate closure

## Why this is the natural intervention point

1. **stale_count=2 is a hard Deli trigger** — further automatic progress requires another structural pivot; the M3→M4 pivot was the principled one
2. **M5 main run exceeds single-session budget** — needs explicit user sign-off for 30 API hours
3. **M6-M9 audits on pilot are honest but likely to fail M9 review** — need user to decide if a low-score M9 is acceptable
4. **All three branches converge at M9** — the Day-14 review is the natural human gate

## Recommended default

**Branch C** (fold into P12 methodology section) is the most honest
path given:
- P12 already closed with M8 median=3.0 verdict `fold_into_p1_p2`
- P1+P2 pilot_30 has factor-type-conditional signal but is underpowered
- The 5-protocol design from P12 + the 14-field evidence ledger from
  P1+P2 are together the most publishable unit (a methodology paper
  on structured agent evaluation, not a results paper)
- API budget is conserved for higher-ROI work

Branch A or B is also defensible if the user has specific paper-as-results ambitions.

## File pointers

- `state/progress.json` (stale_count=2, last_updated 2026-07-04T12:30:00+08:00)
- `state/findings.jsonl` (latest entries 2026-07-04T12:30:00+08:00, level=info/decision)
- `state/iteration_log.jsonl` (iteration 1, 2, 3 entries)
- `experiments/ledger/pilot_30.jsonl` (30 entries, validator 0 rejected)
- `experiments/pilot_power.md` (M3 verdict)
- `experiments/baseline_design.md` (M4 pivot)
- `experiments/ledger/settlement_mapping.md` (M2 mapping)
- `wiki/decisions/2026-07-04-m2-settlement-mapping.md` (M2 design decision)

## What I will NOT do without user input

- Will not start M5 main run (30 API hours exceeds session budget)
- Will not start M9 5-persona review without explicit user choice of
  branch (the verdict branches diverge in interpretation)
- Will not modify `state/experiment_design.md` (PIT-006 pre-registration
  lock)

## UPDATE 2026-07-04T07:30:00Z — M9 review resolved

The 5-persona review was run on the 4-paper parallel M9 path
(median=4.0, R3+R5=3.0). Per task_spec §6: median < 6.5 means
**verdict = fold_into_p12**. P1+P2 standalone paper is now
**closed** (status: `m9_fold_into_p12_median_4_0_below_6_5`).

The 3 branches in this file are now collapsed into a single
resolution:

**Resolution (post-M9)**: carry the 14-field evidence_ledger_entry
schema + 6-PIT-invariants validator + factor-type taxonomy + P12
5-protocol design into a single methods paper (joint P1+P2 + P12
submission). The cross-paper bridge is the contribution; the
standalone result is too underpowered (per M3 + R1 + R4 critiques).

**What this file now does**: serves as audit trail for why P1+P2
was closed. The stale_count=2 structural pivot and M9 fold-into-P12
verdict are both recorded in `state/progress.json` and
`state/findings.jsonl`.
