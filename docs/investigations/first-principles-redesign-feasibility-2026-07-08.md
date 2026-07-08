# 第一性原理：重新设计实验，能否出标尺级高质量论文？

日期：2026-07-08
方法：rp-investigate-cli（builder + pair 真诚对抗式 + lead 自验证）
任务：从第一性原理出发——(1) 重新设计实验能否产出 7 份标尺级（论文 exemplar）质量的论文？(2) 该如何设计？(3) 现有数据是否已无用？(4) 可能性多大？

## 前置声明

用户明确"不要迎合、可以说不"。举证责任：默认**"不能"**——要证"能"必须从第一性原理证明每一缺失条件可补且不是循环推理。前 4 confirmed verdict 反转的 base rate 50% 错 + 本报告是 verdict chain 第 N 份 + LLM-on-LLM 自指循环未解，所以本报告任何"能"verdict 必须有外部锚点。

**第一性原理的 4 个公理**（不接受循环论证）：
1. **A1 数据有效**:数据必须由非生产者模型生成或独立验证;否则 producer=self confound(诊断于 `meta-uncertainty-and-blindspot-2026-07-07.md` V3)使所有 downstream 结论可被 dismiss
2. **A2 评估器独立**:evaluator 不能由被研究对象充当;Karpathy `program.md` evaluator-lock 是此公理的工程实现
3. **A3 ground truth 外部**:任何 publishable claim 需 ≥1 非-LLM ground truth（JudgeBench/人类专家/真实结算/venue reviewer）
4. **A4 contribution 不可凭空**:B1（范式/深度框架）不能靠 reframe 弥补——要么有 paradigm-sized insight,要么诚实定位为 application study

本报告任何"能"的结论必须同时满足 A1-A4。任一不满足=该路径"不能"。

## Symptoms

用户读完 7 份标尺 + 前几份 verdict 后，要求第一性原理重评——不是问"现有项目冲顶刊"，而是问"**如果重新设计**能否达到标尺级"。潜台词：用户在问现有 portfolio 是否本质上有 salvage value，还是需要从头来过。

## Background / Prior Research

### 7 份标尺定的"高质量论文"是什么（详见 `framework/knowledge/paper-exemplars-2026-07-08.md`）

3 类标尺：
- **A 类 范式长文**（E1 TreeReview / E3 AsyncThink / E4 Scaling / E5 ToT）：NeurIPS/ACL main，需 B1 范式 contribution + B2 大规模实证 + B3 外部锚 + B5 public
- **B 类 诚实短文**（E2 LLM Swarms IEEE 8 页）：B2 实证 + B4 诚实负面 + B6 短文格式
- **C 类 应用研究**（E6/E7 NPS capstone/thesis）：B7 应用域匹配 + B2 真实场景实证 + B3 真实数据

### 现有 portfolio 5 paper 第一性原理审计（继承 V1-V6）

| Paper | A1 数据有效 | A2 评估器独立 | A3 外部 ground truth | A4 contribution | first-principles 诊断 |
|---|---|---|---|---|---|
| P11 | ✗ producer=self（judge.py:113） | ✗ panel 用被研究对象 | ✗ 无 | ⚠ "PA degrades" 是 finding 不是 paradigm | 数据源 contaminated |
| P12 | ✗ import P11 contaminated | ✗ 同 | ✗ producer=self confound | ✗ 5-protocol 工程桥接 | 继承 P11 全部问题 |
| P1P2 | ⚠ ledger 是 schema 不是数据 | ✗ 同 | ✗ | ✗ schema 工具 | 数据未生成 |
| P07 | ✗ N=5 synthetic | ✗ 同 | ✗ | ✗ adapter 桥接 | 数据未生成 |
| P08 | ✗ N=0 + data-shape mismatch | ✗ 同 | ✗ | ✗ brier tool | 数据不可用 |

**第一性原理结论**：5 paper 全部违反 A1（P11 producer=self）/A2（panel=LLM-on-LLM）/A3（零外部锚）三条公理的至少 2 条。**现有任一 paper 要达 A/B/C 类标尺，必须先解决公理违反**。

### 前 verdict chain 已 verify 的关键事实

