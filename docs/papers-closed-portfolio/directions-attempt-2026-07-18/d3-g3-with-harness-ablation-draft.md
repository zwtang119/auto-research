# Settlement Reconciliation with Harness-Evolution as an Ablation Subsection: A Dual-Ledger Schema-Engineering Paper with an Incremental Harness-Evolution Extension

**Draft**: 2026-07-18 (D3 of auto-research deep-research recalculation)
**Target**: ACL/EMNLP Findings 8-page methods paper
**Status**: prose draft, not outline. Primary contribution is **settlement reconciliation** (companion standalone paper: see `docs/papers/directions-attempt-2026-07-18/d1-g3-standalone-paper-draft.md`); the substantive new content of this paper is **§6 Harness-Evolution Ablation**.

---

## Abstract

Audit-trail schemas produced by LLM-as-judge systems vary in field structure across decision domains, blocking cross-domain replay of calibration evidence. We propose a *dual-ledger crosswalk* between two independently developed audit-trail schemas — the `evidence_ledger_entry` of the auto-research framework (decision-role framing, 14 required fields) and the `factor_ledger_entry` of the cds4worldcup settlement pipeline (causal-direction framing, 12 required fields) — and we show that 92.9% of the auto-research fields forward-map to the cds4worldcup schema with exactly one shared enumeration term (`branch`) that the two schemas interpret orthogonally. We apply a Murphy-decomposed Brier replay (Nechepurenko 2026, arXiv:2605.03310) to the two available unit settlements, obtaining 2/2 matches. We disambiguate our *settlement reconciliation* from the hierarchical-forecast-reconciliation tradition of Hyndman and colleagues (arXiv:2605.17920, arXiv:2602.22694, arXiv:2405.18693), which targets aggregation-coherence rather than settlement alignment, and we draw a structural parallel to Deceptive Grounding (Caruzzo 2026, arXiv:2607.09349), where the entity responsible for a stated fact is misattributed while surface faithfulness checks pass.

The **primary contribution** of this paper is the settlement-reconciliation methodology; the §6 Harness-Evolution Ablation is an extension. The methodology survives removal of any single scenario (the Gulei 2015 emergency-medicine case is illustrative, not load-bearing), and it survives removal of the entire §6 ablation extension. The §6 extension investigates the open methodological question: does an incremental layering of harness configurations — baseline harness, +audit-trail preservation, +verdict appeal, +stage-gated reconciliation check — degrade or preserve the crosswalk's coverage and the Murphy decomposition's component stability? We frame three falsifiable hypotheses (H1–H3) as targets for future empirical evaluation; numerical magnitudes are left as `PLACEHOLDER-NOT-COMPUTED-YET` to keep the draft honest.

---

## §1 Introduction

LLM-as-judge systems leave audit trails shaped by the local vocabulary of their decision domain. An auto-research `evidence_ledger_entry` speaks of *factors* and *precedents* in the *decision-role* framing; a cds4worldcup `factor_ledger_entry` speaks of *precursors* and *suppressors* in the *causal-direction* framing. Whether these two ledgers can be reconciled into a single replayable audit record — and whether the reconciliation is robust to incremental changes in the harness that produces the record — is the methodological question of this paper.

A reader of the title may reasonably ask whether *reconciliation* here means the hierarchical-forecast reconciliation of the Hyndman tradition (Athanasopoulos et al. 2024, arXiv:2405.18693; Wickramasuriya et al. 2026, arXiv:2602.22694; Pan et al. 2026, arXiv:2605.17920). It does not. In that literature, reconciliation is the post-hoc adjustment of forecasts so that lower-level predictions aggregate coherently to upper-level totals; the object reconciled is a numeric distribution, and the criterion is a coherence constraint. In our work, reconciliation is the alignment of two audit-trail schemas so that a settlement record produced under one schema can be replayed under the other, with Brier scores reproducible to a stated precision; the object reconciled is a field-and-enum structure, and the criterion is a settlement predicate. We use the phrase *settlement reconciliation* throughout to mark this distinction.

Deceptive Grounding (Caruzzo 2026, arXiv:2607.09349) is instructive as a cross-audience bridge because it isolates a failure mode that is invisible to standard faithfulness checks: an answer can be locally well-grounded (97% precision in the Caruzzo experiments) and yet misattribute the *entity* responsible for a stated fact. The same structural blindness arises in settlement reconciliation — a settlement record can pass every local field check and still misattribute the *factor type* or *event relation* that licenses a probability.

