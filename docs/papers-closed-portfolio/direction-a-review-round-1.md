# Direction A — 5-Persona Review Round 1 (2026-07-05)

_Source: docs/papers-closed-portfolio/direction-a-1-page-proposal.md (67 lines, CoBBLEr 3-axis differentiation in §3)_

_Reviewers: 5 paratera (PIT-107) + 1 minimaxi cross-validation_


## Results

| Persona | Model | Score | Weakness |
|---------|-------|-------|----------|
| R1 experimentalist (methodology rigor) | deepseek-v4-pro | 4.0 | No power analysis for N=30, and confounds such as parse failures, judge severity |
| R2 theorist (conceptual contribution) | kimi-k2.5 | 6.0 | CoBBLEr's 6-bias taxonomy lacks theoretical grounding, but the 3-axis anchoring  |
| R3 applied (practical usefulness) | MiniMax-M3 | 4.0 | Practitioner usefulness is limited: 4 anchor types rarely co-exist in real pipel |
| R4 skeptical (false-positive hunting) | deepseek-v4-flash | 5.0 | Leaked-ground-truth manipulation confounds anchor content with prompt formatting |
| R5 systems (engineering quality) | kimi-k2.6 | N/A | Missing env var: TOKEN_PLAN_API_KEY |
| R6 cross (minimaxi provider replication) | MiniMax-M3 | 4.0 | Mechanism experiment conflates 'insufficient adjustment' with confidence-cue eff |

## Aggregate

- R1-R5 median: **4.5**
- R6 cross-validation (minimaxi): 4.0 (deviation from paratera median: -0.5)

## Verdict

**FOLD (median < 5.5)**


Direction A **folds** into a methods paper. Pivot target: G3 dual-ledger bridge (`docs/papers-closed-portfolio/direction-a-mechanism-experiment-spec.md` §7).
