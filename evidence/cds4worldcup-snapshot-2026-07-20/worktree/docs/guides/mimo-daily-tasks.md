# Mimo 日常任务手册 — Goal 模式可执行任务集

> **日期**：2026-06-13
> **位置**：`docs/guides/mimo-daily-tasks.md`（维护者文档）
> **目标**：定义一组安全的、可验证的日常任务，让 Mimo 用 Goal 模式自主执行
> **前提**：Mimo 有视觉识别能力 + Goal 模式（独立验证者判断停止条件是否满足）
> **关联文档**：`docs/ops/mimo-season-campaign.md`（写入边界规则）

---

## ⚠️ 核心教训：防止与 daily-update 冲突

**2026-06-13 发生的事**：Mimo 长程任务在远端推送了 daily update，
与本地未提交的 fan-centric 重设计在 10 个数据文件上冲突，
导致主页内容不一致。

**根因**：`.github/workflows/daily-update.yml` 每天 UTC 00:00 自动跑全管线并 push。

### 防冲突协议（所有 Mimo 任务开始前必做）

```
1. git fetch origin && git pull --rebase origin main
   - 如果有冲突，停止并报告，不要手工解决数据文件冲突
2. 确认 git status 干净后再开始工作
3. 任务完成后立即 commit + push，不要积压未提交改动
```

**给 Mimo 的防冲突 Goal 条件**（可加到任何任务前）：
```
前置检查：git fetch origin 后，git rev-list --count HEAD..origin/main 输出为 0
（本地不落后于远端）。如果 > 0，先 rebase。
```

---

## 任务分级

```
A 类：日常运维（每天/每周，低风险，可全自动）
B 类：渐进式 refactor（小步迭代，中风险，Goal 驱动）
C 类：内容审计（只读，零风险）
D 类：需要人类审批的正式变更（高价值，不自动执行）
```

---

## A 类：日常运维

### A1. CI 绿灯守门（每天可跑）

```
/goal python3 -m pytest tests/ -q 全部通过（0 failed），
python3 scripts/build_site_data.py 以 exit 0 退出，
python3 scripts/verify.py --root wiki/ 无新增 P0/P1，
git status 工作树干净（所有变更已 commit）
```

**上下文**：跑全部测试和构建，确认管线健康。如果测试失败，修复它（不改测试断言来绕过）。
**预计**：10-20 分钟。**风险**：低。

### A2. 数据新鲜度检查（每天）

```
/goal data/processed/market_public_snapshot.json 的 last_fetched_at
是今天（或昨天，考虑到时区），status 为 available，
site/data/homepage.json 的 generated_at 是今天，
results/ops/data-freshness-{今天日期}.md 已写入新鲜度报告
```

**上下文**：检查市场快照和站点数据是否最新。如果 stale，运行 `python3 scripts/fetch_market_snapshot.py` + `build_site_data.py` 刷新。
**预计**：15 分钟。**风险**：低。

### A3. 品牌合规扫描（每周）

```
/goal grep -rn "Kimi\|小米\|Xiaomi\|MiMo\|MiMo Code" site/ 无命中，
grep -rn "投注建议\|ROI\|PnL\|Sharpe\|Kelly\|仓位\|低估\|高估\|value bet" site/ 无命中，
results/ops/compliance-scan-{今天日期}.md 已写入扫描报告
```

**上下文**：扫描公开站点，确保无品牌泄露和投注语言。如果有命中，定位并修复。
**预计**：10-15 分钟。**风险**：低。

---

## B 类：渐进式 Refactor（小步迭代）

> **原则**：一次只改一个关注点，每个改动都有可验证的停止条件。
> 不要一次性大重构——站点世界杯期间必须稳定。

### B1. CSS 重复 media query 合并

```
/goal site/css/portal.css 中 @media (max-width: 640px) 块只有一个
（grep -c "@media.*640px" site/css/portal.css == 1），
所有其他断点块也各自唯一（900px、prefers-reduced-motion 等无重复），
桌面端和移动端截图布局与合并前一致（无视觉回归），
44 测试通过
```

**上下文**：合并重复的 `@media` 块。纯合并，不改规则内容。
**预计**：15 分钟。**风险**：极低。

### B2. JS 共享函数提取到 common.js

```
/goal site/js/common.js 包含 formatDate、escapeHtml、escapeAttr、loadJSON
等被 2+ 文件使用的工具函数，
site/js/homepage.js、match.js、panorama.js、team-detail.js 中不再有这些函数的重复定义
（grep 每个函数名在这些文件中只出现在 import/调用处，无 function 定义），
所有页面截图正常渲染（无 JS 错误），
44 测试通过
```

**上下文**：之前 formatDate 已提取过。继续提取其他重复函数。一次提取一个函数，每提取一个验证一次。
**预计**：30-45 分钟。**风险**：低（逐函数验证）。

### B3. portal.css 分层（4226 行 → 多文件）

