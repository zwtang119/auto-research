# 双篇路线图 v1.3 文献综合与新发现审查

> 日期：2026-07-22
> 执行者：design agent
> 上游：路线图 `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md` v1.3
> 输入：ima-decision-under-uncertainty/ 4 篇（AMW 主引 / Dunning 背景 / BHS 背景 / Tychastic 驳回）+ v1.2 文献扫描 `analysis/roadmap-v12-scan/refscan.md` + 范式解剖 `analysis/kimi-reasoning-assessment/reference-paper-anatomy.md` + 开题 v2 `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`
> 引用纪律：跨域借鉴须声明 + 受条令启发的设计类比须明示（沿用 CLAUDE.md）

---

## 1. 路线图新增方法论部分的价值评估（用户问题 1）

逐节判定：是否值得 (a) **作为论文方法论章节的方法论模板被论文自身引用** / (b) **作为项目级 SOP 沉淀到 `framework/` 跨论文复用** / (c) 不值得，仅流程细节不入引文。

### 1.1 §4.2 AMW 充分统计量两段式重构

- **(a)** **值得入引文。** 路线图已将"Stage 1 估 V(x)"与"Stage 2 验证最优聚合/披露策略"作为 Paper B 方法论主干；该两段式可直接作为 Paper B 方法学章节的子标题。
  - 引用规范：必须在 Paper B 出现"两段式"的段落同时脚注 AMW (Agarwal, Moehring, Wolitzky 2025) + 显式声明"跨域借鉴（human-AI 协作 → LLM 群体，类比依据是充分统计量结构而非结论本身）"——这与 refscan §B1 的判定一致。
  - 不引 *论点*（如"FDA 最优"），只引 *方法论结构*（"先估 V、再设计最优策略、最后实测验证"）。
- **(b)** **值得沉淀 SOP。** "先估充分统计量再设计策略"是任何"设计空间过大不靠穷举"的问题通用方法学骨架。建议沉淀为 `framework/method-patterns/sufficient-statistic-two-stage.md`，标记触发条件"当设计空间 ≥ 10×10 factorial 且主效应先验难以穷举时"。

### 1.2 §4.6 B0.5 pilot 闸门（trace 完整率 100% / 解析成功率 ≥98% / 结算时延 ≤72h / 成本对账 ≤50% 偏差）

- **(a)** **作为子表入引文，但不作为方法论重心。** 这是工程 gate 而非方法学模板；可在论文 Methods § 的"Pipeline validation"小节作为 1 段 + 1 表引用（与 v2 §5.3 的 V-kimi/V-88a/V-72 验证任务同构）。
- **(b)** **值得沉淀 SOP。** 四项阈值的"go/no-go 一票否决"是任何 *前瞻预测系统* 启动前的通用门槛。建议沉淀为 `framework/sop/pilot-go-nogo-thresholds.md`，触发条件"任何带 trace + 实时结算的实验装置"。

### 1.3 §4.7 成本估算（调用量公式 + 量级区间 10⁴–10⁵ / 10²–10³ $ + 降级规则）

- **(a)** **作为方法学子节入引文（但被严重低估）。** 当前路线图把成本写成"内部估算"；实际上"成本可控 + 降级规则"是任何 scaled evaluation 的方法论贡献——与 Benchmark 设计哲学同构（Scaling Agent Systems 范式解剖 §7.1 #3 "Matched token budget" 即同一精神的预演）。建议：把成本模型升级为 Paper B Methods 中的"Cognitive-economic budget" 子节，呼应范式解剖结论条 3。
- **(b)** **值得沉淀 SOP。** "调用量公式 × 量级区间 × 降级规则三件套"是任何 API-economical 实验的通用骨架。建议沉淀为 `framework/sop/api-cost-budget.md`。

### 1.4 §4.8 运行期监控（解析漂移 / 结算延迟 / API 版本变更 → 三类静默失败的校验与处置）

- **(a)** **作为方法学子节入引文（且被低估）。** "静默失败校验"是任何长时段跑动的实验都有的方法论负担——路线图给了"三类"清单值得在 Paper B Methods 中作为 "Runtime Integrity Checks" 子节引用，呼应范式解剖 §4.2 "归因防护"。
- **(b)** **值得沉淀 SOP。** "fail-loud 三类触发器"是通用模式——解析漂移（任何带 schema 解析的管线）、结算延迟（任何带外部 ground-truth 的实验）、API 版本变更（任何依赖第三方服务的实验）。建议沉淀为 `framework/sop/runtime-integrity-checks.md`。

