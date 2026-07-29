# 第 3 章 佛得角之夜的市场情绪——量化评估准确性与前瞻指引

## 论点

本章核心论点：2026 世界杯期间，Polymarket 对西班牙夺冠概率的轨迹呈现显著 recency（近因）过调——价格剧烈波动反映对单场赛果的情绪性反应，而非信息质量的同步提升；相较之下，kimi 模型自 6 月 11 日起冻结于 23.82% 的常数信号，全程反而更稳定、校准更优【Red：kimi 冻结版 6-11】。由此导出：动态并不天然优于静态，更新频率与信息质量是两个独立维度。市场在本届更多扮演结果驱动的事后跟随者，而非可依赖的事前指引信号。

## 论据

### 3.1 市场轨迹完整呈现

依据已结算的 Polymarket 西班牙夺冠概率日频快照【Green：77 个 market_public_snapshot.json 日版】，全轨迹为：16.95%（6-12）→ 16.55%（6-14）→ 13.65%（6-21，佛得角 0-0 后失榜首）→ 10.55%（6-28）→ **10.05%（7-01，谷底）** → 18.25%（7-07）→ **21.15%（7-14）** → 59.05%（7-18/19）→ 100%（结算）。

关键节点 7-14（21.15%）必须保留：当日为半决赛日，市场却对两场半决赛热门全判错——法国 39.0% > 西班牙 21.1%（实际西班牙 2–0 胜），英格兰 21.8% > 阿根廷 17.4%（实际阿根廷 2–1 胜）。市场自 6-21 将头号热门换为法国、峰值 39.0%@7-14，是一次持续约 24 天的错误定价，半决赛终了才被纠正【Green】。

### 3.2 八场赛制澄清

锁定事实底座确认：西班牙实际赛制为 8 场、7 胜 1 平【Green：已结算赛程】。需澄清表面矛盾——"0-0 逼平"与"7 胜"并不冲突：该 0-0 平局发生于小组赛对阵佛得角（6-21），正是触发市场跌至谷底的那场；"7 胜"指小组赛之后连胜的 7 场（4-0 / 1-0 / 3-0 / 1-0 / 2-1 / 2-0 / 1-0，含淘汰赛至决赛）。故西班牙为"1 平 + 7 胜"、全程未尝败绩的冠军，而非"7 战全胜"。谷底价 10.05% 对应的恰是一支实际未输球的冠军队。

### 3.3 kimi 冻结信号与量化校准对照

kimi 自 6-11 起冻结于 23.82%【Red：kimi 冻结版 6-11】，全程高于市场任何时点（除决赛日外）。基于已结算结果计算的评分【Green：n=48 夺冠结算与同池多项 Brier】，均采用"越低越好"约定：

- 冠军 log score（−ln p_Spain）：kimi 1.44 < 市场 1.78（即市场 1.78 > kimi 1.44），kimi 更优；该市场值取自 6-13 单点快照（16.85%），非全程轨迹。
- 同池多项 Brier（21 队概率向量重归一）：kimi 0.688 < 市场 0.753 < CDS 0.930 < 均匀基线 0.952，kimi 校准更优。
- 时间积分 log score（−ln p 逐日均值，6-12→7-19，n=38 个市场快照）：市场 1.744 vs kimi 常数 1.435，冻结信号在时间维积分下仍占优。

### 3.4 预测市场行为文献支撑

