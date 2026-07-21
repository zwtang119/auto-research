# Plan C: Factor Ledger 协议闭环验证报告

> **类型**: plan-c-validation
> **日期**: 2026-06-11
> **状态**: pass

## 1. 验证目标

验证从 CDS4Polymarket 复制的 Factor Ledger schema、template、fixture 能否在 CDS4WorldCup 中支持完整的单场预注册闭环（MVP1）。

## 2. Schema 验证

### 2.1 Schema 完整性

| Schema | 版本 | 必填字段 | 状态 |
|--------|------|---------|------|
| `prediction_card.schema.yaml` | 0.2 | 14 个必填 | ✅ 完整 |
| `factor_ledger_entry.schema.yaml` | 0.2 | 12 个必填 | ✅ 完整 |
| `settlement_record.schema.yaml` | 0.2 | 6 个必填 | ✅ 完整 |

### 2.2 关键字段检查

**prediction_card:**
- `lock` 含 `sha256` + `git_commit` → 预注册锚定 ✅
- `data_package` 区分 `green_sources` vs `red_sources_excluded_from_model` → 来源分级 ✅
- `prompt_config` 含 `market_or_odds_exposed_to_model` + `public_ai_baseline_exposed_to_model` → 控制模型输入 ✅
- `smoke_test` 标志 → 支持历史回测 ✅

**factor_ledger_entry:**
- `origin` 枚举 `cds_generated | kimi_derived | human_seeded` → 来源溯源 ✅
- `settlement_rule` → 可结算性 ✅
- `adjudicator.required_independence` → 独立裁判 ✅
- `calibration_status` → 支持 tracking/supported/rejected/inconclusive ✅

**settlement_record:**
- `scores` 含 Brier + Log Loss + baseline_difference → 评分闭环 ✅
- `factor_updates` 三分类 → 因子结算闭环 ✅
- `protocol_failures` → 失败记录 ✅

### 2.3 Schema 间一致性

| 检查项 | 结果 |
|--------|------|
| prediction_card.match_id ↔ settlement_record.match_id | ✅ 一致 |
| prediction_card.task_type ↔ settlement_record.task_type | ✅ 一致 |
| factor_ledger_entry.match_id ↔ prediction_card.match_id | ✅ 一致 |
| prediction_card.factors_used ↔ factor_ledger_entry.factor_id | ✅ 引用关系正确 |
| factor_ledger_entry.calibration_status ↔ settlement_record.factor_updates | ✅ 状态映射正确 |

## 3. Template 验证

| Template | 状态 |
|----------|------|
| `docs/templates/worldcup/worldcup_prediction_card_v0.2.md` | ✅ 可用 |
| `docs/templates/worldcup/worldcup_system_v0.2.md` | ✅ 可用 |

## 4. Fixture 验证

| Fixture | 用途 | 状态 |
|---------|------|------|
| `artifacts/fixtures/cds4polymarket/predictions/` | 预注册卡示例 | ✅ 含 v0.2 示例 |
| `artifacts/fixtures/cds4polymarket/factor-ledger/` | Factor Ledger 示例 | ✅ 含 YAML |
| `artifacts/fixtures/cds4polymarket/settlement/` | Settlement 示例 | ✅ 含结算记录 |
| `artifacts/fixtures/cds4polymarket/reports/` | 报告示例 | ✅ 含 failure/knowledge update |

## 5. MVP1 单场闭环验证

### 5.1 闭环流程

```
赛前:
  1. 创建 prediction_card.yaml（锁定预测）
  2. 锁定后计算 sha256 + git commit hash
  3. 在 factor_ledger/ 注册相关因子

赛中:
  4. 因子状态保持 tracking

赛后:
  5. 创建 settlement_record.yaml（结算）
  6. 更新 factor_ledger_entry.calibration_status
  7. 生成 knowledge_update 或 protocol_failure 报告
```

### 5.2 MVP1 可执行性判断

| 条件 | 状态 |
|------|------|
| Schema 支持 pre-registration lock | ✅ |
| Schema 支持 factor settlement | ✅ |
| Schema 支持 Brier / Log Loss 评分 | ✅ |
| Template 可渲染 | ✅ |
| Fixture 提供参考实现 | ✅ |
| Git 可用作锁定锚 | ✅ |
| source_ledger 可追溯 | ✅ |

## 6. MVP2 准备状态

MVP2 = 3-5 场滚动闭环。额外需求：

| 需求 | 状态 |
|------|------|
| 多场 match_id 命名规则 | ✅ `wc2026-{group}-m{nn}` |
| 跨场因子追踪 | ✅ factor_id 可跨 match |
| 滚动评分聚合 | ✅ settlement_record 支持逐场 |
| memory_budget 跨场传递 | ✅ prediction_card.memory_budget |

## 7. 差距与建议

| 差距 | 影响 | 建议 |
|------|------|------|
| 2026 赛程数据不完整（仅 4 场 fixture） | MVP1 样本少 | 补充完整 48 队 104 场赛程 |
| 无自动化 CI 验证 schema | 手动验证 | 后续加 yaml schema validate 步骤 |
| settlement 评分需比赛结果 API | MVP1 需手动输入 | 后续接入 FIFA API 或手动录入 |

## 8. 结论

**决策: pass** — Factor Ledger 协议资产可以在 CDS4WorldCup 中运行单场预注册闭环。

MVP1 可以开始：选定第一场比赛 → 填写 prediction_card → 锁定 → 等赛后 settlement。

## 9. 下一步

- MVP1: 选定 2026 世界杯第一场比赛，创建预注册 prediction_card
- MVP2: 设计 3-5 场滚动闭环流程
- 2026 赛程补全：从 FIFA 官方获取完整 104 场赛程数据
