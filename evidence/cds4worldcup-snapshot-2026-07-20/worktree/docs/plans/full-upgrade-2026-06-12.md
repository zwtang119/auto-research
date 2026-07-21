# CDS4WorldCup 全面升级计划

## Goal

构建数据基座 → 自动更新 → 主页同步 → 可回滚的完整升级管线。时间不限，全部推进。

## Background

### 当前项目状态（commit ec3a0be + dirty working tree）

**已完成的基线**：重构 PR-1~3 全部完成并提交（`ebd1bad` → `651cfaf` → `ec3a0be`），CSS bug 修复、escapeHtml 修复、`src/utils/` 提取、测试 7/7 通过。站点有 3 个页面（index/teams/team-detail），`build_site_data.py`（1324 行）驱动全部数据。

**未提交的工作树状态**：
- 3 modified：`AGENTS.md`、`docs/design/specs/2026-06-11-homepage-optimization-spec.md`、`wiki/index.md`
- 11 untracked：2 个 analysis 文档、1 个新 spec、1 个 MiMo 验收调查、1 个计划文档、1 个审阅文档、`mimo_boundary_check.py`、`predictions-data.js`（123KB，无对应 HTML）、`hero-bg.mp4`（2.3MB）、`group_difficulty.py`、1 个 wiki 决策文档
- 2 commits ahead of origin（未 push）

**关键数据问题**：
- **分组映射不一致**：`team_registry.csv` 将阿根廷列为 B 组、法国列为 C 组，但 Wikipedia draw 数据显示阿根廷在 J 组、法国在 I 组。`team_registry.csv` 使用的是更早的分组方案。
- **Wikipedia 原始数据未接入**：`wiki-wc2026-main.json`（229KB，含完整赛程）和 `wiki-wc2026-draw.json`（含分组抽签）未被任何脚本消费
- `wiki-wc2026-groups.json` 获取失败（`missingtitle` 错误）
- 5/6 baselines 为 `designed_not_populated`
- `source_gap_map.csv` 未接入管线
- 27/48 队为 thin-slice

### 可复用的预研资源（cds4polymarket 项目）

cds4polymarket 已完成大量预研，无需重新研究：

| 预研文档 | 路径 | 关键收获 |
|----------|------|---------|
| OSS 组件分析 | `docs/comparisons/external-components-analysis.md` | 8 个外部项目已评估许可证和集成深度，MetaGPT（Agent 角色）、ChatArena（辩论模拟）、BettaFish（多 Agent 论坛）可直接参考 |
| 深度模式审计 | `docs/comparisons/external-code-phase2-deep-pattern-audit-2026-05-22.md` | 12 个可采纳模式 + Python 接口签名 + 测试矩阵，含 wikilink 自动注入、cooldown 重试、frontmatter 解析、LLM JSON 提取 |
| 遗留代码模式 | `docs/comparisons/external-code-phase2-legacy-repo-migration-audit-2026-05-22.md` | 31 个可采纳概念：`ServiceResult[T]`、`SimulationState` 状态机、Arena 编排器、`EnterpriseDNA` 5 维 schema、熔断器模式 |
| LLM 评估方法论 | `docs/concepts/llm-judge-evaluation-methodology.md` | Pairwise 评分、校准集、温度设置、5 维评估框架、inter-rater 可靠性指标 |
| 世界杯实验蓝图 | `docs/superpowers/specs/2026-06-10-worldcup-paper-track-and-experiment-optimization-design.md` | CSV 数据结构、实验流程、baseline 策略、多 judge 系统设计、滚动知识更新协议 |
| 实验优先级 | `docs/superpowers/specs/2026-06-10-kimi-300-agent-brainstorm-synthesis-v2.md` | P0 数据门控 → P1 Marginalia/Factor → P2 双 Kimi 分歧 → P3 Monte Carlo |
| 跨项目复用清单 | `archive/design-docs/CDS_跨项目复用分析_2026-05-01.md` | PolicySimulation-Paper 有 ~70% 所需能力，含 BatchRunner、Arena 编排器、DNAService |
| 技术栈对比 | `docs/comparisons/tech-stack-comparison.md` | Python/FastAPI 推荐 AI 密集型工作 |

