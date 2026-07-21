# Championship Path Simulation Card: 瑞典 (Sweden)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `sweden`

## 1. Team Profile

```yaml
team: 瑞典 (Sweden)
team_slug: sweden
confederation: UEFA
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

瑞典是传统北欧足球强国，但近年来处于人才低谷——2022 世界杯未能出线，2024 欧洲杯同样缺席。亚历山大·伊萨克（Alexander Isak，纽卡斯尔前锋）和德扬·库卢塞夫斯基（Dejan Kulusevski，热刺边锋）是少数在欧洲顶级联赛效力的核心球员。球队传统上以身体对抗、定位球和防守组织见长。F 组同组荷兰、日本和突尼斯，出线需要与日本和突尼斯激烈竞争。

## 2. Championship Thesis

> 如果瑞典夺冠，最可能是因为伊萨克在淘汰赛中展现了世界级射手的终结效率，球队传统的身体对抗和定位球战术在高温淘汰赛中消耗了所有技术型对手，且北欧球队"大赛无名英雄"的传统以最不可思议的方式重演——从无人关注到一路碾压。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 整体实力处于历史低谷 | base_strength_gap | 连续缺席 2022 世界杯和 2024 欧洲杯，球队竞争力明显下降 | FIFA 排名和近期国际赛战绩 |
| 进攻创造力严重不足 | low_scoring_dependency | 除伊萨克和库卢塞夫斯基外缺乏有威胁的进攻球员 | 场均进球数和 xG |
| 中场缺乏顶级控制力 | base_strength_gap | 中场球员多数来自次级联赛，面对顶级中场时可能被碾压 | 中场控球率和传球成功率 |
| 伊萨克的伤病风险 | injury_risk | 伊萨克在纽卡斯尔有过伤病记录，是进攻端不可替代的核心 | 伊萨克出勤率 |
| 日本的技术足球克制瑞典的身体对抗 | tactical_mismatch | 日本的传控风格可能绕过瑞典的高位逼抢 | vs 日本的控球率 |
| 荷兰的全面实力优势 | base_strength_gap | 荷兰在技术、战术和阵容深度上全面优于瑞典 | vs 荷兰的场面表现 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| F 组成功出线 | 小组赛 | 积分 ≥4 | 小组未出线 |
| 伊萨克找到大赛进球节奏 | 小组赛 | 小组赛进球 ≥2 | 伊萨克小组赛 0 球 |
| 定位球成为稳定得分手段 | 小组赛 | 小组赛定位球进球 ≥1 | 定位球 0 进球 |
| 淘汰赛面对技术型球队保持竞争力 | 淘汰赛 | 面对技术型球队场面不失控 | 面对技术型球队被碾压 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 北欧球员在高温中的体能耐受力 | 瑞典球员的体能管理可能优于预期 | 部分 | 比赛下半场的跑动距离 |
| 伊萨克的大赛爆发 | 伊萨克在纽卡斯尔的进球效率暗示他在关键时刻可以爆发 | 是 | 伊萨克单场进球数 |
| F 组对手互相消耗 | 荷兰、日本、突尼斯的技术型对抗可能为瑞典的身体型打法创造空间 | 是 | F 组积分分布 |
| 定位球在淘汰赛中的高价值 | 淘汰赛进球更困难，定位球的边际价值上升 | 是 | 定位球进球占比 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: F 组成功出线
    type: precursor
    observable_proxy: F 组积分
    settlement_rule: 积分 ≥4
  - condition: 伊萨克淘汰赛全程健康且进球效率在线
    type: precursor
    observable_proxy: 伊萨克淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥3
  - condition: 防守端淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 定位球成为淘汰赛的秘密武器
    type: precursor
    observable_proxy: 定位球进球数
    settlement_rule: 淘汰赛定位球进球 ≥2
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
| F-SWE-01 | 伊萨克进球效率 | precursor | 伊萨克淘汰赛进球数 | 淘汰赛进球 ≥3 | public-football-knowledge |
| F-SWE-02 | 定位球转化率 | precursor | 定位球进球数 | 淘汰赛定位球进球 ≥2 | public-football-knowledge |

## 9. Marginalia Notes

> [!memo] 2026-06-13 瑞典是本届赛事中人才低谷期的传统强队。
> 连续缺席 2022 世界杯和 2024 欧洲杯意味着球队的大赛经验极为有限。
> 不进入 Factor Ledger 的原因：大赛经验缺失是结构性条件，难以量化为可判定因子。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-12 | pre-tournament | 初始薄切片版本（Wikipedia draw 数据校正） | WI-0.2 |
| 2026-06-13 | pre-tournament | 深描版本：填充全部 §2-§6, §8, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 F 组第二名或最佳第三名出线（利用身体对抗优势压制突尼斯，与日本竞争第二名），16 强赛面对非顶级对手。伊萨克的个人能力和定位球战术在这一阶段可能制造惊喜。1/8 决赛是合理上限。

**最不可信叙事**: "瑞典大赛 DNA 自动生效"——连续缺席 2022 世界杯和 2024 欧洲杯已证明瑞典不再是那个可以依靠传统和纪律走到深轮次的球队。

**最值得赛中监控的信号**: (1) 伊萨克的进球效率和伤病状态；(2) vs 日本的身体对抗效果（瑞典的身体型打法是否有效克制技术流）；(3) 定位球的转化率（这可能是瑞典在有限实力下最有效的得分手段）。

**如果夺冠，哪些赛前判断有价值**: (1) 伊萨克是本届赛事中被严重低估的世界级射手；(2) 北欧球员的体能管理在高温淘汰赛中被低估；(3) 瑞典的"大赛无名英雄"传统在无人关注的压力释放中可能释放出超常表现。
