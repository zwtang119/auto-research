# Championship Path Simulation Card: 伊拉克 (Iraq)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `iraq`

## 1. Team Profile

```yaml
team: 伊拉克 (Iraq)
team_slug: iraq
confederation: AFC
group: I
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

伊拉克是 2007 年亚洲杯冠军，这是该国足球史上最辉煌的时刻。2026 年是伊拉克自 1986 年以来第二次、也是 40 年来首次重返世界杯决赛圈。球队在亚洲区预选赛中展现了韧性，但整体实力与 I 组的法国、塞内加尔和挪威存在显著差距。核心球员多数效力于中东和次级欧洲联赛，缺乏顶级联赛经验。I 组对伊拉克而言是极其艰难的签运。

## 2. Championship Thesis

> 如果伊拉克夺冠，最可能是因为球队复制了 2007 年亚洲杯的精神奇迹——以超越物理极限的团队凝聚力弥补技术差距，守门员在淘汰赛阶段上演历史级表演，且 I 组强队（法国、塞内加尔、挪威）在互相消耗中集体状态低迷，为伊拉克创造了出线和淘汰赛的低消耗路径。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与 I 组对手的硬实力差距 | base_strength_gap | 法国、塞内加尔、挪威的整体水平远高于伊拉克，小组出线极为困难 | 小组赛控球率和射门比 |
| 缺乏顶级联赛球员 | squad_depth | 核心球员多数不在五大联赛，面对顶级对手时个人能力差距明显 | 球员所在联赛级别和上场时间 |
| 进攻创造力不足 | low_scoring_dependency | 缺乏稳定的得分点和进攻组织者，面对高强度防守时进攻手段有限 | 场均射门数和 xG |
| 大赛经验极度匮乏 | psychological_pressure | 自 1986 年以来未参加世界杯，全队几乎无人有世界杯决赛圈经验 | 首场比赛失误率和紧张程度 |
| 面对高位压迫的应对能力 | tactical_mismatch | 伊拉克球员在俱乐部层面很少面对欧洲顶级压迫体系 | 面对压迫型球队的传球成功率 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| I 组至少取得 1 场胜利 | 小组赛 | 小组赛积分 ≥3 | 小组赛 0 分或 1 分 |
| 找到稳定得分手段 | 小组赛 | 场均进球 ≥1 | 小组赛 3 场 0 球 |
| 防守端保持纪律性 | 小组赛 | 至少 1 场零封或仅失 1 球 | 场场失球 ≥3 |
| 小组出线（极度困难） | 小组赛 | 以小组第二或最佳第三名出线 | 小组垫底 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| I 组强队互耗 | 法国/塞内加尔/挪威互相消耗，可能为伊拉克创造偷分机会 | 是 | I 组积分分布 |
| 守门员历史级表演 | 单场零封或超常扑救可能制造爆冷 | 是 | 守门员扑救率和失球数 |
| 高温天气利好适应型球队 | 伊拉克球员习惯中东高温环境，北美夏季高温可能缩小体能差距 | 是 | 比赛日气温 |
| 对手轻敌 | I 组对手可能低估伊拉克，导致状态松懈 | 部分 | 对手轮换程度和场上专注度 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: I 组至少取得 1 胜 1 平成功出线
    type: precursor
    observable_proxy: I 组积分
    settlement_rule: 小组积分 ≥4 出线
  - condition: 守门员淘汰赛至少 2 场零封
    type: precursor
    observable_proxy: 守门员淘汰赛零封场次
    settlement_rule: 淘汰赛零封 ≥2 场
  - condition: 全队找到至少 2 个稳定得分点
    type: precursor
    observable_proxy: 不同球员进球分布
    settlement_rule: 至少 2 名球员各进 ≥1 球
  - condition: 半决赛前所有对手核心球员至少 1 人缺席
    type: branch
    observable_proxy: 对手伤病情况
    settlement_rule: 至少 2 场淘汰赛对手核心缺席
  - condition: 淘汰赛至少 2 场进入点球大战且获胜
    type: branch
    observable_proxy: 点球大战次数和结果
    settlement_rule: 点球大战胜率 100%
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
| iraq-group-survival | I 组出线能力 | precursor | 小组赛积分 | 积分 ≥4 出线 | public-football-knowledge |
| iraq-defensive-discipline | 防守纪律性 | precursor | 小组赛失球数 | 场均失球 ≤1.5 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 伊拉克为 2026 世界杯 40 年来首次回归的亚洲球队，数据极为有限。
>
> 来源：公开足球知识（亚洲杯历史、预选赛记录）
> 上下文：I 组与法国、塞内加尔、挪威同组，出线概率极低
> 不进入 Factor Ledger 的原因：缺乏足够的可判定数据支撑

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 11 节 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: I 组出线本身已是巨大挑战——法国实力碾压，塞内加尔和挪威也明显占优。伊拉克最现实的路径是凭借防守纪律性和定位球战术在小组赛中偷得 1 胜 1 平，以最佳第三名身份勉强出线。16 强赛面对顶级对手时大概率止步。

**最不可信叙事**: "伊拉克 2007 年亚洲杯夺冠的奇迹可以复制到世界杯"——2007 年亚洲杯是区域性赛事，世界杯的竞争强度和对手水平完全不可同日而语。I 组的三个对手都是世界级球队。

**最值得赛中监控的信号**: (1) 小组赛首场对挪威的结果（决定出线希望的关键战）；(2) 防守端的纪律性和定位球进攻效率；(3) 面对法国时的场面竞争力（反映与顶级球队的真实差距）。

**如果夺冠，哪些赛前判断有价值**: (1) 伊拉克 40 年重返世界杯的精神动力是所有参赛队中最纯粹的；(2) 高温环境可能是缩小实力差距的唯一物理优势；(3) 2007 年亚洲杯证明了伊拉克足球在极端逆境中可以超越自身水平——但复刻概率极低。
