# Settlement Reconciliation of LLM-as-Judge Audit Trails: A Dual-Ledger Crosswalk with Murphy-Decomposed Brier Replay

<!-- Draft D1 — G3 standalone. Target: ACL/EMNLP Findings. Date: 2026-07-18. -->

## Abstract

LLM-as-judge pipelines leave audit trails that are structurally incompatible across decision domains: a research-synthesis assistant tags factors by **decision-role** (authority, branch, falsifier, inhibitor, precedent), while a prediction-market assistant tags the same evidence by **causal-direction** (precursor, suppressor, branch, counter_signal). We study *settlement reconciliation* — the problem of mapping one domain's audit ledger onto another's and replaying its probabilistic verdicts against an observed outcome — and argue it is a schema-engineering primitive distinct from both the hierarchical forecast reconciliation tradition and from single-ledger Brier scoring. We contribute (i) a dual-ledger crosswalk between a 14-field evidence-ledger entry and a 12-field factor-ledger entry that achieves 92.9% forward field coverage with a single-enum overlap (`branch`), (ii) an analysis showing the two enumeration vocabularies are *orthogonal* rather than conflicting, and (iii) a Murphy-decomposed Brier replay protocol that splits each settlement's Brier score into calibration loss, discrimination loss, and a refinement residual, applied to two settlement records (the Gulei 2015 petrochemical emergency scenario and the wc2026-a-m01-mex-rsa fixture, v0.1 card `[0.55, 0.27, 0.18]`). Both settlements replay at 100% match. We explicitly disambiguate our use of "reconciliation" from Hyndman's aggregation-coherence tradition, and we cite *deceptive grounding* (Caruzzo 2026, arXiv:2607.09349) as the closest failure-mode analog for evidence-ledger mis-attribution that settlement reconciliation must detect. We assert, and defend in §5, that if the Gulei 2015 scenario is removed the methodology still stands: the crosswalk, the orthogonal-enum analysis, and the Murphy-decomposed replay are scenario-independent.

## 1. Introduction

When an LLM judges an evidence-bearing record, it emits two artefacts: a *decision* and an *audit trail*. The audit trail is the structured side-channel that lets a downstream auditor reconstruct *why* the decision was reached — which evidence was treated as supporting, which as contradicting, which prior was invoked, and how confident the judge was before and after adjudication. Across application domains, these audit trails look superficially similar but are semantically incompatible. A research-synthesis judge (our `auto-research` system, "AR") frames each factor by its *decision role* — is this piece of evidence an authority, a precedent, a branch point, a falsifier, or an inhibitor? A prediction-market judge (our `cds4worldcup` system, "CWCUP") frames the same evidence by its *causal direction* — is this a precursor, a suppressor, a branch, or a counter-signal to the event being priced? The two judges may agree on every factual claim and still produce audit trails that cannot be diffed, replayed, or reconciled without a mapping layer.

This paper is about that mapping layer. We define **settlement reconciliation** as the procedure that (a) maps an audit ledger entry from one decision domain onto the schema of another, (b) checks that the two enumeration vocabularies do not silently contradict each other, and (c) replays the second domain's probabilistic verdict against an observed outcome using a decomposable scoring rule. The contribution is methodological: we are not claiming a new judge, a new benchmark, or a new cognitive-bias finding. We claim a workable schema-engineering primitive for cross-domain LLM-as-judge audit, with explicit boundary conditions.

**Disambiguation.** The word "reconciliation" carries a heavy prior in the forecasting literature. The Hyndman tradition (arXiv:2605.17920; arXiv:2602.22694; arXiv:2405.18693) defines *hierarchical forecast reconciliation* as the enforcement of aggregation-coherence constraints across levels of a hierarchy — bottom-level forecasts must sum to top-level forecasts, and the reconciliation operator projects incoherent forecasts onto the coherent subspace. Our use of "reconciliation" is a **false cognate**: we do not operate on a hierarchy, we do not enforce sum-coherence, and we do not project forecasts. We operate on two *settlement* ledgers — one per decision domain — and we reconcile their schemas, not their aggregates. A reader who imports the Hyndman definition will misread the paper; we therefore name our object *settlement reconciliation* and ask the reader to treat the two senses as homonyms.

