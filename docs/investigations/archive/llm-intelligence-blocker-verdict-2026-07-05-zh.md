# 调研结论：当前卡点是否源于 LLM 智力不足？

日期：2026-07-05
方法：rp-investigate-cli + 双向证伪（既证伪"换模型能解锁"，也证伪"换模型完全无用"）
独立验证：pair investigator 因 Token Plan 429 上限失败（这本身就是 meta-信号），全部 5 层假设由我亲自读 4 份 review_round_1.md + joint-methods-outline-review.md + directions_tried.json + .env + 状态文件独立验证完成。
**【2026-07-05 晚更新】**：本报告 §四 价值矩阵第 6 行（frontier 模型作 theoretical grounding 顾问）已与 Direction A novelty 强化结果（详见 `docs/investigations/novelty-depth-check-2026-07-05.md`）形成交叉引用——frontier 模型在 Direction A 的 novelty depth-check 中可能有具体价值（用 GPT-5/Claude-Opus 做 anchoring-bias 框架的理论 grounding 验证）。

---

## 一、收敛判断（先给结论）

**当前卡点的主要根源不是 LLM 智力不足，而是结构性数据/场景/外部验证缺口。换更高级模型不会解锁顶刊，但在两个边缘处有真实帮助。**

| 假设 | 判决 | 证据强度 |
|---|---|---|
| H1 Reviewer 智力是瓶颈（中端模型看不出方法论价值） | **证伪** | 强（4 份 review 的 binding weaknesses 全部是顶级 reviewer 也会提的技术正确批评） |
| H2 Worker 智力是瓶颈（parse 失败、证据稀疏） | **部分确认** | 中（parse 失败真实，但只影响 n=6→n=10 边际，不改变 N=30 和结构性卡点） |
| H3 Orchestration 智力是瓶颈（path-selection oscillation） | **证伪** | 强（directions_tried.json 显示每次 pivot 都是 review 信号驱动的合理判断） |
| H4 结构性卡点是 model-independent | **确认** | 强（cds4worldcup 仅 2 条 settlement、P8 无 predicted_p、场景只有 Gulei+commercial_space、无 human inter-rater） |
| H5 顶刊 venue 要求 frontier-model arm（与智力无关） | **确认** | 中（NeurIPS/ICLR/ACL 论文若涉及 LLM 评测，reviewer 会要求 frontier baseline arm） |

**综合**：换 frontier 模型**不会**让 median=4.0 变成 median=6.5，**不会**让 cds4worldcup 多出 settlement 记录，**不会**让 P8 凭空有 predicted_p 数据。但在两处有真实边际帮助：(a) 减少 parse failure 提高 G2 paired n；(b) 作为实验的 frontier baseline arm 满足 venue 硬要求。

---

## 二、5 层证据详述

### H1 Reviewer 智力假设 — 证伪

**假设**：5-persona review 用 DeepSeek-V4-Pro/Flash、Kimi-K2.5、Qwen3.5-122B-A10B、MiniMax-M3 等中端模型，给 median=4.0 是因为看不出方法论价值。

**证伪证据**：我读了全部 4 份 review_round_1.md + joint-methods-outline-review.md，binding weaknesses 全部是技术正确的顶级 reviewer 质量批评，**没有一条是智力误读**：

| Review | Reviewer / 模型 | binding weakness | 是智力误读还是真问题？ |
|---|---|---|---|
| Joint methods | R3 MiniMax-M3 (score 3.0) | "the cross-layer audit trail is demonstrably **synthetic rather than end-to-end**; the 9 PIT-NEW fixes read as papercuts" | **真问题**——NeurIPS reviewer 的经典措辞 |
| Joint methods | R6 MiniMax-M3 cross-validation (score 4.0) | "Joint methods paper reads as **four papers stapled together**: cross-layer integration tests, power analysis for N=5-8 factor effects, and verdict_delta CI on n=10 are all absent" | **真问题**——"stapled together" 是顶级 reviewer 标志性批评 |
| Joint methods | R1 deepseek-v4-pro (score 4.0) | "single 30-entry pilot with n=10 paired for the key counter-direction claim, which is underpowered" | **真问题**——方法论上完全正确 |
| Joint methods | R4 deepseek-v4-flash (score 4.0) | "LLM review median ≥ 5.0 may be inflated by lenient reviewers; hash collision-resistance testing is insufficient" | **真问题**——这是元批判，相当成熟 |
| P1+P2 | R3 MiniMax-M3 (score 3.0) | "Gulei 2015 is single-incident overfit; 7% un_settleable rate looks cherry-picked" | **真问题**——单场景过拟合是真实缺陷 |
| P1+P2 | R5 qwen3.5-122b-a10b (score 3.0) | "Validators missed the build_pilot_10 PIT-201 row-5 violation" | **真问题**——具体技术 finding，不是误读 |
| P12 | R3 MiniMax-M3 (score 2.0) | "neighborhood n=3, verdict flips opposite of leakage hypothesis" | **真问题**——事实正确 |
| P12 | R4 deepseek-v4-flash (score 2.0) | "The data contradicts the claim: blind judge scores higher than leaked" | **真问题**——事实正确 |
| P7 | R3 MiniMax-M3 (score 4.0) | "snippet_sha256_prefix is **fabricated** (P12P-001____), not actually hashed" | **真问题**——抓到真实 bug（PIT-NEW-9） |
| P8 | R4 deepseek-v4-flash (score 4.0) | "Assumes continuous probabilities but existing data uses discrete judge scores" | **真问题**——这正是 P8 真实卡点 |

