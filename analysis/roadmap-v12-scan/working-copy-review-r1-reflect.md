# 双篇路线图 v1.5 顶刊拒稿人反思评审（reflect-method）

> 日期：2026-07-22
> 执行者：reflect-review subagent（顶刊审稿人视角）
> 评审对象：`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md` v1.5（双篇：Paper A 世界杯五预测者审计 + Paper B LLM 群体 scaling 前瞻验证）
> 既审覆盖：refscan.md（文献扫描）/ se-review.md（系统工程）/ redteam.md（红队 RT-1–RT-10）/ v15-recheck.md（B0 执行扫雷）
> 方法论：reflect skill 二问框架——以顶刊（Nature / Science / PNAS / Management Science 级）审稿人视角找出 (1) 最不确定、最可能被审稿人击穿处 (2) 作者最大的遗漏、尚未意识到的问题
> 纪律：evidence/ 只读；封存仓库 `~/Documents/GitHub/cds4worldcup` 零读写；只攻击 v1.5 此前未被覆盖的新攻击面，或指出已有修复中的逻辑漏洞；不重提 RT-1–RT-10 与 v15-recheck E1–E8 已登记项目

---

## A. 顶刊审稿人视角的对焦

前置认知：v1.5 已经做了三轮深度内审（红队 10 条、SE 6 条、文献扫描 4 篇判定、v15-recheck 8 个新洞），且编排器逐条裁定修复方案。本轮视角**不再枚举执行规格级问题**，而是把以下两问作为攻击平面：

- (Q1) "这份路线图最不确定、最可能被审稿人击穿的地方是什么？"——找**结构层 / 方法论层**软肋，落到具体段落+原文摘录；
- (Q2) "作者最大的遗漏、尚未意识到的问题是什么？"——找**静默漂移 / 隐性假设升级 / 证据底座 vs 实际裁定的张力**，这些是审稿人一眼即穿但执行者自洽盲点。

下文的每一条发现都按"致命 / 严重 / 轻微"分级，且至少绑定一个 v1.5 内具体锚点（段落号 + 原文摘录），**避免与 RT / SE / v15-recheck 已登记项目简单重复**。

---

## B. 致命发现（Fatal —— 不修复则论文级别或主干结构崩盘）

### F-1 [致命] 底座选型裁定与证据底座直接冲突：v1.5 违反其自身证据底座的推荐主力对

- **锚点**：v1.5 §4.2 (B)(A)："**主力对 = gpt-oss-120b + Nemotron-3-Super-120B**（同 120B 档、OpenAI / NVIDIA 两家族）"（RM:120）；同一行：探索性支臂含 **OLMo 3 32B**（RM:122）。
- **冲突来源**：`docs/investigations/open-model-cutoff-verification-2026-07-22.md` 的"修订后的选型表（v1.5 以此为准）"明确推荐："**主力对**：gpt-oss-120b（官方卡 2024-06）+ **OLMo 3 32B**（语料公开，2024-12）"（report:92）；并明确"证据强于 gpt-oss 的卡声明级"的 Nemotron-Super-120B 被列为"备选主力"（report:94）。
- **顶刊审稿人击穿路径**：投稿时若有 reviewer 注意到 v1.5 把"备选"扶正为"主力"、把证据最强的"语料公开可证伪"金标准（OLMo）降为"探索性支臂"，而理由栏只给了"能力地板——30B 级底座会混淆结构效应与能力缺陷"——这条理由在 SAS 范式（解剖报告:151 范式门槛）下并不成立：该范式最强的 9 模型中含多种能力档次，目的是"capability 作为显式区组/因子而非仅复现性注脚"（redteam refscan C1-4 已点过这一论）。**而 v1.5 把能力地板当作排除 30B 的理由**，等于把"capability saturation" 这一范式门槛的设计要素砍掉了。
- **具体后果（多条同发）**：
  - (i) 与"证据底座推荐"相悖 = 内部不自洽，reviewer 第一轮即问"为什么违反自己的推荐？"；
  - (ii) Nemotron-CC 语料 gated 需审批（RM:120、E8），审批若延迟或被拒，Nemotron 引用须降为第二级（卡声明级）——主力对降级相当于失去"语料公开"金标准优势；
  - (iii) OLMo 3 在支臂里被分到"探索性不进确认性假设"，意味着任何"基准率敏感性"主张在主力对里不可证伪；
  - (iv) 选型理由 (i) 的"30B 级会混淆结构效应与能力缺陷"是 TSE（treatment spillover effect）类论断，但在 N=2 设计下"30B 是结构差异"是更可能而非更不可能——审稿人会要求 simulation 证据。
