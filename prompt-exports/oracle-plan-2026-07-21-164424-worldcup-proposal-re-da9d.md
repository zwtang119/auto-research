# Orchestrator Checklist（编排器维护，子代理只读）

- [x] Item 1 — Stage 1 系统审查报告 → `analysis/worldcup-proposal-review/stage1-review-report.md`（2026-07-21 完成，720 行，11 节，含 27 条章节级 v2 修改建议）
- [x] Item 2 — Stage 2 data-analysis 文献/趋势数据摘要 → `analysis/worldcup-proposal-review/stage2-data-summary.md` + `stage2-literature-table.csv`（2026-07-21 完成，37 篇 100% verified，含 D1–D6 图表数据块）
- [x] Item 3 — Stage 3 图表生成 → `analysis/worldcup-proposal-review/charts/`（2026-07-21 完成，5 张 PNG：framework-mindmap / literature-trend / domain-distribution / occupancy-risk / coverage-gap，数据全部来自 D1–D6 数据块；mindmap 根标签因渲染限制缩写为"审计链对账比较"，v2 图注需补全称）
- [x] Item 4 — Stage 4 consulting-analysis 重构 → `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`（2026-07-21 完成，563 行/84KB，§0–§10 + 附录 A–F，43 条参考文献，7-check 自评 7/7 PASS，5 张图全部嵌入且路径验证通过；v1.3 原文件零修改；图表路径采用 `../../../analysis/...` 三层上溯——任务书字面 `../../` 有误，已按有效性硬约束修正）

**全部 4 项完成。编排器验证：交付物存在性、图表路径解析、v1.3 未改动均已直接复核通过。**

---

## Final Prompt
<taskname="Worldcup Proposal Review Pipeline"/>

<task>
按用户指令"四阶段流水线"对 `auto-research/docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md`（v1.3, 2026-07-20, **原文件只读，不得就地修改**）做方法论驱动重构：

1. **Stage 1 系统审查**：以 `research/nature-first-class-paper/REPORT.md` 与 `findings/`（F2 邻域范例 / F3 新颖性 / F4 失败签名 + 7-check test / F5 slot 复核）的方法论 5 选题判据 + F4 7-check 为透镜，评估开题报告在（a）研究问题定义、（b）文献综述完整性、（c）研究方法设计、（d）创新点阐述、（e）预期成果 五维度的不足，并对照 evidence-snapshot-gap-analysis-2026-07-20.md 与 worldcup-paper-topic-2026-07-19.md（W6 终裁备忘录）的"协议失败标签 + 硬选/Brier 排名反转"框架识别需补强的位置。产出审查报告（中文，Markdown）。
2. **Stage 2 data-analysis**：对足球预测 / LLM forecasting / 概率预测校准 领域最新文献做深度结构化摘要（可联网），重点是 (i) G3 邻域占位 (`Polymarket-v1`, `Foresight Arena`, `Polymarket-v1`, `Murphy decomposition`, `deceptive grounding`, `AIA Forecaster`, `Merger-arbitrage ICML 2026`, `InfoDelphi` 等已在 F2/F3 落地的论文) 与 2026 世界杯直接竞品（WorldCupBench / worldcup-predictor-2026 / AI World Cup / Hartvég et al. / ModelBall / Prophet Arena / ForecastBench）的占位风险，整理为结构化数据摘要。
3. **Stage 3 chart-visualization**：用本地 `node /Users/tangzw119/.trae/skills/chart-visualization/scripts/generate.js` 生成图表（参考 `/Users/tangzw119/.trae/skills/chart-visualization/references/` 的图表类型清单），至少含（i）研究框架思维导图 / 概念模型、（ii）文献趋势 / 占位风险图、（iii）五类预测者（Elo+Poisson / Coach / CDS 路径 / kimi / 市场）结构差异示意。图表输出到 analysis/worldcup-proposal-review/。
4. **Stage 4 consulting-analysis 重构**：按 `/Users/tangzw119/.trae/skills/consulting-analysis/SKILL.md` Phase 2 规范整合 Stage 1–3 全部素材，产出重构版 `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md` —— **保留 v1.3 主线主题**（"同一审计链下的五类预测者——2026 世界杯预测方法的比较实证研究"），但显式整合方法论改进：(i) 摘要 + 贡献以"方法学机制名词"为主语，避免落入 data-uniqueness 拒信；(ii) §2 文献综述以 F2/F3 邻域范例为锚，分清"组分/组合"新颖性边界，显式 disambiguate 与 Hyndman forecast reconciliation、Gulei 2015 settlement reconciliation、ForecastBench/Prophet Arena/WorldCupBench 等同形 false cognate；(iii) §3 H1–H4 按 7-check 逐项显式锚定（Check 1 single-methodological-insight / Check 2 移除数据独有生存 / Check 3 评估性主张 / Check 4 知识缺口 / Check 5 跨子领域迁移 / Check 6 deep-concern 抗冲击 / Check 7 无 unique 数据可复现）；(iv) §9 预期成果对应 W6 终裁的"协议完整性标签 + 硬选/Brier 反转"与"基准率文献锚点（FIFA 前四首次全部进四强）"；(v) §7 风险与诚实边界吸收 W6 §8 禁用表述清单。
</task>

