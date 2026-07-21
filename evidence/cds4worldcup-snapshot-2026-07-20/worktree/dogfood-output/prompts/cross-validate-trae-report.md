# 交叉验证 Prompt — 确认 Trae AI 报告的错误是否真实存在

> 使用方式：将此 prompt 整段发给 Mimo Code，它会启动站点、截图、逐条验证。
> 背景：Trae AI 用 agent-browser 对站点做了运行时视觉检查，报告了 4 个问题。我们需要用 Mimo 的视觉能力独立确认每个问题是否真实。

---

## 任务

另一个 AI 报告了 CDS4WorldCup 公开站点的 4 个问题。请你**独立验证**每个问题是否真实存在。

你的工作方式：
1. 启动本地服务器
2. 对相关页面截图
3. **只看截图**（不要读代码），判断每个问题是否可见
4. 输出验证结果

---

## 第零步：启动站点

```bash
python3 scripts/build_site_data.py
cd site && python3 -m http.server 8000
```

等待服务器就绪后开始截图。

---

## 验证 ISSUE-001：AI 多视角模块内容是否缺失？

**Trae 的报告**：首页和球队详情页的 AI 多视角模块 HTML 骨架存在，但内容完全空白——没有派别卡片、没有点阵、没有视角文字。

### 验证步骤

1. 打开 `http://localhost:8000/`
2. 等页面加载完，**向下滚动**找到标题含"多视角"或"300 个视角"的区域
3. 截图保存为 `dogfood-output/screenshots/crossval-issue001-homepage.png`

4. 打开 `http://localhost:8000/team.html?team=argentina`
5. 向下滚动，找到标题含"AI 多视角怎么看"的区域
6. 截图保存为 `dogfood-output/screenshots/crossval-issue001-argentina.png`

### 判断标准

看截图回答：

- **如果真实**：你应该看到标题（如"300 个视角，不是一个声音"或"AI 多视角怎么看这队？"），但标题下方是**空白**或者只显示"AI 多视角数据还在整理"这种占位文字。没有彩色卡片，没有小圆点点阵。
- **如果不真实（Trae 误报）**：你应该看到 10 个彩色派别卡片（数据派、赔率派、老球迷派……），每个卡片内有彩色小圆点点阵、派别名称、视角数量、以及一段代表观点文字。

**你需要回答**：
- 首页 AI 多视角区域：[ 空白 / 有内容 ]，截图证据：
- 详情页 AI 多视角区域：[ 空白 / 有内容 ]，截图证据：
- **结论**：Trae 的报告 [ 准确 / 误报 ]

---

## 验证 ISSUE-002：路径推演情景是否为英文？

**Trae 的报告**：球队详情页的"CDS 路径分析"中，"关键情景"模块的描述文字全部为英文（如 "Win all remaining matches → guaranteed top 2"），"Bracket 依赖"也是英文。

### 验证步骤

1. 打开 `http://localhost:8000/team.html?team=argentina`
2. 找到"CDS 路径分析"或"夺冠路拆解"区域
3. 如果需要点击某个按钮或标签才能展开路径分析，就点击它
4. 找到"关键情景"子区域
5. 截图保存为 `dogfood-output/screenshots/crossval-issue002-scenarios.png`

6. 继续向下滚动，找到"Bracket 依赖"或"最大阻力节点"区域
7. 截图保存为 `dogfood-output/screenshots/crossval-issue002-bracket.png`

8. 再打开一支简版球队（如 `http://localhost:8000/team.html?team=panama`）
9. 看它的路径分析是否也有英文
10. 截图保存为 `dogfood-output/screenshots/crossval-issue002-panama.png`

### 判断标准

- **如果真实**：你会在"关键情景"区域看到类似这样的英文文字：
  - "Win all remaining matches → guaranteed top 2"
  - "Already guaranteed qualification (all outcomes → top 2)"
  - "Losing to XXX → qualification at risk"
  - "Lose all 3 group matches → eliminated"
  以及"Bracket 依赖"区域看到：
  - "R16 opponent: W85; QF opponent: W95; SF opponent: W99; Final opponent: W101"
- **如果不真实（Trae 误报）**：所有文字都是中文，如"赢下全部剩余比赛 → 确保前二出线"。

**你需要回答**：
- 情景描述（trigger）的语言：[ 英文 / 中文 ]
- Bracket 依赖的语言：[ 英文 / 中文 ]
- 是否违反 Spec 1.1 "plain Chinese"：[ 是 / 否 ]
- **结论**：Trae 的报告 [ 准确 / 误报 ]

---

## 验证 ISSUE-003：CSS media query 是否重复？

**Trae 的报告**：`portal.css` 中有两个连续的 `@media (max-width: 640px)` 块应该合并。

### 验证方式

这个问题是**代码层面**的，视觉上无法直接看到"两个 media query"。但你可以间接验证：

1. 打开 `http://localhost:8000/`（桌面端 1280×800）
2. 截图保存为 `dogfood-output/screenshots/crossval-issue003-desktop.png`
3. 切换到移动端（390×844）
4. 截图保存为 `dogfood-output/screenshots/crossval-issue003-mobile.png`

### 判断标准

- **如果移动端布局看起来正常**（单列、没有溢出、导航正确），说明 CSS media query **功能正常**，重复只是一个代码整洁问题（不影响用户）
- **如果移动端布局异常**（多列未折叠、内容溢出、导航折行），说明可能有 media query 未生效

