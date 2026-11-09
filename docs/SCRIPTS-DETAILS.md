# docs/SCRIPTS-DETAILS.md — 脚本逐条清单（下移层）

> 2026-11-09 做梦 D4 从 `docs/SCRIPTS.md` 下移，**内容逐字来自原页，未改一字**；capability 由 `tools/build_index.py` 确定性推断。

## 重复骨架模式（本次扫描真实统计）

下表是 185 个脚本中**同名文件出现 ≥2 次**的骨架，说明「按日期新建副本并重写同一套骨架」是系统性现象，而非个别情况。

| 文件名 | 出现次数 | 典型副本 |
|---|---|---|
| `verify.py` | 4 | `analysis/token-1023-append-20261027/verify.py`、`analysis/token-1025-append-20261027/verify.py` |
| `release.py` | 3 | `analysis/token-1023-append-20261027/release.py`、`analysis/token-1025-append-20261027/release.py` |
| `run_checks.py` | 3 | `analysis/token-1023-append-20261027/run_checks.py`、`analysis/token-1025-append-20261027/run_checks.py` |
| `adapter.py` | 2 | `analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/adapter.py`、`analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/adapter.py` |
| `analyze_factorial.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/analyze_factorial.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/analyze_factorial.py` |
| `build_factorial_dataset.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/build_factorial_dataset.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/build_factorial_dataset.py` |
| `coordinator.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/coordinator.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/coordinator.py` |
| `design.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/design.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/design.py` |
| `freeze_inputs.py` | 2 | `analysis/token-imputation-audit-20261026/freeze_inputs.py`、`analysis/token-paper-accounting-20261027/freeze_inputs.py` |
| `generate_factorial.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/generate_factorial.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/generate_factorial.py` |
| `jaccard.py` | 2 | `analysis/tsinghua-1024-dna-value/frozen/jaccard.py`、`analysis/tsinghua-factorial-ablation-20261025/frozen/jaccard.py` |
| `journal.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/journal.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/journal.py` |
| `ledger.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/ledger.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/ledger.py` |
| `production.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/production.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/production.py` |
| `report.py` | 2 | `analysis/token-1023-append-20261027/report.py`、`analysis/token-1025-append-20261027/report.py` |
| `run_factorial.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/run_factorial.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/run_factorial.py` |
| `score_factorial.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/score_factorial.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/score_factorial.py` |
| `worker.py` | 2 | `analysis/tsinghua-1024-dna-value/scripts/worker.py`、`analysis/tsinghua-factorial-ablation-20261025/scripts/worker.py` |


典型重复骨架：`freeze_inputs.py`（冻结输入）/ `verify.py`（校验）/ `release.py`（发布）/ `report.py`（出报告）/ `run_checks.py`（跑检查）/ `test_*.py`（测试）。同名副本散落在不同日期目录，彼此无公共实现，也几乎没有交叉引用。

## 一个任务散落三处的查找路径

历史上同一个任务的信息分散在三处，彼此无交叉引用：

| 层 | 位置 | 例子 |
|---|---|---|
| 计划 | `docs/plans/<topic>-<YYYY-MM-DD>.md` | `docs/plans/token-1023-append-2026-10-27.md` |
| 报告 | `docs/investigations/<topic>-<YYYY-MM-DD>.md` | `docs/investigations/token-1023-handoff-confirmation-2026-10-27.md` |
| 脚本 | `analysis/<topic>-<YYYYMMDD>/` | `analysis/token-1023-append-20261027/`（6 个 .py） |

现在由 [`index.json`](index.json) 的 `related_scripts` / `related_docs` 按主题键自动关联：例如 `docs/plans/token-1023-append-2026-10-27.md` 已关联到 `analysis/token-1023-append-20261027/` 下全部 6 个脚本（`append1023.py` / `release.py` / `report.py` / `run_checks.py` / `test_append1023.py` / `verify.py`）以及对应的 handoff 报告。

**推荐查找路径**：读 [`INDEX.md`](INDEX.md) 按主题定位文档 → 查 `index.json` 该文档的 `related_scripts` / `related_docs` → 按 capability 在本文定位具体脚本 → 判断是否复用。

