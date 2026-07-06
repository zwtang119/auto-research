# 第一性原理扫描：潜在的顶刊方向

> 日期：2026-07-05

## 摘要

本项目目前**按现状还不是 main-track / 顶刊就绪**，但 first-principles 扫描发现了几条之前运营评估低估的非显然方向。最强的候选不是「agent 表现更好」的论文，而是**反向、测量、schema-reconciliation 与可审计性**的论文。

最佳答案：仓库里没有藏着一个立即可投 NeurIPS / ICLR / ACL-main 的 paper，但有 **3 条可信的高层方向**值得考虑：**(1) PA-degrades-fidelity / 角色冲突机制**，**(2) LLM judge 的 calibration paradox**，**(3) 与 cds4worldcup settlement 证据的 dual-ledger schema 调和**。这些方向在 cross-domain 复现或外部验证之前，可达到 Findings / strong workshop 水平；要上升到 main-track 仍需补充条件。

## 排名候选方向

| 排名 | 方向 | 核心 claim | 当前天花板 | Main-track 解锁条件 | 成本 / 风险 |
|---:|---|---|---|---|---|
| 1 | **PA-degrades-fidelity / 角色冲突机制** | 结构化 pure-analysis 提示会在角色冲突下降低角色保真度，与「显式推理更有帮助」的常识相反。 | 6.5-7.0 workshop / Findings 边缘 | 跨领域复现，理想用 cds4worldcup 或另一个非应急决策领域 | 0 新 API 用于写稿；2-3 周。风险：P11 26 轮平台期造成的 review 信任债。 |
| 2 | **Calibration paradox** | 标签泄露让 LLM judge 变得**更严**而不是更宽松：blind > leaked，与通常的 leakage-bias 故事相反。 | 6.5-7.0 若复现 | N=30 paired，第二 judge 家族，第二场景 | 5-8 API 小时；高新颖度但当前 n=10 偏小。 |
| 3 | **Dual-ledger / settlement schema bridge** | auto-research evidence ledger 与 cds4worldcup factor ledger 各自独立演化；调和它们产生一个跨领域 settlement-aware evidence contract。 | 6.5-7.0 Findings / D&B 风格 | cds4worldcup MD2 规模语料，≥80% schema 字段覆盖率，外部基线 | 3-8 API 小时 + 2-3 周。最低成本潜在解锁。 |
| 4 | **Negative heterogeneity 作为第一类发现** | Evidence-ledger 效应按 factor type 条件化：authority / falsifier 有帮助，branch / precedent 没有。 | 6.5-7.0 workshop；7.0-7.5 作为方法学 | N=64/cell 或跨领域 factor-type 复现 | 若直接跑则 ~30 API 小时；若与 schema bridge 一起做则更便宜。 |
| 5 | **Reviewer-noise ceiling / LLM-review psychometrics** | 跨多次 review，reviewer noise 可以超过论文改进信号。 | 6.5-7.0 ACL / EMNLP evaluation track | 人类 reviewer 对比和预注册 review 协议 | 5-10 API 小时 + 人类 reviewer 投入。 |
| 6 | **Audit-chain integrity / hash-fabrication failure** | LLM-agent 证据系统可能伪造 audit hash；证据有效性必须被计算，而非声明。 | 6.0-7.0 security / AI safety workshop | 除 P7 PIT-NEW-9 外再加 2-3 个案例 | 低 API；会议适配窄。 |
| 7 | **Cross-layer integration failure** | 四个绿的组件测试套件可以组合成一个坏的评估系统而没有端到端 contract 测试。 | 6.0-6.5 SE / AI engineering 会议 | 可复现的集成失败和跨层测试套件 | 3-5 API 小时；偏 SE 而非 AI main-track。 |

## 非显然重构

### 1. 停止问「agent 是否提升了」

最强的潜在 claim 是**诊断性的**，不是性能提升的 claim：

- P12 发现了反向 judge 效应。
- P11/Mimo 发现 pure analysis 会降低保真度。
- P1+P2 发现 factor-type 异质性而非均匀提升。
- P7 发现了 audit-chain 完整性缺陷。
- 重复 review 揭示了测量噪声和平台期行为。

这暗示了一个围绕**LLM-agent 评估中证据、判断和干预的局限**的 paper 家族，而非「更好的 agent 系统」。

### 2. cds4worldcup 是最便宜的顶刊天花板解锁

之前的运营计划低估了 cds4worldcup。它有独立的 factor-ledger schema、settlement-record schema、24 场已结算的赛事结果、闭环 Brier 证据。桥接到 auto-research 可以：

