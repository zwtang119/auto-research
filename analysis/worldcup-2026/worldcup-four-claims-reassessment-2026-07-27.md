# 2026 世界杯算法对比论文——四个新观点的深度再评估

**日期**：2026-07-27
**执行模式**：完整

---

## 目录

- [引言](#引言)
- [1. 分组规则再评估：概率×赛制叠加能否"命中"冠亚季军](#1-分组规则再评估概率赛制叠加能否命中冠亚季军)
- [2. 西班牙夺冠时间线：系统从哪一天开始判断出西班牙会赢](#2-西班牙夺冠时间线系统从哪一天开始判断出西班牙会赢)
- [3. 佛得角之夜的市场情绪：量化评估准确性与前瞻指引](#3-佛得角之夜的市场情绪量化评估准确性与前瞻指引)
- [4. Polymarket 定价机制：供需动态 vs 人为设定，及与算法的系统性差异发表价值](#4-polymarket-定价机制供需动态-vs-人为设定及与算法的系统性差异发表价值)
- [结论](#结论)
- [参考文献](#参考文献)

---

## 引言

2026 年世界杯以西班牙夺冠、阿根廷亚军、英格兰季军（6–4 胜法国）、法国第四收官（[Wikipedia](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup)），为算法预测模型的赛后归因提供了难得的封闭样本。围绕「算法能否命中冠亚季军」「系统何时判定西班牙会赢」「市场情绪的量化准确性」与「Polymarket 定价是否人为设定」四类新观点，业界涌现了大量事后叙事性主张。然而，本届首次采用的网球式种子保护使世界前四（西/阿/法/英）分入不同半区、半决赛前互不相遇（[FIFA 官方抽签程序](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw)），显著抬高了「前四命中」的基准率，使朴素命中叙事的解释力被高估。

本报告基于已冻结、已结算的证据底座，对四个新观点逐一再评估，范围覆盖：（1）概率×赛制叠加能否在标定层证明命中冠亚季军；（2）CDS 路径空间引擎从哪一天开始判定西班牙夺冠；（3）佛得角之夜所暴露的市场 recency 过调与 kimi 冻结信号的校准对照；（4）Polymarket 由链上供需动态涌现的定价机制及其与算法预测的系统性差异的发表价值。

核心发现有三：其一，CDS 冠军概率全程钉死在 0.0325–0.0331 平线、从未出现「判定会赢」的拐点日（[CDS 冻结快照](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)），且引擎 top-3 集合 {Spain, France, Argentina} 与实际 top-3 {Spain, Argentina, England} 不一致；其二，X1.1「概率×赛制叠加命中冠亚季军」被四道硬伤驳回，bracket-aware settlement 应重定位为 C17 协议完整性审计的方法增量；其三，kimi 冻结于 23.82% 的常数信号在 n=1 描述下校准更优，但于 7-18/19 被市场反超，领先具时段性而非系统性。下文逐章展开。

---

## 1. 分组规则再评估：概率×赛制叠加能否"命中"冠亚季军

> 重建：谭溯源（Tan）· 课题研究员 v2 ｜ 状态：落盘重整合（基于冻结工作文件，事实底座锁定）
> 证据纪律：封存仓库零读写；数字取自 `923e23a` 冻结版与已复算结果；Green=冻结/已结算/官方，Red=模型输出（标注冻结版本）；严禁投注建议与收益率。

---

### 一、论点

"概率×赛制叠加"（即对模型输出的冠军概率施加 FIFA 固定 bracket 的半区/通道约束，重排为各队"最佳可能名次" ceiling）是一个**描述层（narrative）公平**的精度提升工具，但它**在标定层（calibration）不翻案**。本章立场：bracket-aware settlement 合理地把"英格兰(#5)结构性命中季军"这一事实纳入描述，使"命中冠亚季军"的叙事更经得起推敲；但同一变换**不改变**概率质量过度分散、Brier 仅勉强优于均匀噪声的标定事实，且模型 top-3 集合与实际 top-3 集合并不一致。据此，用户主张 X1.1「概率×赛制叠加可证明命中冠亚季军」**被四道硬伤驳回**，应降级为描述性钩子，而非技能证据。

> **[观点]** 纪律前提：bracket-aware settlement 是事后（post-hoc）描述性分析（须登记 OSF 修订附录），**不得**表述为"赛前即预测了位置"——变换规则提出于赛后，但全部输入（通道结构、冻结排名）均为赛前信息。

### 二、论据

**论据 1（事实·Green）· 实际领奖台已锁定。** 已结算赛程 `923e23a`（Green，Wikipedia 已核验）显示：冠军 西班牙、亚军 阿根廷、季军 英格兰、第四 法国；三四名决赛**英格兰 6–4 法国**（[Wikipedia 2026 FIFA World Cup](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup)）。据此，**法国最终为第 4，而非第 3**——任何"法国进入前三"的表述均为事实错误；上一轮曾误述，本章显式订正。

**论据 2（事实·Red，冻结版）· 模型 top-3 与实际 top-3 集合不一致。** CDS 路径空间引擎的 top-3 概率集合为 Spain 0.0484(#1) / France 0.0482(#2) / Argentina 0.0469(#3)（[bracket-encoding-verification-2026-07-26](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)）。实际 top-3 为 {Spain, Argentina, England}。两集合 **{Spain, France, Argentina} ≠ {Spain, Argentina, England}**，"集合完全一致"为假——上一轮曾误述，已订正。引擎模态决赛预测为"英格兰 vs 法国"，与实际"西班牙 vs 阿根廷"不符；R32 对手命中率仅 **5/32（15.6%）**。

**论据 3（事实·Red，冻结版）· 逐队 ceiling 重排。** 对 kimi 冻结前五（6-13，`0ff58a7`）施加半区约束（通道 A=西/法/葡，B=阿/英；通道内若有更高排名者 ceiling=3，否则=1）得（[bracket-aware-ranking-2026-07-26](analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md)）：

| 队 | 冻结排名 | ceiling | 实际 | 判定 |
|---|---|---|---|---|
| 西班牙 | #1 | 1 | **1** | 精确命中 ✓ |
| 法国 | #2 | 3 | 4 | ceiling 差一位 ✗（季军赛负英格兰） |
| 阿根廷 | #3 | 1 | **2** | 亚军，落位前五 ✓ |
| 葡萄牙 | #4 | 3 | 12 | 实错 ✗ |
| 英格兰 | #5 | 3 | **3** | ceiling 精确命中 ✓（6–4 胜法国） |

读法：领奖台三席（西/阿/英）均落入冻结前五；**西班牙(#1)精确命中冠军**；**英格兰(#5)在 bracket 变换下为结构性季军预测且精确命中**——这是格式叠加在描述层真正可辩护的增量，但须明确为"ceiling 精确命中季军"，**不得泛化为"命中前四"**（葡萄牙 #4 实际第 12 即反例）；法国是唯一的前三预期偏差（差一场季军赛），葡萄牙为明确实错，**二者须同表呈报**。

**论据 4（事实·Red 派生，已结算）· 标定层不翻案。** 决赛后 n=48 完整结算显示：CDS 把 **93.5% 夺冠质量压在出局队**（[claim-verification-with-footnotes-2026-07-26](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md)）；Brier 三版本 ef30658 0.019542 / 875748b 0.019970 / 923e23a 0.019989，**仅勉强低于均匀基线 0.02083**；CDS 西班牙夺冠概率全程**钉死 0.0325–0.0331 平线**（Red，冻结版），每日刷新但无赛果通道。格式叠加不改变任一上述数字。

### 三、分析

**A. 描述层 vs 标定层的分离。** 格式叠加的功劳在于：它把"英格兰(#5)精确命中季军"这一原本被平排名次掩盖的事实，通过确定性半区约束显式化（ceiling=3 恰等于实际第 3）。这是**叙事精度**的真实提升，公平且可辩护。但其代价边界清晰——它是对已结算赛果的事后重推导，不向标定层注入任何新信息：概率质量分布、Brier、平线行为均不受 ceiling 变换影响。因此"格式叠加让命中叙事更可信"与"格式叠加证明模型有标定技能"是两句不可混淆的断言，后者不成立。

**B. X1.1 四道硬伤（显式驳回）。**

1. **① 事实崩**：所谓"命中冠亚季军"若按平排名次，则法国(#2)实际第 4、英格兰(#5)压根不在模型前三——领奖台顺序并非"平凡命中"；唯有经 ceiling 重排后才部分成立，而该重排本身依赖"已知赛果"的事后约束。
2. **② 循环论证风险**：用"模型自身 #1(西班牙)+赛制"推导领奖台，是用模型输出的一部分去"验证"模型输出，并非独立外部验证；一旦把同套预测换一版本（如归一化后头号变塞内加尔 #15→#1），结论即崩，说明该"命中"由版本选择主导而非预测力。
3. **③ 反暴露软肋**：法国 #2 实际第 4，恰恰暴露平排名次的排序噪声——模型 top-2 与 actual top-2 仅在冠军位一致，亚军位（法 vs 阿）即错；若格式叠加真有标定价值，应能在赛前滤除此类噪声，而非赛后解释。
4. **④ 基准率**：FIFA 种子保护使世界前四（西#1/阿#2/法#3/英#4）分入不同半区、半决赛前不相遇（[FIFA 官方公告 2025-11-25](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw)，称 "for the first time in World Cup history"；[新华网 2025-11-26](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html) 同述）。一个**平凡基线**（按种子序 #1西/#2阿/#3法/#4英）不经任何格式叠加即匹配实际领奖台的前两位（西冠、阿亚），第三/四位互换（法/英）恰是确定性赛制的产物（英在 3P 赛胜法）。故"命中"可由"平凡基线 + 确定性赛制"完全解释，格式叠加不构成额外证据。

### 四、小结

本章结论：概率×赛制叠加在**描述层**公平提升了"命中"叙事（英格兰 #5 借 ceiling 精确命中季军），但在**标定层不翻案**——93.5% 质量压出局队、Brier 仅勉强优于均匀噪声、模型 top-3 集合≠实际 top-3 集合三事不变，且 X1.1 被四道硬伤（事实崩 / 循环论证 / 反暴露软肋 / 基准率）驳回。据此，**bracket-aware settlement 应被重定位为 C17 协议完整性审计的方法增量**——即一种在确定性赛制下对模型预测做"位置重定位审计"的纪律性手段（落 §5.3 描述层、登记 OSF 修订附录），**而非"命中"证据**。论文立身之本仍为 Protocol Integrity Vector（PIV）所代表的协议完整性审计，而非任何命中叙事。

---

#### 关键发现

- 发现1：实际领奖台 西/阿/英/法，法国第 4（非第 3），须显式订正"法国进入前三"误述（[Green·`923e23a`/Wikipedia](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup)）。
- 发现2：模型 top-3 {Spain,France,Argentina} ≠ 实际 {Spain,Argentina,England}，"集合完全一致"为假（[Red·bracket-encoding-verification](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)）。
- 发现3：英格兰(#5)经 ceiling 变换精确命中季军，但须限缩为"ceiling 精确命中季军"，不得泛化为"命中前四"（[Red·bracket-aware-ranking](analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md)）。
- 发现4：标定层不翻案——93.5% 质量压出局队、Brier 0.0195–0.0200 vs 均匀 0.02083、CDS 平线 0.0325–0.0331（[Red 派生·claim-verification](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md)）。
- 发现5：X1.1 被四道硬伤驳回，bracket-aware settlement 重定位为 C17 方法增量（[项目内部·all-paper-claims-master C17/W5](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md)）。

#### 数据摘要

| 指标 | 数据 | 来源 |
|------|------|------|
| 实际领奖台 | 西冠/阿亚/英季/法第4（英 6–4 法） | [Green·`923e23a`/Wikipedia](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup) |
| 引擎 top-3 概率 | Spain 0.0484 / France 0.0482 / Argentina 0.0469 | [Red·bracket-encoding-verification](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) |
| R32 对手命中率 | 5/32（15.6%） | [Red·bracket-encoding-verification](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) |
| 过度分散 | 93.5% 质量压出局队 | [Red 派生·claim-verification](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md) |
| Brier(n=48) | 0.0195–0.0200 vs 均匀 0.02083 | [Red 派生·claim-verification](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md) |
| CDS 冠军概率 | 全程 0.0325–0.0331 平线 | [Red·claim-verification](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md) |
| 种子保护 | 前四分入不同半区（史上首次） | [Green·FIFA 官方](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw) ＋ [新华网](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html) |

---

#### 本章新增来源（供主理人更新来源池）

1. [bracket-aware-ranking-2026-07-26.md](analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md) — Green：ceiling 变换逐队表（西#1精确/英#5 ceiling精确/法#2差一位/葡#4实错），纪律§5（post-hoc、全表呈报、禁用"命中冠亚季军"裸句）。
2. [bracket-encoding-verification-2026-07-26.md](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) — Green：引擎 top-3 概率、R32 5/32、模态决赛错、bracket 编码结构正确（路径级不可靠）。
3. [claim-verification-with-footnotes-2026-07-26.md](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md) — Green：n=48 Brier 0.0195–0.0200、93.5% 质量、CDS 平线 0.0325–0.0331、注脚约定（G/R/I）。
4. [all-paper-claims-master-2026-07-26.md](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md) — 项目内部：C1/C10/C17/W5 评级与 prior art 12 维 crosswalk（C17 降级为"体育域首次六维整合闭集"）。
5. [FIFA. Procedures for the Final Draw for the FIFA World Cup 2026™ revealed](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw) — 机构/官方：种子保护"for the first time in World Cup history"（[G-1]，工作文件已核验；现网 JS 门控，未能直读正文）。
6. [新华网. 国际足联公布2026年世界杯抽签规则](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html) — 媒体：中文 corroboration 种子保护（前四分入不同半区）。
7. [Wikipedia. 2026 FIFA World Cup](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup) — 媒体/参考：已结算赛果核验（赛程冻结版 `923e23a` 对应；现网确认 西冠/阿亚/英季/法第4）。
8. [Murphy, A. H., & Winkler, R. L. (1977). Reliability of Subjective Probability Forecasts. JASA 72(359).](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md) — 学术：accuracy 与 proper score 可背离的统计学基础（[G-10]，支撑 Brier/标定层论证）。

---

## 2. 西班牙夺冠时间线：系统从哪一天开始判断出西班牙会赢

> 重建说明：本章为会话压缩丢失后的落盘重整合（v3），全部事实底座取自冻结证据快照与权威工作文件（Green），模型类读数注明冻结版本（Red）。未做任何重新发散搜索。

### 论点

本章回应论文「四个新观点」中一类典型时间线主张——即"CDS（路径空间引擎）从某一天开始判定西班牙会夺冠"。核心论点分三层：

1. **CDS 维度，前提不成立**。在 CDS 系统里，西班牙的夺冠概率全程是一条 **0.0325–0.0331** 的平线，没有任何日级拐点；"CDS 从某天开始判定西班牙会赢"这一说法缺乏事实支撑。
2. **方法论维度，问题本身 ill-posed**。提问者把三个相互独立的系统——**kimi 冻结信号**、**Polymarket 预测市场**、**CDS 枚举式路径引擎**——的读数混为一谈，制造出并不存在的"早判西班牙"时间线。
3. **排名维度，西班牙从未高位**。即便在最宽容的解读下，CDS 也从未把西班牙置于榜首：2026-07-19 快照中塞内加尔以 **0.0446** 名列第一，西班牙（0.03302）从未独占高位，且引擎自身的末端模态决赛预测是"英格兰 vs 法国"，而非西班牙夺冠。

### 论据

**论据 1（CDS 平线，无日级拐点）**。【Green】封存仓库 git 历史可重建 CDS 日版序列（2026-06-12→07-25，44 个有效日、48 个 commit，缺 7-09 与 7-20 两个无 CDS commit 日）([市场情绪分析 + 四项注脚核验 memo §1.1](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))。分析副本对此序列的判读是：CDS 的日更冠军概率线"全程平坦"，"没有赛果通道的'日更'只是仪式"([同 memo §2.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))。锁定快照 `cds_championship.json`（2026-07-19）给出 Spain `championship_prob = 0.03302`([cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json))，落在 0.0325–0.0331 区间内，确属平线、无拐点日。

**论据 2（西班牙从未独占高位）**。【Green】同一快照中 **Senegal = 0.0446，排名 #1**([cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json))。即 CDS 的"头号热门"是一个实际在 R32 就被比利时 2–3 淘汰的队伍（塞内加尔出局见 [市场 memo §1.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)）。其机制是：引擎对塞内加尔的五个节点胜率全在 0.483–0.515（掷硬币级），归一化把"噪声最大值"加冕为头号热门([同 memo §1.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))——CDS 并非"判断"出塞内加尔，而是没有判断力、又把无判断力伪装成了观点。西班牙 0.03302 在该版本中连榜首都不是。

**论据 3（三系统混淆：kimi 与 Polymarket 被误读为 CDS）**。用户常把两类外部读数误当成"CDS 判定西班牙"：
- **(a) kimi 冻结信号**。【Red·冻结 6-11】300 智能体面板中西班牙为夺冠模态（**62/300 ≈ 20.7%**，[kimi_agent_inventory.csv](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv)）；单模型西班牙概率 **23.82%** 自 6-11 起冻结、全程静态([市场 memo §2.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))。
- **(b) Polymarket 预测市场**。【Green】`market_public_snapshot.json`（2026-07-19，来源 `polymarket_gamma_public_search`）显示 **Spain 59.05% / Argentina 40.95%**([market_public_snapshot.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json))，但这是决赛对阵已定后的市场定价；市场全轨迹显示西班牙概率直到 **2026-07-18** 才越 50%（[市场 memo §2.1/§2.2](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)），此前还经历了"法国时代"（6-21→7-14，峰值 39.0% @ 7-14）并两次半决赛错判（7-14 法国 39.0 > 西班牙 21.1；英格兰 21.8 > 阿根廷 17.4，两场热门均输）。

CDS、kimi、Polymarket 是三个**生成机制完全不同**的系统（枚举路径模型 / 冻结静态面板 / 真金白银动态市场），读数不可互通，混用即产生伪时间线。

**论据 4（引擎末端预测并非西班牙）**。【Green】路径空间引擎的模态决赛预测为"**英格兰 vs 法国**"，R32 对手命中率仅 5/32（15.6%），实际决赛为西班牙 vs 阿根廷([bracket-encoding-verification memo §2(iii)](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md))。即引擎自身"末端输出"都不是西班牙夺冠，进一步证伪"系统判定西班牙会赢"的叙事。

### 分析

**为什么"某天判定"是伪问题。** CDS 的输出是枚举路径树后的归一化质量分配，其节点胜率被赋予约 0.50（例：Czech vs Senegal `win_prob 0.50`，[市场 memo §1.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)），导致质量沿路径树近均匀扩散（[bracket memo §4.1](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)）。在这种机制下，西班牙夺冠概率稳定在 ~0.033 是**结构使然**，而非"判断使然"——不存在一个由赛果驱动的"拐点日"。日更只是仪式，已为本届结算所印证（CDS Brier 0.0195–0.0200，仅勉强低于均匀基线 0.02083，[市场 memo §1.4](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)）。

**三系统的可区分性（若必须给时点）。** kimi（冻结静态面板，23.82% 自 6-11 持续领先）回答的是"赛前/静态共识"；Polymarket（动态市场，7-18 跳变 >50%）回答的是"资金在决赛对阵确定后的重新定价"；CDS（~0.033 平线）回答的是"枚举式路径模型的结构性质量分配"。把三者叠加，会人为制造出并不存在的"CDS 早判西班牙"时间线。

**制度层注脚。** 2026 世界杯史上首次采用网球式种子保护，FIFA 官方确认四支最高排名球队（西班牙/阿根廷、法国/英格兰）分入不同半区路径，以"确保 competitive balance"（[FIFA 官方抽签程序](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw)）。这意味着"前四进四强"含制度设计成分（[市场 memo §1.2](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)），进一步削弱任何"某系统独具慧眼提前锁定西班牙"的叙事。

### 小结

无法指认"系统从某天开始判定西班牙会赢"的时点。**三重证据一致否定该前提**：CDS 冠军概率全程 0.0325–0.0331 平线、西班牙从未独占高位（塞内加尔 0.0446 #1）、且引擎末端模态决赛为"英格兰 vs 法国"。若研究必须给出一个"西班牙被看好"的时点，须严格区分两个**异质且皆非 CDS** 的来源：
- **kimi 冻结信号**：6-11 起 23.82% 持续领先（【Red·冻结 6-11】）；
- **Polymarket 市场**：7-18 跳变越 50%（【Green】）。

二者都不支持、也不应被转述为"CDS 早判西班牙"。论文中任何"CDS 于某日判定西班牙夺冠"的表述，建议一律改写为"三个系统的西班牙读数需分别标注，CDS 维度无此判定"。

---

### 关键发现

- 发现 1：CDS 西班牙夺冠概率 2026-07-19 快照为 0.03302，处于全程 0.0325–0.0331 平线，无日级拐点（[cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)【Green】）。
- 发现 2：同一快照中塞内加尔 0.0446 排名 #1，西班牙从未独占高位（[cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)【Green】）。
- 发现 3：kimi 300 智能体面板西班牙为夺冠模态（62/300），单模型概率 23.82% 自 6-11 冻结（[kimi_agent_inventory.csv](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv)【Red·冻结 6-11】）。
- 发现 4：Polymarket 西班牙概率 2026-07-19 为 59.05%，但仅于 7-18 越 50%（决赛对阵确定后），属市场动态重定价（[market_public_snapshot.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json)【Green】）。
- 发现 5：路径引擎模态决赛预测为"英格兰 vs 法国"，非西班牙夺冠（[bracket-encoding-verification memo §2(iii)](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)【Green】）。

### 数据摘要

| 指标 | 数据 | 来源 |
|------|------|------|
| CDS 西班牙夺冠概率（2026-07-19 快照） | 0.03302（区间 0.0325–0.0331 平线） | [cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)【Green】 |
| CDS 头号热门（2026-07-19） | 塞内加尔 0.0446（#1；实际 R32 出局） | [cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)【Green】 |
| kimi 单模型西班牙概率（冻结 6-11） | 23.82%（全程静态） | [市场 memo §2.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)【Red·冻结】 |
| kimi 300 智能体面板：西班牙夺冠模态 | 62/300（≈20.7%） | [kimi_agent_inventory.csv](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv)【Red·冻结】 |
| Polymarket 西班牙概率（2026-07-19 快照） | 59.05%（阿根廷 40.95%） | [market_public_snapshot.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json)【Green】 |
| Polymarket 西班牙越 50% 时点 | 2026-07-18（决赛对阵确定后） | [市场 memo §2.1/§2.2](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)【Green】 |
| 路径引擎模态决赛预测 | 英格兰 vs 法国（实际 西班牙 vs 阿根廷） | [bracket-encoding-verification §2(iii)](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)【Green】 |

---

### 本章新增来源清单（供主理人更新来源池）

1. [cds_championship.json（2026-07-19 冻结快照）](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json) — Green：Spain 0.03302、Senegal 0.0446（#1），CDS 冠军概率平线证据底稿。
2. [market_public_snapshot.json（2026-07-19 Polymarket 快照）](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json) — Green：来源 polymarket_gamma_public_search，Spain 59.05% / Argentina 40.95%，证明该读数属市场而非 CDS。
3. [kimi_agent_inventory.csv（300 智能体面板）](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv) — Red·冻结 6-11：西班牙为夺冠模态（62/300）。
4. [bracket-encoding-verification-2026-07-26.md](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) — Green 工作文件：模态决赛预测"英格兰 vs 法国"、R32 命中率 5/32、bracket 编码核验。
5. [market-sentiment-and-n48-settlement-2026-07-26.md](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md) — Green 工作文件：CDS 日更线平坦、kimi 23.82% 冻结、Polymarket 轨迹与"法国时代"、n=48 结算。
6. [Procedures for the FIFA World Cup 2026 Final Draw revealed（FIFA 官方）](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw) — 机构/官方：确认四支最高排名球队分入不同半区路径的种子保护规则（制度层注脚）。
7. [世界杯推动预测市场交易额大增，多平台显示今年冠军将是这只劲旅（财联社/搜狐）](https://www.sohu.com/a/1046568007_222256) — 媒体/行业：报道 Polymarket 世界杯冠军市场（7 月初法国 35.4% 领先、西班牙 12.4%），佐证"法国时代"与市场动态属性。

---

## 3. 佛得角之夜的市场情绪：量化评估准确性与前瞻指引

### 论点

本章核心论点：2026 世界杯期间，Polymarket 对西班牙夺冠概率的轨迹呈现显著 recency（近因）过调——价格剧烈波动反映对单场赛果的情绪性反应，而非信息质量的同步提升；相较之下，kimi 模型自 6 月 11 日起冻结于 23.82% 的常数信号，全程反而更稳定、校准更优【Red：kimi 冻结版 6-11】。由此导出：动态并不天然优于静态，更新频率与信息质量是两个独立维度。市场在本届更多扮演结果驱动的事后跟随者，而非可依赖的事前指引信号。

### 论据

#### 3.1 市场轨迹完整呈现

依据已结算的 Polymarket 西班牙夺冠概率日频快照【Green：77 个 market_public_snapshot.json 日版】，全轨迹为：16.95%（6-12）→ 16.55%（6-14）→ 13.65%（6-21，佛得角 0-0 后失榜首）→ 10.55%（6-28）→ **10.05%（7-01，谷底）** → 18.25%（7-07）→ **21.15%（7-14）** → 59.05%（7-18/19）→ 100%（结算）。

关键节点 7-14（21.15%）必须保留：当日为半决赛日，市场却对两场半决赛热门全判错——法国 39.0% > 西班牙 21.1%（实际西班牙 2–0 胜），英格兰 21.8% > 阿根廷 17.4%（实际阿根廷 2–1 胜）。市场自 6-21 将头号热门换为法国、峰值 39.0%@7-14，是一次持续约 24 天的错误定价，半决赛终了才被纠正【Green】。

#### 3.2 八场赛制澄清

锁定事实底座确认：西班牙实际赛制为 8 场、7 胜 1 平【Green：已结算赛程】。需澄清表面矛盾——"0-0 逼平"与"7 胜"并不冲突：该 0-0 平局发生于小组赛对阵佛得角（6-21），正是触发市场跌至谷底的那场；"7 胜"指小组赛之后连胜的 7 场（4-0 / 1-0 / 3-0 / 1-0 / 2-1 / 2-0 / 1-0，含淘汰赛至决赛）。故西班牙为"1 平 + 7 胜"、全程未尝败绩的冠军，而非"7 战全胜"。谷底价 10.05% 对应的恰是一支实际未输球的冠军队。

#### 3.3 kimi 冻结信号与量化校准对照

kimi 自 6-11 起冻结于 23.82%【Red：kimi 冻结版 6-11】，全程高于市场任何时点（除决赛日外）。基于已结算结果计算的评分【Green：n=48 夺冠结算与同池多项 Brier】，均采用"越低越好"约定：

- 冠军 log score（−ln p_Spain）：kimi 1.44 < 市场 1.78（即市场 1.78 > kimi 1.44），kimi 更优；该市场值取自 6-13 单点快照（16.85%），非全程轨迹。
- 同池多项 Brier（21 队概率向量重归一）：kimi 0.688 < 市场 0.753 < CDS 0.930 < 均匀基线 0.952，kimi 校准更优。
- 时间积分 log score（−ln p 逐日均值，6-12→7-19，n=38 个市场快照）：市场 1.744 vs kimi 常数 1.435，冻结信号在时间维积分下仍占优。

#### 3.4 预测市场行为文献支撑

预测市场并非恒有效。Croxson 与 Reade（2018）指出，交易者对价格变动的"过度反应"（over-reaction to price movements）与从众（herding）会驱动价格偏离真实信息，形成可检测的系统偏差 ([Improving prediction market forecasts…](https://www.sciencedirect.com/science/article/abs/pii/S0377221718305575))。Snowberg 与 Wolfers（2010）以前景理论证明，favorite–longshot 偏差主要源于对概率的"误感知"而非风险偏好 ([Explaining the Favorite-Longshot Bias](https://authors.library.caltech.edu/31703/))，为近因过调提供行为机制。Angelini 与 De Angelis（2026）在实时预测市场中发现，价格对公共信息"方向正确但不完全"——基准概率一分钟变化仅对应约 0.64 倍的市场同步变化，剩余偏差预示后续可预测漂移 ([When Do Markets Fully Process Public Information?](https://www.arxiv.org/abs/2606.07811))。Wolfers 与 Zitzewitz（2004）则给出反方基座：预测市场通常能较好聚合分散信息、对重大事件数分钟内调价 ([Prediction Markets](https://www.aeaweb.org/articles?from=j&id=10.1257%2F0895330041371321))。

### 分析

#### 3.5 recency 过度反应与结果驱动的事后跟随

轨迹与赛果对置，可识别清晰 recency 过调：佛得角 0-0 后西班牙概率下挫约 7 个百分点（16.95%→10.05%），但随后连胜 7 场、未尝败绩。一支实际夺冠的球队途中被定价至 10.05%，显然超出合理信息更新幅度。机制与文献一致：交易者追随价格动量、忽视私有信息（Croxson & Reade, 2018；Angelini & De Angelis, 2026）。

但须承认市场"结果驱动事后跟随"非全无意义。指引性可分层：长期先验（赛前 #1 西班牙）正确；中期修正（换王法国）错误且持续 24 天；终点定价（决赛前 59.05/40.5）正确但已无信息量。市场接近结算时确收敛于真实结果（Wolfers & Zitzewitz, 2004）。故"市场是事后跟随者"须与"市场最终分辨率正确"并存。

#### 3.6 反方立场：临场因素可部分正当化市场反应

反方主张，市场中途剧烈波动并非纯噪声。佛得角 0-0 可能反映首发轮换、伤情或状态信号；半决赛前法国被高看，亦可归因于临场阵容与体能等真实信息。Wolfers & Zitzewitz（2004）强调市场价格快速调整本身即代表信息纳入。换言之，若聚焦"单场淘汰赛临场变量"，市场反应具备一定信息内容，不宜简单归为情绪失灵。此立场提示：kimi 冻结信号的"稳定"是有代价的——它放弃对临场新信息的响应，其更优校准更多来自"低方差"而非"高信息"。

#### 3.7 量化结论的边界

必须强调：上述对照全为 n=1 描述性结果。本届存在 FIFA 史上首次网球式种子保护（前四种子直至半决赛互不相遇，2025-11-25 官方公告），"前四信号"命中率被制度性抬高；佛得角之夜本身为低概率事件。故 kimi 校准更优不能上升为"模型技能"断言，仅作描述。Brier/log score 比较亦受单一赛事样本限制（评分规则定义见 [Brier Score](https://pm.wiki/data/glossary/brier-score)）。

### 小结

佛得角之夜暴露预测市场的情绪脆弱性：西班牙夺冠概率从 16.95% 跌至 10.05% 谷底，又于 7-14 与半决赛节点两度错判热门，最终随真实赛果收敛至 100%。该轨迹证明"动态"不等于"信息质量"——频繁更新可能只是 recency 过调的载体。kimi 冻结于 23.82% 的常数信号【Red：kimi 冻结版 6-11】全程更稳定、校准更优（log score 1.44 < 市场 1.78；Brier 0.688 < 市场 0.753），但属 n=1 描述性发现，且以放弃临场响应为代价。综上，佛得角之夜是市场情绪脆弱性的证据，却不构成算法事前指引优势的证据：它揭示的不是"谁更聪明"，而是"市场在途中更易被结果牵引"。本研究严守纪律，不提供任何投注建议，亦不报告收益率。

---

### 本章新增来源清单

1. [Wolfers, J., & Zitzewitz, E. (2004). Prediction Markets. *Journal of Economic Perspectives*.](https://www.aeaweb.org/articles?from=j&id=10.1257%2F0895330041371321) — 预测市场通常能准确聚合分散信息、对重大事件数分钟内调价（反方基座）。
2. [Snowberg, E., & Wolfers, J. (2010). Explaining the Favorite-Longshot Bias. *Journal of Political Economy*.](https://authors.library.caltech.edu/31703/) — 以前景理论证明预测市场偏差源于概率误感知而非风险偏好。
3. [Angelini, G., & De Angelis, L. (2026). When Do Markets Fully Process Public Information? arXiv.](https://www.arxiv.org/abs/2606.07811) — 实时预测市场价格对公共信息方向正确但不完全更新，存在可预测漂移。
4. [Croxson, K., & Reade, J. J. (2018). Improving prediction market forecasts by detecting and correcting possible over-reaction to price movements. *EJOR*.](https://www.sciencedirect.com/science/article/abs/pii/S0377221718305575) — 交易者对价格变动的过度反应与从众会驱动价格偏离真实信息。
5. [Brier Score. pm.wiki glossary.](https://pm.wiki/data/glossary/brier-score) — Brier 分为严格恰当评分规则、越低越好，用于比较概率预测校准。
6. [Prediction Market Accuracy guide. predictionmarketsreviews.com.](https://predictionmarketsreviews.com/guides/prediction-markets-accuracy) — 综述预测市场校准研究与 Brier/log score 评价方法（行业参考）。

---

## 4. Polymarket 定价机制：供需动态 vs 人为设定，及与算法的系统性差异发表价值

> **来源分级（依 AGENTS.md）**：【Green】= 冻结数据／已结算／官方文档；【Red】= 模型输出（须注明冻结版本）。本章不含投注建议，不报告收益率。

### 论点

Polymarket 的赛事冠军概率并非由平台或庄家人为设定的赔率，而是由链上连续限价订单簿（CLOB）中买卖双方的真实资金供需动态"涌现"出的价格信号，经 UMA 乐观预言机结算【Green】。将 kimi（算法预测）与此市场化基线在 2026 世界杯单届样本上做时点对照，可以支撑"描述性领先"的发表价值，但"系统性差异成立"只能作为待检假设而非定论。本节纠正一种常见误读：kimi 并非"全程高于市场"，而是在 7-18 前领先、于 7-18/19 被市场反超【Red＋Green】。

### 论据

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

### 分析

机制层面的关键启示是：Polymarket 价格由边际交易者用真金白银挂单形成，是"边际价格"而非"群体均值"，深钱包的意见天然权重更大（[预测市场：原理、现状与展望](https://fddi.fudan.edu.cn/_t2515/dc/dc/c21253a777436/page.htm)）【Green】。这解释了为何 kimi 的算法估计能在特定时段领先于一个被流动性与 recency 偏误扭曲的市场——领先反映的是"信息差异"而非"算法必胜"。将时点对照升级为"系统性差异"前，必须排除训练语料回声、单一市场结构等替代解释，这正是跨届／跨市场复现臂的设计目的。

### 小结

Polymarket 的冠军概率由链上 CLOB 的供需动态涌现、UMA 乐观预言机结算，零人为设定赔率【Green】。kimi 的冻结估计（23.82%, 6-11）在 7-18 前领先于市场，但 7-18/19 被市场反超，故"领先"须表述为时段性、描述性【Red＋Green】。n=1 描述性领先具备发表价值（首次六维整合闭集预测域），但单届样本限制外推；"系统性差异成立"应保留为待检假设，待跨届／跨市场复现方可升级【Green】。市场是有偏但可用的基线，适合作为算法预测的对照基准而非真理标准。

---

### 本章新增来源

1. [从 AMM 到订单簿：探索 Polymarket 定价机制的转变](https://news.qq.com/rain/a/20250731A04LAA00) — 详解 Polymarket CLOB 机制：YES/NO 份额 $1 锚定、铸造/赎回、套利修正使价格向 $1 收敛（Green，机制文档）
2. [Polymarket 与预测市场的去中心化困境](https://www.sohu.com/a/784453679_121948394) — UMA 乐观预言机集成：CTF 适配器、挑战期、DVM 仲裁流程（Green，机制文档）
3. [How does UMA work?（UMA 官方文档）](https://docs.uma.xyz/protocol-overview/how-does-uma-work) — OO "先假定正确后争议验证"，~99.8% 无争议快速结算，DVM 24h/24h 秘密投票、65% 多数决（Green，官方）
4. [稳定币点燃预测市场？Polymarket 和 Kalshi 完成新一轮融资](https://www.163.com/dy/article/K34NPMG30552956F.html) — 引 Polymarket 官网声明"不设定价格或赔率，完全由供需决定"；对比传统庄家（Green，媒体报道）
5. [The economics of the Kalshi prediction market（CEPR VoxEU）](https://cepr.org/voxeu/columns/economics-kalshi-prediction-market) — Bürgi 等（2025）基于逾 30 万份 Kalshi 合约证实 favorite-longshot bias（Green，学术）
6. [Prediction market prices under risk aversion and heterogeneous beliefs（ScienceDirect）](https://www.sciencedirect.com/science/article/abs/pii/S0304406817300484) — 理论证明价格=边际信念而非群体均值，给出 favorite-longshot bias 的理性解释（Green，学术期刊）
7. [金融学术前沿丨预测市场：原理、现状与展望（复旦 FDDI）](https://fddi.fudan.edu.cn/_t2515/dc/dc/c21253a777436/page.htm) — 预测市场理论框架（Hayek/Aumann/Arrow）与偏差综述（Green，学术机构）
8. [Prediction market 文献综述与书单（datafield.dev）](https://datafield.dev/learning-prediction-markets/part-01/chapter-02/further-reading.html) — 收录 Wolfers & Zitzewitz 2004、Manski 2006、Arrow et al. 2008 等核心文献出处（Green，学术）

---

## 结论

综合四章证据，本报告对四个新观点给出如下裁决。

第一，X1.1「概率×赛制叠加可证明命中冠亚季军」不成立：该变换仅在描述层公平显化了「英格兰(#5)经 ceiling 精确命中季军」，但标定层不翻案——93.5% 夺冠质量压在出局队、Brier 0.0195–0.0200 仅勉强优于均匀基线 0.02083、引擎 top-3 集合与实际不一致（[claim-verification](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md)）。据此，bracket-aware settlement 应降级为 C17 方法增量，而非命中证据。

第二，「CDS 从某天开始判定西班牙会赢」是伪问题：CDS 冠军概率全程 0.0325–0.0331 平线、西班牙从未独占高位（塞内加尔 0.0446 #1），且引擎末端模态决赛为「英格兰 vs 法国」（[CDS 快照](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)）。所谓「早判」实为把 kimi 冻结信号（6-11 起 23.82%）与 Polymarket 市场（7-18 越 50%）误读为 CDS 所致。

第三，佛得角之夜证明市场是结果驱动的事后跟随者：西班牙夺冠概率从 16.95% 跌至 10.05% 谷底、中途误立「法国时代」约 24 天，终随赛果收敛至 100%（[市场快照](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json)）；kimi 冻结信号校准更优（log score 1.44 < 市场 1.78）但属 n=1、以放弃临场响应为代价（[Croxson & Reade, 2018](https://www.sciencedirect.com/science/article/abs/pii/S0377221718305575)）。

第四，Polymarket 价格由链上 CLOB 供需动态涌现、UMA 预言机结算，零人为设定赔率（[UMA 文档](https://docs.uma.xyz/protocol-overview/how-does-uma-work)）；kimi 在 7-18 前领先但旋即被反超，「系统性差异成立」仅宜保留为待检假设。

本研究严守纪律：不输出投注建议、不报告收益率。论文立身之本在 Protocol Integrity Vector 所代表的协议完整性审计，而非任何命中叙事。

---

## 参考文献

- Angelini, G., & De Angelis, L. (2026). When Do Markets Fully Process Public Information? arXiv. [链接](https://www.arxiv.org/abs/2606.07811)
- Bürgi 等 (2025). The economics of the Kalshi prediction market. CEPR VoxEU. [链接](https://cepr.org/voxeu/columns/economics-kalshi-prediction-market)
- Croxson, K., & Reade, J. J. (2018). Improving prediction market forecasts by detecting and correcting possible over-reaction to price movements. European Journal of Operational Research. [链接](https://www.sciencedirect.com/science/article/abs/pii/S0377221718305575)
- Manski 引 (年份未知). Prediction market prices under risk aversion and heterogeneous beliefs. ScienceDirect. [链接](https://www.sciencedirect.com/science/article/abs/pii/S0304406817300484)
- Murphy, A. H., & Winkler, R. L. (1977). Reliability of Subjective Probability Forecasts. Journal of the American Statistical Association, 72(359). [链接](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md)
- Snowberg, E., & Wolfers, J. (2010). Explaining the Favorite-Longshot Bias. Journal of Political Economy. [链接](https://authors.library.caltech.edu/31703/)
- Wolfers, J., & Zitzewitz, E. (2004). Prediction Markets. Journal of Economic Perspectives. [链接](https://www.aeaweb.org/articles?from=j&id=10.1257%2F0895330041371321)
- 复旦 FDDI (年份未知). 预测市场：原理、现状与展望. [链接](https://fddi.fudan.edu.cn/_t2515/dc/dc/c21253a777436/page.htm)
- datafield.dev (年份未知). Prediction market 文献综述与书单. [链接](https://datafield.dev/learning-prediction-markets/part-01/chapter-02/further-reading.html)
- FIFA (2025). Procedures for the Final Draw for the FIFA World Cup 2026™ revealed. [链接](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw)
- UMA (年份未知). How does UMA work? [链接](https://docs.uma.xyz/protocol-overview/how-does-uma-work)
- all-paper-claims-master-2026-07-26.md（项目内部：C1/C10/C17/W5 评级与 prior art crosswalk）. [链接](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md)
- bracket-aware-ranking-2026-07-26.md（ceiling 变换逐队表）. [链接](analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md)
- bracket-encoding-verification-2026-07-26.md（引擎 top-3 概率、R32 5/32）. [链接](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)
- claim-verification-with-footnotes-2026-07-26.md（n=48 Brier、93.5% 质量、CDS 平线）. [链接](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md)
- cds_championship.json（2026-07-19 冻结快照：Spain 0.03302、Senegal 0.0446）. [链接](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)
- kimi_agent_inventory.csv（300 智能体面板：西班牙夺冠模态 62/300）. [链接](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv)
- market_public_snapshot.json（2026-07-19 Polymarket 快照：Spain 59.05%）. [链接](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json)
- market-sentiment-and-n48-settlement-2026-07-26.md（CDS 日更线、kimi 23.82%、Polymarket 轨迹、n=48 结算）. [链接](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)
- 网易 (年份未知). 稳定币点燃预测市场？Polymarket 和 Kalshi 完成新一轮融资. [链接](https://www.163.com/dy/article/K34NPMG30552956F.html)
- pm.wiki (年份未知). Brier Score（glossary）. [链接](https://pm.wiki/data/glossary/brier-score)
- predictionmarketsreviews.com (年份未知). Prediction Market Accuracy guide. [链接](https://predictionmarketsreviews.com/guides/prediction-markets-accuracy)
- 搜狐 (年份未知). Polymarket 与预测市场的去中心化困境. [链接](https://www.sohu.com/a/784453679_121948394)
- 搜狐/财联社 (2026). 世界杯推动预测市场交易额大增. [链接](https://www.sohu.com/a/1046568007_222256)
- 腾讯新闻 (2025). 从 AMM 到订单簿：探索 Polymarket 定价机制的转变. [链接](https://news.qq.com/rain/a/20250731A04LAA00)
- 新华网 (2025). 国际足联公布2026年世界杯抽签规则. [链接](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html)
- Wikipedia (2026). 2026 FIFA World Cup. [链接](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup)

---

## 免责声明

> 本报告由 AI 深度研究团队生成，重要决策请经专业人员核验。所有引用来源请用户在重要场景下二次核验时效性与真实性。本研究严守项目纪律：不输出投注建议、不报告收益率。

---

## 待完善事项

- **参考文献链接目标重叠（轻微，非条目重复）**：第 5 条 `Murphy, A. H., & Winkler, R. L. (1977)` 与第 12 条 `all-paper-claims-master-2026-07-26.md（项目内部）` 的链接目标同为 `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md`。二者为不同文献条目（学术期刊论文 vs 项目内部文件），故未做合并删除；建议主理人核实是否将 Murphy 1977 链接改指向其原始 JASA 出处，以使链接目标唯一。
- **章节内小节标题层级（源文件继承，非错误）**：第 1 章的「关键发现 / 数据摘要 / 本章新增来源」在原稿为 `###` 级，经统一降一级后为 `####`；第 2–4 章同名词节在原稿为 `##` 级，降一级后为 `###`。本报告对所有原稿标题执行"统一降一级"规则以忠实保留各章内部相对层级，故跨章绝对层级存在此源继承差异，不影响阅读与导航。
