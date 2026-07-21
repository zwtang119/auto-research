# Path Card Internal Audit Report

> **类型**: research-report
> **日期**: 2026-06-11
> **输入**: 21 张 deep-description 路径卡 (`artifacts/team-cards/*.md`)
> **产出**: `data/processed/path_card_internal_audit.csv`, `data/processed/path_card_obstacle_type_matrix.csv`
> **审计脚本**: `scripts/audit_path_cards.py`

## 1. Executive Summary

21 张 deep-description 路径卡全部通过自动化审计。所有卡片在来源边界、结构完整性和可结算性方面均符合 CDS4WorldCup 当前阶段的预期。

**核心发现**：

1. **障碍类型分布呈"高频泛化 + 低频区分"模式**：6 种障碍类型出现在 ≥67% 的球队中（`low_scoring_dependency`、`psychological_pressure`、`bracket_strength`、`base_strength_gap`、`tactical_mismatch`、`squad_depth`），而仅 `injury_risk`（48%）表现为真正的区分变量。
2. **Miracle Package 可结算性 100%**：全部 89 个条件均包含 `observable_proxy` 和 `settlement_rule`，具备赛后验证能力。
3. **来源边界合规**：全部 21 张卡片的 Kimi 数据在 §9 Marginalia Notes 中正确标注为 Red Source，未泄露至 §2-§6 的事实字段。
4. **结构一致性高但同质化风险存在**：所有卡片的 §4 Required Breakthroughs 均为 4 条，§5 Black Swan Helpers 均为 4 条，呈现出明显的模板约束。

## 2. Input Scope

| 维度 | 数值 |
|------|------|
| 深描卡总数 | 21 |
| 薄切片卡（未审计） | 27 |
| 覆盖洲际 | UEFA (11), CONMEBOL (4), AFC (3), CONCACAF (2), CAF (2) |
| Kimi 覆盖球队 | 21/21 |
| 数据来源 | `artifacts/team-cards/*.md` + `data/processed/team_registry.csv` + `data/processed/kimi_baseline_signals_matrix.csv` |

## 3. Deep Card Coverage

所有 21 张卡的 `status` 均为 `deep-description`，确认：

- §2 Championship Thesis：全部填充（非占位符）
- §3 Primary Obstacles：每队 5-6 个（平均 5.2）
- §4 Required Breakthroughs：每队 4 个
- §5 Black Swan Helpers：每队 4 个
- §6 Miracle Package：每队 3-5 个条件（平均 4.2）
- §7 Path Simulation：全部 `not_run_yet`（预期状态）
- §8 Factor Ledger：全部为空（预期状态，等待 Plan B2）
- §9 Marginalia Notes：全部包含 Kimi 300 Agent 摘要 + Red Source 标注
- §11 Current Interpretation：全部包含四个子段落

## 4. Obstacle Type Distribution

基于 `path_card_obstacle_type_matrix.csv` 的统计：

| 阻力类型 | 出现次数 | 占球队比 | 频率分类 |
|----------|---------|---------|---------|
| `low_scoring_dependency` | 18 | 86% | 高频 |
| `psychological_pressure` | 16 | 76% | 高频 |
| `bracket_strength` | 16 | 76% | 高频 |
| `base_strength_gap` | 15 | 71% | 高频 |
| `tactical_mismatch` | 15 | 71% | 高频 |
| `squad_depth` | 14 | 67% | 高频 |
| `injury_risk` | 10 | 48% | 中频 |
| `travel_fatigue` | 3 | 14% | 低频 |
| `favorite_collision` | 2 | 10% | 低频 |
| `penalty_dependency` | 0 | 0% | 未出现 |

**总障碍条目**: 109（平均每队 5.2）

**注意**: `penalty_dependency` 在 0 张卡的 §3 中出现，但部分卡在 §5 Black Swan Helpers 中提到了点球相关助力（如阿根廷的马丁内斯、摩洛哥的布努）。

