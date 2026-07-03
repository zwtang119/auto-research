# 课题五深度研究方向规划

> **版本**：v5.0 | **日期**：2026-07-01 | **阅读水平**：大学本科及以上
> **前提**：仅知识库API可用；其他上游课题未就绪；当前仿真引擎使用DeepSeek-V4 + RoleDNA驱动Agent角色扮演
> **数据来源**：5个CDS关联仓库（详见§附录）+ 7份课题参考文件 + deepseek_v4角色扮演方法
> **用途**：为课题五的论文选题、实验规划和AutoResearch自动化提供完整指引

---

## §0 新手导读（5分钟了解全貌）

### 这个文档是干什么的？

这是课题五（国家重点研发计划，灾害事故应急决策知识库）的**论文选题指南**。我们有一个运行中的多Agent推演系统（PolicySim），有5个关联代码仓库积累了大量实验数据和代码资产，现在需要决定接下来写什么论文、做哪些实验。

### 核心问题一句话版

> 如何让AI驱动的多Agent系统在灾害应急场景下做出更好的群体决策，并且能用数据证明"真的更好了"？

### 10个论文课题速览

| 编号 | 名称 | 一句话 | 难度 | 代码就绪 | 能否AutoResearch |
|------|------|--------|------|---------|:--:|
| **P1** | 知识库RAG注入 | 让Agent能"查阅"灾害知识库来做决策 | ★★☆ | 85% | 需人工标注 |
| **P2** | Factor Ledger | 自动发现"哪些因素最关键"，并用真实数据验证 | ★★★ | 90% | 需领域知识 |
| **P3** | 决策可解释性 | 把AI的决策逻辑画成指挥员能看懂的图 | ★★★ | 70% | ❌ 需专家 |
| P4 | 灾害链约束 | 让AI知道"泄漏→爆炸→污染"的因果链 | ★★☆ | 60% | ❌ 需API |
| P5 | 反事实推演 | "如果当时做了不同决策，后果会怎样？" | ★★★ | 50% | ❌ 需API |
| P6 | 分层决策架构 | 把Agent从"线性排队"变成"三层分工" | ★★★ | 40% | ❌ 架构设计 |
| **P7** | 信号融合 | 12种数据源融合成一个信号喂给Agent | ★★☆ | 85% | ✅ 零人工 |
| **P8** | 市场校准 | 用真实赌注市场数据校准AI预测 | ★★★ | 75% | ✅ 1个checkpoint |
| P9 | AI群体智慧 | 300个AI角色预测世界杯→降为P8补充 | ★☆☆ | 40% | ❌ |
| P10 | 混合QA框架 | 8个维度评估Agent输出质量 | ★★☆ | 80% | 不适合 |
| **P11** | 内心独白→角色一致性 | 让Agent暴露思考过程，验证RoleDNA人设 | ★★★ | 80% | ✅ 零人工 |
| P12 | Judge校准方法论 | LLM裁判的Gold Sample锚定校准 | ★★☆ | 85% | ✅ 零人工 |

> **Tier 1（Q3立刻动手）**：P2 + P1 + P11 | **Tier 2（Q3下旬）**：P8 + P7 | **Tier 3（Q4+）**：P3 + P12 + P5-P6
> **粗体** = 推荐优先 | AutoResearch = 适合AI自动跑实验 | ❌ = 必须人参与

---

## §1 论文管线全貌

### 时间线（按依赖关系和代码就绪度排序）

```
         2026 Q3                2026 Q4               2027 Q1-Q2
Tier 1 ═ P2 Factor Ledger ═══ 投稿 ───
Tier 1 ═ P1 知识RAG ══════ 投稿 ───
Tier 1 ═ P11 内心独白 ═════ 投稿 ───
Tier 2 ═ P8 市场校准 ═════ 投稿 ───
Tier 2 ═ P7 信号融合 ═════ 投稿 ───
Tier 3 ── P3 可解释性 ────────── 投稿 ───
Tier 3 ── P12 Judge校准 ──────── 投稿 ───
Tier 3 ── P5 反事实 ─────────────── 投稿 ───
```

### 10条论文管线详情

