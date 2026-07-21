# 2026-06-12 Homepage Optimization Spec: 升级讨论与审查

## Goal

对 `docs/design/specs/2026-06-12-homepage-optimization-spec.md`（1286 行）进行批判性审查，评估其升级方案的合理性、完整性和可执行性，并给出分阶段实施建议。

## Background

### 现有站点能力（基于代码探查）

**页面清单**：3 个 HTML 页面，已完整实现。
- `site/index.html`（171 行）— 主页门户：hero、8 队 teaser、AI 多视角、障碍矩阵、基线、市场信号、外部参照图
- `site/teams.html` — 48 队筛选网格，支持搜索/大洲/深度过滤
- `site/team.html` — 单队详情页：分析区块、AI 视角、障碍/突破/黑天鹅列表、图表

**数据契约**：`build_site_data.py`（1324 行）驱动全部数据，输入 → 6 个 JSON 输出。
- 输入：48 队卡片（`artifacts/team-cards/*.md`）、Kimi 300 Agent baseline、Polymarket 快照、CSV 矩阵
- 输出：`teams.json`、`homepage.json`、`team-details.json` + 对应的 inline JS fallback
- 关键函数：`build_teams_json()`（L151）、`build_homepage_json()`（L229）、`build_public_team_details_json()`（L617）
- 安全机制：`_sanitize_public_text()`（L335）替换厂商名、`_validate_public_text_boundary()`（L343）运行时拦截

**视觉系统**：`portal.css`（1397 行），暖纸感设计系统。
- CSS 变量：`--ink #15231e`、`--paper #eef3ea`、`--accent #0f6b4b`、源级标签 green/amber/red
- 断点：900px（双列→单列）、640px（全部堆叠）
- 组件库：`.panel`、`.team-card`、`.source-badge`、`.faction-card`、`.bar-chart`、`.mini-matrix`、`.ref-compare-chart`

**已有数据管线**：
- `fetch_market_snapshot.py`（187 行）— Polymarket Gamma API → `market_public_snapshot.json`，已集成
- 6 个 baseline 定义（`baseline_suite_registry.csv`）— **已设计但未填充数据**
- Wikipedia MiMo 输出（233KB + 81KB + 22KB JSON）— **原始转储，未接入管线**
- Source gap map 显示 0 支队有 Green Source

**CI/CD**：
- `ci.yml`：PR/push 触发 — wiki audit、敏感文件检查、markdown lint、结构完整性、secret scan、单元测试
- `pages.yml`：push main 触发 — build site data → 复制 site/ → 部署 GitHub Pages
- **无定时任务**：市场快照需手动运行，无 `cron`/`schedule` 触发

### 已知未解决的问题

1. **P0 CSS `@media` 包装缺失**（`portal.css:1334-1377`）— 桌面端被强制单列布局，阻塞部署
2. **P1 外部参照图不完整** — 标题说"AI 模型群体 vs 市场参考"但只渲染了市场数据
3. **P1 禁用词列表不完整** — 运行时校验器缺少 `小米`、`MiMo`、`投注建议`、`value bet`
4. **CI 未跑 Python 单元测试** — 回归风险
5. **`public_consensus_gap` 硬编码为 `not_available`** — 无实际计算逻辑

### Spec 的核心提案（简化）

- **8 个 MiMo Code 模块**（M1 赛程 → M8 日报），每日自动运行
- **300 Agent 投票系统**（10 派别 × 30 Agent），SASR 模式
- **多 Agent 辩论**（4-6 Agent MAMR 模式），CDS 夺冠推演
- **交互式全景图**（`site/wc2026/` 新站点），赛程矩阵 + 概率热力 + 点击下钻
- **Wiki 全面重构**：`wiki/teams/`（48 队）、`wiki/players/`、`wiki/matches/`（72+ 场）、`wiki/analysis/daily/`
- **7 周执行计划**，Phase 0-5

---

## 第一部分：Spec 评估（分维度打分）

### 维度 1：架构合理性 — 2/5

**一句话**：Spec 提出 `site/wc2026/` 作为全新站点，但 `site/` 下已有 3 个完整页面（`index.html` 171 行、`teams.html`、`team.html` 105 行）、1397 行 CSS 设计系统、457 行 `homepage.js` 渲染逻辑，以及完整的 JSON 数据契约。新建站点意味着放弃这些已验证的资产。

**支撑理由**：

