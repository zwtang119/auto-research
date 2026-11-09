# docs/INDEX.md — 仓库级人读总索引

> 最近核对：2026-11-05。本页表格由 [`index.json`](index.json) 派生，字段以 `index.json` 为准。
> 建立本页的目的：解决「每次 LLM 都临时构建脚本 / 查资料不准确」——把「先查哪里、什么状态算数、哪里是噪声」写死在仓库里，而不是每次重新推断。

## 查询顺序（LLM 会话开始必读）

1. 先读本页，按主题定位候选文档；需要精确字段时进第 2 步。
2. 再查 [`index.json`](index.json) 精确命中 `path` / `topic` / `status` / `kind` / `related_scripts` / `related_docs`；**命中即用，不再重复扫描**。
3. 需要脚本时先查 [`SCRIPTS.md`](SCRIPTS.md)，按 capability（我要做什么）定位，再决定复用而非重写。
4. 未命中才做只读扫描，且必须限深、排除数据区与只读区（见本文「数据产物区」「只读登记区」）。
5. **禁止**在未查索引前凭 `README.md` 或记忆断言主线状态；状态口径冲突以本文「待裁定」节为准，不擅自二选一。
6. 引用证据快照内文件时注明「证据快照」字样；引用位置统一用 `path:line`。

## 状态准绳

- 状态以 [`../CLAUDE.md`](../CLAUDE.md)「当前活跃主线」表为准。[`../README.md`](../README.md):5 于 2026-11-05 本次任务期间由**外部改动**补上「2026-09-25 已挂起、投稿暂停」标注，与 `CLAUDE.md:11` 在「活跃 / 挂起」上已趋一致（该改动为工作区 pre-existing M，非本团队产生，未触碰）；**遗留分歧是主线版本口径**（双论文 v1.7 / 开题 v2.1 vs 单篇开题 v1.3），见 C1，仍为「待裁定」。
- 本页与 `index.json` 的 `status` 是索引维护时的初判，取值 `active / superseded / archived / dormant / 挂起`；`verified_at` 统一为 2026-11-05（本次核对日）。
- 5 处状态口径冲突只标注、不改原文，全部列在本文「待裁定」节；**本阶段不修改** `README.md`、`CLAUDE.md`、`docs/portfolio/project-index.md`、`docs/investigations/INDEX.md`、`analysis/README.md` 的状态口径正文（唯一例外：用户 2026-11-05 专项裁定方案 B，仅在 `CLAUDE.md`「目录地图」`docs/` 树下新增 1 行 `INDEX.md` 入口指引，不动 `:7` / `:11` / `:23` 等任何状态口径文字；见「入口互链状态与待办」节）。

## 数字口径（「查资料不准」的机制性根因）

2026-11-05 实测，三种统计口径并存且互相不一致。LLM 只看上下文快照或只跑 `git ls-files` 会系统性低估 / 找不到 `analysis/`、`legacy/`、`evidence/`。**查资料请以 `index.json` 的逐条 `path` 为准，不要把任何一层总数当作文件是否存在的依据。**

| 区域 | 磁盘全量（find） | git 已跟踪（git ls-files） | 会话注入快照 | 说明 |
|---|---|---|---|---|
| `docs/` | 2474（基线：173 md / 5 py） | 2468 | — | 其中 2268 个在 `docs/papers-closed-portfolio/experiments/`，是数据产物不是讨论文档；md 数**基线 173（索引建立前）→ 当前 176**（新增 `INDEX.md` / `SCRIPTS.md` 2 篇属索引机制自身、位于 `docs/` 顶层不计入 `docs[]`；再新增本进度文档 1 篇计入 `docs[]`，现为 171 篇）；`docs/` 文件总数基线 2474 → 当前 2479。2474 与 5 py 同为索引建立前基线口径，当前值见 `index.json` 的 `counts.disk_full.docs_md_baseline` / `docs_md_current` |
| `analysis/` | 约 85000（限深 3 有 185 个 .py） | 不入 git 为主 | — | 23 个一级子目录，按日期命名的一次性任务副本 |
| `evidence/` | 850（337 md / 37 py） | 432 | 548 | 证据快照，字节级只读 |
| `legacy/` | 11723（2322 md / 39 py） | 74 | 7546 | 磁盘与 git 口径差距最大的区域 |
| `papers/` | 213（76 md / 22 py） | 204 | — | 高引用只读区 |
| `framework/` | 20（8 md / 3 py） | 17 | — | 只读 |

统计时间与完整口径说明见 `index.json` 的 `counts`（`measured_at` / `basis_note` / `disk_full` / `git_tracked` / `session_injected_snapshot`）。

## 已有索引一览（多套并存且互相打架，勿单独采信）

| 索引 | 状态 |
|---|---|
| [`../CLAUDE.md`](../CLAUDE.md) | 更新 2026-10-27，当前状态准绳 |
| [`../AGENTS.md`](../AGENTS.md) | Agent 入口（3 行极简版，指向 [`../CLAUDE.md`](../CLAUDE.md)）；索引入口指引已落在 CLAUDE.md 目录地图 |
| [`../README.md`](../README.md) | 2026-11-05 外部改动已补挂起标注；版本口径分歧见 C1（待裁定） |
| [`../OBSOLETE.md`](../OBSOLETE.md) | 旧路径重定向；第 40–44 行是给 agent 的约定 |
| [`portfolio/project-index.md`](portfolio/project-index.md) | 2026-07-03，活跃任务顺序已过时（C2） |
| [`investigations/INDEX.md`](investigations/INDEX.md) | Last cleaned 2026-07-08，未收录 2026-10 系列（C3） |
| [`../analysis/README.md`](../analysis/README.md) | 称 `worldcup-2026/` 待建，实际已存在（C4） |
| `papers/*/wiki/index.md` ×4 | 4 个历史副本索引，均未纳入本索引 `docs[]` |

## 入口互链状态与待办

> 用户裁定「状态冲突只标注不改原文、落点仅 `docs/` + `AGENTS.md`」；**2026-11-05 追加专项裁定：采用方案 B「指引放 CLAUDE.md」，仅豁免在 `CLAUDE.md`「目录地图」`docs/` 树下新增 1 行 `INDEX.md` 指引**。因此下列 5 个入口中，仅 `CLAUDE.md` 按专项裁定补了这 1 行（非反向链接、不动状态口径正文）；其余 4 个仍不写回任何反向链接（不给它们加一行、不改一个字）。互链状态以本页登记为准。

| 入口（仓库相对路径） | 本轮是否加反向链接 | 说明 |
|---|---|---|
| `README.md` | 否 | 项目根入口；2026-11-05 有外部改动（见 C1 的 `observed_change`），本团队未触碰 |
| `CLAUDE.md` | 已按用户裁定补 1 行目录地图指引（仅此一处，不动状态口径正文） | 方案 B：在「目录地图」`docs/` 树下新增 `INDEX.md` 行，给出路径与查询顺序；`:7` / `:11` / `:23` 状态口径文字一字未改 |
| `docs/portfolio/project-index.md` | 否 | 旧版组合索引（C2），更新日期 2026-07-03 |
| `docs/investigations/INDEX.md` | 否 | 旧版 investigations 索引（C3），Last cleaned 2026-07-08 |
| `analysis/README.md` | 否 | 分析副本入口（C4），称 `worldcup-2026/`（待建） |

**为何不写反向链接**：用户已明确「状态冲突＝只标注不改原文」，上述文件是状态口径冲突所涉的原文 / 入口；本阶段授权只写 `docs/INDEX.md`、`docs/index.json`、`docs/tools/build_index.py`，根文件写入仅限用户专项豁免的 `CLAUDE.md` 那 1 行。故反向链接不落盘到其余 4 个入口，改为在本页集中登记「入口清单 + 反向互链状态 + 待办」。`docs/INDEX.md` 仍是索引权威入口，发现路径不依赖这些回链。

