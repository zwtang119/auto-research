# Investigation: Plan C 产物 Schema 合规性 & Team Cards 数据一致性

## Summary

对 Plan C 全部 8 个 YAML 文件和 48 张 Team Cards 进行系统性 schema 合规性和数据一致性审计。共发现 **17 处问题**：4 处已知确认 + 4 处新发现 schema 违规（均在 mex-rsa 因子账本） + 8 处 settlement record 类型违规 + 4 处 Team Cards 内容问题。其余 3 个未结算因子账本、3 张预测卡（除 temperature 类型疑义外）和 44 张 Team Cards 均通过检查。

## Symptoms

- `artifacts/plan-c/factor-ledger/wc2026-a-m01-mex-rsa.factors.yaml` 中发现 4 处已知 schema 违规 + 6 处新发现违规
- `artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml` 中发现 8 处类型/位置违规
- `artifacts/team-cards/` 中 4 张卡有内容问题（2 张复制粘贴错误 + 2 张信号字段未更新）

## Background / Prior Research

- 前置调查确认 schedule.json 的分组映射与预期一致
- 未结算的因子账本（qat-sui, bra-mar, ned-jpn）均为 schema 合规
- 预测卡结构完整、概率 sum=1.0、因子交叉引用无误
- Fixture 版 mex-rsa 因子账本合规，问题仅出现在 settlement 后版本

## Investigator Findings

### A. Factor Ledger Schema 违规（mex-rsa 已结算版）

#### A1. adjudicator.status 枚举越界（4 处 · P1 必须修复）

| # | 文件 | 行号 | 值 | Schema 允许 | 因子 |
|---|------|------|----|-------------|------|
| A1-1 | `artifacts/plan-c/factor-ledger/wc2026-a-m01-mex-rsa.factors.yaml` | L25 | `settled_inconclusive` | `[pending, complete]` | f01-home-possession |
| A1-2 | 同上 | L60 | `settled_supported` | `[pending, complete]` | f02-rsa-shots-on-target |
| A1-3 | 同上 | L90 | `settled_rejected` | `[pending, complete]` | f03-mex-corner-count |

**修复方式**: 将值改为 `complete`。结算结果已在 `calibration_status` 字段中正确表达。

#### A2. calibration_status 枚举越界（1 处 · P1 必须修复）

| # | 文件 | 行号 | 值 | Schema 允许 | 因子 |
|---|------|------|----|-------------|------|
| A2-1 | `artifacts/plan-c/factor-ledger/wc2026-a-m01-mex-rsa.factors.yaml` | L38 | `inconclusive_data_gap` | `[tracking, supported, rejected, inconclusive]` | f01-home-possession |

**修复方式**: 改为 `inconclusive`。具体原因已在同条目的 `reason_for_inconclusive` 字段中记录。

#### A3. 未声明字段（3 处字段名 · P2 建议修复）

| # | 文件 | 行号 | 字段名 | 问题 |
|---|------|------|--------|------|
| A3-1 | `artifacts/plan-c/factor-ledger/wc2026-a-m01-mex-rsa.factors.yaml` | L27, L62, L92 | `evidence_summary` | Schema 定义的可选字段为 `adjudication_evidence`，文件使用了不同名称 |
| A3-2 | 同上 | L23 | `protocol_failure_logged` | Schema 中未声明此字段 |
| A3-3 | 同上 | L11 | `settlement_source` (顶层) | Schema 中未声明此顶层字段 |
| A3-4 | 同上 | L12 | `original_ledger` (顶层) | Schema 中未声明此顶层字段 |

**修复方式**: 二选一 — (a) 将数据中的字段名改为 schema 定义的名称；(b) 扩展 schema 以正式采用 agent 使用的更清晰字段名。

#### A4. 其他 Factor Ledger 文件（通过）

- `wc2026-b-m02-qat-sui.factors.yaml` — 3 条目全部合规 ✅
- `wc2026-c-m01-bra-mar.factors.yaml` — 3 条目全部合规 ✅
- `wc2026-f-m01-ned-jpn.factors.yaml` — 3 条目全部合规 ✅

