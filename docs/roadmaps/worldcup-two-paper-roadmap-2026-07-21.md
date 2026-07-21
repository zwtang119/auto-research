# 双篇路线图：世界杯预测审计（上）+ LLM 群体 scaling 前瞻验证（下）

> 日期：2026-07-21
> 版本：v1.3（2026-07-22，按文献扫描 + 系统工程审查两段式重构 Paper B 主干；版本记录见 §9）
> 状态：用户已裁定同意双篇拆分（2026-07-21 会话），本文件为执行路线图
> 上游文档：
> - 开题 v2：`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`（Paper A 的开题底座）
> - 方向评估：`docs/investigations/kimi-reasoning-attribution-assessment-2026-07-21.md`（kimi 推演归因方向拒收裁定 + M1–M5 改造方案）
> - 参照范式解剖：`analysis/kimi-reasoning-assessment/reference-paper-anatomy.md`（Scaling Agent Systems 范式门槛）
> - 文献底座：`analysis/worldcup-proposal-review/stage2-data-summary.md` + `stage2-literature-table.csv`（37 篇 verified）
> - 文献扫描：`analysis/roadmap-v12-scan/refscan.md`（AMW 充分统计量两段式框架与选择性自动化发现）
> - 系统工程审查：`analysis/roadmap-v12-scan/se-review.md`（36 格 power 缺口、B0 规格缺席、pilot/闸门/监控、成本账）

## 1. 决策链（本路线图是怎么来的）

1. 2026-07-19 W6 终裁（`docs/investigations/worldcup-paper-topic-2026-07-19.md`）：主线 = 审计型数据集 + proper-score 反转 + 协议失败标签。
2. 2026-07-21 开题 v2 重构完成：主线定形为 audit-chain-anchored multi-forecaster reconciliation protocol，H1–H5 + PIV，kimi 技能问题**显式留待续篇**（v2 §3 H4-ii）。
3. 2026-07-21 "kimi 推演补全 + 逐条归因为什么对"方向评估：裁定**拒收归档原形态**（Nature 5 判据 0 PASS、7-check 0/7），理由 = ex-post 重建无真值、训练数据/结果污染不可排除、n=1 无统计力。
4. 2026-07-21 用户提出重构："把 kimi 当作假设来源而非证据，前瞻验证 300 分身路径是否有效"——评估确认这是把死路走活的关键转向。
5. 2026-07-21 用户裁定：拆为两篇。上半篇 = 本届世界杯封存预测审计；下半篇 = LLM 群体路径的前瞻 scaling 验证。
6. 2026-07-21 双篇顶刊差距评估（`docs/investigations/two-paper-roadmap-nature-gap-assessment-2026-07-21.md`）：Paper A 7-check 7/7、Paper B 无 FAIL，但发现 Paper B 两大隐藏拒稿点——factorial 统计力缺口约一个数量级（n=350 锚点适用范围被静默扩大）+ M5 信息集消融未落实；用户裁定按 R-B1–R-B6 改进路线图（本版 v1.1）。
7. 2026-07-22 文献扫描（`analysis/roadmap-v12-scan/refscan.md`）+ 系统工程审查（`analysis/roadmap-v12-scan/se-review.md`）并行复核 v1.1：文献端发现 AMW 充分统计量两段式框架与"选择性自动化 + 完全披露、协作辅助增量可忽略"结论；工程端发现 36 格 power 缺口未对账、B0 四件交付物无规格、无 pilot/闸门/监控、成本账缺失。编排器裁定"优化即可，不重构"：Paper B 主干改为 AMW 两段式，确认性旋钮砍至规模 × 信息集（本版 v1.3，原定版本号 v1.2 因 §9 已存在同名边注条目而顺延）。

## 2. 两篇的分工与咬合

| | Paper A（上半篇） | Paper B（下半篇） |
|---|---|---|
| 一句话 | 五份赛前封存预测在同一审计链下的对照阅卷 | kimi 提示的 LLM 群体路径是否真有效：前瞻受控实验 |
| 方法属性 | 事后审计（retrospective audit） | 前瞻实验（prospective experiment） |
| 核心问题 | 怎么阅卷才可信（协议 + 结构差异） | 什么信息结构导致 herding vs 独立判断 |
| 时间 | 现在即可写（数据已冻结） | 需数月积累（Stage 1 估 V(x) 中等量 + Stage 2 按 MDE 定量，§4.3） |
| 角色 | **出题 + 预注册载体** | **答题** |
| venue 定位 | evaluation 类 workshop / 期刊（现实首选） | 扎实后可冲主会；顶刊需跨任务通用性证据 |