<architecture>
**Discovery 阶段交付物（11 个全文件，已固化进 selection，token=53,143 / 118,500 预算内）：**

主轴文件：
- `auto-research/docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` —— 目标 v1.3，原文件，**只读**。主线"五类预测者比较实证"已通过用户裁定为本论文主线；W6 终裁备忘录降为参考；P2 定性已修为"LLM 辅助混合预测器"。
- `auto-research/research/nature-first-class-paper/REPORT.md` —— 方法论透镜。Nature Career《How to write a first-class paper》(Gewin 2018) 5 选题判据（C1–C5）+ F4 7-check test + P1+P2 / Direction Y/Z/X 评分汇总。**Stage 1 评审与此对齐**。
- `auto-research/research/nature-first-class-paper/findings/F2.md` —— 2024–2026 邻域方法学范例 11 篇（Harness externalization arXiv:2604.07236 / Coordination architectural layer arXiv:2605.03310 / InfoDelphi arXiv:2607.01661 / AIA Forecaster arXiv:2511.07678 / Merger-arbitrage ICML 2026 arXiv:2607.09921 / Deceptive grounding arXiv:2607.09349 等）。
- `auto-research/research/nature-first-class-paper/findings/F3.md` —— G3 dual-ledger + Brier replay 新颖性 vs 2024–2026 prior art。Polymarket-v1 / Foresight Arena / Yates decomposition / Multivariate Hyndman reconciliation / DeepHGNN / Counterfactual Brier (Keogh & van Geloven) 等 10 篇 + arXiv 零命中的"dual ledger"组合术语。
- `auto-research/research/nature-first-class-paper/findings/F4.md` —— NeurIPS 2026 E&D Reviewer Guidelines "Datasets-as-endpoints don't meet the bar on their own" + 7-check test 应用至 P1+P2 / Direction Y 的 verdict。
- `auto-research/research/nature-first-class-paper/findings/F5.md` —— Stanford Meta-Harness / Fudan AHE / Harness survey (arXiv:2606.20683 + arXiv:2605.18747) / DeepSeek Harness team 4 slot-occupant 复核（结论：3 占位 verified, 1 unverified, slot 已饱和）。

辅助文件：
- `auto-research/research/nature-first-class-paper/brief.md` —— 5 选题判据 + 项目 D17 / "data-uniqueness ≠ paper-interesting" 规则总览。
- `auto-research/docs/investigations/worldcup-paper-topic-2026-07-19.md` —— 用户 2026-07-19 终裁备忘录。"唯一值得进入下一轮硬 gate 验证的组合方向 W6 = 审计型数据集 + proper-score 反转 + 协议失败标签"，附 Q1–Q3 + C1–C7 评分卡（17/20）与 W6 八条硬 gate（G0–G7）。**Stage 1 须显式吸收 §8 禁用表述清单、§3 联网查新占位风险表、§5 venue / gate 处置、§6 G3 关系。**
- `auto-research/docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` —— 计划 v1.1（设计评审修订后）。W1–W8 工作分解 + 三个硬 go/no-go gate（G1 kimi 溯源 / G0 封存 / G2 管线可复现）。
- `auto-research/docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` —— 2026-07-20 证据快照核查。**重要事实**：漂移扩大（`cds_qualification.json` 也是 07-19 漂移版）+ KO103/KO104 已 Green Source 补齐（西班牙 1–0 阿根廷 a.e.t., 英格兰 6–4 法国）+ H-b/H-c 本人复算确认通过。
- `auto-research/docs/investigations/meta-question-recalibration-first-class-paper-2026-07-17.md` —— 上一轮 first-class paper 元问题校准，反思 v3 / v4 review 历史的同类问题，供 v2 写作时复用结构性教训。

