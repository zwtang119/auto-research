# AutoResearch 课题五项目组合

> **⛔ 组合主线已关闭（2026-07-18，用户决策）**：终裁结论见 [docs/investigations/topic-selection-2026-07-18/verdict-topic-selection-first-principles.md](docs/investigations/topic-selection-2026-07-18/verdict-topic-selection-first-principles.md)，关闭记录见 [docs/portfolio/project-closure-2026-07-18.md](docs/portfolio/project-closure-2026-07-18.md)。
>
> **▶ 当前活跃主线（2026-07-20 用户裁定）：世界杯算法比较实证论文**——开题报告 [docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md](docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md)，执行计划 [docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md](docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md)，证据基础 [evidence/cds4worldcup-snapshot-2026-07-20/](evidence/cds4worldcup-snapshot-2026-07-20/MANIFEST.md)（三级证据结构：封存仓库 → 证据快照 → 分析副本，详见 [CLAUDE.md](CLAUDE.md)）。
>
> **⏸ 其余未关闭课题（开题/休眠状态，勿误关）**：Decision Co-Scientist（开题·暂停待资源，终裁 GO 附条件，重启蓝图已交付）——[docs/investigations/decision-coscientist-proposal/](docs/investigations/decision-coscientist-proposal/README.md)；C1 AI-auto-research 实证（GO 附 4-gate · DORMANT）；G3/D1 Settlement Reconciliation（PARK）；决策流水线（想法记录，未评审）——状态细表见 [CLAUDE.md](CLAUDE.md)「当前活跃主线」。

本目录是课题五相关 AutoResearch 实验组合的根目录。组合关闭前的历史主线（P11 收口 / P12 Judge Calibration / P1+P2 Evidence RAG / P8 / P7）见 [docs/portfolio/project-index.md](docs/portfolio/project-index.md) 与 [docs/roadmaps/topic5-research-directions.md](docs/roadmaps/topic5-research-directions.md)（历史基线）。

## 当前准绳

- 项目地图与约定：[CLAUDE.md](CLAUDE.md)
- Agent 工作指引：[AGENTS.md](AGENTS.md)
- 代号映射：[docs/portfolio/aliases.md](docs/portfolio/aliases.md)
- AutoResearch 运行材料：[docs/autoresearch/README.md](docs/autoresearch/README.md)
- 旧路径重定向：[OBSOLETE.md](OBSOLETE.md)

## 目录说明

```text
auto-research/
├── CLAUDE.md / AGENTS.md / README.md / OBSOLETE.md
├── docs/                          # 组合级文档
│   ├── plans/                     #   计划（含闸门与回退）
│   ├── investigations/            #   开题、终裁、调查
│   ├── papers-closed-portfolio/   #   已关闭组合的论文产出（原 docs/papers/）
│   ├── portfolio/                 #   aliases、命名审计、关闭记录
│   ├── roadmaps/                  #   路线图（含 topic5-research-directions.md）
│   └── autoresearch/  compose/  reviews/
├── evidence/                      # ★ 证据快照（字节级原始，永不修改）
├── analysis/                      # ★ 分析副本根目录（可写，增补记 CHANGELOG）
├── research/                      # 论文标准元研究（Nature 评分 rubric）
├── papers/                        # 活跃论文树（P7/P8/P12/P1+P2，高引用区）
├── legacy/                        # 已关闭/初始化历史目录（约占 95% 体量）
├── framework/                     # 跨论文可复用（schemas/ + knowledge/）
└── state/  logs/                  # 组合级状态与日志（高引用区）
```

## 执行原则

- 根目录做组合决策；子项目目录保存证据和实验。
- 新组合级文档放入 `docs/`；新组合级状态放入 `state/`。
- 证据操作走三级结构：封存仓库零读写，证据快照只读，分析进 `analysis/` 并记 CHANGELOG。
- 不随意移动实验目录内部文件，避免破坏脚本、LaTeX 和 wiki 引用。
- AutoResearch 只用于可验证迭代：每轮必须有产物、日志和停/走判断。