1. **双站点维护负担**：现有 `site/` 需要继续维护（已部署、有用户），同时维护 `site/wc2026/` 会导致 CSS 变量、组件类名、数据清洗逻辑（`_sanitize_public_text()` at `build_site_data.py:335`）两套体系。任何来源政策或禁用词列表的更新都需要同步两处。

2. **数据管线冲突**：`build_site_data.py`（1324 行）是唯一的数据构建入口，输出到 `site/data/`。Spec 提出新的 `src/publish/build_site_data.py` 产生 `site/wc2026/data/`，两个构建脚本会竞争同一个 CI pipeline（`pages.yml`），部署时哪个优先？

3. **设计系统分裂**：现有视觉系统（`portal.css`，暖纸感 `--paper #eef3ea`）与 Spec §5.2.1 提出的新视觉系统（`#FBF9F1` 暖白、`#13233A` 深藏青墨、五色功能色）风格接近但不完全相同。两个色系共存会造成视觉割裂。

4. **SEO 和路由混乱**：`site/index.html` 是主页入口，`site/wc2026/index.html` 又是"全景图主页面"。两个 index.html 在 GitHub Pages 上的路由如何处理？用户从主页如何过渡到全景图？

5. **与竞争 Spec 的策略矛盾**：`docs/design/specs/2026-06-12-public-site-ai-market-upgrade-spec.md` 选择了"扩展现有站点"策略，已有详细的 11 Task 实施计划（`docs/design/plans/2026-06-12-public-site-ai-market-upgrade-plan.md`，1453 行含代码片段）。两个 Spec 对同一件事的策略完全相反，必须先决定走哪条路。

**改进方向**：在现有 `site/` 基础上增量扩展。新增 `site/panorama.html` 和 `site/match.html` 两个页面，复用 `portal.css` 和 `common.js`，在 `build_site_data.py` 中增加新的构建函数。零资产浪费。

---

### 维度 2：范围控制 — 2/5

**一句话**：8 个模块 × 7 周执行计划 × 300 Agent 投票 = 上一版 Spec（4 个 task，已完成）的 20 倍 scope，且未考虑现有未解决的 5 个 bug。

**支撑理由**：

1. **量级跳跃**：前一版 homepage optimization plan（`docs/superpowers/plans/2026-06-11-homepage-optimization.md`）是 4 个 task，全部完成。本 Spec 是 8 个模块 × 每个模块 3-8 个子任务 = 约 40 个 task，scope 膨胀 10 倍。没有论证为什么可以在这个时间框架内完成。

2. **前置条件未满足**：现有站点有 5 个未解决的 bug（P0 CSS @media 断裂 `portal.css:1334-1377`、P1 外部参照图不完整、P1 禁用词列表缺项、CI 未跑单元测试、consensus_gap 硬编码）。在新功能之上搭建全景图等于在裂缝上盖楼。

3. **MiMo Campaign 可靠性存疑**：验收报告 `docs/investigations/mimo-campaign-acceptance-2026-06-12.md` 显示 MiMo Campaign 多次声称完成任务但无实际产出文件（phantom file references），campaign 状态不可信。Spec 大量依赖 MiMo Code 驱动 M1-M8，但未评估这个执行载体的可靠性。

4. **Baseline 套件仍为空**：6 个 baseline 定义（`baseline_suite_registry.csv`）全部为 `designed_not_populated`。Spec 的全景图需要 baseline 数据来展示对比，但这个前置条件被跳过了。

5. **7 周时间线的假设**：假设全职投入、无阻塞、无返工。考虑到 MiMo 的可靠性问题、API 调用的成本和限制、以及前序 bug 的修复，实际可能需要 12-16 周。

**改进方向**：将 8 个模块拆为 3-4 个独立阶段，每阶段有独立的验收门和回滚点。先修复 bug、完成 baseline 填充、验证 MiMo 可靠性，再启动新模块。

---

### 维度 3：数据管线可行性 — 3/5

**一句话**：M1 和 M5 已有基础（Wikipedia 转储 + Polymarket 脚本），M2-M4 需要新基础设施但可行，M6-M8 的可行性取决于执行载体（MiMo vs Python batch）的选择。

**支撑理由**：

1. **M1 赛程（已部分存在）**：Wikipedia MiMo 输出（`wiki-wc2026-main.json` 233KB、`wiki-wc2026-draw.json` 22KB）已包含赛程数据，只是未接入 `build_site_data.py`。预计 2-3 天可完成管线集成。

