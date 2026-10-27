# 调查：三组数据的非时间顺序解读框架

日期：2026-10-27；协调与直接复核：OpenCode gpt-6.1-sol。
状态：直接证据复核及解释综合完成；Deep Investigation 工具链未完整完成（pair admission 被阻塞）。

## Summary

**推荐：设计与测量边界 → 同期八臂成分对比 → 有／无DNA两组两结构并列检视 → 综合共同现象与适用边界。** 用批次表示是 **1025 →〔1023 ∥ 五月〕**，不是1025→1023→五月的证据强弱排行榜。

排序依据是“能区分哪些问题”，不是时间、分差或结果是否正向。八臂先约束归因词汇；两结构数据提供各自条件下重复数更多的整体处理包比较。论文也可先展示整体差异，但不得让展示顺序替代识别逻辑。

## Symptoms

- 按开展顺序写成“发现→验证→机制拆解”，容易把时间先后误当证据关系。
- 三组覆盖不同，不能强行分配同一问题；分别看待不等于统计独立，更不等于三次独立机制复现。

## Background / Prior Research

无需外部检索或git考古。沿用冻结数据与既有来源复核，不重跑实验，不新增评分、bootstrap、合并检验或等价检验。

路径缩写（下文引用为完整前缀加后缀及行号）：

| 缩写 | 仓库相对路径前缀 |
|---|---|
| `I/` | `analysis/tsinghua-1025-vs-may-20261027/` |
| `D/` | `analysis/tsinghua-baseline-audit-20261022/dna-final-20261027/` |
| `F/` | `analysis/tsinghua-factorial-ablation-20261025/` |

**Green Source**：设计、实际请求、文件身份与直接算术核验。**Red Source**：模型生成、评分与全部派生均值/差值，不是现实政策效果或人工真值。下列数字统一继承Red Source：五月冻结 `1fab155a7ec77b275e9340263ea659c684a4b6ef`；1023 snapshot `ff00a6f74b8a0310a7ca2cc29a578b8adc038c6d3a6ffe903c42ac1bdbaea754`；1025补充修订payload `b3ed4dda001f6093502b6236cf4cd80178be294335c3e4d52a449b6a087d0f9e`。

## Investigator Findings

**Pair未能启动，本节没有pair发现。** 两次启动均在provider前因 `authority_revision_conflict` 拒绝，未获得session ID，无在途代理。不能以父分析或Oracle输出冒充pair独立调查。父直接证据与综合见下文。

## Investigation Log

### Phase 1 — 问题与版本

已读项目约定、入口及前轮调查，创建本报告。1023用两例MiniMax YAML授权恢复，原协议并列保留；1025用13重评＋1格式修复补充修订，原available-case另留，不冒称原协议完整结果。版本依据：`D/reports/summary-01/summary.md:11`、`:116-129`；`docs/investigations/tsinghua-1025-vs-may-2026-10-27.md:44`。

### Phase 2–4 — 工具限制与解释审查

- context_builder已按本题与绝对报告路径调用，但返回另一“清洁交付计划”旧prompt/selection及无关回答，不采用，不执行其指令。
- Pair两次启动均为provider前workspace持久化冲突；第二次发生在selection增量变更尝试后，冲突未解除，不再重复启动。
- Selection仅add本题报告、旧调查、汇总和代码切片，返回64文件但内容pending/0 tokens；未clear/set，不能声称文件已传入Oracle。
- Oracle仅审查父直接核验的自包含数字和协议摘要，明确不得声称读过pending文件。导出 `prompt-exports/oracle-chat-2026-10-27-174835-new-chat-5164bf-0306.md`。主lane及另两lane有回答，一lane provider失败；不用Oracle提供新事实。
- 采纳：八臂优先约束归因、两结构组同层、分析与呈现顺序分开。
- 不采纳：①“两结构先行必然择优”过强，整体配置问题可现象先行；②两组各自组内对比不是跨期差，跨期限制主要针对两批之间相减；③五月不均衡的是A评委构成，不是样本格（每格35）；④不能断言独立新采样不存在，只能不冒称独立机制复现/无偏独立噪声。以上纠正依据下述直接数据及代码，而非Oracle多数意见。

