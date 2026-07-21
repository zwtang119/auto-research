# Championship Path Simulation Card: 巴拉圭 (Paraguay)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `paraguay`

## 1. Team Profile

```yaml
team: 巴拉圭 (Paraguay)
team_slug: paraguay
confederation: CONMEBOL
group: D
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

巴拉圭通过南美预选赛获得参赛资格，延续了 CONMEBOL 球队的高竞争门槛传统。球队以防守纪律性和战术纪律性著称，历史上多次在世界杯中制造惊喜（2010 八强是最佳战绩）。米格尔·阿尔米隆（Miguel Almirón）是进攻端最依赖的创造力来源。巴拉圭足球的传统风格是"防守反击+定位球"，技术精细度有限但战术执行力强。D 组同组美国、澳大利亚、土耳其，四队实力相对接近，小组出线机会存在但竞争激烈。

## 2. Championship Thesis

> 如果巴拉圭夺冠，最可能是因为南美足球的战术底蕴在淘汰赛中被充分释放，球队的防守纪律性将每一场淘汰赛拖入低比分消耗战，阿尔米隆的速度在反击中成为不可防守的武器，且 D 组四队实力接近意味着出线过程锻造了最强版本的国家队——用南美足球的韧性和纪律性完成了从防守反击专家到世界冠军的跃迁。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与世界级球队的硬实力差距 | base_strength_gap | 除阿尔米隆外缺乏欧洲顶级联赛核心球员 | vs 顶级对手的控球率和射门比 |
| 进攻创造力严重不足 | low_scoring_dependency | 进攻过于依赖阿尔米隆的个体突破，缺乏系统性的进攻组织 | 场均 xG 和关键传球数 |
| 缺乏稳定的中锋 | low_scoring_dependency | 没有球员在顶级联赛赛季进球达到 15+ | 中锋位置每 90 分钟进球数 |
| D 组四队实力接近的高消耗 | bracket_strength | 美国、澳大利亚、土耳其均为有竞争力的对手，小组赛消耗可能偏大 | D 组累计上场时间/黄牌数 |
| 大赛淘汰赛经验有限 | psychological_pressure | 2010 八强是近年最佳战绩，淘汰赛经验积累不足 | 淘汰赛首场表现 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| D 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 阿尔米隆或替代者保持创造力输出 | 小组赛 | 场均关键传球 ≥2 或进球+助攻 ≥2 | 阿尔米隆被限制且无贡献 |
| 防守纪律性验证 | 全赛程 | 场均失球 ≤1 且至少 1 场零封 | 场均失球 ≥2 |
| 找到阿尔米隆以外的得分点 | 全赛程 | 至少 1 名非阿尔米隆球员进球 ≥2 | 阿尔米隆以外球员 0 球 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| D 组四队互耗创造窗口 | 四队实力接近意味着每场比赛都可能出现意外结果 | 是 | D 组积分分布 |
| 南美足球的战术底蕴被低估 | CONMEBOL 球队在高强度比赛中的战术适应能力可能被低估 | 部分 | 面对欧美球队时的场面 |
| 定位球在淘汰赛成为武器 | 巴拉圭的定位球和角球能力在面对高强度防守时可能成为破局关键 | 是 | 定位球进球占比 |
| 半区有利抽签 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: D 组成功出线
    type: precursor
    observable_proxy: D 组积分
    settlement_rule: 积分 ≥4 出线
  - condition: 阿尔米隆淘汰赛全程健康且创造力在线
    type: precursor
    observable_proxy: 阿尔米隆淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥2
  - condition: 防守端淘汰赛场均失球 ≤0.5
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤0.5
  - condition: 半决赛前避免遭遇法国或阿根廷
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法/阿交手
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
| py-defense-discipline | 防守纪律性 | precursor | 场均失球和零封场次 | 场均失球 ≤1 | public-football-knowledge |
| py-almiron-output | 阿尔米隆创造力 | precursor | 关键传球和进球+助攻 | 场均关键传球 ≥2 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 巴拉圭的 CONMEBOL 预选赛出线本身就是一个竞争力的证明——南美预选赛是世界足坛最残酷的预选赛之一。D 组四队实力接近是巴拉圭的机会也是挑战——每场比赛都是决胜战。
>
> 来源：公开足球知识
> 上下文：D 组分析
> 不进入 Factor Ledger 的原因：南美预选赛表现与世界杯表现的相关性需赛中验证

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充 §1-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 D 组第二或最佳第三名出线（四队互耗中凭借防守纪律性拿到关键分数），16 强赛面对非顶级对手时依靠阿尔米隆的反击和定位球。如果能进入 1/8 决赛，这将是巴拉圭自 2010 年以来在世界杯上的最佳战绩。

**最不可信叙事**: "巴拉圭的防守纪律性可以无限期维持"——2010 八强是当前框架的合理上限，进攻端的创造力不足是结构性问题。但 D 组确实比大多数 CONMEBOL 球队习惯面对的小组更有利。

**最值得赛中监控的信号**: (1) D 组每场比赛的赛果——四队实力接近意味着每场都是决赛；(2) 阿尔米隆的创造力和进球输出；(3) 定位球得分占比——如果过高说明阵地战创造不足。

**如果夺冠，哪些赛前判断有价值**: (1) CONMEBOL 预选赛出线的含金量被低估——在世界上最残酷的预选赛中脱颖而出意味着巴拉圭的基本面比名义实力更强；(2) 防守纪律性在淘汰赛低比分比赛中可能比进攻创造力更有价值；(3) D 组四队实力接近意味着出线过程本身就是最好的淘汰赛准备。
