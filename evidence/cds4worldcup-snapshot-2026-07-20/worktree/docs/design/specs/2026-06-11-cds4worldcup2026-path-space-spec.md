# CDS4WorldCup2026 — 48 队夺冠路径推演与可校准知识空间 Spec

> **类型**: research-product-spec
> **状态**: draft-for-immediate-execution
> **日期**: 2026-06-11
> **创建日期**: 2026-06-11
>
> **PRIMARY_GOAL**: 将 2026 世界杯从“预测冠军”的点估计问题，转化为 48 支球队“在什么条件下可能夺冠”的条件路径空间问题；以 Plan 0 完成分叉复制与资产迁移，以 Plan A 执行夺冠路径推演主线，并保留 MVP-0 决策树作为 Plan B、MVP1&2 Factor Ledger 实验作为 Plan C 兜底方案。

---

## 1. 一句话方案

CDS4WorldCup2026 不直接回答“谁会夺冠”，而是为 48 支球队分别生成一张 **Championship Path Simulation Card**：

> 假设这支球队最终夺冠，世界必须怎样变化？

每张路径卡回答：

- 它必须破解哪些结构性阻力。
- 它需要哪些黑天鹅或路径助力。
- 它的夺冠路径依赖硬实力、签运、低比分防守、点球大战、巨星爆发、环境适应，还是强队自毁。
- 这些判断中哪些能进入 Factor Ledger 被赛后校准，哪些只能作为 Marginalia 语义边注保留。

---

## 2. 项目边界

### 2.1 项目定位

本项目是 CDS 方法论在世界杯场景中的独立实验仓库，继承 CDS 的核心思想：输出决策空间、风险边界、条件路径和可审计知识，而不是输出单点答案。

世界杯是理想测试场，因为它具备：

- 明确参赛主体：48 支球队。
- 明确路径结构：小组赛、淘汰赛、决赛。
- 高不确定性：冷门、红牌、伤病、点球、天气、旅途、心理压力。
- 可结算性：比赛结果和关键事件可在赛后判定。
- 公开讨论丰富：Kimi 白皮书、Kimi 300 Agent、赔率、媒体和公开统计均可作为材料。

### 2.2 非目标

本项目明确不做：

- 不做投注建议。
- 不做收益率、仓位、PnL、Sharpe、Max Drawdown。
- 不宣传“AI 预测世界杯”。
- 不声称 CDS 打败 Kimi、赔率或其他公开 AI。
- 不把 Kimi 300 Agent 当成 300 个独立专家。
- 不强行把所有叙事转为可判定因子。
- 不在数据门控和路径卡 MVP 之前建设 dashboard。

---

## 3. 总体路线

本项目采用四个 plan：

```text
Plan 0: CDS4WorldCup 分叉复制方案
  -> 从 CDS4Polymarket 迁移可复用方法、数据、知识和 fixtures

Plan A: 48 队夺冠路径推演主线
  -> 输出条件路径空间，不做点预测中心化

Plan B: MVP-0 决策树
  -> 判断 Kimi / AI 群体数据是否值得进入校准扩展

Plan C: MVP1&2 兜底方案
  -> 即使 Plan A/B 不收敛，仍保留原 Factor Ledger 协议闭环
```

四者不是互斥关系：

- Plan 0 是分叉项目的资产迁移与边界固化步骤。
- Plan A 是项目北极星和主产品形态。
- Plan B 是开赛前的数据与研究方向门控。
- Plan C 是方法论兜底，确保至少能交付可预注册、可结算、可审计的 Factor Ledger MVP。

---

## 4. Plan 0：CDS4WorldCup 分叉复制方案

### 4.1 Plan 0 目标

Plan 0 回答：

> 这个新分叉项目应该从 CDS4Polymarket 复制什么、总结什么、排除什么，才能独立执行 Plan A/B/C？

Plan 0 的完成标准不是“复制越多越好”，而是让 CDS4WorldCup2026 拥有足够的原始材料、协议模板、知识背景和 fixture，且不会继承 CDS4Polymarket 中与本实验无关的产品、投注或历史包袱。

### 4.2 本次分叉应该做什么

CDS4WorldCup2026 的独立职责：

- 保存世界杯场景下的路径推演、数据门控、Factor Ledger 和赛后校准资产。
- 将 Kimi、赔率、公开统计和比赛事实按 source policy 分级管理。
- 让 Plan A/B/C 共享同一套球队 registry、source ledger、Factor Ledger schema、settlement pipeline 和报告目录。
- 输出 Markdown / CSV / YAML 优先的可审计 artifact，而不是先建设 dashboard。
- 把 CDS 方法论迁移为世界杯专用的轻量实验仓库，而不是复制完整 CDS 产品。

明确不做：

- 不复制完整 CDS 前端或后端应用作为第一阶段依赖。
- 不复制与世界杯实验无关的业务文档、客户交付材料或旧项目状态。
- 不把 Kimi UI 直接作为本项目 UI 基线。
- 不把 CDS4Polymarket 的实验输出当成本项目结论，只作为 provenance、fixture 和协议参考。

### 4.3 可直接从 CDS4Polymarket 复制的部分

建议先做“冻结快照 + 活跃复制”两层。

冻结快照用于追溯，不直接作为活跃输入：

```text
source:
  <CDS4POLYMARKET>/experiments/worldcup-2026-factor-calibration/
target:
  archive/cds4polymarket/worldcup-2026-factor-calibration/
```

活跃复制用于 Plan A/B/C 直接执行：