2. **M5 Polymarket（已实现）**：`fetch_market_snapshot.py`（187 行）已工作，但缺少定时刷新。`pages.yml` 无 `schedule` 触发器。添加 `cron` 到 GitHub Actions 是 1 天的工作量。

3. **M4 数值预测（需新建但可行）**：Elo 预期得分 + 泊松分布是标准方法，Python 标准库即可实现，无需外部依赖。MiMo 在此的角色是"编写/调参脚本"而非"直接预测"——这个设计是合理的。

4. **M7 Agent 投票（架构需重设计）**：§17.1 正确指出 MiMo Code 不能 spawn 子进程。但 Spec 正文未修正——§6.2 和 §7.7 仍按 MiMo Code 直接执行 300 runs 的假设编写。Python batch 脚本是正确方向，但意味着需要 LLM API 密钥管理、重试逻辑、token 预算追踪——这些 Spec 都未涉及。

5. **M8 日报（技能集成未定义）**：Spec 提到 `data-analysis`、`chart-visualization`、`consulting-analysis` 三个技能套装，但 §17.5 指出这些是交互式 Agent 技能，不能由 MiMo Code 内部调用。需要独立 Agent 会话，具体的编排机制未定义。

**改进方向**：优先完成 M1/M5 的管线集成（利用已有数据），然后 M4（纯 Python），最后 M6-M8（依赖 MiMo 或 API 调用的可靠性）。

---

### 维度 4：前端设计完整性 — 2/5

**一句话**：Spec 同时声明"零依赖 HTML/CSS/JS"（§1.3）和"使用 D3.js 预渲染 SVG、plotly HTML 片段、matplotlib PNG"（§7.8.3），自相矛盾。

**支撑理由**：

1. **零依赖 vs D3/Plotly 矛盾**：§1.3 明确声明"不引入 Astro/Next/React 等前端框架；v1 保持零依赖 HTML/CSS/JS"。但 §7.8.3 提到"使用零依赖 JS 在构建期生成（如 D3.js 预渲染为 SVG），或在 Python 中使用 matplotlib/plotly 生成 PNG"。D3.js 和 plotly 都是外部依赖，即使在构建期使用也违反零依赖约束。

2. **现有设计系统被忽略**：`portal.css` 已有成熟的设计系统（CSS 变量、组件类、响应式断点），但 Spec §5.2.1 定义了新的视觉规范（不同的颜色值、不同的功能色体系），没有解释与现有系统的关系。

3. **移动端信息架构不完整**：§17.4 补充了移动端优先级和交互模式，但 Spec 正文没有相应的实现细节。12 组 × 3 轮矩阵在移动端如何展示？Bottom Sheet 的具体交互规格是什么？

4. **图表技术选型悬而未决**：§17.5 提出混合方案（CSS 条形图 + D3 SVG + plotly HTML + matplotlib PNG），但没有评估每种技术在零依赖约束下的可行性。纯 CSS/SVG 可以实现所有需要的图表类型。

5. **响应式策略未定义**：现有 `portal.css` 有两个断点（900px 和 640px），但 Spec 的全景图需要三个层级（桌面矩阵 → 平板小组视图 → 移动端日期聚合），断点策略需要重新设计。

**改进方向**：坚持零依赖约束。所有图表用纯 CSS（条形图）+ 原生 JS 生成 SVG（热力图、时间线、雷达图）。matplotlib 可在构建期预生成 PNG 作为静态图片嵌入，但不算前端依赖。

---

### 维度 5：与现有代码的兼容性 — 2/5

**一句话**：Spec 几乎没有讨论与现有代码的兼容性。新目录结构（`src/pipeline/`、`src/agents/`、`site/wc2026/`、`wiki/teams/`）与现有目录结构（`scripts/`、`artifacts/team-cards/`、`site/`、`wiki/concepts/`）完全不同。

**支撑理由**：

1. **构建脚本的断裂**：现有 `scripts/build_site_data.py` 是 1324 行的单体脚本。Spec 提出新的 `src/publish/build_site_data.py`，但未说明如何与现有脚本共存或迁移。两个脚本同时存在会造成混乱。

