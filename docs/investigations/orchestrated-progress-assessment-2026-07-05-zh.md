# 编排化评估：当前 AutoResearch 进展

> 日期：2026-07-05

## 推荐结论

当前状态**不是顶刊/main-track 就绪**。本项目组合有可发表的素材，但诚实的近期目标是 workshop / Findings，不是 NeurIPS / ICLR / ACL / EMNLP 主会。**最强的立即路径是 14 天 P11 workshop 论文**（用现有证据），并以 **P7 scaffolding/audit-chain 论文**作为可选保险。joint P12 + P1+P2 + P8 + P7 methods 论文不应按现状提交：其实际 6 人评审 outline 中位分 4.0，低于 fallback 阈值。

## Agent 发现

### Agent 1：P11 / P12

- **P11 独立天花板**：6.0-6.5，workshop-only。
- **P12 独立路径**：无，6 人评审中位 3.0，刻意走 `fold_into_p1_p2`。
- **Mimo + v5 整合**：仅在 14 天计划能延长至 Day 21 时才可行。保守预期增益 +0.3 到 +0.5 中位分，不足以让顶刊 claim 成立。
- **算力**：0 新 API 小时。复用现有 P11 927 次运行 + 1,824 次 judge 调用。
- **决策**：推进 14 天 P11 workshop 论文。Day-11 gate：中位分 < 5.8 切换到 2 页 extended abstract；中位分 ≥ 6.3 才开启 Day 15-21 Mimo 整合的可选路径。

### Agent 2：P1+P2 / P8 / P7 / Joint Methods

- **P1+P2 独立路径**：已关闭；当前天花板 3.5-4.5。M5 主运行将消耗约 30 API 小时但不解决 scenario / external-validation 卡点。
- **P8 独立路径**：5.5-6.0 直到数据输出 `predicted_p`；现有 AB 数据是 1-5 judge 评分，不是概率。
- **P7 独立路径**：目前 5.5-6.0，如果把 PIT-NEW-9 audit-chain 修复作为主要贡献抬升，可能 6.0-6.5。
- **Joint methods 论文**：放弃作为发表路径。先前估计 6.5-7.0 的天花板不通过实际的 6 人评审中位 4.0。
- **决策**：把 joint methods outline 转为内部 framework 文档。如果写第二篇论文，用 P7 scaffolding/audit integrity 作为保险。

### Agent 3：Deli AutoResearch 控制回路

- **组合健康度**：假性健康。`stale_count=0` 掩盖了路径选择振荡：P12 fold -> P1+P2 fold -> joint methods fallback -> P11 fallback。
- **M5 主运行**：未授权。属于单方向深挖，有 PIT-003 / PIT-008 复发的风险。
- **cds-keyperson import refactor**：本 14 天窗口未授权；不在 P11 或 P7 scaffolding 的关键路径上。
- **运行计划**：锁定 fallback，重建 iteration 日志，跑 P11 workshop 路径 + 可选 P7 scaffolding，Day 11 评审，Day 13-14 提交或停止。

## 顶刊路径

**当前答案：没有**。现在没有可信的顶刊或 main-track 投稿。

Main-track 变得合理，仅当以下结构性解锁中至少 2 个关闭：

1. **场景多样性**：除了当前 Gulei / commercial-space 之外，至少 3 个独立的决策 / 应急场景。
2. **外部验证**：人类 inter-rater、gold set 或公开 benchmark tie-in，例如 ForecastBench、GAIA、AgentBench 或领域 oracle。
3. **前沿基线**：GPT-5 / Claude Opus / Gemini 级别 model arm，跑在有意义的比较 cell。

如果这 3 项都还关闭，更多 token 主要是改进包装，不能提高发表天花板。

## 算力请求

| 项目 | API 小时 | 决策 |
|---|---:|---|
| P11 workshop 论文 | 0 | 授权 |
| P7 scaffolding 论文 + 评审 | ~3 | 可选保险 |
| P1+P2 M5 主运行 | ~30 | 现在不授权 |
| P12 独立扩展 | 0 | 不重开 |
| P8 概率重跑 | 5-10 | 除非 P8 变成选定的 workshop 轨道否则推迟 |
| cds-keyperson import refactor | 0 | 推迟 |
| 前沿基线 | 0 | 推迟到 scenario + external validation 存在后 |

## 下一个 Gates

| Day | Gate | 决策规则 |
|---|---|---|
| 1-2 | 锁定 fallback 并冻结其他 loop | 在更多迭代前写 checkpoint / progress status |
| 3-5 | P11 4-pillar 重写 | Label leakage + H1c + F1 emergence + H3 Spearman 在 abstract / results 中可见 |
| 6-8 | 可选 P7 scaffolding 草稿 | 如果 audit-chain story 需要 live engine demo 则放弃 |
| 9-11 | 5 人评审 | P11 中位 < 5.8 -> extended abstract；P7 中位 < 5.5 -> 内部文档 |
| 12 | 编译 / 引文检查 | 没有伪造引文；没有未解决的 build 问题 |
| 13-14 | 会议选择 + 提交 | 仅 workshop / Findings；不投 main-track |

## Fallback

如果 P11 和 P7 都未达到 Day-11 阈值，停止组合 loop 而非生成另一条路径。写一个 framework 级 blocked state 引用路径选择振荡，然后仅在至少两个结构性解锁被外部承诺后才重启。

## 底线

当前最好的研究输出是受控的 workshop / Findings 投稿，不是顶刊论文。最有价值的行动是**14 天内从现有证据交付一篇诚实的论文**，然后再决定是否投入人类工作到 scenario diversity、external validation 和 frontier baselines。没有这些结构性输入，额外的 token 很可能重现 P11 风格的评审平台期。

## 推荐实验 / Gates

| Gate | 行动 | 通过条件 | 若失败 |
|---|---|---|---|
| G1 | 写 1 页 PA-degrades-fidelity 摘要 | R1 + R3 ≥ 5.5 在 5 人评审 | 作为独立放弃；保留为 P11 workshop 支柱 |
| G2 | 复现 calibration paradox 到 N=30 paired + 第二 judge | leaked-blind delta 的 CI 仍 < 0 | 仅视为 P12 异常 |
| G3 | 建 auto-research 与 cds4worldcup 间的 dual-ledger crosswalk | 字段覆盖率 ≥ 80% 且无 fatal enum mismatch | 仅发表 schema note |
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
3. **calibration paradox 复现**（小 API，高新颖）；
4. 仅在之后才考虑有算力的 P1+P2 或 main-track 尝试。

缺乏这些 gate，诚实的近期目标仍是 workshop / Findings，不是 main-track。
