# Mimo Code 视觉任务执行计划

> **日期**：2026-06-13（已更新，加入 Goal 模式）
> **目标**：用 Mimo Code 的视觉识别能力验证站点状态，用 Goal 模式自主完成修复和验证
> **总耗时估计**：Phase 1 手动 ~30min，Goal A-D 自主运行 ~2-4h

## ⚡ Goal 模式说明

Mimo Code 支持 Goal 模式：`/goal <停止条件>`。
Agent 自主工作，**独立验证模型**审查全部历史判断条件是否满足。
满足才停，不满足就反馈差距继续。

**详细 Goal 任务定义**见 `dogfood-output/prompts/GOAL-MODE-TASKS.md`

---

## 当前已知状态（代码层面预判）

在写执行计划前，我已从代码层面做了初步判断：

| 问题 | 来源 | 代码层面状态 | 需要视觉确认 |
|------|------|------------|------------|
| P0-formatDate | 视觉检查报告 | ✅ 已修复（已移至 common.js） | 确认 panorama 页无 JS 错误 |
| P0-CSS 裸露规则 | 升级检查报告 | ✅ 已修复（已包裹进 900px media query） | 确认桌面端多列布局正常 |
| P1-图表标题不符 | 升级检查报告 | ⚠️ 需确认 | 截图看图表显示几组数据 |
| ISSUE-001 AI 模块空白 | Trae 报告 | ⚠️ 可能误报（JS 和数据都在） | **最关键**：截图确认 |
| ISSUE-002 路径英文 | Trae 报告 | ✅ 确认（trigger 字段确实是英文） | 截图确认 |
| ISSUE-003 CSS 重复 | Trae 报告 | ✅ 确认（不影响视觉） | 移动端布局是否正常 |
| ISSUE-004 禁词 | Trae 报告 | ⚠️ 仅数据层，UI 不渲染 | 截图 + grep |

---

## 执行顺序

```
Phase 1: 交叉验证（手动，确认 Trae 报告真伪）        ← 正在跑
   ↓ 人类看结果
Goal A: 修复已确认的问题（自主，Goal 模式）           ← 最先启动
   ↓
Goal B: 修复后视觉回归（自主，Goal 模式）             ← 依赖 A
Goal C: CI 绿灯 + 合规扫描（自主，Goal 模式）         ← 依赖 A，可与 B 并行
   ↓
Goal D: 部署就绪检查（自主，Goal 模式）               ← 依赖 B + C
   ↓ 人类 push
```

Phase 2（全站基线）降级为可选——Goal B 的视觉回归已覆盖核心检查。

---

## Phase 1：交叉验证 Trae 报告

**目的**：用 Mimo 的眼睛独立确认 Trae 报告的 4 个问题是否真实，避免基于错误报告做无用功。

**重点**：ISSUE-001（AI 模块空白）最可能是误报，必须先确认。

### 给 Mimo 的 Prompt

