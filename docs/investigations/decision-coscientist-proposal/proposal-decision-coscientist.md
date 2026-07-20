# 开题报告：面向应急决策的策略锦标赛与进化式多智能体推演——现实锚校准的方法与实证

> **Evolving Multi-Agent Deliberation: Tournament-Based Strategy Search with Reality-Anchored Calibration for Emergency Decision-Making**
> 版本：v1.4（F5 settleability 切割 + F1 宽类轨道 + F4 Buncefield 修链 + F2/F3 锚源实测升级）｜ 日期：2026-07-19
> 依据材料：Q1（novelty 与理论谱系）、Q2（ABM 验证定位与引用核验）、Q3（校验臂选型）、Q4（古雷锚试编码）、Q5（第二案例）五份备忘录，同目录存档
> 评审状态：R1、R2 两轮独立评审均已通过并逐条回应（reviews/）

---

## 第 0 章 导读：这份报告在做什么（给非专业读者，5 分钟版）

### 0.1 一句话和三个比喻

**一句话**：这份报告研究的是——能不能让 AI 在电脑里把一场灾难「预演」几百上千次，用「打比赛 + 优胜劣汰」的方法自动找出最好的处置方案，并且用真实灾难的官方档案检验：机器找出的方案靠不靠谱。

**为什么值得做**：今天的应急决策主要靠专家经验和事后人工复盘。2026 年，医学领域已经证明「AI 自动提出假设、互相比赛、优胜劣汰、用实验检验」这套闭环能做出真实发现（两种新药候选在实验室被证实）。我们想知道：同一套方法能不能用到灾害应急决策上。

**三个比喻**，看懂全文只需要它们：

| 比喻 | 对应的概念 | 解释 |
|---|---|---|
| **联赛** | 策略锦标赛 | 候选处置方案两两「打比赛」：各在电脑里把灾害推演几十次，谁的后果（伤亡、控制时间等）更好谁赢，积分排名 |
| **育种** | 策略进化 | 赢家不是终点：把好方案的「基因」（派多少泡沫车、何时疏散、先保哪里）做变异和杂交，产生下一代方案继续比赛，一代比一代强 |
| **标准答案** | 现实锚 | 古雷、郑州的官方事故调查报告被拆成一条条可检验的事实（泡沫用了多少吨、疏散了多少人），机器选出的方案要拿这些「标准答案」对账 |

### 0.2 这套机制怎么判断好坏？（四层评估，人工只出现在三个有限位置）

很多人第一个疑问是：「说方案好坏，到底谁说了算？是不是找人打分？」——不是。判断分四层，每一层的「裁判」都不同：

**第一层：一场比赛谁赢？——不用人。** 两个候选方案（比如「泡沫车派 20 辆」对「派 35 辆」）各自放进推演系统跑几十次，每次推演都是 AI 角色（现场指挥、消防、医疗等八个角色）把灾害完整处置一遍，得到后果的分布。谁的分布在预先声明的主指标（伤亡、控制时间）上更好谁赢。这是统计比较。需要定性判断的地方由 AI 评审打分，但它头上有标准答案盯着（「Gold 锚定」：定期拿已知答案的题目抽查它有没有跑偏）。

**第二层：锦标赛这个机制本身有没有用？——跟四个对照组比。** 冠军方案必须击败：(a) 现在的做法（AI 们商量三轮就出方案）；(b) 随机多试几次挑最好的；(c) 普通遗传算法（没有比赛评审环节的「笨进化」）；(d) 人类专家亲自出的方案；(e) 干脆直接问 AI「你觉得该怎么办」。全部用同样的预算、同一把尺子。只赢 (a) 不算本事，赢了 (b)(c) 才说明「比赛+进化」这个机制本身有增量。关键设计叫**锚分离**：评判冠军用的「标准答案」和进化过程中用的「标准答案」是两套不相交的——防止「自己出题自己考」。

**第三层：赢出来的方案在现实里对不对？——跟真实灾害档案对账。** 古雷（2015 年石化爆炸，烧了 56 小时，零死亡）和郑州（2021 年暴雨地铁淹水，处置被官方认定失当）的官方调查报告，被拆成一条条可检验的「因子」：泡沫消耗多少吨、控制时间几小时、疏散了百分之几、有没有蔓延。**对账检验的是「不违背已知证据和因果机制」，不是「复制历史」**：冠军方案跟历史不同不会因此失分——只有违背物理闸门（比如泡沫用量低于规范下限却说能灭火）或违背证据支持的机制才会失分。两个案例的对账方向也不一样：古雷是「正锚」，看方案是否复现了被证明有效的处置；郑州是「负锚」，编码方式反过来——不是要求方案跟失当的做法一致，而是检验它是否避开了「迟停运、迟封闭」的失败链、复现了「早响应、早转移」的有效部分（比如郭家咀 9.8 万人提前转移零死亡）。**人类专家在这里才出场**：至少 3 名应急专家做「盲评」——不告诉他们结果是什么，只让他们评机器方案与历史记录是否一致，防止人情分和后见之明。此外还有两个完全不用人的独立参照：按消防规范计算的泡沫用量下限、按交通工程方法计算的疏散时间——这些工程模型不懂 AI，算出来多少就是多少，用来给 AI 的推演「卡物理闸门」。要坦白说：闸门只能卡住明显离谱的输出，中间灰色地带仍然靠 AI 推演——所以这一层只叫「旁证」，论文的主要论断建立在第二层（赢对照组）上，历史对账是加分项而不是通行证。

**第四层：AI 评审本身可信吗？——四道关。** ① 已知答案的题目抽查（Gold 锚：由人事先写好标准答案的样例——已知「明显好」「中等」「明显差」的策略对，看 judge 判得对不对）；② 误判率必须远低于 10%（依据：285B 参数的实验显示，10% 的随机误判就足以抹平进化的全部增益；理论分析也表明，判对率减判错率（Youden J）必须大于 0，进化才有正期望）；③ 它的排名必须和工程模型的排序显著相关；④ 换一个底座大模型，结论不能翻转。

**人到底在哪里**（准确地说，就三个位置）：① 人类专家出一套方案当「选手」参赛（它是对照组之一）；② 专家盲评当「历史裁判」（第三层）；③ 最终拍板永远是真人——这是整个系统的底线原则：**AI 只动嘴，不插手**。机器的职责是把方案试遍、把证据摆齐；做决定的始终是人。

### 0.3 一个方案的完整旅程（例子）

以「泡沫车派 35 辆，分三批到场」这个方案为例，看它在系统里会经历什么：

1. **出生**：假设生成模块从知识库和历史案例中得到启发，提出包括它在内的 16 个候选方案。
2. **比赛**：它和另一个方案（比如「泡沫车 45 辆一次压上」）各推演 50 次。它比对手控制时间短、泡沫消耗合理——赢。积分上升。
3. **进化**：它成为「种子」：变异出「35 辆但提前 1 小时预置」「30 辆+加强冷却」等下一代方案，继续比赛。三代之后，冠军是「30 辆分两批+冷却优先」。
4. **对账**：拿古雷档案检验——历史上实际用了 850–1467 吨泡沫、56 小时扑灭、第四罐曾复燃、3 万人提前疏散。冠军方案在这些因子上与历史一致吗？专家盲评逐条裁定。
5. **交付**：如果它赢了所有对照组、对账也过关，系统把它和全部证据（推演分布、对账记录、工程闸门检验）一起交给指挥员。采不采纳，人说了算。

### 0.4 报告结构与阅读路线

- 只想了解思路：读完第 0 章即可。
- 想知道凭什么说「没人做过」「理论上成立」：读第 2 章（文献综述）。
- 想知道具体做什么实验：读第 3–5 章（假设、技术路线、实验设计）。
- 关心能不能做成、风险是什么：读第 6–8 章（可行性、风险、进度）。
- 专业术语随时查：文末「术语表」。

---

## 1. 研究背景与问题提出

### 1.1 背景

复杂决策（政策制定、灾害应急）长期依赖专家经验与事后复盘。我们团队构建的 PolicySim 系统（CDS，计算决策空间方法论）提出「让复杂决策先在机器中运行，再在现实中执行」：用 LLM 多智能体角色扮演模拟应急指挥部的多轮协商，以蒙特卡洛采样输出后果指标的分布（伤亡、处置时间、资源消耗等六维），为指挥员提供决策叙事。系统已具备三个灾害场景、八类角色、知识库注入与人在回路机制，承担国家重点研发计划课题五的研究任务。

