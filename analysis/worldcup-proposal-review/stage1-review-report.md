# Stage 1 系统审查报告：开题报告 v1.3 方法论驱动重构

> 日期：2026-07-21
> 审查对象：`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` (v1.3, 2026-07-20, **原文件只读，未修改**)
> 审查者：Stage 1 子代理
> 透镜：
> - `research/nature-first-class-paper/REPORT.md` 5 选题判据（C1–C5 Mensh/Murphy/Borja+Gorsuch/Doubleday+Konkiel/Gorsuch）
> - `research/nature-first-class-paper/findings/F4.md` 7-check methodological-insight test
> - `research/nature-first-class-paper/findings/F2.md` 2024–2026 邻域方法学范例 11 篇
> - `research/nature-first-class-paper/findings/F3.md` G3 dual-ledger prior art + arXiv 零命中组合术语
> - `docs/investigations/worldcup-paper-topic-2026-07-19.md` (W6 终裁备忘录) §1.4 横向对比 + §2 占位风险表 + §5 G0–G7 + §8 禁用表述清单
> - `docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` F1–F4 缺口分析
> - `docs/investigations/meta-question-recalibration-first-class-paper-2026-07-17.md` 元问题校准（Q1 跨域 / Q2 数据鲁棒 / Q3 发现可被接住）
> 角色：本报告是 4 阶段流水线 Stage 1 交付物；Stage 2 (data-analysis) 与 Stage 3 (chart-visualization) 与 Stage 4 (consulting-analysis 重构) 并行/后续执行

---

## 0. 执行摘要

**一句话审查结论**：v1.3 在 5 维度均有显著进展（kimi 溯源基本闭环、R1–R4 瑕疵登记、n 分层声明、OSF 分析协议定位收窄），但**主线当前 framing 仍以「公开审计链 × 多方法同台 × 真 ex-ante」三元交叉为卖点，落入 F4 §1 (NeurIPS 2026 E&D) 与 F4 §11 (ACL/ARR) 警戒的 data-uniqueness-as-novelty 拒信模板风险**——F4 7-check 中 **Check 1 single-methodological-insight sentence FAIL、Check 5 transferability PARTIAL**。同时 §2 文献综述在 F3 已落地的 2026 prior art（Polymarket-v1、Foresight Arena、Counterfactual Brier (Keogh & van Geloven Epidemiology 2024)、Yates covariance decomposition、Hyndman multivariate reconciliation、InfoDelphi）**零引用**，须扩。evidence-snapshot-gap-analysis-2026-07-20 新发现的 cds_qualification 缺布尔字段与 ops JSON 不存在（CRITICAL）+ 漂移扩大（F1.2/F2.4）v1.3 §5.2 未登记。

**v2 须做四件事**：① §0/§9 摘要与创新点改写为方法学机制名词句式（Check 1 通过）；② §2 文献综述以 F2 11 篇 + F3 10 篇 prior art 重新锚定，与 G3/Hyndman reconciliation / Polymarket-v1 / Foresight Arena / InfoDelphi / Counterfactual Brier 显式 disambiguate（C3 PASS / F4 Check 2/4/5 闭环）；③ §3 H1–H4 按 F4 7-check 逐项显式锚定并新增 H5 协议完整性向量（呼应 W6 §1.4 三描述性发现 + §6 G6）；④ §5.2/§7 新增 cds_qualification 漂移 + ops JSON 不可恢复 + Plan C ledger 状态不一致（CRITICAL gap）+ source-policy 滞后四项诚实边界。

---

## 1. 维度（a）研究问题定义

### 1.1 v1.3 现状

v1.3 §1.2 总问题：**「在完全相同的事前信息与公开可审计的冻结纪律下，五类预测方法在逐场与队伍两个层级上的概率结构（校准度、区分度、质量分布）存在怎样的系统性差异？哪类结构差异对应结算优势？」** 该问题有 3 个明确障碍的正面处理（层级样本量不对称 / 市场基准规格错配 / 作者已见结果），§0.3 三层 n 声明与 §5.5 OSF 分析协议冻结定位。

### 1.2 不足（按 F4 7-check 与 W6 口径）

**不足 1：研究问题当前 framing 仍以"我们这五类预测"为锚，不是以方法学机制名词为主语**——F4 Check 1 single-methodological-insight sentence FAIL。
- 反例（v1.3 §1.2）：「五类预测方法在逐场与队伍两个层级上的概率结构存在怎样的系统性差异」——主语是"五类方法"，不是"审计链锚定的多预测者 reconciliation 协议"。
- 应改：方法学机制名词句式，如「**audit-chain-anchored multi-forecaster reconciliation** 协议如何把 ex-ante 冻结 + 来源分级 + 统一结算 + OSF 协议冻结五件套升格为可复现评估协议？」——主语是协议，不是「我们」。

**不足 2：Knowledge gap 当前是数据缺口而非方法学缺口**——F4 Check 4 PARTIAL。
- v1.3 §2.6 定位陈述：「单一成分都有祖先（回测比较、市场基准、LLM 预测基准），三者同时成立处，在我们核查范围内为空白」——这是「数据缺口」表述，三元交叉的"同时成立处空白"是 data-uniqueness 句式。
- 真正的方法学缺口应是：「在**协议完整性向量**指导下，多预测者的事前冻结同台比较如何从一次性 benchmark 升级为协议级审计方法」——knowledge gap 是方法论级的，非数据级的。

**不足 3：与 W6 §1.4 三描述性发现的对齐不足**——v1.3 吸收了 W6 的 P2 定性修正（LLM 辅助混合预测器），但 W6 §1.4 的三描述性发现（rank-vs-mass 分裂 / 校准排序反转 / 信号与归一化耦合）**未被升级为研究问题**。
- rank-vs-mass 分裂（P3 把冠军排 top-3 但 93.5% 质量落在出局队）→ 应单独成节提问：路径枚举模型在 ranking 与 probability mass 上的语义分裂是不是结构性的？
- 校准排序反转（Coach 硬选 59.7% > Elo 54.9%，但 Brier/Log Loss 全部更差）→ 是研究问题主线，须凸显为"calibration 排序 vs accuracy 排序如何系统反转"。
- 信号与归一化耦合（同池重归一后 Kimi 把阿根廷抬到 19.59% 正确）→ 应作为 H4 sub-question："同覆盖下的概率重新归一化是否放大独立信息"。

**不足 4：作者已见结果的处理仍显薄弱**——v1.3 §1.2 写「本文不做预测预注册，改做分析协议冻结」+ §5.5 列已知/未知数字边界，但 OSF 冻结 = 分析协议（指标 + 纳排 + 已知/未知边界）的承诺强度需在 §0 导读 + §1.2 + §5.5 三处一致显式锚定。当前三处措辞略有差异，会被 reviewer 怀疑「分析协议冻结只是话语标签」。

### 1.3 v1.3 F4 7-check 适用表（仅维度 a）

| Check | 适用 verdict | 证据 |
|---|---|---|
| Check 1 single-methodological-insight sentence | **FAIL** | "五类预测方法的概率结构差异"是问题描述，不是方法学 insight |
| Check 2 移除数据独有生存 | PASS | 移除"我们这五类预测"，audit-chain-anchored reconciliation 协议仍独立 |
| Check 3 评估性主张清晰度 | PARTIAL | 评估性主张（RPS 主指标 + 配对 bootstrap CI + BH 校正）已声明；但"对应结算优势"的统计识别（false-positive 控制、效应量门槛）未明示 |
| Check 4 知识缺口 | PARTIAL | "三元交叉"是数据缺口；须升级为方法学缺口 |
| Check 5 跨子领域可迁移性 | PARTIAL | audit-chain 协议可迁移至保险/法律/医学诊断 evidence→factor→settlement 管线，但 v1.3 §1.3 仅做一句话提示，未显式 |
| Check 6 deep-concern 抗冲击 | PASS | 即使 reviewer 抨击"2026 世界杯是单一赛事无外部效度"，audit-chain + multi-forecaster reconciliation 方法独立生存 |
| Check 7 无 unique 数据可复现性 | PASS | audit-chain 协议可在公开数据上重建（G3/Caruzzo 范式） |

### 1.4 直接对应修改建议（维度 a）

| 章节 | 当前 | 须改为 |
|---|---|---|
| §0.1 一句话 | "五份预测用同一把尺子批改，看不同方法错的方式有何系统性不同" | 主语改为机制名词：「我们提出 audit-chain-anchored multi-forecaster reconciliation 协议，把它应用到 2026 世界杯五类预测的同台比较」 |
| §1.2 总问题 | "五类方法在两个层级上概率结构系统性差异？" | "audit-chain-anchored multi-forecaster reconciliation 协议如何在不同信息源 + 不同校准结构 + 不同归一化口径间捕获预测者的结构差异签名？"——主语是协议，方法学机制名词 |
| §1.2 障碍 1 | 样本量分层声明（R1/R2/R4） | 增加协议完整性向量预声明（ex_ante_status / snapshot_status / source_integrity / schema_status / adjudication_status / baseline_coverage / preregistration_status 七字段） |
| §1.2 障碍 2 | 市场基准规格错配 | 吸收 W6 §1.4 "信号与归一化耦合"——同池重归一化作为协议字段，不是统计技巧 |
| §1.2 障碍 3 | 作者已见结果污染 | 显式锚定 OSF = 分析协议（含指标 / 纳排 / 主对照 / 多重比较规则 / 已知未知边界声明），与 W6 G2 一致 |
| §1.3 意义 | "LLM 群体是否只是市场共识复述"为唯一实证意义 | 升级：(i) 实证 = 五类预测者结构差异签名；(ii) 方法 = audit-chain 可复用评估协议；(iii) 跨子领域证据 = insurance/legal/medical evidence→factor→settlement 管线可套用 |

---

## 2. 维度（b）文献综述完整性

### 2.1 v1.3 §2 引用清单盘点

v1.3 §2.1–2.5 共 13 条引用，§10 参考文献列：

