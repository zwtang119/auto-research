# Adjacent-work Positioning — 决策流水线想法的相邻工作定位

> 本文档为 2026-07-19 评估包组成部分，引用已冻结的开题报告 v1.3.1（`auto-research/docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md`）与项目简报 v1.3（`PROJECT-BRIEF.md`）但不修改它们。本文件对应评估包阶段 1 的三节产出——相邻文献景观的三条切线，用以论证 8 步 Agent 流水线的贡献落点是「应急决策方法论的流程固化 + 步骤级降级协议的显式化」，而非 workflow 架构本身。
>
> 引用材料均沿用侦察交接 A（`prompt-exports/stage1-recon-1.1-workflow-lineage.md`）与侦察交接 B（`prompt-exports/stage1-recon-1.2-1.3-sop-degradation.md`）的核验状态标记。AutoResearch 协议定义引用侦察 A 中已确认路径（`auto-research/docs/autoresearch/orchestrator-prompt.md` + `auto-research/framework/watchdog/README.md`），不在本文件重新发明。

**3 条待复核项**：(1) EvoAgent 标题歧义——arXiv 2406.14228 在搜索引擎返回中同时出现「Self-Evolving Agentic Systems through Multi-Agent Evolution」与「Towards Automatic Multi-Agent Generation via Evolutionary Algorithms」两个标题，arXiv ID 同号，可能是 v1/v2 或搜索引擎合并，需复核 PDF 摘要页；(2) IMO SOPEP/MARPOL 配套决议精确编号（本侦察未命中 MSC.1/Circ.1568 / A.1075(28) 的最新版本号，需下游查 imo.org IMODOCS 复核）；(3) Cooke method + Morgan-Henrion 1990 仅凭知识，未通过本会话联网核验，引用时按 [未核验-需复核] 标注。

**1 条限制声明**：AFlow / ADAS / EvoAgent / Biomni 的 §1.1 对比基于 WebSearch 摘要级证据，未做全文精读（按计划文档风险预案已批准 Biomni 降为摘要级；其余三篇的 §1 Introduction + §5 Related Work 未读），如下游需要全文级精读，应再派 explore 子代理补一次 arXiv 原文核对。

---

## §1.1 LLM agentic workflow 编排谱系（主切线）

LLM agentic workflow 的 2024–2026 文献景观已形成一条清晰的「workflow 进化搜索」谱系。本节选 5 个最近邻做四维对比，目的是确认本想法的「固定 8 步 + 步骤级降级协议」组合点在该谱系中未占位。最近邻是 Co-Scientist（Nature 2026）的 Supervisor 调度层——本项目已存档其 PDF（`sources/Co-Scientist-Accelerating-scientific-discovery-Nature2026-s41586-026-10644-y.pdf`），Supervisor 调度的是 worker 任务队列，不是 SOP 步骤。

AFlow（ICLR 2025 Oral, arXiv:2410.10762）以 Monte Carlo Tree Search 在代码化 workflow 空间中搜索最优 agent DAG；ADAS（ICLR 2025, arXiv:2408.08435）以 Function Search 跨所有代码定义组件搜索 agent 设计（无模板约束）；EvoAgent（arXiv:2406.14228）以 Darwinian GA 进化 agent 群体拓扑与个体能力。这三点共同构成「workflow / agent 进化搜索」红海。Biomni（arXiv:2505.07988, Stanford 2025-05）不在该红海——它强调「整合 105 个科研工具 + 59 个数据库」，固定单 agent 调工具，几乎没有「编排」维度；它与本想法的关系是平行范式而非竞争。

4 维对比的核心是 (c) 编排自由度 与 (d) 内建步骤级降级 两个维度的解耦。Co-Scientist 走「半动态 Supervisor 调度」、AFlow/ADAS/EvoAgent 走「完全动态进化搜索」、Biomni 走「固定单 agent 调工具」——没有任何一个邻居把「固定步骤集」与「显式步骤级降级协议」组合。Co-Scientist 定位正交于本想法：它做「离线策略搜索」（find a hypothesis），Supervisor 的 component-level 重启（Methods line 49「easy restarts in case of any failures」）解决的是「worker 死了怎么办」，不解决「步骤置信度不足时如何传播降级」——这是 step-level 降级协议未占位的核心证据。