### 可复用的代码模式（cds4polymarket 源码）

| 模式 | 位置 | 可复用性 |
|------|------|---------|
| Arena 多 Agent 辩论 | `apps/api/src/engine/arena.ts:15-47` | 47 行核心循环，直接参照用 Python 重写 |
| LLMProvider 抽象 | `llm/provider.ts:10-82` | retry + fallback + JSON extraction 模式 |
| VaultManager 原子写入 | `services/vault-manager.ts:4-56` | tmp + renameSync 模式 |
| 7 阶段管线编排 | `pipeline-stages.ts:34-351` | 阶段模式：start → trace → progress → end |
| 聚合系统 | `aggregation.ts:49-256` | keyword 提取 + LLM synthesis 双层聚合 |
| 质量评估 | `quality-evaluator.ts:5-113` | 5 维度 LLM-as-judge 评分 |

## Approach

### 关键决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 分组数据权威来源 | **Wikipedia draw 数据**（`wiki-wc2026-draw.json`） | 官方抽签结果，team_registry.csv 使用的是早期预估分组 |
| 站点策略 | **扩展现有 `site/`** | 已有 3 页面 + 1397 行 CSS + 完整数据管线，新建站点是浪费 |
| 管线策略 | **扩展 `build_site_data.py`** | 1324 行单体脚本已验证可靠，新增函数而非另起新脚本 |
| LLM 调用方式 | **Python batch 脚本 + LLM API** | MiMo Code 不能 spawn 子进程；参照 cds4polymarket 的 `LLMProvider` retry+fallback 模式 |
| 图表技术 | **纯 CSS + 原生 JS SVG** | 零依赖约束；条形图用 CSS，热力图/时间线用 JS 生成 SVG |
| Agent 投票量级 | **L2：当日比赛 ~1,500 runs/日** | 全量 21,600 runs 成本高、价值增量有限 |
| LLM 提供商 | **MiniMax-M3** | 用户确认；API 兼容 OpenAI 格式；成本远低于 GPT-4 级模型 |

### GitHub Pages 部署约束

本项目部署在 GitHub Pages 上，这是架构的根本约束。所有设计必须遵守：

| 约束 | 影响 |
|------|------|
| **纯静态文件** | 所有数据在构建期预计算为 JSON/JS 文件，浏览器零 API 调用 |
| **构建链路** | `pages.yml` 在 push main 时触发：`checkout → build_site_data.py → 复制 site/ → _publish/ → deploy` |
| **每日更新机制** | 必须通过 GitHub Actions `schedule` 触发 → 运行数据脚本 → **commit 新数据 → push to main** → `pages.yml` 自动重建部署 |
| **双步 CI 流程** | Step 1: `daily-update.yml` 运行 M1-M8 脚本，commit `data/ops/daily-runs/` + `data/processed/` 聚合结果，push to main。Step 2: `pages.yml` 检测 push，运行 `build_site_data.py` 重建站点并部署 |
| **超时限制** | GitHub Actions 默认 6h（`schedule` 触发）。1,500 次 MiniMax-M3 API 调用（每次 ~2-5s）≈ 1-2h，在限制内 |
| **仓库大小** | GitHub 推荐 < 1GB。原始 Agent 投票 + prompt logs 每日 ~150MB — **不可提交到 Git**。策略：只 commit 聚合结果（~720KB/日），原始数据用 `.gitignore` 或本地存储 |
| **Secrets** | MiniMax API key 存为 `SECRETS.MINIMAX_API_KEY`，在 `daily-update.yml` 中通过 `${{ secrets.MINIMAX_API_KEY }}` 注入环境变量 |
| **并发保护** | `pages.yml` 已有 `concurrency: group: pages, cancel-in-progress: true`。`daily-update.yml` 需类似配置，防止两次每日运行重叠 |
| **权限** | `daily-update.yml` 需要 `contents: write` 权限以 commit + push 数据到 main |

### 数据流架构

