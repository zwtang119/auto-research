# 顶刊选题终裁 memo：基于第一性原理的协调员决策

- **日期**：2026-07-18
- **决策者**：协调员（受用户委托拿主意，保留拒绝任何方向包括用户提议的权力）
- **输入**：同目录 `w1-first-principles-criteria.md`（选题标准三层溯源）、`w2-directions-audit.md`（D1-D4 诚实审计）、`w3-ai-autoresearch-landscape.md`（AI 自动化研究景观 + 本地资产）
- **方法声明**：裁决只用权威层准则（Horejs Q1/Q2/Q3 + Gewin L1 升维出的 C1-C7 过滤器），不复述 2026-07-17 recalibration 的项目内部包装（w1 §3 已指出其修辞层过度归因）。

---

## 0. 一句话裁决

**现有 D1-D4 无一够到顶刊**（D4 KILL、D2 KILL、D3 并入 D1、D1 降级为 Findings 诚实版）；**唯一可能够到顶刊（NeurIPS D&B / ICML 主会级）的选题，是把"AI 自动化研究"本身当实证对象：长周期过程 trace + 失败模式 taxonomy + stop/pivot 决策边界（W3-C1）**——GO 附 4 条硬 gate；gate 资源不到位，则诚实结论是"本项目当前没有顶刊课题"，不硬冲。

---

## 1. 裁决框架

- **元原则**（Horejs L2-P0）：写作救不了烂研究。选题不过关，outline 写得再好也没用。
- **三条权威准则**：Q1 问题对多领域重要（不只 immediate field）；Q2 数据鲁棒；Q3 发现能被他人接住。
- **决定性过滤器**（w1 §2）：C2 红线一句话（删掉独占数据后主张必须仍成立）、C5 主张-证据一致（每条主张 ≥2 独立证据）、C7 不可被数据独有救活。
- 对每个方向只问三件事：**Q1/Q2/Q3 各过不过；红线句写不写得出来；删掉独占数据死不死的掉。**

---

## 2. D1-D4 终裁

| 方向 | Q1 | Q2 | Q3 | 终裁 | 决定性理由（证据见 w2） |
|---|---|---|---|---|---|
| D1 G3 standalone | ✗ niche | ✗ | ⚠ | **PARK** | 自报 92.9% vs 实测 64.3%（−28.6pp）；N=2 Brier "100%"是 base-rate 假象；§4 表格全 placeholder。天花板 Findings 7.0-7.5（25-35%），不是顶刊题 |
| D2 verdict-reversal | ⚠ | ✗✗ | ✗ | **KILL** | feature (a) projection residual 在 7 个 AR-only 字段上信息论不可逆；feature (b) Murphy 分解需要的多结果概率向量在 AR 侧不存在（只有 scalar `confidence_before`）；22-investigation corpus 无磁盘 schema。数学上不可计算 = 永久 placeholder |
| D3 +harness ablation | — | ✗ | — | **并入 D1** | §6 全部 HYPOTHESIZED-NOT-TESTED，是 methodology spec 不是 experiment；作 D1 appendix 比独立成文诚实 |
| D4 联合论文 | — | ✗✗ | — | **KILL** | "D2 复用 G3 crosswalk"四处不成立（w2 §3 专项核验）：D1 根本不输出 D4 声称的 per-record 信号；integration ≠ resolution。三个 child 各自不成立，joint 必不成立 |

**关于 D4 的说明**：上一轮"D1 提供方法论核心、D2 作检测器应用于测试台"的交叉点叙事，经逐项核验属错误简化。用户要求"不要轻信"是正确的——联合论文如果送出，审稿人复算即死。

**D1 的善后**（仅当本周期需要一篇产出才做）：按 w2 §7 诚实重写——64.3% 真值入 §3.1、采用磁盘上已有的 5 个 settlement record 替代 N=2、修正 arXiv 交叉引用（≥2 个 ID 作者归属不一致，是 desk-reject trigger）。投 EMNLP Findings / Eval workshop，与顶刊目标解耦。

---

## 3. 直接回答用户："用 AI 做 Auto Research"是不是新方向？

**分两半回答，一半拒绝，一半接受。**

- **作为"造系统"（再造一个 AI Scientist）：不新，拒绝。** 赛道已饱和（w3 §A.2）：Sakana v1/v2、Google co-scientist、OpenAI PaperBench/MLE-bench、Meta MLGym、HKUDS AI-Researcher（NeurIPS 2025 Spotlight）全部占位；前沿实验室算力碾压；2025 H2 起月投稿 30+。我们没有任何比较优势。
- **作为"研究对象"（实证研究 AI 研究系统本身怎么失败）：新，且是文献最大空白。** w3 §A.5/A.6 证据：无人公开 process-level trace（Sakana/AI-Researcher 只公开 pipeline 代码）；没有 grounded failure taxonomy（AI Scientist v2 只列 3-5 个例子）；stop/pivot 决策边界无人量化（Karpathy 公开批评的三种失败无触发条件）；所有 SOTA 数字卡在 20-42%，没人系统回答"为什么"。