预测市场并非恒有效。Croxson 与 Reade（2018）指出，交易者对价格变动的"过度反应"（over-reaction to price movements）与从众（herding）会驱动价格偏离真实信息，形成可检测的系统偏差 ([Improving prediction market forecasts…](https://www.sciencedirect.com/science/article/abs/pii/S0377221718305575))。Snowberg 与 Wolfers（2010）以前景理论证明，favorite–longshot 偏差主要源于对概率的"误感知"而非风险偏好 ([Explaining the Favorite-Longshot Bias](https://authors.library.caltech.edu/31703/))，为近因过调提供行为机制。Angelini 与 De Angelis（2026）在实时预测市场中发现，价格对公共信息"方向正确但不完全"——基准概率一分钟变化仅对应约 0.64 倍的市场同步变化，剩余偏差预示后续可预测漂移 ([When Do Markets Fully Process Public Information?](https://www.arxiv.org/abs/2606.07811))。Wolfers 与 Zitzewitz（2004）则给出反方基座：预测市场通常能较好聚合分散信息、对重大事件数分钟内调价 ([Prediction Markets](https://www.aeaweb.org/articles?from=j&id=10.1257%2F0895330041371321))。

## 分析

### 3.5 recency 过度反应与结果驱动的事后跟随

轨迹与赛果对置，可识别清晰 recency 过调：佛得角 0-0 后西班牙概率下挫约 7 个百分点（16.95%→10.05%），但随后连胜 7 场、未尝败绩。一支实际夺冠的球队途中被定价至 10.05%，显然超出合理信息更新幅度。机制与文献一致：交易者追随价格动量、忽视私有信息（Croxson & Reade, 2018；Angelini & De Angelis, 2026）。

但须承认市场"结果驱动事后跟随"非全无意义。指引性可分层：长期先验（赛前 #1 西班牙）正确；中期修正（换王法国）错误且持续 24 天；终点定价（决赛前 59.05/40.5）正确但已无信息量。市场接近结算时确收敛于真实结果（Wolfers & Zitzewitz, 2004）。故"市场是事后跟随者"须与"市场最终分辨率正确"并存。

### 3.6 反方立场：临场因素可部分正当化市场反应

反方主张，市场中途剧烈波动并非纯噪声。佛得角 0-0 可能反映首发轮换、伤情或状态信号；半决赛前法国被高看，亦可归因于临场阵容与体能等真实信息。Wolfers & Zitzewitz（2004）强调市场价格快速调整本身即代表信息纳入。换言之，若聚焦"单场淘汰赛临场变量"，市场反应具备一定信息内容，不宜简单归为情绪失灵。此立场提示：kimi 冻结信号的"稳定"是有代价的——它放弃对临场新信息的响应，其更优校准更多来自"低方差"而非"高信息"。

### 3.7 量化结论的边界

必须强调：上述对照全为 n=1 描述性结果。本届存在 FIFA 史上首次网球式种子保护（前四种子直至半决赛互不相遇，2025-11-25 官方公告），"前四信号"命中率被制度性抬高；佛得角之夜本身为低概率事件。故 kimi 校准更优不能上升为"模型技能"断言，仅作描述。Brier/log score 比较亦受单一赛事样本限制（评分规则定义见 [Brier Score](https://pm.wiki/data/glossary/brier-score)）。

## 小结

佛得角之夜暴露预测市场的情绪脆弱性：西班牙夺冠概率从 16.95% 跌至 10.05% 谷底，又于 7-14 与半决赛节点两度错判热门，最终随真实赛果收敛至 100%。该轨迹证明"动态"不等于"信息质量"——频繁更新可能只是 recency 过调的载体。kimi 冻结于 23.82% 的常数信号【Red：kimi 冻结版 6-11】全程更稳定、校准更优（log score 1.44 < 市场 1.78；Brier 0.688 < 市场 0.753），但属 n=1 描述性发现，且以放弃临场响应为代价。综上，佛得角之夜是市场情绪脆弱性的证据，却不构成算法事前指引优势的证据：它揭示的不是"谁更聪明"，而是"市场在途中更易被结果牵引"。本研究严守纪律，不提供任何投注建议，亦不报告收益率。

---

## 本章新增来源清单

1. [Wolfers, J., & Zitzewitz, E. (2004). Prediction Markets. *Journal of Economic Perspectives*.](https://www.aeaweb.org/articles?from=j&id=10.1257%2F0895330041371321) — 预测市场通常能准确聚合分散信息、对重大事件数分钟内调价（反方基座）。
2. [Snowberg, E., & Wolfers, J. (2010). Explaining the Favorite-Longshot Bias. *Journal of Political Economy*.](https://authors.library.caltech.edu/31703/) — 以前景理论证明预测市场偏差源于概率误感知而非风险偏好。
3. [Angelini, G., & De Angelis, L. (2026). When Do Markets Fully Process Public Information? arXiv.](https://www.arxiv.org/abs/2606.07811) — 实时预测市场价格对公共信息方向正确但不完全更新，存在可预测漂移。
4. [Croxson, K., & Reade, J. J. (2018). Improving prediction market forecasts by detecting and correcting possible over-reaction to price movements. *EJOR*.](https://www.sciencedirect.com/science/article/abs/pii/S0377221718305575) — 交易者对价格变动的过度反应与从众会驱动价格偏离真实信息。
5. [Brier Score. pm.wiki glossary.](https://pm.wiki/data/glossary/brier-score) — Brier 分为严格恰当评分规则、越低越好，用于比较概率预测校准。
6. [Prediction Market Accuracy guide. predictionmarketsreviews.com.](https://predictionmarketsreviews.com/guides/prediction-markets-accuracy) — 综述预测市场校准研究与 Brier/log score 评价方法（行业参考）。
