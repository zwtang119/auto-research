# Championship Path Simulation Card: 澳大利亚 (Australia)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `australia`

## 1. Team Profile

```yaml
team: 澳大利亚 (Australia)
team_slug: australia
confederation: AFC
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

澳大利亚以体能充沛、身体对抗强硬和战术纪律性著称。2022 世界杯 16 强赛差点淘汰阿根廷（1-2 惜败），证明了球队在大赛中的竞争力。核心球员多数在欧洲联赛效力，但缺乏真正的世界级个体。D 组同组美国、巴拉圭、土耳其，四队实力相对接近，小组出线机会存在但竞争激烈。

## 2. Championship Thesis

> 如果澳大利亚夺冠，那将是世界杯历史上最不可思议的奇迹之一——可能性极低但路径存在：球队依靠极致的防守纪律性在淘汰赛中连续拖入低比分比赛，门将在点球大战中连续超神，且每一轮淘汰赛的对手都恰好处于状态低谷或伤病危机之中——D 组四队实力接近的竞争反而锻造了最强版本的袋鼠军团。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与顶级强队的硬实力差距 | base_strength_gap | 阵容中缺乏世界级球员，整体技术水平与夺冠球队存在数量级差距 | vs 顶级对手的控球率和射门比 |
| D 组四队实力接近的高消耗 | bracket_strength | 美国、巴拉圭、土耳其均为有竞争力的对手，小组赛每场都是决胜战 | D 组积分 |
| 缺乏世界级射手 | low_scoring_dependency | 没有任何球员在顶级联赛赛季进球达到 15+ | 中锋位置每 90 分钟进球数 |
| 创造力不足 | tactical_mismatch | 进攻端缺乏能突破对手防线的个体创造力 | 场均关键传球和过人成功率 |
| 7 场赛制的阵容深度 | squad_depth | 替补与首发差距大，伤病和停赛会直接削弱竞争力 | 替补上场后的场面变化 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| D 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 找到至少 1 个稳定得分点 | 小组赛 | 至少 1 名球员小组赛进球 ≥2 | 全队小组赛进球 ≤2 |
| 防守纪律性验证 | 全赛程 | 场均失球 ≤1 | 场均失球 ≥2 |
| 淘汰赛面对欧洲对手不崩盘 | 淘汰赛 | 面对欧洲球队场面不失控 | 面对欧洲球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| D 组四队互耗创造窗口 | 四队实力接近意味着任何结果都有可能 | 是 | D 组积分分布 |
| 连续对手伤病/状态低谷 | 每一轮淘汰赛恰好面对不在最佳状态的对手 | 是 | 对手淘汰赛伤病报告 |
| 点球大战门将超神 | 澳大利亚在点球大战中可能获得额外机会 | 是 | 是否进入点球大战 |
| 2022 vs 阿根廷经验的释放 | 差点淘汰世界冠军的经历使球队首次相信自己可以与顶级对手抗衡 | 部分 | 球队信心和精神面貌 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: D 组成功出线
    type: precursor
    observable_proxy: D 组积分
    settlement_rule: 积分 ≥4 出线
  - condition: 防守端淘汰赛场均失球 ≤0.5
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤0.5
  - condition: 至少 2 场淘汰赛进入点球大战且全部获胜
    type: branch
    observable_proxy: 点球大战结果
    settlement_rule: 点球大战胜率 100%
  - condition: 至少 3 场淘汰赛对手核心缺席或状态低迷
    type: branch
    observable_proxy: 对手淘汰赛伤病和表现
    settlement_rule: 至少 3 场对手核心缺席
  - condition: 半决赛前避免遭遇法国、西班牙或阿根廷
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法/西/阿交手
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
| au-defense-discipline | 防守纪律性 | precursor | 场均失球和零封场次 | 场均失球 ≤1 | public-football-knowledge |
| au-physicality | 身体对抗能力 | precursor | 对抗成功率和二分之一球赢得率 | 对抗成功率 ≥55% | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（1 条预测）

- 派别分布: 黑马派
- Kimi 聚合概率: 0.33%

#### 代表性 reason（前 5 条）

- [黑马派] conf=35: "小组D无Top10球队，东道主美国也才+6500，身体流打法适合美加墨场地，赔率极度低估。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正小组对手（D 组: 美国/巴拉圭/土耳其），补充 §8，更新日期 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 D 组第二或最佳第三名出线（四队互耗中凭借身体对抗和防守纪律性拿到关键分数），16 强赛面对实力相对接近的对手时依靠防守纪律性拖入低比分比赛。如果能进入 1/8 决赛，这已是澳大利亚在世界杯上的优异战绩。

**最不可信叙事**: "澳大利亚的体能和纪律性可以弥补一切技术差距"——2022 16 强赛差点淘汰阿根廷证明了竞争力，但那是一场比赛的奇迹，不是 7 场赛制的可持续模式。

**最值得赛中监控的信号**: (1) D 组出线过程和消耗；(2) 防守端的纪律性（场均失球）；(3) 进攻端的创造力（关键传球和 xG）。

**如果夺冠，哪些赛前判断有价值**: (1) 澳大利亚的战术纪律性在面对技术型球队时可能比预期更有效；(2) 2022 16 强赛 vs 阿根廷的经验使球队首次相信自己可以在淘汰赛中与顶级对手抗衡；(3) D 组四队实力接近意味着出线过程本身就是最好的淘汰赛准备。
