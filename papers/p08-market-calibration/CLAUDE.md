<!--
re-role-note: prepend 2026-07-03
This directory serves as the **settlement / calibration layer** in the
P1+P2 Evidence Ledger mainline (`../papers/p1p2-evidence-ledger/`). It is the
**consumer** of `evidence_ledger_entry.settlement_rule` and
`evidence_ledger_entry.observed_outcome`; it emits `settlement_record`
and Brier / Log Loss scores back to P1+P2. It does **not** own the
ledger contract — that lives in `../papers/p1p2-evidence-ledger/`. See
`../docs/portfolio/aliases.md` §1 and
`../papers/p1p2-evidence-ledger/wiki/concepts/layer-roles.md` for the
separation of concerns.
-->

# P8 预测市场作为 LLM Agent 推演校准场

> **论文管线**：P8 | **模型**：Minimax M3 | **AutoResearch 协议**：Deli_AutoResearch
> **状态**：初始化 | **目标会议**：EMNLP 2027 / AAAI 2027

## 快速进入

1. 读 `wiki/index.md` 了解本实验知识库全貌
2. 读 `state/task_spec.md` 了解实验任务规格（Brier 需实现、Factor Ledger 仅设计）

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
- 同位：记忆附着在知识点旁边
- 无损：保留原话，不压缩
- 解耦：纯 Markdown，独立于平台
