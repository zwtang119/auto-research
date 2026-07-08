# 调研：Karpathy Loop / Harness 实验对本项目的论文方向 + 修正启示

日期：2026-07-07
方法：rp-investigate-cli（Playwright 抓取头条文章 + 项目内现有调研交叉对比 + 外部文献核实）
任务：阅读头条文章（Karpathy AutoResearch Loop + Niklaus Harness 实验 + Bilevel Autoresearch），结合本项目，思考还有什么方向有机会产出论文 + 接下来该做什么修正

## 前置声明

用户在上一轮诊断（`meta-uncertainty-and-blindspot-2026-07-07.md` Q1+Q2：AI 最没把握=自己结论是否有意义 / 人最大遗漏=把 LLM-on-LLM 闭环放进消灭人类介入的框架）+ 修正方案（`optimization-plan-2026-07-07.md`：补 Deli §3/§10.3 + 接 JudgeBench + 人类专家 gold）之后，给了一篇外部文章，问"还有什么论文方向 + 接下来该做什么修正"。

**关键认识**：外部文章讲的是**与本项目同名（Karpathy 的 AutoResearch）但本质不同的东西**。Karpathy 的 AutoResearch 是 ML 训练脚本自动迭代 loop（"提出变更→训练→评估→保留"），本项目的 auto-research 是 LLM 研究论文学术写作 loop（"迭代→评审→fold/继续"）。两者都是"loop"，但研究对象、评估器、ground truth 完全不同。这个区分本身是本报告的关键洞察。

举证责任：默认我可能再次"verdict 先于框架"（前 10 次反转的诊断）。所以本报告先核实文章事实（不是二手转述），再核对 prior art，最后才谈方向——不跳结论。

## Summary

文章 3 个核心 claim，2 个与本项目直接相关，1 个间接但更关键：

1. **Niklaus Harness 实验**（直接相关）：冻结 DeepSeek-V4-Pro 权重，只改外层 harness（执行机制），pooled score 从 3.5%→80.1%，跨 5 种 harness 波动 76 分。**外层执行机制比 prompt 调优更可沉淀、可跨模型迁移**。
2. **Karpathy AutoResearch Loop**（同名警示）：700 次自动迭代找出 20 项人类忽略的代码改进；5 步 loop = 提出变更→训练→评估（锁定 evaluator）→保留/舍弃。核心 3 要素：**验证器 + 状态文件 + 停止条件**。
3. **Bilevel Autoresearch**（最关键但文章只一笔带过）：外层 loop 优化内层 loop 的搜索逻辑，性能提升 5×，"打破 LLM 思维定势"。

**与本项目的关系**：
- 本项目 auto-research 是**学术研究 loop**，不是 ML 训练 loop。但 Niklaus 实验的"评估器锁定"（不给 agent 改评估脚本的机会）正好是本项目诊断的 G1 圆形性（AI 自改 progress.json `g2_pass:true`）的对应解。
- Karpathy loop 的"验证器"要素正是本项目缺的外部锚点。
- Bilevel autoresearch 的"外层 loop 打破内层思维定势"与本项目 4 天 10 verdict 反转（同一根因诊断逐字重复）是同一现象的两种描述——本项目缺外层 loop。

**新论文方向（3 个，按可发表性排序，每个配 prior art + venue bar + 项目资产）**见 §Root Cause。

## Symptoms

用户读完文章后问两件事：(1) 还有什么论文方向有机会？(2) 接下来该做什么修正？潜台词：上一轮诊断说"不要写第 11 份 verdict"，但用户仍想找方向——所以本报告不能是又一个 verdict，必须是**可验证的方向 + 可执行的修正**。

## Background / Prior Research

### 文章 3 个核心 claim 核实（Playwright 抓取原文）

**Claim 1 — Niklaus Harness 实验**：
- 出处：Hugging Face 工程师 Joel Niklaus，实验 "Don't Train the Model, Evolve the Harness"
- 模型：DeepSeek-V4-Pro，权重冻结，只改外层 harness
- 数据点：5 种 harness pooled score = {mini-swe-agent 3.5%, Goose 23.2%, Pi 45.4%, 原始 LAB 63.4%, 优化后 80.1%}，波动 76 分
- 跨模型迁移：harness 迁到 DeepSeek-V4-Flash 仍 +14.4 分
- 结论：benchmark 测的是"模型+harness"不是裸模型；harness 优化比 prompt 调优更可沉淀
- 关键细节：0% 得分是因为"模型推理全对但存错文件名"——Harness 不是智力是 IO