### 1.5 §10 参考文献（主引 AMW / 背景 Dunning、BHS / 沿用 4 篇 arXiv / 驳回 Tychastic 留痕）

- **(a)** **作为论文 References 节直接引用。** 这是论文自身的引用，不存在"是否值得"问题；唯一质量门槛是"主引标 venue / 背景标引用目的 / 驳回留痕但不入论文 References（仅留档）"。
- **(b)** **值得沉淀 SOP。** 路线图 §10 的"主引 / 背景 / 沿用 / 驳回"四级分类 + 驳回留痕不引，是高质量的文献筛选纪律。建议沉淀为 `framework/sop/reference-tier-classification.md`（4 类定义 + 选用规则 + 驳回不留引的实践）。

**§4.1–§4.5 既有部分**：§4.1 的 herding 双层指标 + AMW/Dunning 信念更新权重机制注记已是方法论内容（入引文）；§4.3 的两段式 power 账与§4.4 归因操作化（M4）与§4.5 期末考规格已是方法学内容（入引文）；三段式差异化论证（4 范式）已立，可入引文。

**汇总**：

| 路线图节点 | (a) 论文入引 | (b) SOP 沉淀 | 触发的 SOP 文件 |
|---|:---:|:---:|---|
| §4.2 AMW 两段式 | ✅ 方法学子节 | ✅ | `method-patterns/sufficient-statistic-two-stage.md` |
| §4.6 B0.5 闸门 | ⚠️ 辅助表 | ✅ | `sop/pilot-go-nogo-thresholds.md` |
| §4.7 成本估算 | ✅ 子节（**建议升级**） | ✅ | `sop/api-cost-budget.md` |
| §4.8 运行期监控 | ✅ 子节（**建议升级**） | ✅ | `sop/runtime-integrity-checks.md` |
| §10 文献分级 | n/a（论文 References） | ✅ | `sop/reference-tier-classification.md` |
| §4.1–§4.5 既有 | ✅ | ⚠️ 可下沉 | (不新设) |

---

## 2. ima 4 篇参考文献评估（用户问题 2）

### 2.1 主引：AMW（Designing Human-AI Collaboration）

**当前路线图判定**：主引。**复核判定**：**主引——但需修订"主引"的内涵**。

**复核理由**：
- AMW 的核心贡献是**方法论结构**（sufficient statistic + 两阶段 + Assumption 2.1/2.2 + V(x) 充分性的检验程序），这是路线图 §4.2 真正在借鉴的部分。**这一借鉴是结构上的、跨域合法的**——充分统计量方法不依赖于具体的决策者是 human 还是 LLM。
- AMW 的 *结论*（under-response 由 own-signal overconfidence 驱动、选择性自动化 + 完全披露最优、协作增量可忽略）则是经验发现，跨域借鉴时要小心：人是 human + AI 是 calibrated classifier；LLM 是 calibrated classifier + 提供自己的 signal——两个语境中的"own signal"同构性不显然。
- **结论**: AMW 适合作为 "方法学主引 + 候选机制外部证据"——但摘要级结论应仅作"启发证据"引用，不作"对 LLM 群体的先验"。

**复用方式建议**：
1. Paper B Methods §2.1 写"Sufficient Statistic Estimand"，明确标注"借鉴 AMW 的 estimand 设计 (Agarwal, Moehring, Wolitzky 2025)，跨域对象为 LLM 群体而非 human-AI 协作"。
2. Paper B Results § 中如出现对 AMW 的发现级别的呼应（如"群体对高自信案例 under-respond"），须重复标注跨域借鉴，并说明 LLM 上的相似现象只是"结构同源、机制未必同"。
3. **研究纪律警示**: AMW 论文为 working paper（路线图 §10 已标记"unknown，引用前须外部核实是否已有期刊版"）。引用前应再核实一次：截至 2026-07-22 NBER 是否已发表、是否有正式期刊接收证明；如果仍是 working paper，"主引"的承重地位需要在 Paper B Discussion 中加一段"局限性：方法学主引源尚为 working paper"。

### 2.2 背景：Dunning（CMU 博士论文）

**当前路线图判定**：背景（仅作 reliance 操作化先例 + own-signal overconfidence 互证）。**复核判定**：**建议升级到"Stage 2 候选机制主引之一"**（**Mechanism Co-Lead Citation**）。