**咬合机制**：Paper A 在公开发表的文本中白纸黑字写下"kimi 群体信号是否含独立信息 = 待检验悬念"（v2 §3 H4-ii 已有此句）。Paper B 以此作为**实验前已公开的假设**，预注册最难的一环由 Paper A 顺手完成——做实验之前就有的猜想，不是看完结果编的。

## 3. Paper A（上半篇）：世界杯五预测者审计

### 3.1 定位

即 v2 开题主线的执行。研究对象不是"谁猜对了冠军"，而是**评估协议本身**：五类预测者（Elo+Poisson P1 / Coach P2 / CDS P3 / kimi 群体 P4 / 市场 P5）在同一审计链下的概率结构差异 + 协议完整性向量（PIV）标注。

> [!memo] 2026-07-22
> "不确定性结构是第一类输出"为 Paper A 的设计哲学提供直接支撑：MCDP-1 明言信息收集虽能减少未知数，却"不可能消除它们，甚至无法接近消除"（p.11；调查文档映射 #4）。因此 PIV 不应被写成审计附属标签，而应与概率结构差异并列为审计结果：协议的可追溯性、缺失与污染边界本身就是对不确定性结构的报告。这与 v2 §3 H4-ii 公开悬念句同向，强化"评估协议本身"而非"谁的数字更大"的写作纪律；属"受条令启发的设计类比"（引用纪律要求明示）。
>
> 来源：MCDP-1, p.11；`cds4polymarket/docs/investigations/uncertainty-decision-methodology-2026-07-21.md` §5.1 #4、`## 引用纪律`。
> 上下文：Paper A §3.1 "评估协议本身"，防止 Paper A 把赛后命中压缩成单一胜者排名。

### 3.2 措辞纪律（红线，违反即返工）

- **禁**："kimi 猜得最准"、"猜冠军的经验"、"前五中四"胜利叙事、"首个/独占"句式（W6 §8 禁用清单 + v2 §7.0 合规对照）。
- **原因**：本届为史上首次 FIFA 前四全部进四强（2026-07-20 Wikipedia Green Source 核验），"前五中四"与"随大流碰上"不可区分——"最准"在 Paper A 的数据里**证明不了**，只能定性为"最值得检验的悬念"。
- **宜**："kimi 信号在冠军层的表现无法与基准率区分，但其群体结构留下一个待检验的疑问（→ 续篇）"。

### 3.3 当前状态与剩余工作

- 开题：v2 已完成（2026-07-21）。
- 执行计划：`docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md`（W1–W8 + G0/G1/G2 闸门）。
- 已知瑕疵处置：v2 §5.2 R1–R5 已登记；证据快照缺口按 `docs/investigations/evidence-snapshot-gap-analysis-2026-07-20.md` 的建议补入。
- 指标：主指标 RPS + Brier Murphy/Yates 分解 + reliability diagram；逐场层（n=72/71）做统计检验，队伍层（n=1）仅描述。

## 4. Paper B（下半篇）：LLM 群体路径的前瞻 scaling 验证

### 4.1 研究问题

**不问**"kimi 当时为什么对"（不可证伪，已拒收）；**改问**：

> 在 LLM 群体预测中，何种结构（群体规模 × 人设多样性 × 聚合规则 × 信息集）导致 herding（趋同跟风），何种结构保住独立判断？

kimi 的 300 分身配置仅作为**假设来源（hypothesis-generating anecdote）**出现，全文措辞纪律：永远"一个有悬念的配置提示了这个方向"，永远不说"kimi 证明了 300 分身有效"。