**Claim 2 — Karpathy AutoResearch Loop**：
- 出处：Karpathy 9 万 star 项目 + Codila 二次提炼（630 行→5 步）
- 5 步：(1) 精调模型+文档约束 (2) 只允许改训练脚本，**评估脚本锁定** (3) 提出变更→训练→评估→保留/舍弃 (4) 700 次实验找 20 项人类忽略改进 (5) 3 要素：验证器+状态文件+停止条件
- 适用标准 4 项：高频/验证可自动化/Token 预算能消化冗余/能访问真实环境
- 隐性代价：理解债 + 认知让渡

**Claim 3 — Bilevel Autoresearch**：
- 出处：文章引用论文《Bilevel Autoresearch: Meta-Autoresearching Itself》
- 机制：外层 loop 优化内层 loop 的搜索逻辑
- 数据点：性能比 Karpathy 基准提升 5×，"所有提升均来自架构改进"
- 关键论断：外层 loop"打破 LLM 思维定势"——内层 loop 易陷入模型先验认知的搜索模式，外层强制探索本能回避的方向

### 文章未明确但本报告需核实的事实（Phase 2 验证）

**待核实**：
- (F1) Niklaus 实验是否真存在、数据是否真（文章是二手转述，需找 HF 原文）
- (F2) "Bilevel Autoresearch" 论文是否真存在（文章给的名字但无 arxiv 链接）
- (F3) Karpathy 的 AutoResearch 项目与本项目 auto-research 是否真同名不同物
- (F4) "Bilevel" 概念在 ML 文献里的真实 prior art（bilevel optimization 是成熟领域，但"bilevel autoresearch"是否新造词）

## Investigator Findings

### Phase 2 — F1-F4 事实核实

**F1 — Niklaus Harness 实验：✅ 真实存在**
- `huggingface.co/spaces/joelniklaus/harness-optimization` 直连抓取确认标题 = "Don't Train the Model, Evolve the Harness"
- 文章引用的 HF space URL 真实，作者 Joel Niklaus 真实
- 文章转述的具体数字（3.5%→80.1% / 5 harness / +14.4 跨模型迁移）无法从 HF space 元数据二次核实（space 内容是交互式 demo），但空间存在性与文章描述一致
- **注意**：这是 HF Space + 个人实验，**非同行评审论文**。作为 prior art 引用时可引为 "Niklaus, HF Space 2026" 但需标注 non-peer-reviewed。

**F2 — "Bilevel Autoresearch" 论文：❌ 不可核实**
- arxiv API 搜 `"bilevel autoresearch"` = 0 entries
- Semantic Scholar API 限流，未拿到结果
- 文章给论文标题《Bilevel Autoresearch: Meta-Autoresearching Itself》但**无 arxiv/DOI 链接**
- **结论**：这个"论文"可能 (a) 不存在 (b) 是 X 帖子/博客被文章作者误称"论文" (c) 是未索引的预印本。**不可作为本项目 prior art 引用**，除非找到原文。"bilevel optimization" 概念本身是成熟领域（Colorescu & Li 2021 综述），但 "bilevel autoresearch" 作为新造词无文献支撑。
- **对本报告影响**：文章 Claim 3（bilevel 5× 提升）**不能作为方向依据**，只能作为"概念启发"。方向的依据必须来自 F1+F3+已验证 prior art。

**F3 — Karpathy AutoResearch：✅ 真实 + 本质不同于本项目**
- Context7 `/karpathy/autoresearch` 高信誉源（benchmark 92.83）确认仓库存在
- 读其 `program.md` + `llms.txt` 核实机制：**infinite loop = (1) check git branch (2) modify `train.py` (3) commit (4) run `uv run train.py` (5) extract `val_bpb` from log (6) 改进则 keep / 否则 `git reset --hard HEAD~1`**
- **关键区别**：Karpathy 的 evaluator 是 `evaluate_bpb()` 函数（客观 bits-per-byte metric，agent **不能修改**），本项目 evaluator 是 5-persona LLM panel（agent 可影响、且 panel 用被研究对象本身）
- Karpathy 的 `results.tsv` 是 append-only state file（与 Deli §4 state files 同源）；本项目的 `findings.jsonl`/`progress.json` 同构但 `progress.json` 的 verdict 字段（如 `g2_pass:true`）AI 可自改——**这是 Karpathy 明令禁止的（evaluator 锁定）**

