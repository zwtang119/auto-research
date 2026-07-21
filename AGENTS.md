# AGENTS.md — Agent 工作指引

> 你正在为 auto-research 仓库工作。先读 `CLAUDE.md`（项目地图与约定），再读本文件。

## 优先阅读顺序

1. `CLAUDE.md` — 目录地图、三级证据结构、禁区
2. 当前活跃主线的入口文档：
   - 开题 `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md`
   - 计划 `docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md`
3. 涉及证据操作时：`evidence/cds4worldcup-snapshot-2026-07-20/MANIFEST.md`

## 核心规则

### 证据纪律（最高优先级，违反即返工）

- **封存仓库**（`~/Documents/GitHub/cds4worldcup`）零读写，无一例外。
- **证据快照**（`evidence/`）只读；禁止任何修改（包括删 .DS_Store、格式化、重命名）。
- 一切分析在**分析副本**（`analysis/<topic>/`）进行；增补逐条记该副本的 `CHANGELOG.md`（内容、来源、时间、执行者）。
- 从 bundle 提取历史版本时，克隆目标必须位于 `analysis/` 内，用完即清。

### 验证纪律

- 子代理/oracle 的断言（文件存在性、数字、路径、因果声明）一律经直接计算复核后才可写入交付物；复核结果（确认/证伪/漏检）要记录在案。
- 论文所用数字必须从冻结数据复算，禁止转引项目自评文档的指标。

### 写作与引用

- 引用代码/文档位置用 `path:line` 格式；引用证据快照内文件时注明"证据快照"字样。
- 事实性声明标 Green Source；预测/模型输出标 Red Source 并注明冻结版本（如 `88a9bfd`）。
- 文档语言：中文为主，术语保留英文原词；文档内日期用 ISO 格式。

### git 纪律

- 不擅自 `git commit`、`git push`、`git reset`、`git rebase`；需要时先向用户请示。
- 移动文件用 `git mv`；删除前列清单给用户。
- 发现工作区有非自己产生的改动（如 `legacy/p11-closed-v5-minimax-m3` 的 modified 标记），不要触碰，向用户报告。

### 边界

- 不输出投注建议、不报告收益率。
- 不做超出任务范围的"顺手优化"；高引用区（`papers/`、`legacy/`、`state/`、`framework/`）只读。
- 计划类工作产物放 `docs/plans/`，调查/开题放 `docs/investigations/`，命名 `<topic>-<YYYY-MM-DD>.md`。

## 当不确定时

1. 先查 `docs/portfolio/aliases.md`（代号映射）与 `docs/portfolio/naming-audit-2026-07-03.md`（命名风险 taxonomy）。
2. 结构性问题（移动、改名、删除）先出方案给用户裁定，再执行。
3. 与主线相关的方向性分歧（如 W6 备忘录 vs 开题），如实标注，不擅自二选一。
