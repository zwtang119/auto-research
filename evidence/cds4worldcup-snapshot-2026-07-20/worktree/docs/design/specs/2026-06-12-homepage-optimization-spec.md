# CDS4WorldCup 赛季全景图与每日自动化分析 Spec

> **类型**: design-spec
> **状态**: draft-for-review
> **日期**: 2026-06-12
> **范围**: 本地 wiki 构建、GitHub Pages 动态展示、MiMo Code 驱动每日自动化分析管线、交互式全景图
> **约束**: 严格遵守 `docs/source-policy.md`；不引入数据库或常驻进程；不输出投注建议、收益率或仓位建议；Wiki 保持 Marginalia 协议

---

## 1. 愿景与目标

### 1.1 核心愿景

构建一张**"世界杯概率全景图"**：以官方赛程为骨架，以多源概率为血肉，以 CDS 方法论为灵魂，每天自动更新并发布到 GitHub Pages。用户进入页面后，第一眼看到的是完整赛程图，每场比赛标注最新概率与关键因子；点击任意球队，下钻到该队的深度路径卡、Agent 预测档案与实时状态。

### 1.2 具体目标

| 编号 | 目标 | 验收标准 |
|------|------|---------|
| G1 | 本地 wiki 构建完整内容体系 | 48 队球队档案、核心球员档案、小组赛 72 场比赛页面、每日赔率与推演记录 |
| G2 | GitHub Pages 静态展示 | 浏览器零依赖访问，构建期预计算所有数据，不直接调用外部 API |
| G3 | 每日自动运行管线 | 类似 policysim-research-Tsinghua 的批量 Agent 运行模式，300+ runs/日 |
| G4 | 8 大 MiMo Code 驱动模块 | 赛程、新闻、球员、数值赔率、市场赔率、CDS 推演、Agent 投票、分析报告 |
| G5 | 交互式全景图 | 赛程图 + 概率热力标注 + 可点击球队下钻 + 关键因子浮层 |

### 1.3 非目标

- 不做实时交易信号或自动投注系统。
- 不引入 Astro/Next/React 等前端框架；v1 保持零依赖 HTML/CSS/JS。
- 不把 Kimi/MiMo 概率作为事实依据输出。
- 不在浏览器端直接调用 Polymarket API 或新闻 API。

---

## 2. 参考项目分析

### 2.1 policysim-research-Tsinghua：批量运行范式

**核心机制**：
- `generate_experiments.py` 驱动 4 模型 × 2 条件 × 35 runs = 280 runs。
- 使用 Python 脚本 + 统一 `api_client.py` 调用多模型 API。
- **MAMR**（Multi-Agent Multi-Round）：3 个企业 Agent，3 轮竞争推演，Centralized 拓扑（编排者聚合竞争态势摘要）。
- **SASR**（Single-Agent Single-Round）：单 Agent 单轮直出基线。
- 防模板化：Jaccard 相似度检查，超阈值则注入扰动并重试。
- Prompt provenance：每次 API 调用记录 prompt log。

**对 CDS4WorldCup 的转译**：
- 设计 `src/pipeline/daily_run.py` 作为批量驱动器，每日 spawn 300 个 MiMo-v2.5 Agent runs。
- 采用 SASR 模式做小组赛 Agent 预测赔率（单 Agent 单任务，适合大规模并行）。
- 采用 MAMR 模式做 CDS 夺冠推演（多 Agent 多轮辩论，适合深度分析）。
- 引入 Jaccard 防模板化检查，避免 Agent 输出趋同。

### 2.2 cds4polymarket：多 Agent 辩论与聚合管线

**核心机制**：
- `Arena` 类：多 Agent 轮询发言，`maxTurns=2`，消息历史注入上下文。
- `pipeline-stages.ts`：7 阶段管线 — Question Normalize → Data Enrichment → Role DNA → Simulation (multi-run) → Aggregation → Report → Quality。
- 双层聚合：keyword extraction（`aggregateRuns`）+ LLM synthesis（`provider.completeJson`）。
- 质量评估：5 维度 LLM evaluation（actionability, specificity, stability 等）。
- 增量上下文：`buildIncrementalContext` 将外部数据变化注入后续 run。

**对 CDS4WorldCup 的转译**：
- CDS 夺冠推演采用 Arena 辩论模式：4-6 个角色 Agent（路径分析师、来源审计员、市场观察员、反方挑战者）进行 2-3 轮辩论。
- 聚合层同时输出 keyword aggregation（结构化因子）和 LLM synthesis（叙事摘要）。
- 每日 run 的 quality metrics 写入 `data/ops/daily-runs/quality/` 供长期追踪。

### 2.3 institute-one：工作流引擎与 Prompt 工程

**核心机制**：
- **Prompt 三明治**：`date_anchor() → persona_block() → context_blocks → task → CITATION_MANDATE → FILE_DELIVERABLE`。
- **工作流 JSON**：`workflows/*.json` 定义线性步骤，每步有 analyst、prompt、output_file。
- **上下文压缩**：`previous_steps_block()` 硬性预算 8000 字符，均摊 + 下限保护，智能摘要优先。
- **VaultWriter**：原子写入（tmp + os.replace）、sha256 ledger、人类编辑检测、跳过未变更。
- **条件认领**：`UPDATE … SET status='running' WHERE status='pending'` 通过 rowcount 判断竞争成功。

**对 CDS4WorldCup 的转译**：
- 在 `src/utils/prompt_builder.py` 实现 Prompt 三明治构建器（零依赖纯 Python）。
- 在 `data/ops/workflows/` 为 8 种标准任务定义 JSON 工作流模板（Path Card Audit、Match Odds Numeric、Agent Vote 等）。
- 在 `src/utils/vault_writer.py` 实现轻量 VaultWriter（`.ledger.jsonl` 替代 SQLite），保护 `candidate/` 和 `mimo_outputs/`。
- `task_queue.json` 引入乐观锁（version 字段）和超期回收（stalled 状态）。

### 2.4 Kimi 300 Agent 世界杯预测：派别化 swarm 与交互展示

**核心机制**：
- 10 派别 × 30 Agent = 300 Agent（数据派、赔率派、老球迷派、玄学派、主帅视角派、伤病赛程派、黑马派、阵容年龄派、心理抗压派、建模派）。
- 夺冠概率 = Σ(confidence_i for agent_i picking team) / Σ(all confidence scores)，归一化为百分比。
- 三区交互网页：过程区（300 Agent 头像网格 + ticker）、结果区（Top8 热力榜 + count-up）、分歧视图（派别切换）。
- 先让用户"押冠军"，再揭晓分布，给出个性化反馈。

**对 CDS4WorldCup 的转译**：
- 小组赛 Agent 预测赔率采用派别化设计：10 个派别，每派 30 Agent，共 300 Agent。
- 每个 Agent 参考当日数据（新闻、伤病、市场赔率、数值模型）进行投票，输出结构化 JSON。
- 聚合算法与 Kimi 一致，但增加"与数值模型偏差"、"与市场赔率偏差"两个分析维度。
- 交互展示吸收 Kimi 的热力榜、派别切换、押冠军互动，但语言改为 CDS 风格（"看夺冠路"而非"押注"）。

---

## 3. 系统架构

### 3.1 总体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                         数据层 (Data Layer)                       │
│  ├─ FIFA 官方赛程/赛果 (Green, 静态)                              │
│  ├─ 新闻/伤病/RSS API (Yellow, 每日快照)                          │
│  ├─ Polymarket API (Yellow, 每日快照)                             │
│  ├─ 数值预测模型输出 (Red, MiMo 生成)                             │
│  └─ Agent 投票档案 (Red, MiMo 生成)                               │
├─────────────────────────────────────────────────────────────────┤
│                       分析层 (Analysis Layer)                     │
│  ├─ M1 赛程抓取 (静态, 赛前一次)                                   │
│  ├─ M2 球队新闻抓取 (RSS/API, 每日)                                │
│  ├─ M3 球员信息抓取 (RSS/API, 每日)                                │
│  ├─ M4 数值预测赔率 (MiMo Script, 每日)                            │
│  ├─ M5 市场赔率快照 (Polymarket API, 每日)                         │
│  ├─ M6 CDS 夺冠推演 (MiMo Arena MAMR, 每日)                        │
│  └─ M7 Agent 预测投票 (MiMo SASR 300 runs, 每日)                   │
├─────────────────────────────────────────────────────────────────┤
│                       聚合层 (Aggregation Layer)                  │
│  ├─ 比赛级概率聚合 (数值 + 市场 + Agent 加权)                       │
│  ├─ 球队级路径更新 (CDS 推演结果注入 Path Card)                     │
│  └─ 日报生成 (data-analysis + chart-visualization + consulting)    │
├─────────────────────────────────────────────────────────────────┤
│                       发布层 (Publish Layer)                      │
│  ├─ wiki/ — Markdown 知识库 (Marginalia 协议)                     │
│  ├─ site/wc2026/ — 静态网页 (GitHub Pages)                        │
│  └─ results/ — 结构化报告与图表                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 新增/扩展目录结构

```
cds4worldcup/
├── src/
│   ├── pipeline/
│   │   ├── daily_orchestrator.py      # 每日管线总控
│   │   ├── m1_schedule_fetcher.py     # 赛程抓取
│   │   ├── m2_news_fetcher.py         # 新闻抓取
│   │   ├── m3_player_fetcher.py       # 球员信息抓取
│   │   ├── m4_numeric_odds.py         # 数值预测赔率
│   │   ├── m5_polymarket_snapshot.py  # Polymarket 快照
│   │   ├── m6_cds_debate.py           # CDS 夺冠推演 Arena
│   │   ├── m7_agent_voting.py         # 300 Agent 投票
│   │   ├── m8_report_generator.py     # 分析报告生成
│   │   └── utils/
│   │       ├── api_client.py          # 统一 API 调用 (借鉴 policysim)
│   │       ├── prompt_builder.py      # Prompt 三明治构建器
│   │       ├── vault_writer.py        # 安全写入
│   │       ├── context_compressor.py  # 上下文压缩
│   │       └── aggregation.py         # 概率聚合算法
│   ├── agents/
│   │   ├── personas/                  # Agent 人格配置
│   │   │   ├── path-analyst.md
│   │   │   ├── source-auditor.md
│   │   │   ├── match-context-analyst.md
│   │   │   ├── settlement-analyst.md
│   │   │   ├── cognitive-auditor.md
│   │   │   └── market-observer.md
│   │   └── factions/                  # 10 派别配置
│   │       ├── data-faction.md
│   │       ├── odds-faction.md
│   │       ├── veteran-faction.md
│   │       ├── mystic-faction.md
│   │       ├── coach-faction.md
│   │       ├── injury-faction.md
│   │       ├── dark-horse-faction.md
│   │       ├── age-faction.md
│   │       ├── mental-faction.md
│   │       └── model-faction.md
│   └── publish/
│       └── build_site_data.py         # 构建 site/data/*.json
├── data/
│   └── ops/
│       └── daily-runs/
│           ├── YYYY-MM-DD/
│           │   ├── schedule/          # 赛程数据
│           │   ├── news/              # 新闻快照
│           │   ├── players/           # 球员状态
│           │   ├── numeric-odds/      # 数值预测赔率
│           │   ├── polymarket/        # 市场赔率快照
│           │   ├── cds-debate/        # CDS 推演原始记录
│           │   ├── agent-votes/       # 300 Agent 投票原始记录
│           │   ├── aggregation/       # 聚合结果
│           │   ├── report/            # 日报 Markdown
│           │   └── quality/           # 质量评估
│           └── archive/               # 历史归档
├── wiki/
│   ├── teams/                         # 48 队档案
│   ├── players/                       # 核心球员档案
│   ├── matches/                       # 小组赛 72 场 + 淘汰赛
│   └── analysis/
│       └── daily/                     # 每日分析摘要
├── site/
│   ├── wc2026/
│   │   ├── index.html                 # 全景图主页面
│   │   ├── team/
│   │   │   └── {team-id}.html         # 球队详情 (生成)
│   │   ├── match/
│   │   │   └── {match-id}.html        # 比赛详情 (生成)
│   │   └── report/
│   │       └── daily-{date}.html      # 日报页面 (生成)
│   └── data/
│       └── wc2026/
│           ├── panorama.json          # 全景图数据入口
│           ├── teams.json             # 球队数据
│           ├── matches.json           # 赛程与概率数据
│           └── daily/                 # 日报数据
└── .github/
    └── workflows/
        └── daily-wc2026-update.yml    # GitHub Actions 定时任务
```

