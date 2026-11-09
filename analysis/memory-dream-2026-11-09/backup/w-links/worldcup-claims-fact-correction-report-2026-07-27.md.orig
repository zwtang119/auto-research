# 2026 世界杯预测主张的事实订正及其对 Paper A 的学术价值重估

**日期**：2026-07-27
**执行模式**：完整

---

## 目录

- 引言
- 1. 分组规则的再订正：固定 bracket 同半区如何证伪「决赛相遇」误读，并稀释「夺冠命中」的学术权重
- 2. CDS 引擎判定时间线的证伪：0.0325–0.0331 平线与「会赢」断言的不可成立
- 3. 佛得角之夜的市场情绪再检：谷底 10.05% 的 recency 过调与事后跟随本质
- 4. Polymarket 定价机制与系统性差异假设：CLOB 偏差、n=1 约束与发表价值的边界
- 5. 综合学术价值裁决：四项订正对 Paper A（协议完整性审计 C17）的净冲击
- 结论
- 参考文献

---

## 引言

用户在本项目结题后，基于已发生的赛果回溯，提出了四项关于「命中」与「学术价值」的主张：其一，西班牙与法国「不可能在决赛相遇」，且西班牙夺冠、法国名列第三；其二，系统（CDS 引擎）在某一日「开始判定西班牙会赢」；其三，佛得角之夜的市场恐慌反向证明本算法的情绪稳健性，可升格为「事前指引」；其四，本算法与 Polymarket 定价存在可发表的「系统性差异」。这些主张在直觉上颇具吸引力，但其前提是否成立，须以可复算数据检验，而非以结果反推。

本报告作为 Phase 4 框架，汇总五章经三审通过的深度调研稿，对上述四项主张逐一验证。调研严格遵循「封存仓库零读写」与「赛前冻结」纪律，所有数字取自冻结版证据快照（如 `923e23a:data/processed/schedule.json` 与 `all-paper-claims-master-2026-07-26.md`），并交叉核验 FIFA 官方抽签、BBC Sport 抽签机制、光明网分组结果等外部权威源。

检验揭示三处关键事实订正：（1）组号误述——西班牙实为 H 组、法国为 I 组，并非用户所称的 E/D 组；（2）名次误述——法国在三四名决赛以 6–4 负于英格兰，实际排名第 4，而非第 3；（3）CDS 从未「判定会赢」——引擎对西班牙夺冠概率全程钉死在 0.0325–0.0331 平线、无日级拐点，「某天开始判定」在数据上无处安放。

最终裁决为净澄清（net clarification）：3 处事实误述被订正、2 处越界主张被收紧，但 Paper A 的立身之本——协议完整性审计（C17 / Protocol Integrity Vector）——经 W5 系统检索确认为与 prior art 部分重叠，并不受四章订正动摇，反而因诚实订正更可辩护。

---

## 1. 分组规则的再订正：固定 bracket 同半区如何证伪「决赛相遇」误读，并稀释「夺冠命中」的学术权重

### 第1章 分组规则的再订正：固定 bracket 同半区如何证伪「决赛相遇」误读，并稀释「夺冠命中」的学术权重

> 作者：谭溯源（Tan）· 课题研究员 v1 ｜ 日期：2026-07-27 ｜ 状态：Phase 3.1 中间工作稿（由发布员整合）
> 证据纪律：封存仓库 `~/Documents/GitHub/cds4worldcup` 零读写；所有数字取自 `923e23a` 冻结版与已复算结果；中文源仅作注脚。

---

### 一、论点

用户前提「西班牙和法国不可能在决赛相遇、最终排名西班牙第1法国第3」**部分成立、部分须显式订正**，由此引出本章三个子结论：

1. 「西法不可能在决赛相遇」**结构性成立**，但其依据必须精确为「FIFA 赛前发布的固定 knockout bracket 将二者落入同一半区」，而**不能**泛称为「分组规则」——二者根本不在同一小组。
2. 「法国第3」为**事实错误**：三四名决赛英格兰 6–4 法国，法国最终为**第4**。
3. 即便纠正后「命中冠军西班牙」成立，因制度（种子保护）与市场（top-5 同中 4/4）的双重稀释，「命中」**仅配作论文 hook**，**不改变 Paper A 的立身之本**——协议完整性审计（C17 / Protocol Integrity Vector）。

> **[观点]** 本章立场：「命中冠军」是叙事钩子而非证据，这是本论文的纪律前提，非待证假设。

---

### 二、论据

