# Championship Path Simulation Card: 突尼斯 (Tunisia)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `tunisia`

## 1. Team Profile

```yaml
team: 突尼斯 (Tunisia)
team_slug: tunisia
confederation: CAF
group: F
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

突尼斯是北非足球的传统强队，2022 世界杯小组赛击败法国（虽法国已提前出线但仍具象征意义）是队史世界杯高光时刻。球队以防守组织和战术纪律性著称，优素福·姆萨克尼（Youssef Msakni）是长期进攻核心。多数球员在欧洲次级联赛或中东联赛效力。F 组同组荷兰、日本和瑞典，出线面临巨大挑战。

## 2. Championship Thesis

> 如果突尼斯夺冠，最可能是因为球队的防守组织在淘汰赛阶段形成了不可穿透的铁桶阵（场均失球 ≤0.5），姆萨克尼等核心球员在反击中展现了致命的效率，且北非球员在高温环境中的体能优势成为淘汰赛的隐性武器——每一场都把比赛拖入低节奏的消耗战，最终在点球大战或定位球中解决战斗。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与荷兰的巨大实力差距 | base_strength_gap | 荷兰的整体实力和技术水平远超突尼斯 | vs 荷兰的控球率和场面表现 |
| 进攻创造力严重不足 | low_scoring_dependency | 突尼斯长期缺乏高水平前锋，进攻效率在非洲球队中属偏低 | 场均进球数和 xG |
| 日本的技术优势 | tactical_mismatch | 日本的传控风格可能轻松穿透突尼斯的中场逼抢 | vs 日本的控球率和被射门数 |
| 阵容深度不足 | squad_depth | 首发有一定竞争力但替补席差距明显 | 替补上场后的技术统计落差 |
| 非洲球队在世界杯淘汰赛的历史天花板 | psychological_pressure | 非洲球队从未进入世界杯半决赛 | 淘汰赛面对欧洲/南美球队时的场面控制力 |
| 缺乏顶级联赛验证的球员 | base_strength_gap | 多数球员来自法国次级联赛、中东联赛或本土联赛 | 首发中五大联赛球员数量 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| F 组至少争取第三名出线 | 小组赛 | 积分 ≥3 | 3 场全败 |
| 防守端保持铁桶阵效率 | 小组赛 | 小组赛场均失球 ≤1 | 场均失球 >2 |
| 找到反击中的致命效率 | 小组赛 | 至少 1 场通过反击进球 | 反击 0 进球 |
| 姆萨克尼或核心球员爆发 | 全赛程 | 至少 1 名核心球员贡献 2+ 进球或助攻 | 核心球员 0 贡献 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 高温天气利好北非球员 | 突尼斯球员对高温环境的适应力优于欧洲对手 | 是 | 比赛日气温 |
| 点球大战的运气因素 | 突尼斯如果把比赛拖入点球，实力差距被压缩为零 | 是 | 比赛是否进入点球 |
| F 组对手互相消耗 | 荷兰、日本、瑞典三强互相消耗可能为突尼斯创造空间 | 是 | F 组积分分布 |
| 2022 击败法国的信心复刻 | 证明突尼斯可以在世界杯中击败顶级对手 | 部分 | 关键场次的场面反应 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: F 组成功出线（至少第三名）
    type: precursor
    observable_proxy: F 组积分
    settlement_rule: 积分 ≥3
  - condition: 防守端淘汰赛场均失球 ≤0.5
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤0.5
  - condition: 姆萨克尼淘汰赛爆发
    type: precursor
    observable_proxy: 姆萨克尼淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥2
  - condition: 至少 2 场淘汰赛进入点球大战
    type: branch
    observable_proxy: 比赛是否进入点球
    settlement_rule: 至少 2 场淘汰赛通过点球晋级
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
| F-TUN-01 | 防守组织效率 | precursor | 场均失球数 | 淘汰赛场均失球 ≤0.5 | public-football-knowledge |
| F-TUN-02 | 姆萨克尼进攻输出 | precursor | 进球+助攻数 | 淘汰赛进球+助攻 ≥2 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 突尼斯 2022 击败法国是重要的心理信号。
> 虽然法国那场比赛已提前出线且轮换了阵容，但这是突尼斯在世界杯中击败顶级对手的首次经历。
> 不进入 Factor Ledger 的原因：单场比赛的心理效应难以量化为可判定因子。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 F 组第三名或勉强出线（利用防守组织力与瑞典和日本竞争），16 强赛面对组头名。突尼斯的防守组织在这一阶段可能制造困难，但进攻端的创造力不足意味着他们很难在淘汰赛中走远。小组出线已是不小的成就。

**最不可信叙事**: "突尼斯的防守铁桶可以锁死一切对手"——防守组织确实出色但进攻端的创造力匮乏意味着突尼斯即使守住也难以得分。2022 击败法国的胜利需要放在对手轮换的背景下理解。

**最值得赛中监控的信号**: (1) vs 瑞典的赛果（决定出线命运的最关键一战）；(2) 防守端的零封率；(3) 反击中的得分效率（防守转进攻的转换速度）。

**如果夺冠，哪些赛前判断有价值**: (1) 突尼斯的防守组织在淘汰赛阶段被严重低估；(2) 北非球员在高温环境中的体能适应力是隐性优势；(3) 2022 击败法国的心理突破比预期更有价值。
