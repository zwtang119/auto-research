# 审计链锚定的对账协议：2026 世界杯五份封存预测的可验证评估（工作稿）

> 状态：连贯工作稿 v0.1（2026-09-11）｜语言：中文；英文摘要附于文首  
> 题目（英）：*Audit-Chain-Anchored Reconciliation: A Protocol for Verifiable Multi-Forecaster Evaluation, Applied to Five Sealed Forecasts of the 2026 FIFA World Cup*  
> 本文件位置：`docs/plans/`（计划类产物）。**不覆盖**冻结开题/路线图正本。  
> 证据纪律：封存仓 `cds4worldcup` 零读写；`evidence/` 快照只读；本轮**未执行 G2 一键复算**、未运行会访问封存仓的脚本。文中数字转引自分析副本与分节草稿，每处给出源文件。进投稿前须以 bundle 复算替换。  
> 主语：协议。不作技能断言，不以命中冠军为证据，不报告投注或收益率。

---

## Abstract（English, working）

Evaluations of ex-ante forecasts often fail silently: snapshots drift, analysis protocols are chosen after outcomes are known, and supposedly independent sources leak into one another. We describe an **audit-chain-anchored reconciliation protocol** that treats **protocol integrity** as a first-class field alongside proper scores. Five components—content-addressed freezing, source tiering, uniform settlement, analysis-protocol freezing, and a Protocol Integrity Vector (PIV)—are applied to five sealed forecasts of the 2026 FIFA World Cup: an Elo–Poisson baseline, an LLM-assisted hybrid, a path-enumeration engine, a 300-agent LLM crowd (Red Source), and market prices.

Using numbers already recorded in the analysis replica (not recomputed in this drafting round), the audit’s descriptive yield includes: a path engine whose championship mass on eliminated teams is 93.5%; node win probabilities near one-half along a representative path; draw probabilities on the Elo baseline about 8.3 percentage points below the registered group-stage draw rate; and a frozen crowd prior that, on a 21-team renormalized pool, records lower multinomial Brier and log scores than selected market snapshots, while a FIFA-ranking proxy on the same pool is stronger still. A rule-based audit of 300 agent reasons finds 38 texts with factual error or exaggeration and identical wrong facts repeated across agents. We do not treat these as skill proofs. Limitations: single tournament; analysis protocol frozen after some results were known; PIV lacks external κ; **G2 one-command reproduction from the evidence bundle is not completed in this round.**

---

## 摘要（中文）

事前预测的同台评估很少在分数上响亮地失败，却常常在输入层沉默地失败：快照漂移、分析口径事后挑选、声明独立的来源互相渗漏。本文提出**审计链锚定对账协议**：把协议完整性与 proper score 并列为一等评估对象。五件套——git 内容寻址冻结、来源分级、统一结算、分析协议冻结、协议完整性向量（PIV）——应用于 2026 世界杯五份封存预测。

本工作稿的数字均来自既有分析副本与分节草稿，**本轮未做 G2 一键复算**。描述性产出包括：路径引擎将 93.5% 的夺冠概率质量分给未进决赛的队伍；代表性路径节点胜率接近 1/2；Elo 平局概率相对注册平局率约低估 8.3 个百分点；在 21 队同池重归一后，冻结的 LLM 群体先验在多项 Brier 与 log score 上低于若干市场快照，但 FIFA 排名代理更低。对 300 条分身理由的规则化分诊将 38 条标为含错误或夸大，并记录同值错误跨分身重复。这些结果用于展示协议能定位失败，**不构成预测技能证明**。局限见文末。

---

## 1. 引言

### 1.1 问题

比较几份“赛前预测”，表面上只需要冻结的预测、冻结的赛果和冻结的评分规则。2026 世界杯提供了一个可以把这三件事同时做完的窗口：赛程已结束，若干预测产物在开赛前被写入内容寻址的仓库，分析副本保存了结算与主张清单。

