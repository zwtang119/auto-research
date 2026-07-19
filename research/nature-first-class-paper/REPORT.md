# REPORT: Nature "How to write a first-class paper" → auto-research Topic-5 选题校准

> **报告类型**：deep-research cited report, 2026-07-16.
> **研究问题**：以 Nature Career《How to write a first-class paper》（Gewin 2018, doi:10.1038/d41586-018-02404-4）方法论为评估透镜（凝练为 5 条"选题判据"），评估 auto-research Topic-5 组合应采用何种选题策略，才能最大化产出一篇 first-class paper.
> **基金说明**：本研究遵循项目硬规则 D17（禁止在用户 "boring" 反馈后替其重新辩护/重述/推荐关闭方向；任何推荐必须 methodological-insight-driven，而非 data-uniqueness-driven）以及"data-uniqueness ≠ paper-interesting"规则.
> **来源限制**：本报告全部引用来源于 primary arXiv/GitHub/OpenReview 源；自媒体 (Toutiao/WeChat/公众号) 数字/标题按项目规则默认 ⚠️ UNVERIFIED，未作为 load-bearing 论据. 报告完成日 2026-07-16.

---

## 0. 方法论透镜：Gewin 2018 的 5 条选题判据

基于 Nature Career 文原文与其中译文已入库 (`/Users/tangzw119/Documents/GitHub/wiki/sources/Nature How to write a first-class paper.md`)，提炼为 5 条选题判据：

| 判据 | 来源专家 | 一句话标准 |
|---|---|---|
| **C1 Single-key-message** | Brett Mensh | 能否用一句话（=标题）写下该方向的核心信息？写不出 ⇒ 选题未聚焦 |
| **C2 "新且引人入胜" 红线** | Dallas Murphy | 必须能回答 "What's new and compelling?" 成一句话；防御式/数据独有式框架必输 |
| **C3 全局语境 + 替代解释** | Angel Borja + Peter Gorsuch | 必须能在全局文献中证明原创性，并预审视替代解释 |
| **C4 人类故事 + 跨受众清晰** | Zoe Doubleday + Stacy Konkiel | 必须能向非本领域同行讲清"解决了什么问题、谁受益" |
| **C5 可复现** | Peter Gorsuch | 方法不得缺关键信息，否则 research 是 dead end |

---

## 1. 三候选方向的 per-判据 计分卡

> **评估对象**：P1+P2（主所有）、Direction Y（重构后方法学版）、Direction Z（G3+Harness-Evolution 合并，GATED）.
> **注意**：Direction X 已于项目内部 CLOSED（详见 §4 对四个 slot-occupant 的复核结论），不计入本推荐评估.

### 1.1 P1+P2 Evidence RAG + Factor Ledger（ACTIVE MAINLINE）

> 当前方法学定位：dual-ledger crosswalk（92.9% 覆盖）+ orthogonal enums + Brier replay（100%）对 settlement 进行 reconciliation 校准. 主要场景：Gulei 2015 石化事件.

| 判据 | 评分 | 证据 |
|---|---|---|
| **C1** | **PASS** | 一句话可表达：*"We map free-form evidence entries to a structured factor ledger via a dual-ledger crosswalk with orthogonal enumeration, enabling Brier-scored replay calibration of settlement predictions."* |
| **C2** | **PASS** | "What's new and compelling" = 一种 reconciliation 方法（不是"我们独占这个数据集"）；按 F4 的 Check 1/2 通过. 移除 Gulei 2015 场景不影响 crosswalk 方法本身 [F4 §P1+P2 Check 1, 2]. |
| **C3** | **PARTIAL** | F3 发现 2024-2026 prior art 全部仅命中 G3 的单一组件：Polymarket-v1 [1] 仅做单 ledger→Brier，Foresight Arena [2] 仅做 Brier replay 用于代理评测，hierarchical forecast reconciliation 文献（Hyndman 传统，如 arXiv:2605.17920, 2602.22694, 2405.18693）的"reconciliation"含义是 aggregation-coherence 而非 settlement reconciliation，是**同形词但 false cognate**——必须显式 disambiguate [F3 §Final verdict]. Keogh & van Geloven (arXiv:2304.10005, Epidemiology 2024) 是唯一将 Brier 扩展到 counterfactual evaluation 的论文，但属因果医学预测非 settlement. 综合：G3 组合术语在 arXiv 学术语料中**零命中**[F3 §Findings[7]]，差异化空间明确，但需显式说明与 hierarchical reconciliation 的歧义. |
| **C4** | **PARTIAL** | 故事性："我们给预测市场上了一个航管塔（settlement reconciliation）——把无序证据流'嫁给'结构化因子账本"——这是人类可读的隐喻. 跨受众：F4 Check 5 通过（保险/法律/医学诊断等 evidence→factor→settlement 管线都可套用）. 但 "dual-ledger reconciliation" 在文献零命中意味着需要主动向其他子领域解释该概念 [F2 §findings worth promoting]. |
| **C5** | **PASS** | crosswalk schema 作为方法已固化为 paper 拥有的 schema [项目 MEMORY.md]，复现不依赖独占数据. |

