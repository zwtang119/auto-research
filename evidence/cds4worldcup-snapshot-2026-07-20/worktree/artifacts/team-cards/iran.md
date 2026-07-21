# Championship Path Simulation Card: 伊朗 (Iran)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `iran`

## 1. Team Profile

```yaml
team: 伊朗 (Iran)
team_slug: iran
confederation: AFC
group: G
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

伊朗是亚洲足球的传统强队，2022 世界杯小组赛击败威尔士展现了竞争力。梅赫迪·塔雷米（Mehdi Taremi，国际米兰前锋）是球队核心，萨达尔·阿兹蒙（Sardar Azmoun）在欧洲联赛有丰富经验。球队以身体素质、防守韧性和反击效率著称，主帅阿米尔·加莱诺伊（Amir Ghalenoei）偏好务实的防守反击战术。G 组同组比利时、埃及和新西兰，出线需要与埃及激烈竞争第二名。

## 2. Championship Thesis

> 如果伊朗夺冠，最可能是因为塔雷米在国际米兰的顶级联赛经验在世界杯舞台上释放了远超预期的进攻效率，球队的防守反击体系在淘汰赛中将每一场比赛拖入低节奏的消耗战，且亚洲球队的"无压力心态"和北美多元文化社区的赛时支持形成了意外的心理优势。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与比利时的实力鸿沟 | base_strength_gap | 比利时整体实力远超伊朗，技术和战术层面存在系统性差距 | vs 比利时的控球率和场面表现 |
| 进攻端创造力不足 | low_scoring_dependency | 塔雷米之外缺乏有威胁的进攻球员，进攻手段单一 | 场均进球数和 xG |
| 面对高位压迫的应对能力 | tactical_mismatch | 伊朗的后场出球能力有限，面对顶级高位压迫可能频繁失误 | 被高位压迫时的失误次数 |
| 场外因素的不确定性 | psychological_pressure | 伊朗足球的场外因素（政治、管理）在大赛中曾多次影响球队表现 | 公开的场外干扰信号 |
| 阵容深度不足 | squad_depth | 塔雷米和阿兹蒙之外缺乏顶级联赛验证的球员 | 替补上场后的技术统计落差 |
| 埃及的萨拉赫威胁 | bracket_strength | 萨拉赫的个人能力可能在 G 组关键战中决定出线归属 | vs 埃及的赛果 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| G 组至少第二名出线 | 小组赛 | 积分 ≥4 | 小组未出线 |
| 塔雷米找到大赛进球节奏 | 小组赛 | 小组赛进球 ≥2 | 塔雷米小组赛 0 球 |
| 防守反击效率验证 | 小组赛 | 至少 1 场通过反击进球且场均失球 ≤1 | 反击 0 进球且场均失球 >2 |
| 淘汰赛面对欧洲球队保持竞争力 | 淘汰赛 | 面对欧洲球队场面不失控 | 面对欧洲球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 北美多元文化社区支持 | 伊朗在北美有大量移民社区 | 是 | 球场氛围 |
| 高温天气利好中东球员 | 伊朗球员对高温环境的适应力优于欧洲/大洋洲对手 | 是 | 比赛日气温 |
| 塔雷米的国际米兰状态延续 | 塔雷米在欧洲顶级联赛的进球效率可能在世界杯中延续 | 是 | 塔雷米单场进球数 |
| 比利时老化暴露弱点 | 比利时黄金一代落幕可能在 G 组中暴露防守弱点 | 是 | 比利时小组赛表现 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: G 组成功出线（至少第二名）
    type: precursor
    observable_proxy: G 组积分
    settlement_rule: 积分 ≥4
  - condition: 塔雷米淘汰赛全程健康且进球效率在线
    type: precursor
    observable_proxy: 塔雷米淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥3
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 淘汰赛至少击败一支欧洲前 10 球队
    type: branch
    observable_proxy: 淘汰赛 vs 欧洲强队赛果
    settlement_rule: 至少 1 场对欧洲前 10 的胜利
  - condition: 半决赛前避免遭遇西班牙或法国
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与西班牙/法国交手
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
| F-IRN-01 | 塔雷米进球效率 | precursor | 塔雷米淘汰赛进球数 | 淘汰赛进球 ≥3 | public-football-knowledge |
| F-IRN-02 | 防守反击效率 | precursor | 反击进球数/场均失球 | 淘汰赛场均失球 ≤1 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 伊朗足球的场外因素是不可忽视的变量。
> 政治环境、管理层更迭和球员待遇等问题在历史上多次影响球队大赛表现。
> 不进入 Factor Ledger 的原因：场外因素不可通过比赛数据判定，属于 Marginalia 范畴。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 G 组第二名出线（击败新西兰，与埃及竞争第二名），16 强赛面对另一个组的第一名。塔雷米的个人能力和球队的防守反击体系在这一阶段可能制造困难。1/8 决赛是合理上限。

**最不可信叙事**: "伊朗的身体素质可以碾压同组所有对手"——伊朗的身体对抗确实出色但面对比利时时技术差距将暴露。2022 世界杯击败威尔士不等于可以稳定击败欧洲中上游球队。

**最值得赛中监控的信号**: (1) vs 埃及的赛果（决定出线命运的关键战）；(2) 塔雷米的进球效率；(3) 防守反击的转换速度（后场抢断到前场射门的平均时间）。

**如果夺冠，哪些赛前判断有价值**: (1) 塔雷米在国际米兰的顶级联赛经验在世界杯中被释放到极致；(2) 伊朗的防守反击体系在淘汰赛中被严重低估；(3) 北美伊朗裔社区的主场支持是隐性优势。