```
/goal site/css/portal.css 拆分为：
  portal-base.css（变量、reset、布局）
  portal-components.css（卡片、图表、导航）
  portal-responsive.css（所有 @media 块）
  portal-print.css（打印样式，如有）
所有 HTML 页面的 <link> 引用更新，
桌面端和移动端所有页面截图与拆分前逐像素一致（无视觉回归），
44 测试通过
```

**上下文**：portal.css 4226 行太大。按职责拆分。**这个任务风险较高**——建议先在分支上做，截图对比后再合并。
**预计**：1-2 小时。**风险**：中。

### B4. 死代码清理

```
/goal site/js/panorama.js 中 expandedMatchId（如仍存在且未使用）已删除，
所有 -data.js 文件中无未消费的字段（可选，需人工确认），
44 测试通过，所有页面截图正常
```

**上下文**：清理已知的死变量和死代码。先 grep 确认未使用再删。
**预计**：20 分钟。**风险**：低。

---

## C 类：内容审计（只读，零风险）

### C1. 48 队 Team Card 全面审计

```
/goal data/ops/candidate/full-48-audit-{今天日期}.csv 存在且含 48 行，
每行包含：team, has_green_source(bool), obstacle_count, placeholder_count,
source_boundary_compliant(bool),
data/ops/review_queue/full-48-audit-review-{今天日期}.md 含摘要统计
（多少队有 Green Source、多少队 placeholder > 5 等）
```

**上下文**：审计 `artifacts/team-cards/` 下全部 48 张卡片。**只读，不修改任何文件**。
**预计**：30-40 分钟。**风险**：零。

### C2. 来源缺口地图

```
/goal python3 scripts/source_gap_scanner.py 运行成功，
data/ops/candidate/source-gap-{今天日期}.csv 已生成，
high/critical 队数已统计在 data/ops/review_queue/source-gap-review-{今天日期}.md
```

**上下文**：运行来源缺口扫描，生成地图。只读。
**预计**：15 分钟。**风险**：零。

### C3. 视觉回归基线（需要视觉能力）

```
/goal dogfood-output/screenshots/baseline-{今天日期}/ 包含 18 张截图
（6 页面 × 桌面/移动/滚动），
dogfood-output/reports/visual-baseline-{今天日期}.md 含逐页 checklist 结果，
所有发现的问题已分级（critical/high/medium/low）
```

**上下文**：用 Mimo 的视觉能力对站点做全面截图 + checklist。这是 Mimo 独有价值所在。
**预计**：30-45 分钟。**风险**：零（只看不动）。

---

## D 类：需要人类审批的正式变更

### D1. Team Registry 重建（task_queue T005）

```
/goal data/ops/review_queue/ 中存在完整的 registry-rebuild formal-change-proposal，
含 10 队移除列表、10 队新增列表、12 组重建对照表，
每个变更都有 Wikipedia/FIFA 来源标注
```

**⚠️ 执行实际修改需要**：`APPROVE_FORMAL_MUTATION: data/processed/team_registry.csv data/processed/schedule.json`

### D2. Wiki 批注修复

```
/goal python3 scripts/audit.py --root wiki/ 输出 issues 数组为空，
所有缺日期的批注已补日期，
wiki/index.md 有今天的 memo 批注
```

**⚠️ 需要**：`APPROVE_FORMAL_MUTATION: wiki/`

---

## 推荐执行节奏

| 频率 | 任务 | 说明 |
|------|------|------|
| **每天** | A1（CI 绿灯）+ A2（数据新鲜度） | 维持管线健康 |
| **每周** | A3（合规扫描）+ C3（视觉基线） | 防止退化 |
| **每周 1-2 个** | B 类任选（B1→B2→B4→B3） | 渐进 refactor |
| **每月** | C1（全队审计）+ C2（来源缺口） | 内容质量 |
| **按需** | D 类（人类审批后） | 正式变更 |

---

## 给 Mimo 的标准启动指令

每次启动 Mimo 做 A/B 类任务时，先发这段：

```
请执行 dogfood-output/prompts/MIMO-DAILY-TASKS.md 中的 [任务编号]。

开始前必须执行防冲突协议：
1. git fetch origin
2. git pull --rebase origin main（如有冲突，停止报告，不要手工解决数据文件）
3. 确认 git status 干净

然后用 Goal 模式执行任务的停止条件。
所有产物按 campaign 规则写入 candidate/review_queue/results/ops。
完成后立即 commit + push。
```

---

## 不适合 Goal 模式的任务（人类必须参与）

| 任务 | 原因 |
|------|------|
| 来源分级判断（Green/Yellow/Red） | 需要人类判断来源可信度 |
| 首页文案 / 中文表达优化 | 主观判断"通不通顺" |
| Spec 设计 / 架构决策 | 创意性工作，无可机器验证的停止条件 |
| 投注相关数据解读 | source-policy 禁止 AI 自行判断 |
| 跨 daily-update 窗口的长程手工工作 | 会与自动推送冲突（见核心教训） |
