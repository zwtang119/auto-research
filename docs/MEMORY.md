# docs/MEMORY.md — 项目会话起始记忆索引（入库 · 权威）

> 建立：2026-11-09 dreaming pass #1；**方案 A 接入后**由 [`../CLAUDE.md`](../CLAUDE.md) 入口直接指向。硬上限 200 行 / 25 KB。
> **本页不是 Agent 入口。** 本仓唯一 Agent 入口是 `AGENTS.md → CLAUDE.md`；本页是 CLAUDE.md 导航到的记忆索引，随仓库同步。
> 定位：只放「下次会话必须知道、且不会频繁变的事实」与「去哪找详情」。事件写当日日志，本页只留链接。
> 状态准绳：`CLAUDE.md`「当前活跃主线」表。**本页不裁决 C1–C5，不改任何状态口径原文。**
> 依据：Anthropic《The components of agent memory》——顶层注入必须小；wiki 是导航层，search 才是取回层；dreaming 的输出必须落到未来会话可达的位置。

## 1. 下次会话先读这三条

1. **状态口径以 `CLAUDE.md` 表为准**：世界杯双论文研究 2026-09-25 起挂起、投稿暂停（无限期）；DORMANT / PARK / 想法记录 ≠ 关闭。`state/progress.json` 有 metadata drift，不可当准绳。
2. **查资料先走索引**：[`INDEX.md`](INDEX.md) → [`index.json`](index.json) → [`SCRIPTS.md`](SCRIPTS.md)；逐篇清单与 C1–C5 明细已下移到 [`INDEX-DETAILS.md`](INDEX-DETAILS.md)、脚本明细在 [`SCRIPTS-DETAILS.md`](SCRIPTS-DETAILS.md)（2026-11-09 结构下移，文字逐字未改）。
3. **主题 wiki 导航**：[`WIKI-INDEX.md`](../analysis/memory-dream-2026-11-09/WIKI-INDEX.md)。需要结论先看这页，需要证据再按各页 `path:line` 回原文——**wiki 不替代原文检索**。

## 2. 四层记忆地图（本仓真实落地位置）

| 层 | 位置 | 规则 |
|---|---|---|
| Injected context | [`AGENTS.md`](../AGENTS.md) → [`CLAUDE.md`](../CLAUDE.md)（**真正预加载的入口**）→ 本页（1 行导航） | 总注入 ≤200 行 / 25 KB；只留链接与稳定事实 |
| Memory representations | [`WIKI-INDEX.md`](../analysis/memory-dream-2026-11-09/WIKI-INDEX.md) + 5 页主题 wiki + [`INDEX.md`](INDEX.md) | 一主题一页，单页 ≤8 KB；增量维护，不满 10% 源簇体积 |
| Memory notes | 本页「已纠错」节 + `.workbuddy/memory/YYYY-MM-DD.md`（本地、append-only） + 各文档「结论/状态」段 | 事实变更写日志，不在本页堆叠同义条目 |
| Transcripts / ground truth | `docs/investigations/`、`docs/plans/`、`analysis/` 原文、会话记录 | 任何断言回查 `path:line` 后入档；`evidence/` 为字节级原始 |

> ⚠️ `.workbuddy/` 被 `.gitignore:6` 忽略，**不随仓库同步**。本地镜像 `.workbuddy/memory/MEMORY.md` 只供 WorkBuddy 会话使用，权威值一律以本页为准；换机器 / 换 agent 时以本页为唯一来源。

## 3. 主题 wiki 入口（五页）

| 主题 | 页 | 覆盖 |
|---|---|---|
| Token 核算（pilot） | [`token-accounting-wiki.md`](../analysis/memory-dream-2026-11-09/token-accounting-wiki.md) | 10 篇 token-* → 4 个不可相加口径 + 8 陷阱 |
| 世界杯主线 | [`worldcup-wiki.md`](../analysis/memory-dream-2026-11-09/worldcup-wiki.md) | A 簇 20 篇 |
| Decision Co-Scientist | [`coscientist-wiki.md`](../analysis/memory-dream-2026-11-09/coscientist-wiki.md) | B 簇 26 篇 |
| 2026-10 token / tsinghua / reprompt | [`oct2026-wiki.md`](../analysis/memory-dream-2026-11-09/oct2026-wiki.md) | C 簇 36 篇 |
| 组合治理 / 终裁链 / 索引机制 | [`governance-wiki.md`](../analysis/memory-dream-2026-11-09/governance-wiki.md) | D 簇 19 篇 |

