# cds-callbook 已迁出本仓

> **类型**：moved-pointer
> **日期**：2026-08-01（T0 执行）
> **原位置**：`analysis/forecast-ledger/` → 已重命名为 `analysis/forecast-ledger-legacy-2026-07-24/`（历史设计稿，**禁止误读为活跃项目**）

## 迁出什么

forecast-ledger 旧方案已演进为 **cds-callbook** 项目：独立公开仓（裸账本 + 轻量 Pages）+ cds4polymarket 私有仓 `experiments/call-test/`（方法厨房）。

## 活跃方案在哪

- **施工层执行计划（真源）**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/plans/cds-callbook-execution-plan-2026-08-01.md`
- **方案层 master plan**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/plans/cds-callbook-implementation-2026-07-24.md`
- **施工标准**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/standards/implementation-plan-standard-v1.md`
- **公开仓（T0 创建）**：`/Users/tangzw119/Documents/GitHub/cds-callbook/`（GitHub: zwtang119/cds-callbook，公开）

## 为什么迁出

- auto-research 是学术研究组合，治理围绕 cds4worldcup 冻结数据集；cds-callbook 是实时营销 track record，数据源 predictionarena.ai 与cds4worldcup 正交，无证据链路可继承。
- cds-callbook 需要公开可见，纳入私有研究组合会让 Pages + 排除逻辑复杂化。
- 详见 cds4polymarket `docs/investigations/cds-callbook-repo-placement-2026-07-24.md`。