与此同时，生物医学领域的 AI 自动科研系统在 2026 年取得标志性进展：Google Co-Scientist（Nature 2026）以「假设生成→Elo 锦标赛→进化精炼→元评审」闭环自改进地产生科学假设；FutureHouse Robin（Nature 2026）打通「文献→假说→实验→分析」全闭环并以湿实验真值校准。这两个系统展示了一个可迁移的方法论骨架：**在假设空间上做锦标赛与进化搜索，并用真值锚住搜索过程**。

科学发现与决策推演在抽象层是同一个搜索问题：假设空间↔策略空间、湿实验↔蒙特卡洛推演、物理真值↔真实灾害记录。但直接把这套闭环搬到决策域会遇到三个 Co-Scientist 不曾面对的问题：

1. **没有湿实验**。CDS 的「实验」本身是 LLM 推演，仿真内部循环无法自证；且实测发现 LLM 多次「独立采样」输出方差为零——采样温度不构成统计意义上的独立随机性。
2. **验证器有噪声且持久**。锦标赛的选择由 LLM judge 执行，而我们实测发现更换 judge 模型会使实验结论翻转；self-play 理论表明，固定的、会犯系统性错误的验证器会给进化闭环钉上一个任何算法都无法突破的质量下限（见 2.4）。
3. **真值是回顾性的**。灾害记录是单点、混杂、有幸存者偏差的历史数据，与前瞻可控的湿实验根本不同。

### 1.2 问题提出

本课题的总研究问题是：**在固定算力预算下，引入锦标赛与进化机制的多智能体应急决策推演，能否在预注册指标上显著优于强基线——且其头部策略能在多个真实灾害记录上获得旁证？** 回答这个问题必须同时解决上述三个决策域特有的障碍，而这些障碍的解决方案本身构成本课题的主要贡献。

### 1.3 意义

- 方法意义：为 LLM 决策仿真提供「以现实校准度为适应度」的进化搜索框架。ABM 验证文献（Windrum et al. 2007）中，经验模式主要被用作模型的筛选器；将其作为生成性选择压力的适应度函数用于自然语言决策策略的进化，在该谱系中没有先例（2.5 给出与参数校准谱系的区分）。
- 应用意义：应急决策的事后复盘目前依赖人工，本课题提供「机器预演 + 真实记录校准」的决策辅助路径，与课题五的灾害事故应急决策知识库建设直接衔接。

## 2. 文献综述

### 2.1 AI 自动科研系统

Co-Scientist（Gottweis et al., Nature 2026）提出七类专职 agent 的假设进化闭环：生成、反思（接外部检索的模拟同行评审）、排名（配对辩论 + Elo 锦标赛）、进化（类比/综合/简化变异）、邻近（假设空间去重）、元评审（评审模式回写提示词，免训练学习）、Supervisor 异步调度；在 203 个研究目标上假设 Elo 随 test-time compute 单调上升，三个生物医学场景经湿实验验证。Robin（Ghareeb et al., Nature 2026）以文献 agent 与数据分析 agent 分工闭环完成「假设→实验→分析→跟进假设」，干性 AMD 案例全周期不到 2 小时、约 10.76 美元，其 LLM judge 重测一致性 88%（人类专家 61%）。Biomni（Huang et al., bioRxiv 2025）从文献自动挖掘领域行动空间构建统一 agent 环境。Minasny et al.（2026, Frontiers in Science）将 Co-Scientist 架构复刻到土壤科学，是目前唯一的跨域移植先例，证明「闭环架构移植」本身可发表。本课题是该架构向决策科学的首次移植尝试，但贡献重心不在移植本身，而在移植逼出的新机制（见 2.5 末与第 9 节）。

### 2.2 LLM 社会与政策仿真

Generative Agents（Park et al., UIST 2023）奠基后，AgentSociety、EconAgent、WarAgent、Concordia 等工作密集出现，但基本不做策略空间搜索或进化，验证普遍是软肋——主流做法是复现 stylized facts 或定性历史对照（最强者 Park et al. 2024 以真人访谈初始化、GSS 答案复现率 85%）。与本课题场景最近的是 Li et al.（arXiv 2509.21868）的 16 个月参与式设计研究：13,000 个 agent 模拟大型集会应急疏散，最终影响志愿者培训与作业流程；但其明确拒绝预测/优化范式，验证仅靠常规场景的经验对照，与本课题形成「制度嵌入路线 vs 自动化决策优化路线」的互补定位。该文发现的「validation filter」（仿真输出须能被对照已有经验验证才会被采信）与「enabling conditions」（可观察基线、权限内杠杆、运营语言）为本课题的案例选择与人在回路设计提供了直接依据。

### 2.3 LLM 驱动的进化、优化与锦标赛

本方向有六条相邻工作线，需逐一区分：

**(a) LLM 进化 ABM 规则**：LEAR（Gurkan et al., GECCO 2025）首次将 LLM 作为变异算子引入多智能体系统的遗传规划，在 NetLogo 采集环境中进化 agent 的移动控制代码，适应度为纯仿真内部计数；其选择机制是 GA 意义上的 tournament selection（亲本采样算子），**而非策略两两对决的配对排名**，无 Elo、无外部真值、无 judge。

**(b) LLM 进化代码/算法**：EoH、FunSearch、AlphaEvolve 进化代码或算法，适应度是可执行真值（测试通过率、目标函数值）——验证器无噪声或低噪声，与本课题面对的「judge 即噪声源」问题不同。

**(c) agent 配置与提示的自动进化**：ADAS（Hu et al., ICLR 2025）用 meta agent 以代码迭代编程生成新 agent；AFlow（Zhang et al., ICLR 2025 Oral）把 agentic workflow 优化表述为代码空间的 MCTS 搜索；EvoAgent（Yuan et al., arXiv 2024）用变异/交叉/选择扩增多 agent 系统；OPRO（Yang et al., ICLR 2024）把 LLM 本身用作优化器迭代生成更优解。这条线进化的是 **agent 的构造（代码/提示/工作流），评价基准是任务分数**；本课题进化的是**决策策略（自然语言干预方案），评价是对真实灾害记录的校准度**。

**(d) 提示与文本参数优化**：DSPy（Khattab et al., 2023）把 LM 调用编译为自改进管道、Promptbreeder（Fernando et al., 2023）以自指进化变异提示、TextGrad（Yuksekgonul et al., 2024）以文本「梯度」反向传播改进文本参数、EvoPrompt（Guo et al., ICLR 2024）连接 LLM 与进化算法做提示优化。这些工作优化的是**提示/文本参数**，评价为任务指标分数；本课题优化的是**决策策略内容本身**，评价为现实校准度——对象与适应度均不同，但机制语言（变异、选择、种群）有重叠，related work 必须显式切割。

**(e) 仿真优化（simulation optimization, OR 谱系）**：运筹学有成熟的「通过仿真优化决策」范式（Amaran et al., Annals of OR 2016），用元模型、排序选择、随机搜索等方法在仿真器上优化工程系统参数。与本文的区别是本质性的：其仿真器是被验证过的离散事件模型、目标函数是良定义的量；本课题的仿真器是 LLM 角色扮演（未验证、随机性可疑）、适应度含 LLM judge 噪声与历史锚区间——**本课题研究的恰恰是仿真优化范式在「不可信仿真器 + 噪声验证器」条件下需要新增的机制**。

**(f) 博弈策略进化**：LLM 进化博弈锦标赛与 IPD 策略进化（arXiv 2501.16173），适应度为博弈内生收益，无现实锚。

### 2.4 Self-play 理论与 judge 噪声：验证器质量决定进化天花板

本课题的理论地基来自 self-play 文献。fictitious play（Robinson 1951）与 PSRO（Lanctot et al., NeurIPS 2017）确立了「种群 + 两两对决 + 最优响应」的迭代框架；league training（Vinyals et al., Nature 2019）以历史对手池维持多样性；α-Rank（Omidshafiei et al., Sci. Rep. 2019）与 Nash averaging（Balduzzi et al., NeurIPS 2018）给出非传递博弈下优于 Elo 的排名方法；Czarnecki et al.（NeurIPS 2020）刻画了真实博弈普遍存在的非传递性（「陀螺」几何）。Gao et al.（ICML 2023）的 reward model 过优化标度律表明：对带噪声的奖励信号持续优化，真实质量先升后降。

