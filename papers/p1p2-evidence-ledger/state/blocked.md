# P1+P2 Evidence Ledger — Blocked State

> Created: 2026-07-03
> Purpose: placeholder for the `state/blocked.md` sink referenced by
> `README.md` §5, `state/task_spec.md` §8, and
> `wiki/decisions/2026-07-03-mainline-configuration.md`.
> While `progress.json.blocked == false`, this file stays empty.

## Trigger conditions (from `state/task_spec.md` §8)

- `stale_count ≥ 4`: stop, freeze automation, hand off to a human reviewer.
- Any PIT-201..PIT-206 invariant bypassed for two consecutive iterations with no fix.
- 30 handcrafted entries where `un_settleable_ratio > 0.4` and no documented cause.
- `confidence_delta_distribution` variance = 0 in `experiments/belief_update_stats.json`.
- ≥ 20% of `audit_trace` rows degraded to free text.

## What to write here

When the mainline halts:

1. **When**: ISO timestamp.
2. **What invariant or rule triggered**: link the rule id.
3. **What was the last good state**: pointer to `state/progress.json` snapshot.
4. **Why we cannot self-recover**: one paragraph.
5. **Recommended next move** (not a request to the user; a write-only record).

## Current status

Empty. The mainline is `initialized` per `state/progress.json`.
