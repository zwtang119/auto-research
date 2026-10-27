# 清华 clean release：一次有界设计审查

2026-10-27｜**内部工作记录，非正式交付；计划仍是唯一正式交付。**

## Context / Scope

已读 `CLAUDE.md`、计划全文与完整 Oracle 导出（三路有效、一路限流无结果）。§6 四项裁定不重开。下文仅为静态设计审查；未委派、未运行验收，未接管实验／补测／token，未读取禁区。

引用别名（均相对 A）：`L=docs/plans/tsinghua-clean-release-2026-10-27.md`；`O=prompt-exports/oracle-plan-2026-10-27-084725-1023-1025-85bb18-7bb5.md`；`T=analysis/token-final-readiness-20261026/readiness.py`；`F=analysis/tsinghua-factorial-ablation-20261025/scripts/analyze_factorial.py`；`I=analysis/tsinghua-baseline-audit-20261022/report-adapter-prep-20261026/INTERFACE.md`。

## Findings / Recommendations — Top 3

1. **token 最终门禁的提供方与可消费证明未闭合。**【Green Source／代码确认】`T:213-224` 无条件返回 NO-GO，不会因交接齐全自行转 PASS。计划同时要求原 gate 真实核验、禁止旁路，又等待上游未实现审批条件（`L:81-83,145`）。【建议】只澄清依赖：哪个上游正式交接将提供可信审批／scope/adoption 验证及其版本化验收入口；未交接就 WAITING。不得让发布层负责补实现，亦不要写“旧 gate 通过”。这不是动态验收结论。

2. **1025 清洁输入到原分析器的诊断适配未定义。**【Green Source／代码确认】`F:125-130` 直接索引 `dataset['costs']` 并输出预算诊断；只包装 `analysis_context` 不解决输入缺字段。计划要求白名单去除这些字段，又要求复用原分析及规范 JSON 精确一致（`L:112,149,240`）。【建议】明确发布副本仅裁掉费用诊断输入／输出依赖，数值函数保持；公私等价只比较白名单后的统计字段，公开重放再比较完整公共结果。不要为适配伪填费用零值，也不必强改 `analyze` 签名。

3. **W7 完成条件先于其报告依赖。**【Green Source／文档确认】离线复算包含报告（`L:159`），但 W7 已要求搬迁断网复算相同，W8 才完成报告且依赖 W7（`L:184-188`）；缺少“可用报告已生成”的阶段边界。【建议】W7 限为脚本／数据／统计就绪，完整报告复算验收移到 W8 后、W9 前；无需另增阶段框架。

## 完整基线的实质遗漏与可删规划

- **接口级漏列一项：**有效基线列 canonical/audit 契约（`O:368-370`）；直接复核 `I:35,50` 确认必须联读 `evaluation_differences`，且它才是分类权威，`duplicate_differences` 已废。`L:95,125` 的保留字段未明确这一点。建议补一句“消费上游该分类及处置结果，旧字段不作权威”，不重做分类／审批。其余关键骨架已覆盖；snapshot 旁路、占位完整、采用后区间一律 NA 等是已拒绝／纠偏项，不算遗漏。
- **可删过度规划：**`L:85` 的断点续构可直接删为“失败保留诊断、新目录全量重建”；保留拒覆盖与发布前验证即可，无需恢复协议。`L:159` 的“每包在线生成／评分入口”宜限定 E23/E25，T 仅离线复算，避免 token 包无故承担实验 runtime。不删完整脚本、990 三格式或必要 provenance，也不增加新任务。
