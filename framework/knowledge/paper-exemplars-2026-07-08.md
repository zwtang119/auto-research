# Paper Exemplars — 质量标杆参照库

> Created: 2026-07-08
> Scope: framework-level. **Purpose**: when evaluating any new paper direction in this portfolio, compare against these 7 exemplars — they define the bar / style / depth the human engineer requires.
> Source: 7 PDFs provided by the human engineer 2026-07-08, archived at `/Users/tangzw119/Downloads/` (PDFs themselves not committed — this wiki records the citation + extraction + pattern).
> Use: every `docs/investigations/*top-journal*.md` and every per-paper `paper/outline.md` MUST cite this file as the bar reference.

---

## 0. How to use this file

| When | Action |
|------|--------|
| Starting a new paper outline | Read §1-§3, pick the closest exemplar type, mirror its structure/depth |
| Evaluating a paper direction | Check the direction against §4 "the 7-criterion bar"; any direction failing ≥3 criteria is below standard |
| Reviewing a draft | Compare draft depth to the exemplar's empirical-evidence depth (§2 N + ablation + cross-model) |
| Choosing venue | Use §3 venue table; align page count + structure to the venue's convention |

**Iron rule**: any verdict about "this paper is workshop-grade / Findings-grade / main-track-grade" MUST cite this file's §4 bar. No more verdict-without-anchor (per `optimization-plan-2026-07-07.md` R9 + PIT-501).

---

## 1. The 7 exemplars — one-line each + type

| # | Short name | Type | Venue-style | Pages | Why here (what facet of "bar" it sets) |
|---|---|---|---|---|---|
| E1 | TreeReview (2506.07642v2) | LLM 应用研究（peer review 框架） | ACL/EMNLP long paper | 32 | **深度**: hierarchical tree of questions + dynamic expansion + ICLR/NeurIPS 派生 benchmark；中科院+港大+清华+港科大广州——**与本 portfolio 同区域作者群**的示例 |
| E2 | LLM-Powered Swarms (2506.14496v2) | LLM vs 经典方法比较研究 | IEEE conference short | 8 | **比较深度 + 诚实负面结果**: LLM Boids 比 classic 慢 300× + ACO 更高 accuracy 但 100× 慢；8 页 IEEE 格式是短文标尺 |
| E3 | AsyncThink / Agentic Organization (2510.26658v1) | LLM 推理范式创新 | 主会议长文 | 22 | **范式 contribution**: organizer-worker async thinking + RL 优化 thinking 结构 + 28% latency ↓ + 跨任务泛化；Microsoft Research |
| E4 | Scaling Agent Systems (Google+MIT) | 实证 scaling-law 论文 | 主会议长文 | 38 | **实证标尺**: 180 configs × 5 architectures × 3 LLM families × 4 benchmarks + R²=0.524 predictive model + 3 dominant effects quantified；Google Research + DeepMind + MIT |
| E5 | Tree of Thoughts (NeurIPS 2023) | LLM 推理框架经典 | NeurIPS main | 14 | **经典范式**: ToT generalizes CoT, self-evaluate + backtrack + lookahead；Game of 24 GPT-4 CoT 4% → ToT 74%；Princeton+Google DeepMind |
| E6 | Distributed Maritime Operations + Unmanned Systems (NPS 2018) | 军事应用 Capstone | NPS 系统工程 capstone | 199 | **应用标尺 + 域**: NPS 海军研究生院 capstone，分布式海上作战 + 无人系统战术——**说明用户需要的安全/国防应用方向** |
| E7 | Recognized Information Picture for DMO (NPS 2025) | 军事应用硕士论文 | NPS thesis | 145 | **应用标尺 + 信息融合**: 2025-03 NPS 硕士论文，分布式海上作战的"识别信息图"——**与 P07 signal-fusion + P11 应急决策方向同域** |

---

## 2. Per-exemplar deep extraction (the bar in concrete terms)

