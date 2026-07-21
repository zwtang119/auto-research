# 评估报告：kimi 推演归因方向（"事后补全 kimi 推演 + 逐条归因为什么对"）的学术价值与顶刊差距

> 日期：2026-07-21 ｜ 执行者：学术价值与顶刊差距评估子代理（编排 Item 2）
> 任务书与预分析：`prompt-exports/oracle-plan-2026-07-21-222835-kimi-6b303c-0b45.md`（task/architecture/relationships/ambiguities 四节；其中 task 节产出路径前缀 `Policysim-v0.2` 为 builder 根目录误判，本报告落位 auto-research）
> 参照范式解剖：`analysis/kimi-reasoning-assessment/reference-paper-anatomy.md`（Towards a Science of Scaling Agent Systems，[arXiv:2512.08296]v2，2025-12-17，arXiv 预印本非同行评审；下文 p.N 为该报告标注的 PDF 物理页码）
> 评估对象（用户提议的新论文方向）：把 kimi（P4，LLM 群体信号，300 分身 × 10 派别，Red Source）的推演过程**事后补全**，逐条分析为什么 kimi 预测的对，并拿 Elo+Poisson（P1）/ Coach（P2）/ CDS 路径枚举（P3）/ 市场（P5）的推演方式做对照，写成类似 "Towards a Science of Scaling Agent Systems" 的对比实验式论文。
> 硬约束继承：不输出投注建议、不报告收益率；封存仓库零读写；`evidence/`、`papers/`、`legacy/`、`state/`、`framework/` 只读；本报告为唯一新增文件，不修改任何既有文件。

---

## ① TL;DR 与裁定结论

**裁定：拒收归档（原形态）。** 四选项（替代主线 / 并入 v2 子研究 / 拒收归档 / 改造后保留为对照素材）中取第三项，理由如下：

1. **该方向的核心动作——"逐条归因为什么 kimi 预测对"——正是 v2 主线显式切割并废弃的叙事。** v2 已用基准率锚点（2026 世界杯为史上首次 FIFA 前四全部进四强，2026-07-20 Wikipedia Green Source 核验）把"前五中四"从技能证据降级为基准率下的常态事件（`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md` §7.1，下文简称 v2:352；§2.6 显式切割，v2:206）。以"为什么对"为标题立项，等于恢复已被废弃数字的叙事地位，与 W6 §8 禁用表述清单的精神直接冲突（`docs/investigations/worldcup-paper-topic-2026-07-19.md` §8，下文简称 W6:377–397）。
2. **该方向在认识论立场上与 v2 主线互斥，无法"并入"。** v2 全部资产建立在 ex-ante 冻结 + OSF 分析协议冻结上（v2 §1.2 障碍 3，v2:97；§5.5，v2:285–287）；新方向本质是 ex-post 重建未记录的推理过程，且"kimi 前五与四强对照"恰在 v2 §5.5 的**已知数字**列表内（v2:287）——对它做"归因式再加工"属于 OSF 冻结语义下的已知结果污染，并入即破坏 v2 的合规结构。
3. **该方向在 Nature 5 判据上 0 PASS / 1 PARTIAL / 4 FAIL，在 F4 7-check 上 0/7 PASS（③④节）**——比已被 DOWNGRADE 的 Direction Y（5/7 FAIL，见 `research/nature-first-class-paper/findings/F4.md:147–155`）更差；它是"data-uniqueness-as-novelty"失败模式的教科书形态：移除"kimi 300 分身独家快照"后，方法学贡献为零。
4. **唯一有方法学价值的零件已被 v2 覆盖，不构成新增子研究。** oracle ambiguities 第 5 条指出的可降级形态（"persona 差异化规则是否产生实质性信息异质"）就是 v2 §3 H4-ii 的既有内容（v2:231），无需另立。

**对"追求极致"的回应**：若用户坚持向该方向投入，第⑦节给出最大化改造方案 M1–M5——但必须诚实说明：改造后的产出物不再是"补全 kimi 推演"，而是一篇以前瞻性 process-tracing 协议为对象的**新论文**，与原方向仅有话题继承关系；且第⑦节末尾列出的五项缺口（kimi 底座版本不可考、赛事已结束、ex-ante 不可回溯、真实 trace 从未存在、生成期污染不可剥离）是**结构性不可修复**的，任何改造都绕不开。

---

## ② 新方向三种技术解读的逐一判定（不回避歧义）

oracle ambiguities 第 1–2 条指出原提议存在两组关键歧义。本评估逐一展开并给判定；未获用户澄清前按最保守解读下判。

### 2.1 "补全推演过程"的三种技术含义

