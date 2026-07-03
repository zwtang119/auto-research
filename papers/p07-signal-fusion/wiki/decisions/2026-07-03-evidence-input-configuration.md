# 2026-07-03 — Evidence Input Layer 重新配置

> 日期：2026-07-03
> 范围：`papers/p07-signal-fusion/`
> 状态：**已采纳**
> 决策者：AutoResearch orchestrator + 本目录 worker
> 反向引用：Roadmap §8, §10；`experiment-pitfalls.md` §5；`data-contracts.md` §10

## 1. 决策

将 `papers/p07-signal-fusion/` 由"12 数据源融合 → 决策质量提升"的薄工程论文框架，**重新定位**为 P1+P2 主线的 **evidence input layer**。

具体含义：

1. 本目录的产物不是"融合后的文本"，而是 `signal_evidence_entry` 行（`data-contracts.md §10`）。
2. 本目录不主张"novel fusion algorithm"（PIT-401）；贡献表述为：ablation protocol、bias-detection contract、evidence-ledger adapter。
3. 本目录不与下游 P1+P2 ledger 抢决策权；只生产 ledger 可消费的证据行。
4. 本目录的消融、偏差检测、freshness 比对，统一接入 `evidence_ledger_entry` 的 `supporting_evidence / contradicting_evidence / freshness_ratio / source_independence` 字段。

## 2. 替代方案与放弃原因

| 备选 | 放弃原因 |
|------|----------|
| 沿用"12 数据源融合 + p<0.05"作为主论文 | Roadmap §1 明示是薄工程，无法支撑 60 分论文 |
| 把 Calibrator 的 2.0× 比率升格为统计检验 | PIT-402：ratio 不是检验；强行包装会被审稿识破 |
| 把 P11 free-text trace 当成信号源 | PIT-207 / PIT-408：trace 不是 evidence |
| 让本目录承担 Brier / Log Loss 计算 | 那属于 P1.2 settlement layer；本目录只生产 `numeric_forecast` 字段 |

## 3. 新约束（必读）

- 输出 schema：`signal_evidence_entry`（含 `source_independence`、`contradicting_signals`、`freshness_window`、`freshness_ratio`、`audit_trace`）。
- 文本预测不作为数值概率；`numeric_forecast` 为 `[0, 1]` 或 `null`。
- `datasource_status != "active"` 的行（含 `polymarket`）一律拒绝。
- `audit_trace` 必须结构化，包含 `tool` + `*_sha256_prefix`。
- 偏差检测走 side-channel，标记 `significance_tested: false`。
- 论文贡献表述禁止使用 "novel fusion algorithm"。

## 4. 影响到的文件

| 文件 | 变化 |
|------|------|
| `state/io_spec.md` | 新建，定义生产者侧 IO 契约 |
| `wiki/index.md` | 改写角色描述、上下游接口、反例清单 |
| `wiki/concepts/signal-to-evidence-contract.md` | 新建，叙述版契约 |
| `claude-prompt.md` | 改写，删去融合主张、强调 evidence 行 |
| `mimo-prompt.md` | 改写，同上 |
| `paper/outline.md` | 新建，论文以 ablation / bias / adapter 为贡献点 |
| `state/task_spec.md` | **本次不改**，保持现有 milestone 框架，下次评审时按新定位重排 |
| `state/progress.json` | **本次不改**，predetermined_config 与新分组一致 |

## 5. 关联决策

- `decisions/datasource-selection.md` — 12 active 数据源选择（保留）
- `decisions/fusion-algorithm.md` — recency + 方向加权（保留，但不再作为论文主张）
- `decisions/quality-thresholds.md` — 2.0× 比率阈值（保留，明确为启发式而非检验）

## 6. 待办（不在本次 scope）

- 重新整理 `state/task_spec.md` 的 M1-M9，按 evidence input layer 重排。
- 实现 `experiments/signals/*.jsonl` 与冲突发现代码（本决策明确**不实现**）。
- 与 `papers/p1p2-evidence-ledger/` 对齐接字段（本目录只声明契约，不写 adapter）。
- 在 5 个 pitfall 都产生 5 次 `pitfall_avoided` 后回收 pre-check。

## 7. 反向引用

- Roadmap：`docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §8
- 数据契约：`../../../../framework/schemas/data-contracts.md` §10
- 反例清单：`../../../../framework/schemas/experiment-pitfalls.md` §5
- 项目组合：`docs/portfolio/project-index.md` §2