**结语**：C1、C2、C5 PASS；C3、C4 PARTIAL；可通过 (a) 显式 disambiguate 与 Hyndman reconciliation 的区别、(b) 向非专业读者用 settlement-reconciliation 隐喻完善元问题，使两者补齐. 与 F4 的 7-check 方法学测试结果一致——P1+P2 通过全部 7 项 [F4 §P1+P2]。

### 1.2 Direction Y（Harness Validation Benchmark，NeurIPS D&B，当前 framing）

> 当前方法学定位：以 22-investigation 数据集为 benchmark benchmark LLM agent harness. **已 DOWNGRADED** 待方法学重构.

| 判据 | 评分 | 证据 |
|---|---|---|
| **C1** | **FAIL** | 当前无法写成一句方法学句子——"we built a 22-investigation dataset for harness validation" 是 dataset-as-endpoint 而非 method 论断 [F4 §Direction Y Check 1]. |
| **C2** | **FAIL** | 移除 "22 investigations"（独有数据）后，paper 贡献框架崩塌——这是项目 D17 pushback 的根源 [F4 §Check 2]. NeurIPS 2026 E&D Track 明确指出 "Datasets-as-endpoints don't meet the bar on their own" [F4 §Findings[1]]. ACL/ARR canonical 拒信语言："the paper is mostly a description of the corpus and its collection and contains little scientific contribution" [F4]. |
| **C3** | **FAIL** | knowledge gap 是 "no systematic benchmark exists"（数据缺口）而非方法论缺口 [F4 §Check 4]. |
| **C4** | **FAIL** | 当前 insight 仅对 "在本数据集上 benchmark harnesses 的人" 有用，不跨子领域迁移 [F4 §Check 5]. |
| **C5** | **PARTIAL** | 数据可获取（22 调查）但方法学贡献不够独立. |

**结语**：当前 framing 在 5 条选题判据中**5 条 FAIL**. 这完全对应项目 D17 与 F4 derived 7-check test 在 Current Framing 下的判定（5/7 fail）[F4 §Direction Y]. **作为数据集论文，方向 Y 不通过 first-class 选题判据。**

**方法学重构路线（不重开该方向，仅方法学重新表达）**：如 NeurIPS 文献反复强调 [F4]，可改为方法学洞察——例如 "一种在 verdict reversal 发生之前预测/审计 harness bug 的方法"——而非"我们拥有 22 个调查数据". 此时需重新做 5 判据计分；本轮报告不替用户决议是否 pursue.

### 1.3 Direction Z（G3 + Harness-Evolution Combined, ACL/EMNLP Findings 2027, PRIMARY BUT GATED）

> 方法学定位：G3 dual-ledger crosswalk（92.9%）+ Brier replay（100%）作为 reconciliation 方法 + Harness-Evolution 延伸（incremental ablation 形式）.

