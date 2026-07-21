# 证据快照清单：cds4worldcup → auto-research

> 快照时间：2026-07-20 ｜ 执行：只读一次性导出（用户授权）｜ 源仓库此后恢复封存，任何分析不得再触碰

## 命名约定（2026-07-20 用户要求统一定义，此后所有文档/对话使用）

| 称呼 | 指代 | 性质 |
|---|---|---|
| **封存仓库**（sealed repo） | `/Users/tangzw119/Documents/GitHub/cds4worldcup`，HEAD `e8d74aa` | 零读写证据原体；论文引用其 GitHub 公开 commit 哈希 |
| **证据快照**（evidence snapshot） | `auto-research/evidence/cds4worldcup-snapshot-2026-07-20/`（本目录） | 封存仓库的一次性只读镜像；**字节级原始，永不修改**；增补信息一律不进本目录 |
| **分析副本**（analysis worktree） | 待建：`auto-research/analysis/worldcup-2026/`（自证据快照派生） | 可写工作区；所有增补（赛果补齐、ex-ante 版本提取、复算产物）进这里，逐条记 `CHANGELOG.md` |

派生关系：封存仓库 →（一次性导出）→ 证据快照 →（派生 + 增补日志）→ 分析副本。三者引用时必须用上表称呼，不得混用"仓库/快照/副本"。

## 源

- 路径：`/Users/tangzw119/Documents/GitHub/cds4worldcup`（**封存仓库**）
- HEAD：`e8d74aab618e6755a0c96232e7b66716d44967c6`（feat(knockout-settlement): 决赛阶段进度更新 + KO赛果录入 + 夺冠46队结算）
- 导出时工作区状态：3 个未跟踪条目（已一并复制，见下）

## 内容

| 项 | 说明 | 校验 |
|---|---|---|
| `cds4worldcup-all.bundle` | 完整 git 历史（`git bundle create --all`），含全部分支与 commit | `git bundle verify` 通过，"records a complete history"，sha1 |
| `worktree/` | HEAD 时点工作区全文镜像（`rsync -a --exclude=.git`），822 个文件，42M | 文件数与体积见本清单 |

## 未跟踪文件（存在于工作区、不在 git 历史，证据等级需单独标注）

1. `.agents/`（目录）
2. `.claude/`（目录）
3. `docs/investigations/system-running-state-and-paper-readiness-2026-06-20.md` ⚠️ **注意：开题报告 §5.1 引用的"内部诊断"文档是未提交状态**——引用它做证据时须用本快照路径而非 GitHub commit 链接

## 使用规则

- 后续全部分析只操作**分析副本**；证据快照仅在需要核对原始字节时读取。
- 验证完整性：`git bundle verify evidence/cds4worldcup-snapshot-2026-07-20/cds4worldcup-all.bundle`；需要历史文件（如 ex-ante 版 `odds.json` @ `88a9bfd`）时从 bundle 提取到分析副本，不回封存仓库。
- 论文 Data Availability 指向：封存仓库 GitHub 公开 commit `e8d74aa` + 证据快照（投稿时随 Zenodo 归档）。

## 封存确认

自本快照完成之时起，封存仓库恢复零读写封存（用户指令 2026-07-20）。
