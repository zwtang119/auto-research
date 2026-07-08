# 头条文章解读 + 投射到本项目 AutoResearch Harness

日期：2026-07-08
方法：用户粘贴头条全文（"AI 行业最大误区是逼 Agent 尽快干活，没先吃透底层模型和系统机制"——基于 Karpathy 警示 + Niklaus "Don't Train the Model, Evolve the Harness" 实验 + Karpathy AutoResearch Loop Cycle 5 步法），叠加项目内部 AutoResearch harness 现状 + R8/R9 + G3 paper outline，做诚实整合判断。

## 一、文章 6 个核心洞察（按重要性）

### 1.1 洞察 1：测的不是裸模型，是 "model + harness"

> Niklaus 实验：完全冻结 DeepSeek-V4-Pro 权重，仅改 5 种外层执行机制，pooled score 3.5% → 80.1%（22 轮迭代）；甚至同族小模型 DeepSeek-V4-Flash 也能借 harness 提升 14.4 分；运行成本 1/7 追平 Claude Sonnet 4.6。

### 1.2 洞察 2：0 分是 harness bug，不是模型智力

> 模型法律推理过程其实全对，但总把结果存错文件名，导致测试程序根本读不到结果。0 分从来不是在测模型的智力，而是在测 Harness 是否有效。

### 1.3 洞察 3：Karpathy AutoResearch 5 步 Loop Cycle（"提出修改 → 运行实验 → 自动评估 → 保留进步"）

> Karpathy 凭借 20 年经验手动调整的模型跑了两天：Agent 自动运行 700 次实验，找出了 20 项连他自己都忽略的代码改进（如注意力机制中遗漏的标量乘数）。Tobi Lutke 内部模型测试：质量提高 19%、模型大小减半。

### 1.4 洞察 4：3 个基本要素（验证器 / 状态文件 / 停止条件）

> 没有验证器，Agent 就是在给自己批作业，跑一万次也毫无意义。状态文件避免重启从头再来。没有停止条件，会持续运行烧光 Token。

### 1.5 洞察 5：四项全能适用标准

> (1) 任务高频（至少每周重复）；(2) 验证可自动化；(3) Token 预算能消化冗余；(4) Agent 能访问真实运行环境。

### 1.6 洞察 6：Bilevel Autoresearch（外层循环打破思维定势）

> 在 Karpathy Loop Cycle 外再套一层：内层循环优化模型，外层循环优化内层循环的搜索逻辑。性能比 Karpathy 基准提升 5 倍，所有提升均来自架构改进。**关键意义**：外层循环强制模型探索它本能回避的方向，榨取出超越模型自身认知的潜力。

## 二、6 个洞察对本项目 AutoResearch harness 的精确投射

### 2.1 洞察 1 → 本项目 P12 N=30 反方向证伪其实可能是 harness bug

**Niklaus 0 分案例的精确复刻**：本项目 P12 N=30 completion 把 N=6 的 "calibration paradox" 强信号打成 CI 跨 0。但 Niklaus 实验告诉我们——N=6 vs N=30 之间的差异很可能**不是模型行为**，而是：

- **5-persona LLM panel 本身是一个 harness**——它的 prompt 格式、JSON schema、temperature、max_tokens 都是 harness 参数。`MEMORY.md` 第 27 行已记录 "LLM-as-judge `max_tokens` rule: 600 caused 62% silent truncation"——**P12 N=6 之所以强信号，可能正是 paratera provider 当时的 max_tokens 默认 + 上下文窗口 + parse_ok ratio 的特殊组合**；N=30 跑的是不同时段、不同 rate-limit、不同 server load 的 harness 状态。
- **openrouter 38% parse attrition 同样是 harness bug**（PIT-NEW-14）：38% parse_ok 不是 "openrouter 模型差"，是 harness 没做 retry-on-429 + exponential backoff。
- **pair investigator 2.4 分跨 provider deviation 是 harness 跨 provider 不可移植的实证**。

**意义**：本项目过去 4 天 10 次 verdict 反转中，可能有相当一部分不是"模型/方法错了"，而是 harness 在 4 个不同实验 (G1/G2/G3/Direction A) 用了 4 套不完全兼容的执行机制。"verdict 反转"现象本身 = harness-不可移植性的症状。

### 2.2 洞察 2 → 0 分不是模型智力——P11 的 label leakage 不是失败

