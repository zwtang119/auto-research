# P7 M1 Review Round 1 — Five-Persona Review

> Generated 2026-07-04T09:35:39Z by `experiments/run_review_round_1.py`.
> 5 distinct model_ids (PIT-107); all via PARATERA_API_KEY.
> Reviewing adapter_signal_to_ledger.py (P7 M1) — layer-roles bridge, not a paper.

## 1. Reviewer set

| # | Persona | model_id | score | binding weakness |
|---|---------|----------|-------|------------------|
| R1 | R1 experimentalist (methodology rigor) | `deepseek-v4-pro` | 6.0 | Independence class resolution for missing_data and source_failure is not fully justified and might be arbitrary. |
| R2 | R2 theorist (signal-theory correctness) | `kimi-k2.5` | 5.0 | Missing_data as contradicting conflates epistemic gaps with active negative evidence; source_failure duplicates missing_data without clear semantic distinction in rejection logic. |
| R3 | R3 applied (P1+P2 consumer-side integration) | `MiniMax-M3` | 4.0 | snippet_sha256_prefix is fabricated (P12P-001____), not actually hashed; snippet_summary omits numeric_forecast and signal_type, hurting downstream audit. |
| R4 | R4 skeptical (PIT-302 false-rejection rate) | `deepseek-v4-flash` | 5.0 | Rejecting all supporting signals without numeric_forecast over-rejects qualitative evidence useful for non-Brier consumers, violating layered audit trail intent. |
| R5 | R5 systems (engineering quality) | `qwen3.5-122b-a10b` | 6.0 | The source_id double-prefix bug indicates weak input validation rather than a typo, requiring stricter schema enforcement on signal_id formatting before ledger adaptation. |

## 2. Aggregate

- Median score across R1..R5: **5.0**
- Mean score: 5.20
- Max score: 6.0

## 3. Verdict (P7 is bridge tooling, threshold = 5.0 not 6.5)

- **Verdict**: `research_grade_acceptable` (5.0 <= median 5.0 < 6.0)
- Action: keep as paper-scoped bridge; document PIT-302 strictness; defer live integration until cds-keyperson import refactor.

## 4. Anti-inflation cap compliance (roadmap §11)

- Max reviewer score = 6.0 ≤ 7.0 ✓

## 5. `unresolved_weakness` (single most-cited)

> snippet_sha256_prefix is fabricated (P12P-001____), not actually hashed; snippet_summary omits numeric_forecast and signal_type, hurting downstream audit.  *(from MiniMax-M3, score=4.0)*

## 6. Calibration context (M2 import-path finding)

Per `state/findings.jsonl` 2026-07-04: M2 attempt to import live
SignalFusionEngine from cds-keyperson failed with ModuleNotFoundError
on `from src.backend...` internal imports. Adapter works on synthetic
5-signal fixture (3 supporting + 2 contradicting) but live engine
integration requires cds-keyperson cwd or relative-import refactor.
P7 M2 stale_count += 1.

## 7. Required follow-up actions

1. Record verdict in `state/findings.jsonl` (level=decision, source=p7_m1_review_round_1)
2. Update `state/progress.json` with M1 review verdict
3. Promote adapter to framework/ if verdict >= production_grade