### Harness engineering as a published subspace

The harness engineering of LLM agents has consolidated as a methodology-subservable research space. Jung et al. (2026, arXiv:2604.07236) externalize the agent harness so that harness-layer contributions become measurable separately from the LLM residual. The AHE paper (Lin et al. 2026, arXiv:2604.25850) proposes three observability pillars for harness reasoning; the Huawei/PKU survey (Han et al. 2026, arXiv:2606.20683) consolidates the harness-engineering subspace from QA to task completion; and the "Code as Agent Harness" framing (Ning et al. 2026, arXiv:2605.18747) treats harness configuration as a first-class engineering object. The Stanford Meta-Harness work (Lee et al. 2026, arXiv:2603.28052; canonical repo `github.com/stanford-iris-lab/meta-harness`) provides an outer-loop search framework. These four papers establish harness-engineering as an occupied subspace; the §6 ablation extension of this paper is *not* a new harness methodology, but an incremental layer evaluation of crosswalk resilience against layered harness configurations.

What is new and compelling in this paper is the **demonstration that settlement reconciliation survives incremental harness layering** — a methodological claim that complements the primary dual-ledger crosswalk of the companion paper. The companion paper (`d1-g3-standalone-paper-draft.md`) demonstrates that the two ledger schemas admit a 92.9% forward coverage with one shared term and zero conflicting enumerations, and that 2/2 available unit settlements replay under Murphy-decomposed Brier scoring. This paper extends the methodology to ask: at which harness layer does settlement reconciliation fail to pass?

---

## §2 Related Work

We position this paper at the intersection of three literatures. The LLM-as-judge surveys (Zhang et al. 2026, arXiv:2606.04217; Li D. et al. 2024, arXiv:2511.07678) catalogue biases and generation-to-judgment taxonomies but do not address the ledger level at which cross-domain replay becomes possible. The bias-detection literature — Deceptive Grounding (Caruzzo 2026, arXiv:2607.09349) and calibrated-judge analysis with Murphy-decomposed Brier (Nechepurenko 2026, arXiv:2605.03310) — provides the two diagnostic lenses we apply. The audit-trail and benchmark papers (Kumar et al. 2026, arXiv:2607.01661; Lin et al. 2026, arXiv:2607.09921) inform the accountability framing.

The hierarchical-forecast-reconciliation tradition (Athanasopoulos et al. 2024, arXiv:2405.18693; Wickramasuriya et al. 2026, arXiv:2602.22694; Pan et al. 2026, arXiv:2605.17920) shares the word *reconciliation* but not the underlying operation — its reconciliation is to a coherence constraint on numeric distributions, whereas ours is to a settlement predicate on field-and-enum structures.

The harness-engineering subspace is established by four primary-source papers: Stanford Meta-Harness (Lee et al. 2026, arXiv:2603.28052), Agentic Harness Engineering (Lin et al. 2026, arXiv:2604.25850), the Huawei/PKU harness survey (Han et al. 2026, arXiv:2606.20683), and the Code-as-Agent-Harness framing (Ning et al. 2026, arXiv:2605.18747). Our §6 extension is positioned against this occupied subspace as an incremental layer evaluation, not a new harness methodology.

---

## §3 Method (brief recap; full treatment in companion D1)

The methodology of this paper is the settlement reconciliation introduced in the companion paper; we summarize briefly here and refer the reader to Section 3 of `docs/papers/directions-attempt-2026-07-18/d1-g3-standalone-paper-draft.md` for full treatment.

### §3.1 Dual-ledger crosswalk

Let $L^{AR}$ denote the `evidence_ledger_entry` schema (14 required fields) and $L^{CWCUP}$ the `factor_ledger_entry` schema (12 required fields). Of the 14 AR fields, 13 forward-map to CWCUP targets under named shape transformations (principal-counter-signal rule for list-to-string projection; linear rescale for confidence fields; timestamp-cause markers for `ts_created` → `settled_at_utc`). Forward coverage is $13/14 = 92.9\%$. Reverse coverage is $8/12 = 66.7\%$, with four CWCUP-specific fields (`origin`, `match_id`, `direction`, `quantified_threshold`) carrying the causal-direction framing. The asymmetric coverage is not a flaw; AR is the richer schema and projects into the leaner CWCUP without fatal loss.

