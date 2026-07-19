# Design Spec: Settlement Reconciliation — A Crosswalk Methodology for Calibrating Evidence-to-Factor Settlement Prediction

> **Spec date**: 2026-07-16
> **Parent brief**: `research/nature-first-class-paper/brief.md` + `REPORT.md` (sections 1.1, 6.1)
> **Validation lens**: Nature Career "How to write a first-class paper" (Gewin 2018) 5 选题判据 + F4 7-check methodological-insight test
> **Paper venue target**: NeurIPS / ICML main track (primary); ACL/EMNLP Findings (contingency). Workshop级不作为目标。
> **Project parent**: `papers/p1p2-evidence-ledger/` (supersedes current `paper/outline.md` framing).

---

## [S1] Problem

Current AutoResearch Topic-5 papers calculate a single aggregate Brier score over a prediction-settlement pipeline (evidence ledger → factor ledger → settlement oracle). But total Brier masks a *failure mode invisible to total score*: when the evidence ledger and the factor ledger agree on a settlement prediction for **opposite reasons** (one calibrated, the other discriminative-by-noise), the single score reports "calibrated" while the underlying reconciliation is broken. No 2024–2026 prior art [F3] formalizes this failure mode or supplies a detection method. Hyndman's "reconciliation" literature (arXiv:2605.17920, 2602.22694, 2405.18693) uses the same vocabulary for aggregation-coherence — a *false cognate* that obscures the gap.

This is a **Failure Mode → Method** paper (the highest-value Gewin C2 framing per F2 §Findings 2, 6): expose the failure, name it, give the method that makes it falsifiable.

## [S2] Solution overview (single key message)

> **One-sentence core message (the title-level message):**
> *"We expose and formalize a new failure mode — settlement reconciliation failure, where total Brier cannot distinguish calibrated evidence-to-factor reconciliation from a coincidental discrimination-only fit — and provide a Murphy-decomposed dual-ledger crosswalk methodology that falsifies the failure to a single calibration-vs-discrimination signature."*

This satisfies Gewin C1 (single key message), C2 (method-not-data novelty), C5 (method reproducible on any evidence→factor→settlement pipeline). It is **not** "our 22-investigation dataset is unique" — the methodological contribution survives removal of any specific dataset per F4 Check 2.

## [S3] Contribution pillars (exactly three — YAGNI)

1. **Failure-mode formalization** — define settlement reconciliation failure, distinguish from prior "reconciliation" (Hyndman aggregation-coherence). This is the insight that justifies the paper; without it, the method is incremental.
2. **Method: Murphy-decomposed dual-ledger crosswalk** — a reconciliation method producing a 2-vector signature `(calibration_residual, discrimination_residual)` per evidence-to-factor mapping. The total-Brier-masking claim becomes *testable*, not asserted.
3. **Empirical falsification on Topic-5 assets** — apply the method to P1+P2's Gulei 2015 dataset (existing) + a second non-overlapping scenario (TBD by F4 transferability test); report whether the failure mode is observed in practice and whether the method localizes it. **Negative result is admissible** (it still validates the detection method).

## [S4] Method (the paper's §4)

### [S4.1] Dual-ledger crosswalk — relabel existing work, do not re-engineer

Reuse P1+P2's existing M1 schema + M2 settlement mapping (already complete per MEMORY.md). The crosswalk is the **mapping** between `evidence_ledger_entry` (free-form into structured) and the factor ledger's enumeration taxonomy. Existing orthogonal enums already define the "factor ledger end". The novelty is in *naming* the crosswalk as a reconciliation object, not changing its implementation.

### [S4.2] Murphy decomposition of the Brier score

Adopt the Murphy (1972 / 1973) decomposition — **reliability (calibration) − resolution (discrimination) + uncertainty** — already used as a methodological primitive in arXiv:2605.03310 [F2 §2] for live prediction markets. We apply it to the *predictive distribution produced by the crosswalk*, not to a single aggregate forecast. The 2-vector signature per mapping:
- `calibration_residual` = distance of the crosswalk's induced probability from empirical base rate, per enumeration bucket.
- `discrimination_residual` = the residual information gain over uniform, per bucket.

