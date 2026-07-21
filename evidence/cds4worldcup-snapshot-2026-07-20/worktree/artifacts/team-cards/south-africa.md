# Championship Path Simulation Card: 南非 (South Africa)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `south-africa`

## 1. Team Profile

```yaml
team: 南非 (South Africa)
team_slug: south-africa
confederation: CAF
group: A
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

南非（Bafana Bafana）是 2023 非洲杯季军，展现了近年来非洲层面的竞争力回升。门将罗恩文·威廉姆斯（Ronwen Williams）是 2023 非洲杯最佳门将，在点球大战中表现突出。珀西·陶（Percy Tau）是进攻端最依赖的创造力来源。球队整体以体能和防守纪律性为基础，进攻创造力有限。A 组同组墨西哥、韩国、捷克，小组出线有难度但并非不可能。

## 2. Championship Thesis

> 如果南非夺冠，最可能是因为威廉姆斯在淘汰赛阶段连续贡献世界级门将从点球大战中拯救球队，球队以极致的防守纪律性将每场淘汰赛拖入低比分消耗战，且 A 组相对温和的小组赛消耗为淘汰赛储备了体能——用非洲球队的身体素质和门将优势弥补了进攻端的系统性不足。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与世界级球队的硬实力差距 | base_strength_gap | 除威廉姆斯外缺乏在欧洲顶级联赛效力的核心球员 | vs 欧美球队的控球率和射门比 |
| 进攻创造力严重不足 | low_scoring_dependency | 珀西·陶是唯一稳定创造力来源，替补水平差距明显 | 场均 xG 和关键传球数 |
| 大赛淘汰赛经验极度缺乏 | psychological_pressure | 南非从未在世界杯淘汰赛中出场，2023 非洲杯季军是最接近的经验 | 淘汰赛首场表现 |
| 7 场赛制的阵容深度 | squad_depth | 替补与首发差距大，伤病停赛会直接削弱竞争力 | 替补上场后场面变化 |
| 北美远征的旅行疲劳 | travel_fatigue | 从南非到北美的长途旅行可能影响恢复 | 比赛间隔的体能数据 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| A 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 珀西·陶以外找到得分点 | 小组赛 | 至少 1 名非陶球员小组赛进球 ≥2 | 陶以外球员 0 球 |
| 防守纪律性验证 | 全赛程 | 场均失球 ≤1 且至少 1 场零封 | 场均失球 ≥2 |
| 淘汰赛面对欧美球队不崩盘 | 淘汰赛 | 面对欧美球队场面不失控 | 面对欧美球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 威廉姆斯点球大战超神 | 2023 非洲杯已验证的点球专家，可在淘汰赛改变战局 | 是 | 是否进入点球大战 |
| A 组其他三队互相消耗 | 墨西哥、韩国、捷克实力接近，互耗可能为南非创造窗口 | 是 | A 组积分分布 |
| 高温天气利好体能型球队 | 南非球员在高温环境中的适应能力可能优于欧洲球队 | 是 | 比赛日气温 |
| 半区有利抽签 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: A 组成功出线
    type: precursor
    observable_proxy: A 组积分
    settlement_rule: 积分 ≥4 出线
  - condition: 威廉姆斯全程健康且淘汰赛状态世界级
    type: precursor
    observable_proxy: 威廉姆斯淘汰赛扑救数和零封场次
    settlement_rule: 淘汰赛场均扑救 ≥4 且至少 1 场零封
  - condition: 防守端淘汰赛场均失球 ≤0.5
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤0.5
  - condition: 半决赛前避免遭遇法国、阿根廷或巴西
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法/阿/巴交手
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
| sa-gk-penalty | 门将点球大战能力 | precursor | 威廉姆斯点球大战扑救率 | 点球大战扑救率 ≥30% | public-football-knowledge |
| sa-defense-discipline | 防守纪律性 | precursor | 场均失球和零封场次 | 场均失球 ≤1 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 南非数据覆盖较薄，2023 非洲杯季军是主要竞技参考。威廉姆斯的点球能力是可验证的独特优势。
>
> 来源：公开足球知识
> 上下文：A 组分析
> 不进入 Factor Ledger 的原因：数据点有限，需赛中验证

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充 §1-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: A 组以最佳第三名或第二出线（利用墨西哥、韩国、捷克三队互相消耗的窗口），16 强赛面对非顶级对手时依靠威廉姆斯的门将能力和全队的防守纪律性拖入低比分比赛。如果能进入 1/8 决赛，这已是南非在世界杯历史上的重大突破。

**最不可信叙事**: "南非凭借非洲杯季军的势头直接竞争冠军"——2023 非洲杯的参赛球队水平与世界杯淘汰赛阶段的对手不可同日而语，进攻端的创造力不足是结构性问题。

**最值得赛中监控的信号**: (1) A 组出线过程和净胜球；(2) 珀西·陶以外球员的进攻贡献；(3) 威廉姆斯的扑救数据——如果场均扑救持续偏高，说明防守压力过大不可持续。

**如果夺冠，哪些赛前判断有价值**: (1) 威廉姆斯是本届赛事最被低估的门将，点球大战能力是南非在淘汰赛中的最大保险；(2) A 组四队实力相对接近意味着小组赛消耗可控，为淘汰赛储备体能；(3) 非洲球队的身体素质在北美高温环境中可能产生额外优势。