| # | 论文方向 | 来源 | 启动 | 投稿 | 目标会议 | 论文概率 |
|---|---------|------|------|------|---------|:--:|
| **P1** | 知识库RAG注入→Agent决策 | v1.0 | Q3立刻 | Q4 | AAAI/IJCAI（AI应用交叉） | 中高 |
| **P2** | Factor Ledger因子自动提取与校准 | v1.0 | Q3立刻 | Q4 | ACL/EMNLP（NLP+Agent） | **高** |
| P3 | 应急决策可解释性 | v1.0 | Q3 | Q1 2027 | JAIR/TCSS（AI应用期刊） | 中 |
| P4 | 灾害链知识→Agent约束 | v1.0 | Q4 | Q2 2027 | ISCRAM（应急信息管理） | 中 |
| P5 | 反事实推演评估 | v1.0 | Q1 2027 | Q3 2027 | Safety Science（安全科学） | 中高 |
| P6 | 分层群体决策架构 | v1.0 | Q1 2027 | Q3 2027 | AAMAS（多Agent顶会） | 中 |
| **P7** | 信号融合→多Agent决策 | v2.0 | Q4 | Q2 2027 | ACM TIST（智能系统） | 中 |
| **P8** | 预测市场校准LLM Agent | v2.0 | Q3 | Q1 2027 | EMNLP/AAAI（评估方法） | **高** |
| P9 | AI群体智慧研究 | v2.0降级 | — | — | 降为P8补充 | — |
| P10 | 混合式Agent QA框架 | v2.0 | Q4 | Q2 2027 | TCSS（社会计算） | 中低 |

---

## §2 P1：知识库RAG注入→Agent决策质量改善

### 用大白话说

> 灾害应急时，指挥员需要查手册、查化学品性质、查历史案例。我们的AI Agent也应该能"查知识库"。这个课题就是给Agent接上课题三的知识库API，让它做决策时能查到相关知识——然后证明查了知识确实比不查做得更好。

### 要解决什么问题？

目前PolicySim的Agent是"裸脑"决策——它只有LLM的训练知识，没有接入课题三构建的专业灾害知识库（处置规程、化学品数据、历史案例）。P1要做的是：

1. **打通知识管道**：让Agent在做决策时自动从知识库检索相关知识
2. **证明知识有用**：通过对照实验（有知识 vs 无知识），量化知识注入对决策质量的改善
3. **找到最佳注入方式**：静态注入（直接塞进提示词）vs 动态检索（按需查询）vs 角色定制（不同Agent查不同知识）

### 实验设计（4组对照 × 100次推演）

```
组A（基线）：纯LLM Agent —— 不给任何额外知识
组B（静态）：预定义的古雷处置规程直接写进Agent的初始指令里
组C（动态）：Agent每轮决策前从知识库API检索相关知识，动态注入
组D（角色定制）：在C的基础上，灭火Agent只查灭火知识，疏散Agent只查疏散知识
```

每次推演用6个指标评估（伤亡人数、财产损失、环境影响、泡沫消耗量、处置时间、人力投入）。

### 里程碑

| 阶段 | 要做的事 | 产出 | 耗时 |
|------|---------|------|------|
| M1 | 开发知识检索管道（调用知识库API→检索结果→注入Agent提示词） | KnowledgeRetriever代码 | 2周 |
| M2 | 4组对照实验 × 100次推演 | 400条实验数据 | 1-2周 |
| M3 | 统计分析 + 论文写作 + 投稿 | 论文 | 3-4周 |

> **论文出口**：AAAI 2027 或 IJCAI 2027（人工智能两大顶会，关注AI技术在实际场景的应用）
> **核心贡献**：(1) RAG在应急决策领域的首次系统验证；(2) 角色定制化知识注入的增量价值证明

### 术语解释
- **RAG（检索增强生成）**：让AI在回答前先"查资料"，把查到的东西作为参考再生成答案。相当于考试时允许翻书。
- **Ablation实验（消融实验）**：逐个去掉系统的一个组件，看性能下降多少——用来证明每个组件都有用。

### 与其他课题的关系
- 与 **P2** 互补：P1负责"信息输入"（给Agent知识），P2负责"输出评估"（判断哪些知识真正影响了决策）
- 可合并为更大论文（详见§12）

---

## §3 P2：Factor Ledger — 推演关键因子自动提取与校准（P0主线）

### 用大白话说

> 每次灾害推演会产生海量数据——哪个Agent的哪步决策真正改变了结果？P2就是要自动从推演数据中找出"关键因子"，就像足球赛后分析"哪个换人改变了比赛"。更进一步，用真实灾害数据来验证找到的因子是不是真的关键。

### 要解决什么问题？

1. **因子发现**：从推演结果中自动识别"前兆因子"（事前能预警的信号）、"抑制因子"（能阻止灾害恶化的措施）、"分支因子"（导致走向分叉的决策点）、"反证因子"（事后证明判断错误的信号）
2. **因子排序**：用Sobol敏感度分析排出"哪些因子最重要"
3. **真实验证**：用古雷石化真实事故数据（1417人/322台车/56小时灭火）来校准——找到的因子跟历史相符吗？

