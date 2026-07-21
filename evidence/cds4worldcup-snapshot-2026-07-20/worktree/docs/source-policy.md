# CDS4WorldCup2026 Source Policy

> **状态**: draft-for-execution
> **日期**: 2026-06-11

## 目的

本文件定义 CDS4WorldCup2026 的来源分级和使用边界，防止项目从“路径空间与可校准知识实验”滑向“AI 预测冠军”或投注建议。

## 来源等级

### Green Source

可作为事实输入进入 Team Path Card、Factor Ledger 或路径引擎。

条件：

- 来源可公开访问或可本地归档。
- 有明确发布时间或数据时间窗。
- 事实字段可被复核。
- 不依赖 LLM 的二次概括作为唯一证据。

例子：

- FIFA / 官方赛程与赛果。
- 比赛技术统计的官方或可信数据源。
- 官方伤病、红黄牌、换人、首发名单。
- 可复核的 Elo / FIFA ranking / 历史比赛结果。

### Yellow Source

可作为候选事实、候选因子或背景线索，但进入 Green Source 前需要核验。

条件：

- 信息有价值，但来源粒度、时间窗或可复核性不足。
- 可能是媒体报道、二级整理、手工表格或非官方数据。

例子：

- 媒体赛前分析。
- 汇总型数据表。
- 新闻报道中的伤病状态。
- Kimi `wc2026_data.md` 中尚未核验的事实条目。

### Red Source

不得作为事实输入进入 CDS 路径引擎或 Factor Ledger 的事实字段，只能作为 baseline、叙事材料、candidate seed 或 parser fixture。

例子：

- Kimi 白皮书中的最终概率、排名或方法叙事。
- Kimi 300 Agent 的 `reason`。
- 其他公开 AI 的预测结论。
- 未核验赔率解释。
- LLM 对资料的总结。

## Kimi 使用边界

允许用途：

- 作为 Plan B 的主要分析对象。
- 作为 AI crowd prediction 语料。
- 作为候选因子种子。
- 作为 Marginalia 边注材料。
- 作为 public AI baseline。
- 作为 parser fixture 和数据门控对象。

禁止用途：

- 不把 Kimi 概率作为 CDS 的事实输入。
- 不把 Kimi reason 直接升格为 Factor Ledger 因子。
- 不把 300 Agent 当作 300 个独立专家。
- 不声称复现 Kimi 内部模型。
- 不用 Kimi 结论证明 CDS 更准。

## 赔率 / 市场信息使用边界

允许用途：

- 作为公开 baseline。
- 作为市场叙事或外部参照。
- 作为“市场如何看待路径”的描述性材料。
- 在明确标注后，用于识别 consensus / contrarian gap。

禁止用途：

- 不输出投注建议。
- 不输出仓位或赔率价值判断。
- 不报告收益率、PnL、Sharpe 或 Max Drawdown。
- 不把赔率变化作为唯一事实源。

## Factor Ledger 入账规则

一个条目进入 Factor Ledger 前必须满足：

- 有 `observable_proxy`。
- 有 `settlement_rule`。
- 有时间窗口。
- 有数据来源。
- 有支持、削弱、反证或 inconclusive 的判定标准。

不满足上述条件的内容进入 Marginalia，而不是被强行转成因子。

## Marginalia 保留规则

以下内容可以进入 Marginalia：

- 有解释价值但无法结算的心理叙事。
- 历史隐喻。
- 球迷直觉。
- 玄学或象征性 reason。
- 模型声称但无法核验的中间过程。

Marginalia 的价值是保留语义，不是伪装成可结算事实。

## 相关文件

- `docs/design/specs/2026-06-11-cds4worldcup2026-path-space-spec.md`
- `docs/path-card-template.md`
- `docs/design/plans/2026-06-11-mvp0-data-gate-plan.md`
