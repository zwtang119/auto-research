# Investigation: Refactoring Analysis Verification

## Summary
经过逐行验证，原始报告中的 28 个问题中：**4 个 P0 bug 全部确认真实**（但其中 2 个级别需下调），**10 个重复代码问题全部确认**，**7 个死代码/清理项全部确认**，**7 个结构改进全部确认**。有 3 个问题的严重级别需要调整。

## Verified Findings

### 🔴 P0 Bug Verification

| ID | 问题 | 验证结果 | 证据 | 根因 |
|----|------|----------|------|------|
| **C1** | CSS 媒体查询断裂 | ✅ **确认，P0 正确** | portal.css L1351-1378 在两个 `@media (max-width:640px)` 之间无条件生效，L1379 有孤立 `}` | Git blame: commit `253f02f8`（"Add AI perspectives"，Jun 12 01:41）替换了 `@media (max-width:900px)` 的内容，原 900px 规则被挤出媒体查询 |
| **C2** | `.source-mixed` CSS 缺失 | ✅ **确认，但降为 P1** | file_search 确认：homepage.js:383 和 team-detail.js:277 返回 "source-mixed"，但 portal.css 中零匹配 | sourceClass() 函数的 fallback 路径从未定义对应 CSS 样式。影响：来源标签只显示无背景色的文字，不是功能性断裂 |
| **P14** | kimi_prob 计算分歧 | ✅ **确认，但降为 P2** | generate_path_cards.py:79 读聚合 JSON (`team_agg.get("probability")`), patch_section9.py:130 用 `len(kimi_agents)/300*100` 近似。注释写明"简单近似" | patch_section9.py 无法访问聚合 JSON（设计限制），是有意妥协，非意外 bug |
| **H1** | teams.html 缺 topbar | ✅ **确认，但降为 P1** | 直接读取 teams.html（55行）：无 `<header>` 元素，仅有一个"返回研究门户"按钮链接 | 创建时未添加 topbar，有替代导航但不一致 |

### 🟠 P1 Duplication Verification

| ID | 重复内容 | 验证结果 | 证据（逐行比对） |
|----|----------|----------|-----------------|
| **P1** | 信号计算逻辑 | ✅ **确认，精确复制** | generate_path_cards.py:94-101 ≡ patch_section9.py:88-103：相同阈值（>10, >20, ≥5, <5），相同信号名 |
| **P2** | §9 Marginalia 生成 | ✅ **确认，近乎一致** | generate_path_cards.py:209-233 ≈ patch_section9.py:41-66：同结构（派别分布→概率→前5条reason→Red Source memo） |
| **P3** | group_kimi_by_team | ✅ **确认，函数体完全一致** | generate_path_cards.py:44-50 ≡ patch_section9.py:32-39：同一个循环，同一个 key 提取 |
| **P5** | slug 生成 | ⚠️ **部分确认** | generate_path_cards.py:69 和 patch_section9.py:122 的内联 slug 代码完全一致。fetch_market_snapshot.py:46 的 slugify() 是不同实现，因为输入不同（API 问题字符串 vs 队伍名）→ **实际上是 2 种 slug 逻辑，不是 3 种** |
| **F1** | escapeHtml/escapeAttr | ✅ **确认，逐字复制** | homepage.js:416-430 和 team-detail.js:280-290 完全一致。teams.js:119-135 用 `||` 替代 `??`（微小不一致） |
| **F2** | sourceClass() | ✅ **确认，完全一致** | homepage.js:379-383 ≡ team-detail.js:273-277 |
| **F3** | 柱状图渲染 | ✅ **确认，3 套 CSS 类名做同一件事** | homepage.js renderObstacleChart/renderExternalReferenceChart, team-detail.js renderBarChart — 同样的宽度计算、标签+轨道+填充模式 |
| **C5** | card-chrome CSS 重复 | ✅ **确认** | portal.css 中 `rgba(255,253,248,.92)` + `border` + `box-shadow` 重复 ~9 次 |

### 🟡 P2 Dead Code Verification