### 实验设计（6步）

```
步骤1：推演→自动提取因子（检测推演过程中后果分布的突变点）
步骤2：人工标注30条轨迹，验证提取器准不准（目标：Recall≥65%）
步骤3：Sobol分析（1000次推演），排出古雷场景的重要性Top 5
步骤4：反事实推演——修改古雷3个关键决策节点，看后果变好还是变坏
步骤5：Multi-Judge裁决（4个AI裁判角色分别判定因子有效/无效/不确定）
步骤6：用古雷真实历史数据对照——我们推演的因子跟历史一致吗？
```

### 里程碑

| 阶段 | 要做的事 | 耗时 |
|------|---------|------|
| M1 | 因子Schema + 自动提取器开发 | 2周 |
| M2 | Sobol分析(1000次推演) + 反事实推演矩阵 | 1-2周 |
| M3 | Multi-Judge裁决系统适配 | 1周 |
| M4 | 论文写作+投稿 | 3-4周 |

> **论文出口**：ACL 2027 或 EMNLP 2027（自然语言处理顶会，当前Agent论文中罕见的"预注册+结算"实证范式）
> **核心贡献**：(1) 四类因子的形式化定义与预注册协议；(2) Sobol驱动的因子自动排序；(3) 古雷真实数据的完整校准闭环

### 吸收能力（来自cds4worldcup）
- 成熟的因子YAML格式（factor_id/origin/event_relation/observable_proxy/settlement_rule）
- Multi-Judge裁决框架（4角色：证据/校准/怀疑/知识裁判）
- Brier/Log Loss校准方法论

---

## §4 P3-P6：二线课题摘要

### P3：决策可解释性分析
> **大白话**：把AI复杂的推演过程画成指挥员能看懂的"因果图"和"决策树"——让非AI背景的应急专家能在10分钟内理解AI为什么这么建议。

### P4：灾害链知识→Agent约束
> **大白话**：知识库里有"泄漏→爆炸→环境污染"这样的因果链数据，让Agent在推演时自动考虑这些连锁反应，提前做预防性资源预置。

### P5：反事实推演
> **大白话**："如果火灾发生时泡沫车没堵在路上会怎样？"——用CDS推演不同决策路径的后果，评估当时的决策是否最优。

### P6：分层决策架构
> **大白话**：把Agent从"三个Agent轮流发言3轮"升级为"指挥部（合作层）+参谋部（推理层）+战斗组（反应层）"的三层架构。

---

## §5 P7：多源信号融合→多Agent决策支持

### 用大白话说

> 灾害应急时，信息来源五花八门——金融市场波动、能源价格变化、新闻报道、学术论文、维基百科……P7做的是把这些"散乱信号"融合成Agent能理解的结构化信息（就像一个情报简报），然后看能不能帮Agent做出更好的决策。

### 要解决什么问题？

目前PolicySim的Agent只用LLM知识做决策。P7从cds-keyperson复用了一个信号融合管线（267行纯函数链），把12种外部数据源的信息融合成统一的结构化信号（镜头权重 + 三情景预测），然后喂给Agent。

### 实验设计

```
4组条件 × 100次推演：
A: 无外部数据（纯LLM）——基线
B: 原始散乱数据（12个数据源的所有信息直接堆给Agent）
C: 融合信号（结构化的镜头权重+三情景预测）
D: 融合信号+偏差诊断（告诉Agent"当前信息可能偏乐观/偏悲观"）

消融实验（50次/组）：逐一移除A/B/C三组数据源，看哪个最不可缺
```

### 里程碑

| 阶段 | 要做的事 | 耗时 |
|------|---------|------|
| M1 | 从cds-keyperson提取SignalFusionEngine（267行链） | 1周 |
| M2 | 4组实验（400次推演） | 2周 |
| M3 | 消融实验 + 统计分析 + 论文 | 3-4周 |

> **论文出口**：ACM TIST（智能系统汇刊）
> **代码就绪度**：85%（链完整但需适配古雷场景）
> **AutoResearch**：✅ 零人工（数据源分组已预配置在task_spec中）

### 已知限制
- SignalFusionEngine代码量小（267行），算法简单（recency线性插值+方向加权）
- Forecaster输出文本描述而非数值概率
- Calibrator仅检测2.0x比率偏差，无统计检验

---

## §6 P8：预测市场作为LLM Agent推演校准场

