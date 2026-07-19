# Q1 备忘录：novelty 区分核查与 self-play 理论谱系定位

- 日期：2026-07-18 ｜ 状态：完成
- 输入：三份全文精读（子代理实读，页码均经核对）
  - LEAR：`sources/lear_gurkan.pdf`（GECCO '25 Companion, pp.2309–2326, DOI 10.1145/3712255.3734368，开源 github.com/can-gurkan/LEAR）
  - 应急政策仿真设计研究：`sources/arxiv_2509.21868.pdf`（v2, 2026-02-08, CMU, 38 页）
  - Self-play 综述：`~/Documents/GitHub/0ref/skill/victorchen96.github.io/auto_research/self_play_survey.pdf`（75 页 V16，AI 生成预印本，**仅托管于作者个人网站，未上 arXiv**）
- 结论先行：**交叉点在两篇最近工作的全文层面仍然空白，kill 条件未触发**；但 novelty 表述必须收窄（§1.3）；self-play 理论给 H4 提供了形式化依据，同时推翻了我们原设计中的两个组件（裸 Elo、无多样性门槛）。

---

## 1. LEAR：不覆盖，但锁死一条上位主张

### 1.1 LEAR 是什么（全文实读）

LEAR（Gurkan et al., GECCO 2025, Northwestern CCL/Wilensky 团队）首次将 LLM 作为**变异算子**引入多智能体系统的遗传规划：在三个 NetLogo 资源采集玩具环境中，进化 turtle 的移动控制代码（`fd/rt/lt` 原语 + 视锥条件判断），适应度是**纯仿真内部计数**（食物数/积分），选择机制是 GA 标准 tournament selection（亲本采样算子，tournament size=8，**不是两两对决，无 Elo**），LLM 只做变异（zero/one/two-shot、注释、伪代码两阶段翻译），无评审、无校准、无外部真值、无知识库。自陈 "first to employ an LLM-GP approach in MAS"（p.2310）。实验规模小（10 agents、300 代、$200）。

### 1.2 逐项区分（关键 6 维）

| 维度 | LEAR | 本方向 |
|---|---|---|
| 进化对象 | 语法受限的运动控制代码 | 自然语言决策策略（选项池语义层） |
| 适应度 | 仿真内部计数 | 对真实灾害记录的校准度（外部真值） |
| 「锦标赛」语义 | GA tournament selection（亲本采样） | 策略两两配对对决 + 排名 |
| judge | 无（Verifier 只查语法） | LLM judge，且其噪声本身是研究对象 |
| 验证 | 适应度曲线上升即算成功（benchmark 性质） | 外部效度验证（推演分布 vs 真实记录） |
| 多角色闭环 | 无（同质种群个体进化；团队进化列 future work） | 生成→锦标赛→进化→元评审闭环 |

### 1.3 对本方向 novelty 表述的约束

- **必须放弃**：任何「首次将 LLM 驱动的进化应用于多智能体系统/仿真」的上位主张——LEAR 已正式发表该主张且开源。
- **可以主张**（LEAR 均未占据）：决策策略语义层（非运动代码）的进化；外部真值校准适应度；两两对决式策略锦标赛；Co-Scientist 闭环向应急决策的移植。LEAR 的 future work（团队进化、更复杂环境）也未触及「外部校准」与「应急决策」。
- **必须引用**：LEAR 出自 NetLogo 发源地团队且已发表，related work 不可回避；引用草稿见附录 A。

## 2. arXiv 2509.21868：正交不覆盖，是可借用的叙事框架

### 2.1 它是什么（全文实读）

CMU 的 HCI 设计研究（CHI 系投稿格式，38 页）：16 个月与大学应急团队 5 人共建，13,000 个 LLM agent 模拟毕业典礼疏散（severe weather/bomb threat），最终录像用于志愿者培训、提案写入 after-action report。**核心立场与我们对立**：明确拒绝预测/优化范式（"not as a set of outcomes to be optimized", p.2），验证仅靠常规场景的经验对照与从业者目测（"We did not have the chance to observe real-world behavior under active threat", p.20）。它模拟的是**被疏散的群众**（协调员是规则实体），不是决策指挥层；无搜索、无进化、无锦标赛、无定量校准。

