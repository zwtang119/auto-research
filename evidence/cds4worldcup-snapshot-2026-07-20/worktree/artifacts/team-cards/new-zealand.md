# Championship Path Simulation Card: 新西兰 (New Zealand)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `new-zealand`

## 1. Team Profile

```yaml
team: 新西兰 (New Zealand)
team_slug: new-zealand
confederation: OFC
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
  coverage: thin
```

新西兰是大洋洲足球的代表性球队，克里斯·伍德（Chris Wood，诺丁汉森林前锋）是唯一在欧洲顶级联赛效力的核心球员。球队以身体素质、空中优势和定位球战术见长，技术层面与世界杯级别球队存在显著差距。温斯顿·里德（Winston Reid）退役后防线缺乏已验证的大赛级别球员。G 组同组比利时、埃及和伊朗，三队实力均明显高于新西兰。

> ⚠️ **数据不足标注**: 新西兰的国际比赛数据主要来自 OFC 地区赛事，与世界杯级别对手的交锋样本极少。本卡基于有限的公开信息做出最佳判断，coverage 标记为 thin。

## 2. Championship Thesis

> 如果新西兰夺冠，最可能是因为克里斯·伍德在淘汰赛中展现了超越所有预期的空中统治力和终结效率（类似 2018 曼朱基奇的角色但更极端），球队的定位球战术在每一场淘汰赛中都产生了决定性进球，且 7 场赛制中反复出现的极端天气和 VAR 争议将比赛拉入了新西兰唯一可能赢的低节奏消耗战。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与 G 组三队的系统性实力差距 | base_strength_gap | 比利时、埃及和伊朗在技术、战术和经验上全面优于新西兰 | 首发阵容中五大联赛球员数量（仅伍德 1 人） |
| 进攻端极度依赖克里斯·伍德 | low_scoring_dependency | 伍德之外几乎没有可靠的得分点 | 伍德进球占总进球比 |
| 缺乏顶级联赛验证的球员 | base_strength_gap | 除伍德外球员多数来自次级联赛或 OFC 地区联赛 | 首发球员联赛级别分布 |
| 防守端面对速度型球员的弱点 | tactical_mismatch | 新西兰后卫转身速度慢，面对快速反击时可能被碾压 | 被快速反击进球数 |
| 阵容深度极度不足 | squad_depth | 首发 11 人之外几乎没有同等水平的替补 | 替补上场后的技术统计落差 |
| 大赛经验几乎为零 | psychological_pressure | 新西兰自 2010 世界杯后从未进入决赛圈（2022 通过附加赛出局），球员缺乏大赛压力的应对经验 | 失误次数和场面控制力 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| G 组至少取得 1 分 | 小组赛 | 3 场小组赛至少 1 场平局 | 3 场全败 |
| 克里斯·伍德在世界杯中进球 | 全赛程 | 伍德至少 1 球 | 伍德 0 球 |
| 定位球成为有效得分手段 | 小组赛 | 至少 1 场通过定位球进球 | 定位球 0 进球 |
| 防守端避免大比分溃败 | 小组赛 | 无场次净负 >3 球 | 出现 0-4 或更大比分失利 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 极端天气事件 | 暴雨或大风可能降低比赛技术含量，将实力差距压缩 | 是 | 比赛日天气 |
| 对手轻敌到极致 | G 组三队可能都视新西兰为"送分题"导致严重轮换 | 是 | 对手首发阵容 |
| 克里斯·伍德的空中统治力 | 伍德在英超验证过的头球能力在世界杯定位球中可能爆发 | 是 | 伍德头球争顶成功率 |
| VAR 争议的运气因素 | 争议判罚在低节奏比赛中可能产生更大的影响 | 是 | VAR 判罚统计 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 6
conditions:
  - condition: G 组至少取得 1 分
    type: precursor
    observable_proxy: 小组赛积分
    settlement_rule: 积分 ≥1
  - condition: 克里斯·伍德全程健康且进球效率在线
    type: precursor
    observable_proxy: 伍德进球数
    settlement_rule: 至少 2 球
  - condition: 定位球成为淘汰赛的秘密武器
    type: precursor
    observable_proxy: 定位球进球数
    settlement_rule: 定位球进球 ≥2
  - condition: 防守端场均失球 ≤1
    type: precursor
    observable_proxy: 失球数
    settlement_rule: 场均失球 ≤1
  - condition: 至少 2 场淘汰赛进入点球大战
    type: branch
    observable_proxy: 比赛是否进入点球
    settlement_rule: 至少 2 场淘汰赛通过点球晋级
  - condition: 半区出现大规模爆冷
    type: branch
    observable_proxy: 其他组赛果
    settlement_rule: 至少 3 个传统强队小组出局
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
| F-NZL-01 | 克里斯·伍德空中威胁 | precursor | 头球争顶成功率和进球 | 至少 2 球且头球争顶成功率 ≥60% | public-football-knowledge |
| F-NZL-02 | 定位球转化率 | precursor | 定位球进球数 | 定位球进球 ≥2 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 新西兰是本届赛事数据覆盖最薄的球队之一。
> OFC 地区赛事的竞争水平与世界杯存在数量级差距，历史交锋数据的预测价值有限。
> 不进入 Factor Ledger 的原因：数据不足以支撑可判定因子的验证。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: G 组第四名出局（实力与同组三队差距过大），但可能在某场比赛中通过克里斯·伍德的空中威胁和定位球战术制造短暂的惊吓。小组出线已是极大的成就。

**最不可信叙事**: "新西兰的身体素质可以弥补技术差距"——克里斯·伍德的空中威胁是真实的但不足以抵消 90 分钟内全方位的技术和战术劣势。G 组三队在技术层面的优势过于巨大。

**最值得赛中监控的信号**: (1) 克里斯·伍德的头球争顶成功率和进球数；(2) 定位球转化率（这是新西兰最可能得分的方式）；(3) 防守端的纪律性（是否避免大比分溃败）。

**如果夺冠，哪些赛前判断有价值**: (1) 这将是世界杯历史上比库拉索夺冠更不可思议的黑天鹅事件；(2) 克里斯·伍德的空中威胁在定位球中的价值被极度低估；(3) 极端天气和 VAR 争议对比赛结果的影响远超预期。
