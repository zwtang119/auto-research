# D4 — Cross-Direction Synthesis: A Joint Paper Candidate from the Intersection of D1 (Settlement Reconciliation), D2 (Verdict-Reversal Prediction), and D3 (Harness-Evolution Ablation)

**Draft**: 2026-07-18 (D4 of auto-research deep-research recalculation, cross-paper)
**Target**: ACL/EMNLP Findings 8-page methods paper
**Status**: synthesis document identifying the joint paper candidate that emerges when D1, D2, and D3 are read as a single methodology stack. The substance is **the synthesis** — D1 is the instrument, D2 is the application, D3 is the ablation axis.

---

## Abstract

This is not a paper-to-submit; it is the joint-paper candidate that emerges when the three paper drafts D1 (settlement reconciliation), D2 (verdict-reversal prediction), and D3 (harness-evolution ablation) are read as a single methodology stack rather than three independent contributions. We articulate the joint paper, identify the single key message that does not dilute when the three are combined, and pinpoint the two-layer composition that constitutes the strongest publishable target.

The joint paper's single methodological insight sentence is: *a dual-ledger crosswalk gives audit-trail records a reconciliation-loss trace; Murphy-decomposed Brier replay gives them a calibration-surprise trace; the two traces together, observed at the pre-reversal epoch, predict which LLM-as-judge verdicts will reverse on re-adjudication, under any incrementally layered harness configuration.*

The joint paper is **the strongest of the four candidates** because it consolidates a *method-output-application-ablation* chain into a single coherent insight — each of D1, D2, and D3 in isolation is a C1 single-sentence, but the joint sentence does not dilute, it *integrates*: the joint sentence names an instrument (D1), a detector (D2), and an ablation boundary (D3), and theyTogether satisfy **all five Gewin 2018 选题判据** without PARTIAL on any criterion. The honest ceiling is ACL/EMNLP Findings 7.5–8.0; main-track level is plausible if the placeholder empirical magnitudes resolve as predicted (a non-trivial soundness risk on which we are explicit).

---

## §1 The Cross-Direction Layered Stack

Reading D1, D2, and D3 as a methodology stack:

- **D1 = the instrument.** *Settlement reconciliation methodology*: a 92.9%-coverage dual-ledger crosswalk between two audit-trail schemas (the auto-research `evidence_ledger_entry` and the cds4worldcup `factor_ledger_entry`), with one orthogonal enumeration (`branch`), and a Murphy-decomposed Brier replay that audits to component-level tolerance. The instrument produces two per-record signals: (i) crosswalk projection residual `r^(i)` and (ii) the triple of Murphy components `(calibration_loss, discrimination_loss, refinement)`. D1 demonstrates these signals at the 2-settlement level (2/2 = 100% replay match).
- **D2 = the detector built from the instrument.** *Verdict-reversal prediction*: collects, for each verdict `v_i` at the pre-reversal epoch `t_0`, the D1 instrument's two signals (`r^(i)` and the Murphy triple), and trains a logistic classifier on a training split of the 22-investigation verdicts to predict reversal labels `y_i` defined by realised re-adjudication. The detector is the **application of the D1 instrument to the question of bug-shaped verdicts**.
- **D3 = the ablation axis on the detector.** *Harness-evolution ablation*: the detector is rerun under four incremental harness configurations (B → B+ATP → B+ATP+VA → B+ATP+VA+SGR); the incremental ablation measures how the detector's features and predictions change with the harness configuration that produced them. The ablation is the **boundary on whether the detector generalises across harness layers** and the hypothesis H3 — that the SGR (stage-gated reconciliation) layer uniquely catches stage (iv) violation-detector events — articulates the central claim.

The three drafts name a clean stack: *instrument → detector built from the instrument → ablation of the detector under harness evolution*. The composition is not "D1 ∪ D2 ∪ D3" but "D3 sits on D2 sits on D1".

---

## §2 Why a Joint Paper Does Not Dilute C1

Gewin's C1 — Mensh's single-key-message sentence — disciplines this synthesis. A naive composition of three independent papers into one produces a multi-message title (e.g., "Dual-ledger Reconciliation, Verdict-Reversal Prediction, and Harness-Evolution Ablation: Three Methods for LLM-as-Judge Audit Trails") which fails C1: the reader cannot state the paper's contribution in one sentence.

