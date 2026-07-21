# Championship Path Simulation Card: 加纳 (Ghana)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `ghana`

## 1. Team Profile

```yaml
team: 加纳 (Ghana)
team_slug: ghana
confederation: CAF
group: L
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

加纳是非洲足球的传统强国，四届非洲杯冠军（1963、1965、1978、1982），2010 年世界杯曾打入八强（苏亚雷斯手球门事件）。库杜斯（Mohammed Kudus）在西汉姆联已证明世界级潜力，帕尔特伊（Thomas Partey）在阿森纳的中场控制力已被验证。乔丹·阿尤（Jordan Ayew）提供了经验和领导力。L 组同组英格兰、克罗地亚和巴拿马，签运中等——与克罗地亚竞争第二出线权是现实目标。

## 2. Championship Thesis

> 如果加纳夺冠，最可能是因为库杜斯在淘汰赛阶段展现了超越年龄的世界级个人表演（类似 2010 年吉安的角色），帕尔特伊的中场屏障在 7 场比赛中提供了非洲球队从未有过的中场控制力，且 2010 年八强的精神遗产在关键时刻提供了心理韧性——球队在北美的高温环境中以物理强度和技术能力的结合碾压了对手。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与英格兰/克罗地亚的整体实力差距 | base_strength_gap | 虽有个别世界级球员但整体阵容深度不足 | vs 顶级对手的控球率和射门比 |
| 库杜斯被针对性限制 | tactical_mismatch | 库杜斯是球队唯一的世界级进攻创造力来源，一旦被锁死全队进攻瘫痪 | 库杜斯每场被犯规次数和触球数 |
| 帕尔特伊伤病风险 | injury_risk | 帕尔特伊近年伤病频繁，中场核心若缺阵则全队攻防体系崩溃 | 帕尔特伊出场时间和体能状态 |
| 防守端的不稳定性 | squad_depth | 后防线缺乏世界级领袖，面对顶级攻击手时可能暴露 | 场均失球和定位球失球占比 |
| L 组英格兰的压倒性优势 | bracket_strength | 英格兰大概率占据小组头名，加纳需与克罗地亚竞争出线 | L 组积分 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| L 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 库杜斯以外进攻点输出 | 小组赛 | 至少 2 名非库杜斯球员小组赛进球 | 全队进球 100% 来自库杜斯 |
| 击败克罗地亚或巴拿马 | 小组赛 | 至少 1 胜 | L 组 0 胜 |
| 防守端至少 1 场零封 | 淘汰赛 | 淘汰赛零封 ≥1 场 | 淘汰赛场场失球 ≥2 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 高温天气利好非洲球队 | 加纳球员的热带气候适应性优于欧洲球队 | 是 | 比赛日气温 |
| 库杜斯爆发世界级表现 | 库杜斯有在西汉姆联证明过的单场改变比赛能力 | 是 | 库杜斯进球+助攻+关键传球 |
| L 组英格兰提前锁定头名后轮换 | 末轮对英格兰可能面对轮换阵容 | 是 | 英格兰末轮阵容 |
| 2010 年精神遗产 | 加纳有在世界杯超越预期的传统 | 部分 | 球队关键时刻的表现 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: 库杜斯淘汰赛进球+助攻 ≥4
    type: precursor
    observable_proxy: 库杜斯淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥4
  - condition: 帕尔特伊全程健康且中场控制力在线
    type: precursor
    observable_proxy: 帕尔特伊淘汰赛出场时间和传球成功率
    settlement_rule: 淘汰赛场均传球成功率 ≥85% 且无因伤缺席
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 半决赛前避免遭遇法国或阿根廷
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法国/阿根廷交手
  - condition: 至少 2 场淘汰赛对手核心球员缺席
    type: branch
    observable_proxy: 对手伤病情况
    settlement_rule: 至少 2 场淘汰赛对手核心缺席
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
| ghana-kudus-impact | 库杜斯进攻影响力 | precursor | 库杜斯每 90 分钟进球+助攻+关键传球 | 小组赛场均关键传球 ≥2 | public-football-knowledge |
| ghana-midfield-control | 中场控制力 | precursor | 帕尔特伊出场时球队控球率 | 帕尔特伊在场时控球率 ≥45% | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 加纳数据有限但核心判断基于库杜斯和帕尔特伊的俱乐部表现以及 2010 世界杯的历史遗产。
>
> 来源：公开足球知识（2010 世界杯记录、库杜斯/帕尔特伊俱乐部数据、非洲杯历史）
> 上下文：L 组与英格兰、克罗地亚、巴拿马同组
> 不进入 Factor Ledger 的原因：缺乏足够的可判定数据支撑因子

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 11 节 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: L 组以小组第二出线（在与克罗地亚和巴拿马的竞争中占据一定优势），16 强赛面对非顶级对手。库杜斯的个体能力和帕尔特伊的中场控制力在这一阶段可能足够制造威胁。1/4 决赛面对欧洲顶级球队时整体阵容深度的差距可能暴露，但加纳有超越预期的传统。

**最不可信叙事**: "加纳可以仅靠库杜斯一个人走远"——库杜斯是世界级球员但足球是 11 人的运动，帕尔特伊的健康和后防线的稳定性同样关键。

**最值得赛中监控的信号**: (1) 库杜斯的进球+助攻和被犯规次数（反映被限制程度）；(2) 帕尔特伊的出场时间和传球成功率（反映中场控制力）；(3) 防守端的零封率和定位球防守。

**如果夺冠，哪些赛前判断有价值**: (1) 加纳的 2010 年世界杯遗产说明这支球队在关键时刻不会怯场；(2) 库杜斯是非洲足球中最接近"世界级创造力"的球员，他的发挥决定了加纳的上限；(3) 高温环境可能是加纳缩小与欧洲球队差距的关键变量。