## 5. Constraint Classification

按照 spec §5.6 的三分类框架：

### 5.1 Universal Constraints（普遍约束）

出现在 ≥60% 球队中，反映世界杯路径的结构性边界条件而非模板填充：

| 阻力类型 | 球队覆盖率 | 判定理由 |
|----------|-----------|---------|
| `low_scoring_dependency` | 86% | 世界杯淘汰赛进球稀缺是实证规律；终结效率问题横跨顶级和二线球队 |
| `bracket_strength` | 76% | 分组赛程和淘汰赛签运是所有球队的客观约束 |
| `base_strength_gap` | 71% | 硬实力差距是世界杯路径的基础性约束 |
| `tactical_mismatch` | 71% | 战术相克性在锦标赛制中具有普遍性 |
| `squad_depth` | 67% | 7 场赛制 + 高温环境使阵容深度成为普遍瓶颈 |

**判定**: 这 5 种类型虽然高频，但每个卡片中的具体表述（如西班牙的"正印中锋终结效率"vs 日本的"缺乏顶级射手"）确实体现了球队特异的机制，不是纯粹的万能填充项。

### 5.2 Differentiating Variables（区分变量）

| 阻力类型 | 球队覆盖率 | 区分力说明 |
|----------|-----------|-----------|
| `psychological_pressure` | 76% | **边界案例**。高频但具体机制有区分力：阿根廷的"卫冕冠军心理负担"、英格兰的"淘汰赛心理魔咒"、德国的"连续两届大赛信心创伤"——虽然类型相同，叙事机制各异 |
| `injury_risk` | 48% | 真正的区分变量：仅特定球队有核心球员伤病风险（亚马尔腿筋、姆巴佩被犯规、内马尔长期伤病），且伤病对象和影响机制因队而异 |
| `travel_fatigue` | 14% | 低频但有区分力：仅阿根廷（跨洲远征）、西班牙（北美高温）、韩国（亚洲远程）提及 |

### 5.3 Template Noise（模板噪声）

**未发现明确的模板噪声**。所有高频阻力类型在具体卡片中均包含球队特异的机制描述和可判定代理。

`psychological_pressure` 处于边界：虽然 76% 的球队包含此类型，但具体内容确实反映了不同球队的不同心理挑战（卫冕压力 vs 心理魔咒 vs 大赛经验匮乏）。建议在后续阶段审查那些仅用泛泛表述（如"心理压力"）而没有具体心理机制的条目。

## 6. Settleability Audit

| 指标 | 数值 |
|------|------|
| 总 Miracle Package 条件数 | 89 |
| 含 observable_proxy 的条件 | 89 (100%) |
| 含 settlement_rule 的条件 | 89 (100%) |
| 可结算条件（两者均明确且非占位符） | 89 (100%) |

**解读**：100% 的可结算率是一个积极信号，说明当前卡片的 §6 构造确实遵循了 Factor Ledger 入账规则（即使这些条件尚未正式进入 Factor Ledger）。

**局限**：部分条件的 `settlement_rule` 包含半定量表述（如"关键时刻不崩盘"、"不与法国交手"），其可结算性取决于赛中数据的粒度。这些条件在严格意义上是"半可结算"的——可以做出二元判断（发生了/未发生），但无法给出连续的概率评分。

## 7. Source Boundary Audit

| 检查项 | 结果 |
|--------|------|
| §9 是否包含 Red Source 标注 | ✅ 全部 21 张卡片均包含 "Kimi reason 暂作为 Red Source / 候选线索保留" |
| §8 Factor Ledger 是否为空 | ✅ 全部为空（等待 Plan B2 Codability Census） |
| §2 Championship Thesis 是否引用 Kimi | ✅ 无引用（均为独立分析） |
| §3-§6 事实字段是否引用 Kimi 概率 | ✅ 无引用（Kimi 数据仅出现在 §9） |
| Kimi 概率是否作为 CDS 事实输入 | ✅ 否（仅作为外部 baseline 信号标签） |

