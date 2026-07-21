# Championship Path Simulation Card: 法国 (France)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `france`

## 1. Team Profile

```yaml
team: 法国 (France)
team_slug: france
confederation: UEFA
group: I
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - high_kimi_probability
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: [kimi-aggregation]
  red_sources: [kimi-300-agent-reasons]
  coverage: sufficient
```

法国是 2018 世界杯冠军、2022 世界杯亚军，德尚执教十余年建立了极具韧性的大赛体系。姆巴佩（Kylian Mbappé）是当今足坛最具破坏力的攻击手，阵容总身价常年位居全球前三。I 组同组有塞内加尔、伊拉克和挪威，小组赛出线应无大碍但塞内加尔的物理强度和挪威的哈兰德构成实质性考验。2026 是德尚谢幕之战，更衣室凝聚力可能达到峰值。

## 2. Championship Thesis

> 如果法国夺冠，最可能是因为德尚谢幕战的情感凝聚力释放了球队长期被压制的进攻潜力，姆巴佩在淘汰赛阶段的个体爆破能力在 7 场赛制中不可阻挡，且法国的阵容深度（每个位置 2+ 世界级选项）在高温和多旅行赛制中形成碾压级容错率。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 小组赛阶段习惯性慢热 | psychological_pressure | 法国在近两届世界杯小组赛均有状态起伏，I 组虽非死亡之组但塞内加尔不容小觑 | 小组赛前 2 场积分/净胜球 |
| 中场创造力依赖格列兹曼状态 | squad_depth | 格列兹曼年龄增长后状态波动加大，法国缺乏同等水平的替代组织者 | 格列兹曼每 90 分钟关键传球数 |
| I 组塞内加尔和挪威的实质威胁 | bracket_strength | 塞内加尔是 2022 非洲杯冠军身体对抗极强，挪威有哈兰德和厄德高双核，小组消耗不可忽视 | 小组赛累计上场时间和伤病 |
| 德尚保守战术的天花板 | tactical_mismatch | 关键淘汰赛中德尚倾向收缩防守，可能浪费进攻端天赋优势 | 淘汰赛阶段控球率和射门数 |
| 姆巴佩被针对性限制 | injury_risk | 对手双人包夹+犯规战术可能导致姆巴佩效率下降或伤病 | 姆巴佩每场被犯规次数和跑动热区 |
| 防线中卫搭档不稳定 | squad_depth | 于帕梅卡诺、科内特、萨利巴均未形成固定搭档，大赛默契存疑 | 中卫组合每场失球数 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| 小组赛前两场锁定出线权 | 小组赛 | 前 2 场拿 ≥4 分 | 前 2 场仅 1 分或更少 |
| 中卫搭档形成稳定组合 | 小组赛 | 同一中卫组合小组赛出场 ≥2 场且零封 ≥1 场 | 小组赛 3 场使用 3 对不同中卫 |
| 格列兹曼或替代者组织输出稳定 | 淘汰赛 | 每 90 分钟关键传球 ≥2.5 | 关键传球 <1.5 且球队进攻停滞 |
| 德尚在关键淘汰赛中释放进攻 | 1/4 决赛起 | 1/4 决赛射门 ≥15 次 | 射门 <8 次且控球率 <45% |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 半区对手提前出局 | 避免在半决赛前遭遇西班牙/英格兰 | 是 | 淘汰赛抽签和对阵结果 |
| 塞内加尔/挪威 I 组互耗 | 降低法国小组赛消耗 | 是 | I 组积分榜和伤病情况 |
| 高温天气利好体能型球队 | 法国阵容深度允许大面积轮换，高温下体能优势放大 | 是 | 比赛日气温 |
| 姆巴佩获得裁判保护 | 减少针对性犯规的干扰 | 是 | 姆巴佩被犯规后判罚率 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 3
conditions:
  - condition: 姆巴佩淘汰赛全程健康且进球效率在线
    type: precursor
    observable_proxy: 姆巴佩淘汰赛每 90 分钟进球+助攻
    settlement_rule: 淘汰赛场均进球+助攻 ≥0.8
  - condition: 中卫搭档形成稳定且有效组合
    type: precursor
    observable_proxy: 中卫组合淘汰赛零封场次
    settlement_rule: 淘汰赛阶段至少 2 场零封
  - condition: 德尚在关键淘汰赛阶段选择进攻性战术
    type: branch
    observable_proxy: 1/4 决赛起控球率和射门数
    settlement_rule: 1/4 决赛起场均射门 ≥12 次
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
| | | | | | |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（63 条预测）

- 派别分布: 主帅视角派, 伤病赛程派, 建模派, 心理抗压派, 数据派, 玄学派, 老球迷派, 赔率派, 阵容年龄派
- Kimi 聚合概率: 21.00%

#### 代表性 reason（前 5 条）

- [数据派] conf=65: "法国总身价14.8亿欧全球最高，姆巴佩2亿欧领衔6名超1亿球员，纸面实力碾压任何对手。"
- [数据派] conf=72: "法国欧国联和预选赛表现稳定，德尚谢幕战13名新人带来额外动力，1.48亿欧阵容容错率最高。"
- [数据派] conf=72: "法国非洲裔球员占比高，对美国夏季湿热气候适应性优于北欧球员，德尚最后一届战意加成。"
- [数据派] conf=72: "FIFA游戏综合能力值法国平均最高，姆巴佩91总评领衔，纸面能力值 translate 到真实胜率约19.2%。"
- [数据派] conf=60: "姆巴佩+登贝莱1对1突破成功率欧洲前三，法国个体能力在淘汰赛单点爆破中价值最高。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 I 组头名出线（德尚的务实策略确保不翻船），16 强赛稳健晋级，1/4 决赛开始姆巴佩进入爆发模式。德尚谢幕战为更衣室注入额外动力，半决赛和决赛中法国的阵容深度在高温+短恢复时间的赛制下成为决定性优势。

**最不可信叙事**: "法国纸面实力最强所以自然会赢"——2020 欧洲杯瑞士逆转已证明天赋不等于胜利。德尚的保守倾向在关键场次可能成为天花板。

**最值得赛中监控的信号**: (1) 小组赛前两场的积分和场面控制力；(2) 中卫搭档的稳定性和零封率；(3) 格列兹曼/替代组织者的关键传球数据。

**如果夺冠，哪些赛前判断有价值**: (1) 德尚谢幕战的情感凝聚力是不可量化的加成；(2) 法国阵容深度在 48 队赛制的多轮淘汰中是最大结构性优势；(3) 姆巴佩在淘汰赛阶段的个体能力是所有球队中最难以防守的变量。