1. Maher 1982 (Statistica Neerlandica)
2. Dixon & Coles 1997 (JRSS A)
3. Groll et al. 2019 (JQAS)
4. Hubáček et al. 2019 (Machine Learning)
5. Gneiting & Raftery 2007 (JASA)
6. Constantinou & Fenton 2012 (JQAS)
7. Tetlock 2005
8. Mellers et al. 2014 (PNAS)
9. Wolfers & Zitzewitz 2004 (JEP)
10. Surowiecki 2004
11. Hong & Page 2004 (PNAS)
12. Halawi et al. 2024 (arXiv:2402.18563)
13. Prophet Arena 2025 (arXiv:2510.17638)

### 2.2 F3 prior art 零引用（关键 gap）

F3 §Findings[1]–[10] 共 10 篇 2024–2026 prior art，**v1.3 §2 全部零引用**：

| F3 finding | 论文 | 在 v2 §2 应放位置 |
|---|---|---|
| [1] Polymarket-v1 (arXiv:2606.04217, Boka Qin 2026-06) | Brier 链接 ground-truth microstructure 质量 | §2.4 预测市场——已有，但 v1.3 §2.4 未引 |
| [2] Foresight Arena (arXiv:2605.00420, Nechepurenko 2026-05) | 首个 permissionless on-chain AI 预测 benchmark（Brier + Alpha Score + Murphy 分解连接） | §2.3 概率预测评估 |
| [3] Automating Forecasting Question Generation (arXiv:2601.22444, Bosse 2026-01) | 自动问题生成 + Brier 评分 | §2.4 预测市场 / §2.5 LLM 预测 |
| [4] Verifiable Rewards for Calibrated Forecasting (arXiv:2607.00164, Singh 2026-06) | Brier as verifiable reward for RL 训练 | §2.3 概率预测评估 + §2.5 LLM 预测 |
| [5] Multivariate Hyndman reconciliation (arXiv:2605.17920, Pinheiro 2026-05) | **forecast reconciliation** aggregation-coherence 同形 false cognate | §2.3 必须显式 disambiguate |
| [6] Counterfactual Brier (Keogh & van Geloven 2024 Epidemiology) | counterfactual Brier via IPW | §2.3 必须引，作为 Brier-replay 的方法论先例 |
| [7] Yates covariance decomposition (arXiv:2603.05544, Hebling Vieira 2026-03) | Brier split 成 3 个非负项（variance mismatch / correlation deficit / calibration-in-the-large） | §2.3 概率预测评估——v2 §5.3 指标升级为 Brier + Murphy decomposition 的直接 hook |
| [8] arXiv 零命中（"dual ledger reconciliation calibration" / "Brier score replay settlement" 等 5 组合术语） | 提供 G3/G4 audit-chain 类方法的 novel 信号 | §2.6 定位陈述 |
| [9] Hyndman hierarchical reconciliation tradition (arXiv:2006.08570 + 2024–2026 follow-ons) | **forecast reconciliation 的另一含义** = aggregation-coherence，与 G3 settlement reconciliation false cognate | §2.3 必须显式 disambiguate（与 [5] 合并处理） |
| [10] DeepHGNN (arXiv:2405.18693) | GNN hierarchical 端到端 reconciliation | §2.1–2.3 供"反例"锚——非足球 / 非预测市场 / 非 evidence-ledger |

### 2.3 F2 邻域方法学范例零引用（F2 11 篇全部未引）

| F2 finding | 论文 | 在 v2 §2 应放位置 |
|---|---|---|
| [1] Harness externalization (arXiv:2604.07236, Jung 2026-04) | agent harness 视角 | §2.2 机器学习谱系末段（可选）或方法章 |
| [2] Murphy decomposition on prediction markets (arXiv:2605.03310, Nechepurenko 2026-05) | coordination 是 separable architectural layer；Murphy-decomposed Brier 在 live prediction markets 上 split calibration vs discrimination | **§2.3 核心引用 + §5.3 指标升级 hook**——v2 §5.3 应升主指标为 RPS + Brier 分解（calibration vs discrimination 分量） |
| [3] InfoDelphi (arXiv:2607.01661, Li 2026-07) | 多代理预测 deliberation 仅在 agents 持 asymmetric evidence 时改善校准，identical-evidence deliberation 即 herding | **§2.5 核心引用 + §3 H4 升级 hook**——v2 H4 应升 "kimi vs 市场是否可区分" → "kimi 群体是否构成 asymmetric evidence 候选，或是 market consensus herding" |
| [4] AIA Forecaster (arXiv:2511.07678, Alur 2025-11) | agentic search + supervisor reconciliation + statistical calibration 三件套；LLM+market 集成超越 market consensus 单独 | §2.5 LLM 预测 + §3 H4 |
| [5] Merger-arbitrage ICML 2026 (arXiv:2607.09921, Jajal 2026-07) | long-context LLM forecasting beats market-implied prob by 24% in Brier via hindsight-guided reasoning | §2.5 LLM 预测 + §2.4 预测市场 |
| [6] Deceptive grounding (arXiv:2607.09349, Caruzzo 2026-07) | RAG failure entity-attribution failure，97% precision detection | **§2.6 定位陈述 + 方法章素材**——v2 §2.6 应引为 evidence-ledger 类失败模式的最近先例（呼应 P3 CDS 路径枚举的 entity-attribution 失败 = 概率挂在出局队上） |
| [7] Action-belief gap (arXiv:2511.13240, Pal 2025-11) | static calibration 不足以预测 agentic consistency | §2.5 LLM 预测 + §3 H4 |
| [8] TREC 2025 RAG Track (arXiv:2603.09891, Upadhyay 2026-03) | attribution verification 升格 first-class eval 轴 | 可选 §2.5 / 方法章 |
| [9] MC-Search ICLR 2026 (arXiv:2603.00873, Ning 2026-02) | process-level RAG attribution (HAVE) | 可选方法章 |
| [10] HARP (arXiv:2605.27489, Rahman 2026-05) | trace-first methodology for multi-agent LLM 失效传播 | §2.5 + 方法章 |
| [11] POMDP-based model validation (arXiv:2606.17383, Dixon 2026-06) | autonomous decision-making 拆 belief → forecast → action → utility 各组件独立校验 | **§2.6 定位陈述 + 方法章核心**——v2 应直接套用 POMDP 框架做 P1+P2+P3+P4+P5 五类预测者组件分解 |

### 2.4 W6 §2 占位风险表的零吸收

v1.3 §2.6 仅一句"单一成分都有祖先... 三者同时成立处空白"——未吸收 W6 §2.2 占位风险表的 7 个直接竞品：

| 占位风险源 | 引用 | v1.3 状态 |
|---|---|---|
| Dubitzky Open International Soccer Database | DOI 10.1007/s10994-018-5726-0 | ❌ 未引 |
| Bunker-Yeung-Fujii 综述 | arXiv:2403.07669 | ❌ 未引 |
| Rezaei-Samadi 2026 世界杯 SDR-Elo | arXiv:2606.24171 | ❌ 未引（直接竞品，必须 disambiguate） |
| Karger ForecastBench ICLR 2025 | arXiv:2409.19839 | ❌ 未引（W6 §2.2 严禁"首个 LLM forecast benchmark" 表述） |
| Prophet Arena ICLR 2026 | arXiv:2510.17638 | ✅ 已引（v1.3 §10[13]） |
| Hartvég 2026 世界杯 LLM forecasting | Preprints.org 202607.0719 | ❌ 未引（**v2 必须显式 disambiguate 并吸收 G7 外部生存测试素材**） |
| WorldCupBench / worldcup-predictor-2026 / AI World Cup / ModelBall / LMU SoccerArena / AlDahoul SSRN | GitHub artifacts + SSRN 6900538 | ❌ 未引（W6 §2.2 严禁"首个 2026 世界杯 LLM benchmark""首个 live 冻结" 表述） |

### 2.5 13 篇 + F3 10 篇 + F2 11 篇 + W6 7 篇 = 共 ≥18 条必须新增文献

**新增清单**（须进 v2 §2 + §10）：
- F2[2] arXiv:2605.03310 Murphy decomposition
- F2[3] arXiv:2607.01661 InfoDelphi
- F2[4] arXiv:2511.07678 AIA Forecaster
- F2[5] arXiv:2607.09921 ICML 2026 Merger-arbitrage
- F2[6] arXiv:2607.09349 Deceptive grounding
- F2[11] arXiv:2606.17383 POMDP-based validation
- F3[1] arXiv:2606.04217 Polymarket-v1
- F3[2] arXiv:2605.00420 Foresight Arena
- F3[5]/[9] arXiv:2605.17920 + arXiv:2006.08570 Hyndman reconciliation（disambiguate 对象）
- F3[6] arXiv:2304.10005 Counterfactual Brier Epidemiology 2024
- F3[7] arXiv:2603.05544 Yates covariance decomposition
- W6 §2 Dubitzky + Bunker + Rezaei-Samadi + Karger + Hartvég 6 篇
- W6 §2 AlDahoul SSRN 6900538 + WorldCupBench/worldcup-predictor-2026/AI World Cup/ModelBall 4 个 GitHub artifacts（作为 venue-occupying 占位风险记录）

### 2.6 直接对应修改建议（维度 b）

