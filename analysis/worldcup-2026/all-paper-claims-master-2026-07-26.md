# 论文观点总清单（全 28 条）+ 逐条注脚 + 诚实证据评级

> 执行：分析副本任务（MANIFEST 第三级）｜ 日期：2026-07-26
> 范围：扫描 `analysis/worldcup-2026/*`、`docs/plans/*`、`docs/investigations/*`、`research/*` 与对话记录，枚举我们提出的全部论文观点，逐条补注脚、给证据评级，并诚实标注"无证据 / 事实错误 / 待验证"。
> 纪律：封存仓库（`~/Documents/GitHub/cds4worldcup`）零读写；本文件写于分析副本；中文源仅作背景注脚，不引入新数字主张。

---

## 0. 总计数与口径说明

| 类别 | 数量 | 说明 |
|---|---:|---|
| **C 类 · 承重实证观点** | **18** | `redteam-claims-dual-lens` 已裁决的 C1–C18（关于"发现了什么"） |
| **F 类 · 基础事实底座** | **2** | 论文依赖但 redteam 未单列的事实（git 逐日序列、赛程冻结版） |
| **S 类 · 战略性定位观点** | **10** | 散落开题/计划/大纲/对话中的"怎么写/怎么定位"决策（非承重主张） |
| **合计** | **30** | 其中 C18 + F2 与既有"5 项主张报告"重叠（见 §6 映射） |

**评级含义**（redteam 双视角裁决）：
- **A / A−**：站得住（负结果 / 方法 / 基础设施类，攻击后仍存）
- **B / B+**：条件站住（描述性，须带全部紧箍咒）
- **C**：站不住（不得作为承重主张，仅可作插图 / 讨论 / hook）

**诚实标记**（本清单新增，逐条标注）：
- ✅ 有证据（仓库内可复算或外部权威源）
- ⚠️ 待验证（依赖未过闸门的事实，投稿前须补）
- ❌ 无证据（仅对话提及或来源缺失，不得写入论文）
- 🔁 口径澄清（数字"打架"经查非错误，而是口径不同）

---

## 1. 注脚约定

- **[G-n]** Green Source：事实性外部权威（FIFA 官方、已核验赛程、主流媒体、可引用文献）
- **[R-n]** Red Source：模型/信号输出（kimi 聚合、CDS 引擎），仅可参考、不可作承重证据
- **[I-n]** Internal：仓库内可复算物（git 历史、快照、截图索引、已结算赛程、复算脚本）
- **冻结版本**：赛程 `923e23a`（Green，Wikipedia 已核验）；CDS `ef30658`（归一化前）/ `875748b`（归一化后）；kimi 西班牙夺冠概率冻结于 23.82%

---

## 2. 承重实证观点 C1–C18（逐条）

### C1 ｜ kimi 前五中四（top5 含全部四强）
**表述**：kimi 冠军基线前五 = 西/法/阿/葡/英，其中西/法/阿/英全部进入四强（4/4）。
**注脚**：[I-1] kimi `kimi_agent_inventory.csv` 冠军基线 top5；[I-9] 市场 6-11 快照 top5 同中 4/4（`worldcup-paper-topic` §1.4）；[G-1] FIFA 种子保护（前四通道设计）压低信息量；[R-1] kimi 属 Red Source。
**评级**：**B**（描述性 hook，非技能断言）
**诚实标记**：⚠️ "市场同中 4/4" 内部源有，但与 kimi 同集合、均被种子保护放大 → 信息量极低；**不得作为"预测能力"证据**，仅可作引言 hook（paper-a-skeleton §1）。

### C2 ｜ kimi 压中冠军（西班牙 23.82% #1）
**表述**：kimi 把西班牙列为夺冠概率第一（23.82%）。
**注脚**：[R-1] kimi 聚合信号冻结 23.82%（Red Source）；[I-10] 对话提及"Fox 全粉笔年也中"——**仅对话，无独立来源**。
**评级**：**B**（同 C1，hook 层级）
**诚实标记**：❌ "Fox 全粉笔年也中冠军"**无证据**，仅对话提及，投稿前须删除或补源；n=1，不构成技能验证。

### C3 ｜ kimi vs 市场三项对照（log / 多项 Brier / 时间积分）
**表述**：kimi 在冠军 log score（1.44<1.78）、同池多项 Brier（0.688<0.753）、时间积分 log score（1.435<1.744）三项均优于市场。
**注脚**：[I-8] `fig6_and_metrics_2026-07-26.py` + `fig6-three-trajectories-2026-07-26.png`：市场 1.744 / kimi 1.435、多项 Brier kimi 0.688 / 市场 0.753；[R-1] kimi；[I-9] 快照时点敏感。
**评级**：**B+**（三项互证强于单点，可入描述层）
**诚实标记**：⚠️ 单一结果向量、日度观测自相关（有效 n≈1）、快照时点敏感——三项一致是亮点但**仍属 n=1 描述性**。

### C4 ｜ 偏离方向命中率（5 对 / 1 平 / 2 错）
**表述**：同池重归一后 kimi 两处偏离方向 ex post 全对（阿根廷↑+11.7pp、葡/巴/荷↓），错在法国↑/英格兰↓，平西班牙↑；5/1/2 全表。
**注脚**：[I-11] kimi 21 队池内重归一偏离方向表（`worldcup-paper-topic` §1.4）；[I-12] "今年中档热门集体低迷→下调策略躺赢"为描述性解释，**无因果源**。
**评级**：**B**（须全表呈报，只报对的两条=摘樱桃）
**诚实标记**：⚠️ "中档热门低迷导致下调躺赢"是事后解释，无独立证据；n=8 样本小。