---

## 4. 本地 Wiki 构建

### 4.1 Wiki 内容体系

Wiki 采用 Marginalia 协议，所有页面为 Markdown，包含元数据块、正文、批注、相关页面链接。

#### 4.1.1 球队档案 (`wiki/teams/{team-slug}.md`)

每队一页，内容：
- **元数据**：队名、FIFA 排名、所属大洲、小组、path_type、tier、资料完整度、最后更新。
- **核心阵容**：主力 11 人 + 关键替补，含位置、俱乐部、身价、状态。
- **夺冠路径卡**：Plan A 路径（已存在，扩展为动态更新）。
- **阻力记录**：来自 path card 的 obstacle list。
- **可结算条件**：Miracle Package 条件清单及结算状态（赛前 pending，赛后 settled/failed）。
- **状态时间线**：每日关键事件批注（`> [!memo] YYYY-MM-DD 内容`）。
- **来源标签**：每个事实声明标注 Green/Yellow/Red。

#### 4.1.2 球员档案 (`wiki/players/{player-slug}.md`)

核心球员（每队 3-5 人）一页，内容：
- **元数据**：姓名、国籍、俱乐部、位置、身价、重要性评级。
- **伤病与状态**：最新伤病、红黄牌、出场状态。
- **历史表现**：近 12 个月国家队数据。
- **批注**：每日状态更新。

#### 4.1.3 赛程页面 (`wiki/matches/{match-id}.md`)

小组赛 72 场 + 淘汰赛，每场比赛一页，内容：
- **元数据**：比赛 ID、日期时间、地点、对阵双方、小组/阶段。
- **赛前分析**：双方近期状态、历史交锋、关键因子。
- **概率档案**：数值预测、市场赔率、Agent 预测，三条时间线。
- **赛后结算**：实际赛果、因子验证、预测偏差分析。
- **来源标签**：赔率数据标注 Yellow/Red，官方赛果标注 Green。

#### 4.1.4 每日分析摘要 (`wiki/analysis/daily/YYYY-MM-DD.md`)

每日自动生成，内容：
- 当日数据更新概览。
- 关键新闻与伤病汇总。
- 概率变化最大的 3 场比赛。
- Agent 投票分布变化。
- CDS 推演结论更新。
- 明日关注清单。

### 4.2 Wiki 更新流程

1. **自动写入区**：`wiki/analysis/daily/`、`wiki/matches/` 的"概率档案"部分可由 MiMo 自动更新（作为 Yellow/Red Source 标注）。
2. **人工审核区**：`wiki/teams/` 的核心路径卡、`wiki/players/` 的身价与阵容需人工审核后才能从 candidate 提升。
3. **赛后锁定区**：比赛结束后，赛果和结算状态由人工确认后写入 Green Source。

---

## 5. GitHub Pages 展示

### 5.1 站点结构

```
site/
├── index.html                    # 现有主页（保留并扩展入口）
├── wc2026/
│   ├── index.html                # 全景图主页面（核心）
│   ├── static/
│   │   ├── panorama.css          # 全景图样式
│   │   └── panorama.js           # 全景图交互逻辑
│   └── data/                     # 构建期生成的 JSON
│       ├── panorama.json         # 全景图主数据（赛程+概率）
│       ├── teams.json            # 球队档案数据
│       ├── matches.json          # 比赛数据（含历史概率时间线）
│       └── daily/
│           └── YYYY-MM-DD.json   # 日报数据
```

### 5.2 全景图主页面 (`site/wc2026/index.html`)

#### 5.2.1 视觉风格

- **底色**：`#FBF9F1`（暖白/米色纸感，延续现有 parchment 质感）。
- **文字**：`#13233A`（深藏青墨）。
- **功能色**：
  - 可靠事实（Green）：深绿 `#2D6A4F`
  - 待核验线索（Yellow）：琥珀 `#C8A45C`
  - 只能参考（Red）：暗红 `#9B2D20`
  - 数据快照：青色 `#5E807A`
- **字体**：无衬线标题 + 等宽数据（借鉴 Kimi 页面）。

#### 5.2.2 页面结构

**首屏：全景赛程图**
- 12 个小组的赛程矩阵（3 轮 × 12 组 = 36 个比赛日单元格，或按小组展示 4 队循环赛）。
- 每场比赛卡片显示：
  - 对阵双方国旗 + 队名
  - 比赛日期时间
  - **核心概率条**：三合一展示（数值预测 | 市场赔率 | Agent 预测），用不同颜色区分。
  - **关键因子图标**：伤病 alert、状态 hot、天气等（hover 显示详情）。
  - 点击卡片 → 下钻到比赛详情页。

**第二屏：球队探索**
- 48 队网格，每队小卡：国旗、队名、小组、资料完整度条、最新夺冠概率（CDS 推演）。
- 点击球队 → 下钻到球队详情页。
- 搜索框 + 按大洲/小组筛选。

**第三屏：概率时间线与对比**
- 选择一场比赛，展示三条概率时间线：
  - 数值预测（蓝线）
  - Polymarket 市场（红线）
  - Agent 共识（绿线）
- 标注重大事件（伤病、新闻发布会等）对概率的扰动。

**第四屏：日报入口**
- 最近 7 天日报卡片，点击展开摘要或跳转完整报告。

#### 5.2.3 交互设计

- **Hover 效果**：比赛卡片 hover 时放大、显示关键因子浮层。
- **点击下钻**：球队 → 球队详情；比赛 → 比赛详情。
- **押冠军互动**（可选，借鉴 Kimi）：让用户先选一个心目中的冠军，然后展示与该选择相关的 Agent 派别分布、概率位置、风险评级。注意文案避免下注暗示，改为"你最看好谁？看看不同视角怎么分析"。
- **派别视角切换**：在 Agent 预测区域，可按 10 个派别切换查看分布。

### 5.3 构建期数据管线

```python
# src/publish/build_site_data.py 逻辑
1. 读取 wiki/teams/*.md → 提取元数据 + 路径卡摘要 → teams.json
2. 读取 wiki/matches/*.md + data/ops/daily-runs/最新数据 → matches.json
3. 读取 data/ops/daily-runs/最新聚合结果 → panorama.json
4. 读取 wiki/analysis/daily/*.md → daily/YYYY-MM-DD.json
5. 所有 JSON 写入 site/wc2026/data/
6. GitHub Actions 在每日 run 结束后自动执行此脚本并 push
```

---

## 6. 每日自动运行：MiMo Code 驱动管线

### 6.1 运行频率与触发

| 项目 | 配置 |
|------|------|
| 频率 | 每日一次，UTC 00:00（北京时间 08:00） |
| 触发器 | GitHub Actions `schedule` + `workflow_dispatch`（手动） |
| 运行时 | Mac mini 本地（MiMo Code 长程 sprint）+ GitHub Actions runner（轻量抓取） |
| 总时长 | 目标 2-4 小时（参考 policysim 的 batch 模式） |
| 历史保留 | 每日数据保留 30 天，超过后归档到 `data/ops/daily-runs/archive/` |

### 6.2 批量运行模式：借鉴 policysim-research-Tsinghua

#### 6.2.1 核心驱动脚本 `src/pipeline/daily_orchestrator.py`

功能类似 policysim 的 `generate_experiments.py`，但适配 CDS4WorldCup 场景：

```python
"""
每日管线总控。
用法:
  python src/pipeline/daily_orchestrator.py --date 2026-06-15 --runs 300
"""
```

执行流程：
1. **Pre-flight**：检查 campaign_state.json、task_queue.json 状态；确认网络可用。
2. **M1-M3 数据抓取**：并行执行赛程（静态）、新闻、球员信息抓取。
3. **M4 数值预测**：MiMo Code 驱动脚本生成小组赛每场比赛的数值预测赔率。
4. **M5 市场快照**：调用 Polymarket API，抓取当日市场赔率。
5. **M6 CDS 夺冠推演**：MiMo Code Arena MAMR 模式，4-6 Agent 辩论 2-3 轮。
6. **M7 Agent 投票**：MiMo Code SASR 模式，300 Agent 并行投票。
7. **M8 报告生成**：调用 data-analysis、chart-visualization、consulting-analysis 生成日报。
8. **Post-flight**：聚合所有结果 → 更新 wiki → 运行 `build_site_data.py` → git push。

#### 6.2.2 统一 API 客户端 `src/pipeline/utils/api_client.py`

借鉴 policysim 的 `api_client.py`：
- 支持多模型调用：MiMo-v2.5（主力）、备用模型。
- 统一封装：重试机制、超时控制、token 使用记录、prompt log 记录。
- 配置从 `config/api-config.yaml` 读取（API 密钥、端点、模型参数）。

```python
def call_model(config, model_name, messages, prompt_log_dir=None, prompt_metadata=None):
    """统一模型调用，返回 (response_text, usage_dict)。"""
```

#### 6.2.3 防模板化机制

借鉴 policysim 的 Jaccard 检查：
- 每个 Agent run 的输出与同一任务的历史输出计算 Jaccard 相似度。
- 阈值：`jaccard_similarity_threshold = 0.7`。
- 超阈值时，自动在 prompt 尾部追加扰动："注意：请避免重复之前的分析角度，尝试从新的视角切入。"
- 最多重试 2 次。

#### 6.2.4 Prompt Provenance

每次 MiMo Code 调用记录：
- `prompt_log_dir/daily-YYYY-MM-DD/prompt-{task}-{run_id}-{timestamp}.json`
- 包含：完整 prompt、模型参数、调用时间、元数据。

