# Spec: 代码重构与 Bug 修复

> **日期**: 2026-06-12
> **状态**: 待审阅
> **来源**: docs/investigations/refactoring-verification-2026-06-12.md
> **关联 spec**: 2026-06-12-public-site-ai-market-upgrade-spec.md

## 目标

基于深度验证的代码审计结果，分三批修复 1 个真实 Bug（C1）、2 个缺失（C2/H1）、~80 行 Python 重复代码、~30 行 JS 重复代码、以及若干死代码。**不改变任何功能行为**，除非是修复已确认的 Bug。

## 范围

### 在范围内
- `site/css/portal.css` — 修媒体查询、补缺失样式、清死 CSS
- `site/teams.html` — 补 topbar
- `scripts/generate_path_cards.py` — 删死 import、改用共享模块
- `scripts/patch_section9.py` — 删重复代码、改用共享模块
- `scripts/audit_path_cards.py` — 去 sys.path hack
- `scripts/build_site_data.py` — 删死 import、删 meta.json 输出
- `src/analysis/group_difficulty.py` — 删死 import
- `src/utils/` — 新建共享模块
- `site/js/common.js` — 新建前端共享工具
- `site/js/*.js` — 删除重复工具函数
- `site/*.html` — 添加 common.js 引用
- `Makefile` — 修 results 目标
- `tests/test_build_site_data.py` — 导入常量替代复制

### 不在范围
- `scripts/build_site_data.py` 拆分（1340 行巨石，侵入性高，暂不动）
- 双格式数据 `.json` + `.js`（file:// 兼容性是设计决策）
- P14 kimi_prob 近似（有意妥协，非 bug）
- 新增测试覆盖（应独立做 spec）
- `site/js/homepage.js` slugToTeamName 去重（可选，非必须）
- 柱状图渲染统一（F3，可选，风险较高）

---

## 任务清单

### Batch 1: Bug 修复（PR-A）

#### Task 1.1: 修复 CSS @media 断裂 [P0] 🟡 CAUTIOUS

**问题**: `portal.css` L1351-1378 的 17 个响应式选择器在两个 `@media (max-width: 640px)` 块之间无条件生效，导致桌面端多列布局被强制为单列。

**根因**: commit `253f02f8`（"Add AI perspectives"）替换了 `@media (max-width: 900px)` 的内容，但将原 900px 块内的规则移出了媒体查询。

**修复**:
1. 将 L1351-1378（4 个规则块）剪切到 `@media (max-width: 900px)` 块（L1321-1334）内
2. 删除 L1379 的孤立 `}`

**验证**: 浏览器测试桌面（>900px）、平板（640-900px）、手机（<640px）三种宽度布局。

**文件**: `site/css/portal.css`

---

#### Task 1.2: 补 .source-mixed CSS 类 [P1] 🟢 SAFE

**问题**: `sourceClass()` 返回 `"source-mixed"` 作为默认值（homepage.js:383, team-detail.js:277），但 `portal.css` 中从未定义该类。

**修复**: 在 `.source-red` 规则后添加:
```css
.source-mixed {
  background: #f0ede6;
  color: var(--muted);
  border-radius: 4px;
  padding: 2px 8px;
  font-size: 0.78rem;
}
```

**验证**: 检查来源标签在所有页面正常显示。

**文件**: `site/css/portal.css`

---

#### Task 1.3: 补 teams.html topbar [P1] 🟢 SAFE

**问题**: `teams.html` 无 `<header class="topbar">` 导航，与 index.html 和 team.html 不一致。

**修复**:
1. 在 `<body>` 后、`<main>` 前插入与 `index.html` 一致的 topbar HTML
2. 同时统一脚本加载方式：`teams.js` 改为 `defer` 加载（与另两个页面一致）

**验证**: 三页面导航栏一致，teams 页面筛选和加载功能正常。

**文件**: `site/teams.html`

---

### Batch 2: 死代码清理（PR-B）

#### Task 2.1: 删除未使用 import [P2] 🟢 SAFE

