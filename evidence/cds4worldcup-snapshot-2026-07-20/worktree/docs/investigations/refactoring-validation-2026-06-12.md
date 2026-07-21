# Investigation: Refactoring Analysis — Verified Findings & Fix Plan

## Summary
逐一验证了 28 项重构发现。确认 **3 项真实 Bug**、**7 项有效重复**、**5 项死代码**、**4 项结构性问题**。调整了部分严重级别。以下是经验证的修复规划，按危险等级和施工顺序排列。

---

## 一、验证结论总表

| ID | 问题 | 真实? | 级别调整 | 危险等级 | 爆炸范围 |
|----|------|-------|----------|----------|----------|
| **C1** | CSS @media (640px) 提前关闭，~17 个选择器无条件生效 | ✅ 真实 Bug | P0 ✅ 正确 | 🟡 CAUTIOUS | portal.css |
| **C2** | `.source-mixed` CSS 类缺失 | ✅ 真实 | P0→**P1** | 🟢 SAFE | portal.css |
| **P14** | `kimi_prob` 近似 vs 精确 | ✅ 真实 | P0→**P2** | 🟢 SAFE | patch_section9.py |
| **H1** | teams.html 无 topbar | ✅ 真实 | P0→**P1** | 🟢 SAFE | teams.html |
| **P1** | 信号计算精确复制 | ✅ 精确复制 | P1 ✅ | 🟢 SAFE | 2 scripts + 新模块 |
| **P2** | §9 生成近乎一致 | ✅ 近似复制 | P1 ✅ | 🟢 SAFE | 2 scripts + 新模块 |
| **P3** | group_kimi_by_team 一致逻辑 | ✅ 精确复制 | P1 ✅ | 🟢 SAFE | 2 scripts + 新模块 |
| **P5** | 三种 slug 实现 | ⚠️ 部分真实 | P1→**P2** | 🟢 SAFE | 3 scripts + 新模块 |
| **F1** | escapeHtml/escapeAttr 复制 | ✅ 精确复制 | P1 ✅ | 🟢 SAFE | 3 JS + 新 common.js |
| **F2** | sourceClass() 复制 | ✅ 精确复制 | P1 ✅ | 🟢 SAFE | 2 JS + 新 common.js |
| **F3** | 柱状图渲染复制 | ✅ 逻辑相同 | P1 ✅ | 🟡 CAUTIOUS | 3 JS + portal.css |
| **C5** | 卡片外观声明重复 ~9 次 | ✅ 真实 | P1→**P2** | 🟢 SAFE | portal.css |
| **P9** | import os 未使用 | ✅ 真实 | P2 ✅ | 🟢 SAFE | 2 scripts |
| **P13** | meta.json 孤立文件 | ✅ 真实 | P2 ✅ | 🟢 SAFE | build_site_data.py |
| **P8** | 测试常量复制 | ✅ 真实 | P2 ✅ | 🟢 SAFE | test_build_site_data.py |
| **C3** | ~15 未使用 CSS 选择器 | ✅ 真实 | P2 ✅ | 🟢 SAFE | portal.css |
| **C4** | 未使用 CSS 变量 | ✅ 真实 | P2 ✅ | 🟢 SAFE | portal.css |
| **H2** | 脚本加载模式不一致 | ✅ 真实 | P2→**P3** | 🟢 SAFE | teams.html |
| **B1** | Makefile results 不运行构建 | ✅ 真实 | P2 ✅ | 🟢 SAFE | Makefile |
| **P12** | 无共享工具模块 | ✅ 真实 | P3 ✅ | 🟢 SAFE | src/utils/ 新建 |
| **P11** | sys.path hack | ✅ 真实 | P3 ✅ | 🟢 SAFE | audit_path_cards.py |

---

## 二、逐项根因与证据

### C1 — CSS @media 提前关闭 ⚡ 真实 Bug
**根因**：commit `253f02f8`（"Add AI perspectives"，Jun 12 01:41）替换了 `@media (max-width: 900px)` 的内容，但将原本在该块内的响应式规则移到了 `@media (max-width: 640px)` 之后，成为无条件规则。
**证据**：
- `portal.css` L1321-1334: `@media (max-width: 900px)` — 只有 AI perspective 的新规则
- `portal.css` L1336-1349: `@media (max-width: 640px)` #1 — AI perspective 的 640px 规则
- `portal.css` L1351-1378: **17 个选择器无条件生效**（原本在 900px 块内）
- `portal.css` L1379: 多余的 `}`
- `portal.css` L1381-1443: `@media (max-width: 640px)` #2 — 原始移动端规则
**影响**：`.hero, .control-panel, .chart-grid` 等桌面端多列布局被强制为单列。

