# Paper A 摘要与引言（创新拉满版 v0.1，2026-07-29）

> 定位：表述策略修订——创新点打头阵用陈述句，限定词集中收编 limitations（§6.4），不再句句消毒 ｜ claim type 不变（方法/描述），altitude 拉满
> 纪律底线（不可谈判）：不作技能断言、不作"预测了冠军/四强"主 claim、FIFA 对照进 limitations

---

## 0. 题目候选（拉满向）

**A（主推）**：*Audited Forecasts: How a Sealed 2026 World Cup Dataset Caught Drift, Leakage, Ceremonial Updates, and Shared Hallucinations — and the Protocol That Catches Them*
（被审计的预测：一份封存的 2026 世界杯数据集如何抓获漂移、渗漏、仪式性更新与共享幻觉——以及能抓获它们的协议）

**B（备用）**：*The Audit Is the Method: Protocol Integrity as a First-Class Metric in Multi-Forecaster Evaluation*

## 1. Abstract（英文版，~230 词）

> Evaluations of ex-ante forecasts rarely fail loudly. They fail silently — through drifted snapshots, post-hoc protocols, contaminated sources, and ceremonial maintenance that updates timestamps without updating content. We introduce the **audit-chain-anchored reconciliation protocol**, the first closed set in sports forecasting that scores **protocol integrity** as a first-class field alongside predictive accuracy: eight Protocol Integrity Vector (PIV) fields covering ex-ante status, snapshot versioning, source integrity, schema validity, adjudication independence, and — new in this work — **ceremonial-update detection**.
>
> We apply the protocol to five sealed forecasters of the 2026 FIFA World Cup (Elo+Poisson, an LLM-assisted hybrid, a path-enumeration engine, a 300-agent LLM crowd, and market prices), all content-addressed and third-party timestamped. The audit's empirical yield: a path-enumeration engine whose championship distribution is statistically indistinguishable from uniform noise (93.5% of mass on eliminated teams) despite correct bracket encoding — a failure we formalize as **accuracy decay ε^depth**; a frozen LLM-crowd prior that beat dynamic market prices on all three proper-score comparisons while 13% of its agents' stated reasons contained factual errors — including **identical hallucinations**, the same wrong fact replicated verbatim across "independent" agents, falsifying error-independence assumptions at the fact level; and a systematic draw-underestimation signature consistent with Poisson independence. We release the full evidence chain — git bundle, 148 server-side workflow records, mail-server timestamps, web archives, and RFC 3161/blockchain anchors — making every number in this paper independently checkable.

## 2. Abstract（中文工作版）

> 事前预测的评估很少"响亮地失败"——它们在沉默中死去：快照漂移、事后协议、来源渗漏，以及只更新时间戳不更新内容的**仪式性维护**。我们提出**审计链锚定对账协议**（audit-chain-anchored reconciliation protocol）：体育预测域首个把**协议完整性**作为与预测分数并列的一等评估字段的闭集——PIV 八字段覆盖事前状态、快照版本、来源完整、schema 有效、结算独立，以及本工作新增的**仪式性更新检测**。
>
> 我们将协议应用于 2026 世界杯五份封存预测（Elo+Poisson、LLM 辅助混合、路径枚举引擎、300 分身 LLM 群体、市场价格），全部内容寻址且第三方时间戳固定。审计的实证产出：一个夺冠分布与均匀噪声统计不可分（93.5% 质量压出局队）但 bracket 编码正确的路径枚举引擎——其失败被形式化为**ε^深度衰减律**；一个在全部三项 proper score 对照上击败动态市场的冻结 LLM 群体先验——而其分身 13% 的理由含事实错误，包括**共享幻觉**（同一条错误事实在"独立"分身间逐字复现，在事实层证伪误差独立假设）；以及与 Poisson 独立性一致的系统性平局低估签名。我们公开完整证据链——git bundle、148 条服务端工作流记录、邮件服务器时间戳、网页存档、RFC 3161 与区块链锚——使本文每个数字都可被独立复算。

## 3. 引言 Pitch（六段，含关键句）

**P1 会撒谎的记分牌**。开篇给数字（拉满）："2026 年 7 月 19 日决赛终场，一个冻结了 36 天的 300 分身 LLM 群体信号在冠军 log score（1.44 vs 1.75）、多项 Brier（0.69 vs 0.75）、时间积分 log（1.44 vs 1.74）三项指标上全部优于 Polymarket 的连续定价——而 market 在半决赛当天对两场比赛的热门判断全部错误。"然后转折："本文的主题不是这个命中，而是：**如果没有审计协议，我们永远无法确认它是不是又一个幸存者故事。**"

**P2 三种死法与一种伪装**。快照漂移（odds.json 主胜 0.7629→0.7004、市场前五末席 0.19pp 互换）、预注册缺位（归一化修正改变头号热门）、来源渗漏（Elo bonus 渗入）、以及第四种——**仪式性维护**（CDS 日更线 37 天平坦：时间戳每日刷新、内容哈希纹丝不动）。"分数的完备性不能替代协议的完备性。"

**P3 协议**。五件套 + PIV 八字段 + 审计链三级（git 内容寻址 / 平台服务端记录 / 第三方时间戳）。"本文把协议完整性从合规清单升格为与预测分数并列的一等评估字段——体育预测域首个六维闭集（经系统文献检索验证，B/C 为实测增量）。"

**P4 审计找到了什么**（实证丰收，六连发）：① 与均匀噪声不可分的夺冠分布（93.5% 错配）及其机制——**ε^深度衰减律**（出线合格、夺冠崩盘，同引擎同参数）；② **共享幻觉**（"哈兰德 2.33 亿欧"×9、"摩洛哥 FIFA 第 7"×8、"24 个月不败"×6——它们连错都错得一模一样）；③ 理由审计显示理由质量与结论正确性脱钩（押出局队的分身错误率是押四强的 6 倍）；④ 平局低估签名；⑤ 冻结先验三口径赢市场的完整案例（含市场"法国时代"24 天错价）；⑥ 仪式性日更的首个机器可检实例。

**P5 一切可查**。"本文没有一句话需要读者信任作者。"证据链五层（git/Actions 148 条/Gmail 6 月邮件/Wayback/OTS+TSA），全部数字可由 bundle 一键复算（G2 闸门）。

**P6 路线图**。§2 文献（W5 crosswalk 与 LMU 划界）→ §3 协议 → §4 数据与封存 → §5 结果（逐场/队伍/市场对照/PIV 标注）→ §6 讨论（含 limitations 集中收编）→ §7 数据可得性。

## 4. Limitations 集中收编（§6.4，唯一住所）

n=1 单届；n=72 逐场推断力上限（只能识别大效应）；FIFA 官方排名在本届为更强单一信号（0.563/1.267，粉笔年+种子保护语境）；OSF 冻结为赛后（作者已见部分结果）；kimi 属 Red Source；市场读数未做逐日流动性调整；PIV 外部生存测试（κ）未过前仅内部应用。

---

## 写作备注

- 与既有骨架的关系：本稿只改表述海拔，不改任何 claim type；骨架 §5 措辞禁忌全部保持（禁句未动）。
- "六连发"每条都有分析副本 memo 注脚；G2 复算后数字逐一对齐。
- English abstract 为工作稿，投稿前需母语级润色。
