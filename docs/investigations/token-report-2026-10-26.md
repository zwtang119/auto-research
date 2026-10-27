# 暂行 token 调用报告（Item 3）

> 2026-10-26；版本 item5-v1。仅 token，不含金额。1023/1025 的实验资源账待完成后追加；本报告不是完整项目总量。权威口径为 `docs/plans/token-report-2026-10-26.md:79-115` 的重要更正，优先于调查中的历史估计。

## 1. 目的、范围与证据约定

报告五月实验的已记录 usage、可辨识的估算及缺口，纳入同研究计划的 model-benchmark 两个阶段，逐批说明二月探索材料的来源限制。不得把这些局部小计加成“完整项目消耗”。

以下 A=`analysis/token-imputation-audit-20261026/`，P=`policysim-research-Tsinghua/`（相邻只读仓），F=`P/archive/pilot-study-2026-02/`。A 是冻结分析输入包，不是 `evidence/` 证据快照。Green Source 表示保存记录的直接读数/确定性复算；Red Source 表示估算，统一注明冻结版本 `item1-v1` 与 estimator id。Item 2 范围及二月裁定采用编排者已复核的任务简报；本次复核范围、未重做的调查明确记在第 11 节。

**数值索引（后文每表沿用这些 ID）：**

| ID | 可复算来源/筛选 | 用途 |
|---|---|---|
| G | A/call-ledger.csv，stage=generation，scope=balanced，按condition汇总total_tokens_value | 匹配三模型生成；S0 |
| E | 同账本 stage=track_a / track_b，按condition、scope汇总 | 评估与GLM拆分 |
| T | 同账本 stage=gt0/gt1/gt2/gt3 的visible_output_chars、planned_calls；KIMI-RATIO / GT-PROMPT-PARTIAL | GT字段计量 |
| O | A/orchestrator-anchor-1023.csv；同账本编排行；ORCH-MEAN | 原生校准记录与五月迁移估算 |
| S | A/scenarios.csv:2-10；A/estimators.yaml:5-43 | S0–S4；先聚合再四舍五入 |
| R | A/orchestrator-reconciliation.json:2-11 | 旧编排数字差额诊断 |
| B | A/reporting-inputs.json 的 benchmark_records / benchmark_sums | Item 2补充冻结计量字段；不冒充Item 1账本 |
| F2 | 用户已复核 Item 2 简报 + 本报告二月表中的原仓 path:line | 文件数量/来源裁定，不是token估算 |

model-benchmark 的 B 冻结字段现以独立 scope=benchmark 追加进统一 ledger；不重抽来源，不并入五月 S0–S4。离线复核入口为 A/verify-report.py。

## 2. 方法：字段级五态与采用顺序

| 状态 | 定义及本报告运用 |
|---|---|
| measured | 同一调用 provider 原生 usage；确定性去除共享副本不变成插补 |
| reconstructed-imputed | 从幸存文本/校准/跨期锚点估算；显式注明对象、估算器及版本 |
| partial | 只恢复部分字段、文本或阶段；不自动具有token值 |
| not-applicable (N/A) | 对指定活动不适用模型API计量；不是整个研究零消耗 |
| unknown | 可能发生消耗而证据不足；null不等于零 |

五态落在字段级：可同时有 measured completion 与 unknown reasoning。采用顺序为：同一调用原生usage → 确定性恢复/共享副本去重 → 有适用性说明的估算单列 → unknown；不强迫总表闭合。

**三条红线：**（1）不把缺失或未知填零，不把估算称实测；（2）不把校准迁移到不同对象而不验证，尤其 Track A 的 combined_output 斜率与固定模板截距不能套 GT 完整 prompt；（3）不以分母错配、共享副本或任意分摊支撑比较。

每个估算器必须声明模型/任务/日期、字符定义（YAML解码后 Python len(str)，Unicode码点）、公式与系数来源、模板固定项、可见/隐藏推理对象、适用域及系统偏差。规格见 A/estimators.yaml:1-45。GT 专用固定项尚未校准，prompt仅partial。调查 `token-report-imputation-feasibility-2026-10-26.md:187-193` 中的中文示例：chars/4 **低估 2.55–3.76倍**，不是高估；该例是外部编码诊断，不是本包估算器或普适系数。增加样本数不能消除共同迁移偏差。

### Supplementary 英文原句（沿用已裁定 Oracle 导出 Q1）

来源：`prompt-exports/oracle-chat-2026-10-26-172349-new-chat-041ac2-9804.md` Q1；以下逐字沿用其中无过期总量的版本。