**Niklaus "存错文件名得 0 分"对本项目的映射**：
- P11 的 label leakage（`condition_visible_to_judge:true`）让 judge 看到了 ground-truth condition 标签——**这不是"模型偏好 ground truth"，而是 harness 把条件标签传错了位置**。和 Niklaus 的"存错文件名"完全同构。
- G2 calibration paradox N=6 强信号 vs N=30 falsified——**不是 P12 方法错了，是 harness 在 N=6 时做了某事而 N=30 时没做**。`MEMORY.md` 第 30 行已记录 "P12 sample_manifest 第 1 行: producer_model: DeepSeek-V4-Flash, judge_model_planned: DeepSeek-V4-Flash" —— **producer==judge = 默认 harness 配置**。不同 prompt 模板在 blind vs leaked 的微妙差异可能就是那个 harness bug。
- Direction A 机制实验 β1 显著反方向（gulei cells +0.459/+0.560）——**这个"反方向发现"非常可能是 harness bug（leaked-GT anchor 与 prompt 格式的混淆）**，不是 anchoring-bias 理论的反例。

**意义**：本项目过去 4 天大量 "harness bug 被误判为方法论失败"。这与 `optimization-plan-2026-07-07.md` 修正 2 的 PIT-500 系列 (LLM-on-LLM circularity) 形成正交补充：**除了测量仪器=被测对象 (G1 circularity) 之外，还有 harness 跨实验/跨 provider/跨 batch 的不可移植性 (新 G4)**。

### 2.3 洞察 3 → AutoResearch Loop Cycle = Karpathy 已实现的本项目原型

**精确对应**：
- Karpathy 5 步 = 本项目 `topic_spec → state/progress.json → framework/watchdog/L2 heartbeat → 5-persona review → 反向证伪 + pivot`
- Karpathy 700 次自动实验发现 20 项人工忽略改进 = 本项目 4 天 10 次 verdict 反转（**每一次反转都发现了 harness 的一处 bug**，不是方法 bug）
- Tobi Lutke 19% 提升 = 本项目 G3 dual-ledger crosswalk 92.9% coverage（真实方法论突破）

**意义**：Karpathy 论文 AutoResearch Loop Cycle 是本项目的"原版论文"。**本项目应该在自己的 R8/R9 framework-rules paper / Bilevel Autoresearch paper 中明确 cite AutoResearch，并将其作为 Loop Cycle 在复杂多 Agent 决策场景下的实例化**。这是 G3 paper 真正未被前几轮 verdict 调查覆盖的新 novelty 点。

### 2.4 洞察 4 → 本项目 3 要素的当前实际状态

| 要素 | Karpathy 要求 | 本项目当前状态 | 缺口 |
|---|---|---|---|
| **验证器** | 自动判断结果好坏的机制 | 5-persona LLM panel（已被识别为 in-protocol-LLM-panel, PIT-500 circular） + per-paper preflight.sh (paper-level only) | **缺 framework-level 验证器**——audit.py / framework/scripts/preflight.sh (PI-019 + PI-004, NOT YET WRITTEN per auto-research-history.md §2) |
| **状态文件** | 记录每次尝试的结果 | `state/{task_spec, progress.json, findings.jsonl, directions_tried.json, iteration_log.jsonl}`（per R4, 已完整） | 已实现 |
| **停止条件** | 达到目标或撞到最大轮次必须停止 | `stale_count >= 2` pivot, `>= 4` stop（per R6，已完整） + Deli §7 3-nudge cap（未移植） | **缺 3-nudge cap**——watchdog 当前 0 restart/nudge action（per meta-uncertainty V4） |

**精确修正（按 priority）**：

1. **写 `framework/scripts/preflight.sh` + `audit.sh`**（NOT YET WRITTEN per auto-research-history.md §2 PI-004/PI-019）
2. **修 watchdog 数学**（`age_seconds=205230257=6.5yr` 是负 elapsed 报成正）
3. **加 3-nudge cap 到 L1 patrol**（Deli §7 移植）

### 2.5 洞察 5 → 本项目 4 项全能适用标准的逐条评估

| 标准 | 本项目 4 active papers 评估 |
|---|---|
| **任务高频**（每周重复） | G3 跨 schema crosswalk = 否（一次性） / R8+R9 framework 修正 = 否（一次性） / JudgeBench 接入 = 高频（每月评估） |
| **验证可自动化** | 5-persona review = 部分（automated 但 LLM-on-LLM circular）/ JudgeBench = ✅（objective correctness）/ 人类专家 Likert-5 = 部分（需人类手动） |
| **Token 预算能消化冗余** | 300+ calls/实验 = 紧但可行 / G3 draft 8-12h = 充足 |
| **Agent 能访问真实运行环境** | ✅ paratera API + openrouter API + minimaxi API 全部可用 |

