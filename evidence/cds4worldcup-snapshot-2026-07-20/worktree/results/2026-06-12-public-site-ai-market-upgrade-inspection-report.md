# CDS4WorldCup 公开站点 AI + Market 升级前端检查报告

> **检查日期**：2026-06-12
> **检查范围**：`site/`（HTML/CSS/JS/JSON）、`scripts/`（构建脚本）、`tests/`（测试）、`docs/guides/`（维护者文档）
> **依据文档**：
> - `docs/design/specs/2026-06-12-public-site-ai-market-upgrade-spec.md`
> - `docs/design/plans/2026-06-12-public-site-ai-market-upgrade-plan.md`
> **检查方法**：静态代码审查 + 自动化测试执行 + 禁词扫描 + 数据 schema 校验 + 响应式断点检查

---

## 一、执行摘要

本次检查针对 CDS4WorldCup GitHub Pages 公开站点的前端实现进行系统性审查，对照升级 spec 与 plan 中的 15 项任务和 13 条验收标准逐一核验。

**总体结论**：升级实现度约为 **90%**。核心功能（AI 多视角模块、市场快照、开发者内容移除、禁词过滤、测试覆盖）均已到位，但存在 **1 个 P0 级 CSS 结构错误** 和 **2 个 P1 级功能/验证缺陷**，需在部署前修复。

| 维度 | 状态 | 说明 |
|---|---|---|
| 界面布局与设计规范一致性 | 部分达标 | P0 CSS 错误导致桌面端布局被强制单列 |
| 用户交互流程合理性与流畅性 | 达标 | 球队卡片点击→单队详情流程正确 |
| 响应式设计在不同设备上的表现 | 部分达标 | 断点存在，但 P0 错误破坏了桌面端布局 |
| 视觉元素统一性与美观度 | 达标 | 莫兰迪色系、点阵动画、纸感背景已落实 |
| 性能优化与加载速度 | 达标 | 零依赖、纯静态、内置兜底 JS 数据 |
| 可访问性与用户体验 | 部分达标 | 缺少部分键盘可访问性支持 |
| 功能实现与需求文档匹配度 | 部分达标 | 外部参考图表标题与内容不符 |
| 测试与自动化验证 | 达标 | 7/7 测试通过，禁词扫描通过 |

---

## 二、问题清单

### P0 — 严重（阻塞部署）

#### P0-1：`portal.css` 存在未包裹 `@media` 的规则块，桌面端布局被强制破坏

- **位置**：`site/css/portal.css`，line 1334–1377，位于第一个与第二个 `@media (max-width: 640px)` 块之间
- **问题描述**：
  在第一个 `@media (max-width: 640px) { ... }`（line 1320–1332）结束后，出现了一大段缩进但**未被任何 `@media` 查询包裹**的 CSS 规则，末尾还跟着一个孤立的 `}`：
  ```css
    .hero,
    .control-panel,
    .insight-band,
    .update-layout,
    .team-detail-hero,
    .detail-grid,
    .chart-grid,
    .table-grid {
      grid-template-columns: 1fr;
    }

    .panel-grid,
    .team-grid,
    .team-teaser-grid,
    .snapshot-grid,
    .outside-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .status-item {
      grid-template-columns: 1fr;
    }

    .signal-strip,
    .source-grid,
    .update-steps {
      grid-template-columns: 1fr;
    }
  }
  ```
  这些规则在**所有屏幕尺寸下全局生效**。由于选择器权重与原始规则相同，它们会覆盖桌面端（>640px）应有的多列布局：
  - `.hero`、`.detail-grid`、`.chart-grid`、`.table-grid` 被强制为单列；
  - `.team-grid`、`.team-teaser-grid`、`.snapshot-grid`、`.outside-grid` 被强制为 2 列（原设计为 3–4 列）。
- **根因推测**：该段代码原本应属于 `@media (max-width: 900px)` 内部，但在添加 AI 相关样式时被意外移出了媒体查询块。孤立的 `}` 是编辑残留。
- **影响范围**：所有访问 `site/` 下任意页面的桌面端用户。

---

### P1 — 中等（建议修复）

#### P1-1：首页外部参考 Top 8 图表标题与内容不符

- **位置**：`site/js/homepage.js`，`renderExternalReferenceChart` 函数
- **问题描述**：
  图表标题渲染为 `"AI 模型群体 vs 市场参考"`，但实际函数逻辑只读取并渲染了 `market_public_baseline.teams`（市场快照数据），完全没有展示 `public_model_crowd`（公开模型群体/AI 多视角）的概率数据。
  Spec 第 6.1 条明确要求该图表应"Compare: public model crowd probability, market snapshot probability if available"，即两者并列对比。