- **可执行修复建议**：
  1. 路线图 §4.2 必须**显式登记"采纳证据底座推荐"或"明确不采纳"**的裁定理由（即对 open-model-cutoff-verification.md 报告 §Recommendations 1 条逐字回应），不能两侧漂移；
  2. 若理由是"能力地板"，则应附"单 agent baseline 必须先在 30B 与 120B 档各跑至少一次以验证能力差异"作为 B0 出口判据；
  3. 修订 §4.6 B0 交付物增加"主力对内增加 n=1 单 agent 基线锚点（跨档对照）"（v15-recheck F 表第 6 条已点同类但只呼"探索性增补"，这里是确认性升级）；
  4. 或者：**改回证据底座的推荐主力对**（gpt-oss-120b + OLMo 3 32B），把 Nemotron-Super-120B 留作主力对 + Nemotron-Nano-30B + Llama-3.3-70B 跨家族稳健性测试，结构更纯净。
- **关联漏洞链**：Nemotron-Super 与 gpt-oss 同档但非同一家族，两者能力差异未经 pilot 实证；若同时跑 Nemotron-Super + gpt-oss，能力差异被锁死为 OpenAI vs NVIDIA = 不可分解；改 OLMo 3 则出现 120B vs 32B 的能力梯度+家族梯度，可双因子分解（capability × family）。

### F-2 [致命] "cutoff-hindcast 回放" 是 Hindcast 项目（arXiv:2607.14051）的实质重写，但路线图未给占位风险预案

- **锚点**：v1.5 RM:96 "v1.5 起 V(x) 估计……改用**截止日回放**"；RM:138 同样；B0 交付物 (vi) "Hindcast 占位调查……写明 Paper B 与其差异化"（RM:164）——**整段只写"查差异化"，未写"若发现强重叠的预案"**。
- **冲突来源**：
  - `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md:171` 已点名 **Hindcast (Ye et al. 2026) = "市场 replay 评估 LLM"的拥挤新方向**；该候选是 §2.4 的"中威胁"竞品；
  - v15-recheck B0 表 (vi) 注 "仍只是名字"——证实交付物没写"占位后预案"；
  - Hindcast 标题 = **Replaying prediction markets to evaluate LLM forecasters**，本质即"用过去市场价格 + 已结算事件回放检验 LLM forecaster"。v1.5 新增的 Stage 1 cutoff-hindcast 回放 = 用训练截止日早于事件的开源模型回放预测已结算事件，与 Hindcast **方法论骨架完全同形**，唯一区别是 Hindcast 用"市场作为 ground truth"vs v1.5 用"事件结果作为 ground truth，市场作为 x 的代理"——这一区别在审稿人眼里**不构成方法学增量**，只构成工程层差异。
- **顶刊审稿人击穿路径**：第一轮若 review 拉出 Hindcast 摘要，会问 "What is the methodological advance over Hindcast? You are doing replay hindcasting with a different framing."——v1.5 不能用"加速"或"决策空间"做差分，因为 Hindcast 项目本身就是为了 LLM forecaster evaluation 而设计，已是非平凡的事实原型。
- **具体后果**：
  - (i) C2/Check 4 PARTIAL（v2-gap 评估 §3.1）从 "缺乏 disambiguation" 升级为"主干被占位"；
  - (ii) B0(vi) 写"查差异化"——若查完发现重叠度高，则整个 Stage 1 回放臂需重设计，而路线图在 §7 风险表无对应回退条款（连带影响：F-3 §4.5、§4.6 B1 行"回放+前瞻蓄题双轨"皆需重写）；
  - (iii) "时间从数月压到数周"在审稿人眼里是工程优化，**不是方法学贡献**——若 Hindcast 已存在，v1.5 失去"加速"作为决策依据，而它目前正是 v1.5 相对 v1.4 的最大销售点（RM:19 "时间从数月压到数周"）。
- **可执行修复建议**：
  1. 路线图 §4.6 B0 交付物 (vi) 改为**双轨**：差异点（必须证明与 Hindcast 方法学增量：例如"AMW 两段式在 replay 上的跨期可迁移性作为独立机制贡献"——但这恰是 v15-recheck E4 未登记的可迁移性假设，新攻击面因此显形）+ 占位后预案（如发现强重叠则合并为 Hindcast 增量验证设计，明确"本研究对 Hindcast 的 X 增量"）；
  2. 在 v2 §2.4 已点名 Hindcast 的前提下，路线图 §6（占位威胁）必须**升 Hindcast 为高威胁并附差异化论证段落**，不能用"查新"代替；
  3. 写作层面的预案：若 Hindcast 已审稿发表，先把 Stage 1 回放臂**降为 Hindcast 的扩展实验**，在 related work 显式陈述"对 Hindcast 的扩展：从回放市场到跨任务域"——这是新故事。