### 用大白话说

> Polymarket是一个用真金白银下注的预测市场（比如"美联储6月会降息吗？"）。真金白银产生的概率比AI"猜"出来的更可信。P8的创意是：用Polymarket的结算结果作为"标准答案"，来检验我们的AI Agent推演到底准不准。

### 要解决什么问题？

LLM Agent的评估是当前AI研究的热门难题——没有可靠的外部标准来判断Agent的判断"对不对"。P8提出：预测市场（真实资金驱动的概率）天然是一个校准场——事件结算后就有明确的对错，可以用来验证Agent的知识注入是否真的改善了推理质量。

### 实验设计

```
Step 1: 知识注入→Agent推演WTI原油事件
Step 2: 推演结果 vs Polymarket市场共识（Brier Score对比）
Step 3: 事件结算→因子可结算率评估
Step 4: 知识写回→推演质量改善（before/after对比）
Step 5: 6领域跨域稳健性分析
```

### 里程碑

| 阶段 | 要做的事 | 耗时 |
|------|---------|------|
| M1 | AB测试数据提取 + Brier计算函数实现(~50行) | 1-2周 |
| M1.5 | ⚠️ 人工选择3-5个案例事件（Agent自动生成候选池） | 人介入 |
| M2-M3 | 因子评估+知识写回实验 | 2周 |
| M4-M5 | 跨域分析+论文 | 3-4周 |

> **论文出口**：EMNLP 2027 或 AAAI 2027
> **核心贡献**：提出"预测市场作为LLM Agent校准场"的创新方法论
> **代码就绪度**：75%（AB数据存在，Brier需手动实现，Factor Ledger仅设计无代码）
> **AutoResearch**：✅ 1个人工checkpoint（M1.5选事件）

---

## §7 P9-P10：降级课题

### P9：AI群体智慧研究

**来源**：cds4worldcup的Kimi 300 Agent数据集（300个AI角色预测世界杯）

**重要说明**：此前错误声称cds4worldcup有"300条人工标注"。经核实：(1) 300条是Kimi AI生成的Agent预测意见，不是人工标注；(2) 原本设计的codability人工标注从未执行（被Reason Recoverability Gate卡住）；（3）标注材料（Excel/rubric/指南）已准备但deferred。

**当前定位**：降级为P8（市场校准）的补充章节，不作为独立论文。理由：n=24场比赛的样本量限制统计功效；标注未执行。

### P10：混合式Agent QA框架

从cds-keyperson的8维质量保证系统派生。工程感较强，理论新颖性需强化。建议降级为P2论文的讨论章节。

---

## §8 P11：内心独白→RoleDNA角色一致性验证（Tier 1 升级）

### 用大白话说

> 目前的Agent推演只能看到最终决定（"我建议调动3台泡沫车"），看不到Agent"是怎么想的"。DeepSeek-V4支持在`<think>`标签中暴露内心独白——比如"（我担心的不是火势本身，而是下风向的化工厂……我得优先保护那个方向）"。P11要做的是：让Agent在`<think>`里写出自己怎么想的，然后验证这些想法跟它被分配的RoleDNA人设是否一致——一个"风险偏好低"的Agent不应该内心独白说"赌一把"。

### 为什么重新评估为Tier 1

之前的v4.0判断"不值得独立论文"，基于两条理由。深度反思后，这两条都不成立：

**理由1"仅适用1个模型"的反驳**：PolicySim仿真引擎本身就绑定DeepSeek-V4——换模型意味着换整个Agent行为模式。研究范围不需要超越PolicySim自身。而且，论文的贡献不是"prompt技巧"，而是"通过暴露思考过程来验证角色一致性"这一方法论——这个方法可以推广到任何支持think标签的模型。

**理由2"效果是概率性的"的反驳**：概率性不意味着不可研究。论文可以报告触发率（如"93%的回合中内心独白成功生成"），并把未触发的回合作为对照组——这反而增加了实验的丰富性（自动产生的对照组）。

### 核心研究问题

> **"在RoleDNA驱动的多Agent推演中，暴露Agent的内心独白（角色沉浸模式）是否提升了角色行为一致性？更一致的角色是否导致了更真实的群体涌现行为？"**

### 为什么有学术价值

1. **角色一致性是未探索维度**：当前LLM Agent论文关注"决策质量""推理能力"，但几乎无人系统研究"Agent的行为是否跟它被分配的人设一致"。内心独白提供了测量一致性的直接窗口。