**(a) 模拟 prompt 链路重跑（还原 300 分身的生成过程）——判定：不可行（BLOCKED，非方法选择问题）。**
kimi 底座模型版本不可考：上游仓库 `worldcup-kimi` 不存在（2026-07-20 核查 GitHub 与本地均无，v2 §7.5，v2:368；`docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` Root Cause 3，下文简称 GAP:132）。快照内可复算的是**聚合层**（`kimi_agent_inventory.csv` 300 行按"信心加权归一化"公式复算 21/21 队逐位一致，V-kimi 预审通过，GAP:35），但**生成层**（同 prompt 重跑 300 agent 得同分布）永久不可验证（v2:368）。用任何现有模型重跑 prompt 链路，产出的不是 kimi 的推演，而是另一个模型在 2026-07 的事后分布——研究对象本身不存在。

**(b) thought-reconstruction（用 LLM 读 300 行 inventory + plan.md 派别规则，重建"kimi 当时可能怎么想"）——判定：FAIL，且是 confirmation bias 的最坏形态。**
该做法 = 用一个 LLM 为另一个 LLM 的已知正确输出编造"看起来合理的"推理链。它满足 ex-post rationalization 的全部特征：无 ground truth 可校验（真实 trace 从未被记录）、编码者（重建用 LLM）知道结果、判定规则不可能先于重建文本冻结（重建prompt 本身就含结果信息）。这是⑤节风险 3 与风险 5 的乘积项。oracle 预分析定性为"confirmation-biased 的 worst case"（ambiguities 1），本评估复核确认：快照内 `wc2026_aggregation.json` 只含 raw agent reasons 的聚合摘录（GAP:71–83 的 F3b 扫描证实无更深层过程记录），重建没有任何可锚定的过程证据。

**(c) 人工/规则逆推（从 kimi 输出逆推可能推理链）——判定：无方法学创新，最多是描述性案例素材。**
manual attribution 无预注册 taxonomy、无盲编码、无一致性量化时，产出的是研究者叙事后验，不是证据。参照范式的处理方式是把这类内容降为 illustrative example，结论权重全部放在可自动复核的定量指标上（解剖报告 §4.2，p.13–14 vs p.17）。(c) 可作为 v2 A4 模块（kimi vs 市场对照）内的描述性段落素材，不支撑独立论文。

### 2.2 "对比实验"的两种对照解读

**解读 I：对比推理过程（kimi 的推演 vs P1/P2/P3/P5 的"推演"）——判定：范畴错误（category error），不成立。**
P1 是 Elo+Poisson 公式、P3 是路径空间枚举、P5 是市场清算结果——三者没有"推理过程"可言；P2 的 LLM 介入环节是选首发 XI（v2 §2.2，v2:151），其"推理"与预测概率之间隔着数值 MC 与 Poisson 两层确定性变换。"对比五者的推演方式"在概念上把算法、枚举、市场机制与语言模型推理混为一谈，无法构造同尺度的对照组。

**解读 II：对比概率分布（五者输出概率的同台比较）——判定：与 v2 §3 H4 完全重合，无新意。**
v2 已预注册：赛前截面 Spearman ρ 三档判定（H4-i）、同池重归一 ensemble（H4-iii，在 21 队交集上重归一，v2:231、244）、市场日度演化对照（A4，v2:244）。W6 §1.4 已产出描述性结果（重归一后 kimi 把阿根廷抬至 19.59% vs 市场 8.98%，两处偏离 ex post 方向全对——**仅作描述，不作技能验证**，W6:99–101）。解读 II 若独立成文，等于把 v2 已锁定的一个 sub-question 拆出来重卖一遍，且丢掉了 v2 的协议完整性框架。

**歧义处置声明**：若用户澄清的技术含义不在 (a)(b)(c) 之内（例如"kimi 团队其实留存了完整 trace"），本评估的②③④节须重做；在现有证据快照核查结论下（GAP:15、132），该可能性已被排除。

---

## ③ Nature 5 选题判据逐项评分表

判据定义与判例来源：`research/nature-first-class-paper/REPORT.md` §0（REPORT:16–20）；Direction Y 的 FAIL 判例（REPORT:43–55）。