LLM judge 的噪声已有系统实证：Zheng et al.（NeurIPS 2023 D&B）记录了 position bias、verbosity bias、self-enhancement bias 与有限推理能力——本课题的 judge 校准对象正是这些已知偏倚。RLVR 方向近期两篇工作使「噪声下的进化上限」具体化：Rad et al.（arXiv 2601.04411）解析 GRPO 在噪声奖励下的相变——由 Youden 指数 J=TPR−FPR 决定，J>0 时噪声只拖慢收敛，J<0 时反学习崩溃；Plesner et al.（arXiv 2604.07666）的实证显示 ≤15% 噪声下峰值精度损失 <2pp，两者存在张力，本文成对引用。Chen（2026，个人网站托管的 AI 生成预印本，定理未经独立验证）在风格化设定下给出噪声下限 2ϵVmax/(1−2ϵ) 与 285B 实验（10% 翻转噪声抹平增益），**本文仅将其作为动机性参照，不承担承重论断**。另有警示性反例：Shao et al.（arXiv 2506.10947）发现随机奖励也能使特定模型（Qwen）提升 21.4pp（放大预训练先验而非真实能力），且高度模型依赖——这要求本课题的跨模型复现不是锦上添花，而是排除「先验放大」替代解释的必需品。

**对本课题的含义**：LLM judge 是固定模型+固定 prompt，属持久性噪声源——judge 校准（H4）从工程细节升级为理论必需品；排名须在非传递假设下进行（α-Rank/Nash averaging，弃用裸 Elo）；种群多样性 D 需显式度量与门槛；锦标赛内部胜率/适应度漂移是 judge 失效的先行指标。

### 2.5 ABM 验证与参数校准：本课题方法的谱系位置

ABM 经验验证有三条主要进路（Windrum et al., JASSS 2007）：间接校准（Monte Carlo 生成分布，检验经验观测能否由模型生成）、Werker-Brenner 经验校准、history-friendly（以特定历史轨迹校准）。Grimm et al.（Science 2005）的模式导向建模（POM）主张用多层级多尺度的多个模式作为模型的接受/拒绝过滤器，并强调最强证据是「未参与建模的独立预测」。Axtell et al.（CMOT 1996）的 docking 确立了随机模型输出比较的三级等价标准（数值/分布/关系），并明确等价检验不替代外部效度。Boero & Squazzoni（JASSS 2005）警告宏观拟合不等于微观机制被验证。

**必须正面区分的一条谱系（R1-N1）**：ABM 的**参数校准优化**早已使用「与数据的距离」作为搜索目标——BehaviorSearch（Stonedahl & Wilensky, 2010/2011）在 NetLogo 参数空间上用 GA/PSO 自动标定，SMD/间接推断（Grazzini & Richiardi, JEDC 2015；Gouriéroux et al. 1993）以模拟矩与经验矩的距离做参数估计，Thiele et al.（JASSS 2014）给出操作手册。因此「calibration-as-fitness」若表述为「谱系中无先例」是过宽的，本课题收窄为三重限定的组合：**(i) 搜索对象是自然语言决策策略（非数值参数向量），(ii) 适应度是对历史外部真值的校准度（非对同一仿真内部目标的距离），(iii) 搜索由「锦标赛+进化+元评审」的生成性闭环驱动（非单点参数优化）**。三者同时成立处，参数校准谱系未覆盖；任何单一成分单独看，都有祖先——这一区分构成本课题 novelty 论证的边界。

经全文精读定位（Q2 备忘录）：本课题的「现实锚校准」骨架是验证谱系的嫡系组合——Windrum 分类中的输出验证（间接校准支系）× POM 多模式过滤，数据形态是 history-friendly 的分布化修正（不逐点拟合轨迹，而是检验推演分布与历史锚区间的一致性）。**新成分有二**：(a) LLM 角色扮演智能体作为被验对象——行为规则由自然语言模型生成，「有效自由度」不可枚举，使过度参数化问题发生质变；(b) 上述三重限定组合下的 calibration-as-fitness。

LLM 时代的验证新工作是 SLALOM（Lee & Seering, PoliSim@CHI 2026 workshop）：提出「stopped clock problem」——模拟可经由完全错误的轨迹到达正确终态，主张从终点对齐转向时间序列模式匹配（gates + DTW）。SLALOM 不占有本课题的任何主张（无锚校准、无适应度耦合、无灾害实证），但其批评正好覆盖本课题的终点/分布对齐——本课题因此将处置行动序列的轨迹模式对照纳入设计（第 5.4 节）。

### 2.6 结算驱动校准

以真实结算结果为真值在单点概率预测方向已成范式（Halawi et al. 2024 逼近人类预测锦标赛水平；Prophet Arena 以预测市场实时结算构建基准），但校准对象是「一个模型对一个问题的概率」，无人用于校准多智能体角色扮演推演的后果分布。本课题的历史灾害锚是该范式向多智能体决策推演的扩展。

### 2.7 定位陈述

综合 2.1–2.6：「Co-Scientist 式闭环 × 多智能体决策推演 × 真实灾害记录校准」三元交叉点在两篇最近工作（LEAR、2509.21868）的全文层面均无占位（Q1 全文核查），但相邻几块（LLM+进化、应急 LLM 仿真、结算校准、agent 自动进化、提示优化）都在快速生长，窗口期以月计。本课题的差异化落点：(1) 决策策略语义层的进化（非代码、非 agent 构造、非提示参数）；(2) 三重限定组合的 calibration-as-fitness（区别于参数校准、仿真内部适应度与仿真优化的良定义目标）；(3) judge 噪声下稳健的选择机制（self-play 理论驱动）；(4) 正负双向真实锚（成功处置 + 处置失当案例）。

**与 disaster-KG 谱系的显式切割**：灾害领域已有 disaster knowledge graph 一线工作——LLM4TyphoonKG（github.com/2BAIHAO/LLM4TyphoonKG）证明该线存在（LLM 抽取台风演化/灾情三元组，无抽取评测、无结算语义，CoT 蒸馏 7B）。本课题锚数据集与之的根本区分在 **settleability（可结算性）**：因子 = 带判定规则、阈值区间、反证信号、盲评字段、来源分级的**可裁定断言**；描述性三元组（实体-关系-实体）不可裁定、无阈值、无反证。本课题锚数据集的统一定位为——**首个可结算（settleable）的灾害决策因子集**，与描述性 KG 三元组显式切割。表述场合：novelty/定位陈述（本节）、预期成果（第 9 节）、资产价值、pipeline 契约（M5）。

## 3. 研究问题与假设

**总问题**：固定算力（token）预算下，锦标赛+进化机制的多智能体应急决策推演，能否在预注册指标上显著优于强基线，且头部策略能在多个真实灾害记录上获得旁证？

**锚分离原则（预注册）**：全实验使用两套不相交的锚——**适应度锚**（驱动锦标赛与进化的校准信号）与**评估锚**（仅用于 H1/H3 终末评估的留出锚）。任何策略在进化期间不得接触评估锚；H1 的「显著优于」只在与适应度锚无关的评估锚与主指标上判定，杜绝「自己出题自己考」的循环。**因子池分配规则（预注册）**：因子按族（前兆/抑制/分支/反证）分层，60% 入适应度池、40% 入评估池，分配在实验启动前冻结；两案因子库存目标 ≥20 条，保证评估池 ≥8 条可裁定因子。