### C2 — `.source-mixed` CSS 缺失
**根因**：`sourceClass()` 函数返回 `"source-mixed"` 作为默认值，但 CSS 中从未定义该类。
**证据**：`file_search("source-mixed")` 在 portal.css 中零匹配；homepage.js:383 和 team-detail.js:277 各一处。
**级别调整**：P0→P1 — 标签仍有文字内容，只是无特殊背景色。不是致命 bug。

### P14 — kimi_prob 计算分歧
**根因**：`generate_path_cards.py` 从聚合 JSON 读取精确概率（`team_agg.get("probability", "N/A")`），而 `patch_section9.py` 因无法访问聚合 JSON 而用 `len(kimi_agents)/300*100` 近似。代码注释明确标注"简单近似"。
**证据**：generate_path_cards.py:79 vs patch_section9.py:131。
**级别调整**：P0→P2 — 这是已知的有意折衷，不是意外 bug。

### H1 — teams.html 缺少 topbar
**根因**：teams.html 设计为独立页面，用"返回研究门户"按钮替代 topbar。
**证据**：teams.html 全文 55 行，无 `<header>` 元素。
**级别调整**：P0→P1 — 有替代导航方式，但用户体验不一致。

### P1 — 信号计算精确复制
**根因**：patch_section9.py 创建时复制粘贴了 generate_path_cards.py 的信号逻辑。
**证据**：generate_path_cards.py:94-101 ≡ patch_section9.py:88-103（相同阈值、相同信号名）。

### P3 — group_kimi_by_team 一致逻辑
**根因**：同上，复制粘贴。
**证据**：generate_path_cards.py:44-50 ≡ patch_section9.py:30-38（函数体完全一致，仅函数名不同）。

### P5 — Slug 实现 — ⚠️ 部分真实
**根因**：generate_path_cards.py 和 patch_section9.py 使用**完全相同**的内联 slug 逻辑（`team["canonical_team"].lower().replace(" ", "-").replace("'", "")`）。fetch_market_snapshot.py 有不同实现是因为它处理 Polymarket 问题字符串而非 CSV 队名。
**级别调整**：P1→P2 — 两个主要脚本实际用相同逻辑，第三个有合理理由不同。

### F1 — escapeHtml/escapeAttr 精确复制
**证据**：homepage.js:416-425 ≡ team-detail.js:280-290（逐字一致，都用 `??`）。teams.js:126-138 也一致但用 `||`。

---

## 三、修复规划（按施工顺序）

### 🔧 第一批：修 Bug（安全、高影响、单文件）

#### Step 1: 修复 C1 — CSS @media 断裂
- **文件**：`site/css/portal.css`
- **操作**：将 L1351-1378 的 4 个规则块合并到 `@media (max-width: 900px)` 块（L1321-1334）内；删除 L1379 的多余 `}`
- **危险等级**：🟡 CAUTIOUS — 改变布局行为，需视觉测试
- **验证**：桌面端应恢复多列布局；移动端（<900px）应保持单列
- **最小步骤**：
  1. 剪切 L1351-1378
  2. 粘贴到 L1334 `}` 之前
  3. 删除 L1379 的多余 `}`
  4. 浏览器测试：桌面 / 平板 / 手机三个宽度

#### Step 2: 修复 C2 — 添加 .source-mixed CSS
- **文件**：`site/css/portal.css`
- **操作**：在 `.source-red` 规则后添加 `.source-mixed` 样式
- **危险等级**：🟢 SAFE — 纯添加，不影响已有样式
- **最小步骤**：
  1. 在 `.source-red` 定义后添加：`.source-mixed { background: #f0efe8; color: var(--muted); }`
  2. 浏览器验证标签样式

#### Step 3: 修复 H1 — teams.html 添加 topbar
- **文件**：`site/teams.html`
- **操作**：添加与 index.html 一致的 topbar HTML
- **危险等级**：🟢 SAFE — 纯 HTML 添加
- **最小步骤**：
  1. 在 `<body>` 后、`<main>` 前插入 topbar HTML
  2. 同时修复 H2：统一脚本加载方式（使用 defer）

### 🔧 第二批：清除死代码（零风险）