**关键判断——我们唯一不可复制的资产不是任何 finding。** G2 calibration paradox 被 N=30 证伪、Direction A 被机制实验证伪、G3 覆盖率自报虚高——findings 层面我们几乎没有幸存物。但**过程资产**（w3 §B.1）是公开文献无等价物的：完整的、带证伪决策记录的、评审透明（6 次 5-persona review + 3 次跨 provider 偏差观察）的长周期研究 trace，外加 Policysim/Tsinghua 多智能体仿真数据与 cds4worldcup 真实结算锚。**包括今天这一次：D4 交叉点造假被审计当场抓获——这本身就是"AI 研究系统如何失败并被发现"的一手过程数据，文献里没有第二个公开样本。**

### 第一性原理检验（W3-C1：trace + failure taxonomy + stop/pivot）

- **Q1 多领域重要：✓ 强。** 所有 frontier lab 都在赌 research agent；"它们如何失败、何时该停"对整个 AI 领域 + AI4Science + meta-science 都重要。这是 D1-D4 全部不具备的。
- **Q2 数据鲁棒：⚠ 当前不过，可达成。** 单项目 trace = N=1 轶事（w3 自承）。但观察到的失败模式可在公开记录上交叉验证（Sakana v1 三篇全拒、v2 1/3 过线、PaperBench 21%、MLGym "无发现能力"、Karpathy 三失败）——外部效度可建，见 §4 gate 2/3。
- **Q3 可被接住：✓（附条件）。** taxonomy + 可观测签名 + stop/pivot 规则对每个造 research agent 的团队直接可用；条件是 trace 数据集必须发布（gate 1），否则退回数据独有赌博（C7 死）。
- **红线句**（C2 测试）："We provide the first process-level empirical account of how autonomous research agents fail over long horizons — observable failure signatures and stop/pivot boundaries, grounded in a complete falsification-laden trace and validated on public failure records." 删掉我们的独占 trace 后，taxonomy 仍需靠公开失败记录存活——这正是 gate 2 存在的理由。

---

## 4. 终裁排序

1. **C1（过程 trace + 失败 taxonomy + stop/pivot 边界）→ GO（附 §5 四 gate）。** 目标 NeurIPS 2026/2027 Datasets & Benchmarks 或 ICML 主会级；w3 诚实估计 35-45%（gate 全过后）。这是桌上唯一 Q1/Q2/Q3 都可能过的题。
2. **C2（跨 provider judge 偏差）→ PARK。** 不独立成文——本项目自己的 G2 就是 N=6 樱桃摘取的受害者，单独写只会撞上 CoBBLEr/JudgeBench 的 N=50-200 体量墙。降级为 C1 的一个 failure mode 章节（judge drift）。
3. **C3（5-persona fold-chain 方法论）→ PARK。** workshop 级，降级为 C1 的 methodology 章节。
4. **D1 → PARK**（Findings 诚实版，仅在本周期需要产出时做，与 C1 解耦）。
5. **D2、D4 → KILL；D3 → 并入 D1。**

---

## 5. C1 的四条硬 gate（GO 前置，估 4-8 周）

| Gate | 内容 | 不过的代价 |
|---|---|---|
| **G1 数据集发布化** | auto-research trace 整理为可发布数据集（progress/findings/iteration log + P11 raw 对照数据 + 本次选题审计链），schema 文档化、匿名化 | Q3 死 → 退回数据独有赌博 |
| **G2 外部验证** | taxonomy 盲应用于 ≥5 个公开失败记录（Sakana v1/v2 failure 分析、PaperBench、MLGym、MLE-bench、ScienceAgentBench；AgentRxiv 若可得）；公开失败被 taxonomy 覆盖率 ≥70% | Q2 死 → N=1 轶事，taxonomy 无外部效度 |
| **G3 预注册 + 评分者信度** | taxonomy 类别与可观测签名先预注册；≥2 名独立 raters 打标，κ ≥ 0.6 | Q2 死 → 事后归纳嫌疑 |
| **G4 红线复审** | 按 w1 C1/C2 写 title + red-line 句，过 2 名非本领域读者 30 秒测试 | C1/C2 死 → 题还没想清楚，不动笔 |

任一 gate 不过 → C1 自动降级为 Findings/workshop 诚实版，不硬冲顶刊。

---

## 6. 拒绝条款（对所有人，包括我自己）

若 G1-G3 的资源（主要是外部验证 + 数据集整理，估 3-4 周全职）无法到位：**诚实结论是"本项目当前没有符合第一性原理的顶刊课题"**。此时的正确动作是——D1 诚实版投 Findings 留个记录、C1 降为 6 个月期主线继续积累外部 trace——而不是把 D4 这类合成品或任何 placeholder paper 送出去被拒。**宁愿承认没有，也不制造垃圾。**

---

## 7. 记录与下一步

- 本 memo 已写入 `docs/investigations/topic-selection-2026-07-18/`，与 w1/w2/w3 三份输入并列。
- `state/progress.json` 追加一条 `topic_selection_first_principles_verdict` event。
- 下一步（待用户确认后启动）：C1 gate G1（trace 数据集整理）+ G2（公开失败记录清单与可得性核实）可并行启动；D1 诚实版是否本周期做，由用户定。
