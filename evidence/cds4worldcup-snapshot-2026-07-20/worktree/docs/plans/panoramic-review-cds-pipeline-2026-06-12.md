# 全景审阅 + CDS 推演 + 管线整合：Plan

## Goal

整合教练模型、CDS 两层推演（小组赛出线 + 夺冠路径）、Polymarket 每日赔率、前端渐进式披露设计，形成完整的升级方案审阅。覆盖前端展示设计、CDS 推演架构、每日管线流程、以及与现有升级计划的关系。

## Background

### 已锁定的设计决策（来自前几轮对话）

**前端展示**：渐进式披露——教练对位模型为主信号（最有叙事性），Elo baseline 和 Polymarket 市场赔率作为可展开层。

**CDS 推演**：两层设计——
- 第一层：小组赛出线推演（3 场对手确定，枚举 3^3=27 种情景，计算积分排名 → 出线概率 + 关键情景卡）
- 第二层：夺冠路径推演（条件概率树，填充 team cards §7 的 null 字段）

**教练模型**：XI 选择按 `(team, formation, opponent)` 缓存，赛中每日重选当天比赛的队（~12-20 LLM 调用/日）。

**管线顺序**：数据采集 → Elo 基线 → 教练模型 → CDS 推演 → 日报。

**CDS 三信号交叉**：Elo+Poisson（数值基线）、教练对位（战术深度）、Polymarket（群体智慧）。分歧本身是重要发现。

### 前端现状（来自 UX 审计）