---

## 7. 八大 MiMo Code 驱动模块详解

### 7.1 模块 M1：赛程抓取 (Schedule Fetcher)

**目标**：抓取 2026 世界杯完整赛程，建立基础数据结构。

**特点**：赛程基本不会改动，赛前一次性抓取即可，后续只需更新赛果。

**实现**：
- 数据源：FIFA 官方 API 或官方网页（Green Source）。
- 输出：`data/ops/daily-runs/YYYY-MM-DD/schedule/matches.json`
- 结构：
  ```json
  {
    "match_id": "A1-MEX-KOR",
    "group": "A",
    "round": 1,
    "date": "2026-06-11",
    "time": "20:00",
    "timezone": "UTC-5",
    "venue": "Azteca Stadium, Mexico City",
    "home_team": "Mexico",
    "away_team": "Korea Republic",
    "status": "scheduled"
  }
  ```
- Wiki 更新：生成/更新 `wiki/matches/{match-id}.md` 的元数据和赛程信息。

**频率**：赛前一次性；赛事期间每日更新赛果。

---

### 7.2 模块 M2：球队新闻抓取 (News Fetcher)

**目标**：抓取 48 支球队的最新新闻，包括训练状态、战术调整、更衣室动态等。

**实现**：
- 数据源：ESPN、BBC Sport、Goal.com 等 RSS feed（Yellow Source）。
- 工具：`feedparser`（Python 零依赖 RSS 解析）或调用新闻 API（如 NewsAPI）。
- 处理：
  1. 按球队关键词过滤新闻。
  2. LLM 摘要：MiMo Code 读取新闻列表，提取每队 3-5 条关键摘要。
  3. 来源标注：每条摘要标注来源 URL 和抓取时间。
- 输出：`data/ops/daily-runs/YYYY-MM-DD/news/{team-slug}.json`
- Wiki 更新：将摘要作为批注写入 `wiki/teams/{team-slug}.md`。

**频率**：每日。

---

### 7.3 模块 M3：球员信息抓取 (Player Fetcher)

**目标**：抓取核心球员的伤病、红黄牌、出场状态。

**实现**：
- 数据源：Transfermarkt 伤病列表、官方球队公告、RSS（Yellow Source）。
- 处理：
  1. 抓取伤病页面或 RSS。
  2. LLM 提取结构化数据：球员名、伤病类型、预计恢复时间、状态（available/doubtful/out）。
  3. 与昨日数据 diff，识别新增伤病或恢复。
- 输出：`data/ops/daily-runs/YYYY-MM-DD/players/{team-slug}.json`
  ```json
  {
    "player": "Eder Militao",
    "team": "Brazil",
    "injury": " thigh tendon rupture",
    "status": "out",
    "source": "https://...",
    "fetched_at": "2026-06-12T08:00:00Z"
  }
  ```
- Wiki 更新：更新 `wiki/players/{player-slug}.md` 的状态时间线。

**频率**：每日。

---

### 7.4 模块 M4：小组赛每场比赛数值预测赔率 (Numeric Odds Predictor)

**目标**：用量化模型生成每场比赛的胜/平/负概率。

**实现**：
- **不是让 MiMo 直接猜概率**，而是 MiMo Code 驱动**脚本执行**量化模型：
  1. MiMo 读取当日数据（球队实力、伤病、历史交锋、主客场）。
  2. MiMo 编写或调用 Python 脚本（如泊松分布、Elo 预期得分、xG 模拟）。
  3. 脚本输出结构化概率。
- 模型建议：
  - **Elo 预期得分**：基于 FIFA/Elo 排名计算预期胜率。
  - **泊松分布**：基于近期场均进球/失球模拟比分分布。
  - **蒙特卡洛**：10000 次随机模拟，考虑伤病因子调整。
- MiMo 的角色：数据工程师 + 模型调参师，而非预测者本身。
- 输出：`data/ops/daily-runs/YYYY-MM-DD/numeric-odds/{match-id}.json`
  ```json
  {
    "match_id": "A1-MEX-KOR",
    "model": "poisson_elo_hybrid",
    "home_win": 0.52,
    "draw": 0.24,
    "away_win": 0.24,
    "expected_goals_home": 1.4,
    "expected_goals_away": 0.9,
    "confidence": "medium",
    "factors": ["home_advantage", "elo_gap", "injury_adjustment"]
  }
  ```
- 来源等级：Red Source（模型输出，非事实）。

**频率**：每日。

---

### 7.5 模块 M5：小组赛市场赔率 (Polymarket Snapshot)

**目标**：抓取 Polymarket 上世界杯相关市场的赔率数据。

**实现**：
- 数据源：Polymarket Gamma API（Yellow Source）。
- 抓取内容：
  - 单场胜负市场（如有）。
  - 小组出线市场。
  - 冠军市场。
- 输出：`data/ops/daily-runs/YYYY-MM-DD/polymarket/snapshot.json`
  ```json
  {
    "market": "World Cup 2026 Winner",
    "teams": [
      {"team": "Spain", "probability": 0.167, "volume": 1200000}
    ],
    "fetched_at": "2026-06-12T08:00:00Z",
    "source_level": "Yellow"
  }
  ```
- 注意：只抓取公开可访问的市场数据，不做交易。
- 展示时必须标注："市场数据仅供参照，不是投注建议。"

**频率**：每日。

---

### 7.6 模块 M6：CDS 夺冠推演 (Championship Path Debate)

**目标**：用多 Agent 辩论推演 48 队的夺冠路径，识别关键节点和阻力。

**实现**：借鉴 cds4polymarket 的 Arena + MAMR 模式。

#### 7.6.1 Agent 角色设计（4-6 人）

| 角色 | 职责 | 模型 |
|------|------|------|
| 路径分析师 (path-analyst) | 推演夺冠路径，识别每轮对手和关卡 | MiMo-v2.5 |
| 来源审计员 (source-auditor) | 审核输入数据的可信度，标记 Green/Yellow/Red | MiMo-v2.5 |
| 市场观察员 (market-observer) | 引入市场赔率作为外部参照，识别共识/分歧 | MiMo-v2.5 |
| 反方挑战者 (devil-advocate) | 主动挑战主流观点，寻找被低估的风险 | MiMo-v2.5 |
| 历史类比师 (historian) | 引入历史模式（卫冕魔咒、东道主效应等） | MiMo-v2.5 |

#### 7.6.2 辩论流程（MAMR，2-3 轮）

**Round 1**：各 Agent 独立分析
- 路径分析师："西班牙的夺冠路径是 H组第一 → 1/8决赛对G组第二 → ..."
- 市场观察员："市场给西班牙 16.7%，但小组赛对手很弱，这个概率可能被低估"
- 反方挑战者："亚马尔腿筋伤势是最大隐患，西班牙历史上从未在美洲夺冠"

**Round 2**：基于他人观点调整
- 各 Agent 看到 Round 1 的全部发言后，调整自己的立场。
- 路径分析师："考虑到反方的伤病提醒，我将西班牙过荷兰/巴西关的概率从 60% 下调到 45%"

**Round 3**（可选）：收敛与共识提取
- 聚焦分歧最大的 2-3 个点进行深化辩论。

#### 7.6.3 聚合输出

- **Keyword Aggregation**：提取关键因子、路径节点、风险事件。
- **LLM Synthesis**：生成结构化 JSON：
  ```json
  {
    "team": "Spain",
    "championship_probability_cds": 0.18,
    "key_path_nodes": [
      {"round": "Group", "opponent": "Uruguay", "pass_probability": 0.75},
      {"round": "R16", "opponent": "Germany", "pass_probability": 0.55}
    ],
    "critical_risks": [
      {"risk": "Yamal injury", "severity": "high", "mitigation": "Fati/Torres cover"}
    ],
    "consensus_areas": ["Group stage should be straightforward"],
    "disagreement_areas": ["Depth vs Germany in QF", "Final opponent uncertainty"],
    "source_level": "Red",
    "generated_at": "2026-06-12T10:00:00Z"
  }
  ```

- Wiki 更新：`wiki/analysis/daily/YYYY-MM-DD.md` 的 CDS 推演部分。

**频率**：每日。

---

### 7.7 模块 M7：小组赛 Agent 预测赔率 (Agent Voting Swarm)

**目标**：300 个 Agent 参考 M1-M5 的数据，对每场比赛给出预测，记录投票档案。

**这是重点模块。**

#### 7.7.1 派别化设计（借鉴 Kimi 300 Agent）

10 派别 × 30 Agent = 300 Agent。

| 派别 | 关注维度 | 数据权重 |
|------|---------|---------|
| 数据派 | 身价、Elo、xG、近期战绩 | 高权重给 M4 数值模型 |
| 赔率派 | 博彩盘口与隐含概率 | 高权重给 M5 Polymarket |
| 老球迷派 | 历史底蕴、大赛基因 | 高权重给历史数据 |
| 玄学派 | 东道主魔咒、卫冕魔咒 | 高权重给叙事因子 |
| 主帅视角派 | 战术体系、克制关系 | 高权重给新闻和战术分析 |
| 伤病赛程派 | 伤病、赛程、气候 | 高权重给 M3 球员信息 |
| 黑马派 | 被低估的冷门队 | 寻找高赔率 + 低市场关注的队 |
| 阵容年龄派 | 核心年龄结构 | 高权重给球员档案 |
| 心理抗压派 | 大心脏、点球、逆境 | 高权重给历史关键战表现 |
| 建模派 | 蒙特卡洛/泊松等量化模拟 | 高权重给 M4，但加入自己的调整 |

#### 7.7.2 每个 Agent 的输入上下文（受控压缩）

借鉴 institute-one 的 `previous_steps_block()` 和 `context_compressor`：
- 每个 Agent 接收的上下文有硬性预算（如 4000 tokens）。
- 内容优先级：
  1. 比赛对阵双方基础数据（队名、排名、近期战绩）。
  2. 关键伤病/状态变化（M3）。
  3. 数值模型输出（M4）。
  4. 市场赔率（M5）。
  5. 相关新闻摘要（M2）。
- 压缩规则：key_findings 优先，原始文本截断。

#### 7.7.3 每个 Agent 的输出格式

```json
{
  "agent_id": "data-05",
  "faction": "数据派",
  "persona": "英超数据分析师，信奉xG和pressing intensity",
  "match_id": "A1-MEX-KOR",
  "prediction": "home_win",
  "confidence": 72,
  "predicted_score": "2-0",
  "reason": "墨西哥主场优势明显，韩国近期热身赛防守漏洞大。xG差1.2。",
  "key_factors": ["home_advantage", "xG_gap", "korea_defense_issues"],
  "disagreement_with_market": "市场给墨西哥胜率50%，我认为应该更高",
  "source_level": "Red"
}
```

#### 7.7.4 批量运行方式（SASR）