- **当前行为**：仅展示市场 Top 8 概率条。
- **期望行为**：展示 `public_model_crowd` 与 `market_public_baseline` 的 Top 8 对比条；当任一方缺失时，对应行显示"待更新"或"暂无"。
- **严重程度**：中。标题误导用户，且未满足 spec 功能要求。

#### P1-2：构建脚本中的禁词校验列表不完整

- **位置**：`scripts/build_site_data.py`，`_validate_homepage_json` 与 `_validate_team_details_json`
- **问题描述**：
  两个验证函数中的 `forbidden` 列表缺少 spec/plan 中明确禁止的以下词汇：
  - `小米`、`Xiaomi`
  - `MiMo`、`MiMo Code Long-Horizon`
  - `投注建议`
  - `value bet`
- **当前状态**：当前数据确实不含这些词汇（已通过外部 `rg` 扫描验证），因此测试和构建均通过。但防御性校验不完整，未来数据更新时存在泄露风险。
- **修复建议**：将 `PUBLIC_VENDOR_FORBIDDEN` 和 `PUBLIC_BETTING_FORBIDDEN` 常量（已在 `tests/test_build_site_data.py` 中定义）提取到共享模块，供构建脚本和测试共同引用。

---

### P2 — 低（优化项）

#### P2-1：`teams.html` 球队卡片点击缺乏键盘可访问性

- **位置**：`site/js/teams.js`
- **问题描述**：整个卡片区域通过 `click` 事件监听跳转，但未处理 `keydown`（Enter/Space），键盘用户无法聚焦并激活卡片。
- **建议**：为 `team-card` 添加 `tabindex="0"` 和 `role="link"`，并监听 `keydown` 事件触发跳转；或直接将卡片整体改为 `<a>` 标签包裹。

#### P2-2：部分 hover 过渡未适配 `prefers-reduced-motion`

- **位置**：`site/css/portal.css`
- **问题描述**：`.team-teaser-card:hover`、`.team-card:hover`、`.faction-card:hover` 均有 `transition` 和 `transform`，但未在 `@media (prefers-reduced-motion: reduce)` 中重置。虽然点阵动画已适配，但卡片位移过渡未覆盖。
- **建议**：在 `prefers-reduced-motion` 媒体查询中统一禁用所有过渡和变换。

#### P2-3：少数 AI 视角片段含英文词汇

- **位置**：`site/data/team-details.json` → `argentina.ai_perspective.snippets`
- **问题描述**：部分 `reason` 字段含英文单词（如 `"invaluable"`、`"ACL"`）。虽非严格违规，但 spec 1.1 要求"plain Chinese that football fans understand"。
- **建议**：在 `_sanitize_public_text` 或 `_short_public_text` 中增加一层纯中文字段校验，或在数据预处理阶段统一替换为中文表达。

---

## 三、改进建议

| 编号 | 对应问题 | 改进方案 | 技术路径 | 预期效果 |
|---|---|---|---|---|
| **R0** | P0-1 | 将裸露的 CSS 规则块正确包裹进 `@media (max-width: 900px)` | 在 `portal.css` 第 1430 行前添加 `@media (max-width: 900px) {`，末尾补 `}` | 桌面端恢复双列/多列布局，移动端保持单列 |
| **R1** | P1-1 | 重写 `renderExternalReferenceChart`，同时渲染两组数据 | 从 `data.public_signal_snapshots.public_model_crowd.top_teams` 提取 Top 8，与 `market_public_baseline.teams` 对比展示；使用双色条区分来源 | 图表标题与内容一致，满足 spec 6.1 对比要求 |
| **R2** | P1-2 | 统一禁词常量 | 将 `PUBLIC_VENDOR_FORBIDDEN` / `PUBLIC_BETTING_FORBIDDEN` 提取到 `scripts/public_boundary.py`，由 `build_site_data.py` 和测试共同 import | 防御性校验完整，未来数据更新不会泄露禁词 |
| **R3** | P2-1 | 增强键盘可访问性 | 在 `teams.js` 的 `renderTeamCard` 中为卡片加 `tabindex="0"`，并增加 `keydown` 监听；或在 CSS 中将 `a` 标签扩大为整块链接 | 支持键盘导航和屏幕阅读器 |
| **R4** | P2-2 | 补全 `prefers-reduced-motion` | 在现有 `@media (prefers-reduced-motion: reduce)` 中追加 `.team-teaser-card, .team-card, .faction-card { transition: none; transform: none; }` | 尊重用户系统级动画偏好 |
| **R5** | P2-3 | 增加英文词汇预警 | 在 `_short_public_text` 中增加对常见英文单词的日志警告（非阻塞） | 提醒维护者将 reason 文本本地化为中文 |

