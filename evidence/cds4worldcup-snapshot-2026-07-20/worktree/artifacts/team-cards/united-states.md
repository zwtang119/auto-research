# Championship Path Simulation Card: 美国 (United States)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `united-states`

## 1. Team Profile

```yaml
team: 美国 (United States)
team_slug: united-states
confederation: CONCACAF
group: D
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

美国是 2026 世界杯的联合东道主之一，拥有完整的"主场"优势——比赛场地、气候适应、球迷支持。普利西奇（Christian Pulisic）在 AC 米兰表现出色，麦肯尼（Weston McKennie）、雷纳（Giovanni Reyna）等球员在欧洲顶级联赛效力。球队的技术水平在 CONCACAF 中领先，2022 世界杯 16 强赛虽然出局但积累了经验。D 组同组巴拉圭、澳大利亚、土耳其，小组出线机会较好。

## 2. Championship Thesis

> 如果美国夺冠，最可能是因为东道主优势（场地、气候、球迷、旅行便利）在 7 场赛制中被放大到了极致，普利西奇在淘汰赛阶段爆发了职业生涯最佳表现，且 D 组相对温和的小组赛为淘汰赛储备了体能和信心——用主场氛围和运动天赋弥补了与欧洲顶级球队之间的技术差距。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与欧洲/南美顶级强队的硬实力差距 | base_strength_gap | 核心球员虽然效力于欧洲联赛但非世界级，整体实力有天花板 | vs 顶级对手的控球率和射门比 |
| 缺乏世界级射手 | low_scoring_dependency | 美国始终缺乏一个赛季 20+ 级别的稳定中锋 | 中锋位置每 90 分钟进球数 |
| 大赛淘汰赛经验不足 | psychological_pressure | 美国的世界杯淘汰赛战绩有限，关键场次可能紧张 | 淘汰赛首场表现 |
| D 组土耳其和澳大利亚的竞争 | bracket_strength | 土耳其和澳大利亚都是有竞争力的对手，小组出线并非毫无风险 | D 组积分 |
| 防守端面对顶级攻击的不稳定性 | tactical_mismatch | 后防线缺乏在顶级联赛已验证的世界级中卫 | vs 强队的失球数 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| D 组头名出线 | 小组赛 | 积分 ≥7 且不败 | D 组第二或第三出线 |
| 普利西奇淘汰赛进攻输出验证 | 淘汰赛 | 淘汰赛阶段进球+助攻 ≥2 | 普利西奇被限制且无贡献 |
| 防守端至少 2 场零封 | 全赛程 | 至少 2 场不失球 | 场场失球 |
| 淘汰赛击败一支欧洲或南美球队 | 淘汰赛 | 面对非 CONCACAF 球队取胜 | 面对欧美球队场面被动且输球 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 东道主优势（场地+气候+球迷） | 7 场赛制中东道主优势的累积效应不可低估 | 是 | 比赛场地、观众人数和氛围 |
| D 组签运有利 | 巴拉圭、澳大利亚、土耳其均为非顶级对手，小组赛消耗可控 | 是 | D 组积分分布 |
| 半区有利抽签 | 东道主可能在抽签中获得有利位置 | 是 | 淘汰赛对阵表 |
| 普利西奇在主场爆发 | 普利西奇在国家队的表现经常优于俱乐部 | 是 | 普利西奇国家队 vs 俱乐部进球率 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 东道主优势在淘汰赛阶段持续发挥作用
    type: precursor
    observable_proxy: 比赛场地和观众氛围
    settlement_rule: 淘汰赛全部在本土进行且观众支持明显
  - condition: 普利西奇淘汰赛进球+助攻 ≥3
    type: precursor
    observable_proxy: 普利西奇淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥3
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 半决赛前避免遭遇法国或阿根廷
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法国/阿根廷交手
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
| us-host-advantage | 东道主主场优势 | precursor | 比赛是否在美国境内进行及观众氛围 | 至少 3 场比赛在美国境内进行 | public-football-knowledge |
| us-pulisic-output | 普利西奇进攻输出 | precursor | 进球+助攻+关键传球 | 淘汰赛进球+助攻 ≥2 | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（3 条预测）

- 派别分布: 主帅视角派, 老球迷派, 赔率派
- Kimi 聚合概率: 1.00%

#### 代表性 reason（前 5 条）

- [赔率派] conf=30: "美国+6500隐含1.5%被严重低估，所有小组赛本土进行，北美首次联合办赛主场氛围决定性。"
- [老球迷派] conf=30: "1994美国世界杯开启了我的足球人生，东道主优势不可低估，D组对手均无夺冠经验。"
- [主帅视角派] conf=35: "东道主备战优势不可低估，D组对手均无夺冠经验，48队扩军增大容错率。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正小组对手（D 组: 巴拉圭/澳大利亚/土耳其），补充 §8，更新日期 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 D 组头名出线（利用东道主优势和相对有利的签运），16 强赛面对第三名球队。普利西奇的个体能力和东道主氛围在这一阶段可能制造惊喜。1/4 决赛是真实天花板——面对欧洲或南美顶级球队时硬实力差距可能暴露。

**最不可信叙事**: "东道主优势可以弥补一切实力差距"——2002 韩国的四强是东道主优势的极限案例，美国不具备同等的竞技基础。但 D 组的签运确实比预期的有利。

**最值得赛中监控的信号**: (1) D 组出线过程和消耗（特别是 vs 土耳其和澳大利亚的场面）；(2) 普利西奇的淘汰赛进攻输出；(3) 面对欧美强队时的场面数据（控球率和射门比）。

**如果夺冠，哪些赛前判断有价值**: (1) 东道主优势在 7 场赛制中的累积效应是所有变量中最不可量化的；(2) 普利西奇在国家队的表现经常超越其在俱乐部的水平；(3) D 组的温和签运为美国提供了近年来最有利的世界杯起点。