2. **Wiki 结构不兼容**：现有 wiki 是 `wiki/concepts/`、`wiki/decisions/`、`wiki/annotations/`——这是 Marginalia 协议定义的结构。Spec 提出的 `wiki/teams/`、`wiki/players/`、`wiki/matches/` 打破了现有结构。`scripts/audit.py` 是否需要重写？

3. **Team cards 的位置混乱**：48 队卡片目前存放在 `artifacts/team-cards/*.md`，由 `build_site_data.py` 的 `parse_markdown_card()`（L84）解析。Spec 提出的 `wiki/teams/` 会是这些卡片的副本还是迁移？如果迁移，`build_site_data.py` 的输入路径需要更新。

4. **数据契约的演进**：`homepage.json` 已有 12+ 个顶层键。全景图数据（`panorama.json`、`matches.json`）应该作为新键加入现有 JSON，还是作为独立文件？Spec 选择独立文件（`site/wc2026/data/`），但这样 `homepage.js` 无法直接渲染全景图数据。

5. **CI/CD 的扩展**：`pages.yml` 目前只运行 `build_site_data.py`。如果新增 `src/pipeline/daily_orchestrator.py` 和 `fetch_market_snapshot.py` 的定时运行，需要新的 workflow 文件或扩展现有 workflow。

**改进方向**：所有新代码沿用现有目录约定。`scripts/` 下新增脚本（不是 `src/pipeline/`），`site/` 下新增页面（不是 `site/wc2026/`），`build_site_data.py` 扩展新函数（不是新脚本）。

---

### 综合评分

| 维度 | 分数 | 核心问题 |
|------|------|---------|
| 架构合理性 | 2/5 | 新站点 vs 扩展现有站点，策略矛盾 |
| 范围控制 | 2/5 | scope 膨胀 10-20 倍，前置条件未满足 |
| 数据管线可行性 | 3/5 | M1/M5 可直接用，M7 架构需重设计 |
| 前端设计完整性 | 2/5 | 零依赖 vs D3/Plotly 矛盾 |
| 与现有代码兼容性 | 2/5 | 目录结构、数据契约、CI/CD 均未对齐 |
| **加权平均** | **2.2/5** | **核心问题：spec 与现有代码库脱节** |

---

## 第二部分：关键发现清单

### Spec 做对了什么（值得保留的设计）

| # | 发现 | 引用 |
|---|------|------|
| ✅ 1 | **参考项目分析扎实**：policysim（批量运行范式）、cds4polymarket（Arena 辩论）、institute-one（Prompt 三明治、VaultWriter）的分析深入且有具体的转译方案 | §2 全节 |
| ✅ 2 | **来源纪律明确**：三级来源分级表（§11.1）清晰列出每种数据类型的来源等级、能否进入 Factor Ledger、页面展示方式，且标注了禁止行为 | §11.1-11.3 |
| ✅ 3 | **M6 多 Agent 辩论设计合理**：4-6 Agent 角色分工（路径分析师/来源审计员/市场观察员/反方挑战者/历史类比师），2-3 轮辩论协议，keyword aggregation + LLM synthesis 双层聚合 | §7.6 |
| ✅ 4 | **每日数据目录结构完整**：`data/ops/daily-runs/YYYY-MM-DD/` 下的 manifest、各模块输出、聚合结果、质量评估、prompt logs 的组织方式清晰且可审计 | §8.1-8.2 |
| ✅ 5 | **防模板化机制**：Jaccard 相似度检查 + 扰动注入 + 最多 2 次重试，避免 300 Agent 输出趋同 | §6.2.3 |
| ✅ 6 | **§17 DeepSeek 审阅诚实且有价值**：主动指出 M7 架构假设错误、数据量问题、Skills 集成方式、移动端信息架构等关键问题，体现了自省能力 | §17 全节 |
| ✅ 7 | **§17.6 三阶段辩论协议补全**：Blind Round → Cross-Examination → Settlement + 分歧审计员，比正文 §7.6 的设计更完善 | §17.6 |
| ✅ 8 | **非目标声明清晰**：不做实时交易信号、不引入前端框架、不把 AI 概率当事实、不在浏览器端调 API——这些约束对项目至关重要 | §1.3 |

### Spec 遗漏了什么（必须补充的内容）