侦察交接 A 第 A 节已确认 AutoResearch 协议定义散落路径：`docs/autoresearch/orchestrator-prompt.md`（零交互 / 新鲜会话 / 停滞检测 / 状态外化四件套原文所在）+ `framework/watchdog/README.md`（L0/L1/L2 心跳看门狗三层实现）。本文件直接引用侦察 A 已核验的路径与原文段，不再列出协议原文——避免与已冻结沉淀重复。R6「Zero-Interaction」与外部配套 SKILL 文件侦察未读，列入「待复核项」性质的扩展阅读建议，不在本节引用。

Biomni 与 EvoAgent 各有一处标注修正：原计划文档「Biomni (bioRxiv 2025)」有误，Biomni 实际是 arXiv 2505.07988（2025-05，Stanford Kexin Huang et al.）；EvoAgent 标题存在歧义——arXiv 2406.14228 在搜索引擎返回中同时出现「Self-Evolving」与「Automatic Multi-Agent Generation」两个标题，arXiv ID 同号，可能为 v1/v2 或搜索引擎合并，需复核 PDF 摘要页。

### §1.1 四维对比表

| 邻居 | (a) 进化对象 | (b) 适应度 | (c) 编排自由度 | (d) 内建步骤级降级协议 |
|---|---|---|---|---|
| Co-Scientist Supervisor（Nature 2026）[已核验-已读全文框架] | 决策策略内容（科学假设） | Elo 锦标赛自评 + 湿实验验证 | 半动态（固定 6 specialist + Supervisor 调度） | ❌ 无 per-step 置信度 |
| AFlow（ICLR 2025 Oral, arXiv:2410.10762）[摘要级] | workflow 架构（agent DAG） | 任务分数（benchmark） | 完全动态（MCTS 在代码空间搜索） | ❌ 无显式降级协议 |
| ADAS（ICLR 2025, arXiv:2408.08435）[摘要级] | agent 设计（含 prompt/tool/control flow 的代码） | 任务分数（24/25 SOTA） | 完全动态（Function Search 无模板约束） | ❌ 无显式降级协议 |
| EvoAgent（arXiv:2406.14228）[摘要级-标题歧义] | agent 群体（个体能力 + 群体拓扑双层进化） | NLP / MMMU benchmark | 完全动态（Darwinian GA 改 agent 拓扑） | ❌ 无显式降级协议 |
| Biomni（arXiv:2505.07988, 2025-05）[摘要级] | 工具集 / 代码环境 | 生物医学多任务 benchmark | 固定（单 agent 调工具） | ❌ 无显式降级协议 |
| **本想法 8 步流水线（本评估包）** | **步骤内部处理逻辑（步骤契约）** | **6 维校准指标 + 校验臂物理闸门（沿用开题 v1.3.1）** | **固定 8 步（Intake→Synthesis）** | **✅ confidence_grade 4 档 + downgrade_reasons + 降级链路传播** |

### §1.1 贡献落点陈述

本想法与 5 个最近邻均不重合：它没有走 workflow / agent 进化搜索红海（区别于 AFlow / ADAS / EvoAgent 的完全动态搜索），也没有把自己装进 Supervisor 调度框架（区别于 Co-Scientist 的半动态 Supervisor），也没有走单 agent 调工具的固定范式（区别于 Biomni）。它在「编排自由度」维度选最固定的端（8 步固定），但通过「内建步骤级降级协议」这一维度补回自适应能力——「固定步骤集 + 显式降级协议」这一组合在 5 邻居中均未占位。贡献落点是「把步骤级降级协议显式化为 Agent 契约」（沿用 ROC 2002 + Avizienis 2004 的可信赖计算分类、§1.3 详述），不是发明 workflow 架构。（约 180 字）

---

## §1.2 应急决策流程化文献（次切线）