#### Step 4: 删除未使用 import
- **文件**：`scripts/build_site_data.py`（删 `import os`）、`scripts/generate_path_cards.py`（删 `import os`）
- **危险等级**：🟢 SAFE
- **验证**：`python3 scripts/build_site_data.py` 正常运行

#### Step 5: 移除 meta.json 输出
- **文件**：`scripts/build_site_data.py`（删除 meta.json 输出行）、`site/data/meta.json`（删除文件）
- **危险等级**：🟢 SAFE — 确认无引用后删除

#### Step 6: 清理未使用 CSS
- **文件**：`site/css/portal.css`
- **操作**：删除 `.panel-grid`, `.panel h3`, `.panel p`, `.status-rail`, `.status-item`, `.status-track`, `.status-fill`, `.status-fill.hold`, `.update-contract`, `.update-steps`, `.page-content`, `.wrapper`；删除 `--pitch` 和 `--grass` 变量
- **危险等级**：🟢 SAFE — 已确认无引用
- **验证**：三页浏览器回归测试

### 🔧 第三批：提取 Python 共享模块

#### Step 7: 创建 src/utils/ 并提取共享函数
- **新建**：`src/__init__.py`、`src/utils/__init__.py`
- **新建**：`src/utils/kimi.py` — 提取 `compute_signals()`, `group_kimi_by_team()`, `build_section_9()`, `slugify()`, `load_csv()`
- **修改**：`scripts/generate_path_cards.py` — 导入共享函数，删除本地副本
- **修改**：`scripts/patch_section9.py` — 导入共享函数，删除本地副本，修正 P14 kimi_prob 使用聚合数据
- **修改**：`scripts/audit_path_cards.py` — 替换 sys.path hack 为正规 `src.utils` 导入
- **危险等级**：🟡 CAUTIOUS — 需确保导入路径正确，CI 测试通过
- **验证**：`python3 scripts/generate_path_cards.py --dry-run` + CI unittest

### 🔧 第四批：提取前端共享模块

#### Step 8: 创建 site/js/common.js
- **新建**：`site/js/common.js` — 包含 `escapeHtml()`, `escapeAttr()`, `sourceClass()`, `loadCdsData()`
- **修改**：`site/js/homepage.js` — 删除本地副本，改为引用 common.js
- **修改**：`site/js/team-detail.js` — 同上
- **修改**：`site/js/teams.js` — 同上，统一 `??` vs `||`
- **修改**：`site/index.html`、`site/team.html`、`site/teams.html` — 添加 `<script src="js/common.js">`
- **危险等级**：🟢 SAFE — 纯重构，不改变行为
- **验证**：三页浏览器回归测试

#### Step 9: 统一柱状图渲染（可选，F3）
- **新建**：`site/js/common.js` 中添加 `renderBarChart(container, items, cssPrefix)`
- **修改**：homepage.js、team-detail.js — 替换 3 个渲染函数为统一调用
- **危险等级**：🟡 CAUTIOUS — 涉及 CSS 类名变更
- **验证**：三页柱状图视觉回归

### 🔧 第五批：构建流水线

#### Step 10: 修复 Makefile results 目标
- **文件**：`Makefile`
- **操作**：`results` 目标先运行 `python3 scripts/build_site_data.py`
- **危险等级**：🟢 SAFE — 补全缺失步骤

#### Step 11: 删除 slugToTeamName 硬编码（可选）
- **文件**：`site/js/homepage.js`
- **操作**：从 teams.json 数据派生，删除 L390-413 硬编码映射
- **危险等级**：🟢 SAFE

---

## 四、不建议现在做的事

| 项 | 原因 |
|----|------|
| 拆分 build_site_data.py 1340 行巨石 | 侵入性高，风险大，暂不影响功能 |
| 删除双格式数据（.json + .js） | file:// 兼容性是设计决策，需确认是否仍需 |
| 添加 7 个缺失测试 | 重要但独立于重构，应作为单独 spec |
| 统一 argparse/类型提示/文档语言 | 风格统一有价值但不紧急 |

---

## 五、建议施工分组

可以合并为 **3 个 PR**：

1. **PR-A（Bug 修复）**：Step 1-3 — CSS 修复 + 缺失样式 + teams.html topbar
2. **PR-B（清理）**：Step 4-6 — 死代码 + 未使用 CSS + meta.json
3. **PR-C（重构）**：Step 7-11 — Python 共享模块 + 前端 common.js + Makefile

每个 PR 都应：CI 通过 + 浏览器三页回归测试。
