# Championship Path Simulation Card: 荷兰 (Netherlands)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `netherlands`

## 1. Team Profile

```yaml
team: 荷兰 (Netherlands)
team_slug: netherlands
confederation: UEFA
group: F
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
  coverage: sufficient
```

荷兰是三届世界杯亚军（1974、1978、2010），从未捧杯是国际足坛最著名的"无冕之王"叙事。范迪克（Virgil van Dijk）领衔的防线、弗伦基·德容（Frenkie de Jong）的中场控制和加克波（Cody Gakpo）的进攻输出构成核心框架。科曼（Ronald Koeman）执教风格务实但缺少顶级对手面前的爆发力。F 组同组日本、瑞典和突尼斯，日本 2022 世界杯击败德西的战绩不可忽视，瑞典的身体对抗也是实质挑战。

## 2. Championship Thesis

> 如果荷兰夺冠，最可能是因为范迪克的防线在淘汰赛阶段建立了不可逾越的屏障（场均失球 ≤0.5），加克波延续了 2022 世界杯的淘汰赛进球效率，且"无冕之王"的 50 年叙事包袱在某个关键瞬间被彻底打破——全队以一种前所未有的方式跨过心理门槛。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| "无冕之王"历史心理包袱 | psychological_pressure | 三次决赛失利（1974、1978、2010）的历史阴影在关键场次可能复发 | 淘汰赛关键场次（决赛/半决赛）的场面表现 |
| 缺乏世界级射手 | low_scoring_dependency | 加克波是唯一已验证的大赛进攻输出点，替补深度不足 | 前 3 场进球分布（是否集中在加克波一人） |
| 弗伦基·德容伤病风险 | injury_risk | 德容近年脚踝反复受伤，中场控制力高度依赖其健康 | 德容出勤率和场均传球数 |
| 科曼的战术天花板 | tactical_mismatch | 科曼的务实风格在小组赛有效但淘汰赛面对顶级教练可能被战术碾压 | 淘汰赛 vs 顶级教练的战术调整效果 |
| 日本的技术冲击 | tactical_mismatch | 日本 2022 世界杯击败德国西班牙的技术足球可能克制荷兰的防守体系 | F 组 vs 日本的赛果 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| F 组头名出线且消耗可控 | 小组赛 | 积分 ≥7 且范迪克/德容无伤停 | 小组未头名或核心伤停 |
| 加克波以外找到第二进攻点 | 小组赛 | 至少 1 名非加克波球员小组赛进球 ≥2 | 加克波以外球员小组赛 0 球 |
| 淘汰赛面对顶级对手不崩盘 | 1/8 或 1/4 决赛 | 面对法国/西班牙/英格兰级别对手场面不失控 | 面对顶级对手被碾压 |
| 范迪克防线零封率验证 | 淘汰赛 | 淘汰赛零封 ≥2 场 | 淘汰赛 0 场零封 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| F 组对手互相消耗 | 日本、瑞典、突尼斯互相消耗降低荷兰小组赛压力 | 是 | F 组积分分布 |
| 半区有利抽签 | 避免淘汰赛连续遭遇顶级对手 | 是 | 淘汰赛对阵表 |
| 加克波复制 2022 淘汰赛爆发 | 大赛淘汰赛阶段加克波有特殊进球嗅觉 | 是 | 加克波淘汰赛进球数 |
| 高温天气利好技术型中场 | 德容的控球在高温下价值放大 | 是 | 比赛日气温 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: 范迪克防线淘汰赛场均失球 ≤0.5
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛 4+ 场中失球 ≤2
  - condition: 弗伦基·德容全程健康且中场控制力在线
    type: precursor
    observable_proxy: 德容淘汰赛传球成功率和出场时间
    settlement_rule: 德容淘汰赛场均传球成功率 ≥90%
  - condition: 加克波淘汰赛进球 ≥3
    type: precursor
    observable_proxy: 加克波淘汰赛进球数
    settlement_rule: 淘汰赛进球 ≥3
  - condition: 半决赛前避免遭遇西班牙或英格兰
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与西班牙/英格兰交手
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
| F-NED-01 | 范迪克防线零封率 | precursor | 淘汰赛零封场次 | 淘汰赛零封 ≥2 场 | public-football-knowledge |
| F-NED-02 | 加克波大赛进球效率 | precursor | 加克波淘汰赛进球数 | 淘汰赛进球 ≥3 | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（6 条预测）

- 派别分布: 主帅视角派, 心理抗压派, 老球迷派, 阵容年龄派, 黑马派
- Kimi 聚合概率: 2.00%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=52: "1974克鲁伊夫、2010斯内德，三代全攻全守流尽泪。格拉芬贝赫1.05亿欧领衔，F组能从容练级。"
- [老球迷派] conf=45: "1978决赛饮恨至今刻骨铭心，全攻全守火种从未熄灭，荷兰8.37亿欧FIFA第6，+2000是最大价值黑马注。"
- [主帅视角派] conf=55: "格拉芬贝赫+廷伯+加克波全是自家青训精品，技术流压迫在F组有练兵空间。"
- [黑马派] conf=55: "荷兰8.37亿欧FIFA第6无超巨球星，拼图型阵容少了巨星包袱，西蒙斯伤缺倒逼团队足球。"
- [阵容年龄派] conf=30: "格拉芬贝赫23岁廷伯23岁骨架体能优势明显，+2000价值投资，美加墨高温赛程青年军有优势。"

> [!memo] 2026-06-13 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正组别为 F 组（日本/瑞典/突尼斯），更新对手分析，填充 §8 | WI-0.2 组别校正 |

## 11. Current Interpretation

**最可信路径**: 以 F 组头名出线（凭整体实力力压日本、瑞典和突尼斯），16 强赛面对相对较弱的对手。范迪克的防守组织和加克波的进攻效率在这一阶段完成磨合。1/4 决赛是关键门槛——如果跨过，科曼的务实风格和"无冕之王"的压力释放可能在半决赛和决赛中产生正向效应。

**最不可信叙事**: "荷兰的美丽足球终将得到回报"——荷兰自克鲁伊夫时代以来已长期不再踢纯粹的美丽足球，科曼的务实风格不是劣势但也不是夺冠的充分条件。

**最值得赛中监控的信号**: (1) 范迪克防线的零封率和组织稳定性；(2) 弗伦基·德容的出勤率和传球数据；(3) 进攻端是否找到加克波以外的稳定得分点。

**如果夺冠，哪些赛前判断有价值**: (1) "无冕之王"的叙事包袱一旦被打破，释放的心理能量可能比任何战术调整都重要；(2) 范迪克在淘汰赛阶段的防守组织是世界级的；(3) 加克波的大赛进球嗅觉是本届赛事中被低估的进攻变量。