| 章节 | 当前 | 须新增/修改 |
|---|---|---|
| §2.3 | 仅 Gneiting-Raftery 2007 + Constantinou-Fenton 2012 | + F3[1] Polymarket-v1 / F3[2] Foresight Arena / F3[6] Counterfactual Brier / F3[7] Yates decomposition / F2[2] Murphy decomposition（5 篇新引） |
| §2.3 | 无显式 disambiguation | 新增 §2.3.1 "forecast reconciliation 同形 false cognate 处置"——显式 disambiguate "Hyndman hierarchical reconciliation" (aggregation-coherence, F3[9]) 与本文 audit-chain-anchored multi-forecaster reconciliation（settlement/data-source integrity 含义） |
| §2.4 | 仅 Wolfers-Zitzewitz 2004 + Hong-Page 2004 + Surowiecki 2004 | + F2[2] Coordination architectural layer / F3[1] Polymarket-v1 database / F3[2] Foresight Arena / F2[4] AIA Forecaster（4 篇新引） |
| §2.5 | 仅 Halawi 2024 + Prophet Arena 2025 | + F2[3] InfoDelphi / F2[4] AIA Forecaster / F2[5] Merger-arbitrage ICML 2026 / F2[7] Action-belief gap / F2[6] Deceptive grounding（5 篇新引） |
| §2.5 | 仅一句"多分身 × 多派别聚合的 LLM 群体信号与市场同台 ex-ante 对照，在核查范围内尚无先例" | **升级为该句**：把 F2[3] InfoDelphi 的"designed information asymmetry"作为 H4 问题升格的 anchor（v2 H4 不再仅问"是否可区分"，而问"何种 asymmetric evidence 缺位导致 herding"） |
| §2.6 | "三元交叉空白" + "novelty 声明目前仅为有限核查" | 替换为：明确列出 W6 §2 占位风险表的 7 个直接竞品（包括 Hartvég 预印本 + 4 个 GitHub artifacts）+ F3 arXiv 零命中组合术语证据（"dual ledger reconciliation calibration" / "audit chain multi forecaster Brier" 等 5 组合术语的零命中报告） |
| §10 | 13 条参考文献 | 至少 +13 条（新增 F2/F3/W6 共 18 条；保留 v1.3 §10 的 5 条经典：Maher/Dixon-Coles/Gneiting-Raftery/Hubáček/Groll） |

---

## 3. 维度（c）研究方法设计

### 3.1 v1.3 §3 H1–H4 假设评估表

| 假设 | 覆盖维度 | 当前形态 | F4 7-check 适用 | W6 §5/G1–G7 适用 |
|---|---|---|---|---|
| H1 | 逐场统计模型有技能（Elo+Poisson 与 Coach 都显著优于均匀+永远主场）| 配对 bootstrap + BH 校正 | Check 3 PARTIAL（评估性主张已声明但效应量门槛缺） | W6 G3 统计识别——paired bootstrap/permutation + 95% CI + reliability/ECE 已对应 |
| H2 | Elo 平局系统性低估 vs Coach 平局接近/高估 | 各层 bootstrap 95% CI | Check 3 PARTIAL | W6 G3 部分覆盖 |
| H3 | CDS 路径枚举引擎过度分散（描述性）| 质量分布汇报无检验 | Check 4 PARTIAL（描述性，但去断言无方法论贡献） | W6 W5/KILL——单赛事单正例不可单独成文 |
| H4 | Kimi 群体信号 vs 市场共识是否可区分 | Spearman 等级相关，ρ ≥ 0.9 / <0.7 / inconclusive | Check 4 PARTIAL | W6 W6/G1——kimi 提升为一等公民（已 v1.3 升级） |

### 3.2 不足（按 F4 7-check 与 W6 口径）

**不足 1：H1–H4 缺 Check 1 single-methodological-insight 显式锚定**——任一 H 都只是结果性预测，不是方法学机制命题。
- 反例：H1 = "P1 与 P2 都显著优于均匀"——这是数据结果预测，不是方法学命题。
- 应升：H1 = "**audit-chain-anchored reconciliation** 协议通过配对 bootstrap CI 即可识别 Elo+Poisson 校准结构对 Coach LLM-assisted hybrid 的稳定性优势"——主语是协议。
- v2 应**前置一段**明示 H1–H4 + 新增 H-protocol/H5 都是 audit-chain-anchored multi-forecaster reconciliation 协议在不同诊断维度的组件级假设。

**不足 2：H1 当前预声明的 RPS + BH 校正 4 个比较**——W6 G3 要求 paired bootstrap / permutation p-value / reliability / ECE / sharpness 全部分解到位；v1.3 §3 H1 仅提"配对 bootstrap + BH 校正"，宽度不足。
- 应升：H1 在 RPS 主指标外，要求按 H/D/A 类别分箱的 reliability（ECE/ACE）、sharpness 分解、最大概率分箱 observed frequency；并在 v2 §5.3 指标表新增"辅助 → 仅探索"两列的具体定义。
- 触发 F4 Check 3：评估性主张清晰度从 PARTIAL 升 PASS。

**不足 3：H4 粒度不足**——v1.3 §3 H4 当前是"ρ ≥ 0.9 / < 0.7 / inconclusive"三档判定。但：
- F2[3] InfoDelphi (arXiv:2607.01661) 指出：identical-evidence deliberation 是 herding，asymmetric evidence 缺位是 herding 的根因——H4 不应仅问"是否独立"，应问"何种 asymmetric evidence 缺位导致 market herding"。
- F2[4] AIA Forecaster (arXiv:2511.07678) 进一步显示 LLM+market 集成可超越 market consensus alone——H4 应进一步升级 sub-question：kimi+市场合并估计是否超越市场单独（同池重归一化的方法学评估）。
- 触发 F4 Check 5：跨子领域可迁移性升至 PASS。

**不足 4：缺 H5 / H-protocol（协议完整性向量）**——W6 §6 推荐贡献结构 (4) 要求"Protocol Integrity Vector" 作为方法学核心新字段，与 prediction score 并列报告。v1.3 §3 / §4 / §7 无对应假设。
- 应升：v2 §3 新增 H5 协议完整性向量的诊断力——(ex_ante, immutable, source_clean, hash_valid, schema_valid, independently_adjudicated, baseline_coverage) 七字段对预测分数分层报告后，是否可以解释 P3 CDS 路径枚举 93.5% 质量压在出局队的现象（CDS 的 schema_valid 可能为 false，hash_valid 可能为 placeholder）；以及 W6 §1.2 "kimi + Elo bonus 同源" 是否可由 source_clean=false 显式表达。
- 触发 F4 Check 2（移除数据独有生存）升 PASS：protocol integrity vector 是 schema-based，独立于本项目独占数据。

**不足 5：§4 五模块中 A5 因子账本 4 场案例**——W6 §6 推荐"独立案例 4 节"或"升级 H5 假设"。v1.3 §4.A5 / §7 列为"次要案例分析"——v2 须显式二选一：保留 n=4 局限声明，或升级为 H5-protocol 子假设。

**不足 6：§5.3 指标表过窄**——主指标 = RPS；辅助 = Brier/Log Loss；仅探索 = 硬选 + 进球差 MAE。
- v2 应吸收 F2[2] Murphy decomposition（arXiv:2605.03310）+ F3[7] Yates 3-项分解（arXiv:2603.05544）——把 Brier 分解为 calibration vs discrimination vs calibration-in-the-large 3 个分量，作为辅助指标独立报告。
- v2 §5.3 升级建议：
  - **逐场主指标**：RPS（保留）
  - **逐场辅助（必报）**：Brier + Murphy/Yates 分解（3 分量）+ Log Loss
  - **逐场辅助（探索）**：reliability diagram（H/D/A 分箱） + ECE/ACE + sharpness
  - **逐场探索**：硬选准确率 + 进球差 MAE（**且需 paired bootstrap CI**）
  - **队伍层**：Brier（仅描述）+ 冠军 log score −log p(champion) + top-5 mass 分轮次淘汰表
  - **时间线**：端点对比（赛前 vs 决赛前）+ 日度演化（描述）

**不足 7：v1.3 §5.5 OSF 冻结物范围偏窄**——v1.3 写"指标定义 + 纳排标准 + 比较族 + 检验方法 + 分层声明 + 已知/未知数字边界声明"。但 W6 §5 G2 要求"每条预测同时标注是否事前、是否冻结、来源是否合规、prompt hash 是否真实、schema 是否通过、是否有独立裁决、基线是否同覆盖"——v2 §5.5 应扩展 OSF 冻结物清单至：
- 指标 + 纳排 + 比较族 + 检验 + 分层 + 已知/未知边界 + **Protocol Integrity Vector 七字段定义** + **同覆盖归一化规则** + **协议字段缺失的事务处理规则（frozen → fail-loud, not fail-silent）**。

**不足 8：§5.2 R1/R2/R4 三条已登记但 F1.2/F1.3/F1.5/F2.2/F2.4 五项新缺口未登记**——
- F1.3 `cds_qualification.json` 缺 qualified/eliminated 布尔字段（CRITICAL）
- F1.5 `results/ops/cds-settlement-2026-07-08.json` 在快照内不存在（CRITICAL，但 pair 已证伪——快照内 36545 字节确实存在；evidence-snapshot-gap-analysis 已 update）
- F1.2 `qual_prob_top2` 数值漂移（MEDIUM，Iran +0.023 11 天延迟重算）
- F2.2 factor-ledger 覆盖率 3.85%（与项目 MVP2 声明一致，但与论文 n=104 口径差距大）
- F2.4 3/4 ledger 状态不一致（B2-QAT-SUI / C1-BRA-MAR / F1-NED-JPN 三个 ledger `factors.yaml` 仍 pending/tracking，但 settlement_record.yaml 已存在）
- v2 §5.2 应显式升级为 R5 (F1.3/F1.5/F1.2/F2.2/F2.4) 四条，附 ≥5 evidence-snapshot-gap-analysis 行号引用。

### 3.3 v1.3 §3–§5 F4 7-check 适用汇总

| Check | v1.3 verdict | 触发升级动作 |
|---|---|---|
| Check 1 single-methodological-insight | **FAIL** | §3 前置一段明示 audit-chain-anchored reconciliation 协议；H1–H4 + H5-protocol 主语改为协议 |
| Check 2 移除数据独有生存 | PASS | 保留 |
| Check 3 评估性主张 | PARTIAL | §5.3 指标表升级为 RPS + Murphy/Yates 分解 + reliability/ECE/sharpness；§5.5 协议完整性向量 |
| Check 4 知识缺口 | PARTIAL | §2.6 替换；knowledge gap 升级为方法论缺口（"协议完整性向量 → 可复用评估协议 → 同覆盖归一化规则"三件套） |
| Check 5 跨子领域 | PARTIAL | §1.3 升级为显式跨域证据（insurance/legal/medical evidence→factor→settlement 管线可套用，POMDP-based validation [F2[11]] 锚） |
| Check 6 deep-concern | PASS | 保留 |
| Check 7 无 unique 数据可复现 | PASS | 保留 |

