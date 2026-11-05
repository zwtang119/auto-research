# 进度记录：2026-11-05（仓库级 LLM 索引机制）

> 范围：为 auto-research 建立可复用索引层，解决「每次 LLM 临时建脚本 / 查资料不准」｜执行：知识库管理团（架构 → 同步 → 独立审核 → 整改）｜状态：已验收、已入库
> 口径：数字均为 2026-11-05 从磁盘实况直接复算，非转引项目自评文档

## 一句话总结

索引机制已落地并通过独立验收；入口按用户 2026-11-05 裁定采用方案 B（`CLAUDE.md` 目录地图补 1 行），`AGENTS.md` 保持用户整理的 3 行极简版，未恢复 49 行旧版。

## 交付

| 文件 | 作用 |
|---|---|
| `docs/INDEX.md` | 人读总索引：171 篇讨论文档、8 主题组，含查询顺序、状态准绳、三层数字口径、5 处待裁定冲突、数据产物区、只读登记区 |
| `docs/index.json` | 机器可查：171 docs / 185 scripts / 5 status_conflicts，含 `related_scripts` / `related_docs` 交叉引用 |
| `docs/SCRIPTS.md` | 按 capability 分 8 类的 185 个脚本登记册 |
| `docs/tools/build_index.py` | 再生脚本：默认写回（幂等、人工字段不覆盖）/ `--dry-run` / `--check`，仅标准库 |
| `CLAUDE.md:31` | 入口指引（方案 B，仅 1 行） |

链路：`AGENTS.md:3` → `CLAUDE.md:31` → `docs/INDEX.md` → `index.json` / `SCRIPTS.md`。`CLAUDE.md` 的 `:7` / `:11` / `:23` 状态口径文字与 `README.md` 一字未改。

## 验收（独立复算）

| 项 | 结果 |
|---|---|
| `index.json` 全量 path 引用 | 1010 条 / 0 失效 |
| `--check` | 362 path / 0 失效 |
| `--dry-run` | 0 新增 / 0 失效 |
| 默认模式幂等 | 连续两次 sha 一致 |
| 重建演练 | `/tmp` 镜像删 `scope` / `counts` / `status_conflicts` 后完整重建，仓库文件未写回 |
| 种子一致性 | `build_index.py` 种子常量与 `index.json` 的 `status_authority` / `why` / `source_note` / `counts` 逐字一致 |
| 禁区 | `evidence/`、`legacy/`、`papers/`、`framework/`、封存仓库零写入 |

审核结论由「条件通过」转「通过」：唯一阻断项（入口链路被外部改动覆盖）已按方案 B 闭合。审核过程中如实证伪了主理人两处记录（阶段 1 的旧 sha、`M AGENTS.md` 归属），均已更正。

## 查明的事实

- **「查资料不准」的机制性根因**：会话注入的目录快照实为 git 已跟踪口径 —— `legacy/` 磁盘 11723 但入 git 仅 74、`evidence/` 850 但入 git 432。只看快照或 `git ls-files` 会系统性找不到 `analysis/` / `legacy/` / `evidence/` 的内容。
- **「每次临时建脚本」的量化证据**：`analysis/` 185 个 `.py` 中仅 1 个标 `reusable=true`（`downloads-pdf-scan/extract.py`）；按日期命名的任务副本反复重写 `freeze_inputs` / `verify` / `release` / `report` / `run_checks` 骨架，且一个任务散落 `docs/plans/` + `docs/investigations/` + `analysis/<副本>/` 三处。
- **5 处状态口径冲突**逐条列 `path:line` 原文并标「待裁定」，未擅自二选一。README / CLAUDE 的「活跃 vs 挂起」分歧已由用户 13:05 / 13:23 改动消解，剩余为主线版本口径（双论文 v1.7 / 开题 v2.1 vs 单篇 v1.3）。

## 已知限制

- `status` 为索引维护初判，**未逐篇内容审读**；权威以 `CLAUDE.md`「当前活跃主线」表为准。
- `scripts[]` 仅覆盖 `analysis/` 限深 3，其余区只做摘要登记；会话注入快照数字口径未确认，`counts` 已标注 `basis`。
- 5 处状态口径冲突仍待用户裁定，本轮不二选一。

## 提交范围

本轮提交仅含 `AGENTS.md`、`CLAUDE.md`、`README.md`、四个 `docs/` 索引产出与本进度文档。工作区其余介入前既有改动（`docs/plans/tsinghua-1024-dna-value-identification-2026-10-27.md`、两处 `papers/*/wiki/index.md`、`.mimosa/`、15 个未跟踪 `analysis/` 目录、`legacy/p11-closed-v5-minimax-m3`）未触碰、未提交。

## 维护

新增讨论文档或脚本后跑 `python3 docs/tools/build_index.py` 登进 `index.json`，再人工补 `status` / `topic` 及 `docs/INDEX.md` 表格行；查路径有效性跑 `--check`。骨架字段每次刷新，人工字段（`status` / `topic` / `verified_at` / `supersedes` / `related_*` / `purpose` / `reusable`）不覆盖。