应急决策领域本身已是流程化的成熟工程基线——把应急决策拆为 SOP + 角色 + 通讯协议这套范式至少在 NIST（2010）、FEMA（2021 v3.0）、IMO（SOLAS / MARPOL / SOPEP）、FAA（Order 7110.65 Ch.10）、NRC（NUREG-0654 + NUREG/CR-7002）等机构有 30 年以上的工程沉淀。本节选 5 篇做 2 维区分——「人类组织侧流程化」（SOP + 角色 + 通讯协议的文档体系）vs「机器侧可降级流程化」（步骤级 schema + confidence 标量 + 降级链路），用以论证流程化本身是工程基线、本贡献是把 SOP 范式与 LLM 步骤级降级协议挂钩。

维度 1 维度上，5 文献均给完整的 SOP + 角色 + 通讯协议：NIST IR 7601（2010-08）给 Emergency Response Officials（ERO）角色清单（指挥 / 通讯 / 协调）+ 决策权责图 + 跨机构通讯协议；FEMA CPG 101 v3.0（2021-09）给 14 个 ICS 标准化职能角色 + ICS-205 通讯计划表单 + 5 步规划循环；NUREG-0654 / FEMA-REP-1（1980，里程碑版本）给核电站应急四档触发（General Emergency / Site Area Emergency / Alert / Notification of Unusual Event）+ 三段权责移交。NUREG/CR-7002（2007）的工程意义特殊——它把「是否需撤离」的人类决策转换为距离门槛（基于烟羽弥散模型 + 应急疏散 ETE 排队模型），输出 T50/T90/T100 三档疏散完成时间，是「机器友好型标量」，开题 v1.3.1 §5.3 已选定它作为校验臂副臂，本想法步骤 6（Validation）直接复用其量化模型作为阈值。

维度 2 维度上，5 文献均不涉及机器侧 step-level degradation + confidence grading。FAA Order 7110.65 Ch.10 给管制员应急授权「偏离既定程序」（emergency situations require immediate action）——这是「人类决策降级」标准范式，把「程序完整度」作为可牺牲的变量换取响应速度，但偏离后由管制员主观责任承担，没有 confidence 标量契约。Phillips-Goodrich-Wenger 2009（*Disasters* 33(1)）描述了「决策权沿指挥链上移」的组织现象（operational → tactical → strategic → policy），但只描述、不规范——它没有给出「漂移后必须输出什么标量」的工程契约。IMO SOLAS / MARPOL / SOPEP 给「船舶遇险决策书」的标准化字段（事故位置、气象、货物、伤员等）——这是「结构化记录」的早期人类侧先例 [未核验-需复核，具体决议编号需下游查 imo.org IMODOCS]，但驱动是法律合规，不是诚实呈现无知。

本想法 8 步流水线与上述文献的耦合方式：维度 1「流程化 SOP + 角色 + 通讯协议」沿用并把角色映射为 Agent 名义职能（Intake / Decomposition / Retrieval / Generation / Simulation / Validation / Judge / Synthesis）；维度 2「机器侧 step-level degradation + confidence grading」是本想法新增——`confidence_grade ∈ {HIGH, MEDIUM, LOW, INSUFFICIENT}` + 降级链路传播（N=INSUFFICIENT → N+1 上限 ≤ MEDIUM）是上述文献都没有的契约层。FAA 的「偏离程序」目标函数是抢时间（响应速度优先），Phillips-Goodrich-Wenger 2009 是组织现象的事后归纳，NRC 系列给量化标量但无契约化降级链路——三者的目标函数与本想法的「诚实呈现无知」都不重合。

本节不重新发明流程化——应急决策的流程化是成熟工程基线。本想法的贡献是把「SOP 范式」与「LLM 步骤级降级协议」挂钩：SOP 给步骤集与角色（沿用 NIST / ICS / IMO），降级协议给每步的 confidence 标量与传播规则——开题 v1.3.1 §4.4 H4 校准四件套是这一协议在 Judge 步的具体落地。

### §1.2 二维区分表

