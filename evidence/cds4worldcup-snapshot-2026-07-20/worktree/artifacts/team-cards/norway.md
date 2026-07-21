# Championship Path Simulation Card: 挪威 (Norway)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `norway`

## 1. Team Profile

```yaml
team: 挪威 (Norway)
team_slug: norway
confederation: UEFA
group: I
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

挪威拥有当今足坛最具破坏力的中锋哈兰德（Erling Haaland）和顶级组织中场厄德高（Martin Ødegaard），这对双人组合在任何球队都足以构成夺冠核心。但自 1998 年以来挪威首次重返世界杯，整体阵容深度和大赛经验与顶级强队存在显著差距。I 组同组法国和塞内加尔，小组出线竞争激烈但并非不可能。

## 2. Championship Thesis

> 如果挪威夺冠，最可能是因为哈兰德在 7 场比赛中贡献了至少 8 球的历史级个人表演，厄德高在中场提供了世界级的创造力支撑，且球队围绕这对双核构建了一套极致高效的防守反击体系——在 2026 世界杯的高温和多旅行赛制中，简洁直接的比赛风格反而成为优势。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 阵容深度严重不足 | squad_depth | 哈兰德和厄德高之外，缺乏同等水平的第三、第四选择 | 首发与替补的技术统计差距 |
| 大赛经验匮乏 | psychological_pressure | 自 1998 年以来未参加世界杯，全队几乎没有淘汰赛级别的大赛经验 | 首场世界杯的表现（紧张程度/失误率） |
| 哈兰德被针对性限制 | tactical_mismatch | 对手可能用三中卫体系+专人盯防完全封锁哈兰德的射门空间 | 哈兰德每场射门数和触球次数 |
| 中场防守硬度不足 | base_strength_gap | 厄德高偏重进攻组织，中场防守端缺乏世界级拦截者 | 对手中路进攻成功率 |
| 淘汰赛遭遇顶级球队的硬实力差距 | base_strength_gap | 即使小组出线，淘汰赛面对法国/西班牙级别的对手时阵容差距明显 | 淘汰赛 vs 顶级对手的场面数据 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 哈兰德小组赛进球效率验证 | 小组赛 | 小组赛进球 ≥3 | 小组赛 0-1 球 |
| 厄德高创造力不受高压限制 | 小组赛 | 场均关键传球 ≥2.5 | 被限制为关键传球 <1.5 |
| 找到哈兰德-厄德高之外的第三得分点 | 小组赛 | 至少 1 名其他球员小组赛进球 ≥1 | 全队进球 100% 来自哈兰德 |
| 防守反击体系在淘汰赛有效 | 淘汰赛 | 淘汰赛首场至少打入 2 球且不失球 | 淘汰赛首场被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| I 组对手整体实力不一 | 小组赛低消耗出线可能性存在但法国是硬骨头 | 是 | I 组积分分布 |
| 哈兰德状态爆发 | 哈兰德在赛季末可能达到体能和状态巅峰 | 是 | 哈兰德赛前进球率 |
| 半区抽签有利 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |
| 高温天气利好简洁直接风格 | 挪威的防守反击不需要大量跑动，高温下体能优势 | 是 | 比赛日气温 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 哈兰德淘汰赛进球 ≥5
    type: precursor
    observable_proxy: 哈兰德淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥5
  - condition: 厄德高全程健康且创造力在线
    type: precursor
    observable_proxy: 厄德高淘汰赛关键传球数
    settlement_rule: 淘汰赛场均关键传球 ≥2.5
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
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
| | | | | | |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（12 条预测）

- 派别分布: 数据派, 老球迷派, 赔率派, 阵容年龄派, 黑马派
- Kimi 聚合概率: 4.00%

#### 代表性 reason（前 5 条）

- [数据派] conf=35: "哈兰德2.33亿欧本赛季状态火热，厄德高伤愈回归，挪威预选双杀意大利证明防守硬度。"
- [赔率派] conf=35: "挪威+3000隐含仅3.2%，但哈兰德2.33亿欧状态火热，北欧球员适应北美温带气候，回报风险比极具吸引力。"
- [老球迷派] conf=25: "哈兰德2.33亿欧状态火热，厄德高已恢复训练，预选双杀意大利，北欧双核有搅局实力。"
- [老球迷派] conf=25: "哈兰德2.33亿欧+厄德高1.28亿欧双核，预选双杀意大利证明6.01亿欧阵容硬度，维京人从不畏惧死亡之组。"
- [黑马派] conf=45: "哈兰德2.33亿欧状态火热，厄德高伤愈回归，预选双杀意大利。法国内耗可趁，+3000回报极高。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 I 组第二或第三出线（法国大概率头名），小组赛依赖哈兰德的个体能力解决战斗。16 强赛面对非顶级对手时，哈兰德-厄德高的双核可能足以制造惊喜。1/4 决赛是真实天花板——面对顶级对手时阵容深度的差距可能暴露。

**最不可信叙事**: "有哈兰德就有夺冠可能"——足球是 11 人的运动，一个前锋无法弥补中后场的系统性差距。

**最值得赛中监控的信号**: (1) 哈兰德的射门数和被犯规次数（反映被限制程度）；(2) 厄德高面对高压逼抢时的传球成功率；(3) 中后场防守的场均失球和失误数。

**如果夺冠，哪些赛前判断有价值**: (1) 哈兰德-厄德高是本届赛事最强的单一双人组合；(2) 简洁直接的防守反击风格在高温赛制中可能被低估；(3) 缺乏大赛经验可能反而是优势——没有历史包袱和心理负担。