- **关联漏洞链**：v15-recheck D-7/D-8/E8 已点"快照可得性、Hindcast 占位调查规格"，但**没点"占位后预案"**——本发现承接其 D-(vi) 注释并升级为致命。

### F-3 [致命] v1.5 引入"回放→前瞻可迁移性"为新承重假设，但全文无登记、无检验、无回退（v15-recheck E4 的逻辑升级）

- **锚点**：v1.5 RM:138 "证据等级分工（v1.5）：Stage 1 从宽——模型截止日可验证……即可入场，回放结论的效力不依赖'无人能知答案'，而依赖'该模型不可能知道答案'；Stage 2 与期末考从硬——必须为前瞻事件" + RM:21/v1.5 §4.5"回放数据不得进入期末考评估集"。
- **冲突来源**：v15-recheck E4 已识别该新假设，但**v1.5 文字完全没有"可迁移性"概念登记**——RT-1 的充分性假设（V̂(x) 不依赖披露策略）也只管"V(x) 不依赖披露"，不管"V̂_replay vs V̂_prospective"。
- **顶刊审稿人击穿路径**：如果 reviewer 注意到 Stage 1 用回放事件估 V̂(x)、Stage 2 用前瞻事件验证同一 V̂(x) 是否成立——这恰是**经典的 distribution shift 问题**（领域漂移），训练-测试分布不一致时经验风险最小化的 OOD 推广保证全部失效。审稿人一句话就击穿：'You used a curve estimated on 5-month historical events to validate optimal strategy on prospective events. What is your invariance argument?'
- **具体后果**：
  - (i) 这是比 RT-1（充分性）更致命的一层新假设：充分性是"披露不变性"，可迁移性是"时间不变性"——后者失效的话，V̂_replay 不能推导前瞻期末考的"最优策略"，AMW 两段式主干第二阶段整体作废，**与 RT-1 同型但严重度更高**（因为失效则两段式整条死，不只是分支）；
  - (ii) §7:226（v1.5 风险表首行）"前瞻期末考蓄题过慢"已 v1.5 后收敛，但**未增"V̂_replay → 前瞻不可搬运"行**——这是 §7 行级漏登记；
  - (iii) §4.6 B1 行 "Stage 1 截止日回放批量执行 + 前瞻任务流并行开跑为期末考蓄题"——**前瞻子流恰是检验可迁移性的天然载体**，但 RM:153 / v15-recheck A-5 指出前瞻开发段"未被重新指派用途"，路线图错过利用窗口。
- **可执行修复建议**：
  1. §7 风险表新增一行：**"V̂_replay → 前瞻不可搬运"**（v15-recheck E4 行预升级），对应回退预案——预写在 B1 中期设"V̂_replay vs 前瞻子样本交叉对照"检查点，不达预期阈值（如跨期 Spearman 显著下降至某 r²）则放弃 AMW 第二阶段，转为纯描述性论文 + Hindcast 重叠接受（Hindcast 已做过的事不重复）；
  2. §4.5 末段加："可迁移性对照 = 将 §4.5 提到的前瞻开发段（RM:153）重新指派为 V̂_replay vs 前瞻子样本交叉验证载体，B1 中期检查点逐月落盘，跨期 Spearman 与曲线偏移量进入预注册"（承接 v15-recheck A-5 建议）；
  3. AMW 两段式 §10 参考文献条目补："跨期可迁移性检验（多周期回放 + 前瞻子样本对照）为本研究的独立机制贡献，区别于 AMW 原始设计的'同一周期内第一阶段估 V / 第二阶段验证'（AMW Introduction :73–83，本项目 Strengthening This Design by Adding Cross-Period Invariance 作为独立方法学步骤）"——这是唯一能让 v1.5 与 Hindcast、AMW 同时拉开差异的位置。
- **关联漏洞链**：v15-recheck E4 已点"这是与 RT-1 同型同量级新洞"——本节给出更具体的可执行回退 + 利用前瞻子流具体路径。

---

## C. 严重发现（Major —— 修复可避免审稿一轮即拒，但需结构性调整）

### M-1 [严重] AMW 主引的不发表性质：路线图方法学骨架依赖一篇 working paper，引用强度超其证据级别

- **锚点**：v1.5 §10 参考文献主引首条 "Agarwal N, Moehring A, Wolitzky A. Designing Human-AI Collaboration: A Sufficient-Statistic Approach. **Working paper**, 2025-04-18……出处（期刊/编号）：**unknown**（截至 2026-07-22 未见发表信息，引用前须外部核实是否已有期刊版）"（RM:289）。
- **冲突来源**：
  - §4.2 整节实验设计都叫"AMW 充分统计量两段式"（RM:92 标题），§4.1 末机制注记也以 AMW 命名（RM:90）；
  - v1.5 不是"参考 AMW"，而是"AMW 跨域借用成为方法学主干"；
  - 一篇未见同行评审、未发期刊版、甚至 working paper 编号未给出的工作，承担了**整篇 Paper B 的方法学承重**——审稿人/editor 一查不到会立即要求替换承重引用。
