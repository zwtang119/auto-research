# P1+P2 Evidence Ledger — Claude Code Entry Point

You are running the P1+P2 evidence-ledger mainline under the Deli_AutoResearch protocol (controllable version). Zero interaction. State files are the only source of truth.

## 1. Cold-start actions (every session)

1. Update `state/progress.json` → `last_seen`.
2. Read `state/task_spec.md`, `state/io_spec.md`, `state/progress.json`, latest row of `state/iteration_log.jsonl`, and the recent rows of `state/findings.jsonl`.
3. Read `wiki/concepts/evidence-ledger-schema.md` and `wiki/decisions/2026-07-03-mainline-configuration.md`.
4. Pick the first milestone in `current_milestone` that is **not** in `completed_milestones`.

## 2. Per-milestone loop

1. Check `state/directions_tried.json`; pick a direction that differs from every prior entry (PIT-008).
2. Execute; write a row to `state/findings.jsonl` AND to `state/iteration_log.jsonl`.
3. Update `state/progress.json` on completion; bump `stale_count` if no new finding (PIT-003).
4. If `stale_count >= 2`, change a structural constraint (scenario, settlement source, audit method); do **not** retune the schema prompt.
5. If `stale_count >= 4`, write `state/blocked.md` and stop.

## 3. Hard constraints

- Read at most 5 large files per iteration; each ≤ 300 lines (PIT-010).
- Never ask the user a question during a run (PIT-011).
- `evidence_ledger_entry` must satisfy PIT-201..PIT-206; failures go to `experiments/rejected_entries.jsonl`.
- P11 free-text traces never become `supporting_evidence[]` (PIT-207).
- `judge_id != "self"` (PIT-013).
- Heartbeat patrol may only `liveness|restart|nudge` (PIT-004).
- Reviews: first round median ≤ 7.0, +1.5/round max, five reviewer personas, and ≥ 2 distinct reviewer models when available (PIT-002, PIT-107).

## 4. Deliverable hand-off

For each finished milestone: write the deliverable under the path listed in `state/task_spec.md` §4; append a row to `state/iteration_log.jsonl` with `preflight_pass: true | false` and `preflight_failed_ids: [...]`.

## 5. Stop conditions

- Day 14 review median ≥ 6.5 + P1.2 settlement channel verified: continue mainline.
- Otherwise: fold back into P12 short paper; do **not** retry this mainline.
- `stale_count >= 4`: stop unconditionally, write `state/blocked.md`.
