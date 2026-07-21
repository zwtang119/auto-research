# Championship Path Simulation Card: 摩洛哥 (Morocco)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `morocco`

## 1. Team Profile

```yaml
team: 摩洛哥 (Morocco)
team_slug: morocco
confederation: CAF
group: C
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

摩洛哥是 2022 世界杯半决赛球队（史上首支非洲四强），雷格拉吉（Walid Regragui）执教下建立了以纪律性防守+快速反击为核心的体系。阿什拉夫（Achraf Hakimi）、阿姆拉巴特（Sofyan Amrabat）、布努（Bounou）等核心球员在欧洲顶级联赛效力。2025 非洲杯冠军和 U20 世界杯冠军进一步证明了摩洛哥足球体系的深度。C 组同组巴西、海地、苏格兰，与巴西争夺小组头名是关键看点。

## 2. Championship Thesis

> 如果摩洛哥夺冠，最可能是因为雷格拉吉的防守反击体系在 C 组中与巴西的对抗中再次证明有效性（2022 已在淘汰赛中击败葡萄牙和西班牙），阿什拉夫的边路突击构成攻防转换的核心武器，且 2022 半决赛的经验使球队在淘汰赛阶段以强队自居而非黑马——用纪律性弥补个体差距，用大赛经验释放心理优势。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与巴西的硬实力差距 | base_strength_gap | 巴西的个体天赋和进攻深度是摩洛哥 C 组最大的直接威胁 | C 组 vs 巴西的控球率和射门数 |
| 进攻创造力不足 | low_scoring_dependency | 防守反击体系在领先时缺乏控制比赛节奏的能力 | 场均射门和 xG |
| 从黑马到强队的身份转换压力 | psychological_pressure | 2022 的惊喜元素不再，对手会充分准备面对摩洛哥 | 淘汰赛面对已准备充分的对手时的场面 |
| 核心球员伤病风险 | injury_risk | 阿什拉夫和阿姆拉巴特的替补水平明显低于首发 | 核心球员出勤率 |
| 淘汰赛面对技术型球队的瓶颈 | favorite_collision | 摩洛哥擅长打反击但在面对更全面的对手时可能处于被动 | vs 技术型球队的控球率 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| C 组至少拿到 4 分出线 | 小组赛 | 积分 ≥4 且净胜球为正 | 小组赛 0-3 分出局 |
| 进攻端找到稳定得分点 | 小组赛 | 场均进球 ≥1.5 | 小组赛场均进球 <1 |
| 阿什拉夫边路攻防两端的稳定输出 | 淘汰赛 | 淘汰赛阶段至少 1 球或 2 助攻 | 阿什拉夫被限制且无进攻贡献 |
| 击败一支顶级对手 | 淘汰赛 | 面对 FIFA 前 10 球队取胜 | 对顶级对手场面完全被动 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| C 组巴西意外翻车 | 巴西在 C 组消耗过大为摩洛哥创造头名窗口 | 是 | C 组积分 |
| 北美大量摩洛哥裔社区支持 | 主场氛围加成 | 是 | 球场观众反应 |
| 高温天气利好防守反击 | 高温下强队进攻效率下降，防守反击性价比上升 | 是 | 比赛日气温 |
| 点球大战布努优势 | 布努是点球大战专家，2022 已验证 | 是 | 是否进入点球大战 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 3
conditions:
  - condition: C 组成功出线
    type: precursor
    observable_proxy: C 组积分
    settlement_rule: 积分 ≥4 出线
  - condition: 阿什拉夫全程健康且进攻输出在线
    type: precursor
    observable_proxy: 阿什拉夫淘汰赛进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥2
  - condition: 防守反击体系在淘汰赛保持零封率 ≥50%
    type: precursor
    observable_proxy: 淘汰赛零封场次
    settlement_rule: 淘汰赛至少 2 场零封
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
| ma-hakimi-output | 阿什拉夫攻防输出 | precursor | 进球+助攻+关键拦截 | 淘汰赛进球+助攻 ≥2 | public-football-knowledge |
| ma-bounou-penalty | 布努点球能力 | precursor | 点球大战扑救率 | 点球大战扑救率 ≥30% | public-football-knowledge |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（12 条预测）

- 派别分布: 主帅视角派, 赔率派, 阵容年龄派, 黑马派
- Kimi 聚合概率: 4.00%

#### 代表性 reason（前 5 条）

- [赔率派] conf=45: "摩洛哥FIFA第7却+5000隐含仅2%，2022四强+2025 U20世冠+非洲杯冠军，非洲球队北美时区无时差劣势。"
- [主帅视角派] conf=52: "非洲球队身体+速度优势在北美气候下如鱼得水，FIFA第7+非洲杯冠军新帅进攻改革。"
- [黑马派] conf=52: "摩洛哥FIFA第7+U20世冠+非洲杯双冠，赔率+5000隐含仅2%。新帅进攻体系在美洲有爆冷土壤。"
- [黑马派] conf=48: "摩洛哥FIFA第7却赔率仅+5000，2022四强+2025非洲杯+U20世冠三线登顶，被严重低估。"
- [黑马派] conf=62: "摩洛哥FIFA第7团队纪律性堪比德甲球队，新帅进攻改革让2022四强队伍更完整。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |
| 2026-06-13 | pre-tournament | 修正小组对手（C 组: 巴西/海地/苏格兰），补充 §8，更新日期 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 C 组第二出线（巴西大概率头名，摩洛哥凭借实力碾压海地和苏格兰锁定第二），16 强赛面对非顶级对手。雷格拉吉的防守反击体系在淘汰赛阶段继续发挥，布努的点球能力成为淘汰赛的保险。如果半区有利（避开法国/英格兰），可能再次闯入半决赛。

**最不可信叙事**: "摩洛哥复制 2022 黑马奇迹即可夺冠"——2022 的惊喜元素已不存在，所有对手都会认真对待摩洛哥。但 C 组的签运确实比 2022 有利——没有西班牙和葡萄牙在小组赛中直接对抗。

**最值得赛中监控的信号**: (1) C 组 vs 巴西的场面（控球率和射门比反映真实差距）；(2) 进攻端的 xG 和转化率；(3) 阿什拉夫的攻防输出。

**如果夺冠，哪些赛前判断有价值**: (1) 2022 半决赛经验使摩洛哥拥有所有非传统强队中最成熟的大赛心态；(2) 雷格拉吉的战术纪律性是所有参赛教练中最被低估的；(3) C 组的温和签运意味着摩洛哥可以以较低消耗进入淘汰赛，体能储备是隐藏优势。