| 判据 | 评定 | 依据 |
|---|---|---|
| **C1 Mensh 一句话** | **FAIL** | 该方向的一句话只能是"我们事后重建了 kimi 的推演并逐条解释它为什么对"——主语是独家结果，不是方法学机制。判例对照：Direction Y 的"we built a 22-investigation dataset"被判 FAIL（REPORT:50）；"we reconstructed kimi's reasoning" 是同构的 result-as-endpoint。写得出句子，但句子不是方法学主张。 |
| **C2 Murphy 新且引人入胜** | **FAIL** | 必须回答"为什么这不是 known failure mode 的又一次重演"：result-driven process tracing 在 NeurIPS 评审语料中是明确警示对象（F4 Findings[8]："deep concerns, if true, represent fundamental shortcomings that preclude publication"，`research/nature-first-class-paper/findings/F4.md:61–63`）。F2 的 11 篇 2024–2026 adjacent first-class 方法学论文（`research/nature-first-class-paper/findings/F2.md`）无一以"解释单次成功"为贡献；最接近的 hop-wise 归因（MC-Search HAVE，[arXiv:2603.00873]）评估的是**真实记录的**检索链。该方向答不出红线问题。 |
| **C3 Borja 全局语境 + 替代解释** | **FAIL** | 替代解释不仅存在，且已被本项目自己定量锚定：基准率（FIFA 前四首次全部进四强，v2:352）、市场回声（InfoDelphi 框架下 identical-evidence deliberation = herding，[arXiv:2607.01661]；v2 §2.5，v2:177）、Red Source 渗入（Elo bonus 进入 P1 代理，v2:368）、纯运气（n=1 不可排除，W6:99）。该方向无法排除其中任何一个——"逐条归因"的全部结论都与四个替代解释观察等价。 |
| **C4 Doubleday/Konkiel 人类故事 + 跨受众** | **PARTIAL** | 唯一有真实强度的判据："300 个 AI 分身怎么'蒙对'了世界杯"对公众有叙事吸引力，人类故事维度可达。但跨受众的**方法学受益者**为零——相邻子领域研究者从"为已知正确输出编造解释"中拿不到任何可迁移工具（对照：P1+P2 的 crosswalk 可迁移至保险/法律/医学，REPORT:38）。 |
| **C5 Gorsch 可复现** | **FAIL** | 生成层不可复现（v2:368：聚合公式与生成规则虽在，同 prompt 重跑得同分布无法验证）；底座模型版本不可考（GAP:132）；重建对象的内部状态从未被记录。他组无法在任何公开数据上复现"重建"本身。 |

**计数：PASS 0 / PARTIAL 1 / FAIL 4。**

---

## ④ F4 7-check methodological-insight test 逐项判定

7-check 定义：`research/nature-first-class-paper/findings/F4.md:125–135`。

| Check | 评定 | 依据 |
|---|---|---|
| **1 单一方法学句子** | **FAIL** | 核心贡献句是"我们重建并归因了 kimi 的推演过程"——"we built/collected/reconstructed X"句式，非 methodological insight。对照 P1+P2 的 PASS 句式（F4:138：贡献是 crosswalk 方法本身）。 |
| **2 移除数据独有生存** | **FAIL** | 心理移除"kimi 300 分身独家快照"后，论文一无所有——归因方法、对照设计、结论全部附着于该独占数据。这是 Check 2 定义要捕获的精确失败形态（F4:130 引 NeurIPS 2026 E&D "Datasets-as-endpoints don't meet the bar on their own"，F4:5–6）。 |
| **3 评估性主张清晰度** | **FAIL** | 主张"kimi 推演步骤 X 导致预测 Y 命中"需每步独立可验证 + 假设与限制声明（v2 §3.0 Check 3 锚定，v2:218）。Red Source + ex-post + n=1 三件套下，每步推演都不可独立验证（oracle relationships 第 5 条，本评估复核确认）——结论性"逐条归因"等于把假设当结论。 |
| **4 知识缺口** | **FAIL** | 该方向陈述的缺口是"没人重建过 kimi 的推演"——数据缺口句式。文献中真实的相邻缺口（生成式 LLM 预测的 process-level attribution 方法缺失）存在，但本方向**不提供**填补它的方法：它提供的恰恰是该缺口文献已警示要避免的做法（无真值的人工叙事）。缺口存在 ≠ 本方向能填。 |
| **5 跨子领域可迁移** | **FAIL** | "为单一已知正确输出构造事后解释"无可迁移的正向价值；若硬要迁移，迁移的是 bad practice。对照 Check 5 的 PASS 判例（F4:142：crosswalk 迁移至任何 evidence→factor→settlement 管线）。 |
| **6 deep-concern 抗冲击** | **FAIL** | reviewer 一条 deep concern——"n=1、ex-post、Red Source，且归因对象无真值"——即致命；作者不能靠"我们的 kimi 数据独家"反驳（F4 Findings[8]，F4:61–63：deep concern 为真时指认额外 strength 无济于事）。 |
| **7 无 unique 数据可复现** | **FAIL** | kimi 底座不可考（v2:368），重建过程依赖未记录的内部状态；另一团队在公开数据上无法复现该"洞见"——因为洞见本身就是数据的附属品。 |

**计数：PASS 0 / PARTIAL 0 / FAIL 7。** 对照系：P1+P2 7/7 PASS（F4:137–145）；Direction Y 2 PARTIAL + 5 FAIL（F4:147–155）；本方向 0/7，是目前项目内评估过的最低分。

---

## ⑤ 五项认识论风险的结构化论证