- **H1（机制有效）**：相同 token 预算、相同评估协议下，锦标赛+进化条件（C2）在预注册主指标上显著优于全部基线：(a) 单批次协商（C0）；(b) best-of-N 随机采样 + 同 judge 重排序；(c) 普通遗传算法（选项池变异，无锦标赛评审）；(d) 人类专家策略集；(e) 直接作答对照臂 B4。**主指标判定规则（预注册）**：主指标为伤亡估计与控制时间两项；「显著优于」= 在至少一项主指标上显著更好（配对检验，α=0.05，BH 校正）且在另一项上无显著更差；两项均无差异或互有胜负时判 H1 不成立。仅赢 C0 不构成支持（稻草人），须赢 (b)(c) 才归因为机制。
- **H2（进化增益）**：策略质量（α-Rank 分数与主指标）随进化代数上升，且上升幅度显著超过「选择伪影」对照曲线（封闭池内重复选头部的机械性上涨，先测出该伪影曲线作对照）。排名工具为 α-Rank/Nash averaging，Elo 仅作展示。
- **H3（现实锚旁证）**：锦标赛头部策略与 ≥2 个真实灾害记录（古雷 4·6 + 郑州 7·20）中事后判定有效的处置行动一致——含实际采取的有效子行动与事后认定「本应采取而未采取」的正确行动；失败链以 counter_signal 因子编码。**汇总判定规则（预注册）**：评估池 ≥8 条裁定因子中 supported 比例 ≥60% 且无任一因子族被系统性 rejected → H3 成立；supported <40% → 不成立；介于其间 → 报 inconclusive 并公布逐因子明细。**先验回忆排除（预注册）**：头部策略须在评估锚上显著优于 B4 直接作答对照臂（同一底座模型、不经锦标赛/进化、直接要求给出最佳策略）——若 C2 与 B4 无显著差异，则「旁证」可由训练语料回忆解释，H3 判不成立。操作化：有效行动以官方调查报告结构化判定；≥3 名领域专家两轮盲评（首轮隐去地名与结局）；匹配粒度按因子类型预注册（锚类=区间重叠≥50%；分支类=事件级、时间窗 ±12h；反信号类=分布形态级）。
- **H4（评审可信）**：Gold 锚定校准后，Multi-Judge 满足：百分比一致率 ≥85% 且 Cohen's κ ≥0.6；**Youden J=TPR−FPR > 0 且带裕度**（作为启发式目标，依据 Rad et al. 的相变分析，不作硬保证）；逐局误判率 ≪10%（self-play 实测阈值）；**judge 排名与校验臂参照排名的 Kendall's τ ≥ 0.5**（≥10 个策略对，限校验臂覆盖维度）；更换 judge 模型不改变主结论；跨 ≥2 个底座模型复现（排除先验放大解释）。

## 4. 研究内容与技术路线

五个模块架在现有 PolicySim 引擎上（图 1 略）：

**M1 决策假设生成 agent**。接课题三灾害知识库与 OSINT 档案，批量生成候选干预策略与情景变异（「夜间泄漏+东北风」「泡沫供应延迟 2h」）；输出走选项池白名单约束（沿用现有防提示词注入设计）。配套建设假设池：聚类去重、谱系追踪（对应 Co-Scientist 的 Proximity，同时承担多样性 D 的度量职能）。

**M2 策略锦标赛编排**。候选策略两两配对，各在推演中运行 N 次，按预注册主指标判胜负；排名用 α-Rank（主）与 Nash averaging（交叉校验），Elo 仅展示；邻近去重防重复采样；全程 token 记账。引擎改造自团队已有的模型级配对+Elo 实现（policysim-research-Tsinghua `tournament.py`，679 行，Bradley-Terry + CI 收敛 + 自适应配对），把「模型×问题」换成「策略×场景」。**锦标赛参数（预注册）**：种群规模 16 个策略；进化代数 ≤6 代或 α-Rank 排名连续两代稳定即收敛。

**M3 策略进化算子**。在干预维度选项池上定义变异（资源量增减、时机前后、范围缩放）与综合（两策略拼接），头部策略进入下轮锦标赛；显式多样性机制：行为多样性度量 D 与最低门槛（self-play 理论：D=0 时多样性驱动改进为零），防止策略空间坍缩。

**M4 评审与元评审层**。Multi-Judge 多角色裁决 + Gold 锚定校准（改造 cds4polymarket `calibration_lib.py`：Gold-H/M/L 三档标准答案检测 judge 跑偏，需将 Gold 锚从「报告质量」场景重建为「灾害决策」场景）；元评审汇总评审模式回写提示词与配置权重（把现有的人工反馈回路自动化）。锦标赛内部胜率/适应度漂移设为 judge 失效告警（self-play 理论的先行指标）。

**M5 现实锚校准协议**。Factor Ledger 结算协议的灾害域 fork（Q4 已完成 9 条古雷因子试编码：前兆/抑制/分支/反证四类，全部双挂钩——推演可观测 + 历史可裁定；适配改动清单：origin 增 `historical_record`、settlement_rule 采用「历史锚区间 ∩ 推演 [P25,P75]」百分位语言、settlement_record 的 Brier/log_loss 换为 percentile_hit/覆盖率、adjudicator 增盲评字段、data_sources 增来源分级）。郑州因子编码按同法执行（Q5 锚盘点已备）。非 LLM 校验臂（第 5.3 节）提供独立于 LLM 的工程参照。**错分离实现**：因子入库时即标注 fitness_pool / eval_pool，两池不相交，分配实验前冻结。**决策行动错源（2026-07-19 实测可用）**：在官方调查报告与公告之外补一组机器可读行动错源——国家防总响应通告（mem.gov.cn `/xw/yjyw/` 2018-01 起静态 HTML 123 页归档、`/xw/yjglbgzdt/` 2020-07 起 88 页）、省厅（yjgl.gd.gov.cn 2020–2025、yjt.fujian.gov.cn 2019 起、yjt.zj.gov.cn 境内直连可爬）、JMA 防灾信息 XML（Digital Typhoon，2012–2026）、IFRC GO API field-report（5,107 条含 `actions_taken`、中国 69 事件多为 GDACS 自动同步）、NWS api.weather.gov CAP 预警（含 Evacuation Immediate）、NTSB CAROL、CSB 报告全本（BP Texas City）；ReliefWeb API 自 2025-11 起需 appname 预审批，未审批返回 410。

## 5. 实验设计

### 5.1 场景

- **古雷 4·6**（主场景）：2015 年福建漳州 PX 爆炸起火，3×1万+1×2万 m³ 储罐燃烧 56h。锚：官方调查报告 + 媒体一手报道，9 条因子已编码。
- **郑州 7·20**（第二场景/异域外部效度）：2021 年特大暴雨地铁 5 号线/京广隧道事件。锚：国务院调查组报告全文（分钟级决策时间线 + 法规级量化阈值），因子编码待执行（估 1 人日）。
- 横州六蓝（储备场景/零污染锚）：2026 年 7 月广西横州洪水（六蓝水库溃坝），事件晚于底座模型训练截止、天然防「背答案」；seed 已建并完成端到端推演测试，待官方调查报告发布后编码入库（见锚池流水线 Tier 4）。合成调试场景仅用于开发，不进入研究。
- **宽类轨道（增补层，H3 旁证的统计强化；不改 H1/H2 设计）**：在「2 深案」之外追加 1 条**宽类**场景，目标仅作为 H3 旁证（N≥60）的统计强化层，不参与 H1 机制比较、不参与 H2 进化增益的判定。首选**台风**（备选**地震**）：台风宽类数据由 IBTrACS v04r01（1842–至今，NCEI 免 key bulk，每周 3 更，引用 Knapp 2010/Gahtan 2024；HDX 镜像 CC BY-IGO）—其内置 CMA 序列可替代原站 tcdata.typhoon.org.cn（WAF 拦脚本）—加省级应急响应通告（决策侧，详 §4 M5）与 EM-DAT 后果数据拼接；地震宽类备选走 USGS FDSN（免 key，PAGER 警级 + ShakeMap）。宽类与深案共用同一套 Factor Ledger 契约（settleable 因子），仅因子族与判定阈值不同；宽类可与零污染锚并行。

### 5.2 条件与基线

四组条件 × 四个基线，全部在**相同评估协议**（同 judge、同扰动分布）与**相同总 token 预算**下运行（锦标赛额外消耗的 judge/生成/元评审 token 计入预算）。**评估与适应度分离**：C1/C2/C3 进化期只接触适应度锚；终末评估只用评估锚（留出场景变体与留出因子），对所有臂一致。