2. **与RoleDNA形成闭环**：cds-keyperson的Role DNA定义了5维行为基因（risk_tolerance/time_preference/market_power/policy_sensitivity/coordination_style）。内心独白可以直接暴露Agent在这些维度上的"真实感受"，从而验证RoleDNA是否真正控制了Agent行为——而非仅仅是一行被忽略的prompt。

3. **可审计性基础设施**：内心独白天然是决策的可审计证据链——"我担心X→我决定Y"的完整推理过程被暴露，比只看输出要可信得多。

4. **与P3（可解释性）的天然互补**：P11是"过程可解释性"（让思考过程可见），P3是"结果可解释性"（让决策链路可视化）。两者可以合并为单一论文（详见§12）。

### 实验设计（3模式 × 古雷场景 × 50次推演）

```
模式A（默认）：Agent不输出think标签（当前PolicySim基线）
模式B（角色沉浸）：Agent在<think>中输出括号包裹的内心独白
模式C（纯分析）：Agent在<think>中输出纯逻辑分析（无内心独白）

每个模式50次MC推演，古雷石化场景。
```

**评估维度**：
1. 角色一致性（RoleDNA Fidelity）：LLM Judge评估Agent行为与分配RoleDNA的匹配度（5维基因各打分1-5）
2. 决策质量：6维指标（与P1/P2相同基线）
3. 群体涌现真实性：Multi-Judge评估群体交互是否呈现真实应急场景的典型模式
4. 内心独白触发率：统计`<think>`标签的成功生成率

### 里程碑

| 阶段 | 要做的事 | 耗时 |
|------|---------|------|
| M1 | 在PolicySim中集成deepseek_v4角色沉浸指令 | 1周 |
| M2 | 3模式×50次推演实验 | 1-2周 |
| M3 | RoleDNA一致性评估（LLM Judge自动评分） | 1周 |
| M4 | 论文写作+投稿 | 2-3周 |

> **论文出口**：ACL 2027 / EMNLP 2027（Agent行为分析 + NLP角色扮演交叉）
> **核心贡献**：(1) 提出"角色一致性"作为LLM Agent评估的新维度；(2) 内心独白作为测量工具的方法论；(3) RoleDNA→行为一致性的定量证据
> **AutoResearch**：✅ 零人工（LLM Judge自动评分角色一致性，不用真人评估）

### 可能与P3合并

P11（内心独白→角色一致性）和P3（决策可解释性）可以合并为论文：*"Inner Monologue as a Window into Multi-Agent Reasoning: Role Consistency and Decision Transparency in Emergency AI Systems"*。贡献：§1内心独白方法论 + §2角色一致性验证 + §3决策可解释性可视化 = 完整的"AI决策透明度"论文。目标：ACL 2027。

---

## §9 P12：LLM Judge校准方法论（新增）

### 用大白话说

> cds4polymarket有一个成熟的Judge校准系统——用3个"标准答案"（Gold-H/M/L）来检查LLM裁判有没有"跑偏"。这个方法本身就能写一篇方法论短文。

### 来源

cds4polymarket的`calibration_lib.py:34-38`定义了Gold-H/M/L三个锚定样本，`ab-test/gold-calibration-design.md`描述了完整的3绝对+3成对对比+漂移检测的校准方法。

### 为什么值得独立成文

LLM-as-Judge是2024-2026最热的评估范式，但几乎所有论文都忽略了"Judge自身的校准"问题。cds4polymarket的Gold Sample锚定 + Pairwise漂移检测提供了一个轻量但系统的方法。这是一个**方法论短文**（short paper / findings），而非长篇大作。

### 实验设计

基于17轮AB测试中的Judge评分数据，分析校准效果：
- 无校准 vs Gold锚定校准 → 评分一致性差异
- 跨轮次Judge漂移检测 → 漂移幅度与Gold锚定的恢复效果
- 不同LLM Judge的校准特性对比

> **论文出口**：ACL Findings / EMNLP Findings（短论文track，4页）
> **核心贡献**：Gold Sample锚定校准方法 + 17轮真实AB测试的实证验证
> **AutoResearch**：✅ 零人工（17轮数据现成，纯统计分析）

---

## §10 仓库代码资产地图

### 5个仓库的核心能力一览