- **May measured:** “Recorded May generation and evaluation tokens were aggregated at the call level, counting shared usage from each joint MAMR generation once; additional evaluation calls were included in the resource ledger but excluded from balanced architecture comparisons.”
- **GT reconstructed-imputed / partial:** “Visible character counts are directly reproducible for GT-2 and surviving GT-1 outputs, whereas token counts are estimates under explicit encoding assumptions; unrecorded prompt usage and unmetered reasoning are not treated as recovered.”
- **GT-0 partial:** “The 50 GT-0 calls represent the planned design; because original outputs and complete dispatch records were not retained, actual token usage and the total number of physical calls including failures or retries are unknown.”
- **Orchestrator:** “May orchestration token usage was estimated from same-task calls in 1023 rather than native May usage; identical prompt character counts do not establish identical completion usage.”
- **February N/A / unknown:** “LLM API token accounting is not applicable to verified locally synthesized February generation artifacts; unresolved provenance, mixed supplementation, and separate GT or interaction stages are reported separately and do not establish zero usage for February as a whole.”
- **Unknown:** “Error, pending, and null-usage records were not interpreted as zero consumption; failed calls with native usage were included in the resource ledger, while unmetered dispatched calls and records with unresolved dispatch status remained unknown.”
- **MiniMax:** “Native MiniMax reasoning_tokens values of zero were retained, but the presence of reasoning_content precluded interpreting them as absence of reasoning or adding token estimates that might already be included in completion usage.”

## 3. 统一主表：一表看全（item5-v1）

Green Source：A/call-ledger.csv:1 的原生字段和确定性聚合；Red Source：`item1-v1 / ORCH-MEAN、KIMI-RATIO` 估算。唯一主表 A/master-table.csv:1 由 A/master_table.py:1 生成，以下为其完整展示；每行一个 experiment × stage × provider × model。各 token 字段单独标状态，行 state 不代表所有字段完整。整数展示先加总再舍入，CSV 保留未舍入值。`calls` 按本次统一口径计数与token聚合相同的记录集合（含usage缺失记录），1025为journal complete调用记录，benchmark为存活结果；逐行notes给出calls basis。五月joint-run meter、GT-0设计槽位、编排推定槽位不冒充实测HTTP发送；GT-3 calls=0。CSV另保留physical_calls，仅有发送证据时给值，未记录重试不计为零。