**herding 的操作化定义**（预注册前必须锁定，缺它则标题构念不可测量）：双层指标，全部可从 trace 自动计算——
1. **群体内部一致性**：同任务内分身输出的方差分解 / token-overlap（参照范式指标族）；
2. **群体-市场一致性**：群体输出相对市场共识的偏差方向统计 + 信息增益 ΔI（接 v2 H4 框架）；
3. 判定阈值随 OSF 预注册冻结。群体与市场一致既可能是 herding（复述共识）也可能是"独立得出同一正确答案"——只有 §4.2 的信息集消融臂能把两者分开。
4. **机制注记**（v1.3）：AMW 与 Dunning 独立互证——人对 AI 预测的 under-response 几乎完全源于**对自身信号精度的过度自信**（own-signal overconfidence），而非对 AI 的不信任。对 Paper B 的含义：herding 的对立面（独立判断）可能同样由"分身对自身 persona 信号的过度加权"维持，herding 由此从"输出相似度"问题深化为**信念更新权重**问题；该机制列为 Stage 2 的候选机制假设（跨域借用 human reliance → agent herding，引用时须声明，见 §10 AMW/Dunning 条目）。

### 4.2 实验设计：AMW 充分统计量两段式主干 + 旋钮分级（v1.3 重构）

**两段式主干**（AMW 框架跨域借用，human-AI 协作 → LLM 群体，引用时须声明；v1.1 的"方案 A 扩量 / 方案 B 砍假设"二选一被两段式吸收而取消）：

- **Stage 1（描述性，moderate n）**：在开发任务流上估计充分统计量 **V(x) = 群体正确率对市场隐含概率 x 的响应曲线**（从 trace + 结算数据非参数估计；参照 AMW 第一阶段"先估 V"模式，V 的凸性/形状用于推导最优披露与聚合策略）。
- **Stage 2（确认性，集中 power）**：在 V(x) 基础上推导并验证**最优聚合/披露策略**（参照 AMW 第二阶段"按冻结策略实测验证"，其预测与实测差 <1.6pp）。确认性假设集中到 Stage 2 的 **1–2 个预注册主效应 + 显式 MDE 声明**（如"本实验可识别 α*≥0.05 的效应"），其余全部为探索性分析、不做确认性断言——v1.1 方案 B 的精神由"备选"扶正为默认设计。
- 充分统计量假设（V 不依赖披露策略）需在 LLM 群体上先检验，AMW Assumption 2.1/2.2 的检验方法可借用；V(x) 低 x 区间（冷门事件）样本稀疏须如实披露。
- v1.1 的"两阶段 adaptive design 写入预注册"要求由两段式主干吸收：Stage 1 = 估计、Stage 2 = 确认，两段规则均写入 OSF 预注册，不再另设筛选规则层。

**旋钮分级**（v1.3：确认性旋钮砍至 2 个，36 格全确认性 factorial 取消——SE review 判定人设、聚合为二阶问题，拿 4 倍样本量换非核心结论属过度设计）：

| 级别 | 旋钮 | 水平 | 检验什么 |
|---|---|---|---|
| 确认性 | 群体规模 | 3 / 10 / 30（对数间隔） | 规模收益曲线形态；是否存在过规模负收益（参照范式：single-agent 超 ~45% 后加 agent 呈负收益） |
| 确认性 | **信息集**（M5 落实，v1.1 第四旋钮地位提升） | 含市场快照 / 不含市场快照 | herding 的因果识别：操纵 agent 能否看到市场信息，是区分"跟风复述"与"独立同答"的唯一干净手段 |
| 探索性 | 人设多样性 | 同构 / 派别差异化 | persona 差异化是否产生实质性信息异质（接 v2 H4-ii 开放问题）；Stage 2 候选机制（信念更新权重，§4.1 机制注记）的探索载体 |
| 探索性 | 聚合规则 | 多数投票 / 加权 / 辩论收敛 / **选择性路由（selective routing）** | AMW 发现最优策略为"选择性自动化 + 完全披露"、协作辅助相对其增量**可忽略**——增设选择性路由臂（按置信度把任务路由给最优子群体，其余直接采纳），检验该发现在预测任务上是否成立（跨域借用须声明）；AMW"完全披露不劣于部分披露"提示信息集臂可加"完整快照 vs 加噪/延迟快照"子水平 |

- 规模水平说明（v1.3）：**300 分身降为可选探索探针**——300 是 kimi 轶事值而非机制需要，曲线形态用对数间隔小水平即可识别拐点与负收益区，300 臂成本约为 3 臂的 100 倍却只贡献曲线末端一个点（成本约束见 §4.7）；写作中明示"本实验检验的是曲线形态而非复刻 300 这一点"（与 §6 第 6 条认识论绝缘裁定一致，呼应 kimi 叙事只剩修辞价值）。