**复核理由**：
- Dunning 与 AMW 在 *机制层面* 独立互证"self-confidence → 拒绝 AI"：
  - AMW：在线 fact-checking 实验，Grether 系数 own signal = 0.8（自己估计）、AI 信号 = 2.3（接近 Bayesian 1.0，Agarwal et al. 2023 同样模型下 own = 0.3 / AI = 1.1）——overconfidence 在自身信号上显著（§6.3 "Overconfidence or AI Neglect?"，原文 p.728 起）。
  - Dunning：Connect Four 实验，自报高 self-confidence 者"拒绝 AI 建议更多、获胜信心更高、胜率反而略低"（原文 Conclusion，p.3657-3707）。
  - 这是**两层独立证据**：AMW 是准实验（人为操纵 AI 评估 x、估计信念更新函数）；Dunning 是行为实验（observational、操纵 AI 可靠性 / 显示形式 / 出场顺序）。互证强度高。
- 路线图 §4.1 末尾已为"persona overconfidence → herding"加注记（Stage 2 候选机制假设），但定位为"跨域借用须声明"的"注记"——权重不够。

**复用方式建议**：
- 把 Dunning 从"背景注脚"升级为 **Mechanism Co-Lead**：Paper B Discussion 段单设一节"Asymmetric Overconfidence in LLM Populations: Hypothesis from Cross-Domain Evidence"，引 AMW + Dunning 两条主引 + 路线图 §4.1 末尾注记作为待验证机制。该机制若 Stage 2 验证为真，是 Paper B 相对现有 LLM-ensemble 文献（如 Schoenegger et al. 2024）的理论增量。
- 路线图 §10 的分类应由"背景"改为"机制共主引 (mechanism co-lead)"。引用规范同 AMW + 显式标注 non-peer-reviewed dissertation + 显式标注"反向：Connect Four 博弈而非预测任务"。

### 2.3 背景：BHS（Strategy Beyond the Hockey Stick）

**当前路线图判定**：背景（实践者书籍，McKinsey 数据"非公开可复算"）。**复核判定**：**同意背景判定；但"非公开可复算"的措辞可以微调**。

**复核理由**：
- BHS 的数据治理层级明显被路线图错误归并为一类"非公开"。实际是**三档**：
  1. **完全公开**: 8% / 59% 基线率、Power Curve 形状、"10 个杠杆解释 80%+ 迁移"等 top-line 数字 → 来自公开书籍 + McKinsey 文章 + 后续学术引用。
  2. **可校验但需付费/会员**: 单公司的经济利润序列、移动分类 → 来自 S&P Capital IQ 替代变量 + McKinsey Corporate Performance Analytics 衍生模型（公司匿名化后可在 McKinsey 衍生数据库查询）。
  3. **严格私有**: 原始企业数据 + 40 变量的具体取值 + 单笔并购行动数据 → 仅 McKinsey 内部。
- 路线图当前措辞"非公开可复算"过于宽泛，把 (1) 也挡掉了。修正措辞：
  - 引用 8% / Power Curve 时标"基于 McKinsey Corporate Performance Analytics 2000-2014 样本 (n=2,393)，其衍生基线率已公开"
  - 不引用 (3) 类微观数据
- 此外，BHS 的 *论点*（outside view vs inside view、自信心反相关于准确性）与 AMW 的 own-signal overconfidence 论点同向——构成本路线图"overconfidence 是普遍现象"的两源证据。

**复用方式建议**：
- Paper A Discussion 段"Reflexivity and Underconfidence"（或类似位置）可引 BHS 作为"过拟合于内部视角的风险"参考——但仅作"实践者文献的同向印证"，不作承重学术引文。
- 路线图 §10 的"非公开可复算"措辞应修订为"其 top-line 数字（如 8% 移动率）可引用并标注 McKinsey 数据库；不可引单项公司归因"。
- 新增洞察（routes 范畴）：BHS 的 "mobility probability 的层级性"（top→top 59% / middle→top 8%）是 *先验基线* 的另一个来源——可在 Paper A 的"结构性偏差刻度"中提供一个"先验移动概率"的 reference-class 论证框架（取代"用市场作基准"这一较窄的来源）。

### 2.4 驳回：Tychastic（NPS 技术报告）

**当前路线图判定**：驳回（军事 C2 / 网络拥塞控制域不相交）。**复核判定**：**同意驳回，确认理由成立**。