**待办（若今后获授权）**：如需进一步强化，可考虑在上述其余 4 个文件顶部各加一行指向 `docs/INDEX.md` 的相对链接（从各文件所在目录出发，例如仓库根文件用 `[仓库级总索引](docs/INDEX.md)`、`docs/portfolio/` 与 `docs/investigations/` 下的文件用 `[仓库级总索引](../INDEX.md)`、`analysis/README.md` 用 `[仓库级总索引](../docs/INDEX.md)`）。当前入口链路已按方案 B 闭合，本轮不执行，待用户明确授权后再补。

**当前发现路径（已闭合，不依赖反向链接）**：用户 2026-11-05 裁定采用方案 B「指引放 CLAUDE.md」，链路为 [`../AGENTS.md`](../AGENTS.md):3 → [`../CLAUDE.md`](../CLAUDE.md)「目录地图」`docs/` 树下的 `INDEX.md` 行 → 本页 `docs/INDEX.md` → `index.json` / `SCRIPTS.md`。本页 `docs/INDEX.md` 自身仍是索引的权威入口，按本页「查询顺序（LLM 会话开始必读）」节（第 6–13 行）进入 `index.json` / `SCRIPTS.md`；这一路径不依赖上述 5 个入口的反向链接，故本轮除方案 B 指定的 1 行目录地图指引外不加回链，不影响索引的可达性。

> 注（2026-11-05 一致性巡检）：用户 2026-11-05 裁定采用方案 B（指引放 CLAUDE.md），**入口链路已闭合**。事实记录：`AGENTS.md` 磁盘内容为 3 行极简版，`git diff -- AGENTS.md` 显示其相对 HEAD 为 `-1,49 +1,3` 的删减，上一阶段登记的「查询顺序」14 行节**当前不在磁盘上**；该改动为工作区 pre-existing M、用户有意整理、非本团队产生，按授权边界**未触碰**、不恢复 HEAD 旧版。本团队仅在 `CLAUDE.md`「目录地图」`docs/` 树下新增 1 行 `INDEX.md` 指引，`CLAUDE.md` 状态口径正文（`:7` / `:11` / `:23`）与 `README.md` 一字未改。

## 按主题 / 主线索引（共 171 篇主干讨论文档）

> 每条给出仓库相对路径（链接为从 `docs/` 出发的相对路径）、一句话说明、`status`、`verified_at`。
> 「说明」对核心文档为人工撰写，对同质归档文档采用文档自身标题并加「归档：」前缀；完整 `kind` / `supersedes` / `related_scripts` / `related_docs` 见 [`index.json`](index.json)。


### A. 世界杯主线（⏸ 挂起）