### C5 ｜ CDS `ef30658` 西班牙 #1（归一化前）
**表述**：归一化前版本西班牙排 #1（0.0484）。
**注脚**：[I-4] `ef30658:data/processed/cds_championship.json` path_nodes；[I-5] 归一化后头号变塞内加尔（`875748b`）。
**评级**：**C**（只能作为版本史事实，不作主张）
**诚实标记**：⚠️ 版本选择风险——挑哪版说话？**不得作为承重主张**；论文禁用"CDS 预测了冠军"。

### C6 ｜ CDS 过度分散 + 塞内加尔机制解剖
**表述**：CDS 把 93.5% 夺冠质量压在出局队；塞内加尔五节点胜率 0.483–0.515（≈掷硬币），归一化把噪声最大值加冕为头号热门（#15→#1）。
**注脚**：[I-4] `ef30658`/`875748b` path_nodes 五节点 + #15→#1 跃迁；[I-5] `923e23a` KO81 Belgium 3–2 Senegal（R32 出局，且首对手捷克都错）；[I-6] n=48 复算（93.5% 质量）。
**评级**：**A**（机制可复算、n=46 结构性、自我证伪——攻击反而加固）
**诚实标记**：✅ 仓库内完全可复算；是 H3"结构失败模式"的具尸检。

### C7 ｜ 硬选准确率–Brier 排名反转（Coach vs Elo）
**表述**：Coach 硬选 59.7% > Elo 54.9%，但 Brier（0.6078 vs 0.5728）与 Log Loss（1.0113 vs 0.9410）均更差。
**注脚**：[I-12] `worldcup-paper-topic` §1.2 结算表；[G-10] Murphy & Winkler (1977) *JASA* 早已指出 accuracy 与 proper score 可背离。
**评级**：**C**（仅插图，教科书已知）
**诚实标记**：⚠️ 非新发现，是已知统计现象；论文仅当插图/分量表征，不得作标题或"过度自信"证据。

### C8 ｜ Elo 平局系统性低估
**表述**：Elo 平均平局概率低于实际约 −8.3pp（全赛段）；MD1 单轮 −17.6pp。
**注脚**：[I-13] `worldcup-paper-topic` §1.2（全赛段 −8.3pp，主胜 +10.9pp）；[I-14] `2026-07-08-group-stage-72-match-evaluation.md` 第 301 行（"整体 −8.3pp、MD1 −17.6pp"）；[G-10] Dixon & Coles (1997) *JRSS A* 低分修正文献锚。
**评级**：**A−**（机制 + 多 matchday 一致 + Poisson 独立性解释）
**诚实标记**：🔁 **数字"打架"经查非错误**——redteam 写"MD1 −17.6pp"、topic 写"全赛段 −8.3pp"，二者并存于证据文件第 301 行，是口径不同（单轮 vs 全程），非事实矛盾。Plan C 3/3 全平局为预注册 replication（[I-15] 结算时间戳验证）。

### C9 ｜ bracket 编码结构正确（半区约束可达）
**表述**：CDS 的 bracket 编码经事后核验结构正确（两个半决赛对阵在其路径结构中从被淘汰方视角可达），但路径级预测不可靠（R32 对手命中率 5/32=15.6%）。
**注脚**：[I-16] `bracket-encoding-verification-2026-07-26.md` §2–§3（France 优势路径含 SF:Spain✓；England 路径含 QF:Norway✓+SF:Argentina✓）；[I-5] R32 对手命中 5/32。
**评级**：**A−**（协议元素，编码正确是义务）
**诚实标记**：✅ 工程核验；**禁用表述**："预测了决赛/半决赛对阵"（模态决赛错误）；"半区规则知识作为命中证据"（编码正确是建模义务）。

### C10 ｜ FIFA 种子保护是制度设计（史上首次）
**表述**：2026 世界杯史上首次网球式种子保护，前四种子分入不同半区、半决赛前不相遇，为制度设计非巧合。
**注脚**：[G-1] FIFA 官方公告（2025-11-25，《Procedures for the Final Draw…revealed》"for the first time in World Cup history"）；[G-3] 新华网 2025-11-26 中文报道；[G-4][G-5] 微信公众号「说个足球」「你挑的吧偶像」 corroboration；[G-2] ESPN 抽签规则详解（2025-12-05）。
**评级**：**A**（来源实锤，防自吹的基准率下调器）
**诚实标记**：✅ 外部权威源完备；含义：任何重仓前四的信号 4/4 命中信息量进一步下调。

### C11 ｜ 市场"法国时代" + 双半决赛错判
**表述**：市场 6-21→7-14 把头号热门换成法国（峰值 39.0%），并在 7-14 两场半决赛前一天同时看错两个热门（法>西、英>阿，两场均热门输）。
**注脚**：[I-7] 77 个 `market_public_snapshot.json` 日版（全轨迹 + 法国时代 + 双错判）；[G-6][G-7][G-8] 佛得角之夜 Polymarket 盈亏（Bloomberg/搜狐/网易）；[I-17] **流动性声明**：Polymarket 单队 outright 流动性/价差未核验，引用"错价"须加"按收盘价读数、未做流动性调整"。
**评级**：**B+**（市场微观结构描述，挂行为金融文献）
**诚实标记**：⚠️ 流动性未调整，n=1；属"流量层子弹"，不得升格为方法主张。

### C12 ｜ CDS 平线 / 仪式性日更（无赛果通道）
**表述**：CDS 西班牙概率全程钉死 0.0325–0.0331，每日 generated_at 刷新但无赛果通道——"每日更新"实质是仪式。
**注脚**：[R-2] CDS `ef30658`/`875748b` 西班牙路径概率 0.0325–0.0331；[I-8] 去时间戳哈希恒定（机器可复算）；提出第九 PIV 字段。
**评级**：**A**（可机器复算，§3.1"活系统伪装"第四种死法标本）
**诚实标记**：✅ 完全可复算；是方法贡献（PIV 字段设计）的实证基础。