---

### B. Settlement Record Schema 违规（8 处）

#### B1. factor_updates 子项类型不匹配（P1 必须修复）

| # | 文件 | 行号 | 字段 | 期望类型 | 实际类型 |
|---|------|------|------|----------|----------|
| B1-1 | `artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml` | L75–83 | `factor_updates.supported` | `list[string]` | `list[object]` |
| B1-2 | 同上 | L84–93 | `factor_updates.rejected` | `list[string]` | `list[object]` |
| B1-3 | 同上 | L94–105 | `factor_updates.inconclusive` | `list[string]` | `list[object]` |

每项包含了 `factor_id`, `evidence`, `confidence_post` 等对象字段，但 schema 仅允许因子 ID 字符串列表。

#### B2. protocol_failures 子项类型不匹配（P1 必须修复）

| # | 文件 | 行号 | 字段 | 期望类型 | 实际类型 |
|---|------|------|------|----------|----------|
| B2-1 | 同上 | L106–121 | `protocol_failures` | `list[string]` | `list[object]` |

每项包含 `failure_id`, `factor_affected`, `severity`, `description`, `resolution`, `resolved` 等对象字段。

#### B3. scores.baseline_difference 类型不匹配（P1 必须修复）

| # | 文件 | 行号 | 字段 | 期望类型 | 实际类型 |
|---|------|------|------|----------|----------|
| B3-1 | 同上 | L57–71 | `scores.baseline_difference` | `map[string, number\|null]` | 嵌套对象（含 `note` 等字符串子字段） |

#### B4. 可选字段位置错误（P2 建议修复）

| # | 文件 | 行号 | 字段 | Schema 位置 | 实际位置 |
|---|------|------|------|------------|----------|
| B4-1 | 同上 | L39–55 | `brier_calculation`, `log_loss_calculation`, `calculation_snippet` | 顶层 | 嵌套在 `scores:` 下 |
| B4-2 | 同上 | L9–10 | `goal_scorers_home_90m`, `goal_scorers_away_90m` | 顶层 | 嵌套在 `result:` 下 |
| B4-3 | 同上 | L31 | `result_source` | 顶层 | 嵌套在 `result:` 下 |

#### B5. result 内嵌套结构违反 map[string, string|number]（P2 建议修复）

| # | 文件 | 行号 | 字段 | 问题 |
|---|------|------|------|------|
| B5-1 | 同上 | L13–16 | `result.red_cards` | 是 `list[string]`，schema 要求 `string\|number` |
| B5-2 | 同上 | L17–30 | `result.match_statistics` | 是嵌套对象，schema 要求 `string\|number` |

---

### C. Prediction Card 检查（通过，1 个低优先级疑义）

| 文件 | 必填字段 | 概率求和 | 枚举值 | factors_used 交叉引用 |
|------|---------|---------|--------|---------------------|
| `wc2026-b-m02-qat-sui.prediction_card.yaml` | ✅ 14/14 | ✅ 1.00 | ✅ | ✅ 3/3 匹配 |
| `wc2026-c-m01-bra-mar.prediction_card.yaml` | ✅ 14/14 | ✅ 1.00 | ✅ | ✅ 3/3 匹配 |
| `wc2026-f-m01-ned-jpn.prediction_card.yaml` | ✅ 14/14 | ✅ 1.00 | ✅ | ✅ 3/3 匹配 |

#### C1. temperature 类型疑义（P3 可忽略）

| # | 文件 | 行号 | 值 | 问题 |
|---|------|------|----|------|
| C1-1 | 全部 3 张卡 | ~L39-40 | `temperature: 0` | YAML 解析为整数；schema 声明 `type: number`。大多数验证器通过（int ⊂ number），但严格类型检查可能标记。建议改为 `0.0`。 |

---

### D. Team Cards 数据一致性（48 张中 44 张通过）