```python
# src/pipeline/m7_agent_voting.py 伪代码

for faction in FACTIONS:
    for i in range(30):
        agent_id = f"{faction['id']}-{i+1:02d}"
        persona = load_persona(faction, i)
        context = build_compressed_context(match, daily_data, budget_tokens=4000)
        prompt = build_agent_voting_prompt(
            date_anchor=date_anchor(),
            persona=persona,
            context=context,
            task="预测这场比赛的胜平负及比分，给出信心和理由",
            citation_mandate=CITATION_MANDATE,
            output_schema=AGENT_VOTE_SCHEMA
        )
        result = call_model(config, "mimo-v2.5", prompt)
        save_vote(agent_id, result)
```

#### 7.7.5 聚合算法

**比赛级聚合**：
- 对每个 `match_id`，汇总 300 个 Agent 的 `prediction`。
- 计算：
  - 原始得票率：`home_win_votes / 300`
  - 信心加权概率：`Σ(confidence_i for home_win) / Σ(all confidence)`
  - 派别分歧指数：10 个派别各自的预测分布的标准差
- 输出：`data/ops/daily-runs/YYYY-MM-DD/agent-votes/aggregation/{match-id}.json`

**球队级聚合**：
- 将小组赛 3 场比赛的预测串联，计算出线概率。
- 结合 CDS 夺冠推演（M6）的路径节点概率，更新夺冠概率。

#### 7.7.6 投票档案

每个 Agent 每次投票的完整记录保存 30 天：
- `data/ops/daily-runs/YYYY-MM-DD/agent-votes/raw/vote-{agent_id}-{match-id}.json`
- 包含：完整 prompt、输出、token 使用、运行时间。
- 用于后续复盘：为什么某个 Agent 在某天改变了立场？

**频率**：每日，小组赛期间覆盖全部 72 场；淘汰赛期间覆盖当轮比赛。

---

### 7.8 模块 M8：分析报告生成 (Daily Report Generator)

**目标**：基于 M1-M7 的全部数据，使用 data-analysis、chart-visualization、consulting-analysis 三个技能套装，生成每日详细分析报告。

**这是人-AI 协作的核心交付物。**

#### 7.8.1 数据准备

MiMo Code 首先聚合当日全部数据为结构化输入：
- `data/ops/daily-runs/YYYY-MM-DD/aggregation/daily-summary.json`
- 包含：赛程状态、新闻摘要、伤病汇总、数值赔率、市场赔率、CDS 推演结论、Agent 投票聚合。

#### 7.8.2 分析维度（data-analysis 技能）

1. **概率漂移分析**：对比昨日 vs 今日，哪些比赛的概率变化最大？驱动因素是什么？
2. **市场 vs Agent 分歧**：哪些比赛存在显著分歧？（`public_consensus_gap`）
3. **派别信号提取**：10 个派别中，哪些派别在某场比赛上高度一致？哪些是分裂的？
4. **球队状态趋势**：基于多日数据，绘制球队状态趋势（上升/下降/震荡）。
5. **伤病影响量化**：新增伤病对某队夺冠概率的边际影响估算。

#### 7.8.3 可视化生成（chart-visualization 技能）

生成以下图表（保存为 PNG/SVG，嵌入报告）：
1. **比赛概率热力矩阵**：X 轴比赛，Y 轴概率来源（数值/市场/Agent/CDS），颜色深浅表示概率。
2. **球队夺冠概率时间线**：Top 8 球队近 N 天的夺冠概率变化。
3. **派别分歧雷达图**：某场比赛在 10 个派别上的预测分布。
4. **市场 vs Agent 散点图**：X 轴市场概率，Y 轴 Agent 概率，偏离对角线的点标注。
5. **关键因子瀑布图**：某队夺冠概率的因子分解（基础实力 + 伤病调整 + 赛程难度 + 状态调整 = 综合概率）。

图表规范：
- 使用零依赖 JS 在构建期生成（如 D3.js 预渲染为 SVG），或在 Python 中使用 matplotlib/plotly 生成 PNG。
- 所有图表标注数据来源和生成时间。
- 图表颜色遵循 5.2.1 的功能色规范。

#### 7.8.4 报告撰写（consulting-analysis 技能）

报告结构（Markdown，中文为主）：

```markdown
# CDS4WorldCup 每日分析报 — 2026 年 6 月 12 日

## 执行摘要
- 今日关键变化（3 句话）。
- 最值得关注的一场比赛及原因。
- 最大分歧点（市场 vs Agent 或派别间）。

## 1. 数据更新概览
- 新闻摘要（5 条）。
- 伤病更新（新增/恢复）。
- 数值模型输出摘要。
- Polymarket 快照摘要。

## 2. 小组赛概率全景
- 各小组出线概率矩阵（表格 + 热力图）。
- 关键比赛分析（3-5 场）。

## 3. CDS 夺冠推演更新
- Top 8 球队路径状态。
- 关键节点概率变化。
- 新增风险或机会。

## 4. Agent 投票分析
- 300 Agent 共识分布。
- 派别视角亮点。
- 与昨日对比的变化。

## 5. 市场 vs Agent 分歧观察
- 分歧最大的 3 场比赛。
- 分歧原因分析。
- 监控建议（哪些信号出现时分歧会收敛）。

## 6. 明日关注清单
- 明日比赛预览。
- 赛前值得监控的新闻/伤病。
- 赛后可对账的条件。

## 7. 方法论与来源声明
- 数据来源列表及等级（Green/Yellow/Red）。
- 模型版本与参数。
- 能力边界声明。
- 免责声明：本报告仅供研究参考，不构成投注建议。
```

#### 7.8.5 发布流程

1. 报告 Markdown 保存到 `wiki/analysis/daily/YYYY-MM-DD.md`。
2. 图表保存到 `results/daily/YYYY-MM-DD/`。
3. `src/publish/build_site_data.py` 将报告转为 HTML（或保留 Markdown 由 GitHub Pages 渲染）。
4. GitHub Actions push 到 `gh-pages` 分支。

**频率**：每日。

---

## 8. 数据流与存储契约

### 8.1 每日数据目录结构

```
data/ops/daily-runs/2026-06-12/
├── manifest.json                  # 当日运行清单与状态
├── schedule/
│   └── matches.json
├── news/
│   └── {team-slug}.json
├── players/
│   └── {team-slug}.json
├── numeric-odds/
│   └── {match-id}.json
├── polymarket/
│   └── snapshot.json
├── cds-debate/
│   ├── round-1.json
│   ├── round-2.json
│   ├── round-3.json
│   └── synthesis.json
├── agent-votes/
│   ├── raw/
│   │   └── vote-{agent_id}-{match_id}.json
│   └── aggregation/
│       └── {match_id}.json
├── aggregation/
│   ├── match-odds-matrix.json     # 比赛级概率聚合
│   ├── team-path-update.json      # 球队路径更新
│   └── daily-summary.json         # 日报输入数据
├── report/
│   └── daily-report.md
├── charts/
│   └── *.png / *.svg
└── quality/
    └── quality-metrics.json
```

### 8.2 数据契约

1. **manifest.json**：每日运行的总控文件，记录各模块状态（success/failed/skipped）、运行时间、token 使用总量。
2. **原子写入**：所有文件写入遵循 VaultWriter 规则（tmp + rename），防止并发覆盖。
3. **来源标注**：每个数据文件必须包含 `source_level` 字段（Green/Yellow/Red）和 `generated_at` 时间戳。
4. **可重建性**：日报的数据输入（`daily-summary.json`）必须足够完整，使得给定输入可以重现报告。
5. **保留策略**：原始投票和 prompt logs 保留 30 天；聚合结果和报告永久保留；过期数据移至 `archive/`。

---

## 9. 交互式全景图详细设计

### 9.1 全景赛程图

#### 9.1.1 布局

采用"小组赛矩阵 + 淘汰赛树"双视图：

**小组赛视图（默认）**：
- 12 列（Group A-L），每列 3 行（Matchday 1/2/3）。
- 每个单元格是一场比赛卡片。
- 卡片尺寸：桌面端 180px × 120px，移动端自适应。

**淘汰赛视图（切换）**：
- 32 强 → 16 强 → 8 强 → 4 强 → 决赛的树状图。
- 每场比赛显示对阵和概率。
- 点击可展开该场比赛的详细分析。

#### 9.1.2 比赛卡片设计

```
┌─────────────────────────┐
│ 🇲🇽 墨西哥    2-0    🇰🇷 韩国 │  ← 对阵 + 预测比分
│ ━━━━━━━●━━━━━━━━━━━━━━━ │  ← 概率条（主场 | 平局 | 客场）
│ 52%    24%    24%       │  ← 数值预测（hover 切换市场/Agent/CDS）
│ ⚠️ 伤病  🔥 状态          │  ← 关键因子图标
│ 6/11 20:00 墨西哥城      │  ← 时间地点
└─────────────────────────┘
```

- **概率条**：三段式，颜色区分（主场绿/平局灰/客场蓝，或按胜率高低渐变）。
- **hover 切换**：默认显示"数值预测"，hover 时小标签切换显示"市场赔率"、"Agent 共识"、"CDS 推演"。
- **因子图标**：
  - ⚠️ 伤病 alert（某队有关键球员缺阵）
  - 🔥 状态 hot（某队近期状态极佳）
  - ❄️ 状态 cold（近期状态差）
  - 🏠 主场优势
  - ⚡ 高分歧（市场 vs Agent 差异 > 15%）

#### 9.1.3 交互行为

- **Click 比赛卡片**：弹出侧边面板或跳转 `match/{match-id}.html`，展示：
  - 双方近期战绩对比
  - 三条概率时间线（数值/市场/Agent）
  - 关键因子详解
  - 300 Agent 派别分布
  - 相关新闻摘要
- **Click 球队名**：跳转 `team/{team-slug}.html`。

### 9.2 球队详情页

```
┌────────────────────────────────────────┐
│ 🇪🇸 西班牙  |  FIFA #1  |  Group H     │
│ [资料完整度条]  [夺冠概率 18%]          │
├────────────────────────────────────────┤
│ 路径卡摘要：                            │
│ H组第一 → R16 vs G2 → QF vs ...        │
│ [展开完整路径卡]                        │
├────────────────────────────────────────┤
│ 关键球员状态：                          │
│ 🟢 亚马尔 - 有望恢复                     │
│ 🟢 佩德里 - 正常                         │
│ 🔴 卡瓦哈尔 - 缺席                       │
├────────────────────────────────────────┤
│ 夺冠概率时间线：                         │
│ [折线图：数值/市场/Agent/CDS 四条线]     │
├────────────────────────────────────────┤
│ 300 Agent 怎么看：                       │
│ [派别分布条形图]                        │
│ 数据派 65% | 玄学派 45% | ...           │
├────────────────────────────────────────┤
│ 阻力记录：                              │
│ 1. 从未在美洲夺冠 [历史]                │
│ 2. 亚马尔腿筋隐患 [伤病]                │
├────────────────────────────────────────┤
│ 可结算条件：                            │
│ □ 小组赛出线（待验证）                  │
│ □ 1/8决赛过关（待验证）                 │
└────────────────────────────────────────┘
```

