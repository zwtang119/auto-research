# Championship Path Simulation Card: 阿尔及利亚 (Algeria)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `algeria`

## 1. Team Profile

```yaml
team: 阿尔及利亚 (Algeria)
team_slug: algeria
confederation: CAF
group: J
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
  coverage: thin
```

阿尔及利亚是非洲足球的传统强队，1990 年非洲杯冠军，2014 年世界杯曾以出色的传控足球险些淘汰 eventual 冠军德国（加时赛 1-2 惜败）。马赫雷斯（Riyad Mahrez）是球队的绝对核心，在曼城和莱斯特城均已证明世界级实力。斯利马尼（Islam Slimani）是非洲杯历史射手榜前列的老将。J 组同组阿根廷、奥地利和约旦，签运中等——避开阿根廷有一定可能但需要在与奥地利和约旦的竞争中占据优势。

## 2. Championship Thesis

> 如果阿尔及利亚夺冠，最可能是因为马赫雷斯在淘汰赛阶段展现了世界级的个人表演（类似 2014 年世界杯对德国的发挥），球队围绕他构建的防守反击体系在高温环境中发挥了超越阵容水平的效率，且 J 组阿根廷之外的两个对手（奥地利、约旦）被成功压制，为淘汰赛积累了信心和体能。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 整体阵容深度不足 | base_strength_gap | 马赫雷斯之外缺乏同级别的世界级球员，球队上限受个体质量制约 | 非马赫雷斯球员的进攻贡献 |
| 马赫雷斯年龄和状态 | injury_risk | 马赫雷斯已 35 岁，离开曼城后竞技水平和对抗强度是否保持存疑 | 马赫雷斯每 90 分钟过人和关键传球数 |
| 进攻创造力过度集中 | low_scoring_dependency | 马赫雷斯承担过多进攻责任，一旦被锁死全队进攻瘫痪 | 马赫雷斯被限制时球队的进球数 |
| 防守端面对欧洲球队的脆弱性 | tactical_mismatch | 面对奥地利的高位压迫体系时，阿尔及利亚的出球和防守组织可能崩溃 | 面对压迫型球队的传球成功率 |
| J 组阿根廷的压倒性优势 | bracket_strength | 阿根廷大概率占据小组头名，阿尔及利亚需在剩余两个对手中竞争出线 | J 组积分 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| J 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 马赫雷斯以外进攻点输出 | 小组赛 | 至少 2 名非马赫雷斯球员小组赛进球 | 全队进球 100% 来自马赫雷斯 |
| 击败奥地利或约旦 | 小组赛 | 至少 1 胜 | 对 J 组非阿根廷对手 0 胜 |
| 防守端零封验证 | 淘汰赛 | 至少 1 场淘汰赛零封 | 淘汰赛场场失球 ≥2 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 高温天气利好北非球队 | 阿尔及利亚球员习惯高温干燥环境，北美夏季天气可能是优势 | 是 | 比赛日气温 |
| 马赫雷斯告别战爆发 | 马赫雷斯可能在最后一届大赛中超常发挥 | 部分 | 马赫雷斯场上表现 |
| 阿根廷 J 组低消耗出线 | 阿根廷可能轮换，给阿尔及利亚留下取分空间 | 是 | 阿根廷 vs 阿尔及利亚时的阵容 |
| 半区有利抽签 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: 马赫雷斯淘汰赛进球+助攻 ≥4
    type: precursor
    observable_proxy: 马赫雷斯淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥4
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 至少 2 名非马赫雷斯球员淘汰赛进球
    type: precursor
    observable_proxy: 非马赫雷斯球员进球数
    settlement_rule: 非马赫雷斯球员淘汰赛合计进球 ≥3
  - condition: 半决赛前避免遭遇法国或西班牙
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法国/西班牙交手
  - condition: 至少 2 场淘汰赛对手核心球员缺席
    type: branch
    observable_proxy: 对手伤病情况
    settlement_rule: 至少 2 场淘汰赛对手核心缺席
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
| algeria-mahrez-output | 马赫雷斯进攻输出 | precursor | 马赫雷斯每 90 分钟进球+助攻+关键传球 | 小组赛场均关键传球 ≥2 | public-football-knowledge |
| algeria-group-competitiveness | J 组出线竞争力 | precursor | J 组 vs 奥地利和约旦的赛果 | 至少 1 胜 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 阿尔及利亚数据有限，核心判断基于马赫雷斯的个体能力和 2014 世界杯的历史表现。
>
> 来源：公开足球知识（2014 世界杯记录、非洲杯历史、马赫雷斯俱乐部数据）
> 上下文：J 组与阿根廷、奥地利、约旦同组，竞争出线权
> 不进入 Factor Ledger 的原因：缺乏足够的可判定数据支撑因子

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 11 节 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: J 组以小组第二或最佳第三名出线（在与奥地利和约旦的竞争中占据优势），16 强赛面对非顶级对手。马赫雷斯的个体能力在这一阶段足以制造威胁，但 1/4 决赛面对欧洲顶级球队时整体实力差距可能暴露。

**最不可信叙事**: "马赫雷斯一个人就能带队走远"——2014 年世界杯阿尔及利亚的整体表现说明这支队需要体系支撑，单纯依赖马赫雷斯的个体能力无法持续 7 场。

**最值得赛中监控的信号**: (1) 马赫雷斯的过人成功率和被犯规次数（反映被限制程度）；(2) 非马赫雷斯球员的进攻贡献（第二、第三得分点是否存在）；(3) 面对奥地利高位压迫时的传球成功率。

**如果夺冠，哪些赛前判断有价值**: (1) 马赫雷斯是世界级球员，但他在国家队的输出长期被低估；(2) 北非球队在北美高温环境中的适应能力可能是被忽视的变量；(3) 2014 年对德国的表现证明了阿尔及利亚面对顶级球队时不会怯场。