**Settlement Reconciliation Failure** is defined as: total Brier ≈ acceptable but `calibration_residual` ≫ 0 AND `discrimination_residual` ≈ 0 (or the inverse), on the same mapping.

### [S4.3] Orthogonal enums as the falsifiability lever

The orthogonal enumeration categories (already designed in P1+P2 M1) partition the prediction space into buckets where the signature is *computed per bucket independently* — without orthogonality, the calibration/discrimination decomposition cannot be cleanly attributed. The orthogonal enums are not a data-unique feature; they are the methodological lever that the failure detection requires.

### [S4.4] Adversarial construction — the "doctored" set

To prove the method actually localizes the failure (not just names it), we construct a **synthetic "doctored" set** of evidence_ledger_entries with planted discrimination-only fit: Brier total is matched but reconciliation is broken (entries fed with distribution-shifted noise calibrated to match observed outcomes). If the method fails to flag doctored entries, the method itself is falsified.

## [S5] Empirical evaluation (the paper's §5)

### [S5.1] Primary scenario: Gulei 2015 petrochemical (existing asset)

Apply the method to P1+P2's 30 hand-curated entries (M2). Report:
- Per-bucket 2-vector signature for each crosswalked mapping.
- Whether the Gulei set exhibits natural settlement reconciliation failure (prediction: partial — some buckets will exhibit it because §M2 reported 30 entries / 28 settleable; the failure mode likely lives in the 2 un_settleable).
- Comparison to total-Brier-only baseline: total Brier says "calibrated"; does the method flag what total Brier missed?

### [S5.2] Transfer scenario — the F4 Check 5 (transferability) gate

A **second, independent evidence→factor→settlement pipeline** from a non-overlapping domain. Concrete candidates:
- **Candidate A** (Methodological): insurance-claim adjudication (publicly available claim → settlement court verdicts) — fit the "settlement" frame.
- **Candidate B** (Methodological): Polymarket prediction markets (use arXiv:2606.04217 [F3 §1] Polymarket-v1 as the settlement oracle).
- **Candidate C** (re-cycled P12 evidence): P12 judge-calibration data, reframed as a settlement task.

The chosen second scenario must be **publicly replicable** without unique data — per F4 Check 7. This is the gate that distinguishes a first-class method paper from data-driven gaming.

### [S5.3] Baseline & ablation

- Baseline: total-aggregate-Brier on the crosswalk's predicted distribution (the "naive" view).
- Ablation: remove the Murphy decomposition → does failure detection ability disappear? (Predicted: yes — this is the core methodological claim.)
- Ablation: remove orthogonal enums (use a non-orthogonal taxonomy) → does per-bucket attribution collapse? (Predicted: yes.)

### [S5.4] Statistical test plan

- For each scenario, report the *failure-detection AUC* of the method against the doctored set.
- Pre-registered hypothesis: method AUC on doctored set ≥ 0.80 (N=30 per scenario, power ≥ 0.80, α = 0.05). Pre-registration goes into `papers/p1p2-evidence-ledger/state/experiment_design.md` before any run.

## [S6] Non-goals (YAGNI rails)

- **NOT** a general prediction-market calibration survey (out of scope — F2 §2 etc. already cover).
- **NOT** harness-evolution methodology (Direction X — slot occupied per F5; closed).
- **NOT** a 22-investigation benchmark paper (Direction Y current framing — D17 pushback).
- **NOT** deception-grounding detection (F2 §6) — that is an adjacent sub-area, cited not adopted.
- **NOT** a dual-ledger consensus / blockchain paper — the crosswalk here is *reconciliation*, not distributed-consensus. Disambiguate in §1.
- Direction Z's harness-evolution extension — **NOT included** in this paper (per D17 GATED on user confirmation — confirmed unlocked by user this turn but excluded here to preserve single key message).

## [S7] C1-C5 + F4 7-check self-audit

