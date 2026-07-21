# Investigation: Phase 0-2 代码质量问题深度分析

> **日期**: 2026-06-12
> **范围**: `checkpoint-pre-upgrade-2026-06-12` → HEAD（90 files，+12,569 -1,353）
> **方法**: context_builder 8 维度扫描 + 文件级验证

## Summary

发现 **12 个问题**（含 5 个 Code Review 已知 + 7 个新发现），其中 **P0 有 2 个**（teams.js XSS、Elo 来源等级错误），**P1 有 4 个**（CODE_MAP 四重复制、assert 生产路径、CI [skip ci] 失效、Elo 零区分度），**P2 有 6 个**（CSS 单文件膨胀、var/const 风格不一致、无渐进增强、JSON 校验缺失、FIFA baseline 均匀、Polymarket 名称暴露）。

---

## 问题清单与评级

### P0 — 必须立即修复

#### Issue 1: teams.js XSS — flag 未转义
- **文件**: `site/js/teams.js:90`
- **症状**: `${team.flag}` 直接注入 innerHTML，未经 `escapeHtml()` 转义
- **根因**: flag 是 emoji 字符串（如 `"🇪🇸"`），开发者认为 emoji 不需要转义。但如果数据源被污染（JSON 文件含恶意内容），可注入任意 HTML
- **爆炸半径**: teams.html 球队列表页 — 48 个球队卡片全部受影响
- **对比**: `homepage.js:89`、`team-detail.js:319` 均正确使用 `escapeHtml(team.flag)`
- **修复**: 改为 `${escapeHtml(team.flag)}`（1 行修复）
- **严重度**: 🔴 P0 — 虽然当前数据安全（emoji flag），但违反项目安全规范，且是唯一未转义的注入点

#### Issue 2: Elo proxy 来源等级错误标记为 Green
- **文件**: `data/processed/baselines/elo-proxy.json` → `site/data/baselines-data.js` → `site/js/team-detail.js`
- **症状**: Elo 模型输出被标记为 `source_level: "green"`（可靠事实），前端显示"可靠事实"标签
- **根因**: `build_baselines_json()` 在 `build_site_data.py` 中将所有 baseline 统一标记为 green，未根据数据来源区分等级
- **爆炸半径**: 所有 48 队的详情页"夺冠概率对比"区域 — Elo 数据显示为"可靠事实"误导用户
- **修复**: (1) `build_site_data.py` 的 `build_baselines_json()` 应根据 baseline 类型设置正确的 source_level（Elo/FIFA = Red 或 Yellow，Market = Yellow） (2) `team-detail.js` 应从 JSON 读取 source_level 而非硬编码"可靠事实"
- **严重度**: 🔴 P0 — 违反 source-policy.md 的核心规则（模型输出不能标为可靠事实）

### P1 — 应在本轮修复

#### Issue 3: CODE_MAP 四重复制（~600 行）
- **文件**: `site/js/panorama.js`（CODE_MAP + CODE_TO_SLUG）、`site/js/match.js`（CODE_MAP）、`site/js/team-detail.js`（TEAM_CODE_MAP + CODE_FLAG_MAP）、`site/js/homepage.js`（slugToTeamName）
- **根因**: 四个页面各自独立开发，未共享球队身份映射。新队加入时需改 4 处
- **爆炸半径**: 任何新增/修改球队数据的变更需同步 4 个文件
- **修复**: 提取 `CODE_MAP` + `CODE_TO_SLUG` + `slugToTeamName` 到 `common.js`，四个页面引用公共版本

#### Issue 4: assert 用于生产验证
- **文件**: `scripts/parse_schedule.py:577-591`（6 处 assert）
- **根因**: 开发时用 assert 做快速验证，未考虑 Python `-O` 优化会跳过
- **爆炸半径**: 如果用 `python -O` 运行，错误数据静默通过，下游全部受污染
- **对比**: 其他脚本（numeric_odds.py、build_site_data.py、fetch_market_snapshot.py）均使用 `if/raise` — 这是唯一的 assert 使用
- **修复**: 替换 6 处 assert 为 `if condition: raise ValueError(...)`

#### Issue 5: CI [skip ci] 对 pages.yml 无效
- **文件**: `.github/workflows/market-snapshot.yml`（commit message 含 `[skip ci]`）、`.github/workflows/pages.yml`（无 `[skip ci]` 检测）
- **症状**: market-snapshot.yml 用 `[skip ci]` 提交，但 pages.yml 不检查 commit message，每天仍然触发完整构建部署
- **根因**: `[skip ci]` 只对 `ci.yml`（PR 检查）有效，pages.yml 没有 skip 检测逻辑
- **爆炸半径**: 每日一次不必要的完整构建（~2-3 分钟 GitHub Actions 运行时间）
- **修复方案**:
  - (a) 在 pages.yml 中添加 `if: "!contains(github.event.head_commit.message, '[skip ci]')"` 条件
  - (b) 或移除 market-snapshot.yml 的 `[skip ci]`，接受每日自动部署（这其实是正确行为 — 市场数据更新后应该重建站）
  - 推荐 (b)：市场数据更新后重建站是期望行为