真正的困难不在评分公式。声称赛前的文件可能在赛后被管线重写；分析口径可能在看见结果后才定型；两条“独立”基线可能共享上游信号。这些失败不一定出现在 Brier 里。**分数完备不能代替协议完备。**

本文的对象因此不是“谁猜对了冠军”，而是：**异源、不同覆盖、不同冻结状态的预测，在何种协议下可以公平对账。** 主语是协议。

### 1.2 允许出现一次的命中叙述，以及为何它不是证据

分析副本记录：一份 300 分身 LLM 群体信号的冠军基线前五与一份市场快照的前五，均覆盖本届四强（西班牙、阿根廷、法国、英格兰）。FIFA 于 2025-11-25 公布本届抽签程序，史上首次采用网球式种子保护，前四种子分入不同半区、半决赛前不相遇。在这一制度下，重仓前四的名单“中四强”信息量被压低。市场快照对日期敏感（前五末席 0.19 个百分点即可换人）。**后文不以命中为证据。** 来源：`all-paper-claims-master-2026-07-26.md`（C1/C10）；`paper-a-skeleton-2026-07-25.md` §1。

### 1.3 贡献（与假设对应）

| 编号 | 贡献 | 假设 | 本工作稿中的证据地位 |
|---|---|---|---|
| C1 | 五件套 + PIV：协议完整性作为一等字段 | H5 | 方法定义已写；外部 κ 未测，PIV 仅内部应用候选 |
| C2 | 逐场层校准结构：命中与 proper score 可分离；平局偏差 | H1、H2 | 引用 72 场注册结算表；未经本轮 G2 |
| C3 | 路径引擎的 rank-vs-mass 分裂 | H3 | 描述性；93.5%、节点 0.5 化、5/32 |
| C4 | LLM 群体 vs 市场的描述对照，以及“是否独立信息”的未裁决悬念 | H4 | 描述层；FIFA 代理必须同台；悬念留给后续实验，本文不写结果 |

Paper B（群体规模 × 信息集）与 E1（共享错误探针）**未执行，本文不报告其结果。**

### 1.4 阅读路线

§2 相关工作与定位收窄；§3 协议；§4 数据与封存（含破口披露）；§5 结果；§6 讨论与局限；§7 数据可得性。数字凡未另注，均**未经 2026-09 本轮 G2 复算**。

---

## 2. 相关工作与定位

足球进球模型的平局低估与低分修正有 Dixon & Coles（1997）等文献；命中率与 proper score 可背离是 Murphy & Winkler（1977）已指出的现象。LLM 预测基准（ForecastBench、Prophet Arena、Foresight Arena 等）与 2026 年体育/事件向工作（LMU LLM-SoccerArena、WorldCupBench、WorldCupArena、WC2026-Agents）占据了 ex-ante 冻结、市场基线和部分 schema 校验。跨域的 WorldFork、SourceBench、ContractBench 分别占据溯源、来源分级、协议失败标注等维度。

2026-07-26 分析副本中的 W5 检索（PRISMA-lite，约 137 候选、38 项纳入 crosswalk）将“空白确认”否定，将贡献收窄为：**在体育预测评估中把六维整合成封闭的一等字段集；增量主要在来源分级与快照漂移监测，而非“首个世界杯 LLM benchmark”。** 该检索本身不是本轮系统复检；§2 的定位以该副本为准，投稿前须复核。Hartvég 等无法验证的条目不得列为占位威胁。来源：`all-paper-claims-master-2026-07-26.md` §8。

本文的 “reconciliation” 指**统一审计链下的对照阅卷**，不是 Hyndman 谱系里对预测值做层级一致性调整。

---

## 3. 协议

### 3.1 三种死法与一种伪装