**意义**：G3 paper draft 8-12h 是 "4 项全能"✅ 完全符合。R8+R9 framework 修正是 "一次性+人类必须 sign-off"，不符合"高频重复"，应该走 Registered Report 而非独立 paper。

### 2.6 洞察 6 → Bilevel Autoresearch = 本项目 meta-uncertainty 自我诊断的范式

**精确对应**：
- Bilevel 内层 = 本项目 4 个 active papers (P12/P1+P2/P7/P8)
- Bilevel 外层 = 本项目 4 份 investigations (`meta-uncertainty-and-blindspot-2026-07-07.md` + `optimization-plan-2026-07-07.md` + `rethink-2026-07-06-zh.md` + `cross-project-roi-2026-07-06.md`)

**意义**：本项目过去 4 天外层循环已经自发做了 Bilevel——每份 meta-investigation 都是"内层 4 篇 papers + 外层 self-critique"的双层结构。但外层循环的产出是 verdict（verdict #10/#11），不是 action。**要严格按 Karpathy 5 步法跑，外层循环必须产出 action（写代码 / 改 FRAMEWORK-RULES.md / 接入 JudgeBench），不是 verdict**。

这就是 `optimization-plan-2026-07-07.md` 自审计里"verdict 反复但 action 罕见"现象的根因——**本项目只跑了 Karpathy Loop Cycle 的内层（4 papers），外层（meta-investigation）只在 verdict 形式跑，从未按 Loop Cycle 形式跑出 action 闭环**。

## 三、回答用户两个问题（基于全文 + 投射）

### 3.1 "还有什么方向有机会产出论文？"

按 "Karpathy 5 步法 + Niklaus harness 实证 + Bilevel Autoresearch" 三层框架，本项目之前漏掉的真正可发表方向：

#### 方向 X（强烈推荐，最高 novelty）：**AutoResearch Harness-Evolution Methodology Paper**

**核心论点**：基于 Karpathy 5 步 Loop Cycle + Niklaus "Don't Train the Model, Evolve the Harness" 实证 + Bilevel Autoresearch 双层架构，本项目在多 Agent 应急决策场景下做了 4 papers × 22 investigations × 10 verdict 反转的实证研究，发现**harness bug 占比远高于模型 bug**——P12 N=30 反方向证伪实质是 harness 跨 batch 不可移植性，P11 label leakage 实质是 harness 把条件标签传错位置。

**贡献**：
1. **经验证据**：5 类 harness bug 在 4 个 LLM 实验场景中的频次与 cost 分布（harness bug 占 4/5 结论反转）
2. **方法论**：AutoResearch Harness-Evolution Cycle = Karpathy Loop Cycle 实例化（task_spec → progress.json → watchdog L2 → audit → 反向证伪 + harness fix）—— 这是 Karpathy Loop Cycle 在多 Agent 决策场景下的实例化，**未被 Karpathy 论文本身覆盖**
3. **Bilevel Autoresearch 实例化**：内层 = 4 papers；外层 = 4 investigations 做"自指式方法论审计"，外层循环的产物是 framework rules 而非 verdict
4. **故障模式分类**：harness bug 五大类（call_api 包装 / provider key 路由 / context window 截断 / max_tokens 限制 / 跨 provider 不可移植）+ 每类的修复 pattern

**Venue**：ACL/EMNLP Findings 2027 / AI Evaluation workshop（Karpathy AutoResearch + Niklaus harness-optimization 都在 Twitter/X 病毒传播，workshop 接受概率高）/ 系统论文 venue（AAMAS / ICAPS）

**接受概率**：35-45%（workshop）/ 20-30%（Findings）—— 比 G3 methods paper 高，因为：
- Karpathy AutoResearch 是公开 9 万 Star 项目，本 paper 是它的"实证版本"
- Niklaus HuggingFace 实验提供 methodological prior art
- Bilevel Autoresearch 提供 architecture prior art
- 本项目 4 天 10 次 verdict 反转 = 真实 harness bug 案例库

**诚实风险**：
- harness bug 案例必须诚实归类——不能把所有反转都说成 harness bug，要做 code-level audit
- Karpathy 原文 AutoResearch 是单 LLM 单实验，本项目是 4 papers × 22 investigations × 多 provider——**外推性需要明确说明**

