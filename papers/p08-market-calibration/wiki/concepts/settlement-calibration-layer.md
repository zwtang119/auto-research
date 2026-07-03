# Settlement / Calibration Layer

> **Concept** | **Author**: portfolio reconfiguration, 2026-07-03 | **Status**: accepted
> **Related decision**: [[decisions/2026-07-03-settlement-layer-configuration]]
> **Owns IO contract**: `state/io_spec.md`

## Definition

The **settlement / calibration layer** is the role P1.2 plays in the 2026-07-03 portfolio layout: it converts P1+P2 evidence-ledger claims into externally verifiable Brier/Log Loss scores by joining each claim's `factor_id` to a real-world Polymarket outcome, and emits a stream of `settlement_record` rows that the P1+P2 project can join against `evidence_ledger_entry.observed_outcome`.

The layer has three jobs:

1. **Settle** — match P1+P2 factors to Polymarket events whose outcomes are already known or scheduled to be known.
2. **Calibrate** — produce Brier/Log Loss aggregates that quantify how well the predicted probability tracks the observed outcome.
3. **Drift-detect** — keep the judge's Gold-H/M/L anchors fresh enough that "judge is calibrated" remains a defensible claim.

The layer explicitly does **not** own factor discovery, factor evaluation, or agent reasoning quality. Those belong upstream (P2.1 for signal input, P1+P2 for ledger).

## Why this role and not "standalone calibration experiment"

The previous framing — "use prediction markets to calibrate LLM agents" — produces a contribution narrative that competes with P12 (judge calibration) and P1+P2 (evidence ledger). Three reasons to reframe:

1. The roadmap (§7) demotes P1.2 from mainline to settlement layer; P1+P2 is the new high-ceiling paper.
2. The Brier/Log Loss computation that would let P1.2 stand alone does not exist yet (`calc_brier.py` is M1.5, deferred); without the calculator, the layer cannot defend a headline number on its own.
3. The P1+P2 evidence-ledger has a hard need for an external settlement source — without it, `evidence_ledger_entry.observed_outcome` is unanchored and the `settleable: true` invariant is vacuous.

Reframing turns P1.2 into the layer that makes P1+P2 evaluable. The contribution shifts from "novel calibration" to "settlement contract that lets a structured ledger be checked".

## Boundary diagram

```
   P2.1 signal_fusion_minimax-m3           P1+P2 evidence-ledger (new mainline)
   ─────────────────────────────          ────────────────────────────────────
   signal_evidence_entry  ─────┐           evidence_ledger_entry
   (numeric_forecast)         │            (factor_id, claim_id,
                                ▼             settlement_rule,
                          ┌─────────────────┐  observed_outcome)
                          │  P1.2 (here)    │ ◀──────────────────┐
                          │  settlement /   │                    │
                          │  calibration    │                    │
                          │  layer          │                    │
                          └─────────────────┘                    │
                                │                                │
                                ▼                                │
                       settlement_record  ─────────────────────► ┘
                       (Brier/Log Loss)
                                │
                                ▼
                       Polymarket outcomes
                       (frozen, /events endpoint)
```

## Settlement contract

`settlement_record` per `data-contracts.md §9`. The contract is the layer's API:

- **Joins** on `factor_id` (from P1+P2) and `event_id` (from Polymarket).
- **Carries** `predicted_p`, `observed_outcome` (0 or 1), `brier_component`, `log_loss_component`.
- **Tags** each row with `source: numeric | anchor | text-extract` so the headline aggregate can filter to `numeric | anchor` only.
- **Anchors** any before/after writeback comparison with `baseline_sha256_prefix` (PIT-306).

## Calibration contract

Brier/Log Loss aggregate per `data-contracts.md §12.7`. Two headline numbers:

- `brier_headline` — over `numeric` and `anchor` rows only.
- `brier_text_extract_only` — reported separately, not part of the headline claim.

The split is structural: text-extracted probabilities (e.g. derived from P2.1's `base/downside/upside` text) are not the same kind of object as a real market quote, and conflating them is PIT-302.

## Drift contract

`state/calibration_lib_audit.md` records the gold-set size and the limit of the drift test it supports. Three anchors can detect a constant offset; they cannot detect distribution shift. If the paper claims "judge is calibrated" on this basis, the gold set must expand (PIT-305, DST-15).

## Non-goals (from `state/io_spec.md §6`)

1. No Factor Ledger implementation. P1.2 reads `factor_id`; it does not write the ledger.
2. No `calc_brier.py` in this pass. The calculator is a follow-up.
3. No second human checkpoint beyond M2 (PIT-303).
4. No text-extract forecasts in the headline Brier (PIT-302, DST-15).
5. No Polymarket pull > 5 events per domain without retry/backoff (PIT-304).
6. No "novel calibration method" claim; the layer is plumbing, not a method.

## Cross-references

- [[decisions/2026-07-03-settlement-layer-configuration]] — the decision
- `state/io_spec.md` — the IO contract
- `framework/schemas/data-contracts.md §9` — `settlement_record` schema
- `framework/schemas/experiment-pitfalls.md §4` — P1.2 pitfalls (PIT-301 to PIT-308)
- `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md §7` — P8 / P1.2 new positioning
- [[concepts/factor-ledger]] — the ledger concept (now owned by P1+P2)
- [[concepts/brier-score]] — Brier/Log Loss definitions (calculator deferred)
- [[concepts/prediction-market-calibration]] — historical framing, still valid as a *means*