### 3.4 直接对应修改建议（维度 c）

| 章节 | 当前 | 须改为 |
|---|---|---|
| §3 前置 | 无 | 加一段明示 H1–H4 + H5-protocol 都是 audit-chain-anchored multi-forecaster reconciliation 协议在不同诊断维度的组件假设 |
| §3 H1 | "P1/P2 显著优于两朴素基线" | 主语改协议；指标层加 ECE/sharpness/brier decomposition 三维度 |
| §3 H2 | "P1 vs P2 平局偏差方向相反且稳定" | 三层（MD1/2/3）bootstrap CI + Dixon-Coles 文献把系统平局低估耦合到 Poisson 独立性 |
| §3 H3 | "P3 描述性过度分散" | 升级为"路径枚举模型的 rank-vs-mass 分裂是否可由 schema_valid=false 解释"——与 H5-protocol 联动 |
| §3 H4 | "P4 vs P5 截面 Spearman ρ 三档判定" | 升级为 sub-question × 3：(i) ρ 三档；(ii) F2[3] 框架下 asymmetric evidence 缺位诊断；(iii) 同池重归一后 LLM+market ensemble 是否超越 market 单独 |
| §3 新增 | — | H5 协议完整性向量的诊断力：(i) 七字段捕获 P3/P5/W6 §1.2 三描述性发现；(ii) 与 prediction score 并列报告；(iii) 在 WorldCupBench / Prophet Arena 公开 artifact 上 external validation |
| §4.A5 | "因子账本 4 场次要案例分析" | 二选一：(a) 升 §3 H5-protocol 子假设，或 (b) 保留 n=4 局限但补 schema violation + ledger 状态不一致显式声明 |
| §5.2 R1–R4 | 三条瑕疵处置 | 升级为 R1–R5：+ R5 = cds_qualification 漂移 + ops JSON + factor-ledger 覆盖率 + ledger 状态不一致（evidence-snapshot-gap-analysis F1.3/F1.5/F1.2/F2.2/F2.4 五项） |
| §5.3 指标表 | RPS 主 + Brier/Log Loss 辅 + 硬选 + 进球差 MAE 探索 | 主=RPS；辅=Brier 全分 + Murphy/Yates 分解 + Log Loss；辅（探索）=reliability/ECE/ACE/sharpness；探索=硬选+进球差 MAE（须配 bootstrap CI） |
| §5.5 OSF 冻结物 | 6 类 | 升级为 ≥10 类：+ 协议完整性向量七字段定义 + 同覆盖归一化规则 + fail-loud 缺失处置规则 |
| §6.2 缺口 | "系统文献检索 / 分析副本未建 / 模型版本不可考 / 管线代码未写" | + W6 §7 A0 决赛 n=48 结算 + A1 不可变 release + A2 statistics + A3 protocol schema + A4 direct competitor crosswalk + A5 external 盲审 + A6 go/no-go（6 项并入 §6.2） |

---

## 4. 维度（d）创新点阐述

### 4.1 v1.3 §9 五项创新点

1. "首个全公开审计链的世界杯多方法比较实证"
2. "五类方法校准偏差结构的系统刻画"
3. "LLM 群体信号 vs 市场共识的可检验对照（溯源已闭环）"
4. "可复用的预测比较协议"
5. "可发布资产：72(71) 场统一结算数据集 + 市场日度概率矩阵 + 管线代码"

### 4.2 不足（按 F4 7-check）

**不足 1：创新点 1 落入 data-uniqueness-as-novelty 拒信模板**——F4 Check 1 FAIL。
- 「首个全公开审计链的世界杯多方法比较实证」= 数据独有 + 时序独家 = F4 §1 NeurIPS 2026 E&D "Datasets-as-endpoints don't meet the bar on their own" + F4 §11 ACL/ARR "the paper is mostly a description of the corpus"。
- v2 应改为方法学机制句式：「**提出 audit-chain-anchored multi-forecaster reconciliation 协议**，把 git 冻结 + 来源分级 + 统一结算 + OSF 分析协议冻结 + Protocol Integrity Vector 七字段五件套升格为可复现评估协议」。
- 主语是协议名词（参照 F2 11 篇范例统一范式），不是"首个""首次"。

**不足 2：创新点 2 是描述性发现，不是方法学贡献**——F4 Check 5 PARTIAL。
- 「五类方法校准偏差结构的系统刻画」是结果性总结，不是可迁移方法学。
- 应改为：「**提出 deviation-direction signature 框架**，把 calibration bias（方向）与 deviation magnitude（量级）解耦，使得协议在不同领域（如保险/法律/医学预测）的 evidence→factor→settlement 管线可套用」（对照 F2[11] POMDP-based validation 范式）。

**不足 3：创新点 3 的"溯源已闭环"误置"溯源状态"于创新点**——F4 Check 1 PARTIAL。
- 当前："LLM 群体信号 vs 市场共识的可检验对照（溯源已闭环）"——括号内容是项目治理优点，不是方法学创新。
- v2 升级：「**提出 asymmetric-evidence-as-herding-diagnostic 框架**，在 F2[3] InfoDelphi 框架下诊断 kimi LLM 群体是否构成 market consensus 复述还是独立信息候选；并以 protocol integrity vector 的 source_clean 字段为关键诊断量」。
- 注意：H4 不再是"ρ 三档"判定，而是 kimi 群体是否构成 asymmetric evidence 候选的机制级诊断。

**不足 4：创新点 4 措辞太泛**——F4 Check 4 PARTIAL。
- 当前："可复用的预测比较协议" = 抽象表述，读者无法具象什么是"可复用"。
- v2 升级：「**封装五件套可复用 audit-chain 协议**：(i) pre-registered analysis-protocol OSF freeze；(ii) Protocol Integrity Vector 七字段 (ex_ante / immutable / source_clean / hash_valid / schema_valid / independently_adjudicated / baseline_coverage)；(iii) 同覆盖归一化规则；(iv) fail-loud 缺失处置；(v) 单命令可复现管线（G2 闸门）」。

**不足 5：创新点 5 把可发布资产列为创新是次等创新**——W6 §6 已警示。
- 当前："可发布资产：72(71) 场统一结算数据集..."——数据集是 cross-method deliverable，不是创新本身。
- v2 降为 §9 末段 cross-method deliverables（不应占据 §9.1–§9.5 主创新点位）。

**不足 6：缺核心创新——H5 协议完整性向量**
- W6 §6 推荐贡献结构 (4) 要求 Protocol Integrity Vector 作为方法学核心新字段；v1.3 §9 5 项无此项。
- v2 §9.1 应升级为新创新点：「**Protocol Integrity Vector 七字段作为可继承的协议级评估对象**：(i) 与 prediction score 并列报告；(ii) 可在 WorldCupBench / Prophet Arena / ForecastBench 公开 artifact 上外部验证；(iii) fail-loud 缺失处置规则使 benchmark 可信度变成 first-class 评估字段」。

### 4.3 v1.3 §9 F4 7-check 适用表

| Check | v1.3 verdict | 触发升级 |
|---|---|---|
| Check 1 single-methodological-insight | FAIL（§9.1 直接踩）；PASS（§9.4 隐含）| §9.1 改协议名词；§9.5 升 H5-protocol |
| Check 2 移除数据独有生存 | PARTIAL（§9.1 FAIL；§9.4 PASS）| §9.1 改 |
| Check 3 评估性主张 | PARTIAL | §9.1/§9.4 加 assumption/limitations 显式锚定 |
| Check 4 知识缺口 | PARTIAL | §9.1 知识缺口升级为方法学缺口表述 |
| Check 5 跨子领域可迁移性 | PARTIAL | §9.1 + §9.4 加 insurance/legal/medical 类比 |
| Check 6 deep-concern 抗冲击 | PASS（§9.4 独立生存）| 保留 |
| Check 7 无 unique 数据可复现 | PASS（§9.4）| 保留 |

### 4.4 直接对应修改建议（维度 d）

| 章节 | 当前 | 须改为 |
|---|---|---|
| §9.1 | "首个全公开审计链的世界杯多方法比较实证" | "提出 audit-chain-anchored multi-forecaster reconciliation 协议，把 git 冻结 + 来源分级 + 统一结算 + OSF 分析协议冻结 + Protocol Integrity Vector 五件套升格为可复现评估协议" |
| §9.2 | "五类方法校准偏差结构的系统刻画" | "提出 deviation-direction signature 框架，把 calibration bias 方向与 magnitude 解耦，跨子领域可套用" |
| §9.3 | "LLM 群体信号 vs 市场共识的可检验对照（溯源已闭环）" | "提出 asymmetric-evidence-as-herding-diagnostic 框架，把 F2[3] InfoDelphi 框架应用到 kimi 群体信号 vs 市场共识对照" |
| §9.4 | "可复用的预测比较协议" | "封装五件套可复用 audit-chain 协议：(i) OSF 预注册；(ii) 七字段 Protocol Integrity Vector；(iii) 同覆盖归一化；(iv) fail-loud 处置；(v) 单命令可复现" |
| §9 新增 | — | §9.5 "Protocol Integrity Vector 七字段作为可继承的协议级评估对象"——列为第 5 项核心创新点；可发布资产降为 §9.6 cross-method deliverables |

---

## 5. 维度（e）预期成果

### 5.1 v1.3 §9 现有预期成果映射

v1.3 §9 罗列 5 项"创新点"+ 1 项"可发布资产"；§8 三选一 venue 列为 IJF / J. Sports Analytics / PLOS ONE，按结果强度裁定。

### 5.2 不足（按 W6 §5 + F4 7-check）

