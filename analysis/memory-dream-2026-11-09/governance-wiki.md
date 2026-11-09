# 组合治理 / 终裁链 / 索引机制 — 主题导航（dreaming D2 · D 簇 19 篇）

> 生成：2026-11-09｜覆盖 `index.json` topic = 组合治理 12 + 课题终裁链 4 + 已有索引/进度/研究计划各 1 = 19 篇（superseded 10 / active 9）
> 性质：导航页；状态准绳以 [`CLAUDE.md`](../../CLAUDE.md)「当前活跃主线」表为准。不改任何原文。

## 当前有效结论

- **组合主线 2026-07-18 已关闭**（用户决策，全项目终止）。关闭名单以 [`project-closure-2026-07-18.md`](../../docs/portfolio/project-closure-2026-07-18.md) §3 为准；当前处于关闭后孵化期（`CLAUDE.md:7`）。
- **DORMANT / PARK / 想法记录 ≠ 关闭**：C1 AI-auto-research 实证（GO 附 4-gate · DORMANT）、G3/D1 Settlement Reconciliation（PARK）、决策流水线（想法记录，未评审）均未关闭（`CLAUDE.md:17-19`）。
- **终裁结论**：现有 D1–D4 无一够到顶刊（D4 KILL、D2 KILL、D3 并入 D1、D1 降级为 Findings 诚实版）；唯一可能够到 NeurIPS D&B / ICML 主会级的，是把「AI 自动化研究」本身当实证对象——长周期过程 trace + 失败模式 taxonomy（`verdict-topic-selection-first-principles.md:10`）。对应 C1 DORMANT。
- **索引机制 2026-11-05 已验收、已入库**：入口采用方案 B（`CLAUDE.md` 目录地图补 1 行 `INDEX.md` 指引），`AGENTS.md` 保持 3 行极简版，未恢复 49 行旧版（`2026-11-05-repo-index-mechanism-progress.md:8,14`）。
- **2026-11-09 做梦 D4**（本次）：`INDEX.md` / `SCRIPTS.md` 逐篇清单下移到 `INDEX-DETAILS.md` / `SCRIPTS-DETAILS.md`，顶层只留链接；状态口径文字逐字未改。授权：用户「均同意」。

## 权威链

| 文档 | 角色 | 状态 |
|---|---|---|
| [`CLAUDE.md`](../../CLAUDE.md) | 项目地图 / 状态准绳 / 三级证据结构 / 禁区 | **状态最高准绳** |
| [`project-closure-2026-07-18.md`](../../docs/portfolio/project-closure-2026-07-18.md) | 关闭记录，CLOSED | 关闭名单以 §3 为准 |
| [`docs/INDEX.md`](../../docs/INDEX.md) + [`docs/index.json`](../../docs/index.json) | 查资料入口；171 篇 docs / 185 scripts | 精确字段以 `index.json` 为准 |
| [`FRAMEWORK-RULES.md`](../../docs/portfolio/FRAMEWORK-RULES.md) | binding on Day 0（M0 of any paper），per-iteration reviewable | active |
| [`aliases.md`](../../docs/portfolio/aliases.md) | 代号 → 目录别名 | active（更新日期 2026-07-03） |
| `2026-07-03-*` 系列 8 篇（configuration-audit / current-layout-diagram / framework-top-level-build-plan / naming-audit / project-index / rename-proposal / restructure-blueprint / topic5 两份 roadmap） | 组合治理旧层 | **全部 `superseded`**；旧路径重定向查 [`OBSOLETE.md`](../../OBSOLETE.md) |
| [`docs/investigations/INDEX.md`](../../docs/investigations/INDEX.md) | 旧 investigations 索引，Last cleaned 2026-07-08 | `superseded`；未收录 2026-10 系列 → 冲突 C3 |
| `topic-selection-2026-07-18/w1`–`w3` + `verdict-*` | 课题终裁链 | active |
| [`e1-hallucination-fingerprint-probe-spec-2026-08-02.md`](../../docs/plans/e1-hallucination-fingerprint-probe-spec-2026-08-02.md) | E1 幻觉指纹前瞻探针规格 v1.0 | 可执行规格，**待用户确认后跑第一轮** |