### 9.3 技术实现

- **前端**：纯 HTML/CSS/JS，零外部依赖。
- **数据**：`site/wc2026/data/panorama.json` 单入口（或按需拆分为 `teams.json` + `matches.json`）。
- **图表**：使用原生 JS 绘制 SVG 图表（参考 Kimi 页面的 CSS 条形图），或构建期预生成 PNG/SVG。
- **响应式**：桌面端矩阵布局，移动端纵向堆叠或小组切换器。

---

## 10. 执行计划

### 10.1 阶段划分

#### Phase 0：基础设施（本周，零依赖）

| 任务 | 输出 | 负责人 |
|------|------|--------|
| P0-1 | `src/utils/prompt_builder.py` — Prompt 三明治构建器 | Agent |
| P0-2 | `src/utils/vault_writer.py` — 安全写入（ candidate/ / mimo_outputs/ ） | Agent |
| P0-3 | `src/utils/context_compressor.py` — 上下文压缩 | Agent |
| P0-4 | `data/ops/workflows/` — 8 种标准任务 JSON 模板 | Agent |
| P0-5 | `task_queue.json` 状态机 + 乐观锁 + 超期回收 | Agent |
| P0-6 | `data/ops/events.jsonl` + `scripts/audit.py --events` | Agent |

#### Phase 1：数据与 Wiki 构建（下周）

| 任务 | 输出 | 依赖 |
|------|------|------|
| P1-1 | M1 赛程抓取脚本 + `wiki/matches/` 72 场比赛页面 | P0 |
| P1-2 | M2 新闻抓取 + M3 球员抓取脚本 | P0 |
| P1-3 | `wiki/teams/` 48 队档案模板 + 已有 deep-description 迁移 | P0 |
| P1-4 | `wiki/players/` 核心球员档案（每队 3-5 人） | P1-3 |
| P1-5 | M4 数值预测赔率脚本（泊松/Elo 基础版） | P0 |
| P1-6 | M5 Polymarket 快照脚本 | P0 |

#### Phase 2：MiMo Code 驱动核心（第 3-4 周）

| 任务 | 输出 | 依赖 |
|------|------|------|
| P2-1 | M7 300 Agent 投票系统（SASR 模式） | P1-5, P1-6 |
| P2-2 | M6 CDS 夺冠推演（Arena MAMR 模式） | P1-3, P1-5 |
| P2-3 | Agent 人格与派别配置（`src/agents/`） | P0-4 |
| P2-4 | 聚合算法（比赛级 + 球队级） | P2-1, P2-2 |
| P2-5 | `src/pipeline/daily_orchestrator.py` 总控 | P2-1 ~ P2-4 |

#### Phase 3：报告与可视化（第 5 周）

| 任务 | 输出 | 依赖 |
|------|------|------|
| P3-1 | M8 日报生成（data-analysis + consulting-analysis） | P2-4 |
| P3-2 | chart-visualization 图表套装 | P3-1 |
| P3-3 | `wiki/analysis/daily/` 日报模板与历史 | P3-1 |

#### Phase 4：前端全景图（第 6 周）

| 任务 | 输出 | 依赖 |
|------|------|------|
| P4-1 | `site/wc2026/index.html` 全景赛程图 | P2-4 |
| P4-2 | `site/wc2026/team/{id}.html` 球队详情 | P1-3, P2-4 |
| P4-3 | `site/wc2026/match/{id}.html` 比赛详情 | P1-1, P2-4 |
| P4-4 | `src/publish/build_site_data.py` 构建脚本 | P4-1 ~ P4-3 |

#### Phase 5：自动化与上线（第 7 周）

| 任务 | 输出 | 依赖 |
|------|------|------|
| P5-1 | `.github/workflows/daily-wc2026-update.yml` | P4-4 |
| P5-2 | 端到端测试（模拟一次完整 daily run） | P5-1 |
| P5-3 | 文档与运维手册 | P5-2 |

### 10.2 关键里程碑

| 日期 | 里程碑 | 验收标准 |
|------|--------|---------|
| D+7 | 基础设施就绪 | prompt_builder, vault_writer, task_queue 状态机可用 |
| D+14 | Wiki 内容骨架完成 | 48 队 + 72 场 + 球员档案有页面，数据抓取脚本可运行 |
| D+28 | 核心分析管线跑通 | 一次完整的 M1-M7 daily run 成功，产出结构化数据 |
| D+35 | 日报与图表生成 | 日报 Markdown + 5 张图表自动生成，质量可接受 |
| D+42 | 全景图上线 | GitHub Pages 可访问，赛程图 + 概率标注 + 点击下钻可用 |
| D+49 | 自动化闭环 | GitHub Actions 每日定时触发，端到端无人工干预 |

---

## 11. 来源纪律与约束重申

### 11.1 三级来源执行

| 数据类型 | 来源等级 | 能否进入 Factor Ledger | 页面展示方式 |
|----------|---------|----------------------|-------------|
| FIFA 官方赛程/赛果 | Green | 是 | 主数据 |
| 官方伤病/首发/技术统计 | Green | 是 | 主数据 |
| Elo/FIFA 排名（可复核） | Green | 是 | 主数据 |
| 新闻/媒体报道 | Yellow | 候选，需核验 | 标注"待核验" |
| Polymarket 市场数据 | Yellow | 否（仅参照） | 标注"市场参考" |
| 数值模型输出（M4） | Red | 否 | 标注"模型模拟" |
| Agent 投票（M7） | Red | 否 | 标注"AI 参考" |
| CDS 推演（M6） | Red | 否 | 标注"推演分析" |

### 11.2 禁止行为

- 不把任何 Agent 预测或模型输出作为"事实"或"推荐"。
- 不输出投注建议、仓位、收益率、PnL、Sharpe、Kelly。
- 不在页面使用"买/卖/下注/赔率价值"等语言。
- 不把 Kimi/MiMo 概率与 CDS 路径卡混为一谈。
- 不在公开页面暴露 API 密钥或内部工具品牌。

### 11.3 免责声明

每个展示概率的页面必须包含：

```
> **声明**：本页面展示的数值模型输出、AI Agent 预测和市场赔率仅供研究参考，
> 不构成投注建议

---

## 17. 增量补充：MiMo Code 架构约束与替代设计（DeepSeek-V4-Flash 审阅）

> **审阅者**: DeepSeek-V4-Flash
> **审阅时间**: 2026-06-12
> **范围**: 对上述 Spec 的批判性审阅，聚焦于 MiMo Code 架构能力边界、数据管线量级、前端交互完整性与技能集成可操作性
> **性质**: 增量补充——仅覆盖 Spec 中未充分讨论或存在架构假设偏差的维度

### 17.1 关键架构偏差：MiMo Code 不是 batch scheduler

**问题陈述**：Spec 隐含一个架构假设——MiMo Code 可以在长程 sprint 内 "spawn 300 个子 agent 并行投票"，就像 policysim-research-Tsinghua 的 `generate_experiments.py` 在 for 循环中调用 650 次 LLM API 一样。这是需要纠正的架构偏差。

| 维度 | policysim 方式 | MiMo Code 方式 |
|------|---------------|---------------|
| 执行载体 | Python 脚本独立 for 循环 | 单一长程 Agent（研究 sitter） |
| 并行能力 | 串行 650 次，每次独立 HTTP 请求 | 单线程顺序执行，无法 spawn 子进程 |
| API 调用 | Python requests 直接调 LLM API | Agent 内部推理，不产生外部 API 调用 |
| 失败隔离 | 单次失败不影响后续 | 单步失败可能中断整个 sprint |
| 适合场景 | 高吞吐批量推理 | 深度推理、多步骤依赖 |

**推荐替代方案：混合架构**

```
MiMo Code 角色：设计 -> 生成 -> 审核（非执行）
  + 设计 Agent 人格配置 (src/agents/factions/ + personas/)
  + 生成每日上下文压缩包 (context_compressor.py 聚合 M1-M5 数据)
  + 审核 300 个投票结果的聚合质量
  + 不执行 300 次投票本身

Python batch 脚本角色：执行（直接调用 LLM API）
  + src/pipeline/m7_agent_voting.py
    + for 循环 300 次，每次调用 MiMo-v2.5 API
  + 由 daily_orchestrator.py 编排，在 MiMo Code 完成 M1-M5 后触发
```

**推荐管线顺序**：
```
MiMo Code sprint (M1-M6, ~2h)
  -> Python batch script (M7, 300 API calls, ~1-2h)
  -> MiMo Code resume (M8 报告撰写 + 聚合分析, ~1h)
  -> build_site_data.py + git push
```

### 17.2 policysim 650 runs 的可迁移性分析

| 维度 | policysim-research-Tsinghua | CDS4WorldCup (M7 Agent 投票) |
|------|----------------------------|------------------------------|
| 总调用次数 | 280-650 runs | 300 runs x 72 matches = 21,600 runs（全量） |
| 单次调用成本 | 短 prompt（1-2K tokens） | 中等 prompt（3-5K tokens） |
| 输出格式 | 自由文本 | 结构化 JSON（含 schema 校验） |
| 防模板化 | Jaccard 相似度检查 | 同左，但量级增大 33x |

**核心发现**：21,600 次/天的 API 调用对 token 预算和 API 成本构成实质性压力。

**建议的优化层次**：

| 层次 | 策略 | runs 减少 | 信息损失 |
|------|------|-----------|---------|
| L1 | 全量 72 场 x 300 Agent | 21,600 | 无（基线） |
| L2 | 仅跑当日比赛（~4-6 场），其余复用前日 | ~1,500 | 低 |
| L3 | 降采样至 100 Agent/场 | 7,200 | 中 |
| L4 | 派别级投票（10 派别） | 720 | 高 |

**推荐**：小组赛 L2（每日 ~1,500 runs），稳定后扩展到 L1；淘汰赛降回 L2-L3。

### 17.3 数据源具体方案评估

#### 17.3.1 新闻抓取（M2）

| 数据源 | 类型 | 覆盖度 | 成本 |
|--------|------|--------|------|
| NewsAPI (newsapi.org) | REST API | 48 队全覆盖 | 免费 tier 500 req/day |
| ESPN FC RSS | RSS | 主要球队 | 免费 |
| BBC Sport RSS | RSS | 欧洲+美洲球队 | 免费 |

**推荐**：NewsAPI 为主，ESPN/BBC RSS 为冗余备份。

#### 17.3.2 球员信息（M3）

| 数据源 | 类型 | 覆盖度 |
|--------|------|--------|
| Transfermarkt 伤病列表 | Web Scrape | 全面（含恢复时间） |
| Flashscore | Web Scrape | 全面，含红黄牌 |

**推荐**：Transfermarkt 为主力，Flashscore 补充红黄牌。

#### 17.3.3 Polymarket 市场赔率（M5）

- 端点：`https://gamma-api.polymarket.com/events?tag=world-cup-2026`
- 备用：`https://clob.polymarket.com/`
- 容错：API 不可用时展示上一日快照 + 标注

