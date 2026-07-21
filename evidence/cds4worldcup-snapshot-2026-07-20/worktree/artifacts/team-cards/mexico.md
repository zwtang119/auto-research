# Championship Path Simulation Card: 墨西哥 (Mexico)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `mexico`

## 1. Team Profile

```yaml
team: 墨西哥 (Mexico)
team_slug: mexico
confederation: CONCACAF
group: A
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

墨西哥是 2026 世界杯的联合东道主之一，拥有部分主场优势。墨西哥足球以技术细腻和进攻激情著称，但长期存在"16 强魔咒"——连续七届世界杯止步 1/8 决赛（1994-2022）。A 组同组南非、韩国、捷克，四队实力相对接近，小组出线前景较好但头名争夺激烈。

## 2. Championship Thesis

> 如果墨西哥夺冠，最可能是因为作为东道主之一彻底打破了"16 强魔咒"的心理枷锁，球队在本土球迷的狂热支持下释放了前所未有的战斗力，且在北美高温环境中找到了最适合自己技术风格的比赛节奏——用东道主的便利完成了从"永远倒在 16 强"到"一路走到决赛"的心理跨越。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| "16 强魔咒"的心理枷锁 | psychological_pressure | 连续七届世界杯止步 1/8 决赛，这个记录本身就是最大的心理障碍 | 1/8 决赛的表现 |
| 与欧洲/南美顶级强队的硬实力差距 | base_strength_gap | 墨西哥球员虽然技术出色但缺乏世界级的个体爆发力 | vs 顶级对手的控球率和射门比 |
| 缺乏世界级射手 | low_scoring_dependency | 墨西哥长期缺乏稳定的赛季 20+ 级别中锋 | 中锋位置每 90 分钟进球数 |
| 防守端面对顶级攻击的脆弱性 | tactical_mismatch | 后防线在面对速度型和技术型攻击时经常暴露 | vs 强队的失球数 |
| A 组四队实力接近的消耗 | bracket_strength | 南非、韩国、捷克均为有竞争力的对手，小组赛消耗可能偏大 | A 组累计上场时间/黄牌数 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| A 组头名出线 | 小组赛 | 积分 ≥7 分或净胜球优势锁定第一 | 小组第二或第三出线 |
| 打破"16 强魔咒" | 1/8 决赛 | 1/8 决赛取胜晋级 1/4 决赛 | 连续第八届止步 1/8 决赛 |
| 找到稳定得分点 | 小组赛 | 场均进球 ≥1.5 | 小组赛场均进球 <1 |
| 淘汰赛面对欧美球队不崩盘 | 淘汰赛 | 面对欧美球队场面不失控 | 面对欧美球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 东道主主场优势 | 墨西哥作为联合东道主有部分主场便利 | 是 | 比赛场地和观众氛围 |
| 北美高温环境 | 墨西哥球员对北美气候的适应性优于欧洲球队 | 是 | 比赛日气温 |
| 打破魔咒后的心理释放 | 一旦越过 16 强，心理释放可能产生爆发效应 | 部分 | 1/4 决赛的表现 |
| 半区有利抽签 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 打破"16 强魔咒"晋级 1/4 决赛
    type: precursor
    observable_proxy: 1/8 决赛结果
    settlement_rule: 1/8 决赛取胜
  - condition: 找到稳定中锋且淘汰赛进球 ≥3
    type: precursor
    observable_proxy: 中锋淘汰赛进球数
    settlement_rule: 中锋淘汰赛进球 ≥3
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
| mx-host-advantage | 东道主主场优势 | precursor | 比赛场地是否在墨西哥境内及观众氛围 | 至少 3 场比赛在墨西哥境内进行 | public-football-knowledge |
| mx-round-of-16-curse | "16 强魔咒" | inhibitor | 1/8 决赛赛果 | 止步 1/8 决赛 = 因子激活 | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（2 条预测）

- 派别分布: 老球迷派, 黑马派
- Kimi 聚合概率: 0.67%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=35: "1986年17岁在阿兹特克见证墨西哥借高原主场杀进八强，这届所有小组赛都在家门口，+7500说明全世界低估东道主。"
- [黑马派] conf=58: "墨西哥所有小组赛都在阿兹特克主场，海拔2200米对手难适应，揭幕战主场气势加成巨大。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正小组对手（A 组: 南非/韩国/捷克），补充 §8，更新日期 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 A 组头名出线（凭借东道主优势和相对有利的小组赛程），16 强赛是关键——如果墨西哥能打破"16 强魔咒"，心理释放可能让球队在 1/4 决赛中超常发挥。东道主优势和北美气候适应是真实的物理加成。

**最不可信叙事**: "墨西哥作为东道主自动获得冠军竞争力"——东道主优势是真实的但不足以弥补与顶级强队之间的硬实力差距。A 组虽然不像死亡之组但捷克和韩国都是严肃的对手。

**最值得赛中监控的信号**: (1) 1/8 决赛的表现（是否能打破魔咒）；(2) 中锋位置的进球产出；(3) 面对欧美强队时的场面数据。

**如果夺冠，哪些赛前判断有价值**: (1) "16 强魔咒"一旦被打破，释放的心理能量可能比任何战术调整都重要；(2) 东道主之一的优势在 7 场赛制中被低估了；(3) 墨西哥的技术足球风格在北美高温环境中可能比预期更有效。