### E1 — TreeReview (2506.07642v2): "深度 LLM 应用研究"标尺
- **作者**: Yuan Chang et al., 中科院国家科学图书馆 + 港大 + 清华 + 港科大广州 —— **本 portfolio 同区域作者群**,作者背景与张辉团队可比
- **Contribution**: TreeReview framework — 把论文评审建模为 hierarchical bidirectional QA:root question 递归分解为 leaf sub-questions,leaf-to-root 聚合得最终 review + 动态扩展机制(follow-up question when needed)
- **Benchmark**: 从 ICLR + NeurIPS venues 构造的 full-review-generation + actionable-feedback benchmark
- **方法论深度**: 不是"用 LLM 做评审"——是"把评审过程重新建模为树状 QA + 动态扩展 + 双向聚合"
- ** venue-style**: ACL/EMNLP long paper(32 页含 appendix)
- **对本 portfolio 的启示**: 这是**张辉团队可比作者群**发的 LLM-peer-review 论文——本 portfolio P12 (judge-calibration) 的方向与 TreeReview 同域,但 P12 当前 median=3.0 远低于此标尺。**TreeReview 的树状 QA + 动态扩展是 P12 没有的 contribution 深度**

### E2 — LLM-Powered Swarms (2506.14496v2): "诚实比较短文"标尺
- **作者**: Muhammad Atta Ur Rahman et al., Lakeside Labs GmbH (奥地利)
- **Contribution**: 用 OpenAI Swarm (OAS) 实现 Boids + ACO 的 LLM 版本,与经典版比较;发现 LLM Boids 慢 300×、LLM ACO 在 18 迭代后 accuracy 更高但慢 ~160×
- **诚实负面结果**: 论文标题就是问号("A New Frontier or a Conceptual Stretch?"),结论明说"LLM-based swarms are not yet ready to replace traditional swarms... but they enrich the design space"
- **venue-style**: IEEE conference 8 页(含 appendix + 作者简介)
- **实证深度**: 30 trials × 5 iterations × 3 prompts = 1350 prompts(Boids) + 18 × 3 × 30 = 1620 prompts(ACO);预定义 random seeds + 4-5 metrics(cohesion/separation/alignment/convergence/learning efficiency/stability)
- **对本 portfolio 的启示**: **8 页 IEEE 格式 + 诚实负面结果 = 可接受的 short-paper 标准**。本 portfolio P11 (inner-monologue) 的"PA degrades fidelity"finding 与此同型(负结果 + 比较)——P11 可参照此 8 页格式发短文。**关键**: 论文 honesty(问号标题 + 明说"not ready")是被接受的,不是"必须正面结果" 

### E3 — AsyncThink (2510.26658v1): "范式创新长文"标尺
- **作者**: Zewen Chi, Furu Wei et al., Microsoft Research
- **Contribution**: Agentic Organization 范式 + AsyncThink protocol — organizer 动态分配 sub-queries 给 workers + 合并中间知识 + RL 优化 thinking 结构;28% latency ↓ vs parallel thinking + accuracy ↑ on 数学推理 + 跨任务泛化
- **venue-style**: 主会议长文 22 页
- **对本 portfolio 的启示**: 这是"范式 contribution"标尺——本 portfolio 当前无任何 paper 有此级别的范式创新。P07/P08/P1P2 的"adapter/ledger/brier"都是工程桥接不是范式。**若 portfolio 要冲主会议,需要这种级别的范式贡献**

### E4 — Scaling Agent Systems (Google+MIT): "实证 scaling-law"标尺
- **作者**: Yubin Kim et al., Google Research + DeepMind + MIT
- **Contribution**: agent system 的 quantitative scaling laws——5 architectures × 3 LLM families × 4 benchmarks × 180 configs;predictive model R²=0.524;3 dominant effects(tool-coordination tradeoff / capability saturation at ~45% / topology-dependent error amplification 17.2× vs 4.4×)
- **实证深度**: 180 configs + 标准化 tools/prompts/token budgets 隔离架构效应 + cross-validated R² + 3 quantified effects with p-values
- **对本 portfolio 的启示**: 这是"实证 scaling-law 论文"标尺——本 portfolio 无任何 paper 达此实证规模(P11 N=240 是单 architecture,P12 N=10/6 underpowered)。**实证 scaling 要 180 configs × ≥3 LLM families × ≥4 benchmarks 才达主会议**

