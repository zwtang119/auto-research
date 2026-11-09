# link-audit — 全仓 Markdown 内部链接分类清单（dreaming D3）

> 日期：2026-11-09｜扫描时点：**方案 A 接入之后**的实际磁盘状态（含 5 页 wiki、1 页 wiki index、2 个下移层、入库的 `docs/MEMORY.md`）。
> 方法：正则抽取 Markdown 标准链接语法（方括号 + 圆括号，此处不复写原式，避免示例文本自指误报）；排除 http/https/mailto/纯锚点；先 `urllib.parse.unquote`；**双基准**解析（相对 md 所在目录 + 相对仓库根）。
> 处置：**只出清单，不批量改写**。授权：用户 2026-11-09「均同意」P3。

## 汇总

- 内部链接 **761** 条；待处理记录 **337** 条（B 类真断链 **192** + W 类写法不一致 **128** + E 类外部链接 **17**）。
- W 类不是文件丢失，单基准解析会把它误算成断链（首轮 53.0% 虚高即由此而来）。
- E 类与 B2 类位于 `evidence/` 字节级只读区，**永不修改**，会永久留在清单；验收指标是「分类 100%」而非「清零」。

### 与做梦前口径对账

| 项 | 做梦前（首轮） | 本次（补做后） | 说明 |
|---|---:|---:|---|
| 内部链接 | 636 | 761 | 做梦期间共新增 125 条链接（5 页 wiki + wiki index + 2 下移层 + 顶层导航 + 入库记忆页）；新增链接双基准全部可达，未引入新断链 |
| 双基准失败 | 209 | 209 | 数量持平；本次把 17 条 `file://` 单列为 E 类 |
| 其中真断链 B | 209（含 file://） | 192 | 口径收紧：外部链接不再算内部断链 |
| W 类写法问题 | 128 | 128 | 未变，本轮不改 |

> 首轮扫描曾把 `COMPARISON.md` 与本报告方法行里的链接语法示例文本误当真实链接，产生 2 条假阳性；已改写示例文本，并用「生成→复扫→再生成」自洽循环出版本报告。`docs/INDEX.md:63` 的 `../INDEX.md` 同属「待办举例」里的示例文本，已按 B3 登记在下方清单，不是真实缺失目标。

> **2026-11-09 三续复核**：补做 dreaming 新增 21 条链接（710 → 731），复扫后 **B192 / W128 / E17、待处理 337 条完全不变**，说明新增链接全部可达。下方 337 条完整清单逐条未变，仅更新汇总总数与扫描时点——这是 dreaming 维护 representation、防止报告数字 drift 的例行动作。

| 子类 | 条数 | 含义 |
|---|---:|---|
| B1 脚本 / 数据产物路径 | 182 | 逐条见下表 |
| 路径基准写法不一致（建议统一为仓库根相对路径） | 128 | 逐条见下表 |
| 外部 / 证据快照历史链接（只读不修） | 17 | 逐条见下表 |
| B2 证据快照内路径（只读，不修） | 5 | 逐条见下表 |
| B3 文档 / 目录路径 | 5 | 逐条见下表 |

## 完整清单（按子类分组，100% 覆盖）

### B1 脚本 / 数据产物路径（182 条）

