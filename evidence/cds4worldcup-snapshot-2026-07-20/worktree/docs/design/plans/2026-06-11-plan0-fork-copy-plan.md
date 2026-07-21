# Plan 0：CDS4WorldCup 分叉复制执行计划

> **类型**: execution-plan
> **状态**: ready-for-implementation
> **日期**: 2026-06-11
>
> **目标**: 从 CDS4Polymarket 迁移 CDS4WorldCup2026 启动 Plan A/B/C 所需的最小资产，并生成可审计 copy manifest。

## 1. 范围

Plan 0 只做分叉复制与来源登记，不解释数据、不跑模型、不写路径卡。

覆盖：

- CDS4Polymarket 世界杯实验冻结快照。
- Plan C 需要的 protocol / schema / template / fixture。
- Plan B 需要的 Kimi canonical raw data。
- Plan A/B/C 共享的 source ledger 与知识边界。

不覆盖：

- 不复制完整 CDS 前端或后端。
- 不复制 Kimi UI 作为本项目 UI 基线。
- 不解压或引入重复 Kimi 数据目录。
- 不修改 raw source。
- 不写投注、收益或赔率价值分析。

## 2. 目标目录

创建或确认：

```text
archive/cds4polymarket/worldcup-2026-factor-calibration/
archive/kimi-ui-reference/
docs/imports/cds4polymarket/
docs/templates/worldcup/
data/raw/kimi/
data/raw/cds4polymarket/
data/source-ledger/
src/factor_ledger/schemas/
artifacts/fixtures/cds4polymarket/
artifacts/reports/
```

## 3. 复制清单

### 3.1 冻结快照

| 来源 | 目标 | 状态 |
|---|---|---|
| `<CDS4POLYMARKET>/experiments/worldcup-2026-factor-calibration/` | `archive/cds4polymarket/worldcup-2026-factor-calibration/` | required |

用途：保留原始实验结构，供 provenance 和人工回查。

### 3.2 活跃导入：协议与模板

| 来源 | 目标 | 用途 |
|---|---|---|
| `methodology_disclosure.md` | `docs/imports/cds4polymarket/methodology_disclosure.md` | 方法披露 |
| `protocol.md` | `docs/imports/cds4polymarket/protocol.md` | Plan C 协议基线 |
| `factor_adjudication_rubric.md` | `docs/imports/cds4polymarket/factor_adjudication_rubric.md` | 因子判定规则 |
| `schemas/*.schema.yaml` | `src/factor_ledger/schemas/` | Prediction / Factor / Settlement schema |
| `templates/worldcup_prediction_card_v0.2.md` | `docs/templates/worldcup/worldcup_prediction_card_v0.2.md` | 预注册卡模板 |
| `templates/worldcup_system_v0.2.md` | `docs/templates/worldcup/worldcup_system_v0.2.md` | 系统提示模板 |

### 3.3 活跃导入：数据与 fixtures

| 来源 | 目标 | 用途 |
|---|---|---|
| `data/source_ledger.md` | `data/source-ledger/cds4polymarket-source-ledger.md` | source ledger 样例 |
| `data/derived/official_schedule_snapshot.csv` | `data/raw/cds4polymarket/official_schedule_snapshot.csv` | 赛程 fixture，需后续核验 |
| `analysis/*.csv` | `artifacts/fixtures/cds4polymarket/analysis/` | 历史分析 fixture |
| `predictions/` | `artifacts/fixtures/cds4polymarket/predictions/` | Plan C 示例输入 |
| `factor-ledger/` | `artifacts/fixtures/cds4polymarket/factor-ledger/` | Factor Ledger 示例 |
| `settlement/` | `artifacts/fixtures/cds4polymarket/settlement/` | Settlement 示例 |
| `reports/*.md` | `artifacts/fixtures/cds4polymarket/reports/` | failure / knowledge update 示例 |

### 3.4 Kimi canonical raw data

| 来源 | 目标 | 状态 |
|---|---|---|
| `worldcup-kimi/2026_World_Cup_White_Paper.pdf` | `data/raw/kimi/2026_World_Cup_White_Paper.pdf` | required |
| `worldcup-kimi/2026世界杯数据全景工作簿.xlsx` | `data/raw/kimi/2026世界杯数据全景工作簿.xlsx` | required |
| `worldcup-kimi/kimi_300_unpacked/wc2026_aggregation.json` | `data/raw/kimi/kimi_300_unpacked/wc2026_aggregation.json` | required |
| `worldcup-kimi/kimi_300_unpacked/*_predictions.json` | `data/raw/kimi/kimi_300_unpacked/` | required |
| `worldcup-kimi/kimi_300_unpacked/wc2026_data.md` | `data/raw/kimi/kimi_300_unpacked/wc2026_data.md` | required |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/data.js` | `archive/kimi-ui-reference/wc2026_predict/data.js` | optional |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/index.html` | `archive/kimi-ui-reference/wc2026_predict/index.html` | optional |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/hero-bg.mp4` | `archive/kimi-ui-reference/wc2026_predict/hero-bg.mp4` | optional |

不复制：

- `worldcup-kimi/extracted_kimi_agent/`，避免与 `kimi_300_unpacked/` 双源重复。
- `worldcup-kimi/*.zip`，第一阶段不需要。

## 4. Copy Manifest

复制完成后生成：

```text
artifacts/reports/plan0-copy-manifest.md
```

建议结构：

```markdown
# Plan 0 Copy Manifest

## Summary

## Directory Creation

## Copied Assets

| source | target | purpose | status | notes |
|---|---|---|---|---|

## Skipped Assets

| source | reason |
|---|---|

## Source Policy Notes

## Readiness Decision

- pass
- pass_with_limitations
- fail
```

## 5. 验证

必须检查：

- required 文件均存在。
- `data/raw/kimi/` 中只有一个 canonical unpacked 数据目录。
- `wc2026_aggregation.json` 可读取。
- prediction JSON 数量大于 0。
- copied schema 文件存在于 `src/factor_ledger/schemas/`。
- `artifacts/reports/plan0-copy-manifest.md` 写明 skipped assets。
- 没有修改 `schema/`、`templates/`、`example/` 根目录协议文件。

## 6. 下一步

Plan 0 完成后进入：

- Plan A0：48 队 registry 与数据缺口报告。
- Plan B0/B1：Kimi reason 直觉锚定与数据可用性。
- Plan C 准备：核验 schema / template / fixture 是否可用于单场闭环。