| 文献 | 维度 1：人类组织侧流程化（SOP + 角色 + 通讯） | 维度 2：机器侧 step-level degradation + confidence grading |
|---|---|---|
| NIST IR 7601（2010-08）ERO 框架 [已核验] | ✅ ERO 角色清单 + 决策权责图 + 跨机构通讯 | ❌ 无 confidence 标量契约 |
| FEMA CPG 101 v3.0（2021-09）+ ICS-300/400 [已核验] | ✅ 14 个 ICS 角色 + ICS-205 通讯表单 + 5 步规划循环 | ❌ 输出物是 Situation Report（叙事），不是结构化 JSON |
| FAA Order 7110.65 Ch.10（持续修订 2026）[已核验] | ✅ 应急授权偏离程序 + 通讯短句模板 | ❌ 偏离由人类主观责任承担，无 confidence 标量 |
| IMO SOLAS / MARPOL / SOPEP [未核验-需复核：具体决议编号] | ✅ 船长应急 SOP + 黄金 1 小时上报 + 决策书结构化 | ❌ 决策书是人类事后填表，非机器事前契约 |
| NUREG-0654/FEMA-REP-1（1980）+ NUREG/CR-7002（2007）[已核验] | ✅ 四档触发 + 三段权责移交 + ETE 距离门槛 | ❌ 触发是外部风险等级驱动，非 Agent 自评 confidence_grade |
| **本想法 8 步流水线（本评估包）** | **✅ Agent 名义职能映射 ICS 角色 + 步骤间 I/O schema 落盘** | **✅ confidence_grade 4 档 + downgrade_reasons + 降级链路传播 + 已知-推断-无知清单** |

### §1.2 贡献落点陈述

应急决策的「流程化」是工程基线（NIST / ICS / IMO / FAA / NRC 30 年沉淀），本想法不发明流程化。本贡献是把「SOP 范式」与「LLM 步骤级降级协议」挂钩——把 SOP 给出的步骤集与角色映射为 Agent 名义职能（维度 1 沿用），并为每步契约化输出 `confidence_grade` 与 `downgrade_reasons`，让降级沿步骤链传播（维度 2 新增）。「步骤级降级 + confidence 标量」这一组合在 5 个流程化文献中均未出现——这是「流程化 + LLM 步骤级降级协议」的耦合点，也是本想法与 Q1 §1.3 已锁定的「novelty 收窄四点」一致的落点。（约 180 字）

机器可读行动锚（decision_actions）的新兴来源——IFRC GO field-report `actions_taken`（`goadmin.ifrc.org/api/v2/`，免 key, 5,107 条）、NWS `api.weather.gov` CAP 预警（含 Evacuation Immediate, 免 key）、NTSB CAROL（CSV/JSON）、CSB 全本 PDF（公有领域）、mem.gov.cn 国家防总响应通告与调查报告栏目（境内直连, 2018 断档为硬约束）、JMA Digital Typhoon XML（CC BY 4.0）——为机器侧流程化补齐了「决策侧决定时点」机器可读来源,与本想法 8 步流水线步骤 3 Retrieval 的 `decision_actions[]` 输出契约对齐（见 `pipeline-design-spec-2026-07-19.md` §2.1 步骤 3, `origin` 枚举扩 `ifrc_go_field_report` / `nws_cap_alert` / `ntsb_carol` / `csb_final_report` 等）；ReliefWeb API 自 2025-11 起需预审批 appname,已不再作为默认落点。

---

## §1.3 降级协议先验（学科祖先核查）

本节核对 3 条降级协议先验的学科归属与本想法的耦合方式——论证本流水线的 4 档 confidence_grade + 降级链路传播「不是发明降级协议」，而是把三个学科祖先的成熟机制耦合进「8 步显式协议」这一具体载体。

**先验 1：Graceful / Partial Degradation**（分布式系统 / 可信赖计算经典）。代表文献为 Patterson, Brown, Wylie, Culler et al. (2002)「Recovery-Oriented Computing (ROC)」UC Berkeley / Stanford UCB/CSD-02-1175 [已核验]，与 Avizienis, Laprie, Randell, Landwehr (2004)「Basic Concepts and Taxonomy of Dependable and Secure Computing」IEEE TDSC 1(1):11-33 [已核验]。核心机制是「服务不硬失败而是按层级降级」——Avizienis taxonomy 给出 graceful degradation 的形式化定义（在故障发生时系统按预先指定的层级逐级退化，每级退化有明确的属性降级幅度与可接受阈值）。ROC 项目的设计哲学是「以恢复替换容错」（recovery over fault tolerance）。本流水线的 `confidence_grade ∈ {HIGH, MEDIUM, LOW, INSUFFICIENT}` 4 档离散标量是 ROC 的「服务是否可用」二元判定改写为离散分级；降级链路传播（N=INSUFFICIENT → N+1 上限 ≤ MEDIUM）是 Avizienis taxonomy 在 Agent 步骤级的工程化落地。本流水线不复制 ROC 的「事后恢复」机制——ROC 是事后恢复，本流水线是事前显式标度。