> [!memo] 2026-07-22
> Paper B 的"规模 × 人设多样性 × 聚合规则 × 信息集"不应被读成"agent 越多越好"。MCDP-1 直接反对完全中心化（p.16；调查文档映射 #7），并把 Mission Tactics 表述为"给任务而不规定完成路径、事后回报"（p.68–69；映射 #8）——这是受条令启发的设计类比，不是原文对 LLM 的结论。其含义：把规模收益与独立判断是否被聚合抹平分开检验；同构/异构对照、聚合规则消融因此有更清晰的设计哲学依据。
>
> 来源：MCDP-1, p.16、p.68–69；`cds4polymarket/docs/investigations/uncertainty-decision-methodology-2026-07-21.md` §5.1 #7、§5.2 #8、`## 引用纪律`。
> 上下文：Paper B §4.2 "三个旋钮"（v1.1 增为四旋钮），特别用于约束"300 分身有效"类事后叙事与"协调结构消融"的占位对照论证。

- 底座：**≥2 个模型家族，其一为版本固定的开源模型**（服务可复现性与规模对照；放弃 kimi 本体——底座版本不可考是结构性缺口）。
- 冻结协议：prompt hash 全冻结 + **OSF 时间戳预注册 + git hash 链每日落盘**（commit-reveal 降级：该机制解决多方竞技场中参赛者事后改答案的对抗性问题，Paper B 单团队无对手方，原设计过度——git 不可变历史 + OSF 时间戳已是学界标准答案）+ **真实 trace 当场全量记录**。
- 任务流与结算来源（地基选择，启动前必须裁定并记录权衡）：
  - (i) 自建题目 + 人工结算——须配多人裁决或自动结算准确率声明（Bosse 式 ~95%，[arXiv:2601.22444]）；
  - (ii) 真实市场（Polymarket 等）——结算 trustless，但赔率公开：agent 可检索则独立判断被结构性污染，故**必须配信息访问控制臂**（与信息集旋钮联动）或禁检索 + 生态效度论证；
  - (iii) 体育赛事——结算干净但频率低，休赛期有断供风险，需与 (i)/(ii) 混合供题。
- 差异化论证（related work 三段式，写作时必须有）：Paper B 是受控 factorial 实验，与 Prophet Arena / ForecastBench / Foresight Arena（能力排行榜，贡献类型不同）差异化真实存在；真正的占位对照是 **Scaling Agent Systems（协调结构消融）与 InfoDelphi（信息对称性消融）**——必须回答"在信息对称性维度与协调结构维度之外，规模 × 人设 × 聚合 × 信息集的增量是什么"。

### 4.3 样本量与统计（v1.3：两段式集中 power，方案 A/B fork 取消）

**锚点溯源**：Foresight Arena [arXiv:2605.00420] 原文（2026-07-21 直接复核摘要页）："detecting a true edge of α* = 0.02 at 80% power requires approximately 350 resolved binary predictions"。该数字属实，但适用边界有三：二元任务、两 agent 单一比较、"50 rounds × 7 markets" 存在时间聚簇（独立有效样本 < 350）。v1.1 曾把它摊到 18 格 factorial（每格 ~19），SE review 进一步指出第四旋钮加入后实为 36 格、缺口约 20 倍且未对账——v1.3 以两段式消解：取消全确认性 factorial，确认性 power 集中于 Stage 2（§4.2），36 格对账问题不再存在。

**两段式 power 账**（启动 B1 前写入 OSF 预注册）：

- **Stage 1（V(x) 估计，描述性）**：目标是曲线形态而非单点显著；n 按曲线分箱精度定（moderate n），预注册中写明分箱规则与每箱样本下限；要求跨 x 全谱覆盖，低 x 区间（冷门事件）样本稀疏如实披露。
- **Stage 2（策略验证，确认性）**：1–2 个预注册主效应，样本量按**显式 MDE 声明**反推（锚点：α*=0.02、80% power ≈ 350 已结算二元预测/比较；任务流时间聚簇按设计效应折算有效样本量，mixed-effects 之外 power 估算须用聚簇调整后口径）；评估集自身须满足 MDE 要求，否则期末考在设计上注定不显著。
- 任务口径：若用体育 W/D/L 三元任务（RPS），须重做 power analysis 或改用二元市场任务对齐锚点。
- 分析：混合效应模型 + bootstrap + 交叉验证 + 全套模型设定诊断（残差 / VIF / 正则化对照，对齐 Scaling Agent Systems 范式）；负结果必报；除均值外报告跨条件方差（"平均最优 ≠ 鲁棒最优"，换模型家族/任务流后不稳健的配置如实标注）。
- 逐场层做推断，赛事级单点仅描述（不重复 n=1 的错误）。