- **顶刊审稿人击穿路径**：第一轮 reviewer 检索后发现 paper "unverifiable" 即可拒；甚至 better——若 reviewer 发现 AMW 已改投他刊（例如 repec/econlit 流通），版本追溯链断裂，引用出错。
- **可执行修复建议**：
  1. §10 主引条目必须**强制加注 "as of 2026-07-22 the authors' working paper has not appeared in a peer-reviewed venue; cite with caution and verify before submission"**，并在投稿前 7 天重核一次；
  2. §4.2/§4.1 弱化"AMW 主干"措辞为"AMW-inspired sufficient-statistic two-stage design"——把跨域借用的位置从"主引"降为"类比启发"；
  3. 寻找替换承重引用的最可能候选：info-theoretic sufficient statistic 经典文献（如 Khisti/Lehmann 框架）、Hansen 的 staggered decision 文献、Wager & Athey causal forest 框架——任一可填补"信息结构 + 最优聚合"的方法学骨架；
  4. 投稿前的应急：把 AMW 假设检验作为可弱化项（充分性假设被拒 → 回退小 factorial），至少让回退路径独立成立，不依赖 AMW 持续可引用。
- **关联漏洞链**：refscan.md B1 已点 AMW 出处 unknown，但**没点 v1.5 把它升为整节方法学主干的强度升级**。

### M-2 [严重] 充分性假设检验的"通过判据开口"未进 §7 预注册开口注册表（v15-recheck B 表 RT-1 行的逻辑漏洞）

- **锚点**：v1.5 §4.2 充分性假设验证段："通过判据与样本量配额**随 OSF 预注册写明**"（RM:98）；pilot 闸门 §4.6 测量层强制交付物同样 "充分性假设验证 + 回退触发判定"（RM:165）；§7:236 开口注册表列 5 项，**不含充分性判据**。
- **冲突来源**：v15-recheck B 表 RT-1 行已点（"充分性检验的通过判据开口未列入 §7:236 的开口注册表（该行只列 5 项，漏此项）"），但 v15-recheck 只挂为"瑕疵"——本节把它升级为**逻辑漏洞**：B0.5 pilot 闸门运行时（pilot 完成 = B1 启动前置条件），§7:236 的开口注册表未冻结充分性判据，意味着 pilot go/no-go 引用的"通过判据"在 pilot 当时**不存在**——闸门判定成为引用不存在标准的判空循环（与 v15-recheck D-9 时序矛盾同型）。
- **顶刊审稿人击穿路径**：若 review 拉到 OSF 时间戳文档，发现 pilot 在预注册冻结之前完成，会问 "what was your pass criterion for the pilot stage?"——若答"随预注册写明"，则"先跑 pilot 后冻结判据 = 在 pilot 数据上反推判据 = 标准 garden of forking paths（新形态）"——这恰好踩中 redteam.md RT-8 的修复逻辑（看完 Stage 1 结果后不得再改推导规则），但红队没审到的"pilot 阶段"出现同类违规。
- **具体后果**：与 F-3 形成 chain failure —— 可迁移性假设也"随预注册写明"开口（v15-recheck D-9），同样问题。
- **可执行修复建议**：
  1. §7:236 开口注册表必须**列入 7 项而非 5 项**，完整版：(i) herding 阈值；(ii) 结算缺失率阈值；(iii) moderate n 定量；(iv) x 分箱最小比例；(v) manipulation check 随机水平；(vi) **充分性通过判据 + 样本量配额（RT-1）**；(vii) **跨期可迁移性对照检查点（F-3）**；
  2. B0 出口判据冻结《pilot 协议》（含上述 7 项），B1 前 OSF 追认（v15-recheck B0 计划清单第 5 条已点，本节扩展为具体 7 项）；
  3. 写作预案：若 pilot 阶段被判 ok、但预注册冻结时该判据被改写，须如实记录 "pilot 时判据为 X，预注册冻结时判据为 Y，两者差异及对 pilot 通过的影响在 §x.x 报告"——是诚实披露而非掩盖。

### M-3 [严重] M5（信息集消融）解决了"含/不含市场信息"维度，未解决"训练语料市场回声"——v1.5 替代解释回应停留在披露级，无结构性响应