| 来源文件 | 行 | 链接目标 |
|---|---:|---|
| `docs/SCRIPTS-DETAILS.md` | 86 | `../analysis/token-imputation-audit-20261026/freeze_inputs.py` |
| `docs/SCRIPTS-DETAILS.md` | 87 | `../analysis/token-imputation-audit-20261026/freeze_thinking.py` |
| `docs/SCRIPTS-DETAILS.md` | 88 | `../analysis/token-paper-accounting-20261027/freeze_inputs.py` |
| `docs/SCRIPTS-DETAILS.md` | 89 | `../analysis/tsinghua-clean-release-20261027/report-work/pin_report_inputs.py` |
| `docs/SCRIPTS-DETAILS.md` | 90 | `../analysis/tsinghua-clean-release-20261027/scripts/freeze_1025_inputs.py` |
| `docs/SCRIPTS-DETAILS.md` | 98 | `../analysis/glm-concurrency-benchmark-20261025/scripts/validate_track_a.py` |
| `docs/SCRIPTS-DETAILS.md` | 99 | `../analysis/token-1023-append-20261027/run_checks.py` |
| `docs/SCRIPTS-DETAILS.md` | 100 | `../analysis/token-1023-append-20261027/verify.py` |
| `docs/SCRIPTS-DETAILS.md` | 101 | `../analysis/token-1025-append-20261027/run_checks.py` |
| `docs/SCRIPTS-DETAILS.md` | 102 | `../analysis/token-1025-append-20261027/verify.py` |
| `docs/SCRIPTS-DETAILS.md` | 103 | `../analysis/token-consumption-handoff-20261027-v1/verifier/verify_handoff.py` |
| `docs/SCRIPTS-DETAILS.md` | 104 | `../analysis/token-final-readiness-20261026/readiness.py` |
| `docs/SCRIPTS-DETAILS.md` | 105 | `../analysis/token-imputation-audit-20261026/verify-report.py` |
| `docs/SCRIPTS-DETAILS.md` | 106 | `../analysis/token-paper-accounting-20261027/run_checks.py` |
| `docs/SCRIPTS-DETAILS.md` | 107 | `../analysis/token-paper-accounting-20261027/verify.py` |
| `docs/SCRIPTS-DETAILS.md` | 108 | `../analysis/token-readiness-audit-20261026/audit.py` |
| `docs/SCRIPTS-DETAILS.md` | 109 | `../analysis/tsinghua-1024-dna-value/scripts/verify_1024.py` |
| `docs/SCRIPTS-DETAILS.md` | 110 | `../analysis/tsinghua-1025-vs-may-20261027/check_protocol.py` |
| `docs/SCRIPTS-DETAILS.md` | 111 | `../analysis/tsinghua-1025-vs-may-20261027/parent_verify.py` |
| `docs/SCRIPTS-DETAILS.md` | 112 | `../analysis/tsinghua-baseline-audit-20261022/A-baseline-audit/audit_baseline.py` |
| `docs/SCRIPTS-DETAILS.md` | 113 | `../analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/verify_historical.py` |
| `docs/SCRIPTS-DETAILS.md` | 114 | `../analysis/tsinghua-baseline-audit-20261022/minimax-empty-response-audit-20261027/audit_minimax_empty.py` |
| `docs/SCRIPTS-DETAILS.md` | 115 | `../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/check_interface.py` |
| `docs/SCRIPTS-DETAILS.md` | 116 | `../analysis/tsinghua-clean-release-20261027/1023-work/gate_check.py` |
| `docs/SCRIPTS-DETAILS.md` | 117 | `../analysis/tsinghua-clean-release-20261027/coordinator-tools/audit_public.py` |
| `docs/SCRIPTS-DETAILS.md` | 118 | `../analysis/tsinghua-clean-release-20261027/report-work/smoke_render.py` |
| `docs/SCRIPTS-DETAILS.md` | 119 | `../analysis/tsinghua-clean-release-20261027/report-work/summary_preflight.py` |
| `docs/SCRIPTS-DETAILS.md` | 120 | `../analysis/tsinghua-clean-release-20261027/report-work/verify_reports.py` |
| `docs/SCRIPTS-DETAILS.md` | 121 | `../analysis/tsinghua-clean-release-20261027/scripts/verify_1025_handoff.py` |
| `docs/SCRIPTS-DETAILS.md` | 122 | `../analysis/tsinghua-clean-release-20261027/scripts/verify_private_public_1025.py` |
| `docs/SCRIPTS-DETAILS.md` | 123 | `../analysis/tsinghua-clean-release-20261027/token-work/run_preparation_checks.py` |
| `docs/SCRIPTS-DETAILS.md` | 124 | `../analysis/tsinghua-factorial-ablation-20261025/monitoring/verify_replacement_live.py` |
| `docs/SCRIPTS-DETAILS.md` | 125 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/smoke_control.py` |
| `docs/SCRIPTS-DETAILS.md` | 126 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/verify_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 127 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_combined_supplementary.py` |
| `docs/SCRIPTS-DETAILS.md` | 128 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_continuation.py` |
| `docs/SCRIPTS-DETAILS.md` | 129 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_execution.py` |
| `docs/SCRIPTS-DETAILS.md` | 130 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/verify_glm_recovery.py` |
| `docs/SCRIPTS-DETAILS.md` | 131 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/acceptance.py` |
| `docs/SCRIPTS-DETAILS.md` | 132 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/analysis_gate.py` |
| `docs/SCRIPTS-DETAILS.md` | 133 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/render_acceptance.py` |
| `docs/SCRIPTS-DETAILS.md` | 134 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/verify.py` |
| `docs/SCRIPTS-DETAILS.md` | 135 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/verify_release.py` |
| `docs/SCRIPTS-DETAILS.md` | 144 | `../analysis/token-1023-append-20261027/release.py` |
| `docs/SCRIPTS-DETAILS.md` | 145 | `../analysis/token-1025-append-20261027/release.py` |
| `docs/SCRIPTS-DETAILS.md` | 146 | `../analysis/token-paper-accounting-20261027/release.py` |
| `docs/SCRIPTS-DETAILS.md` | 147 | `../analysis/tsinghua-1024-clean-release/report-work/build_figures.py` |
| `docs/SCRIPTS-DETAILS.md` | 148 | `../analysis/tsinghua-clean-release-20261027/report-work/build_reports.py` |
| `docs/SCRIPTS-DETAILS.md` | 149 | `../analysis/tsinghua-clean-release-20261027/report-work/finalize_report_family.py` |
| `docs/SCRIPTS-DETAILS.md` | 150 | `../analysis/tsinghua-clean-release-20261027/report-work/render_reports.py` |
| `docs/SCRIPTS-DETAILS.md` | 151 | `../analysis/tsinghua-clean-release-20261027/scripts/finalize_1025_data_stage.py` |
| `docs/SCRIPTS-DETAILS.md` | 152 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/finalize_supplementary.py` |
| `docs/SCRIPTS-DETAILS.md` | 160 | `../analysis/token-1023-append-20261027/report.py` |
| `docs/SCRIPTS-DETAILS.md` | 161 | `../analysis/token-1025-append-20261027/report.py` |
| `docs/SCRIPTS-DETAILS.md` | 162 | `../analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/adapter.py` |
| `docs/SCRIPTS-DETAILS.md` | 163 | `../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/adapter.py` |
| `docs/SCRIPTS-DETAILS.md` | 164 | `../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/converter.py` |
| `docs/SCRIPTS-DETAILS.md` | 165 | `../analysis/tsinghua-clean-release-20261027/report-work/adapt_item1.py` |
| `docs/SCRIPTS-DETAILS.md` | 166 | `../analysis/tsinghua-clean-release-20261027/report-work/compare_reports.py` |
| `docs/SCRIPTS-DETAILS.md` | 167 | `../analysis/tsinghua-clean-release-20261027/report-work/report_core.py` |
| `docs/SCRIPTS-DETAILS.md` | 168 | `../analysis/tsinghua-clean-release-20261027/report-work/summary_report.py` |
| `docs/SCRIPTS-DETAILS.md` | 177 | `../analysis/glm-concurrency-benchmark-20261025/scripts/recover_sasr54.py` |
| `docs/SCRIPTS-DETAILS.md` | 178 | `../analysis/token-1025-append-20261027/capture.py` |
| `docs/SCRIPTS-DETAILS.md` | 179 | `../analysis/token-imputation-audit-20261026/decode_inputs.py` |
| `docs/SCRIPTS-DETAILS.md` | 180 | `../analysis/tsinghua-baseline-audit-20261022/minimax-yaml-recovery-20261027/recover_yaml.py` |
| `docs/SCRIPTS-DETAILS.md` | 181 | `../analysis/tsinghua-clean-release-20261027/scripts/assemble_1025.py` |
| `docs/SCRIPTS-DETAILS.md` | 182 | `../analysis/tsinghua-clean-release-20261027/scripts/prepare_1025_public_tools.py` |
| `docs/SCRIPTS-DETAILS.md` | 183 | `../analysis/tsinghua-clean-release-20261027/scripts/public_projection.py` |
| `docs/SCRIPTS-DETAILS.md` | 184 | `../analysis/tsinghua-clean-release-20261027/scripts/relocate_1025_data_stage.py` |
| `docs/SCRIPTS-DETAILS.md` | 185 | `../analysis/tsinghua-clean-release-20261027/scripts/restore_1025_native_usage.py` |
| `docs/SCRIPTS-DETAILS.md` | 186 | `../analysis/tsinghua-clean-release-20261027/token-work/inspect_handoff.py` |
| `docs/SCRIPTS-DETAILS.md` | 187 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/recover_paratera.py` |
| `docs/SCRIPTS-DETAILS.md` | 188 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/recover_payment.py` |
| `docs/SCRIPTS-DETAILS.md` | 189 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/recover_glm_source.py` |
| `docs/SCRIPTS-DETAILS.md` | 190 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/recover_minimax_source.py` |
| `docs/SCRIPTS-DETAILS.md` | 198 | `../analysis/glm-concurrency-benchmark-20261025/archive/benchmark_glm_concurrency.original.py` |
| `docs/SCRIPTS-DETAILS.md` | 199 | `../analysis/glm-concurrency-benchmark-20261025/scripts/benchmark_glm_concurrency.py` |
| `docs/SCRIPTS-DETAILS.md` | 200 | `../analysis/glm-concurrency-benchmark-20261025/scripts/score_track_b.py` |
| `docs/SCRIPTS-DETAILS.md` | 201 | `../analysis/token-imputation-audit-20261026/master_table.py` |
| `docs/SCRIPTS-DETAILS.md` | 202 | `../analysis/token-imputation-audit-20261026/reproduce.py` |
| `docs/SCRIPTS-DETAILS.md` | 203 | `../analysis/tsinghua-1024-dna-value/frozen/jaccard.py` |
| `docs/SCRIPTS-DETAILS.md` | 204 | `../analysis/tsinghua-1024-dna-value/scripts/analyze_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 205 | `../analysis/tsinghua-1024-dna-value/scripts/design.py` |
| `docs/SCRIPTS-DETAILS.md` | 206 | `../analysis/tsinghua-1024-dna-value/scripts/score_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 207 | `../analysis/tsinghua-1025-vs-may-20261027/recompute.py` |
| `docs/SCRIPTS-DETAILS.md` | 208 | `../analysis/tsinghua-baseline-audit-20261022/B-model-probe/probe_models.py` |
| `docs/SCRIPTS-DETAILS.md` | 209 | `../analysis/tsinghua-clean-release-20261027/report-work/reproduce_reports.py` |
| `docs/SCRIPTS-DETAILS.md` | 210 | `../analysis/tsinghua-clean-release-20261027/scripts/compute_1025_statistics.py` |
| `docs/SCRIPTS-DETAILS.md` | 211 | `../analysis/tsinghua-factorial-ablation-20261025/frozen/jaccard.py` |
| `docs/SCRIPTS-DETAILS.md` | 212 | `../analysis/tsinghua-factorial-ablation-20261025/offline-tmp/probe_replay.py` |
| `docs/SCRIPTS-DETAILS.md` | 213 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/analyze_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 214 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/design.py` |
| `docs/SCRIPTS-DETAILS.md` | 215 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/prepare_design_preview.py` |
| `docs/SCRIPTS-DETAILS.md` | 216 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/score_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 217 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/verify_advisory_replay.py` |
| `docs/SCRIPTS-DETAILS.md` | 225 | `../analysis/token-1023-append-20261027/test_append1023.py` |
| `docs/SCRIPTS-DETAILS.md` | 226 | `../analysis/token-1025-append-20261027/test_append1025.py` |
| `docs/SCRIPTS-DETAILS.md` | 227 | `../analysis/token-1025-append-20261027/test_release_report.py` |
| `docs/SCRIPTS-DETAILS.md` | 228 | `../analysis/token-consumption-handoff-20261027-v1/test/test_verify_handoff.py` |
| `docs/SCRIPTS-DETAILS.md` | 229 | `../analysis/token-final-readiness-20261026/test_readiness.py` |
| `docs/SCRIPTS-DETAILS.md` | 230 | `../analysis/token-paper-accounting-20261027/test_accounting.py` |
| `docs/SCRIPTS-DETAILS.md` | 231 | `../analysis/tsinghua-baseline-audit-20261022/A-baseline-audit/test_audit_baseline.py` |
| `docs/SCRIPTS-DETAILS.md` | 232 | `../analysis/tsinghua-baseline-audit-20261022/B-model-probe/test_probe_models.py` |
| `docs/SCRIPTS-DETAILS.md` | 233 | `../analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/test_verify_historical.py` |
| `docs/SCRIPTS-DETAILS.md` | 234 | `../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/test_final_synthetic.py` |
| `docs/SCRIPTS-DETAILS.md` | 235 | `../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/test_prep.py` |
| `docs/SCRIPTS-DETAILS.md` | 236 | `../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/test_interface.py` |
| `docs/SCRIPTS-DETAILS.md` | 237 | `../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/test_pipeline.py` |
| `docs/SCRIPTS-DETAILS.md` | 238 | `../analysis/tsinghua-clean-release-20261027/report-work/test_reports.py` |
| `docs/SCRIPTS-DETAILS.md` | 239 | `../analysis/tsinghua-clean-release-20261027/scripts/test_1025_isolation_probe.py` |
| `docs/SCRIPTS-DETAILS.md` | 240 | `../analysis/tsinghua-clean-release-20261027/tests/test_1025_data_statistics.py` |
| `docs/SCRIPTS-DETAILS.md` | 241 | `../analysis/tsinghua-clean-release-20261027/tests/test_1025_private_safety.py` |
| `docs/SCRIPTS-DETAILS.md` | 242 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_advisory_resume.py` |
| `docs/SCRIPTS-DETAILS.md` | 243 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_budget.py` |
| `docs/SCRIPTS-DETAILS.md` | 244 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_dynamic_concurrency.py` |
| `docs/SCRIPTS-DETAILS.md` | 245 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_formal.py` |
| `docs/SCRIPTS-DETAILS.md` | 246 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_openrouter_reservation_update.py` |
| `docs/SCRIPTS-DETAILS.md` | 247 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_paratera_reservation_update.py` |
| `docs/SCRIPTS-DETAILS.md` | 248 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_production.py` |
| `docs/SCRIPTS-DETAILS.md` | 249 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_recover_paratera.py` |
| `docs/SCRIPTS-DETAILS.md` | 250 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_recover_payment.py` |
| `docs/SCRIPTS-DETAILS.md` | 251 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_replace_config_batch.py` |
| `docs/SCRIPTS-DETAILS.md` | 252 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_rollback_openrouter_reservation.py` |
| `docs/SCRIPTS-DETAILS.md` | 253 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_smoke.py` |
| `docs/SCRIPTS-DETAILS.md` | 254 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_v31.py` |
| `docs/SCRIPTS-DETAILS.md` | 255 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_w123.py` |
| `docs/SCRIPTS-DETAILS.md` | 256 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_w45.py` |
| `docs/SCRIPTS-DETAILS.md` | 257 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/test_w6.py` |
| `docs/SCRIPTS-DETAILS.md` | 258 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_continue_routes.py` |
| `docs/SCRIPTS-DETAILS.md` | 259 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_recover_glm_source.py` |
| `docs/SCRIPTS-DETAILS.md` | 260 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_recover_minimax_source.py` |
| `docs/SCRIPTS-DETAILS.md` | 261 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_repair_event1135.py` |
| `docs/SCRIPTS-DETAILS.md` | 262 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/test_supplement.py` |
| `docs/SCRIPTS-DETAILS.md` | 263 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/run_item2_tests.py` |
| `docs/SCRIPTS-DETAILS.md` | 264 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/run_tests.py` |
| `docs/SCRIPTS-DETAILS.md` | 265 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_acceptance.py` |
| `docs/SCRIPTS-DETAILS.md` | 266 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_analysis_gate.py` |
| `docs/SCRIPTS-DETAILS.md` | 267 | `../analysis/tsinghua-factorial-ablation-20261025/terminal-acceptance-20261026/test_release.py` |
| `docs/SCRIPTS-DETAILS.md` | 275 | `../analysis/glm-concurrency-benchmark-20261025/scripts/api_client.py` |
| `docs/SCRIPTS-DETAILS.md` | 276 | `../analysis/glm-concurrency-benchmark-20261025/scripts/generate_experiments.py` |
| `docs/SCRIPTS-DETAILS.md` | 277 | `../analysis/glm-concurrency-benchmark-20261025/scripts/host_job.py` |
| `docs/SCRIPTS-DETAILS.md` | 278 | `../analysis/glm-concurrency-benchmark-20261025/scripts/run_stage.py` |
| `docs/SCRIPTS-DETAILS.md` | 279 | `../analysis/token-1023-append-20261027/append1023.py` |
| `docs/SCRIPTS-DETAILS.md` | 280 | `../analysis/token-1025-append-20261027/append1025.py` |
| `docs/SCRIPTS-DETAILS.md` | 281 | `../analysis/token-imputation-audit-20261026/thinking.py` |
| `docs/SCRIPTS-DETAILS.md` | 282 | `../analysis/token-paper-accounting-20261027/accounting.py` |
| `docs/SCRIPTS-DETAILS.md` | 283 | `../analysis/tsinghua-1024-dna-value/scripts/build_factorial_dataset.py` |
| `docs/SCRIPTS-DETAILS.md` | 284 | `../analysis/tsinghua-1024-dna-value/scripts/coordinator.py` |
| `docs/SCRIPTS-DETAILS.md` | 285 | `../analysis/tsinghua-1024-dna-value/scripts/generate_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 286 | `../analysis/tsinghua-1024-dna-value/scripts/journal.py` |
| `docs/SCRIPTS-DETAILS.md` | 287 | `../analysis/tsinghua-1024-dna-value/scripts/ledger.py` |
| `docs/SCRIPTS-DETAILS.md` | 288 | `../analysis/tsinghua-1024-dna-value/scripts/production.py` |
| `docs/SCRIPTS-DETAILS.md` | 289 | `../analysis/tsinghua-1024-dna-value/scripts/profile_scoring.py` |
| `docs/SCRIPTS-DETAILS.md` | 290 | `../analysis/tsinghua-1024-dna-value/scripts/run_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 291 | `../analysis/tsinghua-1024-dna-value/scripts/worker.py` |
| `docs/SCRIPTS-DETAILS.md` | 292 | `../analysis/tsinghua-1025-vs-may-20261027/append_findings.py` |
| `docs/SCRIPTS-DETAILS.md` | 293 | `../analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/prep.py` |
| `docs/SCRIPTS-DETAILS.md` | 294 | `../analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/pipeline.py` |
| `docs/SCRIPTS-DETAILS.md` | 295 | `../analysis/tsinghua-clean-release-20261027/1023-work/run_readonly.py` |
| `docs/SCRIPTS-DETAILS.md` | 296 | `../analysis/tsinghua-clean-release-20261027/coordinator-tools/merge_family.py` |
| `docs/SCRIPTS-DETAILS.md` | 297 | `../analysis/tsinghua-clean-release-20261027/report-work/run_frozen_full.py` |
| `docs/SCRIPTS-DETAILS.md` | 298 | `../analysis/tsinghua-clean-release-20261027/scripts/run_1025_isolated.py` |
| `docs/SCRIPTS-DETAILS.md` | 299 | `../analysis/tsinghua-factorial-ablation-20261025/monitoring/watch_quota_alarm.py` |
| `docs/SCRIPTS-DETAILS.md` | 300 | `../analysis/tsinghua-factorial-ablation-20261025/runtime-deps/typing_extensions.py` |
| `docs/SCRIPTS-DETAILS.md` | 301 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/advisory_resume.py` |
| `docs/SCRIPTS-DETAILS.md` | 302 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/build_factorial_dataset.py` |
| `docs/SCRIPTS-DETAILS.md` | 303 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/coordinator.py` |
| `docs/SCRIPTS-DETAILS.md` | 304 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/dynamic_concurrency.py` |
| `docs/SCRIPTS-DETAILS.md` | 305 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/formal_control.py` |
| `docs/SCRIPTS-DETAILS.md` | 306 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/generate_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 307 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/journal.py` |
| `docs/SCRIPTS-DETAILS.md` | 308 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/ledger.py` |
| `docs/SCRIPTS-DETAILS.md` | 309 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/openrouter_reservation_update.py` |
| `docs/SCRIPTS-DETAILS.md` | 310 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/paratera_reservation_update.py` |
| `docs/SCRIPTS-DETAILS.md` | 311 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/production.py` |
| `docs/SCRIPTS-DETAILS.md` | 312 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/replace_config_batch.py` |
| `docs/SCRIPTS-DETAILS.md` | 313 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/rollback_openrouter_reservation.py` |
| `docs/SCRIPTS-DETAILS.md` | 314 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/run_factorial.py` |
| `docs/SCRIPTS-DETAILS.md` | 315 | `../analysis/tsinghua-factorial-ablation-20261025/scripts/worker.py` |
| `docs/SCRIPTS-DETAILS.md` | 316 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/continue_routes.py` |
| `docs/SCRIPTS-DETAILS.md` | 317 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/repair_event1135.py` |
| `docs/SCRIPTS-DETAILS.md` | 318 | `../analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/supplement.py` |

