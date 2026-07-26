# MOVED — 本目录方案已被 cds-callbook 取代

> **指针文件**（不是新方案）。原 `analysis/forecast-ledger/PLAN.md` + `README.md` 的设计已被合并终稿取代，本目录**不再代表任何活跃项目**。

## 发生了什么

2026-07-24 立项讨论中，对 `forecast-ledger` 项目做了仓库选址拍板：**独立公开仓 + 方法寄宿 cds4polymarket 私有侧**，并改名为 **`cds-callbook`**（`cds-` 能力范式）。原本的"私有仓 + Pages 排除 private-method"架构已过期（方法搬走后仓内本无方法）。

## 活跃方案在哪

- **实施方案合并终稿**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/plans/cds-callbook-implementation-2026-07-24.md`
- **归属与选址调研**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/investigations/cds-callbook-repo-placement-2026-07-24.md`
- **方法研发槽身份卡**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/experiments/call-test/README.md`
- **实施进度**：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/project/progress.md`（搜索 "cds-callbook 项目归属拍板"）

## 关键变更

| 维度 | 本目录（已过期） | 新方案 |
|---|---|---|
| 仓名 | forecast-ledger | **cds-callbook**（独立公开仓） |
| 方法位置 | 本仓库内（待建 private-method/） | cds4polymarket/experiments/call-test/ |
| OTS | 保留 | **删** |
| 节奏 | 私有回溯验证再公开 | day-1 live + 管线冒烟前置 |
| Pages | 私有仓 + 排除 private-method/ | 公开仓 + 轻量 Pages（无需排除） |

## 当前待办

- [ ] `git mv analysis/forecast-ledger/ analysis/forecast-ledger-legacy-2026-07-24/`（保留但加 legacy 后缀，禁止误读为活跃项目）
- [ ] `git mv analysis/forecast-ledger/{PLAN,README}.md analysis/forecast-ledger-legacy-2026-07-24/`（同上）
- [ ] 本文件 `CALLBOOK-MOVED.md` 是否需 git add：用户拍板（它是跨仓指针，本仓不读）
- [ ] 用户说"去做"后：开新仓 `cds-callbook`（顶层 `GitHub/cds-callbook/`），按 §9 实施步骤走

## 为什么不在本仓消化 cds-callbook

- auto-research 是**学术研究组合**（已结束的世界杯比较论文为主线），治理规则（三级证据结构）围绕 cds4worldcup 冻结数据集。
- cds-callbook 是**实时营销 track record**，数据源 predictionarena.ai 与 cds4worldcup 正交，无证据链路可继承。
- 隐私边界：cds-callbook 需要公开可见，强行纳入私有研究组合会让 Pages + 排除逻辑复杂化。
- 详见 `cds-callbook-repo-placement-2026-07-24.md` §1 / §2（auto-research 与 cds4worldcup 深调研结论）。