## 已验证数字（转录原文 `path:line`，未独立复算）

- 三级证据结构：封存仓库零读写 / 证据快照字节级永不修改 / 分析副本可写并逐条记 CHANGELOG（`CLAUDE.md:49-55`）。
- 禁区与高危区：`papers/` `legacy/` `state/` `framework/` 高引用，禁止重命名/移动内部文件；`state/*` 约 478 处引用（`CLAUDE.md:57-61`）。
- 索引机制规模：171 篇主干讨论文档、8 主题组、5 处待裁定冲突、数据产物区 / 只读登记区（`2026-11-05-repo-index-mechanism-progress.md:14`）；脚本 185 个（限深 3）。
- **三种统计口径并存且互不一致**：`disk_full`（find -type f）/ `git_tracked`（git ls-files）/ `session_injected_snapshot`（上下文快照）。`index.json` `counts.basis_note` 明确：只看上下文快照或只跑 git ls-files 会系统性低估 / 找不到 `analysis/`、`legacy/`、`evidence/`。
- `legacy/` 磁盘全量 **11,723** 文件、md 2,322，但仅 **74** 入 git（`index.json` `readonly_zones`）。
- E1 规格：A/B 双臂各 300，C 臂（跨家族泛化，可选第二轮）300（`e1-...-spec:27,31`）。

## 撤回与陷阱

- ❌ **5 处状态口径冲突 C1–C5 只标注、不裁决**（`docs/INDEX.md:319-360`，逐字保留在 `INDEX-DETAILS.md`）。遇冲突以 `CLAUDE.md` 当前活跃主线表为准绳，但不得擅自替用户二选一。
- ❌ **禁止**未查索引前凭 `README.md` 或记忆断言主线状态（`docs/INDEX.md:12`）。
- ❌ `state/progress.json` 的 status 停在 W6 备忘录阶段（metadata drift），未同步 v1.3 主线裁定（`CLAUDE.md:23`、冲突 C5）。
- ❌ `project-index.md`（2026-07-03）的 P12「新建，短期优先」活跃任务顺序已过时（C2）；`investigations/INDEX.md` 自称 current state 但缺 2026-10 约 20 篇（C3）；`analysis/README.md` 称 `worldcup-2026/` 待建，实际已存在（C4）。
- ❌ 别把任何单一文件总数当作「文件是否存在 / 内容是否权威」的依据（`index.json` `counts.basis_note`）。
- ❌ `legacy/` 只读登记：不深挖 2,322 篇历史 md、不写入、不重命名/移动内部文件。
- ❌ `docs/SECRETS.md`、`.env` 敏感，不索引、不外传（`docs/INDEX.md` 维护约定）。

## 未决

| 项 | 状态 |
|---|---|
| C1 世界杯版本口径 / C2 组合状态 / C3 investigations 索引 / C4 analysis README / C5 metadata drift | **全部待裁定** |
| E1 幻觉指纹探针 | 规格 v1.0，待用户确认后跑第一轮 |
| 组合状态 | 已关闭，处于关闭后孵化期；DORMANT/PARK 未关闭也非活跃 |
| 本次做梦 D4 结构下移 | 已执行，待用户复核；原页备份在 `backup/` |

## 原文入口

[`docs/portfolio/`](../../docs/portfolio/) ｜ [`docs/investigations/topic-selection-2026-07-18/`](../../docs/investigations/topic-selection-2026-07-18/) ｜ [`docs/roadmaps/`](../../docs/roadmaps/) ｜ [`docs/progress/`](../../docs/progress/) ｜ [`docs/INDEX-DETAILS.md`](../../docs/INDEX-DETAILS.md) D/E/F 节 ｜ [`docs/index.json`](../../docs/index.json)

> 本页由 dreaming 生成，写入新目录，原文 0 改动。C1–C5 只引用、不裁决。