**现有设计系统**（`site/css/portal.css`）：
- 字体：serif（Songti SC）+ monospace（标签/数值）—— 纸质报告风格
- 色板：ink(#15231e) / paper(#eef3ea) / accent(#0f6b4b) / amber(#b45309)
- 来源 badge：green/yellow/red/mixed 四级信任标签
- 可视化：水平条形图（teal→blue 渐变）、3 段概率条（home/draw/away）、热力矩阵、点阵动画

**当前前端已展示**：
- 首页：obstacle 条形图 + 热力矩阵 + AI vs 市场双柱对比图（top 8 队）
- 球队详情：3 段 win/draw/loss 概率条（Elo+Poisson）+ 3 来源 baseline 对比条
- 所有 AI 数据标注 Red Source badge + "只能参考"

**已识别的前端问题**：
- `panorama.js` 淘汰赛卡片没有概率条（代码注释 "No probability bar for knockout yet"）
- baseline 概率对 top 球队过于平坦（8.5556% 同值，binning artifact）
- 首页外部参考图柱状条重叠（`ref-fill-ai` 和 `ref-fill-market` 在同一 track）
- 首页 6 格指标板 CSS 是 2×2 grid，6 个元素布局不均

### CDS 推演现状（来自 path analysis 审计）

| 组件 | 状态 | 位置 |
|------|------|------|
| CDS 概念框架 | ✅ 叙事层 | `wiki/concepts/cds.md` |
| 48 队叙事路径分析 | ✅ team cards §2-§7 | `artifacts/team-cards/*.md` |
| Miracle Package 结构化条件 | ✅ YAML | `argentina.md:64-76` |
| Path Simulation Notes schema | ⚠️ schema 存在，**全部 null** | `argentina.md:78-86` |
| 单场预测 card schema | ✅ | `src/factor_ledger/schemas/prediction_card.schema.yaml` |
| `scripts/cds_debate.py` | ❌ 不存在 | 计划在 WI-3.5 |
| CDS 辩论输出 schema | ❌ 不存在 | 无 |
| 路径级预测 schema | ❌ 不存在 | 预测卡是单场级的 |
| 淘汰赛 bracket 路径枚举 | ❌ 不存在 | |
| 条件概率计算引擎 | ❌ 不存在 | |

### 每日管线现状

**已有**：`fetch_market_snapshot.py` → Polymarket 每日快照（`market-snapshot.yml` cron UTC 00:00）
**已有**：`numeric_odds.py` → Elo+Poisson 基线
**已有**：`build_site_data.py` → 数据管线（1405 行，`main()` at line 1431）
**计划中**：教练模型（`coach-matchup-model-2026-06-12.md`）
**计划中**：WI-4.3 daily orchestrator

### 关键文件引用

- 教练模型计划：`docs/plans/coach-matchup-model-2026-06-12.md`（已更新 WI-CM.5 为对手感知+赛中更新）
- 现有升级计划：`docs/plans/full-upgrade-2026-06-12.md`
- 前端 homepage：`site/js/homepage.js:289-339`（外部参考双柱图）
- 前端 team-detail：`site/js/team-detail.js`（概率条 + baseline 对比）
- 前端 panorama：`site/js/panorama.js:194`（`oddsMap[match_id]`）
- CI 模式：`.github/workflows/market-snapshot.yml:33`（cron → script → commit → push → pages.yml）
- 来源政策：`docs/source-policy.md`（Green/Yellow/Red 分级）
- Team card 模板：`artifacts/team-cards/argentina.md` §6 Miracle Package + §7 Path Simulation Notes

## Approach

### 1. 三信号并列（per-match，绝不融合）

每场比赛产出三个**独立**概率估计，并列存储、永不融合为单一数字：

| 信号 | 来源脚本 | 来源分级 | 变化频率 | 前端角色 |
|------|---------|---------|---------|---------|
| Elo+Poisson | `numeric_odds.py` | Red（模型） | 赛后 | 可展开基线 |
| 教练对位 | `coach_simulation.py`（WI-CM.6） | Red（模型） | 赛中每日 | **主信号**（最有叙事性） |
| Polymarket | `fetch_market_snapshot.py` | Yellow（群体智慧） | 每日实时 | 可展开参照 |

**分歧即发现**——"教练认为法国 55%，市场只给 40%"是高信息量观察，而非要消除的噪声。融合成单一数字会抹掉这层信息，也违反 source-policy.md（模型输出不得冒充事实）。

### 2. CDS 两层引擎（回答用户问题 4：是的，分两层）

两层是**独立引擎**，输入/输出/消费方都不同，解耦以避免情景枚举爆炸（27 × 条件树）：

| 层 | 输入 | 计算 | 输出 | 消费方 |
|----|------|------|------|--------|
| 小组出线 | 该队 3 场小组赛的三信号概率（对手确定） | 枚举该队 3 场 × {胜/平/负} = 27 种结果 → FIFA 排名算小组位次 | 出线概率 + 关键情景（必胜/已定/危局/已淘汰） | team-detail CDS 面板 |
| 夺冠路径 | 出线概率 + 淘汰赛 bracket + 每轮对手三信号概率 | 条件概率树（出线→R32→R16→QF→SF→Final） | 夺冠概率 + 路径阻力节点 + 填充 team-card §7 的 8 个 null 字段 | team-detail CDS 面板 + team cards |

两层解耦的关键：小组赛对手**确定**（确定性输入），夺冠路径对手**条件化**（概率输入）。分开后各自由可控。

### 3. 前端渐进式披露（回答用户问题 1：如何展示给访客）

80% 球迷要"谁赢+为什么"（对叙事有反应，对裸数字无反应），20% 数据极客要全部方法论。按此分层：

- **比赛级**（panorama + team-detail）：默认显示教练对位概率条（主信号，附阵型+XI+关键对位一句话），点击展开 Elo baseline + Polymarket 对照。淘汰赛卡片补概率条——填补 `panorama.js:418` 的 "No probability bar for knockout yet"。
- **球队级**（team-detail 新增"CDS 路径分析"区）：小组出线情景卡（27 种聚合为 3-4 个关键情景）+ 夺冠路径树（条件概率分支 + 阻力节点高亮）+ §6 Miracle Package 达成状态。
- **首页**：外部参考图从 2 柱（AI/市场）扩为 3 柱（教练/市场/Elo），教练柱用 accent 色区分。

**审美约束**：严格复用现有设计系统（`portal.css`）——serif（Songti SC）+ monospace 标签、ink/paper/accent/amber 色板、teal→blue 渐变条、Green/Yellow/Red 来源 badge。新增可视化（路径树、情景卡）用同一 warm-white panel + gradient bar 风格，**不引入新字体/新色系**。所有模型数据 Red badge + "只能参考"。

### 4. 每日管线（回答用户问题 3：AI 自动化）

```
凌晨 cron（daily-update.yml 链序）:
  ① Polymarket 快照（已有 market-snapshot.yml 模式）
  ② Elo+Poisson 基线（numeric_odds.py，零 LLM）
  ③ 教练模型当日重选（coach_simulation.py --phase=select-xi，仅当天比赛的 4-6 队，~12-20 LLM 调用）
  ④ 教练模拟（coach_simulation.py --phase=simulate，零 LLM）
  ⑤ CDS 推演（cds_path_simulation.py）
       — 小组出线：赛况变化时重算受影响队
       — 夺冠路径：赛前全量一次 + 小组赛阶段结束后重算（对手确定）
  ⑥ 日报（综合三信号 + CDS 路径，最后生成）
```

**教练模型是 CDS 的增强输入而非严格依赖**——CDS 可用 Elo 概率独立降级运行。教练就绪后，路径推演因有阵型+XI 级对位而更准。日报在最后，因为它消费所有上游产物，不是教练模型的输入。

---

## Work Items

### Phase A — CDS 模式 + 小组出线引擎

#### WI-PAN.1 — CDS 路径级输出 schema ✅ DONE (2026-06-12)
**Goal:** 定义小组出线 + 夺冠路径两层输出的数据契约
**Done when:** `src/factor_ledger/schemas/cds_qualification.schema.yaml` + `cds_championship.schema.yaml` 存在；qualification 含 `{team, group, qual_prob, scenarios[]}`，scenario 含 `{label, trigger, resulting_position, prob}`；championship 字段对齐 team-card §7 的 8 字段（championship_path_count, dominant_path_pattern, dominant_failure_node, bracket_dependency, black_swan_dependency, penalty_dependency, injury_sensitivity, simulation_status）
**Key files:** 新建两个 schema，参照 `src/factor_ledger/schemas/prediction_card.schema.yaml` 结构
**Dependencies:** 无
**Size:** S (2h)

#### WI-PAN.2 — 小组积分 + FIFA 排名引擎 ✅ DONE (2026-06-12)
**Goal:** 实现小组积分计算与 FIFA 平级决胜规则
**Done when:** `src/cds/group_standings.py` 给定一组赛果返回 4 队排名，遵循 **FIFA 2026 多队平级规程**（非简单线性顺序）：(1) 积分；若 3+ 队同分，进入**迷你联赛**——仅取同分队相互比赛重算 积分→净胜球→进球数→得分；(2) 仍平则回退**全组** 净胜球→进球数；(3) fair-play 分（纪律数据未入库则跳过）；(4) 抽签。10+ 单元测试覆盖：2 队同分、3 队同分迷你联赛、4 队同分、fair-play 缺失回退。
> ⚠️ **实现者注意**：早先草案写的"积分>净胜球>进球数>H2H"对多队平级是**错的**——FIFA 先在同分队迷你联赛内重算再回退全组。以本规程为准，否则 48 队出线概率会被静默污染。
**Key files:** 新建 `src/cds/group_standings.py` + `tests/test_group_standings.py`；输入对齐 `site/data/schedule.json` 的 group 段
**Dependencies:** 无
**Size:** M (4h)

#### WI-PAN.3 — 小组出线情景推演 ✅ DONE (2026-06-12)
**Goal:** 为每队枚举 3 场小组赛 27 种结果，聚合出线概率 + 关键情景
**Done when:** `scripts/cds_path_simulation.py --layer=qualification` 产出 `data/processed/cds_qualification.json`（48 队）；每队 qual_prob ∈ [0,1] + 关键情景，聚合规则明确：**必胜出线**=剩余所有结果均出线；**已定出线**=qual_prob=1.0；**危局**=qual_prob∈[0.2,0.5] 且依赖他队结果；**已淘汰**=qual_prob=0.0；其余归"正常争夺"；用 Elo 概率作 baseline，教练概率（如就绪）作增强
**Key files:** 新建 `scripts/cds_path_simulation.py`；依赖 `src/cds/group_standings.py`
**Dependencies:** WI-PAN.1, WI-PAN.2；软依赖 WI-CM.6
**Size:** L (1d)

### Phase B — 夺冠路径引擎

#### WI-PAN.4 — 淘汰赛 bracket 枚举 ✅ DONE (2026-06-12)
**Goal:** 从 schedule.json 的 knockout 结构构建完整 bracket 路径图
**Done when:** `src/cds/knockout_bracket.py` 解析三类 slot 引用——位置+组别（`1A/2B`）、最佳第三名复合集（`3ABCDF/3EGHJK`，依赖 FIFA 跨组平衡表）、胜者传播（`W73/W74`）——返回每队**邻接表**路径（`{team: [{round, opponent_slot, match_id}]}` 的 DAG）
**Key files:** 新建 `src/cds/knockout_bracket.py` + **`config/third_place_mapping.json`**（FIFA 跨组平衡表：哪几个组的第三名进哪场 R32——静态参考数据，须先建，约 S/1h）；输入 `site/data/schedule.json` knockout 段
**Dependencies:** `config/third_place_mapping.json` 先行建表（否则第三名槽位无法解析，bracket 只能覆盖 24 个已知小组前二）
**Size:** M (4h)

#### WI-PAN.5 — 夺冠路径条件概率推演 ✅ DONE (2026-06-12)
**Goal:** 沿 bracket 树算每队夺冠概率 + 路径阻力，填充 team-card §7
**Done when:** `scripts/cds_path_simulation.py --layer=championship` 产出 `data/processed/cds_championship.json`。**每节点概率源**明确：对手已配对且有教练预计算 → 用教练概率；否则用 Elo（降级模式 = 全程 Elo）。**§7 八字段映射**：championship_path_count=路径分支数；dominant_path_pattern=最高概率路径的对手序列；dominant_failure_node=单场胜率跌幅最大节点；bracket_dependency=依赖的第三名/抽签槽位；black_swan_dependency=交叉引用 §5 黑天鹅表；penalty_dependency=是否含点球强项门将；injury_sensitivity=核心球员移除后夺冠概率变动；simulation_status=run_complete。与 §6 Miracle Package precursor/branch 条件交叉标注达成状态
**Key files:** `scripts/cds_path_simulation.py`（扩展）；依赖 `src/cds/knockout_bracket.py` + WI-PAN.3 出线概率
**Dependencies:** WI-PAN.1, WI-PAN.3, WI-PAN.4
**Size:** L (1d)

### Phase C — 前端渐进式披露

#### WI-PAN.6 — 比赛级三信号展示 ✅ DONE (2026-06-12)
**Goal:** panorama + team-detail 比赛卡片支持教练（主）+ Elo/Polymarket（可展开）
**Done when:** `panorama.js` 为每场构建教练概率 map（与 `oddsMap` 同构 key：home_win/draw/away_win/confidence/expected_goals_*）；默认显示主信号概率条，可展开看 Elo + Polymarket 对照（交互方式与配色由前端实施者定，复用 portal.css 既有组件）；淘汰赛卡片补概率条（填补现有 "No probability bar for knockout yet" 缺口）；所有模型数据 Red badge + "只能参考"
**Key files:** 修改 `site/js/panorama.js:194`（数据加载）, `site/js/team-detail.js`, `site/css/portal.css`
**Dependencies:** WI-PAN.1；软依赖 WI-CM.7/8
**Size:** L (1d)

#### WI-PAN.7 — 球队级 CDS 路径分析面板 ✅ DONE (2026-06-12)
**Goal:** team-detail 新增"CDS 路径分析"区，含出线情景卡 + Miracle Package 状态（路径树为可选增强）
**Done when:** team.html 新增面板，渲染 (a) 小组出线情景卡（27 种聚合为关键情景 + 出线概率条），(c) §6 Miracle Package 达成条件状态；数据来自 `cds_qualification.json` + `cds_championship.json`；本地 HTTP server 验证渲染
**Key files:** 修改 `site/js/team-detail.js`, `site/team.html`, `site/css/portal.css`；新增 `site/data/cds-paths-data.js`
**Dependencies:** WI-PAN.3, WI-PAN.5
**Size:** M (4h) — MVP 仅含 (a)+(c)
**MVP 后置（可推迟）：** (b) 夺冠路径树可视化——最复杂、最易返工组件，情景卡 + §6 状态已交付约 80% 价值；建议小组赛结束后（对手确定）再做，届时路径树最有意义。此前 WI-PAN.7 不阻塞首发

#### WI-PAN.8 — 首页三信号对比图 + 布局修复 ✅ DONE (2026-06-12)
**Goal:** 外部参考图从 2 柱扩为 3 柱（教练/市场/Elo），修复已知布局问题
**Done when:** 外部参考图（`renderExternalReferenceChart`）由 2 柱（AI/市场）扩展为 3 柱（教练/市场/Elo），按 slug merge；修复双柱同 track 重叠 + 6 格指标板 grid 排布不均（具体类名/行号由实施者定位，不锁死）
**Key files:** 修改 `site/js/homepage.js:289-339`, `site/css/portal.css`
**Dependencies:** WI-PAN.1
**Size:** M (4h)

### Phase D — 管线 + 收尾

#### WI-PAN.9 — CDS 接入构建管线 ✅ DONE (2026-06-12)
**Goal:** cds_path_simulation 输出接入 build_site_data.py
**Done when:** `build_cds_paths_json()` 产出 `site/data/cds-paths.json` + `cds-paths-data.js`；通过 `_validate_public_text_boundary()` 检查；构建成功
**Key files:** 修改 `scripts/build_site_data.py:1431-1440`（main 编排）
**Dependencies:** WI-PAN.3, WI-PAN.5
**Size:** S (2h)

#### WI-PAN.10 — 每日管线编排 ✅ DONE (2026-06-12)
**Goal:** CDS 加入 daily-update.yml 链
**Done when:** daily-update.yml 链序为 Polymarket→Elo→Coach(select-xi)→Coach(simulate)→CDS→report；CDS 步骤 `continue-on-error: true`；赛前全量 workflow + 赛中增量（仅受影响队）触发逻辑就绪
**Key files:** 修改 `.github/workflows/daily-update.yml`（跨计划依赖 full-upgrade WI-4.3 先实施）
**Dependencies:** WI-PAN.3, WI-PAN.5, WI-PAN.9；跨计划依赖 full-upgrade WI-4.3 + coach WI-CM.11
**Size:** M (4h)

#### WI-PAN.11 — 测试 + Factor Ledger + Tag ✅ DONE (2026-06-12) — Factor YAML 生成推迟（per plan note）
**Goal:** 验证 + 知识库更新 + 标记完成
**Done when:** `tests/test_cds_path_simulation.py` 含 8+ 测试（排名引擎、27 枚举、bracket 解析、条件概率、缺失数据降级、文本边界）；`wiki/index.md` 更新含 CDS 页面；`git tag upgrade-phase-cds-done`
**Note:** Factor YAML 生成（遵循 `factor_ledger_entry.schema.yaml`）**可推迟**——同 WI-CM.10，属元数据簿记，不影响用户功能，模型验证通过后再做
**Key files:** 新建 `tests/test_cds_path_simulation.py`；`artifacts/fixtures/cds4polymarket/factor-ledger/` 新增；`wiki/index.md`
**Dependencies:** WI-PAN.5, WI-PAN.10
**Size:** M (4h)

---

## 实施顺序

```
Phase A（schema + 小组出线引擎）:
  WI-PAN.1 (schema)   ─┐
  WI-PAN.2 (排名引擎)  ─┼──→ WI-PAN.3 (出线推演)

Phase B（夺冠路径，依赖 A）:
  WI-PAN.4 (bracket)  ──→ WI-PAN.5 (夺冠推演，依赖 WI-PAN.3)

Phase C（前端，可部分并行 B）:
  WI-PAN.6 (比赛级)   ── 独立，软依赖教练前端数据
  WI-PAN.8 (首页)     ── 独立
  WI-PAN.7 (球队级)   ── 依赖 WI-PAN.3 + WI-PAN.5

Phase D（管线 + 收尾）:
  WI-PAN.9 (管线)     ──→ WI-PAN.10 (CI) ──→ WI-PAN.11 (测试 + tag)
```

**推荐起步**：WI-PAN.1 + WI-PAN.2 + WI-PAN.4 三项无依赖、可并行启动；其中 WI-PAN.6/8（前端）可与引擎开发并行，先用 Elo 数据占位，教练数据就绪后切换。

---

## 与现有计划的关系

| 计划 | 范围 | Work Items |
|------|------|-----------|
| `full-upgrade-2026-06-12.md` | Phase 0-4 基础升级（数据校正、Elo、市场快照、LLM 客户端、日报编排器） | WI-0.x ~ WI-4.x |
| `coach-matchup-model-2026-06-12.md` | 教练决策 + 对位引擎 + 蒙特卡洛（三信号之一） | WI-CM.1 ~ WI-CM.12 |
| **本计划** | CDS 两层引擎 + 前端渐进式披露 + 管线整合 | WI-PAN.1 ~ WI-PAN.11 |

**依赖链**：full-upgrade（WI-4.3 编排器）→ coach（WI-CM.6 概率）→ 本计划 CDS。
**跨计划传递依赖**：WI-PAN.10 依赖 WI-CM.11，而 WI-CM.11 又依赖 WI-4.3 → 完整链 WI-4.3 → WI-CM.11 → WI-PAN.10（图示中未画出，启动 WI-4.3 时须意识到下游还有两层）。
**⚠️ 待协调的陈旧节点**：full-upgrade 计划的 WI-3.5（CDS 辩论 `cds_debate.py`）已被本计划的 `cds_path_simulation.py` **取代**。启动 WI-4.3 前，须先在 full-upgrade 计划中将 WI-3.5 标记 superseded，否则 WI-4.3 会拖入一个不再需要的模块。
**解耦点**：本计划 CDS 可先用 Elo 降级运行（WI-PAN.3 软依赖 WI-CM.6），不必等教练模型完成。前端 WI-PAN.6/8 可用 Elo 数据先行占位。
**前端合并策略**：WI-PAN.6 与 coach WI-CM.8 都改 `panorama.js` 数据 map——建议 WI-CM.8 先落地 `coachMap`，WI-PAN.6 在其上加三信号切换，避免冲突。

---

## 风险与缓解

| 风险 | 缓解 |
|------|------|
| 27 枚举 × 条件树计算量爆炸 | 两层解耦；夺冠层仅赛前 + 赛中重算，不每日全量 |
| 三信号融合诱惑 | 架构禁止融合；并列存储；分歧即发现 |
| 教练模型未就绪阻塞 CDS | CDS 用 Elo 降级运行；教练为增强非硬依赖 |
| 前端信息过载 | 渐进式披露；默认一信号，展开看全貌 |
| 路径树可视化破坏审美 | 复用 portal.css 设计系统；不引入新字体/色系 |
| 三信号高度趋同（无信息量） | 监控信号间偏离度；趋同则某信号冗余，需调参或移除 |

---

## Open Questions

1. **赛制确认**：2026 是否锁定 12 组×4 队 + 小组第三名晋级？（影响 WI-PAN.2 排名规程 + WI-PAN.4 第三名映射表；未锁定则这两项推迟）
2. **教练模型就绪时机**：WI-CM.6 能否在开赛前就绪？（若不能，WI-PAN.3/5 全程用 Elo，软依赖变硬依赖，关键路径改变）
3. **路径树 MVP 范围**：WI-PAN.7 的夺冠路径树是否必须随首发上线，还是后置到小组赛结束？（已在 WI-PAN.7 标为可推迟，确认后定 Phase C 并行度）
4. **WI-3.5 协调**：full-upgrade 的 WI-3.5 是否正式 superseded？（须先在 full-upgrade 计划更新，才能正确 scope WI-4.3）

## References

- `docs/plans/coach-matchup-model-2026-06-12.md` — 教练模型计划（WI-CM.5 已更新）
- `docs/plans/full-upgrade-2026-06-12.md` — 现有 Phase 0-4 升级计划
- `site/css/portal.css` — 现有设计系统
- `site/js/panorama.js:418` — "No probability bar for knockout yet"
- `site/js/homepage.js:289-339` — 外部参考图表
- `site/js/team-detail.js` — 球队详情数据契约
- `.github/workflows/market-snapshot.yml` — 每日市场快照 CI
- `artifacts/team-cards/argentina.md:64-86` — Miracle Package + Path Simulation Notes schema