#### D1. 复制粘贴错误（2 处 · P1 必须修复）

| # | 文件 | 行号 | 问题描述 |
|---|------|------|---------|
| D1-1 | `artifacts/team-cards/argentina.md` | L127 | §11 最可信路径中引用"德尚的务实策略"——Didier Deschamps 是法国队教练，不是阿根廷队。应改为斯卡洛尼或阿根廷相关表述。 |
| D1-2 | `artifacts/team-cards/portugal.md` | L131 | §11 最可信路径中出现"F 组以 K 组头名出线"——"F 组"是复制残留，葡萄牙只在 K 组。应删除"F 组"。 |

#### D2. 信号字段未更新（2 处 · P2 建议修复）

| # | 文件 | 行号 | 问题描述 |
|---|------|------|---------|
| D2-1 | `artifacts/team-cards/portugal.md` | L19-20 | `kimi_baseline_signals: [none_yet]` 但 §9 包含 21 条 Kimi agent reasons，aggregate probability 7.00%，且 `yellow_sources`/`red_sources` 包含 `kimi-aggregation` 和 `kimi-300-agent-reasons`。信号应反映实际 Kimi 数据。 |
| D2-2 | `artifacts/team-cards/england.md` | L19-20 | `kimi_baseline_signals: [none_yet]` 但 §9 包含 15 条 Kimi agent reasons，aggregate probability 5.00%，且数据源包含 Kimi 相关条目。信号应反映实际 Kimi 数据。 |

#### D3. 全部 48 张卡的通用检查结果

| 检查项 | 结果 |
|--------|------|
| `group:` 与 schedule.json 一致 | ✅ 48/48 |
| `status: deep-description` | ✅ 48/48 |
| `source_status.coverage` 在合法范围内 | ✅ 48/48 (sufficient/partial/thin) |
| `path_type: unassigned` | ✅ 48/48 |
| `tier: unassigned` | ✅ 48/48 |
| 无 `<待分析>` 占位符 | ✅ 48/48 |
| 11 节全部有实质内容 | ✅ 48/48 |

---

### E. 因子交叉引用完整性

| 预测卡 | factors_used | 因子账本 factor_id | 匹配 |
|--------|-------------|-------------------|------|
| wc2026-b-m02-qat-sui | 3 IDs | 3 IDs | ✅ 完全匹配 |
| wc2026-c-m01-bra-mar | 3 IDs | 3 IDs | ✅ 完全匹配 |
| wc2026-f-m01-ned-jpn | 3 IDs | 3 IDs | ✅ 完全匹配 |

无孤立因子、无幽灵引用。

## Investigation Log

### Phase 1 - 已知问题确认
**Hypothesis:** 已知的 4 处 schema 违规是仅有的问题
**Findings:** 假设被否定。除 4 处已知问题外，还发现 6 处额外 schema 违规（因子账本）+ 8 处 settlement record 违规 + 4 处 team cards 问题。
**Evidence:** 8 个并行 explore agent 扫描结果 + 直接文件验证
**Conclusion:** 实际问题范围远大于已知范围。结算流程产生了大量 schema 外结构。

### Phase 2 - Team Cards 全面扫描
**Hypothesis:** Team Cards 数据一致性
**Findings:** 48 张卡中 44 张完全合规。4 张有问题：argentina.md (复制粘贴)、portugal.md (复制粘贴+信号未更新)、england.md (信号未更新)。
**Evidence:** 3 个并行 explore agent 批量扫描，按组检查
**Conclusion:** Team Cards 数据质量整体良好，个别卡有内容问题

## Root Cause

### 核心问题：结算 Agent 的 Schema 盲视