**不足 1：venue 选择仅看结果强度，未看 F4 Check 1–7 校准与 W6 校准**。
- v1.3 §8 W6-1 写「初稿（IJF / J. Sports Analytics / PLOS ONE 三选一，按结果强度定）」。
- W6 §5 W6 现实 venue 明确：「ICML/NeurIPS evaluation / data-centric ML / forecasting workshop（以届时实际 CFP 为准）」；stretch venue = NeurIPS 2027 D&B。
- v2 §8 W6-1 应升级为四档候选：(i) NeurIPS 2027 D&B（stretch，若 G0–G7 全过 + external 盲审 κ≥0.6）；(ii) ICML/NeurIPS evaluation workshop（现实，若 G7 不过）；(iii) W6 现实 recommendation 与 v1.3 三选一交叉；(iv) 降级方案（若 G3 statistics 或 G7 external fail）。

**不足 2：预期成果未与 G7 外部生存测试挂钩**——W6 §5 G7 = 至少用 WorldCupBench / 另一 live benchmark 公开 artifact 复核 protocol-failure taxonomy。v1.3 §9 5 项无对应预期成果。
- v2 §9 应显式表达：(i) protocol integrity vector 在 WorldCupBench / Prophet Arena / ForecastBench 上的 external application artifact；(ii) 双人盲审 Cohen's κ≥0.6 报告；(iii) crosswalk 报告（与直接竞品的 12 个维度对比）。

**不足 3：缺预期量化指标（G3 statistics 全套）**——W6 §5 G3 要求 paired bootstrap / permutation / 95% CI / reliability / ECE / 按结果类别分解，全通过后才允许"过度自信"措辞；v1.3 §1.2 / §3 已隐含但 §9 预期成果未量化。
- v2 §9 应明示预期：(i) H1 RPS 配对 bootstrap 双侧 α=0.05 BH 校正 + 95% CI；(ii) H2 三层 (MD1/2/3) bootstrap 95% CI；(iii) H4 Spearman ρ + asymmetric-evidence diagnostic；(iv) H5 protocol integrity vector 七字段报告；(v) 全部指标须在 OSF 预注册冻结后才能产生。

**不足 4：缺预期诚实上限表述**——W6 §8.3 诚实上限要求"在现有 72 场规模下，最强可辩护贡献不是预测性能 SOTA，而是 benchmark integrity audit"。v1.3 §7 7.1/7.6 显式声明，但 §9 预期成果无对应诚实上限。
- v2 §9 应显式：(i) 可发布数据集限于 single-tournament case；(ii) 不外推至其他届次；(iii) 不外推至非足球赛事；(iv) Protocol Integrity Vector 跨赛事的可迁移性仅在外部测试中验证。

**不足 5：§9.4 "可复用的预测比较协议" 在 §10 评审规则 B 5 维 rubric 评分维度未对应**——评审规则 B 写 "novelty / 证据链效度 / 统计严谨性 / 数据可行性 / 诚实边界"，§9 预期成果未对应这 5 维。
- v2 §9 应在每项预期成果后挂 5 维 rubric 自评链接（自评而不是承诺，提高 auditability）。

### 5.3 v1.3 §9 F4 7-check 与 W6 §5 的对应

| 维度 | v1.3 §9 创新 | F4 7-check 适用 | W6 §5 G 对应 |
|---|---|---|---|
| §9.1 全公开审计链 | Check 1 FAIL | G0–G7 隐式对应 |
| §9.2 五类偏差结构 | Check 5 PARTIAL | G3 statistics 部分对应 |
| §9.3 LLM vs 市场 | Check 4 PARTIAL | G6 source isolation |
| §9.4 可复用协议 | PASS（弱） | G2 管线可复现 |
| §9.5 可发布资产 | FAIL（沦为 deliverable）| G1 不可变 release |
| **新增 §9.5 协议完整性向量（v2）** | **新核心创新** | **G4 协议完整性**（W6 §5 已显式要求） |

### 5.4 直接对应修改建议（维度 e）

| 章节 | 当前 | 须改为 |
|---|---|---|
| §8 W6-1 | "IJF / J. Sports Analytics / PLOS ONE 三选一" | 四档候选：(i) NeurIPS 2027 D&B（stretch）；(ii) ICML/NeurIPS evaluation workshop（现实，首选）；(iii) v1.3 三选一；(iv) 降级方案（若 G3/G7 fail） |
| §9 | 5 项创新点 | 6 项创新点（升 §9.5 = Protocol Integrity Vector 七字段作为可继承协议级评估对象）+ cross-method deliverables 作为 §9.6 |
| §9 | 无诚实上限表述 | 每项预期成果后挂"诚实上限声明"——限定 single-tournament case；不外推非足球；Protocol Integrity Vector 跨赛事可迁移性仅在外部测试中验证 |
| §9 | 无 G7 外部生存测试预期 | 加 "§9.X 外部盲审预期"：(i) WorldCupBench / Prophet Arena / ForecastBench external 标注；(ii) Cohen's κ≥0.6；(iii) crosswalk 报告 |
| §9 | 无量化预期 | 加预期量化指标：H1 (RPS paired bootstrap + 95% CI + BH)；H2 (三层 CI)；H4 (Spearman ρ + asymmetric-evidence diagnostic)；H5 (七字段报告) |
| 附录 B | 5 维 rubric 评分 | 5 维 rubric 自评链接进 §9 每项预期成果 |

---

## 6. 跨维度 gap 汇总：F4 7-check ↔ W6 §8 禁用表述 ↔ evidence-snapshot 新缺口

### 6.1 全部 gap 列表（按 F4 Check 维度归并）

| F4 Check 维度 | 具体 gap | v1.3 章节 | v2 须改 |
|---|---|---|---|
| **Check 1 single-methodological-insight** | 主线 framing 落入 data-uniqueness 模板 | §0.1 一句话 / §1.2 总问题 / §9.1 创新点 1 | 主语改 audit-chain-anchored reconciliation 协议 |
| Check 2 移除数据独有生存 | v1.3 已独立 | — | — |
| **Check 3 评估性主张** | 指标表过窄（Brier 单一总分）+ assessment assumption 缺 | §5.3 / §9 预期成果 | 升级 RPS + Murphy/Yates 分解 + reliability/ECE/sharpness |
| **Check 4 知识缺口** | "三元交叉"是数据缺口表述 | §2.6 / §9.1 / §9.3 | 升级为方法学缺口 |
| **Check 5 跨子领域可迁移** | 仅一句话提示 | §1.3 / §9.1 / §9.2 | 显式跨域证据 + deviation-direction signature 框架 |
| Check 6 deep-concern 抗冲击 | v1.3 已独立生存 | — | — |
| Check 7 无 unique 数据可复现 | v1.3 已独立 | — | — |
| **Check 4/5 联动** | H1–H4 缺 H5-protocol | §3 + §4.A5 + §9 | 新增 H5 protocol integrity vector |
| **Check 1 联动 §2 prior art** | F3 10 篇 + F2 11 篇 + W6 7 篇共 ≥18 条零引用 | §2.1–2.5 + §10 | 增 ≥13 条（去重后） |

### 6.2 W6 §8 禁用表述清单对齐

| W6 §8 禁用表述 | v1.3 状态 | v2 须确保 |
|---|---|---|
| "首个世界杯/足球 LLM benchmark" | §9.1 风险；§0.1 已避用 | §0.1/§1.1/§2.6/§9.1 四处统一避用 |
| "首个 live、冻结、事前可结算 benchmark" | §2.6 "三元交叉空白" 风险 | §2.6 替换为"协议方法学空白" + §9.1 改 |
| "首次发现 LLM 足球预测过度自信" | §1.1 / §3 H1 未使用 | W6 §5 G3 要求 reliability+ECE+sharpness 才允许"过度自信"措辞——v2 §3 H2 须先 supports |
| "Coach 是纯 LLM forecasting model" | §0.2 / §2.2 / 附录 C v1.3 已修正为 LLM-assisted hybrid | 保留 v1.3 修正 |
| "六个基线均完整覆盖" | §0.3 三层 n 声明 + §5.2 kimi 覆盖偏差 + §7 各处已声明 | 保留 |
| "淘汰赛全赛程被事前预测" | §5.2 R4 + §7.8 已写入（新增） | 保留 |
| "Plan C 全部 schema-compliant" | §5.2 未显式声明 | v2 §5.2 R5 升级：F2.4 ledger 状态不一致 + 3/4 ledger pending/tracking |
| "multi-judge adjudication 已完成" | v1.3 未声明；W6 §1.3 写 0 行 judge 表 | v2 §1.3 / §7 加诚实声明 |
| "冠军 n=46 partial Brier 证明模型整体校准良好/不良" | §7.2 已声明单层赛事局限性 | 保留 |
| "G3 92.9% 覆盖率已被独立核验" | v1.3 未引用 G3 数字 | 保留不引用 |
| "首个全公开审计链的世界杯多方法比较实证" | §9.1 风险 | §9.1 改 F4 §1 数据独有句式 |
| **新增 W6 §8.3 最大诚实上限**（v1.3 §9 未对应） | §9 缺诚实上限 | v2 §9 每项预期成果后挂诚实上限 |

### 6.3 evidence-snapshot-gap-analysis 新缺口对齐

| Evidence-snapshot F 项 | v1.3 §5.2 状态 | v2 须显式登记 |
|---|---|---|
| F1.3 cds_qualification.json 缺 qualified/eliminated 布尔字段（CRITICAL→HIGH updated）| 未登记 | §5.2 R5 |
| F1.5 results/ops/cds-settlement-2026-07-08.json 缺失（已 pair 证伪——快照内 36545 字节存在）| 未登记（pair 已证伪）| §7 加 brief 注释 |
| F1.2 qual_prob_top2 数值漂移（MEDIUM，Iran +0.023）| 未登记 | §5.2 R5 + V-88a 扩展双文件 |
| F2.2 factor-ledger 覆盖率 3.85% | 未登记（v1.3 §4.A5 提"n=4"但未与 104 场口径校准）| §4.A5 + §7 加覆盖率声明 |
| F2.4 3/4 ledger 状态不一致（B2/C1/F1 三个 ledger `factors.yaml` 仍 pending/tracking）| 未登记 | §5.2 R5 + §7 |
| F4.3 source-policy 自 2026-06-11 draft-for-execution 滞后 | §7.7 已注明版本，未提黄源扩展修订需 | §7.7 + §10 修订 |
| F3b.4 oracle "kimi ↔ cds4polymarket" 关联证伪 | v1.3 v1.2 已记 | 保留 |
| F3a.4 oracle "40 队过滤器" 证伪 | v1.3 v1.2 已记 | 保留 |

