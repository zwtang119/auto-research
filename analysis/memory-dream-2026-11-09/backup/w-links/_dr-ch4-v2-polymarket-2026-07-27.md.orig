# 第 4 章 Polymarket 定价机制：供需动态 vs 人为设定，及与算法的系统性差异发表价值

> **来源分级（依 AGENTS.md）**：【Green】= 冻结数据／已结算／官方文档；【Red】= 模型输出（须注明冻结版本）。本章不含投注建议，不报告收益率。

## 论点

Polymarket 的赛事冠军概率并非由平台或庄家人为设定的赔率，而是由链上连续限价订单簿（CLOB）中买卖双方的真实资金供需动态"涌现"出的价格信号，经 UMA 乐观预言机结算【Green】。将 kimi（算法预测）与此市场化基线在 2026 世界杯单届样本上做时点对照，可以支撑"描述性领先"的发表价值，但"系统性差异成立"只能作为待检假设而非定论。本节纠正一种常见误读：kimi 并非"全程高于市场"，而是在 7-18 前领先、于 7-18/19 被市场反超【Red＋Green】。

## 论据

**4.1 机制：链上 CLOB + UMA 乐观预言机**

Polymarket 的底座是基于 Polygon 的链上抵押与结算系统，采用连续限价订单簿（CLOB）而非自动做市商（AMM）定价（[从 AMM 到订单簿：探索 Polymarket 定价机制的转变](https://news.qq.com/rain/a/20250731A04LAA00)）【Green】。其核心是一组不可动摇的价值等式：任何人可存入 $1 USDC 铸造 1 份 YES 与 1 份 NO 份额，且恒有"1 YES + 1 NO = $1"；YES/NO 作为独立资产在各自订单簿与 USDC 交易，协议层不设价格上限，价格完全由挂单互动涌现（[同上](https://news.qq.com/rain/a/20250731A04LAA00)）【Green】。当 P(YES)+P(NO) 偏离 $1 时，套利者通过"铸造-卖出"或"买入-赎回"将其拉回，市场自身的逐利行为成为价格稳定的决定力量（[同上](https://news.qq.com/rain/a/20250731A04LAA00)）【Green】。

与传统博彩的根本区别在于"无庄家"：平台本身不参与对赌、不设定赔率——正如其官网所陈述，"就像股票交易所不会设定股票价格一样，Polymarket 也不会设定价格或赔率，它们完全由供需关系决定"（[稳定币点燃预测市场？](https://www.163.com/dy/article/K34NPMG30552956F.html)）【Green】。结果裁决交由 UMA 乐观预言机（Optimistic Oracle）：CTF 适配器在市场创建时生成问题并向 OO 发送请求，提议者在挑战期内若无争议即视为正确，否则进入 UMA 代币持有人的 DVM 仲裁（[Polymarket 与预测市场的去中心化困境](https://www.sohu.com/a/784453679_121948394)）【Green】。UMA 官方文档进一步确认，OO 以"先假定正确、后争议验证"运作，目前约 99.8% 的请求在挑战期内无争议快速结算，少数争议交由 DVM 以 24 小时提交／24 小时揭示的秘密投票、65% 多数决解决（[How does UMA work?](https://docs.uma.xyz/protocol-overview/how-does-uma-work)）【Green】。

**4.2 kimi 与市场的概率时点对照（纠正"全程高于"）**

在 2026 世界杯冠军 outright 市场上，kimi 的冻结估计值为 23.82%（快照日 6-11，模型输出，冻结版本 kimi-6-11）【Red】；而 Polymarket 市场在该时点之前的每一个读数都低于这一数值，直到 7-18 市场价才跳升至 59.05%（已结算历史快照）【Green】。因此准确的时序表述是：kimi 的冻结估计在 7-18 之前始终高于市场任何时点，但 7-18/19 市场读数反超了 kimi 的冻结值（[冻结备忘录 faction-lmu-polymarket-2026-07-26](analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md)）【Red＋Green】。这纠正了"kimi 全程高于市场"的绝对化表述——领先是时段性的、描述性的，而非贯穿全周期。

**4.3 n=1 描述性领先的发表价值**

尽管仅是单届世界杯（n=1）的描述性观察，这一领先仍具发表价值：它是首次在"六维整合闭集预测域"中，将算法预测与异质预测者（Elo／混合／路径空间／LLM 群体／市场）同台审计的尝试（[冻结备忘录](analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md)）【Green】。学术文献一贯强调 ex-ante 时态与协议完整性的价值（[Prediction market 文献综述](https://datafield.dev/learning-prediction-markets/part-01/chapter-02/further-reading.html) 引 Wolfers & Zitzewitz 2004、Arrow et al. 2008）【Green】。但单届样本的结构性限制明确：描述性领先不能外推为跨赛事的稳健优势。

**4.4 "系统性差异成立"保留为待检假设**

"kimi 与市场存在系统性差异"是一个待检假设，而非已证实的结论。要将其升级为定论，需要跨多届赛事、跨多个预测市场（Polymarket 之外的 Kalshi、传统博彩等）的复现证据（[冻结备忘录](analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md)）【Green】。在缺乏此类复现前，正文应明确以"假设"而非"定论"呈现，避免发表性偏差。

**4.5 有偏但可用的市场化基线**

市场作为基线并非无偏神谕。学术与机制层面均记录其偏差：Bürgi 等（2025）在分析逾 30 万份 Kalshi 合约时发现显著的 favorite-longshot bias（[The economics of the Kalshi prediction market](https://cepr.org/voxeu/columns/economics-kalshi-prediction-market)）【Green】；理论文献指出，预测市场价格一般不等于概率均值，而是受风险偏好与异质信念影响的边际价格（[Prediction market prices under risk aversion](https://www.sciencedirect.com/science/article/abs/pii/S0304406817300484) 引 Manski 2006）【Green】。本赛事亦有 recency／流动性偏误的实例（如佛得角相关市场 −7pp 的过调，及冠军 outright 市场单笔七位数级别的实质深度证明非幽灵盘）（[冻结备忘录](analysis/worldcup-2026/faction-lmu-polymarket-2026-07-26.md)）【Green】。结论：市场是有偏但可用的信念读数——可作基准，不可当神谕。

## 分析

机制层面的关键启示是：Polymarket 价格由边际交易者用真金白银挂单形成，是"边际价格"而非"群体均值"，深钱包的意见天然权重更大（[预测市场：原理、现状与展望](https://fddi.fudan.edu.cn/_t2515/dc/dc/c21253a777436/page.htm)）【Green】。这解释了为何 kimi 的算法估计能在特定时段领先于一个被流动性与 recency 偏误扭曲的市场——领先反映的是"信息差异"而非"算法必胜"。将时点对照升级为"系统性差异"前，必须排除训练语料回声、单一市场结构等替代解释，这正是跨届／跨市场复现臂的设计目的。

## 小结

Polymarket 的冠军概率由链上 CLOB 的供需动态涌现、UMA 乐观预言机结算，零人为设定赔率【Green】。kimi 的冻结估计（23.82%, 6-11）在 7-18 前领先于市场，但 7-18/19 被市场反超，故"领先"须表述为时段性、描述性【Red＋Green】。n=1 描述性领先具备发表价值（首次六维整合闭集预测域），但单届样本限制外推；"系统性差异成立"应保留为待检假设，待跨届／跨市场复现方可升级【Green】。市场是有偏但可用的基线，适合作为算法预测的对照基准而非真理标准。

---

## 本章新增来源

1. [从 AMM 到订单簿：探索 Polymarket 定价机制的转变](https://news.qq.com/rain/a/20250731A04LAA00) — 详解 Polymarket CLOB 机制：YES/NO 份额 $1 锚定、铸造/赎回、套利修正使价格向 $1 收敛（Green，机制文档）
2. [Polymarket 与预测市场的去中心化困境](https://www.sohu.com/a/784453679_121948394) — UMA 乐观预言机集成：CTF 适配器、挑战期、DVM 仲裁流程（Green，机制文档）
3. [How does UMA work?（UMA 官方文档）](https://docs.uma.xyz/protocol-overview/how-does-uma-work) — OO "先假定正确后争议验证"，~99.8% 无争议快速结算，DVM 24h/24h 秘密投票、65% 多数决（Green，官方）
4. [稳定币点燃预测市场？Polymarket 和 Kalshi 完成新一轮融资](https://www.163.com/dy/article/K34NPMG30552956F.html) — 引 Polymarket 官网声明"不设定价格或赔率，完全由供需决定"；对比传统庄家（Green，媒体报道）
5. [The economics of the Kalshi prediction market（CEPR VoxEU）](https://cepr.org/voxeu/columns/economics-kalshi-prediction-market) — Bürgi 等（2025）基于逾 30 万份 Kalshi 合约证实 favorite-longshot bias（Green，学术）
6. [Prediction market prices under risk aversion and heterogeneous beliefs（ScienceDirect）](https://www.sciencedirect.com/science/article/abs/pii/S0304406817300484) — 理论证明价格=边际信念而非群体均值，给出 favorite-longshot bias 的理性解释（Green，学术期刊）
7. [金融学术前沿丨预测市场：原理、现状与展望（复旦 FDDI）](https://fddi.fudan.edu.cn/_t2515/dc/dc/c21253a777436/page.htm) — 预测市场理论框架（Hayek/Aumann/Arrow）与偏差综述（Green，学术机构）
8. [Prediction market 文献综述与书单（datafield.dev）](https://datafield.dev/learning-prediction-markets/part-01/chapter-02/further-reading.html) — 收录 Wolfers & Zitzewitz 2004、Manski 2006、Arrow et al. 2008 等核心文献出处（Green，学术）
