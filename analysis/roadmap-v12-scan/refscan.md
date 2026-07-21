# 双篇路线图 v1.1 文献扫描（refscan）

> 日期：2026-07-22
> 执行者：文献扫描子代理
> 范围：`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md` v1.1（重点 §4 新增部分）；`/Users/tangzw119/Downloads/ima-decision-under-uncertainty/` 4 篇英文原文；`analysis/worldcup-proposal-review/stage2-literature-table.csv`（37 篇池，下称"L 池"）；`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md` §10（43 条，下称"v2 refs"）
> 边界：只做文献筛选与新发现扫描；不评价路线图流程设计（系统工程审查由另一代理负责）。
> 简称：AMW = Agarwal, Moehring, Wolitzky《Designing Human-AI Collaboration: A Sufficient-Statistic Approach》；Dunning = 《Factors Affecting Appropriate Reliance on AI DSS》（CMU 博士论文）；BHS = Bradley, Hirt, Smit《Strategy Beyond the Hockey Stick》；Tychastic = Ross et al.《Tychastic Optimization of ISRT Information Systems》。

---

## A. 路线图 v1.1 新增部分的引文缺口

逐条列出"论断 → 需要什么类型的文献 → 候选"。候选中标 **真缺口** 者表示 L 池与 ima 4 篇均无可用条目，需另行外部检索。

### A1. §4.1 herding 操作化双层指标

1. **论断**：群体内部一致性用"同任务内分身输出的方差分解 / token-overlap（参照范式指标族）"测量。
   - 需要：多智能体输出趋同/一致性的定量测量先例。
   - 候选：L37 InfoDelphi（arXiv:2607.01661，herding ablation + 诊断粒度）；Scaling Agent Systems 原文——**目前只引了内部文档** `analysis/kimi-reasoning-assessment/reference-paper-anatomy.md`，其规范书目须从该解剖文档提取后补入（本次扫描未见原文，不代拟条目）。
2. **论断**：群体-市场一致性用"偏差方向统计 + 信息增益 ΔI（接 v2 H4）"。
   - 需要：LLM 输出与市场共识对齐度的测量先例。
   - 候选：L05 AlDahoul et al.（SSRN 6900538，"LLM 是否复述市场共识"最近竞品，直接同构）；L13 Prophet Arena（arXiv:2510.17638，market-relative performance，v2 refs #13 已引）。
3. **论断**：群体与市场一致既可能是 herding 也可能是"独立同答"，只有信息集消融能分开（§4.1 末句 + §4.2 第四旋钮）。
   - 需要：信息披露/信号结构作为因果识别手段的方法论文献。
   - 候选：**AMW（ima 新文献，见 B1）**——把 disclosure policy 当作识别变量、用响应函数 V(x) 分离"跟随 AI"与"自有信号"，与第四旋钮逻辑同构，是最强补强；L37 InfoDelphi（信息对称性消融）。

### A2. §4.2 实验设计新增元素

4. **论断**："single-agent 超 ~45% 后加 agent 呈负收益"（规模旋钮行的参照范式依据）。
   - 需要：Scaling Agent Systems 原文规范条目。**目前仅引内部文档**，属必补缺口（书目从 reference-paper-anatomy.md 提取，本扫描不代拟）。
5. **论断**：persona 差异化是否产生实质性信息异质。
   - 需要：群体多样性 → 信息异质 → 聚合收益的先验文献。
   - 候选：v2 refs #11 Hong & Page（PNAS 2004，已引）；L22 Schoenegger et al. Silicon Crowd（arXiv:2402.19379，LLM ensemble 最接近先验）；L28（Phil. Trans. R. Soc. B 2026，crowd-vs-LLM accuracy–correlation effect）。Dunning 仅可作背景（见 B2）。