### 6.4 meta-question-recalibration 三准则（Q1 跨域 / Q2 数据鲁棒 / Q3 可被接住）适用

| 准则 | v1.3 适用 | v2 须强化 |
|---|---|---|
| **Q1 跨域** | §1.3 仅一句话提示（"保险/法律/医学诊断"）| 显式 F4[11] POMDP-based validation 范式锚 |
| **Q2 数据鲁棒** | §5.5 OSF 冻结 + 已知未知边界 + W6 G3 statistics 部分 | + G7 external survival test（W6 §5）+ Murphy/Yates 分解 |
| **Q3 可被接住** | §9.4 "可复用协议" 隐式 | 升为显式：五件套可复用 + Protocol Integrity Vector 跨 benchmark external |

---

## 7. v1.3 文献综述时效性评估（F3 prior art 零引用问题）

### 7.1 系统性评估

| 评估维度 | v1.3 状态 | 严重度 |
|---|---|---|
| F3 10 篇 prior art 引用数 | **0 / 10** | **CRITICAL** |
| F2 11 篇邻域方法学范例引用数 | **0 / 11** | **CRITICAL** |
| W6 §2 占位风险 7 篇直接竞品引用数 | **0 / 7**（除 Prophet Arena 已引）| **HIGH** |
| Hyndman reconciliation 同形词显式 disambiguation | **缺** | **CRITICAL**（F3 §Final verdict 明确要求） |
| Halawi 2024 + Prophet Arena 2025 + Dixon-Coles 1997 + Gneiting-Raftery 2007 经典引用 | 已引 | PASS |

### 7.2 F3 prior art 零引用的具体漏检项（≥10 条）

按 F3 findings 排序：

1. **F3[1] Polymarket-v1 Database (arXiv:2606.04217, Boka Qin 2026-06-02)**: Brier 链接 ground-truth microstructure——v2 §2.4 / §2.5 / §9.2 必须引；是 audit-chain 类似资产最接近的 2026 prior art。
2. **F3[2] Foresight Arena (arXiv:2605.00420, Nechepurenko & Shuvalov 2026-05-01)**: 首个 permissionless on-chain AI 预测 benchmark + Brier + Alpha Score + Murphy 分解连接——v2 §2.4 必须引；W6 §2 general LLM forecasting 必占位。
3. **F3[3] Automating Forecasting Question Generation (arXiv:2601.22444, Bosse 2026-01-30)**: 自动问题生成 + Brier 评分——v2 §2.4 / §2.5 候选引。
4. **F3[4] Verifiable Rewards for Calibrated Forecasting (arXiv:2607.00164, Singh 2026-06-30)**: Brier as verifiable reward for RL——v2 §2.3 / §2.5 必引，对照 W6 §5 G2 复现性。
5. **F3[5] Multivariate Hyndman reconciliation (arXiv:2605.17920, Pinheiro, Bulhões, Hyndman, Rodrigues 2026-05-18)**: forecast reconciliation aggregation-coherence——**v2 §2.3 必须显式 disambiguate**（F3 §Final verdict 要求）。
6. **F3[6] Counterfactual Brier (arXiv:2304.10005, Keogh & van Geloven Epidemiology 2024)**: counterfactual Brier via IPW——v2 §2.3 必引；是 Brier-replay 方法论最近先例。
7. **F3[7] Yates covariance decomposition (arXiv:2603.05544, Hebling Vieira 2026-03-04)**: Brier 3-项分解——v2 §2.3 必引 + §5.3 指标升级 hook。
8. **F3[8] arXiv 5 组合术语零命中**（"dual ledger reconciliation calibration" / "Brier score replay settlement" / 等）——v2 §2.6 必引，作为 audit-chain 类方法 novel 信号。
9. **F3[9] Hyndman hierarchical forecast reconciliation tradition**（arXiv:2006.08570 + 2024–2026 多 follow-ons）——v2 §2.3 显式 disambiguation（与 [5] 联动）。
10. **F3[10] DeepHGNN (arXiv:2405.18693, Sriramulu 2024-05-28)**: GNN hierarchical 端到端 reconciliation——v2 §2.1–2.3 供"反例"锚。

### 7.3 时效性追加问题

W6 §2 占位风险表的"2026 世界杯直接竞品"未被 v1.3 §2.6 引用：

| W6 §2 直接竞品 | v1.3 §2 引用状态 | v2 须引位置 |
|---|---|---|
| Dubitzky Open International Soccer Database (DOI 10.1007/s10994-018-5726-0) | ❌ 未引 | §2.1 "pre-registered soccer prediction benchmark 已存在 216,743 场先例" |
| Bunker-Yeung-Fujii soccer ML survey (arXiv:2403.07669) | ❌ 未引 | §2.1 |
| Rezaei-Samadi 2026 世界杯 SDR-Elo (arXiv:2606.24171, 2026-06 预印本) | ❌ 未引 | **§2.5 必引——direct 2026 competition** |
| Karger ForecastBench ICLR 2025 (arXiv:2409.19839) | ❌ 未引 | §2.4 / §2.5 必引 |
| Hartvég 2026 世界杯 LLM forecasting (Preprints.org 202607.0719) | ❌ 未引 | **§2.5 必引——与本文最直接冲突** |
| AlDahoul Predicting the Pitch (SSRN 6900538) | ❌ 未引 | §2.5 |
| WorldCupBench / worldcup-predictor-2026 / AI World Cup / ModelBall / LMU SoccerArena | ❌ 未引 | §2.5 / §2.6 作为 venue-occupying 记录 |

### 7.4 v1.3 §2.6 "有限核查" 自我标签的诚实性问题

v1.3 §2.6 末写"该 novelty 声明目前仅为有限核查，投稿前须完成系统文献检索（第 6.2 节缺口）"——这是诚实声明但也意味着 §2 现行版的"三元交叉空白"novelty 主张是高风险断言。v2 §2.6 应：

- 删除"三元交叉空白"全部-or-nothing 表述；
- 替换为"在最接近的 2026 prior art (F3 5 篇 + W6 7 篇) 之外，本研究的 (i) 多分身 LLM 群体与预测市场同池重归一化 ex-ante 对照、(ii) audit-chain 协议完整性向量的 prediction score 并列报告，**未经 primary-source 检索在 arXiv 上有完整同形表述**"——是可证伪 novelty 而非泛化 novelty。

---

## 8. 补充文献调研方向 / 数据收集方向

### 8.1 补充文献调研（共 4 个角度）

**调研方向 1：2026 世界杯直接竞品的 §2.5.1 节（约 8 篇）**——补全 W6 §2 占位风险表。
- 必引：Hartvég 2026 世界杯 LLM forecasting (Preprints.org 202607.0719)
- 必引：Rezaei-Samadi 2026 SDR-Elo (arXiv:2606.24171)
- 必引：Karger ForecastBench ICLR 2025 (arXiv:2409.19839)
- 必引：AlDahoul SSRN 6900538
- 必引 + review：WorldCupBench / worldcup-predictor-2026 / AI World Cup (3 GitHub artifacts，v2 §10 引用格式按 GitHub artifact 注明)
- 候选引：ModelBall working paper + LMU LLM SoccerArena notice

**调研方向 2：F3 prior art 的 §2.3 + §2.4 节（约 5 篇）**——补全 Brier / forecast reconciliation / counterfactual Brier 文献锚。
- 必引：F3[5] arXiv:2605.17920 Hyndman multivariate reconciliation（disambiguate 对象）
- 必引：F3[6] arXiv:2304.10005 Counterfactual Brier Epidemiology 2024
- 必引：F3[7] arXiv:2603.05544 Yates covariance decomposition
- 必引：F3[1] arXiv:2606.04217 Polymarket-v1
- 必引：F3[2] arXiv:2605.00420 Foresight Arena

**调研方向 3：F2 邻域方法学范例的 §2.5 + 方法章（约 6 篇）**——补全方法学句式锚。
- 必引：F2[2] arXiv:2605.03310 Coordination as architectural layer（Murphy 分解）
- 必引：F2[3] arXiv:2607.01661 InfoDelphi（asymmetric evidence）
- 必引：F2[4] arXiv:2511.07678 AIA Forecaster（supervisor reconciliation）
- 必引：F2[5] arXiv:2607.09921 ICML 2026 Merger-arbitrage（methodological lever）
- 必引：F2[6] arXiv:2607.09349 Deceptive grounding（evidence-ledger 失败模式最近先例）
- 必引：F2[11] arXiv:2606.17383 POMDP-based validation（autonomous decision 组件分解范式）

**调研方向 4：Hyndman reconciliation 同形 disambiguation 章节（建议新增 §2.3.1，约 4 篇）**。
- arXiv:2605.17920 (Pinheiro et al. 2026-05)
- arXiv:2602.22694 (2026 follow-on)
- arXiv:2311.12279 (2023 follow-on)
- arXiv:2006.08570 (Di Fonzo & Girolimetto 2020-06, hierarchical aggregation-coherence 原始 disambiguate 文献)
- 该 4 篇与 v2 §2.3 联动，作为 forecast reconciliation 同形词的完整 disambiguation 包。

### 8.2 数据收集方向（4 类 Stage 2 必跑）

