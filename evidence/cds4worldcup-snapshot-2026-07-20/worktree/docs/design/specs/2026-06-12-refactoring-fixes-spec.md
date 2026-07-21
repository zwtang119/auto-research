# Spec: 重构修复 — 经验证的问题清单与施工计划

> **日期**: 2026-06-12
> **状态**: 待审批
> **调查报告**: `docs/investigations/refactoring-verification-2026-06-12.md`
> **原则**: 最小步骤、保留行为、由安全到风险递进

---

## 背景

对项目代码进行全面扫描后，识别出 28 个潜在问题。经逐行验证和 Git 考古：

- **1 个真实 P0 Bug**（C1 CSS 媒体查询断裂，桌面端布局被破坏）
- **2 个 P1 问题**（C2 缺失 CSS 类、H1 缺少导航）
- **7 个代码重复**（Python ~80 行 + 前端 ~30 行可消除）
- **5 个死代码/清理项**
- **4 项级别下调**（P14、P5 从报告的原始级别降低）
- **3 项不建议修复**（有意设计或风险大于收益）

## 级别调整说明

| ID | 原始 | 调整后 | 原因 |
|----|------|--------|------|
| C2 | P0 | **P1** | 标签仍有文字内容，只是无特殊背景色；当前数据中 fallback 极少触发 |
| P14 | P0 | **P2** | patch_section9.py 注释明确标注"简单近似"，是有意妥协 |
| H1 | P0 | **P1** | 有"返回研究门户"按钮，不是完全无导航 |
| P5 | P1 | **P2** | 只有 2 种 slug（非 3 种），fetch_market_snapshot 处理不同输入 |

## 不在本 Spec 范围

- 拆分 build_site_data.py（1340 行巨石，侵入性高）
- 删除双格式数据 .json + .js（file:// 兼容性是有意设计）
- 添加 7 个缺失测试（独立 spec）
- 统一 argparse / 类型提示 / 文档语言风格
- 修复 P14 kimi_prob 近似（有意妥协，需架构变更）

---

## 任务清单

### Batch A：Bug 修复（建议 1 个 PR）

---

#### Task A1: 修复 CSS @media (max-width: 640px) 提前关闭

| 属性 | 值 |
|------|-----|
| **ID** | C1 |
| **危险等级** | 🟡 CAUTIOUS |
| **爆炸范围** | `site/css/portal.css` 1 个文件 |
| **根因** | commit `253f02f8`（"Add AI perspectives"）替换了 `@media (max-width:900px)` 内容，导致 L1351-1378 的 17 个响应式选择器成为无条件规则，L1379 出现孤立 `}` |
| **用户影响** | 桌面端 `.hero`, `.control-panel`, `.chart-grid`, `.team-grid` 等多列布局被强制为单列 |

**最小步骤**:
1. 剪切 `portal.css` L1351-1378（4 个规则块）
2. 粘贴到 `@media (max-width: 900px)` 块内（L1333 `}` 之前）
3. 删除 L1379 的多余 `}`

**验证**:
- [ ] 浏览器打开 `index.html`，桌面宽度 (>1200px)：hero 应为双列，不是单列
- [ ] 缩小到 900px 以下：布局应变为单列
- [ ] 缩小到 640px 以下：topbar 应折叠
- [ ] `teams.html` 和 `team.html` 同样测试

**不改动的**:
- `@media (max-width: 640px)` #1（L1336-1349，AI perspective 规则）
- `@media (max-width: 640px)` #2（L1381-1443，原始移动端规则）

---

#### Task A2: 添加 .source-mixed CSS 类

| 属性 | 值 |
|------|-----|
| **ID** | C2 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `site/css/portal.css` 1 个文件 |
| **根因** | `sourceClass()` 函数返回 `"source-mixed"` 作为默认值（homepage.js:383, team-detail.js:277），但 CSS 中从未定义该类 |

**最小步骤**:
1. 在 `.source-red` 规则定义之后添加：
   ```css
   .source-mixed {
     background: #ede8dd;
     color: var(--muted);
   }
   ```
   （样式参考现有 `.source-green`/`.source-yellow`/`.source-red` 的 badge 模式）

**验证**:
- [ ] 搜索确认 portal.css 中新增了 `.source-mixed` 规则
- [ ] 浏览器中首页和球队详情页的来源标签显示正常

---

#### Task A3: 为 teams.html 添加 topbar 导航

| 属性 | 值 |
|------|-----|
| **ID** | H1 + H2 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `site/teams.html` 1 个文件 |
| **根因** | teams.html 创建时没有 topbar，仅有一个文字链接"返回研究门户" |

**最小步骤**:
1. 在 `<body>` 后、`<main>` 前添加 topbar HTML（参考 index.html L11-20 的结构）
2. 同时修复 H2：将 `<script src="js/teams.js"></script>` 移至 `<head>` 并添加 `defer`（与 index.html/team.html 统一）