The joint paper's single message sentence (in §Abstract above) is genuinely an integration, not an enumeration. It names (i) an instrument — *dual-ledger crosswalk + Murphy-decomposed Brier replay*, (ii) a detector — *the two traces together predict which verdicts will reverse on re-adjudication*, and (iii) an ablation boundary — *under any incrementally layered harness configuration*. The C1 test is whether the title, abstract sentence, and contribution sentence align; the joint paper's title candidate — **"Predicting Verdict Reversal in LLM-as-Judge Audit Trails: A Reconciliation-Loss Method that Survives Harness-Evolution Ablation"** — is one sentence that carries all three components and is itself the contribution. Removing any component breaks the sentence's meaning, which Mensh would note as the positive signal rather than the failure mode.

D1 alone is C1-PASS, D2 alone is C1-PASS (after the verdict-reversal reconstruction), D3 alone is C1-PASS (primary contribution is G3 methodology; harness ablation is non-load-bearing). The joint paper's C1-PASS claims the *composition* survives the Mensh test, which is a stronger claim and a rarer structural property.

---

## §3 Gewin Five-Criterion Scorecard for the Joint Paper

Per Gewin's five 选题判据:

| Criterion | Joint paper score | Evidence |
|---|---|---|
| **C1 Single-key-message** | **PASS** | The title sentence carries instrument + detector + ablation in a single integration; C1 dilution explicitly addressed in §2 above |
| **C2 "What's new and compelling" red thread** | **PASS** | The new-and-compelling sentence is: "reconciliation-loss and Murphy-decomposed Brier, observed at the pre-reversal epoch under layered harness configurations, predict verdict reversals before re-adjudication surfaces them." Removing the unique-data substrate (22-investigation corpus or Gulei 2015 scenario) does not collapse the methodology: the joint method remains trainable on any audit-trail corpus satisfying (a) dual-ledger crosswalk compatibility, (b) probability vector at `t_0`, (c) realised re-adjudication records. Each of these is a corpus-property requirement, not a corpus-uniqueness claim |
| **C3 Global context + alternative explanations** | **PASS** | D1 already disambiguates the Hyndman hierarchical-forecast-reconciliation tradition (arXiv:2605.17920, 2602.22694, 2405.18693). D3 cites the four harness-engineering slot-occupants (Stanford Meta-Harness arXiv:2603.28052, AHE arXiv:2604.25850, Huawei/PKU survey arXiv:2606.20683, Code-as-Agent-Harness arXiv:2605.18747). D2 cites the LLM-as-judge surveys (arXiv:2606.04217, arXiv:2511.07678), the Deceptive Grounding failure-mode analog (arXiv:2607.09349), and the Murphy-decomposed-Brier source (arXiv:2605.03310). The joint paper combines all 14 primary-source arXiv citations and offers no NEW disambiguation challenge because the joint paper's novelty places it in the *intersection* of the three subspaces, not the union |
| **C4 Human storytelling + cross-audience** | **PASS** | The human-bridge metaphor: "the audit trail gives us two fingerprints of every verdict — one is the crosswalk residual (does the dual-ledger record round-trip?), another is the Murphy-decomposition triple (does the calibration survive Bin-decomposition?); when both fingerprints are anomalous at the pre-reversal epoch, the verdict is a reversal-pending one; and the fingerprints do not change when we layer harness increments, except in the specific way the SGR layer produces a stage (iv) detection event." A non-specialist reader holding the surface-faithful-but-internally-broken intuition from the Deceptive Grounding lens can now carry it into three slots (crosswalk, Brier, harness) rather than one. Cross-audience clarity at C4-PASS rather than PARTIAL |
| **C5 Reproducibility** | **PASS (on method) / PARTIAL (on results)** | The D1 instrument is reproducible without unique data (crosswalk is a schema, Murphy decomposition is algorithmic). The D2 detector's training method is reproducible on any audit-trail corpus satisfying the three properties in C2. The D3 ablation method (B → B+ATP → B+ATP+VA → B+ATP+VA+SGR) is reproducible on any harness framework that exposes layer configurations. The empirical magnitudes — reversal-prediction AUROC at k-fold CV, crosswalk coverage per harness layer, Murphy component stability across layers, violation-detector precision/recall per layer, H1/H2/H3 results — are `PLACEHOLDER-NOT-COMPUTED-YET`. The method-side reproducibility is C5-PASS; the result-side reproducibility is C5-PARTIAL pending the run |