| ID | 问题 | 验证结果 | 备注 |
|----|------|----------|------|
| **P9** | `import os` 未使用 | ✅ 确认 | build_site_data.py:11, generate_path_cards.py:12 — 用 pathlib.Path，不需要 os |
| **P9b** | `defaultdict` 未使用 | ✅ 确认 | src/analysis/group_difficulty.py |
| **C3/C4** | ~15 未使用 CSS 选择器 + 2 未使用变量 | ✅ 确认 | .panel*, .status-*, .update-*, .wrapper, .page-content, --pitch, --grass |
| **P13** | meta.json 孤立文件 | ✅ 确认 | build_site_data.py 输出但无 HTML/JS 引用 |
| **P8** | 测试常量复制 | ✅ 确认 | test_build_site_data.py 独立定义了 PUBLIC_VENDOR_FORBIDDEN/PUBLIC_BETTING_FORBIDDEN |

### 🔵 P3 Structural Verification

| ID | 问题 | 验证结果 |
|----|------|----------|
| **P12** | 无共享工具模块 | ✅ 确认 — src/utils/ 已在 src/README.md 规划但未创建 |
| **P11** | sys.path hack | ✅ 确认 — audit_path_cards.py:12 |
| **B1** | Makefile results 不运行构建 | ✅ 确认 — 只复制 site/ 到 _publish/ |
| **B4** | pages.yml 与 Makefile 逻辑重复 | ✅ 确认 |
| **B2** | 测试覆盖低 | ✅ 确认 — 7/9 脚本零测试 |
| **H2** | 脚本加载不一致 | ✅ 确认 — teams.js 无 defer |
| **P7** | PLACEHOLDER_PATTERNS 同名不同义 | ✅ 确认 |

## Severity Adjustments

| ID | 原始级别 | 调整后 | 理由 |
|----|----------|--------|------|
| C2 | P0 | **P1** | 标签仍显示，只是无特殊背景色；fallback 场景极少触发 |
| P14 | P0 | **P2** | 代码注释明确标注"简单近似"，是有意妥协而非 bug |
| H1 | P0 | **P1** | 有替代导航（"返回研究门户"按钮），不是完全无路可走 |
| P5 | P1 | **P1 保留但范围缩小** | 实际只有 2 种 slug 逻辑（非 3 种），fetch_market_snapshot 的输入类型不同 |

## Root Cause Analysis

### 根因 1：快速迭代导致代码复制
patch_section9.py 是作为 generate_path_cards.py 的 hotfix 创建的，复制了信号计算、§9生成、分组、slug 等逻辑。代码注释证实这是有意的快速修复。

### 根因 2：AI 视角功能引入时 CSS 编辑失误
Git 考证确认：commit `253f02f8`（"Add AI perspectives"）在编辑 `@media (max-width:900px)` 块时，意外将原有响应式规则移出媒体查询范围。

### 根因 3：缺少共享工具模块
src/README.md 规划了 src/utils/ 但从未创建，导致每个脚本各自实现 CSV 加载、slug 生成等通用功能。

### 根因 4：静态站点无组件化
纯 HTML/JS 站点没有模板系统，导致 topbar、工具函数、柱状图渲染等在各页面间复制粘贴。

## Fix Plan

### 危险等级定义
- 🟢 **SAFE**：纯添加或删除死代码，不改变任何行为
- 🟡 **CAUTIOUS**：可能影响布局或数据，需要视觉/功能测试
- 🔴 **RISKY**：涉及数据流变更或跨文件重构

### 施工顺序（9 步，由安全到风险递进）

---

#### Step 1: 修 CSS 媒体查询 (C1)
- **危险**: 🟡 CAUTIOUS
- **爆炸范围**: `portal.css` 1 个文件
- **最小步骤**:
  1. 将 L1351-1378（4 个规则块，17 个选择器）移入 `@media (max-width: 900px)` 块（L1321-1334）内
  2. 删除 L1379 的孤立 `}`
  3. 在桌面和手机宽度下视觉验证布局
- **验证**: 桌面端应恢复多列布局，手机端不受影响

#### Step 2: 补 .source-mixed CSS (C2)
- **危险**: 🟢 SAFE
- **爆炸范围**: `portal.css` 1 个文件
- **最小步骤**:
  1. 在 source-green/yellow/red 附近添加 `.source-mixed { background: #f0efe8; color: var(--muted); }`
- **验证**: 搜索页面中 source 标签颜色