**修复**:
- `scripts/build_site_data.py:11` — 删除 `import os`
- `scripts/generate_path_cards.py` — 删除 `import os`
- `src/analysis/group_difficulty.py` — 删除 `from collections import defaultdict`

**验证**: `python3 scripts/build_site_data.py` 正常运行；CI 测试通过。

---

#### Task 2.2: 移除 meta.json 孤立输出 [P2] 🟢 SAFE

**问题**: `build_site_data.py` 输出 `site/data/meta.json`，但无任何 HTML/JS 文件引用它。

**修复**:
1. 在 `build_site_data.py` 中删除输出 `meta.json` 的代码（约 2 行）
2. 删除 `site/data/meta.json`

**验证**: `make check` 通过；站点三页面加载正常。

---

#### Task 2.3: 清理未使用 CSS [P2] 🟢 SAFE

**修复**: 从 `portal.css` 删除以下已确认无引用的规则:
- `.page-content`、`.wrapper`
- `.panel-grid`、`.panel h3`、`.panel p`
- `.status-rail`、`.status-item`、`.status-track`、`.status-fill`、`.status-fill.hold`
- `.update-contract`、`.update-steps`
- `:root` 中的 `--pitch` 和 `--grass` 变量

**验证**: 浏览器三页面视觉回归测试（布局无变化）。

---

#### Task 2.4: 测试常量导入替代复制 [P2] 🟢 SAFE

**问题**: `tests/test_build_site_data.py` 独立定义了 `PUBLIC_VENDOR_FORBIDDEN` 和 `PUBLIC_BETTING_FORBIDDEN`，与 `build_site_data.py` 中的定义重复。

**修复**: 在测试文件中从 `build_site_data` 导入这两个常量，删除本地副本。

---

### Batch 3: 代码重构（PR-C）

#### Task 3.1: 创建 Python 共享模块 [P1] 🟡 CAUTIOUS

**问题**: `generate_path_cards.py` 和 `patch_section9.py` 之间有 ~80 行精确复制的代码（信号计算、§9 生成、分组逻辑、slug 生成、CSV 加载）。

**修复**:
1. 创建 `src/__init__.py` 和 `src/utils/__init__.py`
2. 创建 `src/utils/slug.py`:
   ```python
   def slugify(team_name: str) -> str:
       """Canonical slug: lowercase, hyphens for spaces, strip apostrophes."""
       return team_name.lower().replace(" ", "-").replace("'", "")
   ```
3. 创建 `src/utils/kimi.py`:
   - `load_csv(path)` — 从 `patch_section9.py` 提取
   - `group_kimi_by_team(agents)` — 统一两个同名函数
   - `compute_signals(team, kimi_agents, kimi_prob)` — 从任一文件提取
   - `build_section_9(kimi_agents, kimi_prob, date_str)` — 从 `patch_section9.py` 提取
4. 更新 `scripts/generate_path_cards.py`:
   - 删除内联 slug 逻辑（L69），改为 `from src.utils.slug import slugify`
   - 删除内联信号计算（L94-101），改为 `from src.utils.kimi import compute_signals`
   - 删除 `group_kimi_by_team`（L44-50），改为 `from src.utils.kimi import group_kimi_by_team`
5. 更新 `scripts/patch_section9.py`:
   - 删除 `load_csv`（L25-27）、`group_kimi_by_team_zh`（L30-38）、`build_section_9`（L41-66）、`compute_signals`（L86-103）
   - 改为从 `src.utils` 导入
   - 删除内联 slug 逻辑（L122）
6. 更新 `scripts/audit_path_cards.py`:
   - 删除 `sys.path.insert(0, ...)` hack（L12）
   - 改为从 `src.utils` 导入 `load_csv`

**验证**: `python3 scripts/generate_path_cards.py` 生成相同卡片；`make check` 通过。

**注意**: 这是最高风险步骤。导入路径需要正确设置（`scripts/` 文件需要能找到 `src/utils/`）。建议用 `sys.path` 或 `PYTHONPATH` 或 `__main__.py` 方式处理。