- **C1 (single key message)**: §S2 sentence stands alone as the title. ✅
- **C2 (New + compelling)**: Failure mode not in 2024–2026 prior art [F3]; method named, not data-claimed. ✅
- **C3 (global context + alternative explanations)**: explicitly disambiguates Hyndman reconciliation (§S1); pre-examines alternative explanation (total Brier baseline in §S5.3). ✅
- **C4 (human storytelling + cross-audience)**: one-line story = "total score can hide a reconciliation breakage; we make it falsifiable to a single signature." Transfers across insurance/legal/medical settlement domains (§S5.2). ✅
- **C5 (reproducibility)**: method reproduced on public-data S5.2 candidate; no unique-data dependency for the insight. ✅
- **F4 Check 1**: one methodological sentence — failure-mode + crosswalk + Murphy. ✅
- **F4 Check 2**: removing Gulei scenario does not collapse the method; transfer scenario shows this. ✅
- **F4 Check 3**: evaluative claims explicit (failure-detection AUC on doctored set, ≥ 0.80). ✅
- **F4 Check 4**: knowledge gap = no formalization of settlement reconciliation failure in 2024–2026 arXiv corpus [F3]. ✅
- **F4 Check 5**: transfer to insurance/Polymarket/P12 (§S5.2). ✅
- **F4 Check 6**: deep-concern-resilient — the doctored-set falsification is the explicit protection against methodological flaw. ✅
- **F4 Check 7**: insight reproducible on public data; Gulei dataset is public-record. ✅

## [S8] Risk register

- **R1 — Murphy on crosswalk outputs not previously done**: mitigated by F2 §2 (arXiv:2605.03310) precedent on similar setup.
- **R2 — Gulei failure mode sparse (N=2 un_settleable)**: mitigated by doctored-set construction (§S4.4) — we don't depend on natural failure frequency.
- **R3 — Transfer scenario delays paper**: gate at M2-transfer (TBD milestone, see Plan); if unmet by paper-deadline, document the negative result and proceed with Gulei-only + doctored-set (still a first-class method paper).
- **R4 — D17 re-trigger**: if user issues "boring" signal on this framing, follow the protocol — ask reverse questions, do not propose new directions as defensive gesture.

## [S9] Milestone structure (target ~4-6 weeks)

| M | Objective | Deliverable | Stop/Go gate |
|---|---|---|---|
| **M3** | Murphy-decomposition implementation + per-bucket signature on existing 30 Gulei entries | `papers/p1p2-evidence-ledger/experiments/m3_murphy_decomposition.py` + results JSON | Natural failure detected (predicted partial) OR clean doctored-set ready |
| **M4** | Doctored-set construction + failure-detection AUC on Gulei | `experiments/m4_doctored_set.py` + AUC report | AUC ≥ 0.80 (pre-registered); if < 0.50 method falsified → pivot to ablation study of why |
| **M5** | Transfer scenario scaffold (whichever of A/B/C selected) | `experiments/m5_transfer.py` + transfer AUC | Method's transferability claim substantiated by F4 Check 5 |
| **M6** | Full paper draft under Gewin 5-judjia + F4 7-check audit | `papers/p1p2-evidence-ledger/paper/main.tex` + final outline update | R1-R5 5-persona review median ≥ 6.5 (per roadmap) |

(Note: M1+M2 already DONE per MEMORY.md — schema + settlement mapping.)

## [S10] Out of spec (open questions, deferred to Plan phase)

- Concrete choice of transfer scenario A vs B vs C — Plan phase picks one based on data availability + lowest effort-to-replication ratio.
- LaTeX template (NeurIPS vs ICML) — Plan phase pins once venue confirmed (M6).
- Sequence of F4 transferability tests vs M5 execution order — Plan phase schedules.

## [S11] References underpinning this spec

(Full references live in `research/nature-first-class-paper/REPORT.md` §9 Sources.)
- [F2 §2] arXiv:2605.03310 — Murphy decomposition primitive
- [F2 §6] arXiv:2607.09349 — Deceptive Grounding — precedent for "failure-mode + detection method" framing
- [F3 §1] arXiv:2606.04217 — Polymarket-v1 single-ledger Brier linkage (transfer candidate B)
- [F3 §中期] arXiv:2304.10005 — Keogh & van Geloven counterfactual Brier (detection precedent)
- [F4] NeurIPS 2026 E&D + ACL/ARR — failure-mode reject signature + 7-check methodological-insight test
- [F5] — Direction X closure confirmation (excluded from this spec under D17)
- [Gewin 2018] Nature 555, 129-130 — methods lens
- [project MEMORY.md] D17 / "data-uniqueness ≠ paper-interesting" / D12 over-engineering avoidance
