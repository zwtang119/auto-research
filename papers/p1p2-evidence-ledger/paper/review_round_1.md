# P1+P2 Review Round 1 — Five-Persona Review

> Generated 2026-07-04T07:25:56Z by `experiments/run_review_round_1.py`.
> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.
> Reviewing the **post-M4 structural-pivot** claim: factor-type-conditional effect.

## 1. Reviewer set

| # | Persona | model_id | score | binding weakness |
|---|---------|----------|-------|------------------|
| R1 | R1 experimentalist (methodology rigor) | `deepseek-v4-pro` | 5.0 | M4 baseline design lacks a sample size justification for per-factor-type comparisons, risking underpowered detection of the claimed neutral-to-negative effects for branch and precedent. |
| R2 | R2 theorist (conceptual contribution) | `kimi-k2.5` | 5.0 | Factor-type taxonomy lacks theoretical grounding; 14-field schema conflates epistemic and procedural invariants without justifying their joint necessity. |
| R3 | R3 applied (practical usefulness) | `MiniMax-M3` | 3.0 | Gulei 2015 is single-incident overfit; 7% un_settleable rate looks cherry-picked and factor-type-conditional framing barely informs practitioners. |
| R4 | R4 skeptical (false-positive hunting) | `deepseek-v4-flash` | 4.0 | Authority factor positive effect based on n=5 is unstable; per-factor type sample sizes too small to support conditional claim. |
| R5 | R5 systems (engineering quality) | `qwen3.5-122b-a10b` | 3.0 | Validators missed the build_pilot_10 PIT-201 row-5 violation, demonstrating insufficient schema enforcement depth and lacking robust unit tests for critical edge cases in pipeline scripts. |

## 2. Aggregate

- Median score across R1..R5: **4.0**
- Mean score: 4.00
- Max score: 5.0

## 3. Verdict

- **Verdict**: `fold_into_p12` (median 4.0 < 6.5)
- Action: stop P1+P2 standalone paper. Carry 14-field evidence_ledger_entry + 5-protocol P12 design into a methods paper.

## 4. Anti-inflation cap compliance (roadmap §11)

- Max reviewer score = 5.0 ≤ 7.0 ✓

## 5. `unresolved_weakness` (single most-cited)

> Gulei 2015 is single-incident overfit; 7% un_settleable rate looks cherry-picked and factor-type-conditional framing barely informs practitioners.  *(from MiniMax-M3, score=3.0)*

## 6. Calibration context (M3 power analysis)

Per `experiments/pilot_power.md`:
- pilot_30 n=30 yields power=0.48 at d=0.5 (underpowered for uniform-positive claim)
- per-factor_type delta: authority +0.39 / falsifier +0.22 / branch -0.14 / precedent -0.13
- M4 structural pivot: claim re-shaped to factor-type-conditional, NOT tactical reframe
- required scale for d=0.5 detection: N=64/cell (~30 API hours)

## 7. Required follow-up actions

1. Record verdict in `state/findings.jsonl` (level=decision, source=p1p2_m9_round_1)
2. Update `state/progress.json`: status → `m9_close_no_mainline_paper`
3. Carry 14-field evidence_ledger_entry + 5-protocol P12 design into a methods paper