`analysis/` 一级子目录（磁盘实测 **23 个**；其中 **16 个**在限深 3 内含 .py，已登记进 `index.json` 的 `scripts[]`，其余 7 个为不含限深 3 内 .py 的副本 / 资料目录）：

```text
dmo-uncertainty-reading
downloads-pdf-scan
forecast-ledger-legacy-2026-07-24
glm-concurrency-benchmark-20261025
kimi-reasoning-assessment
roadmap-v12-scan
token-1023-append-20261027
token-1025-append-20261027
token-consumption-handoff-20261027-v1
token-consumption-handoff-review-20261027-v1
token-final-readiness-20261026
token-imputation-audit-20261026
token-paper-accounting-20261027
token-readiness-audit-20261026
tsinghua-1024-clean-release
tsinghua-1024-dna-value
tsinghua-1025-vs-may-20261027
tsinghua-baseline-audit-20261022
tsinghua-clean-release-20261027
tsinghua-factorial-ablation-20261025
worldcup-2026
worldcup-2026-review
worldcup-proposal-review
```

## 按 capability 分类（共 185 个）

> `capability` 由 [`tools/build_index.py`](tools/build_index.py) 按文件名确定性推断，取值 `freeze_inputs / verify / release / report / extract / recompute / test / other`。`other` 主要是 `coordinator` / `worker` / `production` / `ledger` / `journal` / `design` 等任务专属业务脚本，无法归入通用能力，按原样登记以免丢条目。


### `freeze_inputs`（5 个）

