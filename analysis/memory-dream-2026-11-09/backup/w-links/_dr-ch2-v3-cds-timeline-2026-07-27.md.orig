# 第2章 西班牙夺冠时间线——系统从哪一天开始判断出西班牙会赢

> 重建说明：本章为会话压缩丢失后的落盘重整合（v3），全部事实底座取自冻结证据快照与权威工作文件（Green），模型类读数注明冻结版本（Red）。未做任何重新发散搜索。

## 论点

本章回应论文「四个新观点」中一类典型时间线主张——即"CDS（路径空间引擎）从某一天开始判定西班牙会夺冠"。核心论点分三层：

1. **CDS 维度，前提不成立**。在 CDS 系统里，西班牙的夺冠概率全程是一条 **0.0325–0.0331** 的平线，没有任何日级拐点；"CDS 从某天开始判定西班牙会赢"这一说法缺乏事实支撑。
2. **方法论维度，问题本身 ill-posed**。提问者把三个相互独立的系统——**kimi 冻结信号**、**Polymarket 预测市场**、**CDS 枚举式路径引擎**——的读数混为一谈，制造出并不存在的"早判西班牙"时间线。
3. **排名维度，西班牙从未高位**。即便在最宽容的解读下，CDS 也从未把西班牙置于榜首：2026-07-19 快照中塞内加尔以 **0.0446** 名列第一，西班牙（0.03302）从未独占高位，且引擎自身的末端模态决赛预测是"英格兰 vs 法国"，而非西班牙夺冠。

## 论据

**论据 1（CDS 平线，无日级拐点）**。【Green】封存仓库 git 历史可重建 CDS 日版序列（2026-06-12→07-25，44 个有效日、48 个 commit，缺 7-09 与 7-20 两个无 CDS commit 日）([市场情绪分析 + 四项注脚核验 memo §1.1](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))。分析副本对此序列的判读是：CDS 的日更冠军概率线"全程平坦"，"没有赛果通道的'日更'只是仪式"([同 memo §2.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))。锁定快照 `cds_championship.json`（2026-07-19）给出 Spain `championship_prob = 0.03302`([cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json))，落在 0.0325–0.0331 区间内，确属平线、无拐点日。

**论据 2（西班牙从未独占高位）**。【Green】同一快照中 **Senegal = 0.0446，排名 #1**([cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json))。即 CDS 的"头号热门"是一个实际在 R32 就被比利时 2–3 淘汰的队伍（塞内加尔出局见 [市场 memo §1.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)）。其机制是：引擎对塞内加尔的五个节点胜率全在 0.483–0.515（掷硬币级），归一化把"噪声最大值"加冕为头号热门([同 memo §1.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))——CDS 并非"判断"出塞内加尔，而是没有判断力、又把无判断力伪装成了观点。西班牙 0.03302 在该版本中连榜首都不是。

**论据 3（三系统混淆：kimi 与 Polymarket 被误读为 CDS）**。用户常把两类外部读数误当成"CDS 判定西班牙"：
- **(a) kimi 冻结信号**。【Red·冻结 6-11】300 智能体面板中西班牙为夺冠模态（**62/300 ≈ 20.7%**，[kimi_agent_inventory.csv](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv)）；单模型西班牙概率 **23.82%** 自 6-11 起冻结、全程静态([市场 memo §2.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md))。
- **(b) Polymarket 预测市场**。【Green】`market_public_snapshot.json`（2026-07-19，来源 `polymarket_gamma_public_search`）显示 **Spain 59.05% / Argentina 40.95%**([market_public_snapshot.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json))，但这是决赛对阵已定后的市场定价；市场全轨迹显示西班牙概率直到 **2026-07-18** 才越 50%（[市场 memo §2.1/§2.2](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)），此前还经历了"法国时代"（6-21→7-14，峰值 39.0% @ 7-14）并两次半决赛错判（7-14 法国 39.0 > 西班牙 21.1；英格兰 21.8 > 阿根廷 17.4，两场热门均输）。

CDS、kimi、Polymarket 是三个**生成机制完全不同**的系统（枚举路径模型 / 冻结静态面板 / 真金白银动态市场），读数不可互通，混用即产生伪时间线。

**论据 4（引擎末端预测并非西班牙）**。【Green】路径空间引擎的模态决赛预测为"**英格兰 vs 法国**"，R32 对手命中率仅 5/32（15.6%），实际决赛为西班牙 vs 阿根廷([bracket-encoding-verification memo §2(iii)](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md))。即引擎自身"末端输出"都不是西班牙夺冠，进一步证伪"系统判定西班牙会赢"的叙事。

## 分析

**为什么"某天判定"是伪问题。** CDS 的输出是枚举路径树后的归一化质量分配，其节点胜率被赋予约 0.50（例：Czech vs Senegal `win_prob 0.50`，[市场 memo §1.3](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)），导致质量沿路径树近均匀扩散（[bracket memo §4.1](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)）。在这种机制下，西班牙夺冠概率稳定在 ~0.033 是**结构使然**，而非"判断使然"——不存在一个由赛果驱动的"拐点日"。日更只是仪式，已为本届结算所印证（CDS Brier 0.0195–0.0200，仅勉强低于均匀基线 0.02083，[市场 memo §1.4](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)）。