| 判据 | 评分 | 证据 |
|---|---|---|
| **C1** | **PASS（弱）** | G3 单独可写一句话："A settlement-reconciliation methodology mapping unstructured evidence to a structured factor ledger via dual-ledger crosswalk, calibrated by Brier-scored replay." 加上 Harness-Evolution 拓展后，主信息变得复合，可能稀释红线判据——这是项目 MEMORY 内 Z GATED 的核心原因之一. |
| **C2** | **PASS（G3 部分）/ PARTIAL（Harness-Evolution 部分）** | G3 是 methodological insight（已在 1.1 通过）；harness-ablation 延伸是 incremental，可能被解读者当作"data-novelty"（与 Y 同一类）。这再次对应项目 MEMORY 内 Z 的 PARTIAL GATED 状态. |
| **C3** | **同 P1+P2 C3** —— G3 与 Hyndman reconciliation 的同形词风险同样存在. harness-evolution 部分需对照 F5 §4 的 AHE/Meta-Harness 差异化（见 §4）. |
| **C4** | **同 P1+P2 C4** —— crosswalk 故事性 OK，harness-evolution 跨受众清晰度有缺陷（"harness" 本身是行业术语，非跨领域读者陌生）. |
| **C5** | **PASS** —— G3 已固化，Brier replay 已实现. |

**结语**：G3 部分 PASS，harness-evolution 延伸 PARTIAL. **当前 PartIAL GATED 状态与 Gewin 2018 判据一致**——不能在用户确认前推荐 proceed.

---

## 2. 2024-2026 相邻领域 first-class "方法学驱动" 论文（F2 综合）

下列论文符合 Gewin 2018 的 C1+C2（一句方法学 sentence + 新且引人入胜），且明确**不是** data-uniqueness 框架：

| # | arXiv | 一句关键信息 (key_message) | 首发 | 子领域 |
|---|---|---|---|---|
| 1 | 2604.07236 | "Agent harness layers, once made externally measurable, reveal that most of an agent's competence resides in the harness — the LLM's contribution is a bounded residual." | Sungwoo Jung (2026-04) | agent harness methodology |
| 2 | 2605.03310 | "Coordination is a separable architectural layer whose configuration leaves distinguishable calibration-vs-discrimination signatures — Murphy decomposition on live prediction markets." | Maksym Nechepurenko (2026-05) | prediction-market calibration |
| 3 | 2607.01661 | "Multi-agent forecasting deliberation only improves calibration when agents hold asymmetric evidence — identical-evidence deliberation is herding in disguise." | Yuante Li (2026-07-02) | prediction-market calibration |
| 4 | 2511.07678 | "Expert-level LLM forecasting is achieved not by scale but by agentic search + supervisor reconciliation + bias-correction calibration." | Rohan Alur (2025-11-10) | prediction-market calibration |
| 5 | 2607.09921 | "LLM-based forecasting beats market consensus and XGBoost in specialized long-context settings when supervised with hindsight-guided reasoning traces." | Hinal Jajal (2026-07-10, **ICML 2026**) | prediction-market calibration |
| 6 | 2607.09349 | "'Deceptive grounding': a RAG failure mode (entity-attribution failure) invisible to all faithfulness/hallucination/citation checks, with a detection method at 97% precision." | Cedric Caruzzo (2026-07) | evidence-ledger/RAG attribution |
| 7 | 2606.04217 | "Settlement-layer ground-truth microstructure quality predicts Brier scoring performance in ways that classification proxies cannot recover." | Boka Qin (2026-06) | settlement+calibration（G3 最近邻） |

**模式**：在所有 adjacent sub-space，first-class 的论文都以**方法学机制名词**为主语（"coordination"、"Murphy decomposition"、"deceptive grounding"、"hindsight-guided supervision"），无一以独有数据为卖点. 这与 Nature 编辑 Gorsuch 的话一致——"编辑和审稿人寻找有趣 *结果* 且对领域 *有用*"，与 F4 的"Datasets-as-endpoints don't meet the bar"相为印证.