6. **论断**：结算路径 (i) 自建题目 + 人工结算须配"Bosse 式 ~95%"准确率声明 → **已引** arXiv:2601.22444（L18），无缺口。
7. **论断**：结算路径 (ii) 真实市场"结算 trustless"但"agent 可检索则独立判断被结构性污染"。
   - 需要：链上结算作 ground truth + 检索污染控制的先例。
   - 候选：L35 Qin Polymarket-v1（arXiv:2606.04217，单账本 settlement-ground-truth 范式）；L36 Foresight Arena（commit-reveal，v2 refs #23 已引）；L12 ForecastBench（contamination-free 设计，v2 refs #24 已引）；L15 Hindcast（arXiv:2607.14051，retrieval snapshots 控污染）。
8. **论断**：差异化三段式中"真正的占位对照是 Scaling Agent Systems 与 InfoDelphi"。
   - 候选：L37 在池；Scaling Agent Systems 原文书目缺失（同 A2-4）。Prophet Arena / ForecastBench / Foresight Arena 均已在池（L13/L12/L36）。

### A3. §4.3 power analysis 重做

9. **论断**：锚点 "α*=0.02、80% power、≈350 resolved binary predictions" → **已溯源** arXiv:2605.00420（L36），无缺口。
10. **论断**：任务流时间聚簇须按设计效应折算有效样本量。
    - 需要：聚簇调整 power analysis / design effect 方法学文献。
    - 候选：**真缺口**（L 池与 ima 均无；需外部检索 cluster-robust / design-effect 文献）。
11. **论断**：两阶段 adaptive design 必须写入预注册，否则构成隐性 garden of forking paths；方案 B 需显式 MDE 声明。
    - 需要：adaptive/sequential design 与预注册方法学文献。
    - 候选：**真缺口**（方法学条目需外部检索）。部分缓解：AMW 的"第一阶段估计充分统计量 → 第二阶段实现并验证最优设计"是两阶段实证设计的先例（非方法论综述，但可作 design pattern 引用，见 B1/C3）。

### A4. §4.4 归因操作化与 §4.5 期末考规格

12. **论断**：双人盲标、Cohen's κ ≥ 0.80、对称编码。
    - 需要：评分者一致性/内容编码方法学经典文献。
    - 候选：**真缺口**（池与 ima 均无；外部检索 Cohen's κ / inter-rater reliability 经典条目）。
13. **论断**：评估集随机分层抽样（非时间块）以避免域偏移与过拟合解释混杂。
    - 需要：评估集划分/分布偏移的评估方法学文献。
    - 候选：**真缺口**（L12 ForecastBench dynamic contamination-free 设计仅部分相关）。
14. **论断**：§4.2 底座"≥2 模型家族，其一为版本固定的开源模型"。
    - 属设计裁定，不强制需文献；若要支撑"跨模型家族稳健性"可引 L37/L36 的多模型对照实践。
15. **论断**（关联 Paper A §3.2）："前五中四与随大流碰上不可区分"的基准率纪律。
    - 候选：v2 refs #7 Tetlock（已引）；BHS 的 outside view / reference-class 论证仅作背景（见 B3），不宜作承重学术引文。

**缺口汇总**：必补 1 项（Scaling Agent Systems 原文书目，从内部解剖文档提取）；真缺口 3 项（聚簇设计效应、adaptive design/预注册方法学、Cohen's κ 编码方法学），均需外部检索；其余论断在 L 池或 ima 4 篇中均有候选。

---

## B. ima 4 篇逐篇判定

### B1. AMW — Designing Human-AI Collaboration: A Sufficient-Statistic Approach

- **一句话概括**：对二元分类任务，用"人在看到校准 AI 评估 x 后的正确率函数 V(x)"作充分统计量，不建结构模型即可求解最优人-AI 协作设计（自动化/委派/披露策略），并在在线事实核查实验中两阶段验证（第一阶段估 V、第二阶段实测五种设计，预测误差 <1.6pp）。
- **判定：值得**（本次扫描中最值得列入的一篇）。
- **支撑路线图位置**：
  - §4.1/§4.2 第四旋钮：AMW 把 disclosure policy 当识别变量、用响应函数分离"跟随信号"与"自有信息"，与"操纵 agent 能否看到市场快照以区分跟风复述 vs 独立同答"同构——为信息集消融提供方法论先例（A1-3）。
  - §4.3：其两阶段设计（先估充分统计量、再实现并验证最优策略）是 roadmap 要求的"两阶段设计写入预注册"的实证先例（A3-11 的部分缓解）。
  - §4.2 差异化论证：提供"设计空间过大不靠穷举实验、靠充分统计量坍缩"的范式对照。
