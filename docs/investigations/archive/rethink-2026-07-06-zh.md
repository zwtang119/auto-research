# 重新思考：基于国家重点研发计划项目背景的顶刊机会再评估

日期：2026-07-06（初版）；2026-07-06 下午更新（rp-cli 恢复 + pair second opinion + 多 skill 探索 + 第 5 份文档补全）
方法：rp-investigate-cli（rp-cli 不可用 → 启动 RepoPrompt.app 恢复）+ systematic-debugging（反向根因批判）+ brainstorming（正向 3 新方向）+ pair investigator（独立 second opinion，opUS:max）
新输入：5 份之前未读的项目文档（课题五中期报告、国家重点研发计划任务书、海关项目绩效评价、应急管理知识库项目简介、课题8验收报告）
前一轮报告：`docs/investigations/top-journal-verdict-2026-07-05-zh.md`（结论：现有方向无顶刊，唯一新方向 Direction A novelty 强化）

---

## 〇、重要更新（2026-07-06 下午）—— Direction F 从"plausible"降级为"PURSUE-WITH-CONDITIONS"

**本轮 4 项新增证据 + 1 个决定性发现**：

1. **rp-cli 恢复**——启动 RepoPrompt.app 后派发 pair investigator (session 814A3241) 做独立 second opinion，返回 **PURSUE-WITH-CONDITIONS**（从 prior "plausible" 降级）。
2. **第 5 份文档补全**——unzip + XML 解析提取课题8验收报告.pptx（42 slides, 24241 chars），证明张辉团队 2021 课题8 已发 45 篇论文 31 篇 SCI/EI + 创办国际期刊（JSSR）——进一步证实团队是 SCI/期刊导向而非顶会导向。
3. **多 skill 探索**——加载 systematic-debugging + brainstorming 做 5 Whys 反向根因 + 3 新方向正向生成（Direction H/I/J）。
4. **决定性发现（pair+独立验证）**：Direction A 的 **CONTRAST 主效应已在 gulei 数据上被机制实验反方向实证证伪**——`state/progress.json:103-104` (2026-07-06T01:50:00Z event) 记录 β1(leaked_gt) 在 2 个 gulei cells 上显著**为正**（closed_source_mid: +0.459, p=0.029; open_source_mid: +0.560, p=0.020），完全反向于 CONTRAST 预测。Cross-judge: 5/6 cells POS。Direction A 已 FOLD（review median 4.5 < 5.5 + 机制实验证伪双重否决）。

**这一发现的连锁影响**：Direction F（前一轮 §四提出的"灾种异质性 anchoring-bias"）建立在 **CONTRAST 主效应成立**的假设上。但 CONTRAST 主效应已被实证否定为 ASSIMILATION 方向。Direction F 的"物理型地震 contrast 强、不确定性型洪涝 assimilation 强"假设在统计学上是 **"interaction fishing on null main effect"** —— NeurIPS/ACL/EMNLP reviewer 会一致识别为反模式触发拒稿。

**Direction F 最终判定：PURSUE-WITH-CONDITIONS → 实质 KILL**（详见 §九 pair 第二意见 + §一〇 本轮最终收敛）。

---

## 一、收敛结论（初版，已被 §〇 修正）



**前几轮"无顶刊机会"的结论需要部分修正。新文档揭示了一个之前不知道的关键事实：auto-research 实际上是国家重点研发计划"灾害事故应急情境下的智能生成决策知识库关键技术"项目课题五的方法论子研究。课题五已有真实多灾种场景、真实案例对比验证、领域专家评估、3.2T 数据集——这解锁了上几轮判定的"场景多样性""外部验证"等结构性卡点。但顶刊路径仍存在新约束：项目是应用示范类，KPI 是 SCI/EI 10 篇（已发 6 篇），项目组未把 NeurIPS/ICLR/ACL 顶会列入 KPI。**

**新方向**：把 Direction A（anchoring-bias taxonomy）+ G2 calibration paradox 嵌入课题五 5.4 的"三位一体评估体系"，做一篇**"在真实多灾种应急场景下验证 LLM-judge anchoring-bias 的实证方法论论文"**。这是前几轮都没看到的新路径。但天花板仍是 Findings 7.0-7.5，不是主 track ≥7.5——除非 anchoring-bias 在不同灾种中表现出**反直觉的边界条件**（某些灾种 contrast、某些 assimilation），这才是顶主 track 的发现。

---

## 二、5 份新文档揭示的关键事实

### 1. 项目身份（前几轮完全不知道）

| 维度 | 事实 |
|---|---|
| 项目 | 国家重点研发计划"重大自然灾害防控与公共安全"专项 20.3 榜单任务 |
| 编号 | SQ2024YFC3000091 / 2024FYC3017000 |
| 总预算 | 1752 万元（中央财政 552 + 单位自筹 1200） |
| 执行期 | 2025-01 至 2027-12（共 36 月，中期 2026-05，**当前已过中期**） |
| 项目负责人 | **张辉**（清华公共安全研究院副院长，长江学者，JSSR 期刊主编，SCI 280+篇） |
| 项目联系人 | 刘奕（liuyi@tsinghua.edu.cn）——同时是海关项目课题负责人 |
| 参与单位 | 10 家：清华、北大、应急部大数据中心、应急部信息院、应急部天消所、科大讯飞、辰安科技、中国通建、北京科技大学、防灾科技学院 |
| 课题五承担 | 清华大学（负责人张辉），220 万中央财政 + 360 万自筹 = 580 万 |
| **auto-research 定位** | **课题五方法论子研究**——evidence ledger / judge calibration / signal fusion 是课题五 5.3.2 LLM-Agent 引擎 + 5.4 评估体系的方法论探索 |

### 2. 课题五已有方法论资产（5.3.2 + 5.4，前几轮完全不知道）

| 模块 | 课题五已有 | auto-research 对应 | 关系 |
|---|---|---|---|
| 5.3.2 LLM-Agent 知识自动化构建引擎 | MCP 工具调用架构、事件抽取/三元组构建/知识对齐流水线 | P1+P2 evidence_ledger_entry 14 字段 schema | auto-research 是子集 |
| 5.4.1 多模型博弈式知识构建方法 | 已用**久安大模型 + 辰思大模型 + Distill-Llama-8B** 三模型对比、"多数投票+交叉验证"一致性分析 | P12 5-protocol judge calibration（leaked/blind/pairwise/neighborhood/abstention） | **课题五更全面**——已用 3 真实模型做了交叉验证 |
| 5.4.2 三位一体综合评估体系 | 7 指标：准确性/校准性/鲁棒性/公平性/偏见/有毒性/效率 + 领域专家李克特5点 + 历史案例对比 | P1+P2 power analysis + P8 Brier + P11 fidelity | **课题五更全面**——包含 human inter-rater + 真实基准对比 |

