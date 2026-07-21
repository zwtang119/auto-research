# Championship Path Simulation Card: 乌兹别克斯坦 (Uzbekistan)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `uzbekistan`

## 1. Team Profile

```yaml
team: 乌兹别克斯坦 (Uzbekistan)
team_slug: uzbekistan
confederation: AFC
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

乌兹别克斯坦是中亚足球的旗帜，2026 年世界杯是其历史上首次参加决赛圈。球队长期在亚洲区预选赛中保持竞争力，阿贝尔·雷斯潘特（Abel Respo）等效力于欧洲联赛的球员提升了球队的天花板。肖穆罗多夫（Eldor Shomurodov）在意甲的效力经历为锋线提供了有限但宝贵的欧洲顶级联赛经验。K 组同组葡萄牙、哥伦比亚和刚果(金)，签运极为艰难。

## 2. Championship Thesis

> 如果乌兹别克斯坦夺冠，最可能是因为球队以极致的战术纪律性和身体对抗强度在 K 组偷得出线权，守门员在淘汰赛上演历史级表演，肖穆罗多夫或替代前锋在反击中把握住了每一个机会，且葡萄牙和哥伦比亚在 K 组的互相消耗为乌兹别克斯坦创造了前所未有的机会窗口——整个夺冠路径依赖至少 5 场"不可能的胜利"。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| K 组两个世界级对手 | bracket_strength | 葡萄牙和哥伦比亚的综合实力远高于乌兹别克斯坦 | K 组控球率和射门比 |
| 首次参加世界杯的零经验 | psychological_pressure | 全队无人有世界杯决赛圈经验，首场比赛可能极度紧张 | 首场比赛失误率 |
| 进攻创造力严重不足 | low_scoring_dependency | 缺乏世界级进攻组织者，面对高强度防守时进攻手段极为有限 | 场均射门数和 xG |
| 与顶级球队的整体实力差距 | base_strength_gap | 技战术水平和球员个体能力与葡萄牙/哥伦比亚存在结构性差距 | 控球率和射门比 |
| 面对高位压迫的应对能力 | tactical_mismatch | 乌兹别克斯坦球员很少面对欧洲级别的压迫体系 | 面对压迫型球队的传球成功率 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| K 组至少击败刚果(金) | 小组赛 | 至少 1 胜 | 小组赛 0 胜 |
| 防守端至少 1 场零封 | 小组赛 | 至少 1 场不失球 | 小组赛场场失球 ≥2 |
| 肖穆罗多夫或替代前锋进球 | 小组赛 | 锋线球员小组赛进球 ≥1 | 小组赛 0 球 |
| 小组出线（极度困难） | 小组赛 | 以最佳第三名出线 | 小组垫底 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| K 组葡萄牙和哥伦比亚互耗 | 两强互相消耗可能为乌兹别克斯坦创造偷分空间 | 是 | K 组积分分布 |
| 守门员爆发 | 单场或连续场次的神勇表现可能制造爆冷 | 是 | 守门员扑救率 |
| 高温天气利好适应型球队 | 中亚干燥气候可能帮助球队适应北美部分赛区的环境 | 是 | 比赛日气温和湿度 |
| 对手轻敌 | 葡萄牙/哥伦比亚可能低估首次参赛的亚洲球队 | 部分 | 对手轮换程度 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 6
conditions:
  - condition: K 组以最佳第三名出线
    type: precursor
    observable_proxy: K 组积分
    settlement_rule: 小组积分 ≥3 且净胜球足以获最佳第三名
  - condition: 守门员淘汰赛至少 2 场零封
    type: precursor
    observable_proxy: 守门员淘汰赛零封场次
    settlement_rule: 淘汰赛零封 ≥2 场
  - condition: 防守端全赛程场均失球 ≤1
    type: precursor
    observable_proxy: 全赛程失球数
    settlement_rule: 场均失球 ≤1
  - condition: 肖穆罗多夫淘汰赛进球 ≥3
    type: precursor
    observable_proxy: 肖穆罗多夫淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥3
  - condition: 至少 2 场淘汰赛对手核心球员缺席
    type: branch
    observable_proxy: 对手伤病情况
    settlement_rule: 至少 2 场淘汰赛对手核心缺席
  - condition: 淘汰赛至少 3 场以 1 球优势获胜
    type: branch
    observable_proxy: 淘汰赛比分
    settlement_rule: 淘汰赛 3+ 场以 1 球优势获胜
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
| uzbekistan-defensive-discipline | 防守纪律性 | precursor | 小组赛失球数 | 场均失球 ≤1.5 | public-football-knowledge |
| uzbekistan-counter-attack | 反击效率 | precursor | 反击进球占比 | 反击进球 ≥总进球 40% | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 乌兹别克斯坦为首次参加世界杯的中亚球队，数据极为有限。核心判断基于亚洲区预选赛表现和肖穆罗多夫的俱乐部数据。
>
> 来源：公开足球知识（亚洲区预选赛记录、肖穆罗多夫俱乐部数据）
> 上下文：K 组与葡萄牙、哥伦比亚、刚果(金)同组，出线概率极低
> 不进入 Factor Ledger 的原因：缺乏足够的可判定数据支撑因子

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 11 节 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: K 组出线本身已是巨大挑战——葡萄牙实力碾压，哥伦比亚明显占优。乌兹别克斯坦最现实的路径是在与刚果(金)的直接对话中取胜，争取以最佳第三名出线。16 强赛面对顶级对手时大概率止步。首次参加世界杯的经验本身就有巨大价值。

**最不可信叙事**: "乌兹别克斯坦可以在 K 组出线甚至走远"——客观评估 K 组两个对手的水平，乌兹别克斯坦的出线概率极低，夺冠概率接近于零。

**最值得赛中监控的信号**: (1) 小组赛对刚果(金)的结果（决定出线希望的唯一可能窗口）；(2) 防守端的纪律性和守门员表现；(3) 肖穆罗多夫面对高强度防守时的触球次数和射门效率。

**如果夺冠，哪些赛前判断有价值**: (1) 首次参加世界杯的球队没有历史包袱，可能释放超常表现；(2) 中亚球队的体能和对抗强度在国际足坛长期被忽视；(3) 但需要诚实承认：夺冠所需的条件组合几乎不可能同时满足，这是本届赛事中概率最低的夺冠路径之一。
