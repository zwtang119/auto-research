## Goal
Execute `state/task_spec.md` milestones in order as the **settlement / calibration layer** for the P1+P2 evidence-ledger mainline (`exp_id: P12E`). On each milestone completion: update `state/progress.json`, append `state/findings.jsonl` and `state/iteration_log.jsonl`. Read `state/io_spec.md` before producing any artefact; the contract binds.

## Role framing (read first)
- Concept: `wiki/concepts/settlement-calibration-layer.md`
- Decision: `wiki/decisions/2026-07-03-settlement-layer-configuration.md`
- Pitfalls: `../../framework/schemas/experiment-pitfalls.md §4` (PIT-301..PIT-308)

## Emits / consumes
- Emits: `experiments/settlement_records.jsonl` (`settlement_record`, `data-contracts.md §9`), `experiments/brier_inputs.jsonl`, `experiments/brier_summary.json`, `experiments/before_after/{before,after}.json`, `state/calibration_lib_audit.md`, `state/implementation_status.md`.
- Consumes: `evidence_ledger_entry.factor_id` from P1+P2; `signal_evidence_entry.numeric_forecast` from P2.1; frozen Polymarket event outcomes.

## ⚠️ Single human checkpoint (PIT-011, PIT-303)
After M2: write `experiments/event_candidates.json` ranked, write `state/blocked.md` with `M2 complete, awaiting human review of top-5 case study candidates.`, then halt. Resume only after human resolution. **No other `level=question` events.**

## Workflow
1. Read `state/task_spec.md` + `state/progress.json`. Find first incomplete milestone.
2. Per milestone: Deliverable + Auto-verifiable → execute → self-check → write back.
3. `stale_count >= 2` → pivot (change event criteria, expand domains, change metric axis — not prompt).
4. `stale_count >= 4` → `state/blocked.md` and stop.

## Paper phase (M6-M9)
- M6 Draft: LaTeX compiles clean, ≥20 refs, all sections present.
- M7 Deep Improvement: ≥6 figures, ≥10 tables, abstract-conclusion aligned.
- M8 Sprint: ≥3 rounds peer review, score trajectory documented.
- M9 Final: zero LaTeX errors.

## Hard non-goals (do NOT)
- No Factor Ledger implementation (PIT-301). P1.2 reads `factor_id`; the ledger lives in P1+P2.
- No `calc_brier.py` in this pass (M1.5 separate milestone, see decision file).
- No text-extract forecasts in headline Brier (PIT-302, DST-15).
- No second human checkpoint (PIT-303).
- No Polymarket pull > 5 events/domain without retry/backoff (PIT-304).
- No "judge is calibrated" claim on 3 gold anchors (PIT-305).
- No writeback comparison without frozen `before.json` (PIT-306).
- No "17 rounds" paper sentence (PIT-307); use directory count.
- No ANOVA with n<3 per cell (PIT-308); directional only.
- No edits to other experiment directories.

## Constraints
- Progress via `state/` files only; logs split into heartbeat / orchestrator / work; outputs to `experiments/`.
- Read-only on `../../cds4polymarket/` and `../../cds4worldcup/`.
- Cap reads: ≤ 5 large files per iteration; ≤ 300 lines per file (PIT-010).
- ~40 rounds → write `state/checkpoint.md` and request restart.

## Known gaps (per `state/task_spec.md` "Known Gaps", unchanged)
- Brier/Log Loss: schema defined, no Python auto-computation → M1.5 (`calc_brier.py`, ~50 lines).
- Factor Ledger: 81-line design doc, 0 Python lines → M3 follows the P1+P2 schema.
- Polymarket API: `/events` only, 15s timeout, ≤5 events/domain.