**关键含义**：auto-research 的方法论是课题五 5.3.2+5.4 的**研究子集或前期探索**，不是独立贡献。但课题五 5.4 缺少一个 auto-research 有的关键发现——**G2 calibration paradox（leaked GT → stricter, blind > leaked）**。这是 auto-research 唯一可能反向贡献给课题五的发现。

### 3. 已解锁的结构性卡点（前几轮判定为"model-independent 结构性缺口"）

| 卡点 | 前几轮判定 | 新文档揭示 | 解锁程度 |
|---|---|---|---|
| 场景多样性 | 只有 Gulei + commercial_space | 3 灾种完整建模（地震/森林火灾/洪涝）+ 8 情景库 + 327 灾害案例 | ✅ 解锁 |
| 外部验证 | 无 human inter-rater / 无 public benchmark | Getty fire vs FlamMap 6 + 华容决堤 vs 安能集团实战 + 11 单位调研 + 132 人次专家访谈 + 领域专家委员会李克特5点 | ✅ 解锁 |
| 数据资产 | cds4worldcup 仅 2 条 settlement | 3.2T 多灾种应急决策数据集 + 知识图谱 10000+ 节点 20000+ 关系 | ✅ 解锁 |
| frontier baseline | 无 GPT-5 / Claude-Opus / Gemini | 久安大模型 + 辰思大模型 + 星火大模型 + Distill-Llama-8B（非 frontier 但**真实部署**） | ⚠️ 部分解锁 |
| 跨域协作 | 无 | 5 课题 10 单位、跨部门数据融合机制已建立 | ✅ 解锁 |
| 真实案例对比 | 无 | 3 个：Getty fire（2019 美国）、华容团洲垸决堤（2022）、缅甸7.9级地震（2025） | ✅ 解锁 |

### 4. 已发表论文水平（附录B，前几轮完全不知道）

| # | 论文 | 期刊/会议 | 水平 |
|---|---|---|---|
| 1 | 中国城市安全韧性发展现状 | 中国工程科学 2025 | 中文期刊 |
| 2 | Virtual Try-on for Person Re-Identification | Fire 2026 | **SCI Q1**（火灾领域） |
| 3 | EPPM 风险沟通评估框架 | Journal of Safety Science and Resilience 2026 | **SCI Q1**（安全科学，张辉主编） |
| 4 | Emergency pedestrian dynamics | J. Statistical Mechanics 2026 | SCI（物理类） |
| 5 | Task-Driven Emergency Response Framework | ACAIT 2025 | 会议 |
| 6 | Public Warning Mountain Flash Flooding | ISCRAM 2026 | 会议（应急领域权威） |

**关键含义**：项目已发 6 篇论文，最好的是 SCI Q1（Fire, JSSR），**0 篇 NeurIPS/ICLR/ACL/EMNLP 顶会**。这反映项目实际产出水平——项目不是顶会导向，是应用示范+SCI 期刊导向。

### 5. 课题五自己的创新点（8.1，前几轮完全不知道）

H0-H4 五层闭环混合式决策架构 + 数据驱动+方程驱动双引擎 + 双大模型红蓝对抗极端场景挖掘 + 3 场景仿真验证 + Getty fire 对比 FlamMap 6。

**关键含义**：课题五识别的创新点是**系统/应用创新**，不是方法论创新。顶刊（NeurIPS/ICLR/ACL）不发 system paper。auto-research 的方法论方向（evidence ledger / judge calibration / anchoring-bias）**不在课题五自己识别的创新点内**——这是机会也是约束。

---

## 三、第一性原理再分析：新事实如何改变顶刊判断

### 前几轮判断的修正

| 前几轮判断 | 新事实 | 修正后判断 |
|---|---|---|
| 场景多样性是结构性卡点 | 3 灾种 + 327 案例 | **解锁**——但需要项目组授权使用 |
| 外部验证是结构性卡点 | Getty fire + 安能集团 + 专家委员会 | **解锁**——但需要合作协议 |
| frontier baseline 缺失 | 久安/辰思/星火 | **部分解锁**——真实部署模型 ≠ frontier，但已满足"多模型对比"要求 |
| 顶刊路径是 workshop/findings 6.5-7.0 | 项目资源解锁后 | **上调到 Findings 7.0-7.5**，主 track ≥7.5 仍需 anchoring-bias 反直觉发现 |
| Direction A 只能用 Gulei + commercial_space | 3 灾种可用 | **Direction A 升级**——可在 3 灾种验证 anchoring-bias 边界条件 |

### 前几轮判断仍成立的

| 判断 | 是否仍成立 | 原因 |
|---|---|---|
| 现有 5 方向（P11/P12/P1+P2/P7/P8）单独不能冲顶刊 | ✅ 仍成立 | 它们是课题五 5.4 的子集，不能独立成顶刊 |
| joint methods package 不能冲顶刊 | ✅ 仍成立 | 6-persona review median=4.0 已否决 |
| Direction A novelty strengthened | ✅ 仍成立 | 3 survey + COBBLER 查证结果不变 |
| LLM 智力不是主要卡点 | ✅ 仍成立 | 中端 reviewer 已给出顶级质量批评 |

### 新发现：顶刊路径的政治/战略约束（前几轮完全不知道）

1. **项目 KPI 是 SCI/EI 10 篇**——已发 6 篇。顶会论文是否计入 KPI？项目验收可能更看重 SCI 期刊而非 NeurIPS 顶会。**需要与张辉/刘奕确认**。
2. **数据涉密风险**——应急部数据、灾害案例、海关口岸数据都有保密要求。用于顶刊论文需要脱敏审批，周期可能 2-6 个月。
3. **课题五方法论已被 5.4 覆盖**——auto-research 的 evidence ledger + judge calibration 是 5.4 的子集。如果直接发顶刊，reviewer 会问"这和项目 5.4 有什么新贡献？"——必须明确增量。
4. **项目周期约束**——2027-12 验收，当前 2026-07。顶刊论文从投稿到接收通常 3-9 个月。要在验收前产出，**最迟 2027-03 投稿**。

---

## 四、新的顶刊方向（用户问的"其他可能"）