**论据 1（事实）· 2026 赛制结构与固定 bracket。** 本届史上首次扩军至 48 队、12 组（每组 4 队）；32 强淘汰赛采用 FIFA **赛前发布的固定 bracket（path）**，非按实时排名重排。[BBC Sport 抽签机制详解](https://www.bbc.com/sport/football/articles/c997y4l20jgo) 明确将 12 组映射至 bracket 的「quadrant（半区/象限）」，组号直接决定 knockout 落位。

**论据 2（事实）· 组号订正：西班牙 H 组、法国 I 组。** 用户前提称「西班牙 E 组、法国 D 组」，**与官方抽签不符**。权威抽签结果：**[西班牙 = H 组](https://m.gmw.cn/2025-12/06/content_1304252440.htm)**（H：西班牙、佛得角、沙特、乌拉圭），**[法国 = I 组](https://m.cyol.com/gb/articles/2025-12/06/content_YOMajAsmpZ.html)**（I：法国、塞内加尔、洲际附加赛胜者、挪威）。该订正亦被赛事数据库交叉核验（H 组含西班牙、I 组含法国）。

**论据 3（事实）· 种子保护制度。** 本届史上首次采用「网球大满贯式」种子保护：世界前四西班牙(#1)/阿根廷(#2)/法国(#3)/英格兰(#4) 分入**不同半决赛路径**，四队同夺小组头名时半决赛前不相遇。[FIFA 官方公告（2025-11-25）](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw) 称其为 "for the first time in World Cup history"；[新华网中文报道](https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html) 同述。

**论据 4（事实）· 同半区推导。** 由固定 bracket 的半区约束可推出：西班牙与阿根廷处**异半区**（仅决赛可遇），法国与英格兰处**异半区**；而法国/英格兰与西班牙/阿根廷「until the semi-finals」方可相遇（[BBC](https://www.bbc.com/sport/football/articles/c997y4l20jgo) 原文：*France and England would not be able to meet either Spain or Argentina until the semi-finals*）。由此锁定：**西班牙(H)与法国(I)同处一个半区，最早仅能于半决赛相遇，绝无可能决赛碰面**。

**论据 5（事实）· 实际赛果（外部权威 + 项目冻结版双重核验）。**
- 决赛：**[西班牙 1–0（加时）阿根廷](https://www.icoachfootball.net/world-cup-2026-knockout-bracket/)**，西班牙夺冠；
- 半决赛：**[西班牙 2–0 法国](https://so.html5.qq.com/page/real/search_news?docid=70000021_2636a5d522730452)**、英格兰 1–2 阿根廷；
- 三四名决赛：**[英格兰 6–4 法国](https://www.icoachfootball.net/world-cup-2026-knockout-bracket/)** → **法国最终第 4**（用户称第 3 错误）。
- 项目内部已结算赛程 `923e23a:data/processed/schedule.json`（Green，Wikipedia 已核验）与上述外部源高度吻合：四强 = 西/阿/法/英，冠军西班牙。[项目文档 `all-paper-claims-master` F2](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md)

**论据 6（事实）· 项目内部 bracket 编码核验。** [`bracket-encoding-verification-2026-07-26.md`](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) 事后复算确认：CDS 引擎的 bracket 编码**结构正确**——实际半决赛「西班牙 2–0 法国」在其路径结构中从被淘汰方（法国）视角**可达（命中）**；但路径级预测并不可靠，**R32 对手命中率仅 5/32（15.6%）**，模态决赛预测「英格兰 vs 法国」与实际「西班牙 vs 阿根廷」不符。编码正确是建模义务，非预测技能。

---

### 三、分析

**A. 为何「不可能决赛相遇」必须精确为「固定 bracket 同半区」而非「分组规则」。** 「分组规则」本身只约束小组内同组不相遇，西法本就不同组（H/I），泛称「分组规则」会误导读者以为约束来自小组同组。真正排除决赛相遇的是**赛前发布的固定 knockout bracket 的半区分配**（论据 1、4）。不精确地表述，会授人以柄——审稿人可指出「不同组何以推出决赛不遇」。本章坚持：约束来源 = 固定 bracket 半区，证据链闭环。

**B. 事实订正的诚实性（最高优先级）。** 两处订正性质不同：E/D→H/I 是**组号笔误**；法国第3→第4 是**实质性赛果错误**（三四名决赛英格兰 6–4 法国，多源一致）。论文须**显式订正、不得为撑「我们命中」结论而淡化**。找不到的数据标缺口、绝不编造——这是本研究的证据纪律（见 `claim-verification-with-footnotes` §0 注脚约定）。

**C. 「夺冠命中」的学术权重被三重稀释（观点，基于事实）。**
- **（1）粉笔年（chalk year）。** 四支受保护种子**全部进入四强**（SF 正是西/法/阿/英），强队普遍中奖，本届为典型「强队中奖年」。[观点，事实底座：四强=前四种子] 在此结构下，「命中前四」接近制度必然，非独家技能。
- **（2）市场 top-5 同中 4/4。** kimi 与市场冠军 baseline top5 均为西/法/阿/葡/英，四强中 4 队命中（C1，[项目文档 I-9](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md)）。命中**非独家**。
- **（3）种子保护压低信息量。** 制度预先排除最危险互杀，任何重仓前四信号的 4/4 命中率被结构性抬高（C10 结论）。
- **结论 [观点]**：「命中冠军」仅配作引言 hook（S2/S7 纪律），且须随车携带三重保险（幸存者偏差 / 种子保护 / 市场后来修对，见 `claim-verification-with-footnotes` §6）。它**不改变 Paper A 的立身之本**。

**D. 立身之本：协议完整性审计（C17 / W5）。** Paper A 的真正贡献是 Protocol Integrity Vector（PIV）——把 ex-ante 冻结、来源分级、统一结算、时态溯源、快照漂移、schema 校验六维整合为预测资产的**一等评估闭集**。[项目文档 C17/W5](analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md) 经 W5 系统检索（PRISMA-lite，~137 候选→38 纳入）裁定：**与 prior art 部分重叠**——WorldFork 占 A/D/E/F、SourceBench 占 B、ContractBench 占 E、LMU *LLM-SoccerArena* 占 ex-ante+schema+协议失败诊断；但**无单一工作把六维打包为封闭一等评估对象**，且 B(来源分级)/C(快照漂移) 为体育预测域空白，构成本工作增量。故 C17 须由「空白」降级为「体育预测域首次六维整合闭集」（诚实避免 overclaim）。相关 prior art：WorldFork (ICML 2026)、SourceBench (arXiv:2602.16942)、ContractBench (arXiv:2605.17281)、LMU LLM-SoccerArena (2026)；统计基础参见 Murphy & Winkler (1977, JASA) 与 Dixon & Coles (1997, JRSS A)。

---

### 四、小结

本章完成三项工作：（1）**组号订正**——西班牙 H 组、法国 I 组（非用户所称 E/D）；（2）**证伪路径澄清**——「西法不可能决赛相遇」结构性成立，但依据须精确为「固定 bracket 同半区」而非「分组规则」，且实际赛果显示法国为**第 4**（非第 3）；（3）**学术权重重估**——即便「命中冠军西班牙」成立，亦被粉笔年、市场 4/4、种子保护三重稀释，仅作 hook，论文立身之本仍为协议完整性审计（C17）。**诚实优先**：两处事实错误均已显式订正，未为结论美化而淡化。

---

#### 本章来源清单（供发布员整合）

| # | 标题 | URL / 路径 | 类型 |
|---|---|---|---|
| 1 | FIFA. *Procedures for the Final Draw for the FIFA World Cup 2026™ revealed* | https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw | 机构 |
| 2 | BBC Sport. *World Cup draw 2026: Format, start time, seeding, pots & dates* | https://www.bbc.com/sport/football/articles/c997y4l20jgo | 媒体 |
| 3 | 光明网. *2026美加墨世界杯分组抽签结果出炉* | https://m.gmw.cn/2025-12/06/content_1304252440.htm | 媒体 |
| 4 | 中青报. *姆巴佩"对话"哈兰德!2026年美加墨世界杯分组抽签结果出炉* | https://m.cyol.com/gb/articles/2025-12/06/content_YOMajAsmpZ.html | 媒体 |
| 5 | icoachfootball. *World Cup 2026 Winner: Spain, Full Bracket, Groups & Results* | https://www.icoachfootball.net/world-cup-2026-knockout-bracket/ | 媒体/数据 |
| 6 | 腾讯新闻. *西班牙1-0艰难战胜卫冕冠军阿根廷…半决赛西班牙2-0法国* | https://so.html5.qq.com/page/real/search_news?docid=70000021_2636a5d522730452 | 媒体 |
| 7 | Wikipedia. *2026 FIFA World Cup*（赛果核验） | https://en.wikipedia.org/wiki/2026_FIFA_World_Cup | 媒体/参考 |
| 8 | 项目内部. `bracket-encoding-verification-2026-07-26.md` | analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md | 项目内部 |
| 9 | 项目内部. `all-paper-claims-master-2026-07-26.md`（C1/C10/C17/W5） | analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md | 项目内部 |
| 10 | 项目内部. `claim-verification-with-footnotes-2026-07-26.md`（§0 注脚/§6 三重保险） | analysis/worldcup-2026/claim-verification-with-footnotes-2026-07-26.md | 项目内部 |
| 11 | 项目内部. 已结算赛程 `923e23a:data/processed/schedule.json` | （证据快照，Green/Wikipedia 已核验） | 项目内部 |
| 12 | Prior art. WorldFork (ICML 2026) / SourceBench (arXiv:2602.16942) / ContractBench (arXiv:2605.17281) / LMU LLM-SoccerArena (2026) | 见 `all-paper-claims-master` §7 [G-13]–[G-19] | 学术 |
| 13 | Murphy, A. H., & Winkler, R. L. (1977). *Reliability of Subjective Probability Forecasts*. JASA 72(359). | 见 `all-paper-claims-master` [G-10] | 学术 |

---

## 2. CDS 引擎判定时间线的证伪：0.0325–0.0331 平线与「会赢」断言的不可成立

### 第2章 CDS 引擎判定时间线的证伪：0.0325–0.0331 平线与「会赢」断言的不可成立

> 草稿（intermediate working draft）｜ 作者：topic-researcher-v2 ｜ 日期：2026-07-27
> 纪律：封存仓库零读写；证据取自分析副本只读文档；事实性陈述带源；不输出投注建议、不报告收益率。

---

### 一、论点

用户前提"系统（CDS 引擎）在某一天开始判定西班牙会赢"在可复算数据层面**不成立**。（事实，依据 `analysis/worldcup-2026/all-paper-claims-master-2026-07-26.md` C12 / `claim-verification-with-footnotes-2026-07-26.md` §5.4 [R-2]）

项目副本显示，CDS 引擎对西班牙夺冠概率的日更序列全程钉死在 **0.0325–0.0331** 区间，不随赛果推进出现任何日级拐点，也从未越过任何可称为"会赢"的阈值（常识上需显著高于其它候选、至少进入高概率区）。因此，该前提应作为**证伪**明确写入，而非作为论文的承重发现。（事实 + 观点）

---

### 二、论据

**1. CDS 日更线是一条平坦的"仪式线"。**
CDS 副本 `ef30658`/`875748b` 中，西班牙路径概率全程为 **0.0325–0.0331**，每日 `generated_at` 字段刷新，但不存在赛果通道——即"每日更新"在实质上不携带新预测信息（`market-sentiment-and-n48-settlement-2026-07-26.md` §2.3；C12 评级 A，可机器复算）。这一平线在 6-12 至 7-25 的 44 个自然日内形态不变，与"某天开始判定会赢"的叙事在几何上互斥。（事实）

即便考察版本选择问题（C5 仅评级 C、禁用"CDS 预测冠军"）：归一化前 `ef30658` 西班牙头名也仅 **0.0484**，归一化后头名变为塞内加尔 **0.0435**（`bracket-encoding-verification-2026-07-26.md` §2；all-paper-claims [I-4]）——任一版本下西班牙都远未接近"会赢"量级。（事实）

**2. 误读来源澄清：三个相互独立的概率源。**
用户可能把两种非 CDS 信号误当作"系统开始判定会赢"的证据，须显式区分：
- **(a) kimi 生成层（Red Source，非 CDS）**：自 **6-11** 起西班牙夺冠概率冻结于 **23.82%** 且列为 #1（all-paper-claims [R-1]）。这是 kimi 模型聚合输出，早于开赛且全程不变，与 CDS 引擎无关。
- **(b) Polymarket 市场（Internal，非 CDS）**：77 个日度快照显示西班牙夺冠概率约于 **7-18/19 越过 50% 升至 59.05%**（claim-verification §5.1 [I-7]）。这是去中心化预测市场的交易价格，反映资金共识，同样不是 CDS 引擎输出。
- **(c) CDS 引擎（Red Source）**：即上文 0.0325–0.0331 平线。三者来自不同子系统、不同机制、不同时间动态，不可混为一谈。（事实）

**3. git 逐日序列的物理基础成立，但 CDS 维度无转折点可写。**
逐日序列本身真实存在且可独立重建：`cds_championship.json` 在 6-12→7-25 共 **48 个 commit 覆盖 44 个自然日**，仅缺 7-09（Daily CDS Update workflow 失败，有 Gmail 失败邮件 `3ad6419` 互证）与 7-20（当日仅市场快照 `68804b1`）；因 git 内容寻址，任意一天的 tree 均可重建，完整性与不可篡改性由哈希保证（[I-1]/[I-2]/[I-3]；F1 评级 A）。（事实）

换言之，时间序列的**物理基础**是坚实的——但这只证明"有逐日记录"，不证明"记录里有预测信号"。在 CDS 维度上，44 天是一条无拐点的平线，因此"系统哪天开始知道西班牙会赢"这一分析在 CDS 轴上**没有可落笔的转折点**。（观点：平线即无信息量）

**4. 对"系统判定会赢"支撑力的诚实评估。**
CDS 引擎在 n=48 终端结算中 Brier 仅 **0.0195–0.0200**，勉强优于均匀基线 **0.02083**（[I-6]；C18 评级 A）；其过度分散（93.5% 质量压在出局队）与路径级不可靠（R32 对手命中 **5/32 = 15.6%**）已被独立核验（C6/C16；bracket-encoding §2–§3）。这些结构失败进一步说明：CDS 的"西班牙概率"既平且低，无法承担"判定会赢"的语义。（事实）

---

### 三、分析

**为什么平线 ≠ "某天开始判定"。** "判定会赢"至少需要一个可识别的跃迁（概率显著抬升并越过阈值）。CDS 序列缺乏这一形态，因此"某天"在数据中无处安放——这不是遗漏，而是信号本身缺席。把"日更"误读为"日级判断"，是 §3.1 所谓"活系统伪装"第四种死法的标本：刷新时间戳制造了"在思考"的错觉，但内容不变。（观点）

**若论文确需一个"系统开始判定"的转折点，应如何落笔。** 可行替代是改用真正有转折的信号并显式标注来源：(i) **kimi 冻结信号**——以 6-11 锁定 23.82% #1 作为"模型层早于赛果的先验"（[R-1]）；或 (ii) **Polymarket 市场**——以 7-18 越过 50%→59% 作为"资金层在决赛对阵确定时的定价跃迁"（[I-7]）。但二者都须带回 n=1 与幸存者偏差的紧箍咒：本届前四种子的通道设计（FIFA 种子保护，[G-1]，史上首次）抬高了所有重仓前四信号的命中率；佛得角之夜（6-16 西班牙 0-0 被人口 54.6 万队逼平，市场谷底 10.05%）若导致崩盘，同一"盲"即是灾难而非盔甲（[G-6]/[G-7]/[G-8]；claim-verification §6 三重保险）。因此即便采用替代转折点，也只可作描述性素材，不得升格为"系统技能"证据。（观点 + 事实）

**对论文主张的直接冲击。** CDS 维度在"判定西班牙会赢"上**无信息量**，不能为"系统判定会赢"提供证据；任何以 CDS 日更序列支撑该断言的写法，均属把"仪式性更新"误认为"预测行为"。建议论文在方法章或局限章明示：CDS 时间线仅证明基础设施完整（可审计、可重建），不构成预测有效性的证据。（观点）

---

### 四、小结

- **事实**：CDS 西班牙夺冠概率全程 0.0325–0.0331 平线、无赛果通道（C12/R-2）；git 48 commit / 44 天序列真实可重建（F1/I-1）；kimi 6-11 冻结 23.82%（R-1）；Polymarket 7-18 越 50%→59%（I-7）；CDS n=48 Brier 0.0195–0.0200 仅略优于均匀基线（C18）。
- **结论**：用户前提"CDS 引擎某天开始判定西班牙会赢"与数据不符，应予以证伪；CDS 维度无日级转折点可写。
- **处置建议（观点）**：如需"系统开始判定"的转折点，应改用 kimi(6-11) 或市场(7-18) 并显式标注来源，且始终受 n=1 / 种子保护 / 幸存者偏差约束；CDS 时间线仅作基础设施完整性的证据，不承载预测有效性主张。

---

#### 本章来源清单（区分事实/观点标注）

| 来源类别 | 具体出处 | 用途 |
|---|---|---|
| CDS 引擎输出（Red Source） | `ef30658`/`875748b` 西班牙路径概率 0.0325–0.0331 [R-2]；all-paper-claims C12 | 平线证伪主证据（事实） |
| kimi 聚合信号（Red Source） | 西班牙夺冠概率冻结 23.82%、#1、自 6-11 [R-1] | 误读源 (a) 区分（事实） |
| Polymarket 市场（Internal） | 77 个 `market_public_snapshot.json` 日版；7-18 越 50%→59.05% [I-7] | 误读源 (b) 区分（事实） |
| git 历史 / 已结算赛程 | 48 commit/44 天 [I-1]；Gmail `3ad6419`、market `68804b1` [I-2]；git 内容寻址 [I-3]；F1；`923e23a` schedule [I-5/F2] | 物理基础（事实） |
| 外部权威/媒体（Green） | FIFA 官方公告 2025-11-25 [G-1]；Bloomberg/网易/搜狐 佛得角之夜 [G-6][G-7][G-8]；Wikipedia 赛果 [G-11] | 种子保护/幸存者偏差背景（事实） |
| 结构失败核验 | bracket-encoding §2–§3（R32 命中 5/32、版本 #1 0.0484/0.0435 [I-4][I-16]）；n=48 复算 [I-6]；C5/C6/C16/C18 | 支撑 CDS 无信息量（事实） |

> 聚合：6 类来源（CDS / kimi / Polymarket / git·赛程 / 外部权威 / 结构核验），跨 ≥3 类（Red 信号、Internal 仓库物、Green 外部权威），满足 ≥5 源 / ≥3 类要求。

---

## 3. 佛得角之夜的市场情绪再检：谷底 10.05% 的 recency 过调与事后跟随本质

### 第3章 佛得角之夜的市场情绪再检：谷底 10.05% 的 recency 过调与事后跟随本质

> 撰写：topic-researcher-v3（谭溯源分身）｜ 日期：2026-07-27 ｜ 基于 analysis/worldcup-2026 三份证据 memo（只读）｜ 证据纪律：封存仓库零读写、分析副本可写、不输出投注建议、不报告收益率。

### 论点

[事实] 2026-06-16，西班牙在小组赛中被人口仅 54.6 万的佛得角 0-0 逼平（佛得角队史首次晋级世界杯，赛前 Polymarket「西班牙获胜」YES 合约挂约 0.92）。[G-6] 这一单场平局触发了预测市场上「西班牙夺冠」概率的剧烈重定价。

[观点] 本章论点：佛得角之夜构成一处天然实验，用以检验市场情绪的准确性及其对赛果的**前瞻指引**作用；而事后回看，市场谷底 10.05% 是一次典型的 **recency 过度反应**，市场情绪本质上是**结果驱动的事后跟随**，对「事前」结果并不具备可靠指引。该判断为单届（n=1）描述性结论，不得升格为普适定律。

（日期注记：用户在访谈中将该事件记为「6-19」，但已核验的赛事记录与媒体源均指向 2026-06-16；本章统一采用 6-16。）

### 论据

**1. 概率轨迹与时间线。** [事实] Polymarket 上「西班牙夺冠」合约的日度快照（共 77 个 `market_public_snapshot.json` 日版）显示：西班牙夺冠概率自 16.95%（6-12）下行，佛得角平局后的 6-21 跌至 13.65%（失去榜首），**7-01 触谷底 10.05%**，随后修复，7-18 升至 59.05%，决赛后归 100%。[I-7]

**2. 谷底对应的真实赛果。** [事实] 西班牙在佛得角平局之后打出 7 战全胜（4-0 / 1-0 / 3-0 / 1-0 / 2-1 / 2-0 / 1-0）并最终夺冠 [I-7][G-9]；同期高盛给出的西班牙夺冠概率约为 26%，高于市场谷底。[G-9] 一个实际未尝败绩的冠军，却曾在五周内以 10.05% 的谷底价交易——谷底与真实之间存在系统性背离。

**3. 与其他信号的对照。** [事实] kimi 聚合信号的西班牙夺冠概率赛前冻结于 **23.82%**，全程高于市场任何时点，直到决赛日才被市场反超 [R-1]；CDS 引擎给出的西班牙路径概率全程钉死在 **0.0325–0.0331**，每日刷新 `generated_at` 却无赛果通道，是一条不携带信息的平线 [R-2]。三者同台：市场谷底 10.05% / kimi 23.82% / 实际 100% / CDS 0.0325–0.0331。

**4. 市场机制的文献坐标。** [事实] 预测市场价格从链上中央限价订单簿（CLOB）的挂单互动中涌现，反映边际交易者的真金白银信念，而非平台观点或民调 [faction memo §3.1]；约 3% 的交易者贡献了大部分价格发现。Wolfers 与 Zitzewitz（2004）论证市场价格近似为信念的加权聚合；但同一文献传统亦承认预测市场存在 favorite-longshot bias 与对显著性事件的 **recency 过调**（Berg, 2008；Arrow et al., 2008）。佛得角之夜的 −7pp 反应正落在该偏差家族之内。

### 分析

**量化对比（表 1）。**

| 信号 | 西班牙夺冠概率 | 性质 | 与真实 100% 的偏离 |
|---|---|---|---|
| 市场谷底（7-01） | 10.05% | 实时跟随、剧烈波动 | −89.95pp |
| kimi 冻结信号 | 23.82% | 赛前冻结、恒定 | −76.18pp |
| 实际赛果 | 100% | 已结算事实 | — |
| CDS 日更线 | 0.0325–0.0331 | 无赛果通道的仪式性日更 | ≈ −99.97pp |

[观点] 仅就「接近真实」而言，kimi 的 23.82% 比市场谷底 10.05% 更接近 100%——但此比较须加注两层限定：其一，kimi 是**赛前冻结信号**，不参与实时跟随，其「稳定」恰恰源于它不随赛果跳动；它反衬的是市场情绪的**不稳定**，而非证明 kimi 拥有更强的事前洞察。其二，CDS 的平线在数值上最远离真相却也最「稳定」；稳定性本身不等于准确性。故「更接近真实」只成立为 n=1 下的描述性观察。

[事实] 在冠军 log score 维度，kimi 1.44 优于市场 1.78（6-13 快照）；时间积分 log score（6-12→7-19，n=38 快照）市场 1.744 对 kimi 常数 1.435，冻结信号在时间维积分下仍占优；同池多项 Brier 亦为 kimi 0.688 < 市场 0.753 < CDS 0.930 < 均匀基线 0.952 [I-8]。但这些指标同属单届（n=1）描述，且本届前四种子的通道保护（FIFA 制度设计）抬升了所有重仓前四信号的命中率，不可外推为技能断言。

[观点] 市场的「指引」可拆为三段：长期先验（赛前 #1 西班牙）正确；中期修正（中途换王法国，6-21→7-14，持续 24 天的错误定价，且 7-14 半决赛日对两场热门判断全错）错误；终点定价（决赛前 59/40.5）正确但已无信息量。于是市场的实际角色是**结果驱动的事后跟随**——它在半决赛结束后才纠正换王错误，而非事前引领。该结论仅作本届（n=1）描述性素材。

**诚实 caveat（C11）。** [事实] Polymarket 单队 outright 市场的历史订单簿深度与买卖价差无公开逐日回溯渠道——gamma API 对已结算市场不返还历史档 [faction memo §3.3]。因此本处所有市场读数维持「**按收盘价、未做流动性调整**」的声明；流动性量级（佛得角之夜单名交易者亏损约 99 万美元、另一名盈利约 470 万美元）足以排除「薄市场噪声定价」这一主要反驳形态，但无法填补逐日深度缺失 [G-6][G-8]。lead/lag（领先/滞后）分析在本章仅为 n=1 描述，不能外推为通用规律。

### 小结

[事实] 佛得角之夜后，市场将西班牙夺冠概率压至 10.05% 谷底，但西班牙最终 7 战全胜夺冠；kimi 冻结信号 23.82% 全程高于市场谷底，CDS 平线 0.0325–0.0331 不携带信息。[观点] 市场情绪在此表现为 recency 过度反应与结果驱动的事后跟随，对赛果不具备可靠的事前指引——该判断为单届（n=1）描述性结论，不构成普适定律。动态更新并不天然优于静态冻结；更新频率与信息质量是两回事。

---

#### 参考文献（本章引用索引）

**[G-6]** Bloomberg（转述）/ 网易. *A single trader on Polymarket lost nearly $1 million when Cabo Verde fought Spain to a stunning draw*. 2026-06-16. https://www.163.com/game/article/DK3UFFO400318PFH_mobile.html
**[G-8]** 搜狐. 《有人赌西班牙不会获胜赢470万美元,也有人100万美元一夜归零》. https://www.sohu.com/a/1037546979_121384220
**[G-9]** 界面新闻 / 网易. 《从经济学家到AI智能体,谁能算准世界杯？》. https://www.jiemian.com/article/14568476.html ｜ https://www.163.com/dy/article/KV4NDAB80534A4SC.html
**[R-1]** kimi 聚合信号：西班牙夺冠概率冻结 23.82%；冠军 log score 1.44（Red Source，仅参考）。
**[R-2]** CDS 引擎（`ef30658`/`875748b`）：西班牙路径概率全程 0.0325–0.0331，无赛果通道（Red Source）。
**[I-7]** 77 个 `market_public_snapshot.json` 日版：西班牙全轨迹 + 法国时代 + 双半决赛错判。
**[I-8]** `fig6_and_metrics_2026-07-26.py` + `fig6-three-trajectories-2026-07-26.png`：时间积分 log score（市场 1.744 / kimi 1.435）、同池多项 Brier（kimi 0.688 / 市场 0.753 / CDS 0.930 / 均匀 0.952）。
**[faction memo]** `faction-lmu-polymarket-2026-07-26.md`：Polymarket CLOB 机制、recency 偏差、流动性核验（§3.1–§3.3）。
**[Wolfers & Zitzewitz 2004]** Wolfers, J., & Zitzewitz, E. (2004). Prediction markets. *Journal of Economic Perspectives*, 18(2), 107–126.
**[Berg 2008]** Berg, J. E. (2008). Prediction markets: From microcosm to macroeconomy. *Interfaces*, 38(3), 187–188.（另见 Berg, Forsythe, Nelson, & Rietz 关于市场偏差的系列研究）
**[Arrow et al. 2008]** Arrow, K. J., et al. (2008). The promise of prediction markets. *Science*, 320(5878), 877–878.

---

## 4. Polymarket 定价机制与系统性差异假设：CLOB 偏差、n=1 约束与发表价值的边界

### 第4章 Polymarket 定价机制与系统性差异假设：CLOB 偏差、n=1 约束与发表价值的边界

> 工作草稿（intermediate working draft）｜执行：分析副本（只读证据快照）｜本文件不触封存仓库、不输出投注建议、不报告收益率。

### 一、论点（Claim）

**【观点/方向性判断】** 若本算法（kimi 冻结信号）与 Polymarket 定价之间存在*系统性差异*，结合预测市场偏差的经典文献（Hanson, 2003；Wolfers & Zitzewitz, 2004；Arrow et al., 2008；Berg, Nelson & Rietz, 2008），该差异**具备发表价值**——其学术增量主要不在于"谁更准"，而在于可定位"我们的算法在哪些已知的偏差维度上更稳健"。但此价值是**方向性判断**，而非已证实的结论；"系统性差异成立"本身仍是**待检假设**，受 n=1、种子保护与幸存者偏差三保险约束，在单届证据下只能提出、不能定论。

### 二、论据（Evidence）

#### 2.1 Polymarket 定价机制：纯市场水位，非人为设定
**【事实】** Polymarket 现行定价为**链下中央限价订单簿（CLOB）的供需均衡**：YES/NO 份额各 $0–$1、恒满足 1 YES + 1 NO = $1，价格从挂单互动中涌现；显示价在买卖价差 ≤$0.10 时取价差中点，否则取最近成交价（腾讯新闻, 2025-07-31；百度百科, Polymarket 词条）。其早年使用 **LMSR/AMM** 做市（Hanson, 2003），后转向订单簿以提升资本效率（腾讯新闻, 2025-07-31）。结算走 UMA 乐观预言机，平台自身**不设庄家**，不参与对赌（百度百科, Polymarket 词条）。

#### 2.2 概率来源的科学性：有偏但可用的信念读数
**【事实】** 价格是**真实交易者用真金白银挂单形成的边际信念**，不是投票、民调或平台观点（腾讯新闻, 2025-07-31；百度百科, Polymarket 词条）。其聚合机制有文献支撑：Wolfers 与 Zitzewitz（2004）指出，市场生成的价格 ≈ 参与者信念的加权聚合。
**【事实】** 但价格 = **边际价格 ≠ 群体均值**——深钱包的意见权重天然更大（Manski 式质疑，亦见 Wolfers & Zitzewitz, 2004 对"边际信念"的提醒）。
**【事实】** 已知结构性偏差：（a）**favorite-longshot 偏差**，极端价合约系统性错价（Berg, Nelson & Rietz, 2008）；（b）对显著性事件的 **recency 过度反应**。本届即有一例：西班牙在佛得角 0–0 后市场概率从 16.95% 跌至谷底 10.05%，而此后七场全胜夺冠，该 −7pp 下探属过度反应（market-sentiment memo, 2026-07-26）。
**【观点】** 综合判断：Polymarket 价格"是有偏但可用的信念读数——可当基线，不能当神谕"（faction memo, 2026-07-26）。

#### 2.3 本算法与市场的 n=1 描述性对照（非技能断言）
**【事实】** 在本届（n=48 队）结算中：kimi 西班牙冻结概率 23.82% 全程高于市场任何时点直至决赛日；冠军 log score kimi 1.44 < 市场 1.78（越低越好），时间积分 log score 市场 1.744 vs kimi 1.435，同池多项 Brier kimi 0.688 < 市场 0.753（market-sentiment memo, 2026-07-26）。
**【事实】** 市场曾出现持续 24 天的"法国时代"错误定价（6-21→7-14，峰值 39.0%），并在 7-14 双半决赛同时看错热门（法 39.0% > 西 21.1%、英 21.8% > 阿 17.4%，两场均为热门输）（market-sentiment memo, 2026-07-26）。
**【事实】** Polymarket 单队 outright 市场有实质深度：佛得角之夜单名交易者输 $99 万、另一名赢 $470 万，足以排除"薄市场噪声定价"这一主要反驳形态（faction memo, 2026-07-26；Bloomberg/网易/搜狐 报道）。

### 三、分析（Analysis）

**【观点】** 上述对照若能在更大样本上复现，发表价值成立的逻辑链为：Arrow 等（2008）论证预测市场是聚合分散信息最有效的已知机制之一；但 Berg 等（2008）与本届 recency 实例共同表明该机制在极端概率与显著冲击下会偏离无偏。本算法作为*冻结的、非资金驱动的*信念表达，天然不暴露于 favorite-longshot 的资本机会成本扭曲，也不对单场赛果做 recency 追涨——这恰好对应两类已知偏差的"反方向"。因此可把论文增量定位为：**在 favorite-longshot 与 recency 两个维度上，算法相对 CLOB 基线更稳健**，而非泛泛宣称"算法更准"。

**【事实/诚实边界】** 但"系统性差异"目前**尚未做统计检验**。需 paired bootstrap 或多赛事样本方能把"描述性领先"升级为"系统性差异"。在 n=1（仅 2026 单届）下，只能作为**假设**提出。三保险进一步削弱可推论性：
1. **n=1 约束**：单届锦标赛，无法排除单年运气成分；
2. **种子保护（粉笔年结构）**：2026 首次采用网球式种子保护（FIFA, 2025-11-25），前四种子各自赢下小组方进四强，"前四全进四强"部分为制度设计，重仓前四信号的信息量被下调；
3. **幸存者偏差**：算法在已夺冠路径上表现良好，但失败路径未被同等计数。

### 四、小结（Conclusion / 边界声明）

**【观点】** 方向性结论：本算法与 Polymarket 定价的*系统性差异*若经统计检验成立，具发表价值，归属"预测市场偏差文献"脉络（Hanson, 2003；Wolfers & Zitzewitz, 2004；Arrow et al., 2008；Berg, Nelson & Rietz, 2008），增量在"偏差维度定位"而非"谁更准"。

**【事实/边界】** 但必须区分两层，不可混淆：
- **"具发表价值"** = 方向性判断（本文立场）；
- **"系统性差异成立"** = 待检假设，n=1 下未做 paired bootstrap / 多赛事检验，不能作结论。

本章所有算法—市场对照均为 n=1 描述性结果，服务于"提出假设"，不构成"证实优越性"。

---

#### 来源清单（≥5 个不同来源，≥3 类）
1. 腾讯新闻（2025-07-31）．《从AMM到订单簿：探索 Polymarket 定价机制的转变以及与 DEX 结合的可能性》．*新闻媒体*．
2. 百度百科．"Polymarket"词条（CLOB + UMA 乐观预言机、无庄家设定）．*百科*．
3. Hanson, R. (2003). *Logarithmic market scoring rules for modular combinatorial information aggregation*．*学术论文*．
4. Wolfers, J., & Zitzewitz, E. (2004). Prediction markets. *Journal of Economic Perspectives, 18*(2), 107–126．*学术论文*．
5. Arrow, K. J., et al. (2008). The promise of prediction markets. *Science, 320*(5878), 877–878．*学术论文*．
6. Berg, J. E., Nelson, F. D., & Rietz, T. A. (2008). Prediction market accuracy in the long run. *International Journal of Forecasting, 24*(2), 285–300．*学术论文*．
7. 项目内部技术备忘录：`faction-lmu-polymarket-2026-07-26.md`（CLOB 机制、边际信念、佛得角 −7pp、流动性核验）．*内部*．
8. 项目内部技术备忘录：`market-sentiment-and-n48-settlement-2026-07-26.md`（kimi 23.82%、log score、n=48 结算、法国时代与双半决赛错判）．*内部*．

#### 事实/观点标记汇总
- 事实（带源）：§2.1 机制、§2.2 价格=边际信念+两偏差、§2.3 全部量化对照、§3 三保险约束。
- 观点/判断：§1 发表价值方向性、§2.2 末句"可当基线不能当神枢"、§3 增量定位逻辑、§4 方向性结论。

---

## 5. 综合学术价值裁决：四项订正对 Paper A（协议完整性审计 C17）的净冲击

### 第5章 综合学术价值裁决：四项订正对 Paper A（协议完整性审计 C17）的净冲击

> 作者：谭溯源（Tan）· 课题研究员 v5 ｜ 日期：2026-07-27 ｜ 状态：Phase 3.1 中间工作稿（综合裁决章）
> 汇聚依据：V1（分组/组号/法国名次）、V2（CDS 时间线）、V3（佛得角/市场情绪）、V4（Polymarket/系统性差异）四章已审草稿。
> 证据纪律：封存仓库零读写；事实引用复用四章标注；不输出投注建议、不报告收益率。

---

### 一、论点

[观点] 经 V1–V4 四章深度调研，四条新观点对 Paper A 的学术价值构成**净澄清（net clarification）**：排除了 **3 处事实误述**（V1 组号笔误与法国第3、V2 "CDS 判定会赢"）、收紧了 **2 处越界主张**（V3 将市场情绪升格为"事前指引"、V4 将"系统性差异"落定为结论），但 Paper A 的立身之本——协议完整性审计（C17 / Protocol Integrity Vector, PIV）——**不受影响，反而因诚实订正更可辩护**。

[事实] 呼应 W5 系统检索结论：C17 与 prior art **部分重叠**（非空白确认、非撞车）。WorldFork 占 A/D/E/F、SourceBench 占 B、ContractBench 占 E、LMU *LLM-SoccerArena* 占 ex-ante+schema+协议失败诊断；但**无单一工作把六维打包为封闭一等评估对象**，且 B（来源分级）/C（快照漂移）为体育预测域空白，构成本工作增量（V1 §三.D，依据 `all-paper-claims-master` C17/W5）。四章订正**不改变**该判定：C17 须持续表述为"体育预测域首次六维整合闭集（B/C 为本工作增量）"。

---

### 二、论据

#### 2.1 四项订正汇总表

| 订正条目 | 类型 | 对 Paper A 的冲击评级 | 关键事实（复用章节标注） |
|---|---|---|---|
| V1 组号 H/I、法国【第4】、同半区 | **事实订正** | **负向·须订正**（组号笔误、法国名次错） | 西班牙=H、法国=I（GMW/中青报）；法国三四名决赛 6–4 负英格兰→**实际第4**（V1 §二.2/5，icoachfootball/腾讯） |
| V2 CDS 平线证伪"系统判定会赢" | **事实订正** | **负向·须移除承重断言** | CDS 西班牙概率全程 0.0325–0.0331 无赛果通道（V2 §二.1，C12/R-2）；"某天开始判定"在数据上无处安放 |
| V3 市场情绪事后跟随（非事前指引） | **边界澄清** | **中性·收紧越界** | 谷底 10.05%=recency 过调，kimi 23.82% 较市场更接近真实；但属 n=1 描述（V3 §三，[I-7]/[R-1]） |
| V4 系统性差异=待检假设（非定论） | **边界澄清** | **中性·收紧越界** | 发表价值=方向性判断；"系统性差异成立"须 paired bootstrap/多赛事检验，n=1 下仅能提出（V4 §三/§四） |

[事实] 评级说明：V1、V2 属"事实订正"（数据/赛果层矛盾，直接否定原文承重写法）；V3、V4 属"边界澄清"（方向性判断与假设边界，不需删事实，须把越界主张降格）。

#### 2.2 X1.1 收口：用户"赛制感知命中"论点的四道硬伤

用户主张："若把概率丢进分组，我们命中率更高——西班牙第一+法国最佳第三，证明我们命中了冠亚季军。"[观点] 该论点须**显式反驳**，四道硬伤齐备：

- **(a) 事实崩。** 法国实际为**第4**（三四名决赛英格兰 6–4 法国），亚军为**阿根廷**、季军为**英格兰**（V1 §二.5）。"命中季军"在事实上即错——根本不存在"法国第三"。
- **(b) 循环论证 / 事后合理化。** 该论点用**赛后实际冠军**（西班牙）反推"法国第三"、再将其算作"我们命中"。这违反本研究的**赛前冻结原则**（ex-ante freeze），是用已知结果反构命中，典型**幸存者偏差**（V1 §三.C；claim-verification §6 三重保险）。
- **(c) 反暴露软肋（最致命）。** 原模型给"法国第二"，但在固定 bracket 同半区约束下，"西班牙夺冠"与"法国第二"**互斥**——同半区中西班牙若夺冠，法国最早仅半决赛相遇、至多第三（V1 §二.1/4，BBC）。这说明原概率是**边际排名概率**，未建模赛制路径。故"叠加赛制"不是增益，而是**暴露原模型漏了路径建模**；把漏洞补上才算方法贡献，不能用它反证"命中更强"。
- **(d) 基准率不消失。** 本届为**粉笔年**（四种子全进四强）+ kimi/市场 top-5 同中 4/4（V1 §三.C；C1），"5 热门中 4 强"在制度与市场双重共识下**本近无信息量**。换一种表述（"丢进分组命中更高"）不能凭空造出信息。

[观点·正确写法] "赛制感知结算（bracket-aware settlement）"应被定位为协议完整性审计（C17）的**新增一等字段 / 方法贡献**——即在六维闭集中补入"赛制路径约束"作为结算与校验维度，从而让 ex-ante 冻结概率与真实 bracket 落位可对照。**它提升的是审计方法学的完备性，而非"命中冠军"的证据权重**。任何试图用它抬高"我们命中了冠亚季军"的写法，均须删去。

---

### 三、分析

[观点] **净冲击的分解。** 四条订正中，V1、V2 直接削减 Paper A 的事实面承重（组号/名次笔误、CDS "判定会赢"断言）；V3、V4 仅收紧主张边界（市场情绪→n=1 描述、系统性差异→待检假设）——二者均不触及方法学内核。四章**无任何一条**能动摇 C17：PIV 的六维整合闭集与来源分级/快照漂移增量，独立于"谁命中冠军""CDS 是否判断会赢"等叙事钩子。

[观点] **诚实订正的复利效应。** 把"命中"降为 hook、把 CDS 平线降为基础设施完整性证据、把市场情绪与市场差异放回"n=1 描述 + 待检假设"，表面是"让利"，实则消解了审稿人最易攻击的三类 overclaim（事实错、因果反推、外推定论）。C17 在 W5 已裁定"部分重叠"，本综合章将其锁定为"体育预测域首次六维整合闭集"——这一降级式诚实表述，使 Paper A 在重压下仍**可辩护**（defensible），恰是审计链诚实方法学（audit-trail honesty）的自证。

[观点] **X1.1 的归宿。** 用户论点虽被四道硬伤反驳，但其直觉——"赛制路径影响概率结算"——有真实方法学价值，应转化为 C17 的 bracket-aware 字段，而非保留为"命中证据"。这既回应了用户关切，又守住证据纪律。

---

### 四、小结

[观点] 总体裁决：V1–V4 四项新观点经深度调研，对 Paper A 构成**净澄清**——排除 3 处事实误述（V1 组号/法国名次、V2 CDS 判定断言）、收紧 2 处越界主张（V3 事前指引、V4 系统性差异定论）。**C17 协议完整性审计与审计链诚实方法学不受影响，反而因诚实订正更可辩护**。X1.1 "赛制感知命中"论点被四道硬伤（事实崩 / 循环论证 / 反暴露软肋 / 基准率）显式驳回，其合理内核改为 C17 的 bracket-aware 一等方法贡献。Paper A 的立身之本稳固。

---

#### 本章来源清单（复用 V1–V4 标注，无新增外部源）
- 本章所有事实引用均来自 V1–V4 四章已审草稿及其标注：`all-paper-claims-master-2026-07-26.md`（C1/C10/C12/C17/W5）、`claim-verification-with-footnotes-2026-07-26.md`（§0/§5/§6）、`bracket-encoding-verification-2026-07-26.md`、`market-sentiment-and-n48-settlement-2026-07-26.md`、`faction-lmu-polymarket-2026-07-26.md`，及 GMW/中青报/icoachfootball/腾讯/BBC 等外部核验源（详见各章来源清单）。
- **本章新增来源：无。**（综合章仅汇聚四章已含标注，未引入新外部文献。）

---

## 结论

综合五章调研，四项主张经检验后呈现清晰分层：3 处事实误述被订正、2 处越界主张被收紧。事实层，组号误述（西 H / 法 I 而非 E/D）、法国名次误述（实际第 4 而非第 3）、以及「CDS 某天判定会赢」断言（全程 0.0325–0.0331 平线、无拐点）均被否证。边界层，佛得角之夜市场谷底 10.05% 定性为 recency 过度反应与结果驱动的事后跟随，不得升格为「事前指引」；算法与 Polymarket 的「系统性差异」仅为 n=1 下的待检假设，须 paired bootstrap 或多赛事检验方能定论。

在这场净澄清中，Paper A 的立身之本——协议完整性审计（C17 / PIV）——维持「部分重叠」判定且不受影响。W5 系统检索显示 WorldFork、SourceBench、ContractBench、LMU LLM-SoccerArena 各覆盖六维中若干维，但无单一工作把六维打包为封闭一等评估对象，且来源分级/快照漂移为体育预测域空白。故 C17 须诚实表述为「体育预测域首次六维整合闭集」。

最后收口 X1.1「赛制感知命中」论点：用户以「西班牙第一+法国第三」反证命中，存在事实崩、循环论证、反暴露软肋与基准率消失四道硬伤，须显式驳回。其合理内核应转化为 bracket-aware settlement（赛制感知结算）作为 C17 新增一等字段——它提升审计方法学完备性，而非提升「命中冠军」证据权重。诚实订正之后，Paper A 根基稳固。

---

## 参考文献

### 学术文献
- Arrow, K. J., et al. (2008). The promise of prediction markets. *Science, 320*(5878), 877–878.
- Berg, J. E. (2008). Prediction markets: From microcosm to macroeconomy. *Interfaces, 38*(3), 187–188.
- Berg, J. E., Nelson, F. D., & Rietz, T. A. (2008). Prediction market accuracy in the long run. *International Journal of Forecasting, 24*(2), 285–300.
- Dixon, M. J., & Coles, S. G. (1997). Modelling association football scores and inefficiencies in the football betting market. *Journal of the Royal Statistical Society: Series A, 160*(3), 389–398.
- Hanson, R. (2003). Logarithmic market scoring rules for modular combinatorial information aggregation. *Journal of Prediction Markets, 1*(1), 3–20.
- Murphy, A. H., & Winkler, R. L. (1977). Reliability of subjective probability forecasts. *Journal of the American Statistical Association, 72*(359), 609–616.
- Wolfers, J., & Zitzewitz, E. (2004). Prediction markets. *Journal of Economic Perspectives, 18*(2), 107–126.

### Prior art
- ContractBench (2026). *arXiv:2605.17281*.
- LMU LLM-SoccerArena (2026). LLM soccer arena: Ex-ante evaluation of language models on soccer prediction.
- SourceBench (2026). *arXiv:2602.16942*.
- WorldFork (2026). ICML 2026.

### 官方与媒体
- BBC Sport (2025). *World Cup draw 2026: Format, start time, seeding, pots & dates*. https://www.bbc.com/sport/football/articles/c997y4l20jgo
- FIFA (2025-11-25). *Procedures for the Final Draw for the FIFA World Cup 2026™ revealed*. https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw
- 光明网 (2025-12-06). *2026美加墨世界杯分组抽签结果出炉*. https://m.gmw.cn/2025-12/06/content_1304252440.htm
- 中国青年报 (2025-12-06). *姆巴佩"对话"哈兰德!2026年美加墨世界杯分组抽签结果出炉*. https://m.cyol.com/gb/articles/2025-12/06/content_YOMajAsmpZ.html
- 新华网 (2025-11-26). *2026世界杯抽签：种子保护制度首次采用*. https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html
- icoachfootball (2026). *World Cup 2026 Winner: Spain, Full Bracket, Groups & Results*. https://www.icoachfootball.net/world-cup-2026-knockout-bracket/
- 腾讯新闻 (2026). *西班牙1-0艰难战胜卫冕冠军阿根廷…半决赛西班牙2-0法国*. https://so.html5.qq.com/page/real/search_news?docid=70000021_2636a5d522730452
- 腾讯新闻 (2025-07-31). *从AMM到订单簿：探索 Polymarket 定价机制的转变以及与 DEX 结合的可能性*.
- 百度百科. *Polymarket* 词条.
- 网易 (2026-06-16). *A single trader on Polymarket lost nearly $1 million when Cabo Verde fought Spain to a stunning draw*. https://www.163.com/game/article/DK3UFFO400318PFH_mobile.html
- 搜狐 (2026). *有人赌西班牙不会获胜赢470万美元,也有人100万美元一夜归零*. https://www.sohu.com/a/1037546979_121384220
- 界面新闻 (2026). *从经济学家到AI智能体,谁能算准世界杯？*. https://www.jiemian.com/article/14568476.html
- 网易 (2026). *从经济学家到AI智能体,谁能算准世界杯？*. https://www.163.com/dy/article/KV4NDAB80534A4SC.html
- Wikipedia (2026). *2026 FIFA World Cup*. https://en.wikipedia.org/wiki/2026_FIFA_World_Cup

### 项目内部
- `all-paper-claims-master-2026-07-26.md`（封存仓库冻结版 / 证据快照）
- `claim-verification-with-footnotes-2026-07-26.md`（封存仓库冻结版 / 证据快照）
- `bracket-encoding-verification-2026-07-26.md`（封存仓库冻结版 / 证据快照）
- `market-sentiment-and-n48-settlement-2026-07-26.md`（封存仓库冻结版 / 证据快照）
- `faction-lmu-polymarket-2026-07-26.md`（封存仓库冻结版 / 证据快照）
- `fig6_and_metrics` (2026-07-26)（封存仓库冻结版 / 证据快照）
- CDS 引擎快照 `ef30658` / `875748b`（封存仓库冻结版 / 证据快照）
- kimi 聚合信号快照（封存仓库冻结版 / 证据快照）
- Polymarket 市场快照 `market_public_snapshot.json`（封存仓库冻结版 / 证据快照）
- 已结算赛程 `923e23a:data/processed/schedule.json`（封存仓库冻结版 / 证据快照）

---

> 本报告由 AI 深度研究团队生成，重要决策请经专业人员核验。所有引用来源请用户在重要场景下二次核验时效性与真实性。

> 各章经明鉴秋 6 维审稿 1 轮通过，无遗留修订项。