| # | 遗漏 | 影响 |
|---|------|------|
| ❌ 1 | **无迁移计划**：没有讨论如何从现有 `site/`（3 页面、1397 行 CSS、6 个 JSON 文件）过渡到新架构。是并行运行？逐步替换？数据如何迁移？ | 新旧系统无法共存，可能导致部署期间服务中断 |
| ❌ 2 | **无测试策略**：8 个新模块（`src/pipeline/m1-m8.py`）+ 新前端页面 + 聚合算法，没有任何测试设计。现有 `tests/` 只有 `test_build_site_data.py`（5 个类）和 `test_fetch_market_snapshot.py`（2 个类） | 新模块无法保证质量，回归风险极高 |
| ❌ 3 | **无成本估算**：M7 全量运行需 300 × 72 = 21,600 次 API 调用/天。每次调用约 3-5K tokens 输入 + 0.5-1K tokens 输出。以典型 LLM API 定价估算，每日成本是多少？月度预算呢？ | 可能超出 API 配额或预算，且在成本未知的情况下无法做量级决策 |
| ❌ 4 | **无错误处理和容错策略**：M2 新闻 API 不可用怎么办？M5 Polymarket API 超时？M4 模型输出异常值？M7 批量运行中部分失败？每个模块的降级策略是什么？ | 单点故障可能阻断整个每日管线 |
| ❌ 5 | **无回滚计划**：每日更新如果引入错误数据（如 API 返回异常值被写入 panorama.json），如何回滚到上一版本？Git revert？有 snapshot 机制吗？ | 错误数据一旦发布到 GitHub Pages，需要明确的回退路径 |
| ❌ 6 | **未讨论现有 5 个 bug**：P0 CSS @media 断裂、P1 外部参照图不完整、P1 禁用词缺项、CI 未跑测试、consensus_gap 硬编码——这些是当前站点的地基问题 | 在 bug 之上搭建全景图，风险传导 |
| ❌ 7 | **未协调竞争 Spec**：`public-site-ai-market-upgrade-spec` 已有详细的 11 Task 计划，~90% 完成。本 Spec 提出替代方案但未说明两者的关系 | 两个 spec 同时推进会造成重复工作和冲突 |
| ❌ 8 | **无 Green Source 获取计划**：Source gap map 显示 0 支队有 Green Source。Spec 的全景图需要 FIFA 官方赛程（Green），但 M1 模块依赖 Wikipedia（Yellow at best） | 来源分级体系的核心层是空的 |
| ❌ 9 | **MiMo Campaign 可靠性未评估**：验收报告显示 MiMo Campaign 有 phantom file references 和状态不可信的问题。Spec 假设 MiMo 可靠驱动 8 个模块，但无可靠性验证 | 可能重复之前的产出缺失问题 |
| ❌ 10 | **Baseline 填充被跳过**：6 个 baseline 全为 `designed_not_populated`。全景图的"外部参照"功能需要 baseline 数据。Spec 直接跳到 M7 300 Agent 投票，但 baseline 对比是更高优先级 | 缺少对比基线，Agent 投票结果无法校准 |

### Spec 中可能有问题的地方

| # | 问题 | 引用 | 建议 |
|---|------|------|------|
| ⚠️ 1 | **`site/wc2026/` 独立站点**：与现有 `site/` 并行，双站点维护，数据管线分裂 | §3.2, §5.1 | 扩展现有 `site/`，新增页面而非新站点 |
| ⚠️ 2 | **零依赖 vs D3/Plotly 矛盾**：§1.3 声明零依赖，§7.8.3 引入 D3.js、plotly、matplotlib | §1.3 vs §7.8.3 | 统一为纯 CSS + 原生 JS SVG 生成，matplotlib 仅构建期使用 |
| ⚠️ 3 | **Wiki 结构重塑可能破坏 Marginalia 协议**：现有 `wiki/` 按 concepts/decisions/annotations 组织，Spec 提出按 teams/players/matches 组织 | §4.1 | 在 `wiki/` 下新增子目录，不重组现有结构 |
| ⚠️ 4 | **M7 正文未吸收 §17 修正**：§7.7 仍按 MiMo Code 直接执行 300 runs 编写，但 §17.1 已指出这不可行 | §7.7 vs §17.1 | 重写 §7.7，明确 Python batch + LLM API 调用模式 |
| ⚠️ 5 | **Prompt 三明治构建器与现有管线的关系**：Spec 提出新的 `src/utils/prompt_builder.py`，但未说明如何与 `build_site_data.py` 中的 `_sanitize_public_text()`（L335）和 `_validate_public_text_boundary()`（L343）协作 | §7.3 (institute-one 转译) | 复用现有清洗/验证逻辑，不新建 |
| ⚠️ 6 | **§17 审阅与正文未合并**：§17 是 DeepSeek 的增量补充，但 Spec 仍然是"正文写 A、审阅说 A 有问题"的状态，没有合成统一版本 | §17 vs §1-16 | 合并为修订版 Spec，消除矛盾 |
| ⚠️ 7 | **每日自动化（§6）的运行载体不明确**：Mac mini 本地 + GitHub Actions runner 的分工是什么？谁负责 M7 的 300 API calls？Mac mini 的可用性如何保证？ | §6.1 | 明确运行载体，添加监控和告警 |

