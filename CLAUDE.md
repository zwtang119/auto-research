# CLAUDE.md — auto-research 项目地图与约定

> 最后更新：2026-07-20（目录重整 + 三级证据结构确立）

## 这是什么

课题五 AutoResearch 组合仓库。组合主线已于 2026-07-18 关闭（`docs/portfolio/project-closure-2026-07-18.md`），当前处于关闭后孵化期。**当前活跃主线：世界杯算法比较实证论文**（用户裁定 2026-07-20，以开题报告为主线）。

## 当前活跃主线

| 线 | 状态 | 入口 |
|---|---|---|
| **世界杯算法比较实证论文** | 活跃开题（主线，v1.3） | 开题：`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` ｜ 计划：`docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` ｜ 缺口调查：`docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` |
| Decision Co-Scientist | 开题·暂停待资源（终裁 GO 附条件，未投入 MVE） | `docs/investigations/decision-coscientist-proposal/` ｜ 计划：`docs/plans/decision-coscientist-experiment-2026-07-19.md` |
| C1 AI-auto-research 实证（process-trace / failure taxonomy） | GO 附 4-gate · DORMANT（未启动，非关闭） | `docs/portfolio/project-closure-2026-07-18.md` §3 |
| G3/D1 Settlement Reconciliation | PARK（未执行，非关闭） | 同上 |
| 决策流水线（idea-decision-pipeline） | 想法记录（未评审、未纳入开题，2026-07-19） | `docs/investigations/decision-coscientist-proposal/idea-decision-pipeline-2026-07-19.md` |
| W6 终裁备忘录 | 参考（用户裁定：开题为主线，本备忘录降为参考） | `docs/investigations/worldcup-paper-topic-2026-07-19.md` |

> ⚠️ 状态口径警告（2026-07-20）：`state/progress.json` 的 status 字段停在 W6 备忘录阶段，未同步 v1.3 主线裁定（metadata drift）。课题状态以本表为准；DORMANT/PARK/想法记录 均**不是**关闭，关闭名单以 `docs/portfolio/project-closure-2026-07-18.md` §3 为准。

## 目录地图

```text
auto-research/
├── CLAUDE.md / AGENTS.md / README.md / OBSOLETE.md
├── docs/
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

- **git 纪律**：不擅自 `git commit`/`push`；移动文件用 `git mv`；改动留给用户审阅。
- **验证纪律**：任何代理（oracle/pair/explore）的具体断言必须经直接计算复核后才入档（2026-07-20 调查：4 条断言 2 证伪 1 漏检）。
- **复算纪律**：论文数字一律以我方管线从冻结数据复算为准，不引用项目自评数字。
- **合规**：不输出投注建议，不报告收益率；事实声明引 Green Source，预测数字引 Red Source 并标注 ex-ante 版本。
- **文档命名**：`docs/plans/<topic>-<YYYY-MM-DD>.md`、`docs/investigations/<topic>-<YYYY-MM-DD>.md`；计划含 Goal/Background/Approach/Work Items/Open Questions/References 与硬 go/no-go 闸门。
- **rp 技能族**：深度规划/调查/编排/构建走 `~/.agents/skills/rp-*`；过期 `prompt-exports/` 及时清理。