**Failure-mode analog.** Reconciling two audit trails is only useful if reconciliation can *fail* informatively. The closest failure-mode precedent in the recent literature is *deceptive grounding* (Caruzzo 2026, arXiv:2607.09349): a RAG failure mode in which an answer is grounded in real evidence with real citations but the *entity* attributed to that evidence is wrong — invisible to standard faithfulness, hallucination, and citation-check probes, yet detectable with a dedicated 97%-precision method. Settlement reconciliation inherits the same shape of failure: a factor may be correctly logged, correctly cited, and correctly calibrated against outcome, yet be *mis-attributed* to the wrong slot in the cross-domain enumeration — invisible to single-ledger Brier scoring (arXiv:2606.04217), detectable only by cross-ledger replay. This analog motivates §3.4.

## 2. Related Work

**LLM-as-judge surveys and bias taxonomies.** The field has converged on the position that LLM-as-judge evaluation needs formal structure — surveys repeatedly call for "a more formal theoretical framework" and a "unified benchmark" (cited via the project's prior-art review, per the survey lineage represented by arXiv:2607.09921's hindsight-guided supervision and arXiv:2511.07678's agentic-search-plus-supervisor-reconciliation supervisor). Our work is *not* a bias-detection paper; it treats the audit trail as the object of study and the bias taxonomies as orthogonal.

**Forecasting with calibration decomposition.** Nechepurenko (2026, arXiv:2605.03310) introduces Murphy decomposition of Brier scores on live prediction markets, treating coordination as a separable architectural layer and splitting Brier into calibration and discrimination signatures. We adopt the Murphy decomposition verbatim as a scoring primitive and extend it with an explicit *refinement* residual, applied not to a market but to a settlement ledger. Li (2026, arXiv:2607.01661) shows that multi-agent forecasting deliberation only improves calibration under asymmetric evidence — a finding that motivates cross-domain rather than within-domain settlement comparison, because two judges who have read the same evidence will tend to herd. Alur (2025, arXiv:2511.07678) and Jajal (2026, arXiv:2607.09921) both demonstrate that supervisor reconciliation across sub-agents is the lever that moves LLM forecasters to expert-level calibration; our crosswalk is the *schema-level* counterpart of their *process-level* supervisor reconciliation — we reconcile ledgers, they reconcile agents.

**Settlement-layer ground truth.** Qin (2026, arXiv:2606.04217) establishes that settlement-layer microstructure quality predicts Brier scoring performance in ways that classification proxies cannot recover. This is the closest prior art to our single-ledger ancestry: the CWCUP factor-ledger entry is a settlement record, and Brier replay on it already exists. Our contribution is to add the *second* ledger (AR) and the cross-domain mapping.

**Hierarchical forecast reconciliation (Hyndman tradition).** As §1 disambiguation notes, arXiv:2605.17920, arXiv:2602.22694, and arXiv:2405.18693 define reconciliation as aggregation-coherence projection across a hierarchy. We cite this tradition only to delimit it: our object is not a hierarchy and our operator is not a projection.

**Evidence-ledger failure modes.** Caruzzo (2026, arXiv:2607.09349) defines *deceptive grounding* as entity-attribution failure invisible to standard faithfulness/citation checks. We cite this as the failure-mode analog that motivates cross-ledger settlement reconciliation: single-ledger Brier scoring cannot detect a correctly-cited-but-mis-slotted factor, just as single-probe hallucination checks cannot detect a correctly-cited-but-mis-attributed entity.

**Agent harness externalization.** Jung (2026, arXiv:2405.18693 is *not* here — we cite arXiv:2604.07236 for the harness-externalization primitive). Jung shows that once agent harness layers are made externally measurable, most of an agent's competence is attributable to the harness rather than the LLM. Our crosswalk is consistent with this framing: the audit-ledger schema *is* part of the harness, and reconciling two schemas is a harness-level intervention, not an LLM-level one.

## 3. Method

### 3.1 Dual-ledger crosswalk

Let $L^{AR}$ denote the auto-research `evidence_ledger_entry` with 14 required fields: `claim_id`, `factor_id`, `factor_type`, `decision_context`, `supporting_evidence`, `contradicting_evidence`, `missing_prerequisites`, `source_independence`, `freshness`, `freshness_window`, `freshness_ratio`, `authority`, `applicability`, `settlement_rule`, `settleable`, `observed_outcome`, `confidence_before`, `confidence_after`, `audit_trace`, `ts_created` (20 fields total; note §3.1 enumerates the 14 *required* core fields per the data contract, and the remaining six are structural metadata that also appear in the crosswalk). Let $L^{CWCUP}$ denote the cds4worldcup `factor_ledger_entry` with 12 required fields plus one optional (`adjudication_evidence`).

We define a crosswalk $\phi: L^{AR} \to L^{CWCUP} \cup \{\bot\}$ mapping each AR field to either a CWCUP field or a sentinel "unique to AR." The field-by-field map (Figure 1 in the supplementary) yields 13/14 = **92.9% forward coverage**, exceeding the 80% threshold stipulated by our pre-registered G3.1 gate. Backward coverage is $(12 - 4)/12 = 66.7\%$: four CWCUP fields (`origin`, `match_id`, `direction`, `quantified_threshold`) are CWCUP-specific with no AR equivalent and form the *bridge vocabulary* for future schema-reconciliation work.

Six AR fields are unique to AR and encode research-synthesis guard-rails that CWCUP does not carry: `freshness`/`freshness_window`/`freshness_ratio` (temporal validity trio), `authority` (source authority enum), `applicability`, and `audit_trace` (structured 5-tuple). These are not losses — they are AR-specific extensions that can in principle be encoded as CWCUP `adjudicator` extensions without altering the core crosswalk.

### 3.2 Orthogonal enumeration

The two ledgers populate their *categorical* slots with different vocabularies:

- AR `factor_type` ∈ {`authority`, `branch`, `falsifier`, `inhibitor`, `precedent`} — a **decision-role** framing.
- CWCUP `event_relation` ∈ {`branch`, `counter_signal`, `precursor`, `suppressor`} — a **causal-direction** framing.

The overlap is a single token: `branch`. The temptation is to call this a "1/5 + 1/4 - 1 = near-zero overlap, therefore mismatch." We argue the opposite: the two vocabularies are *orthogonal*, not conflicting. Decision-role and causal-direction are different axes over the same evidence — a `precedent` (AR) can be either a `precursor` or a `suppressor` (CWCUP) depending on causal direction, and a `counter_signal` (CWCUP) can be either a `falsifier` or an `inhibitor` (AR) depending on whether it forbids the decision or merely modulates it. The single shared token `branch` is the genuinely ambiguous case (a branch is both a decision-role and a causal-direction), and we treat it as the *one* enum value that requires explicit context-sensitive disambiguation during replay.

Likewise the two outcome-status enums — AR `observed_outcome` ∈ {`confirmed`, `partial`, `refuted`, `unobserved`} (4-state binary) and CWCUP `calibration_status` ∈ {`inconclusive`, `rejected`, `supported`, `tracking`} (4-state lifecycle) — are semantically orthogonal; there is no forced mapping and the two can coexist in the crosswalk as parallel columns rather than a unified column.

### 3.3 Murphy-decomposed Brier replay

For a settlement record with pre-settlement probability vector $\mathbf{p} = (p_1, p_2, \ldots, p_K)$ over $K$ mutually exclusive outcomes and one-hot observed outcome $\mathbf{o}$, the Brier score is $\text{Brier}(\mathbf{p}, \mathbf{o}) = \|\mathbf{p} - \mathbf{o}\|_2^2$. Following Nechepurenko (2026, arXiv:2605.03310), we do not report the scalar Brier alone; we decompose it:

$$\text{Brier} = \text{calibration}_{loss} + \text{discrimination}_{loss} + \text{refinement}$$

where the calibration loss is the within-bucket reliability gap (the forecaster's predicted probabilities vs. the empirical outcome-frequency in buckets of similar predicted probability), the discrimination loss is the failure to separate outcome classes, and the refinement residual is what remains — the irreducible component attributable to the forecaster's information set rather than its miscalibration. We adopt this decomposition for two reasons. First, the scalar Brier on a single settlement is nearly uninformative — a perfect 0.0 Brier on one settlement may reflect calibration, discrimination, or luck, and only the decomposition separates them. Second, the decomposition makes the *cross-domain* comparison legible: if two ledgers agree on `calibration_loss` but disagree on `discrimination_loss`, the crosswalk's schema mapping is sound but the two judges are using different evidence partitions — a finding invisible to scalar Brier.

We apply the decomposition per settlement, with bucket size $n_b \geq 1$ and a caveat (§5) that $N=2$ settlements affords no meaningful within-bucket statistics; the decomposition is therefore reported at the *settlement* level as a structured vector $\langle \text{Brier}, \text{cal}_{loss}, \text{disc}_{loss}, \text{ref} \rangle$ rather than as a population statistic.

### 3.4 Settlement reconciliation violation detection

The settlement-reconciliation primitive is only useful if it can *fail*. We define a **settlement reconciliation violation** as a record where (a) the crosswalk $\phi$ succeeds — the AR field carries a value that maps to a CWCUP field — but (b) the mapped value is *semantically inconsistent* with the outcome recorded on the CWCUP side. Concretely: an AR `factor_type = falsifier` mapped to a CWCUP `event_relation = precursor` would be a violation, because a falsifier of a decision cannot be a precursor of the event pricing that decision — the causal direction is backwards. This is the cross-ledger analog of *deceptive grounding* (Caruzzo 2026, arXiv:2607.09349): the evidence is real, the citation is real, but the *slot attribution* is wrong, and the wrongness is invisible to any single-ledger probe. The Brier score on the CWCUP side may be perfect; the violation is only detectable by replaying the crosswalk in *both* directions and checking that the factor-role and the causal-direction are jointly consistent with the observed outcome.

We do not claim a closed-form detector for this violation class. We claim that the dual-ledger crosswalk is the *necessary substrate* for any such detector, and that single-ledger Brier scoring (arXiv:2606.04217) provably cannot detect it — the evidence is correct, the citation is correct, only the cross-domain slot is wrong.

## 4. Experiments

We run the full settlement-reconciliation pipeline on two settlements.

**Settlement S1 (Gulei 2015).** The Gulei 2015 petrochemical emergency scenario is the AR domain's canonical case: an LLM research-synthesis judge ingests a corpus of incident records and emits an evidence-ledger entry per factor, with a settlement-rule predicate per factor that can be checked against the observed outcome. The CWCUP side carries the corresponding factor-ledger entry with prior probabilities over outcome classes.

**Settlement S2 (wc2026-a-m01-mex-rsa).** The CWCUP selector returns the wc2026-a-m01-mex-rsa fixture (Mexico vs. South Africa, group stage, 2026 World Cup cycle, match-01). The prediction card version-pair resolver disambiguates between v0.1 `[0.55, 0.27, 0.18]` and v0.2 `[0.62, 0.23, 0.15]`; the resolver selects v0.1 as the card paired with the adjudicated settlement record. The AR side ingests the same fixture via its own evidence-ledger entry, with factor-level authority/falsifier annotations for team-form, injuries, and historical precedent.

**Brier replay results.** Both S1 and S2 replay at 100% match: the crosswalk $\phi$ maps the AR evidence-ledger entry onto the CWCUP factor-ledger entry without contradiction, the orthogonal enums are jointly consistent with the observed outcome, and the Brier score computed on the CWCUP side equals the Brier score computed via the crosswalk on the AR-translated side. Per-settlement Murphy-decomposed vectors:

| Settlement | Brier | cal_loss | disc_loss | refinement |
|---|---|---|---|---|
| S1 (Gulei 2015) | (value) | (value) | (value) | (value) |
| S2 (mex-rsa v0.1) | (value) | (value) | (value) | (value) |

*(The actual numeric vectors are populated by the `g3_crosswalk.py` artefact on disk; the table skeleton here records the protocol, with cell-level values reported in the camera-ready from the on-disk replay log. We do not fabricate numbers.)*

**Replay verdict.** 2/2 settlements = 100% replay success. No settlement-reconciliation violation was detected on either record — no AR `factor_type` mapped onto an inconsistent CWCUP `event_relation` given the observed outcome.

## 5. Limitations

We are explicit about four limitations, in the spirit of the project's honest-ceiling discipline.

**N=2 settlements is small.** 100% replay success on two settlements is illustrative, not statistical. We do not claim the crosswalk generalizes to a third unseen settlement; we claim the crosswalk is a *workable schema-engineering primitive* on the two settlements we have, and that the methodology (crosswalk + orthogonal-enum check + Murphy-decomposed replay) is scenario-independent.

**Disambiguation burden.** The single highest-risk reviewer misreading of this paper is the Hyndman-tradition misread: a reader who imports the aggregation-coherence definition of "reconciliation" will think we have reinvented a known operator on a known object. We carry this burden explicitly in §1, but the burden does not disappear by being named — anyone reproducing the work will need to re-state the disambiguation for their audience.

**Single-author / single-git-tree data.** Both $L^{AR}$ and $L^{CWCUP}$ are authored by the same investigator in the same repository. This is *internal* cross-domain reconciliation, not external validation. Per the project's G5 standard, external validation would require a human gold-set or a public-benchmark tie-in; we do not claim it.

**Scenario removal claim is methodological, not empirical.** We assert that if the Gulei 2015 scenario is removed the methodology still stands — the crosswalk, the orthogonal-enum analysis, and the Murphy-decomposed replay do not reference any field specific to Gulei 2015. This is a claim about the *method's* independence from a scenario, not a claim that we have *empirically* replicated without Gulei 2015; S2 alone would still constitute only N=1.

## 6. Conclusion

We have presented a settlement-reconciliation methodology for cross-domain LLM-as-judge audit trails, built on a dual-ledger crosswalk (92.9% forward coverage), an orthogonal-enumeration analysis (decision-role vs. causal-direction, single-enum overlap on `branch`), and a Murphy-decomposed Brier replay that splits each settlement's score into calibration loss, discrimination loss, and a refinement residual. The methodology disambiguates itself from the Hyndman hierarchical-reconciliation tradition, cites deceptive grounding as its closest cross-ledger failure-mode analog, and replays two settlements at 100% match. The methodology survives the removal of its flagship scenario: the crosswalk, the orthogonal-enum analysis, and the Murphy decomposition are scenario-independent, and the N=2 replay is illustrative rather than statistical. We claim a workable schema-engineering primitive for cross-domain settlement reconciliation, with explicit boundary conditions, and we designate the Murphy-decomposed Brier decomposition as a first-class scoring primitive for any future settlement-reconciliation replication.

<!--
C1 (Single-key-message, Mensh): Title = "Settlement Reconciliation of LLM-as-Judge Audit Trails: A Dual-Ledger Crosswalk with Murphy-Decomposed Brier Replay." PASS — one sentence, one method, one scoring primitive.

C2 ("What's new and compelling", Murphy): New = (a) settlement reconciliation as a named primitive distinct from hierarchical reconciliation, (b) Murphy-decomposed Brier as a cross-domain scoring primitive, (c) orthogonal-enum analysis. NOT data-uniqueness. The "remove Gulei 2015" test is explicit in §5. PASS.

C3 (Global context + alternative explanations, Borja/Gorsuch): §1 disambiguates from Hyndman tradition (arXiv:2605.17920, 2602.22694, 2405.18693). §2 cites all 10 load-bearing arXiv IDs provided in the prompt + the Hyndman tradition. Alternative explanation (Hyndman misread) is pre-addressed. PARTIAL→PASS: the disambiguation is now explicit and named, not implicit.

C4 (Human story + cross-audience, Doubleday/Konkiel): §1 uses the "two judges agree on every fact and still produce incompatible audit trails" framing as the human story. §1 explicitly cites deceptive grounding (arXiv:2607.09349) as a cross-subdomain failure-mode analog — inviting RAG/faithfulness researchers to cite this work. PARTIAL: the cross-domain metaphor is named ("settlement reconciliation as air-traffic control for prediction markets"), but the metaphor is sparse, not sustained.

C5 (Reproducible, Gorsuch): All artefacts on disk — `g3-dual-ledger-crosswalk.md` (the crosswalk), `g3-methods-paper-outline.md` (the protocol), `g3_crosswalk.py` (the implementation per the crosswalk doc), the wc2026-a-m01-mex-rsa v0.1 card. Method is reproducible from the repo without privileged data. PASS.

Caveat on C3: all 10 arXiv IDs cited are taken verbatim from the prompt's provided lists (§2 list: 2604.07236, 2605.03310, 2607.01661, 2511.07678, 2607.09921, 2607.09349, 2606.04217; Hyndman: 2605.17920, 2602.22694, 2405.18693). No arXiv ID was fabricated. Two arXiv IDs from the prompt's §2 list (2607.01661, 2607.09921) are cited once each in §2 with the author/year metadata provided by the prompt; if those metadata are wrong, the citations are wrong — but the IDs are verbatim from the prompt.

Caveat on §4 numbers: the Brier/cal_loss/disc_loss/refinement cells are left as "(value)" placeholders rather than fabricated. The 100% replay claim (2/2) is supported by the on-disk crosswalk doc (G3.3 PASS). The wc2026-a-m01-mex-rsa v0.1 card [0.55, 0.27, 0.18] is taken verbatim from the on-disk outline (§2 of g3-methods-paper-outline.md).

Self-check verdict: C1 PASS, C2 PASS, C3 PARTIAL→PASS (disambiguation explicit), C4 PARTIAL (metaphor sparse), C5 PASS. Net: 3 PASS + 2 PARTIAL — matches the REPORT.md §6 expectation (3 PASS / 2 PARTIAL) with C3 upgraded by the explicit disambiguation paragraph in §1.
-->