1. **快照漂移。** 分析副本记录：`odds.json` 工作区相对赛前 commit，match 1 主胜 0.7629→0.7004；市场前五末席（阿根廷 vs 巴西）在相隔两天的快照间因 0.19pp 互换。取错版本时，下游统计无法自检。来源：`paper-a-s03-protocol-draft-2026-07-25.md`；`paper-a-s04-data-draft-2026-07-25.md`。
2. **分析协议缺位。** 夺冠文件在赛前有过归一化修正（`875748b`），头号热门改变。修正发生在赛前、动机可以正当，但说明“赛前预测”与“赛前方法”可被分别改写。
3. **来源渗漏。** 草稿登记 LLM 群体信号经 Elo bonus 渗入另一基线的情形，PIV 的 `source_integrity` 应标污染而非装作独立。
4. **仪式性更新。** 分析副本将 CDS 西班牙夺冠概率描述为全程约 0.0325–0.0331、日戳刷新而内容哈希不变（C12）。这不是“系统在学习”，而是时间戳在更新。来源：claims-master C12。

### 3.2 五件套

**(i) git 冻结。** 预测、赛果、代码以 commit 哈希寻址。哈希管内容；author date 可倒签，故时间必须另接审计链。

**(ii) 来源分级。** Green：可独立核验的事实（如已核验赛果）。Red：模型与聚合信号，不得作承重事实。Yellow：市场快照等，作描述参照并声明未做流动性调整。

**(iii) 统一结算。** 同一赛果版本、同一指标族、只在覆盖交集上比较，分母逐任务报告。

**(iv) 分析协议冻结。** 指标、比较族、判定规则冻结后不得再改。**本研究冻结发生在赛后，作者已见部分结果，故不用 pre-registered predictions 一词。**

**(v) PIV。** 八字段与预测分数并列：`ex_ante_status`、`snapshot_status`、`source_integrity`、`prompt_hash_status`、`schema_status`、`adjudication_status`、`baseline_coverage`、`preregistration_status`。无法判定则取最保守值（fail-loud）。外部盲标 κ≥0.6 未做，PIV 在本文仅为内部应用候选。字段表见 `paper-a-s03-protocol-draft-2026-07-25.md` §3.3。

### 3.3 审计链分层

- L1 自声明：git 日期。  
- L2 平台：分析副本记载 GitHub Actions 148 条、保留期曾设 400 天、部分 bot commit。  
- L3 第三方：Gmail 通知、Wayback 赛后存档、OTS/FreeTSA。赛前网页存档为阴性，须披露。  

时间主张必须标明层级。来源：`paper-a-s03` §3.4；`paper-a-s04` §4.2。封存破口（封存声明后仍有日度 bot 写入；原引用锚 `e8d74aa` 未推送，公开引用改为 `923e23a`）在 §4 披露，不在此复述为功绩。

---

## 4. 数据：五份封存预测

本轮不打开封存仓与 evidence 快照。版本号与覆盖以下表转引自 `paper-a-s04-data-draft-2026-07-25.md`，**待 G2 核对**。

| 代号 | 预测者 | 任务层 | 覆盖（草稿口径） | 版本锚（草稿） | 来源级 |
|---|---|---|---|---|---|
| P1 | Elo+Poisson | 逐场 W/D/L | 事前有效 n=71（match 1 无赛前快照） | `88a9bfd`；禁用赛后漂移工作区 | 模型 |
| P2 | Coach 混合（LLM 选阵 + 对位/MC/Poisson） | 逐场 | n=72 | `1c067ec` | 混合；非端到端 LLM |
| P3 | 路径枚举引擎 | 队伍夺冠/出线 | 48 队 | `ef30658` 与归一化 `875748b` **两版并列** | 模型 |
| P4 | 作者自建 300 分身群体 | 21 队夺冠 | 21/48，只比交集 | 首页自 `0ff58a7` 冻结；聚合层曾报 21/21 复算 | **Red Source** |
| P5 | 市场价格 | 队伍 outright | 注册快照约 39 队；另有 77 个日度快照 | 注册基线 2026-06-11 | Yellow；收盘价，未做流动性调整 |

