# Codability Rubric v0.1

## 目标

判断 Kimi 300 Agent 的一句话 reason 是否能转化为可审计、可结算、可进入 Factor Ledger 的知识对象。

## 三层判断

1. `any_codable_atom`：这句话里是否至少有一个事实碎片原则上可核验。
2. `main_claim_codable`：支撑预测的主要理由是否可审计。
3. `ledger_route`：这条 reason 最适合进入 Factor Ledger、作为候选、保留为 Marginalia，还是拒绝。

## 不要做的事

- 不要查资料。
- 不要判断 reason 是否真实。
- 不要根据球队、派别、置信度推断质量。
- 不要把“有一个事实碎片”直接等同于“主理由可审计”。
- 不要把叙事强行转成 Factor Ledger。

## 关键字段

### `atomic_claim_count`

- `0`：没有可拆出的事实或判断主张。
- `1`：一个主要主张。
- `2`：两个主要主张。
- `3+`：三个或更多主张。

### `claim_family_primary`

- `roster`：球员、阵容、年龄、身价等。
- `market`：赔率、市场概率、投注热度等。
- `ranking`：FIFA/Elo/ESPN/模型排名等。
- `historical_result`：历史战绩、近况、预选赛结果等。
- `injury_schedule`：伤病、赛程、体能、旅行等。
- `tactical`：战术、教练、阵型、打法等。
- `psychological`：心理、抗压、团队气氛等。
- `model_internal`：模型输出、内部概率、不可复现算法声称等。
- `mystical`：玄学、命理、周期论等。
- `hearsay`：传闻、朋友消息、未具名内部消息等。
- `vague_narrative`：空泛叙事、无可操作标准的判断。
- `other`：以上都不合适。

### `main_claim_codable`

- `strict`：主理由有明确数值阈值、时间窗、独立来源，几乎可直接结算。
- `moderate`：主理由有明确可观测代理和时间窗，但需要标注者设计 settlement rule。
- `loose`：有事实锚点，但主理由主要依赖定性解释。
- `no`：主理由不可审计。

### `ledger_route`

- `ledger_now`：可直接写成 Factor Ledger 条目。
- `ledger_candidate`：有潜力，但需要清洗、拆分或补充来源。
- `marginalia_only`：有解释/叙事价值，但不应进入 Factor Ledger。
- `reject`：无信息量、不可复核且解释价值低。

## 示例

| reason | 建议判断 |
|---|---|
| 法国14.8亿欧身价+I组最轻松出线路径，模型输出21.4%最高。 | 有 codable atom；主理由部分可审计；模型输出是 Red Source；多半为 `ledger_candidate`。 |
| 南美球队热带基因觉醒，阿根廷会靠冠军气场卫冕。 | 主理由不可审计；`mystical` 或 `vague_narrative`；`marginalia_only` 或 `reject`。 |
| C罗41岁第六次出征，葡萄牙队内气氛空前团结。 | 年龄/参赛次数可核验，但主理由“气氛团结”较难审计；通常 `loose` + `marginalia_only`。 |