### C13 ｜ 证据链五层（git / Actions / Gmail / Wayback / OTS+TSA）
**表述**：预测资产由 git 哈希 + GitHub Actions + Gmail 失败邮件 + Wayback 第三方存档 + OTS/FreeTSA 时间戳五层独立互证，构成可审计证据链。
**注脚**：[I-18] git 内容寻址 + Actions 148 条 + Gmail `3ad6419` 失败通知 + Wayback C14 存档 + OTS/FreeTSA 锚定收据（`evidence/cds4worldcup-timestamp-anchors-2026-07-25/`）。
**评级**：**A**（层层可独立核验，主动披露破口与阴性结果）
**诚实标记**：✅ 论文"区块链存证"传播点；但须如实披露破口（每日漂移、PIV 新实例）。

### C14 ｜ kimi 聚合 21/21 复算
**表述**：kimi 冠军基线前五名单可从 `kimi_agent_inventory.csv` 逐字节复算（21/21 一致）。
**注脚**：[I-19] 聚合层 0.05pp 容差复算通过；[R-3] **生成层模型版本不可考**（上游 `worldcup-kimi/` 在 gitignored 区，溯源完整性待验证）。
**评级**：**A**（聚合层）
**诚实标记**：⚠️ 生成层模型版本不可考已登记降级；kimi 仍属 Red Source，不得作承重证据。

### C15 ｜ "先验即预测"哲学框架
**表述**：佛得角之夜显示"盲者胜明眼人"——prior was the prediction，更新频率≠信息质量。
**注脚**：[I-7] 市场谷底 10.05% 对应实际全胜冠军；[I-20] **反例**：市场终点修正（决赛前 59/40.5）有效，说明先验非永远正确。
**评级**：**B**（讨论章一段，配反例）
**诚实标记**：⚠️ 哲学不是证据；须配反例（市场终点修正有效），不得作为方法断言。

### C16 ｜ 路径级预测不可靠（R32 对手 5/32）
**表述**：CDS 路径级预测不可靠，R32 对手命中率 15.6%（5/32）。
**注脚**：[I-16] bracket memo §2(iii)；[I-5] 模态决赛预测"英格兰 vs 法国"≠实际"西班牙 vs 阿根廷"。
**评级**：**A**（诚实负结果，与 C6 互锁）
**诚实标记**：✅ 诚实资产；论文禁用"预测了决赛对阵"。

### C17 ｜ 协议 / PIV 方法贡献
**表述**：Protocol Integrity Vector（七/八字段）把协议完整性作为与预测分数并列的一等评估对象。
**注脚**：[I-21] `paper-a-skeleton-2026-07-25.md` §3.2 PIV 八字段；[I-22] 外部 κ 未测（W6 G7 待 WorldCupBench 盲审）。
**评级**：**B+**（方法骨架，闸门未过前控制音量）
**诚实标记**：⚠️ Check 4 待 W5 系统检索；外部 κ≥0.6 未测 → PIV 当前仅内部应用候选。
**🔬 W5 系统检索结论（2026-07-26，详见 §8）**：**部分重叠，非空白确认**。各子维度均已被先行工作作为一等字段占据——B(来源分级)被 SourceBench 抢占、E(协议失败标注)被 ContractBench 抢占、A/D/F 被 WorldFork 整合、C(快照漂移)被 Impermanent 触及；但**无单一工作把六维打包为封闭一等评估对象**，且 #9/#10/#11 在体育/事件预测域确为空白。真实最近威胁是 **LMU LLM-SoccerArena**（已占 ex-ante+schema+协议失败诊断），而非无法验证的 Hartvég。C17 须由"空白"降级为"体育预测域首次六维整合闭集（B/C 为本工作增量）"。

### C18 ｜ CDS n=48 Brier ≈ 均匀噪声
**表述**：决赛后完整 48 队 Brier 0.0195–0.0200，仅勉强低于均匀基线 0.02083；冠军 log score kimi 1.44 < 市场 1.78 < CDS 3.03–3.43。
**注脚**：[I-6] n=48 复算脚本（三版本）；均匀基线 0.02083 解析式；[R-1] kimi 1.44；[I-7] 市场 1.78。
**评级**：**A**（诚实且自洽，C6 的定量封口）
**诚实标记**：✅ 是论文需要的含冠军完整 Brier；同时坐实"过度分散"负面结果。

---

## 3. 基础事实底座 F1–F2（论文依赖但 redteam 未单列）

### F1 ｜ git 历史留存完整逐日预测时间序列
**表述**：`cds_championship.json` 在 6-12→7-25 共 48 commit / 44 天，缺 7-09（workflow 失败，Gmail 互证）与 7-20（仅市场快照）。
**注脚**：[I-1] git log；[I-2] Gmail `3ad6419` + market snapshot `68804b1`；[I-3] git 内容寻址可重建任意日 tree。
**评级**：**A**（物理基础）
**诚实标记**：✅ 可独立重建；是"系统哪天开始知道西班牙会赢"分析的物理基础。

### F2 ｜ 已结算赛程冻结版 `923e23a`
**表述**：决赛后完整赛程（西班牙 1-0 阿根廷夺冠，四强=西/阿/法/英）冻结于 `923e23a`，Wikipedia 已核验。
**注脚**：[G-11] Wikipedia 2026 世界杯赛果核验；[I-5] `923e23a:schedule.json` KO 对阵。
**评级**：**A**（Green Source）
**诚实标记**：✅ 所有冠军/四强数字的唯一权威底座。

