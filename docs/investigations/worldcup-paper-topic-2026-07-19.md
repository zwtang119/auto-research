# 备忘录：基于 `cds4worldcup` 已结算结果的论文选题终裁

- **裁决基准日**：2026-07-19
- **仓库复核日**：2026-07-20
- **对象**：`/Users/tangzw119/Documents/GitHub/cds4worldcup`（只读）
- **产出位置**：`auto-research/docs/investigations/worldcup-paper-topic-2026-07-19.md`
- **裁决口径**：Horejs Q1–Q3（跨域重要性、数据鲁棒、发现可接续）+ 本项目 C1–C7 选题过滤器
- **前科约束**：继承 2026-07-18 终裁，不重新包装已经 KILL 的 D2/D4；G3 standalone 维持 PARK，除非新增证据真正改变其数据上限。

---

## 0. 执行摘要：终裁结论

**唯一值得进入下一轮硬 gate 验证的组合方向是：以“带协议完整性标签的事前预测数据集”为主线，以“硬选准确率与 proper score 排名反转”为结果卖点，以协议失败审计为方法贡献。该组合为 `GO（附硬条件）`；其余方向不得独立抢跑。**

这里的 GO 是“允许做 gate work”，不是“新颖性已经证明”：若 G7 外部生存测试失败，W6 只能降为 workshop case report，不得保留 D&B 主张。

建议工作题目：

> **Accuracy and Brier Rank Can Diverge: An Audited Ex-Ante Benchmark of 2026 World Cup Forecasting with Protocol-Failure Labels**  
> **正确率与 Brier 排名可以反转：一个带协议失败标签的 2026 世界杯事前预测基准**

建议红线句：

> 本工作不再声称“首个世界杯 LLM benchmark”，而是把快照漂移、预注册缺失、来源渗漏、schema 违规和裁决缺位变成与 Brier 同等的一等评估对象，并展示硬选准确率更高并不保证概率预测更好。

终裁如下：

| 编号 | 候选方向 | 终裁 | 处置 |
|---|---|---|---|
| W1 | 纯“数据集 + 协议”D&B paper | **PARK** | 已被通用预测 benchmark 与多个 2026 世界杯直接 benchmark 占位；只能作为组合论文的数据骨架 |
| W2 | LLM 预测校准发现短文 | **PARK** | “过度自信”不是当前统计已识别结论，且 2024–2026 文献已正面占位；吸收为 W6 的结果章节 |
| W3 | G3 双账本桥接升级版 | **PARK** | 新世界杯资产没有修复 64.3% 严格覆盖率、内部验证和小样本问题；与 W6 平行，不合并主线 |
| W4 | 协议失败教训 meta 短文 | **PARK（独立）/吸收（主线）** | 作为单项目 N=1 仍弱；吸收到 2026-07-18 已 GO 的 process-trace/failure-taxonomy 主线，并作为 W6 的 protocol-failure labels |
| W5 | 冠军概率过度分散短文 | **KILL（独立）** | 单赛事、单正例、类不平衡严重；仅作 W6 的次级案例 |
| W6 | **审计型数据集 + proper-score 反转 + 协议失败标签** | **GO（附条件）** | 当前最优组合；首选做可发布 benchmark/data note，NeurIPS D&B 仅作 stretch，现实出口为 evaluation/forecasting workshop |

**一句话拿主意**：本项目可以写论文，但不能写成“我们也做了一个世界杯预测 benchmark”；应写成“我们展示了一个真实 live benchmark 如何在看似有分数、有 git、有预注册的情况下仍发生协议完整性破坏，并把这些破坏结构化为可评估标签”。

---

## 1. 证据底盘：实际拥有什么，实际缺什么

### 1.1 可用资产

1. **小组赛双预测器**：
   - Elo+Poisson：严格事前有效 **n=71**；match 1 没有赛前快照，不能并入主统计。
   - Coach 对位预测器：**n=72**；其流水线是 MiniMax LLM 选择 48 队 × 6 阵型的首发 XI，随后由身价位置对位、20 次阵型蒙特卡洛和 Poisson 产生 W/D/L 概率。故准确名称应是 **LLM-assisted hybrid predictor**，不是端到端纯 LLM forecaster。
2. **队伍级 CDS 结果**：出线概率 48 队已完整结算；冠军概率截至本次仓库复核仍为 **n=46**，西班牙与阿根廷决赛结果尚未写入结果文件。
3. **Plan C**：4 场具有 Factor Ledger、预测卡、结算记录和协议失败日志；共 12 因子，5 supported、1 rejected、6 inconclusive。3 个平局案例提供了有解释力的失败分析，但 4 场样本没有统计推断力。
4. **六类注册基线**：uniform、defending champion、FIFA、elo_proxy、market（39 队）、Kimi（21 队）。后两者覆盖不全，必须逐任务报告分母，不能写成“六个完整基线”。
5. **协议与审计资产**：预测卡、source policy（Green/Red）、Factor Ledger schema、git 历史、5 份评估/结算报告。

### 1.2 已结算结果

