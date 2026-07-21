# Championship Path Simulation Card: 埃及 (Egypt)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `egypt`

## 1. Team Profile

```yaml
team: 埃及 (Egypt)
team_slug: egypt
confederation: CAF
group: G
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

埃及是非洲足球的传统强队，但近年来的国际大赛表现令人失望——多次 AFCON 决赛失利（2017、2021 亚军），2022 世界杯小组赛出局。穆罕默德·萨拉赫（Mohamed Salah，利物浦前锋）是队史最伟大的球员，但他在国家队的成就远不及俱乐部。主帅鲁伊·维多利亚（Rui Vitória）执教以来球队攻守趋于平衡。G 组同组比利时、伊朗和新西兰，出线需要与伊朗激烈竞争。

## 2. Championship Thesis

> 如果埃及夺冠，最可能是因为萨拉赫在最后一届世界杯中爆发了超越年龄的进攻表演（类似 2022 梅西的最后一舞），球队在多次 AFCON 决赛失利的痛苦中淬炼出了不可动摇的心理韧性，且北非球员在北美高温环境中的体能优势成为淘汰赛的隐性武器。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 萨拉赫之外缺乏世界级球员 | base_strength_gap | 萨拉赫是唯一在欧洲顶级联赛效力的球员，其余球员水平差距明显 | 首发中五大联赛球员数量 |
| 多次 AFCON 决赛失利的心理创伤 | psychological_pressure | 2017、2021 连续 AFCON 决赛失利，球队在关键场次的信心可能脆弱 | 关键淘汰赛的场面表现 |
| 进攻端过度依赖萨拉赫 | low_scoring_dependency | 萨拉赫缺阵或被限制时进攻创造力骤降 | 萨拉赫进球/助攻占总进球比 |
| 萨拉赫的年龄和伤病 | injury_risk | 萨拉赫 34 岁，7 场高强度赛制的体能可持续性存疑 | 萨拉赫每场跑动距离和出场时间 |
| 比利时的全面实力优势 | base_strength_gap | 比利时在技术、战术和阵容深度上全面优于埃及 | vs 比利时的场面表现 |
| 非洲球队在世界杯淘汰赛的历史天花板 | psychological_pressure | 非洲球队从未进入世界杯半决赛 | 淘汰赛面对欧洲/南美球队时的场面控制力 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| G 组成功出线 | 小组赛 | 积分 ≥4 | 小组未出线 |
| 击败伊朗锁定出线名额 | 小组赛 | vs 伊朗至少 1 胜 | 负伊朗 |
| 萨拉赫之外找到进攻输出 | 小组赛 | 至少 1 名非萨拉赫球员小组赛进球 ≥1 | 萨拉赫以外球员小组赛 0 球 |
| 萨拉赫淘汰赛全程健康 | 全赛程 | 萨拉赫淘汰赛每场出场 ≥70 分钟 | 萨拉赫因伤缺席淘汰赛 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 萨拉赫的"最后一舞"效应 | 类似梅西 2022 的不可量化精神加成 | 部分 | 萨拉赫场上的投入度和创造力 |
| 高温天气利好北非球员 | 埃及球员对高温环境的适应力优于欧洲/大洋洲对手 | 是 | 比赛日气温 |
| G 组比利时的老化问题 | 比利时黄金一代落幕可能暴露弱点 | 是 | 比利时小组赛表现 |
| 伊朗的内部不稳定 | 伊朗足球的场外因素可能影响场上表现 | 部分 | 伊朗队新闻和状态 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: G 组成功出线
    type: precursor
    observable_proxy: G 组积分
    settlement_rule: 积分 ≥4
  - condition: 萨拉赫淘汰赛全程健康且状态世界级
    type: precursor
    observable_proxy: 萨拉赫淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥4
  - condition: 萨拉赫以外至少 2 名球员淘汰赛贡献进球
    type: precursor
    observable_proxy: 进球来源分布
    settlement_rule: 非萨拉赫球员淘汰赛合计进球 ≥3
  - condition: 淘汰赛至少击败一支欧洲前 10 球队
    type: branch
    observable_proxy: 淘汰赛 vs 欧洲强队赛果
    settlement_rule: 至少 1 场对欧洲前 10 的胜利
  - condition: 半决赛前避免遭遇西班牙或法国
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与西班牙/法国交手
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
| F-EGY-01 | 萨拉赫进攻输出 | precursor | 进球+助攻数 | 淘汰赛进球+助攻 ≥4 | public-football-knowledge |
| F-EGY-02 | 萨拉赫依赖度 | counter_signal | 萨拉赫进球占总进球比 | 非萨拉赫球员淘汰赛进球 ≥3 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 埃及是"萨拉赫依赖症"最严重的球队之一。
> 萨拉赫在国家队的成就远不及俱乐部（利物浦），这可能反映了球队整体支持的不足。
> 不进入 Factor Ledger 的原因：萨拉赫依赖度是结构性观察，需要赛 中数据验证。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 G 组第二名出线（击败新西兰，与伊朗竞争第二名），16 强赛面对另一个组的第一名。萨拉赫的个人能力和球队的防守组织在这一阶段可能制造惊喜。如果萨拉赫状态爆发且半区有利，1/4 决赛是可能达到的上限。

**最不可信叙事**: "萨拉赫一个人可以带埃及夺冠"——2022 世界杯已证明萨拉赫在国家队的表现远不如俱乐部，球队整体支持的不足限制了他的发挥。多次 AFCON 决赛失利也说明心理层面存在深层问题。

**最值得赛中监控的信号**: (1) vs 伊朗的赛果（决定出线命运的关键战）；(2) 萨拉赫的进球/助攻占比（过度依赖的危险信号）；(3) 萨拉赫的体能状态（每场跑动距离和下半场表现）。

**如果夺冠，哪些赛前判断有价值**: (1) 萨拉赫的"最后一舞"效应释放了不可量化的精神力量；(2) 多次 AFCON 决赛失利的痛苦反而淬炼出了不可动摇的心理韧性；(3) 北非球员在北美高温环境中的体能优势被严重低估。