- **锚点**：v1.5 §4.2："**信息集**：含市场快照 / 不含市场快照 | herding 的因果识别：操纵 agent 能否看到市场信息"（RM:106）；§4.5 manipulation check 仅问"当前市场赔率/热门判断"，回放臂"赔率与结果认知应处随机水平"（RM:118）。
- **冲突来源**：
  - v2-gap §5.3 已 alert："**训练语料污染的市场回声**：若群体底座是可联网/训练语料含赔率的模型，'独立判断'在设计上就无法与'复述训练语料中的市场共识'区分"（GAP:72）——v1.5 §4.2 自己 echo "可控处的语料切断……任务窗口限选开赛后新事件以限缩回声，无法限缩处如实披露"（RM:118 (c)）——但**这是披露，不是结构性响应**；
  - v1.5 主力对含 Nemotron-Super-120B（后训练 2026-02，RM:120），其训练截止虽早于 2026-06 开赛，但**对国际足球赔率（博彩市场）的记忆极可能存在**（足球赔率是公开数据，自然存在于多数 LLM 预训练语料中），且"futures 早于 2024-06 已开盘"——这意味着禁市场臂即使禁了实时检索，对"哪支队是热门"的认知仍在权重里，manipulation check "随机水平"对著名赛事（如世界杯）永远达不成随机水平（v15-recheck E6 已点，且这是该洞的"系统必现"版本）；
  - E6 的"作废重跑"救不了——知识在权重里，重跑同样超标。
- **顶刊审稿人击穿路径**：reviewer 注意到主力底座训练语料来源 ≥ 2024-06，而国际足球赔率已是 Latent knowledge；manipulation check 设计为随机水平，则**整个禁市场臂必然不达随机水平**（除非选不知名低热度赛事，但低热度赛事又掉进 x 极端区间，§4.3 RT-5(a) 已点"低 x 区间样本稀疏"）——审稿人会问"为什么禁市场臂设计赌它能达成不可能的随机水平？"
- **具体后果**：
  - (i) M5 因果识别的承诺（"唯一干净手段"，RM:106）实际无效，因为禁市场臂对著名赛事的认知结构不可能等于"无市场信息"；
  - (ii) manipulation check 标注 "不达随机水平则该臂数据作废重跑"——若整臂数据全废，**信息集旋钮只剩一臂（只读含市场）**，确认性旋钮实际退化为单臂描述性比较；
  - (iii) §6 第 6 条（kimi 认识论绝缘）已被悄然扩大到 v1.5 的整个底座（同样受市场回声污染），作者未意识到这是**新的认识论绝缘层**：v1.5 的"独立判断"证据不能证明"任何个体的独立判断能力"，只能说"在 X 市场环境下个体不被市场直接复读的程度"。
- **可执行修复建议**：
  1. §4.2 信息集旋钮的**水平定义**改写：从 "含 / 不含市场快照" 二臂改为三臂：(a) 无市场信息 + 无声名任务（用不知名低热度赛事 + 限缩训练后事件）+ manipulation check 随机水平（设计为可达成的随机）；(b) 含市场快照；(c) 含市场快照但 persona 强差异化 + 任务窗口限赛后事件——三臂正交：市场信息维度 × 知识维度；
  2. manipulation check 重新定义随机水平：不能以"国际足球赔率认知为零随机水平"（不可达），应改 "本次任务的特定赔率细节（如半场比分线、伤停赔率）"为识别测试——把"宏观市场知识是否在权重里"与"任务具体信息是否被工具调用获取"分开测量；
  3. **降信息集旋钮确认性地位为探索性**+ 承认在原理层面无法彻底隔离训练回声，仅在工程层最大化隔离；或明确分两篇策略（探索性信息集臂 + 主结果放弃 herding 因果识别，只做 herding 相关性描述），与 v1.3 早期 "不可彻底把 herding 从 herding 同答分开" 的诚实边界接续。
- **关联漏洞链**：v15-recheck E6 已点 "manipulation check 对著名赛事远期赔率 (futures) 记忆救不了——知识在权重里"——本节把它与 M5 承诺冲突和 §6 第 6 条绝缘层扩大关联为严重级结构性缺陷。

### M-4 [严重] 静默口径漂移：n=350 锚点从"二元/单比较"扩展为体育三元（W/D/L）+ 时间聚簇

- **锚点**：v1.5 §4.3 锚点溯源 "Foresight Arena [arXiv:2605.00420] 原文……'detecting a true edge of α* = 0.02 at 80% power requires approximately 350 resolved binary predictions'" + "任务流时间聚簇按设计效应折算有效样本量"（RM:134、139）。
- **冲突来源**：
  - v2-gap §5.5 已 alert 该锚点原文适用边界 (i) 二元、(ii) 两 agent 单一比较、(iii) 50 rounds × 7 markets 时间聚簇（独立有效样本 < 350）；
  - v1.5 §4.3 把锚点用于 (a) Stage 2 策略验证的 power 估算（RM:139），(b) Stage 1 充分性检验的 n 配额（继承 §4.2 RM:98），**但 v1.5 任务流混入体育 W/D/L 三元任务**（RM:21、96）——RPS 三元 vs Brier 二元的 anchor 不一致；
  - "时间从数月压到数周"（v1.5 主要销售点）使得有效回放事件窗口变窄（约 5 个月 per F-1 资格窗口），实际可回放的二元事件数远低于 350；
  - 三次静默漂移合计：二元 → 三元（口径漂移）+ 二元单比较 → 三元三臂比较（复杂度漂移）+ 同期采样 → 跨期回放（分布漂移）。