文件系统外但用户指定的 SKILL/工具路径（**不在 workspace 根内**，下一模型通过文件系统读写）：
- `/Users/tangzw119/.trae/skills/consulting-analysis/SKILL.md` —— Stage 4 重构规范（Phase 2 输出格式）。
- `/Users/tangzw119/.trae/skills/chart-visualization/scripts/generate.js` —— Stage 3 图表生成 node 脚本。
- `/Users/tangzw119/.trae/skills/chart-visualization/references/` —— Stage 3 图表类型参考。

不可写硬约束：
- `~/Documents/GitHub/cds4worldcup` —— **封存仓库，零读写**。所有引用路径只是逻辑指向，真实操作只能走 `auto-research/evidence/cds4worldcup-snapshot-2026-07-20/`（字节级原始）或 `auto-research/analysis/worldcup-2026/`（待建的"分析副本"，所有增补逐条记 CHANGELOG）。
- `auto-research/evidence/` / `auto-research/papers/` / `auto-research/legacy/` / `auto-research/state/` / `auto-research/framework/` —— **只读**。
- 中间产物统一放 `auto-research/analysis/worldcup-proposal-review/`（目录不存在则首次创建）。
- 最终交付物：`auto-research/docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`（新文件，**不动 v1.3 原文件**）。

合规硬约束（继承项目 source-policy.md 2026-06-11 draft-for-execution 版本）：
- 不输出投注建议、收益率、Sharpe / Sortino 等交易指标；
- 市场数据仅作研究基准；
- 中文为主、ISO 日期；
- 引用遵循 5 红线（不首、不冻结、不发现、不 web-only baseline、不 overconfidence 标题）—— 见 W6 §8 禁用表述清单。
</architecture>