| 仓库 | 规模 | 核心资产 | 贡献课题 |
|------|------|---------|---------|
| PolicySim v0.2 | 1232测试 | MC推演引擎、古雷/郑州/洪水3场景 | P1-P6基础设施 |
| cds-keyperson | 24K行/1322测试 | SignalFusionEngine(267行链)、Role DNA(5维基因)、8维QA、5种Memory、266次仿真Vault | P7(信号融合)、P1(RoleDNA增强)、P3(trace系统) |
| cds4polymarket | 21K行/106测试 | Polymarket API(基础)、15+轮AB测试(27目录)、Judge校准(Gold-H/M/L)、Black Swan分析 | P8(市场校准)、P2(Judge校准复用) |
| cds4worldcup | 10K行/44测试 | FIFA路径仿真、Factor Ledger结算(3场验证)、Kimi 300 Agent数据集、Multi-Judge裁决 | P2(结算协议)、P5(路径空间) |
| policysim-research-Tsinghua | 630 runs | MAMR vs SASR主实验(5假设支持)、25效应本体、14机制库、Nature ComSci论文 | P10(630 runs验证)、P1(RoleDNA方法) |

### 关键缺口（已核实）

| 缺口 | 影响 | 需做什么 |
|------|------|---------|
| Brier/Log Loss自动计算不存在 | P8的M4无法自动化 | 实现calc_brier.py(~50行) |
| Factor Ledger仅设计无代码 | P8/P2不能直接使用 | P2按设计从零实现或P8手动评估 |
| Kimi 300标注未执行 | P9独立论文不可行 | 找2名标注者或降级 |
| SignalFusionEngine仅267行 | P7算法简单 | 不影响实验，但论文需坦诚说明 |
| Polymarket API无rate limit | P8大规模调用受限 | 按需补充retry逻辑 |

---

## §11 论文合并分析

### 问题

12个课题中是否有可以有机组合成更大论文的？答案是**有两组可以**。

### 合并方案A：P1 + P2（"信息-决策-校准"闭环）⭐⭐⭐

P1（RAG知识注入）和P2（Factor Ledger校准）共享：
- 同一MC推演引擎（PolicySim）
- 同一应急场景（古雷石化）
- 同一知识源（课题三知识库API）

合并论文结构：*Knowledge-Infused Multi-Agent Emergency Deliberation with Self-Calibrating Factor Analysis*
§1 RAG方法论（信息输入）→ §2 Factor Ledger方法论（输出评估）→ §3 古雷实证验证→ §4 闭环讨论
**策略**：先各自写独立论文投稿ACL/EMNLP。两篇都中了之后，再写一篇JAIR/AIJ synthesis journal paper。

### 合并方案B：P3 + P11（"AI决策透明度"完整论文）⭐⭐⭐⭐

**这是新发现的最佳合并方案。**

P11（内心独白→角色一致性）和P3（决策可解释性）是天然的上下游关系：
- P11提供"过程透明度"：Agent怎么想的（`<think>`内心独白）
- P3提供"结果可视化"：把想法→决策→后果画成图

合并论文结构：*Inner Monologue as a Window into Multi-Agent Reasoning: Role Consistency and Decision Transparency in Emergency AI Systems*
§1 内心独白方法论（过程透明度）→ §2 角色一致性验证（RoleDNA fidelity）→ §3 决策链路可视化（结果透明度）→ §4 完整透明度框架
**优势**：P3原在XAI领域竞争激烈，但加上P11的"内心独白"角度后，变成了Agent内部状态的独特研究方法——差异化大幅提升。**推荐直接合并投稿ACL 2027。**

### 不合并

P8（市场校准）方法论足够独特，独立成文更好。P7（信号融合）+ P10（QA框架）研究问题不同，强行合并牵强。

**建议策略**：先独立投稿P1和P2各一篇。如果两篇都中了，再写一篇synthesis journal paper（JAIR/AIJ），定位为"方法论的完整闭环"。

**P7 + P10：不建议合并**
P7（信号融合）和P10（QA框架）虽有公共基础设施但研究问题不同——一个是"信息预处理"，一个是"后验评估"，强行合并逻辑牵强。

**P8：独立最优**
P8（市场校准）的方法论足够独特，与Polymarket的外部校准场景绑定紧密，独立成文更好。

---

## §12 AutoResearch已初始化项目

位于 `/Users/tangzw119/Documents/GitHub/auto-research/`：

```
auto-research/
├── p1.1-inner-monologue/         # P11: 内心独白→RoleDNA一致性（NEW）
│   ├── state/task_spec.md
│   ├── state/progress.json
│   └── logs/
│
├── p1.2-market-calibration/      # P8: 预测市场校准
│   ├── state/task_spec.md        # 已验证（Brier需实现/Factor Ledger仅设计）
│   ├── state/progress.json       # {human_checkpoints: {M2: pending}}
│   └── logs/
│
└── p2.1-signal-fusion/           # P7: 信号融合
    ├── state/task_spec.md        # 已验证（267行链/12 active datasources）
    ├── state/progress.json       # {data_source_groups: A/B/C预定义}
    └── logs/
```

