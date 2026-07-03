# Paper Outline — P1.2 Settlement / Calibration Layer

> **exp_id**: `P12E` | **Date**: 2026-07-03 | **Status**: draft, pre-M1.5
> **Framing**: P1.2 is the external settlement / calibration layer that makes the P1+P2 evidence-ledger evaluable. **Not** a standalone "novel calibration method" paper.
> **Independence**: this outline covers the case where P1.2 ships its own short paper. If it does not, P1.2 is consumed as a section of the P1+P2 mainline paper (roadmap §7).

## 1. Title (working)

> Settling Evidence: A Prediction-Market Settlement Layer for LLM Agent Belief Updates

(Chinese working title: 证据结算：面向 LLM Agent 信念更新的预测市场结算层)

## 2. Contribution (one paragraph, anti-PIT-301 / PIT-401 framing)

We contribute a **settlement contract** — `settlement_record` (`data-contracts.md §9`) — that joins structured agent evidence (`evidence_ledger_entry`) to externally resolvable prediction-market outcomes and yields Brier/Log Loss components at the factor level. The contribution is plumbing, not a new calibration algorithm. Three explicit non-claims: (i) we do not claim a Factor Ledger implementation in this paper (PIT-301); (ii) we do not claim "judge calibrated" on the basis of 3 gold anchors (PIT-305); (iii) we do not claim cross-domain significance on n<3 cells (PIT-308).

## 3. Outline

1. **Introduction** — why an evidence ledger needs an external settlement source; why prediction markets fit; what this paper is *not* (a method paper).
2. **Related Work** — prediction markets (Polymarket, Kalshi); agent evaluation methodology; LLM-as-judge calibration (cite P12). Gate G1.
3. **Settlement Contract** — `settlement_record` schema; the `source: numeric | anchor | text-extract` split; the `baseline_sha256_prefix` writeback anchor; the join against `evidence_ledger_entry.factor_id`.
4. **Calibration Layer** — Brier/Log Loss aggregation rules; why text-extract is reported separately (PIT-302); why 3 gold anchors detect offset, not drift (PIT-305).
5. **Experiment** — Polymarket pull (≤5 events/domain, PIT-304); single M2 human checkpoint for event selection (PIT-303); writeback before/after design (PIT-306); n>=30 per cell requirement (PIT-007). Gate G2.
6. **Results** — headline Brier/Log Loss from numeric+anchor only; text-extract sub-aggregate reported separately; cross-domain directional consistency (no ANOVA on small cells, PIT-308).
7. **Discussion** — what the layer does not settle (free-text traces, weak signals); what happens if M1.5 calculator is delayed; how this maps onto the P1+P2 mainline.
8. **Limitations** — gold-set size (PIT-305); Polymarket API retry gap (PIT-304); single M2 checkpoint dependency.
9. **Conclusion** — settlement as the missing external anchor for evidence-ledger agent decisions.

## 4. Figures / Tables plan

| # | Type | Content |
|---|------|---------|
| F1 | Diagram | Boundary diagram from `wiki/concepts/settlement-calibration-layer.md`. |
| F2 | Flow | `settlement_record` join: P1+P2 ledger × Polymarket outcome. |
| T1 | Schema | `settlement_record` field table. |
| T2 | Inventory | AB test directory count vs version range (PIT-307). |
| T3 | Audit | Gold-set size + drift-test limit (PIT-305). |
| T4 | Results | Headline Brier/Log Loss + text-extract sub-aggregate. |
| T5 | Results | Per-domain directional consistency (no ANOVA, PIT-308). |
| T6 | Writeback | before/after snapshot with `baseline_sha256_prefix` (PIT-306). |

## 5. Gates and pre-flight

- Gate G1 (Lit): PIT-001, PIT-307, PIT-407.
- Gate G2 (Exp): PIT-005, PIT-006, PIT-007, PIT-302, PIT-304, PIT-306, PIT-308, PIT-403.
- Gate G3 (Structure): PIT-301, PIT-012.
- Gate G5 (Review): PIT-002, PIT-305, PIT-307.
- A1 State: PIT-001, PIT-009, PIT-010.
- A2 Stall: PIT-011, PIT-303.

Full P1.2 pre-flight: `experiment-pitfalls.md §8.4`.

## 6. Open dependencies

- **M1.5** — `calc_brier.py` implementation (separate config pass; not in scope here).
- **P1+P2 mainline** — produces `evidence_ledger_entry.factor_id` rows for the join.
- **Polymarket** — `/events` endpoint; ≤5 events/domain until retry is added.

## 7. Independence gate (roadmap §7)

P1.2 ships as a standalone short paper **only if** it can show: *prediction-market settlement can stably calibrate agent factor-level belief update*. Otherwise it folds into the P1+P2 mainline as a section.