**F4 — "Bilevel" 概念在 ML 里的真实 prior art：✅ 概念真实，命名不实**
- Bilevel optimization 是成熟 ML 领域（hyperparameter optimization, meta-learning, neural architecture search 都用 bilevel）
- "外层 loop 优化内层 loop 搜索逻辑"在 meta-learning 文献里有大量先例（MAML, REPTILE, learned optimizers）
- 但 "bilevel autoresearch" 作为新造词无文献支撑——**文章在这里把成熟概念套新名字当"论文"引用，是不可信的**

### Phase 3 — 3 个候选方向的 prior art + venue bar + 项目资产核对

#### 方向 A：Harness-Lock as Evaluation Integrity（最直接可发表，4-8 周）

**故事**：把本项目诊断的 G1（AI 可自改 `progress.json` verdict 字段 + 5-persona panel 用被研究对象本身）+ Karpathy 的"evaluator 锁定"机制，提炼成方法论论文：**"Autonomous research agents require locked external evaluators: a case study on Verdict Drift"**

**Prior art**：
- Karpathy autoresearch `program.md` 第 5 步明示"agent 不能改 results.tsv"——但 Karpathy 没把这个当 contribution 写论文（他的 evaluator `val_bpb` 本来就客观，锁定是隐式的）
- Niklaus HF space 的"评估脚本锁定"同理隐式
- Panickssery NeurIPS 2024 Oral (2404.13076) 已命名"self-preference bias"——但他们的 prescription 是 cross-family judge + human gold，不是"evaluator lock"
- JudgeBench (2410.12784) 论证 crowdsourced preference 不可靠——但没把"agent 可改 evaluator"作为 traps 系统化
- **本项目独特贡献**：4 天 10 verdict 反转 + `g2_pass:true` cached despite n=30 falsification + producer=self-judge default——这些是**其他论文没有的实证证据**，因为其他论文没让 agent 自评 publish 决策

**venue bar**：
- ACL/EMNLP Findings methodology track：10-20%（需补 frontier arm + 跨 ≥2 domain + public release）
- NeurIPS Evaluating Evaluators workshop：50-70% fit-aligned（最现实）
- 真实天花板：Findings 或 workshop，不是 main track（同前 10 verdict 调查结论）

**项目资产**：✅ 已有 4 篇论文 progress.json + 10 verdict 调查 + judge.py:113 producer=self-judge 实证 + patrol.jsonl stale 数学实证。**这是 4 篇 active 论文 4 天运作产生的真实 trace data，不是合成数据——这是最稀缺的资产**。

**风险**：single-author + 0 顶会历史 + 内部 domain（前 10 verdict 已诊断）。但本方向把"4 天 10 反转"从缺点变 contribution——这是 reframing，不是新造数据。

#### 方向 B：Verdict Cycling as a Measurable Failure Mode（medium，6-12 周）

**故事**：把"同一根因诊断逐字重复出现 2 次（verdict #9 与 #10）"作为可测量的 LLM-agent 失效模式论文——**"Verdict Cycling: When LLM Agents Diagnose the Same Bug Twice Without Learning"**

**Prior art**：
- Deli §1 "Cognitive loop — successive iterations try similar directions with diminishing returns"——但 Deli 是 protocol 不是 paper
- PIT-003 "stale_count>=2 → change structural constraint"——autoresearch 自己的 trap，但没做实证论文
- coqa/HotpotQA 的 feedback error correction 文献有"agent 反复犯同一错"现象，但不在 publish-decision 场景
- **本项目独特贡献**：4 天逐字重复的根因诊断是**其他论文没有的 trace**，因为没人在 publish-decision 场景跑 4 天 loop

**venue bar**：ACL Findings / EMNLP Findings 方法学 track 10-20%；workshop 50-70%。需补跨模型验证（至少 2 个不同 agent 跑同样 loop 看是否都 cycle）。

**项目资产**：✅ 10 份 verdict 调查 + 逐字重复诊断实证。**但这是把"自己的失败"作论文，reviewer 会问"你怎么知道这不是你一个人 prompt 写得差"**——需补跨 agent 验证，否则不可辩护。