| 来源 | 目标 | 用途 |
|---|---|---|
| `experiments/worldcup-2026-factor-calibration/methodology_disclosure.md` | `docs/imports/cds4polymarket/methodology_disclosure.md` | 方法边界与披露 |
| `experiments/worldcup-2026-factor-calibration/protocol.md` | `docs/imports/cds4polymarket/protocol.md` | Plan C 协议基线 |
| `experiments/worldcup-2026-factor-calibration/factor_adjudication_rubric.md` | `docs/imports/cds4polymarket/factor_adjudication_rubric.md` | Factor 判定规则基线 |
| `experiments/worldcup-2026-factor-calibration/data/source_ledger.md` | `data/source-ledger/cds4polymarket-source-ledger.md` | 来源登记样例 |
| `experiments/worldcup-2026-factor-calibration/data/derived/official_schedule_snapshot.csv` | `data/raw/cds4polymarket/official_schedule_snapshot.csv` | 赛程快照 fixture，需再核验 |
| `experiments/worldcup-2026-factor-calibration/schemas/*.schema.yaml` | `src/factor_ledger/schemas/` | Prediction / Factor / Settlement schema |
| `experiments/worldcup-2026-factor-calibration/templates/worldcup_*.md` | `docs/templates/worldcup/` | Prediction card 与 system prompt 模板 |
| `experiments/worldcup-2026-factor-calibration/analysis/*.csv` | `artifacts/fixtures/cds4polymarket/analysis/` | 历史分析 fixture |
| `experiments/worldcup-2026-factor-calibration/predictions/` | `artifacts/fixtures/cds4polymarket/predictions/` | Plan C 示例输入 |
| `experiments/worldcup-2026-factor-calibration/factor-ledger/` | `artifacts/fixtures/cds4polymarket/factor-ledger/` | Factor Ledger 示例 |
| `experiments/worldcup-2026-factor-calibration/settlement/` | `artifacts/fixtures/cds4polymarket/settlement/` | Settlement 示例 |
| `experiments/worldcup-2026-factor-calibration/reports/*.md` | `artifacts/fixtures/cds4polymarket/reports/` | failure / knowledge update 示例 |

复制规则：

- `archive/` 中保留原始相对结构，不改写内容。
- 活跃复制路径中的文件可以在后续 spec 中改写，但必须保留来源说明。
- 不修改本仓库根目录 `schema/`、`templates/`、`example/`，这些属于 Marginalia 协议；世界杯实验 schema 放入 `src/factor_ledger/schemas/` 或 `docs/templates/worldcup/`。

### 4.4 应复制或重写为 wiki 的知识点

以下内容不建议盲目整文件搬运，而应在 `wiki/` 中摘要重写，并链接原始来源：

| 知识点 | CDS4Polymarket 来源 | CDS4WorldCup 目标 |
|---|---|---|
| CDS 战略控制闭环 / S5 知识有效性 | `docs/concepts/cds-strategic-control-loop.md` | `wiki/concepts/cds-strategic-control-loop.md` |
| Factor Ledger 与 Decision Sentinel | `docs/concepts/factor-ledger-and-decision-sentinel.md` | `wiki/concepts/factor-ledger-and-decision-sentinel.md` |
| 世界杯 Factor Calibration 实验协议 | `docs/design/specs/2026-06-09-worldcup-factor-calibration-experiment-design.md` | `wiki/decisions/worldcup-factor-ledger-protocol.md` |
| Kimi 因子池动态校准方案 | `docs/design/specs/2026-06-11-kimi-factor-dynamic-calibration-basic-plan.md` | `wiki/decisions/kimi-factor-calibration-boundary.md` |
| Kimi 300 Agent 综合与风险 | `docs/design/specs/2026-06-10-kimi-300-agent-brainstorm-synthesis-v2.md` | `wiki/decisions/kimi-300-agent-data-boundary.md` |
| 世界杯论文路线与实验优化 | `docs/design/specs/2026-06-10-worldcup-paper-track-and-experiment-optimization-design.md` | `wiki/decisions/worldcup-research-track-map.md` |
| 数据门控、codability、Neff、adjudication yield | 本 spec 与前序讨论 | `wiki/concepts/ai-prediction-audit-boundary.md` |

必须保留的知识约束：

- Kimi 是 Red Source / candidate seed / baseline，不是事实 Green Source。
- 300 Agent 不能默认等同于 300 个独立专家。
- 可判定因子必须有 observable proxy、时间窗口、settlement rule 和来源。
- 不可判定但有解释价值的内容进入 Marginalia，不强行进入 Factor Ledger。
- 赛前 artifact 要 lock / timestamp，赛后只能 settlement 和 knowledge update，不能回填赛前判断。
- 本项目不输出投注建议、仓位、赔率价值或收益指标。

### 4.5 Kimi 数据与代码复制边界

Kimi 原始数据建议复制到唯一 canonical 路径：

```text
data/raw/kimi/
```

必须复制：

| 来源 | 目标 | 用途 |
|---|---|---|
| `worldcup-kimi/2026_World_Cup_White_Paper.pdf` | `data/raw/kimi/2026_World_Cup_White_Paper.pdf` | 白皮书基线、Plan B 数据可用性 |
| `worldcup-kimi/2026世界杯数据全景工作簿.xlsx` | `data/raw/kimi/2026世界杯数据全景工作簿.xlsx` | 球队与数据表候选来源，需核验 |
| `worldcup-kimi/kimi_300_unpacked/wc2026_aggregation.json` | `data/raw/kimi/kimi_300_unpacked/wc2026_aggregation.json` | 300 Agent 聚合数据 |
| `worldcup-kimi/kimi_300_unpacked/*_predictions.json` | `data/raw/kimi/kimi_300_unpacked/` | 逐 agent prediction 数据 |
| `worldcup-kimi/kimi_300_unpacked/wc2026_data.md` | `data/raw/kimi/kimi_300_unpacked/wc2026_data.md` | Kimi 整理材料，Yellow/Red Source |

可选复制：