### Phase 5 — 父直接核验（Green Source）

本轮独立内联Python只读计算，不导入实验工程，不写分析包：

1. 从 `D/statistics/inputs-001/authorized_yaml_recovery/canonical.json:1` 的1260行evaluations重算两期各两条件A/B及对角差。A=SO+TO；每个B评委有效维均值按原loader取3位，再双评均值取3位。每条件315；汇总口径见 `D/reports/summary-01/summary.md:26-34`。
2. 从 `F/supplementary-scoring-20261027/offline-statistics/combined-dataset.json:1` 的360行analysis_view复算八臂均值、四MR差和四DNA差，每臂45。本轮复核冻结采用值与聚合算术，不冒称再次从1080原评分及sidecar重建；原评分逐对象复算见前轮调查F0/F7。
3. 沿 `I/sr-request-pairs.csv:2-91` 逐对重新打开prepared/complete实际事件，90/90 body与route相等、90/90输出不同，不是只复述CSV布尔值。
4. 从 `D/statistics/history-001/period-input.json:1` 的original_evaluations直接计数：五月SASR A全315 coding，MAMR为170标准＋145 coding。
5. 直接读代码：`F/scripts/design.py:102-127`、`F/scripts/generate_factorial.py:93-101`、`:124-135`、`F/scripts/score_factorial.py:33-45`，确认企业名保留、全文评分、信息反馈与措辞绑定。
6. 计算前后输入SHA一致：canonical `bde62e0855c9f60436cd44ba5148c80dd2a4c4d0728f0cd14fc3705ea67a28ad`；combined-dataset `9709e59bb1a7f85c7d3439fdbd60b0fd020b5599a130ef410de48cc2599c871c`。本轮没有新增区间计算。

## Root Cause / 解释风险

根本风险是把不同证据能力写成单一递进故事，而非存在一个必须遵循的时间顺序。

| 中性名称 | 数据定位 | 可以回答 | 不能单独回答 |
|---|---|---|---|
| 同期八臂结构组（1025） | SA/MA×SR/MR×DNA/NoDNA；每臂45、每格5 | 其他设计水平固定时的实现处理包差异、条件依赖 | 纯agent数、纯反思、预算匹配效率、全任务普遍规律 |
| 无DNA两结构组（1023） | SASR/MAMR各315、每格35 | 无显式五属性时，两种整体配置评分差 | SA/MA与SR/MR分别贡献；与五月相减的DNA因果 |
| 有DNA两结构组（五月） | SASR/MAMR各315、每格35 | 另一协议环境中有DNA的整体配置评分差 | 组件贡献；忽略A评委构成不均后的纯生成效应 |

分母与共享批次：`D/reports/summary-01/summary.md:26-34`；八臂与指标边界：`docs/investigations/tsinghua-1025-vs-may-2026-10-27.md:73-106`。MAMR三企业共享批次，315企业输出不等于315独立批次；更多重复不增加政策/企业覆盖。

### 第一层：八臂先约束解释，不给八个均值排总榜

