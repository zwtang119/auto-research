# MVP-0 Data Gate Report

> **日期**: 2026-06-11
> **执行者**: AI-assisted (Claude)
> **决策**: pass_with_limitations

## Summary

对 Kimi 300 Agent 聚合数据执行数据门控。300 条 Agent 预测记录字段完整（零缺失），10 派别 × 30 Agent/派别均匀分布，reason corpus 质量参差但整体可用。主要限制：Kimi 数据仅覆盖 21 支球队（预测中出现），48 队 registry 中 27 队未被提及；174/300 Agent 未在单独 prediction 文件中出现（仅在 aggregation 中）。数据门控结果为 **pass_with_limitations**。后续讨论显示，Kimi reason 需先进入 Reason Recoverability Gate，暂不直接进入 Codability Pilot。

## Source Inventory

| 来源 | 路径 | 类型 | 状态 | 备注 |
|---|---|---|---|---|
| Kimi 300 Agent 聚合 | `data/raw/kimi/kimi_300_unpacked/wc2026_aggregation.json` | JSON | ✅ 可读 | 300 predictions + metadata + top8 + faction_probs |
| Kimi 逐 Agent 预测 | `data/raw/kimi/kimi_300_unpacked/*_predictions.json` | JSON (42 files) | ✅ 可读 | 126/300 agents 有单独文件 |
| Kimi 数据表 | `data/raw/kimi/kimi_300_unpacked/wc2026_data.md` | Markdown | ✅ 可读 | Yellow/Red Source |
| 白皮书 | `data/raw/kimi/2026_World_Cup_White_Paper.pdf` | PDF | ✅ 存在 | 可选，本次未深入解析 |
| Excel 工作簿 | `data/raw/kimi/2026世界杯数据全景工作簿.xlsx` | XLSX | ✅ 存在 | 可选，本次未深入解析 |

### 聚合 JSON 结构

```
{
  "top8": [...],           // 8 支球队加权概率排名
  "all_teams": [...],      // 21 支球队概率排名
  "predictions": [...],    // 300 条 Agent 预测
  "faction_names": [...],  // 10 个派别名称
  "faction_probs": {...},  // 派别 × 球队概率矩阵
  "faction_quotes": {...}, // 每派别 3 条代表性 quote
  "max_hot": {...},        // 最热球队
  "underrated": {...},     // 最被低估球队
  "most_divisive": {...},  // 最具争议球队
  "metadata": {...}        // 元数据
}
```

## Field Availability

### Predictions 字段完整性

| 字段 | 缺失 | 空值 | 通过率 |
|---|---|---|---|
| `agent_id` | 0 | 0 | 100% |
| `faction` | 0 | 0 | 100% |
| `persona` | 0 | 0 | 100% |
| `champion` | 0 | 0 | 100% |
| `top3` | 0 | 0 | 100% |
| `confidence` | 0 | 0 | 100% |
| `reason` | 0 | 0 | 100% |
| `faction_detail` | 0 | 0 | 100% |

**结果**: ✅ 所有核心字段 100% 完整。

### 单独 Prediction 文件对齐

| 指标 | 值 |
|---|---|
| Aggregation 中 agent 数 | 300 |
| 单独文件中 agent 数 | 126 |
| 对齐率 | 42% (126/300) |
| 仅在 aggregation 中 | 174 agents |

**说明**: 42 个 `*_predictions.json` 文件仅覆盖 126 个 agent。174 个 agent 仅存在于聚合文件中。这不影响分析（聚合数据已包含全部 300 条），但意味着无法对 174 个 agent 做单独溯源。

## Team Name Alignment

### Kimi 数据覆盖

| 指标 | 值 |
|---|---|
| Kimi 中唯一球队数 | 21 |
| 48 队 registry 中被覆盖 | 21 |
| 48 队 registry 中未覆盖 | 27 |
| 覆盖率 | 43.8% |

### Kimi 数据中的 21 支球队

| # | 中文 | English | Confederation |
|---|---|---|---|
| 1 | 西班牙 | Spain | UEFA |
| 2 | 法国 | France | UEFA |
| 3 | 阿根廷 | Argentina | CONMEBOL |
| 4 | 葡萄牙 | Portugal | UEFA |
| 5 | 英格兰 | England | UEFA |
| 6 | 德国 | Germany | UEFA |
| 7 | 摩洛哥 | Morocco | CAF |
| 8 | 巴西 | Brazil | CONMEBOL |
| 9 | 挪威 | Norway | UEFA |
| 10 | 荷兰 | Netherlands | UEFA |
| 11 | 克罗地亚 | Croatia | UEFA |
| 12 | 哥伦比亚 | Colombia | CONMEBOL |
| 13 | 日本 | Japan | AFC |
| 14 | 塞内加尔 | Senegal | CAF |
| 15 | 美国 | United States | CONCACAF |
| 16 | 墨西哥 | Mexico | CONCACAF |
| 17 | 乌拉圭 | Uruguay | CONMEBOL |
| 18 | 比利时 | Belgium | UEFA |
| 19 | 澳大利亚 | Australia | AFC |
| 20 | 韩国 | South Korea | AFC |
| 21 | 土耳其 | Turkey | UEFA |

### 球队名标准化

