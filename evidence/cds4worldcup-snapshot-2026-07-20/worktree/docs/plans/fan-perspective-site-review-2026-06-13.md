# 球迷视角站点体检报告: Plan

## Goal

从球迷角度（普通球迷 + 数据型球迷）全面评估 CDS4WorldCup 公站的 5 个页面，先走查体验再检查规格合规，产出一份以理解为主的"体检报告"。

## Background

### 站点全貌

5 个公开页面，纯静态 HTML/CSS/JS，数据预构建为 JSON：

| 页面 | 文件 | 核心内容 |
|------|------|----------|
| 首页 | `site/index.html` + `homepage.js` | Hero + 7 个内容区块（选球队、AI 多视角、进度、难点、外界看法、方法来源、更新记录） |
| 球队列表 | `site/teams.html` + `teams.js` | 48 队卡片，搜索/联合会/深度筛选 |
| 球队详情 | `site/team.html` + `team-detail.js` | 11 个区块（论点、分析、AI 视角、图表、障碍、突破、黑天鹅、监控、小组赛、基线、CDS 路径） |
| 比赛详情 | `site/match.html` + `match.js` | VS 布局 + 三源概率对比 + 比赛信息 |
| 全景赛程 | `site/panorama.html` + `panorama.js` | 104 场赛程，3 种视图（小组/淘汰/日期） |

### 已知 Bug 修复状态（Phase 2 探索确认）

| Bug | 状态 | 证据 |
|-----|------|------|
| P0: `escapeHtml()` 损坏 | ✅ 已修复 | `common.js:17-23` 正确实现 |
| P0: `formatDate()` 未定义 | ✅ 已修复 | `common.js:130-142` 共享函数 |
| P1: baselines-data 禁用词 | ⚠️ 仍在（免责声明内） | `baselines-data.js` — "不用于投注建议。不输出仓位/赔率价值/ROI/PnL/Sharpe" |
| P2: CDS 路径英文文案 | ✅ 已修复 | `cds-paths-data.js` — 0 条纯英文场景 |
| P2: `slugToTeamName()` 仅 4 队 | ✅ 已修复 | `common.js:87` `cdsSlugToName()` 覆盖 48 队 |
| Match 页市场数据/Agent 投票占位 | ❌ 仍为占位 | `match.js:212,218` — "接入后可用" |

### 球迷旅程关键发现

**普通球迷 ("看热闹")：**
- ✅ 首屏 10 秒内可理解站点定位——"我们不直接猜谁会夺冠"
- ✅ 夺冠论点用自然中文叙述，可读性强
- ⚠️ Hero 指标板中"可赛后对账"是项目内部术语，球迷看不懂
- ⚠️ 球队详情页"下一场比赛"信息埋在第 8 个区块以下，不够直观

**数据型球迷 ("看门道")：**
- ✅ CDS 路径分析是最深层内容，含可观测指标和失败信号
- ✅ 三信号对比图（Elo/市场/公共模型）对数据球迷有价值
- ❌ **无法比较两支球队**——只能开两个标签页
- ❌ match.html 无球队链接，是导航死胡同

### 移动端 & 无障碍关键发现

- ✅ 5 个断点（1200/900/768/640/540px）响应式级联设计合理
- ✅ 全景图自动为移动端切换日期视图
- ✅ Hero 标题使用 `clamp()` 平滑缩放
- 🔴 **eyebrow/label 对比度不达标**：`#b45309` on `#eef3ea` 约 4.1:1，低于 WCAG AA（需 4.5:1）— 影响全站所有区块标签
- 🟡 触摸目标偏小：`.cds-signal-toggle` 仅 2px padding、`.view-btn` 在 540px 缩小、`.topnav a` 无最小触摸区域
- 🟡 元数据字号过小：`0.62rem`（~10px）source badge、`0.72rem` 日期标签
- 🟡 球队名称在 768px 时因 `text-overflow: ellipsis` 被截断

### 设计规格验收标准摘要

3 份规格定义了大量验收标准（`§11` 验收门、`§10` 10 项门控、`§9.7` 边界约束）。关键合规维度：

1. **语言合规**：全部面向球迷的文案必须是中文，无英文暴露
2. **投注措辞红线**：不含 bet/edge/value/ROI/仓位等词
3. **来源分级**：所有数据元素必须带来源标签（绿/黄/红）
4. **AI 多视角**：首页必须展示"AI 多视角推演"且不含供应商名称
5. **零依赖**：浏览器直接访问，所有数据预构建
6. **响应式**：1024px 桌面 + 375px 手机无水平滚动

## Approach

分四个部分构建体检报告：