1. **先核查处理实际含义**：SR下SA/MA同body/route，不能当纯agent数操纵。NoDNA下A差−0.7111不能归因提示差，也不能确认独立无偏噪声。请求证据：`I/check_protocol.py:30-55`及本轮90对事件复核。
2. **固定SA/MA与DNA看MR−SR**：按SA/NoDNA、SA/DNA、MA/NoDNA、MA/DNA，A差+2.1778/+2.0667/+3.3333/+2.9556，B差+0.8417/+0.8622/+0.7978/+0.9244。总体方向最一致，但不是四次独立复现，不代表每模型每格皆正；是MR处理包结果，不是纯反思机制。
3. **MR中看MA相对SA，拆开指标/维度/模型**：DNA条件A +1.1333、B +0.0333；B近零是竞争意识等维度和模型间的权衡，不是证明内容没变化。维度与分层依据：`docs/investigations/tsinghua-1025-vs-may-2026-10-27.md:117-135`。
4. **固定结构看DNA−NoDNA**：SASR/SAMR/MASR/MAMR的A差−0.4000/−0.5111/+0.5556/+0.1778，B差−0.0422/−0.0217/−0.0444/+0.0822。不支持跨结构一致正增益，不等于证明无效或等价。

协议边界须前置：MR评分读全部轮次，绑定更多预算、表达机会与措辞；SAMR回灌自身上轮全文，MAMR使用跨企业前800字符生成的共同摘要且措辞不同，不能称纯agent数。NoDNA保留企业名，仅删五属性，不等于无企业知识。代码引用见Phase 5。八臂能拆分**实现处理包**，仍不是纯机制识别，且每格仅5重复并有补充修订。

### 第二层：两组两结构并列检视，不硬排先后

Red Source；本轮直接复核点估计，不新增合并检验：

| 各自条件环境 | MAMR−SASR：A | MAMR−SASR：B |
|---|---:|---:|
| 无DNA两结构（1023） | +2.7111 | +0.7644 |
| 有DNA两结构（五月） | +2.3206 | +0.6110 |

均值定位：`D/reports/summary-01/summary.md:15-24`；本轮从canonical原评分算，不用汇总作计算输入。

整体配置的正差不只出现在八臂的5重复格中；但不能额外证明八臂MR主效应、MA机制或DNA差异独立复现。五月A评委构成不均尤其限制纯生成解释。两组没有统一高低排名；若版面必须线性，可先无DNA后有DNA，作为从较少显式属性信息到增加属性信息的说明顺序，不是发现/验证，也不是无知识/有知识。

### 第三层：综合共同现象与适用边界

- 各自冻结测量下整体MAMR相对SASR均值较高；八臂中MR处理包是总体方向最一致的比较族。
- MA具有条件、维度、模型权衡；DNA既非已证明的普遍增益，也非已证明无用。
- 不把1023−五月当DNA因果，不按时间讲能力进步，不混并显著性，不称三次独立机制复现。
- 跨期服务/评委变化限制归因，不等于已证明它们造成全部分差；组间不可干净相减也不意味着各组内部没有信息。

## Recommendations

### 实际解读

**设计/测量口径 → 八臂内部对比 → 两结构组并列 → 共同结论与边界。** 依据可区分性定序，即使分差翻号也不改变。

### 论文或汇报

1. 问题—证据地图：三种设计分别回答什么。
2. 同期成分比较：MR、MA、DNA及异质性，附SR实现核查。
3. 整体配置方向一致性：有／无DNA两结构并列表，不命名发现集/验证集。
4. 未识别机制与适用边界：全文、预算、共享/压缩/措辞、服务与测量、固定任务覆盖。

可用备选：若研究问题本来是“复杂配置是否整体优于简化配置”，可先展示三组各自整体差异，再八臂拆分。须开篇明确整体处理包而非agent/DNA因果，完整报告对比族，不后见性虚构预注册。现象先行本身不是择优；错误是先定机制再挑证据。

## Preventive Measures

- 以“同期结构组／有DNA两结构组／无DNA两结构组”作解释标题，日期仅作来源索引。
- 分开报告重复数、共享批次、任务覆盖与外推范围；保留版本身份、原协议对照及负向/混合结果。
- 调换呈现顺序时，结论成立条件与强度必须不变；这是叙事审查，不是新统计检验。
- 本次仅新增本报告及工具自动本地导出，不commit/push；不碰封存仓库、evidence、实验产物与已有legacy/papers改动。