1. **复合枚举值融合**: Agent 将两个正交关注点（流程状态 + 结果）融合到 `adjudicator.status` 单一字段中。`settled_supported` 实际上同时表达" adjudication 完成"和"结果为 supported"。
2. **过度限定枚举值**: `inconclusive_data_gap` 是在 `reason_for_inconclusive` 字段已记录原因的情况下，对 `inconclusive` 的冗余细化。
3. **Schema 未覆盖结算后场景**: 当前 schema 仅定义了 `pending`/`complete` 两种 adjudicator 状态，未为结算后扩展预留空间。`evidence_summary`、`protocol_failure_logged`、`settlement_source`、`original_ledger` 等实用字段未被 schema 纳入。
4. **Settlement record 富对象化**: Schema 定义的 `list[string]` 类型对 `factor_updates` 和 `protocol_failures` 过于简单，agent 自然地添加了证据、置信度等结构化信息。

### 次要问题：Team Cards 批量生成的质量控制

1. **复制粘贴残留**: argentina.md 的"德尚"来自 france.md 模板；portugal.md 的"F 组"来自其他卡的模板。
2. **信号字段未同步更新**: kimi_baseline_signals 在 §9 内容填充后未回写更新。

## Recommendations

### 立即修复（P1）

| # | 文件 | 修复动作 |
|---|------|---------|
| 1 | `mex-rsa.factors.yaml` L25, L60, L90 | `settled_*` → `complete` |
| 2 | `mex-rsa.factors.yaml` L38 | `inconclusive_data_gap` → `inconclusive` |
| 3 | `mex-rsa.settlement_record.yaml` | 将 `factor_updates` 和 `protocol_failures` 的对象列表简化为 ID 字符串列表（或更新 schema） |
| 4 | `argentina.md` L127 | "德尚的务实策略" → "斯卡洛尼的战术调配" |
| 5 | `portugal.md` L131 | 删除"F 组"残留文字 |

### Schema 升级（P2）

| # | 动作 | 理由 |
|---|------|------|
| 1 | `factor_ledger_entry.schema.yaml`: 将 `adjudication_evidence` 重命名为 `evidence_summary`（或添加别名） | Agent 自然使用 `evidence_summary`，名称更直观 |
| 2 | `factor_ledger_entry.schema.yaml`: 添加可选字段 `protocol_failure_logged` (string\|null) | 结算后的协议失败追溯是有价值的元数据 |
| 3 | `factor_ledger_entry.schema.yaml`: 添加顶层可选字段 `settlement_source`, `original_ledger` | 已结算的因子账本需要溯源 |
| 4 | `settlement_record.schema.yaml`: 将 `factor_updates.*` 从 `list[string]` 升级为 `list[object]` | 结构化证据信息比纯 ID 列表更有审计价值 |
| 5 | `settlement_record.schema.yaml`: 将 `protocol_failures` 从 `list[string]` 升级为 `list[object]` | 同理，失败详情需要结构化 |
| 6 | `settlement_record.schema.yaml`: 将 `scores.baseline_difference` 从 `map[string, number\|null]` 扩展支持嵌套对象 | 基线差异的详细说明比纯数字更有用 |
| 7 | 预测卡 `temperature: 0` → `temperature: 0.0` | 消除 YAML 整数/浮点歧义 |
| 8 | `portugal.md` L19-20, `england.md` L19-20: 更新 `kimi_baseline_signals` | 反映 §9 中已填充的 Kimi 数据 |

### 可忽略（P3）

| # | 动作 | 理由 |
|---|------|------|
| 1 | 预测卡 `temperature: 0` → `0.0` | 大多数验证器兼容 int/number，实际无影响 |

## Preventive Measures

1. **CI Schema 验证**: 在 CI 中添加 YAML schema 验证步骤（如 `yamlvalidate` 或自定义脚本），在 PR 合并前自动拦截 enum 越界和类型不匹配。
2. **结算 Agent Prompt 约束**: 在 settlement agent 的系统提示中明确注入 schema 枚举值范围，防止 agent 自行扩展枚举。
3. **Team Cards 生成模板校验**: 批量生成后运行 grep 检查常见复制粘贴残留（如跨组引用、错误教练名）。
4. **字段同步检查**: 添加脚本验证 `kimi_baseline_signals` 与 §9 内容的一致性。