**复核理由**：
- Tychastic 的 *域*（DOD ISR-T 网络拥塞控制）、*方法*（动态优化 + tychastic 轨迹优化）、*文献谱系*（控制论 / Lebesgue-Stieltjes 积分）三个维度都与双篇**完全不相交**。任何一个维度都足以否决。
- 唯一启发价值：原文 §6 案例显示"最小化平均拥塞反而放大方差（tr(C) 506.56→597.47），需对协方差迹加路径约束（tr(C)→72.08）"——这是"mean-optimal ≠ robust-optimal"的设计哲学例证。
- 该哲学启发已被路线图 §4.3 隐性吸收（"除均值外报告跨条件方差"），但**原文不引**——驳回理由成立。

**复用方式建议**：
- 不入 Paper A / Paper B References。
- 仅在路线图 §4.3 / §4.8 的"设计哲学注记"中可点名"受 tychastic-style mean-vs-robust 启发"——但 *不引原文*，与路线图 §4.1 的 MCDP-1 边注同款（"受条令启发的设计类比"明示）。
- 路线图 §10 "驳回记录"条目保留——构成"我们看过并评估过"的诚实留痕，反审查时不会被打"为什么没看 Tychastic"。

### 2.5 判定表汇总

| 文献 | 路线图判定 | 复核判定 | 关键修订 |
|---|---|---|---|
| AMW | 主引 | 主引（结构方法学） + 候选机制证据 | 引用前再核实 venue；区分结构借鉴与结论借鉴 |
| Dunning | 背景 | **Mechanism Co-Lead**（建议升级） | 由"背景注脚"升为 Paper B Discussion 段的方法机制共主引 |
| BHS | 背景（非公开可复算） | 背景（"非公开可复算"措辞需分层） | 把数据可获取性分 3 档描述；top-line 数字可引并标注 |
| Tychastic | 驳回 | 驳回（确认） | 保留驳回留痕，类比不引 |

---

## 3. 颠覆性发现（用户问题 4）

逐条检视 4 篇精读 + 路线图 v1.3 + 开题 v2 后，是否有**颠覆**路线图当前方向的发现。

### 3.1 颠覆点（最有力）：AMW 的"协作增量可忽略"对 Paper B 当前旋钮设计的先验攻击

**事实引用**：AMW 在 fact-checking 实验中，预测显示 FDA（Full Disclosure + Automation）= 75.1% vs NDA（No Disclosure + Automation）= 74.8%，实测 = 74.9% vs 74.7%——差 0.2 个百分点（p=0.44，不显著；原文 Table 2, p.557-569）。AMW 摘要明确称："although automation is valuable, the additional benefit from assisting humans with AI predictions is negligible."

**对路线图 v1.3 的影响**：当前 Paper B 设计了两个聚合旋钮——多数投票（探索性）、辩论收敛（探索性）——这都是 *协作辅助* 模式（multi-agent 同时存在 + 意见交互）。**AMW 的先验**（跨域借鉴须声明）是：协作辅助相对选择性自动化的边际增量极小。**当前旋钮设计在先验上注定难以显著**——辩论收敛很可能沦为"NDA 等价"。

**修订建议**：
- 把"选择性路由"从探索性臂 **扶正为确认性主效应的 baseline**（路线图当前 §4.2 表中已列选择性路由探索性臂，建议升级为确认性）。
- 多数投票/加权/辩论收敛保留为探索性臂，但**预注册一个"协作辅助等价于 NDA"的零假设检验**——若 Stage 2 不能拒绝 H₀: "多 agent 协作相对选择性路由无增量"，即作为一个负结果发表（这本身是贡献；herding 判定即贡献，对接 InfoDelphi 框架）。
- 选择性路由按置信度把任务路由给最优子群体，其余直接采纳——这正是路线图 §4.2 注记中 AMW 的"selective automation"精神的 LLM 类比。
- 跨域借鉴声明：必须在 Paper B Methods 显式注明该旋钮升级以 AMW 的协作增量发现为先验（"受 AMW 2025 选择性自动化发现启发"）。

### 3.2 颠覆点（次有力）：V(x) 的 LLM 群体版替代 2 旋钮 factorial 的"更优雅框架"未被 v1.3 完全吸收

**事实引用**：AMW 的核心方法论概念 V(x) — "正确率作为 AI 评估 x 的函数"——是被充分统计量假设（Assumption 1, 原文 p.147-167）支撑的一个 *scalar estimator*，可在 moderate n 的开发集上非参数估计。论文 §4.2 Stage 1 仅估计这一函数，§4.3 由 V 的凸性/形状推导出 *最优* 自动化/披露/聚合策略，§5.2 Stage 2 验证预测与实测差 < 1.6pp。