**结论**：来源边界合规，无 Kimi 数据泄露至事实字段。

## 8. Findings

### F1: 高频障碍类型的区分力不足是最大风险

6 种障碍类型出现在 ≥67% 的球队中。虽然具体描述有球队特异机制，但 **从纯频率角度，这些类型的信息熵极低**。如果后续分析仅依赖障碍类型做路径分类，将缺乏区分力。

**缓解措施**：障碍类型的"为什么重要"和"可判定代理"字段才是真正的区分信息来源，类型标签本身只是粗粒度分类。

### F2: `penalty_dependency` 分类存在但不使用

`penalty_dependency` 在模板中被列为障碍类型，但在 0 张卡的 §3 中出现。这可能反映：
- (a) 点球依赖不是一个赛前的结构 性约束（而是赛中才显现的情境因素）
- (b) 该类型被错误地排除在了障碍构造之外

### F3: §4 和 §5 的结构高度同质化

所有 21 张卡的 §4 Required Breakthroughs 均为 4 条，§5 Black Swan Helpers 均为 4 条。这种精确一致可能是模板约束的产物，而非分析的有机结果。某些球队（如西班牙、法国）可能需要更多突破条件，而其他球队（如澳大利亚、比利时）可能需要更多黑天鹅助力。

### F4: §11 与 §3-§6 的一致性良好

所有 21 张卡的 §11 Current Interpretation 均包含四个子段落（最可信路径、最不可信叙事、监控信号、有价值判断），且内容与 §2-§6 的结构一致。未发现 §11 叙事与 §3-§6 分析结论矛盾的情况。

## 9. Recommended Fixes

1. **丰富低频障碍类型的使用**：`travel_fatigue`（14%）和 `favorite_collision`（10%）是真正有区分力的变量，建议在后续修订中鼓励分析更多球队是否面临这些约束。

2. **审查 `psychological_pressure` 的具体机制描述**：16/21 队包含此类型。建议标注哪些是具体的心理机制（如"卫冕冠军包袱"、"点球大战历史"）vs 泛泛表述（如"心理压力"），后者应降级或补充具体机制。

3. **松绑 §4 和 §5 的数量约束**：允许每队根据实际分析需要填写 2-7 条突破和 2-6 条黑天鹅，而非固定 4 条。

4. **将 `penalty_dependency` 移至 §5 Black Swan Helpers**：点球在当前路径卡框架中更适合作为黑天鹅助力（如阿根廷、摩洛哥的案例），而非赛前结构性障碍。

5. **补充 §8 Factor Ledger 候选**：当前所有 21 张卡的 §8 为空。建议在 Plan B2 完成后，从 §3-§6 的可结算字段中提取至少 2-3 个 Factor Ledger 候选因子。

6. **为长期计划设计阻力类型的信息熵监测**：如果后续扩展到 48 队全覆盖，需重新计算信息熵，因为 27 队薄切片的补充可能改变分布。

## 10. Next Research Implications

1. **Baseline Suite 设计**（本 spec Research Line B）应在比较框架中纳入"障碍类型区分力"作为 CDS vs Kimi 的方法论差异指标。

2. **Plan A2（Path Type 分类）** 可以利用本审计的阻力类型矩阵作为输入特征，但需注意高频类型的低区分力可能导致聚类效果不佳。

3. **可编码性标注**（Plan B2）应优先审计 §3 的"为什么重要"和"可判定代理"字段的可编码性，而非仅依赖类型标签。

---

> [!memo] 2026-06-11 本报告由 AIwork 根据 spec `2026-06-11-aiwork-research-audit-and-baseline-spec.md` 自动生成。所有结论基于 `scripts/audit_path_cards.py` 的定量输出 + 人工审查判定。
