# DMO 不确定性决策文献精读与 CDS 贡献评估

> 日期：2026-07-22
> 执行者：Kimi（主会话 + explore 子代理 agent-0 / agent-1）
> 触发：用户要求解读两篇 DMO 论文中"信息不全下的决策"论述，并评估对 CDS 系列研究（4polymarket / 4Worldcup / policysim）的贡献与重要性
> 阅读材料：`analysis/dmo-uncertainty-reading/`（含两篇 PDF 副本与全文提取文本，见该目录 CHANGELOG.md）
> 文献盘点：`analysis/downloads-pdf-scan/REPORT.md`（Downloads 109 个 PDF 扫描）

---

## 1. 阅读对象

| 文献 | 出处 | 体量 | 方法 |
|---|---|---|---|
| Popa, Stone 等（SEA-27 团队）《Distributed Maritime Operations and Unmanned Systems Tactical Employment》 | NPS 系统工程顶点报告，2018-06 | 199 页 | ExtendSim 离散事件仿真 + 实验设计（DOE）+ 回归/分割树 |
| Elliott《The Recognized Information Picture for Distributed Maritime Operations》 | NPS 硕士论文，2025-03 | 145 页 | 研究综合（research synthesis），约 200 个官方权威来源 |

两篇同为 NPS 的 DMO 研究谱系，间隔七年，视角互补：前者研究**如何制造敌方的信息不全**（进攻面），后者研究**如何消解己方的信息不全**（防御面）。

## 2. SEA-27（2018）精读要点

### 2.1 杀伤链 = 信息门控的序贯决策

传统 F2T2EA 杀伤链被压缩为 FTE（Find-Target-Engage）三阶段（pp. 31–34）。每个阶段是信息阈值门：未"找到"则无权"瞄准"，无火控解则不能"交战"。论文总纲："typically only one phase in the kill chain must be disrupted"（p. 34）——防御方不需要信息优势，只需在一个环节让对手信息不达标。

### 2.2 不确定性的显式量化：AOU

**Area of Uncertainty**（pp. 50–51, 70–71）：以蓝方平台实际位置为圆心、随其航速与未被发现时长扩张的不确定区域。敌方每次扫描失败 AOU 增大；敌方 ISR 资产压缩 AOU。蓝方四类战术（EMCON、干扰、诱饵、蜂群）的全部目标是最大化 AOU。不确定性由此成为**可计算、可优化、可作为实验因变量**的量。

### 2.3 先验信息下的目标分配：欺骗攻击决策先验

附录 F（pp. 141–142）：敌方开战前用"combat power 得分 + level of reach 得分"对蓝方平台加权排序（CVN 8.95 分居首），归一化为任务分配概率（CVN 45%…）。欺骗蜂群直接攻击该先验：蜂群 100% 模仿航母时，分配概率归一化重分配为 CVN 31% / 蜂群 31%（表 9–11，pp. 72–73）。**"敌方误判"被形式化为任务分配概率的系统性稀释**，且收益外溢——导弹载舰被瞄准几率同样下降（p. 119）。

### 2.4 微观信息获取模型与完美信息豁免

探测被建模为 single-look 概率的重复 Bernoulli 扫描；55–75 个 AIS 中立杂波须逐一分类，**分类（classification）是信息不全下决策的时间瓶颈**（pp. 63–66）。干扰以 0–1 降级因子乘在传感器性能上。作者诚实标注两处对蓝方的完美信息授予：干扰假设精确已知敌方频率（p. 76）；蓝方必能正确识别来袭导弹制导类型（p. 74）。另有两项信息维度局限：敌方平台互不共享信息、敌方不打机会目标（均偏袒蓝方，p. 77）。

### 2.5 价值主张

"allowing time for decision makers"（p. 121）：制造敌方信息不全的本质是**制造敌方决策延迟，延迟即先手窗口**。论文同时留下诚实开放问题：find 阶段拖延也让敌方拉近距离，不确定性窗口是双刃剑（p. 52）。

## 3. Elliott（2025）精读要点

### 3.1 问题：条令空白 × 分布式决策需求