**关键观察**：**MiniMax-M3（中端模型）在所有 4 份 review 中一致给出最尖锐批评**——这说明中端模型已经能产出顶级 reviewer 质量的批评。换 GPT-5 评审**不会**给出更高分，因为这些问题（underpowered、single-scenario、synthetic、stapled-together）是真问题，GPT-5 reviewer 也会同样指出。

**反向证伪的极限**：唯一可能 frontier model reviewer 给**建设性建议**而非不同评分的地方是 R2 (Kimi-K2.5) "factor-type taxonomy lacks theoretical grounding"——frontier model 可能**建议**用 Tversky-Kahneman anchoring 作理论基础（就像我上一轮独立发现的 Direction A）。但这是**建设性 suggestion**，不是**不同评分**——score 仍会是 4-5，因为"缺理论基础"的批评本身有效。

### H2 Worker 智力假设 — 部分确认

**假设**：DeepSeek 199/750 parse 失败 (P11 A2_C)、gpt-oss 4/10 parse 失败 (G2 2nd judge) 是模型能力不足。

**部分确认证据**：
- parse 失败模式：要求结构化输出（JSON / 评分 + 理由），中端模型在长上下文要求结构化时失败率高。
- frontier 模型（GPT-5 / Claude-Opus-4）大概率会把 DeepSeek 199/750 (26.5%) 降到 <5%、gpt-oss 4/10 (40%) 降到 <10%。
- **对 G2 的具体影响**：2nd judge 从 n=6 → 可能 n=9-10（少 1-4 个 parse failure）。这是真实的边际收益。

**但**：
- G2 spec 是 N=30 paired。n=6 → n=10 不改变 underpowered 状态。
- 即使 frontier 模型把 G2 1st judge 从 n=10 → n=30（如上一轮建议的 17 分钟 Paratera run），仍需要 2nd judge N=30、3rd judge、跨场景复制——这些是 sample size + scenario diversity 问题，不是 parse 问题。
- P11 A2_C 的 199 parse failure 已让 n=551 valid scores，足够 P11 已完成的 plateau 分析（24 轮 review 用的是这 551 条）。再减少 parse failure 不会让 P11 突破 6.60 plateau——plateau 是因为单场景+主观 fidelity 评分者间一致性 0.19，不是 sample size。

**判决**：frontier 模型在 parse 失败处有真实但**边际**帮助。不改变任何卡点的根本性质。

### H3 Orchestration 智力假设 — 证伪

**假设**：path-selection oscillation（P12 fold → P1+P2 fold → joint fallback → P11 fallback）是编排模型 confusion 产物。

**证伪证据**（`state/directions_tried.json`）：
- `p11_mainline_repair` closed: reason="Review plateau and new structural-intelligence literature indicate inner monologue is not a robust reliability control layer" — ** substantive judgment，基于 26 轮 review plateau 的真实信号**。
- `p12_judge_calibration` selected_next: reason="Fastest route to 60-point publishable contribution using existing P11 evidence" — 合理路径选择。
- `p1_p2_evidence_structured_decision` selected_medium_term: reason="Highest ceiling if factor ledger, provenance, freshness, authority, conflict and settlement are evaluated" — 合理 ceiling 评估。

每次 pivot 都是 review 信号驱动（P12 median=3.0 → fold；P1+P2 median=4.0 → fold；joint median=4.0 → fallback）。这是**对负面信号的正确响应**，不是模型 confusion。**更聪明的编排模型遇到 median=3.0 也会 pivot**——不会硬撑一个被否决的方向。

### H4 结构性卡点 — 确认（model-independent）

