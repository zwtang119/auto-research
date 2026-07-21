# Plan 0 Copy Manifest

> **日期**: 2026-06-11
> **执行者**: AI-assisted (Claude)
> **状态**: complete

## Summary

Plan 0 分叉复制完成。从 CDS4Polymarket 和 worldcup-kimi 迁移了 118 个文件，覆盖冻结快照、活跃协议/schema/模板、数据 fixtures、Kimi canonical raw data 和可选 UI 参考。

- **冻结快照**: 40 文件 → `archive/cds4polymarket/`
- **活跃导入**: 8 文件 → `docs/imports/`, `src/factor_ledger/schemas/`, `docs/templates/worldcup/`
- **数据 fixtures**: 20 文件 → `data/source-ledger/`, `data/raw/cds4polymarket/`, `artifacts/fixtures/cds4polymarket/`
- **Kimi canonical**: 47 文件 → `data/raw/kimi/`（not git-tracked）
- **Kimi UI 参考**: 3 文件 → `archive/kimi-ui-reference/`（optional）

## Directory Creation

| 目录 | 状态 |
|---|---|
| `archive/cds4polymarket/worldcup-2026-factor-calibration/` | ✅ created |
| `archive/kimi-ui-reference/` | ✅ created |
| `docs/imports/cds4polymarket/` | ✅ created |
| `docs/templates/worldcup/` | ✅ created |
| `data/raw/kimi/` | ✅ created (in .gitignore) |
| `data/raw/cds4polymarket/` | ✅ created (in .gitignore) |
| `data/source-ledger/` | ✅ created |
| `src/factor_ledger/schemas/` | ✅ created |
| `artifacts/fixtures/cds4polymarket/analysis/` | ✅ created |
| `artifacts/fixtures/cds4polymarket/predictions/` | ✅ created |
| `artifacts/fixtures/cds4polymarket/factor-ledger/` | ✅ created |
| `artifacts/fixtures/cds4polymarket/settlement/` | ✅ created |
| `artifacts/fixtures/cds4polymarket/reports/` | ✅ created |
| `artifacts/reports/` | ✅ already existed |

## Copied Assets

### §3.1 冻结快照

| source | target | purpose | status | notes |
|---|---|---|---|---|
| `<CDS4POLYMARKET>/experiments/worldcup-2026-factor-calibration/` | `archive/cds4polymarket/worldcup-2026-factor-calibration/` | 冻结快照，provenance 回查 | ✅ copied | 40 files, 完整保留原始结构 |

### §3.2 活跃导入：协议与模板

| source | target | purpose | status | notes |
|---|---|---|---|---|
| `methodology_disclosure.md` | `docs/imports/cds4polymarket/methodology_disclosure.md` | 方法披露 | ✅ copied | |
| `protocol.md` | `docs/imports/cds4polymarket/protocol.md` | Plan C 协议基线 | ✅ copied | |
| `factor_adjudication_rubric.md` | `docs/imports/cds4polymarket/factor_adjudication_rubric.md` | 因子判定规则 | ✅ copied | |
| `schemas/factor_ledger_entry.schema.yaml` | `src/factor_ledger/schemas/factor_ledger_entry.schema.yaml` | Factor Ledger schema | ✅ copied | |
| `schemas/prediction_card.schema.yaml` | `src/factor_ledger/schemas/prediction_card.schema.yaml` | Prediction schema | ✅ copied | |
| `schemas/settlement_record.schema.yaml` | `src/factor_ledger/schemas/settlement_record.schema.yaml` | Settlement schema | ✅ copied | |
| `templates/worldcup_prediction_card_v0.2.md` | `docs/templates/worldcup/worldcup_prediction_card_v0.2.md` | 预注册卡模板 | ✅ copied | |
| `templates/worldcup_system_v0.2.md` | `docs/templates/worldcup/worldcup_system_v0.2.md` | 系统提示模板 | ✅ copied | |

### §3.3 数据与 fixtures