<selected_context>
- `auto-research/docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` (278 行 / 8,902 tok) —— v1.3 主文件：**审计链 + 五类预测者 + 真 ex-ante**主轴；§0 导读 + §1 背景/问题 + §2 文献综述（5 谱系 + 定位）+ §3 H1–H4 假设 + §4 五模块 + §5 数据/分析协议 + §6 可行性 + §7 风险（9 项含 FIFA 前四基准率锚点）+ §8 8 周进度 + §9 5 项创新点 + §10 13 条参考文献 + 附录 A–C 术语/评审规则/版本史。
- `auto-research/research/nature-first-class-paper/REPORT.md` (259 行 / 7,447 tok) —— 5 选题判据（C1 Single-key-message Mensh / C2 红线 Murphy / C3 全局 + 替代解释 Borja+Gorsuch / C4 人类故事 + 跨受众 Doubleday+Konkiel / C5 可复现 Gorsuch）+ F4 7-check test + 计分汇总表（"P1+P2 最佳 / Direction Y 当前 framing 5/7 FAIL / Direction Z GATED / Direction X CLOSED"）+ §7 Nature 2018 五位一体对应。
- `auto-research/research/nature-first-class-paper/findings/F2.md` (103 行 / 3,289 tok) —— 11 篇 2024–2026 方法学范例（arXiv:2604.07236 / 2605.03310 / 2607.01661 / 2511.07678 / 2607.09921 / 2607.09349 等）。**对 v2 §2 文献综述最有价值的锚点**：所有第一梯队 paper 都以方法学机制名词为主语（"coordination" / "Murphy decomposition" / "deceptive grounding" / "hindsight-guided supervision"），无一以数据独有为卖点。
- `auto-research/research/nature-first-class-paper/findings/F3.md` (99 行 / 3,169 tok) —— G3 novel 与 Hyndman forecast reconciliation false cognate 显式 disambiguation 必须项；Polymarket-v1 / Foresight Arena / Counterfactual Brier (Keogh & van Geloven Epidemiology 2024) 等最近邻 prior art 逐篇关键信息 + arXiv 零命中记录（"dual ledger reconciliation calibration" / "Brier score replay settlement" 等 5 组合术语）。
- `auto-research/research/nature-first-class-paper/findings/F4.md` (167 行 / 4,507 tok) —— NeurIPS 2026 E&D reviewer guidance / NeurIPS 2023 reviewer form / ACL/ARR canonical reject language（"the paper is mostly a description of the corpus"）/ 7-check test 完整定义 + Check 1–7 应用于 P1+P2 与 Direction Y 的 verdict。
- `auto-research/research/nature-class-class-paper/findings/F5.md` (84 行 / 3,508 tok) —— Stanford Meta-Harness (arXiv:2603.28052) / Fudan AHE (arXiv:2604.25850) / Two harness-engineering surveys (arXiv:2606.20683 "From QA to Task Completion" + 2605.18747 "Code as Agent Harness") / DeepSeek Harness team UNVERIFIED。**对 v2 §2 不直接相关但提供"避免 slot 误占"的审查纪律样本**。
- `auto-research/research/nature-first-class-paper/brief.md` (40 行 / 1,234 tok) —— 5 判据 + 项目 D17 + "data-uniqueness ≠ paper-interesting" 规则总览 + Phase 2 5 angles。
- `auto-research/docs/investigations/worldcup-paper-topic-2026-07-19.md` (441 行 / 9,452 tok) —— W1–W6 六候选方向 + W6 GO (附条件 G0–G7) 终裁。**最关键素材**：§1.2 已结算结果表（Elo Brier 0.5728/hard 54.9% n=71 / Coach 0.6078/hard 59.7% n=72 / Kimi top-5 4/5 hit / CDS 93.5% mass on eliminated / market 39 队 / Kimi 21 队 / uniform Brier 0.6667）+ §1.4 五类预测器横向对比三描述性发现（rank-vs-mass 分裂 / 校准排序反转 / 信号与归一化耦合）+ §2 联网查新占位风险表（ForecastBench / Prophet Arena / WorldCupBench / worldcup-predictor-2026 / ModelBall / AI World Cup / LMU SoccerArena / Hartvég / AlDahoul）+ §3 W1–W6 per-direction verdict + §4 Q1–Q3 + C1–C7 评分卡 + §5 W6 八条硬 gate + §7 A0–A6 立即行动项 + §8 禁用/可用表述清单 + §9 路线图 + §10 引用清单 + §11 终裁登记。
- `auto-research/docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` (94 行 / 2,777 tok) —— 计划 v1.1。五模块（统一结算管线 / 市场基线同台 / 校准结构差异 / kimi vs 市场 / 因子账本案例）+ W1–W8 工作分解 + 3 个 go/no-go gate + 评审修订记录。
- `auto-research/docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` (150 行 / 4,920 tok) —— F1–F4 + Root Cause + Recommendations + Preventive Measures。**Stage 1 必读**：F1.3/F1.5 cds_qualification.json 高危缺口（qualified/eliminated 布尔缺位 + ops JSON 不存在，但 2026-07-20 pair 误报已被本人复核证伪）+ F2.2/F2.4 factor-ledger 3.85% 覆盖率 + 3/4 ledger 状态不一致 + F4.3 source-policy draft-for-execution 滞后 + 4 类补入信息清单（赛果 / ex-ante 提取 / kimi 溯源 / CHANGELOG）+ 2 个 refuted oracle 断言。
- `auto-research/docs/investigations/meta-question-recalibration-first-class-paper-2026-07-17.md` (~100 行 / 3,938 tok) —— 上一轮 first-class paper 元问题校准反思，提供 v2 重构时的结构性教训（避免重蹈 v3/v4 review history 的失败模式：数据独有标语 + 单场事件结论 + 缺独立验证 + 段层 trade-off 失衡）。
</selected_context>