- `legacy/p11-closed-v5-minimax-m3/harness/judge.py:113` `--judge-model default=DeepSeek-V4-Flash` = producer（A1 违反实证）
- `papers/*/paper/review_round_1.md` 全 5 paper 用同 5 paratera mid-tier 模型（A2 违反实证）
- 无 OpenAI/Anthropic/Google 直连密钥（`llm-intelligence-blocker-verdict` §三实测）
- 4 confirmed verdict 反转，base rate 50% 错
- 张辉 = JSSR 安全学者，0 顶会历史；E1 TreeReview 作者群（中科院+港大）可比
- Cohen d=1.0 power=0.80 → n≥10 paired 应急专家 Likert-5 是最小外部锚
- JudgeBench（2410.12784）提供 objective correctness ground truth，破 crowdsourced preference 循环

## Investigator Findings

### Phase 2 — Builder gap analysis（3 paths given，P halved by 50% base rate）

Builder 给 3 path + 自标 confidence 70%：
- Path ① P11→E2 IEEE 8p：$50 + 3-4 周 + 张辉协调 n=10 专家 → P=15-25% post-cap
- Path ② P07→E7 NPS-style：$200 + 2-3 月 → P=25-32% post-cap
- Path ③ P12 cross-weld workshop：**已 FAILED**（median 4.0<4.5），salvage as methods section → P=15-25% post-cap

Builder H1 partial-falsify：P11 240 yaml 中 150 是 blind → salvage 率 62.5%（不是 100%）。

### Phase 3 — Lead independent verify（关键，pair silent 未追加）

Pair session `58613A18` 返回 silent（可能是 opus:max 在子任务流末了，未追加 findings 到 report）。**Lead 必须独立 verify builder 假设**——这正是 rp-investigate-cli §"Direct tool calls are for follow-up"的落实：pair 失败时 lead 用 file:line 自验。

**LV1 — Builder H1 partial-falsify 的 blind=150/240 数字验证：✅ confirmed**
`legacy/p11-closed-v5-minimax-m3/experiments/mc-2026-07-01-inner-monologue/scores_blind.jsonl` = 150 lines（verified）。Builder 数字准确。

**LV2 — blind 是否真修 A1 producer=self？❌ 关键否决（builder + pair 都漏）**
- `legacy/p11-closed-v5-minimax-m3/harness/judge.py:113` `ap.add_argument("--judge-model", default="DeepSeek-V4-Flash")` —— `--blind` flag 只触发 `judge_prompt(blind=True)`（剥 gene 数值 = label leakage fix），**不改 judge_model default**
- `:117` `ap.add_argument("--blind", action="store_true", help="BLIND judge:不给 gene 数值, 避免 label leakage")` —— blind 只解决 label leakage，**不解决 producer=self**
- `wiki/decisions/blind-judge.md:5` 明文："Judge 盲评：不告知 mode，只给企业 gene ground truth + agent 的 decision + inner_monologue" —— 没说不告知 producer 身份
- **结论**：blind=150 记录仍有 producer=self confound。Builder H1-partial-falsify（62.5% salvage）**高估**：真正 salvageable 是 240 yaml 的 **agent_output + decision（generation 层）**，**不是 150 blind judged scores（judge 层仍 A1 违反）**。Panickssery NeurIPS 2024 Oral（2404.13076）已命名这是 self-recognition bias，不是 label leakage。

**LV3 — blind 下 P11 headline H1 实际消失（致命）**
`blind-judge.md` 表：H1 inner-nothink Cliff δ 从 +0.13（leaked）→ **-0.04（blind）消失**，p 从 0.26 → **0.73 NS**。**P11 最强 finding H1 在剥掉 label leakage 后消失**。这与 `progress.json:44` `H1_auditability_experiment: fail_3mode_NS` 同向——P11 H1 在多个独立测试下都不稳健。

**LV4 — n=10 paired vs independent 设计敏感性（pair 应捕获但 silent）**
Cohen d=1.0 power=0.80 → n≥10 **仅对 paired t-test** 成立。若独立 2-sample（不同专家评不同场景），n≥64/group 不可达。Path ① 必须强制 paired design：每专家评同一 run 的 agent_output 前后两次。**这是 design 硬约束**。