---

## 4. 战略性定位观点 S1–S10（非承重，属"怎么写"）

### S1 ｜ 双论文路线（Paper A 方法论 + Paper B 预注册）
**表述**：拆成 Paper A（Audit-Chain-Anchored Reconciliation 协议方法论，workshop/域内期刊）与 Paper B（预注册实验，evaluation 主会）；Nature/顶会正刊不可达。
**注脚**：[I-23] `paper-a-skeleton-2026-07-25.md`（Paper A）+ `llm-ensemble-scaling-paper-b-b0-2026-07-22.md`（Paper B）；[I-24] 对话路线图修订。
**诚实标记**：⚠️ 为规划决策，非实证主张；Paper B 已演进为"llm-ensemble-scaling"，须与 Paper A 的 H4 咬合。

### S2 ｜ 猜中冠军/四强仅作 hook，不作证据
**表述**："前五中四"只许在引言一段出现，随即声明"本文不以命中为证据"，用基准率（前四全进四强）+ 快照敏感性（0.19pp 漂移）消毒。
**注脚**：[G-1] 种子保护；[I-10] 幸存者偏差（佛得角若崩盘则"盲"成灾难）；[I-1] 市场同中 4/4。
**诚实标记**：✅ 与 C1/C2 的 B 级评级一致；是防自吹的核心纪律。

### S3 ｜ W6 三支柱组合为唯一 GO 方向
**表述**：数据集为主线 + accuracy–Brier 反转为结果卖点 + 协议失败标签为真正新颖点；W1–W5 均 PARK/KILL。
**注脚**：[I-25] `worldcup-paper-topic-2026-07-19.md` §5（W6 GO 附条件；W1/W2/W3/W4 PARK；W5 KILL）；八条硬 gate G0–G7。
**诚实标记**：⚠️ GO 附条件——G0–G4 任一不过自动降 PARK；G7 不过不得投 D&B。

### S4 ｜ 现实 venue = evaluation/workshop，D&B 仅 stretch
**表述**：NeurIPS 2027 D&B 仅 stretch（接受概率 10–20%）；现实出口 ICML/NeurIPS evaluation / data-centric / forecasting workshop（35–50%）。
**注脚**：[I-25] topic §5 venue 映射；[G-12] 直接竞品占位（WorldCupBench / Hartvég / ForecastBench）压低新颖性。
**诚实标记**：⚠️ 多直接竞品已占位，"首个世界杯 LLM benchmark"等表述**严禁**。

### S5 ｜ 分组规则重评（小组出线看积分非对战胜负）
**表述**：小组晋级按积分而非对战胜负；路径难度须按通道（半区）计算，不能简单按"死亡之组"直觉。
**注脚**：[I-26] **仅对话提及，未文档化**；属常识性方法论前提，非论文发现。
**诚实标记**：❌ 无文档化过程记录；仅为分析口径前提，不得作为"发现"写入。

### S6 ｜ 死亡之组 / 路径难度（定性）
**表述**：某些队路径更难（如与强队同半区），但本届因种子保护前四互斥，路径难度被制度拉平。
**注脚**：[I-26] 仅对话；[G-1] 种子保护使"死亡之组"叙事弱化。
**诚实标记**：❌ 仅定性对话，无计算指标；不得作为承重证据，至多作讨论章背景。

### S7 ｜ 佛得角之夜作为引言 hook 叙事
**表述**：6-19 西班牙 0-0 佛得角（人口 54.6 万、队史首进世界杯），市场谷底 10.05%，kimi 冻结 23.82% 纹丝不动，CDS 钉死 0.0325——"盲者胜明眼人"。
**注脚**：[I-7] 市场轨迹；[R-1] kimi 23.82%；[R-2] CDS 平线；[G-6][G-7][G-8] 佛得角 Polymarket 盈亏。
**诚实标记**：⚠️ 须带三重保险（幸存者偏差 / 种子保护 / 市场后来修对）；见既有报告 §6。

### S8 ｜ Paper A 贡献 4 条 + H1–H5 假设体系
**表述**：贡献 C1 协议五件套+PIV / C2 逐场校准结构 / C3 rank-vs-mass 分裂 / C4 kimi vs 市场 asymmetric evidence；假设 H1 逐场技能 / H2 平局低估 / H3 过度分散 / H4 kimi-市场 / H5 协议完整性向量。
**注脚**：[I-23] `paper-a-skeleton-2026-07-25.md` §1 贡献表 + §3 H1–H5。
**诚实标记**：⚠️ H1/H2/H4 须 paired bootstrap + reliability/ECE 后才可称"识别"；H5 外部 κ 未测。

### S9 ｜ OSF 分析协议冻结（非预测预注册）
**表述**：赛事已结束、部分结果作者已知，故冻结"分析协议"（指标/纳排/比较族/已知未知边界），不称"pre-registered predictions"。
**注脚**：[I-24] `worldcup-algorithms-comparison-paper-2026-07-20.md` §Approach；paper-a-skeleton §5.5。
**诚实标记**：✅ 诚实边界；论文须如实披露"作者已见部分结果"。

### S10 ｜ 主语纪律 + 文献占位防御
**表述**：主语永远是"协议"不是"我们拥有独家预测"；须补 ≥13 篇 prior art（F2/F3/W6 共 ≥18，去重后）否则 novelty 高风险。
**注脚**：[I-27] `stage1-review-report.md` §2/§7（F3 10 篇 + F2 11 篇 + W6 7 篇零引用，CRITICAL）；[I-23] skeleton §5 措辞禁忌。
**诚实标记**：⚠️ v1.3 文献综述 0/18 引用，是硬伤；投稿前必须完成系统检索（W5 闸门）。