---

## 第三部分：分阶段推荐方案

### 总体原则

1. **先修后建**：先修复现有 bug，再搭建新功能
2. **增量扩展**：扩展现有 `site/` 和 `scripts/`，不新建平行站点
3. **先数据后展示**：先完成数据管线，再做前端展示
4. **验证驱动**：每个阶段结束前验证 MiMo/API 的可靠性
5. **吸收竞争 Spec**：与 `public-site-ai-market-upgrade-spec` 合并执行

---

### Phase A：修补地基（1-2 周）

**目标**：修复所有已知 bug，完成 AI+Market 升级的剩余 10%，验证 MiMo Campaign 可靠性。

> **Design critique 反馈吸收**：Phase A 从原来的 7 个细粒度 task 简化为 3 个工作项。具体 bug 的行号和修复方案由实施 agent 根据 `docs/investigations/` 下的报告自行确定，不需要在计划中预写。

| 工作项 | 范围 | 验收标准 |
|--------|------|----------|
| **A-Fix**: 修复 P0/P1 bug | P0 CSS `@media` 包装、P1 外部参照图、P1 禁用词列表、CI 单元测试集成、`public_consensus_gap` 计算 | 全部 5 个 bug 的调查报告标记为 resolved；`python3 -m unittest` 通过；CI 自动跑测试 |
| **A-Upgrade**: 完成 competing spec | 按 `public-site-ai-market-upgrade-plan.md` 的 Task 1-11 完成 AI+市场升级 | 13/13 验收标准通过；确认此升级是否修改了 `build_site_data.py` 的数据契约或 `portal.css` 的变量命名空间 |
| **A-Spike**: MiMo 可靠性探索 | 设计 campaign 健康检查机制，连续 3 次运行验证 | 产出结论文档：MiMo 可靠（后续 C4-C6 可考虑 MiMo 参与）或不可靠（C4-C6 必须纯 Python batch） |

**⚠️ 关键决策门**：A-Spike 的结论决定 Phase C 的架构。如果 MiMo 不可靠，C4-C6 变为纯 Python batch + LLM API，这是不同的工程量级。

**⚠️ 契约锁定**：A-Upgrade 完成后，记录 `build_site_data.py` 的最终数据契约和 `portal.css` 的最终变量命名空间，作为 Phase B 的输入约束。

**依赖**：无
**风险**：A7 可能发现 MiMo Campaign 根本性问题，需要调整后续 Phase 对 MiMo 的依赖

---

### Phase B：数据层建设（3-4 周）

**目标**：建立 M1-M5 的数据管线，填充 baseline 套件，实现定时市场刷新。

> **Design critique 反馈吸收**：B8（Wiki 赛程页面）需要在实施前解决 Marginalia 协议兼容性问题（`audit.py` 可能标记新页面为违规）。建议先在 `wiki/` 下新增 `matches/` 子目录并更新 `audit.py` 的白名单。

| 任务 | 交付物 | 验收标准 |
|------|--------|----------|
| B1 赛程管线（M1） | `scripts/fetch_schedule.py`，接入已有 Wikipedia 数据 | 72 场小组赛 + 淘汰赛结构化 JSON |
| B2 定时市场刷新（M5 增强） | `pages.yml` 添加 `schedule` 触发器 | 每日自动运行 `fetch_market_snapshot.py` |
| B3 数值预测基线（M4） | `scripts/numeric_odds.py`（Elo + 泊松） | 48 队 × 72 场的胜/平/负概率 JSON |
| B4 新闻抓取（M2） | `scripts/fetch_news.py`（NewsAPI + RSS） | 每队每日 3-5 条摘要，Yellow Source 标注 |
| B5 球员状态（M3） | `scripts/fetch_player_status.py`（Transfermarkt） | 核心球员伤病/红黄牌/出场状态 |
| B6 Baseline 填充 | 填充 6 个 baseline 的实际数据 | `baseline_suite_registry.csv` 至少 3 个 baseline 变为 `populated` |
| B7 扩展 `build_site_data.py` | 新增构建函数产出赛程/概率 JSON | `site/data/matches.json` 和 `site/data/odds.json` 生成并通过验证 |
| B8 Wiki 赛程页面 | `wiki/matches/{match-id}.md` 模板和 72 场页面 | 每场比赛有元数据、概率档案（空）、赛后结算（空） |