| 任务/预测器 | n | 硬选准确率 | Brier ↓ | Log Loss ↓ | 解释 |
|---|---:|---:|---:|---:|---|
| Elo+Poisson | 71 | 54.9% | **0.5728** | **0.9410** | proper score 最优，但系统性偏主胜、低估平局 |
| Coach 混合预测器 | 72 | **59.7%** | 0.6078 | 1.0113 | 硬选更高，但概率质量弱于 Elo |
| simple_stat | 72 | — | 0.6403 | — | 项目已登记简单统计基线 |
| uniform | 理论 | — | 0.6667 | 1.0986 | 无信息基线 |

关键可写结果有三项：

1. **硬选—proper score 排名反转**：Coach 硬选 59.7% 高于 Elo 的 54.9%，但 Brier（0.6078 vs 0.5728）和 Log Loss（1.0113 vs 0.9410）均更差。该结果说明“选对更多场”不等于“给出的概率更可靠”。
2. **结构性偏差**：Elo 平均主胜概率相对实际主胜率高约 **+10.9pp**，平均平局概率低约 **−8.3pp**。13 场实际结果概率低于 0.20 的 Elo “爆冷”中，11 场是平局。
3. **路径概率过度分散**：截至 n=46，已经出局的 46 队承载冠军概率质量 **93.5%**；头号热门 Senegal 仅 4.39% 且在 R32 出局。该结果是模型级诊断，不是一般规律。

### 1.3 决定性缺口

- 淘汰赛 30 场没有事前预测；“淘汰赛前 pre-register”没有执行。该缺口不可用事后补预测修复，只能作为 missing-by-protocol 公布。
- `judge_adjudication_results.csv` 为 0 行数据；不得声称 multi-judge 裁决已执行。
- 3 张 Plan C 预测卡使用 `plan_c_v0.1_no_fixed_rendered_prompt` 一类占位文本，而 schema 描述要求 rendered prompt 的 SHA-256。
- `odds.json` 在不同 commit 间有 44/72 场漂移；虽然可从 commit `88a9bfd` 恢复 n=71 的评分版本，但当前仓库没有独立、不可变、带 manifest 的赛前快照包。
- 无赛中贝叶斯更新；无法捕捉 MD3 轮换、动机和状态变化。
- Kimi 属 Red source，却通过 Elo bonus 进入 Elo 代理；这使“统计模型 vs LLM”并非完全干净的因果对照。
- market 仅覆盖 39 队、Kimi 仅覆盖 21 队；逐场市场 W/D/L 基线缺失。
- Plan C 已有 schema 违规立案；结算后 artifact 不能被笼统写作 schema-compliant。

上述缺口不是论文附录里一句 limitations 可以消化的问题；它们本身必须进入数据 schema 和评估设计。

### 1.4 现有五类预测器横向对比（2026-07-20 增补）

全部基于冻结的赛前 artifact（Elo/Coach 逐场、CDS 出线与冠军、Kimi 基线、市场赛前基线 `baselines/market-public.json` 快照 2026-06-11）。赛果：西班牙 1:0 阿根廷夺冠，四强 = 西班牙/阿根廷/法国/英格兰。

| 预测器 | 任务层 | 覆盖率 | 冠军概率与排名 | 冠军 log score ↓ | top-5 含四强队 | 逐场 proper score |
|---|---|---|---|---|---|---|
| Kimi 共识基线 | 冠军 | 21 队 | 西班牙 23.82%（#1） | **1.44**（21 队口径） | **4/5** | — |
| 市场赛前基线 | 冠军 | 39 队 | 西班牙 16.44%（#1；同 21 队口径重归一 17.20%） | **1.76**（同口径） | **4/5** | — |
| CDS 路径引擎 | 冠军 | 48 队 | 西班牙 3.30%（#3；头号塞内加尔 4.46% R32 出局，#2 厄瓜多尔 R32 出局） | 3.41 | 3/5 | — |
| uniform | — | 48 队 | 2.08% | 3.87（48 队）/ 3.05（21 队） | — | Brier 0.6667 |
| Elo+Poisson | 逐场 | 71 场 | — | — | — | **Brier 0.5728 / LL 0.9410** / 硬选 54.9% |
| Coach 混合（LLM 选阵+数值 MC） | 逐场 | 72 场 | — | — | — | Brier 0.6078 / LL 1.0113 / **硬选 59.7%** |
| simple_stat 基线 | 逐场 | 72 场 | — | — | — | Brier 0.6403 |
| CDS 出线 | 出线 | 48 队 | — | — | — | Brier 0.2392（vs 常数 0.25；UEFA 全对、CAF 主导失败） |

对比中三个可写进论文的描述性发现（均限定单届赛事、不作方法有效性推断）：