```
外部数据源                    脚本层                    构建层                   前端
─────────────────────────────────────────────────────────────────────────────────────
Wikipedia draw/main    → scripts/parse_schedule.py  ─┐
Polymarket Gamma API   → scripts/fetch_market_snapshot.py ─┤
NewsAPI + RSS feeds    → scripts/fetch_news.py       ─┤
Transfermarkt scrape   → scripts/fetch_players.py    ─┤   scripts/          site/
Elo + Poisson model    → scripts/numeric_odds.py     ─┼→ build_site_data.py → *.json
LLM API (Agent voting) → scripts/agent_voting.py     ─┤   + new functions    + *.js
LLM API (CDS debate)   → scripts/cds_debate.py       ─┤
LLM API (Report gen)   → scripts/generate_report.py  ─┘
                                                      ↓
                                              git push → GitHub Pages
```

所有新脚本输出到 `data/ops/daily-runs/YYYY-MM-DD/`，`build_site_data.py` 从最新数据目录读取并生成前端 JSON。

**每日部署流程**（GitHub Pages 约束下的双步 CI）：

```
UTC 00:00  GitHub Actions schedule 触发 daily-update.yml
    ↓
    Step 1: 运行 M1-M8 数据脚本
      → fetch_market_snapshot.py（市场快照）
      → fetch_news.py（新闻摘要）
      → fetch_players.py（球员状态）
      → numeric_odds.py（数值预测）
      → agent_voting.py（Agent 投票，~1,500 MiniMax-M3 API calls）
      → cds_debate.py（CDS 辩论，~20 MiniMax-M3 API calls）
      → aggregation.py（概率聚合）
    ↓
    Step 2: commit 聚合结果 + data/processed/ 更新
      → git add data/ops/daily-runs/YYYY-MM-DD/aggregation/
      → git add data/processed/*.json（市场快照、聚合数据）
      → git commit -m "daily update YYYY-MM-DD"
      → git push origin main
    ↓
    pages.yml 自动触发（检测到 push to main）
      → checkout → build_site_data.py → _publish/ → deploy
    ↓
    线上站更新完成
```

**数据保留策略**（控制仓库大小）：
- ✅ Git 提交：聚合结果（`aggregation/*.json`）、市场快照、赛程数据、构建产物（`site/data/*.json`）
- ❌ Git 忽略：原始 Agent 投票（`agent-votes/raw/`）、prompt logs、新闻全文（`.gitignore` 规则）
- 📦 本地归档：超过 30 天的原始数据移至 `data/ops/daily-runs/archive/`（本地存储，不提交）

### 回滚策略

1. **Git tag checkpoint**：每个 Phase 完成后打 tag（`upgrade-phase-N-done`），可随时 `git checkout` 回滚
2. **原子写入**：所有数据文件写入遵循 tmp + rename 模式（参照 cds4polymarket `VaultManager`），防止半写
3. **`_publish/` 暂存**：`Makefile` 的 `make results` 先构建到 `_publish/`，验证后再 push
4. **数据快照**：`data/ops/daily-runs/YYYY-MM-DD/manifest.json` 记录每次运行的完整性状态
5. **人工介入点**：`data/ops/review_queue/` 中的文件需人工审核后才能 promotion

### MiMo 边界

| 区域 | MiMo 可写 | 需人工审批 |
|------|----------|-----------|
| `data/ops/candidate/` | ✅ | ✅ promotion 前 |
| `data/ops/mimo_outputs/` | ✅ | ❌ |
| `results/ops/` | ✅ | ❌ |
| `scripts/`, `site/`, `wiki/` | ❌ | — |

### 核心链路

**Phase 0**（checkpoint + 数据校正）→ **Phase 1**（数据基座 M1+M5+M4）→ **Phase 2**（前端全景图）→ **Phase 3**（AI 分析管线 M6+M7）→ **Phase 4**（持续运营 M2+M3+M8）

每个 Phase 完成后：打 tag → push → 验证线上站 → 下一 Phase。

---

## Work Items

### Phase 0: Checkpoint + 数据校正

#### WI-0.1 创建 checkpoint