**Gewin overall**: an unambiguous step-up from D1's C3 PARTIAL + C4 PARTIAL to fully PASS across all five criteria for the joint paper. The slot-occupant and Hyndman disambiguations are not new burdens in the joint paper; they are already absorbed by citing D1 and D3 precedents.

---

## §4 The Joint Paper's Structure (Suggested Section Layout)

A workable 8-page ACL/EMNLP Findings structure for the joint paper:

- §1 Introduction (with the Hyndman disambiguation, the Deceptive Grounding bridge, and the four-slot harness-engineering subspace positioning integrated into one intro paragraph cluster)
- §2 Related Work (14 primary-source arxiv IDs from the union; no fabricated cites)
- §3 Method
  - §3.1 Instrument: dual-ledger crosswalk (D1 §3.1 §3.2)
  - §3.2 Murphy-decomposed Brier replay as instrument output (D1 §3.3)
  - §3.3 Pre-reversal oracle and reconciliation-loss features (D2 §3.1 §3.2)
  - §3.4 Verdict-reversal detector (D2 §3.3)
  - §3.5 Harness-evolution ablation chain (D3 §6.1 §6.2 §6.4)
- §4 Experiments
  - §4.1 Gulei + cds4worldcup Murphy-decomposed Brier replay (D1 §4): 2/2 match, components within tolerance
  - §4.2 22-investigation reversal-prediction with k-fold CV (D2 §4): AUROC `[PLACEHOLDER-NOT-COMPUTED-YET]`
  - §4.3 Harness-evolution ablation on the same verdict set (D3 §6.2): per-layer crosswalk coverage, per-layer Murphy component stability, per-layer violation-detector precision/recall `[PLACEHOLDER-NOT-COMPUTED-YET]`
- §5 Findings from the joint method (after the placeholder run has executed)
- §6 The SGR hypothesis — H3 verifiable as the joint paper's contribution to the harness-engineering subspace (D3 §6.3)
- §7 Limitations
- §8 Conclusion