## 4. 已纠错的记忆（旧值作废，勿再引用）

> 2026-11-09 dreaming pass #1 以磁盘与原文为 ground truth 复核，以下旧断言**已作废**；日志保留原文供追溯，权威值以本节为准。

| 作废断言（位置） | 实测权威值 | 复核方式 |
|---|---|---|
| 严口径注入做梦前「63.5 KB / **468 行**」（`2026-11-09.md:20`） | **63.5 KB / 471 行** | `AGENTS.md` 3 + `CLAUDE.md` 73 + 备份 `INDEX.md.orig` 395 行 |
| 「19 条 `evidence/` 内 `file://` 历史链接」（`2026-11-09.md:12`、规划 §8） | 全仓 `file://` **17** 条，其中 `evidence/` 内 **14** 条、`docs/` 内 3 条 | 全仓正则重扫，按来源目录分组 |
| 「全仓 D1–D5 未执行，等用户放行」（`2026-11-09.md:10`） | **已被同日续 supersede**：用户「均同意」后 P1/P2/P3 已执行完成 | 同文件第 14 节 + 磁盘产物清单 |
| 「项目记忆目录不存在，`.workbuddy/memory/` 未建立」（规划 §3） | **已建立**：本页 + 本地镜像 + `2026-11-09.md` | 磁盘存在性 |
| 「710 条内部链接」（`link-audit.md` 旧汇总、`2026-11-09.md:19`） | **762** 条（pass #2 后复扫，见 §11）；B192 / W0 / E17、待处理 209 条；演进 710 → 731 → 761 → 762 | 全仓重扫，新增链接双基准全部可达 |
| 本地镜像自称「**会话起始记忆的唯一权威索引**」（2026-11-09 补做时的 `.workbuddy/memory/MEMORY.md:3`） | **作废**：真实唯一入口是 `AGENTS.md → CLAUDE.md`；权威页是本页 | `AGENTS.md` 原文 + `git check-ignore .workbuddy/` + 本会话实际注入内容 |

**做梦后实测（权威值，勿再写旧数）**：严口径注入做梦前 **63.5 KB / 471 行**，做梦后（方案 A 前）**20.5 KB / 198 行**（AGENTS 3 + CLAUDE 73 + `docs/INDEX.md` 122）；宽口径 6 文件 **30.7 KB / 324 行**。`docs/INDEX.md` 57.0→14.0 KB、`docs/SCRIPTS.md` 48.5→3.6 KB。原 395+346 行逐字守恒 0 丢失，状态口径关键行 20/20 留存。

## 5. 未决项（不擅自二选一）

- `build_index.py --check` **exit=1（pre-existing，非本轮造成）**：362 条 path 中 183 条失效（182 `scripts` + `state/`）。`docs[]` 171/171 有效；`scripts[]` 182/185 失效。根因是这批脚本目录在当前 worktree 不落盘（B1 断链去掉 `../` 后与失效 scripts 交集 100%），**不是链接写错**。`index.json` 未改（`generated_at` 2026-11-05）。处置待用户裁定：恢复资产，还是标注「历史登记、当前环境不适用」。
- C1–C5 状态口径冲突：全部「待裁定」，只标注不裁决、不改原文。
- W 类 128 条路径基准已统一（当前 0）；B 类 192 条仍在（其中 182 条已由 `local_only` 分类、非「丢失」），E 17 条字节级只读：见 [`link-audit.md`](../analysis/memory-dream-2026-11-09/link-audit.md)。C2/C3/C4/C5 已标「历史登记、不作状态口径」；**C1 已于 2026-11-09 由用户裁定：以 README.md:5 的双论文路线 v1.7 / 开题 v2.1 为准**，单篇开题 v1.3 降为历史版本。
- 未做检索评测（无 25 题 graded criteria），**不得引用文章 13%→48% / 54%→61% 作为本仓收益**。

## 6. 禁区（继承 `CLAUDE.md`）