### E5 — Tree of Thoughts (NeurIPS 2023): "推理框架经典"标尺
- **作者**: Shunyu Yao et al., Princeton + Google DeepMind
- **Contribution**: ToT generalizes CoT — LM 把推理分解为 thoughts(中间状态)+ self-evaluate choices + lookahead/backtrack;Game of 24: GPT-4 CoT 4% → ToT 74%
- **venue-style**: NeurIPS 2023 main,14 页
- **对本 portfolio 的启示**: "self-evaluate + backtrack"是 ToT 的核心——本 portfolio 的 LLM judge 也是 self-evaluate 但缺 backtrack + lookahead。**ToT 是 LLM-judge 自评的方法论先例**

### E6 + E7 — NPS 军事应用 capstone/thesis: "应用方向"+"信息融合"标尺
- **E6**: "Distributed Maritime Operations and Unmanned Systems Tactical Employment",NPS 系统工程 capstone 199 页,2018-06,**Paul T. Beery + Michael P. Atkinson 指导**——分布式海上作战 + 无人系统战术部署
- **E7**: "The Recognized Information Picture for Distributed Maritime Operations",NPS 硕士论文 145 页,2025-03,**Jeffrey P. Elliott**——分布式海上作战的"识别信息图"(RIP for DMO)
- **对本 portfolio 的关键启示**:
  1. **用户需要的应用方向是安全/国防/应急决策**(NPS = 海军研究生院,DMO = 分布式海上作战)——这与本 portfolio 课题五"应急决策"+ 张辉(JSSR 安全学者)背景一致
  2. **"Recognized Information Picture"(识别信息图)= 信息融合**——E7 直接是 P07 signal-fusion 的军事应用对应物。P07 当前定位为"桥接工具",但它的军事应用对应物(E7)是 145 页硕士论文——**说明这个方向有应用研究价值,只是 P07 当前没做出来**
  3. **NPS thesis/capstone 是被接受的 publication venue for this community**——不是 NeurIPS/ACL,但对学生 + 安全学者是 legitimate venue。本 portfolio 张辉团队可比 NPS capstone 投 NPS-style venue

---

## 3. The 7-criterion bar (extracted from the 7 exemplars)

任何本 portfolio 产出的 paper 要被接受为"达标",必须满足以下 7 条中**至少 5 条**:

| # | Criterion | E1 | E2 | E3 | E4 | E5 | E6 | E7 | 本 portfolio 哪些达标 |
|---|---|---|---|---|---|---|---|---|---|
| B1 | **Contribution 深度**(范式创新或深度框架,非工程桥接) | ✅ tree QA | ✅ 比较+负结果 | ✅ async paradigm | ✅ scaling laws | ✅ ToT framework | ✅ DMO 应用 | ✅ RIP 框架 | 无(P07/P08 是桥接) |
| B2 | **实证规模**(N + 多 architecture + 多 LLM family + 多 benchmark) | ✅ ICLR/NeurIPS benchmark | ✅ 30 trials × 2 algorithms | ✅ 数学推理 + 跨任务 | ✅ 180 configs × 3 families × 4 benchmarks | ✅ 3 tasks + GPT-4 | ✅ 战术场景 | ✅ DMO case | P11 N=240 单 arch;P12 N=10/6;n→ |
| B3 | **外部锚点 / 非-LLM ground truth**(human gold / 真实结算 / venue reviewer) | ✅ ICLR/NeurIPS 真实 review | ✅ classic algorithm 作 ground truth | ✅ 数学答案 | ✅ 4 benchmark 真实答 | ✅ Game of 24 答案 | ✅ 真实 DMO 场景 | ✅ 真实海上情报 | 全无 |
| B4 | **Honesty**(诚实负面结果 + 边界声明) | ✅ | ✅✅ 标题问号+"not ready" | ✅ | ✅ p-values | ✅ | ✅ | ✅ | P11 部分(PA degrades) |
| B5 | **Public release**(code/data public + reproducible) | ✅ | ✅ GitHub link | ? | ? | ✅ GitHub | N/A(NPS) | N/A | 全无 |
| B6 | **Venue alignment**(格式 + 页数 + style 对齐目标 venue) | ✅ ACL long | ✅ IEEE 8p | ✅ 长文 | ✅ 长文 | ✅ NeurIPS | ✅ NPS capstone | ✅ NPS thesis | 无 |
| B7 | **Author/applicability match**(作者群 + 应用域与团队可比) | ✅ 中科院+港大(本团队可比) | ✅ | Microsoft | Google+MIT | Princeton | NPS(本团队可比) | NPS(本团队可比) | 张辉团队可比 E6/E7 |