Kimi 数据使用中文名称，所有 21 支球队均可通过一对一映射转为英文名称。未发现同一球队有多个名称变体。team_name_map.csv 已建立映射。

## Agent / Faction Inventory

### 派别分布

| 派别 | Agent 数 | 派别英文标识 |
|---|---|---|
| 数据派 | 30 | data |
| 赔率派 | 30 | odds |
| 老球迷派 | 30 | fan |
| 玄学派 | 30 | mystic |
| 主帅视角派 | 30 | coach |
| 伤病赛程派 | 30 | injury |
| 黑马派 | 30 | dark |
| 阵容年龄派 | 30 | age |
| 心理抗压派 | 30 | mental |
| 建模派 | 30 | model |

**分布**: 完全均匀，每派别 30 Agent。

### 置信度分布

| 指标 | 值 |
|---|---|
| 范围 | 18–85 |
| 均值 | 63.1 |
| 分层 (≤40) | 28 agents (9.3%) |
| 分层 (41–65) | 128 agents (42.7%) |
| 分层 (≥66) | 144 agents (48.0%) |

### Champion 集中度

| 排名 | 球队 | 加权概率 | raw_votes |
|---|---|---|---|
| 1 | 西班牙 | 23.82% | 62 |
| 2 | 法国 | — | — |
| 3 | 阿根廷 | — | — |
| 4 | 葡萄牙 | — | — |
| 5 | 英格兰 | — | — |
| 6 | 德国 | — | — |
| 7 | 挪威 | — | — |
| 8 | 巴西 | — | — |

> 注: 完整 top8 概率见 aggregation.json `top8` 字段。

## Reason Corpus Overview

| 指标 | 值 |
|---|---|
| 总 reason 数 | 300 |
| 非空 reason 数 | 300 (100%) |
| 字符长度范围 | 31–75 |
| 平均字符长度 | 45 |

### 质量初步印象（基于 30 条分层抽样）

- **可验证类**: 约 13/30 条包含可检索事实数据（身价、排名、赔率、战绩）
- **废话类**: 约 4/30 条为纯修辞/玄学推断（"四字恰好26画"、"一甲子大周期"）
- **意外类**: 约 5/30 条包含非主流观点或跨派别冲突（美国东道主优势、挪威哈兰德双核论）
- **有用但不可验证**: 约 8/30 条包含合理的定性分析但缺乏可验证锚点

详细分类见 `artifacts/reports/mvp0-intuition-notes.md`。

## Data Gaps

| Gap | 严重度 | 影响 | 缓解措施 |
|---|---|---|---|
| 仅 21/48 队有预测数据 | 🔴 高 | 27 队无法做 agent-based 预测分析 | 补充白皮书/Excel 数据；仅对 21 队做 agent 预测分析 |
| 174/300 agent 无单独 prediction 文件 | 🟡 中 | 无法单独溯源 58% 的 agent | 聚合数据已包含完整信息，对 reason inventory 无影响 |
| 白皮书/Excel 未深度解析 | 🟡 中 | 可能遗漏额外球队数据 | 阶段 2 可选补充 |
| Confidence 偏高（均值 63.1/100） | 🟢 低 | 可能反映生成式 AI 过度自信 | Neff / faction structure 可后续独立分析 |
| Reason 长度偏短（均值 45 字符） | 🟢 低 | 可能限制可编码性 | Pilot 中评估是否足够支撑 factor 提取 |
| 48 队 registry 的分组信息尚未官方确认 | 🟡 中 | 部分 team_registry.csv 分组信息为推测 | 待官方抽签后更新 |

## Decision

**pass_with_limitations**

### 理由

1. **通过项**: 300 条预测 7 核心字段 100% 完整；10 派别均匀分布；reason corpus 非空可用；agent_id 可唯一标识；球队名可标准化映射。
2. **限制项**: 仅覆盖 21/48 队（43.8%），27 队无 agent 预测数据；174 agent 无单独文件溯源。
3. **结论**: 数据足够支撑 Kimi reason 的下一步门控，但后续已确认阶段 2 应先做 Reason Recoverability Gate，而不是直接做 Codability Pilot。团队覆盖限制需在后续阶段标注。

## 产出清单

| 文件 | 行数/状态 | 路径 |
|---|---|---|
| kimi_agent_inventory.csv | 300 rows | `data/processed/kimi_agent_inventory.csv` |
| team_registry.csv | 48 rows | `data/processed/team_registry.csv` |
| team_name_map.csv | 21 rows | `data/processed/team_name_map.csv` |
| kimi_reason_sample_30.csv | 30 rows | `data/processed/kimi_reason_sample_30.csv` |
| 数据门控报告 | 本文件 | `artifacts/reports/mvp0-data-gate-report.md` |
| 直觉锚定笔记 | 配套 | `artifacts/reports/mvp0-intuition-notes.md` |


## 后续修订：Reason Recoverability Gate

2026-06-11 后续讨论确认：30 条样本暴露出 Kimi reason 的前置问题不是单纯可查性，而是原文存在压缩黑话、人设独白、事实碎片、模型声称和推论判断混杂。Plan B2 已在主 spec 中标记为 `deferred-local-blocker`。Kimi reason 暂不进入 Factor Ledger，只保留为 Red Source / Marginalia / 候选线索。