1. **Part 1：球迷体验走查** — 5 页面 × 2 视角（普通球迷 + 数据型球迷）× 结构化检查项
2. **Part 2：规格合规检查** — 3 类检查而非 8 维度：(a) grep 自动化检查（语言 + 投注 + 品牌）、(b) 视觉检查（响应式 + 无障碍）、(c) 判断型检查（AI 模块质量、导航缺口）
3. **Part 3：差距清单** — 9 字段记录格式 + 已知差距 10 条（以理解为主，非修复方案）
4. **Part 4：工作项清单** — 12 个检查任务，含执行依赖关系

关键设计决策：
- 已修复的 P0 bug（escapeHtml、formatDate、slugToTeamName、英文场景）不重复验证
- Spec v2 的未实现功能（8 步 pipeline、wiki/facts、投票档案、概率全景图 Module J）标记为"未来可检"而非当前差距（见附录 A）
- Match 页占位功能（市场数据 Phase 1、Agent 投票 Phase 3）标记为已知延期而非缺陷
- baselines-data.js 中的禁用词出现在免责声明（否定用法）中，标记为 P1 数据卫生问题
- 零依赖维度已确认全部通过（纯静态 HTML/CSS/JS），不设专门检查任务
- 10 条已知差距直接继承，不重复验证（见附录 B）

执行依赖图（Items 1/6/7/8/9/11 可并行，Item 10 依赖 Item 8）：

```
Item 1 (首页走查) ──────┐
Item 6 (语言合规) ──────┤
Item 7 (投注红线) ──────┤
Item 8 (品牌隔离) ───┐  ├── Item 12 (汇总)
Item 9  (来源标签) ───┤  │
Item 11 (响应式)  ─────┤  │
Item 2  (球队列表) ────┤  │
Item 3  (球队详情) ────┤  │
Item 4  (比赛详情) ────┤  │
Item 5  (全景赛程) ────┘  │
                          └── Item 10 (AI模块，依赖 Item 8)
```

## Work Items

### Item 1 — 首页球迷体验走查
**Goal:** 验证首页在普通球迷和数据型球迷两个视角下的体验质量
**Done when:** 首屏 10 秒理解度确认 ✅/❌、Hero 指标术语可读性评估、8 张球队小卡点击闭环、AI 多视角区块可理解性
**Check method:** 截图首屏（1440×900 + 390×844）+ 视觉审查 + 点击测试
**Key files:** `site/index.html`, `site/js/homepage.js`, `site/data/homepage-data.js`

### Item 2 — 球队列表页走查
**Goal:** 验证球队列表页的搜索、筛选、卡片导航功能
**Done when:** 搜索框中/英文/slug 均可匹配、联合会筛选正确、深度/简版切换正确、卡片点击闭环、简版卡信息充分
**Check method:** 浏览器交互测试（输入搜索 + 筛选 + 点击）
**Key files:** `site/teams.html`, `site/js/teams.js`, `site/data/teams-data.js`

### Item 3 — 球队详情页走查
**Goal:** 验证最深页面的信息层次、数据深度和导航闭环
**Done when:** 单队详情正确加载、默认降级到阿根廷、面包屑导航闭环、分析区块中文叙述风格、AI 视角模块存在且合规、CDS 路径情景无英文
**Check method:** 浏览器交互测试 + `grep -n` 审查渲染文本
**Key files:** `site/team.html`, `site/js/team-detail.js`, `site/data/team-details-data.js`, `site/data/cds-paths-data.js`

### Item 4 — 比赛详情页走查
**Goal:** 验证比赛页的 VS 布局、概率展示和导航缺口
**Done when:** VS 布局可读、概率条可理解、三源概率并列不合成单一值、返回导航正常、占位功能说明清晰、**无球队链接确认为导航缺口**
**Check method:** 浏览器交互测试 + 视觉审查
**Key files:** `site/match.html`, `site/js/match.js`

### Item 5 — 全景赛程页走查
**Goal:** 验证三视图切换、比赛卡片交互和数据展示
**Done when:** 三视图切换正确、移动端默认日期视图、小组赛矩阵可读、比赛卡片点击闭环、球队名链接到 team.html、淘汰赛签表完整
**Check method:** 浏览器交互测试（含 768px 以下宽度）
**Key files:** `site/panorama.html`, `site/js/panorama.js`, `site/data/schedule-data.js`

### Item 6 — 语言合规检查
**Goal:** 验证全站面向球迷的文案符合中文优先原则
**Done when:** 确认所有面向球迷的文案为中文；baselines-data.js 英文公式标记为已知差距
**Check method:** `grep -n 'textContent\|innerHTML' site/js/*.js` 审查渲染文本 + 视觉抽查 baselines 描述
**Key files:** `site/js/*.js`, `site/data/baselines-data.js`

### Item 7 — 投注措辞红线检查
**Goal:** 验证公开数据不含投注建议语言
**Done when:** 确认公开数据不含投注建议语言；`_sanitize_public_text` 覆盖检查（含缺失的"买/卖"中文替换）
**Check method:** `grep -in '投注\|ROI\|PnL\|Sharpe\|Kelly\|仓位\|赔率价值' site/data/*.js` + 审查 `build_site_data.py:_sanitize_public_text`
**Key files:** `site/data/*.js`, `scripts/build_site_data.py`

