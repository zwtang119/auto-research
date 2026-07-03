# P2.1 Evidence Input Layer — 知识库索引

> **新定位 (2026-07-03)**：evidence input layer for the P1+P2 evidence-ledger mainline.
> 不再以"12 数据源融合"作为主论文贡献。生产者发出 `signal_evidence_entry`
> 行供下游 P1+P2 ledger 与 P1.2 settlement 消费。
>
> **实验**：12 active 数据源 → 标准化信号 → 偏差检测 → 结构化证据行
> **模型**：Minimax M3
> **状态**：重新配置阶段 (Roadmap §8, §10)
> **知识库** → `wiki/`（Marginalia v0.3.1）
> **IO 契约** → `state/io_spec.md`

---

## 角色与不目标

| 我做 | 我不做 |
|------|--------|
| 把 12 个数据源映射到 `signal_evidence_entry` | 重新设计融合算法 |
| 暴露 source independence / conflict / freshness | 把文本预测当数值概率 |
| 输出可供下游 P1+P2 ledger 直接消费的证据行 | 跑端到端决策 |
| 维护 Calibrator 的 2.0× 比率检测 side-channel | 给出统计检验 |

具体非目标与反例见 `state/io_spec.md §0` 与 `wiki/decisions/2026-07-03-evidence-input-configuration.md`。

## 概念

- [[concepts/signal-to-evidence-contract]] — signal → evidence ledger entry 的契约（生产者侧）
- [[concepts/signal-fusion-pipeline]] — 既有 267 行融合链，定位为内部实现而非研究贡献
- [[concepts/multi-source-data-fusion]] — 12 数据源如何映射到三组证据分类（Group A/B/C）
- [[concepts/observable-signal]] — 4 种可观测信号类型（confirmed_fact/weak_evidence/missing_data/source_failure）
- [[concepts/information-quality-metrics]] — 信息质量度量：recency 线性插值 + 方向加权 + 2.0x 比率偏差检测
- [[concepts/cds-background]] — CDS 背景、数据源架构（14 领域、19 核心源）

## 决策

- [[decisions/2026-07-03-evidence-input-configuration]] — 2026-07-03 重新配置为 evidence input layer 的决策记录
- [[decisions/datasource-selection]] — 12 个 active datasources 的选择逻辑（与新分组保持一致）
- [[decisions/fusion-algorithm]] — 融合算法选择：保留 recency+方向加权（267 行），不主推
- [[decisions/quality-thresholds]] — 质量阈值与偏差检测阈值

## 批注

- [[annotations/fusion-experiments]] — 融合实验批注（历史；新视角下转写为 evidence 视角）

## 对比

- [[comparisons/fusion-vs-raw]] — 融合信号 vs 原始散乱数据的效果对比（保留作为 ablation 输入）

## 上下游

| 方向 | 接口 | 接收方 |
|------|------|--------|
| 上游 | cds-keyperson 12 active 数据源 | 本目录 |
| 下游 | `signal_evidence_entry` 行 | `papers/p1p2-evidence-ledger/` |
| 下游 | `bias_signal_*` 行 + `numeric_forecast` | `papers/p08-market-calibration/` |

## 反例（不要做）

- 不要把 `polymarket` 重新启用为数据源（PIT-403，datasource_status != active）
- 不要把 `inner_monologue / no_think / pure_analysis` 视为可观测信号（PIT-408）
- 不要把 Forecaster 的文本预测当作数值概率进入 Brier（PIT-302, PIT-406）
- 不要在论文里把 267 行链作为"novel fusion algorithm"主张（PIT-401）

## 相关页面

- 路线图：`docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §8
- 数据契约：`../../../../framework/schemas/data-contracts.md` §10
- 反例清单：`../../../../framework/schemas/experiment-pitfalls.md` §5
- 任务规范：`state/task_spec.md`
- IO 规范：`state/io_spec.md`