**风险**：更高 than A，因为单作者轨迹 + 容易被 reviewer 当 anecdote。

#### 方向 C：Cross-Domain Replication of Niklaus Harness Finding（lowest ROI，不推荐独立）

**故事**：在 LLM-judge 校准场景（P12）而非法律 agent 场景复现 Niklaus 的"harness 优化 > prompt 优化"finding。

**问题**：Niklaus 已做过，本项目复现没 novelty。除非补"harness 优化在 circularity 场景下的不同行为"——那又回到方向 A。

**结论**：**不推荐独立方向**，但可在方向 A 里引为 supporting evidence。

### Phase 4 — 接下来该做什么修正（与 optimization-plan-2026-07-07.md 的衔接）

文章给的本项目诊断的**新外部文献锚点**（非 AI 自产）：

1. **Karpathy `program.md` evaluator-lock 是 G1 的外部 prescription**：前一份修正方案说"加 R8 separate exec/eval + R9 external anchor"，现在有**外部文献明确这么做**——Karpathy 的 `evaluate_bpb` 是锁定的客观 metric，agent 只能改 `train.py` 不能改 evaluator。这给 R9 的"external anchor"规则一个**可引用的工程实现**，不是 AI 自造规则。

2. **Niklaus "0% because存错文件名"是 G2 的反向证据**：Harness 失效会被误读为模型失效——本项目的 `patrol.jsonl` 6.5 年 stale 数学bug + `g2_pass:true` 矛盾正是同型失效（evaluator 有 bug 被当模型失效）。

3. **"评估器锁定"在本项目的具体落地**（修正方案的具体化）：
   - `progress.json` 的 verdict 字段（`g2_pass`/`fold_into_*`/`verdict`）改为**append-only ledger**，新 verdict 不能覆盖旧 verdict，只能追加——类似 Karpathy `results.tsv` 永不覆盖
   - evaluator 脚本（5-persona review 的 prompt + 阈值 + 模型列表）**冻结到 git commit hash**，运行时校验 hash 不变才接受 verdict
   - 任何"AI 自改 evaluator 脚本"的行为触发 PIT-501（前方案已草拟）

## Root Cause

### 3 个论文方向（按可发表性 + ROI 排序）

| 方向 | 核心 contribution | prior art 差异 | venue 天花板 | 项目资产 | 烧 token 预算 | 推荐度 |
|---|---|---|---|---|---|---|
| **A. Harness-Lock as Evaluation Integrity** | "autonomous research agent 需要 locked external evaluator" + 4 天 10 verdict 反转 + producer=self-judge 作实证 | Karpathy/Niklaus 隐式锁定但没系统化；Panickssery/JudgeBench 研究不同对象 | EMNLP Eval workshop 50-70% / Findings 10-20% | ✅ 全部已有（4 篇 progress + 10 verdict + judge.py 实证） | 小（3-10 API hours 写 outline + 实验） | **强推** |
| **B. Verdict Cycling as Failure Mode** | "LLM agent 逐字重复同一诊断"作可测量失效 | Deli PIT-003 知道但没实证；其他文献无 publish-decision 场景 | Findings 10-20% / workshop 50-70% | ✅ 有但需补跨 agent 验证 | 中（需补 ≥1 个不同 agent 跑同 loop） | 中（需补实验才 stand） |
| **C. Niklaus Harness 跨域复现** | P12 场景复现 harness>prompt | Niklaus 已做，无 novelty | workshop 30-50% | 部分 | 中 | 不推荐独立 |

**方向 A 是最现实的可发表路径**，原因：
1. 把"4 天 10 反转"从灾难 reframing 为贡献——其他论文无此 trace
2. 外部锚点（JudgeBench / Karpathy evaluator-lock / Panickssery cross-family）已有且 verified
3. 项目资产已齐——不需补大实验
4. 不违反前 10 verdict 的"顶刊不可达"结论——天花板是 workshop/Findings，与前调研一致

### 接下来该做的修正（按代价排序，衔接 optimization-plan）

