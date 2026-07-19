# Q2 备忘录：ABM 验证谱系定位、SLALOM 对话、引用核验与 LQS 分级

- 日期：2026-07-18 ｜ 状态：完成
- 输入：三份子代理报告（ABM 三经典精读 / SLALOM 全文精读 / 15 条引用核验 + LQS 分级），原文存 `sources/`（grimm2005.pdf、axtell1996.pdf、windrum2007.txt、boero2005.txt、grimm2012.txt、slalom_2604.11466.pdf）

---

## 1. 定位判决：现实锚校准在 ABM 验证 30 年谱系中的位置

**骨架是已知方法的嫡系组合，有两个新成分。**

- **主定位：输出验证（Windrum et al. 2007 分类）**，操作上调和了间接校准进路（§4.5：Monte Carlo 生成分布，检验经验观测值能否由模型生成）与 Werker-Brenner 经验校准（§4.10：按相容百分比赋似然）。我方「不逐点拟合、只检验分布与锚的一致性」正是这两步的标准操作。
- **机制上：POM 多模式过滤**（Grimm et al. 2005；Grimm & Railsback 2012）——多个异质锚点各自作为接受/拒绝过滤器，类别式匹配标准（categorical acceptance），反过度定量。差距：POM 要求模式跨层级（个体行为层+系统层），我方锚点目前只在结果层。
- **数据形态：history-friendly 的分布化修正**。Windrum 批评单轨迹对单轨迹不是强检验，开出的药方是「mDGP 输出轨迹分布要逼近真实历史轨迹」（§5）——我方「分布 vs 锚」正是按此方做的。
- **不是 docking**：Axtell et al. 1996 是模型对模型的等价检验；借用其分布等价统计语言，但其划界（不替代外部效度）恰恰支持我方「旁证」措辞。

**两个新成分**：
1. **被验对象新**：LLM 角色扮演智能体——行为规则由自然语言模型生成，「有效自由度」不可枚举，使 Windrum §5.2 的过度参数化问题发生质变。
2. **calibration-as-fitness 真新**：POM 用模式做接受/拒绝过滤器、间接校准用模式约束参数、Werker-Brenner 用似然事后折扣——该谱系中模式只做**筛选**，从不做**生成性选择压力**。把锚一致度作为进化的连续适应度，谱系中无对应物。这是可主张的真新意，也是最危险处（适应度噪声直接污染选择，见 §3）。

**三条最致命审稿攻击线（预注册时必须回应）**：
1. 等终性 + LLM 无限自由度（Grimm 2012 §2：单模式总能被拟合，for the wrong reasons）→ 对策：多锚点 + 留出锚（校准用锚与检验用锚分离，Grimm 2012 §6a 的校准污染禁令）。
2. 小样本「未能拒绝」陷阱（Axtell §4.2：小样本提高等价假阳性）→ 对策：反转零假设（「差异不超过 X%」）+ bootstrap，Axtell 自己开的药方。
3. 复现≠解释（Windrum §5；Boero & Squazzoni §2.11：宏观对上≠微观机制被验证）→ 对策：结论措辞限定在后果分布层，不声称验证了 LLM 角色的微观决策机制。

## 2. SLALOM：不构成占位，但构成必须回应的方法论批评

SLALOM（Lee & Seering, KAIST；**PoliSim@CHI 2026 workshop**，arXiv 2604.11466，正文 5 页）：「stopped clock problem」——模拟可能经由完全错误的轨迹到达正确终态，故主张从终点对齐转向时间序列模式匹配（gates=[μ_GT±2σ_GT] 过滤器 + 多变量加权 DTW）。

- **零实质占位**：验证对象是过程轨迹而非后果分布；gates 只做剪枝/审计，全文无进化适应度耦合；无灾害实证（案例是会议语料+手工合成轨迹）。
- **但它正好打在我方的软肋上**：现实锚校准本质是终点/分布对齐，暴露在 stopped clock 批评之下。写作必须主动引用并回应，否则审稿人替我们引。
- **吸收方案**（升级为设计元素）：从真实灾害响应时间线提取阶段原型（Fink 1986 危机四阶段，SLALOM 已替我们引好），对推演的处置行动序列做 gates+DTW 轨迹对照；聚合 DTW 分数改造为**第二适应度分量**（结果锚一致性 × 轨迹保真度），进化同时惩罚「终点错」和「轨迹错」。注意 DTW 假设单调时间，灾害推演的分支情景树需在单路径内使用。
- **附带发现**：PoliSim@CHI 2026（"LLM Agent Simulation for Policy" workshop）这个venue 存在——既是社区信号（该方向已有 workshop 生态），也是潜在的降级投稿出口。

## 3. 新增理论输入（超出 Q2 原计划的收获）

核验中发现两篇直接决定 H4 设计的新文献：

1. **Rad et al. 2026（arXiv 2601.04411, "Rate or Fate? RLV^εR"）**：GRPO 在噪声奖励下的相变由 **Youden 指数 J = TPR − FPR** 决定——J>0 时噪声只拖慢收敛（"rate, not fate"），J=0 中性，J<0 反学习崩溃。**这给了我方 judge 校准一个可操作标准：不只是「准确率」，而是 J 显著大于 0 并有裕度**。与 self-play 综述的 285B 实测（10% 翻转噪声抹平增益）互补：一个是阈值条件，一个是剂量-效应。
2. **Plesner et al. 2026（arXiv 2604.07666）**：实证发现 ≤15% 噪声下峰值精度损失 <2pp，且 precision 比 recall 重要——与 Rad 的理论存在张力，引用时须成对呈现。
3. **Spurious Rewards（Shao et al., arXiv 2506.10947）**：随机奖励做 GRPO 也能让 Qwen +21.4pp（机制是放大预训练先验），但高度模型依赖（Llama/OLMo 无此效应）。**对我方是重要边界条件**：锦标赛+进化若带来改进，必须排除「只是在放大底座先验」的解释——跨模型复现（不止 DeepSeek-V4）成为必要实验，而非锦上添花。

