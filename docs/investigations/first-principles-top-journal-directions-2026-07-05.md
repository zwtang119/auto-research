# First-Principles Scan: Latent Top-Journal Directions

Date: 2026-07-05

## Summary

The current project is still **not main-track / top-journal ready as-is**, but the first-principles scan found several non-obvious directions that prior operational assessments underweighted. The strongest candidates are not "the agent performs better" papers. They are **counter-direction, measurement, schema-reconciliation, and auditability papers**.

Best answer: there is no immediate NeurIPS/ICLR/ACL-main submission hidden in the repo, but there are **3 credible high-level directions** worth considering if the user is willing to invest more: (1) PA-degrades-fidelity / role-conflict mechanism, (2) calibration paradox in LLM judges, and (3) dual-ledger schema reconciliation with cds4worldcup settlement evidence. These can plausibly reach Findings / strong workshop now, and might become main-track only after cross-domain replication or external validation.

## Ranked Candidate Directions

| Rank | Direction | Core claim | Current ceiling | Main-track unlock | Cost / risk |
|---:|---|---|---|---|---|
| 1 | **PA-degrades-fidelity / role-conflict mechanism** | Structured pure-analysis prompting can reduce role fidelity under role conflict, contrary to "more explicit reasoning helps" assumptions. | 6.5-7.0 workshop / Findings-borderline | Cross-domain replication, ideally using cds4worldcup or another non-emergency decision domain | 0 new API for write-up; 2-3 weeks. Risk: P11 review-trust debt from 26-round plateau. |
| 2 | **Calibration paradox** | Leaked labels made the LLM judge stricter, not more lenient: blind > leaked, opposite of the usual leakage-bias story. | 6.5-7.0 if replicated | N=30 paired, second judge family, second scenario | 5-8 API hours; high novelty but small current n=10. |
| 3 | **Dual-ledger / settlement schema bridge** | auto-research evidence ledger and cds4worldcup factor ledger evolved independently; reconciling them creates a multi-domain settlement-aware evidence contract. | 6.5-7.0 Findings / D&B style | MD2-scale cds4worldcup corpus, >=80% schema field coverage, external baseline | 3-8 API hours + 2-3 weeks. Lowest-cost latent unlock. |
| 4 | **Negative heterogeneity as first-class finding** | Evidence-ledger effects are factor-type conditional: authority/falsifier help, branch/precedent do not. | 6.5-7.0 workshop; 7.0-7.5 as methodology | N=64/cell or cross-domain factor-type replication | ~30 API hours if powered directly; cheaper if combined with schema bridge. |
| 5 | **Reviewer-noise ceiling / LLM-review psychometrics** | Across repeated reviews, reviewer noise can exceed paper-improvement signal. | 6.5-7.0 ACL/EMNLP evaluation track | Human-reviewer comparison and preregistered review protocol | 5-10 API hours + human reviewer effort. |
| 6 | **Audit-chain integrity / hash-fabrication failure** | LLM-agent evidence systems can fabricate audit hashes; evidence validity must be computed, not asserted. | 6.0-7.0 security / AI safety workshop | 2-3 more case studies beyond P7 PIT-NEW-9 | Low API; venue fit is narrow. |
| 7 | **Cross-layer integration failure** | Four green component test suites can compose into a broken evaluation system without end-to-end contract tests. | 6.0-6.5 SE/AI engineering venue | Reproducible integration failure and cross-layer test suite | 3-5 API hours; more SE than AI main-track. |

## Non-Obvious Reframings

### 1. Stop asking "did the agent improve?"

The strongest latent claims are **diagnostic**, not performance-improvement claims:

- P12 found a counter-direction judge effect.
- P11/Mimo found pure analysis can degrade fidelity.
- P1+P2 found factor-type heterogeneity instead of uniform improvement.
- P7 found an audit-chain integrity defect.
- Repeated reviews revealed measurement noise and plateau behavior.

This suggests a paper family around **limits of evidence, judgment, and intervention in LLM-agent evaluation**, not "better agent system".

### 2. cds4worldcup is the cheapest top-ceiling unlock

The prior operational plan underweighted cds4worldcup. It has an independent factor-ledger schema, settlement-record schema, 24-game settled outcomes, and closed-loop Brier evidence. Bridging it to auto-research could:

- unblock P8's "no predicted probabilities" problem;
- give P1+P2 a second domain;
- test whether factor-type heterogeneity survives outside emergency scenarios;
- produce a schema-reconciliation paper without large new model runs.

### 3. The joint-methods failure is itself evidence

The joint paper failed because the components were individually plausible but not integrated. That can be reframed as a software/evaluation-methods finding:

> Component-level contracts are insufficient; LLM-agent evaluation needs end-to-end contract tests across evidence, judge, settlement, and audit layers.

This is not likely NeurIPS main-track, but it could be a good SE/AI-engineering workshop paper.

### 4. "Top journal" may require switching venue class

If "top journal" strictly means NeurIPS/ICLR/ACL main-track, no direction is currently ready. If it includes ACL/EMNLP Findings, NeurIPS Datasets & Benchmarks, security/SE workshops, or AI-for-science methodology venues, then several directions become credible.

## External Novelty Check

External novelty scout found:

- LLM-as-judge bias is crowded, but **blind > leaked** was not surfaced in the checked literature.
- CoT / structured reasoning literature usually reports positive effects; **PA-degrades-fidelity** is counter-direction.
- Heterogeneous treatment effects are mature statistically, but underused in LLM-evaluation evidence ledgers.
- AI research automation is crowded, but **path-selection oscillation with human-in-the-loop AutoResearch control** is narrower and less covered.
- LLM-agent audit/provenance is under-published; P7's PIT-NEW-9 style hash-fabrication defect sits in an open lane.

External anchors checked include:

- MT-Bench / Chatbot Arena: <https://arxiv.org/abs/2306.05685>
- LLM-as-judge position bias: <https://arxiv.org/abs/2406.07791>
- LLM-as-judge scoring bias: <https://arxiv.org/abs/2506.22316>
- KIEval: <https://arxiv.org/abs/2402.15043>
- OctoTools: <https://arxiv.org/abs/2502.11271>
- RELAY: <https://arxiv.org/abs/2502.08482>
- AI Scientist: <https://arxiv.org/abs/2408.06292>
- AI Scientist v2 repository: <https://github.com/david-hoa2023/ai-scientist-v2>
- AI4Research: <https://ai-4-research.github.io/>
- Heterogeneous treatment effects: <https://link.springer.com/article/10.1007/s10742-016-0156-2>

Note: the external scout reported that some arXiv pages were only reachable through search snippets or secondary summaries in this environment. Before citing in a paper, re-verify all primary PDFs directly.

## Recommended Experiments / Gates

| Gate | Action | Pass condition | If fail |
|---|---|---|---|
| G1 | Write 1-page PA-degrades-fidelity abstract | R1 + R3 >= 5.5 in 5-persona review | Drop as standalone; keep as P11 workshop pillar |
| G2 | Replicate calibration paradox to N=30 paired + second judge | CI remains below 0 for leaked-blind delta | Treat as P12 anomaly only |
| G3 | Build dual-ledger crosswalk between auto-research and cds4worldcup | >=80% field coverage and no fatal enum mismatch | Publish schema note only |
| G4 | Run P8 Brier on cds4worldcup settlement records | Reproduces reported Brier values and baseline differences | Fix schema/calculation before paper |
| G5 | Human or external review for reviewer-noise paper | Human-vs-LLM comparison confirms measurement gap | Keep as internal AutoResearch methodology |

## Final Judgment

There are **other plausible high-level directions**, but none is a no-work hidden top-journal path. The best first-principles insight is that this portfolio's real novelty may be in **how LLM-agent evidence systems fail**:

1. judges react counter-directionally;
2. structured reasoning can harm role fidelity;
3. ledger effects are heterogeneous by factor type;
4. audit chains can be fabricated unless cryptographically checked;
5. reviewer noise can dominate paper iteration.

The highest expected-value sequence is:

1. **PA-degrades-fidelity abstract** (0 API, fast truth test);
2. **dual-ledger bridge with cds4worldcup** (cheap structural unlock);
3. **calibration paradox replication** (small API, high novelty);
4. only then consider a powered P1+P2 or main-track attempt.

Absent those gates, the honest near-term target remains workshop / Findings, not main-track.