- **Goal**: 冻结当前工作树状态为可回滚的 checkpoint
- **Done when**: git tag `checkpoint-pre-upgrade-2026-06-12` 存在；working tree 无未跟踪文件
- **Key files**: 无新文件
- **Steps**: (1) resolve `hero-bg.mp4`（2.3MB 二进制文件 — 加入 `.gitignore` 或 Git LFS） (2) resolve `predictions-data.js`（123KB 孤立数据 — 加入 `.gitignore` 或 commit） (3) commit all uncommitted changes (3 modified + 10 untracked) (4) push to origin (5) `git tag checkpoint-pre-upgrade-2026-06-12` (6) push tag
- **Dependencies**: 无
- **Size**: S (30min)

#### WI-0.2 校正分组数据

- **Goal**: 将 `team_registry.csv` 的分组映射与 Wikipedia 最终抽签结果对齐
- **Done when**: (1) 解析 `wiki-wc2026-draw.json` 提取 12 组 × 4 队的正确分组 (2) 更新 `team_registry.csv` 中所有 48 队的 group 列 (3) 替换不在实际参赛名单中的 10 队（Chile/Costa Rica/Italy/Denmark/Poland/Ukraine/Wales/Venezuela/Nigeria/Cameroon → South Africa/Czech Republic/Bosnia/Haiti/Scotland/Curaçao/Sweden/Cape Verde/DR Congo/Jordan） (4) `build_site_data.py` 重新生成后所有 team 的 group 字段正确
- **Key files**: `data/processed/team_registry.csv`, `data/ops/mimo_outputs/wiki-wc2026-draw.json`
- **Dependencies**: WI-0.1
- **Size**: L (1d)
- **Risk**: ⚠️ **Design critique 发现实际差异为 21 队（11 队缺失 + 10 队多余 + 全部 48 队分组重映射）。** Wikipedia draw 数据是原始 wikitext（`{{#invoke:flag|fb|MEX}}` 模板标记），不是结构化 JSON。解析策略需在实施时确定：正则提取、Python wikitext 解析器、或手动编写映射表。本 WI 可能需要拆分为子步骤：WI-0.2a（wikitext → 结构化 draw JSON）、WI-0.2b（registry rebuild + name_map + team cards）、WI-0.2c（下游数据重新生成）
- **Also requires**: 更新 `team_name_map.csv`（新队伍名映射）和 `artifacts/team-cards/`（为 10 支新队创建卡片、删除 10 支旧队卡片）

#### WI-0.3 验证管线完整性

- **Goal**: 确认数据校正后整条管线仍然健康
- **Done when**: (1) `python3 -m unittest discover -s tests -v` 全部通过 (2) `python3 scripts/build_site_data.py` 成功 (3) `python3 scripts/audit.py --root wiki/` 无新错误 (4) 本地 HTTP server 验证首页/球队页/详情页正常渲染
- **Key files**: `scripts/build_site_data.py`, `tests/test_build_site_data.py`
- **Dependencies**: WI-0.2
- **Size**: S (1h)

#### WI-0.4 Phase 0 tag

- **Goal**: 标记 Phase 0 完成
- **Done when**: `git tag upgrade-phase-0-done` 存在
- **Dependencies**: WI-0.3
- **Size**: S (5min)

---

### Phase 1: 数据基座（M1 赛程 + M5 市场自动化 + M4 数值预测）

#### WI-1.1 赛程解析器（M1）

- **Goal**: 将 Wikipedia 原始数据解析为结构化赛程 JSON，接入 `build_site_data.py`
- **Done when**: (1) `scripts/parse_schedule.py` 从 `wiki-wc2026-main.json` 和 `wiki-wc2026-draw.json` 解析出 72 场小组赛 + 淘汰赛结构 (2) 输出 `data/processed/schedule.json`（每场含 match_id, group, round, date, venue, home/away, status） (3) `build_site_data.py` 新增 `build_schedule_json()` 函数产出 `site/data/schedule.json` (4) 测试覆盖
- **Key files**: 新建 `scripts/parse_schedule.py`, 修改 `scripts/build_site_data.py`
- **Dependencies**: WI-0.3
- **Size**: L (1d)
- **Reference**: cds4polymarket `VaultManager` 原子写入模式

#### WI-1.2 市场快照自动化（M5 增强）