`evidence/`（字节级原始，含 `.DS_Store` 永不修改）、封存仓库 `/Users/tangzw119/Documents/GitHub/cds4worldcup`（零读写）、`legacy/` `papers/` `framework/` `state/` 只读；`docs/SECRETS.md`、`.env` 敏感不入库。C1–C5 与 `README.md` / `CLAUDE.md` / 各 `INDEX.md` 的状态口径正文「只标注不改原文」（用户 2026-11-05 裁定）。

## 7. 记忆增长规则（2026-11-09 从两次失败反思改写）

> 第一次把「做梦」做成了体检 + 索引工程 + 对比报告，纠错降级为「只列清单交用户裁定」；第二次补做了纠错，却把权威页建在被 `.gitignore` 忽略、且不在 `AGENTS.md → CLAUDE.md` 入口链上的本地目录，并错误自称「唯一权威索引」。文章定义里 dreaming 是**写入并重组未来可用记忆**的离线 compute，不是产出报告、也不是建一个没人会读的文件。以下规则防止复发。

1. **验收标准**：一次 dreaming 结束时必须能回答「沿 `AGENTS.md → CLAUDE.md` 走，下次会话打开哪个文件会得到正确答案」。答不出＝没做。产物必须落在**真实入口链可达且随仓库同步（入库）**的位置；本地被忽略的目录、纯报告目录都不算。
2. **纠错必须闭环**：拿 transcript / 原文 / 磁盘当 ground truth 校验现有 notes，发现错误后**在权威层写明作废并给出新值**；「只出待裁定清单」不算纠错。日志 append-only，旧行保留、追加更正段并指向本页。
3. **数字先复核再入记忆**：聚合数字（行数、断链率、压缩比）写入前重算；验证脚本自身会错（本轮已有 21 条硬错误误报、2 条示例文本自指假阳性、口径基准不一致导致 53.0% 虚高的先例）。口径变更要标演进，不静默覆盖。
4. **顶层保持小**：新记忆优先更新本页对应条目，不追加同义内容；超过 200 行 / 25 KB 就把细节下移、留链接。
5. **wiki 是地图不是摘要库**：一主题一页、单 agent 写、链回原文 `path:line`；不与 search 竞争，不追求覆盖率。
6. **不越权**：不裁决 C1–C5、不改状态口径文字、不重建 `index.json`、不批量改链；commit / push 均需用户明确指令，两步不可互相推定。2026-11-09 用户先授权「按 A 执行／合并 worktree」（本地），随后单独授权「推送 Github」；执行状态见 §10。

## 8. 可追溯入口

- 规划：[`docs/plans/memory-dream-2026-11-09.md`](plans/memory-dream-2026-11-09.md)｜对比：[`COMPARISON.md`](../analysis/memory-dream-2026-11-09/COMPARISON.md)
- 校验清单：[`notes-audit.md`](../analysis/memory-dream-2026-11-09/notes-audit.md)、[`link-audit.md`](../analysis/memory-dream-2026-11-09/link-audit.md)｜增补登记：[`CHANGELOG.md`](../analysis/memory-dream-2026-11-09/CHANGELOG.md)
- 索引原页字节级备份：[`backup/`](../analysis/memory-dream-2026-11-09/backup/)（`.orig` 三件，可逐字节回滚）
- 当日事件：`.workbuddy/memory/2026-11-09.md`（本地，不入库）

## 9. 方案 A 接入记录（2026-11-09）

- `CLAUDE.md` 新增 1 行导航指向本页；原有 73 行与状态口径文字**零改动**。
- [`INDEX.md`](INDEX.md) 第 74 行、[`WIKI-INDEX.md`](../analysis/memory-dream-2026-11-09/WIKI-INDEX.md) 改指本页，不再指向被忽略的本地目录。
- `.workbuddy/memory/MEMORY.md` 降级为 WorkBuddy 本地镜像，删除错误自述，只留指向本页的链接。
- 注入链：`AGENTS.md → CLAUDE.md → docs/MEMORY.md`（入库，跨机器同步）；本页 ≤25 KB / 200 行。

- 全仓复扫：内部链接 731 → **761**（+30），B192 / W128 / E17、待处理 337 条不变；残留指向被忽略本地目录的链接 0 条。


## 10. 提交与同步状态（2026-11-09，权威值）