**先验 2：Confidence Calibration in Decision Support**（决策科学 / 认知工程 / 风险分析经典）。代表文献为 Lichtenstein, Fischhoff, Phillips (1982)「Calibration of Probabilities: The State of the Art to 1980」*JEP:HPP* 8(4):545-566 [已核验]。辅助文献为 Cooke method（结构化专家判断 elicitation, Roger Cooke, Resource Center on Structured Expert Judgment）与 Morgan, Henrion (1990)「Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis」[未核验-需复核]。核心机制是「标定自信度 vs 实际正确率曲线」——所谓 70% 置信在长期频率上是否真的是 70%。开题 v1.3.1 §4.4 H4 校准四件套（Gold-anchor pass / Youden J / error rate / Kendall's τ）是这套经典协议在 LLM 决策臂上的现代延伸；本流水线步骤 7（Judge）的 `calibration_check` 四件套直接引用 H4。Morgan-Henrion 的「data → model → expert 三档分类」为「已知-推断-无知」三档判定提供对照——HIGH ≈ data-confirmed / MEDIUM ≈ model-derived / LOW ≈ expert-only / INSUFFICIENT ≈ no source。

**先验 3：Known Unknowns in Intelligence Analysis**（情报分析 / 结构化分析技术经典）。代表文献为 Heuer, R. J. Jr. (1999)「Psychology of Intelligence Analysis」CIA Center for the Study of Intelligence [已核验]，含核心方法 ACH（Analysis of Competing Hypotheses）。辅助文献为 Rumsfeld 2002-02-12 DoD News Briefing（known knowns / known unknowns / unknown unknowns 三分类）[已核验 defense.gov transcript + wired.com + c-span.org 三源]。核心机制是「把无知显式分类 + 反向推断（从证据到假设的权重）以对抗 confirmation bias」。本流水线步骤 2（Decomposition）的 `explicit_known_unknowns` 4 字段（claim / why_unknown / what_would_resolve / confidence_default）严格对齐 ACH 诊断性证据原则；步骤 8（Synthesis）的「已知-推断-无知清单」段落结构上沿用 Rumsfeld 三分类。**本流水线不承诺识别 unknown unknowns**——这是与 CIA tradecraft 的明确脱离点（任务边界自我约束）。

三条先验的耦合方式不同：先验 1 给「降级标量的离散分级结构」、先验 2 给「calibration 的外部频率证据」、先验 3 给「无知分类的语义结构」。三者在各自领域独立应用且沉淀 20–40 年——把它们组合成「流水线步骤级降级协议」这一具体载体的工作未见文献占位。侦察交接 B 的总映射表（8 步 × 3 先验 = 24 个耦合点）已逐项列出 24 个步骤级耦合方式，本节不重复列出，引用侦察 B 的总映射表作为权威源；本节论证的是「三条先验各有学科祖先、耦合点未占位」这一判断——这与 Q1 §1.3 已锁定的 novelty 收窄四点一致，也与 idea §5 第 4 条「贡献点切割在『应急决策方法论的流程固化 + 降级协议』而非架构本身」一致。

### §1.3 先验四维（学科归属 × 与本想法耦合方式）