- **Goal**: 添加 GitHub Actions 定时任务，每日自动刷新市场快照
- **Done when**: (1) `.github/workflows/market-snapshot.yml` 配置 `schedule: cron: '0 0 * * *'` + `workflow_dispatch` (2) 运行 `fetch_market_snapshot.py` → **commit `data/processed/market_public_snapshot.json`** → **push to main** → `pages.yml` 自动重建 (3) 失败时不阻塞（graceful degradation，展示上一日快照 + 标注） (4) `concurrency: group: market-snapshot` 防止重叠
- **Key files**: 新建 `.github/workflows/market-snapshot.yml`
- **Dependencies**: WI-0.3
- **Size**: S (2h)
- **GitHub Pages 约束**: workflow 需要 `permissions: contents: write`，commit 后 push to main 触发 `pages.yml`

#### WI-1.3 数值预测基线（M4）

- **Goal**: 实现 Elo 预期得分 + 泊松分布的纯 Python 预测模型
- **Done when**: (1) `scripts/numeric_odds.py` 输出每场比赛的 home_win/draw/away_win 概率 (2) 基于 FIFA 排名（可用 `team_registry.csv` 中的数据或从 FIFA 官网抓取）+ 近期场均进球/失球模拟（注：xG 数据源待定，初始版本可用历史比赛统计代替） (3) 来源标记为 Red Source (4) `build_site_data.py` 新增 `build_odds_json()` 产出 `site/data/odds.json` (5) 测试覆盖
- **Key files**: 新建 `scripts/numeric_odds.py`, 修改 `scripts/build_site_data.py`
- **Dependencies**: WI-1.1（赛程数据是输入）
- **Size**: L (1d)
- **Reference**: cds4polymarket `ServiceResult[T]` 统一返回模式

#### WI-1.4 Baseline 填充

- **Goal**: 填充 5 个空 baseline 的实际数据
- **Done when**: `baseline_suite_registry.csv` 至少 3 个 baseline 变为 `populated`（FIFA ranking proxy, Elo proxy, market public）
- **Key files**: `data/processed/baseline_suite_registry.csv`, 新建对应的数据文件
- **Dependencies**: WI-1.3
- **Size**: M (4h)

#### WI-1.5 Phase 1 tag

- **Goal**: 标记数据基座完成
- **Done when**: `git tag upgrade-phase-1-done`；`schedule.json` + `odds.json` + 市场自动刷新全部在线
- **Dependencies**: WI-1.4
- **Size**: S (5min)

---

### Phase 2: 前端全景图

#### WI-2.1 全景赛程页面

- **Goal**: 新增 `site/panorama.html` 展示 12 组 × 3 轮赛程矩阵 + 概率热力 + 因子标注
- **Done when**: (1) `site/panorama.html` + `site/js/panorama.js` 渲染赛程矩阵 (2) 每场比赛卡片显示对阵 + 概率条（数值/市场/Agent 三色） + 关键因子图标 (3) 点击卡片弹出比赛详情或跳转 match.html (4) 移动端自动切换日期聚合视图 (5) CSS Grid 布局，沿用 `portal.css` 变量
- **Key files**: 新建 `site/panorama.html`, `site/js/panorama.js`, 修改 `site/css/portal.css`
- **Dependencies**: WI-1.1, WI-1.3
- **Size**: XL (3d)
- **Reference**: Spec §9.1 的卡片设计和 §17.9 的 Heat Zone 编码

#### WI-2.2 比赛详情页

- **Goal**: 新增 `site/match.html` 展示单场比赛的深度分析
- **Done when**: (1) 三条概率时间线（数值/市场/Agent）用纯 JS SVG 渲染 (2) Agent 派别分布条形图（纯 CSS） (3) 关键因子浮层 (4) 相关新闻摘要区
- **Key files**: 新建 `site/match.html`, `site/js/match.js`
- **Dependencies**: WI-1.1, WI-1.3
- **Size**: L (1d)

#### WI-2.3 球队详情增强

- **Goal**: 扩展现有 `team.html` 添加夺冠概率时间线和路径卡动态更新
- **Done when**: (1) 夺冠概率时间线（CDS/数值/市场三线） (2) 路径卡节点概率标注 (3) 阻力记录可视化 (4) `team-detail.js` 新增渲染函数
- **Key files**: 修改 `site/team.html`, `site/js/team-detail.js`, `site/css/portal.css`
- **Dependencies**: WI-1.3, WI-1.4
- **Size**: L (1d)