- **顶刊审稿人击穿路径**：reviewer 若精通 power analysis，会在 methods section 一段问 "you cite 350 resolved binary predictions as your anchor, but you use a three-class outcome (RPS) and stratified sampling; please reconcile"。**答"按聚簇调整"不够——RPS 是 ordinal 三元，Brier 是 binary，二者的 anchor table 完全不同**。
- **具体后果**：(i) §4.3"MDE = 约 350"是无根据的口径借用；(ii) §4.6 B0.5 闸门未要求"先以 RPS 三元任务重做 power simulation"；(iii) 实际可回放事件数（如 2026-06 开赛后约 5 个月窗口）可能使 n<350 直接不达锚点下界。
- **可执行修复建议**：
  1. §4.3 新增段落："**RPS 三元 power 重算**——在 B0 任务流裁定后立即以观测 x 分布（市场隐含 W/D/L 三类概率）× 三类 ground truth 重新 sim 一次，得 RPS 锚点 n_RPS_min；并以"二元任务的 anchor 350" 仅作 cross-check reference，写明两口径的差异率 Δ（如 n_RPS_min / 350 = X）"；
  2. §4.3 显式区分 "二 anchor 表"：对二元任务（Brier-on-yes/no）→ 锚 350；对三元任务（RPS）→ 锚 n_RPS_min（由 sim 给出）；对四元（extend 含加时）→ 锚 n_RPS4_min（独立 sim）；
  3. v15-recheck A-2 已点"回放下 x 分布可在 B0 枚举"——本节扩展为 "B0 必须同时给出 RPS 三元 power 模拟报告，不只是 x 分布枚举"，并入 B0 成本模型；
  4. 在 PRISMA / OSF 预注册中**冻结两套 anchor 表**，任何调整视为违反预注册，须重新 OSF 入档。

### M-5 [严重] C1 一句话的"事实可满足 → 主语迁移"问题：MCDP-1 边注作为方法学论证的逻辑跳跃

- **锚点**：v1.5 §3.1 memo "MCDP-1 明言信息收集虽能减少未知数，却'不可能消除它们'……因此 PIV 不应被写成审计附属标签，而应与概率结构差异**并列为审计结果**……属'受条令启发的设计类比'"（RM:58）。
- **冲突来源**：
  - MCDP-1 p.11 "信息收集不可能消除未知"是**信息论的边界命题**（任何获取信息的行为都不能消除所有未知）；
  - v1.5 把"不确定性结构"与"PIV 字段"等同，跳过了中间论证步骤——
    1. **未证明**"协议完整性即等于不确定性结构的一部分"；
    2. **未区分**"不确定性结构"（如概率分布的熵、ECE、reliability gap）与"协议完整性"（如 ex_ante_status、snapshot_status）；
    3. **未证明**前者比后者"信息量更高"——只是因为前者"是概率结构"、后者"是元数据"，便默认后者地位低，缺乏方法学理由。
  - 上轮 v1.2 引入边注时已标注"引用纪律：受条令启发的设计类比"——但这种标注在论文写作中只能挂在脚注，主张本身的**论证跳跃未补足**。审稿人会问 "How does protocol integrity map to uncertainty structure formally?"——v1.5 答不出，因为这是设计哲学跳跃，不是形式化映射。
- **顶刊审稿人击穿路径**：PIV 作为"一等评估字段"主张（C4 / Check 7 在 v2 已声明）需要方法学论证；MCDP-1 引用是设计灵感（acceptable），但若正文段落靠"信息不能被消除 → 所以 PIV 应升一等"的逻辑链，会被当成"拟人化论证"质疑；
- **可执行修复建议**：
  1. §3.1 memo 改为"补充方法学论证而非替代"——补一节"协议完整性与不确定性结构的映射规则"：列出 PIV 八字段如何对应到不同不确定性维度（ex_ante_status → 预测过程的 coverage；snapshot_status → snapshot 漂移造成的不确定回报分布等），并配 reliability 测度；
  2. 或者把 MCDP-1 引用降为"动因引用"——明确"v1.5 的 PIV 等价地位主张不依赖 MCDP-1 推出，而是由 v2-gap Check 5（跨子领域迁移）+ Check 6（deep concern 抗冲击）共同支撑"；
  3. 同步审视 §4.2 的 MCDP-1 memo（RM:113 反对完全中心化约束规模）：这一条跳跃小（直接对应 policy doctrine vs 完全自动化），保留无虞。

