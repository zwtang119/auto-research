# Championship Path Simulation Card: 约旦 (Jordan)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `jordan`

## 1. Team Profile

```yaml
team: 约旦 (Jordan)
team_slug: jordan
confederation: AFC
group: J
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

约旦是 2023 年亚洲杯亚军（决赛负于东道主卡塔尔），这是该国足球史上最伟大的成就。2026 年世界杯是约旦历史上首次参加决赛圈。球队以纪律性防守和反击为主要战术，核心球员多数效力于中东联赛。J 组同组阿根廷、阿尔及利亚和奥地利，对约旦而言是极为艰难的签运——三个对手的综合实力均明显高于约旦。

## 2. Championship Thesis

> 如果约旦夺冠，最可能是因为球队以极致的防守纪律性和定位球战术在小组赛偷得出线权，守门员在淘汰赛阶段上演了历史级表演（类似 2023 亚洲杯的神勇状态），且 J 组强队（阿根廷、阿尔及利亚、奥地利）在互相消耗和轻敌中为约旦创造了机会窗口，整个夺冠路径依赖至少 4 场"不可能的胜利"。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与 J 组所有对手的硬实力差距 | base_strength_gap | 阿根廷、阿尔及利亚、奥地利三队综合实力均明显高于约旦 | 小组赛控球率和射门比 |
| 首次参加世界杯的大赛经验为零 | psychological_pressure | 全队无人有世界杯决赛圈经验，首场比赛可能极度紧张 | 首场比赛失误率和犯规数 |
| 进攻创造力严重不足 | low_scoring_dependency | 球队缺乏世界级进攻球员，面对高强度防守时进攻手段极为有限 | 场均射门数和 xG |
| 阵容深度不足以支撑 7 场高强度比赛 | squad_depth | 替补与首发差距巨大，一旦核心球员伤停则全队水平骤降 | 替补球员上场后的场面变化 |
| 面对高位压迫的出球能力 | tactical_mismatch | 约旦球员在俱乐部层面很少面对欧洲级别的压迫体系 | 面对压迫型球队的传球成功率 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| J 组至少取得 1 场胜利 | 小组赛 | 小组赛积分 ≥3 | 小组赛 0 分 |
| 防守端至少 1 场零封 | 小组赛 | 至少 1 场不失球 | 小组赛场场失球 ≥2 |
| 定位球成为有效进攻手段 | 小组赛 | 定位球进球 ≥1 | 定位球 0 进球 |
| 小组出线（极度困难） | 小组赛 | 以最佳第三名出线 | 小组垫底 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| J 组强队轻敌 | 阿根廷/奥地利/阿尔及利亚可能低估约旦 | 部分 | 对手轮换程度和场上表现 |
| 守门员复制 2023 亚洲杯神勇 | 约旦守门员在 2023 亚洲杯表现超常，世界杯可能再次爆发 | 是 | 守门员扑救率 |
| 高温天气缩小体能差距 | 约旦球员习惯中东气候，北美高温可能是相对优势 | 是 | 比赛日气温 |
| VAR 和裁判判罚利好防守方 | 约旦以防守为主，VAR 可能限制对手的进攻侵略性 | 是 | VAR 判罚统计 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 6
conditions:
  - condition: J 组以最佳第三名出线
    type: precursor
    observable_proxy: J 组积分
    settlement_rule: 小组积分 ≥3 且净胜球足以获最佳第三名
  - condition: 守门员淘汰赛至少 2 场零封
    type: precursor
    observable_proxy: 守门员淘汰赛零封场次
    settlement_rule: 淘汰赛零封 ≥2 场
  - condition: 定位球淘汰赛进球 ≥3
    type: precursor
    observable_proxy: 定位球进球数
    settlement_rule: 淘汰赛定位球进球 ≥3
  - condition: 全队 7 场仅失 ≤5 球
    type: precursor
    observable_proxy: 总失球数
    settlement_rule: 全赛程失球 ≤5
  - condition: 半决赛前所有对手核心至少 1 人缺席
    type: branch
    observable_proxy: 对手伤病情况
    settlement_rule: 至少 3 场淘汰赛对手核心缺席
  - condition: 淘汰赛至少 3 场 1-0 获胜
    type: branch
    observable_proxy: 淘汰赛比分
    settlement_rule: 淘汰赛 3+ 场 1-0 胜
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
| jordan-defensive-organization | 防守组织纪律性 | precursor | 小组赛失球数 | 场均失球 ≤1.5 | public-football-knowledge |
| jordan-set-piece-efficiency | 定位球进攻效率 | precursor | 定位球进球占比 | 定位球进球 ≥总进球 30% | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 约旦为首次参加世界杯的亚洲球队，数据极为有限。核心判断基于 2023 亚洲杯亚军表现。
>
> 来源：公开足球知识（2023 亚洲杯记录、预选赛表现）
> 上下文：J 组与阿根廷、阿尔及利亚、奥地利同组，出线概率极低
> 不进入 Factor Ledger 的原因：缺乏足够的可判定数据支撑因子

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 11 节 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 约旦的现实目标是 J 组争取 1 场胜利（最可能是对阿尔及利亚），以最佳第三名身份出线。如果出线，16 强赛面对顶级对手时大概率止步。但 2023 亚洲杯的亚军经历证明约旦可以在不被看好的情况下超越预期。

**最不可信叙事**: "约旦 2023 亚洲杯亚军的表现可以复制到世界杯"——亚洲杯是区域性赛事，世界杯的对手水平和比赛强度完全不同。J 组的三个对手即使是最弱的阿尔及利亚也有马赫雷斯这种世界级球员。

**最值得赛中监控的信号**: (1) 小组赛首场对阿尔及利亚的结果（决定出线希望的关键战）；(2) 防守纪律性和守门员表现；(3) 定位球进攻的效率（可能是约旦唯一的得分手段）。

**如果夺冠，哪些赛前判断有价值**: (1) 约旦是本届赛事中"不可能的奇迹"的终极候选——首次参赛+最弱签运；(2) 2023 亚洲杯的亚军经历证明这支球队有在高压环境下发挥超常的能力；(3) 但夺冠需要的条件组合概率接近于零，任何对约旦夺冠的预测都需要承认这一点。