### 路径基准写法不一致（建议统一为仓库根相对路径）（128 条）

| 来源文件 | 行 | 链接目标 |
|---|---:|---|
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 26 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 47 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 49 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 61 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 83 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 84 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 85 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 86 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 93 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 94 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 95 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 96 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 97 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 104 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 105 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 106 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 107 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 111 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 129 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 129 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 129 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 131 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 131 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 131 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 134 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 134 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 135 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 135 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 139 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 143 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 143 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 143 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 147 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 161 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 162 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 163 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 164 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 165 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 171 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 172 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 173 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 174 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 175 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 176 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 177 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 183 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 184 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 185 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 186 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 187 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 274 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 278 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 282 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 286 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 315 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 317 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 319 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 333 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 340 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 341 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 342 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 343 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 344 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 345 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 346 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/worldcup-four-claims-reassessment-2026-07-27.md` | 347 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-claims-fact-correction-report-2026-07-27.md` | 68 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-claims-fact-correction-report-2026-07-27.md` | 70 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-claims-fact-correction-report-2026-07-27.md` | 82 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/worldcup-claims-fact-correction-report-2026-07-27.md` | 86 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 18 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 20 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 32 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 54 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 55 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 56 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 57 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 64 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 65 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 66 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 67 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 68 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 75 | `analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 76 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 77 | `analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 78 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v2-grouping-2026-07-27.md` | 82 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v1-grouping-2026-07-27.md` | 34 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v1-grouping-2026-07-27.md` | 36 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v1-grouping-2026-07-27.md` | 48 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch1-v1-grouping-2026-07-27.md` | 52 | `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch4-v2-polymarket-2026-07-27.md` | 19 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch4-v2-polymarket-2026-07-27.md` | 23 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch4-v2-polymarket-2026-07-27.md` | 27 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch4-v2-polymarket-2026-07-27.md` | 31 | `analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 15 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 15 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 15 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 17 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 17 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 17 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 20 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 20 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 21 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 21 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 25 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 29 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 29 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 29 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 33 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 47 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 48 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 49 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 50 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 51 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 57 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 58 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 59 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 60 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 61 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 62 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 63 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 69 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 70 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 71 | `evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 72 | `analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md` |
| `analysis/worldcup-2026/_dr-ch2-v3-cds-timeline-2026-07-27.md` | 73 | `analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md` |
| `docs/INDEX.md` | 63 | `docs/INDEX.md` |

### 外部 / 证据快照历史链接（只读不修）（17 条）

| 来源文件 | 行 | 链接目标 |
|---|---:|---|
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 233 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/prompts.py#L51-L63` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 254 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/prompts.py#L91-L99` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 255 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/workflows.py#L163-L199` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 259 | `file:///Users/tangzw119/Documents/GitHub/cds4worldcup/docs/ops/mimo-season-campaign.md#L347-L507` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 303 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/scheduler.py#L52-L68` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 329 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/router/executor.py#L113-L193` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 339 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/workflows.py#L146-L222` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 359 | `file:///Users/tangzw119/Documents/GitHub/cds4worldcup/docs/ops/mimo-season-campaign.md#L244-L277` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 381 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/research.py#L186-L268` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 394 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/research.py#L195-L223` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 454 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/scheduler.py#L116-L176` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 502 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/analyst_daily.py#L41-L62` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 555 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/workflows.py#L87-L104` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/wiki/decisions/institute-one-audit-for-cds4worldcup.md` | 562 | `file:///Users/tangzw119/Documents/GitHub/0ref/institute-one/app/institute/archive.py#L31-L88` |
| `docs/portfolio/FRAMEWORK-RULES.md` | 96 | `file:///Users/tangzw119/.claude/skills/Deli_AutoResearch/SKILL.md` |
| `docs/portfolio/FRAMEWORK-RULES.md` | 111 | `file:///Users/tangzw119/.claude/skills/Deli_AutoResearch/SKILL.md` |
| `docs/portfolio/FRAMEWORK-RULES.md` | 131 | `file:///Users/tangzw119/.claude/skills/Deli_AutoResearch/SKILL.md` |