<!-- MASTER-TABLE:START -->
| experiment | stage | provider | model | calls | prompt_tokens | completion_tokens | reasoning_tokens | visible_completion_tokens | reasoning_accounting_mode | state | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1023 | generation | openrouter | deepseek/deepseek-v4-flash | 470 (records=470) | 300,424 [measured] | 855,825 [measured] | 789,795 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | generation | openrouter | openai/gpt-oss-120b | 421 (records=421) | 323,880 [measured] | 634,739 [measured] | 223,019 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | generation | paratera | Qwen3.5-122B-A10B | 420 (records=420) | 245,603 [measured] | 2,205,559 [measured] | 2,018,624 [measured] | 186,935 [measured] | included_in_completion | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | orchestrator | openrouter | deepseek/deepseek-v4-flash | 70 (records=70) | 97,355 [measured] | 26,956 [measured] | 19,176 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | orchestrator | openrouter | openai/gpt-oss-120b | 70 (records=70) | 129,659 [measured] | 101,645 [measured] | 83,176 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | orchestrator | paratera | Qwen3.5-122B-A10B | 70 (records=70) | 99,764 [measured] | 294,326 [measured] | 286,780 [measured] | 7,546 [measured] | included_in_completion | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | track_a | paratera | GLM-5.1 | 447 (records=447) | 1,250,822 [partial] (440/447) | 6,490,988 [partial] (440/447) | 6,058,158 [partial] (440/447) | 432,830 [partial] (440/447) | included_in_completion | partial | calls basis=surviving-call-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | track_b | openrouter | moonshotai/kimi-k2.5 | 631 (records=631) | 1,175,468 [measured] | 867,427 [measured] | 852,393 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1023 | track_b | paratera | MiniMax-M2.7 | 632 (records=632) | 1,164,332 [partial] (630/632) | 684,612 [partial] (630/632) | 0 [partial] (630/632) | unknown [unknown] | included_in_completion | partial | calls basis=surviving-call-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | 161 (records=161) | 123,816 [partial] (151/161) | 402,404 [partial] (151/161) | 356,983 [partial] (151/161) | unknown [unknown] | separate_line_item | partial | calls basis=journal-complete-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | generation | openrouter | openai/gpt-oss-120b | 179 (records=179) | 175,075 [partial] (174/179) | 281,061 [partial] (174/179) | 95,289 [partial] (174/179) | unknown [unknown] | separate_line_item | partial | calls basis=journal-complete-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | 196 (records=196) | 129,653 [partial] (187/196) | 922,772 [partial] (187/196) | 840,727 [partial] (187/196) | 82,045 [partial] (187/196) | included_in_completion | partial | calls basis=journal-complete-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | orchestrator | openrouter | deepseek/deepseek-v4-flash | 12 (records=12) | 17,463 [measured] | 3,864 [measured] | 1,865 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=journal-complete-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | orchestrator | openrouter | openai/gpt-oss-120b | 14 (records=14) | 25,975 [measured] | 21,151 [measured] | 18,411 [measured] | unknown [unknown] | separate_line_item | measured | calls basis=journal-complete-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | orchestrator | paratera | Qwen3.5-122B-A10B | 16 (records=16) | 21,930 [measured] | 66,067 [measured] | 64,326 [measured] | 1,741 [measured] | included_in_completion | measured | calls basis=journal-complete-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | track_a | paratera | GLM-5.1 | 229 (records=229) | 653,076 [partial] (225/229) | 3,182,902 [partial] (225/229) | 2,961,369 [partial] (225/229) | 221,533 [partial] (225/229) | included_in_completion | partial | calls basis=journal-complete-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | track_b | openrouter | moonshotai/kimi-k2.5 | 229 (records=229) | 428,711 [partial] (228/229) | 532,489 [partial] (228/229) | 584,554 [partial] (228/229) | unknown [unknown] | separate_line_item | partial | calls basis=journal-complete-records; not a census of unlogged HTTP retries; OpenRouter completion-reasoning is not verified visible output; running snapshot; raw reasoning zero does not establish no thinking; estimator_id=PROVIDER-DIFFERENCE |
| 1025 | track_b | paratera | MiniMax-M2.7 | 231 (records=231) | 429,763 [measured] | 266,406 [measured] | 0 [measured] | unknown [unknown] | included_in_completion | measured | calls basis=journal-complete-records; not a census of unlogged HTTP retries; running snapshot; raw reasoning zero does not establish no thinking |
| 2026-05 | generation | openrouter | gpt-oss-120b | 140 (records=140) | 366,370 [measured] | 390,554 [measured] | unknown [unknown] | unknown [unknown] | separate_line_item | measured | calls basis=joint-run-meters-and-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; reasoning为独立计费项的裁定；五月语义未独立验证，Qwen字符比率不能支持此路径 |
| 2026-05 | generation | openrouter | nemotron-3-super | 170 (records=170) | 143,888 [measured] | 325,285 [measured] | unknown [unknown] | unknown [unknown] | separate_line_item | measured | calls basis=joint-run-meters-and-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; reasoning为独立计费项的裁定；五月语义未独立验证，Qwen字符比率不能支持此路径; nemotron 5月独有未参与1023；deprecated，60%截断及英文泄露，数据不可用于模型比较 |
| 2026-05 | generation | paratera | deepseek-v4-flash | 140 (records=140) | 355,369 [measured] | 428,224 [measured] | unknown [unknown] | unknown [unknown] | included_in_completion | measured | calls basis=joint-run-meters-and-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径 |
| 2026-05 | generation | paratera | qwen3.5-122b | 140 (records=140) | 261,551 [measured] | 2,107,270 [measured] | unknown [unknown] | unknown [unknown] | included_in_completion | measured | calls basis=joint-run-meters-and-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径 |
| 2026-05 | gt0 | paratera | kimi-k2.5 | 25 (records=25) | unknown [partial] (0/25) | unknown [partial] (0/25) | unknown [unknown] | unknown [unknown] | included_in_completion | partial | calls basis=planned-slots; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 路由冲突：冻结config为paratera，后续用户称openrouter；保留冻结值待澄清; 模式仅描述配置路径；本阶段无原生五月completion可验证; planned_calls=25/model; actual sends unknown |
| 2026-05 | gt0 | paratera | minimax-m2.7 | 25 (records=25) | unknown [partial] (0/25) | unknown [partial] (0/25) | unknown [unknown] | unknown [unknown] | included_in_completion | partial | calls basis=planned-slots; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 模式仅描述配置路径；本阶段无原生五月completion可验证; planned_calls=25/model; actual sends unknown |
| 2026-05 | gt1 | paratera | kimi-k2.5 | 10 (records=10) | unknown [partial] (0/10) | unknown [unknown] | unknown [unknown] | 17,134 [reconstructed-imputed] | included_in_completion | reconstructed-imputed | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 路由冲突：冻结config为paratera，后续用户称openrouter；保留冻结值待澄清; 模式仅描述配置路径；本阶段无原生五月completion可验证; surviving successful annotations only; retries unknown; estimator_id=GT-PROMPT-PARTIAL;KIMI-RATIO |
| 2026-05 | gt1 | paratera | minimax-m2.7 | 10 (records=10) | unknown [partial] (0/10) | unknown [unknown] | unknown [unknown] | unknown [unknown] | included_in_completion | partial | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 模式仅描述配置路径；本阶段无原生五月completion可验证; surviving successful annotations only; retries unknown; estimator_id=GT-PROMPT-PARTIAL |
| 2026-05 | gt2 | paratera | kimi-k2.5 | 630 (records=630) | unknown [partial] (0/630) | unknown [unknown] | unknown [unknown] | 1,060,348 [reconstructed-imputed] | included_in_completion | reconstructed-imputed | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 路由冲突：冻结config为paratera，后续用户称openrouter；保留冻结值待澄清; 模式仅描述配置路径；本阶段无原生五月completion可验证; surviving successful annotations only; retries unknown; estimator_id=GT-PROMPT-PARTIAL;KIMI-RATIO |
| 2026-05 | gt2 | paratera | minimax-m2.7 | 630 (records=630) | unknown [partial] (0/630) | unknown [unknown] | unknown [unknown] | unknown [unknown] | included_in_completion | partial | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 模式仅描述配置路径；本阶段无原生五月completion可验证; surviving successful annotations only; retries unknown; estimator_id=GT-PROMPT-PARTIAL |
| 2026-05 | gt3 | unknown | not-applicable | 0 (records=1) | N/A [not-applicable] | N/A [not-applicable] | N/A [not-applicable] | N/A [not-applicable] | unknown | not-applicable | calls basis=rule-based; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; mode unknown：glm-coding不是已裁定的两provider路径；GT-3无模型调用 |
| 2026-05 | orchestrator | openrouter | gpt-oss-120b | 70 (records=70) | 129,659 [reconstructed-imputed] | 101,645 [reconstructed-imputed] | unknown [unknown] | unknown [unknown] | separate_line_item | reconstructed-imputed | calls basis=inferred-orchestration-slots; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; reasoning为独立计费项的裁定；五月语义未独立验证，Qwen字符比率不能支持此路径; 模式仅描述配置路径；本阶段无原生五月completion可验证; estimator_id=ORCH-MEAN |
| 2026-05 | orchestrator | paratera | deepseek-v4-flash | 70 (records=70) | 97,355 [reconstructed-imputed] | 26,956 [reconstructed-imputed] | unknown [unknown] | unknown [unknown] | included_in_completion | reconstructed-imputed | calls basis=inferred-orchestration-slots; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 模式仅描述配置路径；本阶段无原生五月completion可验证; estimator_id=ORCH-MEAN |
| 2026-05 | orchestrator | paratera | qwen3.5-122b | 70 (records=70) | 99,764 [reconstructed-imputed] | 294,326 [reconstructed-imputed] | unknown [unknown] | unknown [unknown] | included_in_completion | reconstructed-imputed | calls basis=inferred-orchestration-slots; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 模式仅描述配置路径；本阶段无原生五月completion可验证; estimator_id=ORCH-MEAN |
| 2026-05 | track_a | glm-coding | glm-5.1-coding | 460 (records=460) | 1,206,758 [measured] | 2,219,974 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; mode unknown：glm-coding不是已裁定的两provider路径；GT-3无模型调用; 路由冲突：冻结config为glm-coding/智谱coding endpoint，后续用户称paratera；保留冻结值待澄清 |
| 2026-05 | track_a | paratera | glm-5.1 | 170 (records=170) | 545,289 [measured] | 793,786 [measured] | unknown [unknown] | unknown [unknown] | included_in_completion | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径 |
| 2026-05 | track_b | paratera | glm-5.1 | 298 (records=298) | 730,375 [measured] | 717,177 [measured] | unknown [unknown] | unknown [unknown] | included_in_completion | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径 |
| 2026-05 | track_b | paratera | kimi-k2.5 | 630 (records=630) | 1,098,123 [measured] | 223,582 [measured] | unknown [unknown] | unknown [unknown] | included_in_completion | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径; 路由冲突：冻结config为paratera，后续用户称openrouter；保留冻结值待澄清 |
| 2026-05 | track_b | paratera | minimax-m2.7 | 630 (records=630) | 1,094,083 [measured] | 670,907 [measured] | unknown [unknown] | unknown [unknown] | included_in_completion | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; 5 月 reasoning 不可拆（GT-3 N/A）；provider 为冻结配置，非逐调用路由回执; completion 含思考是paratera路径语义裁定，不表示五月拆分实测；Qwen 7.82/6.67仅支持paratera路径 |
| benchmark | benchmark-generation | unknown | deepseek-v4-flash | 18 (records=18) | 1,683 [measured] | 86,271 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | deepseek-v4-pro | 18 (records=18) | 1,683 [measured] | 94,036 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | glm-5.1 | 18 (records=18) | 1,730 [measured] | 74,241 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | kimi-k2.5 | 18 (records=18) | 1,748 [measured] | 23,468 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | kimi-k2.6 | 18 (records=18) | 1,748 [measured] | 36,180 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | mimo-v2.5-pro | 18 (records=18) | 6,310 [measured] | 49,698 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | minimax-m2.7 | 18 (records=18) | 2,051 [measured] | 32,535 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-generation | unknown | qwen3.6-plus | 18 (records=18) | 1,840 [measured] | 84,423 [measured] | unknown [unknown] | unknown [unknown] | unknown | measured | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | deepseek-v4-flash | 493 (records=493) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | deepseek-v4-pro | 386 (records=386) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | glm-5.1 | 386 (records=386) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | kimi-k2.5 | 493 (records=493) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | kimi-k2.6 | 386 (records=386) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | mimo-v2.5-pro | 386 (records=386) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | minimax-m2.7 | 386 (records=386) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
| benchmark | benchmark-judge | unknown | qwen3.6-plus | 386 (records=386) | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown [unknown] | unknown | unknown | calls basis=surviving-call-records; not a census of unlogged HTTP retries; provider 未冻结；model 为原样目录标签；calls为存活结果数，遗漏重试unknown |
<!-- MASTER-TABLE:END -->