每个项目遵循Deli_AutoResearch协议（零交互/状态外化/新鲜会话/停滞检测）。

---

## §13 执行节奏（Q3 2026）

```
Week 1-2 (7月):
  Tier 1: P2 Factor Ledger Schema + 因子提取器开发
  Tier 1: P1 KnowledgeRetriever管道开发
  Tier 1: P11 内心独白指令集成 + 3模式推演(150次)
  辅助:   P8 AB测试数据提取 + Brier计算实现(~50行)

Week 3-4 (7-8月):
  Tier 1: P2 Sobol分析(1000推演) + P1 4组实验(400推演)
  Tier 1: P11 RoleDNA一致性LLM Judge评分
  辅助:   P8 案例事件候选池生成（等人工选择M1.5）

Week 5-6 (8月):
  Tier 1: P2 反事实推演 + P1 统计分析 + 论文初稿
  Tier 1: P11 统计分析 + 论文初稿
  Tier 2: P8 因子评估 + 知识写回实验

Week 7-8 (8-9月):
  Tier 1: P2+P1+P11 三篇论文修改+投稿
  Tier 2: P7 信号融合实验启动（预配置完成）
```

---

## §14 不做清单

| 事项 | 原因 |
|------|------|
| 建独立知识图谱/向量数据库 | 与课题3重复，知识库API已支持 |
| 全模态PoC（图像/视频/语音） | 上游API未就绪 |
| 物理模型集成 | 课题二API未就绪 |
| 24小时监控平台 | 非课题五KPI |
| P11独立成论文 | 方法仅适用1模型，效果概率性 |
| P9 Codability独立成论文 | 标注未执行+n=24限制 |
| 从零构建SignalFusionEngine | cds-keyperson已有 |
| Kimi 300标注重新做 | 被gate卡住，暂不推动 |

---

## §15 术语表

| 术语 | 解释 |
|------|------|
| MC（蒙特卡洛） | 多次随机模拟取平均值的方法。类似掷1000次骰子看分布。 |
| Agent | AI驱动的模拟角色（如"消防指挥Agent""医疗Agent"） |
| RAG（检索增强生成） | 让AI在生成回答前先查资料 |
| Factor Ledger（因子账本） | 记录"哪些因素影响了决策"的系统化数据库 |
| CDS（计算决策空间） | 把复杂决策问题转化为可计算、可推演的模型 |
| Sobol敏感度分析 | 一种数学方法，算出每个输入变量对最终结果的影响大小 |
| Brier Score | 预测准确度的评分（0=完美，1=全错，0.25=瞎猜） |
| Ablation（消融实验） | 逐个移除系统组件，看性能下降多少——证明每个组件有用 |
| 反事实推演 | "如果当时不这样做，会怎样？"的模拟分析 |
| Polymarket | 用真金白银下注的预测市场平台 |
| Multi-Judge裁决 | 多个AI裁判角色分别判断同一件事，看他们是否一致 |

---

## 附录

### 参考文件
- 课题五中期报告（H0-H4架构 + 知识库五层双驱动）
- PolicySim Roadmap: `docs/roadmap/2026-06-07-cds-12month-roadmap.md`
- 三方评估: `topic5-three-way-assessment.md`
- Deli_AutoResearch Framework: `0ref/skill/victorchen96.github.io/auto_research/framework.html`
- deepseek_v4_roleplay_instruct: `https://github.com/victorchen96/deepseek_v4_rolepaly_instruct`

### 代码仓库
- `~/Documents/GitHub/Policysim-v0.2` — MC推演引擎（主战场）
- `~/Documents/GitHub/cds-keyperson` — SignalFusionEngine + Role DNA（23K行）
- `~/Documents/GitHub/cds4polymarket` — Polymarket校准场（21K行）
- `~/Documents/GitHub/cds4worldcup` — Factor Ledger结算（10K行）
- `~/Documents/GitHub/policysim-research-Tsinghua` — MAMR/SASR学术主线（630 runs）

### AutoResearch目录
- `~/Documents/GitHub/auto-research/p1.2-market-calibration/`
- `~/Documents/GitHub/auto-research/p2.1-signal-fusion/`


---

## §16 决策路径方法论（2026-07-03 沉淀）

> **来源**：`legacy/p11-closed-v5-minimax-m3/wiki/decisions/2026-07-03-comprehensive-synthesis.md`
> **不修改以上任何文字**——这是为未来项目沉淀的方法论