---

#### Task 3.2: 创建前端 common.js [P1] 🟢 SAFE

**问题**: `escapeHtml`、`escapeAttr`、`sourceClass` 在 3 个 JS 文件中逐字复制。

**修复**:
1. 创建 `site/js/common.js`:
   ```javascript
   function escapeHtml(value) {
     return String(value ?? "")
       .replace(/&/g, "&amp;")
       .replace(/</g, "&lt;")
       .replace(/>/g, "&gt;")
       .replace(/"/g, "&quot;")
       .replace(/'/g, "&#039;");
   }
   function escapeAttr(value) {
     return escapeHtml(value).replace(/`/g, "&#096;");
   }
   function sourceClass(label) {
     if (label === "可靠事实") return "source-green";
     if (label === "待核验线索") return "source-yellow";
     if (label === "只能参考") return "source-red";
     return "source-mixed";
   }
   ```
2. 在 3 个 HTML 文件的 `<head>` 中添加:
   ```html
   <script src="js/common.js"></script>
   ```
3. 从 `homepage.js`、`teams.js`、`team-detail.js` 中删除这 3 个函数的本地副本
4. 修复 `teams.js` 中 `||` → `??` 的不一致

**验证**: 三页面功能正常（来源标签、错误提示、特殊字符显示）。

---

#### Task 3.3: 修复 Makefile results 目标 [P2] 🟢 SAFE

**问题**: `results` 目标只复制 `site/` 到 `_publish/`，不运行 `build_site_data.py`，可能发布过时数据。

**修复**: 在 `results` 目标的 cp 之前添加:
```makefile
	python3 scripts/build_site_data.py
```

**验证**: `make results` 后检查 `_publish/data/teams.json` 包含最新数据。

---

## 执行约束

1. **每个 Batch 为独立 PR**，PR 之间无依赖
2. **每个 Task 内不混做其他 Task 的修改**
3. **Batch 3（重构）依赖 Batch 1 通过视觉测试** — 确保重构前站点行为正确
4. **CI 必须通过**: `make check` + `python3 -m unittest tests/`
5. **不做范围外的事**: 不拆巨石、不加测试、不改 kimi_prob
6. **视觉回归**: 每个 Batch 合并前需在三页面浏览器检查

## 施工顺序

```
Batch 1 (Bug 修复)
  ├── Task 1.1  ← 最高优先，唯一真实 P0
  ├── Task 1.2
  └── Task 1.3
  → 视觉验证通过后 →
Batch 2 (死代码清理)
  ├── Task 2.1
  ├── Task 2.2
  ├── Task 2.3
  └── Task 2.4
  → CI 通过后 →
Batch 3 (代码重构)
  ├── Task 3.1  ← 最高风险，需仔细测试
  ├── Task 3.2
  └── Task 3.3
```

## 风险与回退

| 风险 | 可能性 | 影响 | 回退策略 |
|------|--------|------|----------|
| Task 1.1 修后布局异常 | 低 | 高 | Git revert 该 commit，手动调整 CSS |
| Task 3.1 导入路径错误 | 中 | 中 | 回退到原始内联代码 |
| Task 3.2 common.js 加载顺序问题 | 低 | 低 | 调整 script 标签顺序 |
| 删除 CSS 后发现某选择器实际被用 | 低 | 低 | Git revert 恢复该规则 |

## 完成标准

- [ ] C1: 桌面端恢复多列布局，手机端保持单列
- [ ] C2: .source-mixed 标签有背景色
- [ ] H1: teams.html 有与 index.html 一致的 topbar
- [ ] 死 import 全部删除，CI 绿灯
- [ ] meta.json 已删除，站点不受影响
- [ ] Python 共享模块创建，generate_path_cards + patch_section9 各减 ~40 行
- [ ] common.js 创建，3 个 JS 文件各减 ~10 行
- [ ] Makefile results 目标先构建再复制
- [ ] 全部测试通过，三页面视觉正常
