# CLAUDE.md — auto-research 项目地图与约定

> 最后更新：2026-10-27（补充单代理与交付优先约定）

## 这是什么

课题五 AutoResearch 组合仓库。组合主线已于 2026-07-18 关闭（`docs/portfolio/project-closure-2026-07-18.md`），当前处于关闭后孵化期。**当前主线（2026-09-25 起挂起、投稿暂停）：世界杯算法比较实证论文**（用户裁定 2026-07-20，以开题报告为主线）。

## 当前活跃主线

> ⏸ **2026-09-25 用户决定：世界杯双论文研究挂起、投稿暂停（无限期）。恢复时可能随 cds4polymarket P1~P7 同步投稿，视校对人意见。**

| 线 | 状态 | 入口 |
|---|---|---|
| **世界杯算法比较实证论文** | ⏸ 挂起（2026-09-25，原活跃开题 v1.3） | 开题：`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` ｜ 计划：`docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` ｜ 缺口调查：`docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` |
| Decision Co-Scientist | 开题·暂停待资源（终裁 GO 附条件，未投入 MVE） | `docs/investigations/decision-coscientist-proposal/` ｜ 计划：`docs/plans/decision-coscientist-experiment-2026-07-19.md` |
| C1 AI-auto-research 实证（process-trace / failure taxonomy） | GO 附 4-gate · DORMANT（未启动，非关闭） | `docs/portfolio/project-closure-2026-07-18.md` §3 |
| G3/D1 Settlement Reconciliation | PARK（未执行，非关闭） | 同上 |
| 决策流水线（idea-decision-pipeline） | 想法记录（未评审、未纳入开题，2026-07-19） | `docs/investigations/decision-coscientist-proposal/idea-decision-pipeline-2026-07-19.md` |
| W6 终裁备忘录 | 参考（用户裁定：开题为主线，本备忘录降为参考） | `docs/investigations/worldcup-paper-topic-2026-07-19.md` |
| DMO 不确定性决策文献精读（SEA-27 2018 + Elliott 2025，含 4polymarket/4Worldcup/policysim 贡献评估） | 参考（知识沉淀，已关闭 2026-07-22） | `docs/investigations/dmo-uncertainty-decision-reading-2026-07-22.md` ｜ 材料：`analysis/dmo-uncertainty-reading/`、`analysis/downloads-pdf-scan/` |

> ⚠️ 状态口径警告（2026-07-20）：`state/progress.json` 的 status 字段停在 W6 备忘录阶段，未同步 v1.3 主线裁定（metadata drift）。课题状态以本表为准；DORMANT/PARK/想法记录 均**不是**关闭，关闭名单以 `docs/portfolio/project-closure-2026-07-18.md` §3 为准。

## 目录地图

```text
auto-research/
├── CLAUDE.md / AGENTS.md / README.md / OBSOLETE.md
├── docs/
│   ├── INDEX.md                # ★ 仓库级总索引（docs/INDEX.md）：会话开始先读，再查 index.json / SCRIPTS.md
│   ├── plans/                  # 计划文档（含闸门与回退条款）
│   ├── investigations/         # 开题、终裁、调查（含 worldcup-algorithms-proposal/）
│   ├── papers-closed-portfolio/  # 已关闭组合的论文产出（原 docs/papers/，2026-07-20 改的名）
│   ├── portfolio/              # aliases.md、命名审计、关闭记录
│   ├── roadmaps/               # 路线图（含 topic5-research-directions.md）
│   ├── autoresearch/  compose/  reviews/
├── evidence/                   # ★ 证据快照（字节级原始，永不修改）
│   └── cds4worldcup-snapshot-2026-07-20/   # 含完整 git bundle + 工作区镜像 + MANIFEST
├── analysis/                   # ★ 分析副本根目录（可写，增补记 CHANGELOG；见内 README）
├── research/                   # 论文标准元研究（nature-first-class-paper 评分 rubric）
├── papers/                     # 活跃论文树（P7/P8/P12/P1+P2）——高引用区
├── legacy/                     # 已关闭/初始化历史目录（占仓库约 95% 体量）
├── framework/                  # 跨论文可复用（schemas/ + knowledge/）
├── state/  logs/               # 组合级状态与日志——高引用区
└── .env(.sample)               # 本地配置（不入库）
```

## 三级证据结构（2026-07-20 用户裁定，强制）

| 称呼 | 指代 | 规则 |
|---|---|---|
| **封存仓库** | `/Users/tangzw119/Documents/GitHub/cds4worldcup`（HEAD `e8d74aa`） | **零读写**。论文引用其 GitHub 公开 commit 哈希 |
| **证据快照** | `evidence/cds4worldcup-snapshot-2026-07-20/` | 字节级原始，**永不修改**（含 .DS_Store 也不删） |
| **分析副本** | `analysis/<topic>/` | 可写；所有增补（赛果、ex-ante 提取、复算）逐条记 `CHANGELOG.md` |

## 禁区与高危区

- **封存仓库**：任何进程不得读写。需要其内容时从证据快照或 bundle 提取。
- `papers/`、`legacy/`、`state/`、`framework/`：高引用区（`state/*` 约 478 处引用），禁止重命名/移动内部文件。
- `docs/SECRETS.md`、`.env`：敏感内容，不入库不外传。

## 工作约定

- **执行默认**：单代理负责到底，允许独立工具并行与后台任务；仅用户明确要求时启用 subagent、context_builder 或 Oracle，执行细则见 `AGENTS.md`。
- **交付优先**：围绕用户目标确定交付物与必要验收条件；条件满足即交付并停止，不自行扩展审计、重建或审批流程。非阻断问题随已知限制交付，证据与隐私底线仍须满足。

- **git 纪律**：明确指令后按授权执行 `git commit`/`push`；历史改写类（`reset`/`rebase`/强推）仍先请示；移动文件用 `git mv`。`prompt-exports/`、`logs/`、`state/` 自 2026-09-25 起本地专用、不入库。
- **验证纪律**：任何代理（oracle/pair/explore）的具体断言必须经直接计算复核后才入档（2026-07-20 调查：4 条断言 2 证伪 1 漏检）。
- **复算纪律**：论文数字一律以我方管线从冻结数据复算为准，不引用项目自评数字。
- **合规**：不输出投注建议，不报告收益率；事实声明引 Green Source，预测数字引 Red Source 并标注 ex-ante 版本。
- **文档命名**：`docs/plans/<topic>-<YYYY-MM-DD>.md`、`docs/investigations/<topic>-<YYYY-MM-DD>.md`；简单任务直接执行，复杂任务的计划只保留目标、步骤、验收条件及真实阻塞项，按需设置 go/no-go 闸门。
- **rp 技能族**：按任务需要使用 `~/.agents/skills/rp-*`，不默认启动多代理或多轮审查；`prompt-exports/` 清理仍遵守删除前列清单的规则。