### 16.1 核心方法：硬决策 + 回退条款

**当面对** 12+ 个候选路径 + Gate 4 评分低（5.0/5.2 vs 目标 7.0+）+ 2 个月时间已花 + 多 reviewer 反馈 — **采用 3 步决策流程**：

| 步骤 | 动作 | 目的 |
|------|------|------|
| **1. 选 1 条主路径 + 明确回退条件** | 选 ROI 最高的路径；写硬性回退条款（如 "IF X at checkpoint THEN Y"）| 终止 oscillation |
| **2. 选 1 个 hard checkpoint** | 决策路径上设单一时间点 + 单一 GO/NO-GO 指标 | 给振荡系统 single attractor |
| **3. 选 1 个 fallback** | 失败时的次优目标 + 时间预算 | 限制下行情境 |

### 16.2 工程控制论 3 类反馈循环诊断

每个长期项目都存在 3 类反馈循环：

| 循环 | 诊断 | 修复 |
|------|------|------|
| **文字修复循环**（文字层 actuator）| 文字层变化不能 escape 到 7.0+ | 改为结构层 actuator（换实验设计/数据） |
| **核心假设验证失败循环**（H1 falsified） | pivot 到替代假设（H1c/H3）但要改 paper story | 改 paper 故事 + 承认 negative result |
| **路径选择循环**（path 振荡，12+ paths）| 选 1 条 + hard checkpoint | 终止 LIMIT CYCLE |

**诊断问句**：
- "这是 structural 还是 text-level 问题？"
- "3 个 feedback loop 哪个没 fixable？"
- "hard checkpoint 在哪里？"

### 16.3 4 视角评审（每次决策前必跑）

| 视角 | 关注 | 关键问题 |
|------|------|---------|
| **工程应用方** | "能 deploy 到 production 吗？" | "这个 finding 能 reproduce 吗？" |
| **项目方（课题五）** | "4 deliverables 满足吗？" | "项目能 close 吗？" |
| **论文 reviewer** | "会 accept 吗？" | "7.0+ 吗？novelty 够吗？" |
| **学术价值** | "5 年后有人 cite 吗？" | "这贡献有 durable identity 吗？" |

### 16.4 12+ Path 分类法（避免"路径爆炸"）

每次 brainstorm 路径时，**强制 4 分类**：

| 分类 | 问题 | 推荐度 |
|------|------|------|
| **A. Fix existing data** | 数据错了修 / 故事错了重写 | 高 ROI（如 6 blockers fix 1-2 周）|
| **B. New paper with existing data** | 新角度新标题新 hook | 中高 ROI（重新包装 F1 即可）|
| **C. Re-run** | 重做实验 | 低 ROI（除非 baseline 验证）|
| **D. Restart** | 换研究问题 | 极低 ROI（除非有反预期发现）|

**推荐 99% 选 A 或 B**——C/D 只在 A/B 失败时考虑。

### 16.5 Gate 4 评分诊断 checklist（每次投 paper 前）

按重要性排：

| 优先级 | 检查项 | 修复难度 |
|------|------|---------|
| 🔴 P0 | 数据完整性（parse failure <5%）| 低（修 prompt 或 structured output）|
| 🔴 P0 | 测量可靠性（inter-rater κ>0.4）| 中（修 rubric）|
| 🔴 P0 | 样本量 power analysis | 低（增 N）|
| 🟡 P1 | 统计方法完备性（post-hoc + effect size + CI）| 中 |
| 🟡 P1 | 因果 identification 明确 | 高（可能要重设计实验）|
| 🟢 P2 | 论文故事（problem → method → result → insight 流畅）| 中（重写）|
| 🟢 P2 | 写作清晰度（abbreviation 定义、figure 充分）| 低 |

### 16.6 立即决策的 3 选项

每次 long-running paper 项目**必须有**这 3 选项之一：

1. **Hard checkpoint 路径**（如 360-run 验证 hybrid 78% vs 32%）
2. **直接 fallback paper**（用现有 H1c + H3 写 workshop paper）
3. **状态保持**（❌ 不要选这个——会无限振荡）

**不要选 3**——它就是问题。

### 16.7 方法论总结

> **核心**：每个 research 项目必须有 (a) 一条主路径 + hard checkpoint + fallback + (b) 清晰的停止条件 + (c) 终止振荡的机制。
> 
> 没有这三件事的项目 = doomed loop。

---

> **用法**：当新项目陷入"我该走哪条路"困局时，回到 §16.1 决策流程。