**验证**:
- [ ] teams.html 显示与其他两个页面一致的顶部导航栏
- [ ] 导航链接（首页、球队总览）可正常跳转
- [ ] 脚本加载方式与 index.html 一致

---

### Batch B：死代码清理（建议 1 个 PR）

---

#### Task B1: 删除未使用的 Python import

| 属性 | 值 |
|------|-----|
| **ID** | P9 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | 2 个 Python 文件 |

**最小步骤**:
1. 删除 `scripts/build_site_data.py:11` 的 `import os`
2. 删除 `scripts/generate_path_cards.py` 的 `import os`

**验证**:
- [ ] `python3 scripts/build_site_data.py` 正常运行
- [ ] `python3 -m unittest` 全部通过

---

#### Task B2: 移除 meta.json 孤立输出

| 属性 | 值 |
|------|-----|
| **ID** | P13 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `scripts/build_site_data.py`（删除输出代码）、`site/data/meta.json`（删除文件） |

**最小步骤**:
1. 在 `scripts/build_site_data.py` 中找到输出 `meta.json` 的代码（约 2-3 行），删除
2. 删除 `site/data/meta.json`

**验证**:
- [ ] `python3 scripts/build_site_data.py` 运行后不再生成 `site/data/meta.json`
- [ ] 搜索确认无 HTML/JS 文件引用 `meta.json`

---

#### Task B3: 清理未使用的 CSS 选择器和变量

| 属性 | 值 |
|------|-----|
| **ID** | C3 + C4 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `site/css/portal.css` 1 个文件 |

**最小步骤**:
1. 删除以下未使用的 CSS 规则（经搜索确认无 HTML/JS 引用）：
   - `.page-content`
   - `.wrapper`
   - `.panel-grid`, `.panel h3`, `.panel p`
   - `.status-rail`, `.status-item`, `.status-track`, `.status-fill`, `.status-fill.hold`
   - `.update-contract`, `.update-steps`
2. 删除 `:root` 中未使用的 CSS 变量：`--pitch`, `--grass`

**验证**:
- [ ] 三页面（index/teams/team）视觉无变化
- [ ] 浏览器开发工具中无新增 404 或样式错误

---

#### Task B4: 提取重复的 CSS card-chrome 声明块

| 属性 | 值 |
|------|-----|
| **ID** | C5 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `site/css/portal.css` 1 个文件 |

**最小步骤**:
1. 在 CSS 中创建 `.card-chrome` 共享类：
   ```css
   .card-chrome {
     background: rgba(255, 253, 248, 0.92);
     border: 1px solid var(--line);
     box-shadow: 0 10px 24px rgba(47, 42, 35, 0.07);
   }
   ```
2. 在受影响的选择器（`.team-card`, `.control-panel`, `.team-teaser-card`, `.snapshot-card`, `.team-quick-panel`, `.detail-main-card`, `.reference-card`, `.analysis-card`, `.chart-card`, `.detail-panel`）中添加 `card-chrome` 类名
3. 从各选择器中删除重复的 background/border/box-shadow 声明

**注意**: 此任务涉及 HTML 文件中对应元素添加 `class="card-chrome"`，需确认哪些 HTML 需要修改。

**验证**:
- [ ] 三页面卡片外观（白底、边框、阴影）无视觉变化

---

#### Task B5: 修复测试文件中的常量复制

| 属性 | 值 |
|------|-----|
| **ID** | P8 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `tests/test_build_site_data.py` 1 个文件 |

**最小步骤**:
1. 修改 `tests/test_build_site_data.py`，从 `scripts/build_site_data.py` 导入 `PUBLIC_VENDOR_FORBIDDEN` 和 `PUBLIC_BETTING_FORBIDDEN`
2. 删除文件中独立定义的相同常量

**验证**:
- [ ] `python3 -m unittest tests/test_build_site_data.py` 通过

---

### Batch C：代码去重（建议 1 个 PR，可拆分为 2）

---

#### Task C1: 创建 Python 共享工具模块

| 属性 | 值 |
|------|-----|
| **ID** | P1 + P2 + P3 + P4 + P5 + P11 |
| **危险等级** | 🟡 CAUTIOUS |
| **爆炸范围** | 新建 `src/utils/` + 修改 3 个脚本 |

**最小步骤**:
1. 创建 `src/__init__.py`（空文件）
2. 创建 `src/utils/__init__.py`（空文件）
3. 创建 `src/utils/slug.py`：
   ```python
   def slugify(team_name: str) -> str:
       return team_name.lower().replace(" ", "-").replace("'", "")
   ```