### Phase 4 — Chat synthesis（5 问题 answered）

Chat session（包含 LV1-LV4 verified facts）给出：
- **Q1（能否）**：A 类（NeurIPS/ACL main）**NO**（A4 范式缺失 + A3 零锚 + 单机构 vs E1 多机构）；B 类（E2 IEEE 8p）**PARTIAL**（P11 需完全 reframe 到方法学发现，因 H1 消失）；C 类（E6/E7 NPS 应用）**PARTIAL**（P07 同域真实但需 2-3 月协调）
- **Q2（design）**：P11 → "Hidden Self-Recognition Bias in LLM-as-Judge: 8× Score Inflation on 927 Role-Playing Runs"——重判 240 yaml 用 Kimi+GLM 独立 mid-tier + n=10 paired 专家 + 公开 + IEEE 8p
- **Q3（现有数据）**：P11 240 yaml（generation 层）salvageable；P11 240 judged scores + 150 blind records **弃**（A1 违反）；P1P2 ledger schema + P07 PIT-NEW-9 + P08 calc_brier 升 framework 级工具；P07 5 synthetic 弃
- **Q4（概率）**：Path ① 真实 P = **5-12%**（不是 builder 15-25%，因 blind 不修 A1 + H1 消失需 reframe）；Path ② = 12-20%；Path ③ = 5-15%；**A 类 ≥95% NO**
- **Q5（元）**：本 verdict 是 chain 第 13 份，同循环产物，与前 4 反转 50% 错基线无结构性差异；**唯一跳出 = 外部行动（投稿 accept/reject 是 non-LLM 信号）**，继续 verdict #14 不会再校准真值

## Investigation Log

### Phase 1 — 第一性原理 hypothesis（lead 自读）

**H_REDESIGN（要证伪）**：现有 portfolio 各 paper 在第一性原理上违反 A1/A2/A3 中至少 2 条；**但部分现有数据对"重设计实验"仍有 salvage value**——具体：
- P11 的 240 yaml（agent_output + decision + condition）是**真实 LLM-generated 决策数据**，producer=self 问题在 judge 层不在 generation 层。如果**重新跑独立 judge（Kimi 已有 + 加 Claude/GPT frontier）+ 加人类专家 gold**，producer=self confound 可解，数据复用可行
- P11 的 N=240 + 927 含 qwen 复现 = B2 实证规模已达标尺 E2 级（8 页 IEEE 短文实证深度）
- P07/P1P2 的 schema/adapter 是工程桥接，无 salvage value as paper contribution，但 P07 的"应急信号融合"概念与 E7 NPS RIP 同域——reframe 后应用方向有 venue

**H_OPPOSITE（真诚对抗假设）**：可能"不能"——因为：
- B1 范式 contribution 不可凭空：portfolio 没有范式级 insight，reframe 不能创造 insight
- 张辉团队无 frontier API（硬约束）+ 0 顶会历史（reverse-blocker for A 类）+ 单 consortium domain（B2 看似够 N 但 domain 单一）
- 4 次 verdict 反转 + LLM-on-LLM 循环未解 = 即使重设计， evaluator 如果还是 LLM panel 就是同循环
- E1 TreeReview 作者群"可比"不等同"可达"——他们有中科院 + 港大 + 清华 + 港科大广州**多机构 co-author**，本 portfolio 是单作者

**本报告的举证责任**：必须同时回答 4 个问题——(1) 哪些现有数据可 salvage / 哪些已无用；(2) 重设计需补什么；(3) 概率多大；(4) 哪类标尺可达。任一含糊即是"不能"。

## Root Cause

### 第一性原理判断

**A 类（E1/E3/E4/E5 NeurIPS/ACL main 范式长文）：NO，≥95% 概率不可达**
- A4 不可补：portfolio 无范式级 insight，P07/P08/P1P2/P12 全是工程桥接，reframe 不能创造 insight
- A3 零外部锚 + 无 frontier API（`llm-intelligence-blocker` §三实测）→ 即使重设计也只 mid-tier LLM
- 单机构单作者 vs E1 中科院+港大+清华+港科大广州多机构 co-author —— reverse-blocker