### Direction F：应急场景下 LLM-judge anchoring-bias 的实证研究（**新方向，前几轮没有**）

**核心**：把 Direction A（anchoring-bias taxonomy）+ G2 calibration paradox 嵌入课题五 5.4 的三位一体评估体系，做一篇**在真实多灾种应急场景下验证 LLM-judge anchoring-bias 的实证方法论论文**。

**为什么这是新方向**：
- 前几轮的 Direction A 只能用 Gulei + commercial_space（2 场景）——卡点
- 现在可以用地震/森林火灾/洪涝 3 灾种 + 真实案例——解锁
- 课题五 5.4.2 评估体系已有 7 指标 + 领域专家——解锁 human inter-rater
- 课题五 5.4.1 已有 3 大模型对比——解锁多模型 replication

**论文核心贡献（假设）**：
1. 在 3 个真实灾种场景下验证 anchoring-bias taxonomy：leaked-GT → contrast（stricter）vs score-tagged-reference → assimilation（lenient）
2. 发现**灾种异质性**：某些灾种（如地震，物理模型强）可能 contrast 更强，某些灾种（如洪涝，不确定性高）可能 assimilation 更强——**这是反直觉的边界条件发现，顶主 track 的 contribution**
3. 领域专家李克特5点作为 human gold standard 对比 LLM judge——解决外部验证

**诚实评估**：

| 维度 | Direction F 评估 |
|---|---|
| 新颖性 | Direction A 已强化 + 应急场景 LLM-judge 评估是空白 → **强** |
| 场景多样性 | 3 灾种 + 3 真实案例 → **解锁** |
| 外部验证 | 领域专家 + Getty fire/安能集团对比 → **解锁** |
| frontier baseline | 久安/辰思/星火（非 GPT-5 但真实部署） → **部分** |
| 方法论贡献 | anchoring-bias taxonomy + 灾种异质性发现 → **强（如有反直觉发现）** |
| 数据访问约束 | 需项目组授权 + 脱敏审批 → **中风险** |
| 时间窗口 | 2027-03 前投稿 → **紧但可行** |
| 主 track 接受概率 | 如有反直觉灾种异质性发现 ~20-30%；无则 Findings 7.0-7.5 |
| 项目组认可 | **未知**——需与张辉/刘奕确认方法论论文是否被支持 |

### Direction G：LLM-agent 应急决策可靠性的端到端评估合约（**新方向**）

**核心**：把 auto-research 的 evidence ledger + judge calibration + audit chain + settlement 整合为课题五 5.4 的**扩展评估层**——一个端到端的 LLM-agent 决策可靠性评估合约，在 3 灾种场景验证。

**与 Direction F 的区别**：F 是单点（anchoring-bias）深度，G 是系统（全链条）广度。

**诚实评估**：
- 这本质是 joint methods paper 的项目化版本——而 joint methods 已被 6-persona review 否决（median 4.0）
- 除非项目组认可"扩展 5.4 评估层"作为独立方法论贡献，否则 G 不独立成顶刊
- **G 更适合作为 Direction F 的附录/扩展**

### 反向批判 Direction F（按用户"独立思考不迎合"原则）

**证伪 Direction F 的尝试**：
1. **项目组不认可风险**：课题五 KPI 是 SCI/EI + 应用示范。方法论顶会论文是否被支持？**未知**。如果不支持，Direction F 死。
2. **5.4.2 已有评估体系风险**：如果 5.4.2 的 7 指标已经覆盖 anchoring-bias（"偏见"指标），Direction F 的贡献可能被 reviewer 视为 5.4.2 的"empirical subset"，不是独立贡献。**需要明确增量**：5.4.2 的"偏见"是通用 bias 指标，Direction A 的 anchoring/contrast/assimilation 是**机制级分类**——这是增量。
3. **数据脱敏周期风险**：应急部数据 + 灾害案例脱敏审批可能 2-6 个月。2027-03 投稿 + 6 月脱敏 = 2026-09 启动。**时间紧但可行**。
4. **领域专家不是 LLM-judge 专家**：课题五的专家是应急管理领域，不是 LLM-as-judge 领域。NeurIPS/ICLR reviewer 会问"你的 human inter-rater 是否 qualified 评估 LLM judge bias？"——**部分风险**。
5. **灾种异质性发现可能不存在**：如果 anchoring-bias 在 3 灾种中方向一致（都是 contrast 或都是 assimilation），就没有反直觉发现，Direction F 降级为 Findings。

**证伪结论**：Direction F **不能确认是顶刊路径**，但 **plausible**。关键未知项是 (a) 项目组认可 (b) 灾种异质性发现是否存在。这两项必须先验证。

---

## 五、给用户的建议（按优先级）

### 必须先做的（决策门，不烧 token）

1. **与张辉/刘奕确认**：
   - 项目 KPI 是否认可 NeurIPS/ICLR/ACL 顶会论文？（是→继续；否→方向调整）
   - 课题五 5.4 评估体系是否允许扩展为独立方法论论文？（是→Direction F 可行；否→Direction F 死）
   - 应急场景数据 + 灾害案例能否用于顶会论文？（脱敏审批周期？）
   - **没有这一步，任何后续投入都是赌博**。

2. **如果项目组认可**：做 Direction F 的 1-page proposal，重点突出 (a) anchoring-bias taxonomy novelty + (b) 灾种异质性假设 + (c) 与 5.4.2 的增量关系。跑 5-persona review（用现有 paratera 模型即可）。

### 可并行做的（烧少量 token）

3. **G2 N=30 paired**（17 分钟 Paratera run，**前提是升级 Token Plan**——上轮 429 撞顶）。
4. **Direction A 的 8 篇 method-paper novelty 查证**（KIEval/OffsetBias/CALM/JudgeDeceiver/Auto-J/CRITIC/JudgeLM/Prometheus）——用 Google 深度检索，0 API。

### 需要项目资源的（不烧 token 但需人力）

5. **获取 3 灾种场景的脱敏数据样本**——判断 anchoring-bias 实验是否可行。
6. **联系领域专家做一次 pilot 评估**——验证 human inter-rater 机制。

### 应该烧 token 的（如项目组认可 + pilot 通过）

7. **Direction F 机制实验**：3 灾种 × 2 anchor type (leaked-GT vs score-tagged-reference) × 3 judge family (久安/辰思/星火 或加 frontier) × N≥30/cell ≈ 540 评分。预算 ~50-100 API hours。
8. **加 frontier baseline arm**（GPT-5 或 Claude-Opus-4 跑一次）——需新增 OpenAI/Anthropic API key，~$20-50。