### 4.4 归因操作化（M4 纪律）

- 预注册归因 taxonomy（事先定义"推理对/错"的操作标准，不看完结果再定）；
- 对称编码：命中与未命中**同样编码**（只看成功案例是 confirmation bias 温床）；
- 双人盲标，Cohen's κ ≥ 0.80；纯人工逐条归因无预注册/盲标/一致性 = 弱证据，降格为 illustrative；
- 自动指标层优先：§4.1 的 herding 双层指标从 trace 自动计算，人工编码仅作补充，结论权重放在可自动复核的定量指标上（对齐参照范式做法）。

### 4.5 期末考规则（防迭代过拟合，v1.1 补齐规格）

- 迭代期：可在开发任务流上自由调试；
- **评估集划分规则**：随机分层抽样（非时间块——避免赛事日历引入的域偏移与"过拟合"解释混杂）；评估集规模与开发/评估各自的 power 分配写入预注册（评估集自身须满足 Stage 2 的 MDE 要求，否则期末考在设计上注定不显著）；
- **方法冻结粒度清单**（预注册中列明）：prompt / persona 规则 / 聚合权重在 B2 起点冻结；确认性旋钮水平（规模 3/10/30 × 信息集）随 Stage 2 预注册冻结，探索性臂的调整如实记录；
- 时间外验证如实报告（参照范式 GPT-5.2 外推验证：过就过，不过就写不过）。

### 4.6 时间线（粗估，v1.3 插入 B0.5 pilot 闸门）

| 阶段 | 内容 | 量级 |
|---|---|---|
| B0 | 群体底座搭建（≥2 模型家族）+ 冻结协议 + trace 记录管线 + 任务流/结算来源裁定。**出口 = 四件规格化交付物**（每件一页内写完，缺一件不得放行 B0.5）：(i) trace schema 字段清单（task_id / agent_id / model_family / 模型版本指纹 / prompt hash / persona 配置 / 原始输出 / 解析后概率 / 时间戳 / 结算状态）+ 完整性校验规则；(ii) 冻结验证 SOP（谁、何时、如何重算 hash 比对、日志留存格式）；(iii) 任务流调度规则（选题频率、去重、同日聚簇控制）；(iv) 结算来源裁定记录（(i)/(ii)/(iii) 三路径权衡与截止日期） | 2–4 周 |
| B0.5 | **pilot 小规模试跑**（~数十次预测 × 小规模臂）。go/no-go 判据（全部满足才放行 B1）：trace 完整率 100%；解析成功率 ≥98%；结算时延中位数 ≤72h；成本实测 vs §4.7 估算偏差 ≤50%（超标即先修管线再放量，返工成本被闸门限制在 pilot 量级） | 1–2 周 |
| B1 | 持续预测任务流运行 + 运行期监控（§4.8）：Stage 1 积累 V(x) 估计样本（moderate n，按预注册分箱下限） | 数月（取决于任务频率） |
| B2 | 达量后按冻结粒度清单冻结方法，Stage 2 期末考 + 统计分析 | 2–4 周 |
| B3 | 写作与投稿（含三段式差异化论证） | 4–6 周 |

### 4.7 成本估算（量级与降级规则，v1.3 新增）

- **调用量公式**：API 调用次数 = 已结算预测数 × 分身数 × 模型家族数；辩论收敛臂多轮交互再乘 3–5 倍。
- **量级区间**（按主流 API 定价量级粗估）：Stage 1（moderate n × 规模臂 3/10/30 × ≥2 模型家族）约 10⁴–10⁵ 次调用；Stage 2（按 MDE 定量 × 确认性 2 旋钮）同量级或更低；全篇合计约 10⁴–10⁵ 次调用、10²–10³ 美元区间。B0 内做一页成本模型（单价 × 调用量 × 臂数 × 冗余系数），作为 B0.5 pilot 对账基准。
- **历史背景（已被规避的旧方案）**：v1.1 方案 A（10³–10⁴ 已结算预测 × 300 分身 × ≥2 模型家族）约需 **60 万–600 万次调用**、10³–10⁵ 美元区间（SE review A5 的成本警告）——该风险由两段式 + 旋钮削减 + 300 降探针规避，方案 A 已废止，此处仅留档说明。
- **降级规则**（成本超阈值即触发，逐级执行）：先砍探索性臂（含 300 探针与辩论收敛臂）→ 再缩 Stage 1 分箱精度 → 确认性 Stage 2 的 MDE 声明为最后调整项（调整须回预注册修订并留痕）。

