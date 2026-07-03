# P1.2 Market Calibration — Knowledge Base Index

> **Experiment**: P1.2 — Settlement / Calibration Layer | **exp_id**: `P12E` | **Model**: Minimax M3
> **Role in portfolio**: external settlement layer for the P1+P2 evidence-ledger mainline (roadmap §7)
> **Knowledge base** → `wiki/` (Marginalia v0.3.1)
> **IO contract** → `state/io_spec.md`
> **Reconfiguration date**: 2026-07-03

> [!memo] 2026-07-03 — Reconfigured as settlement / calibration layer. The old "standalone Polymarket calibration" framing is replaced by the settlement_record contract in `data-contracts.md §9`. Brier/Log Loss is now a means, not the contribution. See [[decisions/2026-07-03-settlement-layer-configuration]].

---

## Concepts

- [[concepts/settlement-calibration-layer]] — **NEW** how P1.2 fits into the P1+P2 evidence-ledger portfolio as the external settlement layer
- [[concepts/prediction-market-calibration]] — Polymarket as an external calibration field (historical framing; now read as a *means* not the contribution)
- [[concepts/brier-score]] — Brier/Log Loss definitions and the M1.5 calculator (still **not implemented**; `calc_brier.py` is a separate milestone)
- [[concepts/factor-ledger]] — Factor Ledger design pointer; the ledger itself lives in P1+P2, **not** here (PIT-301)
- [[concepts/knowledge-writeback]] — knowledge writeback reframed as **belief update with settlement evidence** (roadmap §7)
- [[concepts/ab-test-framework]] — cds4polymarket A/B testing framework; 15+ rounds, 6 domains, Gold-H/M/L judge drift
- [[concepts/cds-background]] — CDS S5 knowledge-validity context; why prediction markets provide a settlement field

## Decisions

- [[decisions/2026-07-03-settlement-layer-configuration]] — **NEW** decision to reconfigure P1.2 as settlement/calibration layer with the `settlement_record` schema
- [[decisions/event-selection]] — M2 event selection (single human checkpoint; PIT-303)
- [[decisions/brier-implementation]] — Brier calculator implementation plan (deferred to M1.5)
- [[decisions/factor-evaluation]] — Factor evaluation method (now points to P1+P2 ledger, not local implementation)

## Annotations

- [[annotations/experiment-log]] — experiment run log
- [[annotations/ab-test-rounds]] — per-round A/B testing analysis (historical)

## Comparisons

- [[comparisons/calibration-methods]] — market calibration vs expert calibration vs historical comparison

---

## Boundaries

| This directory emits | This directory consumes | This directory does NOT do |
|----------------------|--------------------------|----------------------------|
| `settlement_record` rows (one per factor × outcome) | `evidence_ledger_entry.factor_id` from P1+P2 | Own the Factor Ledger (PIT-301) |
| Brier/Log Loss aggregates (numeric + anchor only) | `signal_evidence_entry.numeric_forecast` from P2.1 | Reinterpret text forecasts as numeric (PIT-302) |
| Gold-set audit (`state/calibration_lib_audit.md`) | Frozen Polymarket event outcomes | Lead the paper's contribution narrative |
| Writeback before/after snapshots | — | Add a second human checkpoint (PIT-303) |

Full contract: `state/io_spec.md`. Pitfalls: `experiment-pitfalls.md §4` (PIT-301 to PIT-308).
