# P2.1 Paper Outline — Evidence Input Layer

> Created: 2026-07-03
> Status: configuration pass. No claims made beyond what `state/io_spec.md`
> and `state/task_spec.md` already declare. **Out of scope**: writing
> prose, picking a venue, deciding on submission format.

## 0. One-line framing

P2.1 is the **evidence-input adapter** of the P1+P2 evidence-ledger
mainline. It does not propose a novel fusion algorithm. Its
contributions are a contract, an ablation protocol, and a
bias-detection side-channel.

## 1. Contributions (allowed, per PIT-401)

| # | Contribution | Type |
|---|--------------|------|
| C1 | `signal_evidence_entry` contract — schema + invariants that let the downstream `evidence_ledger_entry` consume producer rows without re-interpretation. | Artifact |
| C2 | Ablation protocol over the 3-source-group taxonomy (A: Market, B: Event, C: Reference), measured by downstream `source_independence` and `freshness_ratio`. | Method |
| C3 | Bias-detection side-channel with explicit `significance_tested: false`, isolating the Calibrator's 2.0× ratio from the producer rows. | Method |
| C4 | Adapter boundary clarifying what is **not** in scope: free-text reasoning (PIT-408), text-as-probability (PIT-302/406), inactive datasources (PIT-403). | Boundary |

## 2. Forbidden framings (PIT-401)

- "novel fusion algorithm"
- "thin engineering paper"
- "we propose a new way to combine sources"
- any claim that the 267-line chain is itself a contribution

## 3. Section sketch

| § | Title | Anchors |
|---|-------|---------|
| 1 | Introduction | Why 12-source fusion alone is not a paper; what an evidence input layer adds. |
| 2 | Related Work | Signal fusion literature; evidence-based decision making; PIT-207 cross-reference. |
| 3 | `signal_evidence_entry` Contract | Schema + 4 clauses (independence / conflict / freshness / bias). |
| 4 | Ablation Protocol | 3 groups × drop-one; effect on downstream `source_independence` / `freshness_ratio`. |
| 5 | Bias-Detection Side-Channel | Calibrator output as separate rows; `significance_tested: false`. |
| 6 | Adapter Boundary | What P2.1 does not do (free-text → ledger, text-as-probability). |
| 7 | Limitations | 267 lines, ratio-only bias, no statistical test, 1 inactive datasource. |
| 8 | Conclusion | Inputs to P1+P2 evidence-ledger mainline. |

## 4. Tables and figures (≥6 figures + ≥10 tables, per M7)

| ID | Type | Content | Source |
|----|------|---------|--------|
| F1 | Figure | Producer → consumer data flow diagram | `state/io_spec.md §1` |
| F2 | Figure | Conflict discovery walkthrough | `wiki/concepts/signal-to-evidence-contract.md §2.2` |
| F3 | Figure | Freshness-ratio surface | `state/io_spec.md §5` |
| F4 | Figure | Bias-detection side-channel | `state/io_spec.md §6` |
| F5 | Figure | 4-condition × 100-run coverage map | `state/task_spec.md` |
| F6 | Figure | Adapter boundary diagram | this outline §3 C4 |
| T1-T3 | Tables | Per-group ablation results | `experiments/ablation/` (planned) |
| T4-T7 | Tables | Validator pass/fail per PIT-403/408/206/203 | `state/io_spec.md §2.2` |
| T8 | Table | Bias-detection side-channel counts | `experiments/calibrator/` (planned) |
| T9 | Table | MC inventory (4 × 100) | `experiments/mc_inventory.json` (planned) |
| T10 | Table | Component inventory (MemoryLayer = 6) | `state/component_inventory.md` (planned, PIT-407) |

## 5. Cross-references

- `state/task_spec.md` — milestones M1-M9
- `state/io_spec.md` — IO contract and validators
- `wiki/concepts/signal-to-evidence-contract.md` — narrative version
- `wiki/decisions/2026-07-03-evidence-input-configuration.md` — framing decision
- `../../framework/schemas/data-contracts.md` §10 — canonical shape
- `../../framework/schemas/experiment-pitfalls.md` §5 — P2.1 pitfalls
- `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §8 — P7 降级为输入模块

## 6. Out of scope for this outline

- Section prose drafting
- Choice of venue (workshop vs. main track)
- Figure rendering (handled by paper-writing skill group)
- Concrete numerical claims (none yet; the experiments have not been re-run under the new framing)