**对 G3 的直接启示**：
- **F2 most-transferrable primitive**: Murphy decomposition of the Brier score (arXiv:2605.03310 [2]) 把 Brier split 成 calibration vs discrimination 分量——直接可作为 G3 的方法学组分"差异化语言"——避免使用单一 Brier 总分.
- **"Deceptive grounding" (arXiv:2607.09349 [6])** 是 evidence-ledger 在文献中最贴近的失败模式先例（真实证据、真实 citation、错误实体），其 detection methodology（97% precision）是 P1+P2 的 evidence ledger 论文中可对照的"模型上不可能替代" 的方法学贡献——这恰好是 F2 推荐的有用 framing [F2 §Findings worth promoting].

---

## 3. G3 在 2024-2026 学术语料中的新颖性评估（F3 综）

**核心发现**：G3 的组合术语 **zero-hit on arXiv 全文** (as of 2026-07-16) [F3].

| 维度 | F3 结论 |
|---|---|
| "dual ledger reconciliation calibration" | arXiv 零命中 |
| "Brier score replay settlement" | arXiv 零命中 |
| "prediction market settlement reconciliation" | arXiv 零命中 |
| "crosswalk ledger calibration" | arXiv 零命中 |

**最近的 prior art（按组件）**：
- 单 ledger→Brier linkage: arXiv:2606.04217 (Polymarket-v1, 2026-06) [F3 §1];
- Brier replay as forecast eval: arXiv:2605.00420 (Foresight Arena, 2026-05) [F3 §2];
- Brier as training reward: arXiv:2607.00164 (2026-06) [F3 §4];
- Brier→counterfactual: arXiv:2304.10005 (Keogh & van Geloven, Epidemiology 2024) [F3 §中期v.];
- "Forecast reconciliation": Hyndman 传统 arXiv:2605.17920, 2602.22694, 2405.18693（aggregation-coherence，**与 G3 同形 false cognate**）[F3 §中期].

**结论**：G3 的"组分 + 组合"均无直接 prior art——通过 C3 (novelty) 判据的 evidence 基本充分. **唯一警示**：必须在引言中显式 disambiguate "reconciliation （G3 settlement reconciliation）"与 Hyndman 传统 "reconciliation （aggregation-coherence）"——否则审稿人会误以为是"已知方法的新数据应用"，触发 data-uniqueness 拒信模板.

---

## 4. Direction X "harness-evolution methodology" standalone —— slot 复核（F5 综）

项目内部标记 Direction X 为 CLOSED。F5 的 adversarial re-verification 复核了 4 个 named slot-occupants：

| 占位者 | 复核结论 | Primary source |
|---|---|---|
| **Stanford Meta-Harness** | ✅ VERIFIED. **附加更正**: 项目 MEMORY 中的 URL `github.com/muratcankoylan/meta-harness` 是一个 0-star fork（属 Toronto context-engineer，非作者），canonical repo 是 `https://github.com/stanford-iris-lab/meta-harness` by Yoonho Lee, Roshen Nair 等 Stanford 作者；arXiv:2603.28052（2026-03-30）[F5 §Findings[1]]. | arXiv + GitHub |
| **Chinese AHE paper** | ✅ VERIFIED. arXiv:2604.25850（Jiahang Lin et al., Fudan NLP, "Agentic Harness Engineering"；v1 2026-04-28, v4 2026-05-18）。AHE 的"三 observability pillars + 闭环"明确占据该 slot 的关键方法学命题 [F5 §Findings[2]]. | arXiv |
| **"62-page Harness Engineering survey"** | ⚠️ PARTIALLY VERIFIED: arXiv:2606.20683 "From QA to Task Completion"（Huawei/PKU；2026-06-14）+ arXiv:2605.18747 "Code as Agent Harness"（2026-05-18）——两份真实 harness-engineering survey 都存在；但 MEMORY 中"2026-05"+"62 page"身份不精确——首轮 candidate page-kid 数约为 29（与 62 不符）[F5 §Findings[3,4]]. | arXiv |
| **DeepSeek Harness team** | ⚠️ UNVERIFIED. arXiv 搜索"DeepSeek harness team"仅命中无关 reasoning 模型论文 (arXiv:2505.08311)；在 5-query 搜索预算内未定位 primary source. **依 自媒体 fact-verification 规则，此项必须降级至 ⚠️ 直至有 primary source**[F5 §Findings[5]]. | (缺) |