## 4. 引用核验结果（15 条，附修正）

全部核验完成，关键修正：

| 条目 | 修正 |
|---|---|
| Shumailov et al. 2024 | Nature 正式版标题是 "AI models collapse when trained on recursively generated data"（631:755-759, DOI 10.1038/s41586-024-07566-y）；「The curse of recursion」只配 arXiv 版，不可混排 |
| α-Rank (Omidshafiei 2019) | Scientific Reports **9:9937**，DOI 10.1038/s41598-019-45619-9（补齐卷期文章号） |
| Zinkevich 2007 (CFR) | 页码以 DBLP 为准 **1729–1736**（流传 905–912 系印刷版本混淆） |
| Balduzzi 2018 | 页码 **3272–3283**（DBLP/official） |
| Windrum 2007 | 篇名实为 "**Alternatives and Prospects**"（非 "Problems and Open Issues"，那是姊妹篇 Fagiolo et al. 2007, Computational Economics 30(3):195-226, DOI 10.1007/s10614-007-9104-4）；**JASSS 该文无 DOI**，流传的 10.18564/jasss.3308 无效 |
| LEAR | 首作者为 **Gurkan, Can**（误写 "Gurkan, A."）；应引 ACM DOI 10.1145/3712255.3734368 而非 CCL PDF |
| Robinson 1951 | J. = **Julia** Robinson，DOI 10.2307/1969530 |
| Rad et al. | 真实条目是 arXiv **2601.04411**；arXiv 2604.07666 是另一篇（Plesner et al.），此前转述张冠李戴 |

其余（Lanctot 2017=1711.00832、Vinyals 2019=10.1038/s41586-019-1724-z、Czarnecki 2020=2010.09679、Gao 2023=2210.10760/PMLR 202:10835、Alemohammad 2024=2307.01850、Minasny 2026=10.3389/fsci.2026.1721295、FunSearch=10.1038/s41586-023-06924-6、EoH=2401.02051/PMLR 235:32201）均核实无误。

**勘误待办（超出本 goal 写权限，仅记录）**：`docs/investigations/medical-ai-to-cds-mapping-2026-07-18.md` 参考文献 #10 "Gurkan, A." 应为 "Gurkan, C."，且应换 ACM DOI——留待用户处理或解除边界时修。

## 5. LQS 分级（标准取自 paper-writing.html Stage 2）

标准：Recency 30% / Citation 25% / Venue 20% / Institution 10% / Acceptance 15%；≥7 must-cite、5–7 conditional、<5 drop。完整 31 条分级表见子代理报告，要点：

- **must-cite（11 条）**：Co-Scientist 9.5、Robin 9.5、TranscriptFormer ~9.2、FunSearch 8.0、Shumailov ~8.0、EoH 7.8、Elemento N&V 7.5、Generative Agents ~7.5、Gao 2023 7.4、EconAgent 7.2 +（跨档）Minasny ~7.0
- **战略例外保留（LQS 对经典有 Recency 偏差，但构成 novelty 论证承重墙）**：Robinson 1951（5.9）、Grimm 2005（6.3）、Axtell 1996（4.3 按分 drop 但概念一手出处）、LEAR、arXiv 2509.21868（5.0，最近邻）、SLALOM（~5.1，直接对话者）、PSRO/Vinyals/Balduzzi/Czarnecki（均 6.8）
- **真 drop**：Claude for Science 产品页（4.7，正文以 web 资源提及即可，不进 bib）、Chen 2026 self-play 综述（3.8，按 Q1 口径只作带 provenance 警告的二手引用）
- **待人工复核**：Halawi et al. 2024 的 NeurIPS 收录状态（档位差 4.8→7.2）；Elemento N&V 的确切 DOI；Nature 选型指南 DOI 独立复现；TranscriptFormer 首作者拼写；2509.21868 接收状态；所有被引数区间入库前 Google Scholar 快照存档。

## 6. 对开题报告设计的影响（累积 Q1+Q2）

1. H3 操作化升级：多锚点 + 留出锚分离（校准/检验不共用）；反转零假设 + bootstrap；匹配粒度预注册；结论措辞限后果分布层。
2. 新增轨迹保真维度：处置行动序列的 gates+DTW 对照，作为第二适应度分量（回应 stopped clock）。
3. H4 标准升级：judge 校准报告须含 **Youden J（>0 带裕度）**+ 逐局误判率（≪10%）+ 跨模型复现（防 Spurious Rewards 式先验放大）。
4.  novelty 论证承重墙明确：calibration-as-fitness（谱系中模式只做筛选）+ LLM 推演作为被验对象。
5. 降级出口多了一个真实 venue：PoliSim@CHI workshop 系列。

## 7. Q3 输入

校验臂选型（疏散/火灾简化模型）现在有了文献约束：校验臂本身也须满足「独立、可解释、参数可得」，且其输出粒度要能接入 gates+DTW 轨迹对照（单路径、单调时间）。
