# CHANGELOG — analysis/memory-dream-2026-11-09/

按 `CLAUDE.md` 三级证据结构：分析副本可写，所有增补逐条登记。**本目录为新增，不含任何证据快照内容，不修改任何既有文件。**

## 2026-11-09（记忆「做梦」pilot）

| 时间 | 增补 | 文件 | 来源 / 依据 | 性质 |
|---|---|---|---|---|
| 14:19 | 新建 | `token-accounting-wiki.md` | `docs/investigations/token-*.md` 10 篇原文，逐条回查 `path:line` | dreaming 产物（representation 层）；导航页，非原文替代品 |
| 14:19 | 新建 | `COMPARISON.md` | 本地只读脚本实测（文件数/字节/行/链接双基准/md5） | 对比与验收报告 |
| 14:19 | 新建 | `CHANGELOG.md` | 本文件 | 增补登记 |
| 14:19 | 新建（目录外） | `docs/plans/memory-dream-2026-11-09.md` | Anthropic《The components of agent memory》2026-11-06 + 本仓实测基线 | 全仓做梦规划（未执行） |

## 只读边界核对

- 读取：`docs/investigations/token-*.md`（10 篇）、`docs/plans/` 部分文档头、`docs/INDEX.md`、`CLAUDE.md`、`README.md`、`AGENTS.md`、`OBSOLETE.md`、`docs/SCRIPTS.md`。
- **未写入**：以上任何既有文件；写入前后 17 个关键文件 md5 一致。
- **未触碰**：`evidence/`（字节级只读）、`legacy/`、`papers/`、`framework/`、`state/`、`docs/SECRETS.md`、`.env`、外部封存仓库 `/Users/tangzw119/Documents/GitHub/cds4worldcup`（零读写）。
- **未执行**：删除、移动、重命名、git commit/push、实验复算、外部模型调用。
- 状态口径冲突 C1–C5：仅按 `docs/INDEX.md` 原登记引用，**未裁决、未写回任何状态正文**。

## 测量口径备注

- 断链采用双基准（相对 md 目录 + 相对仓库根）；单基准 53.0% 为虚高值，修正后 32.9%（209/636）；128 条为路径写法不一致。
- 全仓 md 的 mtime 为 worktree 检出时间，不用于判断陈旧。
- 数字均为本地实测，未引用项目自评数字；论文/账本数字未独立复算，仅转录并标注原文位置。

## 2026-11-09（14:2x 全仓 P1/P2/P3，用户「均同意」）

| 增补 | 文件 | 依据 / 方法 |
|---|---|---|
| 新建 | `notes-audit.md` | 171 篇 `docs[]` 机器规则校验 + 分级复核；A1 / B17 / C20，首轮误报已降级并留档 |
| 新建 | `worldcup-wiki.md` / `coscientist-wiki.md` / `oct2026-wiki.md` / `governance-wiki.md` | 四簇 A20 / B26 / C36 / D19，逐篇抽取原文标题与结论行，五节固定结构，均 ≤8KB |
| 新建 | `link-audit.md` | 写回后全仓重扫，双基准，337 条 100% 分类；自洽循环生成；含 D5 根因节 |
| 新建 | `COMPARISON.md` §7 | 全仓执行前后对比与验收结论 |
| **修改（授权内）** | `docs/INDEX.md`、`docs/SCRIPTS.md` | 仅结构下移：逐篇表格与 C1–C5 明细移到新增 `docs/INDEX-DETAILS.md` / `docs/SCRIPTS-DETAILS.md`；**状态口径文字 0 改动**，逐字守恒 395+346 行 0 丢失 |
| 新建 | `backup/INDEX.md.orig`、`backup/SCRIPTS.md.orig`、`backup/index.json.orig` | 写入前字节级备份，可逐字节回滚 |

- 写入前试运行不写回；备份后写回；写回后与 `.orig` 逐行逐字比对（Counter 守恒）；修复后重测。
- 只读核对：`build_index.py --check`（只读模式，退出码 1，183 条 pre-existing 失效 path，未修改 `index.json`）。
- 全仓既有文件改动仅上述 2 个；其余 15 个关键文件 md5 不变；禁区零读写；未 commit/push。
- **未完成**：W 类 128 条写法统一、B 类断链修复、`index.json` 重建、C1–C5 裁决、检索评测。