#### WI-2.4 导航整合

- **Goal**: 主页 → 全景图 → 球队 → 比赛的完整导航链
- **Done when**: (1) `index.html` 的 topbar 新增"全景图"链接 (2) 全景图中的球队名可跳转 team.html (3) 比赛卡片可跳转 match.html (4) 所有页面有面包屑导航
- **Key files**: 修改 `site/index.html`, `site/panorama.html`, `site/css/portal.css`
- **Dependencies**: WI-2.1, WI-2.2, WI-2.3
- **Size**: M (4h)

#### WI-2.5 构建管线集成 + 验证

- **Goal**: 确保 `build_site_data.py` 产出全景图所需的全部数据，端到端验证
- **Done when**: (1) `build_site_data.py` 产出 `schedule.json`, `odds.json`, `panorama.json` (2) `make results` 成功构建完整站点 (3) 桌面/平板/移动端全路径可用 (4) 测试覆盖新数据契约
- **Key files**: 修改 `scripts/build_site_data.py`, `tests/test_build_site_data.py`
- **Dependencies**: WI-2.4
- **Size**: M (4h)

#### WI-2.6 Phase 2 tag

- **Dependencies**: WI-2.5
- **Size**: S (5min)

---

### Phase 3: AI 分析管线（M6 CDS 辩论 + M7 Agent 投票）

#### WI-3.1 LLM API 客户端（MiniMax-M3）

- **Goal**: 统一的 LLM 调用基础设施，基于 MiniMax-M3 API
- **Done when**: (1) `scripts/llm_client.py` 封装 MiniMax-M3 API 调用（OpenAI 兼容格式） (2) 支持 retry(3次) + exponential backoff + token 记录 + prompt log (3) JSON 提取（处理 markdown code block 包裹） (4) API key 从环境变量 `MINIMAX_API_KEY` 读取（GitHub Actions 通过 secrets 注入） (5) 成本追踪：每次调用记录 input/output tokens (6) 测试覆盖
- **Key files**: 新建 `scripts/llm_client.py`
- **Dependencies**: WI-0.3
- **Size**: L (1d)
- **Reference**: cds4polymarket `llm/provider.ts:10-82` retry+fallback+JSON extraction
- **Cost estimate**: MiniMax-M3 ~1,500 runs/日 × ~4K input + 500 output tokens ≈ ~6.75M tokens/日；MiniMax-M3 定价约 ¥1/M input + ¥2/M output → 每日约 ¥10-15

#### WI-3.2 Agent 人格与派别配置

- **Goal**: 定义 10 派别 × 30 Agent 的人格配置文件
- **Done when**: (1) `config/factions/` 下 3-4 个初始派别配置（迭代扩展到 10 个） (2) 每派别含关注维度、数据权重、persona 模板 (3) 可被 `agent_voting.py` 和 `cds_debate.py` 加载
- **Key files**: 新建 `config/factions/*.yaml`
- **Dependencies**: WI-1.1（派别配置需引用 schedule.json 的比赛结构）
- **Size**: M (4h)
- **Note**: **Design critique 建议**: 先用 3-4 个派别验证 LLM 输出确实有差异，再扩展到 10 个。避免 10 个固定 persona 的前提是 prompt engineering 第一次就能成功。

#### WI-3.3 上下文压缩器

- **Goal**: 将 M1-M5 的当日数据压缩到 Agent 可消费的 4K token 预算内
- **Done when**: (1) `scripts/context_compressor.py` 接收当日数据目录，输出压缩后的上下文字符串 (2) key_findings 优先，原始文本截断 (3) 测试覆盖压缩率和信息保留
- **Key files**: 新建 `scripts/context_compressor.py`
- **Dependencies**: WI-1.3
- **Size**: M (4h)

#### WI-3.4 Agent 投票系统（M7）

