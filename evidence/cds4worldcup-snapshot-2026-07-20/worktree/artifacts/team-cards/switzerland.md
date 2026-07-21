# Championship Path Simulation Card: 瑞士 (Switzerland)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `switzerland`

## 1. Team Profile

```yaml
team: 瑞士 (Switzerland)
team_slug: switzerland
confederation: UEFA
group: B
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
  coverage: sufficient
```

瑞士是国际大赛中最稳定的"隐形强队"——连续三届世界杯打入淘汰赛（2014、2018、2022），2020 欧洲杯八强点球淘汰法国是近年来最惊艳的表现。格拉尼特·扎卡（Granit Xhaka）是中场核心，曼努埃尔·阿坎吉（Manuel Akanji）是世界级中卫，扬·索默（Yann Sommer）虽然年事已高但仍是顶级门将。球队以战术纪律性、团队防守和淘汰赛竞争力著称。B 组同组加拿大、波黑、卡塔尔，瑞士是小组头名的有力竞争者。

## 2. Championship Thesis

> 如果瑞士夺冠，最可能是因为扎卡的中场控制和阿坎吉的防守组织在淘汰赛中构建了不可穿透的体系框架，索默的门将能力在点球大战中提供了额外保险，且 B 组低消耗的头名出线为淘汰赛储备了体能和信心——用大赛经验和战术纪律性弥补了缺乏世界级攻击手的不足，在淘汰赛的每一场僵局中找到胜利的方式。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 缺乏世界级射手 | low_scoring_dependency | 没有任何球员在顶级联赛赛季进球达到 20+，进攻终结力有限 | 中锋位置每 90 分钟进球数 |
| 与顶级强队的硬实力差距 | base_strength_gap | 核心球员虽效力于顶级俱乐部但非头牌，进攻创造力有天花板 | vs 顶级对手的控球率和射门比 |
| 索默年龄和状态风险 | injury_risk | 索默已年近 40，门将位置的状态波动可能直接影响防守 | 索默扑救成功率和反应速度 |
| 进攻创造力不足 | tactical_mismatch | 阵地战中缺乏能突破对手防线的个体创造力，过于依赖团队配合 | 场均关键传球和过人成功率 |
| 淘汰赛面对技术型球队的瓶颈 | favorite_collision | 瑞士擅长打硬仗但在面对技术更精细的球队时经常处于被动 | vs 技术型球队的控球率 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| B 组头名出线 | 小组赛 | 积分 ≥7 且不败 | 小组第二或第三出线 |
| 找到稳定的进攻终结方案 | 小组赛 | 小组赛场均进球 ≥2 且至少 1 场 3+ 进球 | 小组赛场均进球 <1.5 |
| 淘汰赛击败一支顶级对手 | 淘汰赛 | 面对 FIFA 前 10 球队取胜 | 对顶级对手场面完全被动 |
| 中场控制力验证 | 全赛程 | 扎卡中场对抗成功率 ≥55% | 扎卡中场对抗成功率 <45% |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| B 组低消耗出线 | 加拿大、波黑、卡塔尔整体竞争力有限，可能低消耗头名出线 | 是 | B 组积分和伤病情况 |
| 索默点球大战超神 | 索默的点球扑救能力已在 2020 欧洲杯 vs 法国中验证 | 是 | 是否进入点球大战 |
| 半区有利避开法国/西班牙 | 瑞士对法国有历史心理优势但整体仍需避开最顶级对手 | 是 | 淘汰赛对阵表 |
| 北美气候利好防守型球队 | 高温下强队进攻效率下降，瑞士的防守体系性价比上升 | 是 | 比赛日气温 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 3
conditions:
  - condition: B 组头名出线且小组赛低消耗
    type: precursor
    observable_proxy: B 组积分和黄牌/伤病
    settlement_rule: 积分 ≥7 且无关键球员伤病
  - condition: 扎卡中场控制力维持且淘汰赛场均关键传球 ≥2
    type: precursor
    observable_proxy: 扎卡淘汰赛传球和对抗数据
    settlement_rule: 淘汰赛传球成功率 ≥85% 且对抗成功率 ≥55%
  - condition: 半决赛前避免遭遇法国和西班牙
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
| ch-xhaka-control | 扎卡中场控制力 | precursor | 扎卡传球成功率和对抗成功率 | 传球成功率 ≥85% | public-football-knowledge |
| ch-akanji-defense | 阿坎吉防守组织 | precursor | 场均失球和零封场次 | 场均失球 ≤1 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 瑞士是 B 组中综合实力最强的球队，连续三届世界杯淘汰赛的经验是独特资产。2020 欧洲杯淘汰法国证明了球队在淘汰赛中的上限。B 组签运有利——低消耗出线可能是瑞士最大的隐藏优势。
>
> 来源：公开足球知识
> 上下文：B 组分析
> 不进入 Factor Ledger 的原因：大赛经验是定性因素，需赛中量化

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充 §1-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 B 组头名低消耗出线（三场小组赛均在掌控范围内），16 强赛面对第三名球队，1/4 决赛依靠扎卡的中场控制力和阿坎吉的防守组织与顶级对手周旋。如果拖入点球大战，索默的经验是额外保险。半决赛是瑞士在世界杯上的历史性突破。

**最不可信叙事**: "瑞士的稳定性自动等于冠军竞争力"——稳定性使瑞士成为淘汰赛常客但从未接近冠军，缺乏世界级射手是结构性天花板。

**最值得赛中监控的信号**: (1) B 组头名出线的消耗程度（黄牌、伤病）；(2) 进攻终结效率——如果场均 xG 转化率偏低，说明终结问题是结构性而非偶然性的；(3) 面对淘汰赛级别对手时中场的对抗成功率。

**如果夺冠，哪些赛前判断有价值**: (1) 瑞士的大赛淘汰赛经验是所有 B 组球队中最丰富的——这可能是最重要的隐性资产；(2) B 组的低消耗出线窗口为瑞士提供了在淘汰赛前积累体能和信心的独特机会；(3) 索默在点球大战中的能力是瑞士在淘汰赛僵局中的最大保险。