**7 条中至少 5 条达标 = "可发表";<5 = 不达标**。

---

## 4. Per-exemplar structural template (for new paper drafts)

### E1/E3/E5-style(范式框架长文,ACL/NeurIPS long)
```
1. Abstract (problem + contribution + 1 key result)
2. Introduction (problem + why hard + contribution list + roadmap)
3. Related Work (≥3 prior paradigms + 本工作 differs)
4. Method (framework formal + algorithm + 1 figure)
5. Benchmark construction (从真实 venue 派生)
6. Experiments (main result + ablation + cross-model + efficiency)
7. Analysis / Discussion (failure cases + boundary)
8. Conclusion + Limitations + Future Work
9. Appendix (prompts + hyperparams + additional results)
```

### E2-style(诚实比较短文,IEEE 8 页)
```
1. Abstract (问题 + 比较对象 + 1 句诚实结论)
2. Introduction (领域 + 比较 motivation + roadmap)
3. Background (经典方法 + LLM 方法)
4. System Description (硬件 + 软件 + LLM + 算法)
5. Evaluation (case study 1 + case study 2 + metrics table + figure)
6. Discussion (prompt engineering role + new frontier or fad?)
7. Conclusion (诚实 + future hybrid)
8. Appendix (prompts + author bios)
```

### E6/E7-style(应用研究 capstone/thesis,NPS-style)
```
1. Executive Summary / Abstract
2. Background (operational context — DMO / 应急 / 海上)
3. Literature Review (military + technical)
4. Problem Statement (operational gap)
5. Methodology / System Design
6. Scenario / Case Study
7. Analysis (results + limitations)
8. Recommendations / Future Work
9. Appendices (sensor data + simulation outputs)
```

---

## 5. Cross-references

- `framework/schemas/experiment-pitfalls.md` PIT-007 (N<30 不是 claim) — 本文件 B2 实证规模的对应 PIT
- `docs/investigations/optimization-plan-2026-07-07.md` R9 (external anchor required) — 本文件 B3 外部锚点的对应规则
- `docs/investigations/per-paper-top-journal-2026-07-08.md` — 前 5-paper verdict 用的 6-criteria 表,本文件 §3 的 7-criterion bar 是其精化版(+ B1 contribution 深度 + B7 author match)
- `docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md` — verdict-without-external-anchor diagnosis,本文件 B3/B5 是 fix
- 张辉团队背景: JSSR 主编(安全学者),课题五 = 应急决策——E6/E7 NPS DMO 是同域应用标尺

---

## Appendix A: 7 PDF extraction metadata

| PDF | Pages | Words extracted | Saved text |
|-----|-------|-----------------|------------|
| 2506.07642v2.pdf (TreeReview) | 32 | 5504 | /tmp/pdf-extract/2506.07642v2.txt |
| 2506.14496v2.pdf (LLM Swarms) | 8 | 4159 | /tmp/pdf-extract/2506.14496v2.txt |
| 2510.26658v1.pdf (AsyncThink) | 22 | 3902 | /tmp/pdf-extract/2510.26658v1.txt |
| DISTRIBUTED MARITIME OPERATIONS... (NPS E6) | 199 | 40087 | /tmp/pdf-extract/DISTRIBUTED_MARITIME_OPERATIONS_AND_UNMANNED_SYSTEMS_TACTICAL_EMPLOYMENT.txt |
| THE RECOGNIZED INFORMATION PICTURE... (NPS E7) | 145 | 25177 | /tmp/pdf-extract/THE_RECOGNIZED_INFORMATION_PICTURE_FOR_DISTRIBUTED_MARITIME_OPERATIONS_1.txt |
| Towards a Science of Scaling Agent Systems | 38 | 12525 | /tmp/pdf-extract/Towards_a_Science_of_Scaling_Agent_Systems.txt |
| Tree-of-Thoughts.pdf | 14 | 6180 | /tmp/pdf-extract/Tree-of-Thoughts.txt |

Extracted via `pdf.py extract.text` (pdf skill, 2026-07-08). PDFs themselves live in `/Users/tangzw119/Downloads/` and are NOT committed to the repo (per .gitignore + storage discipline). This wiki file is the durable record.