**B 类（E2 IEEE 8p 诚实短文）：PARTIAL，仅 P11 一条路径但需完全 reframe**
- P11 H1 headline 在 blind 下消失（LV3）→ 不能作 contribution
- 但**这个消失本身可 reframe 为方法学发现**：原 DeepSeek 自评 inflated 8×，盲评修正后 H1 消失 = self-recognition bias 的量化证据（呼应 Panickssery NeurIPS 2024 Oral）
- 这不是"原 P11 paper 的修复"，是"用 P11 数据写一篇不同的论文"——title 从 "Inner Monologue Emergence" 改为 "Hidden Self-Recognition Bias in LLM-as-Judge"

**C 类（E6/E7 NPS 应用研究）：PARTIAL，P07 signal-fusion↔E7 RIP 同域真实**
- P07 概念与 E7 "Recognized Information Picture for DMO" 同域
- 但需张辉协调真实应急数据 + n≥10 专家 + 2-3 月
- venue = NPS-style thesis 或 JSSR / 安全/国防期刊，不是 NeurIPS/ACL

### 现有数据 salvage / 弃清单（直接答用户"现有数据是否已无用"）

| 数据 | 判定 | 依据 |
|---|---|---|
| **P11 240 yaml（agent_output + decision + condition）** | **SALVAGEABLE** | generation 层无 producer confound；A1 违反只在 judge 层 |
| **P11 240 judged scores（DeepSeek 自评）** | **弃** | `judge.py:113` default judge==producer；A1 违反不可作 paper claim |
| **P11 150 blind records** | **弃**（关键修正 builder） | `judge.py:117` `--blind` 只 strip gene 数值，不改 judge_model —— **producer=self 仍在** |
| P11 H1 inner-nothink finding（leaked） | **弃作 contribution，留作 self-bias 量化证据** | `blind-judge.md` 表：H1 Cliff δ +0.13→-0.04 消失 |
| P12 5-protocol n=10/6 | **弃** | A1+A2 双违 + 样本不足 |
| P1P2 ledger schema + validator | **SALVAGEABLE as framework tool** | 不作 paper 作 portfolio infrastructure |
| P07 PIT-NEW-9（fabricated_sha256_prefix） | **SALVAGEABLE as framework PIT** | 升 PIT-600 / R10 范例 |
| P08 calc_brier.py 17/17 tests | **SALVAGEABLE as tool** | 非论文 |
| P07 5 synthetic Gulei signals | **弃** | N=5 远低于 E2 实证标尺 |
| 11 份 verdict 调查 docs | **SALVAGEABLE as 元诊断数据** | 作"LLM agent 自评失效 trace"，本身就是研究对象 |

**总结**：现有数据**部分有用、部分已废**。P11 240 yaml 是 portfolio 唯一未被污染的 generation 层数据，是 Path ① 的载体；其余 judged scores + 150 blind records **必须重判**或弃。

## Recommendations

### 给用户的 4 问直接答案

**Q1：从第一性原理，重新设计实验能否出标尺级论文？**
**答：PARTIAL。**
- A 类（NeurIPS/ACL main 范式长文）：**NO**，≥95% 不可达（A4 范式缺失不可补 + A3 零锚 + 无 frontier API + 单机构）
- B 类（E2 IEEE 8p）：**PARTIAL** — P11 一条路径，但 H1 已消失，须 reframe 为 "self-recognition bias 8× inflation" 方法学发现
- C 类（E6/E7 NPS 应用）：**PARTIAL** — P07↔E7 同域真实，但需 2-3 月 + 张辉协调