- **Goal**: Python batch 脚本执行 L2 量级 Agent 投票（~1,500 runs/日，仅当日比赛）
- **Done when**: (1) `scripts/agent_voting.py` 按 `config/factions/` 配置生成投票 (2) 每个 Agent 接收压缩上下文，输出结构化 JSON（prediction, confidence, reason, key_factors） (3) Jaccard 防模板化检查（阈值 0.7） (4) 聚合算法：原始得票率 + 信心加权 + 派别分歧指数 (5) 输出到 `data/ops/daily-runs/YYYY-MM-DD/agent-votes/` (6) 测试覆盖
- **Key files**: 新建 `scripts/agent_voting.py`, `scripts/aggregation.py`
- **Dependencies**: WI-3.1, WI-3.2, WI-3.3
- **Size**: XL (3d)
- **Reference**: cds4polymarket `Arena` 47 行核心循环 + `aggregation.ts` 双层聚合

#### ~~WI-3.5 CDS 辩论系统（M6）~~ — ⚠️ SUPERSEDED

> **Superseded** by `docs/plans/panoramic-review-cds-pipeline-2026-06-12.md` WI-PAN.3/5 (`cds_path_simulation.py`).
> The panoramic plan replaces the debate-style CDS with a two-layer simulation engine (qualification + championship), which is more tractable and directly fills team-card §7 fields.
> **Do NOT implement `cds_debate.py`.** The Arena debate concept may be revisited later as a reporting layer, but the core CDS engine is now the path simulation approach.

- ~~**Goal**: 多 Agent 辩论推演夺冠路径，参照 cds4polymarket 的 Arena 模式~~
- **Status**: SUPERSEDED — see panoramic plan WI-PAN.3 (qualification) + WI-PAN.5 (championship)
- **Original scope**: `scripts/cds_debate.py` with 3-stage debate protocol — no longer needed
- **Dependencies**: None (removed from dependency chain; WI-4.3 should not reference this item)

#### WI-3.6 前端 AI 数据集成

- **Goal**: 将 Agent 投票和 CDS 辩论结果接入前端展示
- **Done when**: (1) `build_site_data.py` 新增函数读取投票/辩论数据 (2) 全景图页面展示 Agent 共识概率 (3) 球队详情页展示 CDS 推演结果 (4) 比赛详情页展示派别分布 (5) 所有 AI 数据标注"只能参考"标签
- **Key files**: 修改 `scripts/build_site_data.py`, `site/js/panorama.js`, `site/js/match.js`, `site/js/team-detail.js`
- **Dependencies**: WI-3.4, WI-3.5, WI-2.5
- **Size**: L (1d)

#### WI-3.7 Phase 3 tag

- **Dependencies**: WI-3.6
- **Size**: S (5min)

---

### Phase 4: 持续运营（M2 新闻 + M3 球员 + M8 日报）

#### WI-4.1 新闻抓取（M2）

- **Goal**: 每日抓取 48 队相关新闻，LLM 摘要，Yellow Source 标注
- **Done when**: (1) `scripts/fetch_news.py` 使用 NewsAPI（免费 tier 500 req/day）+ ESPN/BBC RSS 备份 (2) 按队关键词过滤，每队 3-5 条摘要 (3) 输出 `data/ops/daily-runs/YYYY-MM-DD/news/` (4) 前端比赛/球队页面展示相关新闻
- **Key files**: 新建 `scripts/fetch_news.py`
- **Dependencies**: WI-0.3, **WI-3.1**（LLM 摘要调用）
- **Size**: L (1d)

#### WI-4.2 球员状态（M3）

- **Goal**: 每日抓取核心球员伤病/红黄牌/出场状态
- **Done when**: (1) `scripts/fetch_players.py` 抓取 Transfermarkt 伤病列表 (2) LLM 提取结构化数据（球员/伤病/状态/恢复时间） (3) 与昨日 diff 识别变化 (4) 输出 `data/ops/daily-runs/YYYY-MM-DD/players/` (5) 前端球队详情展示球员状态
- **Key files**: 新建 `scripts/fetch_players.py`
- **Dependencies**: WI-0.3, **WI-3.1**（LLM 提取调用）
- **Size**: L (1d)

#### WI-4.3 每日编排器