**采集方向 1：WorldCupBench / worldcup-predictor-2026 / AI World Cup / Prophet Arena / ForecastBench 5 个公开 artifact 的 protocol-failure 标注 pilot**——为 W6 G7 外部生存测试做基础。
- v2 §9.1 预期成果直接挂此数据采集。

**采集方向 2：kimi LLM 群体信号在 F2[3] InfoDelphi 框架下的 asymmetric evidence diagnostic 数据**——为 v2 H4 sub-question (ii) 提供诊断数据。
- v2 §3 H4 / §5.4 比较族锁定。

**采集方向 3：Brier 分解 Murphy + Yates 在逐场 72 场 + 队伍 n=48 上的实证分量数据**——为 v2 §5.3 指标升级提供原始数据。
- v2 §5.3 指标表 + §9.2 预期量化指标。

**采集方向 4：Protocol Integrity Vector 七字段在 cds4worldcup 五个预测器上的标定数据**——为 v2 H5-protocol 提供 example application。
- v2 §3 H5 + §5.5 OSF 冻结物扩展 + §9.5 创新点 5。

### 8.3 Stage 2 子代理须负责的范围

按本任务 brief，Stage 2 由另一并发子代理执行；本 Stage 1 输出仅做"调研方向 + 采集方向"清单，下文 §10 给出 v2 章节修改建议，但 Stage 2 outputs（stage2-* files）不由本 Stage 1 子代理产生，本子代理不写 / 不修改 `analysis/worldcup-proposal-review/stage2-*.md`。

---

## 9. 可拓展的新研究视角（v2 候选）

### 9.1 视角 1：从 ranking-calibration reversal 到 multi-forecaster decision decomposition

W6 §1.4 已暗示三描述性发现（rank-vs-mass 分裂 / 校准排序反转 / 信号与归一化耦合）；v2 应把三者作为单一框架"POMDP-based multi-forecaster decision decomposition"（F2[11] arXiv:2606.17363 POMDP-based validation 范式）：
- belief 阶段：哪个预测者的 probability mass 是 calibrated
- forecast 阶段：哪个预测者的 ranking 是 discriminative
- action 阶段：哪个预测者的 hard-pick 准确率高（不一定 aligned with calibration）
- utility 阶段：三种口径下"谁更准"都依赖口径——这就是 ranking-calibration reversal 的方法学解释

该视角 4 步分解既可套用 W6 §1.4 三描述性发现，又符合 F2[11] POMDP-based validation 范式，跨子领域可迁移。

### 9.2 视角 2：asymmetric evidence diagnosis（基于 F2[3] InfoDelphi）

F2[3] InfoDelphi 指出 identical-evidence deliberation 即 herding。v2 §3 H4 可升级为 asymmetric-evidence diagnostic 框架：
- kimi LLM 群体是否构成 asymmetric evidence 候选
- 市场是否只是 market consensus 的复述
- kimi + 市场 同池重归一后是否超越 market 单独
- 在 protocol integrity vector 的 source_clean=false 上，kimi + Elo bonus 同源是否构成 evidence pollution

该视角跨子领域可迁移（任何 evidence-fusion 场景：multi-source intelligence / medical second opinion / expert panel 预测均可套用）。

### 9.3 视角 3：protocol integrity vector 作为 first-class evaluation object

W6 §6 推荐贡献结构 (4) 的核心新字段。v2 §3 H5 升为方法学核心新假设：
- ex_ante / immutable / source_clean / hash_valid / schema_valid / independently_adjudicated / baseline_coverage 七字段
- 与 prediction score 并列报告
- 在 WorldCupBench / Prophet Arena / ForecastBench 公开 artifact 上 external validation（Cohen's κ≥0.6）
- fail-loud 缺失处置规则使 benchmark 可信度从附录移到 first-class

跨子领域可迁移：医学影像诊断 quality label / 法律判决 evidence integrity / 保险索赔 audit chain 均可套用。

### 9.4 视角 4：deviation-direction signature 框架（F2[2] Murphy decomposition 升级）

F2[2] arXiv:2605.03310 把 coordination 视为可配置 architectural layer，Brier 用 Murphy 分解 split calibration vs discrimination。v2 §3 H2 / H3 / H4 可统一为 deviation-direction signature 框架：
- direction：哪个预测者的 probability mass 偏向哪个 outcome category
- magnitude：偏差大小
- structure：偏差是否在 MD1/MD2/MD3 三层稳定
- per-sample-pattern：偏差是否在样本级（p_act<0.20 爆冷）有结构化特征

该视角跨子领域可迁移（任何 calibration bias 分析：保险定价 / 信用评分 / 医学诊断阈值设定）。

### 9.5 视角 5：Brier + RPS + Murphy decomposition + reliability 4 件套评分体系（F2[2] + F3[7] + W6 G3 综合）

v2 §5.3 指标表须从 v1.3 的"RPS 主 + Brier/Log Loss 辅 + 硬选 + 进球差"升级为：
- 主指标：RPS（保留）
- 辅必报：Brier + Murphy 分解（calibration vs discrimination）+ Yates 3-项分解 + Log Loss
- 辅探索：reliability diagram（H/D/A 分箱）+ ECE/ACE + sharpness
- 探索：硬选 + 进球差 MAE（须 paired bootstrap CI）

### 9.6 视角 6：external-survival evaluation（W6 G7 + Cochrane κ 双人盲审）

W6 §5 G7 要求至少用 WorldCupBench / 另一 live benchmark 公开 artifact 复核 protocol-failure taxonomy。v2 §9 预期成果须挂：
- cross-comparison 报告：与 WorldCupBench / Prophet Arena / ForecastBench / Hartvég 4 个直接竞品在 12 个维度（future-only / freeze / prompt equality / model count / market baseline / proper score / calibration / reason trace / source policy / schema validation / protocol-failure annotation）的逐项对比
- 双人盲审 Cohen's κ≥0.6（若不可达则降为 workshop case report）

### 9.7 视角 7：audit chain 在其他赛事 / 其他领域的可迁移性（验证 F4 Check 5）

F4 Check 5 要求 insight 跨子领域可迁移。v2 §1.3 / §9 须显式：
- insurance claims evidence → factor → settlement pipeline
- legal verdict evidence → factor → judgment pipeline
- medical diagnosis evidence → factor → diagnostic conclusion pipeline

并以 F2[11] POMDP-based validation (arXiv:2606.17363) 为 anchor，明确"audit chain protocol 是 POMDP validation 的一个变体"的范式归属。

### 9.8 视角 8：fail-loud benchmarking 的方法学贡献（protocol integrity vector 视角 2）

把 benchmark 可信度作为 first-class 评估对象：
- prediction score + protocol score 双轨报告
- protocol score = (ex_ante × immutable × source_clean × hash_valid × schema_valid × independently_adjudicated × baseline_coverage) 七字段 weighted sum
- 若任一字段 fail-loud，则 protocol score 标 incomplete
- 评审者可直接用 protocol score 过滤 outlier benchmark

---

## 10. v2 修改建议（按章节）

> 本节是 Stage 1 子代理的最终输出之一；Stage 4 consulting-analysis 重构子代理将以本节 + Stage 1 审查 + Stage 2 文献 + Stage 3 图表 为输入，产出 `proposal-worldcup-algorithms-v2.md`。

### 10.1 章节级修改总表