<relationships>
- **v1.3（目标）** → **W6 终裁备忘录 (2026-07-19)**：v1.3 主线 = W6 主线（用户 2026-07-20 用户 Up-front 访谈裁定 → 已反映在 v1.3 §页眉 + §0 + §2 + §5）。W6 备忘录 §8 禁用表述 + §1.4 横向对比 + §5 八条 gate 必须并入 v2 §7 + §3 + §9。
- **v1.3 → F4 7-check test**：v1.3 当前 H1–H4 + 五模块对应 7-check 中的部分项，但 Check 1 single-methodological-insight / Check 2 移除数据独有生存 / Check 4 knowledge gap / Check 7 无 unique 数据可复现 在 v1.3 中**未显式锚定**——v2 须逐项补充。
- **v1.3 §2 文献综述** → **F3 prior art**：v1.3 当前仅引 Dixon-Coles 1997 / Groll 2019 / Hubáček 2019 / Gneiting-Raftery 2007 / Constantinou-Fenton 2012 / Wolfers-Zitzewitz 2004 / Hong-Page 2004 / Halawi 2024 / Prophet Arena 2025。F3 揭露的更接近 prior art（Polymarket-v1 2026-06 / Foresight Arena 2026-05 / Counterfactual Brier (Keogh & van Geloven Epidemiology 2024) / Yates covariance decomposition 2026-03 / Hyndman multivariate reconciliation 2026-05）v1.3 **零引用**——v2 §2 必须扩。
- **v1.3 §2 → F2 邻域方法学范例**：F2 11 篇范例的写作范式（"方法学机制名词 + 单句关键信息"）应作为 v2 §0 导读 + §1.2 一句话陈述 + §9 创新点的句法模板。
- **v1.3 §3 H4**（kimi vs 市场 Spearman ρ） → **F2 arXiv:2607.01661 (InfoDelphi) "designed information asymmetry as the key enabler"**：H4 现在只问"是否可区分"，v2 应吸收 InfoDelphi 把"是否独立信息"升级为"何种 asymmetric evidence 缺位导致 herding"的诊断粒度。
- **v1.3 §5 指标** → **F3 arXiv:2605.03310 Murphy decomposition**：v1.3 Brier/RPS/Log Loss 单一总分，应吸收 Murphy decomposition 把 Brier split 为 calibration vs discrimination 分量——v2 §5 升级为"主指标 RPS + Brier 分解分量 + reliability diagram"。
- **v1.3 §7.1（基准率陷阱）** → **W6 §1.4 + evidence-snapshot 基准率锚点**：v1.3 §7.9 已写入"FIFA 前四首次全部进四强"事实，v2 §7 应升级为更结构化的"基准率论证 + 历史赛事 top-5 命中率分布表"。
- **v1.3 §9 创新点 1–5** → **F4 Check 1 single-methodological-insight sentence**：v1.3 创新点 1 "首个全公开审计链的世界杯多方法比较实证" 是 data-uniqueness 句式（受 F4 §1 警示）；v2 §9 应改为方法学机制句式，例如"提出一种 audit-chain-anchored multi-forecaster reconciliation protocol，以 git 冻结 + 来源分级 + 统一结算 + OSF 分析协议冻结的五件套把 '公开审计链预测比较' 升格为可复现评估协议"。
- **evidence-snapshot-gap-analysis-2026-07-20.md** → **v1.3 §5.2 已知瑕疵处置**：v1.3 §5.2 R1/R2/R4 三条已登记；F1.2/F2.4 新发现的"qualification.json 漂移" 与"plan-c ledger 状态不一致"在 v1.3 中**未提及**——v2 §5.2 / §7 应新增。
- **meta-question-recalibration-first-class-paper-2026-07-17.md** → **v2 整体**：该反思报告记录了 v3/v4 的失败签名（数据独有 + 单场事件结论 + 缺独立验证 + 段层 trade-off 失衡），供 v2 写作时复用结构性教训。