- 本地提交 `a1f480b`（做梦 pass #1 + 方案 A，20 文件）已由用户「推送 Github」授权推至 `origin/main`；`git push` 输出 `f592df4..a1f480b`、退出码 0，并由 GitHub 通道独立复核远端 `main` HEAD = `a1f480bfe769fd496df716a9802a4f5a89d605bb`。
- 主工作区 `git merge --ff-only` 已完成；`main`、`workbuddy/main-92053ddb`、`origin/main` 三者同指，ahead/behind = 0/0。
- **主工作区原有 22 条未提交改动（4 tracked 修改 + 18 未跟踪）不在此提交内**，仍保持本地未提交状态；不要误判为已同步。
- 作废声明：`COMPARISON.md` §7.4 / §8.3、`CHANGELOG.md` 各续、以及 `a1f480b` 提交信息里「未 commit/push」「未 push」均为**当时状态**，推送后已失效，以本节为准。历史行按 append-only 保留，不回改。
- 本节为「同步状态」唯一权威入口；后续推送 / 合并只更新本节对应条目，不新增同义页。
- ✅ **2026-11-09 pass #2 已获用户「提交并推送到 GitHub」明确授权**：执行后远端 `main` 为 `c2acd3a` 之后的新提交，具体 sha 以 `git log -1` / 远端 HEAD 为准（本节不写死 sha，避免数字漂移）。改动含 `docs/index.json`、`docs/tools/build_index.py`、7 个 W 类链接文件、`CLAUDE.md` 三行状态口径对齐及若干记录。


## 11. pass #2 权威状态（2026-11-09，按根因建议执行）

- `docs/index.json` 增 `local_only`（183 条）：182 个 `analysis/` 脚本从未入库 + `state/` 被 `b378f00` 移出 git 并 `.gitignore:31` 忽略。`--check` 现按环境分类，worktree / 主工作区均 exit=0，真实失效 0。
- `docs/tools/build_index.py` 三处：`mode_check` 分类、`compose` 保留 `local_only`、默认 regenerate 写回防护（在 worktree 内 exit=3、不写回）。
- W 类链接 **128 → 0**（7 文件 / 112 行，试运行 + 备份 + 逐字节验收全过）。当前内部链接 **762** / B192 / W0 / E17 / 待处理 209；演进 710 → 731 → 761 → 762。
- 15 个未跟踪 `analysis/` 目录**判否、不入库**：约 30.4 GB / 32 万文件、含 `.env` 真实 API Key 与 venv，仓库 public；是否指定白名单待用户裁定。
- C2/C3/C4/C5 标「历史登记、不作状态口径」；**C1 已裁定**：以 README.md:5 双论文 v1.7 / 开题 v2.1 为准，`CLAUDE.md:8/16/23` 已按裁定对齐，原文备份在 `backup/CLAUDE.md.pre-c1.orig`。
- 新建 `analysis/memory-dream-2026-11-09/eval-set-draft.md`（25 题草案）；**用户 2026-11-09 判定不做检索评测，草案仅存档、不执行**；C7 标准答案按 C1 裁定定稿但不使用。opencode 临时 worktree 已清理，可用 `worktree add --detach … b378f00` 重建。
- 本轮提交与推送已获用户明确授权；同步状态以 §10 为准（本节不写死 sha，避免数字漂移）。


### 补记：D4 逐字守恒结论的 1 行例外（2026-11-09 pass #2）

- 此前「原 395 + 346 行逐字守恒、丢失/改写 0 行」**现需修正**：本轮 W 类统一把 `docs/INDEX.md:63` 的自指链接从 `docs/INDEX.md` 改为 `INDEX.md`，原 395 行中该行不再逐字出现；`SCRIPTS.md` 仍为 0 丢失。
- 终态实测：`INDEX.md` 原 395 行 → 丢失/改写 **1 行**；`SCRIPTS.md` 原 346 行 → **0 行**。改写前顶层原页字节级备份在 `backup/w-links/INDEX.md.orig`（D4 之前的完整 395 行原页仍在 `backup/INDEX.md.orig`）。
- 性质：只改链接目标，非状态口径文字；状态口径关键行 18/18 逐字留存。历史结论保留在本页前文，以此补记为准。