## 2026-11-09（三续：补做 dreaming pass #1，用户质疑后）

| 增补 | 文件 | 依据 / 性质 |
|---|---|---|
| 新建 | `WIKI-INDEX.md` | 五页 wiki 的 index + 跨簇地图；对应文章 Figure 15「补 index」；导航层，≤8KB |
| 新建（目录外） | `.workbuddy/memory/MEMORY.md` | 顶层注入 header / 权威索引；含 4 条旧断言作废声明与 6 条记忆增长规则 |
| 追加 | `.workbuddy/memory/2026-11-09.md` | append-only 更正段，旧错误行保留但声明作废 |
| 修改（授权内，仅增 1 行） | `docs/INDEX.md` | 顶层导航补 WIKI-INDEX / MEMORY.md 链接；原有 122 行逐字未动，状态口径文字 0 改动 |
| 追加 | `COMPARISON.md` §8、`CHANGELOG.md` 本节 | 真做梦 pass 的性质判定、前后对比与登记 |

- ground truth：备份 `.orig` 三件、磁盘实际文件、全仓正则重扫；4 条旧断言作废均附复核方式（见 `MEMORY.md §4`）。
- 不改：C1–C5 原文、`docs/index.json`、`README.md` / `CLAUDE.md` 状态正文、任何只读区；未 commit/push。
- 复扫维护：`link-audit.md` 汇总 710 → **731**（新增 21 条链接全部可达），B192 / W128 / E17 / 待处理 337 不变；同步更新 `COMPARISON.md`、`WIKI-INDEX.md`、`MEMORY.md §4` 的同一数字，避免 representation 残留过时值。

## 2026-11-09（四续：方案 A，用户「按 A 执行」）

| 增补 | 文件 | 依据 / 性质 |
|---|---|---|
| 新建 | `docs/MEMORY.md` | 入库权威记忆索引，≤25KB/200行；由 `CLAUDE.md` 入口指向；含 6 条作废声明与 6 条增长规则 |
| 修改（仅新增 1 行） | `CLAUDE.md` | 顶部增「会话起始先读 docs/MEMORY.md」导航；HEAD 原有 73 行逐字保留，状态口径 0 改动 |
| 修改 | `docs/INDEX.md:74` | 会话起始记忆索引改指入库页 |
| 修改 | `WIKI-INDEX.md` 第 4 / 46 行 | 上游入口与未决项引用改指入库页 |
| 覆盖重写（本地、gitignored） | `.workbuddy/memory/MEMORY.md` | 降级为 WorkBuddy 本地镜像，删除错误自述 |
| 复扫维护 | `link-audit.md` / `COMPARISON.md` / `WIKI-INDEX.md` / `docs/MEMORY.md` | 内部链接 731 → 761，B/W/E 分类不变 |

- 授权：用户 2026-11-09「按 A 执行，完毕后检查 Github 是否已经推送，检查并合并 worktree」。
- 不改：C1–C5 状态口径原文、`docs/index.json`、`README.md`、任何只读区；未 push。


## 2026-11-09（五续：推送 Github，用户「推送 Github」）

| 增补 | 文件 | 依据 / 性质 |
|---|---|---|
| 新建小节 | `docs/MEMORY.md` §10 | 提交 / 推送 / 同步状态唯一权威入口；显式作废旧断言 |
| 修改（规则同步） | `docs/MEMORY.md` §7 第 6 条 | 由「未含推送」改为两步授权已分别执行，指向 §10 |
| 追加 | `COMPARISON.md` §10 | 推送实测与「未 commit/push」历史行作废声明 |
| 追加 | 本节 | 增补登记，append-only |
| 追加（本地、gitignored） | `.workbuddy/memory/2026-11-09.md` | 当日事件 |

- 推送实测：`f592df4..a1f480b main -> main`，exit=0；GitHub 通道复核远端 HEAD = `a1f480bfe769fd496df716a9802a4f5a89d605bb`；ahead/behind = 0/0。
- 作废声明：本报告前四续及 `COMPARISON.md` §7.4 / §8.3 中「未 commit/push」「未 push」均为当时状态，推送后失效；权威值见 `docs/MEMORY.md §10`。历史行保留不回改。
- 不包含：主工作区 22 条原有未提交改动（4 tracked + 18 未跟踪），仍留在本地；未裁决 C1–C5、未重建 `index.json`、未批量改链。