每项按"风险表述—证据—消解路径—残余上限"四段展开。结论先行：五项风险各自都有局部消解路径，但**残余上限的交集**决定了该方向的天花板是一节描述性附录，不是一篇论文。

### 5.1 基准率陷阱

- **风险表述**："kimi 前五中四进四强"在本届基准率下不罕见；任何以"命中"为前提的归因都是把常态事件当作待解释异常。
- **证据**：2026 世界杯为史上首次 FIFA 排名前四球队全部进四强（西班牙/阿根廷/法国/英格兰；2026-07-20 Wikipedia Green Source 核验，GAP:32）；kimi 前五实际成绩：西班牙（#1）冠军、阿根廷（#3）亚军、法国（#2）四强、英格兰（#5）第四、葡萄牙（#4）16 强（GAP:33；Red Source、冻结版本 2026-06-05 聚合，v2:352）。"前五中四"的胜利叙事已被 v2 §2.6（v2:206）与 §7.0 合规表显式切割。
- **消解路径**：任何归因分析前置基准率对照——构造"零信息重仓热门"基线（FIFA 排名前 N 直接作为预测），比较 kimi 相对该基线的增量命中；增量不显著则归因对象消失。
- **残余上限**：基准率对照只能**否定**"命中=技能"，永远不能**正面建立**"推演步骤 X 导致命中"。消解后的最好结果是"kimi 相对热门基线无显著增量"或"有增量但不可归因"——两种结果都不支撑原方向的论文主张。

### 5.2 Red Source + 同源污染

- **风险表述**：kimi 信号项目自定级 Red Source"只能参考"，且经 Elo bonus 渗入 P1 代理——"统计模型 vs LLM 群体"的对照在生成期已被污染。
- **证据**：v2 §7.5（v2:368）：kimi 信号经 Elo bonus 渗入 P1 代理（W6 §1.3，W6:76）；PIV 的 source_integrity 字段对 P4 标 red_contaminated（v2 §3 H5，v2:232）；source-policy 仍为 2026-06-11 `draft-for-execution` 版本（GAP:87–96 的 F4 核查）。底座模型版本不可考（v2:368）。
- **消解路径**：v2 既定处置——无 kimi ablation 或将 P1 标注为 contaminated hybrid proxy（W6 G6，W6:276）；PIV 字段显式表达污染。
- **残余上限**：污染发生在 2026-06 的生成期，事后不可剥离；ablation 只能回答"没有 kimi 的 P1 长什么样"，回答不了"kimi 自己为什么对"。归因结论的可信度上限被永久锁定在 Red Source 的"只能参考"定级上。

### 5.3 ex-post 重建

- **风险表述**："补全推演过程"= 事后重建未记录的推理过程，与项目 ex-ante 纪律正面冲突。
- **证据**：v2 §1.2 障碍 3（v2:97）：赛事已结束，预测预注册不可能，改做 OSF 分析协议冻结；§7.3 已知结果污染（v2:360）；§5.5 已知数字列表明确包含"kimi 前五与四强对照"（v2:287）——新方向的归因对象恰是 OSF 语义下的**已知数字再加工**。oracle ambiguities 第 6 条指出：若不先 OSF 冻结推演补全的判定规则，该加工即是污染源。
- **消解路径**：理论上可先把重建的判定规则（taxonomy、编码协议、纳入/排除标准）OSF 冻结，再生成重建文本。
- **残余上限**：冻结规则防的是"看着结果挑口径"，防不了"无真值"——kimi 的真实推理 trace 从未存在，重建文本的每一步都没有可对照的 ground truth。即使流程完全合规，产出物的认识论地位仍是"受控的虚构"，不是证据。

### 5.4 赛事级 n=1

- **风险表述**：单届赛事无统计推断力；"前五中四"单点结果不可做置信区间/假设检验。
- **证据**：v2 §3 分层声明（v2:224）：队伍级 n=48 夺冠概率 = 单届赛事，仅描述；§7.6 单届外部效度（v2:372）；Foresight Arena power analysis 锚点（区分 α*=0.02 约需 350 个已结算预测，v2:277）——本方向的有效样本是 1 届赛事 × 5 个 top 位置，差两个数量级以上。
- **消解路径**：跨赛事/跨任务扩展（见⑦ M3）。
- **残余上限**：对 **kimi 这个对象**而言不可消解——2026 世界杯已结束，kimi 300 分身快照是"文档部分可考的一次性 LLM 群体快照"（GAP:132），同协议跨赛事复现不存在。消解路径只能通过更换研究对象实现，即原方向被消解路径自身取消。

### 5.5 结果驱动的选择性编码