- 解除 P8「没有预测概率」的问题；
- 给 P1+P2 一个第二领域；
- 测试 factor-type 异质性是否在应急场景之外也成立；
- 不需要大量新模型调用就能产出一个 schema-reconciliation 论文。

### 3. joint-methods 的失败本身就是证据

joint 论文失败是因为各组件单独看着合理但没有整合。这可以重构为一个软件 / 评估方法学发现：

> 组件级 contract 是不够的；LLM-agent 评估需要跨越 evidence、judge、settlement、audit 层的端到端 contract 测试。

这不太可能 NeurIPS main-track，但可以是一篇不错的 SE / AI-engineering workshop 论文。

### 4. 「顶刊」可能需要切换会议类别

如果「顶刊」严格指 NeurIPS / ICLR / ACL main-track，则没有方向就绪。如果包括 ACL / EMNLP Findings、NeurIPS Datasets & Benchmarks、security / SE workshops 或 AI-for-science methodology 会议，则多个方向变得可信。

## 外部新颖性检查

外部调研发现：

- LLM-as-judge bias 文献已拥挤，但 **blind > leaked** 在所查文献中未被浮现。
- CoT / 结构化推理文献通常报告**正向**效应；**PA-degrades-fidelity** 是反方向的。
- 异质处理效应在统计学上已成熟，但在 LLM 评估证据账本上未被充分利用。
- AI 研究自动化文献已拥挤，但**带人参与的 AutoResearch 控制的路径选择振荡**更窄、覆盖更少。
- LLM-agent audit / provenance 文献发表偏少；P7 的 PIT-NEW-9 风格 hash-fabrication 缺陷位于一条开放车道上。

外部锚点：

- MT-Bench / Chatbot Arena：<https://arxiv.org/abs/2306.05685>
- LLM-as-judge position bias：<https://arxiv.org/abs/2406.07791>
- LLM-as-judge scoring bias：<https://arxiv.org/abs/2506.22316>
- KIEval：<https://arxiv.org/abs/2402.15043>
- OctoTools：<https://arxiv.org/abs/2502.11271>
- RELAY：<https://arxiv.org/abs/2502.08482>
- AI Scientist：<https://arxiv.org/abs/2408.06292>
- AI Scientist v2 repository：<https://github.com/david-hoa2023/ai-scientist-v2>
- AI4Research：<https://ai-4-research.github.io/>
- Heterogeneous treatment effects：<https://link.springer.com/article/10.1007/s10742-016-0156-2>

注：外部调研报告此环境中部分 arXiv 页面只能通过搜索片段或次要摘要触达。在引用于论文前需直接复核所有主 PDF。

## 推荐实验 / Gates

| Gate | 行动 | 通过条件 | 若失败 |
|---|---|---|---|
| G1 | 写 1 页 PA-degrades-fidelity 摘要 | R1 + R3 ≥ 5.5 在 5 人评审中 | 放弃作为独立；保留为 P11 workshop 支柱 |
| G2 | 复现 calibration paradox 到 N=30 paired + 第二 judge | leaked-blind delta 的 CI 仍 < 0 | 仅视为 P12 异常 |
| G3 | 建立 auto-research 与 cds4worldcup 间的 dual-ledger crosswalk | 字段覆盖率 ≥ 80% 且无 fatal enum mismatch | 仅发表 schema note |
| G4 | 在 cds4worldcup settlement records 上跑 P8 Brier | 复现报告的 Brier 值和 baseline difference | 提交前修复 schema / 计算 |
| G5 | 对 reviewer-noise 论文做人类或外部评审 | 人类 vs LLM 对比确认 measurement gap | 仅保留为内部 AutoResearch methodology |

## 最终判断

存在**其他可信的高层方向**，但没有一个是不花工作就能拿到的隐藏顶刊路径。最好的 first-principles 洞察是，本项目组合的真实新颖性可能在于**LLM-agent 证据系统如何失败**：

1. judges 做出反向反应；
2. 结构化推理会损害角色保真度；
3. ledger 效应按 factor type 异质；
4. audit chain 除非密码学检验否则可能被伪造；
5. reviewer noise 可以主导论文迭代。

最高预期价值序列是：

1. **PA-degrades-fidelity 摘要**（0 API，快速真伪检验）；
2. **dual-ledger bridge 与 cds4worldcup**（低成本结构性解锁）；
3. **calibration paradox 复现**（小 API，高新颖度）；
4. 仅在之后才考虑有算力的 P1+P2 或 main-track 尝试。

缺乏这些 gate，诚实的近期目标仍是 workshop / Findings，不是 main-track。