### B2 证据快照内路径（只读，不修）（5 条）

| 来源文件 | 行 | 链接目标 |
|---|---:|---|
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/docs/index.md` | 7 | `ops/mimo-season-campaign.md` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/dogfood-output/report.md` | 42 | `screenshots/issue-001-step-1.png` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/dogfood-output/report.md` | 45 | `screenshots/issue-001-step-2.png` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/dogfood-output/report.md` | 48 | `screenshots/issue-001-step-3.png` |
| `evidence/cds4worldcup-snapshot-2026-07-20/worktree/dogfood-output/report.md` | 51 | `screenshots/issue-001-result.png` |

### B3 文档 / 目录路径（5 条）

| 来源文件 | 行 | 链接目标 |
|---|---:|---|
| `papers/README.md` | 5 | `../FRAMEWORK-RULES.md` |
| `papers/README.md` | 32 | `../FRAMEWORK-RULES.md` |
| `papers/p1p2-evidence-ledger/wiki/concepts/layer-roles.md` | 11 | `../../../papers/p07-signal-fusion/` |
| `papers/p1p2-evidence-ledger/wiki/concepts/layer-roles.md` | 13 | `../../../papers/p08-market-calibration/` |
| `docs/INDEX.md` | 63 | `../INDEX.md` |

