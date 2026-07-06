# Orchestrated Assessment: Current AutoResearch Progress

Date: 2026-07-05

## Recommendation

Current state is **not top-journal / main-track ready**. The portfolio has publishable material, but the honest near-term target is workshop/findings, not NeurIPS/ICLR/ACL/EMNLP main track. The strongest immediate path is a **14-day P11 workshop paper** using existing evidence, with **P7 scaffolding/audit-chain paper as optional insurance**. The joint P12 + P1+P2 + P8 + P7 methods paper should not be submitted as-is: its actual 6-persona outline review median is 4.0, below the fallback threshold.

## Agent Findings

### Agent 1: P11 / P12

- **P11 standalone ceiling:** 6.0-6.5, workshop only.
- **P12 standalone:** no viable path; median=3.0, deliberate `fold_into_p1_p2`.
- **Mimo + v5 integration:** conditional only if the 14-day plan can extend to Day 21. Conservative expected gain is +0.3 to +0.5 median, not enough to make a top-journal claim.
- **Compute:** 0 new API hours. Use existing P11 927 runs and 1,824 judge calls.
- **Decision:** GO for 14-day P11 workshop. Day-11 gate: median < 5.8 means switch to a 2-page extended abstract; median >= 6.3 opens optional Day 15-21 Mimo integration.

### Agent 2: P1+P2 / P8 / P7 / Joint Methods

- **P1+P2 standalone:** closed; current ceiling 3.5-4.5. M5 main run would cost ~30 API hours but does not fix scenario/external-validation blockers.
- **P8 standalone:** 5.5-6.0 until data emits `predicted_p`; existing AB data is 1-5 judge scores, not probabilities.
- **P7 standalone:** 5.5-6.0 now, possibly 6.0-6.5 after elevating the PIT-NEW-9 audit-chain fix as the primary contribution.
- **Joint methods paper:** abandon as a publication path for now. The prior estimated 6.5-7.0 ceiling does not survive the actual 6-persona review median=4.0.
- **Decision:** turn joint methods outline into internal framework documentation. If writing a second paper, use P7 scaffolding/audit integrity as insurance.

### Agent 3: Deli AutoResearch Control Loop

- **Portfolio health:** false-healthy. `stale_count=0` masks path-selection oscillation: P12 fold -> P1+P2 fold -> joint methods fallback -> P11 fallback.
- **M5 main run:** not authorized. It is a single-direction dig and risks PIT-003 / PIT-008 recurrence.
- **cds-keyperson import refactor:** not authorized for this 14-day window; not on the critical path for P11 or P7 scaffolding.
- **Operating plan:** lock fallback, rebuild iteration logs, run P11 workshop path and optional P7 scaffolding, review by Day 11, submit or stop by Day 14.

## Top-Journal Route

**Current answer: no.** There is no credible top-journal or main-track submission now.

Main-track becomes rational only if at least two of the following structural unlocks close:

1. **Scenario diversity:** at least 3 independent decision/emergency scenarios beyond the current Gulei / commercial-space base.
2. **External validation:** human inter-rater, gold set, or public benchmark tie-in such as ForecastBench, GAIA, AgentBench, or a domain oracle.
3. **Frontier baseline:** GPT-5 / Claude Opus / Gemini-tier model arm on a meaningful comparison cell.

If all three remain closed, more tokens mostly improve packaging, not publication ceiling.

## Compute Ask

| Item | API hours | Decision |
|---|---:|---|
| P11 workshop paper | 0 | Authorize |
| P7 scaffolding paper + review | ~3 | Optional insurance |
| P1+P2 M5 main run | ~30 | Do not authorize now |
| P12 standalone expansion | 0 | Do not reopen |
| P8 probability re-run | 5-10 | Defer unless P8 becomes a chosen workshop track |
| cds-keyperson import refactor | 0 | Defer |
| Frontier baselines | 0 | Defer until scenario + external validation exist |

## Next Gates

| Day | Gate | Decision rule |
|---|---|---|
| 1-2 | Lock fallback and freeze other loops | Write checkpoint / progress status before more iteration |
| 3-5 | P11 4-pillar rewrite | Label leakage + H1c + F1 emergence + H3 Spearman visible in abstract/results |
| 6-8 | Optional P7 scaffolding draft | Drop if audit-chain story needs live engine demo |
| 9-11 | 5-persona reviews | P11 median < 5.8 -> extended abstract; P7 median < 5.5 -> internal docs only |
| 12 | Compile / citation check | No fabricated citations; no unresolved build issue |
| 13-14 | Venue selection + submission | Workshop/finding only; no main-track submission |

## Fallback

If P11 and P7 both miss their Day-11 thresholds, stop the portfolio loop instead of spawning another path. Write a framework-level blocked state citing path-selection oscillation, then restart only after at least two structural unlocks are externally committed.

## Bottom Line

The current best research output is a controlled workshop/finding submission, not a top-journal paper. The most valuable action is to **ship one honest paper from existing evidence within 14 days**, then decide whether to invest human work into scenario diversity, external validation, and frontier baselines. Without those structural inputs, additional tokens are likely to recreate the P11-style review plateau.