4. 创建 `src/utils/csv_helpers.py`：
   ```python
   def load_csv(path) -> list[dict]:
       import csv
       with open(path, encoding="utf-8") as f:
           return list(csv.DictReader(f))
   ```
5. 创建 `src/utils/kimi.py`：
   - `group_kimi_by_team(agents)` — 从 generate_path_cards.py:44-50 提取
   - `compute_signals(team, kimi_agents, kimi_prob)` — 从 patch_section9.py:86-103 提取
   - `build_section_9(kimi_agents, kimi_prob, today)` — 从 patch_section9.py:41-66 提取
6. 修改 `scripts/generate_path_cards.py`：
   - 删除本地 `group_kimi_by_team()`, 内联信号计算, 内联 slug 逻辑
   - 替换为 `from src.utils.kimi import ...`, `from src.utils.slug import slugify`
7. 修改 `scripts/patch_section9.py`：
   - 删除本地 `load_csv()`, `group_kimi_by_team_zh()`, `compute_signals()`, `build_section_9()`, 内联 slug
   - 替换为从 `src.utils` 导入
   - 预期删除 ~80 行
8. 修改 `scripts/audit_path_cards.py`：
   - 删除 `sys.path.insert(0, str(ROOT / "scripts"))` hack
   - 替换为从 `src.utils` 导入 `load_csv`

**验证**:
- [ ] `python3 scripts/build_site_data.py` 输出不变（对比 git diff site/data/*.json）
- [ ] `python3 -m unittest` 全部通过
- [ ] `make check` 通过

**不改动的**:
- `scripts/fetch_market_snapshot.py` 的 `slugify()` — 处理不同输入（API 问题字符串），保持独立
- 任何 `src/analysis/` 或 `src/factor_ledger/` 下的文件

---

#### Task C2: 提取前端 common.js

| 属性 | 值 |
|------|-----|
| **ID** | F1 + F2 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | 新建 `site/js/common.js` + 修改 3 个 JS + 3 个 HTML |

**最小步骤**:
1. 创建 `site/js/common.js`：
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
2. 在 3 个 HTML 文件的 `<head>` 中（data.js 之后）添加：
   ```html
   <script src="js/common.js"></script>
   ```
3. 从 `site/js/homepage.js` 删除 `escapeHtml()`, `escapeAttr()`, `sourceClass()` 的本地副本
4. 从 `site/js/team-detail.js` 删除同样 3 个函数的本地副本
5. 从 `site/js/teams.js` 删除 `escapeHtml()`, `escapeAttr()` 的本地副本，同时修复 `||` → `??` 不一致

**验证**:
- [ ] 三页面加载无 JS 错误
- [ ] 首页球队卡片内容正常显示（escapeHtml 工作正常）
- [ ] 球队详情页来源标签颜色正确（sourceClass 工作正常）
- [ ] 搜索页面（teams.html）筛选功能正常

---

### Batch D：构建流水线（可与 Batch B 合并）

---

#### Task D1: 修复 Makefile results 目标

| 属性 | 值 |
|------|-----|
| **ID** | B1 |
| **危险等级** | 🟢 SAFE |
| **爆炸范围** | `Makefile` 1 个文件 |

**最小步骤**:
1. 在 `results` 目标的 `@rm -rf _publish` 之前添加：
   ```makefile
   python3 scripts/build_site_data.py
   ```

**验证**:
- [ ] `make results` 后 `_publish/data/teams.json` 包含最新构建数据

---

## 施工顺序

```
Batch A (Bug 修复)     ← 最高优先
  A1 → A2 → A3
    ↓
Batch B (死代码清理)   ← 零风险
  B1 → B2 → B3 → B4 → B5（任意顺序）
    ↓
Batch C (代码去重)     ← 需要测试
  C1 (Python) → C2 (前端)
    ↓
Batch D (构建流水线)   ← 可与 B 合并
  D1
```

## PR 分组建议

| PR | 内容 | Tasks | 风险 |
|----|------|-------|------|
| **PR-1** | Bug 修复 | A1, A2, A3 | 🟡 低 |
| **PR-2** | 清理 + 流水线 | B1-B5, D1 | 🟢 极低 |
| **PR-3** | 代码去重 | C1, C2 | 🟡 中 |

每个 PR 的验收标准：
- [ ] `make check` 通过
- [ ] `python3 -m unittest` 通过
- [ ] 浏览器三页面（index/teams/team）回归测试通过

## 总工作量估计

| Batch | 改动文件数 | 新建文件 | 预计净增/删行数 |
|-------|-----------|---------|---------------|
| A | 3 | 0 | ~+20 / -0 |
| B | 4 | 0 | ~+5 / -80 |
| C | 9 | 4 | ~+60 / -120 |
| D | 1 | 0 | ~+1 / -0 |
| **合计** | **17** | **4** | **~+86 / -200** |