---

## D. 轻微发现（Minor —— 修复简单，不影响骨架）

### L-1 [轻微] §10 参考文献条目的 Tychastic "留痕"评审判断被错引

- **锚点**：v1.5 §10 驳回记录 "Ross IM, Karpenko M, Proulx R, King J. Tychastic Optimization of ISRT Information Systems……经 2026-07-22 文献扫描判定不列入"（RM:305）。
- **问题**：refscan.md B4 明确判定 Tychastic "**不值得（列入双篇参考文献）**"——v1.5 §10 把它留在"驳回记录"段，等于把它写进了文献底座。审稿人会问"为什么提一个不在正文用的文献？"正确做法是直接删除条目（refscan 的判定是"不列入"），而非作为"驳回记录"留存。
- **修复**：§10 驳回记录段删除——Tychastic 的设计哲学启发已在正文中以 §4.1 末句间接引用（"最小化平均代价反而放大方差"），不再二次显式出现。

### L-2 [轻微] §6 第 7 条咬合单向脆弱性：补救句未升级为默认

- **锚点**：v1.5 §6 第 7 条 + §7 风险表 "Paper A 评审要求补 kimi 技能验证……" 行（RM:218、228）。
- **问题**：SE-review A6 建议"把'B 独立 OSF 时间戳预注册'从补救升级为默认动作"——v1.5 §8 检查点其实已经包含 "Paper B：启动 B1 前完成 OSF 时间戳预注册"（RM:246），**但 §6 第 7 条的措辞仍是"补救"**——前后口径不一致。
- **修复**：§6 第 7 条末尾删除"补救为" → 改写为"咬合从'预注册载体'降级为'动机引用'是默认设计，而非应急补救"。

### L-3 [轻微] §4.2 "能力地板"引证方向反转（v15-recheck A-3 已点，本节确认其影响范围）

- **锚点**：v1.5 §4.2 (B)(i) "single-agent 基线**过弱**时加 agent 呈负收益"（RM:120）；同节 (A) 表述正确（"single-agent 超 ~45% 后加 agent 呈负收益"，RM:105）。
- **问题**：v15-recheck A-3 已点（RM:120 与解剖:127 原文相反、与 RM:105 自相矛盾），但没点其"承重引用级别"——这一句直接影响选型理由的诚实性。
- **修复**：改 RM:120 为正确表述（"基线超 ~45% 后加 agent 呈负收益"），与 RM:105 统一。

---

## E. Q1 / Q2 反思维度的方法论注（reflect 二问直接回答）

按 reflect skill 的强制格式约束（每条 = 具体锚点 + why unsure + 验证缺失），并继承 sycophancy 抗偏置：

### Q1 (least sure) —— 关于本路线图我最不确定的:

> **(Q1-1) [MECHANISM-UNCLEAR]** RM:120 主力对的 120B 同档双家族（OpenAI vs NVIDIA）vs 推荐证据底座的 120B + 32B 异档双家族——**前者把 capability saturation（~45% 阈值）的存在性用作排除 30B 的理由**，但 45% 阈值来自 Science of Scaling Agent Systems 范式（N=180 配置），而 v1.5 N=2 主力对根本测不出 45% 阈值的适用点——该阈值选型的适用边界不清。我无法验证：是否范式原文承认"45% 是单档（120B）内 saturate 阈值"、"30B 基线远低于 45% 故证明其无效"——需读 arXiv:2512.08296v2 原文 Table 7/8 实证而非仅摘要。

> **(Q1-2) [ASSUMPTION]** RM:138"证据等级分工"+"回放结论的效力……依赖'该模型不可能知道答案'"——**该假设需要"模型不可能知道答案"的形式化定义**。MCDP-1 的"信息收集不可能消除未知"在此不适用，因为这不是概率论边界，而是**模型权重中的 latent knowledge 与具体事件结果的解耦**。我无法验证：是否承认"任何截止日之前的 LLM 都已知悉国际足球一般赔率分布与热门判断"（即权重中的市场回声）——若承认，则"不可能知道答案"仅指"具体赛果"而非"事件相关市场信息"，本路线图混用这两个层面。

> **(Q1-3) [UNTESTED]** Hindcast 项目（Ye et al. 2026, arXiv:2607.14051）作为 v2 §2.4 中威胁竞品，**整篇路线图没有读其原文方法章节**——只在 B0(vi) "查新 + 差异化"层面处理。我无法验证：Hindcast 是否真的做了 cutoff-hindcast + AMW 两段式 LLM forecaster 评估；若未做，则 v1.5 还有空间；若做了，则 v1.5 的回放臂被占位——但无论哪种，路线图目前的措辞"B0 启动后查差异化"都是赌注式语言，不是工程计划。