**对路线图 v1.3 的影响**：v1.3 仅把 AMW 两段式作为"Stage 1 估 V(x) + Stage 2 验证最优策略"的主干（§4.2 重构），但**保留了"规模 3/10/30 × 信息集"2 个确认性旋钮**——这是把 AMW 的两段式当成"减少 factorial"的手法，未把它当成"取代旋钮概念"的替代品。

**修订建议**：
- 在 Stage 1 内部增设一个 **V_LLM(x) 估计**作为核心产物（不在 Stage 1 末做策略决策，仅估计曲线形态、检验 V 在 LLM 群体上是否仍为凸 / 是否依赖披露策略 = AMW Assumption 2.1/2.2 的 LLM 类比验证）。
- 仅在 V_LLM(x) 估计稳定后，Stage 2 才进入"规模 × 信息集"消融——这样 factorial 的目的是 *验证* 而非"主线"。
- 这一改动实质上是把路线图 §4.2 的 *Stage 1 描述性*与 *Stage 2 确认性*之间插入一个 *Stage 1.5 充分性检验*。门槛低但意义大：若 V_LLM(x) 在 LLM 上不满足 Assumption 2.1/2.2，则 Stage 2 的任何最优策略验证都失去方法学合法性。

### 3.3 颠覆点（结构性挑战）：AMW 的"agent skill dominates architecture"对路线图"≥2 模型家族"判定的强化

**事实引用**：AMW 摘要：AI 能力主导团队表现（来源 AMW §6.4 + 路线图 §6 上下文）；Dunning 摘要：AI reliability 是团队表现最大决定因素（Dunning 摘要，原文 p.91-101）；Scaling Agent Systems 范式解剖 §7.1 #2 显示其 mixed-effects 模型 architecture 主效应远小于 capability 主效应（这是 Kim et al. 2025 表 3 / 表 4 的核心发现）。

**对路线图 v1.3 的影响**：路线图 §4.2 把"≥2 模型家族"作为 *复现性注脚* + *底座版本要求*，**但**没有把它作为析因实验的 *显式区组因子*。

**修订建议**：
- "≥2 模型家族"应升级为"≥2 模型家族，每个家族写为显式区组 (blocking factor)"——而不是单纯"换底座看复现性"。
- 这一点对 Stage 1 的 V_LLM(x) 估计与 Stage 2 的策略验证都成立——不同模型家族的 V_LLM(x) 形态可能截然不同，单家族结果不具推广性。
- **风险**: 加入"模型家族"作为显式因子 = 旋钮数从 2 上升到 3——回到 v1.1 的 36 格问题。**化解**: 仅用 *block structure*（模型家族作为区组而非可操纵旋钮），估计时分家族估计 + pool 估计两个报告，power 损失由 v1.3 的两段式集中 power 抵消。

### 3.4 非颠覆性启发（记录但不升级）

- **AMW Stoplight (K=3) ≈ FDNA**: 这是一个 *已知内插值*，对 Paper B 启发"按 LLM 群体共识度分桶披露"作信息集旋钮的子水平——但这已被路线图 §4.2 末尾"AMW 完全披露不劣于部分披露 → 信息集臂可加完整快照 vs 加噪/延迟子水平"的注记部分吸收，**不构成颠覆**，仅加固。
- **Dunning "hard opponent → uncritical reliance"**：显示环境极端性会破坏自我监控——对 Paper B 的 "任务难度切换" 旋钮有启发（v1.3 未覆盖，可作 §3 的备选论述），但属低优先级启发。
- **BHS "more data, more confident, more dangerous"**：与 AMW own-signal overconfidence + 路线图 §3.2 "前五中四不可区分" 三联同向——这是 *多源印证* 而非 *新发现*。
- **Tychastic "mean-optimal ≠ robust-optimal"**：作为路线图 §4.3 隐性吸收的哲学启发（"除均值外报告跨条件方差"），已在 refscan §C1-5 提过——不重复造轮。

### 3.5 是否有颠覆？一句话回答

**有——§3.1 与 §3.2 是颠覆路线图当前方向的发现**：
- §3.1 颠覆"协作辅助旋钮"的先验合法性；
- §3.2 颠覆"AMW 两段式只是减少 factorial 的工具"的角色定位，应当升级为"取代旋钮概念的方法学主干"。

修订建议详 §3.1 / §3.2。

---

## 4. 候选新猜想（用户问题 4 续，作为 H4-ii 之后接续假设）