> 开题 v1.3 / v2.1、双论文路线图 v1.7、Paper A 各节草稿、缺口调查与证据进度。2026-09-25 用户决定无限期挂起、投稿暂停；`README.md:5` 已于 2026-11-05 由外部改动补上「2026-09-25 已挂起、投稿暂停」标注，与 `CLAUDE.md:11` 在活跃/挂起上已趋一致，不再对立；剩余分歧为主线版本口径（双论文 v1.7 / 开题 v2.1 vs 单篇开题 v1.3），见 C1（待裁定）。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/investigations/cds4worldcup-settlement-experiment-executed-2026-07-08.md`](investigations/cds4worldcup-settlement-experiment-executed-2026-07-08.md) | cds4worldcup 结算实验：从调研到执行完成的完整记录 | `挂起` | 2026-11-05 |
| [`docs/investigations/dmo-uncertainty-decision-reading-2026-07-22.md`](investigations/dmo-uncertainty-decision-reading-2026-07-22.md) | DMO 不确定性决策文献精读（已关闭 2026-07-22） | `archived` | 2026-11-05 |
| [`docs/investigations/two-paper-roadmap-nature-gap-assessment-2026-07-21.md`](investigations/two-paper-roadmap-nature-gap-assessment-2026-07-21.md) | 评估报告：双篇路线图离顶刊多远（Nature gap assessment） | `挂起` | 2026-11-05 |
| [`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`](investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md) | 世界杯开题 v2.1（W5 后定位，README 列为主线） | `挂起` | 2026-11-05 |
| [`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md`](investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md) | 世界杯算法比较实证论文开题（v1.3，CLAUDE.md 列为主线） | `挂起` | 2026-11-05 |
| [`docs/investigations/worldcup-paper-topic-2026-07-19.md`](investigations/worldcup-paper-topic-2026-07-19.md) | W6 终裁备忘录（用户裁定降为参考） | `superseded` | 2026-11-05 |
| [`docs/plans/llm-ensemble-scaling-paper-b-b0-2026-07-22.md`](plans/llm-ensemble-scaling-paper-b-b0-2026-07-22.md) | Paper B B0 执行计划：LLM 群体预测 scaling 实验的启动阶段 | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-abstract-intro-bold-2026-07-29.md`](plans/paper-a-abstract-intro-bold-2026-07-29.md) | Paper A 摘要与引言（创新拉满版 v0.1，2026-07-29） | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-full-draft-2026-09-11.md`](plans/paper-a-full-draft-2026-09-11.md) | 审计链锚定的对账协议：2026 世界杯五份封存预测的可验证评估（工作稿） | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-s03-protocol-draft-2026-07-25.md`](plans/paper-a-s03-protocol-draft-2026-07-25.md) | Paper A §3 初稿：The Protocol（方法核心章） | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-s04-data-draft-2026-07-25.md`](plans/paper-a-s04-data-draft-2026-07-25.md) | Paper A §4 初稿：Data（五份封存预测与证据链） | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-s05-2-team-level-draft-2026-07-27.md`](plans/paper-a-s05-2-team-level-draft-2026-07-27.md) | Paper A §5.2 初稿：队伍层（H3：路径枚举引擎的 rank-vs-mass 分裂） | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-s05-3-kimi-vs-market-draft-2026-07-27.md`](plans/paper-a-s05-3-kimi-vs-market-draft-2026-07-27.md) | Paper A §5.3 初稿：kimi vs 市场（A4 模块，H4） | `挂起` | 2026-11-05 |
| [`docs/plans/paper-a-skeleton-2026-07-25.md`](plans/paper-a-skeleton-2026-07-25.md) | Paper A 论文骨架（章节结构 + 每节要点 + 图表落位） | `挂起` | 2026-11-05 |
| [`docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md`](plans/worldcup-algorithms-comparison-paper-2026-07-20.md) | 世界杯算法比较论文计划（2026-07-20 裁定） | `挂起` | 2026-11-05 |
| [`docs/plans/worldcup-paper-outline-and-supplements-2026-07-20.md`](plans/worldcup-paper-outline-and-supplements-2026-07-20.md) | 世界杯论文：选题细化、IMRaD 写作大纲与补充工作规划 | `挂起` | 2026-11-05 |
| [`docs/progress/2026-07-26-evidence-roadmap-progress.md`](progress/2026-07-26-evidence-roadmap-progress.md) | 进度记录：2026-07-25 → 07-26（证据链建设 + W5 定位落地 + 分析副本批次） | `挂起` | 2026-11-05 |
| [`docs/reviews/plan-critique-paper-b-b0-2026-07-22.md`](reviews/plan-critique-paper-b-b0-2026-07-22.md) | 计划批评：Paper B B0 执行计划（草案） | `挂起` | 2026-11-05 |
| [`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md`](roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md) | 世界杯双论文路线图工作稿 | `挂起` | 2026-11-05 |
| [`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md`](roadmaps/worldcup-two-paper-roadmap-2026-07-21.md) | 世界杯双论文路线图 v1.7 | `挂起` | 2026-11-05 |

（本组 20 篇）

### B. Decision Co-Scientist（开题·暂停待资源）

> 终裁 GO 附条件、未投入 MVE；`PROJECT-BRIEF.md` 是陌生人入口。状态 `dormant`（暂停，非关闭）。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/investigations/decision-coscientist-proposal/PROJECT-BRIEF.md`](investigations/decision-coscientist-proposal/PROJECT-BRIEF.md) | Decision Co-Scientist 陌生人入口单文档简报 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/README.md`](investigations/decision-coscientist-proposal/README.md) | Decision Co-Scientist 开题工作包（交接文档） | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/adjacent-work-positioning-2026-07-19.md`](investigations/decision-coscientist-proposal/adjacent-work-positioning-2026-07-19.md) | Adjacent-work Positioning — 决策流水线想法的相邻工作定位 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/anchor-authenticity-and-corpus-2026-07-19.md`](investigations/decision-coscientist-proposal/anchor-authenticity-and-corpus-2026-07-19.md) | 调研：锚文档真实性核验与官方调查报告语料扩容 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/anchors/anchor-pool-pipeline.md`](investigations/decision-coscientist-proposal/anchors/anchor-pool-pipeline.md) | 现实锚池（Anchor Pool）建设流水线：现状、命名与自动化分层 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/asset-mapping-2026-07-19.md`](investigations/decision-coscientist-proposal/asset-mapping-2026-07-19.md) | 决策流水线资产映射——Policysim-v0.2 → 8 步流水线复用与缺口（2026-07-19） | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/idea-decision-pipeline-2026-07-19.md`](investigations/decision-coscientist-proposal/idea-decision-pipeline-2026-07-19.md) | 想法备忘录：决策流水线——把 CDS 决策科学拆成 Agent 流水线 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/pipeline-design-spec-2026-07-19.md`](investigations/decision-coscientist-proposal/pipeline-design-spec-2026-07-19.md) | 决策流水线设计规范——8 步 Agent 流水线 I/O 契约、降级协议与编排论证 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md`](investigations/decision-coscientist-proposal/proposal-decision-coscientist.md) | Decision Co-Scientist 开题主文档 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/q1-novelty-and-theory.md`](investigations/decision-coscientist-proposal/q1-novelty-and-theory.md) | Q1 备忘录：novelty 区分核查与 self-play 理论谱系定位 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/q2-abm-validation-and-citations.md`](investigations/decision-coscientist-proposal/q2-abm-validation-and-citations.md) | Q2 备忘录：ABM 验证谱系定位、SLALOM 对话、引用核验与 LQS 分级 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/q3-validation-arm-selection.md`](investigations/decision-coscientist-proposal/q3-validation-arm-selection.md) | Q3 备忘录：非 LLM 校验臂选型 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/q4-gulei-anchor-encoding.md`](investigations/decision-coscientist-proposal/q4-gulei-anchor-encoding.md) | Q4：古雷「4·6」因子锚编码探针（G3）——Factor Ledger schema 灾害域适配性评估 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/q5-second-case-selection.md`](investigations/decision-coscientist-proposal/q5-second-case-selection.md) | Q5 备忘录：第二真实案例选定 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/redteam-review-2026-07-19.md`](investigations/decision-coscientist-proposal/redteam-review-2026-07-19.md) | 决策流水线评估包独立红队评审 — 2026-07-19 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/reviews/r1-response.md`](investigations/decision-coscientist-proposal/reviews/r1-response.md) | R1 评审意见的逐条回应（v1.0 → v1.1） | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/reviews/r1-review.md`](investigations/decision-coscientist-proposal/reviews/r1-review.md) | 独立评审报告 R1 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/reviews/r2-response.md`](investigations/decision-coscientist-proposal/reviews/r2-response.md) | R2 评审意见的逐条回应（v1.1 → v1.2） | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/reviews/r2-review.md`](investigations/decision-coscientist-proposal/reviews/r2-review.md) | R2 独立评审：开题报告 v1.1《面向应急决策的策略锦标赛与进化式多智能体推演——现实锚校准的方法与实证》 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/revision-brief-2026-07-19.md`](investigations/decision-coscientist-proposal/revision-brief-2026-07-19.md) | 文档修订简报（2026-07-19 晚） | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/ruling-memo-2026-07-19.md`](investigations/decision-coscientist-proposal/ruling-memo-2026-07-19.md) | 决策流水线评估包终裁 memo — 2026-07-19 | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/source-inventory-2026-07-19.md`](investigations/decision-coscientist-proposal/source-inventory-2026-07-19.md) | 灾害决策推演数据源盘点（定向核查版） | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/topic-eval-explained-em-audience-2026-07-19.md`](investigations/decision-coscientist-proposal/topic-eval-explained-em-audience-2026-07-19.md) | 选题思路说明：Decision Co-Scientist | `dormant` | 2026-11-05 |
| [`docs/investigations/decision-coscientist-proposal/topic-eval-top-journal-2026-07-19.md`](investigations/decision-coscientist-proposal/topic-eval-top-journal-2026-07-19.md) | 选题终裁 memo：Decision Co-Scientist 顶刊可行性评价（第二趟管线） | `dormant` | 2026-11-05 |
| [`docs/plans/decision-coscientist-experiment-2026-07-19.md`](plans/decision-coscientist-experiment-2026-07-19.md) | Decision Co-Scientist 实验计划 | `dormant` | 2026-11-05 |
| [`docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md`](reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md) | Plan Critique: decision-coscientist-experiment-2026-07-19.md | `dormant` | 2026-11-05 |

（本组 26 篇）

### C. 2026-10 token / tsinghua / reprompt 系列（当前最新工作区）

