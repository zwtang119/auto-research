# 第1章 分组规则再评估——概率×赛制叠加能否"命中"冠亚季军

> 重建：谭溯源（Tan）· 课题研究员 v2 ｜ 状态：落盘重整合（基于冻结工作文件，事实底座锁定）
> 证据纪律：封存仓库零读写；数字取自 `923e23a` 冻结版与已复算结果；Green=冻结/已结算/官方，Red=模型输出（标注冻结版本）；严禁投注建议与收益率。

---

## 一、论点

"概率×赛制叠加"（即对模型输出的冠军概率施加 FIFA 固定 bracket 的半区/通道约束，重排为各队"最佳可能名次" ceiling）是一个**描述层（narrative）公平**的精度提升工具，但它**在标定层（calibration）不翻案**。本章立场：bracket-aware settlement 合理地把"英格兰(#5)结构性命中季军"这一事实纳入描述，使"命中冠亚季军"的叙事更经得起推敲；但同一变换**不改变**概率质量过度分散、Brier 仅勉强优于均匀噪声的标定事实，且模型 top-3 集合与实际 top-3 集合并不一致。据此，用户主张 X1.1「概率×赛制叠加可证明命中冠亚季军」**被四道硬伤驳回**，应降级为描述性钩子，而非技能证据。

> **[观点]** 纪律前提：bracket-aware settlement 是事后（post-hoc）描述性分析（须登记 OSF 修订附录），**不得**表述为"赛前即预测了位置"——变换规则提出于赛后，但全部输入（通道结构、冻结排名）均为赛前信息。

## 二、论据

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

## 三、分析

**A. 描述层 vs 标定层的分离。** 格式叠加的功劳在于：它把"英格兰(#5)精确命中季军"这一原本被平排名次掩盖的事实，通过确定性半区约束显式化（ceiling=3 恰等于实际第 3）。这是**叙事精度**的真实提升，公平且可辩护。但其代价边界清晰——它是对已结算赛果的事后重推导，不向标定层注入任何新信息：概率质量分布、Brier、平线行为均不受 ceiling 变换影响。因此"格式叠加让命中叙事更可信"与"格式叠加证明模型有标定技能"是两句不可混淆的断言，后者不成立。

**B. X1.1 四道硬伤（显式驳回）。**

1. **① 事实崩**：所谓"命中冠亚季军"若按平排名次，则法国(#2)实际第 4、英格兰(#5)压根不在模型前三——领奖台顺序并非"平凡命中"；唯有经 ceiling 重排后才部分成立，而该重排本身依赖"已知赛果"的事后约束。
2. **② 循环论证风险**：用"模型自身 #1(西班牙)+赛制"推导领奖台，是用模型输出的一部分去"验证"模型输出，并非独立外部验证；一旦把同套预测换一版本（如归一化后头号变塞内加尔 #15→#1），结论即崩，说明该"命中"由版本选择主导而非预测力。
3. **③ 反暴露软肋**：法国 #2 实际第 4，恰恰暴露平排名次的排序噪声——模型 top-2 与 actual top-2 仅在冠军位一致，亚军位（法 vs 阿）即错；若格式叠加真有标定价值，应能在赛前滤除此类噪声，而非赛后解释。
4. **④ 基准率**：FIFA 种子保护使世界前四（西#1/阿#2/法#3/英#4）分入不同半区、半决赛前不相遇（[FIFA 官方公告 2025-11-25](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw)，称 "for the first time in World Cup history"；[新华网 2025-11-26](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html) 同述）。一个**平凡基线**（按种子序 #1西/#2阿/#3法/#4英）不经任何格式叠加即匹配实际领奖台的前两位（西冠、阿亚），第三/四位互换（法/英）恰是确定性赛制的产物（英在 3P 赛胜法）。故"命中"可由"平凡基线 + 确定性赛制"完全解释，格式叠加不构成额外证据。

## 四、小结

本章结论：概率×赛制叠加在**描述层**公平提升了"命中"叙事（英格兰 #5 借 ceiling 精确命中季军），但在**标定层不翻案**——93.5% 质量压出局队、Brier 仅勉强优于均匀噪声、模型 top-3 集合≠实际 top-3 集合三事不变，且 X1.1 被四道硬伤（事实崩 / 循环论证 / 反暴露软肋 / 基准率）驳回。据此，**bracket-aware settlement 应被重定位为 C17 协议完整性审计的方法增量**——即一种在确定性赛制下对模型预测做"位置重定位审计"的纪律性手段（落 §5.3 描述层、登记 OSF 修订附录），**而非"命中"证据**。论文立身之本仍为 Protocol Integrity Vector（PIV）所代表的协议完整性审计，而非任何命中叙事。

---

### 关键发现

- 发现1：实际领奖台 西/阿/英/法，法国第 4（非第 3），须显式订正"法国进入前三"误述（[Green·`923e23a`/Wikipedia](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup)）。
- 发现2：模型 top-3 {Spain,France,Argentina} ≠ 实际 {Spain,Argentina,England}，"集合完全一致"为假（[Red·bracket-encoding-verification](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)）。
- 发现3：英格兰(#5)经 ceiling 变换精确命中季军，但须限缩为"ceiling 精确命中季军"，不得泛化为"命中前四"（[Red·bracket-aware-ranking](analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md)）。
- 发现4：标定层不翻案——93.5% 质量压出局队、Brier 0.0195–0.0200 vs 均匀 0.02083、CDS 平线 0.0325–0.0331（[Red 派生·claim-verification](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md)）。
- 发现5：X1.1 被四道硬伤驳回，bracket-aware settlement 重定位为 C17 方法增量（[项目内部·all-paper-claims-master C17/W5](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md)）。

### 数据摘要

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

### 本章新增来源（供主理人更新来源池）

1. [bracket-aware-ranking-2026-07-26.md](analysis/worldcup-2026/bracket-aware-ranking-2026-07-26.md) — Green：ceiling 变换逐队表（西#1精确/英#5 ceiling精确/法#2差一位/葡#4实错），纪律§5（post-hoc、全表呈报、禁用"命中冠亚季军"裸句）。
2. [bracket-encoding-verification-2026-07-26.md](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) — Green：引擎 top-3 概率、R32 5/32、模态决赛错、bracket 编码结构正确（路径级不可靠）。
3. [claim-verification-with-footnotes-2026-07-26.md](analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md) — Green：n=48 Brier 0.0195–0.0200、93.5% 质量、CDS 平线 0.0325–0.0331、注脚约定（G/R/I）。
4. [all-paper-claims-master-2026-07-26.md](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md) — 项目内部：C1/C10/C17/W5 评级与 prior art 12 维 crosswalk（C17 降级为"体育域首次六维整合闭集"）。
5. [FIFA. Procedures for the Final Draw for the FIFA World Cup 2026™ revealed](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw) — 机构/官方：种子保护"for the first time in World Cup history"（[G-1]，工作文件已核验；现网 JS 门控，未能直读正文）。
6. [新华网. 国际足联公布2026年世界杯抽签规则](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html) — 媒体：中文 corroboration 种子保护（前四分入不同半区）。
7. [Wikipedia. 2026 FIFA World Cup](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup) — 媒体/参考：已结算赛果核验（赛程冻结版 `923e23a` 对应；现网确认 西冠/阿亚/英季/法第4）。
8. [Murphy, A. H., & Winkler, R. L. (1977). Reliability of Subjective Probability Forecasts. JASA 72(359).](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md) — 学术：accuracy 与 proper score 可背离的统计学基础（[G-10]，支撑 Brier/标定层论证）。