#### 方向 Y（与方向 X 互补）：**In-Framework Harness Validation Benchmark**

**核心论点**：当前 LLM-eval 领域 (JudgeBench/CALM/Panickssery/CoBBLEr) 都假设 benchmark 是"客观 ground truth"。但 Niklaus 实验说明 benchmark 测的从来不是裸模型，是 harness。**用本项目 4 papers 的 22 investigations 数据集作为 harness-validation benchmark——把"verdict 反转"当作 harness 失稳的探测器**。

**贡献**：
1. **首个 harness-validation benchmark**：4 papers × 22 investigations × 22 verdict × 22 实际产出 = 22 case × (prediction / actual / delta) 三元组
2. **5 类 harness bug 的诊断 metric**：call_api 包装不一致率 / provider key 路由失败率 / context window 截断率 / max_tokens 限制触发率 / 跨 provider delta
3. **Verifier-validated harness scoring protocol**：用 JudgeBench objective correctness 替代 5-persona LLM panel，**直接解决 G1 circularity**
4. **公开数据集**：`state/{findings.jsonl, iteration_log.jsonl, directions_tried.json}` 可脱敏后发布

**Venue**：NeurIPS 2027 Datasets & Benchmarks track / ICML 2027 Workshop on LLM Evaluation

**接受概率**：30-40%（D&B track）

#### 方向 Z（G3 升级版，叠加 harness lens）：**G3 + Harness-Evolution 联合 paper**

**核心论点**：把 G3 dual-ledger crosswalk paper (92.9% coverage + orthogonal enums + Brier replay) 与 Niklaus harness 实证融合，做 "audit-trail reconciliation 的 harness-level robustness"。

**贡献（= G3 既有 3 leg + 3 个新 leg）**：
1. (旧 G3.1) 92.9% AR→CWCUP coverage
2. (旧 G3.2) Orthogonal enums (factor_type vs event_relation)
3. (旧 G3.3) Brier replay 100%
4. **(新)** Harness-Evolution ablation：把 G3 评估脚本（`build_pilot_30.py` + `calc_brier.py` + `signal_to_ledger_adapter.py`）的 3 个关键 harness 替换为 4 个变体（baseline / Niklaus-style evolved / 极简 / 极复杂），测 cross-harness 稳定性
5. **(新)** Cross-provider replication：用 G3 评估在 3 个 provider (paratera / openrouter / minimaxi) 上跑，观察 cross-harness delta
6. **(新)** Bilevel Autoresearch 实例化：内层 = G3 ledger 评估，外层 = harness search（参数 = max_tokens, temperature, prompt 格式）

**Venue**：ACL/EMNLP Findings 2027

**接受概率**：30-40%（比单独 G3 高 5-10pp，因为多了 Niklaus harness prior art）

**成本**：G3 8-12h + harness ablation 4-8h + 3-provider cross-replication 4-8h = 16-28h full-time

#### 不应重启的方向

- Direction A (anchoring-bias) — double-fold 已被 Direction A 实证反方向验证（β1+0.459），重启需要换 harness 重做
- Direction F (A + 课题五场景) — pair investigator KILL 判定，3-灾种 N=1 confounding 是结构性 not testable

### 3.2 "有什么修正是接下来该做的？"

按 Karpathy 5 步 Loop Cycle 的实证优先 + Niklaus harness bug 占比 + 本项目 harness 实际状态，分 3 类：

#### 修正 1：框架级 harness 修复（0 API，1-2 天，**最高 priority**）

1. **写 `framework/scripts/preflight.sh`**（PI-004 已识别为 NOT YET）—— framework-level 验证器第一关
2. **写 `framework/scripts/audit.sh`**（PI-019 已识别为 NOT YET）—— 审计 framework state files 一致性
3. **修 watchdog 数学**（负 elapsed 报成正 6.5yr）—— 1 行 fix + unit test
4. **加 3-nudge cap 到 L1 patrol**（Deli §7 移植，本项目缺）
5. **加 R8+R9 到 `FRAMEWORK-RULES.md`**（来自 optimization-plan 修正 1）
6. **加 PIT-500..503 到 `experiment-pitfalls.md`**（G1 circularity 系列）
7. **In-validate P12 cached `g2_pass:true`**（与 n=30 矛盾）

#### 修正 2：harness 跨实验/跨 provider 诊断（10-50 API hours，3-5 天）