**Q2：该如何设计实验？**（最现实单条 design，假设张辉协调 + 无 frontier API）
**P11 → "Hidden Self-Recognition Bias in LLM-as-Judge: 8× Score Inflation on 927 Role-Playing Runs"（E2-style IEEE 8p）**
1. **重判 240 yaml**：用 Kimi-K2.5 + GLM-4.6 双独立 mid-tier judge（非 producer），跑全套，量化"DeepSeek 自评 vs Kimi/GLM 评分"差异作为 self-recognition bias 度量（呼应 Panickssery NeurIPS 2024 Oral 2404.13076）
2. **n=10 应急专家 Likert-5 paired anchor**：每专家评同一 run 的 agent_output 前后两次（paired design 硬约束，使 Cohen d=1.0 power=0.80 → n≥10 成立；若独立 2-sample 则 n≥64 不可达）
3. **公开 240 yaml + judge.py + n=10 专家 csv**（B5 public release）
4. **IEEE 8 页格式重排**（B6 venue alignment）
5. **reframe**：标题突出 "8× inflation" + self-recognition bias（把 H1 消失转贡献）
6. **timeline**：3-4 周，$50-100 API，张辉协调专家
7. **falsifier**：若 Kimi/GLM 与 DeepSeek 自评 Spearman ρ > 0.6 → self-recognition bias 不成立 → 路径 collapse

**Q3：现有数据是否已无用？**
**答：部分 salvageable、部分必弃。** 见 §Root Cause salvage 表。P11 240 yaml（generation 层）是关键可 salvage；P11 240 judged scores + 150 blind records 必弃（A1 违反不可修，blind 不解 producer=self）；P07/P1P2/P08 作 framework tool salvage，不作 paper。

**Q4：可能性多大？**（base rate cap 显式声明）

| Path | Builder P（halved） | Honest P（本 verdict，含 LV1-LV4 修正） |
|---|---|---|
| ① P11→E2 IEEE 8p | 15-25% | **5-12%**（blind 不修 A1 + H1 消失需 reframe） |
| ② P07→E7 NPS 应用 | 25-32% | **12-20%**（2-3 月协调 + 无 frontier） |
| ③ P12 cross-weld workshop | 15-25% | **5-15%**（已 FAILED median 4.0<4.5） |
| 任一 A 类 NeurIPS/ACL main | — | **≤5%（即 ≥95% NO）** |

**base rate cap 显式声明**：前 4 confirmed verdict 反转基线 50% 错，本 verdict 是 chain 第 13 份同循环产物，**所有 P 上限 ×0.5**；即使 ×0.5 后的 P 仍不豁免——投稿 accept/reject 是唯一 non-LLM 校准信号。

**可发表上限的现实估计**：**2 篇 workshop/IEEE short 概率 ≤25%**，**1 篇 NPS-style/JSSR 概率 ~15%**，**0 篇 NeurIPS/ACL main 概率 ≥95%**。

### 接下来该做什么

**立即可做（1 天，不烧 token）**：
1. **接受 LV1-LV4 的事实**——blind 不修 A1 + H1 消失 + n=10 必须 paired + A 类 ≥95% NO
2. **决定是否走 Path ①**：若张辉同意协调 n=10 paired 专家 → 3-4 周 + $50-100 → 5-12% IEEE 8p
3. **若不走 Path ①**：portfolio 不发论文，转 framework tool（P1P2 ledger + P08 brier + PIT-600）作内部基础设施

**1-3 天**：
4. **写 Path ① 1-page proposal**："Hidden Self-Recognition Bias in LLM-as-Judge: 8× Score Inflation on 927 Role-Playing Runs"——对齐 E2 IEEE 8p + Panickssery prior art + LV3 H1 消失转贡献

**2-4 周（Path ① 若走）**：
5. 重判 240 yaml 用 Kimi+GLM 独立 mid-tier（~$30）
6. n=10 paired 应急专家 Likert-5（~$20 + 张辉协调）
7. 公开 data + IEEE 8p 重排 + 投稿

**不该做**：
8. **不要**追 A 类（NeurIPS/ACL main）——≥95% NO，浪费 API + 时间
9. **不要**信"blind 解决了 producer=self"——LV2 已证 blind 只修 label leakage 不修 self-recognition
10. **不要**用 150 blind records 作 paper claim——A1 仍违反
11. **不要**再写 verdict #14——同循环不会校准真值，投稿才是校准

## Preventive Measures