CWC 体系下三张战术图各有归属（pp. 3, 47）：ADC→RAP（空情）、SCC→RMP（海情）、IWC→RIP（信息）。RAP/RMP 边界清晰；**RIP 从未在条令中定义**（p. 86）。而 DMO 的分布式机动要求每艘单舰在任务式指挥下独立管理完整战术图（结论 p. 87）——条令空白直接转化为单舰决策者的不确定性。

### 3.2 RIP 的定义突破：没有 tracks 的图景

RAP/RMP 由 tracks（可瞄准的航迹）构成；**RIP 的大部分内容没有航迹、无法被传统方式瞄准**（pp. 85–86）：① 无形物——敌我态势与意图、能力评估、行为模式与 TTP、信息影响/叙事、决策本身；② 非可触物理信息要素——热与信号辐射、电子信号、比特流、数据链、C2、AI/ML。组织框架 = IWC 三条工作线（Table 9，p. 55）：可靠 C2（AC2）、战场感知（BA）、一体化火力（IF）。价值定位：**RIP 给 DMO 带来"left of kill chain"能力**（p. 86）——I&W 上报以聚焦传感器、机动兵力。

### 3.3 信息不全的制度性来源

"在 A2/AD 环境中，战术 COP 可能退化为仅靠建制内（organic）传感器；全能力 COP 需建制内＋非建制（战区/区域/战略级）ISR 共同喂入"（p. 45）。**信息不全的程度随对抗强度变化**——强敌对抗下图景天然残缺。密级制度（need-to-know、分隔化）进一步制度化地切碎知识（pp. 9, 21）。

### 3.4 决策者信息需求的形式化：CCIR 分解链

BA 节（p. 76）：**CCIR（指挥员关键信息需求）＝ PIR（优先情报需求）＋ FFIR（己方信息需求）→ EEI（决策所需关键信息要素）→ 未解问题以 RFI 上报**。把"我不知道什么"显性化，并据此分配稀缺情报资源。配套 JIPOE 流程：界定环境 → 评估对手 → 判定敌可能行动方案（COA）。

### 3.5 战场透明化改变不确定性的性质

商业空间 ISR（SAR、RF 地理定位、EOCL 光电合同）使高端侦察能力商品化（pp. 65–67）："海军计划必须假定对手拥有至少与美国相当的国家能力，并能获取同样的商业能力"（p. 67）。不确定性从"我们不知道"转向**双方互见、比拼决策速度与质量**（decision advantage）。

### 3.6 信息不全的作战化分级：TACSIT 三级

按"对手对我的确定性"分级（pp. 81–82）：TACSIT 3（己方未知未定位 → C-ISRT 为主）→ TACSIT 2（被大致定位 → C-ISRT＋CTTG）→ TACSIT 1（被瞄准可交战 → CTTG＋ASMD 动能/非动能一体化）。**每一级不确定性对应一张行动菜单**。配套：SIGCON 信号特征五分类（p. 78）、MILDEC 的 See–Think–Do 认知操纵链（p. 81）。

### 3.7 批判性评价

贡献：首次在非密层级把 RIP 系统化为概念（三图分工、IWC 三 LOE、intangibles 定义、left-of-kill-chain 定位）。局限：① "定义"实为功能清单，无可检验的完整度度量；② 无决策理论——反复说 RIP"improves decision-making"，但"RIP 不全时人如何决策"是黑箱；③ 零实证（无演习数据/案例/访谈）；④ 细节粗糙（p. 54 将 Table 9 误引为 Table 8）。

## 4. 两篇对照

| | SEA-27（2018） | Elliott（2025） |
|---|---|---|
| 视角 | 制造敌方信息不全 | 消解己方信息不全 |
| 方法 | 仿真 + DOE | 200 源研究综合 |
| 核心概念 | AOU、time-to-find/target、任务分配概率 | RIP、CCIR→EEI、TACSIT、left of kill chain |
| 不确定性来源 | 杂波/蜂群/干扰/EMCON（可工程化） | A2/AD 退化、信息孤岛、条令空白（制度性） |
| 决策主体 | 概率过程（无学习扫描机器） | 人（单舰 TAO/OOD 在任务式指挥下做时敏决策） |
| 自述局限 | 完美信息授予蓝方 | 纯描述、无模型无验证 |