**主表脚注（必须与数字一起阅读）：**

1. **provider 语义不同，是最重要的计量陷阱。** paratera 为 `included_in_completion`；1023/1025 OpenRouter 按用户授权标 `separate_line_item`。原生字段及不一致是 Green Source，独立计费解释仍须计量协议核对，不由 pricing 字段或 reasoning>completion 单独证明。原生 total 不自动加 reasoning。OpenRouter 的 completion−reasoning 不足以证实可见输出，因此本表 visible 标 unknown；旧算术差额保留在 ledger 供审计。paratera 仅在拆分一致且无 zero-with-content 时提供字段差额。
2. **5 月 reasoning 不可拆出**：模型阶段为空/null + unknown，GT-3 为 N/A，绝不填 0。五月 provider 来自冻结配置，非历史逐调用路由回执；gpt-oss 为 OpenRouter，不能按模型名推定。Qwen 五月 452,057/57,801=7.82、1023 443,310/66,419=6.67 token/字符，支持限定于 paratera 的包含口径，不外推至任何OpenRouter行。冻结配置中Kimi/MiniMax实际均为paratera；此前概称两者为OpenRouter不正确。
3. **1023/1025 为运行中快照**：2026-10-26T10:56:25.937944+00:00–2026-10-26T10:56:30.333853+00:00，非原子停写。1023 已按 realpath 去重；1025 按 journal call_id 中 generation/summary/score 任务身份拆阶段，不按模型猜阶段。完成后必须按 A/append-1023-1025-checklist.md:1 追加重算，当前不是最终资源总量。
4. **nemotron-3-super 为五月独有，未参与1023，已 deprecated**；编排者核验的 config 标注 60% 截断与英文泄露、数据不可用，不能与1023/1025作模型比较，但已发生的记录保留于资源账。
5. `reasoning_tokens=0` 保留 provider 原值，不表示无思考；全快照 reasoning measured 4,460 条，538 条（12.06%）大于 completion，929 条 zero-with-content。1023 GLM 440 条：reasoning **6,058,158 / completion 6,490,988 = 93.33%**，可见差额 432,830。部分字段只报已知小计及覆盖数，unknown 不作零。
6. 五月 generation 含不匹配资源；用于架构比较须筛 `scope=balanced`：SASR 808,076（315 meters）、MAMR 3,101,262（105 joint-run meters），合计3,909,338。全部评估9,300,054已含额外GLM 1,447,552，不能另加。GT-0 50为设计槽位；GT-1/2仅存活成功产物，不是重试完整清单。
7. ORCH-MEAN 五月估算749,705，来自1023的210条锚点（prompt 326,778、completion 422,927），不是五月实测；旧742,055未复现，749,714与749,705差9，另7,650无可追溯公式，不能叫舍入。GT-2 Kimi可见估算1,060,348（敏感性1,037,174–1,084,582，非CI），GT-1为17,134；MiniMax原生completion未知，不用代理补主表。
8. benchmark 原样模型标签仅来自冻结路径，provider 未保存在计量字段附录，故 unknown；144生成结果有usage，3,302评分结果无usage。calls按这些存活结果记录计数；实际完整HTTP发送数/重试不能由存活文件数推断。没有合格估算器则不插补。