**P4 谱系（必须与官方活动分开）。** 2026-08-02 分析副本判定：该 300 分身来自作者项目 `worldcup_ui_upgrade`（生成时间戳 2026-06-05），不是 Moonshot 官方 Token Goal 活动。官方活动另有架构与另一头版结论，不得混引。底座版本无生成日志字段；同日 memo 后文将用户初报的 K2.7 更正为 K2.6（发布时间线排除法），**仍为间接证据级**。来源：`kimi-lineage-verification-2026-08-02.md`。

**封存结构与破口。** 纪律为：封存仓 → 只读快照 → 可写分析副本，单向。已披露：封存声明后日度工作流仍写入；引用锚更正为 `923e23a`。2026-07-25 后的 branch protection 等服务端强制，见 s04 §4.2；本轮未核验平台当前设置。

已知瑕疵 R1–R6（match 1、odds 漂移、无淘汰赛逐场预注册、qualification 字段、ledger 4/104、市场 0.19pp）见 s04 §4.3，映射为 PIV，不在结果章假装不存在。

逐场层基线在草稿中为均匀、永远主胜、FIFA 排名代理；市场不进入逐场层。队伍层市场进入对照。

---

## 5. 结果

**读法：** §5.1–5.3 为已落盘数字的转述与口径澄清；§5.4 为 PIV 读法；§5.5 因子账本仅作覆盖率警告。未经 G2 的数字不得升格为“本文复算确认”。

### 5.1 逐场层：硬选与概率质量（H1/H2）

注册结算报告（`cds4worldcup/results/2026-07-08-group-stage-72-match-evaluation.md`，本轮未重跑）记载：

| 方法 | 评估样本 | 硬选准确率 | Brier（↓） | Log Loss（↓） |
|---|---:|---:|---:|---:|
| Elo+Poisson | 71 场事前 | 54.9% | 0.5728 | 0.9410 |
| Coach 混合 | 72 场 | 59.7% | 0.6078 | 1.0113 |

样本不完全相同，**不得仅凭此表宣称统计显著优劣。** 硬选只看最高概率项；Brier/Log Loss 评价整组概率。Coach 硬选更高、Brier 更差，与 Murphy–Winkler 已知现象同向，**不作新理论标题**（claims-master 将 C7 评为插图级）。

Elo 平均平局概率 0.1943，相对该报告中的实际平局率 27.8%，约 −8.3 个百分点；MD1 单轮另有 −17.6pp 的口径。两数并存于源文件，**不是互相证伪，论文必须标明口径**（C8）。这为 Poisson 独立性偏差提供诊断素材，不是本轮因果识别。

分析副本另记 FIFA 排名 chalk 在 72 场硬选 58.3%（42/72），永远主胜 47.2%，均匀 33.3%。来源：`random-vs-fifa-baselines-2026-07-29.md`。该 memo 同时给出夺冠层 FIFA 代理多项 Brier 0.563、log 1.267，优于 kimi 与市场的同池数字。**任何“群体赢市场”的句子必须带“未赢 FIFA 代理、粉笔年+种子保护”限定。** FIFA 代理的概率映射是否严格事前冻结，本轮未核，作补充基线而非官方发布概率。

### 5.2 队伍层：路径编码正确与概率分配失败（H3）

`paper-a-s05-2-team-level-draft-2026-07-27.md` 转述：n=46 出局结算下，出局队承载赛前夺冠质量 **93.5%**，决赛两队合计 6.5%。均匀每队 1/48 时出局 46 队承载 95.8%。机制解剖：塞内加尔五节点条件胜率均在约 0.48–0.52；归一化把 #15（0.0335）变为 #1（0.0435）而路径概率未改；R32 预测对手为捷克、实际为比利时。bracket 核验称半决赛对阵在路径结构中可达，但 R32 对手命中 5/32（15.6%）。来源：s05-2；`bracket-encoding-verification-2026-07-26.md`。

**失败定位在节点概率，不在“路径枚举方法全体无效”。** 同一草稿称出线任务 Brier 0.2392、低于 0.25 基准（源 `ca0e3ff`），即低难度任务与高难度任务不可混为一谈。两版夺冠文件并列披露，论文不挑选“引擎的预测”。

