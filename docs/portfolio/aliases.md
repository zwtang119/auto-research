# AutoResearch 项目代号 → 目录别名

> 更新日期：2026-07-03
> 用途：把文档中出现的论文代号（P7 / P8 / P12 / P1+P2）映射到仓库内具体目录。
> 详细角色说明见 `project-index.md` §2 和各目录自己的 `CLAUDE.md` / `README.md`。

## 1. 论文代号与目录映射

| 代号 | 全称 / 主题 | 主目录 | 备注 |
|------|-------------|--------|------|
| P7 | 多源信号融合 / evidence input layer | `papers/p07-signal-fusion/` | 当前主入口；`legacy/p07-legacy-init-2026-07/` 为旧实现，不作主入口 |
| P8 | 预测市场校准 / settlement layer | `papers/p08-market-calibration/` | 当前主入口；`legacy/p08-legacy-init-2026-07/` 为旧实现，不作主入口 |
| P12 | Judge Calibration | `papers/p12-judge-calibration/` | 短期优先主线；唯一目录 |
| P1+P2 | Evidence RAG + Factor Ledger 概念主线 | `papers/p1p2-evidence-ledger/` | **概念主目录**；不重写 P7/P8/P12 文件，只消费它们的产物 |

## 2. 代号交叉引用

| 代号 | 内部消费 | 内部产出 |
|------|----------|----------|
| P7 → `papers/p07-signal-fusion/` | 12 个 active datasources | `signal_evidence_entry`（喂给 P1+P2） |
| P8 → `papers/p08-market-calibration/` | `evidence_ledger_entry` 的 `settlement_rule` / `observed_outcome` | `settlement_record`、Brier / Log Loss（服务 P1+P2） |
| P12 → `papers/p12-judge-calibration/` | P11 抽出的 sample manifest | 评估 P1+P2 factor quality 的盲评 / pair / neighborhood 协议 |
| P1+P2 → `papers/p1p2-evidence-ledger/` | P7 的 signal evidence、P8 的 settlement、P12 的 judge 协议、P11 的反例 | `evidence_ledger_entry` schema、Day 14 review |

## 3. 旧实现目录（不作为主入口）

| 目录 | 对应代号 | 状态 |
|------|----------|------|
| `legacy/p07-legacy-init-2026-07/` | P7 旧实现 | 初始化；不作为主入口 |
| `legacy/p08-legacy-init-2026-07/` | P8 旧实现 | 初始化；不作为主入口 |
| `legacy/p11-closed-v5-mimo/` | P11 旧实现 | 已关闭到 7.0 级 |
| `legacy/p11-closed-v5-minimax-m3/` | P11 主版本 | 主线收口，结果被 P1+P2 当反例 |

## 4. 使用约定

- 文档中提到 "P7" → 写 `papers/p07-signal-fusion/`。
- 文档中提到 "P8" → 写 `papers/p08-market-calibration/`。
- 文档中提到 "P12" → 写 `papers/p12-judge-calibration/`。
- 文档中提到 "P1+P2" / "Evidence RAG" / "Factor Ledger" → 写 `papers/p1p2-evidence-ledger/`。
- 旧实现目录只在显式讨论历史时使用，并在文末注明版本（mimo / minimax-m3）。