---

## 5. 事实一致性核查（诚实说"不是错误"与"真问题"）

| 项目 | 结论 | 处理 |
|---|---|---|
| C8 "−17.6pp vs −8.3pp" 数字打架 | 🔁 **非错误**，口径不同（MD1 单轮 vs 全赛段），证据文件第 301 行两数字并存 | 论文须注明口径，不得并排不解释 |
| "Fox 全粉笔年也中冠军"（C2 注脚） | ❌ **无证据**，仅对话 | 删除或补独立源；不得写入 |
| kimi 生成层模型版本（C14） | ⚠️ 不可考，已降级 | Red Source 标注，不作承重 |
| kimi 覆盖 21 队 vs top3 27 队（C1/C3/C4） | ⚠️ 口径混淆；top3 是否新增覆盖待验证（F2 in outline） | 区分 champion(21) 与 top3(27)；top3 零覆盖则标 `frozen_sample_zero_evidence` |
| 市场流动性未调整（C11） | ⚠️ 真实缺口 | 引用"错价"须加"按收盘价、未做流动性调整" |
| 分组规则 / 死亡之组（S5/S6） | ❌ 仅对话、未文档化 | 不作发现；仅方法论前提/讨论背景 |
| v1.3 文献 0/18 零引用（S10） | ⚠️ 硬伤 | W5 闸门前不得定稿 Related Work |
| C5 版本选择（CDS #1 归谁） | ⚠️ 版本风险 | C 级，禁用"CDS 预测冠军" |

---

## 6. 与既有"5 项主张报告"的映射

既有 `claim-verification-with-footnotes-2026-07-26.md` 的 5 项主张，本清单已吸收并扩展：

| 既有报告主张 | 本清单对应 | 状态 |
|---|---|---|
| 1. git 逐日序列 48commit/44天 | **F1** | ✅ 吸收 |
| 2. FIFA 种子保护制度 | **C10** | ✅ 吸收（含中文源） |
| 3. 塞内加尔机制 | **C6** | ✅ 吸收 |
| 4. n=48 结算 | **C18** | ✅ 吸收 |
| 5. 市场情绪 | **C11 + S7** | ✅ 吸收（C11 实证 + S7 hook） |

既有报告 §6 三重保险、参考文献索引仍有效，与本清单参考文献合并见下。

---

## 7. 参考文献索引（合并）

**[G-1]** FIFA. *Procedures for the Final Draw for the FIFA World Cup 2026™ revealed*. 2025-11-25. https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/procedures-pots-final-draw
**[G-2]** ESPN. FIFA World Cup 2026 draw coverage (rules explainer 2025-12-05; format reform 2025-11-25).
**[G-3]** 新华网. 《国际足联公布2026年世界杯抽签规则》. 2025-11-26. https://www.news.cn/sports/20251126/275e59c0b82844059c9b218935cab795/c.html
**[G-4]** 微信公众号「说个足球」. 《世界杯国家队：西班牙队——斗牛士归来》. 2026-03-31（搜狗微信检索摘要）.
**[G-5]** 微信公众号「你挑的吧偶像」. 《2026年世界杯的告别之战!》. 2026-03-13（搜狗微信检索摘要）.
**[G-6]** Bloomberg（转述）/ 网易. *A single trader on Polymarket lost nearly $1 million when Cabo Verde fought Spain to a stunning draw*. 2026-06-16. https://www.163.com/game/article/DK3UFFO400318PFH_mobile.html
**[G-7]** 搜狐. 《92%胜率惨遭翻车!西班牙碾压数据被零封,佛得角缔造百万级盈亏名场面》. 2026-06-16. https://www.sohu.com/a/1037208148_121924582
**[G-8]** 搜狐. 《有人赌西班牙不会获胜赢470万美元,也有人100万美元一夜归零》. https://www.sohu.com/a/1037546979_121384220
**[G-9]** 界面新闻 / 网易. 《从经济学家到AI智能体,谁能算准世界杯？》. https://www.jiemian.com/article/14568476.html ｜ https://www.163.com/dy/article/KV4NDAB80534A4SC.html
**[G-10]** Murphy, A. H., & Winkler, R. L. (1977). *Reliability of Subjective Probability Forecasts*. JASA 72(359). ｜ Dixon, M. J., & Coles, S. G. (1997). *Modelling Association Football Scores*. JRSS A 160(2).
**[G-11]** Wikipedia. *2026 FIFA World Cup*. https://en.wikipedia.org/wiki/2026_FIFA_World_Cup （赛果核验）
**[G-12]** WorldCupBench (dckthulhu) / Hartvég et al. Preprints.org 202607.0719 / ForecastBench (Karger, ICLR 2025) — 直接竞品占位，见 `worldcup-paper-topic` §2.

**[R-1]** kimi 聚合信号：西班牙夺冠概率冻结 23.82%；冠军 log score 1.44（Red Source，仅参考）.
**[R-2]** CDS 引擎（`ef30658`/`875748b`）：西班牙路径概率全程 0.0325–0.0331，无赛果通道（Red Source）.
**[R-3]** kimi 生成层模型版本不可考（上游 `worldcup-kimi/` gitignored，溯源待验证）.

