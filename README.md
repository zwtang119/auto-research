# AutoResearch 课题五项目组合

本目录是课题五相关 AutoResearch 实验组合的根目录。当前主线已经从“P11 内心独白继续大修”调整为：

1. **P11 收口**：保留负结果、label leakage 和 judge calibration 样本。
2. **P12 Judge Calibration**：短期优先，目标 60 分可发表小论文。
3. **P1+P2 Evidence RAG + Factor Ledger**：中期主线，冲击更高质量论文。
4. **P8 / P1.2 Market Calibration**：作为外部 settlement / calibration layer。
5. **P7 / P2.1 Signal Fusion**：作为 evidence input layer，除非升级为 evidence topology，否则不单独主打。

## 当前准绳

- 新路线图：[docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md](docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md)
- 项目索引：[docs/portfolio/project-index.md](docs/portfolio/project-index.md)
- 代号映射：[docs/portfolio/aliases.md](docs/portfolio/aliases.md)
- AutoResearch 运行材料：[docs/autoresearch/README.md](docs/autoresearch/README.md)
- 历史全量规划：[topic5-research-directions.md](topic5-research-directions.md)

## 目录说明

```text
auto-research/
├── README.md
├── topic5-research-directions.md
├── docs/                          # portfolio + roadmap + investigations
│   ├── roadmaps/
│   ├── portfolio/                 # aliases.md, FRAMEWORK-RULES.md, audits
│   ├── investigations/
│   ├── autoresearch/
│   └── compose/                   # plans + specs + reports
├── framework/                     # ★ cross-paper reusable (schemas/ + knowledge/)
├── state/                         # portfolio-level state
├── logs/                          # portfolio-level logs
├── papers/                        # ★ ACTIVE paper trees (P7/P8/P12/P1+P2)
├── legacy/                        # ★ Closed/initialized historical dirs
├── victorchen96.github.io/        # reference (cloned, NOT ours)
└── OBSOLETE.md                    # old-path redirect
```

## 执行原则

- 根目录做组合决策；子项目目录保存证据和实验。
- 新组合级文档放入 `docs/`。
- 新组合级状态放入 `state/`。
- 不随意移动实验目录内部文件，避免破坏脚本、LaTeX 和 wiki 引用。
- AutoResearch 只用于可验证迭代：每轮必须有产物、日志和停/走判断。