| 先验 | (a) 学科归属 | (b) 主代表文献（核验状态） | (c) 核心机制 | (d) 与 8 步流水线耦合方式 |
|---|---|---|---|---|
| **先验 1**：Graceful / Partial Degradation | 分布式系统 / 可信赖计算 | Patterson et al. ROC 2002 UCB/CSD-02-1175 [已核验]；Avizienis et al. 2004 IEEE TDSC [已核验] | 服务不硬失败，按层级降级；每级退化有明确属性降级幅度 | `confidence_grade` 4 档离散标量；`downgrade_reasons`；N=INSUFFICIENT → N+1 ≤ MEDIUM 传播 |
| **先验 2**：Confidence Calibration in Decision Support | 决策科学 / 认知工程 / 风险分析 | Lichtenstein-Fischhoff-Phillips 1982 JEP:HPP [已核验]；Cooke method + Morgan-Henrion 1990 [未核验-需复核] | 标定自信度 vs 实际正确率曲线；data / model / expert 三档分类 | 步骤 7 `calibration_check` 四件套（直接引用 H4）；步骤 2 `explicit_known_unknowns[].confidence_default` 4 档；步骤 8 已知-推断-无知清单三档 |
| **先验 3**：Known Unknowns in Intelligence Analysis | 情报分析 / 结构化分析技术 | Heuer 1999 CIA CSI（含 ACH）[已核验]；Rumsfeld 2002-02-12 DoD Briefing [已核验] | 无知三分类 + 反向推断对抗 confirmation bias | 步骤 2 `explicit_known_unknowns` 4 字段对齐 ACH 诊断性证据；步骤 4 候选对应可证伪假设；步骤 8 沿用 Rumsfeld 三分类 |
| **本想法 8 步流水线（本评估包）** | — | — | — | **三先验耦合进 8 步显式协议：耦合点 8×3 = 24 个（侦察交接 B 总映射表权威源），未在文献中占位** |

### §1.3 贡献落点陈述

三条先验各有成熟学科祖先：先验 1（ROC + Avizienis）在分布式系统沉淀 20 余年，先验 2（Lichtenstein-Fischhoff-Phillips + H4）在决策科学沉淀 40 余年，先验 3（Heuer ACH + Rumsfeld）在情报分析沉淀 25 年。本贡献不是发明降级协议，也不是发明 calibration 或 known-unknowns——而是在「8 步 Agent 流水线」这一具体载体上把三条先验耦合为「步骤级降级 + 置信度标量 + 无知清单」的显式契约。耦合点共 8 步骤 × 3 先验 = 24 个，侦察交接 B 的总映射表已逐项列出；本节论证的是「三先验耦合进 8 步显式协议」这一点在文献中未占位——这是本想法与 Q1 §1.3 已锁定的 novelty 收窄四点一致的另一面。（约 180 字）

---

## 修订记录（附录 A）

- v1.0 / 2026-07-19 / pair 主笔生成
- 输入：侦察交接 A（`prompt-exports/stage1-recon-1.1-workflow-lineage.md`）+ 侦察交接 B（`prompt-exports/stage1-recon-1.2-1.3-sop-degradation.md`）+ `q1-novelty-and-theory.md` §1.3 / §3 + `idea-decision-pipeline-2026-07-19.md` §4 / §5 + 计划文档阶段 1
- 待复核：3 项（EvoAgent 标题歧义 / IMO 决议编号 / Cooke method + Morgan-Henrion 1990 现行版本号）
- 限制声明：AFlow / ADAS / EvoAgent / Biomni 4 篇为摘要级证据（计划文档已批准 Biomni 降为摘要级；其余 3 篇的 §1 + §5 未全文精读）
- 评审状态：未评审（阶段 4 红队评审的输入材料）

- v1.1 / 2026-07-19 / pair 主笔最小补丁（修订简报 Item 5）
- 修订依据：`revision-brief-2026-07-19.md` F2（决策行动锚源）。
- 修订范围（仅 1 处 + 本附录追加）：
  - §1.2 末尾增补一段「机器可读行动锚新兴来源」及与 8 步流水线 `decision_actions` 对齐声明（IFRC GO / NWS CAP / NTSB / CSB / mem.gov.cn / JMA Digital Typhoon;ReliefWeb appname 硬约束声明）。
- 未改动：§1 preamble / §1.1 全部 / §1.3 全部 / §1.2 二维区分表与贡献落点陈述 / 3 项待复核项 / 1 项限制声明；v1.0 输入与限制声明保持；保持字数预算与既有结论不变。
- 评审状态：与红队评审范围并列输入,未单独触发新一轮评审。