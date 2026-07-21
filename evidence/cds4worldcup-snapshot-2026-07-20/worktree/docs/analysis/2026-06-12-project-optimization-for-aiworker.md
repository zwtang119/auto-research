# CDS4WorldCup 项目优化报告（面向 AIworker）

> **Date**: 2026-06-12
> **Audience**: 接手优化工作的 AIworker / 编程代理
> **Status**: 执行指导
> **Scope**: 公共站点、构建流水线、重构 spec、MiMo 运营约束

## 1. 操作边界

CDS4WorldCup 是面向 2026 FIFA 世界杯的路径空间与可校准知识实验项目。它不是博彩系统，也不是单一答案的预测产品。

在执行任何工作之前，请先阅读：

1. `CLAUDE.md`
2. `AGENTS.md`
3. `wiki/index.md`
4. `docs/source-policy.md`
5. 当前正在执行的 spec 或报告

硬性规则：

- `docs/design/specs/**` 为只读参考，不得修改现有 spec。
- `docs/references/**` 为敏感内容，不得提交入库。
- 不得修改 `schema/`、`templates/` 或 `example/`。
- 不得输出投注建议、仓位大小、ROI、PnL、Sharpe、Kelly 或 value bet 相关表述。
- 绿色来源可作为事实输入；黄色来源仅作为线索；红色来源仅作为基线、叙事、赛程或候选材料。
- 公共站点内容可以使用"AI 多视角分析"，但不得暴露 Kimi、小米、MiMo 或供应商特定代理品牌。

如在 `docs/ops/mimo-season-campaign.md` 下工作，所有 MiMo 输出在人工审核前均为候选/红色来源。正式文件在未经明确 `APPROVE_FORMAL_MUTATION` 授权前不得修改。

## 2. 当前优化判断

以下两份文档应配合阅读：

- `docs/design/specs/2026-06-12-refactoring-fixes-spec.md`
- `results/2026-06-12-public-site-ai-market-upgrade-inspection-report.md`

重构 spec 可执行，但不能盲目全量运行。需要小幅执行修正：

- 执行 P0/P1 缺陷修复。
- 补充前端报告中缺失的 AI vs 市场图表修复。
- 将 `card-chrome` 视为较高风险的前端重构，而非安全清理。
- 修复重复的禁用词验证器，而非仅修复重复的测试常量。

公共站点检查报告的主要发现是准确的，但不应直接用作独立的构建指令，因为它与重构 spec 存在重叠。

## 3. 已验证问题清单

### P0：阻塞级

| ID | 问题 | Files | 必需操作 |
|---|---|---|---|
| C1 | CSS 媒体查询断裂：响应式网格规则逃逸出 `@media (max-width: 900px)`，导致桌面布局强制变为单列 | `site/css/portal.css` | 将裸露的响应式规则移回 900px 媒体查询内部，并删除孤立的闭合花括号 |

### P1：本轮执行

| ID | 问题 | Files | 必需操作 |
|---|---|---|---|
| C2 | `sourceClass()` 可能返回 `source-mixed`，但 CSS 中未定义 `.source-mixed` | `site/css/portal.css` | 添加 `.source-mixed` 样式 |
| H1/H2 | `teams.html` 无共享顶栏，且 `teams.js` 的加载方式与其他页面不同 | `site/teams.html` | 添加共享顶栏；将 `teams.js` 移至 head 并使用 `defer` 加载 |
| FE-1 | 外部参考图表标题显示 AI vs 市场，但实现中仅渲染了市场数据 | `site/js/homepage.js`, `site/css/portal.css` | 并排渲染公开模型群体预测和市场快照 |
| FE-2 | 禁用词验证存在但在严格验证器中重复且不一致 | `scripts/build_site_data.py`, `tests/test_build_site_data.py` | 在构建脚本和测试中使用单一共享的禁用词来源 |

### P2：P0/P1 完成后执行

| ID | 问题 | Files | 建议 |
|---|---|---|---|
| Python 重复代码 | Kimi 分组、信号计算、CSV 加载和 slug 逻辑存在重复 | `scripts/generate_path_cards.py`, `scripts/patch_section9.py`, `scripts/audit_path_cards.py` | P0/P1 落地后提取 `src/utils/` 辅助函数 |
| 前端重复代码 | `escapeHtml`、`escapeAttr` 和 `sourceClass` 存在重复 | `site/js/*.js`, `site/*.html` | 提取 `site/js/common.js`；仔细验证脚本加载顺序 |
| Makefile 缺陷 | `make results` 仅复制 `site/` 而未重建数据 | `Makefile` | 在发布前添加 `python3 scripts/build_site_data.py` |

