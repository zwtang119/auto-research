# 1025 综合与逐案例 PDF 交付计划

日期：2026-10-27；父协调：gpt-6.1-sol。用户批准1份综合报告及全部360份逐案例报告，可并行。

## Goal / Background

F=`analysis/tsinghua-factorial-ablation-20261025`；新增R=`F/reports-20261027`。旧1023/五月管线、原run、脚本、补测及统计只读。无实验API、凭据、字体/浏览器下载，无commit/push。

## Approach / Work Items

- [x] A：独占R/summary，综合PDF/HTML/JSON及验证工具；简洁正文与完整统计附录。
- [x] B：独占R/cases，360份PDF/HTML/JSON与索引；先样张覆盖8臂、3模型、1135及补测，父技术核验放行后批量。
- [x] C：依赖A/B，独占R/verification，独立验证覆盖/来源/数值/原文/PDF，父直接复跑并记录。

A/B并行且不得修改对方目录，不写F根CHANGELOG（父独占），各自有CHANGELOG。其他wiki、legacy、token/1023工作不触碰。

## 口径合同

- 首屏“补充修订（13重评+1格式修复）；不是原预注册完整结果”。原主分析A355/B351、原完整估计/CI NA不覆盖；修订A/B各360。数字直接核对机器JSON。
- 区分指标A与因子A；保留探索性、多重比较、条件依赖、模型评委、长度混淆限制，不宣称现实因果/最优。
- 案例PDF含全部轮次可见回答与三评委完整判定/评分/原始可见回答、来源及修订；完整prompt和reasoning在HTML/JSON，PDF明示未收录思考正文，未打印prompt不得冒称已含。可在PDF加入prompt附录。不补造缺项，不擅改有效解析。
- 按设计键/call_id/hash匹配，不按文件顺序猜。修订保留原失败与新成功，1135原文/修复diff保留且无新发送。
- 本机Chromium离线A4、嵌入CJK字体；旧CSS可参考不修改。无GT、不新增判定。费用未知不补零，不混币种，预留不当花费。
- 不设页数上限。样张技术检查后批量；实际能看图才记目视确认，否则标“构建/内容检查通过、视觉未确认”。允许在此明确边界交付技术版，不称已锁版。

## Go / No-Go

来源/修订映射不清、输入hash变化、正文/数字不一致或泄密则停问；不得猜。机器检查与目视状态分开。父直接核验代理断言。

## Open Questions

按上述范围实施；出现实际不可解映射向用户澄清。

## References

- F/supplementary-scoring-20261027/offline-statistics/{REPORT.md,analysis.json,comparison.json,combined-dataset.json,provenance.json,manifest.json}
- docs/reviews/tsinghua-report-visual-preflight-2026-10-27.md
- analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/adapter.py（只读）
- prompt-exports/oracle-plan-2026-10-27-104827-1025-85a13e-2d74.md仅候选建议，含历史任务/未核实数字；本计划优先，数字必须直接核验，不继承旧任务限制，不自造产品阻塞。

## 父核验记录

待交付后记录命令、结果及视觉边界。

### 2026-10-27 父直接复验与批量放行

Green Source：父运行summary/verify_delivery.py，返回CONTENT_CHECK_PASS_VISUAL_UNCONFIRMED；25页、两指标各32对比/72格、14来源映射、1066原有效保持、16测试、双引擎1730块/317整行与CJK嵌入检查通过。父运行cases/scripts/cases.py verify，返回同状态；360键/1080评分、6388 HTML pre块、1066原有效保持、14修订、9样张共206页，8臂/3模型/1135/三评委补测覆盖。技术样张闸门放行，B继续剩余351PDF。C独立验收已并行启动，只写verification。当前未实际看图，不称视觉通过。以上是本地文件/计算检查，不代表模型输出真实有效。

父直接清点：360 PDF/360 HTML/360 JSON，PyMuPDF逐文件共7255页，PDF总134647216字节；重新扫描7592旧源集合与SHA全部未变，根CHANGELOG冻结前缀未变。B完成全部本地渲染，父全量正文verify与C独立验收继续，暂不把生成完成等同最终内容验收。

最终父直接复跑verification/verify_reports.py --final：FINAL_361_PDFS、361 PDF/7280页、read_only=true、independent=true，所有来源/数字/正文/索引/manifest检查通过；13重评+1格式修复、原1066有效保持、15partial_ontology和1partial_dimensions原记录保留。独立12负向测试父复跑通过。结果保留R/parent-final-verification.json。视觉始终UNCONFIRMED_NOT_VIEWED，未实际目视，不锁版。三个工作项均完成。