```
你是一个视觉审查员。请验证另一个 AI 报告的 4 个站点问题是否真实。

## 准备

1. 构建站点数据：
   python3 scripts/build_site_data.py

2. 启动本地服务器：
   cd site && python3 -m http.server 8000

3. 创建截图目录：
   mkdir -p dogfood-output/screenshots/crossval

## 验证任务

### 任务 1：AI 多视角模块是否有内容？（最关键）

另一个 AI 说首页和详情页的 AI 多视角区域是空白的。

步骤：
a) 打开 http://localhost:8000/，向下滚动找到"多视角"或"300 个视角"区域，截图保存为 dogfood-output/screenshots/crossval/001-homepage-ai.png
b) 打开 http://localhost:8000/team.html?team=argentina，向下滚动找到"AI 多视角怎么看这队"，截图保存为 dogfood-output/screenshots/crossval/001-argentina-ai.png

看截图判断：
- 如果看到 10 个彩色派别卡片（数据派、赔率派……），每个有彩色小圆点和文字 → Trae 误报
- 如果只看到标题，下方空白或"AI 多视角数据还在整理" → Trae 准确

### 任务 2：路径推演情景是否为英文？

步骤：
a) 打开 http://localhost:8000/team.html?team=argentina，找到"CDS 路径分析"或"夺冠路拆解"区域，展开它，找到"关键情景"子区域，截图保存为 dogfood-output/screenshots/crossval/002-scenarios.png
b) 继续向下找到"Bracket 依赖"，截图保存为 dogfood-output/screenshots/crossval/002-bracket.png
c) 打开 http://localhost:8000/team.html?team=czech-republic（或任意简版队），看路径分析是否也有英文，截图保存为 dogfood-output/screenshots/crossval/002-czech.png

看截图判断：
- 如果看到 "Win all remaining matches → guaranteed top 2" 这类英文 → 确认准确
- 如果看到"赢下全部剩余比赛 → 确保前二出线"这类中文 → 误报

### 任务 3：桌面端和移动端布局是否正常？

步骤：
a) 桌面端（1280×800）打开首页，截图保存为 dogfood-output/screenshots/crossval/003-desktop.png
b) 移动端（390×844）打开首页，截图保存为 dogfood-output/screenshots/crossval/003-mobile.png

看截图判断：
- 桌面端 Hero 区域是否为左右双列（左边文字，右边数据面板）？
- 移动端是否折叠为单列？
- 有没有横向滚动条或内容溢出？

### 任务 4：页面上是否能看到禁止词汇？

步骤：
a) 首页向下滚动到"外界怎么看"区域，截图保存为 dogfood-output/screenshots/crossval/004-homepage-ref.png
b) 运行代码检查：
   grep -rn "ROI\|PnL\|Sharpe\|仓位" site/data/ 2>/dev/null | head -10
   grep -rn "Kimi\|小米\|Xiaomi\|MiMo" site/ 2>/dev/null | head -10
   grep -rn "投注建议\|低估\|高估" site/ 2>/dev/null | head -10

看截图 + grep 结果判断：
- 截图可见文字中是否有禁止词？
- grep 结果是否有命中？（即使命中，也要看截图中是否可见）

### 额外：检查已知历史问题

a) 打开 http://localhost:8000/panorama.html，检查浏览器 Console 有无红色错误，截图保存为 dogfood-output/screenshots/crossval/extra-panorama.png

## 输出

请按以下格式输出每个验证结果：

| # | 问题 | 验证结论 | 截图证据 | 一句话说明 |
|---|------|---------|---------|-----------|
| 001 | AI 模块空白 | 准确/误报 | 文件名 | ... |
| 002 | 路径英文 | 准确/误报 | 文件名 | ... |
| 003 | 布局异常 | 正常/异常 | 文件名 | ... |
| 004 | 禁词 | 可见/仅数据层/无 | 文件名 | ... |
| 历史 | formatDate | 已修复/仍存在 | 文件名 | ... |

完成后关闭本地服务器。
```

### 预期产出
- 8–10 张截图到 `dogfood-output/screenshots/crossval/`
- 一份验证结果表格

### 交付给人类的判断点
Phase 1 完成后，人类需要看验证结果再决定 Phase 3 修什么。

---

## Phase 2：全站视觉基线

**目的**：建立完整的截图基线，发现 Phase 1 未覆盖的视觉问题。

**前提**：Phase 1 已完成。

### 给 Mimo 的 Prompt

```
你是一个视觉测试员。对 CDS4WorldCup 站点做一次全站视觉基线测试。

## 准备

1. cd site && python3 -m http.server 8000
2. mkdir -p dogfood-output/screenshots/baseline

## 截图清单

对每个页面截 3 张图：
- 桌面端首屏 (1280×800)
- 桌面端滚动后（向下 800px）
- 移动端首屏 (390×844)

| 页面 | URL | 文件名前缀 |
|------|-----|-----------|
| 首页 | / | baseline-homepage |
| 全景页 | /panorama.html | baseline-panorama |
| 球队列表 | /teams.html | baseline-teams |
| 阿根廷详情 | /team.html?team=argentina | baseline-argentina |
| 西班牙详情 | /team.html?team=spain | baseline-spain |
| 巴拿马详情（简版） | /team.html?team=panama | baseline-panama |

文件名格式：`{前缀}-{desktop|scroll|mobile}.png`

共 18 张截图。

## 逐页 Checklist

对每一张截图，检查以下项目，记录 ✅ 或 ❌：

### 布局
1. 桌面端 Hero 是双列布局
2. 球队/数据网格是多列（3-4列）
3. 移动端全部折叠为单列
4. 无横向滚动条
5. 导航栏正常显示

### 内容
6. 中文正常渲染（无乱码、无方块字）
7. 国旗 emoji 显示
8. 概率数字在 0-100% 范围
9. 无意外的长段英文

### 图表
10. 条形图有颜色（非空白）
11. 热力图/矩阵可见
12. 来源标签（可靠事实/待核验线索/只能参考）可见

### AI 模块（首页 + 详情页）
13. 首页显示 10 个派别卡片 + 点阵
14. 详情页显示 AI 视角片段
15. 颜色为莫兰迪色系

### 合规
16. 无 "Kimi/小米/Xiaomi/MiMo" 字样
17. 无 "投注建议/ROI/PnL/仓位" 字样
18. 无开发者路径（scripts/、data/processed/）
19. 免责声明存在

## 输出

将结果写入 `dogfood-output/reports/visual-baseline-{今天日期}.md`，格式：

```markdown
# 视觉基线报告 — {日期}