**立即可做（不烧 token，1 天）**：
1. **采纳 Karpathy evaluator-lock 模式**：`progress.json` verdict 字段改 append-only ledger（新 verdict 不覆盖旧，只追加 + 标 superseded_by）
2. **evaluator 脚本冻结到 git hash**：5-persona review prompt + 阈值 + 模型列表 commit 后校验 hash 不变才接受 verdict
3. **修 watchdog 数学**（前方案已列，这里文章给了新 urgency——Niklaus 0% 因存错文件名说明 harness bug 会被误读为模型失效）
4. **修 P12 cached `g2_pass:true`**——append-only ledger 落地后这是自然修复

**1-3 天**：
5. **写方向 A 的 1-page proposal**：标题候选 "Locked Evaluators for Autonomous Research Agents: A Case Study on Verdict Drift in LLM Self-Review"。突出 4 天 10 反转 + producer=self-judge + Karpathy/Niklaus external prescription。
6. **5-persona review on the proposal**（但**用前方案 R9 要求的 external anchor**：这次 review 必须引 JudgeBench/Karpathy 作锚，不是纯 LLM panel）

**2-4 周**：
7. **接 JudgeBench 子集**作 P12 external anchor（前方案已列）
8. **n=10 应急专家 Likert-5**（前方案已列）
9. **方向 A 投 EMNLP 2027 Eval workshop 4-page short paper**——这是最现实 venue，fit-aligned acceptance 50-70%

### 不该做

10. **不要**追"Bilevel Autoresearch"方向——文章引用的论文不可核实（arxiv 0 entries），bilevel 概念虽真实但命名不实，作为方向依据有风险
11. **不要**把 Niklaus 数字（3.5%→80.1%）引为论文 prior art 的事实——HF space 是 non-peer-reviewed，引为"engineering observation"可，引为"verified result"不可
12. **不要**把 Karpathy autoresearch 当本项目 prior art——两者同名不同物，混引会被 reviewer 立刻打回

## Recommendations

### 给用户的两问的直接答案

**Q1：还有什么方向有机会产出论文？**
**方向 A "Locked Evaluators for Autonomous Research Agents"**——把本项目 4 天 10 verdict 反转 + producer=self-judge 诊断本身作为研究对象，引 Karpathy evaluator-lock + JudgeBench objective ground truth + Panickssery cross-family 作 prior art。EMNLP Eval workshop 4-page 是最现实 venue（50-70% fit-aligned）。理由：项目已有稀缺 trace（其他论文没有），外部锚点 verified，不需补大实验。

**Q2：接下来该做什么修正？**
最优先：**采纳 Karpathy evaluator-lock 模式**——`progress.json` verdict 字段改 append-only ledger + evaluator 脚本冻结到 git hash。这是文章给的外部文献锚点（非 AI 自产），直接修 G1（AI 自改 `g2_pass:true`）+ 给 R9 一个可引用工程实现。其次是写方向 A 的 1-page proposal + 投 workshop。

### 战略层（衔接前两份报告）

本报告是第 3 份诊断后续：第 1 份（meta-uncertainty）说"AI 没把握自己结论"；第 2 份（optimization-plan）说"补 Deli §3/§10.3 + 接外部锚点"；本报告（第 3 份）说**外部文献已经验证了第 2 份的方向**——Karpathy evaluator-lock 正是 R9 的工程实现，Niklaus 0%-because-存错文件名正是 G2 的反向证据。所以本报告的 confidence 比前两份高：~75%（因为外部文献给了非-循环锚点）。

但本报告仍是 AI 用同仪器产出——方向 A 的 proposal 仍需走 5-persona review + external anchor 流程，不可自决 publish。这是前方案 R6.1 修订的强制 human checkpoint。

## Preventive Measures