## 处置建议（不执行）

- W 类：若日后统一链接写法，仅改这些链接的路径基准；**本轮不改**，避免批量改写引入新断链。
- B1/B3/B4：需逐条判断「目标已删除 / 拼写错 / 曾规划但未生成」，再决定是否补页或改链；本轮不判断、不修改。
- B2/E：`evidence/` 字节级只读，按项目规则零改动。

## 根因（D5 验收新增）

`python3 docs/tools/build_index.py --check` 退出码 **1**：362 条 path 中 **183 条失效**（182 `scripts` + 1 `readonly_zones` 的 `state/`）。自算复核：`docs[]` 171/171 有效，`scripts[]` 182/185 失效；`index.json` `generated_at=2026-11-05`，`git diff -- docs/index.json` 为 **0**，本轮未改该文件。

把 B1 的 182 条链接目标去掉 `../` 前缀后与失效 scripts 路径比对：**交集 182 / 182（100%）**。即 182 条「断链」与 `index.json` 的 182 条失效脚本是**同一批资产**——对应目录在当前 worktree 不落盘（抽查父目录均不存在；`analysis/` 限深 3 实际只有 3 个 `.py`，而索引登记 185 个）。`state/` 与 `logs/` 目录在本 worktree 同样不存在。

**结论：这些不是链接拼写错误，是索引登记了当前检出环境不存在的资产。** 属 pre-existing（做梦前即存在），非本轮破坏。本轮不重建 `index.json`、不批量改链。若要修复，需先确认：这批脚本应从其他工作区/快照恢复，还是应把 `scripts[]` 标为「历史登记、当前环境不适用」。

> **方案 A 复核**：接入 `docs/MEMORY.md` 后全仓复扫 **731 → 761**（+30 条），B192 / W128 / E17、待处理 337 条仍完全不变；原先指向被忽略的 `.workbuddy/memory/MEMORY.md` 的 3 条链接已全部 repoint 到入库页，残留 0 条。