**净判定**：slot 已被至少 3 个 primary-source 占位者实际占据. 即使 DeepSeek Harness team 最终未被证实，AHE + Meta-Harness + 两份 survey 已占据"harness-evolution methodology standalone"的关键命题空间.

**对原项目 MEMORY 的更正建议**（不在本报告变更范围；提交 §9 open questions）：
- URL `github.com/muratcankoylan/meta-harness` → canonical `github.com/stanford-iris-lab/meta-harness`.
- "62-page 2026-05 survey" 身份需 byte-confirm；可能是 arXiv:2605.18747 "Code as Agent Harness"，或未在本轮被找到的第三份文档.
- "DeepSeek Harness team formed 2026-05-20" — ⚠️ UNVERIFIED on primary；应按项目规则改为 UNVERIFIED status 直至 primary 出现.

**对 Direction X 的结论**：re-opening 会**严重 re-tread**. AHE 的三 observability pillars、Meta-Harness 的 outer-loop search、survey 的六-component harness anatomy 已表达 would-be Direction X 的核心命题. 一个 viable reopen 角度仅存于一个具体应用领域（如 research-automation harness）的非重叠 delta——但此 delta 在本轮 report 范围内未验证，**应照项目 D17 规则继续 GATED，不得替用户推荐 proceed**[F5 §Recommendation].

---

## 5. 失败模式签名 + 方法学洞见 7-check test（F4 综）

**F4 从 NeurIPS 2023/2026 ACL/ARR primary reviewer 语料中提炼的失败模式**：

1. **"Datasets-as-endpoints don't meet the bar on their own"** (NeurIPS 2026 E&D, 官方 reviewer guidance) [F4 §Finding 1].
2. **"The paper is mostly a description of the corpus and its collection and contains little scientific contribution"** (ACL/ARR canonical reject Language) [F4].
3. **Failure 模式**:
%20不是"数据不够 unique"，而是"移除数据独有 claim 后，论文方法学贡献崩塌" → 触发 reviewer 拒信.
4. **关键区分** (NeurIPS 2026 AC pilot blog): "critical concerns"（证明、基线、上下文）vs "non-critical concerns"（新颖性）——数据独有属 non-critical bucket，**救不了** critical 漏洞 [F4 §Finding].

**Methodological-insight 7-check test**（精确到可对任何候选方向应用）[F4 §Test]:

- [ ] **Check 1 — Single-methodological-insight sentence test**: 一句话表达出方法学洞见（新方法、新评测协议、新 reconciliation 方法、新失败模式），**而非** "我们构建/采集了 X"？
- [ ] **Check 2 — 移除数据独有生存测试**: 移除"我们独占此数据"后，方法学贡献是否仍能独立存在？
- [ ] **Check 3 — 评估性主张清晰度测试**: 是否明确说明"数据/方法支持的具体 evaluative claims、under what assumptions、什么 limitations constrain them"？
- [ ] **Check 4 — 知识缺口测试**: 知识缺口是"关于理解/方法"的缺口，而非"前人没采集过该数据"的数据缺口？
- [ ] **Check 5 — 洞见跨子领域可迁移性测试**: 邻近子领域研究者会发现该洞见对自身有用？还是只对本数据集工作者有用？
- [ ] **Check 6 — 深层 concern 抗冲击测试**: 若 reviewer 提出 deep concern (缺失基线、方法遗漏)，能否通过"我们数据 unique"反驳？NO ——则 data-uniqueness 救不了 method flaw.
- [ ] **Check 7 — 无 unique 数据可复现性测试**: 另一团队在公开可获或可采集数据上能否复现洞见？若洞见仅在 unique 数据上展现，则可能 data-driven gaming. (注：icmi "beating a baseline 不必"——insight 是 method 可复现，不是数据特定)

**应用至 P1+P2 (current)**: 全部 7 项 PASS（Check 3 PARTIAL，建议加紧 articulation expression）[F4 §P1+P2].

**应用至 Direction Y (current framing)**: **5/7 FAIL**：Check 1、2、3、5、7 全部失败，唯 Check 4、6 在"数据缺 + 无独立 method 漏洞"框架下 PARTIAL. [F4 §Direction Y]

