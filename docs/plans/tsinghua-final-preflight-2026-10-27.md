# 最终阶段前离线预检计划

日期：2026-10-27；执行协调：gpt-6.1-sol。用户批准执行历史验收与3样张视觉/PDF预检，不含全量统计或批量报告。

## Goal / Background

报告适配与统计准备已完成；本轮只补不依赖GLM收齐的两项。当前运行实验、已有适配器及统计准备目录只读，不新增实验模型调用、不修改统计政策、不代替最终审批。

## Approach / Work Items

- [x] H：历史有DNA正式630键与原CSV验收。独占 `analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/`。完成标准：权威/白名单来源可追溯、SHA256盘点、630键与NA/舍入逐列复算；有差异或权威不清则BLOCKED并留证。由父直接复跑后记录结论。代理3170E0E3-4A2C-46EF-AEE2-8918F5548A35。
- [ ] V（部分完成，视觉未确认）：3样张视觉与PDF预检。独占 `analysis/tsinghua-baseline-audit-20261022/report-visual-preflight-20261027/`。完成标准：3PDF、字体/页数/文本检查、实际可见截图与视觉结论或具体工具阻塞；仅新副本可修版式，不改数据。主报告 `docs/reviews/tsinghua-report-visual-preflight-2026-10-27.md`。代理BFE75EFA-4C60-4997-BF5E-504245E77F1E。

两项无相互依赖，并行执行；父核对交付、复算代理断言，不以代理摘要替代验收。

## 父直接复核结果（2026-10-27）

Green Source：父直接运行 `historical-acceptance-20261027/verify_historical.py --out .../parent-rerun-01`，返回 HISTORICAL_AUTHORITY_GATE_PASS、630键、metric_mismatches=0，authority hash与代理交付一致。另直接复跑14项合成回归全部通过。历史统计release仍未审批。

父直接运行 `report-visual-preflight-20261027/scripts/verify_delivery.py`：3PDF页数23/26/35，46可见原文块双引擎检查通过、JSON未改，返回 CONTENT_CHECK_PASS_VISUAL_UNCONFIRMED。当前会话无可见图像，视觉目标未闭合；不声称84页视觉通过，不启动630批量。副本patch未合入原适配器。

## Open Questions / Go-No-Go

- 历史正式白名单/权威如果不唯一，不擅选，不释放历史统计gate。
- PDF页数合同尚需核对；不自行发明。默认折叠报告不等于全文留痕PDF。
- 不进入最终1890全量验收、真实跨期统计、630报告批量或任何付费实验恢复。
- 封存仓库零读写，证据快照只读；既有用户wiki改动不触碰。

## References

- `docs/plans/tsinghua-dna-ablation-2026-10-23.md`
- `docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md`
- `analysis/tsinghua-baseline-audit-20261022/statistics-prep-20261026/README.md`
- `analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/INTERFACE.md`
