# Championship Path Simulation Card: 科特迪瓦 (Côte d'Ivoire)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `côte-divoire`

## 1. Team Profile

```yaml
team: 科特迪瓦 (Côte d'Ivoire)
team_slug: côte-divoire
confederation: CAF
group: E
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

科特迪瓦是 2023 年非洲杯冠军（本土夺冠），这是继 2015 年之后的第二座 AFCON 奖杯。虽然德罗巴时代的黄金一代已远去，但新一代球员如塞巴斯蒂安·阿莱（Sébastien Haller）、弗兰克·凯西（Franck Kessié）和尼古拉·佩佩（Nicolas Pépé）在欧洲顶级联赛有丰富经验。主帅埃默斯·法埃（Emerse Faé）在 2023 AFCON 上临时接手并率队夺冠，证明了出色的更衣室管理能力。E 组同组德国、库拉索和厄瓜多尔，出线需与厄瓜多尔竞争。

## 2. Championship Thesis

> 如果科特迪瓦夺冠，最可能是因为 2023 AFCON 本土夺冠的信心惯性在世界杯舞台上释放，凯西在中场提供了攻防两端的世界级输出，且非洲球员的身体素质在高温淘汰赛中形成了结构性优势——速度和力量在北美夏季成为不可阻挡的武器。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与德国的实力差距 | base_strength_gap | 德国是 E 组明显实力最强的球队，科特迪瓦面对顶级对手时的系统性弱点可能暴露 | vs 德国的控球率和场面表现 |
| 进攻端缺乏稳定终结者 | low_scoring_dependency | 阿莱虽有大赛进球但效率不稳定，佩佩在阿森纳后已远离巅峰 | 中锋位置每 90 分钟进球数 |
| 非洲球队在世界杯淘汰赛的历史天花板 | psychological_pressure | 非洲球队从未进入世界杯半决赛，这一历史包袱在关键场次可能产生影响 | 淘汰赛面对欧洲/南美球队时的场面控制力 |
| 阵容深度不足 | squad_depth | 首发 11 人有一定竞争力但替补席差距明显 | 替补上场后的技术统计落差 |
| 厄瓜多尔的身体对抗和体能 | tactical_mismatch | 厄瓜多尔球员多数适应高原比赛，体能储备可能优于科特迪瓦 | vs 厄瓜多尔的对抗成功率 |
| 战术纪律性波动 | tactical_mismatch | 非洲球队在面对严密战术体系时容易出现阵型散乱 | 面对战术纪律好的球队时的失球数 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| E 组至少第二名出线 | 小组赛 | 积分 ≥4 | 小组未出线 |
| 击败厄瓜多尔锁定出线名额 | 小组赛 | vs 厄瓜多尔至少 1 分 | 负厄瓜多尔 |
| 凯西或核心中场在淘汰赛爆发 | 淘汰赛 | 至少 1 场淘汰赛进球+助攻 ≥1 | 核心中场淘汰赛 0 贡献 |
| 防守端在淘汰赛保持组织纪律 | 淘汰赛 | 淘汰赛场均失球 ≤1 | 淘汰赛场均失球 >2 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 2023 AFCON 冠军的信心惯性 | 本土夺冠的经历可能在世界杯中转化为额外的心理韧性 | 部分 | 关键场次的场面反应 |
| 北美高温利好非洲球员体能 | 科特迪瓦球员的身体素质在高温环境中可能优于欧洲对手 | 是 | 比赛日气温和下半场表现 |
| 德国轻敌 | 德国可能在 E 组轻视非洲对手 | 是 | 德国 vs 科特迪瓦的首发阵容 |
| E 组其他对手互相消耗 | 厄瓜多尔与德国的对抗可能为科特迪瓦创造出线窗口 | 是 | E 组积分分布 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: E 组成功出线（至少第二名）
    type: precursor
    observable_proxy: E 组积分
    settlement_rule: 积分 ≥4
  - condition: 凯西全程健康且中场输出世界级
    type: precursor
    observable_proxy: 凯西淘汰赛传球和抢断数据
    settlement_rule: 淘汰赛场均传球成功率 ≥85%
  - condition: 前锋线找到稳定终结
    type: precursor
    observable_proxy: 前锋淘汰赛进球数
    settlement_rule: 淘汰赛合计进球 ≥4
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
| F-CIV-01 | 凯西中场输出 | precursor | 传球成功率+抢断数 | 淘汰赛场均传球成功率 ≥85% | public-football-knowledge |
| F-CIV-02 | 前锋终结效率 | precursor | 前锋 xG 转化率 | 淘汰赛 xG 转化率 ≥40% | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 科特迪瓦 2023 AFCON 本土夺冠是重要的信心信号。
> 法埃的更衣室管理能力在大赛中可能是隐性优势。
> 不进入 Factor Ledger 的原因：更衣室管理能力难以用可判定代理量化。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 E 组第二名出线（击败库拉索，与厄瓜多尔竞争第二名），16 强赛面对另一个组的第一名或第二名。科特迪瓦的身体素质和 AFCON 冠军的信心在这一阶段可能制造惊喜。1/8 决赛或 1/4 决赛是合理上限。

**最不可信叙事**: "科特迪瓦已经具备与欧洲顶级强队系统性抗衡的实力"——2023 AFCON 虽然夺冠但过程并不稳定，世界杯面对德国级别的对手时结构性弱点可能暴露。

**最值得赛中监控的信号**: (1) vs 厄瓜多尔的赛果（决定出线命运的关键战）；(2) 凯西的中场控制数据；(3) 防守端的组织纪律性（面对高压逼抢时的失误率）。

**如果夺冠，哪些赛前判断有价值**: (1) 2023 AFCON 冠军的信心惯性是真实的且可迁移的；(2) 非洲球员的身体素质在北美夏季高温中形成了结构性优势；(3) 法埃的更衣室管理能力在大赛中被严重低估。