- **规范引文条目**：
  Agarwal N, Moehring A, Wolitzky A. Designing Human-AI Collaboration: A Sufficient-Statistic Approach. Working paper, 2025-04-18（文中日期）. 作者单位：MIT/NBER、Purdue、MIT。JEL: C91, D83, D89, D47。出处（期刊/编号）：unknown（原文未见发表信息，引用前须外部核实是否已有期刊版）。
- **注意**：实验对象是人-AI 协作（人是决策者），Paper B 是全 LLM 群体——引用时须声明跨域借用（human reliance → agent herding 的类比），不能写成对 LLM 群体的直接结论。

### B2. Dunning — Factors Affecting Appropriate Reliance on AI Decision Support Systems

- **一句话概括**：CMU 博士论文（导师 Fischhoff），三个 Connect Four 人机实验，操纵 AI 顾问的技能水平、输出展示形式（类别/概率/top-3 排序）、出场顺序与对手技能，测量"适当接受/适当拒绝"——结论：顾问可靠性是团队表现最大决定因素；高自我置信者更多拒绝 AI 建议、表现反而略差；被试几乎没有从 AI 顾问中学到东西。
- **判定：仅背景**。
- **理由**：其"appropriate acceptance/rejection"操作化与"顾问技能 × 展示形式"factorial 对 §4.1 操作化有设计启发，且"自我置信 → 拒绝建议"与 AMW 的 own-signal overconfidence 互证；但研究对象是人机 teaming（非 LLM 群体）、任务为博弈游戏、且为非同行评审学位论文，不宜作承重引文。可在 related work 脚注作为 reliance 操作化的先例引用。
- **规范引文条目**（若引用）：
  Dunning RE. Factors Affecting Appropriate Reliance on Artificial Intelligence Decision Support Systems. PhD dissertation, Department of Engineering and Public Policy, Carnegie Mellon University, Pittsburgh, PA, 2024-08. 出处 URL：unknown（原文未见）。
- **重要勘误提示**：roadmap 若引用须注意其实验 3 的 "Oracle Policy" 评分、skill score 定义与 Paper B 的 proper-score 体系不同，不可混用术语。

### B3. BHS — Strategy Beyond the Hockey Stick

- **一句话概括**：McKinsey 合伙人基于数千家大企业样本的实证管理书：企业经济利润呈 Power Curve，10 个杠杆解释 80% 以上的上下迁移；主张用"外部视角"（reference-class 基准率）对冲战略室里的社会性偏差（hockey stick 预测、归因错误、把业绩当能力）。
- **判定：仅背景**（实践者书籍，非学术文献）。
- **与路线图的弱关联**：Ch.3 "Bold forecasts" 三节（缺乏基准线、业绩归因错误、如何应对不确定性）与 Paper A §3.2 措辞纪律、v2 §7.1 基准率陷阱、§4.4 归因操作化在精神上同向；"outside view"可衬托 Paper A 的市场基准率论证。但双篇论文的任何承重论断都不应引此书。
- **规范引文条目**（若作背景引用）：
  Bradley C, Hirt M, Smit S. *Strategy Beyond the Hockey Stick: People, Probabilities, and Big Moves to Beat the Odds*. Hoboken, NJ: John Wiley & Sons, 2018. © 2018 McKinsey & Company.
- **勘误提示**：其 "1 out of 2,393"（Apple 级公司）、"8% 平均上移概率"、"10 变量解释 80%+ 迁移"等数字出自 McKinsey Corporate Performance Analytics 自有样本（Ch.4/Exhibit 14），若引用须标注为其内部数据，非公开可复算数据。