**本次路由复核及未解决冲突：** `inputs.zip` 内 `P/config/experiment-config.yaml` 与 `decoded-inputs.json` 一致：gpt-oss/nemotron=openrouter，DeepSeek/Qwen/GLM-5.1/MiniMax/Kimi=paratera，GLM-5.1-coding=glm-coding（`https://open.bigmodel.cn/api/coding/paas/v4`）。后续用户指定Kimi=openrouter、GLM-coding=paratera与该冻结证据不符，当前保留冻结provider并在对应行标注冲突。不得将用户指定路由冒充配置原文。所有五月paratera行mode=included_in_completion，所有openrouter行mode=separate_line_item；这是provider语义裁定，不是五月reasoning拆分实测。GLM-coding路径尚无适用语义裁定故unknown；GT-3无调用故unknown/N/A。benchmark缺provider字段，不能借五月配置推断其路由，保持unknown。

## 4. 5 月与 1023/1025 的可比性

Green Source：编排者已复核的同模型同条件 **SASR 每 run completion**（只比较保存的 completion 字段，不等于跨 provider 全部计费 token）。数值沿用 `docs/plans/token-report-2026-10-26.md:117-140` 的比较裁定，不重新抽取五月。

| 模型 | 5 月每 run completion | 1023 每 run completion | 变化 |
|---|---:|---:|---:|
| qwen3.5-122b | 4,305 | 4,326 | +0.5%，基本一致 |
| deepseek-v4-flash | 800 | 1,194 | +49% |
| gpt-oss-120b | 814 | 1,299 | +60% |
| nemotron-3-super（不进入 matched 比较） | 1,916 | 未使用 | — |

Qwen的7.82与6.67 token/字符比较仅是 **paratera路径观察**；它不支持OpenRouter的五月completion是否包含reasoning，也不能恢复任何五月逐调用拆分。OpenRouter separate_line_item是本次授权的独立计费项裁定，五月语义未独立验证。

“五月明显偏低”不能概括为全部模型或漏算思考，须区分三个叠加因素：

**(a) 模型构成与分母：** 五月 SASR 400 runs 中有85个 nemotron（21.25%），它每 run 1,916，比 DeepSeek 800 / gpt-oss 814 高，但低于 Qwen 4,305；不能误写成“三主模型最高”。纳入它同时增加五月分子、分母，并缩小与1023整体均值的表观差距。按表中舍入值作说明，五月 matched-3 均值约1,973，混入nemotron后约1,961；1023 matched-3约2,273。严格 matched 口径下五月 SASR 更低，nemotron 仍须排除。