## 总览
| 页面 | 检查项通过 | 检查项失败 | 截图数 |
|------|----------|----------|-------|

## 逐页结果
（每页一个 section，列出 ✅/❌）

## 发现的问题
（列出所有 ❌ 项，附截图引用和严重程度）

## 无问题项确认
（列出所有 ✅ 项，一句话描述看到了什么）
```

完成后关闭本地服务器。
```

### 预期产出
- 18 张基线截图
- 一份完整的视觉基线报告

---

## Goal A：修复已确认的问题（Goal 模式自主运行）

**前提**：Phase 1 验证结果已完成，人类已看过结果。

**方式**：直接发 Goal 停止条件，Mimo 自主完成。

### 停止条件

```
/goal cdspath.json 中所有 scenario trigger 为中文，bracket_dependency 使用中文轮次名，
build_site_data.py exit 0，pytest 全部通过，无越界修改，修复日志已写入 results/ops/
```

### 完整上下文（与 Goal 一起发）

见 `dogfood-output/prompts/GOAL-MODE-TASKS.md` 中 **Goal A** 部分。

包含：修复背景、翻译映射表、约束条件。

### 需要人类做的事

1. 看 Phase 1 结果
2. 批准修复：`APPROVE_FORMAL_MUTATION: site/ src/ scripts/`
3. 启动 Goal

Mimo 会自己：修改代码 → 构建 → 测试 → 验证 → 循环直到停止条件满足。

---

## Goal B：修复后视觉回归验证（Goal 模式自主运行）

**前提**：Goal A 完成。

### 停止条件

```
/goal 首页+详情页+全景页截图已保存到 dogfood-output/screenshots/postfix/，
截图中情景描述为中文，概率数字未变，首页桌面端双列布局未被破坏，Console 无红色错误，
回归报告已写入 dogfood-output/reports/
```

### 完整上下文

见 `GOAL-MODE-TASKS.md` 中 **Goal B** 部分。

Mimo 会自己：启动服务器 → 截图 → 对比修复前后 → 确认无回归 → 写报告。

---

## 总览：给人类的操作手册

```
Phase 1（手动）→ [看结果] → APPROVE → Goal A（自主）→ Goal B+C（自主）→ Goal D（自主）→ [确认] → push
```

| 步骤 | 谁做 | 做什么 | 产出 | 人类介入 |
|------|------|-------|------|---------|
| Phase 1 | Mimo | 交叉验证 Trae 报告 | 验证表 + 截图 | 看结果 |
| **判断点** | **人类** | **看 Phase 1，批准修复** | **决策** | **必做** |
| Goal A | Mimo 自主 | 修复代码 + 构建测试 + 写日志 | 代码变更 | 不需要 |
| Goal B | Mimo 自主 | 截图对比 + 视觉回归 | 回归报告 | 不需要 |
| Goal C | Mimo 自主 | CI 测试 + 禁词扫描 | 合规报告 | 不需要 |
| Goal D | Mimo 自主 | 部署就绪最终检查 | 就绪报告 | 不需要 |
| **部署** | **人类** | **push** | **上线** | **必做** |

### 人类只需要做 3 件事

1. **看 Phase 1 结果** → 决定哪些问题确认
2. **批准修复** → `APPROVE_FORMAL_MUTATION: site/ src/ scripts/`
3. **确认 Goal D 报告** → `git push`

中间 2–4 小时 Mimo 自主运行，你不需要盯着。

## 完整文件索引

| 文件 | 用途 |
|------|------|
| `dogfood-output/prompts/GOAL-MODE-TASKS.md` | 4 个 Goal 的停止条件 + 上下文（主要参考） |
| `dogfood-output/prompts/EXECUTION-PLAN.md` | 本文件（总计划） |
| `dogfood-output/prompts/cross-validate-trae-report.md` | Phase 1 交叉验证 prompt |
| `dogfood-output/prompts/deep-visual-audit.md` | 深度视觉审查 prompt（可选） |
| `.mimocode/commands/visual-site-test.md` | 日常视觉测试命令 |