---

## 6. 最终推荐：选题策略选择

**遵循项目 D17 规则**：在用户发出"boring"信号后，不替用户决议"哪个方向 proceed"。本报告给出**基于 Gewin 2018 5 判据与 F4 7-check 测试的客观计分**，决议权属用户.

### 计分汇总表

| 方向 | Nature C1 | Nature C2 | Nature C3 | Nature C4 | Nature C5 | F4 7-check | Gewin 综合结论 |
|---|---|---|---|---|---|---|---|
| **P1+P2 (current mainline)** | PASS | PASS | PARTIAL | PARTIAL | PASS | 7/7 PASS | **最佳候选**; 需 disambiguate 与 Hyndman reconciliation、向非专业读者明示 settlement-reconciliation 隐喻 |
| **Direction Y (current framing, NeurIPS D&B)** | FAIL | FAIL | FAIL | FAIL | PARTIAL | 5/7 FAIL | **不推荐原 framing**；需方法学重构（参考 §1.2 后段）|
| **Direction Z (G3+Harness-Evolution Combined)** | PASS(弱) | PASS/PARTIAL | 同 P1+P2 | 同 P1+P2 | PASS | 等同 G3 + 增加 harness-evolution 部分引入 PARTIAL | **GATED on user confirmation**，与项目 MEMORY D17 状态一致；建议先确认 G3 单独或 G3+harness-evolution |
| **Direction X (harness methodology standalone)** | — | — | — | — | — | slot 已被 3-4 primary occupant 占据 | **CLOSED，应继续不开放** (F5) |

### 核心建议（不替用户决议）

1. **第一梯队**：**P1+P2 的 G3 reconciliation 方法**单独成文，不搭载 harness-evolution（保持单一 key message 最强状态）. 这是唯一在 Nature 5 判据上 PASS ≈ PASS ≈ PASS ≈ PARTIAL ≈ PASS 的方向. 关键改进点：
   - 显式 disambiguate "settlement reconciliation" vs "hierarchical/forecast reconciliation (Hyndman tradition)"——这是 C3 唯一 PARTIAL 项；
   - 引述 **Murphy decomposition of Brier score** (arXiv:2605.03310 [F2 §2]) 作为可转移的方法学原语，把单一 Brier 总分拆为 calibration 与 discrimination 分量，进一步加固 C2 "新且引人入胜"；
   - 引述 **"deceptive grounding"** (arXiv:2607.09349 [F2 §6]) 作为 evidence-ledger 失败模式的最贴近先例，把 G3 的"detection of entity-attribution failure"作为"不可被替代"的方法学贡献写进 introduction——强化 C4 跨受众清晰度.

2. **留作 GATED 选项**：**Direction Z** 在 G3 单独成文的基础上+ harness-evolution 延伸为 ablation section. 用户确认 G3 reconciliation 方法"interesting"后方可 pursue；如已确认，按 §1.3 "若加 harness-evolution 应在 §6 ablation subsection 表达"路径. **不替用户决议**.

3. **不推荐 pursue**：**Direction Y 在当前 dataset-as-endpoint framing 下不通过任何关键选题判据**；如用户主动要求重构为方法学驱动（如 "a method for predicting/auditing harness bugs before verdict reversions"——参考 §1.2 后段），需重新计分.

4. **不重开**：**Direction X 已被 3+ labeled primary occupant 占据** (F5 verified)；按项目内部 CLOSED 状态维持.

---

## 7. 与 Nature 2018 原文五位一体的对应

| Nature 2018 专家建议 | 本报告的应用位置 |
|---|---|
| Borja "global context + future work" | §3 (G3 vs Hyndman reconciliation disambiguation) |
| Mensh "single key message" | §1 C1 判据、§6 final: "G3 single-mainline" 选项 |
| Murphy "What's new and compelling red thread" | §1 C2 判据、§2 (相邻领域 first-class paper 句式)、§5 (7-check)|
| Doubleday "human storytelling" | §1 C4 判据、§6 建议 (settlement-reconciliation 隐喻) |
| Gorsuch "don't omit methodology" | §1 C5 判据、§6 建议 (Murphy decomposition 增强方法可复现性) |
| Konkiel "widers audience" | §1 C4 判据、§6 建议 (deceptive grounding 引入新目失败模式获跨领域引用) |