#### Step 3: 补 teams.html topbar (H1)
- **危险**: 🟢 SAFE
- **爆炸范围**: `teams.html` 1 个文件
- **最小步骤**:
  1. 在 `<body>` 后 `<main>` 前插入与 index.html 一致的 topbar HTML
  2. 统一脚本加载模式（data.js in head + app.js with defer）
- **验证**: 三页面导航一致

#### Step 4: 清理死代码 (P9, P13)
- **危险**: 🟢 SAFE
- **爆炸范围**: 3 个 Python 文件
- **最小步骤**:
  1. 删除 `build_site_data.py:11` 的 `import os`
  2. 删除 `generate_path_cards.py` 的 `import os`
  3. 删除 `group_difficulty.py` 的 `from collections import defaultdict`
  4. 删除 `build_site_data.py` 中输出 `meta.json` 的代码（~2 行）
  5. 删除 `site/data/meta.json`
- **验证**: `make check` 和测试通过

#### Step 5: 清理死 CSS (C3, C4, C5)
- **危险**: 🟢 SAFE
- **爆炸范围**: `portal.css` 1 个文件
- **最小步骤**:
  1. 删除 .panel-grid/.panel h3/.panel p 块
  2. 删除 .status-rail/.status-item/.status-track/.status-fill 块
  3. 删除 .update-contract/.update-steps 块
  4. 删除 .page-content/.wrapper 规则
  5. 删除 :root 中的 --pitch 和 --grass
  6. 提取 `.card-chrome` 共享类（background/border/shadow），替换 ~9 处重复
- **验证**: 三页面视觉回归测试

#### Step 6: 提取 Python 共享模块 (P1-P3, P5)
- **危险**: 🟡 CAUTIOUS
- **爆炸范围**: 新建 `src/utils/` + 修改 2 个脚本
- **最小步骤**:
  1. 创建 `src/__init__.py` 和 `src/utils/__init__.py`
  2. 创建 `src/utils/slug.py`：提取 `slugify(team_name)` 函数
  3. 创建 `src/utils/kimi.py`：提取 `group_kimi_by_team()`, `compute_signals()`, `build_section_9()`
  4. 创建 `src/utils/csv_helpers.py`：提取 `load_csv()`
  5. 修改 `generate_path_cards.py` 和 `patch_section9.py` 从 `src.utils` 导入
  6. 删除 `audit_path_cards.py` 的 `sys.path` hack，改用正规导入
- **验证**: `python3 scripts/generate_path_cards.py` 生成相同的卡片

#### Step 7: 提取前端 common.js (F1, F2)
- **危险**: 🟢 SAFE
- **爆炸范围**: 新建 `site/js/common.js` + 修改 3 个 HTML + 3 个 JS
- **最小步骤**:
  1. 创建 `site/js/common.js`：提取 `escapeHtml`, `escapeAttr`, `sourceClass`
  2. 在 3 个 HTML 的 `<head>` 中添加 `<script src="js/common.js"></script>`
  3. 从各 JS 文件中删除这些函数的副本
- **验证**: 三页面功能正常

#### Step 8: 修 Makefile 构建目标 (B1, B4)
- **危险**: 🟢 SAFE
- **爆炸范围**: `Makefile` 1 个文件（pages.yml 不变）
- **最小步骤**:
  1. 在 `results` 目标中添加 `python3 scripts/build_site_data.py` 调用（在 cp 之前）
- **验证**: `make results` 后 `_publish/` 中的 JSON 包含最新数据

#### Step 9: [可选] 统一柱状图渲染 (F3) + slugToTeamName 去重 (F5)
- **危险**: 🟡 CAUTIOUS
- **爆炸范围**: 3 个 JS 文件 + portal.css
- **最小步骤**:
  1. 在 common.js 中提取 `renderBarChart(data, cssPrefix)` 参数化函数
  2. 统一 CSS 类名为一种（或保留参数化前缀）
  3. homepage.js 中用 teams.json 数据替换硬编码的 slugToTeamName 映射
- **验证**: 柱状图和球队名称显示正常

### 不建议修复的项目
- **P14 (kimi_prob 近似)**：注释已标注为有意妥协。修复需要架构变更（让 patch 脚本访问聚合 JSON），风险大于收益。建议记录为已知技术债。
- **B2 (测试覆盖)**：长期目标，不阻塞当前重构。
- **F6 (双格式数据)**：file:// 兼容性是有意设计，~644 KB 重复不构成问题。