> 约 36 篇 2026-10 新增讨论与报告，`docs/investigations/INDEX.md` 完全未收录（C3）。这些文档与 `analysis/` 下按日期命名的脚本副本的对应关系，见 `index.json` 的 `related_scripts` 与 [`SCRIPTS.md`](SCRIPTS.md)。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/investigations/reprompt-all-sessions-model-vs-tool-time-2026-10-27.md`](investigations/reprompt-all-sessions-model-vs-tool-time-2026-10-27.md) | 调查：全项目会话时间复算——剔除工具执行后重新判断（GPT 思考慢？） | `active` | 2026-11-05 |
| [`docs/investigations/reprompt-slow-sessions-1023-1025-2026-10-27.md`](investigations/reprompt-slow-sessions-1023-1025-2026-10-27.md) | 调查：1023/1025 系列会话耗时过长的原因（GPT 思考慢？） | `active` | 2026-11-05 |
| [`docs/investigations/token-1023-handoff-confirmation-2026-10-27.md`](investigations/token-1023-handoff-confirmation-2026-10-27.md) | 1023 接入交接：编排者独立复核确认 | `active` | 2026-11-05 |
| [`docs/investigations/token-adoption-handoff-confirmation-2026-10-27.md`](investigations/token-adoption-handoff-confirmation-2026-10-27.md) | 1023 / 1025 采用集：恢复核查与编排者确认 | `active` | 2026-11-05 |
| [`docs/investigations/token-consumption-handoff-2026-10-27.md`](investigations/token-consumption-handoff-2026-10-27.md) | Token 正式消费交接调查：批准链缺项与候选包 v1 | `active` | 2026-11-05 |
| [`docs/investigations/token-readiness-recheck-2026-10-26.md`](investigations/token-readiness-recheck-2026-10-26.md) | Token 复核更正说明与有限接入准备 | `active` | 2026-11-05 |
| [`docs/investigations/token-report-2026-10-26.md`](investigations/token-report-2026-10-26.md) | 暂行 token 调用报告（Item 3） | `active` | 2026-11-05 |
| [`docs/investigations/token-report-2026-10-27.md`](investigations/token-report-2026-10-27.md) | Token 统一报告：1023 冻结接入与 replacement | `active` | 2026-11-05 |
| [`docs/investigations/token-report-complete-2026-10-27.md`](investigations/token-report-complete-2026-10-27.md) | Token 统一报告：1025 replacement 完成与1023缺失说明 | `active` | 2026-11-05 |
| [`docs/investigations/token-report-corrections-2026-10-26.md`](investigations/token-report-corrections-2026-10-26.md) | Token 更正登记表（只读源仓；未执行替换） | `active` | 2026-11-05 |
| [`docs/investigations/token-report-imputation-feasibility-2026-10-26.md`](investigations/token-report-imputation-feasibility-2026-10-26.md) | Investigation: 未记录 token 部分的"采用值"可行性（2月试验及全部实验） | `active` | 2026-11-05 |
| [`docs/investigations/token-report-paper-accounting-2026-10-27.md`](investigations/token-report-paper-accounting-2026-10-27.md) | Token 论文核算：采用集主表、资源账附录、历史估算另列 | `挂起` | 2026-11-05 |
| [`docs/investigations/tsinghua-1025-vs-may-2026-10-27.md`](investigations/tsinghua-1025-vs-may-2026-10-27.md) | 调查：1025八臂实验与五月实验的现象及可能解释 | `active` | 2026-11-05 |
| [`docs/investigations/tsinghua-dna-protocol-equivalence-2026-10-23.md`](investigations/tsinghua-dna-protocol-equivalence-2026-10-23.md) | Investigation: DNA 配套消融的历史协议等价性 | `active` | 2026-11-05 |
| [`docs/investigations/tsinghua-three-datasets-reading-order-2026-10-27.md`](investigations/tsinghua-three-datasets-reading-order-2026-10-27.md) | 调查：三组数据的非时间顺序解读框架 | `active` | 2026-11-05 |
| [`docs/plans/token-1023-append-2026-10-27.md`](plans/token-1023-append-2026-10-27.md) | 1023 Token 冻结接入计划 | `active` | 2026-11-05 |
| [`docs/plans/token-1025-append-2026-10-27.md`](plans/token-1025-append-2026-10-27.md) | 1025 Token replacement 与1023缺失核查 | `active` | 2026-11-05 |
| [`docs/plans/token-consumption-handoff-2026-10-27.md`](plans/token-consumption-handoff-2026-10-27.md) | Token 正式消费交接计划（候选 v1 与批准路径） | `active` | 2026-11-05 |
| [`docs/plans/token-paper-accounting-2026-10-27.md`](plans/token-paper-accounting-2026-10-27.md) | Token 论文三层核算实施与验收计划 | `挂起` | 2026-11-05 |
| [`docs/plans/token-readiness-recheck-2026-10-26.md`](plans/token-readiness-recheck-2026-10-26.md) | Token 复核与最终接入准备 | `active` | 2026-11-05 |
| [`docs/plans/token-report-2026-10-26.md`](plans/token-report-2026-10-26.md) | Plan: Token 调用报告（分阶段交付） | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-1024-dna-value-identification-2026-10-27.md`](plans/tsinghua-1024-dna-value-identification-2026-10-27.md) | 1024：匿名MAMR中的DNA消融 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-clean-release-2026-10-27.md`](plans/tsinghua-clean-release-2026-10-27.md) | 清华 1023 / 1025 实验与全项目 Token 清洁交付：执行计划 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-dna-ablation-2026-10-23.md`](plans/tsinghua-dna-ablation-2026-10-23.md) | 原实验配套 DNA 消融：最小改动方案 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-dna-ablation-handoff-2026-10-23.md`](plans/tsinghua-dna-ablation-handoff-2026-10-23.md) | DNA 配套消融：执行 Agent 交接文档 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md`](plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md) | 1023 DNA 消融：报告层数据适配器设计（方案，未实施） | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-dna-final-closeout-2026-10-27.md`](plans/tsinghua-dna-final-closeout-2026-10-27.md) | 1023 DNA配套消融：最终验收—正式统计—报告交付 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-factorial-ablation-evaluation-2026-10-25.md`](plans/tsinghua-factorial-ablation-evaluation-2026-10-25.md) | 1025独立八条件消融研究计划 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-factorial-pdf-reports-2026-10-27.md`](plans/tsinghua-factorial-pdf-reports-2026-10-27.md) | 1025 综合与逐案例 PDF 交付计划 | `active` | 2026-11-05 |
| [`docs/plans/tsinghua-final-preflight-2026-10-27.md`](plans/tsinghua-final-preflight-2026-10-27.md) | 最终阶段前离线预检计划 | `active` | 2026-11-05 |
| [`docs/progress/2026-10-27-tsinghua-clean-release-progress.md`](progress/2026-10-27-tsinghua-clean-release-progress.md) | 进度记录：2026-10-22 → 10-27（清华 policysim 线：1023 DNA 消融 / 1025 八臂析因 / token 三层核算 / 清洁交付） | `active` | 2026-11-05 |
| [`docs/reviews/tsinghua-clean-release-critique-2026-10-27.md`](reviews/tsinghua-clean-release-critique-2026-10-27.md) | 清华 clean release：一次有界设计审查 | `active` | 2026-11-05 |
| [`docs/reviews/tsinghua-dna-ablation-critique-2026-10-23.md`](reviews/tsinghua-dna-ablation-critique-2026-10-23.md) | 清华 DNA 消融计划：Phase 6 独立文档审查 | `active` | 2026-11-05 |
| [`docs/reviews/tsinghua-factorial-ablation-review-2026-10-25.md`](reviews/tsinghua-factorial-ablation-review-2026-10-25.md) | 八条件因子消融计划：限定评审 | `active` | 2026-11-05 |
| [`docs/reviews/tsinghua-factorial-ablation-v2-review-2026-10-25.md`](reviews/tsinghua-factorial-ablation-v2-review-2026-10-25.md) | Tsinghua factorial ablation v2 限定评审 | `active` | 2026-11-05 |
| [`docs/reviews/tsinghua-report-visual-preflight-2026-10-27.md`](reviews/tsinghua-report-visual-preflight-2026-10-27.md) | 三样张视觉/PDF预检设计 review | `active` | 2026-11-05 |

（本组 36 篇）

### D. 组合治理、关闭与已有索引

> 组合主线已于 2026-07-18 关闭；`project-index.md` 的 P12「新建，短期优先」活跃任务顺序停在 2026-07-03（C2）。关闭名单以 `docs/portfolio/project-closure-2026-07-18.md` §3 为准。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/investigations/INDEX.md`](investigations/INDEX.md) | 旧版 investigations 索引（停在 2026-07-08） | `superseded` | 2026-11-05 |
| [`docs/investigations/topic-selection-2026-07-18/verdict-topic-selection-first-principles.md`](investigations/topic-selection-2026-07-18/verdict-topic-selection-first-principles.md) | 顶刊选题终裁 memo：基于第一性原理的协调员决策 | `active` | 2026-11-05 |
| [`docs/investigations/topic-selection-2026-07-18/w1-first-principles-criteria.md`](investigations/topic-selection-2026-07-18/w1-first-principles-criteria.md) | W1: 从第一性原理提取【如何选题才能写出 first-class paper】的标准清单 | `active` | 2026-11-05 |
| [`docs/investigations/topic-selection-2026-07-18/w2-directions-audit.md`](investigations/topic-selection-2026-07-18/w2-directions-audit.md) | W2 — 4 方向诚实审计（GO/PARK/KILL 决策依据） | `active` | 2026-11-05 |
| [`docs/investigations/topic-selection-2026-07-18/w3-ai-autoresearch-landscape.md`](investigations/topic-selection-2026-07-18/w3-ai-autoresearch-landscape.md) | W3 · AI 自动化研究（AI-driven auto research）外部景观与本地资产 | `active` | 2026-11-05 |
| [`docs/portfolio/2026-07-03-configuration-audit.md`](portfolio/2026-07-03-configuration-audit.md) | 2026-07-03 Experiment Configuration Audit | `superseded` | 2026-11-05 |
| [`docs/portfolio/FRAMEWORK-RULES.md`](portfolio/FRAMEWORK-RULES.md) | 框架规则（含 R7 cite-restoration，归档不得删的依据） | `active` | 2026-11-05 |
| [`docs/portfolio/aliases.md`](portfolio/aliases.md) | 论文代号映射（P7 / P8 / P12 / P1+P2） | `active` | 2026-11-05 |
| [`docs/portfolio/current-layout-diagram-2026-07-03.md`](portfolio/current-layout-diagram-2026-07-03.md) | AutoResearch 当前布局示意图 (2026-07-03) | `superseded` | 2026-11-05 |
| [`docs/portfolio/framework-top-level-build-plan-2026-07-03.md`](portfolio/framework-top-level-build-plan-2026-07-03.md) | Framework Top-Level Build Plan (2026-07-03) | `superseded` | 2026-11-05 |
| [`docs/portfolio/naming-audit-2026-07-03.md`](portfolio/naming-audit-2026-07-03.md) | Naming Audit Report — 2026-07-03 | `superseded` | 2026-11-05 |
| [`docs/portfolio/project-closure-2026-07-18.md`](portfolio/project-closure-2026-07-18.md) | 组合主线关闭记录（当前权威关闭名单） | `active` | 2026-11-05 |
| [`docs/portfolio/project-index.md`](portfolio/project-index.md) | 旧版项目组合索引（2026-07-03，状态已知过时） | `superseded` | 2026-11-05 |
| [`docs/portfolio/rename-proposal-2026-07-03.md`](portfolio/rename-proposal-2026-07-03.md) | P-directory Rename Proposal (Draft 2026-07-03) | `superseded` | 2026-11-05 |
| [`docs/portfolio/restructure-blueprint-2026-07-03.md`](portfolio/restructure-blueprint-2026-07-03.md) | AutoResearch 仓库结构重构蓝图（草案 2026-07-03） | `superseded` | 2026-11-05 |
| [`docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md`](roadmaps/2026-07-03-topic5-autoresearch-roadmap.md) | 2026-07-03 路线图（旧版执行准绳） | `superseded` | 2026-11-05 |
| [`docs/roadmaps/topic5-research-directions.md`](roadmaps/topic5-research-directions.md) | 课题五全量方向规划（历史基线） | `superseded` | 2026-11-05 |
| [`docs/progress/2026-11-05-repo-index-mechanism-progress.md`](progress/2026-11-05-repo-index-mechanism-progress.md) | 仓库级 LLM 索引机制交付与验收（2026-11-05） | `active` | 2026-11-05 |