**[I-1]** git log `/data/processed/cds_championship.json`：48 commits / 44 days（6-12→7-25）.
**[I-2]** Gmail 失败通知 `3ad6419`（2026-07-09 11:30）+ market snapshot `68804b1`（7-20）.
**[I-3]** git 内容寻址：任意日 tree 可重建 `cds_championship.json`.
**[I-4]** `ef30658`/`875748b` path_nodes：塞内加尔五节点 0.4832–0.5154；#15→#1 归一化跃迁.
**[I-5]** `923e23a` schedule.json：KO81 Belgium 3–2 Senegal（R32）；模态决赛预测错误.
**[I-6]** n=48 复算脚本（同 bracket memo）；均匀基线 Brier = 0.02083 解析式.
**[I-7]** 77 个 `market_public_snapshot.json` 日版：西班牙全轨迹 + 法国时代 + 双半决赛错判.
**[I-8]** `fig6_and_metrics_2026-07-26.py` + `fig6-three-trajectories-2026-07-26.png`：时间积分 log score（市场 1.744 / kimi 1.435）、同池多项 Brier（kimi 0.688 / 市场 0.753 / CDS 0.930 / 均匀 0.952）.
**[I-9]** `worldcup-paper-topic-2026-07-19.md` §1.4：kimi 与市场 top5 同中 4/4（西法阿葡英）.
**[I-10]** 对话记录："Fox 全粉笔年也中冠军" — **仅对话，无独立来源（❌）**.
**[I-11]** kimi 21 队池内重归一偏离方向表（阿根廷+11.7pp 等）.
**[I-12]** `worldcup-paper-topic` §1.2 结算表（Elo Brier 0.5728 n=71 / Coach 0.6078 n=72）.
**[I-13]** `worldcup-paper-topic` §1.2：Elo 平局 −8.3pp（全赛段）、主胜 +10.9pp.
**[I-14]** `2026-07-08-group-stage-72-match-evaluation.md` 第 301 行："整体 −8.3pp、MD1 −17.6pp".
**[I-15]** Plan C 3/3 全平局结算时间戳验证（`results/2026-07-08-*`）.
**[I-16]** `bracket-encoding-verification-2026-07-26.md` §2–§3（R32 命中 5/32；半决赛可达）.
**[I-17]** 市场流动性声明：Polymarket 单队 outright 流动性/价差未核验.
**[I-18]** `evidence/cds4worldcup-timestamp-anchors-2026-07-25/`：EVIDENCE-CHAIN + 校验和 + 锚定收据.
**[I-19]** kimi 聚合层 0.05pp 容差复算（21/21）.
**[I-20]** 市场终点修正反例（决赛前 59/40.5 有效）.
**[I-21]** `paper-a-skeleton-2026-07-25.md` §1 贡献表 + §3.2 PIV 八字段.
**[I-22]** W6 G7 外部盲审 κ 未测（待 WorldCupBench）.
**[I-23]** `paper-a-skeleton-2026-07-25.md` + `llm-ensemble-scaling-paper-b-b0-2026-07-22.md`.
**[I-24]** `worldcup-algorithms-comparison-paper-2026-07-20.md` §Approach（OSF 分析协议冻结）.
**[I-25]** `worldcup-paper-topic-2026-07-19.md` §5（W6 GO + 八 gate）/ §2 占位风险.
**[I-26]** **仅对话提及，未文档化**：分组规则重评、死亡之组/路径难度（❌ 无过程文档）.
**[I-27]** `stage1-review-report.md` §2/§7：F3 10 + F2 11 + W6 7 篇 prior art 零引用（CRITICAL）。
**[I-28]** 本文件 §8：W5 四专家并行系统检索（PRISMA-lite）执行记录。
**[I-29]** Hartvég Preprints 202607.0719 三次检索均 404、SVS/THR 全网无定义 —— **无法验证，不得列为占位威胁**（E3 诚实标注）。
**[I-30]** "Polymarket-v1 / Boka Qin 2606.04217" 在 E3+E4 两次独立检索均未命中 —— **幻影引用，从 prior art 清单删除**（stage1 review 曾引为最近邻）。
**[I-31]** willianpinho/worldcup-predictor-2026 与 974103107/AI-World-Cup 以所给 handle 检索不到（有同名/近义仓库如 vastxie/ai-worldcup-2026）—— **handle 疑似失效，作者二次核对**。

**[G-13]** WorldFork: *From Forecast Scores to Auditable Benchmarks* (ICML 2026), OpenReview id=MKraFpVNKM —— 占 A/D/E/F 维度（预注册/泄漏审计/溯源/trace 级失败/endpoint schema），缺 B/C。
**[G-14]** SourceBench (2026), arXiv:2602.16942 —— dim B(来源质量分级)精确匹配（RAG/引用域）。
**[G-15]** ContractBench (2026), arXiv:2605.17281 —— dim E(15 类协议失败标注为一等字段)精确匹配（agent 工具域）。
**[G-16]** OracleProto (2026), arXiv:2605.03762 —— dim A(知识截止+时态掩码冻结)+泄漏检测。
**[G-17]** Impermanent: *Live Benchmark for Temporal Generalization* (2026), arXiv:2603.08707 —— dim C(真实数据漂移/时序泛化)。
**[G-18]** OpenClawBench (2026), arXiv:2605.29253 —— dim E(流程异常标注为一等监督)。
**[G-19]** LMU *LLM SoccerArena* (2026), llm-soccerarena.com —— **真实最近威胁**：ex-ante 时间戳 + schema 校验 + 协议失败诊断（invalid/repair/normalization/missing/consistency 率）。
**[G-20]** WC2026-Agents (2026), arXiv:2607.17765 —— ex-ante + schema + 市场基线。
**[G-21]** WorldCupArena (2026), arXiv:2607.18084 —— 13 模型、prompt 统一、含市场基线。
**[G-22]** vBase / Data Provenance Initiative (Nature MI 2024) —— dim D(point-in-time 溯源审计)。
**[G-23]** Notch Protocol (2026) —— commit-reveal + 链上 Brier，溯源对象为预言者技能。
**[G-24]** Zeileis/Groll 2026 ML 世界杯预测（zeileis.org）—— ex-ante + 市场基线 + 校准，无协议审计维度。

