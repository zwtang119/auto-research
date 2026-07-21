# Championship Path Simulation Card: 加拿大 (Canada)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `canada`

## 1. Team Profile

```yaml
team: 加拿大 (Canada)
team_slug: canada
confederation: CONCACAF
group: B
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

加拿大是 2026 世界杯联合东道主之一，拥有完整的主场优势。阿方索·戴维斯（Alphonso Davies）是拜仁慕尼黑的主力左后卫/边锋，乔纳森·大卫（Jonathan David）在里尔持续保持高效进球率。球队以速度和运动能力见长，2022 世界杯虽然小组出局但积累了宝贵的大赛经验。B 组同组波黑、卡塔尔、瑞士，出线机会存在但瑞士是小组最大威胁。

## 2. Championship Thesis

> 如果加拿大夺冠，最可能是因为东道主优势在 7 场赛制中被放大到了极致，戴维斯的速度在淘汰赛阶段成为不可防守的武器，大卫的进球效率在世界杯舞台上爆发，且 B 组相对可控的签运为淘汰赛积累了信心和体能——用主场氛围和运动天赋弥补了战术精细度的不足。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与欧洲顶级强队的硬实力差距 | base_strength_gap | 除戴维斯和大卫外缺乏世界级球员，整体技术含量有限 | vs 顶级对手的控球率和射门比 |
| 缺乏顶级大赛淘汰赛经验 | psychological_pressure | 2022 小组出局是仅有的近期世界杯经验，淘汰赛经验为零 | 淘汰赛首场表现 |
| 防守端面对顶级攻击的不稳定性 | tactical_mismatch | 后防线缺乏世界级中卫，面对技术型攻击时可能暴露 | vs 强队的失球数 |
| 进攻端过度依赖大卫的进球 | low_scoring_dependency | 大卫是唯一稳定得分点，其他前锋水平差距明显 | 大卫 vs 其他球员的进球占比 |
| 战术精细度不足 | tactical_mismatch | 球队战术体系相对简单，面对战术复杂的对手时可能被破解 | 面对战术成熟球队时的场面 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| B 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 大卫保持进球效率 | 小组赛 | 大卫小组赛进球 ≥2 | 大卫 0 球 |
| 防守端至少 1 场零封 | 小组赛 | 小组赛至少 1 场不失球 | 小组赛场场失球 |
| 淘汰赛面对欧洲球队不崩盘 | 淘汰赛 | 面对欧洲球队场面不失控 | 面对欧洲球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 东道主主场优势（场地+气候+球迷） | 7 场赛制中东道主优势的累积效应不可低估 | 是 | 比赛场地、观众人数和氛围 |
| B 组瑞士以外对手相对可控 | 波黑和卡塔尔的竞争力有限，可能低消耗出线 | 是 | B 组积分分布 |
| 戴维斯速度在淘汰赛成为武器 | 戴维斯的冲刺速度在反击中可能不可阻挡 | 是 | 戴维斯过人成功率和关键冲刺 |
| 半区有利抽签 | 东道主可能在抽签中获得有利位置 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 东道主优势在淘汰赛阶段持续发挥作用
    type: precursor
    observable_proxy: 比赛场地和观众氛围
    settlement_rule: 淘汰赛全部在本土进行且观众支持明显
  - condition: 大卫淘汰赛进球 ≥3
    type: precursor
    observable_proxy: 大卫淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥3
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
| ca-host-advantage | 东道主主场优势 | precursor | 比赛是否在加拿大境内进行及观众氛围 | 至少 3 场比赛在加拿大境内进行 | public-football-knowledge |
| ca-david-goals | 乔纳森·大卫进球效率 | precursor | 大卫每 90 分钟进球数 | 小组赛+淘汰赛场均进球 ≥0.5 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 加拿大作为联合东道主的优势被低估。2022 世界杯的经验虽短暂但为球员提供了大赛氛围的参考。B 组签运尚可——瑞士是强敌但波黑和卡塔尔提供了拿分机会。
>
> 来源：公开足球知识
> 上下文：B 组分析
> 不进入 Factor Ledger 的原因：东道主优势的量化需赛中验证

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充 §1-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 B 组第二出线（瑞士大概率头名，加拿大与波黑、卡塔尔争夺第二），16 强赛面对非顶级对手时依靠戴维斯的速度和大卫的进球效率制造惊喜。东道主氛围在这一阶段可能产生额外加成。1/4 决赛是合理的天花板——面对欧洲或南美顶级球队时硬实力差距可能暴露。

**最不可信叙事**: "东道主优势可以弥补一切实力差距"——2022 世界杯小组出局证明了加拿大的竞技基础仍有差距，东道主优势是加成而非替代。

**最值得赛中监控的信号**: (1) B 组 vs 瑞士的场面数据（反映真实差距）；(2) 大卫的进球效率；(3) 戴维斯的攻防两端贡献——如果攻强守弱则防守漏洞可能被淘汰赛对手利用。

**如果夺冠，哪些赛前判断有价值**: (1) 东道主优势在 7 场赛制中的累积效应是所有变量中最不可量化的；(2) 戴维斯的速度在淘汰赛反击中可能比任何战术安排都更有效；(3) B 组签运提供了低消耗出线的窗口，体能储备可能是隐藏优势。