（本组 18 篇）

### E. AutoResearch 框架、跨项目编排与元评审

> 框架运行材料、跨项目编排规格与路线图 v1.3 元评审。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/analysis/roadmap-v13-meta-review/literature-synthesis.md`](analysis/roadmap-v13-meta-review/literature-synthesis.md) | 双篇路线图 v1.3 文献综合与新发现审查 | `active` | 2026-11-05 |
| [`docs/analysis/roadmap-v13-meta-review/se-review.md`](analysis/roadmap-v13-meta-review/se-review.md) | 路线图 v1.3 系统工程审查 | `active` | 2026-11-05 |
| [`docs/autoresearch/2026-07-03-experiment-configuration-plan.md`](autoresearch/2026-07-03-experiment-configuration-plan.md) | Experiment Configuration Orchestration Plan | `active` | 2026-11-05 |
| [`docs/autoresearch/README.md`](autoresearch/README.md) | AutoResearch 框架与运行材料入口 | `active` | 2026-11-05 |
| [`docs/autoresearch/bootstrap-skills.md`](autoresearch/bootstrap-skills.md) | bootstrap-skills.md | `active` | 2026-11-05 |
| [`docs/autoresearch/orchestrator-prompt.md`](autoresearch/orchestrator-prompt.md) | Deli AutoResearch Orchestrator — WorkBuddy Agent Prompt | `active` | 2026-11-05 |
| [`docs/compose/plans/2026-07-03-cross-project-pitfalls-plan.md`](compose/plans/2026-07-03-cross-project-pitfalls-plan.md) | Cross-Project Pitfall Wiki — Plan (NOT executed) | `active` | 2026-11-05 |
| [`docs/compose/plans/2026-07-03-p12-m1-pre-registration.md`](compose/plans/2026-07-03-p12-m1-pre-registration.md) | P12 Judge Calibration M1 Implementation Plan | `active` | 2026-11-05 |
| [`docs/compose/plans/2026-07-04-p12-m2-m8-execution-plan.md`](compose/plans/2026-07-04-p12-m2-m8-execution-plan.md) | P12 AutoResearch — 6-Step Execution Plan | `active` | 2026-11-05 |
| [`docs/compose/specs/2026-07-16-settlement-reconciliation-paper-design.md`](compose/specs/2026-07-16-settlement-reconciliation-paper-design.md) | Design Spec: Settlement Reconciliation — A Crosswalk Methodology for Calibrating Evidence-to-Factor Settlement Prediction | `active` | 2026-11-05 |
| [`docs/investigations/karpathy-loop-harness-2026-07-07.md`](investigations/karpathy-loop-harness-2026-07-07.md) | Karpathy autoresearch / evaluator-lock 外部 prior art 核查 | `active` | 2026-11-05 |
| [`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`](investigations/meta-uncertainty-and-blindspot-2026-07-07.md) | 元诊断：LLM-on-LLM 自指循环与人类盲点 | `active` | 2026-11-05 |

（本组 12 篇）

### F. 研究计划与调查开题（未归入上述主题）

> 2026-07 早期的方向评估、prior art 核查与开发项目研究调查，按 `kind` 归档于此。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md`](investigations/evidence-snapshot-gap-analysis-2026-07-20.md) | Investigation: 证据快照缺口分析——哪些信息需要补入分析副本 | `active` | 2026-11-05 |
| [`docs/investigations/experiment-success-evaluation-2026-07-08.md`](investigations/experiment-success-evaluation-2026-07-08.md) | 实验成功度评估：对比 7 参考论文 + venue 判定 | `active` | 2026-11-05 |
| [`docs/investigations/first-principles-redesign-feasibility-2026-07-08.md`](investigations/first-principles-redesign-feasibility-2026-07-08.md) | 第一性原理：重新设计实验，能否出标尺级高质量论文？ | `active` | 2026-11-05 |
| [`docs/investigations/kimi-reasoning-attribution-assessment-2026-07-21.md`](investigations/kimi-reasoning-attribution-assessment-2026-07-21.md) | 评估报告：kimi 推演归因方向（"事后补全 kimi 推演 + 逐条归因为什么对"）的学术价值与顶刊差距 | `active` | 2026-11-05 |
| [`docs/investigations/medical-ai-to-cds-mapping-2026-07-18.md`](investigations/medical-ai-to-cds-mapping-2026-07-18.md) | 医学 AI 自动科研方法论能否用于决策科学：映射分析、红队评审与选题论证 | `active` | 2026-11-05 |
| [`docs/investigations/meta-question-recalibration-first-class-paper-2026-07-17.md`](investigations/meta-question-recalibration-first-class-paper-2026-07-17.md) | 用 Nature《How to write a first-class paper》方法论重校本项目元问题 | `active` | 2026-11-05 |
| [`docs/investigations/open-model-cutoff-verification-2026-07-22.md`](investigations/open-model-cutoff-verification-2026-07-22.md) | Investigation: Tsinghua 主力模型训练截止日可证明性复核 + 单模型充分性评估 | `active` | 2026-11-05 |
| [`docs/investigations/optimization-plan-2026-07-07.md`](investigations/optimization-plan-2026-07-07.md) | 优化方案：如何从 LLM-on-LLM 自指循环中进步 | `active` | 2026-11-05 |
| [`docs/investigations/paper-directions-vs-exemplar-bar-2026-07-08.md`](investigations/paper-directions-vs-exemplar-bar-2026-07-08.md) | 基于标尺的论文方向再评估 | `active` | 2026-11-05 |
| [`docs/investigations/repoprompt-ce-agent-triage-2026-07-09.md`](investigations/repoprompt-ce-agent-triage-2026-07-09.md) | RepoPrompt CE Agent Triage — 2026-07-09 | `active` | 2026-11-05 |
| [`docs/investigations/repoprompt-ce-backcompat-bug-triage-2026-07-09.md`](investigations/repoprompt-ce-backcompat-bug-triage-2026-07-09.md) | RepoPrompt CE Back-Compat Bug Triage — 2026-07-09 | `active` | 2026-11-05 |
| [`docs/investigations/repoprompt-ce-bug-localisation-2026-07-09.md`](investigations/repoprompt-ce-bug-localisation-2026-07-09.md) | RepoPrompt CE Bug Localisation — Issue #399 (Supervisor sessions ingest raw child transcripts) | `active` | 2026-11-05 |
| [`docs/investigations/research-for-dev-projects-2026-07-08.md`](investigations/research-for-dev-projects-2026-07-08.md) | 为 3 个开发项目设计研究：第一性原理 + 价值评估 + paper 可行性 | `active` | 2026-11-05 |
| [`docs/investigations/research-for-dev-projects-v2-2026-07-08.md`](investigations/research-for-dev-projects-v2-2026-07-08.md) | 重答 3 项目研究方向（Auto-Research 方法视角）+ 文档清理记录 | `active` | 2026-11-05 |
| [`docs/plans/e1-hallucination-fingerprint-probe-spec-2026-08-02.md`](plans/e1-hallucination-fingerprint-probe-spec-2026-08-02.md) | E1 实验规格：幻觉指纹前瞻探针（Hallucination Fingerprint Probe） | `active` | 2026-11-05 |