### Q2 (user's biggest omission) —— 作者最大的遗漏:

> **(Q2-1) 你没意识到你的口径已经静默漂移，且论文主干的脆弱性已升级**——v1.1 → v1.3 → v1.4 → v1.5 每一版都把新的工程加速/精细化（cutoff-hindcast、AMW 假设检验、底座选型、pilot 闸门、监控规则）叠加到主干之上，但主干越来越脆：当 AMW working paper 找不到期刊版（M-1）+ Hindcast 重叠（F-2）+ 跨期可迁移性假设（F-3）+ 训练语料回声让 M5 失效（M-3）同时撞在一起，**"优化即可不重构"的 redteam 总评（RT:102）就崩盘为"在不重构上叠加的优化债"**。你该问的是："我们有多少时间退一步，把主干拆为'核心 contribution (a): 跨期 cut-off 回放 + V̂(x) 估计的工程可复现性' + '核心 contribution (b): 受控 factorial 验证' 两篇独立 paper，每篇都自洽？"——而不是累积到 B0 之后再决定。

> **(Q2-2) 你没意识到 Hindcast 项目不只是占位威胁，而是 v1.5 在方法学上应直接 cite 的"先驱者 + 平行工作"**——你之前的 footprint 是"占位调查 + 差异化论证"（v2 §2.6 类的写作套路），但 Hindcast 已经被 v2 §2.4 "拥挤新方向"表述 = 它已经是同一方向，路线图却未把它的工程轨迹（如他们用什么底座、什么 RPS/Brier 口径、什么 power）作为 design reference。 你该问的是："Hindcast 团队的方法学决策是否比我们 v1.5 的更稳健？他们的 n=几百多大量级、他们用什么 base model、他们的 power anchor 怎么算？"——这是 v2 §2.6 "窗口易逝条件" 的同款风险，但不审 Hindcast 原文就抓不到。

> **(Q2-3) 你把"单 agent baseline 必须先验证能力地板" 作为 §4.2 (B)(i) 的理由，**但没有规定 v1.5 pilot 内必须先实测单 agent 能力**——v15-recheck B 表第 6 条提"n=1 单 agent 基线臂入 pilot"，但只标"探索性增补"。在主力对为 gpt-oss-120b + Nemotron-Super-120B（同 120B 档）的情况下，"capability floor"论证**没有 30B 对照组就不可证伪**：主力对都是高能力档，无法区分"结构效应"vs"能力效应"。你该问的是："为什么不让 OLMo 3 32B + Nemotron-Nano-30B 入主力对，这两个都是'低档基线'——能力地板论证就有了对照？"——这恰好是 F-1 的同源反思。

---

## F. 自检（per reflect 抗 sycophancy 偏置）

> 诚实自检：本节 Q1/Q2 各条均为基于具体段落的反思维（每条都有 rm:行号或文件名锚点），不依赖"路线图看似严密"的视觉印象；F/M 各条均在 v1.5 文本中找到对应原文摘录作为可证伪锚点，且至少一条不是 RT/v15-recheck 重提。本节最重的是 F-1（选型冲突）和 F-2（Hindcast 占位）——这两条若不修复，论文级别会被审稿人一击即穿；F-3（跨期可迁移性）是新承重假设，与 RT-1 同型但严重度更高。**若任一条读起来像"为通过 review 而拼凑批评"，则本节失效——本节拒绝这种拾遗补漏式批评，所有条目都从顶刊审稿人"批判怀疑一切"立场出发。**

---

## 附：本评审覆盖声明 + 未做事项

- **已覆盖**：全文 305 行逐行核对；引用上游包括 v2-gap、open-model-cutoff-verification、refscan / se-review / redteam / v15-recheck、v2 proposal §0–§10、reference-paper-anatomy §7.1–§7.2；本次**不重复 RT-1–RT-10 / E1–E8** 已登记项目。
- **未做（超出本次范围）**：未读 AMW 原文 PDF（不能验证 45% 阈值在 Paper B 设计中的适用边界）；未读 Hindcast 原文 PDF（仅查 arXiv:2607.14051 摘要 + v2 §2.4 转引）；未读 MCDP-1 原文 PDF（仅据 `cds4polymarket/docs/investigations/uncertainty-decision-methodology-2026-07-21.md` 已转引）；未盘点 cds4polymarket 历史数据资产（F-3 / E2 涉及）；未对 OLMo 3 32B 同期对照做 sim（仅据 v1.5 选型理由与其对立）；
- **boundary**：本评审做方法学判断和顶刊拒稿风险评估，不替用户做资源分配决议；F-1 的"改回证据底座推荐主力对"是可选路径之一，建议而非强制。