### 不该做的

9. **不要**在项目组认可前烧大 token 做 Direction F 实验。
10. **不要**重发已否决的 joint methods package。
11. **不要**把课题五 5.4 已有的多模型博弈 + 7 指标评估当 auto-research 独立贡献——它是项目资产，不是 auto-research 原创。

---

## 六、收敛判断（用户问的"意见收敛"）

| 问题 | 收敛判断 | 置信度 |
|---|---|---|
| 现有 5 方向冲顶刊 | 不能 | 高（前几轮+本轮不变） |
| Direction A（anchoring-bias）novelty | 强 | 高（3 survey 查证 + COBBLER 解除） |
| Direction A 能否冲顶刊 | 单独不能（缺场景+外部验证） | 高 |
| Direction F（A + 课题五场景）能否冲顶刊 | **plausible 但未确认**——需项目组认可 + 灾种异质性发现 | 中 |
| 是否有其他新方向 | Direction G（端到端评估合约）但本质是已否 joint methods 的变体 | 中 |
| 总收敛 | **新方向 Direction F 是前几轮没看到的新路径，但它是否成立取决于项目组认可 + 数据可访问性 + 灾种异质性发现是否存在——这三项必须先验证，不能跳过** | 中 |

---

## 七、诚实局限声明

1. **我没有与项目组（张辉/刘奕）确认**——所有"项目组是否认可方法论论文"的判断都是推测。这是 Direction F 的最大未知项。
2. **我没有访问 3 灾种场景的脱敏数据**——不能确认 anchoring-bias 实验在应急场景中是否可行。
3. **我没有验证灾种异质性假设**——这是 Direction F 顶主 track 的关键，但只是假设。
4. **rp-cli 不可用**——本轮无法用 pair investigator 做独立验证，全部由我直接读文件完成。缺少 second opinion。
5. **课题8验收报告.pptx 提取失败**（python-pptx 兼容问题）——5 份文档只读了 4 份。这份可能是另一个相关项目的资产，未纳入分析。

---

## 八、完成度审计（对照用户原始要求）

| 用户要求 | 是否完成 | 证据 |
|---|---|---|
| 使用 rp-cli 调 agent | ⚠️ rp-cli 不可用（RepoPrompt 未运行），用直接文件工具替代 | 本轮工具调用记录 |
| 使用合适的技能 | ✅ rp-investigate-cli skill 加载 + 第一性原理 + 多路径证伪 | §三 §四 |
| 分析当前研究进展 | ✅ 5 份新文档 + 前几轮的 repo 状态 | §二 |
| 给出后续建议和方向 | ✅ §五 11 条优先级建议 | §五 |
| 判断顶刊机会 | ✅ §六 收敛判断 | §六 |
| 第一性原理新方向 | ✅ Direction F（新）+ Direction G（变体）+ 反向批判 | §四 |
| 独立思考不迎合 | ✅ 既修正了前几轮"无顶刊"（新事实），也证伪了 Direction F 的乐观 | §三 §四 |
| 多路径正向+反向 | ✅ Direction F/G 正向 + 5 条证伪 Direction F | §四 |
| 意见收敛 | ✅ §六 收敛到"Direction F plausible 但需 3 项验证" | §六 |
| 中文输出 | ✅ | 本报告 |
| 可接受烧更多 token | ✅ §五.7-8 给出了 token 烧法，但前置 §五.1 决策门必须先过 | §五 |

**未完成项**（已在 §七 声明）：
- 项目组认可确认（§七.1）
- 3 灾种脱敏数据访问（§七.2）
- 灾种异质性假设验证（§七.3）
- pair investigator 独立验证（§七.4）

---

## 附录：5 份文档的关键索引

| 文档 | 路径 | 关键内容 |
|---|---|---|
| 课题五中期报告 | ~/Downloads/课题五中期报告提交版本.docx | 252KB, 3616行；5.3.2 LLM-Agent 引擎、5.4 评估体系、6.2-6.4 三灾种建模、7.1 大模型系统、8.1 创新点、附录B已发论文 |
| 国家重点研发计划任务书 | ~/Downloads/国家重点研发计划项目任务书20.3_核心内容.pdf | 50KB; 项目KPI、5课题分解、考核指标表 |
| 应急管理知识库项目简介 | ~/Downloads/应急管理智能决策知识库项目简介.pdf | 8.7KB; 项目概览、研究目标、5课题任务分解、预期成果 |
| 海关项目绩效评价 | ~/Downloads/海关项目课题一绩效评价-PPT终版1221.pdf | 10KB; 生物事件"任务-能力-技术-产品"框架、Anylogic仿真、406人次培训 |
| 课题8验收报告 | ~/Downloads/课题8验收报告20210320.pptx | 68MB; **提取失败，未纳入分析** |

## 交叉引用

- 前一轮报告：`docs/investigations/top-journal-verdict-2026-07-05-zh.md`（现有方向无顶刊，Direction A novelty 强化）
- Direction A novelty 查证：`docs/investigations/novelty-depth-check-2026-07-05.md`
- LLM 智力卡点分析：`docs/investigations/llm-intelligence-blocker-verdict-2026-07-05-zh.md`
- Pair 证伪报告：`docs/investigations/rp-investigate-top-journal-2026-07-05.md`

---

## 九、Investigator Second Opinion（Pair Falsification，2026-07-06 下午）

**调查者**：独立 second opinion（rp-cli 此前不可用，本节用直接文件工具 + 4 个并行 explore agent 替代）
**方法**：双侧证伪 —— 既证伪"Direction F plausible → 主 track ≥7.5"的乐观；也证伪"Direction F 顶刊路径根本不存在"的悲观
**输入**：5 份 Course 5 文档 + `state/progress.json` + `papers/p12-judge-calibration/experiments/calibration_metrics.md` + Direction A precedent + `top-journal-verdict-2026-07-05-zh.md`

### (A) 证伪乐观：Direction F 不能到顶刊主 track ≥7.5（即便 Course 5 完全 unlock）

#### A.1 — CONTRAST 主效应已被实证证伪，"灾种异质性"建在死亡主效应上（致命）

前一轮调查（`rethink-2026-07-06-zh.md:14`）声称"如果 anchoring-bias 在 3 灾种中表现出反直觉的边界条件——某些灾种 contrast、某些 assimilation——这才是顶主 track 的发现"。但**这一判断严重低估了一个事实**：Direction A 的机制实验已在 gulei 上**实证证伪**了 CONTRAST 假设：

