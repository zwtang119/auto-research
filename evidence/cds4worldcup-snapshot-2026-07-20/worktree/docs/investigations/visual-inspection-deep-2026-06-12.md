# 深度视觉检查报告 — CDS4WorldCup 站点

## Summary
对 CDS4WorldCup GitHub Pages 站点执行深度视觉检查。两个 AI（初审 + 偏离度审计）共发现 **13 个问题**，其中 1 个 P0 运行时错误、1 个 P1 合规风险、5 个 P2 体验/一致性缺陷、6 个 P3 代码质量问题。初审中关于"首页 Hero 缺少移动端断点"的判断经验证**有误**——该断点存在于 `@media (max-width: 900px)` L1296。

---

## 问题总览

| # | 等级 | 问题 | 文件 | 行号 | 爆炸半径 | 是否需要修复 |
|---|------|------|------|------|----------|------------|
| 1 | **P0** | panorama.js 调用未定义 `formatDate()` | panorama.js | L477 | 全景页所有用户 | ✅ 必须修复 |
| 2 | **P1** | baselines 数据含禁止词汇 | baselines-data.js | L1（market.description） | 线上公开数据 | ✅ 必须修复 |
| 3 | **P2** | 子页面无 `<footer>` 元素 | match/team/teams.html | — | 4 个页面所有用户 | ⚠️ 建议修复 |
| 4 | **P2** | 导航栏链接数不一致 | 全部 HTML | — | 子页面用户 | ⚠️ 建议修复 |
| 5 | **P2** | baselines 数据含学术化英文公式 | baselines-data.js | L1（fifa_ranking/elo.description） | 线上公开数据 | ⚠️ 建议修复 |
| 6 | **P2** | panorama 死 DOM（match-detail 从未显示） | panorama.js | L246-251 | 全景页 104 张卡片 | ⚠️ 建议清理 |
| 7 | **P2** | CSS 重复 `@media (max-width: 640px)` 块 | portal.css | L1319 + L1334 | 维护者 | ⚠️ 建议合并 |
| 8 | **P3** | `expandedMatchId` 声明未使用 | panorama.js | L5 | 无 | 可选清理 |
| 9 | **P3** | `CODE_MAP` 别名重复声明 | panorama.js + match.js | L12 / L15 | 无 | 可选清理 |
| 10 | **P3** | `.hero` 初审误判 | — | — | — | ❌ 不是问题 |
| 11 | **P3** | `.control-panel` 初审误判 | — | — | — | ❌ 不是问题 |
| 12 | **P3** | 子页面无 breadcrumb | panorama/teams.html | — | 导航便利性 | 可选增强 |
| 13 | **P3** | `.eyebrow` 的 `text-transform: uppercase` 对中文无效 | portal.css | L39 | 样式 | 可选清理 |

---

## 问题详细分析

### 问题 #1 — P0：panorama.js `formatDate()` 未定义

**根因**：`formatDate()` 函数在 `homepage.js:449` 和 `match.js:323` 中各自定义了一份。但全景页只加载 `common.js` + `panorama.js`，不加载 `homepage.js` 或 `match.js`。`panorama.js:477` 调用了 `formatDate()` 但该函数在全景页作用域中不存在。

**现象**：全景页 `updateGeneratedAt()` 执行时抛出 `ReferenceError: formatDate is not defined`，导致 `[data-generated-at]` 元素的"数据生成：xxxx"文本永远不会渲染。

**爆炸半径**：全景页所有用户。错误被 `initPanorama().catch()` 捕获，但 catch 块只显示错误消息到 panorama-grid 容器，可能覆盖已渲染的赛程数据。

**证据**：
- `panorama.js:476-478`：`el.textContent = "数据生成：" + formatDate(scheduleData.generated_at);`
- `common.js`：无 `formatDate` 定义
- `panorama.html`：只加载 `js/common.js` + `js/panorama.js`

**修复方式**：在 `common.js` 中添加 `formatDate()` 共享函数，然后从 `homepage.js` 和 `match.js` 中删除各自的副本。或在 `panorama.js` 顶部定义本地 `formatDate`。

**紧急度**：🔴 立即修复

---

### 问题 #2 — P1：baselines 数据文件含禁止词汇

**根因**：`build_site_data.py` 生成 `baselines.json` 时，直接复制了内部数据源的 `description` 字段，未执行 spec 1.4 要求的清洗。

**证据**（`baselines-data.js` L1，market.description）：
> "基于 Polymarket 公开赔率转隐含概率（归一化至 100%）。来源等级: Yellow（仅作描述性参照）。不用于投注建议。**不输出仓位/赔率价值/ROI/PnL/Sharpe**。"

包含的禁止词汇：`仓位`、`赔率价值`、`ROI`、`PnL`、`Sharpe`。