1. **Kimi 与市场命中组成同集合但内部分配不同，且 Kimi 的两处偏离方向全部正确**：两者 top-5 均为西/法/阿/葡/英、同中 4/5；但同池重归一后 Kimi 把阿根廷抬到 19.59%（市场 8.98%）、把葡萄牙压到 6.56%（市场 11.72%）——阿根廷进决赛、葡萄牙 R16 出局，两处偏离 ex post 全对；冠军 log score 1.44 vs 1.76。**这是描述性亮点，不是技能验证**（n=1 赛事，无法排除运气或二手共识）。
2. **路径引擎的信号在排序层保留、在概率质量层丢失**：CDS 把冠军排第 3（与市场/Kimi 同列 top-5 中的 3 席），但概率质量 93.5% 落在出局队——「可能性几何」与「概率估计」的语义分裂（rank-vs-mass 分裂），缺失环节是校准/重加权而非信息。
3. **三层任务上每类预测器各有胜负，任何「谁更准」都依赖口径**：Kimi/市场赢在冠军层（锐且命中）、Elo 赢在逐场 proper score、Coach 赢在硬选准确率、CDS 出线层优于常数基线——**评估轴与归一化口径的选择足以翻转排名**，这正是 W6 把协议完整性与评估口径显式化列为一等公民的实证基础。

---

## 2. 联网查新：新颖性占位风险

### 2.1 足球预测数据集与事前 benchmark

足球概率预测早有成熟先验：

