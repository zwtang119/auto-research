# Paper Outline — Evidence-Structured Agent Decision Making for Emergency Response

> Working title. Target: ICLR / NeurIPS main track, contingency for workshop.
> AutoResearch gates (paper-writing skill group): G1 Lit, G2 Exp, G3 Struct, G4 Figs, G5 Review.

## 1. Abstract

Problem. Emergency-response multi-agent systems produce decisions whose evidence is buried in free-text reasoning traces; downstream calibration, settlement and audit cannot reliably connect observations to claims.

Method. We define `evidence_ledger_entry`, a 14-field structured record with six validator-enforced invariants (contradiction/missing disclosure, source independence, freshness, settlement rule, confidence shift, audit trace). We ground the schema on Gulei-class petrochemical events with settlement via prediction-market and public-outcome oracles.

Findings. 30 hand-curated entries resolve to 78% settleability; coverage-vs-conclusion audit flags 12% of entries as evidence-light. Baseline agent fails one of six invariants on 41% of decisions; evidence-ledger variant reduces that to 9% while preserving non-inferior decision quality.

Significance. Establishes the **contract surface** for verifiable agent decisions: it is not a retrieval algorithm, it is a contract that makes downstream arbitration possible.

## 2. Introduction

- Free-text reasoning trace cannot serve as evidence (cite P11 label leakage).
- Decision contract vs. memory writeback.
- Two-week roadmap as a structural not tactical choice.

## 3. Related Work

- LLM-as-judge calibration (links to `papers/p12-judge-calibration/`).
- Factor models in finance / causal inference.
- Prediction-market settlement in agent calibration (links to `papers/p08-market-calibration/`).
- Signal fusion as evidence input (links to `papers/p07-signal-fusion/`).

## 4. Method

### 4.1 `evidence_ledger_entry` schema (cite `data-contracts.md` §8)

### 4.2 Six invariants and their rationale (cite PIT-201..PIT-206)

### 4.3 Bridge to settlement (cite `evidence_ledger_entry.settlement_rule` → `settlement_record`)

## 5. Experiment

### 5.1 Pilot: 10 handcrafted, then 30 settleable
### 5.2 Baseline vs evidence-ledger
### 5.3 Coverage audit + settleability audit
### 5.4 Pilot power analysis (`experiments/pilot_power.md`)

## 6. Results

- Settleability ratio.
- Belief-update variance.
- Invariant hit rate (baseline vs evidence-ledger).
- Failure mode mapping back to PIT-* ids.

## 7. Discussion

- What the ledger **does not** solve.
- Limitations: scope is emergency-response; settlement depends on oracle availability.
- Ethical: settlement requires public outcomes; ambiguous outcomes remain `un_settleable: true`.

## 8. Conclusion

- The contract surface is the contribution.
- Path forward: standardize `evidence_ledger_entry` as a deliberation artefact.

## 9. References

≥ 60 cited works covering LLM-judge calibration, factor models, settlement markets, signal fusion.

## 10. Appendices

- A. Full schema JSON example (10 entries).
- B. Validator implementation notes.
- C. Pilot run ledger (`experiments/ledger/pilot_run.jsonl`).
- D. Pre-registration (`state/experiment_design.md`).
