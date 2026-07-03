# P1.2 — Claude Code Entry Point (Settlement / Calibration Layer)

> **exp_id**: `P12E` | **Role**: external settlement / calibration layer for P1+P2
> **IO contract**: `state/io_spec.md` | **Decision**: `wiki/decisions/2026-07-03-settlement-layer-configuration.md`

## Start

1. Read `state/task_spec.md` and `state/progress.json`. Find the first incomplete milestone.
2. Read `state/io_spec.md` before producing any artefact. The contract binds.
3. Read `wiki/concepts/settlement-calibration-layer.md` for role framing.
4. Read `../../framework/schemas/experiment-pitfalls.md §4` (PIT-301..PIT-308) and §6 prompt anti-patterns.

## What this directory emits

- `experiments/settlement_records.jsonl` — `settlement_record` rows (`data-contracts.md §9`).
- `experiments/brier_inputs.jsonl` + `experiments/brier_summary.json` — typed feed and headline aggregate.
- `experiments/before_after/{before,after}.json` — writeback snapshot pair.
- `state/calibration_lib_audit.md`, `state/implementation_status.md` — drift and design-vs-code audits.

## What this directory does NOT do

- No Factor Ledger implementation (PIT-301). Reads `factor_id` from P1+P2.
- No `calc_brier.py` in this pass (M1.5, separate milestone).
- No text-extract forecasts in headline Brier (PIT-302, DST-15).
- No second human checkpoint (PIT-303). M2 is the only one.
- No Polymarket pull > 5 events/domain without retry/backoff (PIT-304).
- No "judge is calibrated" claim on 3 gold anchors (PIT-305).
- No writeback comparison without frozen `before.json` (PIT-306).
- No "17 rounds" paper sentence (PIT-307); use the directory count.
- No ANOVA with n<3 per cell (PIT-308); report direction only.
- No edits to other experiment directories.

## Workflow

1. Update `state/progress.json` `last_seen` on entry.
2. For each milestone: read Deliverable + Auto-verifiable in `state/task_spec.md`, execute, self-check, write back.
3. Every iteration: append `state/findings.jsonl` and `state/iteration_log.jsonl`.
4. `stale_count >= 2` → pivot (change event criteria, expand domains, change metric axis — not prompt).
5. `stale_count >= 4` → write `state/blocked.md` and stop.

## M2 single human checkpoint (PIT-011, PIT-303)

After M2: write `experiments/event_candidates.json` ranked, write `state/blocked.md` with `M2 complete, awaiting human review of top-5 case study candidates.`, then halt. Resume only after human resolves the candidate list. **No other `level=question` events.**

## Constraints

- Zero interaction outside M2.
- State files are the only source of truth; chat is ephemeral (PAP-10, PIT-009).
- Read-only on `cds4polymarket/` and `cds4worldcup/`. Never move or rename.
- Cap reads: ≤ 5 large files per iteration; ≤ 300 lines per file (PIT-010).
- After ~40 rounds: write `state/checkpoint.md` and ask for restart.

## Pitfalls to self-check before marking iteration done

PIT-301, PIT-302, PIT-303, PIT-304, PIT-305, PIT-306, PIT-307, PIT-308. See `experiment-pitfalls.md §8.4` for the full P1.2 pre-flight checklist.