### 2.2 可借用的四件东西

1. **「Validation filter / trust bootstrap」叙事**（p.14-15）：先用可验证基线场景建立校准可信度，再外推新场景——正是我方 Gold 锚定 + 留出测试的实践版论证，该文用 16 个月换来的结论我们可以用定量实验检验。
2. **场景选择的 enabling conditions**（p.18）：有可直接观察的重复基线、决策杠杆在从业者权限内、结果可用运营语言讨论——作为我方 G3 锚案例的筛选标准。
3. **「Fix-it response」访谈法**（p.15-16, 19）：给从业者看故意不完美的输出问「缺什么」而非「对不对」——若做从业者可用性研究，低成本高产出。
4. **权限边界警示**（p.13, 20）：bomb 场景下权限移交警方导致仿真建议无法落地——我方多角色协商需内建权限边界，否则输出策略可能不可执行。

## 3. Self-play 综述：理论谱系与两个设计修正

### 3.1 与本方向同构的理论框架

综述中心论点：**验证信号质量决定 self-play 改进天花板**（p.4）。我方「策略锦标赛+进化」在博弈论上就是 self-play/PSRO 家族：策略池=种群、推演对决=对局、judge=验证器、变异算子=策略探索。因此其理论直接适用：

- **Theorem 3（重采样噪声，p.12-14）**：exploitability ≤ Vmax·n/T + 2ϵVmax/(1−2ϵ)。ε=逐局误判率。
- **Theorem 4（持久性腐败，p.14-15，更贴合我方）**：固定的学习型验证器（同一输入总返回同样错误）下存在**算法无关下限** Θ(ϵVmax)——任何算法、任何查询预算都无法突破。**我方 LLM judge 是固定模型+固定 prompt，正属于这个 regime**：这就是「judge 质量决定进化天花板」的形式化，H4（judge 校准）从工程细节升级为理论必需品。
- **285B 实测（pp.48-55）**：10% 随机翻转噪声即可抹平全部训练增益（+4.8%→+0.1%）；30% 进入主动伤害区（−4.1%）；噪声通道持续支付不应得奖励（观测奖励降幅仅为真实降幅的 1/2.5-1/3，Goodhart 签名）；**训练分布指标是验证器失效的先行指标**（held-out 退化滞后且被 KL 锚缓冲）。推论：我方 judge 逐局误判率须压到远低于 10% 才有正期望进化；锦标赛内部胜率/适应度漂移应设为 judge 失效告警。
- **失败模式映射**（pp.41-43）：reward hacking=进化讨好 judge；strategy cycling=非传递策略空间（A克B克C克A）+封闭池；mode/model collapse=多样性丧失+自评闭环无外部锚。综述给出的 self-play 成功四条件（可靠验证信号、丰富搜索空间、足够容量、多样性维持机制）可作我方方法适用性自检。

### 3.2 两个设计修正（改变原 v3 设计）

1. **弃用裸 Elo，改用 α-Rank / Nash averaging 交叉校验**（综述 8.2, pp.43-44）：Elo 假设传递性，应急策略在场景变体间大概率非传递；且封闭池选头部的 Elo 机械性上涨正是 v3 红队指出的「选择伪影」。修正：Elo 仅作展示；头部选择与主结论依赖 α-Rank（Omidshafiei et al. 2019, Scientific Reports——标题即 "evaluation by evolution"，是锦标赛+进化最贴近的一手祖先）或 Nash averaging（Balduzzi et al. 2018），H2 的「选择伪影对照」用 α-Rank 分数重算。
2. **多样性 D 成为一等指标**（Theorem 5, pp.15-16）：改进率 ∝ D(P)/K。变异算子不能只看头部适应度，需显式行为多样性度量与最低门槛（对应 Co-Scientist 的 Proximity 去重——去重与多样性是一体两面）。

### 3.3 引用安全性（重要）