#### 17.3.4 数值模型（M4）

不依赖外部 API。MiMo Code 编写 Python 量化脚本本地执行：Elo 基线、泊松分布、蒙特卡洛模拟。输出为 Red Source。

### 17.4 交互全景图的移动端信息架构

Spec 设计了桌面端 12 组 x 3 轮矩阵，但移动端不可直接复用。

#### 17.4.1 移动端内容优先级

| 优先级 | 内容 | 展示方式 |
|--------|------|---------|
| P0 | 今日/明日比赛 | 横向滚动卡片 |
| P1 | 小组出线概率 | 纵向列表 |
| P2 | Top 5 夺冠概率 | 紧凑条形图 |
| P3-P5 | 派别分布/时间线/完整赛程 | 点击展开/筛选器 |

#### 17.4.2 推荐交互模式

- 小组赛：日期聚合模式 -- "今日/明日"区块 + 底部 tab
- 淘汰赛：时间线导航 -- R32 -> R16 -> QF -> SF -> F
- 通过 detectViewport() 自动切换

#### 17.4.3 触摸交互

Tap 比赛卡片 -> Bottom Sheet 面板（替代独立详情页，减少跳转）
Tap 球队名 -> 导航到详情页

### 17.5 Skills 套装集成方案

三个技能是交互式 Agent 技能，不是可导入的 Python 库。正确调用方式：

```
daily_orchestrator.py 最后阶段：
  1. MiMo Code 聚合数据 -> daily-summary.json
  2. 启动独立 Agent 会话 -> data-analysis 技能
  3. 启动独立 Agent 会话 -> chart-visualization 技能
  4. 启动独立 Agent 会话 -> consulting-analysis 技能
```

关键：这三个技能不能由 MiMo Code 内部调用（单一长程 agent 无法嵌套调用其他 Agent 技能）。

图表技术选型：
- 夺冠概率条形图 -> 原生 CSS（零依赖）
- 概率热力矩阵/时间线 -> D3.js 预渲染 SVG
- 派别分歧雷达图 -> plotly HTML 片段
- 关键因子瀑布图 -> matplotlib PNG

### 17.6 CDS 夺冠推演辩论协议详细设计

#### 17.6.1 三阶段辩论协议

```
阶段 1：独立前提声明（Blind Round）
  - 各 Agent 在看不到他人观点的情况下独立写出：依据数据、核心论点、信心分
  - 目的：防止锚定效应

阶段 2：交叉质询（Cross-Examination Round）
  - 各 Agent 看到全部声明后必须：指出不同点、评估分歧类型（数据差异/权重差异）、调整概率
  - 目的：识别分歧本质

阶段 3：收敛与分歧登记（Settlement Round）
  - 各 Agent 给出最终概率估计
  - 聚合器记录：共识区域（+/-5%）、分歧区域（SD > 10%）、分歧原因分类
```

#### 17.6.2 分歧审计员角色

增加第 7 个 Meta-Agent，不参与辩论，只负责：
1. 识别哪些分歧值得深挖
2. 标记数据差异型分歧 -> 生成 fact-check 任务
3. 标记权重差异型分歧 -> 作为认知多样性证据保留

输出直接进入 M8 报告章节。

### 17.7 Agent 投票档案的数据量预算

| 项目 | 每日新增 | 30 天总量 |
|------|---------|----------|
| 原始投票 JSON | 21,600 条 ~ 43MB | ~1.3GB |
| 聚合结果 | 72 场 ~ 720KB | ~21MB |
| Prompt logs | 21,600 条 ~ 108MB | ~3.2GB |
| 合计 | ~152MB/日 | ~4.5GB/30天 |

原始数据在 GitHub 仓库中不可行。建议策略：
- 聚合结果 -> Git 永久保留（几百 KB/日）
- 原始投票 -> Git LFS 30 天或本地存储
- Prompt logs -> .gitignore 7 天

每日自动生成 vote_diff.json：立场反转、信心变化 > 20、Spearman 相关系数。

### 17.8 构建期 vs 运行时的前端数据策略

| 层级 | 内容 | 加载时机 | 更新频率 | 数据量 |
|------|------|---------|---------|-------|
| Static | 赛程/球队基本信息 | 构建期嵌入 HTML | 一次 | < 50KB |
| Semi-static | 球员档案/历史交锋 | JSON 写入 | 每日 | < 200KB |
| Dynamic | 概率/投票/新闻摘要 | JSON 写入 | 每日 | < 500KB |
| On-demand | 辩论记录/时间线 | 点击后 fetch | 每日 | < 2MB |

首屏：内联 panorama.json，零异步请求，秒开。

### 17.9 交互全景图视觉分层与 Heat Zone

#### 17.9.1 Z-axis 视觉分层

```
Z5: 伤病 alert / 状态异常 -> 最高权重
Z4: 概率条（数值 | 市场 | Agent）-> 核心数据
Z3: 关键因子图标 -> 辅助决策
Z2: 对阵 + 比分 -> 基础信息
Z1: 时间地点 -> 次要信息
```

#### 17.9.2 Heat Zone 编码

| Zone | 条件 | 卡片样式 |
|------|------|---------|
| Red Zone | 市场 vs Agent 分歧 > 15% | 暗红左边框 3px |
| Yellow Zone | 关键球员伤病新增 | 琥珀色上边框 2px |
| Green Zone | 实力与概率一致 | 默认 |
| Hot Zone | 概率变化 > 10%（vs 昨日） | 青色呼吸动画 |

#### 17.9.3 三层关联

在 panorama.json 中预计算：比赛 -> 关联球员状态 + 关联新闻摘要。hover 时浮层展示，无需跳转。

### 17.10 审阅小结

| 章节 | 意见 | 等级 |
|------|------|------|
| M7 Agent 投票 | 架构假设需纠正：MiMo Code 不能 spawn 子进程，需 Python batch | **高** |
| M6 CDS 推演 | 辩论协议需补全三阶段 + 分歧审计员 | 中 |
| M8 报告生成 | Skills 调用方式需明确（独立 Agent 会话） | 中 |
| 全景图 | 移动端适配需补全 | 中 |
| 数据源 | 具体方案需明确（NewsAPI/Transfermarkt/Polymarket） | 低 |
| 数据量 | 原始投票存储策略需调整 | 低 |

---

> **审阅结论**: 核心需要修正的是 M7 的执行架构假设（17.1）和补全辩论协议细节（17.6）。其余增量内容属于实施层面的明确化。

> **作者**: DeepSeek-V4-Flash
> **日期**: 2026-06-12

---

## 18. 增量补充：DeepSeek-V4-Pro UI/UX 设计架构审查

> **作者**: DeepSeek-V4-Pro
> **日期**: 2026-06-12
> **角色**: UI/UX Design Architect
> **方法**: 对本 spec 的独立审查，结合对 policysim-research-Tsinghua 批量运行范式、cds4polymarket Arena 辩论架构、institute-one 工作流引擎、Kimi Agent 世界杯 UI 升级包的交叉阅读。聚焦于本 spec 中设计系统、交互模式、信息架构、可访问性和视觉工程化的结构性缺口。以下仅记录增量信息——正向增强和负向修正。

### 18.1 负向：本 spec 缺乏完整的设计 Token 体系，视觉一致性无法保证

当前 spec 第 5.2.1 节定义了 6 个颜色值（`#FBF9F1`、`#13233A`、`#2D6A4F`、`#C8A45C`、`#9B2D20`、`#5E807A`），但没有定义完整的 design token 层级。在实际开发中，6 个颜色值无法覆盖组件状态（hover/focus/active/disabled）、语义色彩（success/warning/error/info）、表面色（surface/overlay/elevated）、文本层级（primary/secondary/tertiary/disabled）等需求。缺乏 token 体系会导致实现阶段出现大量"硬编码临时色"，破坏视觉一致性。

**建议修正**：在 spec 中增加 Design Token 附录，定义三层 token 体系：

**Layer 1 — Primitive Tokens（基础色板）**：
```css
/* 暖白纸感底色系 */
--color-parchment-50:  #FEFDF9;
--color-parchment-100: #FBF9F1;  /* 主底色 */
--color-parchment-200: #F5F0E4;
--color-parchment-300: #EDE5D4;

/* 深藏青墨色系 */
--color-ink-900: #0A1525;
--color-ink-800: #13233A;  /* 主文字 */
--color-ink-700: #1E3A5F;
--color-ink-600: #2A5080;
--color-ink-500: #3D6DA8;

/* 功能色系 */
--color-green-700: #2D6A4F;   /* Green Source */
--color-green-500: #40916C;
--color-green-300: #95D5B2;
--color-amber-600: #C8A45C;   /* Yellow Source */
--color-amber-400: #DDB86A;
--color-amber-200: #F0DFB0;
--color-red-700:  #9B2D20;    /* Red Source */
--color-red-500:  #C44536;
--color-red-300:  #E88B7A;
--color-teal-600: #5E807A;    /* 数据快照 */
--color-teal-400: #7EA89E;
--color-teal-200: #B8D4CD;

/* 中性色系（边框、分割线、禁用态） */
--color-neutral-100: #F5F5F5;
--color-neutral-200: #E5E5E5;
--color-neutral-300: #D4D4D4;
--color-neutral-400: #A3A3A3;
--color-neutral-500: #737373;
--color-neutral-600: #525252;
```

**Layer 2 — Semantic Tokens（语义映射）**：
```css
/* 表面 */
--surface-primary:    var(--color-parchment-100);
--surface-secondary:  var(--color-parchment-200);
--surface-elevated:   var(--color-parchment-50);
--surface-overlay:    rgba(10, 21, 37, 0.6);

/* 文字 */
--text-primary:       var(--color-ink-800);
--text-secondary:     var(--color-ink-600);
--text-tertiary:      var(--color-neutral-500);
--text-disabled:      var(--color-neutral-300);
--text-on-dark:       var(--color-parchment-50);

/* 来源等级 */
--source-green:       var(--color-green-700);
--source-green-bg:    var(--color-green-300);
--source-yellow:      var(--color-amber-600);
--source-yellow-bg:   var(--color-amber-200);
--source-red:         var(--color-red-700);
--source-red-bg:      var(--color-red-300);

/* 交互状态 */
--interactive-default:   var(--color-ink-800);
--interactive-hover:     var(--color-ink-600);
--interactive-active:    var(--color-ink-900);
--interactive-focus:     var(--color-teal-600);
--interactive-disabled:  var(--color-neutral-300);

/* 语义反馈 */
--feedback-success:  var(--color-green-500);
--feedback-warning:  var(--color-amber-400);
--feedback-error:    var(--color-red-500);
--feedback-info:     var(--color-teal-400);

/* 边框 */
--border-default:    var(--color-neutral-200);
--border-strong:     var(--color-neutral-300);
--border-focus:      var(--color-teal-600);
```

