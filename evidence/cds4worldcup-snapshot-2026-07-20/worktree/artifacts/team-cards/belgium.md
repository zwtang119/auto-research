# Championship Path Simulation Card: 比利时 (Belgium)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `belgium`

## 1. Team Profile

```yaml
team: 比利时 (Belgium)
team_slug: belgium
confederation: UEFA
group: G
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - kimi_longshot
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: [kimi-aggregation]
  red_sources: [kimi-300-agent-reasons]
  coverage: partial
```

比利时的"黄金一代"已进入尾声，德布劳内（Kevin De Bruyne）仍是世界顶级中场但年龄和伤病已开始影响其稳定性。卢卡库（Romelu Lukaku）的终结效率持续波动，库尔图瓦（Thibaut Courtois）在门线上的世界级水平是最后的防线保障。G 组同组埃及、伊朗和新西兰，小组出线有较大把握但埃及的萨拉赫和伊朗的韧性不可小觑。

## 2. Championship Thesis

> 如果比利时夺冠，最可能是因为德布劳内在最后一届大赛中爆发了超越年龄的组织表演，库尔图瓦在淘汰赛阶段提供了不可逾越的门线保障，且"黄金一代"最后的余晖以最不可思议的方式完成了未竟的使命——用最后一口气跑完全程。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 黄金一代落幕的实力断层 | base_strength_gap | 核心球员老化且新一代尚未达到同等水平，整体实力与 2018 巅峰期差距明显 | 首发阵容平均年龄和球员身价对比 |
| 德布劳内的伤病和体能限制 | injury_risk | 德布劳内近两个赛季伤病频繁，7 场高强度比赛的健康是最大风险 | 德布劳内出勤率和每 90 分钟跑动距离 |
| 卢卡库终结效率的不稳定性 | low_scoring_dependency | 卢卡库在大赛关键场次的终结效率长期低于俱乐部水平 | 卢卡库大赛 xG vs 实际进球差 |
| 更衣室凝聚力问题 | psychological_pressure | 比利时多语言/多文化更衣室的内部矛盾在大赛中曾多次爆发 | 公开的更衣室不和信号 |
| G 组埃及的萨拉赫威胁 | bracket_strength | 萨拉赫的个人能力可以在任何比赛中改变战局 | G 组 vs 埃及的赛果 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 德布劳内全程健康且创造力在线 | 小组赛 | 场均关键传球 ≥3 | 德布劳内因伤缺席或效率大幅下降 |
| 卢卡库找到大赛终结节奏 | 小组赛 | 小组赛进球 ≥2 且 xG 转化率 ≥40% | 小组赛大量机会但 0-1 球 |
| G 组头名出线 | 小组赛 | 积分 ≥7 | 小组第二或第三出线 |
| 库尔图瓦在淘汰赛阶段的关键扑救 | 淘汰赛 | 淘汰赛至少 1 场零封且有关键扑救 | 库尔图瓦淘汰赛无零封 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 德布劳内最后一届大赛的情感爆发 | 类似莫德里奇效应的不可量化精神加成 | 部分 | 德布劳内场上的创造力和投入度 |
| 库尔图瓦超神表演 | 世界级门将在淘汰赛可以单独赢下 1-2 场比赛 | 是 | 库尔图瓦扑救率和 xG 阻止值 |
| 半区有利抽签 | 避免淘汰赛早期遭遇法国/西班牙 | 是 | 淘汰赛对阵表 |
| G 组低消耗出线 | 为老化的核心阵容储备淘汰赛体能 | 是 | G 组积分和上场时间 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: 德布劳内淘汰赛全程健康且创造力世界级
    type: precursor
    observable_proxy: 德布劳内淘汰赛关键传球数
    settlement_rule: 淘汰赛场均关键传球 ≥3
  - condition: 卢卡库淘汰赛 xG 转化率 ≥50%
    type: precursor
    observable_proxy: 卢卡库淘汰赛 xG vs 实际进球
    settlement_rule: 淘汰赛 xG 转化率 ≥50%
  - condition: 库尔图瓦淘汰赛至少 2 场零封
    type: precursor
    observable_proxy: 淘汰赛零封场次
    settlement_rule: 淘汰赛零封 ≥2 场
  - condition: 更衣室不出现公开矛盾
    type: precursor
    observable_proxy: 媒体报道和球员公开表态
    settlement_rule: 无公开更衣室矛盾
  - condition: 半决赛前避免遭遇法国或西班牙
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法国/西班牙交手
```

## 7. Path Simulation Notes

```yaml
simulation_status: not_run_yet
championship_path_count: null
dominant_path_pattern: null
dominant_failure_node: null
bracket_dependency: null
black_swan_dependency: null
penalty_dependency: null
injury_sensitivity: null
```

## 8. Factor Ledger Candidates

| factor_id | factor_name | relation | observable_proxy | settlement_rule | source |
|---|---|---|---|---|---|
| F-BEL-01 | 德布劳内创造力输出 | precursor | 场均关键传球数 | 淘汰赛场均关键传球 ≥3 | public-football-knowledge |
| F-BEL-02 | 卢卡库终结效率 | precursor | xG 转化率 | 淘汰赛 xG 转化率 ≥50% | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（1 条预测）

- 派别分布: 老球迷派
- Kimi 聚合概率: 0.33%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=35: "2018黄金一代最后之舞，G组签运极佳，+3500赔率被低估，德布劳内还有最后一点魔法。"

> [!memo] 2026-06-13 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正组别为 G 组（埃及/伊朗/新西兰），更新对手分析，填充 §8 | WI-0.2 组别校正 |

## 11. Current Interpretation

**最可信路径**: 以 G 组头名出线（整体实力高于同组对手），小组赛依赖德布劳内的创造力和库尔图瓦的门线稳定性。16 强赛面对非顶级对手时可能过关。1/4 决赛是真实天花板——核心球员的体能和伤病问题在这一阶段可能暴露。

**最不可信叙事**: "比利时黄金一代终于要在最后一届大赛中正名"——黄金一代的实力窗口已经关闭，2026 的比利时更多是一支正在重建的球队而非争冠球队。

**最值得赛中监控的信号**: (1) 德布劳内的出勤率和关键传球数；(2) 卢卡库的 xG 转化率；(3) 更衣室氛围（任何公开矛盾的信号）。

**如果夺冠，哪些赛前判断有价值**: (1) 德布劳内和库尔图瓦在淘汰赛阶段的个体能力仍然是世界级的；(2) "黄金一代"的告别情绪可能释放不可量化的精神力量；(3) 比利时的实力被低估了——核心球员虽然老化但经验和比赛智慧在淘汰赛中仍有价值。