### P3：延后或拆分

| 事项 | 原因 |
|---|---|
| `card-chrome` 提取 | 涉及 CSS、静态 HTML 和动态生成的 JS 卡片。不是纯粹的安全清理。应移至前端重构 PR 或延后。 |
| 拆分 `scripts/build_site_data.py` | 影响面大。需要专门的 spec 和回归测试。 |
| 移除 `.json` + `.js` 双重数据输出 | 双重输出支持 `file://` 回退方案。保留。 |
| 修复 `patch_section9.py` `kimi_prob` 近似计算 | 已记录为有意的折衷方案。需要架构变更。 |
| 键盘激活和减少动效优化 | 有效的 UX 改进，但非本次修复的阻塞项。 |

## 4. 推荐执行计划

### PR-1：公共站点缺陷修复

范围：

- `site/css/portal.css`
- `site/teams.html`
- `site/js/homepage.js`

任务：

1. 修复 `portal.css` 中逃逸的媒体查询规则。
2. 添加 `.source-mixed`。
3. 在 `teams.html` 中添加顶栏，并以 `defer` 方式加载 `teams.js`。
4. 重写 `renderExternalReferenceChart()` 使其真正比较 AI 公开模型群体预测与市场快照。

此 PR 不包含 `card-chrome`。

执行提示：

```text
Execute the public-site bug-fix pass.

Read first:
- CLAUDE.md
- AGENTS.md
- docs/source-policy.md
- docs/design/specs/2026-06-12-refactoring-fixes-spec.md
- results/2026-06-12-public-site-ai-market-upgrade-inspection-report.md

Apply only these changes:
1. In site/css/portal.css, move the bare responsive grid rules currently around L1352-L1378 back inside @media (max-width: 900px), before that media block closes. Delete the orphan closing brace left behind. Do not change the two max-width: 640px blocks.
2. Add .source-mixed after the source badge styles:
   background: #ede8dd;
   color: var(--muted);
3. In site/teams.html, add the same topbar pattern used by index.html/team.html. Move js/teams.js into head with defer, preserving data/teams-data.js before it.
4. In site/js/homepage.js, rewrite renderExternalReferenceChart() to render both:
   - snapshots.public_model_crowd.top_teams
   - snapshots.market_public_baseline.teams
   The chart must show side-by-side AI crowd and market values for Top 8 teams. If either value is missing, show "待更新" or "暂无" for that side. Keep all public-source boundary copy and do not introduce vendor or betting terms.

After edits, run:
python3 scripts/build_site_data.py
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py

Then start:
python3 -m http.server 8000 --directory site

Browser-check index.html, teams.html, and team.html?team=argentina at desktop, <900px, and mobile widths.
```

验收标准：

- 桌面端首页英雄区恢复为两列。
- 900px 以下布局变为单列。
- 640px 以下顶栏整洁堆叠。
- `teams.html` 顶栏与站点其余页面一致。
- 外部参考图表显示两个参考渠道，而非仅有市场。
- 浏览器控制台无 JavaScript 错误。
- 禁用词扫描保持清洁。

### PR-2：构建边界与低风险清理

范围：

- `scripts/build_site_data.py`
- `tests/test_build_site_data.py`
- `Makefile`
- 可选的简单无用 import / `meta.json` 清理

任务：

1. 移除未使用的 import。
2. 仅在确认无 HTML/JS 引用 `meta.json` 后才删除孤立的 `meta.json`。
3. 在严格验证器中用模块级常量或 `_validate_public_text_boundary()` 替换重复的禁用词列表。
4. 更新 `tests/test_build_site_data.py` 使测试与构建代码共享相同的禁用词。
5. 使 `make results` 在复制 `site/` 之前重新构建站点数据。

执行提示：

