# Championship Path Simulation Card: 西班牙 (Spain)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `spain`

## 1. Team Profile

```yaml
team: 西班牙 (Spain)
team_slug: spain
confederation: UEFA
group: H
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - high_kimi_probability
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: [kimi-aggregation]
  red_sources: [kimi-300-agent-reasons]
  coverage: sufficient
```

西班牙是 2024 欧洲杯冠军、2023 欧国联冠军，FIFA 世界排名第 1。德拉富恩特治下完成了从 tiki-taka 到高位压迫+快速转换的战术进化。亚马尔（Lamine Yamal）、佩德里（Pedri）、尼科·威廉姆斯（Nico Williams）组成的新生代攻击线是当前国际足坛最具创造力的三角之一。H 组同组有乌拉圭、沙特阿拉伯和佛得角，小组出线几乎无悬念，但乌拉圭的高强度压迫可能成为小组赛的实质挑战。

## 2. Championship Thesis

> 如果西班牙夺冠，最可能是因为德拉富恩特的传控-压迫混合体系在高温淘汰赛中持续消耗对手，亚马尔-佩德里中场三角提供不可阻挡的进攻创造力，且 2024 欧洲杯冠军的信心惯性使球队在关键淘汰赛时刻保持冷静，H 组的平稳出线为淘汰赛阶段储备了充足的体能和战术调试空间。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 正印中锋终结效率 | low_scoring_dependency | 莫拉塔之后缺乏稳定 9 号位，面对低位防守时进攻创造力无法转化为进球 | 中锋位置每 90 分钟进球数 |
| 亚马尔腿筋伤病风险 | injury_risk | 亚马尔 2024-25 赛季多次腿筋问题，核心边路爆点不可替代 | 亚马尔赛前体能报告/出场时间 |
| 淘汰赛遭遇低位铁桶 | tactical_mismatch | 西班牙对深度防守的破解能力有限，2022 世界杯负日本即为例证 | 面对低位防守球队时 xG 转化率 |
| 半区可能提前遭遇法国/英格兰/德国 | favorite_collision | 夺冠路径上可能在 1/4 决赛或半决赛遇到同级别对手 | 淘汰赛对阵表 |
| 北美高温环境体能消耗 | travel_fatigue | 西班牙球员多数来自温和气候联赛，北美夏季高温可能影响传控体系持续性 | 比赛下半场跑动距离下降幅度 |
| H 组乌拉圭的高强度压迫测试 | bracket_strength | 乌拉圭贝尔萨体系的高强度压迫是小组赛唯一的实质检验 | vs 乌拉圭的控球率和射门比 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 确立稳定 9 号位方案 | 小组赛 | 至少一名中锋在 3 场小组赛中贡献 2+ 进球或关键助攻 | 小组赛结束中锋 0 球 |
| 亚马尔全程健康 | 全赛程 | 无腿筋相关缺席，淘汰赛每场出场 ≥60 分钟 | 亚马尔因伤缺席任何淘汰赛 |
| 破解低位防守能力验证 | 淘汰赛首场 | 面对低位防守球队至少打入 2 球 | 被低位防守限制为 0-1 球 |
| H 组以头名出线 | 小组赛 | 积分 ≥7 分或净胜球优势锁定第一 | 小组第二出线 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 半区强队提前出局 | 降低淘汰赛路径难度，避免提前遭遇法国/英格兰/德国 | 是 | 关注其他组淘汰赛结果 |
| VAR 判罚有利于高位压迫方 | 西班牙高位压迫造犯规和越位的战术获益 | 是 | 关键场次 VAR 判罚统计 |
| 高温天气放大传控优势 | 技术型球队在高温下体能管理优于跑动型球队 | 是 | 比赛日气温和湿度 |
| 乌拉圭小组赛消耗过大 | H 组唯一强敌提前耗尽体能，淘汰赛阶段竞争力下降 | 是 | 乌拉圭小组赛伤病/黄牌情况 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 3
conditions:
  - condition: 亚马尔全程健康且淘汰赛状态在线
    type: precursor
    observable_proxy: 亚马尔淘汰赛出场时间及关键传球数
    settlement_rule: 淘汰赛阶段无因伤缺席且场均关键传球 ≥2
  - condition: 中锋位置提供稳定终结输出
    type: precursor
    observable_proxy: 中锋位置球员淘汰赛进球数
    settlement_rule: 淘汰赛阶段中锋合计进球 ≥3
  - condition: 半决赛前避免遭遇法国
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法国交手
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
| F-ESP-01 | 亚马尔健康状况 | precursor | 亚马尔出场时间/伤病报告 | 淘汰赛全程无因伤缺席 | public-football-knowledge |
| F-ESP-02 | 中锋终结效率 | precursor | 中锋位置 xG 转化率 | 淘汰赛 xG 转化率 ≥40% | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（62 条预测）

- 派别分布: 主帅视角派, 伤病赛程派, 建模派, 心理抗压派, 数据派, 玄学派, 老球迷派, 赔率派, 阵容年龄派
- Kimi 聚合概率: 20.67%

#### 代表性 reason（前 5 条）

- [数据派] conf=78: "西班牙自2024年3月以来保持不败，FIFA世界排名第1，2024欧洲杯冠军，亚马尔2.33亿欧领衔的xG数据统治力被赔率低估。"
- [数据派] conf=78: "西班牙进攻三区传球成功率欧洲最高，亚马尔+佩德里+祖比门迪的技术三角在高压下控球稳定性最佳。"
- [数据派] conf=78: "西班牙传球网络完成率与战术执行力在所有强队中最稳定，FIFA排名第1实至名归。"
- [数据派] conf=65: "日本三笘薰缺席削弱边路，西班牙阵容深度最佳，且亚马尔腿筋伤势恢复乐观。"
- [数据派] conf=78: "西班牙自2024年3月不败的防守组织力被赔率低估，零封率在欧洲杯期间高达67%。"

> [!memo] 2026-06-13 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正组别为 H 组（乌拉圭/沙特/佛得角），更新对手分析，填充 §8 | WI-0.2 组别校正 |

## 11. Current Interpretation

**最可信路径**: 以 H 组头名出线（凭实力碾压沙特和佛得角，与乌拉圭的比赛决定头名归属），16 强赛面对相对较弱的第三名球队，8 强赛开始展现 2024 欧洲杯级别的统治力。德拉富恩特的体系在高温环境下通过控球降低比赛节奏，亚马尔和尼科·威廉姆斯的边路突击在淘汰赛阶段逐渐加码，半决赛和决赛中中场控制力成为决定性优势。

**最不可信叙事**: "西班牙传控美学自然碾压一切"——2022 世界杯小组赛负日本已证明控球率不等于胜利。H 组虽然出线无忧，但淘汰赛遭遇低位防守型球队时可能重蹈覆辙。

**最值得赛中监控的信号**: (1) 亚马尔每场出场时间和腿筋相关动作；(2) 中锋位置的进球产出和 xG 转化率；(3) 面对低位防守时的控球射门比（控球率高但射门少的危险信号）。

**如果夺冠，哪些赛前判断有价值**: (1) H 组的平稳出线为淘汰赛储备了体能和战术调试空间——轻松小组赛并非坏事；(2) 德拉富恩特体系是 2024-2026 周期最稳定的战术框架；(3) 西班牙新生代（亚马尔、佩德里、尼科）是本届赛事最强的 U23 核心组合。