**你需要回答**：
- 桌面端布局：[ 正常（多列）/ 异常（单列）]
- 移动端布局：[ 正常（单列）/ 异常（溢出/多列）]
- **结论**：Trae 报告的 CSS 重复 [ 确认存在但不影响 / 影响功能 / 无法视觉确认 ]

> 注意：此问题需同时运行 `grep -n "@media.*640px" site/css/portal.css` 来精确确认代码层面是否有两个块。

---

## 验证 ISSUE-004：公开数据中是否含禁止词汇？

**Trae 的报告**：`baselines-data.js` 的 `description` 字段包含 "ROI"、"PnL"、"Sharpe"、"仓位" 等禁止词汇（以否定形式出现，如"不输出 ROI/PnL/Sharpe"）。

### 验证方式

这个需要**两种验证**：

#### A. 代码验证

```bash
# 检查 site/ 下所有文件是否包含禁止词汇
grep -rn "ROI\|PnL\|Sharpe\|仓位" site/data/
grep -rn "Kimi\|小米\|Xiaomi\|MiMo" site/
grep -rn "投注建议\|低估\|高估\|value bet" site/
```

#### B. 视觉验证

即使数据文件中有这些词，关键是**用户能否在页面上看到它们**。

1. 打开 `http://localhost:8000/`
2. 向下滚动到"外界怎么看"区域
3. 截图保存为 `dogfood-output/screenshots/crossval-issue004-homepage-baselines.png`

4. 打开 `http://localhost:8000/team.html?team=argentina`
5. 找到外部参考/baselines 区域
6. 截图保存为 `dogfood-output/screenshots/crossval-issue004-argentina-baselines.png`

### 判断标准

- **如果真实（视觉层面）**：你能在截图中**直接看到** "ROI"、"PnL"、"Sharpe"、"仓位" 等文字
- **如果真实但仅数据层面**：grep 找到了这些词，但截图中看不到——说明是数据文件卫生问题，不直接影响用户
- **如果不真实**：grep 和截图都没有这些词

**你需要回答**：
- grep 结果：[ 有 / 无 ] 禁止词汇
- 截图中用户可见：[ 有 / 无 ] 禁止词汇
- **结论**：Trae 的报告 [ 准确且影响用户 / 准确但不影响用户（数据卫生问题）/ 误报 ]

---

## 额外验证：之前的已知问题

在截图过程中，顺便确认以下历史问题：

### P0-历史：panorama.js 的 `formatDate()` 未定义

1. 打开 `http://localhost:8765/panorama.html`
2. 打开浏览器开发者工具的 Console 面板
3. 看是否有红色错误 `ReferenceError: formatDate is not defined`
4. 截图保存为 `dogfood-output/screenshots/crossval-panorama-console.png`

**判断**：Console 有无红色错误？

### P0-历史：桌面端布局是否被强制单列

看你之前截的 `crossval-issue003-desktop.png`：

- 首页 Hero 区域应该是**左右双列**（左边文字 + 右边数据面板）
- 如果整个页面都是单列 = P0 仍然存在

### P1-历史：外部参考图表标题与内容不符

1. 在首页向下滚动找到"外界怎么看"区域下方的图表
2. 图表标题写的是什么？
3. 图表中实际显示了几组数据条？（一组绿色条 = 只有市场数据；两组不同颜色条 = 有对比）

截图保存为 `dogfood-output/screenshots/crossval-external-ref-chart.png`

**判断**：
- 标题：`______`
- 数据条组数：`______`
- 标题和内容是否一致：[ 是 / 否 ]

---

## 输出格式

完成后，输出以下结构化报告：

```markdown
# 交叉验证报告 — Trae AI 报告确认

**日期**：{今天}
**验证方式**：本地服务器截图 + 代码 grep
**站点版本**：{git log --oneline -1}

## 验证结果总览

| # | Trae 报告的问题 | Mimo 验证结论 | 证据截图 | 备注 |
|---|----------------|--------------|---------|------|
| 001 | AI 多视角模块内容缺失 | ✅确认 / ❌误报 | | |
| 002 | 路径推演情景为英文 | ✅确认 / ❌误报 | | |
| 003 | CSS 重复 media query | ✅确认 / ⚠️代码问题不影响视觉 | | |
| 004 | 数据含禁止词汇 | ✅确认影响用户 / ✅确认仅数据层 / ❌误报 | | |
| 历史-P0 | formatDate 未定义 | ✅确认 / ❌已修复 | | |
| 历史-P0 | 桌面端单列布局 | ✅确认 / ❌已修复 | | |
| 历史-P1 | 图表标题内容不符 | ✅确认 / ❌已修复 | | |

## 每个问题的详细判断

### ISSUE-001
（你的描述 + 截图引用）

### ISSUE-002
（你的描述 + 截图引用）

...（依次列出）

## Trae 报告的可信度评估

- 准确的问题数：? / 4
- 误报的问题数：? / 4
- 部分准确的问题数：? / 4
- 总体评价：[ 高度可信 / 部分可信 / 需要更多验证 ]
```

---

## 约束

- 你的主要判断依据是**截图**，不是代码。代码 grep 只作为 ISSUE-003 和 ISSUE-004 的补充。
- 如果截图和代码结果矛盾，以截图为准（用户看到什么，什么就是真实）。
- 完成后关闭本地服务器。
- 所有截图保存到 `dogfood-output/screenshots/`。