---

## 8. W5 系统文献检索执行报告（2026-07-26 补充）

> 方法：deep-research 框架 + PRISMA-lite；四领域专家并行（E1 协议完整性审计 / E2 LLM 预测基准 / E3 世界杯直接竞品 / E4 调和与市微观）。
> 库：arXiv、Semantic Scholar、Google Scholar、ACL Anthology、NeurIPS/ICML/ICLR/KDD、SSRN、GitHub artifact、Preprints.org。
> 窗口：2015–2026（重点 2023–2026）。目的：把 novelty 声明从"定向核查 37 篇"升级为"系统检索"，产 12 维 crosswalk，裁决 C17。

### 8.1 PRISMA-lite 聚合

| 专家 | 检索命中(去重) | 初筛保留 | 纳入 crosswalk | 排除主因 |
|---|---:|---:|---:|---|
| E1 协议完整性 | ~42 | 16 | 13 | MLOps 工程工具、通用复现清单（仅"提及"非一等字段） |
| E2 LLM 基准 | ~24 | 8 | 7 | 综述、纯时序/校准非基准、重复 |
| E3 世界杯竞品 | 19 | 12 | 7 验证 + 5 未验证 | Hartvég/AlDahoul/ModelBall/handle 失效 |
| E4 调和/市微观 | ~52 | 24 | 11 | 经典误命中、非审计层 |

**合计**：去重候选约 137 条，纳入 crosswalk 约 38 项（含跨域占位），未验证 5 项单列。

### 8.2 12 维 crosswalk 主表（验证竞品）

图例：Y=是 / N=否 / ~或P=部分。维度：①Future-only ②Freeze ③Prompt= ④#Model ⑤Market ⑥Proper ⑦Calibration ⑧Reason ⑨Source policy ⑩Schema ⑪Protocol-fail ⑫Ex-ante audit/drift/provenance。

| 竞品（年·验证级） | ① | ② | ③ | ④ | ⑤ | ⑥ | ⑦ | ⑧ | ⑨ | ⑩ | ⑪ | ⑫ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **LMU LLM-SoccerArena** (2026·①) | Y | Y | Y | ~8 | P | Y | Y | Y | P | **Y** | **Y** | P |
| **WorldCupBench** (mverab·①) | Y | Y | Y | 11 | Y | Y | P | Y | N | **Y** | P | P |
| **WC2026-Agents** (arXiv:2607.17765·①) | Y | Y | Y | 4+1 | Y | Y | Y | Y | N | P | P | P |
| **WorldCupArena** (arXiv:2607.18084·①) | Y | P | Y | 13 | Y | P | P | Y | P | P | P | P |
| **ForecastBench** (arXiv:2409.19839·①) | Y | N | N | Y | N | Y | ~ | N | N | N | N | N |
| **Prophet Arena** (arXiv:2510.17638·①) | Y | N | Y | Y | Y | Y | Y | ~ | N | N | N | N |
| **Foresight Arena** (arXiv:2605.00420·①) | Y | ~ | N | Y | Y | Y | Y | N | N | N | N | **~** |
| **InfoDelphi** (arXiv:2607.01661·①) | ~ | N | N | Y | ~ | Y | Y | Y | ~ | N | N | N |
| **Halawi** (arXiv:2402.18563·①) | Y | ~ | N | Y | ~ | Y | ~ | Y | ~ | N | N | N |
| **Merger-arb** (arXiv:2607.09921·①) | Y | N | N | Y | Y | Y | Y | Y | N | N | N | N |
| **AIA Forecaster** (arXiv:2511.07678·①) | Y | N | N | N | Y | Y | Y | ~ | ~ | N | N | N |
| **Zeileis/Groll 2026** (zeileis.org·①) | Y | Y | N/A | 1 | Y | Y | P | P | N | N | N | N |
| **Rezaei-Samadi SDR-Elo** (arXiv:2606.24171·①) | Y | Y | N/A | 11* | N | Y | N | N | N | N | N | N |

**跨域占位（E1 发现，证"分量已被占"）**：WorldFork(ICML26, 占①②⑥⑦→A/D/E/F)、SourceBench(占⑨B)、ContractBench(占⑪E)、OracleProto(占①A)、Impermanent(占⑫C)、vBase/Data Provenance(占⑫D)、OpenClawBench(占⑪E)。

### 8.3 C17 三结局裁决

| 结局 | 是否满足 | 证据 |
|---|---|---|
| **空白确认**（Check 4 PASS，C17 全音量） | ❌ **不满足** | 各子维度均已被先行工作作为一等字段占据（B→SourceBench、E→ContractBench、A/D/F→WorldFork、C→Impermanent） |
| **部分重叠**（收窄到"五件套闭集+PIV 八字段"，仍活） | ✅ **满足** | 无单一工作把六维打包为封闭一等评估对象；#9/#10/#11 在体育/事件预测域确为空白；B(来源分级)/C(快照漂移) 是 WorldFork 缺的拼图 |
| **直接撞车**（贡献塌缩，降级） | ❌ **不满足** | 无工作同时覆盖六维；LMU 占 ex-ante+schema+协议失败诊断但未做成"一等计分字段闭集" |

**裁定**：**部分重叠**。C17 由"空白/有限核查"降级标注为——*"首次在体育/事件预测域把六维整合为预测资产的一等评估闭集（其中 A/D/E/F 已被 WorldFork 等 anticipate，B/C 为本工作增量）"*。否则存在被 reviewer 指 overclaim 的风险。