**(b) run 数与计量单元：** 五月 SASR为3模型×105=315，加85个nemotron=400；平衡MAMR为3模型×35=105个joint-run meters，产生315个企业产物。1023 SASR为3模型×35=105，MAMR为3模型×35=105个联合runs；每模型35 SASR＋35 MAMR=70个架构episodes，而非210个episodes。生成可包含多轮HTTP发送和重试，主表物理记录数不能当这些run数。brief中“每模型105 MAMR”“210 runs/模型”混淆了企业产物与run，已在此澄清；不可用主表所有generation（含unmatched资源）替代matched分母。

**(c) 模型族的已观察差异：** DeepSeek、gpt-oss分别高约49%/60%，Qwen仅约0.5%。编排者已核验两期 max_tokens 均为2048，不能归因于输出上限变化。不过DeepSeek五月配置为paratera、1023实际请求为OpenRouter，provider路由与语义同时变化；这证明保存字段的差异，**不能单独归因为模型本身变贵或生成更长**。

**推荐口径：matched 3 模型 × matched run 数 × per-run 均值**，限定相同条件/阶段与provider语义；SASR与MAMR分开比较。**禁止口径：直接比总量**，因为run数、模型数、阶段数不同。1025还是不同设计的运行中快照，当前没有本节同条件matched估计，不能把1023的+49%/+60%直接外推到1025。跨期差异不是因果实验，也不能据此证明所有五月usage完整。

旧独立thinking表已撤并；A/thinking-tokens-1023-1025.csv仅为主表筛选视图，附件保留范围与provider语义说明。

## 5. 五情景（Red Source项均冻结item1-v1）

| 情景 | 数字与对象（S） | 最主要可争议假设 |
|---|---|---|
| S0 measured baseline | 生成3,909,338；共同产出3.8378×，episode 11.5135× | 只覆盖已记录生成，未包括缺失阶段 |
| S1 + ORCH-MEAN | 编排749,705；MAMR生成+编排3,850,967；两条件4,659,043；共同产出4.7656×，episode 14.2968× | 跨期同任务均值能否迁移；非实测比较 |
| S2 KIMI-RATIO | GT-2 Kimi可见completion中心1,060,348；敏感性1,037,174–1,084,582 | 共同编码/任务偏差；不能当CI |
| S3 MINIMAX-SCENARIO | **1,058,844 visible-token-equivalent**（Kimi编码代理）与 **3,507,421 completion情景**（字符/0.608）；差2,448,577 | 两者是不同对象、不是上下界；差额也不是恢复出的reasoning |
| **S4 LEGACY-DIAGNOSTIC：仅历史失效诊断** | 历史输入总量25,375,098及端点23,649,443–26,018,830；旧编排742,055；强制GT各半后，生成+编排+GT比1.4655×（1.4436–1.5365）；加实测条件评估后1.5836×（1.5651–1.6398） | GT prompt模板错位、强制各半无证据、GLM不平衡；全部是旧算法演算，非实际消耗或有效区间 |

S1原表保留742,055与749,714作为未采用对照，只用于差额审计。**S4不得进入摘要、主结果或有效区间，不是完整项目估计。** GT-2字符并不对半，GT-1种子也不对半；不能靠分摊共享GT把架构比压近一。

## 6. 更正后的头条比值

**主报3.8378×，辅报11.5135×；原11.3283×撤回。** Green Source G/S0：

- 共同企业产出单位：3,101,262 / 808,076 = 3.8378×。两边都是315企业产物。
- 每架构episode：(3,101,262/105) / (808,076/315) = 11.5135×。一次MAMR产出三企业，一次SASR产出单企业。
- 原式：(9,303,786/315)/(1,042,908/400)=11.3283×。9,303,786是**已撤回的三倍共享副本朴素和**；SASR旧分母又混入85份不匹配nemotron。旧式仅作错误说明，来源 A/summary.md:19-21 与冻结原始文件。

可直接用于审稿说明：
> 在匹配三种生成模型并去除 MAMR 共享 usage 副本后，MAMR 与 SASR 的已记录生成 token 比在共同企业产出单位下为 3.8378×，在各自架构 episode 单位下为 11.5135×；后者比较一次三企业联合生成与一次单企业生成。两项结果均不含编排摘要、GT 或评估阶段。

更正登记见 `token-report-corrections-2026-10-26.md` 与同名CSV。旧11.51×数值可等于episode比，但原表把MAMR三个副本当315独立观测、未注明单位仍须改；旧效应量/显著性不能沿用。

## 7. 二月探索材料逐批裁定

数量与来源为 **Green Source F2（编排者已复核Item 2）**；不是Item 1 token ledger，均不得字符换算为消耗。