### 4.8 运行期监控（B1 常驻，v1.3 新增）

每次运行落盘四字段：调用数 / 解析成功率 / 模型版本指纹 / 结算状态；周级自动对账。三类静默失败的校验节点与处置规则（与项目既有 fail-loud 纪律同构）：

| 静默失败 | 机理 | 校验与处置 |
|---|---|---|
| 解析漂移 | 分身输出格式漂移 → 概率解析失败被静默丢弃，各臂存活率不等即引入选择偏差 | 解析成功率 <98% 即 fail-loud 停流排查，修复前的数据分段标记 |
| 结算延迟 | 结算延迟 / 市场作废 → 样本悄悄缩水且非随机缺失 | 周级结算状态对账，缺失率超阈值（预注册写明）即停流并记录缺失机制 |
| API 版本变更 | 服务端模型版本变更使"版本固定"承诺悄悄失效（prompt hash 管不住 system 侧） | 模型版本指纹逐次落盘，指纹变更即 fail-loud 停流，变更前后数据在分析中分段标记 |

## 5. 衔接与依赖

- **Paper A → Paper B**：A 的公开文本 = B 的预注册假设来源；B 引用 A 的 H4-ii 悬念与 PIV 标注方法。
- **Paper B 不依赖 Paper A 先发表**：B 的实验可即刻启动（B0 阶段与 A 的写作并行）。
- **共享纪律**：证据三级结构（封存仓库零读写 / 证据快照只读 / 分析副本可写增补 + CHANGELOG）；不输出投注建议、收益率、交易指标；市场数据仅作研究基准；中文为主、ISO 日期。

## 6. 结构性边界（任何迭代都绕不开，如实保留）

1. 2026 世界杯已结束，ex-ante 不可回溯——关于 kimi 本体的故事**到此为止**；
2. kimi 底座模型版本不可考（上游仓库不存在，2026-07-20 核查）；
3. kimi 真实推理 trace 从未被记录，"补全"对象本体论上不存在；
4. kimi 信号 Red Source 定级 + Elo bonus 生成期污染不可剥离；
5. 300 分身快照一次性，同协议复现不存在。

含义：Paper B 是**受轶事启发的新实验**，不是 kimi 研究的续命。两篇都不宣称恢复 kimi 的"正确性"。

**v1.1 新增（顶刊差距评估 2026-07-21 §⑦.3 新发现）**：

6. **Paper B 与 kimi 之间的认识论绝缘是永久的**：换底座意味着 Paper B 的任何结果（阳性或阴性）都不构成对 kimi 当时配置有效性的证据——写作中若出现"kimi 路径被验证"类句式即越界；
7. **双篇咬合的单向脆弱性**：咬合依赖 Paper A 公开文本中的 H4-ii 悬念句；若 A 审稿要求删改该句，B 的"实验前已公开假设"叙事即受损——补救为 B 独立做 OSF 时间戳预注册（届时咬合从"预注册载体"降级为"动机引用"），此风险可管理不可消除。

## 7. 风险与备选

| 风险 | 应对 |
|---|---|
| B1 数据积累过慢 | 降级为 pilot 研究（如实标注样本量上限），或并入 live benchmark 任务流加速结算 |
| 自建群体复现不出 kimi 式信号 | 负结果如实报告（herding 判定本身即贡献，接 InfoDelphi 框架） |
| Paper A 评审要求补 kimi 技能验证 | 引用 H4-ii 声明 + 本路线图，说明技能验证属续篇前瞻设计 |
| 旋钮组合爆炸 | v1.3 已消解：两段式 + 确认性旋钮砍至规模 × 信息集（§4.2），探索性臂不做确认性断言 |
| 统计力不足（factorial 摊薄 + 期末考低 power） | v1.3 两段式集中 power 于 Stage 2（1–2 主效应 + 显式 MDE 声明，§4.3）；评估集 power 分配写入预注册（§4.5） |
| pilot 未过 go/no-go | 修管线后重跑 pilot，不放量 B1（§4.6 B0.5 判据：trace 完整率 / 解析成功率 / 结算时延 / 成本对账） |
| 成本超阈值 | §4.7 降级规则：先砍探索性臂 → 再缩 Stage 1 分箱精度 → 最后调 MDE（回预注册修订留痕） |

