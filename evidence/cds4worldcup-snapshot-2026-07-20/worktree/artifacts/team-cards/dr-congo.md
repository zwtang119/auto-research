# Championship Path Simulation Card: 刚果(金) (DR Congo)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `dr-congo`

## 1. Team Profile

```yaml
team: 刚果(金) (DR Congo)
team_slug: dr-congo
confederation: CAF
group: K
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - none_yet
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: []
  red_sources: []
  coverage: thin
```

刚果(金)是非洲足球历史强国，两届非洲杯冠军（1968、1974），1974 年以扎伊尔名义首次参加世界杯。近年来非洲区预选赛中展现了竞争力，重返世界杯决赛圈。球队拥有在欧洲联赛效力的球员，但整体阵容与 K 组的葡萄牙和哥伦比亚存在显著差距。K 组签运艰难，面对两个世界级对手。

## 2. Championship Thesis

> 如果刚果(金)夺冠，最可能是因为球队的物理强度和个体技术在北美高温环境中形成了碾压级优势，在 K 组利用葡萄牙和哥伦比亚的互相消耗偷得出线权，守门员在淘汰赛阶段上演了非洲球队从未有过的连续神勇表演，且整个夺冠路径建立在极致的防守反击和定位球战术之上。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| K 组葡萄牙和哥伦比亚的压倒性实力 | bracket_strength | 两个世界级对手使小组出线极为困难 | K 组积分 |
| 与顶级球队的整体实力差距 | base_strength_gap | 技战术水平和球员个体能力与葡萄牙/哥伦比亚存在结构性差距 | 控球率和射门比 |
| 进攻创造力不足 | low_scoring_dependency | 缺乏世界级进攻组织者和稳定射手 | 场均 xG 和进球数 |
| 大赛经验匮乏 | psychological_pressure | 自 1974 年以来首次参加世界杯，全队缺乏决赛圈经验 | 首场比赛失误率 |
| 阵容深度不足 | squad_depth | 替补与首发差距大，无法支撑 7 场高强度比赛 | 替补上场后的场面数据 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| K 组至少击败乌兹别克斯坦 | 小组赛 | 至少 1 胜 | 小组赛 0 胜 |
| 防守端面对葡萄牙/哥伦比亚保持纪律 | 小组赛 | vs 强队失球 ≤2 | 被大比分击败 |
| 小组出线（极其困难） | 小组赛 | 以最佳第三名出线 | 小组垫底 |
| 守门员至少 1 场淘汰赛零封 | 淘汰赛 | 淘汰赛零封 ≥1 场 | 淘汰赛场场失球 ≥2 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| K 组葡萄牙和哥伦比亚互耗 | 两强互相消耗可能为刚果(金)创造偷分空间 | 是 | K 组积分分布 |
| 高温天气利好非洲球队 | 刚果(金)球员的热带气候适应性优于欧洲/南美球员 | 是 | 比赛日气温 |
| 守门员爆发 | 单场或连续场次的神勇表现可能制造爆冷 | 是 | 守门员扑救率 |
| 对手轻敌 | 葡萄牙/哥伦比亚可能低估非洲对手 | 部分 | 对手轮换程度 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: K 组以最佳第三名出线
    type: precursor
    observable_proxy: K 组积分
    settlement_rule: 小组积分 ≥4 出线
  - condition: 守门员淘汰赛至少 2 场零封
    type: precursor
    observable_proxy: 守门员淘汰赛零封场次
    settlement_rule: 淘汰赛零封 ≥2 场
  - condition: 防守端全赛程场均失球 ≤1
    type: precursor
    observable_proxy: 全赛程失球数
    settlement_rule: 场均失球 ≤1
  - condition: 至少 2 场淘汰赛对手核心缺席
    type: branch
    observable_proxy: 对手伤病情况
    settlement_rule: 至少 2 场淘汰赛对手核心缺席
  - condition: 淘汰赛至少 2 场 1-0 获胜
    type: branch
    observable_proxy: 淘汰赛比分
    settlement_rule: 淘汰赛 2+ 场 1-0 胜
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
| dr-congo-physical-intensity | 物理强度优势 | precursor | 场均对抗成功率 | 对抗成功率 ≥55% | public-football-knowledge |
| dr-congo-climate-adaptation | 高温气候适应 | precursor | 下半场跑动距离保持率 | 下半场跑动距离 ≥上半场 90% | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 刚果(金)数据极为有限。核心判断基于非洲足球的一般特征和预选赛表现。
>
> 来源：公开足球知识（非洲杯历史、预选赛记录）
> 上下文：K 组与葡萄牙、哥伦比亚、乌兹别克斯坦同组
> 不进入 Factor Ledger 的原因：缺乏足够的可判定数据支撑因子

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 11 节 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: K 组出线本身已是巨大挑战——葡萄牙实力碾压，哥伦比亚明显占优。刚果(金)最现实的路径是在与乌兹别克斯坦的直接对话中取胜，争取以最佳第三名出线。16 强赛面对顶级对手时大概率止步。但非洲球队在世界杯上的爆冷历史（如 2022 摩洛哥）说明不可完全排除奇迹。

**最不可信叙事**: "刚果(金)的非洲球员天赋可以自动转化为胜利"——天赋不等同于团队效率，面对战术纪律性极高的欧洲和南美球队时，纯天赋远远不够。

**最值得赛中监控的信号**: (1) 小组赛对乌兹别克斯坦的结果（决定出线希望的关键战）；(2) 守门员的扑救率和失球数；(3) 面对葡萄牙/哥伦比亚时的场面竞争力。

**如果夺冠，哪些赛前判断有价值**: (1) 非洲球队的物理强度在高温环境中被严重低估；(2) 刚果(金)的足球传统（两届非洲杯冠军）说明这个国家有足球基因；(3) 但夺冠需要的条件组合几乎不可能同时满足，应诚实面对这一现实。