> 冻结 / 锁定输入（freeze_* / pin_*）。做「冻结数据版本、把输入钉住」时先查这里。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/token-imputation-audit-20261026/freeze_inputs.py`](../analysis/token-imputation-audit-20261026/freeze_inputs.py) | freeze_inputs 能力脚本：freeze_inputs.py | `false` |
| [`analysis/token-imputation-audit-20261026/freeze_thinking.py`](../analysis/token-imputation-audit-20261026/freeze_thinking.py) | freeze_inputs 能力脚本：freeze_thinking.py | `false` |
| [`analysis/token-paper-accounting-20261027/freeze_inputs.py`](../analysis/token-paper-accounting-20261027/freeze_inputs.py) | freeze_inputs 能力脚本：freeze_inputs.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/pin_report_inputs.py`](../analysis/tsinghua-clean-release-20261027/report-work/pin_report_inputs.py) | freeze_inputs 能力脚本：pin_report_inputs.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/freeze_1025_inputs.py`](../analysis/tsinghua-clean-release-20261027/scripts/freeze_1025_inputs.py) | freeze_inputs 能力脚本：freeze_1025_inputs.py | `false` |

### `verify`（39 个）

> 校验 / 审计 / 预检（verify_* / check_* / validate_* / audit_* / preflight / gate / acceptance / smoke / readiness）。数量最多，是重复骨架最严重的类别。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/glm-concurrency-benchmark-20261025/scripts/validate_track_a.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/validate_track_a.py) | verify 能力脚本：validate_track_a.py | `false` |
| [`analysis/token-1023-append-20261027/run_checks.py`](../analysis/token-1023-append-20261027/run_checks.py) | verify 能力脚本：run_checks.py | `false` |
| [`analysis/token-1023-append-20261027/verify.py`](../analysis/token-1023-append-20261027/verify.py) | verify 能力脚本：verify.py | `false` |
| [`analysis/token-1025-append-20261027/run_checks.py`](../analysis/token-1025-append-20261027/run_checks.py) | verify 能力脚本：run_checks.py | `false` |
| [`analysis/token-1025-append-20261027/verify.py`](../analysis/token-1025-append-20261027/verify.py) | verify 能力脚本：verify.py | `false` |
| [`analysis/token-consumption-handoff-20261027-v1/verifier/verify_handoff.py`](../analysis/token-consumption-handoff-20261027-v1/verifier/verify_handoff.py) | verify 能力脚本：verify_handoff.py | `false` |
| [`analysis/token-final-readiness-20261026/readiness.py`](../analysis/token-final-readiness-20261026/readiness.py) | verify 能力脚本：readiness.py | `false` |
| [`analysis/token-imputation-audit-20261026/verify-report.py`](../analysis/token-imputation-audit-20261026/verify-report.py) | verify 能力脚本：verify-report.py | `false` |
| [`analysis/token-paper-accounting-20261027/run_checks.py`](../analysis/token-paper-accounting-20261027/run_checks.py) | verify 能力脚本：run_checks.py | `false` |
| [`analysis/token-paper-accounting-20261027/verify.py`](../analysis/token-paper-accounting-20261027/verify.py) | verify 能力脚本：verify.py | `false` |
| [`analysis/token-readiness-audit-20261026/audit.py`](../analysis/token-readiness-audit-20261026/audit.py) | verify 能力脚本：audit.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/verify_1024.py`](../analysis/tsinghua-1024-dna-value/scripts/verify_1024.py) | verify 能力脚本：verify_1024.py | `false` |
| [`analysis/tsinghua-1025-vs-may-20261027/check_protocol.py`](../analysis/tsinghua-1025-vs-may-20261027/check_protocol.py) | verify 能力脚本：check_protocol.py | `false` |
| [`analysis/tsinghua-1025-vs-may-20261027/parent_verify.py`](../analysis/tsinghua-1025-vs-may-20261027/parent_verify.py) | verify 能力脚本：parent_verify.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/A-baseline-audit/audit_baseline.py`](../analysis/tsinghua-baseline-audit-20261022/A-baseline-audit/audit_baseline.py) | verify 能力脚本：audit_baseline.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/verify_historical.py`](../analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/verify_historical.py) | verify 能力脚本：verify_historical.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/minimax-empty-response-audit-20261027/audit_minimax_empty.py`](../analysis/tsinghua-baseline-audit-20261022/minimax-empty-response-audit-20261027/audit_minimax_empty.py) | verify 能力脚本：audit_minimax_empty.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/check_interface.py`](../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/check_interface.py) | verify 能力脚本：check_interface.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/1023-work/gate_check.py`](../analysis/tsinghua-clean-release-20261027/1023-work/gate_check.py) | verify 能力脚本：gate_check.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/coordinator-tools/audit_public.py`](../analysis/tsinghua-clean-release-20261027/coordinator-tools/audit_public.py) | verify 能力脚本：audit_public.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/smoke_render.py`](../analysis/tsinghua-clean-release-20261027/report-work/smoke_render.py) | verify 能力脚本：smoke_render.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/summary_preflight.py`](../analysis/tsinghua-clean-release-20261027/report-work/summary_preflight.py) | verify 能力脚本：summary_preflight.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/verify_reports.py`](../analysis/tsinghua-clean-release-20261027/report-work/verify_reports.py) | verify 能力脚本：verify_reports.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/verify_1025_handoff.py`](../analysis/tsinghua-clean-release-20261027/scripts/verify_1025_handoff.py) | verify 能力脚本：verify_1025_handoff.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/verify_private_public_1025.py`](../analysis/tsinghua-clean-release-20261027/scripts/verify_private_public_1025.py) | verify 能力脚本：verify_private_public_1025.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/token-work/run_preparation_checks.py`](../analysis/tsinghua-clean-release-20261027/token-work/run_preparation_checks.py) | verify 能力脚本：run_preparation_checks.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/monitoring/verify_replacement_live.py`](../analysis/tsinghua-factorial-ablation-20261025/monitoring/verify_replacement_live.py) | verify 能力脚本：verify_replacement_live.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/smoke_control.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/smoke_control.py) | verify 能力脚本：smoke_control.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/verify_factorial.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/verify_factorial.py) | verify 能力脚本：verify_factorial.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_combined_supplementary.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_combined_supplementary.py) | verify 能力脚本：verify_combined_supplementary.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_continuation.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_continuation.py) | verify 能力脚本：verify_continuation.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_execution.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_execution.py) | verify 能力脚本：verify_execution.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_glm_recovery.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_glm_recovery.py) | verify 能力脚本：verify_glm_recovery.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/acceptance.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/acceptance.py) | verify 能力脚本：acceptance.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/analysis_gate.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/analysis_gate.py) | verify 能力脚本：analysis_gate.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/render_acceptance.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/render_acceptance.py) | verify 能力脚本：render_acceptance.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/verify.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/verify.py) | verify 能力脚本：verify.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/verify_release.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/verify_release.py) | verify 能力脚本：verify_release.py | `false` |
| [`analysis/worldcup-2026/reason_audit_full_2026-07-29.py`](../analysis/worldcup-2026/reason_audit_full_2026-07-29.py) | verify 能力脚本：reason_audit_full_2026-07-29.py | `false` |

### `release`（9 个）

> 发布 / 定稿 / 渲染（release_* / finalize_* / render_* / build_report* / figure）。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/token-1023-append-20261027/release.py`](../analysis/token-1023-append-20261027/release.py) | release 能力脚本：release.py | `false` |
| [`analysis/token-1025-append-20261027/release.py`](../analysis/token-1025-append-20261027/release.py) | release 能力脚本：release.py | `false` |
| [`analysis/token-paper-accounting-20261027/release.py`](../analysis/token-paper-accounting-20261027/release.py) | release 能力脚本：release.py | `false` |
| [`analysis/tsinghua-1024-clean-release/report-work/build_figures.py`](../analysis/tsinghua-1024-clean-release/report-work/build_figures.py) | release 能力脚本：build_figures.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/build_reports.py`](../analysis/tsinghua-clean-release-20261027/report-work/build_reports.py) | release 能力脚本：build_reports.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/finalize_report_family.py`](../analysis/tsinghua-clean-release-20261027/report-work/finalize_report_family.py) | release 能力脚本：finalize_report_family.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/render_reports.py`](../analysis/tsinghua-clean-release-20261027/report-work/render_reports.py) | release 能力脚本：render_reports.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/finalize_1025_data_stage.py`](../analysis/tsinghua-clean-release-20261027/scripts/finalize_1025_data_stage.py) | release 能力脚本：finalize_1025_data_stage.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/finalize_supplementary.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/finalize_supplementary.py) | release 能力脚本：finalize_supplementary.py | `false` |