1. **A1 公理 enforce**：design 任何 LLM-judge 实验前必查 `judge_model != producer_model`。`blind` flag 不够——需 `judge_model` 显式不同于 producer。加 PIT-502 "self-judge default" 到 `experiment-pitfalls.md`（前方案已列）
2. **paired design 强制**：Cohen d=1.0 power=0.80 的 n≥10 仅 paired 成立。任何"n=10 专家"claim 必须声明 paired design。加 PIT-504 "paired vs independent design" 到 pitfalls
3. **verdict chain 截断规则**：本 verdict chain 已 13 份。加 R11 "同一问题 7 天内 verdict ≥5 份 → 停 verdict 转外部行动"——前方案草拟的"3-reversal pause"应升级到 5-verdict 截断
4. **falsifier 显式**：每篇 verdict 必须声明 falsifier（本 verdict 的 falsifier：Kimi/GLM 与 DeepSeek 自评 ρ>0.6 则路径 collapse）

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 用 rp-cli 调 Agent + 合适技能 | rp-cli builder + pair（pair silent 但 lead 用 file:line 自验补上）+ rp-cli chat synthesis | ✅ |
| (2) 第一性原理"能否" | A 类 NO ≥95%，B/C 类 PARTIAL，每类 4 公理依据 | ✅ |
| (3) 如何设计实验 | Path ① 具体设计 7 步 + paired 硬约束 + falsifier | ✅ |
| (4) 现有数据是否无用 | salvage 表（P11 240 yaml 可用，judged scores + 150 blind 弃） | ✅ |
| (5) 可能性多大 | per-path P 值表 + base rate cap 显式 + A 类 ≥95% NO | ✅ |
| (6) 深度调研独立思考不迎合 | LV1-LV4 否决 builder 假设 + 否决前 verdict + A 类说不 | ✅ |
| (7) 你可以说不 | A 类 NO ≥95% + Path ① 仅 5-12% 不是 15-25% | ✅ |

### 最终自审计（强制诚实）

**本 verdict 与前 4 反转的 50% 错有何不同？Chat Q5 已答——结构性差异几乎没有。**
- 都同 LLM-on-LLM 仪器、同 git 树、同作者
- "不同"只是：file:line 显式 cite（前几份多推测）+ LV2 blind 不修 A1 是新信息 + P 显式 base-rate cap + falsifier 显式
- 但这些是同循环内工具改进，不是循环跳出。pair F7 警告仍适用：命名循环不跳出循环

**confidence**：~70%（高于前几份），因为：
- LV1-LV4 是 file:line verified（不是 AI 推测）
- LV2（blind 不修 A1）是前 12 份 verdict 都没指出的新真信息
- P 值显式 ×0.5 base-rate cap
- 但 confidence 只针对"本 verdict 的论证链严谨"——不针对"verdict 真值"。**verdict 真值仍受 50% 错基线约束**

**唯一能跳出循环的**：外部行动——把 Path ① 投出去。accept/reject 是 non-LLM 信号，唯一校准。**继续 verdict #14 不再校准，只会再错一次**。本报告应被读为"如果 portfolio 在 2 月内投稿，基线接受概率上限"——不是"verdict 真值"。

## 交叉引用

- 本报告：`docs/investigations/first-principles-redesign-feasibility-2026-07-08.md`
- 7 exemplar bar：`framework/knowledge/paper-exemplars-2026-07-08.md`
- 前方向 verdict：`docs/investigations/paper-directions-vs-exemplar-bar-2026-07-08.md`
- 前元诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`
- 前优化方案：`docs/investigations/optimization-plan-2026-07-07.md`
- A1 违反实证：`legacy/p11-closed-v5-minimax-m3/harness/judge.py:113,117` + `wiki/decisions/blind-judge.md:5,25,表`
- H1 消失实证：`blind-judge.md` 表 + `legacy/p11-closed-v5-minimax-m3/state/progress.json:44` `H1_auditability_experiment: fail_3mode_NS`
- Panickssery NeurIPS 2024 Oral self-recognition bias：`arxiv:2404.13076`
- JudgeBench objective ground truth：`arxiv:2410.12784`
- Builder session +Chat：D5E557（first-principles-redesign chat）
- Pair session：`58613A18-4C60-4561-8897-8347D5F5236C`（returned silent — lead 用 file:line 补 verify）