## 8. 检查点

- [ ] Paper A：按 v2 开题 + 计划 v1.1 推进 W1–W8，过 G0/G1/G2 闸门
- [ ] Paper B：B0 管线就绪（四件规格化交付物齐：trace schema + 冻结验证 SOP + 任务流调度规则 + 结算来源裁定记录；trace 记录跑通 demo）
- [ ] Paper B：B0.5 pilot 试跑通过 go/no-go（trace 完整率 100% / 解析成功率 ≥98% / 结算时延中位数 ≤72h / 成本实测对账）
- [ ] Paper B：任务流上线，首批前瞻预测落盘，运行期监控四字段逐次落盘（§4.8）
- [ ] Paper B：启动 B1 前完成 OSF 时间戳预注册（Stage 1 分箱规则与每箱下限、Stage 2 的 1–2 主效应 + 显式 MDE、herding 操作化阈值、期末考划分规则、冻结粒度清单）
- [ ] Paper B：Stage 1 达量（V(x) 分箱下限）→ 按冻结粒度清单冻结 → Stage 2 期末考（按 MDE 定量）
- [ ] 双篇交叉引用核对（A 的悬念句 = B 的假设句，措辞一致）

## 9. 版本记录

- v1.0（2026-07-21）：初版。依据 2026-07-21 会话裁定（双篇拆分同意）撰写；上游 = v2 开题 + kimi 归因方向拒收评估 + Scaling Agent Systems 范式解剖。
- v1.1（2026-07-21）：按双篇顶刊差距评估（`docs/investigations/two-paper-roadmap-nature-gap-assessment-2026-07-21.md`）R-B1–R-B6 补救路径改进：§4.1 新增 herding 操作化双层指标；§4.2 新增第四旋钮（信息集消融，落实 M5）+ 底座 ≥2 模型家族 + 任务流/结算来源三路径裁定 + 三段式差异化论证要求；§4.3 重做 power analysis（锚点溯源 [arXiv:2605.00420] + 方案 A 扩量 10³–10⁴ / 方案 B 砍假设 + MDE + adaptive design 预注册）；§4.5 期末考规则补齐规格（随机分层、power 分配、冻结粒度清单）；§4.6/§7/§8 同步更新；§6 新增结构性边界第 6–7 条。
- v1.2（2026-07-22）：追加两条方法论边注：§3.1 旁引 MCDP-1 p.11 支撑"PIV 是审计结果之一而非附属标签"；§4.2 表格后引 MCDP-1 p.16/p.68–69 约束"规模 × 异构 × 聚合 × 信息集"的设计哲学（来源 `cds4polymarket/docs/investigations/uncertainty-decision-methodology-2026-07-21.md` §5.1 #4/#7、§5.2 #8，引用纪律均按"受条令启发的设计类比"标注）。无内容性改动。
- v1.3（2026-07-22）：按文献扫描（`analysis/roadmap-v12-scan/refscan.md`）+ 系统工程审查（`analysis/roadmap-v12-scan/se-review.md`）修订，编排器裁定"优化即可，不重构"：
  - (A) Paper B 主干改为 AMW 充分统计量两段式：§4.2/§4.3 重写为 Stage 1 估 V(x)（描述性、moderate n）→ Stage 2 验证最优聚合/披露策略（确认性、1–2 主效应 + 显式 MDE），v1.1 方案 A/B fork 与两阶段 adaptive design 被两段式吸收；聚合旋钮增补选择性路由探索臂；§4.1 herding 操作化补 AMW/Dunning 信念更新权重机制注记（Stage 2 候选机制）；
  - (B) 旋钮削减：确认性旋钮 = 规模 × 信息集（人设、聚合降探索性）；规模水平改 3/10/30 对数间隔，300 分身降为可选探索探针（成本约束）；commit-reveal 降级为 OSF 时间戳 + git hash 链；
  - (C) §4.6 时间线改 B0 → B0.5 pilot → B1 → B2 → B3：B0.5 go/no-go 判据写明，B0 四件交付物规格化；
  - (D) 新增 §4.7 成本估算（调用量公式、量级区间、降级规则；旧方案 A 60万–600万次调用警告留档为被规避的历史背景）；
  - (E) 新增 §4.8 运行期监控（解析漂移 / 结算延迟 / API 版本变更三类静默失败的校验与处置）；
  - (F) 新增 §10 参考文献（主引 AMW；背景 Dunning、BHS；沿用四篇 arXiv 条目补全；Tychastic 驳回留痕）；
  - (G) §1 决策链加第 7 条；§2/§4.5/§7/§8 同步消除对已废止方案 A/B 的引用。
  - 版本号说明：编排器清单原定 v1.2，因本节已存在 v1.2（MCDP-1 边注）条目，顺延为 v1.3。
  - 保持不动：Paper A（§3）、措辞纪律、§6 结构性边界、§4.4 归因操作化、§4.5 随机分层划分（SE review B4–B6 的 κ 门槛/期末考划分/PIV 字段精简建议未经编排器裁定，不纳入本版）。
