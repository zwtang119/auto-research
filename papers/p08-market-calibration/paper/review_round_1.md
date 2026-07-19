# P8 M1.5 Review Round 1 — Five-Persona Review

> Generated 2026-07-04T09:31:42Z by `experiments/run_review_round_1.py`.
> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.
> Reviewing calc_brier.py (P8 M1.5) — methodology/scaffolding component, not a paper.

## 1. Reviewer set

| # | Persona | model_id | score | binding weakness |
|---|---------|----------|-------|------------------|
| R1 | R1 experimentalist (methodology rigor) | `deepseek-v4-pro` | 5.0 | The API forces callers to manually flatten multiclass probabilities, and aggregate_scores() lacks explicit handling of missing outcome data, risking silent errors in portfolio summaries. |
| R2 | R2 theorist (probabilistic-foundation correctness) | `kimi-k2.5` | 6.0 | Factor-update 0.7/0.3 thresholds lack probabilistic justification; should derive from calibration curve or expected value of information, not arbitrary cut. |
| R3 | R3 applied (P1+P2 pipeline integration) | `MiniMax-M3` | 5.0 | calc_brier.py consumes ledger fields but factor_update heuristic (p>=0.7 + o=1) is too rigid and biases audit toward overconfident correct predictions only. |
| R4 | R4 skeptical (data shape mismatch) | `deepseek-v4-flash` | 4.0 | Assumes continuous probabilities but existing data uses discrete judge scores, reducing practical utility. |
| R5 | R5 systems (engineering quality) | `qwen3.5-122b-a10b` | 6.0 | Hard confidence thresholds at 0.7 and 0.3 ignore boundary uncertainty, reducing robustness for continuous calibration tasks. |

## 2. Aggregate

- Median score across R1..R5: **5.0**
- Mean score: 5.20
- Max score: 6.0

## 3. Verdict (P8 is methodology/scaffolding, threshold = 5.0 not 6.5)

- **Verdict**: `research_grade_acceptable` (5.0 <= median 5.0 < 6.0)
- Action: keep as paper-scoped tool; document known limitations.

## 4. Anti-inflation cap compliance (roadmap §11)

- Max reviewer score = 6.0 ≤ 7.0 ✓

## 5. `unresolved_weakness` (single most-cited)

> Assumes continuous probabilities but existing data uses discrete judge scores, reducing practical utility.  *(from deepseek-v4-flash, score=4.0)*

## 6. Calibration context (M1 data-shape finding)

Per `state/findings.jsonl` 2026-07-04: M1 attempt to parse cds4polymarket
ab-test/analysis/ab_test_17rounds_data.xlsx found 9 sheets containing
judge scores (discrete 1-5) and winner labels — NOT continuous
prediction_p in [0,1] needed by calc_brier.py. Brier computable;
upstream data shape is wrong. P8 M1 stale_count += 1.

## 7. Required follow-up actions

1. Record verdict in `state/findings.jsonl` (level=decision, source=p8_m15_review_round_1)
2. Update `state/progress.json` with M1.5 review verdict
3. Promote calc_brier.py to framework/ if verdict >= production_grade