## 5. Downloads 文献盘点结论（详 `analysis/downloads-pdf-scan/REPORT.md`）

109 个顶层 PDF 中：直接相关仅 Elliott 一篇；间接相关 8 篇（NBR《Mapping China's Strategic Space》、ToT/GoT、Self-Play 综述、三篇群体智能、SEA-27 本体）。其余为自有 CDS 材料 16 个、CDS 推演输出 16 个、课程教材、商业文档等。**判断：本地藏书中不确定性决策的理论层（POMDP / RDM / info-gap / DMDU）为空，现有均为应用层与 LLM 推理层。**

---

## 6. 对 CDS 系列研究的贡献映射与重要性判断

### 6.0 判断口径

- **重要性 = 可操作增量 × 与现有架构的同构度 × 当前路线图的缺口覆盖**。已在路线图/开题中覆盖的（如 MCDP-1 边注）降级为"增援"而非"新方向"。
- 以下全部为**受军事条令/工程文献启发的设计类比**，沿用 `cds4polymarket/docs/investigations/uncertainty-decision-methodology-2026-07-21.md` 的引用纪律：作为假设与设计语言引用，不作为 CDS 领域的经验证据。

### 6.1 跨线通用（最高价值）

**G1. "信息可得性层"应成为所有 CDS 推演/实验的一等公民。**
SEA-27 给蓝方授予完美信息（频率已知、导弹必识别）是其最大方法论瑕疵；Elliott 的 RIP 则把"每个节点看到什么"建为显式对象。教训正反对照：**任何多智能体推演都必须把 per-agent 的 recognized picture（ground truth 的退化子集）建为显式状态变量，并如实披露"上帝视角泄漏"边界**。
- 落点：policysim 引擎（每个 agent 的图景完整度/AOU 类比量作为状态）；Paper B（信息集臂的本质就是操纵 recognized picture）；4polymarket（agent 检索到什么是可审计的）。
- **重要性：高。** 这是两篇论文对所有 CDS 项目最有迁移价值的一条，直接对应仓库已有的"信息访问控制臂"（roadmap §4.2）与"结构性污染"（§6-4）关切，但把它从"实验旋钮"升格为"架构原则"是新增量。

### 6.2 对 4polymarket

**P1. CCIR→PIR→FFIR→EEI→RFI 需求分解链 → agent 的信息采集决策框架。**
预测 agent 的检索/采集目前是启发式的；CCIR 链提供建制化模板：先定义"本决策需要知道什么"（EEI），分解为采集任务，未解问题显式登记（RFI）。与 CDS 的 evidence-ledger / factor-ledger（P1+P2）**天然同构——evidence ledger 就是民事版 RIP**：每条证据带来源、时效、置信度，每个未解 EEI 是 ledger 中的显式空洞。
- **重要性：高。** 可操作、零理论风险、与现有 schema 同构；把"信息不全"从隐式背景变成显式台账，正是 CDS 的核心主张。

**P2. TACSIT 三级 → 市场"定价充分度"分级与"不交易"纪律。**
TACSIT 按"对手对我的确定性"分级行动；市场语境翻转为"我的判断相对市场共识的信息优势"分级：Level 3（我有市场未定价的私有信号 → 建仓窗口，类比 C-ISRT 期）；Level 2（部分定价）；Level 1（已充分定价 → 无 edge，**不行动**）。不确定性下最重要的决策常常是不决策——这为"何时放弃交易"提供纪律化判据。
- **重要性：中-高。** 概念映射干净，但需操作化为可计算的"定价充分度"指标（如相对 consensus 的 ΔI 与信号新鲜度），且不得触碰投注建议红线。