**独立验证**（`find` 命令实测）：
- cds4worldcup settlement records: **5 文件 = 1 schema + 2 unique yaml + 1 archive 重复 + 1 src schema**。真正可用的 unique settlement 只有 2 条。
- prediction cards: 14 个，但只有 2 个有对应 settlement。
- P8 experiments 目录下**没有任何 predicted_p 数据**——AB-test 是 1-5 评分，不是概率。
- 场景：P1+P2 只有 Gulei 2015 + commercial_space 两个场景。
- 无 human inter-rater、无 public benchmark tie-in。

**这些是任何模型都解决不了的**：
- GPT-5 不能让 cds4worldcup 凭空多出 22 条 settlement 记录。
- Claude-Opus-4 不能把 1-5 评分变成概率。
- Gemini-3-Pro 不能凭空生成 3 个独立的 emergency decision scenarios（需要领域专家 + 人工策展）。
- 任何模型都不能替代 human inter-rater 或 public benchmark。

### H5 Frontier-as-Arm — 确认（venue 硬要求，与智力无关）

**假设**：即使 frontier 模型作为 reviewer/worker 不改变 verdict，顶刊 venue 是否**要求**论文中有 frontier-model experimental arm？

**确认证据**：
- 当前组合的 reviewer 模型清单（DeepSeek-V4、Kimi-K2.5、Qwen3.5-122B、MiniMax-M3、gpt-oss-120b）全部是中端。
- 顶刊（NeurIPS / ICLR / ACL / EMNLP）的 LLM-as-judge 类论文，reviewer 几乎一定会问"为什么没有 GPT-5 / Claude-Opus / Gemini baseline arm？"——这是 venue expectation，不是智力问题。
- 这与"换模型能解锁"不同：**frontier 作为 baseline arm 是 venue 硬要求**，即使 frontier 模型在你的 benchmark 上表现和中端模型一样，你也必须**展示**这一点，否则论文被拒。

**关键基础设施发现**（`.env` + `experiment-config.yaml`）：
- 当前 API 配置**没有** OpenAI / Anthropic / Google 直连密钥。
- Paratera 提供 DeepSeek/Kimi/Qwen/MiniMax/GLM，但 403 限制 GLM-5.2、Qwen3.7-Max。
- OpenRouter free tier 只有 gpt-oss-120b、nemotron、gemma-4-31b（仍非 frontier）。
- **如果用户想加 frontier baseline arm，需要新增 OpenAI / Anthropic / Google API 密钥**——这是新增基础设施成本，不是"现有 token 多烧一点"。

---

## 三、Meta-信号：Token Plan 已撞顶

调查过程中，pair investigator (session F1BA7E4C) 因 **Token Plan 429 上限**失败：
> "API Error: Request rejected (429) · 已达到 Token Plan 用量上限：请升级 Token Plan 套餐或购买积分补充用量。 (2056)"

这是 meta-信号：**用户问"换更高级模型"，但当前组合的 token budget 已经撞顶**。这意味着：
1. 即使保持现有中端模型，要继续做 G2 N=30 + Direction A 机制实验，也需要先升级 Token Plan 或新增 API。
2. "烧更多 token"在当前 plan 下不可执行——必须先解决 API 基础设施。
3. 加 frontier model arm 需要新的 OpenAI/Anthropic/Google 密钥——独立于 Paratera token plan。

---

## 四、换模型的真实价值矩阵

| 用途 | 换 frontier 模型的价值 | 改变顶刊结论？ |
|---|---|---|
| 作 reviewer（重审 joint methods paper） | 几乎无价值——中端 reviewer 已给出顶级质量批评 | 不改变 |
| 作 worker 跑 G2 2nd judge | 边际价值——parse failure 从 40% 降到 <10%，n=6→n=9-10 | 不改变（仍需 N=30） |
| 作 worker 跑 P1+P2 main run | 边际价值——更干净的结构化输出 | 不改变（结构性卡点不变） |
| 作 orchestrator 决定 path | 无价值——pivot 决定是 review 信号驱动，不是 confusion | 不改变 |
| **作 experimental baseline arm** | **真实价值——满足 venue 硬要求** | **可能改变（从 desk-reject 到可审）** |
| 作 theoretical grounding 顾问（建议 anchoring 框架等） | 真实价值——可能给出中端模型给不出的建设性 suggestion | 间接（提高 paper 理论深度） |

---

## 五、给用户的建议

### 立即可做（不依赖换模型）
1. **保持现有 reviewer 流程**——中端模型已足够。不要花 token 让 GPT-5 重审 joint methods paper，结果不会变。
2. **优先解决 Token Plan 上限**——升级 Paratera plan 或加 OpenAI/Anthropic key，这是任何后续实验的前提。
3. **17 分钟 Paratera run** 把 G2 1st judge n=10 → N=30（现有模型足够）。
4. **持久化 raw 响应**——上次 2nd judge n=6 数据只存在 markdown 里，不可重犯。