- **风险表述**："逐条归因为什么对"只对命中的条目编码，是 confirmation-biased process tracing——per-item success attribution 总是事后讲得通的循环论证。
- **证据**：oracle relationships 第 5 条；F4 Findings[8]（F4:61–63）；参照范式的对照做法：归因标签须有先验 taxonomy + 操作性判定阈值 + 可靠性量化（κ > 0.80），纯人工逐条归因属弱证据，该范式自身把 process trace 降为 illustrative（解剖报告 §4.2，p.13–14 vs p.17；§7.2 归因底线，解剖报告：153）。
- **消解路径**：预注册编码 taxonomy + 对称编码协议（对预测**错误**的场次/队伍同等密度编码）+ 双人盲编码 + Cohen's κ ≥ 0.80 + 自动可复核指标替代人工判读。
- **残余上限**：对称编码与盲编码只适用于存在真实 trace 的对象；对重建出来的伪 trace 做对称编码，是对虚构文本的二次虚构——编码程序越严格，越暴露底层无真值。该风险与 5.3 复合，是五项风险中唯一一个"消解路径会反噬对象本身"的。

---

## ⑥ 与参照范式的门槛对照：离顶刊多远（核心量化节）

门槛来源：解剖报告 §7.2（`analysis/kimi-reasoning-assessment/reference-paper-anatomy.md:148–153`），从 "Towards a Science of Scaling Agent Systems"（[arXiv:2512.08296]v2）反推的最低门槛。**注意诚实前提**：该参照文自身是 arXiv 预印本，非顶刊接收版——它代表的是"方法学严谨的对照实验范式"的门槛，顶刊要求只会更高不会更低。

### 6.1 门槛对照表

| 门槛维度 | 范式最低要求（锚点） | 本方向当前状态 | 可满足度 | 差距量级 |
|---|---|---|---|---|
| **样本量** | 单 benchmark ≥ 50 instances；总 runs 10⁴ 量级（15,750，p.20）；分析单元（配置）≥ 三位数（N=180，p.10） | 赛事 n=1；队伍层 21 队；300 分身是同一未知模型的同质采样，不构成独立配置 | **不可满足** | 10²–10³ 倍 |
| **对照组** | 强单系统 baseline + 预算匹配（matched token budget，p.19–20）；比较集覆盖机制维度两端的结构化消融（p.8, p.12）；simpler-alternative 对照（p.19 Table 3） | kimi 为一次性快照，无法重跑任何消融臂；P1/P2/P3/P5 与 kimi 无共同输入、无预算概念，对照是解读 II 的概率分布比较（= v2 H4-iii 已有内容） | **不可满足** | 结构性 |
| **统计力** | 主效应报 95% CI 与 p；模型结论须 CV（5-fold, experiment-level holdout）+ bootstrap（n=1,000）+ 残差诊断 + VIF（p.17）；负结果必报 | n=1 无任何检验可行；最近文献锚点：区分 α*=0.02 需 ~350 个已结算预测（v2:277） | **不可满足** | ≥ 2 个数量级 |
| **归因底线** | 先验 taxonomy + 操作性判定阈值 + 可靠性量化 κ > 0.80（该文 validators κ=0.87–0.91，p.12）；纯人工逐条归因属弱证据（解剖报告：153） | 无 taxonomy、无编码协议、无编码者；且归因对象（重建 trace）无真值，κ 在原理上无从计算——一致性只能度量"两个编码者对虚构文本的共识" | **不可满足（最致命）** | 原理级 |
| **时间外验证** | out-of-sample 外推验证并允许报失败（GPT-5.2 验证 4/5 成立、SAS 高估 +49.5% 如实报告，p.32–33） | 赛事已结束，无任何"未来"可留出；ex-ante 不可回溯；唯一可设想的"留出"（对 kimi 未覆盖的 27 队）无预测可验证 | **不可满足** | 结构性 |

### 6.2 三档 venue 的差距清单与补救路径

**NeurIPS 2026 E&D（Datasets & Benchmarks / Evaluations 档）**
- 差距清单：Check 1–7 全 FAIL（④节）；直接触发官方 reviewer guidance "Datasets-as-endpoints don't meet the bar on their own"（F4:5–6）与 ACL/ARR 拒信句式 "mostly a description of the corpus ... little scientific contribution"（F4:86–87）；无 evaluative claim 可挂（F4 Findings[2]，F4:13–14）。
- 补救路径：转化为方法学论文（⑦ M1+M2+M4）；样本量 ≥ 数百个独立结算预测（⑦ M3）；外部 artifact 双人盲复核 κ ≥ 0.6（W6 G7 先例，W6:277）。补救后的论文与原方向的关系 = 话题继承，非同一研究。