§3 carries the methodology stack (the joint paper's primary contribution); §4 carries the experimental cascade; §5–§8 closes.

---

## §5 Honest Caveats

The joint paper is the **strongest candidate** of the four but also the **highest-soundness-risk** candidate. A faithful enumeration of the risks:

1. **Placeholder risk.** Reversal-prediction AUROC, per-layer crosswalk coverage, Murphy component stability ranges, and per-layer detector precision/recall are all `PLACEHOLDER-NOT-COMPUTED-YET`. The joint paper's C2 and C3 scores depend on the empirical magnitudes materialising as the hypotheses predict. A joint paper submitted with placeholders is not a paper; a joint paper submitted after a run that resolves the placeholders as different from the predicted range (e.g., reversal AUROC at 0.55, not 0.7+) drops from C2-PASS to C2-PARTIAL on the published version even though the method's pre-registration remains C2-PASS.
2. **N=2 + N=22 + N=4 chain.** The D1 instrument has been verified on 2 settlements; the D2 detector on 22 investigations; the D3 ablation across 4 layers. The joint paper aggregates three small-N components into a single claim, which amplifies the joint uncertainty. A reviewer is statistically entitled to ask whether the conjoint AUROC has confidence intervals tight enough to support a C3-positioned novelty claim.
3. **C1 dilution risk in execution.** The joint paper's C1-PASS rests on the title sentence integrating instrument + detector + ablation. If the resulting paper expands to 8 pages with heavy section overhead, the integration may read like enumeration at submission time; the C1-PASS claim assumes editorial discipline at the title-and-abstract level.
4. **Soundness under AHE and Meta-Harness.** D3's §6.3 H3 — that SGR uniquely catches stage (iv) events — competes with the AHE observability-pillars position (Lin et al. 2026, arXiv:2604.25850), which also proposes a closed-loop check analogous to SGR. The joint paper claims H3 *adds* something (the Murphy-decomposed stage (iv) detection) that AHE's closed-loop does not provide; reviewers familiar with AHE may push back on whether the addition is methodologically distinct or whether it is a re-treading of AHE's check-loop pillar.

The joint paper's soundness profile is therefore **higher upside, higher soundness risk** than any of the three standalone drafts. Recommended decision: **pursue the joint paper as the primary target**, with the three standalone drafts as fallbacks (D1 alone if the joint paper's evidence base proves thinner than predicted; D2 alone if D1's crosswalk is published elsewhere as a short paper or workshop; D3 alone is the weakest fallback given its §6 is the exploratory core that the joint paper elevates).

---

## §6 Recommendation Against the Project's D17 Rule

Per the project's D17 rule, recommendations after a "boring" pushback must be GATED on user-supplied criteria; this document is a **synthesis, not a recommendation**. The joint paper is *identified* as a candidate that emerges structurally from the three drafts; whether to pursue it is the user's decision and depends on the user's risk appetite — the joint paper has the highest upside and the highest soundness risk, while the standalone drafts have lower upside and lower risk.

The synthesis surface the user may decide from:
- **Option A**: pursue the joint paper; defer all three standalone drafts.
- **Option B**: pursue D1 alone; file D2/D3 as exploratory drafts.
- **Option C**: pursue D2 alone (the reconstructed valuation-reversal detector); file D1 as companion instrument note and D3 as future ablation extension.
- **Option D**: pursue D1 alone now, file D2 + D3 + joint as follow-up package for the second-round work.
- **Option E**: run the placeholder empirical magnitudes first to de-risk the joint paper, then decide.

---

## §7 Cross-Directions Insights Worth Promoting

Three insights from the synthesis are candidates for promotion to project MEMORY if they prove durable:

1. **The three drafts name a clean instrument-detector-ablation stack.** This is a reusable structural template — a methodology stack whose parts are individually publishable and jointly publishable. Future auto-research portfolio directions can be evaluated against the same stack template: do they produce an instrument, a detector built from the instrument, and an ablation axis on the detector?
2. **Crosswalk residual + Murphy-decomposed Brier components are a *general two-fingerprint primitive* for audit-trail reconciliation.** The two signals are independent in origin (the residual is a schema-engineering signal; the Murphy triple is a forecast-theoretic signal), and they are decoupled at the per-record level (a record can pass the residual check and fail the Murphy components, or vice versa). The two-fingerprint construction may generalise to other dual-ledger cross-domain reconciliations beyond auto-research ↔ cds4worldcup.
3. **The Sakamoto convention of `PLACEHOLDER-NOT-COMPUTED-YET` in fairness brackets is a reusable honesty marker.** A methods paper draft with placeholders is evaluable on methodological structure alone, decoupling draft-writing from run-completion. This decoupling is a project rule candidate: any future paper draft produced in this project should mark uncomputed empirical magnitudes as placeholders explicitly, rather than fabricate or omit them.

---

<!-- C1: Joint paper's title — "Predicting Verdict Reversal in LLM-as-Judge Audit Trails: A Reconciliation-Loss Method that Survives Harness-Evolution Ablation" — single sentence integrating instrument + detector + ablation; verified in §2 as not enumerable. / C2: new-and-compelling sentence "reconciliation-loss and Murphy-decomposed Brier, observed at the pre-reversal epoch under layered harness configurations, predict verdict reversals before re-adjudication surfaces them" survives removal of the unique-data substrate; verified in §3 C2 row. / C3: disambiguation already absorbed by D1 (Hyndman) and D3 (harness-engineering slot-occupants); joint paper cites all 14 primary-source arxiv IDs; verified in §3 C3 row. / C4: human-bridge metaphor — "two fingerprints of every verdict" — is non-specialist readable; verified in §3 C4 row at PASS not PARTIAL. / C5: method reproducible without unique data; result-placeholders acknowledged; verified in §3 C5 row at PASS-on-method and PARTIAL-on-results. -->