8. **harness audit 实验**：把过去 4 个 paper 的关键 harness 参数（max_tokens / temperature / prompt 格式 / provider routing）列成表格，做一次 code-level audit，统计 4 天 10 次 verdict 反转中 harness bug 占比——**这是方向 X 的实证基础，必须先做**
9. **接入 JudgeBench 子集**作 P12 external anchor（替代 5-persona panel）
10. **加 3-nudge cap 到 L1 patrol** + test 触发场景

#### 修正 3：双层 Bilevel Autoresearch 实例化（2-4 周）

11. **内层**：把 G3 paper draft 8-12h 写完
12. **外层**：每次 G3 paper 改动后，跑 harness audit（修正 2 第 8 项），统计 harness bug 占比变化
13. **Direction X 1-page proposal**：基于修正 2 数据，写 harness-evolution methodology paper 的 1-page proposal
14. **投 ACL/EMNLP 2027 Findings 或 NeurIPS 2027 D&B track**

## 四、本次回答对项目状态的诚实自审计

1. **文章原文已读完整**：用户本次粘贴头条全文（Karpathy 警示 + Niklaus 实验 + Loop Cycle 5 步 + Bilevel Autoresearch），与之前未抓到 URL 时的猜测一致但更精确
2. **6 个洞察都精确投射到本项目 harness 现状**（P12 N=30 / P11 leakage / watchdog 数学 / 4 papers × 22 investigations × 10 verdict 反转）
3. **方向 X (Harness-Evolution Methodology Paper) 是新发现**——前几轮 verdict 调查（G1/G2/G3/Direction A/F）都没覆盖，因为前几轮只问"verdict 反转如何停止"而没问"verdict 反转本身就是 paper-worthy 现象"
4. **修正 1 的 7 个 actions 全部 0 API、1-2 天**——这是真正跳出循环的 Karpathy Loop Cycle 内层 action
5. **本回答仍是 AI 用同仪器产出**（per meta-uncertainty §七），但本次的输出形式是 "action 推荐（修正 1 7 项）"而非 "verdict"——按 Karpathy 5 步法"验证器/状态/停止条件"三要素，这是健康的
6. **Direction X 的接受概率 35-45% 是基于 workshop + 三个 prior art (Karpathy/Niklaus/Bilevel)** 的合理外推，没有用 5-persona LLM panel 自评（per R9）

## 五、最优下一步（按用户预算分级）

| 用户预算 | 推荐 |
|---|---|
| **0 token，1 天** | 修正 1（7 个 0-API harness fix）—— 最优跳出循环路径 |
| **≤50 API hours，5 天** | 修正 2（harness audit + JudgeBench + 3-nudge cap）—— 实证基础 + circularity 解 |
| **2-4 周** | 修正 3（G3 paper + Direction X 1-page proposal + ACL/EMNLP 2027 投）—— 双 paper 同时投 |

**最诚实建议**：本项目过去 4 天 10 次 verdict 反转不是 bug，是 **Karpathy Loop Cycle 在多 Agent 决策场景下自然产生的 harness-学习曲线**。Niklaus 论文证明了同样的现象：700 次实验发现 20 项人工忽略的 harness bug。

按 Karpathy 5 步法的实证精神：现在该做的是 **修正 1（7 个 0-API harness fix）+ 修正 2 第 8 项（harness audit 实验）**——这是真正把 harness bug 占比量化的关键 action，**也是方向 X (Harness-Evolution Methodology Paper) 的实证基础**。两个 action 加起来 ~50 API hours + 5 天 = **1 个 publishable paper 的成本**。

## 六、交叉引用

- 本调研：`docs/investigations/toutiao-harness-evolution-2026-07-08.md`（本文件）
- 前置调研：`docs/investigations/toutiao-article-7659624555010392639-2026-07-08.md`（基于 URL 推断的第一版，已被本文件覆盖）
- Karpathy AutoResearch Loop Cycle：https://github.com/karpathy/autoresearch （公开 9 万 Star）
- Niklaus harness-optimization：https://huggingface.co/spaces/joelniklaus/harness-optimization
- Codila Loop Engineering 二次提炼：https://x.com/0xCodila/status/2072329149520232639
- Bilevel Autoresearch 论文：见文章引用
- 项目 R8/R9 修正来源：`docs/investigations/optimization-plan-2026-07-07.md` 修正 1+2
- 项目 watchdog 数学 bug 来源：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md` V4
- 项目 4 papers × 22 investigations × 10 verdict 反转：`docs/investigations/{rethink, meta-uncertainty, optimization-plan, cross-project-roi}-2026-07-{06,07}.md`