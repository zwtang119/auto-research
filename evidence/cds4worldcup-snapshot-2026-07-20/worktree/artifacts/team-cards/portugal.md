# Championship Path Simulation Card: 葡萄牙 (Portugal)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `portugal`

## 1. Team Profile

```yaml
team: 葡萄牙 (Portugal)
team_slug: portugal
confederation: UEFA
group: K
tier: unassigned
tier_status: pending_data_gate
path_type: unassigned
path_type_status: unassigned
kimi_baseline_signals:
  - none_yet
source_status:
  green_sources: [public-football-knowledge]
  yellow_sources: [kimi-aggregation]
  red_sources: [kimi-300-agent-reasons]
  coverage: sufficient
```

葡萄牙是 2016 欧洲杯冠军，罗伯托·马丁内斯（Roberto Martínez）执教以来球队保持了稳定的进攻输出。B 席（Bernardo Silva）、布鲁诺·费尔南德斯（Bruno Fernandes）、鲁本·迪亚斯（Rúben Dias）、维蒂尼亚（Vitinha）构成的核心在俱乐部层面均是世界级。C罗（Cristiano Ronaldo）第六次参赛的象征意义巨大但战术角色待定。K 组同组哥伦比亚、刚果(金)和乌兹别克斯坦，葡萄牙在小组中实力占优但哥伦比亚构成实质威胁。

## 2. Championship Thesis

> 如果葡萄牙夺冠，最可能是因为 B 席-布鲁诺-维蒂尼亚的中场三人组在淘汰赛阶段提供了攻防两端的全面控制力，鲁本·迪亚斯领衔的防线在 7 场赛制中保持足够的零封率，且马丁内斯成功解决了 C 罗战术定位问题——让 C 罗在关键时刻作为超级替补而非首发核心。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| K 组竞争不容小觑 | bracket_strength | 哥伦比亚是 2024 美洲杯强队，刚果(金)的身体对抗也不可轻视，小组消耗需控制 | K 组累计伤病和黄牌数 |
| C 罗战术角色未解 | tactical_mismatch | C 罗坚持首发但体能和跑动已不支持高压体系，球队进攻效率受其牵制 | C 罗首发 vs 替补时球队进球效率差 |
| 中锋位置终结效率 | low_scoring_dependency | 若 C 罗不首发，替代中锋（如贡萨洛·拉莫斯）的稳定性未经大赛验证 | 中锋位置每 90 分钟 xG 转化率 |
| 边路防守被针对 | squad_depth | 坎塞洛（Cancelo）和达洛特（Dalot）攻强守弱，面对顶级边路可能暴露 | 对手边路进攻占比和成功率 |
| 历史大赛心理包袱 | psychological_pressure | 葡萄牙除 2016 欧洲杯外大赛淘汰赛阶段屡次翻车 | 关键淘汰赛的场面控制力和领先后守成能力 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| C 罗战术角色明确化 | 小组赛 | 确定且稳定的 C 罗使用方案（首发/替补/轮换）并产出结果 | 小组赛结束仍频繁更换 C 罗角色 |
| K 组出线且消耗可控 | 小组赛 | 出线且核心球员无伤无停赛 | 核心球员伤停或出线过程消耗过大 |
| 中锋位置进球效率验证 | 淘汰赛 | 无论 C 罗或替代者，中锋淘汰赛进球 ≥2 | 中锋淘汰赛 0 球 |
| K 组以头名出线 | 小组赛 | 积分 ≥7 分或净胜球优势锁定第一 | 小组第二或第三出线 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 哥伦比亚在 K 组状态波动 | 降低同组最强对手的淘汰赛竞争力 | 是 | K 组哥伦比亚的伤病和状态 |
| C 罗接受替补角色并爆发 | 释放进攻端灵活性，C 罗关键球能力在替补上场时放大 | 是 | C 罗替补上场后的进球/助攻 |
| 半区有利抽签 | 避免淘汰赛连续遭遇顶级对手 | 是 | 淘汰赛对阵表 |
| VAR 有利于进攻方 | 布鲁诺·费尔南德斯的远射和定位球获益 | 是 | VAR 判罚统计 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 4
conditions:
  - condition: B 席-布鲁诺-维蒂尼亚中场三人组淘汰赛全程健康
    type: precursor
    observable_proxy: 三人淘汰赛出场时间
    settlement_rule: 三人淘汰赛合计缺席 ≤1 场
  - condition: C 罗角色问题不成为更衣室风险
    type: precursor
    observable_proxy: C 罗公开表态和场上肢体语言
    settlement_rule: 无公开不满或场上消极表现
  - condition: 鲁本·迪亚斯防线保持零封率 ≥50%
    type: precursor
    observable_proxy: 淘汰赛零封场次
    settlement_rule: 淘汰赛至少 2 场零封
  - condition: 避免在 1/4 决赛前遭遇法国或英格兰
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 1/4 决赛前不与法国/英格兰交手
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

### Kimi 300 Agent 摘要（21 条预测）

- 派别分布: 主帅视角派, 伤病赛程派, 建模派, 心理抗压派, 数据派, 玄学派, 老球迷派, 赔率派, 阵容年龄派, 黑马派
- Kimi 聚合概率: 7.00%

#### 代表性 reason（前 5 条）

- [数据派] conf=72: "维蒂尼亚+内维斯双核驱动攻防转换效率欧洲前三，C罗第六次参赛领导力加成难以量化。"
- [赔率派] conf=55: "凯利公式显示葡萄牙+1100隐含8.3%，模型估计真实概率11.5%，维蒂尼亚+内维斯双核被系统性低估。"
- [赔率派] conf=52: "中东投注数据显示C罗第六次参赛引发阿拉伯资本大量涌入葡萄牙，+1100高赔率具备正期望值。"
- [赔率派] conf=55: "亚洲市场对葡萄牙情报反应滞后，欧洲已将+1100压至+1000，印度仍有+1150，存在套利价值。"
- [老球迷派] conf=72: "C罗41岁第六次出征创历史，葡萄牙FIFA第4且9.57亿欧身价位列前五，航海家精神不灭。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 K 组头名出线（凭实力优势力压哥伦比亚），16 强赛面对相对较弱的第三名球队，8 强赛开始展现世界级统治力。如果 C 罗接受关键替补角色，葡萄牙的进攻灵活性将成为淘汰赛阶段的隐藏优势。

**最不可信叙事**: "C罗第六次世界杯带队夺冠的完美结局"——C罗 的体能和跑动已不支持 7 场首发，强行以他为核心可能浪费中场三人的天赋。

**最值得赛中监控的信号**: (1) C 罗的首发/替补使用方案和对应进攻效率；(2) B 席和布鲁诺的关键传球数和控球率；(3) 边后卫被针对的频率和成功率。

**如果夺冠，哪些赛前判断有价值**: (1) 葡萄牙的中场三人组（B 席+布鲁诺+维蒂尼亚）是本届赛事最被低估的中场；(2) C 罗角色问题的解决方案决定了葡萄牙的上限；(3) K 组签运尚可但哥伦比亚构成实质威胁，小组赛需认真应对。
