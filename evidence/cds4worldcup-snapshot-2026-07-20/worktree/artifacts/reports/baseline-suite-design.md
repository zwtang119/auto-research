# Baseline Suite Design Report

> **类型**: research-report
> **日期**: 2026-06-11
> **状态**: designed_not_populated
> **Spec**: `docs/design/specs/2026-06-11-aiwork-research-audit-and-baseline-spec.md`

---

## 1. 目的

本报告设计一套朴素基线和外部 baseline，用于回答：

> 如果一个极简 baseline 已经解释了公开共识，那么 Kimi 和 CDS 分别新增了什么信息？

**核心原则**：不做冠军预测，不输出投注建议，不报告 ROI/PnL/Sharpe。

---

## 2. Baseline 列表

### 2.1 uniform_48 — 无信息基线

| 属性 | 值 |
|------|-----|
| baseline_id | `uniform_48` |
| 名称 | 48 队均匀分布 |
| 构造规则 | 每支球队分配 1/48 ≈ 2.08% 夺冠概率 |
| 来源等级 | Mixed（理论构造，无外部数据） |
| 用途 | 所有其他 baseline 的逻辑地板 |

**为什么不重要但必须存在**：如果一个方法不比均匀分布好，那它不包含任何信息。这是 Brier Score 的零点参照。

### 2.2 defending_champion — Recency Bias 基线

| 属性 | 值 |
|------|-----|
| baseline_id | `defending_champion` |
| 名称 | 上届冠军自动续约 |
| 构造规则 | 阿根廷 100%，其余 47 队 0% |
| 来源等级 | Green（2022 FIFA World Cup 赛果） |
| 用途 | 测试"押注最近冠军"这一朴素认知偏差 |

**价值**：如果其他 baseline 在 Brier Score 上不超过这个基线太多，说明预测增量有限。

### 2.3 fifa_ranking_proxy — 单因子实力基线

| 属性 | 值 |
|------|-----|
| baseline_id | `fifa_ranking_proxy` |
| 名称 | FIFA 排名倒数归一化 |
| 构造规则 | 取 FIFA 排名倒数 1/R，归一化为概率分布（R = 排名位次） |
| 来源等级 | Green（FIFA Men's World Ranking 公开发布） |
| 数据需求 | 赛前最后一次发布的 FIFA 排名 |

**局限性**：FIFA 排名被广泛认为信息量低于 Elo，且更新频率低。但它是最公开可获取的实力指标。

### 2.4 elo_proxy — 单因子实力基线（改进版）

| 属性 | 值 |
|------|-----|
| baseline_id | `elo_proxy` |
| 名称 | Elo 等级分归一化 |
| 构造规则 | 取 Elo 分差转为期望胜率；按 Monte Carlo 模拟或闭合公式分配夺冠概率 |
| 来源等级 | Green（如 eloratings.net 公开数据） |
| 数据需求 | 赛前最终 Elo 分数 |

**改进**：Elo 优于 FIFA 排名因为它包含了比赛强度和对手质量信息。需确认赛前最终数据的可得性。

### 2.5 market_public_baseline — 外部共识基线

| 属性 | 值 |
|------|-----|
| baseline_id | `market_public_baseline` |
| 名称 | 市场公开赔率基线 |
| 构造规则 | 取公开赔率隐含概率；去除 overround 后归一化为概率分布 |
| 来源等级 | Mixed（Yellow for aggregation; Green for raw public odds） |
| 数据需求 | Polymarket 或主流体育赔率平台的赛前赔率快照 |

**约束**（per source-policy.md）：
- ✅ 仅作为"市场如何看待路径"的描述性参照
- ✅ 用于识别 consensus / contrarian gap
- ❌ 不做投注建议
- ❌ 不输出 ROI、PnL、Sharpe 或 Max Drawdown

### 2.6 kimi_public_ai_baseline — AI Crowd 基线

| 属性 | 值 |
|------|-----|
| baseline_id | `kimi_public_ai_baseline` |
| 名称 | Kimi 300 Agent 聚合基线 |
| 构造规则 | 21 队使用 Kimi 原始聚合概率（归一化至 100%）；27 队标记为 `not_covered_by_kimi`，不分配概率 |
| 来源等级 | **Red**（per source-policy.md：Kimi 概率为 Red Source） |
| 数据需求 | `data/processed/kimi_baseline_signals_matrix.csv`（已处理数据） |

**覆盖范围**：Kimi 300 Agent 仅覆盖 21/48 队。21 队概率归一化至 100%（Kimi 聚合概率已覆盖全部概率质量）。27 队标记为 `not_covered_by_kimi`，不分配概率，不补充均匀分布。

**Brier Score 计算规则**：仅在 21 队 Kimi 覆盖范围内计算，或将 21 队分布归一化至 100%（因为 Kimi 已覆盖其全部概率质量）。

**Smoothing 规则**：如需完整 48 队概率分布（例如与其他 baseline 对比），另建 `kimi_smoothed_baseline`，不修改原始 Kimi 基线。

