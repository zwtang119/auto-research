<!--
re-role-note: prepend 2026-07-03
This directory serves as the **evidence input layer** in the P1+P2
Evidence Ledger mainline (`../papers/p1p2-evidence-ledger/`). It is the
**producer** of `signal_evidence_entry` rows that get promoted into
`evidence_ledger_entry.supporting_evidence[]` /
`evidence_ledger_entry.contradicting_evidence[]`. The fusion algorithm
itself is **not** the paper contribution; the P1+P2 mainline reads
what this directory produces. See `../docs/portfolio/aliases.md` §1
and `../papers/p1p2-evidence-ledger/wiki/concepts/layer-roles.md` for the
separation of concerns.
-->

# P7 多源信号融合 → 多 Agent 决策支持

> **论文管线**：P7 | **模型**：Minimax M3 | **AutoResearch 协议**：Deli_AutoResearch
> **状态**：初始化 | **目标会议**：ACM TIST

## 快速进入

1. 读 `wiki/index.md` 了解本实验知识库全貌
2. 读 `state/task_spec.md` 了解实验任务规格（SignalFusionEngine 267行纯函数链、12 active datasources）

## Marginalia 知识库

本实验使用 Marginalia 边注系统。知识库位于 `wiki/`。

### 每次对话开始时
- 读取 `wiki/index.md` 了解知识库全貌

### 对话中遇到以下情况时
- 讨论了新概念 → 在 `wiki/concepts/` 创建页面
- 做了实验决策 → 在 `wiki/decisions/` 记录

### 完成实质工作后
- 更新 `wiki/index.md`（如有新页面）
- 在相关页面添加批注：`> [!memo] YYYY-MM-DD 内容`

## 三原则
- 同位、无损、解耦