每条猜想含：一句话陈述 + 可证伪化操作定义 + 嵌入路线图方式。

### 4.1 H5 — "Stoplight (K=3) 在 LLM 群体中亦近似最优"

- **一句话陈述**：把 LLM 群体按"群体内部 token-overlap 共识度"分入 3 桶（高共识 / 不确定 / 低共识），仅披露桶标签而非完整概率——这一近似最优策略在 LLM 群体预测任务上仍成立。
- **可证伪化操作定义**：Stage 1 估计 V_LLM(x)；按 V(x) 形状取最优三分位点；Stage 2 在新数据上对照完整披露 / 桶标签披露 / 按 x 选择性披露三策略，预测精度差距 < 1.6pp 即判"Stoplight ≈ FDNA"在 LLM 上同样近似成立。AMW 摘要的 "Stoplight ≈ FDNA" 是这个猜想在 fact-checking 上的镜像（原文 Table 2, p.568：SL 72.5% vs FDNA 72.3%，差 +0.2pp 不显著）。
- **嵌入方式**：
  - 路线图落点：§4.7 信息集旋钮下的子水平（"完整快照 vs 加噪/延迟快照 vs 桶标签"），预注册为 Stage 2 的一个三级臂。
  - Paper A 影响：无（上游是审计型数据集，与披露策略无关）。
  - 若验证通过：L 池文献中尚无 LLM 群体版本的 disclosure-simplification 文献，可能成为 *Paper B 的一个独立方法学贡献*（不为 herding 议题、为披露设计的工程简化）。

### 4.2 H6 — "herding 的信念更新分解"

- **一句话陈述**：把 AMW 的 own-signal overconfidence vs AI neglect 分解机制移植到 LLM 分身——每个 persona 的"persona noise" (s_ij) 与"市场共识采纳度" (x_ij) 可被分离估计；herding = x_ij 过强（市场信号主宰 persona 信号）。
- **可证伪化操作定义**：构造正交化的两变量（market-implied prob persona_weight + persona-posterior prob persona_weight），从 LLM trace 估计权重方差分解；高 herding 必导致 x_ij 权重 >> s_ij 权重；low herding 则两者相当。Stage 1 可在对照数据上（信息集臂 = 不含市场快照）独立验证 s_ij 的边际贡献。
- **嵌入方式**：
  - 路线图落点：§4.1 herding 操作化双层指标的"机制版"扩展（路线图 §4.1 末尾已埋伏笔为"信念更新权重问题"，本猜想把它扶正为 Stage 2 的一个预注册次级假设）。
  - 与 Dunning 提升为"机制共主引"配合：AMW (因子化) + Dunning (行为) + H6 (LLM 上的) = 三源互证。
  - 验证失败也不损失价值（直接证明 herding 由其他机制驱动，框架仍立）。

### 4.3 H7 — "agent-level effort crowd-out"

- **一句话陈述**：AMW 发现 fact-checking 中人类对 AI 披露减少 effort 8-13%（原文 Table 3, p.642-655），但精度影响小；LLM 群体中等价物是 token 数 / round 数 / 工具调用——若信息集越详尽 → 调用越省，则 herding = effort crowd-out 的群体级对应物。
- **可证伪化操作定义**：从 LLM trace 提取 (a) 输出 token 数 / round 数；(b) 工具调用次数；(c) 解析后概率的 entropy。按信息集臂（含/不含市场快照）比较 (a)(b)(c) 的组间差；差 > 阈值 + direction 与 AMW 符号一致即印证。
- **嵌入方式**：
  - 路线图落点：作为 §4.8 运行期监控的"扩展监控项"+ §4.1 herding 双层指标的"机制辅助诊断"——非独立旋钮，作为 *诊断信号* 而非主实验。
  - 若发现：把"暴露于市场信号使分身省 effort"作为一个独立机制补丁，加进 InfoDelphi 框架（asymmetric evidence 是必要而非充分；effort cost 也须 asymmetrize）。
  - 这是 AMW §5.3 表格 3 的 "External Sources / Clicked Google / Time Taken" 三个 metric 的 LLM 类比——把认知行为学的 effort 测量翻译到 LLM 的 token-level effort 测量。

### 4.4 三条猜想优先级与组合

| 猜想 | 优先级 | 对路线图影响 | 是否独立可发表 |
|---|---|---|---|
| H5 (Stoplight 在 LLM) | 低-中 | 仅 §4.7 子水平 | 可（披露简化单独发表） |
| H6 (信念更新分解) | **高** | 升级 §4.1 末尾注记为确认性次级假设 | 直接进 Paper B Discussion |
| H7 (effort crowd-out) | 中 | 升级 §4.8 监控项 + 辅助 §4.1 诊断 | 进 Paper B §4 Runtime subsection |