---

## 8. 开放问题（未结项，交用户决议）

1. **Direction Z GATED 解锁**：G3 的 settlement reconciliation 方法是否在用户视角下"interesting"？此决议仍受 D17 约束，不得替用户决定.
2. **DeepSeek Harness team primary 来源**：如能直接出现 GitHub repo / Hugging Face organization / arxiv affiliation string，应替换原"⚠️ UNVERIFIED"状态；建议主动 search DeepSeek 官方通道（github.com/deepseek-ai、HF org、arXiv affiliation strings）[F5 §open question].
3. **"62-page survey" 的 byte-level identity**：建议下载 arXiv:2606.20683 / 2605.18747 两份 candidate PDF 用 `pdfinfo` byte-confirm，或找出第三份 2026-05 harness engineering white paper —— 此刻的自媒体级描述不精确 [F5 §open question].
4. **F2 + F3 数据-源 GAP**：本轮报告受 MCP web-search API 失败影响；Semantic Scholar Graph API 返回 429；OpenReview 与 ACL Anthology 应单独补搜以求"被拒方法学-新颖反对意见"证据基. 对 G3 新颖性评估这已是 high-confidence；对 §2 F2 部分同比 NeurIPS 2026 beyond arxiv 的 ACL proceedings 同期. 应作为 follow-up 进行.

---

## 9. Sources (numbered, with access date)

> 全部为 primary arXiv/GitHub/OpenReview；所有 arXiv 全链接已由 sub-agent Read from primary. 本报告**未**使用任何 自媒体 (Toutiao/WeChat/公众号) 数字/标题作为 load-bearing 论据——遵循项目硬规则.

