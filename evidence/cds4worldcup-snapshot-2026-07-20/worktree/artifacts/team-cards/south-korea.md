# Championship Path Simulation Card: 韩国 (South Korea)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `south-korea`

## 1. Team Profile

```yaml
team: 韩国 (South Korea)
team_slug: south-korea
confederation: AFC
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

韩国是亚洲足球的传统强队，孙兴慜（Son Heung-min）是国家队历史上最伟大的球员，也是当前国际足坛最稳定的攻击手之一。球队以高强度跑动和战术纪律性著称。李刚仁（Lee Kang-in）在巴黎圣日耳曼的成长提供了额外的创造力维度。A 组同组墨西哥、南非、捷克，小组出线机会较好——这是近年来韩国最有利的世界杯分组之一。

## 2. Championship Thesis

> 如果韩国夺冠，那将是孙兴慜职业生涯的终极加冕——可能性极低但路径存在：孙兴慜在淘汰赛阶段爆发了超越一切的个人表演，李刚仁的中场创造力提供了关键的第二维度，球队的超高强度跑动在高温环境中成为碾压级武器，且 A 组相对温和的签运为淘汰赛储备了体能和信心。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与欧洲/南美顶级强队的硬实力差距 | base_strength_gap | 除孙兴慜和李刚仁外缺乏世界级球员 | vs 顶级对手的控球率和射门比 |
| 孙兴慜以外的进攻输出不足 | low_scoring_dependency | 孙兴慜承担了绝大部分进攻责任，其他前锋水平差距明显 | 孙兴慜 vs 其他球员的进球占比 |
| 缺乏世界级中卫 | squad_depth | 后防线核心位置缺乏顶级联赛验证的球员 | vs 强队的失球数和失误次数 |
| 7 场赛制的体能可持续性 | travel_fatigue | 高强度跑动是否在 7 场中可持续是物理限制 | 第 4 场起全队跑动距离 |
| 大赛淘汰赛心理障碍 | psychological_pressure | 除 2002 主场四强外，韩国在世界杯淘汰赛中表现有限 | 淘汰赛首场表现 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| A 组成功出线 | 小组赛 | 积分 ≥5 出线 | 小组未出线 |
| 孙兴慜和李刚仁以外找到稳定得分点 | 小组赛 | 至少 1 名非孙/李球员小组赛进球 ≥2 | 孙/李以外球员 0 球 |
| 防守端保持纪律性 | 全赛程 | 场均失球 ≤1 | 场均失球 ≥2 |
| 淘汰赛面对欧美球队不崩盘 | 淘汰赛 | 面对欧美球队场面不失控 | 面对欧美球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 孙兴慜职业生涯终极爆发 | 孙兴慜在最后一届世界杯中可能超常发挥 | 部分 | 孙兴慜赛前进球率 |
| A 组温和签运低消耗出线 | 与往届死亡之组相比，A 组出线消耗可能较低 | 是 | A 组积分和伤病情况 |
| 高温天气利好跑动型球队 | 韩国的体能优势在高温中可能放大 | 是 | 比赛日气温 |
| 北美大量韩裔社区支持 | 主场氛围加成 | 是 | 球场观众反应 |
| 李刚仁创造力爆发 | 李刚仁在巴黎的成长可能在世界杯舞台上释放 | 是 | 李刚仁关键传球和进球数 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 孙兴慜淘汰赛进球 ≥3
    type: precursor
    observable_proxy: 孙兴慜淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥3
  - condition: A 组以头名或第二出线
    type: precursor
    observable_proxy: A 组积分
    settlement_rule: 积分 ≥5 出线
  - condition: 防守端淘汰赛场均失球 ≤0.5
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤0.5
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
| kr-son-output | 孙兴慜进攻产出 | precursor | 孙兴慜淘汰赛进球+助攻 | 淘汰赛进球+助攻 ≥3 | public-football-knowledge |
| kr-pressing-intensity | 高压跑动强度 | precursor | 全队每 90 分钟跑动距离 | 跑动距离排名前 8 | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（1 条预测）

- 派别分布: 老球迷派
- Kimi 聚合概率: 0.33%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=18: "2002四强那是我们的黄金时刻，孙兴慜虽不在巅峰但太极虎永不言弃。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正小组对手（A 组: 墨西哥/南非/捷克），补充 §8，更新日期 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 A 组第二或头名出线（这是近年来韩国最有利的世界杯分组），16 强赛面对非顶级对手时依靠孙兴慜的个体能力和李刚仁的创造力制造惊喜。如果能进入 1/4 决赛，这将是韩国在非主场世界杯中的历史性突破。

**最不可信叙事**: "2002 的奇迹可以复制"——2002 的主场优势不可复制，但 2026 的 A 组确实是韩国近年来最有利的分组，不应过度悲观也不应过度乐观。

**最值得赛中监控的信号**: (1) 孙兴慜的进球效率和被犯规次数；(2) 李刚仁的关键传球和创造力输出；(3) 非孙/李球员的进攻贡献——如果第三得分点出现，韩国的竞争力将显著提升。

**如果夺冠，哪些赛前判断有价值**: (1) 孙兴慜是本届赛事中个体能力与球队整体实力差距最大的球员——他的最后一届世界杯可能是最大的情感变量；(2) 韩国的高强度跑动在北美高温中可能产生比预期更大的效果；(3) A 组的温和签运意味着韩国首次以低消耗进入淘汰赛阶段，体能储备可能是隐藏优势。