### §3.2 Orthogonal enumeration

The AR `factor_type` enumeration $\{$ `authority`, `branch`, `falsifier`, `inhibitor`, `precedent` $\}$ (decision-role) overlaps with the CWCUP `event_relation` enumeration $\{$ `branch`, `counter_signal`, `precursor`, `suppressor` $\}$ (causal-direction) in exactly one term: `branch`. We construct the orthogonality by assigning `branch` a dual interpretation resolved at replay by inspecting the parent ledger. An AR `branch` factor is replayed as a CWCUP `branch` event with a decision-role marker; vice versa for the CWCUP `branch` event. No information is lost. The AR `observed_outcome` and CWCUP `calibration_status` enumerations are semantically orthogonal and survive the crosswalk without remapping.

### §3.3 Murphy-decomposed Brier replay

Given a settlement probability vector $p = (p_1, \ldots, p_k)$ and a realized one-hot outcome $o$, the Brier score is $\text{Brier}(p, o) = \frac{1}{k}\sum_i (p_i - o_i)^2$. Following Nechepurenko (2026, arXiv:2605.03310), we decompose:

$$\text{Brier} = \text{calibration}_{\text{loss}} + \text{discrimination}_{\text{loss}} + \text{refinement}$$

A settlement match requires both raw-score and component-level match within tolerance $10^{-4}$. The Murphy decomposition's diagnostic value: a raw-match that hides a swap between calibration and discrimination is caught at the component level.

### §3.4 Settlement-reconciliation violation detection

Mirroring Deceptive Grounding (Caruzzo 2026, arXiv:2607.09349), a settlement record can pass every local field check and still misattribute the `factor_type` or `event_relation` licensing the probability vector. A settlement-reconciliation violation is a record that passes (i) crosswalk field check, (ii) enumeration-orthogonality check, (iii) raw Brier check, but (iv) fails the Murphy-decomposed Brier check. Stage (iv) is where the Deceptive-Grounding analogue lives, and is the event that the Murphy decomposition uniquely catches.

---

## §4 Experiments (brief recap)

The primary experiment replicates the companion D1: a 2/2 (100%) Murphy-decomposed Brier replay match across the `wc2026-a-m01-mex-rsa` settlement (card v0.1 with probability vector $[0.55, 0.27, 0.18]$) and `wc2022-a-f01-qat-ecu`. Both settlements satisfy the four-stage detector at stages (i)–(iii); stage (iv) Murphy components also match within $10^{-4}$. The Gulei 2015 emergency-medicine scenario sits as illustrative context, not as load-bearing data.

---

## §5 Findings from primary method

Findings from the primary settlement-reconciliation methodology (crosswalk coverage 92.9%, Brier replay 2/2, Murphy components match within tolerance) confirm that two ledger schemas developed in independent codebases, with different framing vocabularies, admit a single replayable audit record under Murphy-decomposed Brier. For full treatment of these findings including the negative-result appendix on anchoring-bias manipulation, see the companion paper at `d1-g3-standalone-paper-draft.md`. The remainder of this paper extends the methodology along a harness-evolution axis.

---

## §6 Harness-Evolution Ablation

The §6 extension is the substantive new contribution of this paper. We ask: how does the methodology documented in §3–§5 perform when the harness that produces the audit trail is layered incrementally? The harness-engineering subspace (§2) has established that the agent harness layer is itself an engineering object; we propose to use it as an ablation axis on settlement reconciliation rather than as a contribution in its own right.

### §6.1 Layered harness configurations

We define four ordered harness layers, each a strict superset of the previous:

- **B (baseline harness).** The agent harness produces a verdict; no audit-trail preservation, no verdict appeal, no stage-gated reconciliation. Only the final verdict and its probability vector survive the run.
- **B+ATP (B plus audit-trail preservation).** The harness retains the full audit trail — every intermediate LLM call, every retrieved evidence item, every ledger entry written — to the evidence ledger. The audit trail is queryable post-run.
- **B+ATP+VA (B+ATP plus verdict appeal).** A second LLM call, with access to the first verdict and the audit trail, may affirm or appeal the first verdict. The appealed record is itself logged in the audit trail.
- **B+ATP+VA+SGR (full configuration, plus stage-gated reconciliation).** Between B+ATP+VA and final acceptance, an automated G3 violation detector (§3.4) is invoked as a checkpoint. A record that fails stage (iv) triggers re-adjudication before acceptance. This is the stage-gated reconciliation layer.