**爆炸半径**：`baselines-data.js` 作为 `<script>` 标签加载到首页，`window.CDS4WORLDCUP_BASELINES` 对象可被浏览器控制台访问。虽然当前 UI 渲染代码（`homepage.js`、`team-detail.js`）只使用 `construction_rule_short` 和 `display_boundary` 属性，不直接暴露 `description`，但数据本身已作为公开站点资源发布。

**修复方式**：
1. 在 `build_site_data.py` 中添加 `description` 字段的词汇清洗逻辑
2. 或从公开 JSON 中移除 `description` 字段（若前端不消费该字段）
3. 或用中文自然语言替换当前的 `description` 内容

**紧急度**：🟠 尽快修复

---

### 问题 #3 — P2：子页面无 `<footer>` 元素

**根因**：`index.html` 的 `</main>` 后没有语义化的 `<footer>` HTML 元素（其"更新记录"section 充当事实上的页脚）。其他 4 个页面连这个 section 都没有。

**影响页面**：
- `match.html`：无任何页脚
- `panorama.html`：有 `.panorama-footer` section（免责声明），但不是语义 `<footer>`
- `team.html`：无任何页脚
- `teams.html`：无任何页脚

**爆炸半径**：所有子页面用户。长页面（如 team.html，可滚动 3000+px）滚到底部时无视觉终止信号。

**修复方式**：创建共享的 `<footer>` 组件（可通过 JS 注入或 HTML 模板），包含免责声明 + 最后更新时间 + 返回首页链接。

**紧急度**：🟡 下次迭代修复

---

### 问题 #4 — P2：导航栏链接数不一致

**根因**：各页面独立编写 topbar，未使用共享模板。`index.html` 包含 6 个锚点跳转链接（选球队、AI 多视角、看难点、外界怎么看、方法和来源、更新记录），这些锚点只存在于首页，子页面不需要，但子页面也没有替代的导航元素。

**具体差异**：
| 页面 | 导航链接数 | 链接内容 |
|------|----------|---------|
| index.html | 9 | 首页 + 全景图 + 球队 + `|` + 6 个锚点 |
| panorama.html | 3 | 首页 + 全景图 + 球队 |
| team.html | 3 | 首页 + 全景图 + 球队 |
| teams.html | 3 | 首页 + 全景图 + 球队 |
| match.html | 3 | 首页 + 全景图 + 球队 |

**评估**：这是有意为之——子页面没有锚点 section。但"跳转到首页的某个 section"功能对子页面用户也有价值。不是 bug，是设计决策。

**紧急度**：🟡 可在下次导航重构时处理

---

### 问题 #5 — P2：baselines 数据含学术化英文公式

**根因**：同问题 #2，`description` 字段未经公众语言清洗。

**证据**（`baselines-data.js` L1）：
- `fifa_ranking.description`：`"P(team_i) = (1/rank_i) / Σ(1/rank_j)。排名来源: FIFA Men's World Ranking 2025-11-19..."`
- `elo.description`：`"P(i beats j) = elo_i / (elo_i + elo_j)。Top-20 来源: World Football Elo Ratings (eloratings.net)...Bradley-Terry 参数..."`

**与 spec 冲突**：Spec 1.1 要求 *"Use plain Chinese that football fans understand"*。当前 `description` 含数学公式和英文术语。

**爆炸半径**：同问题 #2，数据未被 UI 直接渲染，但作为公开数据产物与公众语言导向不一致。

**修复方式**：将 `description` 替换为中文自然语言说明，如 "根据 FIFA 排名换算每队的夺冠参考概率"。

**紧急度**：🟡 与问题 #2 一并处理

---

### 问题 #6 — P2：全景页 match-detail 死 DOM

**根因**：`panorama.js:246` 每张比赛卡片都渲染了一个 `div.match-detail`（含场馆、城市、预测详情），但卡片的 click handler（`bindMatchCardClicks`）直接跳转到 `match.html?id=xxx`，从未展开这些 detail div。

**影响**：104 场小组赛 × ~15 行隐藏 HTML ≈ 1560 行无效 DOM，增加约 15% 的全景页 DOM 体积。

**爆炸半径**：仅影响全景页的 DOM 大小和内存占用。对用户无直接可见影响。

**修复方式**：二选一：
1. **删除**：从 `renderMatchCard()` 中移除 `match-detail` 渲染逻辑（推荐，最简单）
2. **实现**：添加 hover/click 展开功能，在跳转前显示场馆和 xG 信息

**紧急度**：🟡 低优先级，技术债务

---

### 问题 #7 — P2：CSS 重复 `@media` 块

**根因**：快速迭代开发中，新规则追加到了文件末尾而非合并到已有的 640px 块。

**证据**：
- `portal.css:1319`：`@media (max-width: 640px)` — 包含 `.ai-perspective-section`、`.faction-grid`、`.ref-compare-row`
- `portal.css:1334`：`@media (max-width: 640px)` — 包含 `.topbar`、`.topnav`、`.portal`、`.metric-board`、`.team-grid` 等