| 臂 | 内容 |
|---|---|
| C0 | 单批次三轮协商（现行 PolicySim 基线） |
| C1 | 仅锦标赛（M2） |
| C2 | 锦标赛 + 进化（M2+M3） |
| C3 | 全闭环（+M4 元评审回灌） |
| B1 | best-of-N 随机采样 + 同 judge 重排序 |
| B2 | 普通 GA（选项池变异，无锦标赛评审，评估器相同） |
| B3 | 人类专家策略集（≥3 名应急专家各出 1 套策略） |
| B4 | 直接作答对照臂：同一底座模型、不经锦标赛/进化，直接要求给出最佳策略（隔离训练语料回忆与闭环搜索的贡献） |

消融：无反思评审、无邻近去重、无 Gold 校准，各减一组。

### 5.3 非 LLM 校验臂

回应「证据链全栈 LLM」的结构性质疑，装进两个独立工程参照（Q3 已完成选型与协议）：

- **主臂（泡沫+控制时间）**：GB 50151 泡沫需求下限（1 万 m³ 罐单次进攻原液 ≈9.2 吨）× 车辆到达时刻表供给曲线 F(t) × 回归速率烧尽上界（50–80h）。输出累计泡沫消耗与剩余燃烧面积参照轨迹；判异规则示例：推演泡沫 < 下限/3 且宣称扑灭→标红；控制时间 > 烧尽上界×1.2→标红。泡沫车数（10–45 辆）是推演原生干预变量，可直接接入参照计算。
- **副臂（疏散）**：NUREG/CR-7002 ETE 区域疏散排队模型（动员曲线三档 + 瓶颈点排队），输出 T50/T90/T100 与累积 S 曲线；SFPE 水力模型作「比物理极限还快即假」的下界闸门。
- 校验臂自身的可信性依据：ETE 有 Katrina/Irma 飓风逐小时标定先例；罐火有 Goyang 2018 反演（Kwon et al. 2021）与 480 起罐火案例库（Persson & Lönnermark 2004）。
- 判异用「下限闸门+区间」而非点估计（规范值是设计下限；实际含复燃与冗余——古雷 850/1467 吨 vs 下限数十吨）。
- **覆盖范围声明**：校验臂覆盖泡沫、控制时间、疏散三个维度；**伤亡估计维度暂无独立参照**（热辐射半径→暴露人口的转换链假设过多，列为二期），因此伤亡维度的 judge 评分以较低置信度报告，H4 的效度证据仅在校验臂覆盖维度上主张。

### 5.4 轨迹保真对照（回应 stopped clock）

分布对齐之外，对两个可观测维度做过程级对照：泡沫消耗曲线与疏散累积曲线。从真实记录提取阶段原型（响应启动→高峰处置→控制→收尾，对应 Fink 危机四阶段），定义变量 gates（[μ±2σ]），对推演轨迹做单路径 DTW 对齐；聚合 DTW 分数作为第二适应度分量（结果锚一致性 × 轨迹保真度）。注意 DTW 假设单调时间，灾害分支情景树限单路径内使用。

### 5.5 预注册统计方案

- **主指标与判定**：伤亡估计、控制时间为预注册主指标；判定规则见 H1（逐项 + 互不为负）。
- **功效与样本量**：放弃此前被本团队自己证伪的 N=240 先例。按本团队 P12 实验的实测教训（N=6 强信号在 N=30 反转，诚实效应量上限 δ≈0.2–0.3）：δ=0.3、双侧 α=0.05、功效 0.8 时每组约需 N=175；δ=0.2 时约 N=395。优先采用**配对设计**（同一场景扰动种子跨条件配对，Wilcoxon 符号秩检验）提高功效；非配对比较用置换检验或 Mann-Whitney U。正式实验前以 C0 试跑数据重算功效。
- **检验与校正**：多重比较按假设族（H1 族、H3 族）分别做 BH 校正；报告 Cliff's δ 与置信区间；锚对照采用**反转零假设**——预注册等价界值（主指标相对 C0 均值的差异 ≤15% 判「等价」）+ bootstrap（Axtell et al. 1996 §4.2 的药方，防小样本「未能拒绝」假阳性）。
- **锦标赛参数**：种群 16、代数 ≤6 或连续两代 α-Rank 稳定（见 M2）。
- **随机性方案（G2）**：拉丁超立方采样场景参数 + 固定随机种子 + 模型版本钉死；「LLM 响应的条件独立性」明确列为局限；提示词扰动方案的分布有效性检验（输出分布的独立同分布性）作为 G2 的方法产出。
- **预算口径**：总 token（含 judge/生成/元评审），各臂一致；**成本实测前置**（W1–W4 完成单臂成本试跑并外推总预算，作为 go/no-go 输入）。
- **污染控制（预注册）**：锚隔离（策略生成不见锚值）；两轮去标识化盲评；±30% 参数扰动平行变体——策略精确复述史实数字（201.9mm、953、40cm）即判 contaminated 剔除；settlement 优先用语料稀薄锚（247=18+87+142 车辆分布、75cm 标高等）；泄露基线（直接测模型对事故细节的先验知悉度）；B4 直接作答对照臂（见 H3）。
- **模型漂移**：底座版本钉死 + 漂移监测（投稿周期内补实验须用同版本快照）。

## 6. 可行性分析

### 6.1 已有基础（磁盘核查确认）

- **推演引擎**：PolicySim 三场景、八角色、三轮协商、六维指标提取、约 1200 项自动化测试（工程稳定性证据）。
- **锦标赛引擎**：policysim-research-Tsinghua `tournament.py`（BT+Elo+CI+自适应配对）可改造；630 runs MAMR/SASR 基线数据可作对照参照。
- **结算协议**：cds4polymarket 世界杯实验全套 Factor Ledger schema/rubric/预注册 lock；cds4worldcup 5 场实例；古雷 9 因子试编码已完成（Q4），郑州报告 PDF（2026-07-19 实测存活，https://www.mem.gov.cn/gk/sgcc/tbzdsgdcbg/202201/P020220121639049697767.pdf ）与古雷报告 HTML（实测存活，https://yjt.fj.gov.cn/zwgk/sgxxgk_gb/sgdcbg/202501/t20250102_6601366.htm ）均纳入 KB。
- **judge 校准**：cds4polymarket `calibration_lib.py`（Gold-H/M/L + 漂移检测）。
- **选项池**：干预维度即现成变异空间；RoleDNA 五维行为基因（cds-keyperson）可作基因型空间零件。
- **知识源**：课题三知识库 API、OSINT 模块。

### 6.2 缺口（连零件都没有，构成本课题建设工作）

策略级锦标赛编排、选项池变异/进化算子、元评审反馈闭环、Multi-Judge 实现（现仅空表头）、假设池管理；sim 侧三个可观测性缺口（Q4 发现）：初控-复燃两阶段状态机、罐区 1.5D 几何拓扑、伤亡伤/亡分离——不补齐，相关因子永远 inconclusive。

### 6.3 可行性结论

**可行（附条件）**。证据：novelty 在两篇最近工作的全文层面确认空白（Q1）；理论地基成立且可操作（Youden J、误判率阈值、α-Rank）；方法谱系位置明确（Q2，含与参数校准谱系的区分）；校验臂有监管级方法与验证先例（Q3）；古雷锚试编码成功（适配改动有限且已列清单，Q4）；第二锚三要素全满分且 sim 侧零成本（Q5）。条件：G2 统计合法性工作（2–4 周，属研究问题非工程任务）；sim 侧三个可观测性补齐；专家 panel（≥3 名，W1 启动招募）；跨底座模型复现的算力预算（W4 成本试跑后确认）。

## 7. 风险与诚实边界