**P3. JIPOE 流程 → 事件推演管线模板。**
JIPOE（界定环境 → 评估行为体 → 枚举并排序 COA）与 CDS 的事件推演管线几乎一一对应；I&W（征兆与预警）定位 = left-of-kill-chain，即"价格大幅移动前的征兆监测"（行为模式 patterns of life、叙事拐点）。
- **重要性：高（与 policysim 共享）。** 见 6.4 S1。

### 6.3 对 4Worldcup（Paper A / Paper B）

**W1. Paper A：PIV 作为"不确定性结构报告"的同向增援。**
路线图 v1.2 已用 MCDP-1 p.11 支撑"PIV 是审计结果之一而非附属标签"（roadmap §3.1 边注）。Elliott 提供第二支撑：A2/AD 下 COP 退化为 organic-only——**图景完整度本身随环境强度变化，因此必须在审计中显式报告**。五个预测者可重述为五种"信息图景"（Elo≈patterns of life；Coach≈专家 HUMINT；CDS≈机器推演；kimi 群体≈群体信号；市场≈资金加权共识）——为 related work 提供信息融合文献入口。
- **重要性：中。** 增援而非新方向；五图景类比有 framing 价值，无方法增量。

**W2. Paper B：信息集臂的设计语言与机制注记。**
Paper B 确认性旋钮"信息集（含/不含市场快照）"本质就是操纵分身的 recognized picture——herding 实验可重述为：**操纵群体成员的 AOU，观察决策何时趋同**。SEA-27 的"加噪/降级因子"思路支持 roadmap v1.3 已列的"完整快照 vs 加噪/延迟快照"子水平；AMW/Dunning 的 own-signal overconfidence 机制（roadmap §4.1 注记）与军事版"对自身传感器过度自信"同构。
- **重要性：中。** 提供解释语言与一个可实现的子臂，但主干设计已由 AMW 两段式覆盖。

**W3. 聚合规则的具体机制：先验评分加权。**
SEA-27 附录 F 的"combat power 评分 → 概率分配"是"按先验价值分配决策资源"的模板：Paper B 聚合臂可按分身历史校准分（Brier reliability 分量）加权，而非等权投票——与已有的选择性路由臂互补。
- **重要性：中。** 具体、可实现，但属聚合臂内的局部设计选项。

### 6.4 对 policysim

**S1. JIPOE + "最可能 COA vs 最危险 COA"双轨 → 推演报告模板。**
军事情报在不确定性下的标准做法是**同时报告最可能行动方案与最危险行动方案**——这与 CDS"黑天鹅生存指南"的定位直接对应：PolicySim 的决策叙事报告可采用 JIPOE 结构化输出（环境约束 → 行为体能力/意图 → COA 枚举 → 双轨排序）。cds4polymarket 已有 MCDP-1 方法论文档铺垫，JIPOE 是其在流程层的具体化。
- **重要性：高。** 直接可写进引擎报告模板与推演逻辑，产品级增量。

**S2. 完美信息陷阱 → 引擎的效度红线（与 G1 同源）。**
PolicySim 引擎知道全部 ground truth，agent 易获得超现实可得性的信息——SEA-27 的完美信息豁免正是前车之鉴。**在引擎中强制"每个 agent 只看到其 recognized picture"是推演效度的前提**，否则推演输出对真实决策的可迁移性无法辩护（呼应 `research-for-dev-projects-2026-07-08.md` 的"应急推演有效性研究"设计）。
- **重要性：高。** 与 G1 是同一原则在引擎层的强制化；若不落实，PolicySim 有效性验证研究在设计上就被污染。

**S3. 任务式指挥（mission command）→ 分布式 agent 的授权边界。**
Elliott 结论章的"分布式决策能力缺口"（条令/训练只在打击群级，DMO 却要求单舰独立）正是多智能体推演的核心问题：agent 信息不全时自主决策，系统如何保证整体一致？军事答案 = 指挥意图显式化（给任务不给路径＋事后回报，MCDP-1 p.68–69 已被引用）。PolicySim 可把 commander's intent 实现为 agent 的显式约束对象。
- **重要性：中-高。** 对多行为体对抗类场景（政策博弈、台海类）直接可用；对自然灾害类单主体场景价值递减。

