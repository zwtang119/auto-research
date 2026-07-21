# Championship Path Simulation Card: 乌拉圭 (Uruguay)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `uruguay`

## 1. Team Profile

```yaml
team: 乌拉圭 (Uruguay)
team_slug: uruguay
confederation: CONMEBOL
group: H
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
  coverage: partial
```

乌拉圭是两届世界杯冠军（1930、1950），贝尔萨（Marcelo Bielsa）执教以来注入了标志性的高强度压迫和体能足球。巴尔韦德（Federico Valverde）是世界级的中场发动机，努涅斯（Darwin Núñez）虽终结效率波动但跑动和压迫能力极强。H 组签运尚可，小组出线有一定把握。

## 2. Championship Thesis

> 如果乌拉圭夺冠，最可能是因为贝尔萨的高强度压迫体系在淘汰赛阶段让所有对手陷入体能地狱，巴尔韦德在中场提供了攻防两端的世界级输出，且努涅斯在关键场次中终于将无限跑动转化为稳定进球——贝尔萨的足球哲学在 7 场赛制中找到了终极验证。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 贝尔萨体系的体能可持续性 | squad_depth | 高强度压迫在 7 场赛制中是否可持续是最大的物理限制 | 第 4 场起全队跑动距离下降幅度 |
| 努涅斯终结效率的不稳定性 | low_scoring_dependency | 努涅斯创造了大量机会但转化率波动极大 | 努涅斯 xG vs 实际进球差 |
| 阵容深度不足以支撑 7 场高强度比赛 | squad_depth | 贝尔萨体系要求极高跑动量，替补水平不足以维持同等强度 | 替补上场后跑动强度和战术执行差距 |
| 缺乏世界级中卫 | base_strength_gap | 后防线缺乏在顶级联赛已验证的世界级中卫 | 场均失球和对抗成功率 |
| 淘汰赛面对技术型球队的控制力不足 | tactical_mismatch | 贝尔萨的压迫体系面对传控型球队（西班牙）可能被消耗 | vs 传控球队的控球率和射门比 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 努涅斯找到稳定终结 | 小组赛 | 小组赛进球 ≥2 且 xG 转化率 ≥50% | 小组赛大量机会但 0-1 球 |
| H 组头名出线 | 小组赛 | 积分 ≥7 且净胜球优势 | 小组第二或第三出线 |
| 贝尔萨体系在第 4 场后仍保持高强度 | 淘汰赛 | 16 强赛全队跑动距离 ≥110km | 跑动距离下降至 <105km |
| 巴尔韦德淘汰赛输出验证 | 淘汰赛 | 淘汰赛进球+助攻 ≥2 | 巴尔韦德淘汰赛 0 球 0 助攻 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| H 组低消耗出线 | 为高强度淘汰赛储备体能 | 是 | H 组积分和上场时间 |
| 努涅斯在关键场次超常发挥 | 努涅斯的波动性意味着他在某几场可能爆发 | 是 | 努涅斯单场进球数 |
| 半区有利抽签 | 避免淘汰赛过早遭遇传控型球队 | 是 | 淘汰赛对阵表 |
| 高温天气中贝尔萨体系对手更快耗尽体能 | 高强度压迫在高温下对防守方消耗更大 | 是 | 比赛日气温 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 贝尔萨体系在淘汰赛 4+ 场中保持体能强度
    type: precursor
    observable_proxy: 淘汰赛全队跑动距离
    settlement_rule: 淘汰赛场均跑动距离 ≥108km
  - condition: 努涅斯淘汰赛进球效率稳定
    type: precursor
    observable_proxy: 努涅斯淘汰赛 xG 转化率
    settlement_rule: 淘汰赛 xG 转化率 ≥50%
  - condition: 巴尔韦德全程健康且输出世界级
    type: precursor
    observable_proxy: 巴尔韦德淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥2
  - condition: 半决赛前避免遭遇西班牙
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与西班牙交手
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
| F-URU-01 | 努涅斯终结效率 | precursor | 努涅斯 xG 转化率 | 淘汰赛 xG 转化率 ≥50% | public-football-knowledge |
| F-URU-02 | 巴尔韦德中场输出 | precursor | 巴尔韦德淘汰赛进球+助攻 | 淘汰赛进球+助攻 ≥2 | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（2 条预测）

- 派别分布: 老球迷派, 黑马派
- Kimi 聚合概率: 0.67%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=30: "1950马拉卡纳父亲见证天蓝军团踩碎巴西冠军梦，七十六年轮回。H组出线后轻装上阵，民族血性不在乎排名。"
- [黑马派] conf=48: "乌拉圭赔率+6500隐含仅1.5%，FIFA第10却与西班牙同组被极度看衰。南美球队美洲作战自带气候适应优势。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 确认 H 组（西班牙/沙特/佛得角），填充 §8，日期更新 | WI-0.2 校正 |

## 11. Current Interpretation

**最可信路径**: 以 H 组头名出线，小组赛通过高强度压迫碾压实力不如自己的对手。16 强赛继续依靠体能和压迫优势过关。1/4 决赛是体能的转折点——如果贝尔萨的体系在第 4 场后仍保持强度，乌拉圭可能在半决赛中创造惊喜。

**最不可信叙事**: "贝尔萨的哲学最终将在世界杯得到正名"——7 场赛制是贝尔萨体系的物理极限测试，历史上贝尔萨的球队在长赛制中从未走到最后。

**最值得赛中监控的信号**: (1) 全队跑动距离随赛程推进的变化趋势；(2) 努涅斯的 xG 转化率；(3) 巴尔韦德的中场控制数据。

**如果夺冠，哪些赛前判断有价值**: (1) 贝尔萨的高强度压迫在高温淘汰赛中可能比预期更有效——因为对手的消耗更快；(2) 巴尔韦德是本届赛事中最被低估的全能中场；(3) 努涅斯的波动性意味着他的"爆发场次"可能恰好落在关键的淘汰赛。
