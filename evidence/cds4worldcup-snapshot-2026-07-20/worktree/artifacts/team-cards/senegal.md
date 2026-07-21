# Championship Path Simulation Card: 塞内加尔 (Senegal)

> **类型**: path-card-mvp-a1
> **状态**: deep-description
> **日期**: 2026-06-13
> **team_slug**: `senegal`

## 1. Team Profile

```yaml
team: 塞内加尔 (Senegal)
team_slug: senegal
confederation: CAF
group: I
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
  coverage: partial
```

塞内加尔是 2022 非洲杯冠军，拥有马内（Sadio Mané）、库利巴利（Kalidou Koulibaly）、门迪（Édouard Mendy）等在欧洲顶级联赛已验证的球员。球队的物理强度和技术能力在非洲球队中独树一帜。I 组同组法国、伊拉克和挪威，与法国的对话将决定小组头名归属，挪威的哈兰德也构成实质威胁。

## 2. Championship Thesis

> 如果塞内加尔夺冠，最可能是因为马内在最后一届大赛中提供了超越年龄的领导力和进球效率，库利巴利领衔的防线在淘汰赛阶段建立了非洲球队从未有过的防守纪律性，且球队的物理强度在北美高温环境中成为碾压级优势。

## 3. Primary Obstacles

| 阻力 | 类型 | 为什么重要 | 可判定代理 |
|---|---|---|---|
| 与欧洲/南美强队的硬实力差距 | base_strength_gap | 整体技术水平和战术复杂度与顶级球队存在结构性差距 | vs 顶级对手的控球率和射门比 |
| 马内年龄和状态下滑 | injury_risk | 马内已不在巅峰期，能否在 7 场高强度比赛中保持输出存疑 | 马内每 90 分钟进球+助攻 |
| 战术体系复杂度不足 | tactical_mismatch | 面对高位压迫和复杂战术体系时，塞内加尔的应对手段有限 | 面对压迫型球队的失误率 |
| I 组法国的顶级竞争 | bracket_strength | 法国是 2018 冠军和 2022 亚军，塞内加尔与法国的硬实力差距可能决定小组排名 | I 组 vs 法国的场面数据 |
| 进攻创造力过度依赖马内 | low_scoring_dependency | 马内之外缺乏世界级进攻创造力 | 进球来源分布 |

## 4. Required Breakthroughs

| 突破 | 发生阶段 | 最低条件 | 失败信号 |
|---|---|---|---|
| I 组成功出线 | 小组赛 | 积分 ≥4 出线 | 小组未出线 |
| 马内以外的进攻输出 | 小组赛 | 至少 2 名非马内球员小组赛进球 | 全队进球 100% 来自马内 |
| 库利巴利防线零封验证 | 淘汰赛 | 至少 1 场淘汰赛零封 | 淘汰赛场场失球 ≥2 |
| 击败一支欧洲对手 | 淘汰赛 | 面对欧洲球队取胜 | 面对欧洲球队场面被动且输球 |

## 5. Black Swan Helpers

| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |
|---|---|---|---|
| 高温天气利好体能型球队 | 塞内加尔的物理强度在高温下优势放大 | 是 | 比赛日气温 |
| 法国在 I 组的消耗为塞内加尔创造机会 | I 组法国状态波动可能为塞内加尔创造取分空间 | 是 | 法国 I 组的伤病和状态 |
| 马内告别战情感爆发 | 马内可能在最后一届大赛中超常发挥 | 部分 | 马内场上表现 |
| 半区有利抽签 | 避免淘汰赛早期遭遇顶级对手 | 是 | 淘汰赛对阵表 |

## 6. Miracle Package

```yaml
minimum_conditions_count: 5
conditions:
  - condition: 马内淘汰赛进球效率保持在巅峰水平
    type: precursor
    observable_proxy: 马内淘汰赛每 90 分钟进球+助攻
    settlement_rule: 淘汰赛进球+助攻 ≥3
  - condition: 库利巴利防线淘汰赛场均失球 ≤1
    type: precursor
    observable_proxy: 淘汰赛失球数
    settlement_rule: 淘汰赛场均失球 ≤1
  - condition: 找到马内以外至少 2 个稳定得分点
    type: precursor
    observable_proxy: 非马内球员淘汰赛进球数
    settlement_rule: 非马内球员淘汰赛合计进球 ≥3
  - condition: 半决赛前避免遭遇法国或西班牙
    type: branch
    observable_proxy: 淘汰赛对阵表
    settlement_rule: 半决赛前不与法国/西班牙交手
  - condition: 至少 2 场淘汰赛对手核心球员缺席
    type: branch
    observable_proxy: 对手淘汰赛伤病情况
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
| | | | | | |

## 9. Marginalia Notes

### Kimi 300 Agent 摘要（3 条预测）

- 派别分布: 老球迷派, 黑马派
- Kimi 聚合概率: 1.00%

#### 代表性 reason（前 5 条）

- [老球迷派] conf=30: "2002迪奥普一球斩落卫冕冠军法国，我在达喀尔彻夜狂欢。塞内加尔FIFA第14，非洲狮血管里流淌的是从不信赔率的热血。"
- [老球迷派] conf=20: "2002年斩落法国我在达喀尔彻夜狂欢，FIFA第14 ESPN第13，马内精神永在。"
- [黑马派] conf=55: "塞内加尔半数法甲青训出品，FIFA第14却仅+5000，与法国挪威同处I组能突围即证明实力。"

> [!memo] 2026-06-11 Kimi reason 暂作为 Red Source / 候选线索保留。
> 等待 Plan B2 Codability Census 完成后决定哪些可进入 Factor Ledger。

## 10. Update Log

| 日期 | 阶段 | 更新 | 影响 |
|---|---|---|---|
| 2026-06-11 | pre-tournament | 初始薄切片版本 | MVP-A1 |
| 2026-06-11 | pre-tournament | 深描版本：填充 §2-§6, §11 | 路径空间分析可用 |

## 11. Current Interpretation

**最可信路径**: 以 I 组第二出线（在与挪威和伊拉克的竞争中占据优势），利用身体强度优势争夺小组第二。16 强赛面对非顶级对手时，塞内加尔的防守强度和反击速度可能制造惊喜。1/4 决赛是合理的上限——面对欧洲顶级球队时技术差距可能暴露。

**最不可信叙事**: "塞内加尔的物理强度可以碾压任何对手"——物理强度不等同于足球能力，面对技术型球队时单纯的强度可能被控球消解。

**最值得赛中监控的信号**: (1) 马内的进球效率和跑动距离；(2) 库利巴利防线的零封率；(3) 面对压迫型球队时的失误率。

**如果夺冠，哪些赛前判断有价值**: (1) 塞内加尔是非洲足球中最接近"欧洲化"的球队——核心球员全部在欧洲顶级联赛效力；(2) 高温环境中的物理强度优势被严重低估；(3) 马内的领导力在最后一届大赛中可能产生超常效应。
