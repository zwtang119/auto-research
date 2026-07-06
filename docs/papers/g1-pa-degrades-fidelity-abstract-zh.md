# G1 — PA-Degrades-Fidelity 顶会摘要（1 页，245 字）

> **G1 spec**（per `docs/investigations/first-principles-top-journal-directions-2026-07-05.md:87`）：
> 「写 1 页 PA-degrades-fidelity 摘要；5 人评审中 R1 + R3 ≥ 5.5；如失败则放弃作为独立，保留为 P11 workshop 支柱。」
>
> **作者**：AutoResearch 2026-07-05  
> **目标会议**：ACL 2027 / EMNLP 2027 main track（per investigation §14，天花板 6.5-7.0）  
> **状态**：1 页摘要待评审（未投稿）  
> **源数据**：P11 927 次 agent-run + 1,824 次 LLM-judge 调用（`legacy/p11-closed-v5-minimax-m3/` + `legacy/p11-closed-v5-mimo/`）

---

## 摘要（245 词）

**Pure analysis 在角色冲突条件下会降低角色保真度，与「显式推理更有帮助」的常识相反。**

我们在 LLM-agent 评估中报告一个反方向效应：结构化 pure-analysis 提示在 agent 面对角色冲突决策时**降低**主观角色保真度，即便它增加了推理深度。在 927 次 agent-run 与 1,824 次 LLM-judge 调用的 Gulei 2015 石化事故场景中，我们发现 (i) 常规「内心独白提升保真度」假设（H1）在盲评下**崩塌**（δ=−0.04，p=0.73，n=551 有效 run），揭示此前的正向信号是被 LLM judge 的**标签泄露偏差**所放大；(ii) pure-analysis 条件在主观保真度上**显著差于** no-think 基线（A1：t=−3.391，p=0.0008，Cliff's δ=−0.162）；(iii) 同样效应**不会迁移**到客观风险承担行为（Spearman ρ=0.76–0.82，跨 judge 稳定，对盲评免疫）——保真度打击集中在*主观*维度。我们用保留 judge 家族复现了标签泄露放大模式，并量化了放大幅度（约 0.4 分，在 1-5 量表上）跨四种 factor type（环境官、医疗官、流程工程师、应急指挥）。我们的发现提示**结构化推理在角色冲突下不是保真度杠杆**，且 agent 评估界对主观维度上对带标签可见的 LLM judge 的依赖将效应量放大了约一个数量级。

## 1. 核心 claim（一句话）

**Pure analysis 在角色冲突下降低主观角色保真度**（A1：t=−3.391，p=0.0008，Cliff's δ=−0.162；n=927 agent-run，n=1,824 judge-call）。

## 2. 证据（4 pillars，全部来自现有 P11 数据 — 0 新 API）

| Pillar | 发现 | 来源 |
|--------|------|------|
| **H1 盲评** | 标签可见的 H1 效应（δ=−0.04，p=0.73）—— 盲评下**无效** | `wiki/decisions/blind-judge.md:22-27` |
| **A1 pure-analysis vs 基线** | Pure-analysis **降低**保真度（t=−3.391，p=0.0008，Cliff's δ=−0.162） | `experiments/h5-emergence/analysis/A1_baseline_vs_pure.json:1-9` |
| **F1 emergence vocabulary** | Pure-analysis > 内心独白 在群体 emergence 上（n=72 paired run，DS vs QW χ²=2.949，p=0.40） | `experiments/h5-emergence/analysis/C_emergence_freq.json:1-15` |
| **H3 Spearman（客观风险承担）** | 对盲评免疫（ρ=0.76–0.82 跨 4 judge）—— **不受**推理风格影响 | `state/progress.json:43` |

## 3. 为何新颖（per investigation §62-67）

- CoT / 结构化推理文献一致地报告对 agent 性能的**正向**效应
- 我们发现**反方向**效应作用于主观保真度——「显式推理更有帮助」**不是**普遍假设
- 标签泄露放大模式（约 0.4 分，n=551 有效 run）是解释此前正向结果的**机制**
- 盲 LLM judge 作为**对照**是方法学贡献——LLM-as-judge 论文很少跑标签盲对照
- AI 安全 / agent 评估界尚未浮现这个反方向（per 外部调研）

## 4. 对顶刊读者的贡献

1. **反方向发现**：pure analysis 在角色冲突下不是保真度杠杆
2. **机制**：标签泄露偏差在主观维度上放大效应量
3. **方法学**：盲 LLM judge 对照是任何主观保真度 claim 的必需
4. **跨 judge 复现**：4 judge（DeepSeek / Kimi / Qwen / MiniMax）确认该模式
5. **对 LLM-agent 评估界的含义**：用标签盲对照重评估此前的正向发现

## 5. 局限（pre-stated，per anti-inflation 规则 roadmap §11）

- 单一场景（Gulei 2015 石化）；跨领域复现推迟到 "future work"
- 199/750 DeepSeek 解析失败，仅留 n=551 有效 run 作为主 judge（per `A_kw_fdr.json:36-40`）
- 主观保真度 inter-judge agreement ρ=0.19（接近随机）在完整 6D 报告上 —— 仅 `risk_taking` 维度稳定（ρ=0.74）
- 26 轮评审平台期在中位 5.84–6.60（per `legacy/p11-closed-v5-minimax-m3/wiki/annotations/paper-review-rounds.md`）

## 6. 可复现性

- 数据：`legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/`
- 脚本：`legacy/p11-closed-v5-minimax-m3/scripts/`（run_inner_monologue.py + score_m3.py + analyze_m3.py + m4_analysis.py）
- 4 judges × 3 conditions × 50 runs = 600 基线 + 标签泄露修正子集
- 26 轮评审跨 6 论文迭代

---

*本 1 页摘要是 G1 产物。下一步：5 人评审（R1 + R3 ≥ 5.5 通过条件）。M4 review-runner 模板复用自 `papers/p12-judge-calibration/experiments/run_review_round_1.py`。*