**约束**（per source-policy.md）：
- ✅ 作为 public AI baseline
- ❌ 不作为 CDS 事实输入
- ❌ 不用 Kimi 结论证明 CDS 更准

---

## 3. Source Policy Compliance

| Baseline | Source Level | 合规状态 |
|----------|-------------|---------|
| uniform_48 | Mixed (theoretical) | ✅ 无外部数据依赖 |
| defending_champion | Green | ✅ 基于 2022 赛果 |
| fifa_ranking_proxy | Green | ✅ 公开发布的排名 |
| elo_proxy | Green | ✅ 公开可复核的 Elo 分数 |
| market_public_baseline | Mixed | ✅ 赔率仅作描述性参照；已标注"不用于投注建议" |
| kimi_public_ai_baseline | Red | ✅ 已标注 Red Source；仅作 AI baseline 对比用 |

---

## 4. Staged Calibration Design

不只在冠军产生后做一次性 Brier Score 比较，而是在四个阶段分别评估 baseline 的 path survival / mass loss：

### 4.1 Checkpoint: post_group_stage（小组赛结束后）

| 可结算问题 | 度量 |
|-----------|------|
| baseline 的概率 mass 是否仍留在存活球队上 | Mass Retention Ratio = 存活球队概率之和 / 总概率 |
| 被淘汰球队的概率 mass 有多大 | Mass Lost = 被淘汰球队概率之和 |
| 是否有 baseline 的 Top-3 球队被淘汰 | Top-3 Survival Rate |

**注意**：小组赛阶段不宣称证明谁"更准"。此 checkpoint 仅作为 path survival 诊断。

### 4.2 Checkpoint: round_of_16（16 强赛后）

| 可结算问题 | 度量 |
|-----------|------|
| Top-8 强队的路径是否被 baseline 预测 | Top-8 Coverage = Top-8 中 baseline Top-8 球队数 / 8 |
| 弱队的 baseline mass 是否已被淘汰 | Underdog Elimination Rate |

### 4.3 Checkpoint: quarterfinal（1/4 决赛后）

| 可结算问题 | 度量 |
|-----------|------|
| baseline 是否集中于仍存活强队 | Final 4 Coverage |
| baseline 的概率分布是否已收敛 | Distribution Entropy 变化 |

### 4.4 Checkpoint: final（冠军产生后）

| 可结算问题 | 度量 |
|-----------|------|
| 冠军的 baseline 排名 | Champion Rank in Baseline |
| 完整 Brier Score | Brier = Σ(p_i - o_i)² 其中 o_i=1 仅对冠军 |
| Ranked Probability Score | 衡量 Top-N 预测精度 |

**最终 settlement 不宣称 CDS 或 Kimi "更准"**。仅报告各 baseline 的 Brier Score 和 RPS，让数据说话。

---

## 5. Settlement Methodology

### 5.1 Brier Score

对每个 baseline，计算：

```
Brier = (1/N) * Σ_i (p_i - o_i)²
```

其中 N = 48（球队数），p_i 为 baseline 分配给球队 i 的夺冠概率，o_i 为 0/1（1 仅对冠军）。

Brier Score 越低越好。uniform_48 的 Brier Score 约为 (1/48) * (1 - 1/48) ≈ 0.0206。

### 5.2 Ranked Probability Score (RPS)

衡量 Top-N 预测精度，比纯 Brier 更适合多类别排名场景。

### 5.3 Mass Retention Ratio

在阶段性 checkpoint 中衡量 baseline 的生存力：

```
MRR_t = Σ_{i ∈ alive_t} p_i / Σ_all p_i
```

MRR_t = 1.0 表示所有 baseline mass 都在存活球队上。

### 5.4 不做什么

- ❌ 不报告 ROI、PnL、Sharpe、Max Drawdown
- ❌ 不宣称任何 baseline "战胜市场"
- ❌ 不用 CDS 结果作为 baseline 的一部分
- ❌ 不在小组赛阶段宣称预测优势

---

## 6. Implementation Notes

### 6.1 当前状态

所有 6 个 baseline 均为 `designed_not_populated`。数据尚未填充，因为：

1. **uniform_48**：可在任何时间填充（纯理论值）
2. **defending_champion**：可在任何时间填充（阿根廷 100%，其余 0%）
3. **fifa_ranking_proxy**：需要赛前最终 FIFA 排名数据
4. **elo_proxy**：需要赛前最终 Elo 分数
5. **market_public_baseline**：需要赛前赔率快照
6. **kimi_public_ai_baseline**：数据已在 `kimi_baseline_signals_matrix.csv` 中，但需要转为夺冠概率分布

### 6.2 数据填充时机

建议在赛前最后一个工作日（预计 2026 年 6 月中旬）统一填充所有 baseline 概率分布，冻结为 pre-tournament snapshot。

### 6.3 不伪造数据

在数据不可得时，`status` 保持为 `designed_not_populated`。不为任何 baseline 编造概率值。

---

## Appendix: Registry

完整 baseline 注册表见 `data/processed/baseline_suite_registry.csv`。