**推荐组合**：H6 + H7 一起进 Paper B（前者是主结论的机制支撑，后者是诊断信号）；H5 作为后续短文。

---

## 5. 更优雅的论文框架或实验方案（用户问题 4 续）

三个子问题逐一评估。

### 5.1 (a) AMW 两段式是否有更简单的替代？

**当前 v1.3 状态**: AMW 两段式 + 规模 (3/10/30) × 信息集 (含/不含市场) = 2 旋钮 factorial，已经是 AMW 精神下的"较简单替代"——但仍依赖 factorial。

**更简单的替代**:
- **直接做 V_LLM(x) 一个 estimator**，不做任何 factorial；Stage 1 估计 V(x)；Stage 2 由 V(x) 推导 *1 个* 最优聚合策略并验证。
- 旋钮 = 0（不操作化 factorial）；确认性假设 = 1（"V(x) convex"或"non-convex"二选一）。
- 优势：样本量需求大幅下降（V(x) 估计本身只要 moderate n + 分箱合理）；确认性检验简单；与路线图 §4.3 的 power 缺口最契合。
- **风险**：低 x 区间（冷门事件）样本稀疏；Assumption 2.1/2.2（充分性假设）在 LLM 群体上未必成立——必须在 Stage 1.5 (即 §3.2 的修订建议) 先验证。
- **判定**：可作为 *路线图 v1.4 的进一步简化*——但当前 v1.3 已是对 v1.1 的"优化即可不重构"裁定；建议**将这个替代方案作为 v2.0 候选留档**，下一轮优化时再上。

### 5.2 (b) herding 操作化（双层指标）是否有更直接的测量？

**当前 v1.3 状态**: §4.1 双层指标 = (i) 群体内部一致性（方差分解 / token-overlap）+ (ii) 群体-市场一致性（信息增益 ΔI）+ 信息集臂作识别。

**更直接的测量候选**:
- **单一信息论度量**: persona 输出与市场共识的 mutual information I(p_persona; p_market)。这是单一数字，跨 x 区间、跨任务流统一可测，比双层 + 信息集臂的间接识别更简洁。
  - 优势：单度量便于汇报；与 AMW V(x) 的"充分统计量"哲学一致——为一个量设计一个度量。
  - 风险：mutual information 在 LLM 输出非数值概率时估计困难（需离散化 + binning）+ bias 修正（Miller-Madow 等）。
- **预测级 black-box 测量**: 给评分者看"匿名化的群体输出 + 一句市场描述"，让评分者二分类"输出是否看过市场"——本质是信息集的语义级测量。
  - 优势：测的是 *信息* 而非 *形式*；herding 的语义定义（"是否真的看过市场"）精准匹配。
  - 风险：评分者可靠性必须量化（与 v2 §5.3 的 Cohen's κ ≥ 0.6 同款纪律）；评分者的认知成本高（每组输出评估需要 30-60 分钟）。
- **判定**: 维持 v1.3 的"双层 + 信息集臂"作为默认操作化，但**H6（信念更新分解，§4.2）**作为 *机制版* 升级——单一 MI 度量可作为 H6 的副产物，不必单独占路线图节点。

### 5.3 (c) Paper A 与 Paper B 的咬合机制是否有更优雅的形式？

**当前 v1.3 状态**: "悬念句 + 预注册" = Paper A 公开 H4-ii 悬念，Paper B 以此为预注册假设。

**更优雅的候选**:
- **形式 A：悬念句 + 预注册（保持）**——v1.3 裁定，已有 v2 H4-ii 文本对位。**不修订**。
- **形式 B：双向暴露 = Paper A 描述性 → Paper B 确认性 → Paper A 复检**——把双篇改成 *三角* 结构：Paper A 描述、Paper B 确认（OSF 预注册 H）、Paper A 后附一节 "Revisiting H4-ii after Paper B"。优势：闭合环路，构成 *closed-loop finding*。
  - 风险：违反 §6 第 7 条 "双篇咬合单向脆弱性"已记录的风险（Paper A 评审改 H4-ii 句则 Paper B 预注册假设即受损）；三角结构加剧了这个脆弱性。
  - 判定：**不采纳**——理由是当前的 v6 §7 单向脆弱已可管理，三角结构不增力但增险。
