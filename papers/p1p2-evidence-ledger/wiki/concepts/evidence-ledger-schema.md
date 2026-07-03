# Evidence Ledger Schema

> Source: `../../../../framework/schemas/data-contracts.md` §8; pitfall ids from §3 of `experiment-pitfalls.md`.

## Purpose

An `evidence_ledger_entry` is the atomic unit of a decision. It binds a **claim** to its **supporting** and **contradicting** evidence, names its **missing prerequisites**, declares **source independence**, **freshness**, **authority**, **applicability**, **factor type**, a machine-checkable **settlement rule**, an **observed outcome**, **confidence before/after**, and an **audit trace**.

## The 14 fields

| # | Field | Type | Why it must exist |
|---|-------|------|-------------------|
| 1 | `claim_id` | `C-P1P2-NNN` | decision-level handle |
| 2 | `decision_context` | string | narrows the universe of applicability |
| 3 | `supporting_evidence[]` | refs | positive signal |
| 4 | `contradicting_evidence[]` | refs | negative signal (PIT-201) |
| 5 | `missing_prerequisites[]` | refs | honest gap declaration (PIT-201) |
| 6 | `source_independence` | int ≥ 1 | guards authority claims (PIT-202) |
| 7 | `freshness`, `freshness_window`, `freshness_ratio` | trio | time-weighted truth (PIT-203) |
| 8 | `authority` | enum high/med/low | gauge of provenance weight |
| 9 | `applicability` | string | transfer boundary |
| 10 | `factor_type` | enum | precedent / inhibitor / branch / falsifier / authority |
| 11 | `settlement_rule` | predicate | what would falsify or confirm (PIT-204) |
| 12 | `observed_outcome` | {label, ts, value} | ground truth once available |
| 13 | `confidence_before` / `confidence_after` | float [0,1] | belief update shape (PIT-205) |
| 14 | `audit_trace[]` | structured steps | auditability (PIT-206) |

## Six invariants (one line each)

1. PIT-201: a claim must declare either contradicting evidence or missing prerequisites.
2. PIT-202: authority needs at least two independent sources.
3. PIT-203: stale ratio > 1 ⇒ claim flagged `stale: true`.
4. PIT-204: settleable ⇒ settlement rule is a checkable predicate.
5. PIT-205: 80% of entries must shift confidence; zero variance is a failure signal.
6. PIT-206: audit trace is an array, not a free-text comment.

## Why not "supporting + retrieved" only

Confirmation only writes are exactly what killed P11's H1. The ledger contract forces **negative** and **missing** evidence into the entry, otherwise downstream evaluation silently trusts the producer.