**ICML（主会方法学档）**
- 差距清单：无方法学贡献（Check 1 FAIL）；无对照实验设计（解读 I 范畴错误、解读 II 与 v2 重合，②节）；2026 年同题已有 hindsight-guided supervision 的强先例（Jajal et al., [arXiv:2607.09921]，ICML 2026）——该文的事后推理轨迹用于**训练监督**且有市场对照与 24% Brier 改进，反衬本方向把事后推理用于**解释**既无对照又无效应量。
- 补救路径：需要一个可证伪的机制假设（如"信息集消融可隔离 LLM 群体信号的独立信息增量"，⑦ M5）+ 冻结协议下的前瞻性 trace 采集（⑦ M2）+ 多模型多赛事重复（⑦ M3）。工作量为全新研究级别。

**JASA（统计档）**
- 差距清单：统计推断为零——n=1 无 CI、无检验、无 power；对照污染（Red Source 渗入）违反独立性前提；proper scoring 框架下无任何可估参数。
- 补救路径：按 power analysis 设计样本量（≥350 个已结算预测，v2:277 锚点）；预注册判定规则与比较族；Murphy/Yates 分解框架（[arXiv:2605.03310]、[arXiv:2603.05544]）。**对本方向原形态 = 不可达**，因为 n=1 是结构性的（5.4 残余上限）。

**Nature 顶刊档（任务书提及）**：C1–C5 仅 1 项 PARTIAL（③节），无讨论必要；Nature 级要求跨领域重大意义 + 无可辩驳证据链，本方向两项皆无。

---

## ⑦ "追求极致"章节：最大化改造方案（若用户坚持投入）

前提声明：以下改造逐条注明修复哪个 FAIL/PARTIAL 项；改造 M2 起，研究对象实际已更换，产出物是**新论文**而非原方向的修复版。本节同时诚实标注不可修复项。

### 7.1 五条改造

**M1. 把研究对象从"为什么对"改为可证伪的机制问题。**
将问题重写为："persona 差异化规则是否在 LLM 群体信号中产生实质性信息异质（asymmetric evidence 候选），还是训练语料市场共识的回声？"——这是 InfoDelphi 框架（[arXiv:2607.01661]）的可证伪问题，且 v2 §3 H4-ii 已预留位置（v2:231）。
*修复：C3（替代解释变为研究对象本身）、Check 4（缺口变为方法学缺口）。*
*注意：该问题 v2 已有，M1 单独不构成新论文，只构成 H4-ii 的深化。*

**M2. 把 ex-post 重建改为带冻结协议的前瞻性 process-tracing。**
放弃 kimi（对象不可考），自建可考底座的 LLM 群体：开源模型（版本固定）、300 分身 prompt 链路全部 git 冻结 + prompt hash 真实化、**全程记录真实 reasoning trace**、对**未来**赛事/任务做 ex-ante 预测。归因分析的对象从"重建的伪 trace"变为"真实记录的 trace"，参照 MC-Search HAVE 的 hop-wise 归因范式（[arXiv:2603.00873]）与 POMDP 组件分解（[arXiv:2606.17383]）。
*修复：C5、Check 7、风险 5.3（ex-post→ex-ante）。*
*成本：完整新实验；且需等待新的结算周期。*

**M3. 把样本量从 n=1 赛事扩展为跨赛事/跨任务设计。**
在持续结算的任务流上（ForecastBench / Prophet Arena 式题目流，或跨 2018/2022/2026 多届赛事的 information-barrier 回测，先例 Rezaei & Samadi [arXiv:2606.24171]）运行 M2 的群体协议，积累 ≥350 个已结算预测（Foresight Arena power 锚点，v2:277），使归因结论可做统计检验与时间外留出验证。
*修复：风险 5.4（n=1）、⑥表统计力行、JASA 档差距、时间外验证门槛。*

**M4. 把归因操作化为可自动复核指标 + 预注册 taxonomy + 多编码者 κ。**
按参照范式的归因底线（解剖报告：153）执行：(i) 成功/失败模式的先验 taxonomy 在分析前 OSF 冻结；(ii) 归因标签操作化为可从 trace 自动计算的特征（信息增益、证据-结论对齐度、token-overlap 结构——参照范式 p.12–13 的中介指标设计）；(iii) 对称编码协议：命中与未命中条目同等密度编码；(iv) 双人盲编码 Cohen's κ ≥ 0.80，达不到则归因主张降级为描述。
*修复：风险 5.5、⑥表归因底线行（最致命项）、Check 3。*

**M5. 把对照设计从"对比推理过程"重构为信息集消融。**
控制输入信息集（含/不含市场快照、含/不含 Elo 表、含/不含新闻检索），以结构化消融隔离 herding vs 独立信息——这把解读 I 的范畴错误转化为 InfoDelphi 式可证伪实验，对照组是同一群体的不同信息臂（预算匹配、同底座），而非五个异质预测器。
*修复：C2（"新且引人入胜"= 信息集消融作为群体信号审计方法）、Check 1（方法学句子："我们以信息集消融隔离 LLM 群体信号相对市场共识的独立信息增量"）、②节解读 I 的范畴错误。*

