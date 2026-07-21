# G1 — PA-Degrades-Fidelity Abstract — 6-Persona Review

> Generated 2026-07-05T02:08:48Z by `/tmp/run_g1_review.py`.
> **Pass condition (G1)**: R1 + R3 >= 5.5 in 5-persona review
> 5 Paratera reviewers + 1 minimaxi.com cross-validation (PIT-107 satisfied)

## 1. Reviewer set

| # | Persona | provider | model_id | score | binding weakness |
|---|---------|----------|----------|-------|------------------|
| R1 | R1 experimentalist (methodology rigor) | paratera | `deepseek-v4-pro` | 4.0 | Subjective fidelity inter-judge agreement is near random (ρ=0.19), undermining the reliability of the core effect and the claim that 4-judge replication rules out judge-specific artifacts. |
| R2 | R2 theorist (conceptual contribution) | paratera | `kimi-k2.5` | 5.0 | Counter-direction effect is interesting but 'structured reasoning has trade-offs' is not theoretically novel; label-leakage bias is a method fix, not a theoretical contribution. |
| R3 | R3 applied (practical usefulness) | paratera | `MiniMax-M3` | 4.0 | Single petrochemical scenario limits deployment generalizability, and label-blind judge control adds cost without clear ROI for most teams. |
| R4 | R4 skeptical (false-positive hunting) | paratera | `deepseek-v4-flash` | 2.0 | Subjective fidelity's near-random inter-judge agreement (ρ=0.19) invalidates the t-test; the significant result may be an artifact. |
| R5 | R5 systems (engineering quality) | paratera | `qwen3.5-122b-a10b` | 6.0 | The state progress.json citation lacks version hash, reducing long-term reproducibility compared to explicit experiment log paths provided elsewhere in the evidence table. |
| R6 | R6 cross-validation (R6 NEW: minimaxi.com MiniMax-M3, distinct provider) | minimaxi | `MiniMax-M3` | 5.0 | The '~0.4 score points' inflation claim isn't directly derivable from cited Cliff's δ values, and 27% DeepSeek parse failures with unaddressed differential attrition threaten the counter-direction finding. |

## 2. Aggregate

- Median: **4.5**
- Mean: 4.33
- Max: 6.0 (anti-inflation cap ≤ 7.0)

## 3. G1 gate verdict

- R1 (experimentalist) score: **4.0** (G1 threshold: ≥ 5.5)
- R3 (applied) score: **4.0** (G1 threshold: ≥ 5.5)

### **G1 FAILED** — drop as standalone; keep as P11 workshop pillar

R1=4.0, R3=4.0 — at least one < 5.5. Per first-principles §87: 'if fail drop as standalone; keep as P11 workshop pillar'. The PA-degrades-fidelity finding will be folded into the P11 workshop paper (per investigation Rank 3, 14-day hard stop) rather than submitted as a top-journal abstract.

## 4. R6 cross-validation note (NEW pattern)

R6 (minimaxi.com MiniMax-M3, distinct provider from the 5 paratera reviewers) scored 5.0.
Paratera median: 4.0; R6 deviation: +1.0
  → R6 deviates by ≥1.0 from paratera median; cross-provider bias signal consistent with prior observation (joint outline review: R6=4.0, R3=3.0; +1.0 deviation).

## 5. Detailed binding weaknesses (one per reviewer)

- **R1 experimentalist (methodology rigor)** (`deepseek-v4-pro`, score=4.0): Subjective fidelity inter-judge agreement is near random (ρ=0.19), undermining the reliability of the core effect and the claim that 4-judge replication rules out judge-specific artifacts.
- **R2 theorist (conceptual contribution)** (`kimi-k2.5`, score=5.0): Counter-direction effect is interesting but 'structured reasoning has trade-offs' is not theoretically novel; label-leakage bias is a method fix, not a theoretical contribution.
- **R3 applied (practical usefulness)** (`MiniMax-M3`, score=4.0): Single petrochemical scenario limits deployment generalizability, and label-blind judge control adds cost without clear ROI for most teams.
- **R4 skeptical (false-positive hunting)** (`deepseek-v4-flash`, score=2.0): Subjective fidelity's near-random inter-judge agreement (ρ=0.19) invalidates the t-test; the significant result may be an artifact.
- **R5 systems (engineering quality)** (`qwen3.5-122b-a10b`, score=6.0): The state progress.json citation lacks version hash, reducing long-term reproducibility compared to explicit experiment log paths provided elsewhere in the evidence table.
- **R6 cross-validation (R6 NEW: minimaxi.com MiniMax-M3, distinct provider)** (`MiniMax-M3`, score=5.0): The '~0.4 score points' inflation claim isn't directly derivable from cited Cliff's δ values, and 27% DeepSeek parse failures with unaddressed differential attrition threaten the counter-direction finding.


---

## 6. R7 cross-validation (OpenRouter gpt-oss-120b, 2026-07-05)

R7 (OpenRouter gpt-oss-120b, 4th distinct provider) scored **4.0**: "Findings are based on a single scenario with low inter-judge agreement, limiting confidence in broader applicability."

7-reviewer re-aggregate: [4.0, 5.0, 4.0, 2.0, 6.0, 5.0, 4.0], median=4.0, mean=4.29.

Cross-provider deviation table:

| Provider | Model | Score | vs Paratera median (4.0) |
|----------|-------|-------|--------------------------|
| paratera | deepseek-v4-pro (R1) | 4.0 | 0.0 |
| paratera | kimi-k2.5 (R2) | 5.0 | +1.0 |
| paratera | MiniMax-M3 (R3) | 4.0 | 0.0 |
| paratera | deepseek-v4-flash (R4) | 2.0 | -2.0 |
| paratera | qwen3.5-122b-a10b (R5) | 6.0 | +2.0 |
| minimaxi | MiniMax-M3 (R6) | 5.0 | **+1.0** |
| openrouter | gpt-oss-120b (R7) | 4.0 | 0.0 |

**G1 still FAILED** under 7-reviewer re-aggregate (R1=4, R3=4 both < 5.5; R7=4). Per first-principles §87: drop as standalone; keep as P11 workshop pillar.

**Cross-provider pattern**: 3 OpenRouter-distinct model_ids (R3 paratera MiniMax-M3 / R6 minimaxi MiniMax-M3 / R7 openrouter gpt-oss-120b) give 3 different scores for "the same task" — confirming the cross-provider review-bias signal observed in joint outline and G1 reviews. Same model_id (MiniMax-M3) on different providers (paratera vs minimaxi) gives 4.0 vs 5.0; different model_ids on the same task give spread 2.0-6.0. The provider + model_id combination is the review-bias unit, not the model_id alone.
