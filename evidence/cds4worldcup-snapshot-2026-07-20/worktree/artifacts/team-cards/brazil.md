# Championship Path Simulation Card: 巴西 (Brazil)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `brazil`

## 1. Team Profile

```yaml
team: 巴西 (Brazil)
team_slug: brazil
confederation: CONMEBOL
group: C
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - kimi_longshot
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: [kimi-aggregation]
  red_sources: [kimi-300-agent-reasons]
  coverage: sufficient
```

巴西是五届世界杯冠军，但自 2002 年后再未夺冠，近两届分别止步 1/4 决赛（2018、2022）。维尼修斯（Vinícius Jr）、罗德里戈（Rodrygo）领衔的攻击线拥有顶级个体能力，但近年来防守组织和战术纪律性持续下滑。C 组同组摩洛哥、海地、苏格兰，签运极为有利，小组头名出线几无悬念。

## 2. Championship Thesis

> 如果巴西夺冠，最可能是因为维尼修斯的个体爆破能力在淘汰赛阶段无法被战术限制，球队在防守端找到了被长期缺失的组织纪律性——用结构化的防守框架释放前场的自由度，且 C 组的温和签运为淘汰赛储备了体能和信心。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 防守组织和战术纪律性 | tactical_mismatch | 巴西近年来在关键场次中防守松散，缺乏系统的防守训练和执行 | 场均失球数和定位球失球数 |
| 中场控制力不足 | base_strength_gap | 缺乏一个世界级的控球型中场（卡塞米罗老化，替代者未验证） | 中场控球率和对抗成功率 |
| 内马尔伤病/状态不确定性 | injury_risk | 内马尔长期伤病困扰，能否在 2026 保持健康和竞技状态存疑 | 内马尔赛前赛季出场时间和进球率 |
| 关键淘汰赛的心理脆弱 | psychological_pressure | 2014 半决赛 1-7 和 2022 点球负克罗地亚的创伤可能仍有残留 | 淘汰赛关键时刻（落后/点球大战）表现 |
| 缺乏稳定的中锋选项 | low_scoring_dependency | 维尼修斯和罗德里戈更适合边路，中锋位置缺乏赛季 20+ 级别射手 | 中锋位置每 90 分钟进球数 |
| 淘汰赛可能遭遇欧洲顶级队 | favorite_collision | 夺冠路径上可能在 1/4 决赛或半决赛遇到同级别对手 | 淘汰赛对阵表 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 防守体系建立且有效 | 小组赛 | 小组赛场均失球 ≤1 且至少 1 场零封 | 小组赛失球 ≥4 |
| 维尼修斯淘汰赛个体爆破验证 | 淘汰赛 | 淘汰赛阶段至少 2 球或 3 助攻 | 维尼修斯被限制且无进攻贡献 |
| 中场控制力提升 | 全赛程 | 中场对抗成功率 ≥50% | 中场对抗成功率 <45% |
| 克服淘汰赛心理障碍 | 1/4 决赛 | 1/4 决赛过关（近两届均止步于此） | 连续第三届止步 1/4 决赛 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 内马尔健康回归且状态爆发 | 释放前场第三维度，使维尼修斯获得更多空间 | 是 | 内马尔赛季末伤病报告 |
| 半区有利避开欧洲顶级队 | 避免在淘汰赛过早遭遇法国/西班牙/英格兰 | 是 | 淘汰赛对阵表 |
| 阿根廷提前出局 | 降低南美德比压力和媒体焦点 | 是 | 阿根廷淘汰赛进度 |
| 巴西球迷大规模到场 | 北美有大量巴西裔社区，主场氛围加成 | 是 | 球场观众构成 |
| C 组极低消耗出线 | 摩洛哥是唯一严肃对手，海地和苏格兰预计可控 | 是 | C 组积分和消耗 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 3
conditions:
  - condition: 防守体系在淘汰赛阶段场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛场均失球
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 维尼修斯淘汰赛全程健康且状态在线
    type: precursor
    observable_proxy: 维尼修斯淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥3
  - condition: 半决赛前避免遭遇法国或西班牙
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
| br-vini-output | 维尼修斯进攻产出 | precursor | 维尼修斯淘汰赛进球+助攻 | 淘汰赛进球+助攻 ≥3 | public-football-knowledge |
| br-defense-organization | 防守组织纪律性 | inhibitor | 场均失球和定位球失球数 | 场均失球 ≥1.5 = 因子激活 | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（11 条预测）

- 派别分布: 主帅视角派, 伤病赛程派, 建模派, 玄学派, 老球迷派, 赔率派, 阵容年龄派
- Kimi 聚合概率: 3.67%

#### 代表性 reason（前 5 条）

- [赔率派] conf=58: "东京投注站巴西占总注额35%，远高于欧洲平均18%，但欧洲庄家+800更客观，价值在跟欧洲市场。"
- [赔率派] conf=65: "平台巴西投注占总流水47%，本土彩民用真金白银投票，维尼修斯174M+安切洛蒂执教。"
- [赔率派] conf=55: "感受度假地实时投注情绪，巴西+800在拉美游客中投注单堆积如山。"
- [老球迷派] conf=60: "2002罗纳尔多捧起第五颗星，整条街跳桑巴。维尼修斯1.74亿欧新头牌，等24年该绣第六颗了。"
- [玄学派] conf=55: "木星2025年6月入双子座，象征双翼齐飞，巴西维尼修斯+拉菲尼亚边路双子星得木星加持。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正小组对手（C 组: 摩洛哥/海地/苏格兰），补充 §8，更新日期 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 C 组头名低消耗出线（摩洛哥是唯一严肃对手，海地和苏格兰预计可控），16 强赛和 1/4 决赛依靠维尼修斯的个体能力解决战斗，这是巴西最可靠的赢球模式。如果防守端意外地建立了组织纪律性（这是最大的不确定性），巴西在半决赛和决赛中的个体天赋足以对抗任何对手。

**最不可信叙事**: "五星巴西的天赋自动转化为冠军"——自 2002 年以来，天赋不等于冠军已反复被验证。防守纪律性的缺失是结构性问题。但 C 组的温和签运确实为巴西提供了近年来最有利的淘汰赛起点。

**最值得赛中监控的信号**: (1) 防守组织的纪律性（场均失球、定位球失球）；(2) 维尼修斯的被犯规次数和过人成功率；(3) 中场对抗成功率（反映中场控制力的真实水平）。

**如果夺冠，哪些赛前判断有价值**: (1) 巴西的问题从来不是天赋而是纪律，如果解决了纪律问题天赋就会自动释放；(2) 维尼修斯是当前国际足坛淘汰赛阶段最具破坏力的个体之一；(3) C 组的温和签运是巴西近年来最有利的世界杯分组，低消耗出线的体能优势在淘汰赛中可能被放大。