### 7.2 结构性不可修复缺口（任何改造都绕不开）

1. **2026 世界杯已结束**：ex-ante 不可回溯；该届赛事上任何"前瞻性"设计都不可能补做。
2. **kimi 底座模型版本不可考**：上游仓库不存在（2026-07-20 核查，v2:368；GAP:132）；任何"重跑 kimi"都不是 kimi。
3. **kimi 真实推理 trace 从未被记录**："补全"的对象在本体论上不存在——这不是方法缺口，是对象缺口。
4. **生成期污染不可剥离**：Red Source 定级 + Elo bonus 渗入发生在 2026-06，事后任何 ablation 都无法还原未污染的反事实（5.2 残余上限）。
5. **kimi 300 分身快照的一次性**：同协议跨赛事复现不存在（GAP:132 定性"一次性 LLM 群体快照"），M3 的跨赛事扩展只能更换对象实现。

### 7.3 改造后的现实定位

M1–M5 全部执行后的论文，其一句话是"以冻结协议前瞻性 process-tracing + 信息集消融，审计 LLM 群体信号相对市场共识的独立信息增量"——这与原方向（"解释 kimi 为什么对"）的关系是：**原方向是该论文的一个被取消的动机注脚**。现实 venue 上限参照 W6 §5 的诚实估值口径：全新前瞻性数据 + 外部复核通过前，workshop 档；通过后可望 evaluation 类主会/workshop，NeurIPS E&D 为 stretch。预计新增工作量：一个完整实验周期（协议设计 + 采集 + 等待结算 + 分析），量级为月。

---

## ⑧ 与 v2 关系审查与裁定理由

### 8.1 三维度互斥确认（继承 oracle relationships 并复核落锚）

| 维度 | v2 主线 | 新方向 | 锚点 |
|---|---|---|---|
| 认识论立场 | ex-ante 冻结 + OSF 分析协议冻结 | ex-post 重建未记录过程 | v2:97, 285–287 |
| 评估对象 | 协议完整性（PIV 为一等字段） | 预测者"心智"（逐条归因） | v2:232（H5）vs 本报告④ |
| 方法 | reconciliation（同台结算对账） | attribution（单对象事后解释） | v2:16（摘要）vs ②节 |

三维互斥 ⇒ "并入 v2 子研究"不可行：并入会把 ex-post 产物引入 OSF 冻结后的分析流，直接违反 v2 §7.3 已知结果污染对策（v2:360）与 §5.5 已知/未知数字边界（kimi 前五对照在已知列表内，v2:287）。

### 8.2 套用 W6 §6.2 三段裁定范式

W6 对 G3 outline 的裁定范式为"吸收零件 / 论文并行 / 旧核心数字废弃"（W6:300–307）。对新方向套用：

- **吸收零件**：可吸收的仅两件——(i) deviation-direction signature 框架可用于描述 kimi 相对市场的偏差方向（v2 §3 H2 框架借用，v2:229）；(ii) kimi 与市场两处偏离方向 ex post 全对的描述性观察，已作为 H4-iii 的动机写入 v2（v2:231）。两者**均已在 v2 内**，无新零件可吸收。
- **论文并行**：ex-post 重建与 v2 ex-ante 主线认识论互斥（8.1），若强行并行成独立论文，会与 v2 争夺同一批证据资产（kimi 21 队信号、市场快照）且互相削弱——v2 的纪律边界（"技能验证留待续篇"，v2 §9.3 诚实上限，v2:408）会被并行论文的归因主张架空。
- **旧核心数字废弃**：项目首页"前五中四"已显式废弃（v2:206、352；W6 §8.2 禁用表述，W6:386–397）。新方向以"为什么 kimi 预测对"为标题 = 把已废弃数字重新立为叙事中心——这是对既有裁定的逆行，构成拒收的独立充分理由。

### 8.3 裁定理由汇总

1. 评分面：Nature 5 判据 0 PASS / 1 PARTIAL / 4 FAIL；F4 7-check 0/7 PASS（③④）。
2. 门槛面：五条范式最低门槛全部不可满足，其中归因底线（无真值 → κ 原理上不可计算）与时间外验证（赛事已结束）为结构性缺席（⑥）。
3. 关系面：与 v2 三维互斥、无新零件可吸收、以废弃数字为标题（8.1–8.2）。
4. 风险面：五项认识论风险的残余上限交集 = 描述性附录（⑤）。
5. 唯一可行保留形态（v2 H4-ii 子分析）已存在于 v2，不构成新增（①理由 4）。

**裁定：拒收归档。** 归档口径：本报告 + oracle 导出文件即为归档记录；若未来 M2–M5 新研究启动，原方向作为"动机与教训"在该研究的 related work 中以一节引用。

### 8.4 改造后保留时的降级路径（备查）

