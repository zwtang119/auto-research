# 问卷字段备选方案

如果改用问卷星、飞书或 Google Forms，每条 reason 应重复以下问题。推荐仍使用 Excel，因为问卷平台回收后通常需要额外清洗。

## 固定展示

- reason_id
- reason_text

## 选择题

1. atomic_claim_count：0 / 1 / 2 / 3+
2. claim_family_primary：roster / market / ranking / historical_result / injury_schedule / tactical / psychological / model_internal / mystical / hearsay / vague_narrative / other
3. claim_family_secondary：none / roster / market / ranking / historical_result / injury_schedule / tactical / psychological / model_internal / mystical / hearsay / vague_narrative / other
4. observable_proxy：direct / proxy_needed / none / model_internal
5. time_window：pre_tournament / group_stage / match_level / tournament_level / undefined
6. settlement_rule_type：numeric_threshold / event_occurrence / ordinal_judgment / none
7. source_likelihood：green_possible / yellow_possible / red_only / unknown / impossible
8. any_codable_atom：yes / no
9. main_claim_codable：strict / moderate / loose / no
10. ledger_route：ledger_now / ledger_candidate / marginalia_only / reject
11. annotation_confidence：high / medium / low

## 填空题

- dominant_claim_text
- notes