| 批次/活动 | 存活产物/范围（F2） | token裁定 | 证据与含义 |
|---|---|---|---|
| 02-19 | 54输出文件 | 所有token栏unknown | F/mc-2026-02-19/README.md:3仍为待执行；来源未证实，不能推定API调用或本地生成 |
| 02-21 | 2,451 + 51文件 | 指定命名模型的产物生成N/A | F/mc-2026-02-21/EXECUTION-INSIGHTS.md:28,33-35披露平台限制、人工补全、Python填充；本次采用Item 2更细批次裁定，而非旧调查笼统mixed |
| 02-22 | 250 Kimi + 990其他 + 50 + 40；GT占位及h3脚本 | N/A | F/mc-2026-02-22/EXECUTION-INSIGHTS.md:1259-1261,1279,1562,1571为脚本生成；gt_annotation_gpt4o.py:39-44为placeholder，无模型调用 |
| 02-23 | 270；过程副本270逐字节相同，只计一套 | 命名模型实验调用N/A | F/mc-2026-02-23/experiment-plan/OPERATION-LOG.md:11-45执行者Agent；CMD-P1-00*.md为IDE agent手写YAML指令，不是指定模型API实验证据 |
| 02-26 | 244 raw + 3 GT | 命名模型实验调用N/A | IDE agent/本地编制；不是命名模型API输出的已核验样本 |
| 02-26 generate_gt_gpt5mini.py | API代码存在，执行未证 | unknown | F/mc-2026-02-26/scripts/generate_gt_gpt5mini.py:36,48,62；代码不等于执行 |

F2补充裁定：二月树唯一API/provider代码在上述GT脚本；批量生成脚本伪造hash的正确位置是 **F/batch_generate_gpt4o_p2a_agents.py:17**，不是旧调查的27。已提交GT的 `gt_annotation.metadata.{annotator,timestamp,total_runs_analyzed}` 与 `effects:` schema不符合该脚本输出，文件timestamp为2026-02-25T00:00:00，与脚本datetime.now().isoformat()不符，而且不在2026-02-25 zip中，故不能归因于该脚本实际执行。此处因果裁定基于Item 2组合证据，不仅基于时间戳。

F/mc-2026-02-22/scripts/h3_cost_benefit.py:214-215的18,000/2,000是硬编码演示值，不是消耗；F/meta/20-model-manifest.md:63-72只是价格表，没有调用数或计量；F/mc-2026-02-26/prompts/PROMPT-MAMR.md没有landscape/集中摘要结构，不能迁入五月的调用结构。IDE agent编写过程可能使用tokens，但不属于命名模型实验调用；其消耗另为unknown，N/A不能概括为二月整体零消耗。

**面向审稿人的措辞：**
> 早期材料含本地模板/随机合成及来源未能核实的探索性产物；不作为独立 LLM 调用或模型能力比较的实证样本，不纳入 API token 统计。可核验 API 实验另行报告。

必须同时披露：P/paper/10-draft/draft-0316.md:49,71,75,89,349曾用“实验设计”“244轮推演”“270次蒙特卡洛模拟”等正式实验措辞，并据此作能力论断。仅改称pilot不足以消除误导；上述句子进入单独更正项。该稿没有token数，不能作为五月比值来源。

## 8. 纳入范围

| 活动 | 决定 | 计量或理由 |
|---|---|---|
| model-benchmark generation | **INCLUDE** | Green Source B：144/144存活文件有token_count；prompt **18,793**、completion **480,852**、total **499,645** measured；不是完整发送覆盖率 |
| model-benchmark judge/tournament | **INCLUDE，单独行** | B：3,088 comparisons + 214 scores = **3,302**存活调用结果，无token字段；本报告unknown，没有合格估算器，不自行插补 |
| legacy/p11-* | EXCLUDE | 已关闭的独立论文线；本阶段不并入 |
| docs/papers-closed-portfolio/experiments/direction_a/ | EXCLUDE + 计量陷阱登记 | 另一论文；completion_tokens实际为len(content)，详见下节 |
| papers/（p07/p08/p12/p1p2） | EXCLUDE | 不同论文/问题；与direction_a不同，其review记录存在真实provider completion字段；p12主judge有丢usage，若未来做组合级报告需另审 |
| analysis/kimi-reasoning-assessment/ | EXCLUDE | 文献笔记，不是调用实验 |
| cds4polymarket/experiments/ | EXCLUDE | WorldCup足球因子校准，另一研究计划；只有prompt_chars/response_chars不能改称token，阅读不等于纳入 |
| 1023/1025资源账 | DEFER | 实验未终结；见第10节，现有校准锚点不代表资源账已纳入 |

model-benchmark属于同研究计划：P/model-benchmark/questions/D1-3.yaml:5直接询问本研究结果；P/docs/analysis_for_paper_upgrade.glm51.md:479列作论文来源（Green Source F2）。范围认定优先于文件夹名。

[^concurrency]: `analysis/glm-concurrency-benchmark-20261025/` 排除于账本总量，仅作技术测试说明：11 HTTP sends，9 measured合计157,199，1 error + 1 pending为unknown（Green Source：Item 2编排者已复核简报；本次未重读测试目录、不并入Item 1）。

范围补注见并发测试脚注[^concurrency]。

## 9. 审稿人最容易发现的计量陷阱