| source | target | purpose | status | notes |
|---|---|---|---|---|
| `data/source_ledger.md` | `data/source-ledger/cds4polymarket-source-ledger.md` | source ledger 样例 | ✅ copied | |
| `data/derived/official_schedule_snapshot.csv` | `data/raw/cds4polymarket/official_schedule_snapshot.csv` | 赛程 fixture | ✅ copied | in .gitignore, 需后续核验 |
| `analysis/*.csv` (6 files) | `artifacts/fixtures/cds4polymarket/analysis/` | 历史分析 fixture | ✅ copied | + README.md |
| `predictions/` (2 subdirs) | `artifacts/fixtures/cds4polymarket/predictions/` | Plan C 示例输入 | ✅ copied | mvpa/ + phase-minus1/ |
| `factor-ledger/` (3 files) | `artifacts/fixtures/cds4polymarket/factor-ledger/` | Factor Ledger 示例 | ✅ copied | |
| `settlement/` (1 file) | `artifacts/fixtures/cds4polymarket/settlement/` | Settlement 示例 | ✅ copied | |
| `reports/*.md` (4 files) | `artifacts/fixtures/cds4polymarket/reports/` | failure / knowledge update 示例 | ✅ copied | |

### §3.4 Kimi canonical raw data

| source | target | purpose | status | notes |
|---|---|---|---|---|
| `worldcup-kimi/2026_World_Cup_White_Paper.pdf` | `data/raw/kimi/2026_World_Cup_White_Paper.pdf` | 白皮书基线 | ✅ copied | in .gitignore |
| `worldcup-kimi/2026世界杯数据全景工作簿.xlsx` | `data/raw/kimi/2026世界杯数据全景工作簿.xlsx` | 球队数据表 | ✅ copied | in .gitignore |
| `worldcup-kimi/kimi_300_unpacked/wc2026_aggregation.json` | `data/raw/kimi/kimi_300_unpacked/wc2026_aggregation.json` | 300 Agent 聚合 | ✅ copied | |
| `worldcup-kimi/kimi_300_unpacked/*_predictions.json` | `data/raw/kimi/kimi_300_unpacked/` (42 files) | 逐 agent prediction | ✅ copied | 42 prediction files |
| `worldcup-kimi/kimi_300_unpacked/wc2026_data.md` | `data/raw/kimi/kimi_300_unpacked/wc2026_data.md` | Kimi 整理材料 | ✅ copied | Yellow/Red Source |
| `worldcup-kimi/kimi_300_unpacked/plan.md` | `data/raw/kimi/kimi_300_unpacked/plan.md` | 数据计划说明 | ✅ copied | |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/data.js` | `archive/kimi-ui-reference/wc2026_predict/data.js` | UI 数据结构参考 | ✅ copied | optional |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/index.html` | `archive/kimi-ui-reference/wc2026_predict/index.html` | UI 参考 | ✅ copied | optional |
| `worldcup-kimi/kimi_300_unpacked/wc2026_predict/hero-bg.mp4` | `archive/kimi-ui-reference/wc2026_predict/hero-bg.mp4` | 视觉参考 | ✅ copied | optional |

## Skipped Assets

| source | reason |
|---|---|
| `worldcup-kimi/extracted_kimi_agent/` | 与 kimi_300_unpacked/ 内容重复，避免双源污染 |
| `worldcup-kimi/*.zip` (3 files) | 第一阶段不需要，留在原仓库 |
| `worldcup-kimi/kimi_300_unpacked/predictions_data_*.json` (non-faction pattern) | 已复制 42 个 faction-prefixed predictions，额外 predictions_data_*.json 已包含在复制中 |

## Source Policy Notes

- `data/raw/kimi/` 在 `.gitignore` 中，Kimi 数据仅保留在本地，不会被 git 追踪。
- Kimi 全部数据按 source-policy.md 分级为 **Red Source**（candidate seed / baseline），不作为事实 Green Source。
- 300 Agent 不能默认等同于 300 个独立专家（Neff 待 Plan B 测定）。
- CDS4Polymarket 实验输出只作为 provenance、fixture 和协议参考，不作为本项目结论。
- 本项目不输出投注建议、仓位、赔率价值或收益指标。

## Verification Results

| 检查项 | 结果 |
|---|---|
| required 文件均存在 | ✅ pass |
| `data/raw/kimi/` 中只有一个 canonical unpacked 目录 | ✅ pass (仅 kimi_300_unpacked/) |
| `wc2026_aggregation.json` 可读取 | ✅ pass |
| prediction JSON 数量 > 0 | ✅ pass (42 files) |
| copied schema 文件存在于 `src/factor_ledger/schemas/` | ✅ pass (3 schema files) |
| manifest 写明 skipped assets | ✅ pass |
| 未修改 `schema/`、`templates/`、`example/` 根目录协议文件 | ✅ pass |

## Readiness Decision

**pass**

所有 required 资产已复制，skipped 资产已记录原因，source policy 约束已确认。CDS4WorldCup2026 具备进入 Plan A0/B0/C 准备的条件。