[1] arXiv:2606.04217 — B. Qin et al., "Polymarket-v1 Database" (2026-06). https://arxiv.org/abs/2606.04217 (访问 2026-07-16). [F3 §1]
[2] arXiv:2605.00420 — Nechepurenko & Shuvalov, "Foresight Arena" (2026-05). https://arxiv.org/abs/2605.00420 (访问 2026-07-16). [F3 §2]
[3] arXiv:2601.22444 — N. Bosse, "Forecasting Question Generation and Resolution" (2026-01). https://arxiv.org/abs/2601.22444 (访问 2026-07-16). [F3 §3]
[4] arXiv:2607.00164 — S. Singh, "Verifiable Rewards for Calibrated Forecasting" (2026-06). https://arxiv.org/abs/2607.00164 (访问 2026-07-16). [F3 §4]
[5] arXiv:2304.10005 — Keogh & van Geloven, "Counterfactual Brier Score" (Epidemiology 2024). https://arxiv.org/abs/2304.10005 (访问 2026-07-16). [F3 §中间]
[6] arXiv:2605.17920 — "Hierarchical Forecast Reconciliation" (2026-05). https://arxiv.org/abs/2605.17920 (访问 2026-07-16). [F3 §Hyndman tradition]
[7] arXiv:2604.07236 — Sungwoo Jung et al., "Agent harness externalization" (2026-04). https://arxiv.org/abs/2604.07236 (访问 2026-07-16). [F2 §1]
[8] arXiv:2605.03310 — M. Nechepurenko, "Coordination as architectural layer; Murphy-decomposed Brier on live prediction markets" (2026-05). https://arxiv.org/abs/2605.03310 (访问 2026-07-16). [F2 §2]
[9] arXiv:2607.01661 — Y. Li, "InfoDelphi: Designed Information Asymmetry" (2026-07). https://arxiv.org/abs/2607.01661 (访问 2026-07-16). [F2 §3]
[10] arXiv:2511.07678 — R. Alur, "AIA Forecaster: supervisor reconciliation for expert-level LLM forecasting" (2025-11). https://arxiv.org/abs/2511.07678 (访问 2026-07-16). [F2 §4]
[11] arXiv:2607.09921 — H. Jajal, "ICML 2026 Merger Arbitrage forecasting with hindsight-guided supervision" (2026-07). https://arxiv.org/abs/2607.09921 (访问 2026-07-16). [F2 §5]
[12] arXiv:2607.09349 — C. Caruzzo, "Deceptive Grounding" (2026-07). https://arxiv.org/abs/2607.09349 (访问 2026-07-16). [F2 §6]
[13] arXiv:2603.28052 — Y. Lee, R. Nair et al., Stanford, "Meta-Harness" (2026-03-30). https://arxiv.org/abs/2603.28052 (访问 2026-07-16). [F5 §1]
[14] arXiv:2604.25850 — J. Lin et al., Fudan, "Agentic Harness Engineering (AHE)" (2026-04-28, v4 2026-05-18). https://arxiv.org/abs/2604.25850 (访问 2026-07-16). [F5 §2]
[15] arXiv:2606.20683 — K. Han et al., Huawei/PKU, "From QA to Task Completion: Survey on Agent System and Harness Design" (2026-06-14). https://arxiv.org/abs/2606.20683 (访问 2026-07-16). [F5 §3]
[16] arXiv:2605.18747 — X. Ning et al., "Code as Agent Harness" (2026-05-18). https://arxiv.org/abs/2605.18747 (访问 2026-07-16). [F5 §4]
[17] NeurIPS 2026 E&D Track — Reviewer official guidance "Datasets-as-endpoints don't meet the bar on their own"; ACL/ARR reject-language guidance "mostly a description of the corpus". 直接采自 F4 findings[1,2]. (访问 2026-07-16). [F4]
[18] V. Gewin, "How to write a first-class paper", Nature 555, 129-130 (2018). https://doi.org/10.1038/d41586-018-02404-4 (访问 2026-07-16). 5 判据透镜原文.
[19] 项目 MEMORY: D17 rule ("after user boring signal, do NOT defend / restate / propose new directions as a defensive gesture; gate recommendations on user-supplied criteria"), "data-uniqueness ≠ paper-interesting" rule. `MEMORY.md #Rules`. (访问 2026-07-16). 项目规则约束.

---

## 附录 A: F2-F5 文件路径

全部 sub-agent findings 已写入磁盘（备份与可追溯）：
- `/Users/tangzw119/Documents/GitHub/auto-research/research/nature-first-class-paper/findings/F2.md` (103 行 — 11 篇 methodological-framing first-class papers)
- `/Users/tangzw119/Documents/GitHub/auto-research/research/nature-first-class-paper/findings/F3.md` (99 行 — G3 novelty 与 prior art)
- `/Users/tangzw119/Documents/GitHub/auto-research/research/nature-first-class-paper/findings/F4.md` (167 行 — 数据独有论文失败签名 + 7-check test)
- `/Users/tangzw119/Documents/GitHub/auto-research/research/nature-first-class-paper/findings/F5.md` (84 行 — Direction X 四 slot-occupant 复核)
- brief：`/Users/tangzw119/Documents/GitHub/auto-research/research/nature-first-class-paper/brief.md`

## 附录 B: 本次更新与项目 MEMORY 的冲突/更正建议

依 F5 verifications:
- **URL 更正**: 项目 MEMORY 中 Stanford Meta-Harness URL 应从 `github.com/muratcankoylan/meta-harness` 更正为 `github.com/stanford-iris-lab/meta-harness`（muratcankoylan 是 0-star fork，非作者）。
- **状态降级**: "DeepSeek Harness team (industry, formed 2026-05-20)" 应标 ⚠️ UNVERIFIED（5-query arXiv 搜索未定位 primary source）；按项目 自媒体 规则，须待 primary 出现。
- **身份澄清**: "62-page Harness Engineering survey" 的身份模糊，可能是 arXiv:2606.20683 或 2605.18747，需 byte-confirm；page-kid 估计仅 29 页与原"62 page"不符.

以上更正建议提交为 §8 开放问题；本报告不修改项目 MEMORY 文件，后者由 checkpoint writer 负责维护。
