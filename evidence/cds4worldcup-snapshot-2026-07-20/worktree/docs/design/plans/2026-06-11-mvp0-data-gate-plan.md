# MVP-0 数据门控执行计划

> **类型**: execution-plan
> **状态**: completed-2026-06-11
> **日期**: 2026-06-11
>
> **目标**: 在不等待世界杯比赛结果的情况下，判断 Kimi / AI 群体数据是否值得进入 CDS4WorldCup2026 的扩展校准实验。
>
> **执行结论**: `pass_with_limitations` — 字段可用，但 Kimi reason 后续进入 `Reason Recoverability Gate`，暂不直接进入 Codability Census。

## 1. 范围

本计划覆盖 Plan B 的阶段 0-1。阶段 2 原计划为 Codability Pilot，但后续已修正为 Reason Recoverability Gate。

不覆盖：

- 不做完整 Markov 路径引擎。
- 不做 48 队深描路径卡。
- 支持 Plan A0 / A1 所需的 48 队 registry、数据覆盖状态和薄切片路径卡输入。
- 不做赛后 settlement。
- 不修改 Kimi 原始文件。

## 2. 输入

候选输入目录：

- `data/raw/kimi/`
- 外部来源可从原始仓库复制：
  - `worldcup-kimi/2026_World_Cup_White_Paper.pdf`
  - `worldcup-kimi/2026世界杯数据全景工作簿.xlsx`
  - `worldcup-kimi/kimi_300_unpacked/wc2026_aggregation.json`
  - `worldcup-kimi/kimi_300_unpacked/*_predictions.json`
  - `worldcup-kimi/kimi_300_unpacked/wc2026_data.md`

## 3. 输出

建议输出：

- `artifacts/reports/mvp0-intuition-notes.md`
- `artifacts/reports/mvp0-data-gate-report.md`
- `data/processed/team_registry.csv`
- `data/processed/team_name_map.csv`
- `data/processed/kimi_agent_inventory.csv`
- `data/processed/kimi_reason_sample_30.csv`

## 4. 阶段 0：直觉锚定

### 做法

1. 从 Kimi 300 Agent reason 中抽 20-30 条。
2. 人工阅读，不做正式标注。
3. 记录四类信号：
   - 可验证。
   - 废话。
   - 意外。
   - 有用但不可验证。

### 输出格式

`artifacts/reports/mvp0-intuition-notes.md`

```markdown
# MVP-0 Intuition Notes

## 样本来源

## 四类信号

### 可验证

### 废话

### 意外

### 有用但不可验证

## 初始直觉
```

### 验收

- 至少记录 20 条 reason 的阅读印象。
- 不把这一步当作正式 codability 结果。

## 5. 阶段 1：数据可用性

### 检查项

| 检查项 | 通过标准 |
|---|---|
| 白皮书概率表 | 有 Top8+ 球队的冠军 / 出线概率 |
| 聚合 JSON | 每个 agent 有 `faction` / `champion` / `confidence` / `reason` |
| 逐 agent JSON | 能和聚合数据通过 `agent_id` 对齐 |
| 白皮书 ↔ Agent 球队名 | 可通过标准化匹配 |
| 48 队 registry | 能建立唯一球队名列表 |
| reason inventory | 能统计 reason 数、派别数、置信度分布 |

### 输出字段

`data/processed/kimi_agent_inventory.csv`

- `agent_id`
- `faction`
- `persona`
- `champion`
- `top3`
- `confidence`
- `reason`
- `source_file`

`data/processed/team_name_map.csv`

- `canonical_team`
- `zh_name`
- `en_name`
- `aliases`
- `source`
- `confidence`

`data/processed/team_registry.csv`

- `canonical_team`
- `zh_name`
- `en_name`
- `confederation`
- `group`
- `source_status`
- `coverage_status`
- `notes`

### 报告结构

`artifacts/reports/mvp0-data-gate-report.md`

```markdown
# MVP-0 Data Gate Report

## Summary

## Source Inventory

## Field Availability

## Team Name Alignment

## Agent / Faction Inventory

## Reason Corpus Overview

## Data Gaps

## Decision

- pass
- pass_with_limitations
- fail
```

## 6. 阶段 2 准备：30 条 reason 抽样

抽样要求：

- 按派别 × 置信度分层。
- 不按球队分层。
- 保留原文 reason。
- 保留 source_file 和 agent_id。

输出：

`data/processed/kimi_reason_sample_30.csv`

字段：

- `sample_id`
- `agent_id`
- `faction`
- `confidence`
- `champion`
- `reason`
- `source_file`

## 7. 决策规则

阶段 1 出口：

- `pass`: 字段齐全，进入下一步门控；后续已修正为 Reason Recoverability Gate。
- `pass_with_limitations`: 字段部分缺失，但 reason corpus 可用；后续已修正为 Reason Recoverability Gate，并标注限制。
- `fail`: 无法读取或对齐 Kimi 核心数据，进入路径 E。

## 8. 验证

执行后检查：

- 输出 CSV 行数符合预期。
- reason 字段非空。
- faction 分布可统计。
- 无修改 raw source。

## 9. 执行结果记录（2026-06-11）

### 阶段 0 直觉锚定：已完成
- 输出：`artifacts/reports/mvp0-intuition-notes.md`
- 30 条 reason 已阅读分类（可验证/废话/意外/有用但不可验证）
- 直觉预判 codability ~70%——**这只是直觉估计，不是 pilot 结果**

### 阶段 1 数据可用性：已完成
- `kimi_agent_inventory.csv`：300 行，字段 100% 完整（agent_id, faction, persona, champion, top3, confidence, reason, faction_detail）
- `team_registry.csv`：48 行（21 队 Kimi 覆盖 + 27 队 missing-from-kimi）
- `team_name_map.csv`：21 行中英文映射
- 10 派别每派 30 条，完美均匀
- Kimi 覆盖 21/48 队（43.8%），27 队无 agent 预测

### 阶段 2 准备：已完成
- `kimi_reason_sample_30.csv`：30 条分层抽样
- **注意**：30 条仅用于直觉锚定，不用于正式 codability 结论

### 决策：pass_with_limitations
- **亮点**：300 条预测零缺失，10 派别均匀，reason 可读可用
- **限制**：仅 21/48 队覆盖，27 队无数据
- **数据缺口**：48 队完整赛程需补充外部来源

## 10. 后续修订

基于后续讨论和标注包试制结果，Plan B2 不继续扩大为 300 条 Codability Census，而是修正为 **Reason Recoverability Gate**：

- 原因：Kimi reason 存在人设独白、事实碎片、模型声称、推论判断和省略主谓宾的压缩黑话混合。
- 结论：直接做人类 codability 标注会把“读不读得懂”误当成“可不可审计”。
- 当前状态：`deferred-local-blocker`。该卡点只阻塞 Kimi reason 进入 Factor Ledger，不阻塞 Plan A1 或 Plan C。
- 若未来恢复：先做 30-50 条小样本 recoverability check，再决定是否进入 codability / Neff / historical anchoring。

### Build in Public 边界
- GitHub 仓库：Private（源代码不公开）
- GitHub Pages：Public（结果与方法论公开）
- raw data（data/raw/）：不发布到 Pages
- artifacts/reports/：逐项白名单决定是否发布
- 未收敛的分析结论：不公开