**均匀 Brier 口径（必须改正读法）。** s05-2 写 n=48 Brier 0.0195/0.0200，并称均匀基线 0.02083。0.02083 等于 1/48，是把**均匀概率误写成均匀 Brier**。若采用该草稿写出的  
`[Σ₄₆ pᵢ² + (1−p_Spain)² + p_Argentina²] / 48`  
且均匀 pᵢ=1/48，则均匀值应为 **47/2304≈0.02040**，不是 0.02083。在未做 G2 重算前，**不以“统计上等同均匀噪声”或“仅勉强优于均匀”为承重句**；只保留 93.5% 质量分布与节点 0.5 化的机制描述。CDS 三版本 0.0195–0.0200 仍视为草稿报告值。

### 5.3 LLM 群体与市场：描述对照，不是技能竞赛（H4）

对照设计（s05-3）：P4 自某一 commit 起字节冻结；P5 为日度快照。比较在 21 队交集、同池重归一上进行。

草稿报告（**待 G2**）：

| 指标（↓） | kimi 冻结 | 市场 | 备注 |
|---|---:|---:|---|
| 冠军 log | 1.435 | 1.746（6-13 快照） | 单点 |
| 时间积分 log | 1.435 | 1.744 | 38 日快照均值；**不是 38 次独立赛事** |
| 同池多项 Brier | 0.688 | 0.753 | 21 队向量 |

对照：草稿中 CDS 多项 Brier 0.930、均匀 0.952。市场轨迹描述（法国时代、半决赛双热门判断错误、佛得角后西班牙价格下跌）见 s05-3，属 n=1 微观结构叙述，须声明未做流动性调整。

成对排序、ceiling 变换、偏离 5/1/2、派别 8/9 与 9/9 均为描述层，全表才能报，禁止只报“猜对的两条”。**H4-ii（表型多样是否等于信息独立）本文不裁决**，作为后续受控实验的问题，不把未跑的 Paper B 当结果。

FIFA 代理在同池 proper score 上更低（§5.1）。完整梯队读法应是：**FIFA 代理（该 memo）< kimi < 市场 < CDS < 均匀**（Brier/log 两套数字见 `random-vs-fifa-baselines-2026-07-29.md`）。不得写“kimi 是本届最佳信号”。

### 5.4 理由审计：共享错误的描述证据

`reason-audit-full300-2026-07-29.md`：规则化分诊 300 条——事实基本成立 99（33.0%），含错误或夸大 38（12.7%），氛围/不可核验 163（54.3%）。同值错误重复：身价张冠李戴 ×9、摩洛哥排名 ×8、不败月数 ×6。押出局队的分身错误率高于押部分四强队伍的分身，但 4% 比较组**不是全部四强**，本文不采用“六倍”作标题。

这是规则匹配下界，不是双人盲标，不是通用幻觉率。它支持把“人设多样”写成**待检验的独立性假设**，而不是已证明的群体智慧。

### 5.5 PIV 与因子账本

五预测者 × 八字段全表在 s03 中仍为定义，实际取值表待与 G2/PIV 标注一并填写。本工作稿只要求读者用二维读法：分数优但 `snapshot_status=drifted` 或 `source_integrity=red_contaminated` 的对象，不得在协议下被读成单轴第一。

因子账本覆盖 4/104、状态不一致（s04 R5），**n=4 不得外推**。

---

## 6. 讨论

协议的用处首先是**给失败命名**：漂移、仪式性更新、节点无观点却被归一化加冕、覆盖子集被说成全量、命中率掩盖校准失败。这些失败模式是诊断力的证据，不是项目耻辱，也不是“路径枚举无用”或“LLM 不能预测”的一般定律。

可迁移的问题是 evidence → 冻结 → 结算 → 完整性字段，而不是世界杯本身。保险、医学、法律评估若缺少这套字段，同样会得到漂亮分数和不可复核的输入。本文不声称已经完成跨域验证。

