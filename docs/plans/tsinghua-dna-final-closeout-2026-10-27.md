# 1023 DNA配套消融：最终验收—正式统计—报告交付

日期2026-10-27；协调gpt-6.1-sol。用户授权推进至正式统计和报告；两项MiniMax离线YAML恢复已明确批准，不新增实验调用。

## Goal / Background

将GLM v12终态630、Kimi630、MiniMax630冻结为可审计的1890采用集，显式加入已批准的两项解析恢复派生视图，执行既定描述统计并交付630 HTML/PDF/JSON及中文汇总。不改原论文主检验，不作DNA因果归因。

## Approach / 输入

- 工作根：`analysis/tsinghua-baseline-audit-20261022/dna-final-20261027/`；所有既有分析目录、D/冻结数据只读。阶段子目录acceptance/statistics/reports独占，根台账由父协调。
- 规划参考（只读，不把Oracle断言当已确认事实）：`/Users/tangzw119/Documents/GitHub/auto-research/prompt-exports/oracle-plan-2026-10-27-081137-1023-2-5690f8-36e2.md`。多个lane意见不一致时先直接核查。
- 原口径：`docs/plans/tsinghua-dna-ablation-2026-10-23.md:115-125`；报告方案`docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md`计数/路径需实测。复用prep代码在新目录中的明确副本，记录原/新hash。
- 历史来源：historical-acceptance-20261027/parent-rerun-01，父已630×34零失配；overlay manifest固定`f7832c64b3a852654b634116c180a9a6564a0f7a6d673a23f6fbaf98557e991a`。

## Work Items

| 项 | Goal / Done when | Key modules | Dependencies | Size |
|---|---|---|---|---|
| W1 | 新capture、稳定性、630输入/1890原采用与恢复双视图，hash/继承/物理请求逐条清点，父直接复核；无硬冲突才final PASS | acceptance；report-adapter-prep；minimax-yaml-recovery | 无 | L |
| W2 | 两期1260槽、历史judge身份映射及原loader逐项一致；执行预定bootstrap，原协议/恢复版并列；正式输入release hash绑定 | statistics；statistics-prep；historical-acceptance | W1通过及实际政策缺口裁定 | L |
| W3 | 630 bundle/HTML/PDF、全量机器核验、中文汇总、可复算清单；看图不可用则视觉明确未确认 | reports；report-visual-preflight | W1数据；中文汇总依赖W2 | L |

- [x] W1 最终冻结与全量验收（父verify/live、48测试、final export及1890原对象直接核验通过）
- [x] W2 正式统计（双视图正式COMPLETE；父独立重算均值、差值、64个bootstrap区间及hash/CSV通过）
- [x] W3 报告生成与交付核验（630/630父全量只读深检、中文汇总与最终hash通过；视觉未确认）

## Open Questions / Go-No-Go

- 字节门：若所有历史evaluation逐字节相同，遵守严格路径，不人为要求批准无差异例外；实际metadata/byte差异先留证，不能自动放宽旧门；评分/未知差异硬阻断。
- 缺失权重：先核验实际有效覆盖。恢复主视图如每格35有效，则原pooled与格等权数学相同，不制造不必要审批；原协议对照存在缺失时不得暗改主指标，实际有差异再列明裁定。不根据结果有利性选口径。
- MiniMax恢复为已批准视图，原对象/空scores对照永久保留，不扩展一般容错parser，不增加采用/请求数。
- 父技术审批只代表核查后的执行决定，不伪装用户批准尚未裁定政策。
- 报告沿用已预检的默认折叠HTML与明确省略思考的PDF，完整JSON保留；不自行发明页数合同、不虚构GT、不以机器通过代视觉。可生成带明确视觉未确认状态的交付，不宣称完满视觉验收。
- 禁读写封存cds4worldcup；evidence只读，原D不写、不启停、不重评、不调用实验API。既有wiki改动不触碰。

## Verification / References

父逐阶段直接复跑关键验收/测试，记录确认/证伪；每阶段fresh agent，独占写，下一阶段先核前阶段。测试失败/工具失败留证，不空称PASS。参见CLAUDE.md、AGENTS.md以及前述预检/恢复README与PARENT-VERIFICATION。

## 2026-10-27 09:04协调更新

W2准备41/41、W3准备29/29父直接重跑通过。W1旧evidence-04与更新源码不可复现，待原W1唯一lane冻结新candidate后父复跑；不以旧结果放行。控制面路由事件及重复接管停止清单见final根PARENT-COORDINATION-20261027.md。正式统计/630批量尚未运行。

## 正式统计父验收（2026-10-27）

W2两视图正式运行成功且父独立复算全部均值/差值/64个bootstrap区间与hash/CSV通过；W2完成。精确输入、脚本、结果及批准见final根parent-statistics-verification-01与statistics/PARENT-STATISTICS-VERIFICATION-01.md。W3批量仍进行，中文汇总现可使用正式JSON；不得把正式COMPLETE当630报告completion。

## 最终交付（2026-10-27）

W1/W2/W3均已机器验收收口。总入口`analysis/tsinghua-baseline-audit-20261022/dna-final-20261027/reports/DELIVERY-INDEX.html`；中文汇总`reports/summary-01/summary.{html,md}`；630报告ZIP约1.19GB。父全量verify-only exit0（630/630失败0，406.944s），父独立payload/统计/汇总验证与35文件最终manifest逐项hash通过。原ZIP/completion不改，汇总由SUMMARY-STATUS独立承接。视觉未实际确认；PDF省略思考且非完整留痕，JSON完整。无新增实验调用、无git commit/push；既有legacy/wiki及其他工作线改动未触碰。证据见final根PARENT-REPORTS-VERIFICATION-01.md及各parent-*.json。