### Item 8 — 品牌隔离检查
**Goal:** 验证公开页面和数据不含供应商名称
**Done when:** 确认 site/ 下无 Kimi/小米/MiMo 名称（排除注释中的说明性文字）
**Check method:** `grep -ri 'kimi\|小米\|xiaomi\|mimo' site/`（排除合法英文单词中的 mimo）
**Key files:** `site/` 全目录

### Item 9 — 来源标签覆盖率检查
**Goal:** 验证所有数据区块带来源标签
**Done when:** 确认所有数据区块带来源标签（Green/Yellow/Red + 中文标签名）；特别检查 team.html 的小组赛、基线、CDS 路径区块
**Check method:** 浏览器 JS console 执行 `document.querySelectorAll('.source-badge')` 逐页检查
**Key files:** `site/index.html`, `site/team.html`, `site/match.html`, `site/js/common.js`

### Item 10 — AI 多视角模块深度检查
**Goal:** 验证 AI 模块的内容质量和合规性
**Done when:** 10 张派别卡均有内容且无禁用词；球队详情页 AI 视角模块存在；AI 区块明确标注"只代表外部看法"
**Check method:** 浏览器视觉审查 + `grep` 派别理由中的禁用词
**Key files:** `site/js/homepage.js`, `site/js/team-detail.js`, `site/data/homepage-data.js`
**Dependencies:** Item 8（品牌隔离扫描结果）

### Item 11 — 响应式 & 无障碍检查
**Goal:** 验证桌面和移动端的显示质量和可访问性
**Done when:** 桌面 1024px + 手机 375px 无水平滚动；eyebrow 对比度（#b45309 on #eef3ea ≈ 4.1:1）确认不达标；触摸目标最小尺寸检查；元数据字号检查
**Check method:** Chrome DevTools 响应式模式（1024/768/540/375 宽度）+ 对比度计算
**Key files:** `site/css/portal.css`, `site/*.html`

### Item 12 — 差距汇总与定级
**Goal:** 汇总所有检查结果，产出最终差距清单
**Done when:** 完成差距清单（9 字段格式：编号/维度/页面/Spec 条款/差距描述/严重度/影响范围/是否已知/证据）
**Dependencies:** Items 1–11 全部完成

## Open Questions

- Match 页的两个占位功能（市场数据、Agent 投票）是按计划延后的 Phase 1/3 功能，还是需要加速？
- "可赛后对账"是否应该从 Hero 指标板中移除或改写为球迷可理解的表述？
- 球队比较功能的优先级如何——是核心缺失还是可接受的 v1 范围？

## Appendix A：Spec v2 未来功能验收状态

以下 Spec v2 §9.7 的验收标准因功能未实现，标记为"未来可检"：

| §9.7 # | 验收标准 | 当前状态 | 评测处理 |
|--------|---------|---------|---------|
| 1 | wiki/facts/ 四类页面 schema 模板已建 | ❌ `wiki/facts/` 不存在 | 未来可检 |
| 2 | 8 步 pipeline 端到端跑通 | ❌ 无 `src/pipeline/` | 未来可检 |
| 3 | 投票档案可被报告读取 | ❌ 无 `data/ops/vote_archive/` | 未来可检 |
| 4 | 概率全景图 Module J 响应式正确 | ❌ panorama 是赛程视图非概率全景图 | 未来可检 |
| 8 | 浏览器不解析 wiki/facts/*.md | ✅ 当前架构满足 | 通过 |
| 9 | 报告页显示统计诚实指标 | ❌ 无 results/ 公开报告页 | 未来可检 |
| 10 | 30 天前投票档案已归档 | ❌ 投票系统未实现 | 未来可检 |

## Appendix B：已关闭发现索引（不重复验证）

| 来源 | 编号 | 问题 | 状态 |
|------|------|------|------|
| visual-inspection | #1 | panorama.js formatDate 未定义 | ✅ 已修复 |
| code-review | — | escapeHtml 损坏 | ✅ 已修复 |
| code-review | — | slugToTeamName 仅 4 队 | ✅ 已修复 |
| cross-validation | ISSUE-002 | CDS 路径英文情景 | ✅ 已修复 |

## References

- 设计规格 v1: `docs/design/specs/2026-06-11-homepage-optimization-spec.md`
- 设计规格 v2: `docs/design/specs/2026-06-12-homepage-optimization-spec.md`
- AI/市场升级规格: `docs/design/specs/2026-06-12-public-site-ai-market-upgrade-spec.md`
- 视觉检查报告: `docs/investigations/visual-inspection-deep-2026-06-12.md`
- 代码审查报告: `docs/investigations/code-review-and-site-loading-2026-06-12.md`
- 交叉验证报告: `dogfood-output/cross-validation-report.md`