**Layer 3 — Component Tokens（组件级）**：
```css
/* 比赛卡片 */
--match-card-bg:           var(--surface-primary);
--match-card-border:       var(--border-default);
--match-card-hover-border: var(--interactive-hover);
--match-card-shadow:       0 2px 8px rgba(10, 21, 37, 0.08);
--match-card-hover-shadow: 0 4px 16px rgba(10, 21, 37, 0.12);

/* 概率条 */
--prob-bar-home:    var(--color-teal-600);
--prob-bar-draw:    var(--color-neutral-400);
--prob-bar-away:    var(--color-ink-500);
--prob-bar-bg:      var(--color-neutral-200);
```

**理由**：三层 token 体系是 industry standard（参考 Material Design 3、Radix Colors、Tailwind CSS）。Layer 1 定义色板，Layer 2 定义语义映射，Layer 3 定义组件绑定。这确保：(1) 颜色修改只需改 Layer 1，(2) 组件之间的视觉一致性由 Layer 2 保证，(3) 新组件开发时无需重新思考颜色语义。

### 18.2 负向：Typography Scale 缺失，信息层级无法落地

本 spec 第 5.2.1 节仅提到"无衬线标题 + 等宽数据"，但没有定义字体、字号、行高、字重的层级体系。在 72 场比赛 + 48 支球队 + 300 Agent 投票的信息密度下，缺乏 typography scale 会导致信息层级扁平化，用户无法快速区分"关键数据"和"背景信息"。

**建议修正**：定义 typography scale（基于 16px 基准，1.25 modular scale）：

```css
/* 字体族 */
--font-sans:      'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono:      'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

/* 字号层级 */
--text-xs:     0.75rem;   /* 12px — 辅助标注、来源标签 */
--text-sm:     0.875rem;  /* 14px — 次级信息、因子标签 */
--text-base:   1rem;      /* 16px — 正文 */
--text-lg:     1.25rem;   /* 20px — 卡片标题 */
--text-xl:     1.5rem;    /* 24px — 区段标题 */
--text-2xl:    1.875rem;  /* 30px — 页面标题 */
--text-3xl:    2.375rem;  /* 38px — Hero 标题 */
--text-4xl:    3rem;      /* 48px — 夺冠概率大数字 */

/* 行高 */
--leading-tight:  1.2;   /* 大标题 */
--leading-normal: 1.5;   /* 正文 */
--leading-relaxed: 1.7;  /* 长文本 */

/* 字重 */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;

/* 应用规则 */
/* 夺冠概率数字 → text-4xl + font-bold + font-mono（等宽确保数字对齐） */
/* 球队名称 → text-lg + font-semibold + font-sans */
/* 来源等级标签 → text-xs + font-medium + font-mono */
/* 因子描述 → text-sm + font-normal + font-sans */
```

**理由**：等宽字体用于数字（概率、比分、时间戳）确保跨行对齐和可扫描性；无衬线用于标题和正文确保可读性。这个区分在 Kimi UI 中被验证有效——等宽数字让"75% / 62% / 58%"在视觉上形成整齐的列，用户可以快速扫描和比较。

### 18.3 负向：Spacing System 缺失，布局密度控制缺乏依据

本 spec 提到了"桌面端 180px × 120px"的比赛卡片尺寸，但没有定义系统级的 spacing scale。72 场比赛的赛程图需要精确的间距控制——间距过大会导致信息密度不足，过小会导致视觉拥挤。

**建议修正**：定义 4px 基准 spacing scale：

```css
--space-1:  0.25rem;  /* 4px  — 微小间距 */
--space-2:  0.5rem;   /* 8px  — 紧凑间距 */
--space-3:  0.75rem;  /* 12px — 默认内边距 */
--space-4:  1rem;     /* 16px — 卡片内边距 */
--space-5:  1.25rem;  /* 20px — 卡片间距 */
--space-6:  1.5rem;   /* 24px — 区段内间距 */
--space-8:  2rem;     /* 32px — 区段间距 */
--space-10: 2.5rem;   /* 40px — 大区段间距 */
--space-12: 3rem;     /* 48px — 页面级间距 */
--space-16: 4rem;     /* 64px — Hero 区段间距 */

/* 比赛卡片网格 */
--panorama-card-width:  180px;
--panorama-card-height: 120px;
--panorama-gap:         var(--space-3);  /* 12px 卡片间距 */
--panorama-group-gap:   var(--space-6);  /* 24px 小组间距 */
```

**理由**：4px 基准是 web 设计的事实标准，与浏览器默认的 16px 基准兼容。12px 卡片间距在 72 场比赛的网格中试算：12 组 × (180px + 12px) = 2,304px，超出 1440px 桌面宽度，需要 2 行或 scroll，这是合理的——用户自然预期小组赛赛程需要滚动浏览。

### 18.4 负向：Component States 定义不完整，交互反馈缺失

本 spec 第 9.1.2 节描述了比赛卡片的静态外观，但未定义完整的交互状态。卡片式 UI 的核心交互状态包括：default、hover、focus、active、pressed、disabled、loading、empty、error。缺少这些定义会导致键盘用户无法获知当前焦点位置、数据加载中用户看到空白、某个比赛数据缺失时卡片显示异常。

**建议修正**：为比赛卡片定义完整状态矩阵：

```
default:  背景 var(--match-card-bg), 边框 var(--match-card-border), cursor pointer
hover:    背景 var(--surface-elevated), transform translateY(-2px) scale(1.02), 
          transition 200ms ease-out, 显示因子浮层
focus-visible: outline 2px solid var(--border-focus), outline-offset 2px
active:   transform translateY(0) scale(0.98), transition 100ms ease-in
disabled: opacity 0.5, cursor not-allowed, 显示"数据暂缺"占位符
loading:  骨架屏（3 条灰色脉冲条 + shimmer 动画）
empty:    灰色虚线边框, 显示"XX月XX日"日期占位
error:    红色虚线边框, 显示"数据加载失败"图标 + 上次已知数据 + 时间戳
```

**概率条状态**：
```
default:    三段式 home/draw/away 颜色 + 百分比数字
hover:      显示概率来源标签 + 完整概率值（如 52.3%）
single-source: 显示该来源标签，其他来源灰色虚线占位
multi-source:  默认显示"Agent 共识"，提供切换按钮（数值 | 市场 | Agent | CDS）
              切换时概率条宽度平滑过渡（transition: width 300ms ease）
```

### 18.5 负向：Accessibility（WCAG 2.1 AA）完全缺失

本 spec 全文未提及无障碍要求。对于一个面向公众的 GitHub Pages 站点，WCAG 2.1 AA 是基本合规要求。

**建议增加**：在 spec 中增加无障碍约束章节：

1. **颜色对比度**：所有文字-背景组合必须满足 WCAG AA 对比度 ≥ 4.5:1（正常文字）、≥ 3:1（大文字）。具体验证：
   - `#13233A` on `#FBF9F1` = ~13.5:1 ✅
   - `#C8A45C`（Yellow Source）on `#FBF9F1` = ~2.4:1 ❌ **不满足 AA**
   - **修正**：Yellow Source 标签改为深色文字 + 琥珀色背景徽章（`#C8A45C` bg + `#13233A` text）

2. **键盘导航**：所有交互元素可通过 Tab 键访问，焦点顺序匹配视觉顺序，Skip-to-content 链接。

3. **屏幕阅读器**：概率数值必须有 `aria-label`（如 `aria-label="主队胜率 52%，平局 24%，客队胜率 24%，来源：Agent 共识"`），球队国旗必须有 `alt` 文本，因子图标必须有 `aria-label`。

4. **语义 HTML**：使用 `<nav>`、`<main>`、`<article>`、`<section>`、`<table>` 包裹对应内容。

5. **减少动画**：尊重 `prefers-reduced-motion: reduce`，禁用所有过渡动画和脉冲效果。

6. **焦点指示器**：所有可聚焦元素必须有可见的 `:focus-visible` 指示器，颜色使用 `--border-focus`（Teal）。

### 18.6 正向：全景图应设计为"渐进式信息披露"而非"数据墙"

第 9.1 节描述的全景赛程图在概念上正确，但在 UX 执行层面，72 场比赛同时展示会造成"数据墙"效应——用户看到密密麻麻的概率数字，无法快速定位关注点。

**建议升级**：将全景图重构为三层渐进式信息披露架构：

**Layer 1 — 概览层（首屏）**：
- 今日焦点（2-4 场比赛大卡片）：占据首屏 60% 视觉权重
- Top 8 夺冠概率热力榜：横向条形图，占 30% 视觉权重
- 概率异动快报：3 条"昨日 vs 今日"变化最大的比赛/球队
- 用户 5 秒内理解"今天最值得关注什么"

**Layer 2 — 浏览层（滚动或点击"全部赛程"）**：
- 小组赛赛程矩阵，12 组按顺序排列，每组显示简化卡片（对阵 + 概率条）
- 提供"按日期"和"按小组"两种分组切换
- 用户 30 秒内找到自己关注的球队/比赛

**Layer 3 — 深度层（点击比赛/球队卡片）**：
- 侧边面板或新页面显示完整详情（概率时间线、Agent 派别分布、关键因子、新闻摘要）
- 用户 2-3 分钟内完成深度理解

**移动端适配**：Layer 1 垂直堆叠，Layer 2 改为小组选择器（下拉），Layer 3 全屏模态。

**理由**：渐进式信息披露是信息密集型仪表盘的最佳实践（参考 Bloomberg Terminal、FiveThirtyEight 选举模型）。用户不应被要求一次处理 72 场比赛的所有数据。

### 18.7 正向：概率条的"多源切换"是本 spec 最具创新性的交互模式，但需要更精确的 UX 规范

第 9.1.2 节的概率条 hover 切换设计是一个很好的想法，但当前描述过于简略。

**建议细化**：

```
┌──────────────────────────────────────────────┐
│ 🇲🇽 墨西哥          2:0          🇰🇷 韩国      │
│ ┌──────────────────────────────────────────┐ │
│ │████████████████░░░░░░░░░░░░░░░░░░░░░░░░░│ │  ← 概率条
│ │  52%             24%             24%     │ │
│ └──────────────────────────────────────────┘ │
│ [数值预测 ●] [市场赔率 ○] [Agent ○] [CDS ○]  │  ← 来源切换器
│  ⚠️ 伤病  🔥 状态  🌧️ 天气                   │  ← 因子图标
│  6/11 20:00 墨西哥城                         │
└──────────────────────────────────────────────┘
```

**切换行为**：
- 点击来源标签（非 hover）切换概率条显示——hover 切换会导致误触
- 切换时概率条宽度平滑过渡（`transition: width 400ms cubic-bezier(0.4, 0, 0.2, 1)`）
- 切换后概率条颜色微调：数值预测保持青色系，市场赔率切换为琥珀色系，Agent 共识为绿色系，CDS 推演为紫色系
- 当前选中的来源标签高亮（`font-weight: 600` + 下划线）

**偏差可视化**：当两个来源对同一场比赛的预测偏差 > 15% 时，显示 ⚡ 分歧指示器，点击打开分歧详情浮层。

### 18.8 负向：本 spec 的"认知校准器"交互存在 UX 风险