- **形式 C：把 H4-ii 改为 *机制级* 命题**——当前悬念句措辞是 "kimi 群体信号是否含独立信息 = 待检验悬念"（v2 §3 H4-ii）。改为机制级 "kimi 群体是否暴露 own-signal overconfidence 而非 market signal 采纳 → 期待信念更新权重不对称"——与 §3.1 / §4.2 的 H6 配合，把悬念从 *What happens* 升级到 *What mechanism*。
  - 优势：更利于 Paper B 的机制版讨论；为 Dunning 升级为机制共主引创造文本对位。
  - 风险：v2 的 H4-ii 措辞已锁定，提议改动需经 Pipeline validate + 编辑层裁定。
  - 判定：**轻微建议（不强制）**——若路线图 / 开题 v2 的 v2.x 版本接受微调，可上行。
- **形式 D：跨篇"叙述对账"而非"实验对账"**——把 Paper A 的 H4-ii 悬念句升级为 *frame-setting* 段而非 *suspense* 句，Paper B 不依赖该句而是 *引用* 它作为领域内的开放问题——解耦两条线性脆弱性路径。
  - 优势：降低 v6 §7 的脆弱性。
  - 风险：失去"实验前已公开假设"的叙事价值。
  - 判定：**不采纳**——"实验前已公开假设"是路线图 §2 "咬合机制"的核心价值，解耦会损失该叙事。

**综合判定**：**维持形式 A（悬念句 + 预注册）**，**形式 C 作为可选微调**（把悬念句从 "是否含独立信息" 升级为 "是否暴露 own-signal overconfidence 机制"）。其他形式不采纳，理由详见各判定段。

---

## 6. 元方法注记（自指）

本审查本身的元方法注记：

- **跨域借鉴标签**: §2.1 AMW、§3.1 §3.2 §3.3 §4.1 §4.2 §4.3、§5.1 §5.2 §5.3 中提到的所有 "human-AI → LLM 群体" 推断均为跨域借鉴，按引用纪律标注。
- **受条令启发**: §3.4 中提到的 "AMW Stoplight 启发披露简化"、"Dunning 启发环境极端性破坏监控"、"BHS 印证多源 overconfidence" 等均为受条令启发的设计类比，按 CLAUDE.md 引用纪律明示。
- **可靠性边界**: 本审查的 *事实声明* 基于精读 4 篇原文 + refscan.md + reference-paper-anatomy.md + proposal v2；*判定* 基于上下文用户 2026-07-20 启动的"对每一份引用文献的有效性挑战 + 跨域借鉴边界标定"框架。所有 *判定* 都附理由路径，便于下游审查者驳回而非作为铁案。
- **未做事项**:
  - 未外部检索 3 项 refscan §A 真缺口（聚簇设计效应 / adaptive design 方法学 / Cohen's κ 方法学）——属另一任务，本审查不重复造轮。
  - 未再核实 AMW 期刊发表状态（路线图 §10 标记 "unknown"）；建议引用前必须再做一次外部核实。
  - 未对 4 篇的实际页码做 PDF 物理页码二次校对——本审查使用文件章节标识符（如"AMW §6.3"）而非逐页脚注，避免与未来 PDF 版本错位。

---

## CHANGELOG

| 时间 | 内容 | 来源 | 执行者 |
|------|------|------|--------|
| 2026-07-22 | 新增 `literature-synthesis.md`：对路线图 v1.3 新增方法论部分（§4.2 / §4.6 / §4.7 / §4.8 / §10）的价值评估（论文入引 vs SOP 沉淀 vs 不入） + 4 篇参考文献复核判定（AMW 维持主引但限定内涵；Dunning 建议升级为 Mechanism Co-Lead；BHS 措辞分层；Tychastic 驳回确认）+ 颠覆性发现 3 条（AMW 协作增量可忽略、V(x) 替代旋钮、模型家族 blocking 强化）+ 候选新猜想 3 条（H5 Stoplight / H6 信念更新分解 / H7 effort crowd-out）+ 优雅框架评估（5.1 V(x) 替代 factorial；5.2 MI 单度量 / black-box 测量；5.3 维持形式 A、形式 C 可选微调） | `docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21.md` v1.3 + `analysis/roadmap-v12-scan/refscan.md` + `analysis/kimi-reasoning-assessment/reference-paper-anatomy.md` + `/Users/tangzw119/Downloads/ima-decision-under-uncertainty/` 4 篇原文 | design agent |