#### Issue 6: Elo 模型零区分度
- **文件**: `scripts/numeric_odds.py:91-103`
- **症状**: 10 支 UEFA 队全部 Elo 1780，4 支 CONMEBOL 全部 1770。同组同洲队概率几乎相同
- **根因**: Elo 仅按洲际分档，无队伍级差异化因子
- **爆炸半径**: 72 场小组赛预测中，约 30+ 场（同洲对阵）的概率无区分度
- **修复**: 引入 FIFA 排名或 Kimi baseline 概率作为差异化权重（至少分 3 档而非 1 档）

### P2 — 建议改进

#### Issue 7: portal.css 单文件 2457 行
- **症状**: Phase 0-2 新增 1059 行 CSS，总文件 2457 行
- **修复**: 拆分为 `portal-base.css` + `panorama.css` + `match.css`

#### Issue 8: JS 风格不一致
- **文件**: `match.js`（36 处 var）、`panorama.js`（14 处 var）vs 其他文件用 const/let
- **修复**: 统一为 const/let

#### Issue 9: 新页面无渐进增强
- **文件**: `panorama.html`、`match.html` — 完全依赖 JS 渲染，无 JS 时页面空白
- **修复**: 添加 `<noscript>` 提示或基本 HTML 骨架

#### Issue 10: 前端 JSON 校验缺失
- **文件**: 所有 JS 文件的 fetch 处理 — 仅 catch fetch 错误，不校验 JSON 结构
- **修复**: 添加基本字段存在性检查

#### Issue 11: FIFA ranking baseline 也近均匀
- **文件**: `data/processed/baselines/fifa-ranking-proxy.json` — 10 队共享 8.5556%
- **根因**: baseline 用洲际均值计算，未引入实际 FIFA 排名数据
- **修复**: 获取真实 FIFA 排名积分作为权重

#### Issue 12: Polymarket 名称在公开数据中
- **文件**: `site/data/baselines-data.js`（description 含 "基于 Polymarket 公开赔率"）
- **严重度**: 低 — source-policy.md 只禁止 AI 供应商名（Kimi/Xiaomi/MiMo），Polymarket 是数据源名称
- **修复**: 可选 — 改为"市场公开赔率"

---

## Investigation Log

### Phase 1 - Initial Triage
**Hypothesis:** Code review 的 5 个问题是系统性模式问题的表现
**Findings:** 确认 — 扩展到 8 维度扫描后额外发现 7 个问题
**Conclusion:** Confirmed — 根因是四个页面独立开发未共享代码、数据管线缺少来源等级传递机制

### Phase 2 - Context Builder 8 维度扫描
**工具**: context_builder，32 files，94K tokens
**覆盖维度**: 代码重复、assert、XSS、CI/CD、数据模型、供应商名、博彩语言、错误处理
**关键发现**: teams.js XSS（P0）、Elo 来源等级错误（P0）、CODE_MAP 四重复制（非三重复制）

### Phase 3 - 文件级验证
**验证项**: (1) teams.js:90 确认 flag 未转义 (2) parse_schedule.py 确认 6 处 assert (3) baselines-data.js 确认 source_level 错误
**Conclusion:** All findings confirmed

---

## Root Cause

1. **代码重复根因**: 四个页面由独立 agent 并行开发，未建立共享数据模块的约定。common.js 仅含 3 个函数（escapeHtml/escapeAttr/sourceClass），缺少球队身份映射
2. **来源等级根因**: `build_baselines_json()` 未根据 baseline 类型区分 source_level，统一标为 green。前端 `team-detail.js` 进一步硬编码"可靠事实"标签
3. **XSS 根因**: teams.js 是早期代码（Phase 0 之前），当时 flag 转义意识不一致。后续 homepage.js/team-detail.js 修复了但 teams.js 遗漏
4. **assert 根因**: parse_schedule.py 是 Phase 1 新脚本，开发者用 assert 做快速验证。项目其他脚本不使用 assert
5. **CI 根因**: `[skip ci]` 约定只在 ci.yml 中有效，pages.yml 不检查 commit message

## Recommendations

| 优先级 | Issue | 修复工作量 | 修复位置 |
|--------|-------|-----------|---------|
| P0 | teams.js XSS | 1 行 | `teams.js:90` |
| P0 | Elo 来源等级 | ~20 行 | `build_site_data.py` + `team-detail.js` |
| P1 | CODE_MAP 提取 | ~50 行 | `common.js` + 4 个 JS 文件 |
| P1 | assert 替换 | ~12 行 | `parse_schedule.py:577-591` |
| P1 | [skip ci] 决策 | ~5 行 | `market-snapshot.yml` 或 `pages.yml` |
| P1 | Elo 区分度 | ~30 行 | `numeric_odds.py:91-103` |

## Preventive Measures

- **共享数据模块**: 在 `common.js` 中维护唯一的球队映射表，新增球队只改一处
- **来源等级传递**: `build_site_data.py` 的每个 `build_*_json()` 函数必须显式设置 source_level，禁止默认 green
- **XSS 检查清单**: 所有 innerHTML 赋值必须使用 `escapeHtml()`，CI 中添加 ESLint 规则检测
- **assert 禁用约定**: 在 CLAUDE.md 或 AGENTS.md 中添加 "不使用 assert" 规则
- **CI 文档**: 记录 `[skip ci]` 只对 ci.yml 有效，pages.yml 不受影响