1. **字符伪装成token：** auto-research/docs/papers-closed-portfolio/experiments/direction_a/run_review_round_1.py:136接收后丢弃usage，:151写入 `completion_tokens: len(content)`；results/review_round_1.json继承该字段。名称不能证明计量来源，必须标为visible_output_chars；本次不求和，也不修改源文件。
2. **MAMR共享usage三倍计数：** 三企业文件是同一个joint-run meter，不是三个独立token观测；旧9,303,786仅作撤回值展示。
3. **11.3×/11.51×并存：** P/wiki/annotations/current-state.md:98,142口径冲突；后一数也必须注明episode分母。
4. **MiniMax reasoning=0：** provider原字段保留，但不能解释为无推理，也不能向可能已含推理的completion再加代理量。
5. **GT-0输出丢失：** 设计调用数不是物理发送数，解析合并结构不是原始输出，没有可靠completion下界。
6. **二月脚本/IDE合成：** 产物数量、伪造hash、模型标签或价格表不能替代API provenance；正式实验措辞须更正。

7. **completion token 语义因 provider 而异：** paratera 已核实 completion 含思考，不能把 GLM 约649万 completion 误读为可见文本；OpenRouter reasoning 另列且可能大于 completion，禁止跨 provider 一律做减法或加法。见第3节及字段覆盖列。

## 10. 1023/1025追加区——明确占位，当前无资源总数

**本节规定最终追加动作；第3节提供运行中快照，不代表阶段二完整资源账。**

执行版见 A/append-1023-1025-checklist.md。顺序：

1. 等待两个实验分别提供complete标记、退出码及停写确认；缺一则不冻结/抽取。
2. 在新的analysis追加目录冻结calls、journal及完成凭据，记录UTC时间、原路径、SHA-256、文件别名映射；先冻结再抽取，所有提取程序只读冻结副本。
3. 1023必须按 `os.path.realpath` 解析五路目录别名，冻结前保留alias→realpath映射；只折叠同一物理文件，真实重发/替换不能按fingerprint折叠。
4. 1025 token以journal为准，以call_id/attempt关联prepared与complete；`provider-ledger.json`只有金额，不能替代token；raw token_usage为空也不能填零。
5. 使用Item 1同schema生成新stage行，额外身份信息放sidecar；error/pending/null usage保留unknown，usage覆盖率说明分母。
6. 在新版本生成combined ledger：逐字节保留interim行，仅ADD新行；独立保留中间版文件、快照和数字，不能覆盖本次账本或报告。
7. 对新数据按阶段/任务/模型重新定义可比较单位，报告新的S0–S4适用性与比值；保留五月历史S0–S4，不把不同实验简单相加为统一架构比。必要时仍保留unknown，不强迫完整总量。
8. 校验哈希、别名、真实重试、原生字段守恒、CSV行数与前缀不变；输出最终版报告和差异日志，再更新引用。

## 11. 复现、核验范围与局限

```sh
python3 analysis/token-imputation-audit-20261026/reproduce.py
python3 analysis/token-imputation-audit-20261026/verify-report.py
```

第一条用五月冻结输入和新增 thinking-inputs.zip 离线复现Item 1及Item 4，不访问外仓或活动实验；第二条核对本报告计量摘录、B附录、登记表与原文冻结副本。Item 3 历史发布 SHA-256 清单保留为 A/reporting-release-manifest.json；Item 4 历史清单为 A/thinking-release-manifest.json，Item 5 当前清单为 A/master-release-manifest.json，覆盖包内文件及报告/登记表；未来追加须先对照此发布基线，不能现场重新认可已漂移的中间版。包内有manifest、12,263行call-ledger（五月4,319行、阶段二快照4,498行、benchmark 3,446行）、estimators、calibration、scenarios、summary、README、CHANGELOG，以及inputs.zip、decoded-inputs.json、checks、shared-usage、编排锚点/差额附件（行数源 A/checks.json 的 rows 字段；不含表头）。

Item 1源快照时间（A/manifest.json:2）：**2026-10-26T09:35:00.109476+00:00**；engine=item1-v1。Item 3补充字段采集时刻及原仓文本SHA-256见A/reporting-inputs.json。B只冻结计量字段与哈希，未保存model-benchmark完整输出文本；足以复算字段加总，但不等同重新审计provider回执。

本次直接核验：Item 1 ledger和情景数；登记项原文/行号/编码；model-benchmark逐文件计量字段及缺失字段；direction_a写入逻辑；draft-0316上述原文。二月全树存在性、逐批数量、重复副本和GT执行归因沿用Item 2已核验简报，未重新跑全树调查。更正计划所称21处经逐项展开为**24处**；登记另含相邻旧均值行3处、二月措辞5处、direction_a代码2处，共**34项**（来自登记CSV，不是token数）。

**不能据此得出：** 完整项目总token或可信有限区间、完整端到端架构成本比、缺失调用零消耗、二月命名模型能力优劣、GT输出的原生隐藏推理量，或token更少即研究质量更高。S0是已记录生成计量子集，不是全流程usage完整案例；跨期编排、Kimi跨任务编码与MiniMax情景是可被审稿人挑战的假设。Item 1 checks中旧目标未复现的PARTIAL保留为审计历史，本报告采用重要更正，不伪造旧规格验收通过。
