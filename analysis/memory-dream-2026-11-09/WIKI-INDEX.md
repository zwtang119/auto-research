# WIKI-INDEX — 做梦 wiki 总览（导航层 · 2026-11-09）

> 本页是 dreaming pass #1 补建的 **index 页**（对应文章 Figure 15「补 index / repoint 悬空链接」）。五页 wiki 各管一个主题，本页只做地图，不复写内容。
> 上游入口：[`CLAUDE.md`](../../CLAUDE.md)（本仓唯一 Agent 入口）→ [`docs/MEMORY.md`](../../docs/MEMORY.md)（会话起始记忆索引，入库）→ [`docs/INDEX.md`](../../docs/INDEX.md)（第 70 节导航）。
> **状态准绳仍是 `CLAUDE.md`「当前活跃主线」表；本页不裁决 C1–C5，不改任何状态口径原文。**

## 一页一簇

| 簇 | 主题页 | 源簇 | 页体积 | 什么时候查它 |
|---|---|---:|---:|---|
| pilot | [Token 核算](token-accounting-wiki.md) | 10 篇 `token-*.md`，225,850 B | 6.87 KB | 有人报「全项目 token 消耗 = 47,293,807」时——该数字**不存在** |
| A | [世界杯主线](worldcup-wiki.md) | 20 篇 | 5.31 KB | 双论文主线、开题 v1.3、挂起裁定、缺口调查 |
| B | [Decision Co-Scientist](coscientist-wiki.md) | 26 篇 | 6.55 KB | 终裁 GO 附条件、MVE 未投入、4-gate / DORMANT 口径 |
| C | [2026-10 token / tsinghua / reprompt](oct2026-wiki.md) | 36 篇 | 7.10 KB | 10 月会话调查、reprompt 调查、token 口径演进 |
| D | [组合治理 / 终裁链 / 索引机制](governance-wiki.md) | 19 篇 | 6.32 KB | 2026-07-18 组合关闭、索引机制、状态冲突 C1–C5 的出处 |

合计 111 篇纳入主题导航，5 页共 32.15 KB（约为 pilot 源簇的 14%；四簇源簇未计字节）。单页均 ≤8 KB。

## 跨簇关系（地图的连线）

- **D → A**：组合关闭（D）之后才确立世界杯双论文为主线（A）；A 的「挂起」是 2026-09-25 用户裁定，D 里的关闭名单不含它。
- **A → B**：世界杯开题与 Co-Scientist 都走过「终裁 GO 附条件」，但 B **未投入 MVE**，不可写成已执行。
- **pilot → C**：token 核算页是 C 簇里 `token-*` 子集的单点深页；C 页给时间与调查脉络，pilot 页给不可相加的四个口径。两者**不要合并**——合并会把「撤回警示」冲淡。
- **各页 → 原文**：每页末尾链回 `path:line`。**wiki 是地图不是证据**，凡涉及数字、状态、裁定，一律回原文复核。

## 使用规则（来自文章实验边界）

1. **wiki + search 才有效**：文章 Stainless 语料 `wiki alone` 最高 48%、`search alone` 53%、`wiki + search` 54%→61%。本仓做法是「先查本页定位 → 按 `path:line` 回原文取回」，不把 wiki 当答案源。
2. **单文档可检索的问题不必用 wiki**：文章 LAB 任务在「文本搜索一份文档即可」时 wiki 无收益。本仓同理，别为可 grep 的事实绕一层。
3. **别让 wiki 长过原文**：文章反例是 wiki 203 KB / corpus 115 KB（1.77×），「effectively abstracted nothing」。本仓硬上限单页 8 KB。
4. **增量维护**：后续 dreaming 只做 add / correct / prune / repoint，不新建第二份全文摘要库。

## 校验与清单（不是 wiki，别当结论读）

| 文件 | 作用 |
|---|---|
| [`notes-audit.md`](notes-audit.md) | 171 篇结论/状态机器校验：A 字段不一致 1 / B 读取陷阱 17 / C 索引派生状态 20（预期） |
| [`link-audit.md`](link-audit.md) | 全仓链接 100% 分类：762 内部链接、209 待处理（B192 / W0 / E17）；演进 710 → 731 → 761 → 762 |
| [`COMPARISON.md`](COMPARISON.md) | 做梦前后实测对比、口径与边界 |
| [`CHANGELOG.md`](CHANGELOG.md) | 本目录所有增补的逐条登记 |
| [`../backup/`](backup/) | 索引原页字节级备份（`.orig` 三件，回滚入口） |

## 边界

- `evidence/`、`legacy/`、`papers/`、`framework/`、`state/` 与封存仓库：`link-audit.md` 中相关断链按字节级只读处理，**永不修改**；验收指标是「分类 100%」而非「清零」。
- 183 条失效 `scripts` 路径为 pre-existing（当前 worktree 不落盘），`docs/index.json` 未改，处置待用户裁定，详见 [`docs/MEMORY.md §5`](../../docs/MEMORY.md)。
- 本仓**没有评测集**，不得把文章 13%→48% / 54%→61% 的准确率收益外推到本轮。


## 检索评测草案（2026-11-09 pass #2）

| 文件 | 用途 |
|---|---|
| [`eval-set-draft.md`](eval-set-draft.md) | 25 题草案，**仅存档**；用户裁定不做检索评测，不执行 |