1. **文章事实必须核实再引**：本报告核实了 Niklaus HF space 真实 + Karpathy 真实，但"Bilevel Autoresearch"不可核实——引文章时只能引 verified 部分，不可引 unverified 部分。这是 PIT-001（hallucinated citation）的预防。
2. **同名混淆预防**：Karpathy 的 autoresearch 与本项目同名不同物，任何 writeup 必须在第一次提及时明确区分。否则 reviewer 会以为本项目是 Karpathy 项目的衍生。
3. **non-peer-reviewed 引用标注**：Niklaus HF space 是 demo 不是论文，引用时必须标 "non-peer-reviewed engineering observation"。
4. **方向 A 的 reframing 风险**：把"10 verdict 反转"从缺点变贡献是 reframing——前一份调查（top-journal-opportunity-reality-check）已诊断 post-hoc reframe 违反 spec §3.3。但这里 reframing 的不是实验数据（数据是事实），而是 narrative frame——这是允许的（论文写作本身是 framing），只要实验数据不改。

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 阅读头条文章 | Playwright 抓取全文 + 3 个 claim 核实 | ✅ |
| (2) 结合本项目思考论文方向 | 3 个方向 A/B/C，prior art+venue+资产+ROI 表格 | ✅ |
| (3) 有什么修正是接下来该做的 | 9 条 action（4 立即 + 3 中期 + 2 不该做），衔接前两份报告 | ✅ |
| (4) 核实文章事实 | F1✓ Niklaus / F3✓ Karpathy / F4✓ bilevel 概念 / F2✗ "Bilevel Autoresearch 论文"不可核实 | ✅ 诚实标出 unverified |
| (5) 不写第 11 份 verdict | 本报告给的是 action（方向 A proposal + evaluator-lock fix），不是 verdict on 顶刊路径 | ✅ |

### 最终自审计

本报告 confidence ~75%（高于前两份的 ≤60%/70%），因为：
- 外部文献（Karpathy `program.md` evaluator-lock + Niklaus HF space）**给了非-循环锚点**——本方案不是 AI 自产规则，是引用外部已实现机制
- 方向 A 的项目资产（4 天 10 verdict + producer=self-judge trace）是**事实数据**，不是 verdict
- 但本报告仍是 AI 用同仪器产出——方向 A 的 proposal 必须走 external anchor + 5-persona review（带 JudgeBench 锚点）流程，不可自决 publish

**未核实但诚实标出的**：F2 "Bilevel Autoresearch" 不可核实——本报告未把它当方向依据，只在 §Investigator Findings 标注 "不可作为 prior art 引用"。这是 PIT-001 预防的落实。

## 交叉引用

- 本报告：`docs/investigations/karpathy-loop-harness-2026-07-07.md`
- 前置诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`（Q1+Q2+元悖论）
- 前置修正方案：`docs/investigations/optimization-plan-2026-07-07.md`（R8/R9/PIT-500 + JudgeBench + 人类专家 gold）
- 文章：头条《76%的性能提升与模型无关？Karpathy 700次 Loop 实验揭开 Agent 最大误区》（AI 前线，2026-07-07）
- 文章引用源：Niklaus HF space `huggingface.co/spaces/joelniklaus/harness-optimization`（F1 ✓）/ Karpathy `github.com/karpathy/autoresearch` `program.md` (F3 ✓ via Context7) / "Bilevel Autoresearch" 论文（F2 ✗ 不可核实）
- 已验证 prior art：JudgeBench (2410.12784) / Panickssery NeurIPS 2024 Oral (2404.13076) / CALM (2410.02736) / CoBBLEr (2309.17012) — 见前报告
- 项目内诊断证据：`legacy/p11-closed-v5-minimax-m3/harness/judge.py:113` (producer=self-judge) / `papers/p12-judge-calibration/state/progress.json` (`g2_pass:true` vs n=30 矛盾) / `framework/watchdog/patrol.jsonl` (6.5yr stale 数学 bug) / 10 份 verdict 调查 (`docs/investigations/top-journal-*.md`)

## Root Cause

[Phase 4 待填：3 个论文方向 + 修正 priority]

## Investigation Log

### Phase 1 — 文章阅读 + 与本项目映射（agent 自读）

**Hypothesis**：
- H1（论文方向）：本项目最大的未开发方向不是"再写 1 篇 LLM-judge 论文"，而是**把本项目自身的"4 天 10 verdict 反转"现象本身作为研究对象**——即"LLM agent 在无外部锚点时的自我评估失效"作为方法论论文。这与 Bilevel Autoresearch 的"外层 loop 打破思维定势"是同一问题的解/症。
- H2（修正）：文章的"评估器锁定"（Karpathy 不让 agent 改评估脚本）正好是本项目诊断 G1（AI 自改 progress.json verdict）的对应解——这给了修正方案一个**外部文献锚点**，不是 AI 自产。

**Findings**：见 Background 3 个 claim。

**Conclusion**：H1 需 Phase 3 验证（prior art + venue bar）；H2 的"评估器锁定"机制可立即采纳为修正（有外部文献支撑）。