## Construction Order Summary

```
Step 1 (C1 CSS 媒体查询)  ← 最高优先，唯一的真实 P0
  ↓
Step 2 (C2 补 CSS 类)     ← 纯添加，零风险
Step 3 (H1 补 topbar)     ← 纯添加，零风险
Step 4 (P9/P13 死代码)    ← 纯删除，零风险
Step 5 (C3-C5 CSS 清理)   ← 删除+提取，低风险
  ↓
Step 6 (P1-P3 Python 共享模块) ← 重构，需测试
Step 7 (F1-F2 前端 common.js)  ← 重构，需测试
Step 8 (B1 Makefile 修复)      ← 纯添加，低风险
  ↓
Step 9 [可选] (F3 柱状图统一)   ← 重构，可延后
```

## Preventive Measures
1. 创建 `src/utils/` 共享模块后，新脚本应从该模块导入而非复制
2. CSS 修改后应做桌面+手机宽度视觉检查
3. 添加 CI 步骤在构建后验证站点可访问性


## Execution Outcome (2026-06-12)

按 spec 执行 PR-1 → PR-2 → PR-3 三批，复查结论如下。

### 已完成

| Batch | 内容 | 验证 |
|-------|------|------|
| PR-1 | portal.css `@media (max-width:900px)` 修复（L1280，括号配平 225/225）；补 `.source-mixed`；`renderExternalReferenceChart` 改为 public_model_crowd + market 并列双柱 | CSS 括号平衡 + 节点功能测试 ✅ |
| PR-2 | 删 `import os`；停生成 `meta.json`（文件已删）；两个 validator 改用 `PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN`；清 ~15 未用 CSS 选择器 + 2 未用 CSS 变量；teams.html 补 topbar + defer；Makefile `results` 加 build | 7/7 测试 + 重建 ✅ |
| PR-3 | 提取 `src/utils/{slug,csv_helpers,kimi}.py`；generate_path_cards / patch_section9 改用共享模块；新增 `site/js/common.js`；3 个 JS 删重复函数、3 个 HTML 统一 data→common→page 脚本顺序 | 脚本 AST 解析 + 导入解析 + 功能测试 ✅ |

### 复查中抓到的新 P0（已修）

> **escapeHtml 实体回退**：PR-3 抽取 `common.js` 时，命名 HTML 实体被剥离 —— `&amp;→&`、`&lt;→<`、`&gt;→>`、`&quot;→(删除)`，只剩 `&#039;` 正确。三页 JS 全部依赖这一份，等同全员退化，正是 commit `ebd1bad` 修过的站点级 bug。
>
> 根因：抽取时按"显示文本"复制，命名实体在读取渲染层被解码，数字实体 `&#039;`/`&#096;` 幸存。已按 HEAD 版逐字节还原并用 node 功能验证。

### 遗留 / 待确认

- **validator 禁词收窄**：统一到常量后，英文 `buy/sell/profit` 不再被拦截。与团队 curated 列表一致，但鉴于 source-policy「不输出投注建议」，是否需要补回这几条待定。
- **未纳入本次提交**：AGENTS.md（自动记忆日志）、wiki/index.md + wiki/decisions/institute-one-*、scripts/mimo_boundary_check.py、src/analysis/group_difficulty.py、docs/analysis/* 与 MiMo 调查文档 —— 属于另一条 MiMo/institute-one 工作线，留待单独提交。
- **card-chrome 提取**：按修正 Prompt 暂缓（JS 动态生成卡片，改 HTML 会漏）。

### Commit & 发布状态

- 本地提交：`10b0c55 refactor: extract shared utils, fix portal.css media query + escapeHtml regression`（28 文件，+1530 / -391）。
- 推送 **未完成**：本环境到 `github.com:443` 连接超时（`gh api` 能连 api.github.com 并确认 push 权限，但 git push 走的 github.com:443 不通）。
- 待执行：在可联网环境运行 `git push origin main`（会把 `5f32359` + `10b0c55` 一起推上去，CI 会跑 unit tests + TruffleHog）。