### 8.4 时间风险（v2 已登记"占位窗口风险"）

- **LMU SoccerArena：中高**。其 2026-06-11 预印本刻意将准确率结果延后至赛果出炉后按固定计划计算；若赛后 v2 把 ex-ante 时间戳+结构化校验升级为显式"drift/provenance audit"，将覆盖本工作第 ⑫ 维。对策：方法章**显式引用 LMU 并划清边界**（一等字段化 vs 辅助诊断）。
- WorldCupBench / WC2026-Agents：已冻结发布，方向稳定，抢发风险低。
- Hartvég：无法验证（见 8.5），风险未知，不得据此调整措辞。

### 8.5 诚实纠错（本次检索最值钱的部分）

| 我们 prior art 清单里的项 | W5 结论 | 处理 |
|---|---|---|
| Hartvég SVS/THR（被列为"最大占位威胁"） | **三次检索 404、SVS/THR 全网无定义，无法验证** | 从"威胁"降级为"待作者核对"，不得写入对比或"非首个"声明 |
| Polymarket-v1 / Boka Qin 2606.04217（stage1 引为最近邻） | E3+E4 两次独立检索均**查无此文** | **幻影引用，删除** |
| willianpinho/worldcup-predictor-2026、974103107/AI-World-Cup | 所给 handle **检索不到**（有同名/近义仓库如 vastxie/ai-worldcup-2026） | handle 疑似失效，作者二次核对 |
| "v1.3 文献 0/18 零引用"硬伤 | 现已检索到真实 prior art（WorldFork/SourceBench/ContractBench/LMU 等） | 须把这批**加入** §2 文献与 crosswalk，原"零引用"状态已过时 |

### 8.6 全部 30 条观点 × W5 先验艺术冲击评估

| 观点 | 是否受 prior art 挑战 | 结论 / 动作 |
|---|---|---|
| **C17 / H5（PIV）** | ⚠️ 部分 | 降级为"域首次六维整合"，补 LMU 划界（见 8.3） |
| **C13（证据链五层）** | ⚠️ 部分 | WorldFork/verievals/vBase 占 provenance——须强调"体育多源跨方法"差异化 |
| **C7（accuracy-Brier 反转）** | ✅ 已知 | Murphy-Winkler(1977) 已覆盖，维持 C 级仅插图 |
| **C8（平局低估）** | ✅ 已知 | Dixon-Coles(1997) 须正式引用，维持 A− |
| **C6（过度分散/塞内加尔）** | ❌ 无 | WC 域无同类失败模式 prior art，安全 |
| **C10（种子保护）** | ❌ 无 | FIFA 官方，安全 |
| **C11（市场法国时代）** | ❌ 无 | 行为金融 n=1 描述，安全（流动性 caveat 保留） |
| **C16（路径不可靠）** | ❌ 无 | 安全 |
| **C1/C2（kimi 命中）** | ❌ 无 | 维持 n=1 hook，不变 |
| **S4（venue）** | ⚠️ 强化 | LMU/WorldCupBench 确为真实竞品 → "首个 benchmark"严禁更硬 |
| **S10（文献防御）** | 🔄 反转 | 原"0/18 零引用"已过时；现须补 WorldFork/SourceBench/ContractBench/LMU 等，否则仍属硬伤 |
| **S1（双论文路线）/S2/S3/S5/S6/S7/S8/S9/F1/F2** | ❌ 无 | 不受 prior art 冲击 |

### 8.7 §2.6 定位陈述修订稿（W5 后）

> 在最接近的 2026 prior art（WorldFork、SourceBench、ContractBench、LMU SoccerArena、ForecastBench、Prophet Arena、Foresight Arena、InfoDelphi）之外，本工作的差异化在于：**（i）首次在体育/事件预测域将 ex-ante 冻结、来源分级（Green/Red）、统一结算、时态溯源、快照漂移、schema 校验六维整合为预测资产的一等评估闭集（Protocol Integrity Vector）**；其中 A/D/E/F 已被 WorldFork 等 anticipate，本工作的增量是 B(来源分级) 与 C(快照漂移监测) 这对 WorldFork 缺失的拼图，以及将它们作为**一等计分字段**而非辅助诊断。该声明经 W5 系统检索（PRISMA-lite，137 候选→38 纳入）验证，非"有限核查"。

---

## CHANGELOG

- 2026-07-26：建论文观点总清单。扫描 `analysis/worldcup-2026/*`、`docs/plans/*`、`docs/investigations/*`、`research/*` + 对话记录；枚举 **18 承重实证（C1–C18）+ 2 基础事实（F1–F2）+ 10 战略定位（S1–S10）= 30 条**；逐条补 [G/R/I] 注脚 + 证据评级（A/B/C）+ 诚实标记（✅/⚠️/❌/🔁）；§5 事实一致性核查澄清 C8 数字非错误、标出 Fox 无源/kimi 版本/分组规则未文档化等真问题；§6 映射既有 5 项主张报告。
- 2026-07-26（下午）：执行 **W5 系统文献检索**（deep-research + PRISMA-lite，四专家 E1–E4 并行）。产出 §8：12 维 crosswalk 主表（13 验证竞品 + 跨域占位）、C17 三结局裁决=**部分重叠**（降级为"体育域首次六维整合闭集"）、时间风险（LMU 中高）、诚实纠错（Hartvég 404 无法验证 / Polymarket-v1 幻影引用 / 两 repo handle 失效 / 原 0/18 零引用已过时）、全部 30 条观点×prior art 冲击评估、§2.6 定位陈述修订稿。C17 评级加 W5 注记；§7 增 [G-13]–[G-24]、[I-28]–[I-31]。
