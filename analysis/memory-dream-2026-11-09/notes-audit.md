# notes-audit — 171 篇主干讨论文档的结论/状态校验（dreaming D1）

> 日期：2026-11-09｜方法：**机器规则校验 + 分级复核**，非人工逐篇裁决、非状态裁定。
> 输入：`docs/index.json` 的 `docs[]`（171 条）+ 每篇正文前 40 行。输出只写新文件，未改任何原文 / `index.json`。
> 授权：用户 2026-11-09「均同意」P1。

## 结论先行

**结构完整性 100%，语义层 1 条待确认。** 171 篇 `path` 全部存在、`supersedes` 引用全部有效、`verified_at` 全部为 2026-11-05、0 条路径失效。真正需要人工确认的是 1 条字段不一致；另有 20 条「索引派生状态」与 17 条「读取陷阱」，**均不是文档错误**。

| 分级 | 条数 | 含义 | 处置 |
|---|---:|---|---|
| A · 字段不一致 | 1 | `supersedes` 有值但 `status` 非 `superseded` | 列清单，交用户裁定，不自动改 |
| B · 读取陷阱 | 17 | `status=active` 但正文写明「未执行 / 待批准 / NO-GO / 撤回」；或 `dormant` 但出现「已完成」 | 提醒：文档有效 ≠ 文档所述工作已执行；不改字段 |
| C · 索引派生状态 | 20 | `status=挂起` 但正文前 40 行无挂起依据 | **预期行为**：索引按 2026-09-25 主线挂起裁定批量派生，非文档缺陷 |

> ⚠️ **首轮规则曾把 38 条全部当问题（含 21 条硬错误），是验证脚本自身误报**。复核后 C 类降级为「预期」。此处保留该过程，避免后续复用错误聚合数字。与项目既有教训一致：referenced 存绝对路径却拿相对路径比对，会把孤儿率虚高到 97%。

## A · 字段不一致（需人工确认）

- `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md:5` — 有 supersedes 但 status=挂起（topic=世界杯主线）

## B · 读取陷阱（17 条，不改字段）

| 文档 | 行 | 状态 | 规则提示 |
|---|---:|---|---|
| `docs/investigations/decision-coscientist-proposal/PROJECT-BRIEF.md` | 4 | `dormant` | status=dormant 但正文出现完成/交付词，需人工判读 |
| `docs/investigations/decision-coscientist-proposal/README.md` | 3 | `dormant` | status=dormant 但正文出现完成/交付词，需人工判读 |
| `docs/investigations/reprompt-all-sessions-model-vs-tool-time-2026-10-27.md` | 10 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/investigations/token-consumption-handoff-2026-10-27.md` | 5 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/investigations/token-readiness-recheck-2026-10-26.md` | 5 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/investigations/token-report-corrections-2026-10-26.md` | 1 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/token-consumption-handoff-2026-10-27.md` | 7 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/token-readiness-recheck-2026-10-26.md` | 13 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/token-report-2026-10-26.md` | 3 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/tsinghua-1024-dna-value-identification-2026-10-27.md` | 3 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/tsinghua-clean-release-2026-10-27.md` | 22 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/tsinghua-dna-ablation-2026-10-23.md` | 3 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/tsinghua-dna-ablation-handoff-2026-10-23.md` | 5 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md` | 3 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/portfolio/aliases.md` | 27 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/portfolio/project-closure-2026-07-18.md` | 4 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |
| `docs/reviews/tsinghua-clean-release-critique-2026-10-27.md` | 7 | `active` | status=active 但正文含撤回/未执行/待批/NO-GO 限制词，需人工判读 |

## C · 索引派生状态（20 条，预期）

| 文档 | 行 | 说明 |
|---|---:|---|
| `docs/investigations/cds4worldcup-settlement-experiment-executed-2026-07-08.md` | 1 | 主线挂起由索引派生，正文无自述 |
| `docs/investigations/token-report-paper-accounting-2026-10-27.md` | 1 | 主线挂起由索引派生，正文无自述 |
| `docs/investigations/two-paper-roadmap-nature-gap-assessment-2026-07-21.md` | 5 | 主线挂起由索引派生，正文无自述 |
| `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md` | 7 | 主线挂起由索引派生，正文无自述 |
| `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` | 7 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/llm-ensemble-scaling-paper-b-b0-2026-07-22.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-abstract-intro-bold-2026-07-29.md` | 17 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-full-draft-2026-09-11.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-s03-protocol-draft-2026-07-25.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-s04-data-draft-2026-07-25.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-s05-2-team-level-draft-2026-07-27.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-s05-3-kimi-vs-market-draft-2026-07-27.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/paper-a-skeleton-2026-07-25.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/token-paper-accounting-2026-10-27.md` | 16 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/plans/worldcup-paper-outline-and-supplements-2026-07-20.md` | 3 | 主线挂起由索引派生，正文无自述 |
| `docs/progress/2026-07-26-evidence-roadmap-progress.md` | 1 | 主线挂起由索引派生，正文无自述 |
| `docs/reviews/plan-critique-paper-b-b0-2026-07-22.md` | 11 | 主线挂起由索引派生，正文无自述 |
| `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md` | 5 | 主线挂起由索引派生，正文无自述 |
| `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md` | 5 | 主线挂起由索引派生，正文无自述 |

## 方法与边界

- 规则：① 正文前 40 行状态词正则；② `status` 与状态词交叉；③ `supersedes` / `verified_at` 字段一致性；④ 全量 `path` 与 `supersedes` 目标存在性（两项 0 失效）。
- **未做**：逐篇人工阅读 171 篇全文、复算文档中的论文数字、判定任何状态口径冲突 C1–C5。
- **不改**：`docs/index.json`、`README.md`、`CLAUDE.md`、各 `INDEX.md` 状态口径正文、任何归档 / 证据仓文件。
- 状态准绳仍以 `CLAUDE.md`「当前活跃主线」表为准；本文件只提供可复核的机器校验清单。