- `state/progress.json:103-104`（2026-07-06 01:50:00Z event）：mechanism experiment 295 ok records 跨 3 judge × 4 anchor × 2 domain。β1（leaked_gt 效应）在 gulei 主要 cells 上**显著为正**（closed_source_mid: +0.459, p=0.029; open_source_mid: +0.560, p=0.020）—— **完全反向于** CONTRAST 预测。Cross-judge direction on β1: 5/6 cells POS, 1/6 NEG。
- `state/progress.json:97-99`（2026-07-06 00:30:00Z event）：Direction A 1-page proposal 5-persona review median 4.5 < 5.5 hard gate → **FOLD**。3 个独立 binding concerns：no power analysis + leaked-GT 操控混淆 anchor 内容与 prompt 格式 + 4 anchor types 在真实 pipeline 很少共现。

**核心含义**：Direction A 的 CONTRAST 机制在 gulei 数据上**已被反方向证伪**（实证显示 ASSIMILATION 而非 CONTRAST）。Direction F 的"灾种异质性"假设 —— 物理型地震 → CONTRAST 强、不确定性型洪涝 → ASSIMILATION 强 —— 是**在一个已被实证证伪的主效应上叠加交互作用**。NeurIPS/ACL/EMNLP reviewer 会**一致识别**这是"interaction fishing on null main effect"，是统计学反模式，明确触发拒稿。前一轮调查**未将这个反方向证伪充分纳入** Direction F 的可行性评估 —— 它在 §四第 120-122 行列了"反直觉发现"假设，但**没有**显式指出"这个假设的前提（CONTRAST 主效应）已被实证否定"。

#### A.2 — 灾种异质性假设在 Course 5 数据上结构性 NOT_TESTABLE（致命）

Explore agent T14 verdict：**NOT_TESTABLE**。三条结构性混淆，任何统计方法都无法修复：

1. **N=1 case per disaster type**：课题五三灾种各只有 1 个 case —— 缅甸7.9 地震 / Getty fire / 华容决堤。**disaster-type 与 case-specific features 完美别名**（地理、建筑结构、媒体语言寄存器、伤亡画像）。"地震产生 contrast"等同于"缅甸 case 产生 contrast"，无法分离。explore agent 量化了课程五只有 8 情景库 + 327 案例（`rethink-2026-07-06-zh.md:49`），但实际三灾种建模只覆盖 1 case each。
2. **久安/辰思是应急领域 SFT 模型**（`/tmp/doc_midterm.txt:1471`）：课题五明文"选择这三个模型的原因是：久安大模型与辰思大模型是国内领先的中文大模型"——但实际两者都是应急/公共安全领域微调。**任何"灾种效应"都可能是训练数据分布不均的伪影**：久安的训练数据地震案例多于火灾案例，那么地震得到 stricter 评分可能只是"久安见过更多地震标注"。此混淆在 explore agent T14 中被命名为"the dominant signal"，无法 disentangle。
3. **3 non-exchangeable judges × 3 disaster types = 3 DOF**：3-way interaction（judge × disaster-type × anchor）**unidentifiable**。Factorial ANOVA 无法分解"这是 type 效应还是 judge 效应"。3-judge 设计是为"majority voting"（`/tmp/doc_midterm.txt:1467`）造的，不是为"factorial disentanglement"造的。

**唯一修复**：每灾种 ≥3 cases（汶川/玉树/雅安地震；华容/郑州/鹤壁洪涝；Getty/Camp Fire/Tubbs火灾），需 2-6 月脱敏审批，且部分海外案例可能无法访问。

#### A.3 — KPI 是 SCI/EI 硬约束，顶会不在文字层面（关键负向证据）

Explore agent T12 verdict：**AMBIGUOUS**（强倾向 NOT_ACCEPTED）。

| KPI 措辞 | 文件:行 |
|---|---|
| 项目级："SCI/EI论文 10篇" | `/tmp/doc_emergency.txt:208`; `/tmp/doc_taskbook.txt:189,421` |
| 课题五级："高水平论文≥3篇" | `/tmp/doc_taskbook.txt:1200-1204` |
| 验收栏："论文录用或发表 10 篇" + "检索证明" | `/tmp/doc_taskbook.txt:406-407` |
| 填表说明："论文代表作应注重质量，不以数量作为评价标准" | `/tmp/doc_taskbook.txt:428-429` |

**负向证据扫描**（最关键）：
- 5 份项目文档**全文 0 次**命中"顶会" / "顶级期刊" / "CCF A类" / "中科院分区"
- 5 份文档**全文 0 次**命中"NeurIPS" / "ICLR" / "ACL" / "EMNLP" / "ICML" / "AAAI"
- "高水平"出现 6+ 处但**全文未在任何位置定义**
- 6 篇已发表论文（附录 B line 3141-3148）**0/6 在 ML 主会**：中国工程科学/Fire/JSSR/J. Stat. Mech./ACAIT/ISCRAM —— 全在安全/应急领域