**S4. See–Think–Do → 对抗性行为体的认知建模模板。**
MILDEC 规划逻辑（让目标看到 X → 相信 Y → 行动 Z）为推演中的谣言/对手策略建模提供链条式模板，优于随机噪声扰动。
- **重要性：中。** 适用范围限于含对抗行为体的场景。

### 6.5 重要性总表

| 编号 | 贡献 | 落点 | 重要性 | 一句话理由 |
|---|---|---|---|---|
| G1 | 信息可得性层 = 一等公民 | 全线 | **高** | 从实验旋钮升格为架构原则，两篇论文正反对照 |
| P1 | CCIR→EEI 需求分解链 | 4polymarket | **高** | 与 evidence-ledger 同构，零风险可操作 |
| S1 | JIPOE + COA 双轨报告 | policysim | **高** | 直接进引擎模板，承接 MCDP-1 已有铺垫 |
| S2 | 完美信息红线 | policysim | **高** | 不落实则有效性验证研究被设计性污染 |
| P2 | TACSIT→定价充分度分级 | 4polymarket | 中-高 | 需操作化指标；受合规红线约束 |
| S3 | mission command→授权边界 | policysim | 中-高 | 对抗类场景直接可用，场景依赖 |
| P3 | I&W / 征兆监测 | 4polymarket+policysim | 中-高 | left-of-kill-chain 定位，流程层增量 |
| W1 | PIV 增援 + 五图景类比 | 4Worldcup Paper A | 中 | MCDP-1 边注已覆盖主干，此为增援 |
| W2 | 信息集臂设计语言 | 4Worldcup Paper B | 中 | AMW 主干已覆盖，提供解释与子臂 |
| W3 | 校准分加权聚合 | 4Worldcup Paper B | 中 | 聚合臂局部设计选项 |
| S4 | See–Think–Do 认知建模 | policysim | 中 | 仅对抗场景适用 |

### 6.6 总体判断

1. **这批认知是重要的，但重要性分布陡峭**：真正够"高"的是四条（G1、P1、S1、S2），共性是**把"谁知道什么"从背景假设变为显式对象**——这与 CDS 的核心主张（决策的计算化、可审计化）同构，且都能在不改动现有路线图主干的前提下落地。
2. **对 4Worldcup 双篇的直接增量有限（全为"中"）**：路线图 v1.2/v1.3 已通过 MCDP-1 边注与 AMW 框架覆盖了主要设计哲学，两篇 DMO 论文是同向增援。不建议为此改动 Paper A/B 主干；可在写作时作为 related work 的信息融合入口引用。
3. **最大受益者是 policysim 与 4polymarket**：二者正处在"引擎/方法论成形期"，JIPOE、CCIR 链、信息可得性层都是可立即进入设计的建制化模板；且 cds4polymarket 已有 MCDP-1 方法论文档，本批文献补齐了其在**信息需求管理（CCIR）与流程（JIPOE）**两个环节的空缺。
4. **边界声明**：两篇来源一为仿真（假设偏袒蓝方）、一为纯文献综合（零实证），军事类比在 CDS 语境中一律按"受条令启发的设计类比"标注，不得作为经验证据引用；涉及市场部分不输出投注建议与收益率。

## 7. 参考

- `analysis/dmo-uncertainty-reading/`（两篇 PDF 副本 + 提取文本 + CHANGELOG）
- `analysis/downloads-pdf-scan/REPORT.md`（109 PDF 盘点）
- `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md` v1.3（MCDP-1 边注、AMW 两段式、信息集旋钮）
- `docs/plans/decision-coscientist-experiment-2026-07-19.md`（Policysim-v0.2 引擎现状）
- `docs/investigations/research-for-dev-projects-2026-07-08.md`（Policysim 有效性研究设计）
- 引用页码：SEA-27 报告为 PDF 印刷页（pp. 31–34, 50–52, 63–66, 70–77, 119–121, 141–142）；Elliott 论文为印刷页（pp. 3, 9, 21, 45, 47, 54–55, 65–67, 76, 78, 81–82, 85–87）
