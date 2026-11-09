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


## 逐篇清单（已下移 · 2026-11-09 做梦 D4）

> 171 篇主干讨论文档的逐篇表格（原 A–H 节）已移至 [`INDEX-DETAILS.md`](INDEX-DETAILS.md)；精确字段仍以 [`index.json`](index.json) 为准，查询顺序不变。
> 185 个脚本的清单已移至 [`SCRIPTS-DETAILS.md`](SCRIPTS-DETAILS.md)；需要脚本时先查 [`SCRIPTS.md`](SCRIPTS.md) 的 capability 索引。
> 记忆做梦 wiki **总览 / 索引页**：[`WIKI-INDEX.md`](../analysis/memory-dream-2026-11-09/WIKI-INDEX.md)（五页地图、跨簇关系、使用规则）。会话起始记忆索引：[`MEMORY.md`](MEMORY.md)（入库，由 `../CLAUDE.md` 入口指向，权威值以此页为准）。
> 主题导航（dreaming wiki）：[世界杯主线](../analysis/memory-dream-2026-11-09/worldcup-wiki.md) ｜ [Decision Co-Scientist](../analysis/memory-dream-2026-11-09/coscientist-wiki.md) ｜ [2026-10 token / tsinghua](../analysis/memory-dream-2026-11-09/oct2026-wiki.md) ｜ [组合治理](../analysis/memory-dream-2026-11-09/governance-wiki.md)。
> 本轮只移动结构、不改动任何状态口径文字；原页字节级备份见 [`backup/`](../analysis/memory-dream-2026-11-09/backup/)；授权：用户 2026-11-09「均同意」。

## 待裁定：状态口径冲突（只标注，不改原文）

> 以下 5 处冲突逐条回查过原文，均**只列清单、不修改任何原文**。遇到冲突时以 [`../CLAUDE.md`](../CLAUDE.md)「当前活跃主线」表为状态准绳，但不得擅自替用户二选一；需裁定时提交用户。每条附两条（或以上）互相矛盾的原文摘录，位置统一 `path:line`。

> 5 处冲突的明细（原文逐字保留）见 [`INDEX-DETAILS.md`](INDEX-DETAILS.md)。顶层只留索引，不擅自裁决：

- C1 — 世界杯主线口径：双论文 v1.7 / 开题 v2.1 vs 单篇开题 v1.3 + 已挂起 ｜ **裁定：待裁定**（明细见 `INDEX-DETAILS.md`）
- C2 — 组合主线状态：P12「新建，短期优先」活跃任务顺序 vs 2026-07-18 已关闭 ｜ **裁定：待裁定**（明细见 `INDEX-DETAILS.md`）
- C3 — investigations 索引停在 2026-07-08，未收录 2026-10 的 token-* / tsinghua-* 系列 ｜ **裁定：待裁定**（明细见 `INDEX-DETAILS.md`）
- C4 — analysis/README.md 称 worldcup-2026/ 待建，实际已存在并运行到 2026-09-11 ｜ **裁定：待裁定**（明细见 `INDEX-DETAILS.md`）
- C5 — state/progress.json 的 status 停在 W6 备忘录阶段（metadata drift） ｜ **裁定：待裁定**（明细见 `INDEX-DETAILS.md`）
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