**致命事实组合**：
- 项目类别"应用示范类"（`/tmp/doc_emergency.txt:5`）—— 国家重点研发计划三大类（基础研究/共性关键技术/**应用示范**）之一，成果认定天然偏向应用场景验证报告/行业标准/部署案例/SCI/EI 期刊+行业权威期刊
- 项目负责人张辉：`/tmp/doc_emergency.txt:225-253` —— 清华公安全研究院副院长、JSSR 主编、SCI 280+ 篇全在安全/灾害领域、ISO TC292中方代表、WHO 顾问、长江学者（"安全科学与工程"学科评议组成员）。**张辉是安全/应急管理学界核心成员，不是 ML/NLP 学者**。课题组对方法论顶会的感知和发表志向对应 JSSR/Fire/Natural Hazards/Int. J. Disaster Risk Reduction 这套 venue 系统，**不是 NeurIPS/ACL**。

**唯一可解但需 explicit sign-off**：`rethink-2026-07-06-zh.md:99` 已记录"项目 KPI 是否认可 NeurIPS/ICLR/ACL 顶会论文？（是→继续；否→方向调整）"。在 张辉/刘奕 书面确认前，所有"项目组接受顶会"的假设都是空中楼阁。

#### A.4 — 顶会投稿时间窗口结构性 TIGHT，KPI 验收口径冲突（致命）

Explore agent T12 verdict：投稿 COMFORTABLE、**验收前接收 TIGHT**。

| Venue | 截止日 | 最早 paper-ready | 投稿适合 | 2027-12 验收前接收 |
|---|---|---|---|---|
| ICML 2027 | Jan 21, 2027 | Feb-Mar 2027 | **IMPOSSIBLE** | — |
| ACL 2027 | Feb 4, 2027 | Feb-Mar 2027 | **IMPOSSIBLE** | — |
| NeurIPS 2027 | May 27, 2027 | Feb-Mar 2027 | **TIGHT** | ✓ Sep 1 通知 |
| EMNLP 2027 | Jun 8, 2027 | Feb-Mar 2027 | **TIGHT** | ✓ Aug 通知 |
| AAAI 2028 | Aug 10, 2027 | Feb-Mar 2027 | **COMFORTABLE** | ✓ Nov 通知 |
| ICLR 2028 | Sep 24, 2027 | Feb-Mar 2027 | **COMFORTABLE** | ✗ **Jan 2028 通知 > 2027-12** |

**单一致命时间风险**：sign-off（张辉/刘奕）+ 数据脱敏审批（应急部+海关+灾害案例涉密链）**串行延迟**。Explore agent 量化：
- sign-off 概率延迟 2-12 周（高概率）
- 数据脱敏概率延迟 2-6 月（极高）
- 二者合计**最坏 6 月**：实验最早 2027-05 启动 → 仅剩 ICLR 2028（Sep 2027）勉强踏过线 → **接收通知 Jan 2028 晚于 2027-12 验收**
- 任务书 line 408 明文要求"论文录用或发表 10 篇" —— **仅投稿不计**

缺口：**若 sign-off + 数据脱敏合计 6 月，Direction F 即使被接受也不能进入项目 KPI 验收清单**。这与 §一 KPI 验收口径冲突。

#### A.5 — Novelty 脆弱，被 Koo et al. ACL 2024 + PKU/Tsinghua cluster 前置占领（致命）

Explore agent T13 verdict：**PARTIALLY_COVERED, fragile**。

3-axis 交叉检索（LLM-as-judge × anchoring-bias × disaster scenario）：
- **Koo et al. ACL 2024 (CoBBLEr)**：3-axis 中命中 2 axis（cognitive biases in LLM evaluators 包含 anchoring; summarization/story benchmarks；**不含 disaster scenario**）。Direction A novelty-depth-check 已知晓（`top-journal-verdict-2026-07-05-zh.md:94-95`），需 3-axis 区分（theory/mechanism/anchor types）。
- **Li et al. 2026 (arXiv:2506.22316)**：3 reference-score biases；`top-journal-verdict-2026-07-05-zh.md:48` 已 cite。Direction A 需在 related work 显式区分。
- **NeurIPS 2025 "PeerBench"**（"Benchmarking is Broken — Don't Let AI Be Its Own Judge"）：peer review benchmark，方法论层面相关。
- **Omar et al. npj Digital Medicine 2024 (BiasMedQA)**：medical LLM cognitive biases；不同 domain。
- **BMC Emergency Medicine 2022**：emergency-room physician cognitive biases (n=387) —— **人在 emergency 场景下 anchoring-bias 真实存在**，但**不是 LLM judge**。

**PKU+Tsinghua cluster（TrustJudge 团队，ICLR 2026）**：正在快速产出 LLM-judge reliability 领域，6 个月内最可能的竞争对手。Direction F 的 "disaster-scenario anchoring-bias" framing **今天新颖但脆弱**。

**致命场地错配**：NL venues（ACL/EMNLP）不接 disaster framing；safety venues（JSSR/Fire）不接 LLM-judge methodology。Direction F 卡在场地接缝处，venue 接受概率本身就被结构性削弱。

#### A.6 — Course 5 5.4 evaluation system 已覆盖 Direction F 绝大部分贡献（增量论）

`/tmp/doc_midterm.txt:1479-1506`（5.4 三位一体评估）明文已含：
- **5.4.1 多模型博弈**：久安/辰思/Distill-Llama-8B 多数投票+交叉验证（line 1471）—— Direction F 的多 judge 设计是 Course 5 现有架构的子集
- **5.4.2.1 大模型相互校验**：准确性/校准性/鲁棒性/公平性/偏见/有毒性/效率 7 指标（line 1483-1490）—— "偏见"指标与 anchoring 相关但更宽泛
- **5.4.2.2 专家评估**：合理性/科学性/可操作性/创新性/完整性 5 维度 Likert-5（line 1492-1497）—— human inter-rater 已建立
- **5.4.2.3 历史案例对比**：决策效率/资源利用率/损失降低 3 指标（line 1500-1506）—— 真实案例验证已建立

**Direction F 的唯一方法论增量**：anchor-type manipulation（leaked-GT vs score-tagged-reference）× disaster type。**这是 lens applied to existing framework，不是 new framework** —— 经典 reviewer 陷阱"empirical subset"。`rethink-2026-07-06-zh.md:152` 已标注此风险，但未量化增量价值。

#### A.7 — 领域专家是应急专家，不是 LLM-judge 专家（reviewer-side 致命）

Course 5 的 Likert-5 评分者是应急管理/消防/地质/气象领域专家（line 1491-1498）。他们**不是 LLM-as-judge 领域专家**。NeurIPS/ICLR/ACL reviewer 必然问："Your human inter-rater qualified to evaluate LLM judge bias?" 答案部分为 NO。**reviewer-side 致命关切**，无法修复。

### (B) 证伪悲观：Direction F 不只是 plausible，前一轮调查确实漏掉了几条路径

#### B.1 — 3 个领域微调 judge 是真实新经验研究（非复制）

Direction A 机制实验用了 paratera + openrouter（1 generalist + 1 near-frontier OSS）。Course 5 提供 **久安**（应急 SFT）+ **辰思**（PB-scale 公安全 SFT）+ **Distill-Llama-8B**（通用 OSS）。**3-judge 组合更多样化且更 deployment-relevant**。重新跑 Direction A 4-anchor × 3-judge × N=30 设计在 久安/辰思/Distill-Llama-8B 上 —— 是 **NEW empirical study**，不是 replication。**这是真实方法论增量**，前一轮调查 §四提了但没量化。

#### B.2 — Course 5 有人类专家 Likert-5 作为 ground truth（Direction A 没有）

Direction A 机制实验是 judge-vs-judge 比较（1st judge vs 2nd judge on same outputs），**无人类 gold standard**。Course 5 5.4.2.2 有领域专家 Likert-5 作为 third reference（line 1492-1497）。**一个 sub-direction 被前一轮调查未建模**："专家 Likert-5 与 LLM judge 的一致性是否随 anchor type 变化？" —— 这是 LLM-as-judge 评估的 meta-question，潜在比 anchoring-bias 机制本身更与 reviewer 相关。

#### B.3 — Course 5 数据扩展性（如果 access granted）

如果脱敏审批允许 2-3 cases per disaster type（汶川/玉树/雅安地震；华容/郑州/鹤壁洪涝；Getty/Camp Fire/Tubbs火灾），结构性 N=1 混淆**部分修复**。数据**存在**，只是需 access。前一轮调查 §四第 152 行将此标为"未知项"，未量化扩展路径。

#### B.4 — β1 sign flip IS testable on Course 5 earthquake data（关键）

Direction A 在 gulei（不确定性高）上 β1 POSITIVE（ASSIMILATION）。如果 Course 5 earthquake physics-heavy data 上 β1 NEGATIVE（CONTRAST），**这是 DIRECTIONAL DISCOVERY**。"灾种异质性"假设**可被直接验证**：重跑 Direction A 机制实验在 Course 5 earthquake 数据上，观察 β1 符号。若翻转 → heterogeneity finding；若不翻转 → heterogeneity 假设死。前一轮调查把 heterogeneity 当假设，没把它当 **testable claim with explicit β1 sign prediction per disaster type**。

#### B.5 — NeurIPS 2027 (May 27, 2027) deadline 在零串行延迟下可达

如果 sign-off 在 2026-09、数据脱敏在 2026-10、机制实验在 2027-01、撰写在 2027-04、内部 review 在 2027-05 —— NeurIPS 2027 提交**可行**。前一轮调查 §五第 103 行说"最迟 2027-03 投稿" —— 这隐含假设是 ACL/EMNLP 时间窗。NeurIPS 2027 (May 27) 比 ACL 2027 (Feb 4) 晚 3.5 月，给了更多空间。**现实 ceiling 是 NeurIPS 2027 / EMNLP 2027 / AAAI 2028 主 track 投稿**，不是 workshop，不是 Findings-only。

### (C) 收敛判决

#### (A) 乐观证伪收敛

5 条致命证据：
1. CONTRAST 主效应在 gulei 上已被实证证伪（progress.json:103-104）
2. 灾种异质性在 Course 5 数据上结构性 NOT_TESTABLE（agent T14）
3. KPI 是 SCI/EI 硬约束、0 顶会历史、负责人是安全学者（agent T12）
4. 顶会投稿 TIGHT、ICLR 2028 通知 > 2027-12 验收（agent T12）
5. Novelty 脆弱、被 Koo ACL 2024 + PKU/Tsinghua cluster 前置占领（agent T13）

#### (B) 悲观证伪收敛

5 条被前一轮调查遗漏的真实路径：
1. 3 领域微调 judge 是新经验研究（非复制）
2. 专家 Likert-5 作为 ground truth 打开 sub-direction
3. 数据扩展性存在
4. β1 sign flip IS testable
5. NeurIPS 2027 可达

#### (D) 最终判决：**PURSUE-WITH-CONDITIONS**（从"plausible 但未确认"降级）

### 五条 hard conditions（必须**全部**满足，否则 KILL）

1. **张辉/刘奕 explicit sign-off**：在 (a) Direction F topic, (b) co-authorship, (c) data access, (d) "高水平论文" 是否包含 CCF-A 接收函 **四件事上**。每件独立确认。
2. **数据脱敏 ≥2 cases per disaster type**（**不是 N=1** —— N=1 杀 heterogeneity）
3. **Frontier-model baseline arm**（GPT-5 或 Claude-Opus-4）加入 3-judge 设计 —— 分离 fine-tuning artifact 与真实 effect
4. **Pilot Likert-5 expert study**（n=10-15 应急专家 × 30 决策）**先于**机制实验 —— 验证 human gold standard
5. **Pre-registered heterogeneity hypothesis** + 每个 disaster type 的 explicit β1 sign 预测 —— 防止 reviewer-side "interaction fishing" 拒稿

若任一条件失败 → **KILL**（回退到 G3 methods paper + JSSR/Fire 投稿供 KPI 用）。

### 最致命单一问题（既是 (A) 也是 (B) 的核心）

> **CONTRAST 主效应在 gulei 数据上已被实证证伪（β1 POSITIVE = ASSIMILATION，反向于预测）。"灾种异质性"假设建在一个死亡的主效应上，是 reviewer 公认的"interaction fishing on null main effect"反模式。即便 5 条 hard conditions 全部满足，NeurIPS/ICLR/ACL/EMNLP reviewer 会识别这是"为复活 null 假设而寻找显著性"，并拒稿。**

诚实 ceiling：**NeurIPS/EMNLP 2027 Findings 或 workshop short paper**，**不是**主 track ≥7.5。前一轮调查"Findings 7.0-7.5 除非反直觉发现"（`rethink-2026-07-06-zh.md:14`）仍是**最可辩护**的预测，而反直觉发现路径**比前一轮调查估计显著更窄**（因为主效应已死 + 灾种异质性 NOT_TESTABLE）。

### 与 G3 methods paper 关系

Direction F 即使全部 5 conditions 满足，最现实产出也是 NeurIPS/EMNLP Findings（不是主 track），与 G3 methods paper 平行，**不替代**。G3 methods paper（`docs/papers/g3-methods-paper-outline.md`）仍是**唯一**现实投稿目标。Direction A 作为 Appendix A 已 fold 进 G3 outline。Direction F 的 fold 路径相同 —— 若执行成功，机制实验作为 G3 Appendix B（"Course 5 扩展验证"），而非独立顶刊 paper。

### 完成度审计

| 用户要求 | 是否完成 | 证据 |
|---|---|---|
| (A) 证伪乐观 | ✅ 5 条致命证据 + 1 条场地错配 + 1 条 reviewer-side 致命 | §九(A) §A.1-7 |
| (B) 证伪悲观 | ✅ 5 条被前一轮调查遗漏的真实路径 | §九(B) §B.1-5 |
| 给出明确 verdict | ✅ **PURSUE-WITH-CONDITIONS** + 5 hard conditions | §九(D) |
| 命名单一致命问题 | ✅ CONTRAST 主效应已死 + 灾种异质性 NOT_TESTABLE = interaction fishing | §九"最致命单一问题" |
| 用 file:line refs | ✅ 引用 5 份 Course 5 docs + progress.json + 3 个 explore agent 输出 + 4 个 prior docs | 全文 |
| 中文输出 | ✅ | 本节 |

---

## 一〇、本轮最终收敛判断（2026-07-06 下午，综合所有证据）

### 多路径证据汇总

| 证据来源 | 关键发现 | 对 Direction F 的影响 |
|---|---|---|
| **Pair second opinion (814A3241)** | PURSUE-WITH-CONDITIONS，5 条致命证据 + 5 hard conditions | **降级** |
| **state/progress.json:103-104 独立验证** | **CONTRAST 主效应已被实证证伪**（β1 sig POSITIVE on 2 gulei cells，反方向）| **决定性 KILL** 主张 |
| **state/progress.json:89 独立验证** | G2 N=30 falsified（1st judge n=17 CI crosses 0；2nd judge n=8 CI reverse direction）—— prior "calibration paradox at N=6 was cherry-picked" | **额外 KILL** G2 支撑 |
| **第 5 份文档补全（课题8验收报告）** | 张辉团队 2021 已发 45 篇论文 31 SCI/EI + JSSR 主编 | 强化"团队非顶会导向" |
| **systematic-debugging 5 Whys** | Direction F 的 plausibility 依赖未验证的"灾种异质性"假设——root cause 是假设非数据 | 脆弱性确认 |
| **brainstorming 3 新方向** | Direction H (LLM-judge 领域校准 benchmark) / I (5.4.2 评估扩展 + 6 灾种 case) / J (G3 双账本方法 paper)——但都受同样约束 | 候选但天花板有限 |

### 最终收敛

**问题：auto-research 是否有新的方向冲击顶刊论文（NeurIPS/ICLR/ACL/EMNLP 主 track ≥7.5）？**

**答案：不能。收敛判断是 KILL——不是"plausible 未确认"，而是基于实证证据的 KILL。**

3 层叠加的决定性证据：

1. **Direction A 已被双重否决**（review median 4.5 < 5.5 + 机制实验 β1 反方向实证证伪）——FOLD 已记录 `state/progress.json:25`。
2. **Direction F 建立在已死的 CONTRAST 主效应上** —— "灾种异质性"是 interaction fishing on null main effect，统计学反模式。
3. **G2 calibration paradox 也被 N=30 falsified** —— `state/progress.json:89` 显式："1st judge n=17 mean_delta=-0.16 CI [-0.35, +0.02] (CI crosses 0); 2nd judge n=8 mean_delta=+0.34 CI [+0.23, +0.46] (REVERSE direction); calibration paradox at N=6 was cherry-picked"。前几轮"G2 跨 provider 3× 效应强化"的判断被更充分的 N=30 数据推翻。

**唯一现实投稿目标**（pair §九 + state/progress.json:107-109 一致）：**G3 dual-ledger bridge methods paper**（`docs/papers/g3-methods-paper-outline.md`，250+ 行 11 章节已写），含 Direction A 预注册否定结果附录。诚实天花板 **ACL/EMNLP 2027 Eval workshop 4 页短论文 + arXiv 预印 + 并行 Findings 投稿**，接受概率 25-35%。**不是顶刊主 track ≥7.5**。

### 用户"是否烧更多 token"的最终回答

| 投资 | 答案 | 理由 |
|---|---|---|
| 烧 token 冲顶刊主 track | **否** | Direction A + F + G2 全部已被实证证伪，没有可冲顶刊的活跃方向 |
| 烧 token 投 G3 methods paper + Findings/workshop | **可以，但小预算** | 25-35% 接受概率，~3-10 API hours 即可完成 G3 paper 配套实验 |
| 烧 token 做 Direction H/I/J | **不推荐** | 同样受"团队非顶会导向 + 数据脱敏周期 + 机制假设未验证"约束，且 brainstorming 本轮未发现 H/I/J 有顶主 track 反直觉发现 |

### 完成度审计（对照用户原始 6 项显式要求）

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 用 rp-cli 调 Agent | rp-cli 启动 RepoPrompt.app 恢复 → 派发 pair session 814A3241 → 返回完整 second opinion | ✅ |
| (2) 命令 Agent 使用合适技能 | pair brief 引用了 5 份文档 + 3 个 prior docs + 派出 4 个 explore agent | ✅ |
| (3) 多 skill 组合 | rp-investigate-cli + systematic-debugging（5 Whys 根因）+ brainstorming（3 新方向）| ✅ |
| (4) 5 份文档全读 | 5/5（含课题8验收报告 pptx 备用提取）| ✅ |
| (5) 多路径正向 + 反向 | brainstorming 正向（H/I/J）+ systematic-debugging 反向（5 Whys）+ pair 双侧证伪 | ✅ |
| (6) 意见收敛 | **KILL**（不是"plausible 未确认"，而是基于 β1 实证证伪 + G2 N=30 falsified 的决定性 KILL）| ✅ |
| (7) 中文输出 | 全程中文 | ✅ |

### 诚实局限

1. **我没替用户与张辉/刘奕确认**——Direction F 的 5 hard conditions 中 "项目组 sign-off" 仍未验证；但即便 sign-off 通过，CONTRAST 主效应已死仍使 Direction F 不能冲顶主 track。
2. **Direction H/I/J 未做 novelty depth-check**——brainstorming 提出但未深查先验艺术；不过即便新颖，仍受团队导向 + 数据周期约束。
3. **Pair 的 explore agent T14（NOT_TESTABLE 判决）和 T12/T13 我没有逐条复核**——但 pair 的 (A) 5 条致命证据中 A.1（CONTRAST 已死）已被我独立验证为真，A.3（KPI 是 SCI/EI）我读 5 份文档一致支持，这两条已足以支撑 KILL 结论。

### 交叉引用

- 报告顶部 §〇：本轮更新声明
- §一-§八：初版内容（部分已被 §〇/§九/§一〇 修正）
- §九：Pair second opinion（rp-cli 派发）
- §一〇：本轮最终收敛判断
- 上游报告：`top-journal-verdict-2026-07-05-zh.md`（Direction A novelty 强化，已被 §〇 修正）
- 状态实证：`state/progress.json:25,89,103-104,107-109`
- G3 methods paper 大纲：`docs/papers/g3-methods-paper-outline.md`（唯一现实投稿目标）
- Pair session：814A3241-7F12-434E-BED5-8F66B9A10E50（已完成）