```text
Execute the build-boundary cleanup pass.

Keep behavior stable. Do not refactor build_site_data.py beyond the requested boundary fix.

Required changes:
1. Remove unused import os from scripts/build_site_data.py and scripts/generate_path_cards.py.
2. Remove site/data/meta.json generation only if rg confirms no site HTML/JS references meta.json.
3. In scripts/build_site_data.py, make _validate_homepage_json() and _validate_team_details_json() use PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN, or call _validate_public_text_boundary(). Do not leave smaller local forbidden lists.
4. In tests/test_build_site_data.py, import the forbidden constants from the loaded build_site_data module instead of maintaining duplicate lists.
5. In Makefile results target, run python3 scripts/build_site_data.py before copying site/ to _publish/.

Run:
python3 scripts/build_site_data.py
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
make check

Check:
rg 'Kimi|kimi|小米|Xiaomi|MiMo|MiMo Code|投注建议|ROI|PnL|Sharpe|Kelly|仓位|低估|高估|正期望|value bet' site/
```

验收标准：

- 测试通过。
- 公共禁用词扫描无非预期命中的公共内容。
- `make results` 后 `_publish/data/*.json` 为最新状态。
- 构建输出变更已理解且符合预期。

### PR-3：行为稳定后再重构

范围：

- 新建 `src/utils/`
- 新建 `site/js/common.js`
- 脚本和页面 import

任务：

1. 提取 Python 辅助函数：
   - `src/utils/slug.py`
   - `src/utils/csv_helpers.py`
   - `src/utils/kimi.py`
2. 保持 `scripts/fetch_market_snapshot.py` 的 slug 逻辑独立，因为它解析的是市场问题文本而非标准队名。
3. 将前端辅助函数提取到 `site/js/common.js`。
4. 将 `common.js` 放在数据脚本之后、页面脚本之前。

重要细节：

- `teams.js` 仅包含 `escapeHtml()` 和 `escapeAttr()`，不包含 `sourceClass()`。
- 如果 `common.js` 未在延迟页面脚本执行前加载，页面将因缺少辅助函数而报错。

推荐验证：

```bash
python3 scripts/build_site_data.py
python3 scripts/generate_path_cards.py
python3 -m unittest
make check
git diff site/data/*.json
```

验收标准：

- 生成的站点数据不变，除非 PR 有意更改数据。
- 三个公共页面渲染无控制台错误。
- 球队搜索/筛选功能正常。
- 来源徽章样式正确。

## 5. 浏览器验证清单

运行：

```bash
python3 -m http.server 8000 --directory site
```

检查：

| 页面 | URL | 必需检查项 |
|---|---|---|
| 首页 | `http://localhost:8000/` | 桌面端英雄区两列；AI 多视角可见；外部参考图表包含 AI 和市场渠道；无控制台错误 |
| 球队列表 | `http://localhost:8000/teams.html` | 顶栏存在；筛选功能正常；卡片链接到详情页；移动端布局无溢出 |
| 球队详情 | `http://localhost:8000/team.html?team=argentina` | 头部导航正常；来源标签样式正确；图表渲染正常；无控制台错误 |

视口检查：

- 桌面端：宽度 >= 1200px
- 平板：宽度约 900px
- 移动端：390px x 844px

## 6. 自动化验证清单

最终交接前运行：

```bash
python3 scripts/build_site_data.py
python3 -m unittest tests/test_build_site_data.py tests/test_fetch_market_snapshot.py
python3 -m unittest
make check
python3 scripts/audit.py --root wiki/
```

运行禁用词扫描：

```bash
rg 'Kimi|kimi|小米|Xiaomi|MiMo|MiMo Code|投注建议|ROI|PnL|Sharpe|Kelly|仓位|低估|高估|正期望|value bet' site/
```

审查 git 状态：

```bash
git status --short
git diff --stat
```

不得暂存或提交：

- `docs/references/**`
- `.playwright-mcp/**`
- 意外的本地代理文件
- 工作开始前已存在的无关脏文件

## 7. 本次扫描后的已知缺口

以下内容应成为独立的 spec 或后续任务：

- 为 `scripts/` 下更多脚本编写专用测试。
- 更大规模地拆分 `scripts/build_site_data.py`。
- 更完善的可点击球队卡片无障碍优化。
- 悬停过渡的减少动效覆盖。
- 正式的 MiMo 文件工厂工具：prompt 构建器、任务队列状态机、安全写入器。

## 8. 简要决策摘要

推荐的即时路径：

1. 先做 PR-1。它修复实际用户可见的故障。
2. 再做 PR-2。它加强公共边界检查和构建可复现性。
3. 站点视觉稳定后再做 PR-3。
4. 将 `card-chrome` 延后至前端重构工作，因为它不是安全的死代码清理。