- **Goal**: 串联 M1-M8 的每日运行
- **Done when**: (1) `scripts/daily_orchestrator.py` 按 M1→M5→M4→M7→M6→M8 顺序执行 (2) 输出 `manifest.json` 记录各模块状态 (3) 单模块失败不阻塞后续模块 (4) 可手动触发（`python3 scripts/daily_orchestrator.py --date YYYY-MM-DD`） (5) GitHub Actions `schedule` 触发（`daily-update.yml`，cron UTC 00:00） (6) **执行完毕后 commit 聚合结果 + push to main** → 触发 `pages.yml` 自动重建部署 (7) `concurrency` 配置防止重叠运行 (8) 需要 `contents: write` 权限
- **Key files**: 新建 `scripts/daily_orchestrator.py`, 新建 `.github/workflows/daily-update.yml`
- **Dependencies**: WI-3.4, WI-3.5, WI-4.1, WI-4.2
- **Size**: L (1d)
- **GitHub Pages 约束**: workflow 需要 (a) `permissions: contents: write` (b) commit 后 push to main (c) 只 commit 聚合结果（不 commit 原始投票/prompt logs），控制仓库大小 (d) `concurrency: group: daily-update` 防止重叠

#### WI-4.4 日报生成（M8）

- **Goal**: 基于 M1-M7 数据自动生成每日分析报告
- **Done when**: (1) `scripts/generate_report.py` 聚合当日数据为日报 Markdown (2) 报告含：概率漂移分析、市场 vs Agent 分歧、派别信号、球队状态趋势 (3) **初始版本**：纯 Markdown 报告存 `results/daily/`，通过 GitHub Pages 直接渲染 (4) 来源声明和免责声明自动附加 (5) **后续版本**：matplotlib 预生成 PNG + `site/report.html` 渲染
- **Key files**: 新建 `scripts/generate_report.py`; 后续版本：`site/report.html`, `site/js/report.js`
- **Dependencies**: WI-4.3, WI-2.5
- **Size**: L (1d)（初始 Markdown 版本）；后续 HTML 版本另加 L (1d)

#### WI-4.5 Phase 4 tag

- **Dependencies**: WI-4.4
- **Size**: S (5min)

---

### 回滚检查点总览

```
checkpoint-pre-upgrade-2026-06-12   ← WI-0.1
        ↓
upgrade-phase-0-done                ← 数据校正完成
        ↓
upgrade-phase-1-done                ← 数据基座完成
        ↓
upgrade-phase-2-done                ← 前端全景图完成
        ↓
upgrade-phase-3-done                ← AI 分析管线完成
        ↓
upgrade-phase-4-done                ← 持续运营闭环
```

任何阶段可 `git checkout upgrade-phase-N-done` 回滚。

## Open Questions

1. ~~分组映射不一致~~ → **已决策**：以 Wikipedia draw 为准，WI-0.2 执行校正
2. 2 个本地 commits 需要 push — 是否在 checkpoint 之前 push？
3. ~~LLM 提供商~~ → **已决策**：MiniMax-M3（OpenAI 兼容格式，~¥10-15/日）
4. xG 数据源 — WI-1.3 的泊松模型初始版可用历史统计替代，后续再考虑 xG 数据接入

## References

- `docs/design/specs/2026-06-12-homepage-optimization-spec.md` — 完整升级 Spec（1286 行）
- `docs/plans/homepage-optimization-spec-review-2026-06-12.md` — Spec 审查报告
- `docs/analysis/2026-06-12-mimo-file-research-factory-for-pm.md` — MiMo 工厂运营模式
- `docs/analysis/2026-06-12-project-optimization-for-aiworker.md` — AI Worker 优化指南
- `docs/design/specs/2026-06-12-refactoring-fixes-spec.md` — 重构修复 Spec（PR-1~3 已完成）
- `docs/investigations/refactoring-validation-2026-06-12.md` — 重构验证报告
- cds4polymarket: `docs/comparisons/external-code-phase2-deep-pattern-audit-2026-05-22.md`
- cds4polymarket: `docs/superpowers/specs/2026-06-10-worldcup-paper-track-and-experiment-optimization-design.md`
- cds4polymarket: `docs/concepts/llm-judge-evaluation-methodology.md`