1. **Elemento 式边界（重组 vs 原创）**：策略进化的变异空间是人事先定义的选项池，机器「进化」出的方案本质是人类处置知识的重组与再组合。本文主张限定为**搜索效率与校准质量的提升**，不主张机器原创处置方案。
2. **真值硬度**：历史记录是回顾性、单点、有幸存者偏差的数据（火被灭了 ≠ 处置最优）。对策：结论措辞限「旁证」；多案例（正锚古雷 + 负锚郑州）；留出锚；反转零假设。
3. **复现≠解释**（Windrum；Boero & Squazzoni）：后果分布一致不验证微观决策机制。结论限定在后果分布层。
4. **等终性 + LLM 自由度**（Grimm）：单模式总能被拟合。对策：多锚点 + 校准/检验锚分离 + 机制检验（反事实对照，如郑州停运时滞的剂量-反应关系）。
5. **judge 效度**：信度≠效度（稳定地错也是 88%）。对策：H4 的效度部分（与校验臂 Kendall's τ，限覆盖维度）+ Youden J（启发式目标）+ 跨 judge 稳健性 + 跨底座复现（防 Spurious Rewards 式先验放大）。
6. **训练数据污染**：两大锚都是超大公共事件。对策见 5.5 污染控制六条（含 B4 回忆对照臂）。
7. **内部主张切割**：Tsinghua 仓库挂起方向 `ideas/09`（古雷政策响应回顾性验证，效应本体 recall/precision，十年政策尺度）与本课题（现场处置策略优化，56 小时尺度）按「验证对象+时间尺度+方法」三轴切割，互相引用；资源紧张时按回退条款合并。
8. **单司法辖区**：两锚均为中国案例；Buncefield（2005 英国 Buncefield 油库爆炸，HSE 官方直链 404）现使用英国国家档案馆 webarchive 归档的 `buncefieldinvestigation.gov.uk` 副本与 FABIG 镜像（Vol.1 https://www.fabig.com/media/tpuaseey/buncefield-incident-miib-final-report-volume-1-dec2008.pdf ；Vol.2 https://www.fabig.com/media/jkvgpiv3/buncefield-incident-miib-final-report-volume-2-dec2008.pdf ，Crown copyright 非商用限制）作为第三锚候选，做跨辖区稳健性——六源中最贴应急指挥决策。**行动锚采集三条硬约束**（2026-07-19 实测后补入）：(a) **2018 断档**——国家防总响应通告归档仅 2018-01 起，2018 年前无官方机读记录，事件采样须避开 2018 年前的中国官方响应源；(b) **历史预警报文无机读存档**——中国气象历史预警报文（含中央气象台台风公报过季不可追溯）无机器可读历史，写入策略生成时不得假设其可回填为行动锚；(c) **ReliefWeb appname**——ReliefWeb API 自 2025-11 起需 appname 预审批（未审批返回 410），不可作为隐式可用源；以上三条为采集准入门坎，违反的锚行不入因子库。

## 8. 进度安排与回退条款（18–22 周）

| 周 | 工作 | 检查点 |
|---|---|---|
| W1–W4 | G2 统计方案与分布检验；sim 侧三个可观测性补齐启动；**单臂成本试跑并外推总预算**；**专家 panel 招募启动（并行）** | **W4 末：G2 不过或总预算超上限 → go/no-go** |
| W5–W11 | M1–M4 模块实现（含 Multi-Judge 从零实现）；Gold 锚灾害域重建；郑州因子编码 | — |
| W10–W14 | G3 锚协议定稿（含留出锚冻结、盲评启动）；校验臂实现；**宽类轨道工作包（台风首选 / 地震备选，N≥60）+ 前瞻采集基础设施补齐（F6，约 1–2 天）** | **W14 末：锚协议未就绪（含违反 §7 风险 8 三条行动锚采集硬约束的锚行未清理）→ 触发回退（见下）** |
| W15–W19 | 主实验（4 条件 + 4 基线 + 3 消融，统一协议与预算） | — |
| W20–W22 | 统计分析、论文写作、投稿（主选 IJCAI 2027，备选 AAMAS 2027；降级出口 PoliSim@CHI 类 workshop） | — |

**预写回退条款**（防路径振荡）：IF W14 末 G3 未就绪 THEN 改投 workshop 版（闭环方法 + 仿真内实验，明确标注无现实锚）或与 Tsinghua 09 方向合并；IF 宽类机判不达标 THEN 降级为生成侧素材（不入结算），不影响深案主线；IF G2 不可达 THEN 终止并将统计合法性负结果写成方法短文（诚实产出）；IF 评审三轮不过 THEN 按缺口备忘录降级（本开题的评审规则，见附）。

## 9. 预期成果与创新点

1. **面向应急决策的策略进化算子与元评审反馈闭环**（磁盘真空区；决策策略语义层的进化，区别于 LEAR 的运动代码、ADAS/AFlow 的 agent 构造、DSPy 系的提示参数）。
2. **三重限定组合的 calibration-as-fitness**：自然语言策略 × 历史外部真值校准度 × 生成性闭环（与 ABM 参数校准谱系、仿真优化谱系正面区分）；正负双向真实锚（成功 + 失当案例）。**首个可结算（settleable）的灾害决策因子集**——因子 = 带判定规则、阈值区间、反证信号、盲评字段、来源分级的可裁定断言；与 disaster knowledge graph 一线（如 LLM4TyphoonKG，LLM 抽取台风演化/灾情三元组、无抽取评测、无结算语义）显式切割：描述性三元组不可裁定，本课题锚带 settlement_rule 与反证信号。
3. **judge 噪声下稳健的选择机制**：self-play 理论驱动的校准标准（Youden J、误判率 ≪10%）、非传递排名（α-Rank）、多样性门槛、选择伪影对照。
4. **LLM 推演作为实验装置的方法检验**：统计合法性方案（G2）与非 LLM 校验臂协议（工程闸门 + 轨迹对照）。
5. 可发布资产：**2 深案 + 1 宽类**可结算（settleable）灾害决策 Factor Ledger 锚数据集、锦标赛协议、校验臂参照实现。

**§9 末 · 二期展望：标度测量层（G2 之后启动，不动 MVE 第一优先）**。G2 与 MVE 完成后，本课题拟启动二期工作包——**100–200 受控配置**扫描，自变量取 judge 噪声 / Youden J / 协调结构 / 模型能力 / 灾种，验证协议采 held-out + 跨底座离样本，输出标度律与失效相图。范式参照 arXiv:2512.08296 *Towards a Science of Scaling Agent Systems*（180 配置 × 1.5 万 runs + 标度律），本课题差异点=以真实世界灾害档案为真值锚。**深案层扩至 3–4 封顶**（古雷+郑州+1–2 国外对照：洪涝对照首选 US 众院《A Failure of Initiative》[Katrina]、化工对照首选 CSB West Fertilizer，全文已 2026-07-19 实测存活、公有领域，依据 `anchor-authenticity-and-corpus-2026-07-19.md`），**宽类 ≥120 事件**（台风+地震双宽类 × N≥60），**灾种 3–4 个、每个凑齐参数/行动/后果三层锚**。venue 映射：NeurIPS D&B 现状已够；Nature ComSci 需三层齐发 + 前瞻锚 1–2 季；Nature/Science 主刊需前瞻命中或外部复现 >1 年。本段为远期工作，不进入 MVE 第一优先。

## 10. 参考文献（已经逐条核验；AI 生成来源已标注）