---

## 四、优先级划分

| 优先级 | 建议编号 | 严重程度 | 影响范围 | 实施难度 | 备注 |
|---|---|---|---|---|---|
| **立即执行** | R0 | P0 | 全站桌面端用户 | 极低（1 行 CSS） | **阻塞部署** |
| **本轮执行** | R1 | P1 | 首页外部参考区 | 中（~30 行 JS） | 功能与 spec 不符 |
| **本轮执行** | R2 | P1 | 构建校验逻辑 | 低（重构常量） | 防御性加固 |
| **后续迭代** | R3 | P2 | `teams.html` 键盘用户 | 低 | 无障碍优化 |
| **后续迭代** | R4 | P2 | 动画敏感用户 | 极低 | 体验优化 |
| **后续迭代** | R5 | P2 | 文案本地化 | 低 | 质量提升 |

---

## 五、已达标项确认

以下 spec/plan 要求项经验证**已完整实现**，无需修改：

1. **球队点击进入单队详情**：`team.html?team=<slug>` 链接正确，详情页仅展示单队。
2. **详情页移除开发者说明**：`update_contract` 已从 `site/data/team-details.json` 和 `site/team.html` 中移除，无"后续更新"、"每场比赛后"等文案。
3. **首页 AI 多视角模块可见**：`#ai-perspectives` 模块包含 300 视角统计、10 派别卡片、莫兰迪点阵。
4. **无厂商品牌泄露**：`rg` 扫描确认 `site/` 下无 `Kimi`、`小米`、`Xiaomi`、`MiMo`、`MiMo Code Long-Horizon`。
5. **无投注/投资语言**：`rg` 扫描确认无 `投注建议`、`ROI`、`PnL`、`Sharpe`、`Kelly`、`仓位`、`低估`、`高估`、`正期望`、`value bet`。
6. **市场快照脚本可用**：`scripts/fetch_market_snapshot.py` 功能完整，可通过 CLI 生成 `data/processed/market_public_snapshot.json`。
7. **市场快照失败不阻塞构建**：`build_site_data.py` 中 `_build_market_snapshot` 已处理缺失情况，显示"市场快照待更新"。
8. **测试覆盖**：`tests/test_build_site_data.py`（5 项）+ `tests/test_fetch_market_snapshot.py`（2 项）= **7/7 通过**。
9. **维护者文档已分离**：`docs/guides/public-site-update-flow.md` 存在，且未被 `site/` 引用。
10. **来源分级标签正确**：Green/Yellow/Red 三级标签在首页、详情页、图表区均正确展示。
11. **文案为球迷白话中文**：整体语言符合 spec 1.1 要求，避免学术/英文堆砌。
12. **轻量图表**：全部使用 CSS 条形图，未引入 D3/ECharts/Chart.js。
13. **纯静态站架构保持**：Python 构建期生成 JSON/JS 兜底，浏览器只负责渲染。

---

## 六、结论与下一步行动建议

### 结论

CDS4WorldCup 公开站点的 AI + Market 升级整体质量较高，核心功能与品牌边界控制均已到位。**唯一阻塞部署的问题是 `portal.css` 中一处遗漏的 `@media` 包裹**，导致桌面端布局被破坏。修复后，站点即可满足全部 13 条验收标准中的 12 条（剩余 P1-1 图表对比功能建议在同一次提交中补齐）。

### 下一步行动

1. **立即修复 P0-1**：修改 `site/css/portal.css`，将裸露规则块包裹进 `@media (max-width: 900px)`。
2. **本轮补齐 P1-1**：修改 `site/js/homepage.js`，使 `renderExternalReferenceChart` 同时渲染 public model crowd 与市场快照数据。
3. **本轮补齐 P1-2**：重构禁词常量为共享模块，更新构建脚本和测试的引用。
4. **重新构建与验证**：
   ```bash
   python3 scripts/build_site_data.py
   python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
   python3 -m http.server 8000 --directory site
   ```
5. **浏览器验证**：检查 `http://localhost:8000/` 和 `http://localhost:8000/team.html?team=argentina` 在桌面端（>900px）和移动端（390x844）的布局。
6. **提交并部署**：确认无 `AGENTS.md`、`.playwright-mcp/`、`docs/references/` 等敏感文件被 stage 后，commit 并 push 到 `main`。

---

*报告生成时间：2026-06-12*
*检查工具：静态代码审查 + unittest + ripgrep + 浏览器布局推演*