### B4. Tychastic — Tychastic Optimization of ISRT Information Systems

- **一句话概括**：NPS 技术报告：把对手 ISR 信息网络建模为排队流网络，用动态优化求"最小拥塞"基线与"最大拥塞"火力注入策略；在网络配置参数未知时以 tychastic（基于支撑集/Lebesgue-Stieltjes 积分，不用 Ito 随机微积分）轨迹优化求鲁棒策略——案例显示最小化"平均"拥塞反而增大方差（tr(C) 506.56→597.47），而对协方差迹加路径约束的 tychastic 策略把 tr(C) 降到 72.08。
- **判定：不值得**（列入双篇参考文献）。
- **理由**：军事 C2/网络拥塞控制域，与双篇的主题、方法、文献谱系均不相交；引用反而稀释文献聚焦度。其概念价值见 C2/C3（仅作设计哲学启发，不引）。
- **规范引文条目**（备查，不建议列入）：
  Ross IM, Karpenko M, Proulx R, King J. Tychastic Optimization of ISRT Information Systems. NPS-MAE-23-009, Naval Postgraduate School, Monterey, CA, 2023-10. https://hdl.handle.net/10945/73591（美国政府作品，Distribution A）。
- **勘误提示**：§6 的 "U(0.5, 1/3)" 记法原文自相矛盾（"uniform distribution with mean mu and standard deviation sigma"，但均匀分布应由区间端点定义），引用其数字时须小心。

---

## C. 颠覆性发现与新猜想

### C1. 与 Paper B 设计直接冲突或补强的发现

1. **（补强，最重要）"跟随 vs 自有信息"可用响应函数识别，而非只靠行为标签**。
   AMW 发现人对 AI 预测的 under-response 几乎完全源于**对自身信号精度的过度自信**，而非对 AI 的不信任（§6.3 "Overconfidence or AI Neglect?"，文件 Designing_..._Approach.md:728 起；摘要同述）。对 Paper B 的含义：herding 的对立面（"独立判断"）可能同样由"分身对自身 persona 信号的过度加权"维持——这为 persona 多样性旋钮提供了行为机制假设，也把 herding 从"输出相似度"深化为"信念更新权重"问题。Dunning 独立复现了同向现象（高自我置信 → 更多拒绝 AI 建议、表现略差；Conclusion 章，Factors_..._Systems.md:3799 起），两篇互证，说明该机制跨任务稳健。
2. **（潜在冲突）"协作/辅助的增量价值可忽略"对聚合规则旋钮构成先验挑战**。
   AMW 核心结论：最优策略是"AI 置信则自动化、不确定则委派给人并完全披露"，而"人机协作辅助"相对"选择性自动化+委派"的额外收益**可忽略**（摘要；Introduction，Designing_..._Approach.md:63-69）。映射到 Paper B 聚合旋钮：连续加权/辩论收敛式"混合聚合"可能系统性输给"选择性路由"（按置信度把任务路由给最优子群体，其余直接采纳）。当前三水平（多数投票/加权/辩论收敛）**没有选择性路由臂**——这是先验文献支持的一个设计盲区。跨域借用须声明（human-AI → LLM 群体）。
3. **（补强）完全披露优于部分披露**。AMW 估得 V(x) 为凸，推出对委派案例**完全披露 AI 预测最优**，与此前"部分披露更优（防努力挤出）"的结论相反——他们承认努力挤出存在但太弱（Introduction，Designing_..._Approach.md:63）。对第四旋钮的水平设置有含义：若给 agent 看市场快照，"看完整快照 vs 看加噪/延迟快照"可作为子水平，且先验是完整披露不劣。
4. **（补强/风险提示）顾问技能是团队表现的最大决定因素**（Dunning 摘要与 Conclusion）。映射到 Paper B：底座模型能力的主效应可能淹没结构旋钮的效应——支持 §4.2 "≥2 模型家族"要求，且提示 model family 应作为析因的显式区组/因子而非仅复现性注脚。
5. **（概念补强，不引原文）Tychastic 的"平均最优 ≠ 鲁棒最优"**。Tychastic §6 案例：对不确定参数最小化平均代价反而放大方差，须直接对统计量（协方差迹）加约束才得到鲁棒策略（Tychastic_..._Systems.md:408-410）。映射：Paper B 若以"平均 RPS/Brier 最优"选配置，可能在换模型家族/换任务流后不稳健；期末考除均值外应报告跨条件方差（与 §4.3"负结果必报、全套诊断"同向）。属设计哲学类比，不建议引用原文。