| 来源 | 目标 | 用途 |
|---|---|---|
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/data.js` | `archive/kimi-ui-reference/wc2026_predict/data.js` | UI 数据结构参考 / parser fixture |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/index.html` | `archive/kimi-ui-reference/wc2026_predict/index.html` | UI 参考，不作为本项目 UI 基线 |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/hero-bg.mp4` | `archive/kimi-ui-reference/wc2026_predict/hero-bg.mp4` | 视觉参考，不进入数据分析 |

暂不复制：

- `worldcup-kimi/extracted_kimi_agent/`：它与 `kimi_300_unpacked/` 内容重复，避免双源污染。若后续发现差异，只在 source ledger 记录差异后再处理。
- `worldcup-kimi/*.zip`：作为外部原始包可暂留在原仓库，不进入 Plan B 的第一批输入。
- Kimi UI 升级代码：不作为 CDS4WorldCup 的前端基础。

### 4.6 前端与可视化策略

第一阶段不建立新的前端 UI spec，也不接入完整 CDS 前端。

原因：

- Plan A/B/C 的关键风险在数据可用性、路径卡表达、Kimi reason 可恢复性、Factor Ledger 协议闭环和 settlement pipeline，不在界面。
- 过早做 dashboard 会把项目拉回“冠军榜 / 热力榜”叙事。
- 当前 Markdown / CSV / YAML artifacts 足够支撑 MVP-A1、Plan B 阶段 0-1 归档、Plan B2 暂缓记录和 Plan C schema 复用。

后续只有在满足以下条件后，才单独创建 UI / 绘图 spec：

- MVP-A1 48 队薄切片路径卡完成，并证明卡片结构能覆盖全量球队。
- Plan B 完成数据可用性门控；Plan B2 已明确是否继续或暂缓。
- Team Path Card、Path Matrix、Factor Ledger 三类输出字段稳定。
- 明确需要展示“路径空间”而不是“预测榜单”。

若创建 UI spec，建议文件为：

```text
docs/design/specs/YYYY-MM-DD-worldcup-path-space-visualization-ui-spec.md
```

推荐 UI 原则：

- 先做静态图表和 Markdown report，再考虑交互式前端。
- 如需复用现有系统，应优先基于 CDS / Policysim 前端的报告与决策空间模式，而不是 Kimi UI。
- Kimi `wc2026_predict/` 只作为外部 UI 数据结构参考，不作为代码继承对象。

### 4.7 Plan 0 完成标准

Plan 0 完成时应具备：

- `archive/cds4polymarket/worldcup-2026-factor-calibration/` 冻结快照。
- `data/raw/kimi/` 中有唯一 canonical Kimi 数据副本。
- `docs/imports/cds4polymarket/` 中有方法、协议、rubric。
- `src/factor_ledger/schemas/` 中有世界杯实验 schema。
- `docs/templates/worldcup/` 中有世界杯 prediction card / system 模板。
- `artifacts/fixtures/cds4polymarket/` 中有历史 prediction / factor / settlement fixture。
- `wiki/` 中记录关键迁移知识点和边界。
- `docs/source-policy.md` 与迁移后的 source ledger 一致。

---

## 5. Plan A：48 队夺冠路径推演主线

### 5.1 核心问题

对每支球队，不问“它夺冠概率是多少”，而问：

> 如果这支球队最终夺冠，它需要破解哪些阻力？需要哪些条件同时成立？

### 5.2 方法架构

```text
公开数据 / Kimi 数据 / 赛程结构
  -> 数据门控与字段对齐
  -> 初始球队状态建模
  -> Markov / Monte Carlo 路径推演
  -> 夺冠路径推演分析
  -> Bayesian 因子与球队状态更新
  -> Factor Ledger / Marginalia 双轨记录
  -> 阶段性路径卡更新
  -> 赛后校准与知识回写
```

### 5.3 数据依赖闸门

本项目必须区分 **可先做的骨架** 和 **必须等数据分析后才能定的模型/分类/权重**。否则很容易把研究者直觉写进代码，再让后续数据“证明”这个直觉。

| 开发项 | 是否可先开发 | 必须等待的数据分析 | 原因 | 允许的前置产物 |
|---|---|---|---|---|
| 48 队 registry | 可以 | Plan 0 数据复制、赛程/球队来源核验 | 这是所有后续工作的主键 | `team_registry.csv` |
| Team Path Card 模板 | 可以 | 不需要等完整数据，但必须支持 `thin/missing` | 模板是容器，不是结论 | Markdown 模板 |
| Path Type taxonomy | 不可以 | 48 队 `path_signals` 矩阵；Kimi reason 仅在通过 recoverability gate 后作为辅助 | 分类必须从全量分布中归纳，不能等待或依赖 Kimi reason | 候选 signal 词表 |
| `tier` / 强弱档位 | 不可以定死 | 官方排名、Elo/历史结果、Kimi/市场覆盖状态 | 档位会影响路径解释，不能靠印象 | `tier_status: unassigned` |
| 初始实力参数 | 不可以定死 | Green/Yellow source 可用性和缺口报告 | Markov/Bayesian 的参数源会决定模型含义 | 参数字段占位 |
| Markov / Monte Carlo 引擎 | 可以做接口，不做正式参数 | 48 队 registry、小组/bracket、初始实力 proxy | 没有转移概率时只能跑空壳 | engine skeleton / dry-run |
| Bayesian 更新权重 | 不可以 | Plan C 可结算因子 yield、历史 anchoring；Kimi reason 需先通过 recoverability gate | 权重应来自可结算信号，不是直觉 | 更新接口 |
| Factor Ledger 入账阈值 | 部分可以 | Plan C 协议规则；Kimi reason 暂不作为入账来源 | 阈值过严/过松都会扭曲发现 | 最小入账规则 |
| 黑天鹅/阻力排行 | 不可以 | 48 队薄切片矩阵完成 | 排行必须来自全量矩阵 | 维度字段 |
| 4 队深描样本 | 可以 | 48 队薄切片至少已启动 | 深描是 QA，不是范围替代 | QA 样本清单 |
| UI / 可视化 | 不可以 | Path Card / Matrix / Ledger 字段稳定 | 否则 UI 会固化错误结构 | 静态 Markdown/CSV |
| 论文主张 | 不可以 | Plan A1/A2 结果 + Plan C 闭环结果；Plan B 只作为输入质量边界 | 主张必须从数据门控出口长出来 | 论文候选列表 |

执行原则：

- **先做 registry、source inventory、模板、copy manifest。**
- **再做 48 队薄切片和 MVP-0 数据分析。**
- **最后才定 taxonomy、权重、排行、UI 和论文主张。**

### 5.4 三个技术层

#### Markov / Monte Carlo 路径层

用途：模拟赛事状态如何从小组赛推进到冠军。

输入：

- 48 队名单。
- 小组结构。
- 晋级规则。
- 淘汰赛 bracket 规则。
- 初始球队实力参数。
- 单场胜平负或晋级概率。

输出：

- 每队夺冠路径样本。
- 最常见夺冠路径。
- 最脆弱路径节点。
- 最可能遭遇的强敌。
- 路径难度指数。
- 路径依赖程度。

说明：Markov 层不是论文主张，只是路径生成引擎。

#### Bayesian 更新层

用途：根据比赛事实更新球队状态和因子可信度。

更新对象：

- 球队进攻状态。
- 防守稳定性。
- 伤病与阵容状态。
- 旅途与体能负担。
- 战术适配。
- 点球 / 门将 / 淘汰赛抗压能力。
- 因子有效性。

说明：Bayesian 层不直接作为“最新冠军榜”宣传，只服务路径卡更新。

#### 夺冠路径推演层

用途：把路径样本翻译成 CDS 风格的解释性产物。

每队回答：

- 这支球队最现实的夺冠路径是什么。
- 哪一轮是最大死亡关。
- 它必须避开哪些对手。
- 它需要哪些强队提前出局。
- 它需要哪些自身状态改善。
- 它最依赖哪类方差。
- 如果它夺冠，事后最可能被解释为哪种故事。

### 5.5 Path Type 分类

Path Type 不能在数据分析前固定。它不是研究者先拍脑袋指定的分类法，而是 Plan A0 / A1 之后基于 48 队 `path_signals` 矩阵生成的 **data-derived taxonomy**。Kimi reason 只有在通过 recoverability gate 后才能作为辅助材料。

在数据完成前，只允许使用 `path_signals` 描述球队暴露出的路径信号，不给出最终 `path_type`。例如：

- `base_strength_signal`
- `bracket_signal`
- `low_scoring_signal`
- `penalty_signal`
- `injury_signal`
- `depth_signal`
- `superstar_signal`
- `climate_travel_signal`
- `favorite_collapse_dependency`
- `narrative_only_signal`

Path Type 的生成顺序：

1. Plan A0 建立 48 队 registry、赛程结构、基础实力 proxy 和来源缺口。
2. Plan A1 为 48 队各写一张薄切片路径卡，只记录 `path_signals` 和证据状态。
3. Plan B 阶段 0-1 提供 Kimi 覆盖限制；Plan B2 暂缓后，不再把 Kimi reason 作为 Path Type 前置输入。
4. 基于 48 队 `path_signals` 矩阵归纳 Path Type taxonomy；Kimi reason 仅在通过 recoverability gate 后作为辅助证据。
5. 每个 Path Type 必须有定义、证据阈值、代表球队、反例和不确定性说明。

候选词表可以作为标注辅助，但不得在 MVP-A0/A1 前当作最终分类使用：

| 类型 | 含义 |
|---|---|
| `dominant_favorite` | 硬实力碾压型 |
| `bracket_leverage` | 路径套利型 |
| `low_variance_defense` | 低比分防守型 |
| `penalty_survival` | 点球 / 门将方差型 |
| `superstar_spike` | 单核爆发型 |
| `youth_surge` | 年轻阵容体能爆发型 |
| `veteran_tournament_craft` | 老将淘汰赛经验型 |
| `host_climate_edge` | 东道主或环境适应型 |
| `favorite_collapse_required` | 强队自毁依赖型 |
| `narrative_only` | 主要依赖不可判定叙事，暂不进入强模型 |

验收规则：

- MVP-A1 完成前，`path_type` 必须标记为 `unassigned` 或 `provisional`。
- MVP-A2 才允许发布 `docs/path-type-taxonomy.md`。
- 若数据不足以支持分类，应保留 signal matrix，而不是强行分类。

### 5.6 核心产物

#### Team Path Card

建议路径：

```text
artifacts/team-cards/<team_slug>.md
```

最小字段：

```yaml
team: Morocco
tier: unassigned
tier_status: pending_data_gate
baseline_probability_status: not_estimated
path_type: unassigned
path_type_status: unassigned
path_signals:
  - low_scoring_signal
  - penalty_signal
  - favorite_collapse_dependency
primary_obstacles:
  - elite_attacking_gap
  - bracket_strength
  - squad_depth
required_breakthroughs:
  - win_group_or_avoid_top_seed
  - force_low_scoring_knockout_games
  - goalkeeper_overperformance
black_swan_helpers:
  - favorite_injuries
  - penalty_shootout_cluster
  - bracket_collapse
miracle_package:
  minimum_conditions: 4
  description: "..."
calibration_status: tracking
```

#### 48 队路径矩阵

建议路径：

```text
artifacts/path-matrix/worldcup2026_path_matrix.csv
```

核心列：

- `team`
- `tier`
- `path_type`
- `path_type_status`
- `path_signals`
- `coverage_status`
- `base_strength`
- `path_difficulty`
- `black_swan_dependency`
- `upset_dependency`
- `penalty_dependency`
- `injury_sensitivity`
- `bracket_dependency`
- `championship_path_count`
- `dominant_failure_node`

#### Factor Ledger

建议路径：

```text
artifacts/factor-ledger/*.yaml
```

只记录可判定因子：

- 有 observable proxy。
- 有时间窗口。
- 有支持 / 削弱 / 反证判定规则。
- 有来源。
- 有赛后 adjudication。

#### Marginalia Ledger

建议路径：

```text
artifacts/marginalia/*.md
```

记录不能强行账本化但有语义价值的内容：

- 球迷叙事。
- 心理判断。
- 历史隐喻。
- 玄学类 reason。
- 模型无法验证但可能解释人类信念的材料。

### 5.7 Plan A MVP 阶段

#### MVP-A0：数据门控

目标：确认能否建模。

产物：

- 48 队名单。
- 小组赛结构。
- Kimi Top8 / 300 Agent 覆盖情况。
- 球队名称映射表。
- 数据缺口报告。
- 初始可用 proxy 清单。

成功标准：

- 48 队可唯一映射。
- 小组结构可编码。
- 至少能标注 48 队 `coverage_status`。
- Kimi 300 Agent reason 可抽样读取。

#### MVP-A1：48 队薄切片路径卡

目标：48 支球队全部覆盖，而不是先只做几支代表队。

输出：

- 48 张薄切片路径卡。
- 1 张 48 队路径矩阵初版。
- 每队的 `path_signals`，但不强行给最终 `path_type`。
- 每队的来源状态：`sufficient` / `partial` / `thin` / `missing`。

成功标准：

- 48 队都有一张最小路径卡。
- 每张卡至少包含 2 个主要阻力。
- 每张卡至少包含 1 个可追踪的 `path_signal`。
- 数据不足的球队被明确标记为 `thin` 或 `missing`，不靠想象补齐。
- `path_type` 保持 `unassigned` / `provisional`，等待 MVP-A2 数据派生分类。
- 读者不会把它误解成投注建议。

#### MVP-A1-QA：4 队深描质检样本

4 队不再是范围替代，只用于检查模板是否足够表达不同路径。

建议选：

- 1 支顶级热门，例如西班牙 / 法国。
- 1 支传统强队，例如阿根廷 / 巴西 / 德国。
- 1 支中强队，例如葡萄牙 / 荷兰 / 英格兰。
- 1 支黑马，例如摩洛哥 / 日本 / 挪威 / 克罗地亚。

输出 4 张加厚版路径卡，用于质检：

- 是否能从薄切片升级为深描。
- 是否能区分 Factor Ledger candidates 与 Marginalia。
- 是否暴露模板字段不足。

#### MVP-A2：数据派生 Path Type taxonomy

目标：在 48 队薄切片和 Plan B 数据分析后，再生成 Path Type taxonomy。

产物：

- `docs/path-type-taxonomy.md`。
- `artifacts/path-matrix/worldcup2026_path_signal_matrix.csv`。
- `artifacts/path-matrix/worldcup2026_path_type_assignment.csv`。
- 每个 Path Type 的定义、证据阈值、代表球队、反例。

成功标准：

- 分类来源于 48 队 signal matrix 和数据门控结果。
- 每个分类有数据依据；无法支持的候选类型被删除或合并。
- 不把叙事相似误判为可判定因子相似。

#### MVP-A3：48 队完整路径矩阵

目标：把全量薄切片升级为可比较路径空间。

产物：

- 48 队完整路径矩阵。
- 48 张标准路径卡。
- 黑天鹅依赖排行。
- 阻力类型排行。
- `path_type` 分布和不确定性说明。

#### MVP-A4：赛事滚动更新

节奏：

- 小组赛后更新一次。
- 32 / 16 强后更新一次。
- 8 强后更新一次。
- 半决赛后更新一次。
- 决赛后完成校准复盘。

---

## 6. Plan B：MVP-0 决策树 v2

### 6.1 Plan B 目标

Plan B 回答：

> Kimi / AI 群体数据值不值得被纳入扩展校准实验？

它不回答 CDS 协议能否运行，也不替代 Plan A 的路径空间主线。

Plan B 的最佳窗口是世界杯开赛前，因为大部分分析不需要比赛结果。

### 6.2 当前状态与总体结构

Plan B 已完成阶段 0-1。MVP-0 数据门控结论为 `pass_with_limitations`：Kimi 聚合数据字段完整，300 条 reason 可读入，但 reason 文本呈现明显的压缩黑话、人设独白、数据碎片、模型声称和推论判断混合。

因此 Plan B2 从原先的 `Codability Pilot` 调整为 **Reason Recoverability Gate**。这不是项目总卡点，而是 Kimi reason 进入 Factor Ledger 的局部卡点。

```text
阶段 0  [直觉锚定]              已完成：读 30 条 reason，形成直觉笔记
  ↓
阶段 1  [数据可用性]            已完成：pass_with_limitations
  ↓
阶段 2  [Reason Recoverability] 局部卡点：暂缓，不阻塞 Plan A / Plan C
  ↓
阶段 3  [Neff / 派别结构]       暂缓：可独立分析 champion/top3，但不解决文本可恢复性
  ↓
阶段 4  [耦合检验]              暂缓：需先有 recoverability / codability 标签
  ↓
阶段 5  [历史 Anchoring]        暂缓：需先有可恢复、可查、可结算的 reason 子集
```

### 6.3 阶段 0：直觉锚定

状态：已完成。

产物：

- `artifacts/reports/mvp0-intuition-notes.md`
- `data/processed/kimi_reason_sample_30.csv`

关键发现：30 条 reason 能提供直觉锚定，但不能承担正式 codability 结论。样本中出现大量混合句，例如人设开场、事实碎片、模型声称和判断结论压缩在同一句内。

### 6.4 阶段 1：数据可用性

状态：已完成。

产物：

- `artifacts/reports/mvp0-data-gate-report.md`
- `data/processed/kimi_agent_inventory.csv`
- `data/processed/team_registry.csv`
- `data/processed/team_name_map.csv`

结论：`pass_with_limitations`。

通过项：

- 300 条 Agent 预测核心字段完整。
- 10 个派别各 30 条，分布均匀。
- reason corpus 可读入。

限制项：

- Kimi 数据只覆盖 21/48 队。
- 174/300 agent 仅存在于 aggregation 中，没有单独 prediction 文件。
- reason 文本高度压缩，不适合直接交给普通人做正式 codability 标注。

### 6.5 阶段 2：Reason Recoverability Gate

状态：**deferred-local-blocker**。

#### 6.5.1 为什么从 Codability 改成 Recoverability

原计划直接做 codability 标注，但数据分析显示这一步跳得太快。许多 Kimi reason 不是完整论证，而是：

- 人设独白，例如“1966 年刚出生，这辈子等足球回家”。
- 可查事实碎片，例如“贝林厄姆 1.63 亿欧”。
- 模型黑箱声称，例如“协同过滤将西班牙与历史冠军模板特征匹配”。
- 推论判断，例如“+500 虽热但合理”。
- 省略主谓宾的足球黑话。

如果直接让人类标注“是否可审计”，标注结果可能测到的是“普通人能不能读懂压缩文本”，而不是“AI reason 是否可进入 Factor Ledger”。

#### 6.5.2 新门控问题

阶段 2 只回答三个更基础的问题：

| 门控 | 问题 | 失败含义 |
|---|---|---|
| 可读性 | 人类能否看懂原文在说什么 | 原文不适合直接标注 |
| 可恢复性 | 能否把原文改写成普通中文且不改变原意 | 无法进入 fact-check / Factor Ledger |
| 可查性 | 恢复后的清楚主张里是否有事实片段可以核验 | 只能做 Marginalia 或 Red Source |

#### 6.5.3 当前决策

阶段 2 阻塞的是 **Kimi reason 作为 Factor Ledger 输入**，不是 CDS4WorldCup 项目整体。

| 对象 | 是否被阻塞 | 说明 |
|---|---|---|
| Kimi reason 进入 Factor Ledger | 是 | 必须先证明 reason 可恢复为清楚主张 |
| Kimi reason 作为 Marginalia / Red Source | 否 | 可继续作为叙事材料、baseline、候选线索 |
| Plan A 48 队夺冠路径推演 | 否 | Plan A 可用 Green / Yellow Source 独立推进 |
| Plan C MVP1&2 Factor Ledger 协议闭环 | 否 | Plan C 不依赖 Kimi reason 质量 |
| Path Type taxonomy | 部分影响 | 不再等待 Kimi codability 结论；以 Plan A1 的 48 队 signal matrix 为主依据 |

#### 6.5.4 暂缓的人类标注

已生成的人类标注包保留为实验材料，但暂不发送 300 条正式标注。未来只有满足以下条件之一才恢复：

- 需要写“AI 预测理由可读性 / 可恢复性边界”的短文。
- Plan A1 完成后，确实需要从 Kimi reason 中提取候选信号。
- 有足够时间先做 30-50 条小样本 recoverability check。

若恢复，顺序必须是：

1. 研究者或 LLM 先为 reason 生成普通中文释义，不添加新事实。
2. 人类小样本检查 30-50 条：原文是否看懂、释义是否保真、是否有可查片段。
3. recoverability 通过后，再做 codability / Factor Ledger candidate 标注。

### 6.6 阶段 3：Neff / 派别结构

状态：暂缓，不作为 Plan A1 前置。

Neff / 派别结构仍可基于全量 300 条 `champion` / `top3` / `confidence` 独立运行，但它不能解决 reason 文本可恢复性问题。因此现阶段不再把 Neff 放在 Plan A1 前面。

恢复条件：

- 需要判断“300 Agent 是否真的有独立认知结构”。
- 或需要为论文短文 `Three Hundred Echoes` 提供证据。

### 6.7 阶段 4：耦合检验

状态：暂缓。

只有当阶段 2 产生稳定的 recoverability / codability 标签后，才有必要检验“可恢复性 / 可审计性是否与派别结构相关”。

### 6.8 阶段 5：历史 Anchoring

状态：暂缓。

历史 anchoring 需要一个可恢复、可查、可结算的 reason 子集。当前 Kimi reason 尚未通过 recoverability gate，因此不应提前投入 2022 历史结算。

### 6.9 Plan B 当前出口

当前出口不是原来的 A-E 论文路径，而是一个工程决策：

> Plan B2 暂停为局部卡点；Kimi reason 暂不进入 Factor Ledger；项目主线转向 Plan A1 和 Plan C。

具体执行：

- 继续 Plan A1：48 队薄切片夺冠路径推演卡。
- 继续 Plan C：MVP1&2 Factor Ledger 协议闭环准备。
- Kimi reason 保留为 Red Source / Marginalia / 候选线索，不作为可结算因子来源。

---

## 7. Plan C：MVP1&2 兜底方案

### 7.1 Plan C 目标

Plan C 回答：

> 即使 Kimi 数据不可用、codability 不稳定、Neff 不成立，CDS 协议本身能否跑通？

Plan C 是兜底方案，不依赖 Kimi 数据是否高质量。

### 7.2 Plan C 与 Plan B 的区别

| 维度 | Plan C: MVP1&2 | Plan B: MVP-0 |
|---|---|---|
| 研究对象 | CDS 协议 + CDS 自生成因子 | Kimi 300 Agent 数据质量 |
| Kimi 身份 | Red Source / baseline / candidate seed | 主要分析对象 |
| 时间线 | 世界杯期间实时 | 世界杯前优先完成 |
| 需要比赛结果 | 需要赛后 settlement | 大部分不需要 |
| 产出 | prediction card + factor ledger + settlement + knowledge update | 方向决策 + 数据质量报告 |
| 核心问题 | CDS 协议能不能跑通 | Kimi 数据值不值得用 |

一句话：

> Plan B 回答“Kimi 数据值不值得用来做校准”，Plan C 回答“CDS 协议能不能跑通”。

### 7.3 MVP1：单场预注册闭环

目标：验证一个比赛级 prediction card / factor ledger / settlement record 能够完整跑通。

最小流程：

```text
赛前资料
  -> source ledger
  -> prediction card
  -> factor ledger
  -> lock / timestamp
  -> 比赛发生
  -> settlement record
  -> scoring
  -> failure log
  -> knowledge update
```

最小产物：

- `prediction_card.yaml`
- `factor_ledger.yaml`
- `settlement_record.yaml`
- `source_ledger.md`
- `protocol_failure_log.md`
- `knowledge_update_log.md`

成功标准：

- 赛前锁定时间明确。
- 所有因子有 observable proxy 和 settlement rule。
- 赛后能完成至少一个 factor adjudication。
- 失败原因不被混入质量比较。

### 7.4 MVP2：小批量滚动闭环

目标：在 3-5 场比赛上重复 MVP1，观察协议稳定性。

新增要求：

- 每场比赛使用一致 schema。
- 记录 factor adjudication yield。
- 记录 inconclusive / uncodable 分布。
- 记录协议失败类型。
- 允许前序比赛的已结算知识通过结构化 update 影响后续比赛，但不能任意赛后改写赛前判断。

成功标准：

- 至少 3 场完整闭环。
- 没有赛后回填赛前 artifact。
- `inconclusive_rate` 可解释。
- 形成最小 failure taxonomy。

### 7.5 Plan C 停止条件

出现以下情况，暂停扩展，先修协议：

- 连续 3 场无法生成可判定因子。
- `inconclusive_rate` 连续高于 70%。
- 赛前 lock / hash / timestamp 缺失。
- 赛后 settlement 需要大量自由解释。
- Kimi 或赔率信息污染了 CDS Green Source 输入。

---

## 8. 四个 Plan 兼容性声明

| 维度 | Plan 0 | Plan A | Plan B | Plan C |
|---|---|---|---|---|
| 主问题 | 分叉要复制什么 | 48 队如何可能夺冠 | Kimi 数据是否值得用 | CDS 协议能否跑通 |
| 核心产物 | copy manifest / imported docs / canonical raw data | Team Path Card / Path Matrix | 决策树报告 / 数据质量报告 | Prediction Card / Factor Ledger |
| 是否依赖 Kimi | 复制 Kimi canonical raw data | 可用但不依赖 | 依赖 | 不依赖 |
| 是否依赖赛果 | 不依赖 | 滚动阶段依赖 | 历史 anchoring 依赖，主体不依赖 | 依赖 |
| 失败后价值 | 明确缺口与缺失资产 | 仍有路径解释产品 | 得到数据边界论文 | 得到协议失败记录 |
| 对 CDS 贡献 | 迁移边界和 provenance | 决策空间主输出 | 输入质量门控 | 知识有效性闭环 |

执行原则：

- 先执行 Plan 0，建立 canonical 数据副本、协议 fixture 和知识边界。
- Plan B 已完成阶段 0-1；阶段 2 标记为局部卡点后，不再阻塞主线。
- 同时用 Plan A1 做 48 队薄切片路径卡，确保全覆盖；4 队深描只作为质检样本。
- Plan C 不被 Plan B 结果阻塞；即使 Plan B 失败，Plan C 仍继续作为协议兜底。

---

## 9. 推荐执行时间线

```text
现在
  │
  ├─ Day 0-1: Plan 0 分叉复制与迁移 manifest
  │
  ├─ Day 1-2: Plan B 阶段 0-1 + Plan A 数据门控
  │
  ├─ Day 3-5: Plan B2 标记为 Reason Recoverability 局部卡点，暂不扩大人类标注
  │
  ├─ Day 3-6: Plan A1 48 队薄切片路径卡 + 4 队深描质检
  │
  ├─ Day 6-7: Plan C MVP1&2 协议闭环准备
  │
  └─ 世界杯开始后: Plan C MVP1&2 继续实时预注册与 settlement
```

并行安排：

- Plan 0 是 Plan A/B/C 的共同前置，不需要等待 UI 或路径引擎。
- Plan A1 是下一主线，因为 Plan B2 已经完成其门控职责：阻止 Kimi reason 在未恢复为清楚主张前进入 Factor Ledger。
- Plan C 可在比赛窗口独立推进，不等待 Plan B 全部完成。

---

## 10. 推荐仓库结构

```text
CDS4WorldCup2026/
  README.md
  docs/
    methodology.md
    source-policy.md
    path-type-taxonomy.md
    imports/
      cds4polymarket/
    templates/
      worldcup/
    design/
      specs/
      plans/
  data/
    raw/
      kimi/
      cds4polymarket/
    processed/
    source-ledger/
  archive/
    cds4polymarket/
    kimi-ui-reference/
  notebooks/
    exploratory/
  src/
    data_gate/
    team_registry/
    path_engine/
    bayesian_update/
    factor_ledger/
    report_generator/
  artifacts/
    fixtures/
      cds4polymarket/
    team-cards/
    path-matrix/
    factor-ledger/
    marginalia/
    reports/
  tests/
  scripts/
```

---

## 11. 第一实施包

### Task 1：建立项目目录骨架

创建：

- `data/raw/`
- `data/raw/kimi/`
- `data/raw/cds4polymarket/`
- `data/processed/`
- `data/source-ledger/`
- `archive/cds4polymarket/`
- `archive/kimi-ui-reference/`
- `docs/imports/cds4polymarket/`
- `docs/templates/worldcup/`
- `artifacts/fixtures/cds4polymarket/`
- `artifacts/team-cards/`
- `artifacts/path-matrix/`
- `artifacts/factor-ledger/`
- `artifacts/marginalia/`
- `artifacts/reports/`
- `src/data_gate/`
- `src/team_registry/`
- `src/path_engine/`
- `src/bayesian_update/`
- `src/factor_ledger/`
- `src/report_generator/`
- `tests/`

验收：

- 目录存在。
- 不覆盖现有 `schema/`、`templates/`、`example/`。

### Task 2：执行 Plan 0 复制

创建执行计划：

- `docs/design/plans/2026-06-11-plan0-fork-copy-plan.md`

复制对象：

- CDS4Polymarket 世界杯实验冻结快照。
- Plan C 所需 protocol / schema / template / fixture。
- Kimi canonical raw data。
- Kimi UI reference 的最小可选快照。

验收：

- 有 copy manifest，记录来源、目标、用途和状态。
- Kimi 只保留一个 canonical unpacked 目录。
- 复制结果不会污染 Green Source。
- Plan A/B/C 的输入路径能被后续脚本稳定引用。

### Task 3：写 source policy

创建：

- `docs/source-policy.md`

内容：

- `green_source`
- `yellow_source`
- `red_source`
- Kimi 的允许用途与禁止用途。
- 赔率 / Polymarket 的允许用途与禁止用途。

验收：

- Kimi 不作为事实 Green Source。
- 市场信息不导向投注建议。

### Task 4：写 Plan B 数据门控脚本规格

创建：

- `docs/design/plans/2026-06-11-mvp0-data-gate-plan.md`

内容：

- 阶段 0-1 的输入、输出、检查项。
- Kimi JSON / PDF / xlsx 字段检查。
- 球队名标准化规则。

验收：

- 能指导后续脚本实现。
- 不需要比赛结果。

### Task 5：写 48 队路径卡模板

创建：

- `docs/path-card-template.md`

内容：

- Team profile。
- Primary obstacles。
- Required breakthroughs。
- Black swan helpers。
- Miracle package。
- Factor Ledger candidates。
- Marginalia notes。
- Update log。

验收：

- 能直接用于 48 队 MVP-A1 薄切片。
- 支持 `path_signals`、`path_type_status`、`coverage_status`，避免过早固定 Path Type。

### Task 6：建立 48 队全覆盖清单与 4 队质检样本

输出：

- `artifacts/reports/mvpa1-four-team-selection.md`

48 队要求：

- 所有参赛队必须在 registry 中有唯一 canonical name。
- 所有球队必须有一张薄切片路径卡。
- 数据不足不能跳过，只能标记为 `thin` / `missing`。

4 队质检样本建议组合：

- 顶级热门：西班牙或法国。
- 传统强队：阿根廷或巴西。
- 中强队：葡萄牙、德国、荷兰或英格兰。
- 黑马：摩洛哥、日本、挪威或克罗地亚。

验收：

- 48 队全部进入 registry。
- 4 队样本覆盖不同 `path_signals`，而不是预设 `path_type`。
- 每队选择理由明确。

### Task 7：暂缓 UI spec

记录：

- 第一阶段不建立新的 UI / 绘图 spec。
- 等 MVP-A1 48 队薄切片路径卡和 Plan B 数据门控完成后，再判断是否创建 `worldcup-path-space-visualization-ui-spec.md`。

验收：

- spec 中明确“不先做 dashboard”。
- 若后续需要 UI，优先复用 CDS / Policysim 决策空间模式，而不是 Kimi UI。

---

## 12. 完成标准

本 spec 的第一阶段完成标准：

- Plan 0 完成复制 manifest，Kimi canonical raw data、CDS4Polymarket protocol/schema/fixture、关键知识边界均已迁移。
- Plan A 有 48 张薄切片夺冠路径推演卡，其中 4 张为深描质检样本。
- Path Type taxonomy 不在数据前固定；MVP-A2 才生成数据派生分类。
- Plan B 已完成阶段 0-1；阶段 2 标记为 Reason Recoverability 局部卡点，Kimi reason 暂不进入 Factor Ledger。
- Plan C 的 MVP1&2 不被阻塞，保留原协议兜底。
- Kimi 数据的用途被明确边界化。
- 项目不会被误解成“AI 猜冠军”或“投注系统”。

---

## 13. Readiness Review

### 13.1 Plan 0 是否清晰

结论：清晰，可以立即实施。

已写明：

- 本次分叉要做什么。
- 哪些 CDS4Polymarket 资产可以直接复制。
- 哪些知识点应重写进 `wiki/`。
- 哪些 Kimi 数据必须复制、哪些可选复制、哪些暂不复制。
- 不复制完整 CDS 前端、后端或 Kimi UI 作为第一阶段依赖。

Plan 0 的唯一前置条件是执行复制命令并生成 manifest。

### 13.2 Plan A 是否清晰

结论：MVP-A0 / MVP-A1 清晰，可以在 Plan 0 后开始；完整 Markov / Monte Carlo 引擎和最终 Path Type taxonomy 还不应立刻写。

已清楚：

- 目标是 48 队夺冠路径推演，不是证明某队必夺冠。
- MVP-A1 先做 48 队薄切片路径卡，确保全覆盖。
- 4 队深描只作为质检样本，不替代 48 队范围。
- Path Type 只能在 MVP-A1 的 48 队 `path_signals` 矩阵后数据派生，不能先验固定；Kimi reason 不再作为前置条件。
- Team Path Card、Path Matrix、Factor Ledger、Marginalia 的产物边界已定义。

尚未满足完整引擎实施条件：

- 48 队 registry 尚未落盘。
- 小组赛结构和淘汰赛 bracket 规则尚未编码。
- 初始实力参数来源尚未核验。
- Path Type taxonomy 尚未有数据依据。

因此下一步应先做 Plan A0 数据门控和 MVP-A1 48 队薄切片路径卡，不直接写 Markov engine，也不先发布 Path Type taxonomy。

### 13.3 Plan B 是否清晰

结论：清晰，可以在 Kimi 数据复制后立即实施阶段 0-1。

已清楚：

- Plan B 是 MVP-0 决策树，不替代 Plan A。
- 阶段 0-1 已完成；阶段 2 已修正为 Reason Recoverability Gate，并标记为局部卡点。
- `docs/design/plans/2026-06-11-mvp0-data-gate-plan.md` 已覆盖阶段 0-1 的执行计划。

下一步：

- 不继续扩大人类标注。
- 将 Kimi reason 保留为 Red Source / Marginalia / 候选线索。
- 主线转向 Plan A1 与 Plan C。

### 13.4 Plan C 是否清晰

结论：清晰，复制协议与 schema 后即可进入实施准备。

已清楚：

- Plan C 回答 CDS 协议是否跑通，不依赖 Kimi 数据质量。
- MVP1/MVP2 的 artifact、流程、停止条件已定义。
- 可从 CDS4Polymarket 直接复制 protocol、schemas、templates、factor adjudication rubric、prediction/factor/settlement fixtures。

下一步：

- Plan 0 复制后，检查 schema 路径与本仓库目录是否一致。
- 再决定是否把 Plan C 写成单独 implementation plan。

### 13.5 UI / 绘图 spec 是否需要现在建立

结论：暂不需要。

原因：

- 当前风险在数据与协议，不在可视化。
- Markdown / CSV / YAML 已足够完成 Plan 0、Plan A1、Plan B 阶段 0-1 归档和 Plan C 准备。
- 过早 UI 会把项目吸回热力榜或预测榜。

触发条件：

- MVP-A1 48 队薄切片路径卡完成。
- Plan B 数据门控阶段 0-1 已完成，且 Plan B2 已明确继续或暂缓。
- Path Card / Matrix / Factor Ledger 字段稳定。

触发后再创建独立 UI spec，并优先基于 CDS / Policysim 前端模式，而不是 Kimi UI。

### 13.6 是否具备分叉 + 实施 Plan 0/A/B/C 的条件

结论：具备“分叉 + Plan 0 + Plan A0/A1 48 队薄切片 + Plan B0/B1 + Plan C 准备”的条件；暂不具备“完整 48 队 Markov 引擎 + Path Type taxonomy 定稿 + 前端 UI”的条件。

可立即开始：

- Plan 0：复制资产并生成 manifest。
- Plan A0：建立 48 队 registry 与数据缺口报告。
- Plan A1：写 48 队薄切片夺冠路径推演卡，另做 4 队深描质检。
- Plan B0/B1：读 Kimi reason、跑字段 inventory。
- Plan C 准备：复制 protocol/schema/template/fixture。

暂缓：

- 完整 Markov / Monte Carlo engine。
- Path Type taxonomy 定稿。
- 新前端 dashboard。
- 论文主张定稿。

---

## 14. 相关页面

- [[concepts/cds]]
- [[concepts/decision-control-plane]]
- [[decisions/cds-business-rebuild]]

---

> [!memo] 2026-06-11 CDS4WorldCup2026 从预测问题转为条件路径空间问题
>
> 来源：用户关于分叉新项目 CDS4WorldCup2026、48 队夺冠路径推演、MVP-0 决策树和 MVP1&2 兜底方案的讨论。
> 上下文：原 Kimi 因子校准方案容易回到“预测最优因子”重力井；本 spec 将主线改为 48 队条件路径空间，同时保留 Plan B 数据门控和 Plan C Factor Ledger 兜底。