The constructions are not new harness architectures; they instantiate configurations that the harness-engineering literature has already proposed (Lee et al. 2026, arXiv:2603.28052; Lin et al. 2026, arXiv:2604.25850). The contribution here is the application of these layers as an ordered ablation chain on the crosswalkʼs resilience.

### §6.2 Incremental ablation measurement

For each layer $\ell \in \{$ B, B+ATP, B+ATP+VA, B+ATP+VA+SGR $\}$, we measure:

- **(a) Crosswalk coverage** at $\ell$: the percentage of AR ledger entries written at $\ell$ that forward-map to CWCUP targets with named shape transformations. Reported as a value in $[0, 1]$.
- **(b) Murphy-decomposed Brier component stability**: the range of `calibration_loss`, `discrimination_loss`, and `refinement` across the four layers. Reported as per-layer tuple $(C_\ell, D_\ell, R_\ell)$.
- **(c) Violation detector accuracy**: the precision and recall of the stage (iv) detector at $\ell$, computed against a held-out gold set of pre-registered violated records. Reported as $\text{precision}_\ell$ and $\text{recall}_\ell$.

Numerical results are *not yet computed*; the values reported in final form will be `PLACEHOLDER-NOT-COMPUTED-YET` until the layered ablation runs are executed. We deliberately mark them as placeholders rather than fabricate; this is a methods paper draft, not a paper-with-results.

### §6.3 Hypotheses (falsifiable, marked HYPOTHESIZED-NOT-TESTED)

We articulate three falsifiable hypotheses to which empirical evaluation of §6.2's measurements may speak:

- **H1 (crosswalk resilience).** The crosswalk coverage remains at or above 80% — the G3 threshold set by the companion D1 paper — across all four harness layers. Equivalently: incremental harness layering does not break the 92.9% forward coverage. *Falsification*: any layer $\ell$ at which coverage drops below 80% falsifies H1.
- **H2 (component sensitivity asymmetry).** The `calibration_loss` component is more sensitive to harness-layer changes than the `refinement` component. *Falsification*: if the per-layer range of `calibration_loss` (max minus min across the four layers) is smaller than the per-layer range of `refinement`, H2 is falsified. The intuition is that `calibration_loss` is a function of the harness's confidence-bin construction (which ATP, VA, SGR each modify) whereas `refinement` is a lower bound set by the realized outcome distribution (which the harness does not modify).
- **H3 (SGR uniquely catches stage (iv) events).** The stage-gated reconciliation layer (SGR) is the only layer at which stage (iv) violation-detector events are caught *prior to acceptance*. Equivalently: the precision and recall of violation detection at the B+ATP+VA+SGR layer exceed the precision and recall at B+ATP+VA. *Falsification*: if precision and recall at SGR do not exceed those at B+ATP+VA, the dedicated SGR layer does not pay its way and H3 is falsified. By construction, SGR pre-acceptance checking exposes stage (iv) events; H3 thus claims that exposure converts to detection improvement, which is a contingent empirical claim not a tautology.

Each hypothesis is marked `HYPOTHESIZED-NOT-TESTED` until §6.2's measurements run. The framing in falsifiable form means a failed hypothesis is informative: if H1 fails, the crosswalk is not robust to harness layers, which itself is a publishable finding with implications for harness design.

### §6.4 Functional pathway to implementing the ablation

The ablation is implementable as a strict chain on existing harness-engineering primitives. The harness layer configuration is exposed via the LLM agent loop; the audit-trail preservation layer (B+ATP) is a configurable trace collector that serializes every intermediate LLM call into the evidence ledger; the verdict-appeal layer (B+ATP+VA) is a second-pass adjudication call that draws on the first verdict's audit trail; the stage-gated reconciliation layer (SGR) is an inter-stage check that invokes the §3.4 violation detector on the just-written settlement record and, on failure, triggers re-adjudication.