若用户不接受拒收、选择最小成本保留：降级路径为把新方向压缩为 v2 A4 模块（kimi vs 市场对照）内的一个**描述性段落**——"kimi 派别规则结构与偏差方向的描述性观察"，措辞限描述、禁归因动词（"导致""因为"），标注 Red Source + n=1 + 基准率三重限定，且不产生任何独立论文资产。该段落的方法学功能已由 v2 H4-ii 覆盖（v2:231），降级后新增信息量 ≈ 0——这正是本评估不推荐该路径的原因。

---

## ⑨ 引用与已知边界声明（OSF-style）

### 9.1 引用锚点清单

**仓库内文件**（path:line；证据快照内文件未直接引用原文，仅经二手核查报告转引并注明）：
- v2 开题：`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`——§7.1 基准率论证（:352）、§7.5 kimi 残余不可考（:368）、§3 H4（:231）、§5.5 OSF 与已知数字（:285–287）、§3 分层声明（:224）、§5.3 power 锚点（:277）、§2.6 切割声明（:206）、§9.3 诚实上限（:408）。
- W6 终裁：`docs/investigations/worldcup-paper-topic-2026-07-19.md`——§6.2 三段范式（:300–307）、§8 禁用表述（:377–397）、§1.4 描述性发现（:99–101）、§5 G6/G7 gate（:276–277）。
- 缺口分析：`docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md`——基准率锚点（:32）、kimi 前五成绩（:33）、H-b 21/21 复算（:35）、kimi 一次性快照定性（:132）、F3b 扫描（:71–83）。
- 判据库：`research/nature-first-class-paper/REPORT.md`（C1–C5 定义 :16–20；Direction Y 判例 :43–55）；`findings/F4.md`（7-check :125–135；Findings[1] :5–6；Findings[8] :61–63）；`findings/F2.md`（11 范式库）；`findings/F3.md`（组合术语零命中先例）。
- 参照解剖：`analysis/kimi-reasoning-assessment/reference-paper-anatomy.md`——最低门槛（:148–153）、κ 0.87–0.91（:66）、15,750 runs（:53）、N=180（:52）、out-of-sample（:106）、trace illustrative（:74, 89–90）。

**外部文献**（arXiv 简注）：[arXiv:2512.08296]（参照范式，预印本）；[arXiv:2607.01661]（InfoDelphi）；[arXiv:2603.00873]（MC-Search HAVE）；[arXiv:2606.17383]（POMDP 组件分解）；[arXiv:2607.09921]（hindsight-guided supervision，ICML 2026）；[arXiv:2605.03310]（Murphy 分解实证）；[arXiv:2603.05544]（Yates 重排）；[arXiv:2606.24171]（跨届 information-barrier 回测先例）；[arXiv:2605.00420]（Foresight Arena power analysis）。

**事实性声明来源分级**：基准率与赛果 = Green Source（Wikipedia，2026-07-20 核验，经 GAP 转引）；kimi 相关数字 = Red Source，冻结版本 2026-06-05 聚合（v2:254 口径）；范式门槛数字 = 参照解剖报告的 PDF 页码转引（Green-to-report）；本报告全部判断性结论 = 评估者意见，非事实声明。

### 9.2 本评估自身的局限

1. **未读参照论文原文 PDF**：对 "Towards a Science of Scaling Agent Systems" 的全部认知来自 Item 1 解剖报告（其自身声明：每实例重复次数未明确、预注册/盲标/多编码者程序 PDF 中未找到、该文仅为 arXiv v2 非同行评审——解剖报告：159–162）。若原文与解剖报告有出入，⑥节门槛表须复核。
2. **新方向的 novelty 判断非系统检索**：②④节对"生成式 LLM 预测 process-attribution 文献"的判断依赖 oracle 预分析 + F2/F3 的定向核查，未做独立系统文献检索；若存在 2026 年"ex-post reasoning reconstruction as method"的正面先例，C2 判定可能需调整（但 n=1 + 无真值问题不受影响）。
3. **NeurIPS 2026 E&D 判定依据转引**：reviewer guidelines 引文经 F4 收录（F4:5–14），本评估未直接访问 neurips.cc 原文。
4. **歧义未澄清**：②节的三种技术解读判定基于最保守假设（ambiguities 1–2 未获用户澄清）；若用户澄清的含义超出 (a)(b)(c)，相关判定须重做。
5. **裁定边界**：本报告做方法学判断，不替用户做资源分配决议（继承项目 D17 规则精神，REPORT:167–169）；⑦节改造方案是"若坚持投入"的条件性回答，不是 proceed 推荐。
6. **数字复核口径**：本报告未重跑任何复算（V-kimi 21/21、基准率核验等均转引 GAP/v2 的已核验结论并注明日期）；按项目验证纪律，这些转引结论的原始核验记录分别位于 GAP:35、GAP:32。