- Dubitzky et al. 的 **Open International Soccer Database** 包含 216,743 场、52 个联赛、35 个国家，并支撑 2017 Soccer Prediction Challenge；挑战要求在结果未知时提交对 206 场未来比赛的概率预测，采用固定时间线和 RPS 评分。论文发表于 *Machine Learning* 108:9–28（2019），DOI: [10.1007/s10994-018-5726-0](https://doi.org/10.1007/s10994-018-5726-0)。
- Bunker, Yeung, Fujii 的综述将该数据库称为事实上的 benchmark，并系统讨论 Brier、RPS、Log Loss 与准确率；见 arXiv:[2403.07669](https://arxiv.org/abs/2403.07669)。
- Rezaei & Samadi 2026 预印本以 2018/2022 世界杯共 128 场做严格 information-barrier 回测，并比较 11 个 Elo/Poisson/时序/机器学习模型；见 arXiv:[2606.24171](https://arxiv.org/abs/2606.24171)。

**占位判断**：不能声称“首个足球事前预测数据集”“首个用 proper scoring rule 评估足球预测”“首个冻结未来比赛做 acid test”。本项目的可能增量只能在**协议审计粒度**，不在任务或指标首创。

### 2.2 通用 LLM forecasting 与 calibration

- Halawi et al., **Approaching Human-Level Forecasting with Language Models**, NeurIPS 2024，DOI: [10.52202/079017-1598](https://doi.org/10.52202/079017-1598)，已经比较 LLM 与人群预测、使用 Brier 和校准图，并表明零样本基座模型校准较弱，而检索、微调和集成可以改善校准。
- Karger et al., **ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities**, ICLR 2025，建立持续更新的 1,000 题未来事件 benchmark、夜间结算、公开 leaderboard，并比较公众、39 名 superforecasters 与 LLM；见 arXiv:[2409.19839](https://arxiv.org/abs/2409.19839) 和 [ICLR 2025 poster](https://iclr.cc/virtual/2025/poster/28507)。
- Yang et al., **LLM-as-a-Prophet / Prophet Arena**, ICLR 2026 program 收录，连续采集 live tasks，报告 1,300+ 已结算事件、23 个模型，并同时评估 Brier、ECE 和市场相对表现；见 arXiv:[2510.17638](https://arxiv.org/abs/2510.17638) 和 [ICLR 2026 poster](https://iclr.cc/virtual/2026/poster/10009102)。

**占位判断**：“live、持续更新、无污染、Brier/ECE、LLM vs human/market”的通用 benchmark 叙事已经高度饱和。72 场单赛事数据不能在规模或普适性上与之正面竞争。

### 2.3 2026 世界杯与 LLM 体育预测的直接竞品

这是本次查新最决定性的部分：

1. **WorldCupBench**（GitHub artifact）：统一提示、结构化 JSON、冻结赛前、72 场 1X2 概率、Brier 与 provenance；仓库同时出现“10 models”和“11×72 predictions”口径，且 freeze-v3 没有完整冠军 bracket，但已直接占据“冻结的世界杯 LLM 概率 benchmark”位置。见 [dckthulhu/WorldCupBench](https://github.com/dckthulhu/WorldCupBench)。
2. **worldcup-predictor-2026**（GitHub artifact）：Claude/Gemini/OpenAI × web/baseline/enriched 三臂，72 场小组赛、完整 knockout bracket、原始输出和 Brier；见 [willianpinho/worldcup-predictor-2026](https://github.com/willianpinho/worldcup-predictor-2026)。
3. **AI World Cup**（GitHub artifact）：统一 full-tournament prompt、人工提交、多模型 leaderboard 与可复现评分；见 [974103107/ai-world-cup](https://github.com/974103107/ai-world-cup)。
4. Hartvég et al., **Forecasting the FIFA World Cup 2026 with Large Language Models**，Preprints.org v1（2026-07-10），比较 reasoning、web augmentation、agentic 与 open-weight 条件，涵盖小组、淘汰赛和冠军三层任务；见 [202607.0719](https://www.preprints.org/manuscript/202607.0719)。该文尚非同行评审，但已占据标题与 benchmark framing。
5. AlDahoul et al., **Predicting the Pitch or Repeating the Public?**，SSRN preprint，研究世界杯预测中的 consensus bias；DOI: [10.2139/ssrn.6900538](https://doi.org/10.2139/ssrn.6900538)。
6. Geoff Gibbins/ModelBall 2026 作者托管 working paper 声称在 18 个联赛、979 场、4 个前沿模型上发现系统性过度自信，并用 bias-derived shrinkage 改善 Brier 4.6%–7.3%；见 [author-hosted PDF](https://modelball.ai/papers/improving-llm-predictions-2026-04-27.pdf)。该材料尚缺独立同行评审，且其 r=0.997 只来自 4 个模型，不能作为定论；但对“首次发现 LLM 足球预测过度自信”构成直接新颖性威胁。
7. LMU Munich 已公开 **LLM SoccerArena** 项目，计划以动态真实赛果和 leaderboard 比较模型、检索与不确定性处理；见 [LMU project notice](https://www.lmu.de/en/newsroom/news-overview/news/fifa-world-cup-how-well-can-ai-predict-sports-results-675684e5.html)。

**综合占位风险**：

| 可声称内容 | 风险 | 结论 |
|---|---|---|
| 首个 2026 世界杯 LLM benchmark | 极高 | **禁止** |
| 首个冻结赛前预测并赛后结算 | 极高 | **禁止** |
| 首次用 Brier/ECE 看 LLM forecasting | 极高 | **禁止** |
| 首次发现 LLM 体育预测过度自信 | 极高 | **禁止** |
| 首次比较 web/agentic/no-web 条件 | 极高 | **禁止** |
| 把协议破坏结构化为 benchmark labels，并与预测分数联合发布 | 中等、可争 | **本项目唯一潜在可守红线（待 G7 外部复核）** |
| Factor Ledger 对 final score 失败的可裁定分解 | 中等、可争 | 可作方法/诊断贡献，但必须解决 schema 与裁决缺位 |

---

## 3. 候选方向枚举

### W1：纯数据集 + 协议 D&B

**核心主张**：发布 2026 世界杯双预测器、六类基线、队伍级 CDS 结算、Plan C 因子结算和 git 审计链。

**问题**：作为“一个新 benchmark”，规模和模型覆盖均被 ForecastBench、Prophet Arena、WorldCupBench 等压制；当前 immutable snapshot、KO coverage、市场基线和 schema 又不完整。

### W2：LLM 预测校准发现短文

**核心主张**：Coach 硬选更准但 Brier/Log Loss 更差，且存在主胜高估、平局低估。

**必要纠偏**：

- Coach 是 LLM 选择首发 XI 后接数值模拟的混合流水线；它可以作为“LLM-assisted forecasting system”，不能不加限定地写成“LLM 直接给概率”。
- “硬选更准但 Brier 更差”只识别出 **accuracy–proper-score reversal**，不能单凭该差异识别“过度自信”。过度自信必须由 reliability diagram、分箱 observed frequency、ECE/ACE 或明确的 sharpness–calibration 分解支持。
- 主胜 +10.9pp、平局 −8.3pp 是 Elo 的结构偏差；不能无条件归因于 Coach 或 LLM。

### W3：G3 桥接方法论文升级版

**核心主张**：把新增 4 个 Plan C 结算与世界杯结果并入 dual-ledger bridge，把 schema reconciliation 与协议失败检测升级为方法论文。

**问题**：2026-07-18 审计已确认严格语义覆盖率是 9/14=64.3%，不是旧 outline 的 92.9%；旧 Brier replay 2/2 是版本消歧后的 illustrative result；新增 settlement 同属一组内部资产，并且 Plan C 本身存在 schema 违规和 0 行 judge 表。新增数据提高厚度，但不改变外部效度。

### W4：协议失败教训 meta 短文

**核心主张**：live forecasting benchmark 在实践中如何发生“预注册未执行、hash 占位、快照漂移、Red source 渗漏、裁决缺位、schema 漂移”。

**优势**：跨足球、预测市场、AI agent evaluation 都重要；他组可以直接复用 failure signatures 和 stop/go checklist。

**问题**：当前只有一个项目实例，taxonomy 是事后归纳；独立成文会退化成 postmortem。它最适合成为 2026-07-18 已裁定 GO 的“process trace + failure taxonomy + stop/pivot”主线中的一个高质量案例。

### W5：冠军路径概率过度分散短文

**核心主张**：93.5% 冠军质量落在已出局 46 队，头号热门 R32 出局，说明路径枚举过度分散。

**问题**：48 队冠军任务最终只有一个正例；按队伍平均的 binary Brier 被 47 个零结果支配，不能单独反映对冠军的识别能力。该现象高度依赖本项目 200-MC 路径引擎，缺跨赛事复现。

### W6：审计型数据集 + proper-score 反转 + 协议失败标签（组合方向）

**核心主张**：发布的不只是预测和赛果，而是一个带**协议完整性状态**的数据对象：每条预测同时标注是否事前、是否冻结、来源是否合规、prompt hash 是否真实、schema 是否通过、是否有独立裁决、基线是否同覆盖。以此重新解释“硬选更高但 Brier 更差”与 Plan C 的因子级失败。

**为什么组合后比各单篇更强**：

- 数据集给 W2 真实、可重算的落点；W2 给数据集一个非“只发布数据”的结果红线。
- W4 的失败模式不是附录道歉，而是 W6 的新字段和评估轴，因而有方法贡献。
- 即使删掉“2026 世界杯”独占数据，protocol-integrity annotation 和 audit checklist 仍可迁移到其他 live benchmark，能通过 C2/C7 的反向生存测试——但前提是做外部复核。

---

## 4. Q1–Q3 + C1–C7 逐项评分

### 4.1 评分口径

- **2 = PASS**：当前证据已基本满足。
- **1 = CONDITIONAL**：方向成立，但有明确硬 gate 未过。
- **0 = FAIL**：当前证据不支撑，或先验工作已占位。
- 总分仅用于排序；**Q2 或 C5 为 0 时，即使总分较高也不得 GO**。
- 分数不是自动裁决器；§5 另适用两条项目级 gate：**单项目 N=1 的 meta claim 未经外部复核不得 GO；方法新颖性未经直接竞品 crosswalk 不得 GO**。W4 因前一条维持 PARK；W6 仅以 G7 待验证的 conditional GO 进入下一轮。

| 方向 | Q1 跨域重要 | Q2 数据鲁棒 | Q3 可接续 | C1 标题一句话 | C2 红线/去独占 | C3 大背景 | C4 广读者 | C5 主张-证据 | C6 他组接得住 | C7 非数据独有 | 总分/20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| W1 纯 D&B | 1 | 1 | 2 | 2 | 1 | 2 | 1 | 1 | 2 | 1 | **14** |
| W2 校准短文 | 1 | 1 | 1 | 2 | 0 | 2 | 1 | 0 | 1 | 1 | **10** |
| W3 G3 升级 | 1 | 0 | 1 | 2 | 1 | 1 | 1 | 0 | 1 | 1 | **9** |
| W4 协议 meta | 2 | 1 | 2 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | **16** |
| W5 冠军过散 | 0 | 1 | 1 | 2 | 0 | 1 | 0 | 0 | 0 | 0 | **5** |
| **W6 组合** | **2** | **1** | **2** | **2** | **1** | **2** | **2** | **1** | **2** | **2** | **17** |

### 4.2 决定性解释

- **W4 总分高但仍 PARK**：Q2/C5 只是条件通过；N=1 项目 postmortem 不能靠“六类失败很多”伪装成六个独立样本。
- **W6 排第一但不是无条件 GO**：其红线可以跨域，但数据包尚未达到论文级不可变性，统计结论尚缺不确定性检验和 calibration identification。
- **W2/W3 触发硬否决**：W2 的“过度自信”证据不足且首创性失败；W3 的核心 coverage 和 external validation 均未补齐。

---

## 5. 逐方向终裁、venue 与诚实上限

### W1：PARK

- **venue**：仅适合 evaluation/data-centric/forecasting workshop 或数据说明文；不建议独立冲 NeurIPS D&B。
- **条件**：若要重启，必须与 W2/W4 合并为 W6，而非继续堆数据字段。
- **诚实上限**：workshop 6–8 页，约 6.5–7.0 档；单纯 dataset paper 的 D&B 接受概率主观估计低于 10%。

### W2：PARK；吸收进 W6

- **venue**：独立时最多 sports analytics / forecasting / uncertainty evaluation workshop short paper。
- **重启条件**：至少完成配对 bootstrap、Brier 差置信区间、reliability diagram、ECE/ACE、最大概率 sharpness、按 H/D/A 的校准分解，并加入至少两个真正端到端 LLM 模型或一个同覆盖市场基线。
- **诚实上限**：当前 6.0–6.5；补齐后可到 workshop 6.5–7.0。不得以“overconfidence”作标题，除非分箱校准支持。

### W3：PARK；与 W6 平行，不升级

- **venue**：维持既有建议——EMNLP 2027 Eval workshop 4 页；Findings 仅在严格覆盖重算、真实 replay、外部 scenario 全部完成后尝试。
- **条件**：以 64.3% strict semantic coverage 重写；采用磁盘已有 ≥5 settlement records；清零 placeholder；补外部数据和独立 rater。
- **诚实上限**：沿用既有裁决的 ACL/EMNLP Findings 7.0–7.5，现实首选 workshop；不因世界杯新结果上调。

### W4：PARK（独立）；吸收到既有 C1 process-trace 主线

- **venue**：作为外部验证完成后的 failure-taxonomy paper，可考虑 NeurIPS D&B / agent evaluation / meta-science workshop；当前仅作 case section。
- **条件**：taxonomy 先冻结，盲应用到至少 5 个外部 live benchmark/forecasting 项目；≥2 raters，Cohen’s κ≥0.6；发布可观测签名和 stop/pivot 规则。
- **诚实上限**：当前 workshop 6.5–7.0；满足外部验证后才可能 7.0–7.5。它不应再新建一条 standalone portfolio，而应服务 2026-07-18 已 GO 的 C1。

### W5：KILL（独立）

- **venue**：无独立投稿建议。
- **处置**：在 W6 作为一个次级诊断图；最终 n=48 后同时报告冠军 log score `−log p(champion)`、冠军 prior rank、top-k mass，而不是只报 48 个 binary outcome 的平均 Brier。
- **诚实上限**：case note，不构成论文。

### W6：GO（附条件）

- **stretch venue**：NeurIPS 2027 Datasets & Benchmarks。
- **现实 venue**：ICML/NeurIPS 的 evaluation、data-centric ML、forecasting 类 workshop（以届时实际 CFP 为准）。
- **诚实上限**：若下述 gate 全过，D&B borderline（约 6.5–7.0；主观接受概率 10%–20%）；workshop 约 35%–50%。若缺外部复核或 immutable release，自动降级为 workshop/data note，不冲 D&B。该 D&B 估值显著低于 2026-07-18 C1 的 35%–45%，因为 W6 面临多个同届世界杯直接竞品、样本限于单赛事且 C5 仍为 CONDITIONAL；两者不是同一证据上限。

#### W6 八条硬 gate

| Gate | 必须完成 | 不过的后果 |
|---|---|---|
| G0 最终结算 | KO104 决赛后完成 championship n=48，保留冻结 prior | 数据集不完整，不能写 tournament-wide |
| G1 不可变发布 | 把 `88a9bfd` Elo、Coach、赛果、CDS、Plan C、commit IDs 和 SHA-256 manifest 复制到可发布 release；原仓库保持只读 | “ex-ante benchmark”不可信 |
| G2 缺失显式化 | 每个任务写 denominator/coverage；KO 30 场标 `not_preregistered`，不得事后回填 | 发生 hindsight contamination |
| G3 统计识别 | paired bootstrap/permutation、95% CI、reliability/ECE、按结果类别分解；只有通过后才允许“过度自信”措辞 | W2 只能写描述性反转 |
| G4 协议完整性 | 真实 prompt hash；schema 全量验证；0 行 judge 表要么补独立盲评并标 post-hoc，要么明确排除 judge claim | protocol 贡献失去可信度 |
| G5 基线公平 | market/Kimi 按覆盖分母报告；补同覆盖逐场市场基线，或明确缺失；禁止跨覆盖直接排序 | skill claim 不成立 |
| G6 来源隔离 | 对 Kimi→Elo bonus 做无 Kimi ablation，或把 Elo 明确标为 contaminated hybrid proxy | “统计 vs LLM”因果解释不成立 |
| G7 外部生存测试 | 至少用 WorldCupBench/另一 live benchmark 的公开 artifact 复核 protocol-failure taxonomy，证明不靠本项目独占数据 | C2/C7 失败，只剩数据独有赌博 |

**自动回退**：G0–G4 任一不过，W6 从 GO 降为 PARK；G7 不过，不得投 D&B，只保留 workshop case report。

---

## 6. 最优组合与 G3 的关系

### 6.1 “数据集为主线 + 校准发现为卖点”是否成立？

**成立，但需改成三件套，而不是两件套：**

> **数据集为载体 + accuracy–proper-score reversal 为实证卖点 + protocol-failure labels 为真正新颖点。**

若只有“数据集 + 校准发现”，会同时撞上 ForecastBench/Prophet Arena 和 ModelBall/WorldCupBench；加入协议失败标签后，论文才有一条删掉独占数据仍可存活的方法红线。

推荐贡献结构：

1. **Artifact**：不可变、可重算的双预测器 + 队伍级路径预测 + Plan C 因子结算数据包。
2. **Finding**：硬选准确率与 Brier/Log Loss 排名反转；Elo 的主胜/平局结构偏差。
3. **Method**：Protocol Integrity Vector，例如 `(ex_ante, immutable, source_clean, hash_valid, schema_valid, independently_adjudicated, baseline_coverage)`；预测分数与协议分数并列报告。
4. **Negative evidence**：KO 预注册缺失、snapshot drift、judge empty table 等失败不是被“修掉”，而是作为 benchmark 的审计标签发布。

### 6.2 对 G3 outline：吸收、并行还是废弃？

结论是：**方法零件吸收，论文主线并行，旧核心数字废弃。**

- **吸收**：Factor Ledger 的可结算结构、Green/Red source policy、schema validator、严格/宽松 crosswalk 区分，以及“总 Brier 不能解释失败在哪一层”的问题意识。
- **并行**：W6 研究的是 live forecasting benchmark 的协议完整性；G3 研究的是跨账本 schema reconciliation。二者强行合并会重演 2026-07-18 对 D4 的批评——integration 不等于 resolution，并会稀释 C1。
- **废弃/冻结**：旧 outline 中 92.9% forward coverage 和 n=2 “100% replay”不得再作主证据。真实 strict coverage 是 64.3%；n=2 仅能说明版本配对能复算，不能说明方法有效。
- **保留状态**：不删除 G3 outline，但取消“升级版主推”资格，维持 PARK；W6 完成后可把其 protocol-integrity vector 作为 G3 的外部应用候选，而不是反过来让 G3 驮着 W6。

### 6.3 与 2026-07-18 C1 process-trace 主线的关系

W4 的六类失败应直接并入已 GO 的“过程 trace + failure taxonomy + stop/pivot”主线，作为一个完整、时间戳明确、存在真实损失的案例。**不要为了 World Cup 再造第二篇 meta paper。** W6 发布事件级数据，C1 发布跨项目 failure taxonomy；二者可共享 annotation schema，但研究问题与投稿保持分离。

---

## 7. 立即行动项（按顺序）

### A0. “今晚补结算”——现应立即执行

按任务时点的原话，**“今晚补结算”**是第一优先级：KO104 决赛（2026-07-19，Spain vs Argentina）结束后，用冻结的 `cds_championship.json` prior 完成 championship **n=48** 全量结算。由于本次仓库复核已是 2026-07-20 且结果目录仍只有 7 月 18 日 n=46 partial settlement，此项已经逾期，应立即补做。

最少同时报告：

- 48 队 binary Brier（保持与前序报告可比）；
- 实际冠军的 `−log p(champion)`；
- 实际冠军 prior rank、两名决赛队 prior mass、top-5/top-10 title mass；
- 对 binary Brier 的类不平衡警告。

**边界**：本备忘录只登记行动，不修改 `cds4worldcup`。

### A1. 建不可变 release，而不是继续引用可漂移工作树

在允许写入的 `auto-research` 或独立 release 仓库中，复制并登记：

- `git show 88a9bfd:data/processed/odds.json`；
- Coach 形成/预测文件及生成时间；
- 赛果快照；
- CDS qualification/championship priors；
- Plan C cards/ledgers/settlements；
- 每个对象的 origin commit、生成时间、SHA-256、schema version。

不得在只读 `cds4worldcup` 中“清洗后覆盖原件”。

### A2. 先做统计识别，再决定标题是否出现 calibration/overconfidence

- 对共同 71 场做 Elo vs Coach paired bootstrap；另单报 Coach n=72。
- 给 Brier、Log Loss、accuracy delta 置信区间和 permutation p-value。
- 做 H/D/A reliability、ECE/ACE、最大概率分箱、sharpness。
- 若 Coach 显示低 sharpness 而非 overconfidence，标题必须保留“accuracy–Brier ranking reversal”，删除“overconfidence”。

### A3. 把失败变成 schema

新增公开数据字典，不回写源仓库：

- `ex_ante_status`：valid / invalid / unknown；
- `snapshot_status`：immutable / commit_recoverable / drifted；
- `source_integrity`：green_only / red_contaminated / mixed；
- `prompt_hash_status`：valid / placeholder；
- `schema_status`：pass / fail + violation IDs；
- `adjudication_status`：independent / same_author / absent；
- `baseline_coverage`：n/N；
- `preregistration_status`：executed / missed / post_hoc。

### A4. 做直接竞品 crosswalk

对 ForecastBench、Prophet Arena、WorldCupBench、worldcup-predictor-2026、ModelBall 至少比较：future-only、freeze、prompt equality、model count、market baseline、proper score、calibration、reason trace、source policy、schema validation、protocol-failure annotation。若没有一个维度由本项目独占，W6 自动 PARK。

### A5. 用外部 artifact 做一次盲审计

冻结 failure taxonomy 后，盲审 WorldCupBench 或另一公开 benchmark；由至少两名 rater 独立标注，计算 κ。目标不是挑别人错误，而是验证 taxonomy 在离开本项目后仍可操作。

### A6. 写作前 go/no-go

只有 G0–G7 全表完成后，才写完整 paper outline；在此之前只写 dataset card、analysis notebook 和 claim–evidence matrix。若外部生存测试失败，停止 D&B 叙事，改写为 workshop case report。

---

## 8. 诚实边界与禁用表述

### 8.1 可以说

- “我们发布一组具有真实赛后结算、可恢复事前版本和显式协议失败标签的世界杯预测 artifact。”
- “在本数据上，LLM-assisted Coach 混合预测器的硬选准确率更高，但 Elo+Poisson 的 Brier/Log Loss 更好。”
- “Elo 对主胜和平局存在方向稳定的结构偏差。”
- “协议完整性缺口会改变 benchmark 可解释性；它们应作为数据字段而非事后脚注。”

### 8.2 不可以说

- “首个世界杯/足球 LLM benchmark。”
- “首个 live、冻结、事前可结算 benchmark。”
- “首次发现 LLM 足球预测过度自信。”
- “Coach 是纯 LLM forecasting model。”
- “六个基线均完整覆盖。”
- “淘汰赛全赛程被事前预测。”
- “Plan C 全部 schema-compliant。”
- “multi-judge adjudication 已完成。”
- “冠军 n=46 partial Brier 证明模型整体校准良好/不良。”
- “G3 92.9% 覆盖率已被独立核验。”

### 8.3 最大诚实上限

在现有 72 场规模下，最强可辩护贡献不是预测性能 SOTA，而是**benchmark integrity audit**。即使 W6 所有 gate 通过，也不应声称普遍的 LLM forecasting 定律；结果限定为一个高审计密度的 single-tournament case。真正把上限推到 NeurIPS D&B，需要至少一个外部 benchmark 的复核、公开不可变 release、可重复的 protocol-integrity annotation，以及统计上可识别的校准结论。

---

## 9. 终裁后的组合路线图

| 时间 | 目标 | 退出条件 |
|---|---|---|
| 0–1 天 | n=48 结算、immutable manifest、缺失矩阵 | 无冠军最终结算或无法恢复事前快照 → PARK |
| 2–4 天 | paired statistics、reliability/ECE、source ablation | “过度自信”不可识别 → 改写为 ranking reversal，不影响 W6 |
| 3–7 天 | protocol-integrity schema + 外部 benchmark crosswalk | 红线与竞品无差异 → PARK |
| 1–2 周 | 外部 artifact 双人盲审、κ、dataset card | κ<0.6 或 taxonomy 不可迁移 → 只投 case workshop |
| 2–3 周 | W6 outline + claim–evidence matrix | 任一承重 claim 只有单证据 → 删除该 claim |

**最终优先级**：W6 gate work > W4 吸收到 C1 > G3 保持 PARK > W2/W5 不单独写。

---

## 10. 主要引用与查新链接

1. Dubitzky, W., Lopes, P., Davis, J., & Berrar, D. *The Open International Soccer Database for Machine Learning*. **Machine Learning** 108, 9–28 (2019). DOI: [10.1007/s10994-018-5726-0](https://doi.org/10.1007/s10994-018-5726-0).
2. Bunker, R., Yeung, C., & Fujii, K. *Machine Learning for Soccer Match Result Prediction*. arXiv:[2403.07669](https://arxiv.org/abs/2403.07669), 2024.
3. Halawi, D., Zhang, F., Yueh-Han, C., & Steinhardt, J. *Approaching Human-Level Forecasting with Language Models*. NeurIPS 2024. DOI: [10.52202/079017-1598](https://doi.org/10.52202/079017-1598).
4. Karger, E. et al. *ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities*. ICLR 2025. arXiv:[2409.19839](https://arxiv.org/abs/2409.19839).
5. Yang, Q. et al. *LLM-as-a-Prophet: Understanding Predictive Intelligence with Prophet Arena*. ICLR 2026 / arXiv:[2510.17638](https://arxiv.org/abs/2510.17638).
6. Hartvég, Á. et al. *Forecasting the FIFA World Cup 2026 with Large Language Models*. Preprints.org [202607.0719](https://www.preprints.org/manuscript/202607.0719), 2026. **预印本，非同行评审**。
7. AlDahoul, N., Abdul Karim, H., & Tan, M. J. *Predicting the Pitch or Repeating the Public?* SSRN. DOI: [10.2139/ssrn.6900538](https://doi.org/10.2139/ssrn.6900538). **预印本**。
8. Gibbins, G. *How can you improve the predictive power of LLMs in sports?* [ModelBall author-hosted working paper](https://modelball.ai/papers/improving-llm-predictions-2026-04-27.pdf), 2026. **未核见独立同行评审；只作 novelty threat，不作承重事实**。
9. [dckthulhu/WorldCupBench](https://github.com/dckthulhu/WorldCupBench), [willianpinho/worldcup-predictor-2026](https://github.com/willianpinho/worldcup-predictor-2026), [974103107/ai-world-cup](https://github.com/974103107/ai-world-cup). **公开工程 artifact，非同行评审论文**。
10. Rezaei, M., & Samadi, S. Y. *Predicting the 2026 FIFA World Cup with Sufficient Dimension Reduction of Elo Rating Histories*. arXiv:[2606.24171](https://arxiv.org/abs/2606.24171), 2026. **预印本**。

---

## 11. 最终裁决登记

- **GO（附条件）**：W6 审计型数据集 + proper-score 反转 + 协议失败标签。
- **PARK**：W1 纯 D&B、W2 校准短文、W3 G3 升级、W4 独立 meta 短文。
- **KILL（独立）**：W5 冠军概率过度分散短文。
- **最优组合**：数据集作主线、accuracy–proper-score reversal 作结果卖点、protocol-failure labels 作新颖性核心。
- **G3 关系**：吸收零件、论文并行、旧 92.9%/2-of-2 核心数字废弃；G3 outline 保留 PARK，不升级为主线。
- **立即行动首项**：KO104 决赛后“今晚补结算”——现已逾期，立即完成 championship n=48。