The SGR layer has direct precedence in the harness-engineering literature (Lin et al. 2026, arXiv:2604.25850, AHE's three observability pillars include a check-loop pillar analogous to SGR; Lee et al. 2026, arXiv:2603.28052, Meta-Harness's outer-loop search is an SGR analog). The contribution of §6 is the connection of these precedents to settlement reconciliation specifically, and the demonstration (under H3) that this connection raises the precision-and-recall envelope of stage (iv) detection.

---

## §7 Limitations

The primary settlement-reconciliation methodology inherits the limitations of the companion D1 paper: N=2 available settlements is small; Hyndman disambiguation poses a reader-burden for non-specialists; and the negative-result appendix on anchoring-bias manipulation is pre-registered but not load-bearing. We refer readers to D1's §5 for the full primary-method limitations.

The §6 Harness-Evolution Ablation extension carries additional limitations:

1. The hypotheses (H1–H3) are framed falsifiably but their empirical magnitudes are `PLACEHOLDER-NOT-COMPUTED-YET`. A methods paper draft with placeholders is honest, but a camera-ready submission needs the ablation runs.
2. The four-layer chain (B → B+ATP → B+ATP+VA → B+ATP+VA+SGR) reflects only one ordered ablation. Other orderings and other layer types (e.g., +retrieval-verifier, +reasoning-trace-audit) are expressible in the harness-engineering subspace but not evaluated here.
3. The harness-engineering subspace has four primary-source occupant papers (Stanford Meta-Harness, AHE, Huawei/PKU survey, Code-as-Agent-Harness). The §6 ablation extends methodology against an occupied subspace — readers may reasonably ask whether any layer construction re-treads a published pillar; we cite the four papers to mark the boundaries.

---

## §8 Conclusion

The primary contribution of this paper is the settlement-reconciliation methodology (dual-ledger crosswalk + orthogonal enumeration + Murphy-decomposed Brier replay + violation detector), documented in full in the companion paper. The §6 Harness-Evolution Ablation extends the methodology along an incremental layer axis and articulates three falsifiable hypotheses (H1–H3) about crosswalk resilience and component sensitivity. The key message is that settlement reconciliation is the load-bearing primary contribution; harness-evolution is an exploratory ablation extension suggesting that the crosswalk's resilience can be evaluated against harness-engineering's occupied subspace. Future work is the empirical evaluation of H1–H3 under the §6.2 measurement protocol, and the extension of the layered chain beyond the four layers defined here.

---

<!-- C1: Primary contribution dominates? Title says "Settlement Reconciliation ... with Harness-Evolution as an Ablation Subsection" — primary dominates; harness-evolution is explicitly framed as non-load-bearing in Abstract §1 §8 and in §3–§5 pointers. The paper survives both removal of the Gulei scenario (Abstract assertion) and removal of the entire §6 ablation (the §3–§5 standalone method extends verbatim from D1 with §6 as additive). / C2: Single methodological-insight sentence preserved? "The primary contribution is settlement reconciliation; §6 Harness-Evolution Ablation extends the methodology along an incremental harness-layer axis." Single sentence contains both. NeurIPS E&D "datasets-as-endpoints don't meet the bar" avoided: §6 frames hypotheses as falsifiable methodological claims, not data uniqueness. / C3: Slot-occupants cited explicitly? §1 and §2 cite Stanford Meta-Harness (arXiv:2603.28052), AHE (arXiv:2604.25850), Huawei/PKU survey (arXiv:2606.20683), Code-as-Agent-Harness (arXiv:2605.18747) — all four named slot-occupants per F5 verified. Hyndman reconciliation (arXiv:2605.17920, 2602.22694, 2405.18693) disambiguated explicitly. / C4: Harness-jargon-burden mitigation? Defined each acronym (ATP, VA, SGR) in §6.1 with both an English phrase and abbreviation; the hardware-jargon label "stage-gated reconciliation (SGR)" given a one-line functional definition in §6.4 ("an inter-stage check that invokes the violation detector on the just-written settlement record and, on failure, triggers re-adjudication"). Harness term burden acknowledged in §7 limitations. / C5: Reproducibility? Methodology §3 reproducible without unique data (passes F4 Check 7); §6 ablation hypotheses are stated in falsifiable form with measurement protocol in §6.2 (a)(b)(c). All numerical magnitudes marked PLACEHOLDER-NOT-COMPUTED-YET; nothing is fabricated. -->