**依赖**：Phase A 完成
**关键决策点**：B4/B5 的数据源是否需要付费 API？免费 tier 的覆盖度是否足够？

---

### Phase C：分析层建设（4-6 周）

**目标**：实现 Agent 投票（M7）、CDS 辩论（M6）、聚合算法，建立每日管线编排器。

| 任务 | 交付物 | 验收标准 |
|------|--------|---------|
| C1 API 客户端 | `scripts/api_client.py`（统一 LLM 调用） | 支持多模型、重试、token 记录、prompt log |
| C2 Agent 人格配置 | `src/agents/personas/` + `src/agents/factions/` | 10 派别 × 30 Agent 的配置文件 |
| C3 上下文压缩器 | `scripts/context_compressor.py` | 将 M1-M5 数据压缩到 4K tokens 预算内 |
| C4 Agent 投票系统（M7） | `scripts/agent_voting.py` Python batch | L2 量级（当日比赛 ~1,500 runs），输出结构化 JSON |
| C5 防模板化检查 | Jaccard 相似度 + 扰动注入 | 相似度 > 0.7 的输出自动重试 |
| C6 CDS 辩论系统（M6） | `scripts/cds_debate.py` Arena MAMR | 4-6 Agent 辩论 2-3 轮，输出共识+分歧分析 |
| C7 聚合算法 | `scripts/aggregation.py` | 比赛级概率聚合（数值+市场+Agent 加权）+ 球队级路径更新 |
| C8 每日编排器 | `scripts/daily_orchestrator.py` | 串联 B1-B5 + C4-C7，输出 manifest.json |

**依赖**：Phase B 完成
**风险**：C4 的 API 成本需要监控；C6 的辩论质量需要人工评估

> **Design critique 反馈吸收**：
> - C1 的 API 执行环境需要明确：API 密钥来源（GitHub Actions secrets? 本地 env?）、`daily_orchestrator.py` 的运行载体（Mac mini vs GitHub Actions，后者有 2h 超时限制）
> - C4 的 L-level 决策（L2 ~1,500 runs vs L1 21,600 runs）直接影响成本和工程量，需在 Phase A 结束时确定
> - 如果 A-Spike 判定 MiMo 可靠，C4-C6 可简化为 MiMo 驱动 + 人工审核；否则必须纯 Python batch
> - **Spec §2 的参考项目模式值得保留**：policysim 的 `generate_experiments.py` batch 驱动、cds4polymarket 的 `Arena` 多轮辩论、institute-one 的 `VaultWriter` 原子写入和 `previous_steps_block()` 上下文压缩。这些模式可以直接指导 C1-C8 的实现，不应随 Spec 的其他问题一起被丢弃。

---

### Phase D：全景图前端（4-6 周）

**目标**：在现有 `site/` 上扩展全景图页面、比赛详情页、球队详情增强，零依赖实现。

> **Design critique 反馈吸收**：D 可以用 mock 数据先行原型开发，但 D6（构建管线集成）和 D7（导航整合）依赖 C 的聚合产出和 A-Upgrade 的最终站点状态。实际关键路径是 A → B → C → D（D 可并行原型，但不可并行交付）。B→D 的数据契约（JSON schema）需要在 B7 完成时锁定。