（本组 15 篇）

### G. 已关闭组合论文产出（归档）

> `docs/papers-closed-portfolio/` 下 22 篇论文草稿 / 评审 / 摘要，均已随组合主线关闭而归档，不作现状引用。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/papers-closed-portfolio/direction-a-1-page-proposal.md`](papers-closed-portfolio/direction-a-1-page-proposal.md) | 归档：Direction A — 1-Page Proposal: A Unified Anchoring-Bias Taxonomy for LLM-as-a-Judge | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/direction-a-mechanism-experiment-spec.md`](papers-closed-portfolio/direction-a-mechanism-experiment-spec.md) | 归档：Direction A Mechanism Experiment — Detailed Cell Design | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/direction-a-review-round-1.md`](papers-closed-portfolio/direction-a-review-round-1.md) | 归档：Direction A — 5-Persona Review Round 1 (2026-07-05) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/directions-attempt-2026-07-18/d1-g3-standalone-paper-draft.md`](papers-closed-portfolio/directions-attempt-2026-07-18/d1-g3-standalone-paper-draft.md) | 归档：Settlement Reconciliation of LLM-as-Judge Audit Trails: A Dual-Ledger Crosswalk with Murphy-Decomposed Brier Replay | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/directions-attempt-2026-07-18/d2-rescore-card.md`](papers-closed-portfolio/directions-attempt-2026-07-18/d2-rescore-card.md) | 归档：d2-rescore-card.md | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/directions-attempt-2026-07-18/d2-verdict-reversal-paper-draft.md`](papers-closed-portfolio/directions-attempt-2026-07-18/d2-verdict-reversal-paper-draft.md) | 归档：Verdict-Reversal Prediction: Detecting Harness Bugs Before a Reversal Occurs in LLM-as-Judge Audit Trails | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/directions-attempt-2026-07-18/d3-g3-with-harness-ablation-draft.md`](papers-closed-portfolio/directions-attempt-2026-07-18/d3-g3-with-harness-ablation-draft.md) | 归档：Settlement Reconciliation with Harness-Evolution as an Ablation Subsection: A Dual-Ledger Schema-Engineering Paper with an Incremental Harness-Evolution Extension | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/directions-attempt-2026-07-18/d4-cross-direction-joint-paper-synthesis.md`](papers-closed-portfolio/directions-attempt-2026-07-18/d4-cross-direction-joint-paper-synthesis.md) | 归档：D4 — Cross-Direction Synthesis: A Joint Paper Candidate from the Intersection of D1 (Settlement Reconciliation), D2 (Verdict-Reversal Prediction), and D3 (Harness-Evolution Ablation) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g1-abstract-review-zh.md`](papers-closed-portfolio/g1-abstract-review-zh.md) | 归档：G1 — PA-Degrades-Fidelity 摘要 — 6 人评审 | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g1-abstract-review.md`](papers-closed-portfolio/g1-abstract-review.md) | 归档：G1 — PA-Degrades-Fidelity Abstract — 6-Persona Review | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g1-pa-degrades-fidelity-abstract-zh.md`](papers-closed-portfolio/g1-pa-degrades-fidelity-abstract-zh.md) | 归档：G1 — PA-Degrades-Fidelity 顶会摘要（1 页，245 字） | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g1-pa-degrades-fidelity-abstract.md`](papers-closed-portfolio/g1-pa-degrades-fidelity-abstract.md) | 归档：G1 — PA-Degrades-Fidelity 顶会摘要 (1 page) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g2-n30-completion.md`](papers-closed-portfolio/g2-n30-completion.md) | 归档：G2 — N=30 Completion (calibration paradox with 2nd judge) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g2-p12-calibration-paradox-replication-zh.md`](papers-closed-portfolio/g2-p12-calibration-paradox-replication-zh.md) | 归档：G2 — P12 Calibration Paradox 复现（含第二 judge） | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g2-p12-calibration-paradox-replication.md`](papers-closed-portfolio/g2-p12-calibration-paradox-replication.md) | 归档：G2 — P12 Calibration Paradox Replication with Second Judge | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g3-brier-replay-results.md`](papers-closed-portfolio/g3-brier-replay-results.md) | 归档：G3 — Brier Replay with Version-Pair Resolver (v3) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g3-dual-ledger-crosswalk-zh.md`](papers-closed-portfolio/g3-dual-ledger-crosswalk-zh.md) | 归档：G3 — Dual-Ledger Crosswalk（auto-research ↔ cds4worldcup） | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g3-dual-ledger-crosswalk.md`](papers-closed-portfolio/g3-dual-ledger-crosswalk.md) | 归档：G3 — Dual-Ledger Crosswalk (auto-research ↔ cds4worldcup) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/g3-methods-paper-outline.md`](papers-closed-portfolio/g3-methods-paper-outline.md) | 归档：G3 Dual-Ledger Bridge Methods Paper — Outline (Direction A fold target) | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/joint-methods-outline-review.md`](papers-closed-portfolio/joint-methods-outline-review.md) | 归档：Joint Methods Paper Outline — 6-Persona Review | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/joint-methods-paper-outline.md`](papers-closed-portfolio/joint-methods-paper-outline.md) | 归档：A Structured Contract for Verifiable Agent Decisions | `archived` | 2026-11-05 |
| [`docs/papers-closed-portfolio/method-paper-depth-check-prompt.md`](papers-closed-portfolio/method-paper-depth-check-prompt.md) | 归档：The 8 method papers (sorted by relevance to anchoring-bias framing) | `archived` | 2026-11-05 |

（本组 22 篇）

### H. 历史归档调查（归档，per R7 保留可查、不得作现状引用）

> `docs/investigations/archive/` 下 22 篇形成 4 次结论反转的 verdict chain，按 `FRAMEWORK-RULES.md` R7 保留可查，但不得作为当前结论引用。

| 相对路径 | 说明 | status | verified_at |
|---|---|---|---|
| [`docs/investigations/archive/cross-project-roi-2026-07-06.md`](investigations/archive/cross-project-roi-2026-07-06.md) | 归档：跨项目 ROI：研究资产如何帮助 3 个开发项目 + 顶刊机会再评估 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/direction-a-decision-memo-2026-07-05.md`](investigations/archive/direction-a-decision-memo-2026-07-05.md) | 归档：Direction A — Decision Memo (2026-07-05 深夜) | `archived` | 2026-11-05 |
| [`docs/investigations/archive/direction-xyz-prior-art-recheck-2026-07-08.md`](investigations/archive/direction-xyz-prior-art-recheck-2026-07-08.md) | 归档：上一份回答"3 个新方向"的诚实反查 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/first-principles-top-journal-directions-2026-07-05-zh.md`](investigations/archive/first-principles-top-journal-directions-2026-07-05-zh.md) | 归档：第一性原理扫描：潜在的顶刊方向 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/first-principles-top-journal-directions-2026-07-05.md`](investigations/archive/first-principles-top-journal-directions-2026-07-05.md) | 归档：First-Principles Scan: Latent Top-Journal Directions | `archived` | 2026-11-05 |
| [`docs/investigations/archive/high-quality-paper-direction-research-2026-07-08.md`](investigations/archive/high-quality-paper-direction-research-2026-07-08.md) | 归档：高质量 Paper 方向调研（reasoning structure paradigm 切入） | `archived` | 2026-11-05 |
| [`docs/investigations/archive/llm-intelligence-blocker-analysis-2026-07-05.md`](investigations/archive/llm-intelligence-blocker-analysis-2026-07-05.md) | 归档：Investigation: Are the Blockers Caused by Insufficient LLM Intelligence? | `archived` | 2026-11-05 |
| [`docs/investigations/archive/llm-intelligence-blocker-verdict-2026-07-05-zh.md`](investigations/archive/llm-intelligence-blocker-verdict-2026-07-05-zh.md) | 归档：调研结论：当前卡点是否源于 LLM 智力不足？ | `archived` | 2026-11-05 |
| [`docs/investigations/archive/novelty-depth-check-2026-07-05.md`](investigations/archive/novelty-depth-check-2026-07-05.md) | 归档：Novelty Depth-Check: Direction A (Unified Anchoring-Bias Taxonomy for LLM Judges) | `archived` | 2026-11-05 |
| [`docs/investigations/archive/orchestrated-progress-assessment-2026-07-05-zh.md`](investigations/archive/orchestrated-progress-assessment-2026-07-05-zh.md) | 归档：编排化评估：当前 AutoResearch 进展 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/orchestrated-progress-assessment-2026-07-05.md`](investigations/archive/orchestrated-progress-assessment-2026-07-05.md) | 归档：Orchestrated Assessment: Current AutoResearch Progress | `archived` | 2026-11-05 |
| [`docs/investigations/archive/p11-inner-monologue-paper-readiness-2026-07-03.md`](investigations/archive/p11-inner-monologue-paper-readiness-2026-07-03.md) | 归档：Investigation: p1.1 Inner Monologue Paper Readiness | `archived` | 2026-11-05 |
| [`docs/investigations/archive/per-paper-top-journal-2026-07-08.md`](investigations/archive/per-paper-top-journal-2026-07-08.md) | 归档：逐项目顶刊机会审计：是否伪机会 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/post-gate-and-qlib-assessment-2026-07-05.md`](investigations/archive/post-gate-and-qlib-assessment-2026-07-05.md) | 归档：Post-Gate and Qlib Relevance Assessment | `archived` | 2026-11-05 |
| [`docs/investigations/archive/rethink-2026-07-06-zh.md`](investigations/archive/rethink-2026-07-06-zh.md) | 归档：重新思考：基于国家重点研发计划项目背景的顶刊机会再评估 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/rp-investigate-top-journal-2026-07-05.md`](investigations/archive/rp-investigate-top-journal-2026-07-05.md) | 归档：Investigation: AutoResearch Top-Journal Opportunity (Fresh rp-investigate-cli Pass) | `archived` | 2026-11-05 |
| [`docs/investigations/archive/top-journal-kill-falsification-2026-07-06.md`](investigations/archive/top-journal-kill-falsification-2026-07-06.md) | 归档：调研：顶刊 Kill Verdict 反向证伪 + 跨项目增益再评估 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/top-journal-opportunity-reality-check-2026-07-06.md`](investigations/archive/top-journal-opportunity-reality-check-2026-07-06.md) | 归档：调研：上一轮"顶刊机会真实存在"verdict 的反向证伪 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/top-journal-readiness-2026-07-05.md`](investigations/archive/top-journal-readiness-2026-07-05.md) | 归档：Investigation: AutoResearch Top-Journal Readiness | `archived` | 2026-11-05 |
| [`docs/investigations/archive/top-journal-verdict-2026-07-05-zh.md`](investigations/archive/top-journal-verdict-2026-07-05-zh.md) | 归档：调研结论：auto-research 项目能否冲击顶刊？ | `archived` | 2026-11-05 |
| [`docs/investigations/archive/toutiao-article-7659624555010392639-2026-07-08.md`](investigations/archive/toutiao-article-7659624555010392639-2026-07-08.md) | 归档：头条文章 ID 7659624555010392639 调研 + 项目方向再思考 | `archived` | 2026-11-05 |
| [`docs/investigations/archive/toutiao-harness-evolution-2026-07-08.md`](investigations/archive/toutiao-harness-evolution-2026-07-08.md) | 归档：头条文章解读 + 投射到本项目 AutoResearch Harness | `archived` | 2026-11-05 |

（本组 22 篇）


## 待裁定：状态口径冲突（只标注，不改原文）

> 以下 5 处冲突逐条回查过原文，均**只列清单、不修改任何原文**。遇到冲突时以 [`../CLAUDE.md`](../CLAUDE.md)「当前活跃主线」表为状态准绳，但不得擅自替用户二选一；需裁定时提交用户。每条附两条（或以上）互相矛盾的原文摘录，位置统一 `path:line`。

### C1 — 世界杯主线口径：双论文 v1.7 / 开题 v2.1 vs 单篇开题 v1.3 + 已挂起

- `README.md:5`：「**▶ 当前主线（2026-09-25 已挂起、投稿暂停）：世界杯双论文路线（2026-07-21 用户裁定拆分；v1.7 路线图 2026-07-26）**……开题 v2.1」
- `CLAUDE.md:7`（2026-11-05 当前磁盘）：「**当前主线（2026-09-25 起挂起、投稿暂停）：世界杯算法比较实证论文**（用户裁定 2026-07-20，以开题报告为主线）」
- `CLAUDE.md:7`（HEAD 历史引文，仅作证据保留，非当前状态；可经 `git show HEAD:CLAUDE.md | sed -n '7p'` 回溯）：「**当前活跃主线：世界杯算法比较实证论文**（用户裁定 2026-07-20，以开题报告为主线）」
- `CLAUDE.md:11`：「⏸ **2026-09-25 用户决定：世界杯双论文研究挂起、投稿暂停（无限期）**」
- 冲突点：活跃/挂起表述已由 2026-11-05 外部改动消解（`README.md:5` 与 `CLAUDE.md:7` 均已补「已挂起 / 投稿暂停」标注，与 `CLAUDE.md:11` 一致）；剩余分歧为主线版本口径（双论文 v1.7 / 开题 v2.1 vs 单篇开题 v1.3）。**裁定：待裁定。**

### C2 — 组合主线状态：P12「新建，短期优先」活跃任务顺序 vs 2026-07-18 已关闭

- `docs/portfolio/project-index.md:3`：「更新日期：2026-07-03 / 用途：让根目录一眼看清每条实验线的角色、状态和下一步」
- `docs/portfolio/project-index.md:27`：「`papers/p12-judge-calibration` | P12 Judge 校准 | **新建，短期优先** | 从 P11 抽 sample manifest」
- `docs/portfolio/project-index.md:36`：「1. **P12 Judge Calibration**：新建目录，作为短期主任务。」
- `CLAUDE.md:7`：「**组合主线已于 2026-07-18 关闭**（`docs/portfolio/project-closure-2026-07-18.md`），当前处于关闭后孵化期」
- 冲突点：旧索引给出活跃任务顺序，项目地图记录已关闭。**裁定：待裁定。**

### C3 — investigations 索引停在 2026-07-08，未收录 2026-10 的 token-* / tsinghua-* 系列

- `docs/investigations/INDEX.md:3`：「**Last cleaned: 2026-07-08.** 6 canonical docs kept current; 22 stale verdict-chain / intermediate docs archived under `archive/`」
- `docs/investigations/INDEX.md:6`：「## Canonical (read these first — current state)」（第 8–17 行的 6+1 条 canonical 清单不含任何 2026-10 文档）
- 磁盘实存佐证：`docs/investigations/token-report-2026-10-27.md`、`docs/investigations/tsinghua-1025-vs-may-2026-10-27.md`（2026-10 新增报告，未被 canonical 收录）
- 冲突点：自称 current state 的清单缺 2026-10 约 20 篇新文档。**裁定：待裁定。**

### C4 — analysis/README.md 称 worldcup-2026/ 待建，实际已存在并运行到 2026-09-11

- `analysis/README.md:17`：「| `worldcup-2026/`（**待建**） | `evidence/cds4worldcup-snapshot-2026-07-20/` | 计划 W1 建立，见 `docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` |」
- `analysis/worldcup-2026/CHANGELOG.md:1`：「# CHANGELOG — analysis/worldcup-2026/」
- `analysis/worldcup-2026/CHANGELOG.md:5`：「## 2026-09-11（Paper A 连贯工作稿 · 不改证据）」
- 冲突点：README 说待建，目录已存在且含 CHANGELOG、2 个 .py 与多篇工作稿；`analysis/` 另有 23 个一级子目录、185 个 .py。**裁定：待裁定。**

### C5 — state/progress.json 的 status 停在 W6 备忘录阶段（metadata drift）

- `CLAUDE.md:23`：「⚠️ 状态口径警告（2026-07-20）：`state/progress.json` 的 **status 字段停在 W6 备忘录阶段，未同步 v1.3 主线裁定**（metadata drift）。课题状态以本表为准」
- `state/progress.json:3`：`"status": "PAUSED_2026_07_20_worldcup_paper_topic_W6_GO_with_8_gates_pending_A0_final_settlement"`
- `CLAUDE.md:7`（2026-11-05 当前磁盘）：「当前主线（2026-09-25 起挂起、投稿暂停）：世界杯算法比较实证论文（用户裁定 2026-07-20，以开题报告为主线）」
- `CLAUDE.md:7`（HEAD 历史引文，仅作证据保留，非当前状态；可经 `git show HEAD:CLAUDE.md | sed -n '7p'` 回溯）：「当前活跃主线：世界杯算法比较实证论文（用户裁定 2026-07-20，以开题报告为主线）」
- 冲突点：CLAUDE.md 自报 metadata drift，state 文件仍是 W6 阶段 status。**裁定：待裁定。**

## 数据产物区

| 区 | 文件数 | 定性 | 访问规则 |
|---|---|---|---|
| `docs/papers-closed-portfolio/experiments/` | 2268 | **历史实验数据产物**（.txt / .json 为主），**非讨论文档** | 只读登记；不写入、不逐条索引、不参与 `docs[]` 扫描 |

`docs/` 索引建立前基线共 2474 个文件（2026-11-05 交付后当前 2479），其中 2268 个在此数据区；若不单列隔离，会把 171 篇讨论文档淹没在数据噪声里，这正是「查资料不准」的另一来源。`index.json` 的 `data_zones` 亦登记此区。

## 只读登记区

> `evidence/` 与 `legacy/` **仅做只读登记**，不深挖 `legacy/` 的 2322 篇历史 md、不写入。证据快照为字节级只读；封存仓库 `/Users/tangzw119/Documents/GitHub/cds4worldcup` 零读写，任何进程不得碰。

| 区 | 磁盘全量 | git 已跟踪 | md | py | 访问规则 |
|---|---|---|---|---|---|
| `evidence/` | 850 | 432 | 337 | 37 | 证据快照，字节级只读：禁止任何修改（含删 `.DS_Store`、格式化、重命名）；深遍历会拖慢，只做摘要登记；引用其中文件须注明「证据快照」 |
| `legacy/` | 11723 | 74 | 2322 | 39 | 只读登记；不深挖历史 md、不写入、不重命名 / 移动内部文件 |
| `papers/` | 213 | 204 | 76 | 22 | 高引用区，只读；含 4 个 `papers/*/wiki/index.md` 历史索引 |
| `framework/` | 20 | 17 | 8 | 3 | 只读 |
| `state/` | 6 | — | 2 | 0 | 高引用只读区；`state/progress.json:3` 见冲突 C5 |
| 封存仓库（`../cds4worldcup`，仓库外部） | — | — | — | — | **零读写，无一例外** |

## 索引再生与维护

- 固定再生脚本：[`tools/build_index.py`](tools/build_index.py)（置于 `docs/tools/` 的理由：与讨论文档隔离，避免被 `docs[]` 误收为讨论文档，也避免脚本自指循环）。
- 三种模式：`python3 docs/tools/build_index.py`（默认，写回且幂等）、`--dry-run`（不写回）、`--check`（只校验 `index.json` 全部 `path` 是否仍存在并输出失效清单）。
- 扫描约定：只读扫描 `docs/` 主干子目录与 `analysis/`（**限深 3**）；排除 `docs/papers-closed-portfolio/experiments/` 数据区、隐藏目录、`docs/` 顶层文件；**不深遍历 `evidence/`、`legacy/`、`papers/`、`framework/`**（`analysis/` 全量约 85000 文件，不限深会导致进程被 SIGTERM）。
- 字段分工：骨架字段（`path` / `mtime` / `size` / `heading` / `kind` / `capability` / `workdir`）每次按磁盘刷新；**人工维护字段（`status` / `topic` / `verified_at` / `supersedes` / `title` / `related_scripts` / `related_docs` / `purpose` / `reusable`）绝不覆盖**，可直接编辑 `index.json`。
- 无第三方依赖，macOS / Python 3 直接可跑。

## 维护约定

- 新增讨论文档沿用既有英文路径命名 `<topic>-<YYYY-MM-DD>.md`，正文中文，路径与既有英文命名保持不变。
- 新增页运行一次 `python3 docs/tools/build_index.py` 登进 `index.json`，再人工补 `status` / `topic` / 说明。
- `docs/` 顶层文件（`INDEX.md`、`SCRIPTS.md`、`SECRETS.md`）不进 `docs[]`；`docs/SECRETS.md`、`.env` 为敏感内容，不索引、不外传。
- 不做超出范围的「顺手优化」；不输出投注建议、不报告收益率。