| 章节 | 修改类型 | 主要内容 | 对应 F4 Check / W6 / G |
|---|---|---|---|
| 页眉 | 微改 | 登记 "v2 = F4 Check 1/3/4/5 升格版 + W6 §1.4 三发现 H5 化 + evidence-snapshot R5 升级 + §2 prior art 增 ≥13 条" | 全部 |
| §0.1 一句话 | **重写** | 主语改 audit-chain-anchored reconciliation 协议 | F4 Check 1 |
| §0.2 五位考生 | 微改 | 加 P2/P4 LLM 介入环节差异（已 v1.3 部分修正） + 加 protocol integrity vector 七字段标 | F4 Check 3 |
| §0.3 三层 n | 微改 | 加 protocol integrity vector 字段 | F4 Check 3 |
| §0.4 阅读路线 | 微改 | 加 "§3 H5 协议完整性向量" 提示 | F4 Check 4 |
| §1.1 背景 | 改 | "LLM 群体是否只是市场共识的复述" 升级为 "F2[3] InfoDelphi 框架下 asymmetric evidence 候选判定" | F4 Check 4 / 5 |
| §1.2 总问题 | **重写** | 主语改协议；障碍 1 升级 protocol integrity vector；障碍 2 扩 §1.4 信号与归一化耦合；障碍 3 锚 OSF | F4 Check 1 / 3 / 4 |
| §1.3 意义 | 改 | 三段：(i) 实证 = 五类结构差异签名；(ii) 方法 = audit-chain 可复用协议；(iii) 跨子领域 = insurance/legal/medical 套用 | F4 Check 5 |
| §2.1 足球预测统计 | 改 | + Dubitzky + Bunker + Rezaei-Samadi 3 篇 | W6 §2 |
| §2.2 机器学习 | 改 | 保留；+ LLM-assisted hybrid 鉴别性表述（已 v1.3） | — |
| §2.3 概率预测评估 | **大改** | + F3[1]/F3[2]/F3[6]/F3[7]/F2[2] 5 篇 + 新增 §2.3.1 Hyndman reconciliation 同形 disambiguation | F3 §Final verdict |
| §2.4 预测市场 | 改 | + F3[1] Polymarket-v1 / F3[2] Foresight Arena / F2[4] AIA Forecaster / Karger ForecastBench / Wolfers-Zitzewitz | — |
| §2.5 LLM 预测 | **大改** | + F2[3] InfoDelphi + F2[4] AIA Forecaster + F2[5] Merger-arbitrage ICML 2026 + F2[7] Action-belief gap + F2[6] Deceptive grounding + Hartvég + AlDahoul + WorldCupBench/worldcup-predictor-2026/AI World Cup 4 占位风险 | F2[3][4][5][6][7] |
| §2.6 定位陈述 | **重写** | "三元交叉空白" → "最接近 2026 prior art + W6 7 篇 + F3 5 篇 + F2 6 篇之外，protocol integrity vector + audit-chain protocol + 同覆盖归一化无 primary-source 同形" | F4 Check 4 / 8 |
| §3 前置 | **新增** | "H1–H5 都是 audit-chain-anchored multi-forecaster reconciliation 协议在不同诊断维度的组件假设" | F4 Check 1 |
| §3 H1 | **重写** | 主语改协议；指标加 ECE/sharpness/Brier decomposition | F4 Check 3 |
| §3 H2 | 改 | 三层 CI 完整；Poisson 独立性耦合 | — |
| §3 H3 | **重写** | P3 = rank-vs-mass 分裂；与 H5-protocol schema_valid 联动 | F4 Check 4 |
| §3 H4 | **重写** | 三 sub-question：ρ 三档 + asymmetric evidence diagnosis + 同池重归一 ensemble | F4 Check 4 / F2[3] |
| §3 H5 | **新增** | 协议完整性向量七字段诊断力 | W6 §6 (4) / G4 / G7 |
| §4.A1–A4 | 微改 | H5-protocol 渗透进 A1/A2/A4 | F4 Check 3 |
| §4.A5 | 二选一 | 升 §3 H5 子假设 or 保留 n=4 局限 + schema violation 声明 | F4 Check 4 |
| §5.1 数据资产 | 改 | + cds_qualification 漂移 + ops JSON + factor-ledger 覆盖率 + ledger 状态不一致 4 项 | evidence-snapshot F1.2/F1.3/F1.5/F2.2/F2.4 |
| §5.2 已知瑕疵 | **升级 R5** | R5 = cds_qualification 漂移 + ops JSON + factor-ledger + ledger 状态不一致 + source-policy 黄源扩展 | evidence-snapshot + W6 G4 |
| §5.3 指标 | **重写** | RPS 主 + Brier/Murphy/Yates 分解辅 + reliability/ECE/sharpness 探索 | F2[2] / F3[7] |
| §5.4 比较族 | 改 | + asymmetric evidence diagnostic + 同池重归一 ensemble | F2[3] |
| §5.5 OSF 冻结物 | **扩 ≥4 类** | + Protocol Integrity Vector 七字段定义 + 同覆盖归一化规则 + fail-loud 缺失处置 | W6 §5 G4 |
| §5.6 证据保全 | 改 | + analysis/worldcup-2026/ 命名 + CHANGELOG 框架 | 已有 |
| §6.1 已有基础 | 微改 | — | — |
| §6.2 缺口 | 改 | + W6 §7 A0–A6 6 项 | W6 §7 |
| §6.3 可行性结论 | 微改 | 加 H5-protocol + F4/F2/F3 prior art 引用 | F4 |
| §7.风险 | **改/加** | 重组为 7 + 3（新）+ 周延诚实上限；吸收 W6 §8 禁用/可用表述清单 | W6 §8 |
| §7.1 基准率陷阱 | 微改 | + FIFA 前四全部进四强 锚（已 v1.3 v1.2） | 已有 |
| §7.X H5-protocol 风险 | **新增** | 协议完整性向量的 blind-application 风险 + Cohen's κ 不足的降级路径 | W6 G7 |
| §8 W6-1 | 改 | 四档 venue 候选 | F4 Check 7 / W6 §5 |
| §9 创新点 | **全改** | 见 §9.1–§9.5 表 | F4 Check 1/4/5 |
| §9.1 | **重写** | 主语改 audit-chain-anchored reconciliation 协议 | F4 Check 1 |
| §9.2 | **重写** | deviation-direction signature 框架 | F4 Check 5 |
| §9.3 | **重写** | asymmetric-evidence-as-herding-diagnostic 框架 | F2[3] / F4 Check 4 |
| §9.4 | **重写** | 五件套可复用 audit-chain 协议 | F4 Check 4 |
| §9.5 | **新增** | Protocol Integrity Vector 七字段作为协议级评估对象 | W6 §6 (4) / G4 / G7 |
| §9.6 (新) | **新增** | cross-method deliverables（原 §9.5 降级） | — |
| §9.诚实上限（每项预期） | **新增** | single-tournament case；不外推非足球；PIV 跨赛事可迁移性仅在外部测试中验证 | W6 §8.3 |
| §10 参考文献 | 改 | + ≥13 条（F2/F3/W6 共 ≥18，去重保留 ≥13） | F2/F3/W6 |
| 附录 A | 改 | + Protocol Integrity Vector 七字段术语 + Murphy/Yates decomposition 术语 | F2[2] / F3[7] |
| 附录 B | 微改 | 评审规则升级为 6 维（+ protocol integrity dimension） | — |
| 附录 C | 改 | v2.0 = Stage 1–4 流水线重构版登记 | 本报告 |

### 10.2 必读入档项（F4 + W6 + evidence-snapshot + Stage 4 子代理前置条件）

v2 必须入档（即 Stage 4 子代理必须吸收）：
1. ≥13 条新增参考文献（F2/F3/W6 共 ≥18，去重后至少 +13）
2. F4 §0 5 选题判据作为隐式骨架贯穿 v2 全部章节
3. F4 7-check test 作为 §3 H1–H5 + §9 创新点的 self-audit 锚
4. W6 §8 禁用/可用表述清单作为 §9 / §7 / 摘要的 negative-test 锚
5. evidence-snapshot-gap-analysis F1.3/F1.5/F1.2/F2.2/F2.4/F4.3 作为 §5.2 / §7 / 附录 C v2.0 的诚实边界锚
6. meta-question-recalibration Q1/Q2/Q3 三准则作为 §1.3 / §9 / 附录 B 的元质量锚
7. Protocol Integrity Vector 七字段作为 §3 H5 / §5.5 / §9.5 / 附录 A 的方法学核心新字段锚
8. crosswalk 报告（v1.3 vs W6 7 篇 + F3 5 篇 + F2 6 篇）的 12 维度对比（仅在 Stage 2 文献子代理产出 stage2-data-summary.md 后由 Stage 4 合并）

### 10.3 Stage 4 子代理的输入清单

由 Stage 4 consulting-analysis 子代理消费：

| 输入 | 路径 | 类型 |
|---|---|---|
| Stage 1 审查报告（本文件）| `analysis/worldcup-proposal-review/stage1-review-report.md` | 中文 Markdown |
| Stage 2 文献数据摘要（待 Stage 2 子代理产出）| `analysis/worldcup-proposal-review/stage2-data-summary.md` + CSV | （不归本子代理范围）|
| Stage 3 图表（待 Stage 3 子代理产出）| `analysis/worldcup-proposal-review/charts/` | （不归本子代理范围）|
| v1.3 原文件（只读）| `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` | F4 透镜锚 |
| F4 7-check test | `research/nature-first-class-paper/findings/F4.md` | F4 7-check 锚 |
| F2 邻域方法学 | `research/nature-first-class-paper/findings/F2.md` | F2 11 篇锚 |
| F3 prior art | `research/nature-first-class-paper/findings/F3.md` | F3 10 篇锚 |
| W6 终裁备忘录 | `docs/investigations/worldcup-paper-topic-2026-07-19.md` | W6 §5/§8 锚 |
| evidence-snapshot 缺口分析 | `docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` | F1–F4 诚实边界锚 |
| 元问题校准反思 | `docs/investigations/meta-question-recalibration-first-class-paper-2026-07-17.md` | Q1/Q2/Q3 锚 |
| 计划 v1.1 | `docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` | W1–W8 工作分解锚 |
| consulting-analysis SKILL | `~/.trae/skills/consulting-analysis/SKILL.md`（本地文件系统，Stage 4 须读取）| Phase 2 输出格式锚 |

### 10.4 v2 论文内部一致性 checker（Stage 4 内部自检）

| 检查项 | 期望状态 |
|---|---|
| §0.1 / §1.2 / §9.1 三处是否统一使用 audit-chain-anchored reconciliation 协议名词？ | YES |
| §2.3 + §10 是否显式 disambiguate Hyndman reconciliation？ | YES |
| §3 是否新增 H5 协议完整性向量？ | YES |
| §5.2 R1–R5 是否全部登记（W6 已知 3 + evidence-snapshot 新增 2-4）？ | YES |
| §5.3 指标表是否升级为 RPS + Murphy/Yates 分解？ | YES |
| §5.5 OSF 冻结物是否 ≥10 类（含 PIV 七字段 + fail-loud 规则）？ | YES |
| §7 风险与诚实边界是否吸收 W6 §8 禁用/可用全部条目？ | YES |
| §7 是否新增 H5-protocol 风险节？ | YES |
| §8 W6-1 是否给出 4 档 venue 候选？ | YES |
| §9 是否升级 5 项创新点（其中 ≥3 项主语为方法学机制名词）？ | YES |
| §10 参考文献是否 ≥26 条（v1.3 13 + 新增 ≥13）？ | YES |
| 附录 A 是否新增 Protocol Integrity Vector 术语？ | YES |
| 附录 C v2.0 是否登记本次重构依据？ | YES |

---

## 11. Stage 1 交付物声明

本报告是 4 阶段流水线 Stage 1 子代理的最终输出，**不**写 stage2-* 文件（并发子代理负责）；**不**写 charts 文件（Stage 3 子代理负责）；**不**修改 `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` v1.3 原文件；**不**修改任何 evidence / papers / legacy / state / framework 路径下的只读文件。

本报告输出至：`analysis/worldcup-proposal-review/stage1-review-report.md`（本文件）。

合规声明：
- 不输出任何投注建议、收益率、Sharpe / Sortino 等交易指标；
- 市场数据仅作研究基准；
- 中文为主、ISO 日期（2026-07-21）；
- 引用遵循 5 红线（不首、不冻结、不发现、不 web-only baseline、不 overconfidence 标题）—— 见 W6 §8 禁用表述清单；
- Stage 4 子代理须以本报告作为前置输入，按 consulting-analysis Phase 2 输出格式产出 v2 重构版。
