# Layer Roles — P1+P2 in the AutoResearch Portfolio

> Source: `README.md` §3 + `docs/portfolio/aliases.md` §1.
> Purpose: fix the read-only relationship between the P1+P2 conceptual
> mainline and the two sibling mainlines it depends on.

## The three roles

| Layer | Directory | Role in P1+P2 |
|-------|-----------|---------------|
| Evidence **input** | [`../../../papers/p07-signal-fusion/`](../../../papers/p07-signal-fusion/) | Source of `signal_evidence_entry` rows that get promoted into `supporting_evidence[]` / `contradicting_evidence[]`. P1+P2 does **not** re-implement fusion. |
| Evidence **decision contract** | [`../../`](../../) (this directory) | Owns the `evidence_ledger_entry` schema, six invariants, audit trace, and the `confidence_before` / `confidence_after` belief update. |
| Settlement / **calibration** | [`../../../papers/p08-market-calibration/`](../../../papers/p08-market-calibration/) | Consumer of `settlement_rule` and `observed_outcome`; emits `settlement_record` and Brier / Log Loss. P1+P2 does **not** own calibration math. |

## Why this is a separation of concerns

- P1+P2 is the **decision contract** — it asserts that every claim carries its contradicting evidence, missing prerequisites, source independence, freshness, authority, applicability, settlement rule, observed outcome, confidence before/after, and audit trace.
- P2.1 (P7) is the **signal layer** — it asserts that multi-source signals become typed rows with conflict and freshness metadata. P1+P2 reads what P2.1 produces; it does not duplicate fusion logic.
- P1.2 (P8) is the **settlement layer** — it asserts that `settlement_rule` becomes a checkable predicate and produces a calibration score. P1+P2 writes `settlement_rule`; P1.2 evaluates it.

## Anti-patterns this prevents

- PIT-401: re-implementing P2.1 inside P1+P2 (a "12-source fusion" thin paper).
- PIT-403: inventing a separate settlement math in P1+P2 and drifting from P1.2.
- PIT-408: treating P11 free-text reasoning traces as `supporting_evidence[]` (they are at best `observability_comment` with `trace_grounded: false`).

## Cross-references

- `../README.md` §3 "与已有目录的关系" — mainline-authored relationship table.
- `../wiki/decisions/2026-07-03-mainline-configuration.md` — why the layers are separated.
- `../../../docs/portfolio/aliases.md` §1 — code-name → directory map.
- `../../../framework/schemas/data-contracts.md` §8 — schema anchor.
- `../../../framework/schemas/experiment-pitfalls.md` §3 — P1+P2 pitfall ids.
