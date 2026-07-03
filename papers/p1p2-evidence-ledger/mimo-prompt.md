# P1+P2 Evidence Ledger — Mimo Entry Point

Goal: Auto-execute milestones M1→M9 in `state/task_spec.md` and produce a Day-14 go/no-go (`state/decisions/2026-07-17-go-no-go.md`). Zero interaction.

## Workflow

1. **Boot.** Read `state/task_spec.md` + `state/progress.json`. Update `last_seen`. Find first non-completed milestone.
2. **Pre-flight.** Validate pre-registration (`state/experiment_design.md` exists) and that the chosen direction differs from all `directions_tried.json` entries.
3. **Execute.** Produce the milestone deliverable in the exact path in `state/task_spec.md` §4. Validate against the six invariants in `state/io_spec.md` §2.
4. **Write-back.** Append rows to `state/findings.jsonl` (with `verified: bool`, `pitfall_id`, `source_path`) and `state/iteration_log.jsonl` (with `preflight_pass`, `unresolved_weakness`, `review_median` on review rows). Update `state/progress.json`.
5. **Pivot logic.** No new findings → `stale_count += 1`. At ≥ 2, switch a **structural** axis (scenario, settlement source, audit method). At ≥ 4, write `state/blocked.md` and stop.

## Hard rules

- 5-large-file cap per iteration; ≤ 300 lines per file (PIT-010).
- `evidence_ledger_entry` must satisfy PIT-201..PIT-206.
- `experiment_design.md` is read-only after the run starts (PIT-006).
- Reviews: anti-inflation cap (first ≤ 7.0, +1.5 max/round) and ≥ 2 distinct reviewer models (PIT-002, PIT-107).
- No `level=question` in any log; no user prompts.

## Dependencies

- `../legacy/p11-closed-v5-minimax-m3/` — read only, for **anti-patterns** (PIT-207 / PIT-408); never its `scores.jsonl` as evidence.
- `../papers/p07-signal-fusion/experiments/signals/` — read only, sources `signal_evidence_entry`.
- `../papers/p08-market-calibration/experiments/brier_inputs.jsonl` — read only, sources `settlement_record`.
- `../../../framework/schemas/data-contracts.md`, `../../../framework/schemas/experiment-pitfalls.md`, `../docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md`.

## Stop conditions (mirror `claude-prompt.md` §5)

- Day 14 review median ≥ 6.5 + settlement channel verified → continue.
- Otherwise → fold into P12 short paper.
- `stale_count ≥ 4` → `state/blocked.md`, stop.
