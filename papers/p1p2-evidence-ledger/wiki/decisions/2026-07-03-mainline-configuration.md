# 2026-07-03 — Mainline Configuration Decision

> Status: ACCEPTED · Owner: P1+P2 worker · Date: 2026-07-03

## Why schema-first, not benchmark-first

Roadmap §6.2 explicitly rejects the framing "RAG接入后效果更好". The contribution must be the **ledger contract**, not another retrieval benchmark. Therefore:

- Day 1-2 deliverable is `evidence_ledger_entry` schema + 10 handcrafted entries, not a retrieval leaderboard.
- The first ever `experiments/ledger/pilot_10.jsonl` is hand-curated to demonstrate that every field can be filled honestly and that the six invariants catch the most common shortcuts.

## Why not "extend P2.1 first"

P2.1 is repositioned as evidence-input layer (roadmap §8). Same-direction work would compete with the deployed harness, dilute `signal_evidence_entry`, and re-introduce PIT-401 ("267 lines as research contribution"). P1+P2 reads what P2.1 produces; it does not duplicate it.

## Why not "extend P1.2 first"

P1.2 must own the **settlement** semantics (Brier / Log Loss / factor evaluability). If P1+P2 invents its own settlement layer, both projects will drift. The contract is: P1+P2 writes `settlement_rule`; P1.2 evaluates it. This is a **separation-of-concerns**, not a delay.

## Anti-patterns explicitly disallowed

- PIT-001: do not write claims or citations without `verified: true` and a `source_path`.
- PIT-006: do not move the goalposts after seeing the pilot numbers — freeze `state/experiment_design.md` before any run.
- PIT-207 / PIT-408: P11 free-text traces **never** enter `supporting_evidence[]`. They may appear as `observability_comment` at most, with `trace_grounded: false`.

## Stale / pivot plan

- `stale_count ≥ 2`: swap the **scenario** (e.g., from Gulei to a public Polymarket outcome), not the schema prompt.
- `stale_count ≥ 4`: stop, write `state/blocked.md`, hand back to a human reviewer.

## Cross-references

- `state/task_spec.md` §4 milestones, §8 stale rules.
- `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §6 mainline.
- `../../../../framework/schemas/data-contracts.md` §8 evidence ledger entry.
- `../../../../framework/schemas/experiment-pitfalls.md` §3 P1+P2 traps.