**关键依赖链（下一模型重写时必须保留的因果链）**：
1. **用户 Up-front 决策（2026-07-20）= 主线 + n 分层声明** → v1.3 §0.3 三层 n 声明 + §5.5 OSF 协议冻结；
2. **五位"考生"识别** = Elo+Poisson / Coach / CDS / kimi / 市场 + §0.2 一句话描述 → v1.3 表格 + §2 谱系映射；
3. **kimi 溯源基本闭环** = H-b/H-c 21/21 复算一致 + 88a9bfd 提取逐位一致 + 版本不可考声明 → v1.3 §5.3 V-kimi/V-88a + §7.5；
4. **证据三级结构** = 封存仓库零读写 + 证据快照字节级原始 + 分析副本可写增补 → v1.3 §5.6 + §0 命名约定；
5. **FIFA 前四基准率锚点** = 2026-07-20 Wikipedia Green Source 核验（首次 FIFA 前四全部进四强） → v1.3 §7.9 + W6 §3 H4 描述。
</relationships>

<ambiguities>
1. **两套对照框架的优先级排序**：F4 7-check test 要求 Check 1 "single-methodological-insight sentence" 排除 data-uniqueness 框架；但 W6 终裁明确将数据集作为主线（"审计型数据集"）。下一模型须调和——v2 §0 一句话应以"方法学机制名词"为主语（Check 1），但 §9 创新点允许"可发布资产 = 数据集"作为 cross-method deliverable（Check 2 通过：移除"我们独占此数据"后 crosswalk 方法仍独立）。
2. **"协议失败标签"是否独立成创新点**：W6 终裁把 protocol integrity vector 列为方法学核心新字段；v1.3 §9.4 已写"可复用的预测比较协议"。下一模型须在 v2 §3 H5 增加 H-protocol（协议完整性向量的诊断力）以避免"可复用协议"沦为描述。
3. **kimi 比较族规模**：v1.3 §5.4 已锁定 5 法族（kimi 升一等公民）；W6 备忘录要求 V-kimi 失败则降级为 4。下一模型须保留预写降级路径，**不强行二分**——v2 §5.4 应明示 G1 决策前 5 族为预期态、G1 失败预写降级。
4. **Plan C 是否独立成节**：v1.3 §4.A5 把 Plan C 因子账本 4 场案例作为"次要"案例分析；W6 终裁 §6 把 Plan C 失败模式纳入既有 C1 process-trace 主线。下一模型须决定——v2 §4 保留"次要案例分析"位置（与 W6 主线不冲突），还是升级为独立 H5 假设（更结构化但引入并行假设）。
5. **本地 skill 文件不在 workspace 内**：consulting-analysis SKILL.md / chart-visualization scripts 位于 `/Users/tangzw119/.trae/skills/`，**不在 RepoPrompt 根内**。下一模型需通过本地文件系统（read_file / shell）访问；如路径失败须汇报而非猜测。
</ambiguities>


## Selection
- Files: 11 total (11 full)
- Total tokens: 25280 (Auto view)
- Token breakdown: full 25280
- Token accounting: incomplete from active_tab_published; refresh pending; incomplete: files

### Files
### Selected Files
auto-research/
├── docs/
│   ├── investigations/
│   │   ├── worldcup-algorithms-proposal/
│   │   │   └── proposal-worldcup-algorithms.md — 8,902 tokens (full)
│   │   ├── evidence-snapshot-gap-analysis-2026-07-20.md — 4,920 tokens (full)
│   │   ├── meta-question-recalibration-first-class-paper-2026-07-17.md — 0 tokens (full)
│   │   └── worldcup-paper-topic-2026-07-19.md — 0 tokens (full)
│   └── plans/
│       └── worldcup-algorithms-comparison-paper-2026-07-20.md — 2,777 tokens (full)
└── research/
    └── nature-first-class-paper/
        ├── findings/
        │   ├── F2.md — 0 tokens (full)
        │   ├── F3.md — 0 tokens (full)
        │   ├── F4.md — 0 tokens (full)
        │   └── F5.md — 0 tokens (full)
        ├── REPORT.md — 7,447 tokens (full)
        └── brief.md — 1,234 tokens (full)


---

## Generated Plan

## Chat Send ✅
- **Chat**: `worldcup-proposal-review-B1A8A4` | **Mode**: plan


> 💡 Continue this plan conversation with ask_oracle(chat_id: "worldcup-proposal-review-B1A8A4", new_chat: false)