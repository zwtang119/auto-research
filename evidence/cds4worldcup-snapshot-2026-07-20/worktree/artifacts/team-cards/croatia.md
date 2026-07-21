# Championship Path Simulation Card: 克罗地亚 (Croatia)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `croatia`

## 1. Team Profile

```yaml
team: 克罗地亚 (Croatia)
team_slug: croatia
confederation: UEFA
group: L
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

克罗地亚是 2018 世界杯亚军和 2022 世界杯季军，以极小的人口基数反复在世界大赛中超越预期。莫德里奇（Luka Modrić）的最后一届世界杯是全队的情感驱动力，科瓦契奇（Mateo Kovačić）、布罗佐维奇（Marcelo Brozović）等中场提供了坚实的控制力。L 组同组英格兰、加纳和巴拿马，英格兰是最大竞争对手但小组出线应无大问题。但核心阵容的老化是不可忽视的现实。

## 2. Championship Thesis

> 如果克罗地亚夺冠，最可能是因为莫德里奇的告别季释放了全队前所未有的情感凝聚力，中场三人组的技术和控制力在淘汰赛的高压环境中再次证明了韧性，且球队延续了加时赛和点球大战的"不死鸟"传统——用心理韧性弥补体能和阵容深度的不足。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 核心阵容严重老化 | base_strength_gap | 莫德里奇 40 岁，多名核心 30+，7 场高强度比赛体能不可持续 | 下半场跑动距离下降幅度 |
| 莫德里奇体能天花板 | injury_risk | 莫德里奇能否在淘汰赛全场保持影响力存在硬约束 | 莫德里奇淘汰赛出场时间和跑动距离 |
| 缺乏顶级射手 | low_scoring_dependency | 克罗地亚长期缺乏稳定进球的 9 号位，进攻端依赖中场后插上 | 前 3 场进球来源分布 |
| 加时赛/点球大战的体能消耗 | squad_depth | 克罗地亚依赖拖入加时/点球取胜，每多一场加时对老化阵容是巨大消耗 | 淘汰赛加时赛次数 |
| L 组英格兰的顶级竞争 | bracket_strength | 英格兰阵容深度和个体能力在 L 组碾压，克罗地亚大概率竞争小组第二 | L 组 vs 英格兰的场面数据 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 找到稳定得分手段 | 小组赛 | 场均进球 ≥1.5 且不全部来自中场 | 小组赛场均进球 <1 |
| 莫德里奇出场管理成功 | 小组赛 | 莫德里奇小组赛出场 ≤180 分钟且淘汰赛可满状态 | 淘汰赛莫德里奇明显体能不足 |
| 年轻球员（如苏契奇等）承担更多责任 | 小组赛 | 至少 1 名 U25 球员小组赛进球或助攻 ≥2 | U25 球员 0 贡献 |
| 避免 1/4 决赛前进入加时赛 | 淘汰赛 | 16 强赛 90 分钟内解决战斗 | 16 强赛即进入加时 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 莫德里奇告别战的情感凝聚力 | 不可量化的精神加成，可能让球队超越体能极限 | 部分 | 更衣室氛围和场上拼搏程度 |
| 半区有利避开顶级对手 | 利用经验和韧性淘汰二三档球队 | 是 | 淘汰赛对阵表 |
| 点球大战利瓦科维奇优势 | 利瓦科维奇（Livaković）是点球大战专家，2022 已验证 | 是 | 是否进入点球大战 |
| L 组低消耗出线 | 为老化阵容储备淘汰赛体能 | 是 | L 组积分和上场时间 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 莫德里奇淘汰赛至少 3 场首发且控制力在线
    type: precursor
    observable_proxy: 莫德里奇淘汰赛传球成功率和出场时间
    settlement_rule: 淘汰赛场均传球成功率 ≥88% 且出场 ≥3 场
  - condition: 找到至少 1 个稳定得分点
    type: precursor
    observable_proxy: 非中场球员的进球数
    settlement_rule: 非中场球员淘汰赛合计进球 ≥3
  - condition: 淘汰赛最多 1 场进入加时
    type: precursor
    observable_proxy: 淘汰赛加时赛场次
    settlement_rule: 淘汰赛加时赛 ≤1 场
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
| | | | | | |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（7 条预测）

- 派别分布: 心理抗压派, 老球迷派, 阵容年龄派, 黑马派
- Kimi 聚合概率: 2.33%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=50: "1976年帕年卡勺子点球掀翻德国时全世界也不看好我们，克罗地亚FIFA第10，莫德里奇最后一届东欧韧性被低估。"
- [老球迷派] conf=35: "1998苏克金靴到2018莫德里奇金球，我亲历格子军每一步。莫德里奇最后一舞必将点燃铁血防线。"
- [老球迷派] conf=30: "1974拉托13球摘铜、1982博涅克闪耀，波兰黄金一代钢铁意志在克罗地亚延续。"
- [老球迷派] conf=20: "莫德里奇40岁第五次出征绝唱，FIFA排名10的格子军遇上最轻松L组，南斯拉夫足球最壮丽的谢幕。"
- [黑马派] conf=38: "FIFA第10连续两届大赛进前三，莫德里奇最后一舞+最轻松小组配置，大赛韧性被赔率低估。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 L 组第二出线（英格兰大概率头名），小组赛管理莫德里奇出场时间。16 强赛依靠中场控制力和利瓦科维奇的稳定性过关。1/4 决赛再次拖入加时或点球——这是克罗地亚最擅长的赢球模式。如果半区有利，莫德里奇告别战可能在半决赛创造最后的奇迹。

**最不可信叙事**: "克罗地亚的韧性可以无限次超越体能极限"——7 场高强度比赛中，老化的核心阵容至少会在某一场达到物理极限。

**最值得赛中监控的信号**: (1) 莫德里奇的下半场跑动距离和传球成功率；（2）全队加时赛/点球大战的次数和体能消耗；(3) 非 midfield 进球数（反映是否找到稳定的锋线输出）。

**如果夺冠，哪些赛前判断有价值**: (1) 莫德里奇最后一届世界杯的情感驱动力是本届赛事中最不可量化但可能最强大的变量；(2) 克罗地亚的大赛淘汰赛经验在 48 队赛制中可能被低估；(3) 点球大战的利瓦科维奇是淘汰赛阶段最被低估的门将。