### `report`（9 个）

> 出报告 / 摘要 / 适配（report_* / summary_* / adapter / adapt_* / compare_report*）。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/token-1023-append-20261027/report.py`](../analysis/token-1023-append-20261027/report.py) | report 能力脚本：report.py | `false` |
| [`analysis/token-1025-append-20261027/report.py`](../analysis/token-1025-append-20261027/report.py) | report 能力脚本：report.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/adapter.py`](../analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/adapter.py) | report 能力脚本：adapter.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/adapter.py`](../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/adapter.py) | report 能力脚本：adapter.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/converter.py`](../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/converter.py) | report 能力脚本：converter.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/adapt_item1.py`](../analysis/tsinghua-clean-release-20261027/report-work/adapt_item1.py) | report 能力脚本：adapt_item1.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/compare_reports.py`](../analysis/tsinghua-clean-release-20261027/report-work/compare_reports.py) | report 能力脚本：compare_reports.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/report_core.py`](../analysis/tsinghua-clean-release-20261027/report-work/report_core.py) | report 能力脚本：report_core.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/summary_report.py`](../analysis/tsinghua-clean-release-20261027/report-work/summary_report.py) | report 能力脚本：summary_report.py | `false` |

### `extract`（15 个）

> 抽取 / 解码 / 恢复（extract_* / decode_* / capture_* / recover_* / restore_* / inspect_* / prepare_* / assemble_*）。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/downloads-pdf-scan/extract.py`](../analysis/downloads-pdf-scan/extract.py) | 通用 PDF 文本抽取，独立于任何按日期命名的任务副本 | `true` |
| [`analysis/glm-concurrency-benchmark-20261025/scripts/recover_sasr54.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/recover_sasr54.py) | extract 能力脚本：recover_sasr54.py | `false` |
| [`analysis/token-1025-append-20261027/capture.py`](../analysis/token-1025-append-20261027/capture.py) | extract 能力脚本：capture.py | `false` |
| [`analysis/token-imputation-audit-20261026/decode_inputs.py`](../analysis/token-imputation-audit-20261026/decode_inputs.py) | extract 能力脚本：decode_inputs.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/minimax-yaml-recovery-20261027/recover_yaml.py`](../analysis/tsinghua-baseline-audit-20261022/minimax-yaml-recovery-20261027/recover_yaml.py) | extract 能力脚本：recover_yaml.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/assemble_1025.py`](../analysis/tsinghua-clean-release-20261027/scripts/assemble_1025.py) | extract 能力脚本：assemble_1025.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/prepare_1025_public_tools.py`](../analysis/tsinghua-clean-release-20261027/scripts/prepare_1025_public_tools.py) | extract 能力脚本：prepare_1025_public_tools.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/public_projection.py`](../analysis/tsinghua-clean-release-20261027/scripts/public_projection.py) | extract 能力脚本：public_projection.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/relocate_1025_data_stage.py`](../analysis/tsinghua-clean-release-20261027/scripts/relocate_1025_data_stage.py) | extract 能力脚本：relocate_1025_data_stage.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/restore_1025_native_usage.py`](../analysis/tsinghua-clean-release-20261027/scripts/restore_1025_native_usage.py) | extract 能力脚本：restore_1025_native_usage.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/token-work/inspect_handoff.py`](../analysis/tsinghua-clean-release-20261027/token-work/inspect_handoff.py) | extract 能力脚本：inspect_handoff.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/recover_paratera.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/recover_paratera.py) | extract 能力脚本：recover_paratera.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/recover_payment.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/recover_payment.py) | extract 能力脚本：recover_payment.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/recover_glm_source.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/recover_glm_source.py) | extract 能力脚本：recover_glm_source.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/recover_minimax_source.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/recover_minimax_source.py) | extract 能力脚本：recover_minimax_source.py | `false` |

### `recompute`（20 个）

> 复算 / 重放 / 打分 / 分析（recompute_* / reproduce_* / replay_* / score_* / analyze_* / compute_* / probe_* / benchmark_*）。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/glm-concurrency-benchmark-20261025/archive/benchmark_glm_concurrency.original.py`](../analysis/glm-concurrency-benchmark-20261025/archive/benchmark_glm_concurrency.original.py) | recompute 能力脚本：benchmark_glm_concurrency.original.py | `false` |
| [`analysis/glm-concurrency-benchmark-20261025/scripts/benchmark_glm_concurrency.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/benchmark_glm_concurrency.py) | recompute 能力脚本：benchmark_glm_concurrency.py | `false` |
| [`analysis/glm-concurrency-benchmark-20261025/scripts/score_track_b.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/score_track_b.py) | recompute 能力脚本：score_track_b.py | `false` |
| [`analysis/token-imputation-audit-20261026/master_table.py`](../analysis/token-imputation-audit-20261026/master_table.py) | recompute 能力脚本：master_table.py | `false` |
| [`analysis/token-imputation-audit-20261026/reproduce.py`](../analysis/token-imputation-audit-20261026/reproduce.py) | recompute 能力脚本：reproduce.py | `false` |
| [`analysis/tsinghua-1024-dna-value/frozen/jaccard.py`](../analysis/tsinghua-1024-dna-value/frozen/jaccard.py) | Jaccard 相似度实现；与 tsinghua-factorial-ablation-20261025/frozen/jaccard.py 构成重复骨架，可作为抽取公共实现的参考 | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/analyze_factorial.py`](../analysis/tsinghua-1024-dna-value/scripts/analyze_factorial.py) | recompute 能力脚本：analyze_factorial.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/design.py`](../analysis/tsinghua-1024-dna-value/scripts/design.py) | recompute 能力脚本：design.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/score_factorial.py`](../analysis/tsinghua-1024-dna-value/scripts/score_factorial.py) | recompute 能力脚本：score_factorial.py | `false` |
| [`analysis/tsinghua-1025-vs-may-20261027/recompute.py`](../analysis/tsinghua-1025-vs-may-20261027/recompute.py) | recompute 能力脚本：recompute.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/B-model-probe/probe_models.py`](../analysis/tsinghua-baseline-audit-20261022/B-model-probe/probe_models.py) | recompute 能力脚本：probe_models.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/reproduce_reports.py`](../analysis/tsinghua-clean-release-20261027/report-work/reproduce_reports.py) | recompute 能力脚本：reproduce_reports.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/compute_1025_statistics.py`](../analysis/tsinghua-clean-release-20261027/scripts/compute_1025_statistics.py) | recompute 能力脚本：compute_1025_statistics.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/frozen/jaccard.py`](../analysis/tsinghua-factorial-ablation-20261025/frozen/jaccard.py) | recompute 能力脚本：jaccard.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/offline-tmp/probe_replay.py`](../analysis/tsinghua-factorial-ablation-20261025/offline-tmp/probe_replay.py) | recompute 能力脚本：probe_replay.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/analyze_factorial.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/analyze_factorial.py) | recompute 能力脚本：analyze_factorial.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/design.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/design.py) | recompute 能力脚本：design.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/prepare_design_preview.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/prepare_design_preview.py) | recompute 能力脚本：prepare_design_preview.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/score_factorial.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/score_factorial.py) | recompute 能力脚本：score_factorial.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/verify_advisory_replay.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/verify_advisory_replay.py) | recompute 能力脚本：verify_advisory_replay.py | `false` |