### C2. 可作为新选题的猜想

1. **"充分统计量 V(x) for LLM crowds"**：对 LLM 群体定义 V(x) = 群体在市场隐含概率为 x 时的已结算正确率，先估 V、再用信息设计方法求最优"市场信号披露 + 聚合"策略，两阶段验证。这把 Paper B 从"4 旋钮 18 格 factorial"改写为"估计一条响应曲线 + 验证一个最优策略"，样本量需求与确认性假设数量都大幅下降——直接回应 §4.3 统计力缺口。（出处：AMW 全文框架，Designing_..._Approach.md:35、:55、:117；两阶段设计的稀缺性自述见其 Related Literature。）
2. **"herding 的信念更新分解"**：把 AMW 的 under-response 分解（own-signal overconfidence vs signal-source under-confidence）移植到 LLM 分身：通过操纵 persona 先验强度与市场信号精度，分解群体趋同究竟由"persona 信号过弱"还是"市场信号过强"驱动。可作 Paper B 的一个预注册次级假设或独立短文。（出处：AMW §6.2–6.3，Designing_..._Approach.md:690、:728；Dunning 自我置信发现互证。）
3. **"tychastic 基准"**：把模型家族、任务流等不确定环境因素当 tychastic 参数 p，选配置时优化 worst-case/方差约束目标而非均值，形成"鲁棒群体预测配置"选题。（出处：Tychastic §4–6，Tychastic_..._Systems.md:253-414。）概念启发，原文不引。

### C3. 比当前 Paper B 更优雅的论文框架/实验方案

**AMW 两阶段充分统计量设计（最值得认真考虑）**：第一阶段在开发任务流上估计 V(x)（群体正确率对市场隐含概率的响应函数，可从 trace + 结算数据非参数估计），用凸性/形状检验推导最优披露与聚合策略；第二阶段按冻结策略在期末考集上验证预测精度（AMW 做到预测与实测差 <1.6pp，Introduction，Designing_..._Approach.md:73-83）。相对当前 18 格 factorial：
- 确认性假设从"多主效应 + 交互"坍缩为"一条曲线 + 一个策略验证"，天然满足 §4.3 方案 B 的"1–2 个预注册主效应 + MDE"精神；
- "两阶段 + 预注册"与 §4.3 adaptive design 要求结构兼容（第一阶段 = 筛选/估计，第二阶段 = 确认）；
- herding 判定从"输出相似度阈值"升级为"响应函数对基准线的偏离"，§4.1 操作化可直接嫁接。
风险：V(x) 的估计本身需要跨 x 全谱的已结算样本，低 x 区间（冷门事件）样本稀疏；充分统计量假设（V 不依赖披露策略）需在 LLM 群体上先验证——AMW 的 Assumption 2.1/2.2 检验方法（Designing_..._Approach.md:700 起）可借用。

---

## 附：本次扫描未做事项

- 未核实 AMW 是否已有期刊发表版（引用前须外部检索确认 venue）。
- 未提取 Scaling Agent Systems 原文书目（在其解剖文档 `analysis/kimi-reasoning-assessment/reference-paper-anatomy.md`，属 A2-4 必补项）。
- 真缺口 3 项（聚簇设计效应 / adaptive design 方法学 / Cohen's κ 方法学）未做外部检索，按需另起任务。