1. Gottweis J, et al. Accelerating scientific discovery with Co-Scientist. *Nature* 655:487, 2026. DOI: 10.1038/s41586-026-10644-y
2. Ghareeb AE, et al. A multi-agent system for automating scientific discovery (Robin). *Nature* 655:497, 2026. DOI: 10.1038/s41586-026-10652-y
3. Huang K, et al. Biomni: A general-purpose biomedical AI agent. *bioRxiv* 2025.05.30.656746
4. Minasny B, et al. Enhancing soil science research with multi-agent artificial intelligence systems. *Frontiers in Science* 4:1721295, 2026. DOI: 10.3389/fsci.2026.1721295
5. Elemento O. News & Views on AI scientists. *Nature* 655:313–314, 2026（付费墙，论点据摘要转述）
6. Which 'AI scientist' suits your lab? *Nature* 新闻特写, 2026-07-10. DOI: 10.1038/d41586-026-02091-6
7. Park J, et al. Generative agents: Interactive simulacra of human behavior. *UIST* 2023. arXiv:2304.03442
8. Park J, et al. Generative agent simulations of 1,000 people. 2024. arXiv:2411.10109
9. Piao J, et al. AgentSociety. 2025. arXiv:2502.08691
10. Li N, et al. EconAgent. *ACL* 2024. arXiv:2310.10436
11. Hua W, et al. WarAgent. 2023. arXiv:2311.17227
12. Vezhnevets A, et al. Concordia/GABM. 2023. arXiv:2312.03664
13. Li Y, Das S, Shirado H. What makes LLM agent simulations useful for policy practice? An iterative design study in emergency preparedness. 2026. arXiv:2509.21868
14. Gurkan C, et al. LEAR: LLM-driven evolution of agent-based rules. *GECCO '25 Companion*:2309–2326. DOI: 10.1145/3712255.3734368
15. Hu S, Lu C, Clune J. Automated design of agentic systems (ADAS). *ICLR* 2025. arXiv:2408.08435
16. Zhang J, et al. AFlow: Automating agentic workflow generation. *ICLR* 2025 (Oral). arXiv:2410.10762
17. Yuan S, et al. EvoAgent: Towards automatic multi-agent generation via evolutionary algorithms. 2024. arXiv:2406.14228
18. Yang C, et al. Large language models as optimizers (OPRO). *ICLR* 2024. arXiv:2309.03409
19. Khattab O, et al. DSPy: Compiling declarative language model calls into self-improving pipelines. 2023. arXiv:2310.03714
20. Fernando C, Banarse D, Michalewski H, Osindero S, Rocktäschel T. Promptbreeder: Self-referential self-improvement via prompt evolution. 2023. arXiv:2309.16797
21. Yuksekgonul M, et al. TextGrad: Automatic "differentiation" via text. 2024. arXiv:2406.07496
22. Guo Q, et al. Connecting large language models with evolutionary algorithms yields powerful prompt optimizers (EvoPrompt). *ICLR* 2024. arXiv:2309.08532
23. Will systems of LLM agents cooperate? 2025. arXiv:2501.16173
24. Liu F, et al. Evolution of heuristics (EoH). *ICML* 2024, PMLR 235:32201–32223. arXiv:2401.02051
25. Romera-Paredes B, et al. Mathematical discoveries from program search with large language models (FunSearch). *Nature* 625:468–475, 2024. DOI: 10.1038/s41586-023-06924-6
26. Amaran S, Sahinidis NV, Sharda B, Bury SJ. Simulation optimization: A review of algorithms and applications. *Annals of Operations Research* 240(1):351–380, 2016. DOI: 10.1007/s10479-015-2019-x
27. Robinson J. An iterative method of solving a game. *Annals of Mathematics* 54(2):296–301, 1951. DOI: 10.2307/1969530
28. Lanctot M, et al. A unified game-theoretic approach to multiagent reinforcement learning (PSRO). *NeurIPS* 30:4190–4203, 2017. arXiv:1711.00832
29. Vinyals O, et al. Grandmaster level in StarCraft II using multi-agent reinforcement learning. *Nature* 575:350–354, 2019. DOI: 10.1038/s41586-019-1724-z
30. Omidshafiei S, et al. α-Rank: Multi-agent evaluation by evolution. *Scientific Reports* 9:9937, 2019. DOI: 10.1038/s41598-019-45619-9
31. Balduzzi D, et al. Re-evaluating evaluation. *NeurIPS* 31:3272–3283, 2018. arXiv:1806.02643
32. Czarnecki WM, et al. Real world games look like spinning tops. *NeurIPS* 33:17443–17454, 2020. arXiv:2010.09679
33. Zinkevich M, et al. Regret minimization in games with incomplete information (CFR). *NIPS* 20:1729–1736, 2007
34. Gao L, Schulman J, Hilton J. Scaling laws for reward model overoptimization. *ICML* 2023, PMLR 202:10835–10866. arXiv:2210.10760
35. Zheng L, et al. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS* 36 (Datasets and Benchmarks):46595–46623, 2023. arXiv:2306.05685
36. Shumailov I, et al. AI models collapse when trained on recursively generated data. *Nature* 631:755–759, 2024. DOI: 10.1038/s41586-024-07566-y
37. Alemohammad S, et al. Self-consuming generative models go MAD. *ICLR* 2024. arXiv:2307.01850
38. Chen D. Self-play in the age of foundation models: A comprehensive survey. 2026. **个人网站托管的 AI 生成预印本，定理未经独立验证**（仅作动机性参照，不承担承重论断）
39. Rad A, et al. Rate or fate? RLV^εR: Reinforcement learning with verifiable noisy rewards. 2026. arXiv:2601.04411
40. Plesner A, Guzmán F, Athalye A. An imperfect verifier is good enough: Learning with noisy rewards. 2026. arXiv:2604.07666
41. Shao R, et al. Spurious rewards: Rethinking training signals in RLVR. 2025. arXiv:2506.10947
42. Halawi D, et al. Approaching human-level forecasting with language models. 2024. arXiv:2402.18563
43. Yang, Wu, et al. Prophet Arena. 2025. arXiv:2510.17638
44. Grimm V, et al. Pattern-oriented modeling of agent-based complex systems: Lessons from ecology. *Science* 310:987–991, 2005. DOI: 10.1126/science.1116681
45. Grimm V, Railsback SF. Pattern-oriented modelling: A 'multi-scope' for predictive systems ecology. *Phil. Trans. R. Soc. B* 367:298–310, 2012. DOI: 10.1098/rstb.2011.0180
46. Axtell R, Axelrod R, Epstein JM, Cohen MD. Aligning simulation models: A case study and results. *CMOT* 1(2):123–141, 1996. DOI: 10.1007/BF01299065
47. Windrum P, Fagiolo G, Moneta A. Empirical validation of agent-based models: Alternatives and prospects. *JASSS* 10(2):8, 2007（无 DOI）
48. Boero R, Squazzoni F. Does empirical embeddedness matter? *JASSS* 8(4):6, 2005
49. Fagiolo G, Moneta A, Windrum P. A critical guide to empirical validation of agent-based models in economics. *Computational Economics* 30(3):195–226, 2007. DOI: 10.1007/s10614-007-9104-4
50. Stonedahl F, Wilensky U. BehaviorSearch [computer software]. Northwestern University, 2010；及 Finding forms of flocking: Evolutionary search in ABM parameter-spaces. *MABS 2010*, LNCS 6532:61–75, 2011. DOI: 10.1007/978-3-642-18345-4_5
51. Grazzini J, Richiardi M. Estimation of ergodic agent-based models by simulated minimum distance. *J. Economic Dynamics and Control* 51:148–165, 2015. DOI: 10.1016/j.jedc.2014.10.006
52. Gouriéroux C, Monfort A, Renault E. Indirect inference. *J. Applied Econometrics* 8(S1):S85–S118, 1993. DOI: 10.1002/jae.3950080507
53. Thiele JC, Kurth W, Grimm V. Facilitating parameter estimation and sensitivity analysis of agent-based models. *JASSS* 17(3):11, 2014. DOI: 10.18564/jasss.2503
54. Lee J, Seering J. SLALOM: Simulation lifecycle analysis via longitudinal observation metrics for social simulation. *PoliSim@CHI 2026*. arXiv:2604.11466
55. Jones J, Walton F, Wolshon B, et al. Criteria for development of evacuation time estimate studies. *NUREG/CR-7002 Rev.1*, U.S. NRC, 2021
56. Helbing D, Farkas I, Vicsek T. Simulating dynamical features of escape panic. *Nature* 407:487–490, 2000. DOI: 10.1038/35035023
57. Shokri M, Beyler CL. Radiation from large pool fires. *J. Fire Protection Engineering* 1(4):141–150, 1989. DOI: 10.1177/104239158900100404
58. Babrauskas V. Estimating large pool fire burning rates. *Fire Technology* 19:251–261, 1983. DOI: 10.1007/BF02380810
59. Kwon K, Kim Y, Kwon Y, Koseki H. Study on accidental fire at a large-scale floating-roof gasoline storage tank. *J. Loss Prev. Process Ind.* 73:104613, 2021. DOI: 10.1016/j.jlp.2021.104613
60. Persson H, Lönnermark A. Tank fires: Review of fire incidents 1951–2003. *SP Report* 2004:14
61. GB 50151-2010《泡沫灭火系统设计规范》；GB 50074-2014《石油库设计规范》；GB 50160-2008（2018年版）《石油化工企业设计防火标准》；NFPA 11
62. 福建省应急管理厅《腾龙芳烃（漳州）有限公司"4·6"爆炸着火重大事故调查报告》, 2015（公开全文）
63. 国务院灾害调查组《河南郑州"7·20"特大暴雨灾害调查报告》, 2022（应急管理部官网公开全文）
64. Fink S. Crisis management: Planning for the inevitable. 1986（危机四阶段原型）

---

## 附录 A：术语表（按文中出现顺序）