### `test`（43 个）

> 测试（test_* / run_tests / *_test.py）。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/token-1023-append-20261027/test_append1023.py`](../analysis/token-1023-append-20261027/test_append1023.py) | test 能力脚本：test_append1023.py | `false` |
| [`analysis/token-1025-append-20261027/test_append1025.py`](../analysis/token-1025-append-20261027/test_append1025.py) | test 能力脚本：test_append1025.py | `false` |
| [`analysis/token-1025-append-20261027/test_release_report.py`](../analysis/token-1025-append-20261027/test_release_report.py) | test 能力脚本：test_release_report.py | `false` |
| [`analysis/token-consumption-handoff-20261027-v1/test/test_verify_handoff.py`](../analysis/token-consumption-handoff-20261027-v1/test/test_verify_handoff.py) | test 能力脚本：test_verify_handoff.py | `false` |
| [`analysis/token-final-readiness-20261026/test_readiness.py`](../analysis/token-final-readiness-20261026/test_readiness.py) | test 能力脚本：test_readiness.py | `false` |
| [`analysis/token-paper-accounting-20261027/test_accounting.py`](../analysis/token-paper-accounting-20261027/test_accounting.py) | test 能力脚本：test_accounting.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/A-baseline-audit/test_audit_baseline.py`](../analysis/tsinghua-baseline-audit-20261022/A-baseline-audit/test_audit_baseline.py) | test 能力脚本：test_audit_baseline.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/B-model-probe/test_probe_models.py`](../analysis/tsinghua-baseline-audit-20261022/B-model-probe/test_probe_models.py) | test 能力脚本：test_probe_models.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/test_verify_historical.py`](../analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/test_verify_historical.py) | test 能力脚本：test_verify_historical.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/test_final_synthetic.py`](../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/test_final_synthetic.py) | test 能力脚本：test_final_synthetic.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/test_prep.py`](../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/test_prep.py) | test 能力脚本：test_prep.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/test_interface.py`](../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/test_interface.py) | test 能力脚本：test_interface.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/test_pipeline.py`](../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/test_pipeline.py) | test 能力脚本：test_pipeline.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/test_reports.py`](../analysis/tsinghua-clean-release-20261027/report-work/test_reports.py) | test 能力脚本：test_reports.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/test_1025_isolation_probe.py`](../analysis/tsinghua-clean-release-20261027/scripts/test_1025_isolation_probe.py) | test 能力脚本：test_1025_isolation_probe.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/tests/test_1025_data_statistics.py`](../analysis/tsinghua-clean-release-20261027/tests/test_1025_data_statistics.py) | test 能力脚本：test_1025_data_statistics.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/tests/test_1025_private_safety.py`](../analysis/tsinghua-clean-release-20261027/tests/test_1025_private_safety.py) | test 能力脚本：test_1025_private_safety.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_advisory_resume.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_advisory_resume.py) | test 能力脚本：test_advisory_resume.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_budget.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_budget.py) | test 能力脚本：test_budget.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_dynamic_concurrency.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_dynamic_concurrency.py) | test 能力脚本：test_dynamic_concurrency.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_formal.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_formal.py) | test 能力脚本：test_formal.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_openrouter_reservation_update.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_openrouter_reservation_update.py) | test 能力脚本：test_openrouter_reservation_update.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_paratera_reservation_update.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_paratera_reservation_update.py) | test 能力脚本：test_paratera_reservation_update.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_production.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_production.py) | test 能力脚本：test_production.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_recover_paratera.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_recover_paratera.py) | test 能力脚本：test_recover_paratera.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_recover_payment.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_recover_payment.py) | test 能力脚本：test_recover_payment.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_replace_config_batch.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_replace_config_batch.py) | test 能力脚本：test_replace_config_batch.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_rollback_openrouter_reservation.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_rollback_openrouter_reservation.py) | test 能力脚本：test_rollback_openrouter_reservation.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_smoke.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_smoke.py) | test 能力脚本：test_smoke.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_v31.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_v31.py) | test 能力脚本：test_v31.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_w123.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_w123.py) | test 能力脚本：test_w123.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_w45.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_w45.py) | test 能力脚本：test_w45.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/test_w6.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/test_w6.py) | test 能力脚本：test_w6.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_continue_routes.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_continue_routes.py) | test 能力脚本：test_continue_routes.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_recover_glm_source.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_recover_glm_source.py) | test 能力脚本：test_recover_glm_source.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_recover_minimax_source.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_recover_minimax_source.py) | test 能力脚本：test_recover_minimax_source.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_repair_event1135.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_repair_event1135.py) | test 能力脚本：test_repair_event1135.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_supplement.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_supplement.py) | test 能力脚本：test_supplement.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/run_item2_tests.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/run_item2_tests.py) | test 能力脚本：run_item2_tests.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/run_tests.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/run_tests.py) | test 能力脚本：run_tests.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_acceptance.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_acceptance.py) | test 能力脚本：test_acceptance.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_analysis_gate.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_analysis_gate.py) | test 能力脚本：test_analysis_gate.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_release.py`](../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_release.py) | test 能力脚本：test_release.py | `false` |

### `other`（45 个）

> 任务专属业务脚本（coordinator / worker / production / ledger / journal / design / accounting 等），无法归入通用能力。

| 脚本（仓库相对路径） | 用途 | reusable |
|---|---|---|
| [`analysis/glm-concurrency-benchmark-20261025/scripts/api_client.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/api_client.py) | other 能力脚本：api_client.py | `false` |
| [`analysis/glm-concurrency-benchmark-20261025/scripts/generate_experiments.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/generate_experiments.py) | other 能力脚本：generate_experiments.py | `false` |
| [`analysis/glm-concurrency-benchmark-20261025/scripts/host_job.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/host_job.py) | other 能力脚本：host_job.py | `false` |
| [`analysis/glm-concurrency-benchmark-20261025/scripts/run_stage.py`](../analysis/glm-concurrency-benchmark-20261025/scripts/run_stage.py) | other 能力脚本：run_stage.py | `false` |
| [`analysis/token-1023-append-20261027/append1023.py`](../analysis/token-1023-append-20261027/append1023.py) | other 能力脚本：append1023.py | `false` |
| [`analysis/token-1025-append-20261027/append1025.py`](../analysis/token-1025-append-20261027/append1025.py) | other 能力脚本：append1025.py | `false` |
| [`analysis/token-imputation-audit-20261026/thinking.py`](../analysis/token-imputation-audit-20261026/thinking.py) | other 能力脚本：thinking.py | `false` |
| [`analysis/token-paper-accounting-20261027/accounting.py`](../analysis/token-paper-accounting-20261027/accounting.py) | other 能力脚本：accounting.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/build_factorial_dataset.py`](../analysis/tsinghua-1024-dna-value/scripts/build_factorial_dataset.py) | other 能力脚本：build_factorial_dataset.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/coordinator.py`](../analysis/tsinghua-1024-dna-value/scripts/coordinator.py) | other 能力脚本：coordinator.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/generate_factorial.py`](../analysis/tsinghua-1024-dna-value/scripts/generate_factorial.py) | other 能力脚本：generate_factorial.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/journal.py`](../analysis/tsinghua-1024-dna-value/scripts/journal.py) | other 能力脚本：journal.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/ledger.py`](../analysis/tsinghua-1024-dna-value/scripts/ledger.py) | other 能力脚本：ledger.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/production.py`](../analysis/tsinghua-1024-dna-value/scripts/production.py) | other 能力脚本：production.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/profile_scoring.py`](../analysis/tsinghua-1024-dna-value/scripts/profile_scoring.py) | other 能力脚本：profile_scoring.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/run_factorial.py`](../analysis/tsinghua-1024-dna-value/scripts/run_factorial.py) | other 能力脚本：run_factorial.py | `false` |
| [`analysis/tsinghua-1024-dna-value/scripts/worker.py`](../analysis/tsinghua-1024-dna-value/scripts/worker.py) | other 能力脚本：worker.py | `false` |
| [`analysis/tsinghua-1025-vs-may-20261027/append_findings.py`](../analysis/tsinghua-1025-vs-may-20261027/append_findings.py) | other 能力脚本：append_findings.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/prep.py`](../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/prep.py) | other 能力脚本：prep.py | `false` |
| [`analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/pipeline.py`](../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/pipeline.py) | other 能力脚本：pipeline.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/1023-work/run_readonly.py`](../analysis/tsinghua-clean-release-20261027/1023-work/run_readonly.py) | other 能力脚本：run_readonly.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/coordinator-tools/merge_family.py`](../analysis/tsinghua-clean-release-20261027/coordinator-tools/merge_family.py) | other 能力脚本：merge_family.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/report-work/run_frozen_full.py`](../analysis/tsinghua-clean-release-20261027/report-work/run_frozen_full.py) | other 能力脚本：run_frozen_full.py | `false` |
| [`analysis/tsinghua-clean-release-20261027/scripts/run_1025_isolated.py`](../analysis/tsinghua-clean-release-20261027/scripts/run_1025_isolated.py) | other 能力脚本：run_1025_isolated.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/monitoring/watch_quota_alarm.py`](../analysis/tsinghua-factorial-ablation-20261025/monitoring/watch_quota_alarm.py) | other 能力脚本：watch_quota_alarm.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/runtime-deps/typing_extensions.py`](../analysis/tsinghua-factorial-ablation-20261025/runtime-deps/typing_extensions.py) | other 能力脚本：typing_extensions.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/advisory_resume.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/advisory_resume.py) | other 能力脚本：advisory_resume.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/build_factorial_dataset.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/build_factorial_dataset.py) | other 能力脚本：build_factorial_dataset.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/coordinator.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/coordinator.py) | other 能力脚本：coordinator.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/dynamic_concurrency.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/dynamic_concurrency.py) | other 能力脚本：dynamic_concurrency.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/formal_control.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/formal_control.py) | other 能力脚本：formal_control.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/generate_factorial.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/generate_factorial.py) | other 能力脚本：generate_factorial.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/journal.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/journal.py) | other 能力脚本：journal.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/ledger.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/ledger.py) | other 能力脚本：ledger.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/openrouter_reservation_update.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/openrouter_reservation_update.py) | other 能力脚本：openrouter_reservation_update.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/paratera_reservation_update.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/paratera_reservation_update.py) | other 能力脚本：paratera_reservation_update.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/production.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/production.py) | other 能力脚本：production.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/replace_config_batch.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/replace_config_batch.py) | other 能力脚本：replace_config_batch.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/rollback_openrouter_reservation.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/rollback_openrouter_reservation.py) | other 能力脚本：rollback_openrouter_reservation.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/run_factorial.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/run_factorial.py) | other 能力脚本：run_factorial.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/scripts/worker.py`](../analysis/tsinghua-factorial-ablation-20261025/scripts/worker.py) | other 能力脚本：worker.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/continue_routes.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/continue_routes.py) | other 能力脚本：continue_routes.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/repair_event1135.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/repair_event1135.py) | other 能力脚本：repair_event1135.py | `false` |
| [`analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/supplement.py`](../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/supplement.py) | other 能力脚本：supplement.py | `false` |
| [`analysis/worldcup-2026/fig6_and_metrics_2026-07-26.py`](../analysis/worldcup-2026/fig6_and_metrics_2026-07-26.py) | 世界杯图 6 与指标复算（绑定 2026-07-26 冻结数据，一次性） | `false` |



> 以上为原 `docs/SCRIPTS.md` 第 20–336 行的逐字副本。