两个块之间还有其他 CSS 规则（非 media query），它们本可以放在同一个 `@media` 块中。

**爆炸半径**：不影响渲染（CSS 解析器正常处理重复 media query），但增加维护成本和文件体积。

**修复方式**：将 L1334 起的 `@media (max-width: 640px)` 内容合并到 L1319 的块中。

**紧急度**：🟢 代码整洁，随时可修

---

### 问题 #8-9 — P3：死代码和代码重复

**#8 `expandedMatchId`**：`panorama.js:5` 声明 `let expandedMatchId = null` 但全文从未读写。推测是展开功能的残留状态变量。

**#9 `CODE_MAP` 别名**：`panorama.js:12` 和 `match.js:15` 各自声明 `var CODE_MAP = CDS4WORLDCUP_COUNTRY_MAP`，以及本地 `codeFlag`/`codeName` 包装函数。这些与 `common.js` 导出的 `cdsCodeFlag`/`cdsCodeName`/`cdsCodeSlug` 功能完全重复。

**紧急度**：🟢 技术债务，不影响功能

---

### 问题 #10-11 — 已排除：初审误判

**#10 `.hero` 移动端断点**：初审认为缺少断点，实际在 `portal.css:1296`（`@media (max-width: 900px)`）中 `.hero` 已折叠为 `grid-template-columns: 1fr`。**不是问题。**

**#11 `.control-panel` 平板断点**：同上，L1296 的 900px 断点已覆盖 `.control-panel`。**不是问题。**

---

### 问题 #12 — P3：子页面无 breadcrumb

**现状**：只有 `match.html` 和 `team.html` 有面包屑导航。`panorama.html` 和 `teams.html` 没有。

**评估**：panorama 和 teams 是顶级页面，不需要面包屑。这是有意为之，不是遗漏。

**紧急度**：🟢 不需要修复

---

### 问题 #13 — P3：`text-transform: uppercase` 对中文无效

**证据**：`portal.css:38-42`
```css
.eyebrow, .label {
  text-transform: uppercase;
}
```

中文文本如"2026 世界杯 · 夺冠路拆解"被 `uppercase` 处理后，汉字无变化，但英文数字和标点可能被意外大写化。

**爆炸半径**：视觉影响极小，仅影响 `.eyebrow` 和 `.label` 元素中的英文字符。

**紧急度**：🟢 可选清理

---

## 根因总结

1. **函数共享缺失**（问题 #1）：`formatDate()` 在 homepage.js 和 match.js 中各定义了一份，未提取到 common.js。panorama.js 开发时假设该函数可用但实际不可用。
2. **数据管道清洗缺失**（问题 #2、#5）：`build_site_data.py` 未对 `description` 字段执行 spec 要求的词汇清洗和公众语言转换。
3. **组件化不足**（问题 #3、#4）：页脚和导航栏在每个 HTML 页面中独立编写，未使用共享模板或 JS 注入。
4. **快速迭代遗留**（问题 #6、#7、#8、#9）：多 commit 快速开发期间产生的死代码、重复代码和未合并的 CSS 块。

---

## 修复建议（按优先级排序）

### 立即修复（P0-P1）

1. **`common.js` — 添加共享 `formatDate()`**
   - 将 `homepage.js:449-455` 的 `formatDate` 移动到 `common.js`
   - 从 `homepage.js` 和 `match.js` 中删除各自的 `formatDate` 副本
   - `panorama.js` 自动获得该函数

2. **`build_site_data.py` — 清洗 `description` 字段**
   - 删除或替换 `baselines.json` 中 market.description 的禁止词汇
   - 将 `fifa_ranking.description` 和 `elo.description` 的英文公式替换为中文说明
   - 或从公开 JSON 中移除 `description` 字段（若前端不消费）

### 下次迭代修复（P2）

3. **创建共享页脚组件** — 通过 `common.js` 注入或 HTML 模板
4. **清理 panorama.js 死 DOM** — 移除 `match-detail` 渲染或实现展开功能
5. **合并重复 CSS `@media` 块** — portal.css L1334 合并到 L1319

### 可选改进（P3）

6. 清理 `expandedMatchId` 死变量
7. 统一 `CODE_MAP` 别名为 `common.js` 函数
8. 评估是否为子页面增加首页锚点导航

---

## 预防措施

1. **共享函数集中管理**：所有跨页面使用的工具函数必须放在 `common.js` 中，禁止在页面 JS 中重复定义
2. **数据管道增加清洗步骤**：`build_site_data.py` 应在输出前对所有文本字段执行 spec 合规检查
3. **CSS 组织规范**：新规则应合并到已有 `@media` 块中，不要在文件末尾追加新的同断点块
4. **定期死代码扫描**：使用 lint 工具检测未使用的变量和函数