结构性边界（保留）：单届 n=1；逐场 n=72 只能识别大效应；市场为不对称强基线且流动性未调整；kimi 生成层版本间接；分析协议赛后冻结；G2 未过；PIV 无外部 κ。种子保护使前四相关命中贬值。官方同期另一套 300 分身系统（不同架构、不同头版）说明“300”这个数字本身不是能力保证。

---

## 7. 数据可得性与本工作稿边界

引用锚按分析草稿为 `923e23a`（赛程冻结口径）。Zenodo DOI 未在本轮确认。复现入口在计划中指向 git bundle、校验和与时间戳收据；**本轮不提供、不执行一键复算。** 赛前第三方网页存档为阴性披露。

任何人引用本稿数字，应同时引用对应分析文件，并注明 **2026-09-11 工作稿 / 非 G2 定稿**。

---

## 8. 结论

我们把 2026 世界杯五份封存预测写成一次**评估协议的压力测试**，而不是一次预测比赛。在现有分析副本上，协议能够指出：逐场命中与概率质量可以分开；路径结构正确可以与夺冠质量分配失败并存；冻结先验可以在描述性 proper score 上优于部分市场快照，却仍弱于简单的 FIFA 代理；人设群体可以共享同一错误事实。

这些观察支撑继续把协议完整性当作一等对象。它们不支撑“机器集体智慧已证实或已证伪”，也不支撑“本工作预测了冠军”。完整 G2、PIV 外部测试与前瞻群体实验是后续任务，不是本稿的结果。

---

## 附录 A　数字来源与本轮状态

| 数字/主张 | 来源文件 | 本轮 |
|---|---|---|
| Elo 54.9% / 0.5728 / 0.9410，n=71；Coach 59.7% / 0.6078 / 1.0113，n=72；平局 −8.3pp | `cds4worldcup/results/2026-07-08-group-stage-72-match-evaluation.md`（只引用路径，未打开封存仓复算） | 未 G2 |
| 93.5%；塞内加尔节点；0.0195/0.0200；出线 0.2392 | `paper-a-s05-2-team-level-draft-2026-07-27.md` | 未 G2；均匀 0.02083 **不采用** |
| 21 队 Brier/log/时间积分；5/1/2 | `paper-a-s05-3-kimi-vs-market-draft-2026-07-27.md` | 未 G2 |
| FIFA 58.3%；同池 0.563 / 1.267 | `analysis/worldcup-2026/random-vs-fifa-baselines-2026-07-29.md` | 未 G2 |
| 99/38/163；×9/×8/×6 | `reason-audit-full300-2026-07-29.md` | 规则分诊，非盲标 |
| 谱系非官方活动 | `kimi-lineage-verification-2026-08-02.md` | 间接版本 |
| 0.7629→0.7004；0.19pp | s03/s04 | 草稿已核验口径，未本轮复算 |
| 5/32 | bracket memo / s05-2 | 未 G2 |
| C12 平线 0.0325–0.0331 | claims-master | 未 G2 |
| 148 Actions；Wayback；OTS | s04 / 进度 2026-07-26 | 未本轮核验平台 |

## 附录 B　禁止措辞（校核用）

不得使用：首个世界杯 LLM benchmark；pre-registered predictions；我们预测中了冠军/四强（结果章）；kimi 证明了；kimi 是最佳信号；统计上等同均匀（在 0.02083 口径下）；幻觉率 13%；六倍错误率（未定义的四强全集）；收益率、投注建议；把官方 Token Goal 当作本文数据。

允许：协议、审计链、描述性对照、Red Source、待 G2、待后续实验。

---

## 写作备注（不入对外正文）

- 本文件由 2026-09-11 将 skeleton、s03、s04、s05-2、s05-3、摘要稿、claims-master、理由审计、谱系 memo、FIFA memo 收束而成。  
- 未改 evidence、未跑 fig6 脚本、未 commit。  
- 表 1 PIV 取值、图 1–6 仍缺，校核包只交文字稿。  