- 该综述是 **AI 生成、仅托管于个人网站的预印本**（未上 arXiv，自报评审分）。Theorem 3/4/5 经查**在经典文献中无直接出处**（其参考文献未引 stochastic fictitious play 经典工作，也未引 RLVR 噪声奖励新文献如 Shao et al. 2025 "Spurious Rewards"）——定理只能作为「Chen (2026, AI-generated preprint) 在风格化假设下的原创形式化」二手引用，285B 实验属单一团队不可复现结果，引用时必须如实标注。
- 承重的经验论断应引一手文献：Gao et al. 2023（reward overoptimization 标度律）、Robinson 1951（fictitious play）、Lanctot et al. 2017（PSRO）、Vinyals et al. 2019（league training/AlphaStar）、Czarnecki et al. 2020（非传递性几何）、Omidshafiei et al. 2019（α-Rank）、Shumailov et al. 2024 / Alemohammad et al. 2024（model collapse）。**该综述的参考文献表本身也是 AI 生成，每条入库前须过 DBLP/OpenReview 核验**（已发现 α-Rank 条缺卷期等瑕疵）。
- 待核验补引：Shao et al. 2025（Spurious Rewards，错误奖励下 RLVR 仍可能改进——对我方是重要反例/边界条件）、Rad et al. 2026（GRPO 奖励噪声理论分析）。Q2 阶段核验。

## 4. Q1 结论

1. **Kill 条件未触发**：两篇最近工作全文层面均不覆盖本方向核心主张；交叉点空白确认到全文深度。
2. **Novelty 表述收窄为四点**：决策策略语义层进化、外部真值校准适应度、两两对决策略锦标赛（区别于 GA tournament selection）、Co-Scientist 闭环向应急决策移植。
3. **理论地基确立**：验证器质量决定闭环天花板（Theorem 4 的持久性腐败 regime 是我方 judge 的准确模型）；judge 误判率须 ≪10%（285B 实测）；训练分布漂移=judge 失效先行指标。
4. **设计修正两处**：α-Rank/Nash averaging 替代裸 Elo；多样性 D 显式度量与门槛。
5. **带入 Q2 的待办**：ABM 验证文献定位（POM/docking/Windrum/SLALOM）；一手文献 DBLP 核验（含 §3.3 清单）；Spurious Rewards 等反例核验。

## 附录 A：LEAR 引用草稿（related work 用）

> 与本文最接近的是 Gurkan 等人的 LEAR 框架（GECCO 2025），该工作首次将 LLM 作为变异算子引入多智能体系统的遗传规划，在三个 NetLogo 资源采集环境中进化 agent 的移动控制代码。LEAR 与本文同属「LLM+进化计算+多智能体仿真」的交叉地带，但存在本质区别：LEAR 进化的是语法受限的低层运动规则，适应度完全来自仿真内部计数，旨在为 LLM-GP 方法提供基准；本文进化的是应急决策场景中的自然语言决策策略，通过策略两两对决进行选择，并将适应度定义为推演后果分布对真实灾害记录的校准度。此外，本文研究的 LLM judge 噪声校准问题在 LEAR 中没有对应——其适应度由仿真状态直接计算，不存在评审噪声。LEAR 自陈的局限（个体级评估、玩具环境、无外部验证）恰好界定了本文的增量空间。

## 附录 B：2509.21868 引用草稿（related work 用）

> Li et al. [arXiv:2509.21868] 通过 16 个月的参与式设计研究，与大学应急团队共建了 13,000-agent 的毕业典礼疏散 LLM 仿真，最终影响了协调员培训与作业流程。该工作确立了 LLM 仿真对政策实践者「有用」的过程条件（可验证基线、信任引导、与制度协同演化），但刻意回避预测与优化，仅通过从业者的定性判断对常规非应急场景做验证。本文针对的正是其留下的互补问题：LLM 决策仿真能否对历史灾害记录做定量校准，并借此成为应急决策的搜索空间——他们的 agent 模拟被疏散的人群，有用性由制度采纳度量；我们的 agent 模拟指挥层角色，有用性由校准度与决策质量度量。