第 17 节审阅中提到"先押后揭晓"的交互模式，但若用户选择夺冠概率极低的球队（< 5%），展示排名可能让用户感到被冒犯——这不是"校准"而是"打脸"。

**建议修正**：

1. **不排名、不比较**：不展示"你的选择排第 X 名"。代之以"有 Y% 的 Agent 也看好这支球队"
2. **派别共鸣**：展示"你的思维模式最接近 XX 派"——正面反馈，暗示独特分析视角
3. **风险提示而非否定**：展示"XX 派提醒你注意 Z 个风险点"——建设性方式呈现反对意见
4. **概率语境化**：用历史数据提供语境（"过去 10 届世界杯中，有 3 支类似排名的球队杀入四强"）
5. **可选退出**：提供"跳过，直接查看全部数据"按钮

**文案约束**：
- ✅ "有 12% 的 Agent 也看好这支球队。数据派尤其认同你的判断。"
- ❌ "你的选择排第 23 名，只有 12% 的 Agent 同意你。"

### 18.9 正向：Motion Design 应作为"信息引导"而非"装饰"

本 spec 未提及动效设计。在信息密集的仪表盘中，动效的核心价值是引导用户注意力（"这里变了"）和解释空间关系（"这个卡片展开了"）。

**建议增加**：Motion Design 规范：

```css
--duration-instant:  100ms;  /* 按钮按下 */
--duration-fast:     200ms;  /* 卡片 hover */
--duration-normal:   300ms;  /* 概率条切换、面板展开 */
--duration-slow:     500ms;  /* 页面过渡 */
--duration-reveal:   800ms;  /* 首屏 count-up 动画 */

--ease-default:  cubic-bezier(0.4, 0, 0.2, 1);
--ease-enter:    cubic-bezier(0, 0, 0.2, 1);
--ease-exit:     cubic-bezier(0.4, 0, 1, 1);
```

**动效应用规范**：

| 场景 | 动效 | 时长 | 目的 |
|------|------|------|------|
| 概率数字更新 | count-up 数字滚动 | 800ms | 吸引注意"数据变了" |
| 概率条切换来源 | 宽度过渡 | 300ms | 平滑比较不同来源 |
| 比赛卡片 hover | 上浮 + 阴影增强 | 200ms | 暗示可点击 |
| 卡片点击展开 | 高度展开 + 内容淡入 | 300ms | 解释空间关系 |
| 概率异动高亮 | 脉冲光环 | 2s × 1次 | 标记"新变化" |

**概率异动动画**：当日概率变化 > 5% 的比赛卡片，初次加载时显示脉冲光环（`box-shadow: 0 0 0 0 var(--color-teal-400)` → `0 0 0 8px transparent`），光环消失后概率条以新值渲染。动效仅播放一次，用户可通过设置关闭。

### 18.10 负向：导航模型未定义，用户会迷失在页面层级中

本 spec 提到了多个页面（`index.html`、`team/{id}.html`、`match/{id}.html`、`report/daily-{date}.html`），但没有定义导航模型。

**建议修正**：定义全局导航模型：

**全局导航栏（固定顶部）**：
```
🏆 CDS4WorldCup  │ 全景图 │ 赛程 │ 球队 │ 日报 │ 关于
```

**面包屑导航（二级页面）**：
```
全景图 > 球队 > 阿根廷
全景图 > 赛程 > A组 > 阿根廷 vs 秘鲁
```

**移动端导航**：底部固定导航栏（类似 iOS Tab Bar），5 个图标按钮。

**当前位置指示**：导航栏中当前页面高亮（`font-weight: 600` + 下划线），面包屑中最后一项为当前页面（不可点击，灰色）。

### 18.11 正向：Loading/Empty/Error 状态的三层处理策略

本 spec 提到了"保留策略"和"降级模式"，但未从 UX 角度系统定义各种状态的展示策略。

**建议增加**：三层状态处理策略：

**第一层：数据抓取层（M1-M5）失败** → **Graceful Degradation with Timestamp**：
- M5 失败 → 概率条切换器中"市场赔率"选项置灰，显示 tooltip："市场数据暂不可用（最后更新: 2026-06-11）"
- 关键原则：部分数据缺失不阻塞页面展示，但必须明确标注哪些数据缺失、最后更新时间

**第二层：分析层（M6-M7）失败** → **Fallback to Previous Day**：
- M7 失败 → 展示昨日投票结果，顶部显示横幅："Agent 投票数据为昨日，今日数据正在重新生成中…"
- 关键原则：展示"最后已知的良好数据"而非空白

**第三层：发布层（GitHub Pages）部署失败** → **Static Fallback**：
- 保留上一次成功部署的页面，顶部显示静态横幅："数据更新于 YYYY-MM-DD，今日更新遇到技术问题"
- 关键原则：站点永远可访问，数据可能不是最新的但不会完全消失

### 18.12 正向：Agent 投票档案应作为"可探索的 UX 资产"而非纯数据存储

本 spec 将 Agent 投票档案视为数据存储，但从 UX 角度，投票档案是极具吸引力的内容资产。用户会好奇"300 个 AI 各自是怎么想的？"——这种好奇心是驱动深度交互的引擎。

**建议增加**：Agent 投票档案的可视化探索界面：

**Agent 画廊视图**（`/agents`）：300 个 Agent 缩略卡片（头像 + 派别 + 今日预测准确率），可按派别筛选、按"今日最准"/"今日最极端"/"今日改变立场"排序。

**Agent 档案页**（`/agents/{agent-id}`）：基本信息、预测历史时间线、准确率统计、最近预测理由全文、"最相似的 5 个 Agent"、"最分歧的 5 个 Agent"。

**Agent 辩论回放**（`/debate/{session-id}`）：来自 M6 CDS 推演的辩论记录，以对话气泡时间线展示，每轮辩论结束显示"本轮共识"和"本轮分歧"。

**实施优先级**：P3（Phase 3），不阻塞 MVP。但 Agent 档案的数据结构应在 Phase 1 设计好，确保后续可扩展。

### 18.13 负向：日报 UX 设计被过度简化为"Markdown 渲染"

本 spec 第 7.8 节将日报定义为 Markdown 文件，但 Markdown 渲染的日报在 UX 上表现不佳——缺乏交互性、图表静态、导航困难。

**建议修正**：日报应设计为结构化 HTML 页面，而非 Markdown 渲染：

**日报页面结构**（`/report/daily-2026-06-12.html`）：
- 顶部锚点导航：[执行摘要] [概率全景] [CDS推演] [Agent投票] [分歧观察]
- 执行摘要：3 句话总结 + 关键数字卡片（3 列）
- 小组赛概率全景：交互式热力矩阵 + 概率变化最大 3 场卡片
- CDS 夺冠推演：Treemap Top 8 + 路径节点变更表
- Agent 投票分析：10 派别堆叠条形图 + 派别分歧雷达图
- 市场 vs Agent 分歧：散点图 + 分歧最大 3 场比赛详情
- 明日关注：比赛预览卡片
- 关键交互：锚点跳转、图表 hover 详情、"返回顶部"浮动按钮、"上一日/下一日"切换

**理由**：日报是用户每天回访的核心内容。结构化 HTML 页面 + 交互式图表 + 导航锚点，让日报成为"产品"而非"文档"。

### 18.14 正向：应定义"首屏关键绩效指标"（Above-the-Fold KPIs）

本 spec 定义了数据质量指标，但没有定义 UX 质量指标。

**建议增加**：首屏 UX KPI：

| 指标 | 目标 | 测量方式 |
|------|------|---------|
| 首屏加载时间 | < 2s（3G 网络） | Lighthouse / WebPageTest |
| 首屏数据 payload | < 200KB（压缩后） | Chrome DevTools Network |
| 首屏可交互时间 (TTI) | < 3s | Lighthouse |
| 关键信息获取时间 | < 5s（用户找到今日焦点比赛） | 用户测试 |
| 移动端可用性 | 全部功能在 375px 宽度可用 | 响应式测试 |
| 可访问性评分 | Lighthouse Accessibility ≥ 90 | Lighthouse |
| 无 JS 可用性 | 核心内容在 JS 禁用时可见 | 手动测试 |
| 球队详情页到达率 | 从首页到球队详情 ≤ 2 次点击 | 信息架构验证 |

**无 JS 降级策略**：概率条默认显示数值预测（静态 HTML），JS 启用后增加来源切换；图表 JS 禁用时显示数据表格替代；导航使用 `<details>/<summary>` 实现折叠导航。

### 18.15 综合评论：本 spec 的架构设计扎实，但视觉设计系统严重欠规范

本 spec 在系统架构、数据管线、模块划分方面表现出色。第 2 节对三个参考项目（policysim、cds4polymarket、institute-one）的分析精准到位，第 6-7 节的 8 模块设计具有可执行性。

但从 UI/UX 设计架构的角度，本 spec 存在一个结构性缺陷：**将视觉设计视为"配色方案 + 页面布局"，而非"设计系统"**。具体表现为：

1. **颜色定义不完整**：6 个颜色值无法覆盖所有组件状态。需要 Layer 1-3 的完整 token 体系（见 18.1）
2. **Typography 缺失**：没有字号、字重、行高层级。信息层级无法落地（见 18.2）
3. **Spacing 缺失**：没有间距 scale。布局密度无法精确控制（见 18.3）
4. **Component States 缺失**：没有定义 hover/focus/active/disabled/loading/empty/error 状态（见 18.4）
5. **Accessibility 缺失**：没有 WCAG 合规要求（见 18.5）
6. **Motion Design 缺失**：没有动效规范（见 18.9）
7. **Navigation Model 缺失**：没有全局导航模型（见 18.10）

这些缺失不是"锦上添花"——它们直接影响实现阶段的一致性、可维护性和用户体验质量。如果 6 个颜色值在没有完整 token 体系的情况下进入开发，不同的开发者会自行推断 hover/focus 颜色，导致视觉不一致。

**建议行动**：在 Phase 0（基础设施）中增加"P0-7：Design Token 体系定义"任务，将 18.1-18.5 的 token 定义转化为 `site/wc2026/static/tokens.css` 文件。这是零依赖、纯 CSS 的任务，与 P0 的"零依赖"约束完全兼容。

---

> [!memo] 2026-06-12 DeepSeek-V4-Pro UI/UX 设计架构审查
>
> 来源：对本 spec 的独立审查，结合 policysim-research-Tsinghua、cds4polymarket、institute-one、Kimi Agent UI 升级包的交叉阅读。
> 上下文：本 spec 的架构设计扎实，但视觉设计系统存在结构性缺口：缺乏完整 design token 体系（三层）、typography scale、spacing system、component states 矩阵、accessibility 规范、motion design 规范和导航模型。本补充识别了 6 个负向修正和 8 个正向增强，核心建议是在 Phase 0 增加"P0-7：Design Token 体系定义"任务。
> 方法论：作为 UI/UX Design Architect，审查聚焦于设计系统的完整性、可执行性和跨组件一致性，而非功能需求或技术架构。
