# Championship Path Simulation Card: 苏格兰 (Scotland)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `scotland`

## 1. Team Profile

```yaml
team: 苏格兰 (Scotland)
team_slug: scotland
confederation: UEFA
group: C
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
  coverage: partial
```

苏格兰是足球历史上最古老的球队之一，但自 1998 年以来首次重返世界杯决赛圈。安德鲁·罗伯逊（Andrew Robertson）是利物浦和国家队队长，约翰·麦金（John McGinn）在阿斯顿维拉表现出色，斯科特·麦克托米奈（Scott McTominay）在那不勒斯展现了中场得分能力。球队以身体对抗、高强度跑动和定位球为主要武器。2024 欧洲杯小组出局但积累了宝贵的大赛经验。C 组同组巴西、摩洛哥、海地，与摩洛哥争夺第二是现实目标。

## 2. Championship Thesis

> 如果苏格兰夺冠，最可能是因为罗伯逊的领导力和麦金的得分能力在淘汰赛中爆发了超越个体水平的集体能量，球队的定位球和高强度跑动在北美高温环境中成为碾压级武器，且 C 组与巴西和摩洛哥的对抗意外地锻造出了最强版本的国家队——用纯粹的意志力和体能优势完成了从 24 年世界杯缺席到世界冠军的史诗级跨越。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与巴西和摩洛哥的硬实力差距 | base_strength_gap | 巴西的个体天赋和摩洛哥的战术纪律性都是结构性优势 | vs 巴西/摩洛哥的控球率和射门比 |
| 缺乏世界级射手 | low_scoring_dependency | 麦金虽然是优秀中场但非顶级射手，锋线缺乏稳定 20+ 级别中锋 | 中锋位置每 90 分钟进球数 |
| 24 年世界杯缺席的代际经验缺口 | psychological_pressure | 长期缺席世界杯导致球队缺乏淘汰赛级别的经验积累 | 淘汰赛首场表现 |
| 技术精细度不足 | tactical_mismatch | 球队以身体和意志力见长但缺乏面对技术型球队时的控球能力 | vs 技术型球队的控球率 |
| 阵容深度有限 | squad_depth | 替补与首发差距大，伤病停赛会直接削弱竞争力 | 替补上场后场面变化 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| C 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 击败海地且从巴西或摩洛哥拿分 | 小组赛 | vs 海地全取 3 分 + vs 巴/摩至少 1 分 | vs 海地丢分且 vs 巴/摩 0 分 |
| 麦金或麦克托米奈进球效率验证 | 小组赛 | 中场球员小组赛合计进球 ≥2 | 中场球员 0 球 |
| 防守纪律性验证 | 全赛程 | 场均失球 ≤1 | 场均失球 ≥2 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| C 组巴西和摩洛哥互耗 | 两强互相消耗为苏格兰创造第二出线窗口 | 是 | C 组积分 |
| 苏格兰球迷的大规模到场 | "Tartan Army"的声势在北美可能提供额外支持 | 是 | 球场观众反应 |
| 高温天气利好体能型球队 | 苏格兰的高强度跑动在高温中可能放大效果 | 是 | 比赛日气温 |
| 定位球在淘汰赛成为武器 | 苏格兰的定位球能力在面对高强度防守时可能是破局关键 | 是 | 定位球进球占比 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: C 组成功出线
    type: precursor
    observable_proxy: C 组积分
    settlement_rule: 积分 ≥4 出线
  - condition: 麦金淘汰赛进球+助攻 ≥2
    type: precursor
    observable_proxy: 麦金淘汰赛进攻输出
    settlement_rule: 淘汰赛进球+助攻 ≥2
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 半决赛前避免遭遇法国或西班牙
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法/西交手
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
| sc-set-piece | 定位球得分效率 | precursor | 定位球进球占总进球比 | 定位球进球占比 ≥30% | public-football-knowledge |
| sc-robertson-leadership | 罗伯逊领导力 | precursor | 左路攻防输出和队长影响力 | 助攻+关键传球 ≥1/场 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 苏格兰 24 年后重返世界杯本身就是一个重大叙事。C 组虽然巴西和摩洛哥很强，但 48 队赛制下的最佳第三名规则为苏格兰提供了额外窗口。vs 海地是最关键的小组赛——必须全取 3 分。
>
> 来源：公开足球知识
> 上下文：C 组分析
> 不进入 Factor Ledger 的原因：世界杯长期缺席的影响需赛中验证

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充 §1-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 C 组第二或最佳第三名出线（击败海地，从巴西或摩洛哥身上争取 1 分），16 强赛面对非顶级对手时依靠身体对抗、定位球和"Tartan Army"的声势。如果能进入 1/8 决赛，这将是苏格兰自 1974 年以来在世界杯上的最佳战绩。

**最不可信叙事**: "苏格兰的激情和意志力可以弥补一切技术差距"——2024 欧洲杯小组出局证明了激情不足以弥补与顶级球队的结构性差距。但 C 组并非不可突破——摩洛哥是可竞争的对手。

**最值得赛中监控的信号**: (1) vs 海地的赛果——必须获胜；(2) 定位球得分占比——如果过高说明阵地战创造不足；(3) 麦金和麦克托米奈的进攻输出——中场得分是苏格兰最独特的武器。

**如果夺冠，哪些赛前判断有价值**: (1) 24 年的等待赋予了这支球队独特的历史叙事动力——"Tartan Army"的支持可能是本届赛事最忠诚的球迷力量；(2) 高强度跑动和定位球在北美高温中可能比预期更有效；(3) 麦金是本届赛事中最被低估的中场得分手之一。