| 任务 | 交付物 | 验收标准 |
|------|--------|----------|
| D1 全景图页面 | `site/panorama.html` + `site/js/panorama.js` | 12 组 × 3 轮矩阵 + 概率条 + 因子图标 |
| D2 比赛详情页 | `site/match.html` + `site/js/match.js` | 三条概率时间线 + Agent 派别分布 + 新闻摘要 |
| D3 球队详情增强 | 扩展 `site/team.html` 和 `team-detail.js` | 夺冠概率时间线 + 路径卡动态更新 + 阻力记录 |
| D4 日报页面 | `site/report.html` + `site/js/report.js` | 每日分析报告 HTML 渲染 |
| D5 全景图 CSS | 扩展 `portal.css` 新增全景图组件 | Heat Zone 编码、响应式矩阵、移动端日期聚合 |
| D6 构建管线集成 | 更新 `build_site_data.py` 产出全景图数据 | `panorama.json` + `matches.json` + `daily/*.json` |
| D7 导航整合 | 更新 `index.html` 的导航栏 | 主页 → 全景图 → 球队 → 比赛的完整导航链 |
| D8 端到端验证 | 浏览器自动化测试 | 桌面/平板/移动端全路径可用 |

**依赖**：Phase B 的数据管线 + Phase C 的分析结果（但可以先用 mock 数据开发前端）
**关键决策点**：D1 的矩阵布局是 CSS Grid 还是 SVG？建议 CSS Grid（零依赖、响应式友好）

---

### 阶段总览

```
Phase A（1-2 周）    修补地基 + MiMo 可靠性探索
    ↓ [关键决策门：MiMo 可靠? → 影响 C 架构]
Phase B（3-4 周）    数据管线 M1-M5
    ↓ [数据契约锁定：matches.json / odds.json 的 JSON schema]
Phase C（4-6 周）    分析层 M6-M7 + 编排器
    ↓ [实际关键路径：D 不能跳过 C 交付]
Phase D（4-6 周）    全景图前端（B 后可 mock 原型，C 后交付）
```

**总时长**：12-18 周（考虑返工和阻塞）
**关键里程碑**：
- Phase A 结束：线上站点健康、AI+Market 升级完成、MiMo 可靠性结论
- Phase B 结束：每日数据管线自动运行、baseline 有实际数据、JSON 数据契约锁定
- Phase C 结束：Agent 投票和 CDS 辩论可运行、聚合算法产出概率
- Phase D 结束：全景图上线、GitHub Pages 展示完整

---

## Open Questions

经过分析，以下问题需要在实施前明确：

1. **站点策略选择**：扩展现有 `site/`（推荐）还是新建 `site/wc2026/`（Spec 原方案）？这决定了后续所有前端工作的基础。

2. **竞争 Spec 的处置**：`public-site-ai-market-upgrade-spec` 已有详细计划且 ~90% 完成。是合并到本 Spec 的 Phase A，还是独立完成后再启动本 Spec？

3. **M7 Agent 投票的量级决策**：全量（21,600 runs/日）vs L2（当日比赛 ~1,500 runs）vs L3（100 Agent/场 ~7,200 runs）？量级直接影响 API 成本和运行时长。

4. **MiMo Campaign 的角色边界**：考虑到验收报告中的可靠性问题，MiMo Code 应该负责哪些模块？建议限制在 M1-M5（数据准备）和 M8（报告撰写），M6-M7（辩论+投票）用 Python batch 脚本。

5. **§17/§18 审阅意见的处置**：这些审阅指出了正文的关键问题。是修订正文合并审阅意见，还是保持增量补充形式？建议修订正文。

## References

- `docs/design/specs/2026-06-12-homepage-optimization-spec.md` — 被审 Spec（1286 行）
- `docs/design/specs/2026-06-12-public-site-ai-market-upgrade-spec.md` — 竞争 Spec（~90% 完成）
- `docs/design/plans/2026-06-12-public-site-ai-market-upgrade-plan.md` — AI+市场升级计划（11 Task）
- `docs/superpowers/plans/2026-06-11-homepage-optimization.md` — 初始主页计划（已完成）
- `docs/investigations/code-review-and-site-loading-2026-06-12.md` — 站点加载 bug 调查（escapeHtml 事故）
- `docs/investigations/f1-f6-review-findings-2026-06-12.md` — F1-F6 审查发现
- `docs/investigations/refactoring-validation-2026-06-12.md` — 重构验证（C1 CSS @media bug）
- `docs/investigations/mimo-campaign-acceptance-2026-06-12.md` — MiMo Campaign 验收报告
- `docs/guides/public-site-update-flow.md` — 公开站更新流程
- `docs/source-policy.md` — 来源分级政策
- `results/2026-06-12-public-site-ai-market-upgrade-inspection-report.md` — AI+市场升级检查报告
