# Championship Path Simulation Card: 佛得角 (Cape Verde)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `cape-verde`

## 1. Team Profile

```yaml
team: 佛得角 (Cape Verde)
team_slug: cape-verde
confederation: CAF
group: H
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

佛得角是非洲西海岸岛国（人口约 50 万），2023 年非洲杯打进八强创造了队史最佳战绩。球队大量依赖葡萄牙裔归化球员——许多球员在葡萄牙青训体系中成长，如瑞恩·门德斯（Ryan Mendes）和肯尼·罗查·桑托斯（Kenny Rocha Santos）。球队风格带有明显的葡萄牙技术足球烙印。H 组同组西班牙、沙特阿拉伯和乌拉圭，三队实力均明显高于佛得角。

> ⚠️ **数据不足标注**: 佛得角的国际比赛数据主要来自 AFCON 和非洲预选赛，与世界杯级别对手的交锋样本极少。本卡基于有限的公开信息做出最佳判断，coverage 标记为 thin。

## 2. Championship Thesis

> 如果佛得角夺冠，最可能是因为葡萄牙裔归化球员的欧洲青训底色在世界杯舞台上产生了远超预期的化学反应（类似 2002 塞内加尔的爆发但更极端），球队的"微型国家"心态（没有任何压力和包袱）使每一场比赛都成为自由的超级发挥，且淘汰赛阶段的连续黑天鹅事件将实力差距压缩到零。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与 H 组三队的系统性实力差距 | base_strength_gap | 西班牙是世界第 1，乌拉圭是传统强队，沙特有 2022 击败阿根廷的经验 | 首发阵容中五大联赛球员数量 |
| 缺乏顶级联赛核心球员 | base_strength_gap | 多数球员来自葡萄牙次级联赛或小联赛 | 首发球员联赛级别分布 |
| 阵容深度极度不足 | squad_depth | 首发 11 人之外几乎没有同等水平的替补 | 替补上场后的技术统计落差 |
| 大赛经验几乎为零 | psychological_pressure | 队史首次参加世界杯决赛圈，球员和教练组缺乏应对大赛压力的经验 | 失误次数和场面控制力 |
| 进攻端缺乏稳定得分手段 | low_scoring_dependency | 缺乏高水平前锋，进攻效率在非洲球队中属偏低 | 场均进球数和 xG |
| 面对西班牙传控体系的无力 | tactical_mismatch | 西班牙的控球能力可能让佛得角整场比赛触球不到 30 次 | vs 西班牙的控球率 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| H 组至少取得 1 分 | 小组赛 | 3 场小组赛至少 1 场平局 | 3 场全败 |
| 葡萄牙裔核心球员发挥欧洲联赛水平 | 全赛程 | 至少 1 名葡萄牙裔球员贡献进球或助攻 | 葡萄牙裔球员 0 贡献 |
| 找到防守端的稳定性 | 小组赛 | 场均失球 ≤2 | 场均失球 >3 |
| 避免大比分溃败 | 小组赛 | 无场次净负 >3 球 | 出现 0-4 或更大比分失利 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 葡萄牙裔球员的"隐形足球文化" | 葡萄牙青训体系赋予的技术底色可能在关键时刻闪光 | 部分 | 葡萄牙裔球员的传球和控球数据 |
| 对手轻敌 | 西班牙和乌拉圭可能视佛得角为"送分题"导致严重轮换 | 是 | 对手首发阵容 |
| 高温天气 | 佛得角球员对热带气候的适应力可能优于欧洲/南美对手 | 是 | 比赛日气温和湿度 |
| 2023 AFCON 八强的信心惯性 | 队史最佳战绩可能在世界杯中转化为额外的心理韧性 | 部分 | 关键场次的场面反应 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 6
conditions:
  - condition: H 组至少取得 1 分
    type: precursor
    observable_proxy: 小组赛积分
    settlement_rule: 积分 ≥1
  - condition: 葡萄牙裔核心球员贡献至少 1 球
    type: precursor
    observable_proxy: 进球统计
    settlement_rule: 至少 1 名葡萄牙裔球员进球或助攻
  - condition: 防守端场均失球 ≤1.5
    type: precursor
    observable_proxy: 失球数
    settlement_rule: 3 场失球合计 ≤5
  - condition: 避免大比分溃败
    type: precursor
    observable_proxy: 每场比分差
    settlement_rule: 无场次净负 >2 球
  - condition: 半区出现大规模爆冷
    type: branch
    observable_proxy: 其他组赛果
    settlement_rule: 至少 2 个传统强队小组出局
  - condition: 至少 2 场淘汰赛进入点球大战
    type: branch
    observable_proxy: 比赛是否进入点球
    settlement_rule: 至少 2 场淘汰赛通过点球晋级
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
| F-CPV-01 | 葡萄牙裔球员贡献度 | precursor | 进球+助攻数 | 至少 1 人贡献进球或助攻 | public-football-knowledge |
| F-CPV-02 | 防守稳定性 | counter_signal | 场均失球数 | 3 场失球合计 ≤5 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 佛得角是本届赛事数据覆盖最薄的球队之一。
> 人口仅约 50 万，国际比赛样本极少。但葡萄牙裔归化球员的欧洲青训底色是隐性优势。
> 不进入 Factor Ledger 的原因：数据不足以支撑可判定因子的验证。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: H 组第四名出局（实力与同组三队差距过大），但葡萄牙裔球员的技术底色可能在某场比赛中短暂闪光。2023 AFCON 八强的经验使球队不至于在大赛舞台上完全崩溃。小组出线已是极大的成就。

**最不可信叙事**: "佛得角的葡萄牙血统可以复制葡萄牙的成功"——归化球员的葡萄牙青训背景确实赋予了技术底色，但球员个体水平与葡萄牙国家队存在数量级差距。

**最值得赛中监控的信号**: (1) vs 沙特阿拉伯的赛果（H 组中最有可能取分的一场）；(2) 葡萄牙裔核心球员的传球和控球数据；(3) 防守端的组织纪律性（是否避免大比分溃败）。

**如果夺冠，哪些赛前判断有价值**: (1) 这将是世界杯历史上最大尺度的黑天鹅事件之一；(2) 葡萄牙裔归化球员的"隐形足球文化"价值被极度低估；(3) 2023 AFCON 八强的经验在世界杯中产生了远超预期的信心惯性。