| 术语 | 通俗解释 |
|---|---|
| CDS（计算决策空间） | 我们团队的方法论：把复杂决策问题变成可以在电脑里反复模拟、比较、检验的形式。口号是「让复杂决策先在机器中运行，再在现实中执行」 |
| PolicySim | CDS 的载体系统：输入决策问题，AI 角色扮演多方推演，输出后果的分布与决策报告 |
| 蒙特卡洛推演（MC） | 同一场景用随机扰动重复模拟几十上百次，得到后果的**分布**（而不是单一答案），看的是「大概率会怎样、最坏会怎样」 |
| LLM | 大语言模型（本报告中的 AI 角色与 AI 评审都由它驱动；底座模型为 DeepSeek-V4） |
| token 预算 | 算力花费的统一计量。所有实验臂花同样多的 token，才算公平比较——防止「赢是因为多烧了钱」 |
| 锦标赛（tournament） | 候选策略两两配对，各推演 N 次比较后果，按胜负累积排名（比喻：联赛） |
| Elo | 国际象棋式评分制：赢强的对手加分多，赢弱的加分少。本报告仅作展示，不作排名依据 |
| α-Rank / Nash averaging | 不要求「A 赢 B、B 赢 C 则 A 必赢 C」的排名方法（策略间常常是石头剪刀布关系，Elo 会失真） |
| 进化算子（变异/综合） | 对好方案做「微调」（变异：资源增减、时机前后）或「拼接」（综合：两个方案各取一部分），产生下一代候选（比喻：育种） |
| 多样性 D | 候选池里方案的差异程度。差异归零时进化会「近亲繁殖」退化，需显式维持 |
| LLM judge | 用大模型当评审：给两个候选的推演结果判胜负或打分 |
| Multi-Judge | 多个不同「人格」的 AI 评审分别裁定，看是否一致 |
| Gold 锚定校准 | 定期拿「已知标准答案」的题目抽查 judge 有没有跑偏（高/中/低三档标准答案） |
| Youden J | 评审质量的指标：判对率减去判错率。J>0 表示比瞎猜强；理论表明 J≤0 时进化不但无效反而有害 |
| 现实锚（anchor） | 来自真实灾害档案的可检验事实（泡沫吨数、控制时间、疏散率），用来给推演「对答案」 |
| Factor Ledger（因子账本） | 把现实锚结构化为一条条因子的账本：每条因子写明可观测指标、数值阈值、判定规则、反证信号，以及裁定状态 |
| 适应度锚 vs 评估锚 | 两套不相交的锚：前者在进化过程中当「教练」用，后者只在终末评估当「考官」用——防止「自己出题自己考」 |
| 校验臂 | 不依赖 LLM 的独立工程参照（消防规范泡沫量计算、疏散排队模型），给推演「卡物理闸门」 |
| gates + DTW | 轨迹对照方法：不只看结果对不对，还看过程曲线形状像不像（防止「停摆的钟」——终点对了但过程全错） |
| 预注册 | 实验前把假设、指标、判定规则、统计方法全部冻结写下来，防止事后挑数据 |
| 反事实/留出锚 | 反事实＝「如果当时不这样做会怎样」的对照推演；留出锚＝专门留出来不参与训练、只用于最终检验的锚 |
| 选择伪影 | 在封闭候选池里反复选最好的，分数会机械性上涨——这不是真进步，必须先测出这条「假进步曲线」作对照 |
| Spurious Rewards 警示 | 研究发现：给 AI 随机奖励有时也能「提升」（只是放大了它已有的习惯）——所以必须换不同底座模型复现，排除假象 |

## 附录 B：本开题的评审规则（预注册）

评审由一个无作者上下文的独立子代理按五维 rubric 执行：novelty 区分度 / 证据链效度 / 统计严谨性 / 工程可行性 / 诚实边界（各 1–5 分）。通过标准：无未决致命问题且五维均 ≥3。每轮修改逐条回应评审意见；结构性问题不得以文字修改冒充解决。最多 3 轮；3 轮不过则产出缺口备忘录降级。

## 附录 C：版本记录

- v1.0（2026-07-19）：初稿。
- v1.1：R1 后修订——锚分离原则、H1/H3 判定规则、novelty 收窄（三重限定）、补 ADAS/AFlow/OPRO/Zheng 2023、统计口径、成本前移 W4、伤亡效度降级、Chen 2026 降动机性参照、Kwon 作者更正。
- v1.2：R2 后修订——补提示优化与仿真优化两条先验线切割；因子池分配规则；新增 B4 直接作答对照臂；H4 效度操作化（Kendall's τ）；锦标赛参数；工期重排 18–22 周。R2 评审总评：通过。
- v1.3：**可读性修订**——新增第 0 章导读（给非专业读者：一句话、三个比喻、四层评估结构、一个方案的完整旅程、阅读路线）与附录 A 术语表；正文内容同 v1.2 未变。
- v1.3.1：经非专业读者测试后修订导读——澄清「对账」逻辑（检验「不违背已知证据与因果机制」而非「复制历史」；郑州负锚的对账方向是避开失败链、复现有效部分；物理闸门的灰色地带与「旁证」定位）；补充误判率 10% 的依据与 Gold 锚样例来源。
- v1.4（2026-07-19）：按修订简报 `revision-brief-2026-07-19.md` 外科手术式修订，正文骨架与既有结论未动。① §2.7 与 §9 创新点 2 按 F5 切割 settleability：定位陈述统一为「首个可结算（settleable）的灾害决策因子集」，与 disaster knowledge graph 一线（LLM4TyphoonKG，LLM 抽取台风演化/灾情三元组、无抽取评测、无结算语义）显式区分；因子=带判定规则、阈值区间、反证信号、盲评字段、来源分级的可裁定断言。② §5.1 按 F1 增补宽类轨道（H3 旁证的统计强化层，N≥60），首选台风（IBTrACS v04r01 + 内置 CMA 序列 + 省级响应通告 + EM-DAT）、备选地震（USGS FDSN）；明示不改 H1/H2 设计。③ §4 M5 按 F2 补决策行动锚源清单（mem.gov.cn / 省厅 / JMA 防灾信息 XML / IFRC GO API field-report `actions_taken` / NWS api.weather.gov CAP / NTSB CAROL / CSB 报告全本）。④ §6.1 按 F3 把「公开全文」升级为「2026-07-19 实测存活」，附郑州 7·20 PDF 与古雷 4·6 HTML 链接。⑤ §7 风险 8 按 F4① 修 Buncefield：HSE 官方直链 404 改用英国国家档案馆 webarchive 归档 + FABIG 镜像（Crown copyright 非商用），并补 2018 断档、中国气象历史预警报文无机读存档、ReliefWeb API 自 2025-11 起需 appname 预审批三条行动锚采集硬约束。⑥ §8/§9 与 v1.4 增量的最小对齐（不重排工期、不改 go/no-go）：§9 预期成果第 5 条「双灾害 Factor Ledger 锚数据集」按 §5.1 宽类轨道与 §9 创新点 2 的 settleability 切割，对齐为「2 深案 + 1 宽类可结算（settleable）灾害决策 Factor Ledger 锚数据集」；§8 W10–W14 登记宽类轨道工作包（台风首选 / 地震备选，N≥60）与前瞻采集基础设施补齐（F6，约 1–2 天），W14 检查点交叉引用 §7 风险 8 三条行动锚采集硬约束；§8 预写回退条款补宽类降级路径（机判不达标 → 降级为生成侧素材，不影响深案主线）。⑦ 二期工作包「标度测量层」：§9 预期成果末增「二期展望：标度测量层（G2 之后启动，不动 MVE 第一优先）」段落——100–200 受控配置扫描，自变量=judge 噪声 / Youden J / 协调结构 / 模型能力 / 灾种，验证协议=held-out + 跨底座离样本；范式参照 arXiv:2512.08296 *Towards a Science of Scaling Agent Systems*（180 配置 × 1.5 万 runs + 标度律），本课题差异点=真实世界真值锚；深案 3–4 封顶（古雷+郑州+1–2 国外对照，US 众院《A Failure of Initiative》[Katrina] + CSB West Fertilizer 首选）+ 宽类 ≥120（台风+地震双宽类 × N≥60）+ 灾种 3–4 个 × 三层锚（参数/行动/后果）；venue 映射 NeurIPS D&B / Nature ComSci / 主刊三档；明确不动 MVE 第一优先。