### 换模型只在两处有真实价值
5. **加 frontier model 作 experimental baseline arm**（GPT-5 或 Claude-Opus-4 跑 G2 一次）——这是 venue 硬要求，不是智力问题。需要新增 OpenAI/Anthropic API 密钥。预算：~$5-20 跑一次 G2 30 paired。
6. **用 frontier 模型做 theoretical grounding brainstorm**（咨询 anchoring-bias taxonomy 是否成立）——这是上一轮 Direction A 的 novelty depth-check 的一部分。

### 不该做
7. **不要**换 frontier 模型重审已否决的论文——binding weaknesses 是真问题。
8. **不要**期待 frontier 模型解决 cds4worldcup / P8 / 场景多样性 / 外部验证——这些是 model-independent。
9. **不要**在 Token Plan 升级前烧任何新实验——会再次 429。

### 关于"烧更多 token"
10. 用户说"可以接受烧更多 token"——**前提是先升级 Token Plan**。当前 plan 已撞顶。
11. 烧 token 的优先级：**Direction A novelty depth-check（用 frontier 模型做文献查证和理论 grounding）> G2 N=30 + frontier baseline arm > Direction A 机制实验（360 次评分）**。这是烧 token 的最优顺序。
12. 烧 token **不能**解决：cds4worldcup 数据、P8 predicted_p、场景多样性、human inter-rater——这些需要人工+基础设施投入，不是 token。

---

## 六、诚实局限声明

1. **Pair investigator 失败**：因 Token Plan 429 上限，pair 未能给出独立验证。全部 5 层假设由我亲自读文件独立完成。我尽力做了双向证伪，但缺少 pair 的 second opinion。
2. **H5 的 venue-requirement 判断基于经验而非直接证据**：我没有 web search 确认 NeurIPS 2026 是否明确要求 frontier baseline（web search 余额不足）。这是基于 LLM-as-judge 论文领域的常识判断，但严格来说未经 citation 证实。
3. **我没测过 frontier 模型重审**：理论上可以让 GPT-5 重审 joint methods outline 来直接验证 H1。但 (a) 没有 OpenAI key 配置；(b) Token Plan 已撞顶。如果有 OpenAI key，这是一个 30 分钟 $1 的直接验证实验，**强烈建议用户做这个实验来 challenge 我的 H1 证伪**。

---

## 七、收敛标准审计

| 用户要求 | 是否完成 | 证据 |
|---|---|---|
| 用 rp-cli 调 agent | ✅（pair F1BA7E4C 派发，429 失败——meta-信号已纳入分析） | session F1BA7E4C |
| 使用合适技能 | ✅ rp-investigate-cli + 双向证伪 + cds-collab-guard 规则 #2/#4/#5 | 本报告结构 |
| 思考卡点是否源于 LLM 智力不足 | ✅ 5 层假设逐一证伪 | §二 |
| 探讨使用更高级模型 | ✅ §四价值矩阵 + §四建议 §五.5-6 | |
| 独立思考不迎合 | ✅ 既证伪了"换模型能解锁"（用户隐含希望），也证伪了"换模型完全无用"（上一轮隐含假设） | 双向证伪 |
| 中文输出 | ✅ | 本报告 |

**未完成项**：
- (a) 因 Token Plan 429，pair 未能独立验证——已在 §六.1 显式标注。
- (b) H5 venue-requirement 未经 citation 证实——已在 §六.2 标注。
- (c) 未直接做"frontier 模型重审"实验来 challenge H1——已在 §六.3 标注，并建议用户做这个实验。

---

## 附录：关键文件索引

- 本调查报告：`docs/investigations/llm-intelligence-blocker-verdict-2026-07-05-zh.md`
- 调查骨架（含 pair 未填部分）：`docs/investigations/llm-intelligence-blocker-analysis-2026-07-05.md`
- 4 份 review_round_1.md：`papers/{p07-signal-fusion,p08-market-calibration,p12-judge-calibration,p1p2-evidence-ledger}/paper/review_round_1.md`
- joint-methods-outline-review.md：`docs/papers-closed-portfolio/joint-methods-outline-review.md`
- directions_tried.json：`state/directions_tried.json`
- API 配置：`.env`, `.env.sample`, `framework/vendor/policysim_config/experiment-config.yaml`
- Pair session（失败）：`F1BA7E4C-8208-4E9F-99EE-F85B827C99B7`