- v1.4（2026-07-22）：开题报告侧联动——`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` 升 v1.4，新增 §1.4 设计哲学（FM 6-0 §1-74 单引文开篇，标注"受条令启发的设计类比"），与本路线图 v1.2 两条 MCDP-1 边注同源（`cds4polymarket/docs/investigations/uncertainty-decision-methodology-2026-07-21.md` 启发 1）。本路线图正文无改动。

## 10. 参考文献

**主引**

- Agarwal N, Moehring A, Wolitzky A. Designing Human-AI Collaboration: A Sufficient-Statistic Approach. Working paper, 2025-04-18（文中日期）. 作者单位：MIT/NBER、Purdue、MIT. JEL: C91, D83, D89, D47. 出处（期刊/编号）：unknown（截至 2026-07-22 未见发表信息，引用前须外部核实是否已有期刊版）。引用时须声明跨域借用：实验对象为 human-AI 协作（人是决策者），Paper B 为全 LLM 群体。

**背景**

- Dunning RE. Factors Affecting Appropriate Reliance on Artificial Intelligence Decision Support Systems. PhD dissertation, Department of Engineering and Public Policy, Carnegie Mellon University, Pittsburgh, PA, 2024-08. 出处 URL：unknown（非同行评审学位论文，仅作 reliance 操作化先例背景引用；其 "Oracle Policy" 评分与 skill score 定义与本项目 proper-score 体系不同，不可混用术语）。
- Bradley C, Hirt M, Smit S. *Strategy Beyond the Hockey Stick: People, Probabilities, and Big Moves to Beat the Odds*. Hoboken, NJ: John Wiley & Sons, 2018.（实践者书籍，仅作"外部视角/基准率"背景，不作承重学术引文；其样本数字出自 McKinsey 内部数据，引用须标注非公开可复算。）

**沿用（正文已引，补全条目）**

- Nechepurenko, Shuvalov（first names unknown）. Foresight Arena: An On-Chain Benchmark for Evaluating AI Forecasting Agents. arXiv:2605.00420 v2, 2026-05-04.
- Bosse. Automating Forecasting Question Generation and Resolution for AI Evaluation. arXiv:2601.22444 v2, 2026.
- Li et al. InfoDelphi: designed information asymmetry for multi-agent belief revision. arXiv:2607.01661, 2026.
- Kim Y, Gu K, Park C, Park C, Schmidgall S, Heydari AA, Yan Y, Zhang Z, Zhuang Y, Liu Y, Malhotra M, Liang PP, Park HW, Yang Y, Xu X, Du Y, Patel S, Althoff T, McDuff D, Liu X. Towards a Science of Scaling Agent Systems. arXiv:2512.08296v2 [cs.AI], 2025-12-17. Google Research / Google DeepMind / MIT（通讯作者 Yubin Kim、Xin Liu；© 2025 Google；书目自 `analysis/kimi-reasoning-assessment/reference-paper-anatomy.md` 提取）。

**驳回记录**

- Ross IM, Karpenko M, Proulx R, King J. Tychastic Optimization of ISRT Information Systems（NPS-MAE-23-009, Naval Postgraduate School, 2023-10）：军事 C2/网络拥塞控制域，与双篇主题、方法、文献谱系均不相交，经 2026-07-22 文献扫描判定**不列入**（仅备查，不引原文）。
