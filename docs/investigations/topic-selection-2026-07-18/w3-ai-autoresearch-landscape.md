# W3 · AI 自动化研究（AI-driven auto research）外部景观与本地资产

> 日期：2026-07-18  
> 作者：auto-research 课题五 portfolio  
> 范围：Part A 外部景观调研（2024-2026）+ Part B 本地 GitHub 资产扫描  
> 目标：为"AI 自动化研究"作为论文方向提供决策依据；产出 3 个候选 paper claim  
> 关联：w1/w2 由并行 agent 撰写，本文件不触碰

---

## 摘要（TL;DR）

1. **赛道拥挤度：高（已收敛为模板化对比）**。Sakana v1/v2、Google AI co-scientist、Agent Laboratory、HKUDS AI-Researcher、PaperBench、MLGym、MLE-bench、ScienceAgentBench、CycleResearcher 在 2024-2026 集中爆发；几乎所有"first-class"贡献都被 front-runner 占位（novel 方法 + 大规模 benchmark + 已知失败模式）。  
2. **SOTA 真实水平**：(a) 完全自动化端到端研究——AI Scientist v2 只有 1/3 稿件通过 ICLR workshop 评审达到人类平均接收阈值（[arxiv 2504.08066](https://arxiv.org/abs/2504.08066)）；(b) ML 任务——MLE-bench o1 拿 7 块金牌但仅在小 subset 比赛（[OpenAI 报告](https://openai.com/index/mle-bench/)）；(c) 论文复现——PaperBench 最佳 21%（[PaperBench 报告](https://openai.com/index/paperbench/)）；(d) 科学代码——ScienceAgentBench 最高 32-42% 独立解决率（[arxiv 2410.05080](https://arxiv.org/abs/2410.05080)）。**没有任何系统能 end-to-end 做出 ICLR/NeurIPS 主会接收论文**。  
3. **可发表贡献缺口**：(i) 长周期真实研究过程的 trace 数据；(ii) 自动研究失败模式的实证 taxonomy；(iii) AI review 的校准（auto-judge 偏差被人手和文献都极少量化）；(iv) "什么时候 stop"的决策边界（cognitive loop / premature convergence / tangent failure——Karpathy 公开批评的三种）。  
4. **本地资产独特性**：auto-research 仓库已固化**多条长周期真实研究 trace**（state/iteration_log.jsonl 3 条；state/findings.jsonl 8 条带证伪决策记录；state/progress.json 17 个里程碑事件含 5-persona review 评分 + fold chain + G2 N=30 falsification；legacy/ 含 P11-pure-analysis/p11-no-think/p11-inner-monologue 三组 raw 实验对照数据），这是公开文献里没有先例的资产。  
5. **3 个候选 paper claim**（详见末节）：C1 长周期 trace + failure taxonomy、C2 auto-judge 跨模型跨 provider 偏差实证、C3 5-persona fold chain 方法论。

---

## Part A · 外部景观（2024-2026）

### A.1 系统清单与定位

| 系统 | 出品 | 时间 | 端到端？| 关键证据 / 评测 |
|---|---|---|---|---|
| **The AI Scientist v1** | Sakana AI | 2024-08 | 单篇 paper 自动化（依赖 code template）| ICLR 2025 workshop 投稿，**3 篇均未达人类平均接收阈值**；揭示了需要 code template 的局限 |
| **The AI Scientist v2** | Sakana AI | 2025-04 | 端到端 + VLM 反馈 + progressive tree-search | [arxiv 2504.08066](https://arxiv.org/abs/2504.08066) / [arxiv 2508.09479](https://arxiv.org/abs/2508.09479)。3 篇投稿 ICLR workshop，**1/3 超过人类平均接收阈值**——第一篇端到端通过 peer review 的 AI 论文 |
| **AI co-scientist** | Google DeepMind | 2025-02 | 多 agent hypothesis generation | 基于 Gemini 2.0；已联合 Stanford 验证三个生物医学场景（AML 药物 repurposing、肝纤维化、抗微生物耐药） |
| **Agent Laboratory** | Schmidgall (JHU) | 2025 | 三阶段 pipeline（lit review / experiment / report）| 通过 AgentRxiv 实现 agent 间上传/接力；用 o1/gpt-4o/deepseek-chat 做底层 |
| **AI-Researcher** | HKUDS | 2025（NeurIPS 2025 Spotlight）| 端到端 + 多域评估 | 三阶段（Resource Collector/Filter/Idea → Design-Impl-Val-Refine → Writer）；CV/NLP/DM/IR 四域评估 |
| **PaperBench** | Stanford / OpenAI | 2024-12 | **不是 agent，是 benchmark** | 复现 20 篇 ICML 2024 论文，最佳 agent 21% 准确率 |
| **MLGym** | Meta | 2025-02 | **benchmark + framework** | 13 个 open-ended AI 研究任务；评测 Claude-3.5/Llama-3.1/GPT-4o/o1/Gemini-1.5 |
| **MLE-bench** | OpenAI | 2024-10 | **Kaggle 工程 benchmark** | 75 个 Kaggle 比赛；o1 拿 16.9% 比赛金牌（超过 Kaggle 人类 median）|
| **ScienceAgentBench** | OSU-NLP | 2024-10 | **科学代码 benchmark** | 102 任务来自 44 篇 paper；最佳 agent 32.4% 独立 / 42.2% (o1-preview + self-debug) |
| **CycleResearcher** | aiming-lab | 2025-10 | 自动化反馈 + 迭代 refinement | 用 MLE-bench 验证；核心机制 = 把 review feedback 当 first-class 信号 |

### A.2 赛道拥挤程度判断

**结论：高，已饱和**。证据：

1. **arXiv 投稿密度**：2025 年 H2 起 `cs.AI` + `cs.CL` 与 "AI Scientist / AI-Researcher / automated research" 相关的月投稿超过 30 篇；awesome-autoresearch 列表已收 50+ 系统。
2. **frontier lab 站位**：Google (co-scientist) + OpenAI (DeepResearch + PaperBench + MLE-bench) + Sakana (v1/v2) + Meta (MLGym) + Anthropic (DeepResearch) + Hugging Face (Karpathy autoresearch space) 全部已入场；学术界 (HKUDS, JHU, OSU, Stanford) 也密集发布。
3. **venue 拥挤**：NeurIPS 2025 D&B 与 Workshops、ICLR 2026 Workshops、ACL/EMNLP 2026 已经为这一方向开辟专门 session。CycleResearcher、Agent Laboratory、MLGym、AI-Researcher 都在抢占 ACL/EMNLP/ICML 2026-2027 的位置。
4. **重复度高**：v1/v2 之间的差异（tree-search vs beam-search）实质上是同一思路的工程迭代；多个 system 都是 "lit review → experiment → write-up" 的模板化实现，差异化只体现在 prompt / orchestrator 的细节。

### A.3 SOTA 真实水平（数字 + 含义）

| 任务 | SOTA | 含义 |
|---|---|---|
| 端到端写一篇 workshop 接收论文 | AI Scientist v2 1/3 超过人类阈值 | "能跑通 pipeline"和"能通过 peer review"之间仍隔一道墙 |
| ICML 主会论文复现 | PaperBench 21% | 复现一篇论文所需的多日专家工作量是当前 agent 的极限 |
| Kaggle ML 工程比赛 | MLE-bench o1 16.9% 金牌 | 短周期 (≤24h) ML 工程任务接近人类 median，但远不及 Kaggle grandmaster |
| 数据驱动科学代码 | ScienceAgentBench 42.2% (o1-preview + self-debug) | 10x 成本才能换 10% 提升，性价比差 |
| 多任务 AI 研究 | MLGym frontier models "能改进 baseline 但不能产生新算法/架构/假设" | 现有模型**没有发现能力**（discovery capability = 0）|
| 迭代改进（feedback loop）| CycleResearcher 在 MLE-bench 上提升 vs baseline | 反馈循环确实是 next step，但 absolute number 仍低 |

**关键观察**：所有 SOTA 数字都落在 20-42% 这个区间——**没有突破 50%**，意味着当前 frontier 模型在"研究"这一任务上仍处于明显早期。

### A.4 典型被接收 / 被拒结果

| 结果 | 系统 | 含义 |
|---|---|---|
| **拒**：AI Scientist v1 三篇全部低于人类阈值 | Sakana | 首次端到端系统级尝试，明确暴露 "code template 依赖" 与 "无 VLM 反馈" 两个结构性短板 |
| **接收**：AI Scientist v2 1/3 超过人类阈值 | Sakana | VLM 反馈 + progressive tree-search 的确补齐了 v1 的部分缺口，但仍是 workshop 级别 |
| **接收**：AI-Researcher → NeurIPS 2025 Spotlight | HKUDS | 学术端到端系统在 NeurIPS 被认可，**意味着 "system paper" 仍可发**；但竞争激烈 |
| **接收**：CycleResearcher → 2025-10 arxiv | aiming-lab | "feedback as first-class" 思路得到曝光，但还未进入 venue track |

### A.5 First-class 贡献需要的形态

从过去 18 个月已接收 / 高引工作中可归纳出四类**可重复的高价值贡献形态**：

1. **新 benchmark**（最大众）
   - PaperBench / MLGym / MLE-bench / ScienceAgentBench 全部是这一形态
   - 必备组件：≥50 task + 跨模型评测 + hierarchical rubric + 与原作者 co-author 校验
   - 风险：被同质化（已有 4-5 个相似 benchmark）
   - **窗口仍开但正在关闭**——需要非重复维度

2. **新能力证明**（system paper）
   - Sakana v1/v2、Agent Laboratory、AI-Researcher 走这条线
   - 必备组件：open-source + 端到端可跑 + 至少 1 个 case study 超过人类基线
   - 风险：算力门槛（论文复现 / MLE-bench 需要 100+ GPU-hours）

3. **失败分析 / failure taxonomy**（最稀缺）
   - 目前**没有** system-level 的工作把"agent 在长周期研究中的失败"做实证 taxonomy
   - 个别工作（AI Scientist v2 §failure cases）只列举 3-5 个例子，没有 grounded framework
   - **窗口最大**

4. **校准与偏差实证**（emerging）
   - CycleResearcher 涉及 review feedback 校准但没量化偏差
   - JudgeBench、CoBBLEr、KIEval 等 LLM-as-judge benchmark 与 auto-research 部分重叠但**没有专门针对 AI 研究产出的 reviewer**

### A.6 文献明显空白（基于外部景观推断）

| 空白 | 现有工作 | 缺口 |
|---|---|---|
| **长周期真实研究过程 trace 数据** | Sakana v2 / AI-Researcher 公开了 pipeline 代码但**不公开 trace**（intermediate decisions / fold events / 失败回滚）| 没有公开数据集可以"重放"一次研究过程 |
| **自动研究失败模式 taxonomy** | 个别论文散落列举（calibration paradox、context drift、cognitive loop）但**没有统一 framework** | 没有 "auto research failure modes v1" 这种 ground-truth taxonomy |
| **AI review 的校准** | JudgeBench 评测 LLM-as-judge 但**针对一般 NLI 任务**；CoBBLEr、KIEval 测 confidence / bias 但**不在 auto-research context** | 自动研究产出的 AI 评审 vs 人类评审的 calibration 缺口巨大 |
| **Stop / pivot 的决策边界** | Karpathy autoresearch 公开提到三种失败（infinite loop / premature convergence / tangent），但**没有量化触发条件** | "什么时候该 stop / pivot / continue" 是 LLM-on-LLM loop 的核心，没人 formali |
| **跨模型 / 跨 provider 偏差** | auto-judge 工作有 prompt-format confound 记录，但**没有跨 4-5 家 provider 的对照实证** | G2 N=30 falsification 暴露的 cherry-pick 问题在文献里没看到同等级证据 |

---

## Part B · 本地资产（只读扫描）

### B.1 auto-research（本仓库 · 重点扫描）

**项目本质**：portfolio-level 自动化研究框架，跑过 P11 (inner monologue) / P12 (judge calibration) / P1+P2 (evidence ledger) / P7 (signal fusion) / P8 (market calibration) / Direction A (unified anchoring) 多条线。

#### B.1.1 Trace 数据资产

| 文件 | 行数 | 内容 | 独特性 |
|---|---|---|---|
| `state/iteration_log.jsonl` | 3 行 | 3 个里程碑（M0-M1 / M2-M3 / M5-M7 config）+ outcome + next | 短，仅 portfolio-level |
| `state/findings.jsonl` | 8 行 | portfolio 决策 + G3 dual-ledger crosswalk + G2 N=6/30 实证 + Direction A FOLD verdict | **含证伪决策记录**（G2 N=30 FALSIFIED）—— 这是公开文献里几乎没有的资产 |
| `state/progress.json` | 17 events | 多轨推进 + natural_deli 触发 + m9 fold + 5-persona review verdicts + cross-project ROI | **事件类型最丰富**：含 5-persona review scores、fold verdict、cherry-pick 揭露、cross-provider bias |
| `state/directions_tried.json` | 4 directions | p11_mainline_repair (closed) / p12_judge_calibration / p1_p2_evidence_structured_decision | 决策路径固化 |
| `state/task_spec.md` | 80+ 行 | task spec 含 stale_count / 5-persona / fold 规则 | AutoResearch protocol 的 first-class 文档 |
| `logs/heartbeat.jsonl` | 1 行 | portfolio init | 短 |
| `logs/orchestrator.jsonl` | 1 行 | portfolio reorganization | 短 |
| `logs/work.jsonl` | 1 行 | roadmap written | 短 |
| `logs/p12_m{2,3,4,5b}_run.log` | 4 个 run | P12 阶段 run log | P12 全过程 |

**核心判断**：
- portfolio-level trace 集中在 progress.json（17 events）+ findings.jsonl（8 决策）
- 真正长的是**P11 与 Direction A 的实验数据**：
  - `legacy/p11-closed-v5-mimo/experiments/` 内有 `p11_inner_monologue` / `p11_no_think` / `p11_pure_analysis` 三个 ablation 实验目录
  - `legacy/p11-closed-v5-minimax-m3/experiments/mc-2026-07-01-inner-monologue/raw-data/` 跨 ISPACE / LANDSPACE / SPACETIMETECH / LONGHU / VANKEE / ZHONGHAI 六场景 × 3 条件 × qwen & non-qwen 共 30+ 个 raw-data 子目录——**这是公开文献里没有等价数据集的 agent-judge 对照数据**

#### B.1.2 5-persona review 实证证据（来自 progress.json）

- **P12 M8**：median=3.0 → fold_into_p1_p2
- **P1+P2 M9**：median=4.0 → fold_into_p12（评分 [3,3,4,5,5]）
- **P8 M1.5**：median=5.0 → research_grade_acceptable
- **P7 M1**：median=5.0 → research_grade_acceptable
- **Direction A 1-page**：median=4.5 < 5.5 → FOLD（评分 [4,6,4,5,N/A,4]）
- **Joint methods paper (6-persona)**：median=4.0 < 4.5 → FALLBACK
- **G1 (PA-degrades)**：median=4.5 < 5.5 → FAILED as standalone
- **Cross-provider bias signal observed 3 times**：R6 (minimaxi.com MiniMax-M3) 评分比 paratera 端 MiniMax-M3 高 +1.0

#### B.1.3 Fold chain 决策纪律

证据序列：
1. m9_p1p2_fold_into_p12_verdict → P1+P2 fold into P12
2. direction_a_5persona_review_FOLD → Direction A fold by review
3. direction_a_mechanism_experiment_FOLD_data → Direction A fold by mechanism experiment
4. g3_methods_paper_outline_COMPLETE → 唯一 active paper 目标

**证伪决策纪律**：G2 N=30 falsification 是核心证据——
> G2 N=6 (n=6) delta=-3.67 CI [-4.0,-3.0] → G2 N=30 (n=30) delta=-0.16 CI [-0.35,+0.02]，**前 6 个 sample_id 是 cherry-picked**，calibration paradox 在 N=30 下消失。

**独特性**：这是公开文献中**罕见的自我证伪 trace**（不是 single-shot finding，而是先 PASS 后 FALSIFIED 的完整记录）。

#### B.1.4 auto-research 作为论文资产的评估

| 维度 | 评分 | 说明 |
|---|---|---|
| 资产独特性 | ★★★★★ | 长周期 trace + 证伪决策 + 跨模型/跨 provider 对照数据，公开文献无等价 |
| 可重现性 | ★★★★ | state 文件全部 jsonl + markdown，但**代码未充分开源** |
| 与 AI auto research 主线契合度 | ★★★★★ | 本身就是 auto research system 的真实运行 trace |
| 失败模式覆盖 | ★★★★ | cherry-pick / cross-provider bias / fold chain / 5-persona review 阈值 |
| 外部锚点 | ★★ | 缺少与 PaperBench / MLE-bench 的对照 |

### B.2 其他本地项目（README 一句话 + 是否可作 AI auto research 论文资产）

| 项目 | 一句话定位 | 论文资产潜力 |
|---|---|---|
| **Marginalia** | 文档级批注记忆系统，AI 助手驱动的知识管理协议 | ★★★——是 agent 长期记忆 / 知识沉淀的 protocol；可作为 AI 研究 agent 的 memory layer 实证 |
| **PaperMirror** | (无 README，跳过) | ?——需 ls 后判断 |
| **mvp-net-agent** | DesignArena Builder 机制的全栈 MVP 生成 Prompt skill | ★——与 AI auto research 无直接关联 |
| **flow-island** | 智能墨水屏伴侣，AI 语音分任务+四象限 | ★——产品项目，无研究价值 |
| **0ref** | 引用资源聚合目录（含 MetaGPT / BettaFish / claude-mem / autogen / claude-code 等 50+ repo）| ★★★——可作为 auto research 工具栈的**baseline comparison 资产** |
| **myskill** | (无 README，跳过) | ? |
| **cds-keyperson** | CDS M4 S4 role realism 实验 | ★★——keyperson 决策数据可作 LLM-as-judge 校准的 case |
| **evolution-medical-ai** | AI 驱动药物研发助手 MVP，覆盖 WP1-17 | ★★——领域知识 pipeline，但与 auto research 不直接 |
| **Stock-Claw-OS** | AI 投资研究助理，多分析师人格 + 长期记忆 | ★——产品项目 |
| **Policysim-v0.2** | 大型 NestJS + Vue 政策仿真系统，含 MC 仿真、AI 决策、OSINT、prompt 管理 | ★★★★——**多智能体仿真决策系统**，是 AI research agent 决策验证的天然 testbed；docs/SimulationTest/ 含 mc-2026-02-19 三模型（glm5/kimi/minimax）× 两 phase × 6 场景的 raw runs，**与 P11 ISPACE/LANDSPACE/SPACETIMETECH 六场景高度可比** |
| **policysim-v0.1** | Vue 3 + TS + Vite 模板 | ★——模板，无研究价值 |
| **policysim-v0.1-tsinghua** | Vue3 + Go-zero 政策仿真 v2.0 | ★★——基础设施，docs/investigations/ 含 d=1.19 mc-2026-05-05 清华路径论文数据 |
| **policysim-research-Tsinghua** | 多智能体政策仿真（目标 Nature Computational Science / PNAS）| ★★★★——**Plan A 280 runs 已就位**（4 模型 × 2 条件 × 35 runs），是 AI agent 仿真能力的真实验证资产 |
| **PolicySimulation** | (无 README，跳过) | ? |
| **cds4worldcup** | CDS × 2026 FIFA 世界杯路径空间实验 | ★★★——**真实结算锚**（factor ledger 与 settlement 配对），可作 AI auto research 的 calibration 外部锚 |
| **cds4polymarket** | Polymarket 量化分析引擎，AI 驱动报告 | ★★★——同样有真实结算锚，但 G3 已确认 17-round AB-test xlsx 无 predicted_p 列 |

### B.3 资产组合的综合判断

本地资产最强组合是 **auto-research trace + Policysim-v0.2 多智能体仿真数据 + cds4worldcup 真实结算锚**：

- auto-research 提供**长周期决策 trace**（独一无二的"自我证伪"数据）
- Policysim-v0.2 与 policysim-research-Tsinghua 提供**多智能体仿真真实数据**（mc-2026-02-19 与 mc-2026-05-05 两套）
- cds4worldcup 提供**真实结算外部锚**（factor ledger + settlement）

**auto-research 自身 trace 是"过程数据"（process-level），Policysim / cds4worldcup 是"结果数据"（outcome-level with ground-truth settlement）**——这两层组合形成 end-to-end auto-research 论文的最强差异化壁垒。

---

## Part C · 候选 Paper Claims

> 三个 claim 按 ROI 排序。每个含 (claim, 证据, 天花板 venue, 与已有工作的差异点)。

### C1 · 长周期真实研究过程 trace + Failure Taxonomy 实证（高 ROI）

- **Claim**：对 30+ 个真实长周期（≥30 天）自动化研究项目的 trace 进行实证聚类，可得出 5-7 个稳定的 failure modes（如 infinite-search loop / premature-convergence / cherry-pick winner / cross-provider judge drift / cost explosion / scope-creep / fold-after-replication），并能给出每种 mode 的**可观测签名**（heartbeat 间隔 / log pattern / cost trajectory / 评审者分歧度）。
- **所需证据**：
  - auto-research state/iteration_log.jsonl + state/progress.json + state/findings.jsonl（~30 events，**已就位**）
  - legacy/p11*/experiments/ 内的 raw 实验数据（**已就位**）
  - 需要再扫 5-10 个外部开源 auto-research 项目的 trace（如果存在）；如不存在则以本地 1 个项目 + 公开 benchmark 失败案例（Sakana v1 三篇被拒 / PaperBench 21% / MLE-bench 16.9% / ScienceAgentBench 32.4%）凑数
  - 一套 taxonomy 的 inter-rater agreement（≥2 名独立 raters 对 trace 打 mode，κ ≥ 0.6）
- **天花板 venue**：NeurIPS 2026 Datasets & Benchmarks / ICML 2026 Workshop on AutoML / ACM TiiS  
- **差异化**：CycleResearcher / Sakana / AI-Researcher 都**不公开 trace**；PaperBench / MLE-bench 只评测 output 不评测 process；**这是 process-level benchmark 的空白**
- **诚实评估**：争取度 35-45%（D&B track）；ROI 高但需要额外 5-10 个项目 trace 的外部数据
- **对应 `meta-question-recalibration` §4.3 S3 Verification-as-Reasoning**：Q1/Q3 ✅，Q2 需补跨域（这正是 C1 想补的）

### C2 · Auto-Judge 跨模型跨 provider 偏差实证（高天花板）

- **Claim**：在 N=30 paired LLM-as-judge 评估上，**第二 judge (openrouter gpt-oss-120b) 与第一 judge (paratera deepseek-v4-pro) 的评分差存在系统性方向反转**——平均 delta 在 N=6 时为 -3.67，N=30 时变为 +0.34，意味着 N≤10 的样本量普遍不可靠。这与文献中 JudgeBench / CoBBLEr / KIEval 的 N=50-200 形成方法论冲击。
- **所需证据**：
  - auto-research findings.jsonl 中的 G2 N=6 / N=30 完整记录（**已就位**）
  - cross-provider bias 3 次重复观察（R6 minimaxi vs R3 paratera）的实证（**已就位**）
  - 需要扩展到 **≥4 provider × ≥3 judge family × ≥3 task type** = 36 cells，N=30/cell = 1080 judge calls
  - 与 CycleResearcher (MLE-bench) / Sakana v2 (ICLR workshop) 的 reviewer-side 偏差对照
- **天花板 venue**：ACL 2027 Findings / EMNLP 2027 Eval Workshop / NeurIPS 2027 D&B
- **差异化**：CoBBLEr 测 confidence / bias 但**不在 auto-research 上下文**；KIEval 测 knowledge 偏差但**不跨 provider**；**本工作的实证跨 4-5 家 provider** 是文献缺口
- **诚实评估**：争取度 25-35%（ACL Findings）；与 G3 dual-ledger bridge methods paper **直接同构**，可作为其 evaluation 章节扩展
- **风险**：N=30 paired 在多次 reviewer 看来仍"小样本"，需要公开数据集补到 N=100 才稳

### C3 · 5-persona fold-chain 方法论（基础工程贡献）

- **Claim**：对 AI auto research 方向决策，采用"5-persona 异质 judge review + pre-registered mechanism experiment"的双重 gate，比传统 single-reviewer 或 multi-vote 更能避免 LLM-on-LLM circularity。证据来自 auto-research 6+ 次 5-persona review + 1 次 pre-registered mechanism experiment（Direction A N=256+N=128 = 384 calls，机制假设被实证 falsify）的完整 fold chain。
- **所需证据**：
  - auto-research 6 个 5-persona review verdict（已就位）
  - Direction A mechanism experiment 数据（已就位，295 ok records）
  - 需要 1-2 个外部项目复现 fold chain（如对 cds4polymarket 的 5-persona review 跑一遍，验证 protocol 的 cross-project 适用性）
  - pre-registration protocol 的 specification document
- **天花板 venue**：EMNLP 2027 Eval Workshop / ACL 2027 Workshop on Research Methods / NeurIPS 2027 Workshop on AI for Science
- **差异化**：CycleResearcher 提 review feedback loop 但**没量化 reviewer 异质性**；Agent Laboratory / AI-Researcher 都没把 review 协议化；**这是研究方法论的空白**
- **诚实评估**：争取度 30-40%（workshop / short paper）；天花板较低（C 类 PARTIAL，与 `first-principles-redesign` §4 中 B 类同等）

### C-排序的诚实提醒

- 三个 claim 都在 `meta-question-recalibration-2026-07-17.md` §4.3 的 first-class 候选池**之外**：
  - 既有 best candidate S1 Survey（满足 Q1/Q2/Q3）+ S3 Verification-as-Reasoning + P11→E2 IEEE 短文
- 本 W3 的 3 个 claim 是**对"AI auto research"作为单独方向**（而非用 auto research 做某具体应用）的候选
- 若 auto-research portfolio 仍坚持"主论文 S1 Survey + S3 Verification-as-Reasoning + P11 IEEE 短文"的三线，C1/C2/C3 可作为**配套 / 配套衍生**：
  - C1 → S3 Verification-as-Reasoning 的方法论章节
  - C2 → 任何 LLM-as-judge 章节的补强
  - C3 → S1 Survey 中"methodology limitation"的小节

---

## 附录 · 引用与可验证锚点

### 外部景观引用

- AI Scientist v2：https://arxiv.org/abs/2504.08066 ；失败案例分析 https://arxiv.org/abs/2508.09479
- Google AI co-scientist：https://storage.googleapis.com/coscientist_paper/ai_coscientist.pdf
- Agent Laboratory：https://github.com/SamuelSchmidgall/AgentLaboratory
- AI-Researcher：https://github.com/HKUDS/AI-Researcher
- PaperBench：https://openai.com/index/paperbench/
- MLGym：https://arxiv.org/abs/2502.14499
- MLE-bench：https://openai.com/index/mle-bench/
- ScienceAgentBench：https://arxiv.org/abs/2410.05080
- CycleResearcher：https://arxiv.org/abs/2511.19467
- awesome-autoresearch：https://github.com/AI4Scientist/awesome-autoresearch
- Karpathy autoresearch 公开批评（"infinite loop / premature / tangent" 三种 failure）

### 本地资产锚点

- `~/Documents/GitHub/auto-research/state/progress.json` 17 events 含完整 fold chain
- `~/Documents/GitHub/auto-research/state/findings.jsonl` G2 N=6 / N=30 falsification 记录
- `~/Documents/GitHub/auto-research/state/directions_tried.json` 4 个方向决策路径
- `~/Documents/GitHub/auto-research/legacy/p11-closed-v5-minimax-m3/experiments/mc-2026-07-01-inner-monologue/raw-data/` 跨 6 场景 × 3 条件 × qwen/non-qwen
- `~/Documents/GitHub/Policysim-v0.2/docs/SimulationTest/mc-2026-02-19.migrated/` 三模型 × 两 phase × 6 场景
- `~/Documents/GitHub/cds4worldcup/` factor ledger + settlement 真实外部锚

### 内部一致性

- 与 `docs/investigations/meta-question-recalibration-first-class-paper-2026-07-17.md` §4.3 既有 first-class 候选池（S1 / S3 / P11 IEEE）**不冲突**，作为"AI auto research 单独方向"的互补候选
- 与 `state/directions_tried.json` 当前 `selected_next: p12_judge_calibration` + `selected_medium_term: p1_p2_evidence_structured_decision` **不冲突**，作为方向 G3 dual-ledger bridge 的衍生 paper 候选

---

**完。W3 不动 w1/w2。**