**三系统的可区分性（若必须给时点）。** kimi（冻结静态面板，23.82% 自 6-11 持续领先）回答的是"赛前/静态共识"；Polymarket（动态市场，7-18 跳变 >50%）回答的是"资金在决赛对阵确定后的重新定价"；CDS（~0.033 平线）回答的是"枚举式路径模型的结构性质量分配"。把三者叠加，会人为制造出并不存在的"CDS 早判西班牙"时间线。

**制度层注脚。** 2026 世界杯史上首次采用网球式种子保护，FIFA 官方确认四支最高排名球队（西班牙/阿根廷、法国/英格兰）分入不同半区路径，以"确保 competitive balance"（[FIFA 官方抽签程序](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw)）。这意味着"前四进四强"含制度设计成分（[市场 memo §1.2](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md)），进一步削弱任何"某系统独具慧眼提前锁定西班牙"的叙事。

## 小结

无法指认"系统从某天开始判定西班牙会赢"的时点。**三重证据一致否定该前提**：CDS 冠军概率全程 0.0325–0.0331 平线、西班牙从未独占高位（塞内加尔 0.0446 #1）、且引擎末端模态决赛为"英格兰 vs 法国"。若研究必须给出一个"西班牙被看好"的时点，须严格区分两个**异质且皆非 CDS** 的来源：
- **kimi 冻结信号**：6-11 起 23.82% 持续领先（【Red·冻结 6-11】）；
- **Polymarket 市场**：7-18 跳变越 50%（【Green】）。

二者都不支持、也不应被转述为"CDS 早判西班牙"。论文中任何"CDS 于某日判定西班牙夺冠"的表述，建议一律改写为"三个系统的西班牙读数需分别标注，CDS 维度无此判定"。

---

## 关键发现

- 发现 1：CDS 西班牙夺冠概率 2026-07-19 快照为 0.03302，处于全程 0.0325–0.0331 平线，无日级拐点（[cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)【Green】）。
- 发现 2：同一快照中塞内加尔 0.0446 排名 #1，西班牙从未独占高位（[cds_championship.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json)【Green】）。
- 发现 3：kimi 300 智能体面板西班牙为夺冠模态（62/300），单模型概率 23.82% 自 6-11 冻结（[kimi_agent_inventory.csv](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv)【Red·冻结 6-11】）。
- 发现 4：Polymarket 西班牙概率 2026-07-19 为 59.05%，但仅于 7-18 越 50%（决赛对阵确定后），属市场动态重定价（[market_public_snapshot.json](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json)【Green】）。
- 发现 5：路径引擎模态决赛预测为"英格兰 vs 法国"，非西班牙夺冠（[bracket-encoding-verification memo §2(iii)](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md)【Green】）。

## 数据摘要

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

## 本章新增来源清单（供主理人更新来源池）

1. [cds_championship.json（2026-07-19 冻结快照）](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/cds_championship.json) — Green：Spain 0.03302、Senegal 0.0446（#1），CDS 冠军概率平线证据底稿。
2. [market_public_snapshot.json（2026-07-19 Polymarket 快照）](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/market_public_snapshot.json) — Green：来源 polymarket_gamma_public_search，Spain 59.05% / Argentina 40.95%，证明该读数属市场而非 CDS。
3. [kimi_agent_inventory.csv（300 智能体面板）](evidence/cds4worldcup-snapshot-2026-07-20/worktree/data/processed/kimi_agent_inventory.csv) — Red·冻结 6-11：西班牙为夺冠模态（62/300）。
4. [bracket-encoding-verification-2026-07-26.md](analysis/worldcup-2026/bracket-encoding-verification-2026-07-26.md) — Green 工作文件：模态决赛预测"英格兰 vs 法国"、R32 命中率 5/32、bracket 编码核验。
5. [market-sentiment-and-n48-settlement-2026-07-26.md](analysis/worldcup-2026/market-sentiment-and-n48-settlement-2026-07-26.md) — Green 工作文件：CDS 日更线平坦、kimi 23.82% 冻结、Polymarket 轨迹与"法国时代"、n=48 结算。
6. [Procedures for the FIFA World Cup 2026 Final Draw revealed（FIFA 官方）](https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw) — 机构/官方：确认四支最高排名球队分入不同半区路径的种子保护规则（制度层注脚）。
7. [世界杯推动预测市场交易额大增，多平台显示今年冠军将是这只劲旅（财联社/搜狐）](https://www.sohu.com/a/1046568007_222256) — 媒体/行业：报道 Polymarket 世界杯冠军市场（7 月初法国 35.4% 领先、西班牙 12.4%），佐证"法国时代"与市场动态属性。
