# 决策流水线评估包独立红队评审 — 2026-07-19

> 评审人：独立评审子代理（无作者上下文）。评审日期：2026-07-19。

---

## 一、评审独立性声明

### 1.1 允许且已读（8 份，按访问顺序）

| # | 文件 | 行数 | 精读范围 |
|---|---|---|---|
| 1 | `idea-decision-pipeline-2026-07-19.md` | 1–68 | 全文 |
| 2 | `PROJECT-BRIEF.md` | 1–217 | 全文 |
| 3 | `proposal-decision-coscientist.md` | 1–367 | §0–§5 + 附录 A–C |
| 4 | `reviews/r2-review.md` | 1–124 | 全文（仅作结构 rubric 借用，不引用其措辞） |
| 5 | `adjacent-work-positioning-2026-07-19.md` | 1–104 | 全文 |
| 6 | `pipeline-design-spec-2026-07-19.md` | 1–435 | 全文 |
| 7 | `asset-mapping-2026-07-19.md` | 1–95 | 全文 |
| 8 | `prompt-exports/stage4-code-audit.md` | 1–115 | 全文 |

### 1.2 未读（按任务约束）

- `prompt-exports/` 下其它任何文件（尤其 `oracle-plan-*` 与 `stage1/2/3-recon-*` 草稿）
- q1/q2/q5 备忘录
- `sources/` 下 PDF
- Policysim-v0.2 任何源码

### 1.3 评审结构沿用

借用了 r2-review.md 的五维 rubric（novelty / 效度 / 统计严谨性 / 可行性 / 诚实边界）与"评分+≥2 段理由+严重清单"组织形式；**不复制其具体措辞**，所有发现均针对本评估包文本给出独立证据。

---

## 二、五维评分表

| 维度 | 分数 | 严重问题数 | fatal? |
|---|---|---|---|
| 1. novelty 区分度 | 4 | 2 | 否 |
| 2. 证据链效度 | 3 | 3 | 否 |
| 3. 统计/协议严谨性 | 3 | 2 | 否 |
| 4. 工程可行性 | 3 | 2 | 否 |
| 5. 诚实边界 | 4 | 1 | 否 |

**fatal 计数：0**（五维均 ≥3；fatal 阈值为 ≤2）。

---

## 三、逐维理由

### 维度 1 — novelty 区分度：4/5

**真实优点。** `adjacent-work-positioning-2026-07-19.md` §1.1–§1.3 三条切线采取了清晰的"祖先已存在、组合点未占位"修辞：§1.1 把 AFlow/ADAS/EvoAgent 归入"workflow 进化搜索红海"、Co-Scientist Supervisor 定位为"半动态调度、不解决步骤级降级"、Biomni 定位为"单 agent 调工具"；§1.2 把 NIST/ICS/FAA/NUREG/IMO 归入"30 年人类组织侧流程化工程基线"；§1.3 把 ROC 2002 + Avizienis 2004、Lichtenstein-Fischhoff-Phillips 1982 + Morgan-Henrion、Heuer 1999 + Rumsfeld 三条先验分别映射到 `confidence_grade` 离散分级、`calibration_check` 四件套、`explicit_known_unknowns` 四字段。这种"先承认先验、再论证耦合点空缺"的写法比硬性宣称"全网无先例"诚实得多，且与开题 v1.3.1 §2.5 R1-N1 三重限定组合修辞同源，跨文档一致。贡献落点收窄为"应急决策方法论的流程固化 + 步骤级降级协议显式化"——这一收窄与 idea §5 第 4 条"贡献点切割"的内部声明吻合，**novelty 没有滑向 AFlow/ADAS 红海**。

**真实问题。** (a) §1.1 自承"AFlow / ADAS / EvoAgent / Biomni 4 篇为摘要级证据"（附录 A 限制声明），但 §1.1 四维对比表对 5 个邻居均作出"❌ 无 per-step 置信度"或"❌ 无显式降级协议"二值判定——摘要级证据能否支撑"明确缺失"的断定，是评估包未回答的方法学瑕疵；同一切线内"3 条待复核项"（EvoAgent 标题歧义 / IMO 决议编号 / Cooke method + Morgan-Henrion 1990）直接暴露了 §1.2 与 §1.3 的证据不闭合——其中 Cooke method 与 Morgan-Henrion 1990 被 §1.3 用于"data / model / expert 三档分类"的承重论据（表格先验 2 行 (c) 列），但核验状态为 `[未核验-需复核]`，这与该行声称"`calibration_check` 四件套直接引用 H4"的承重论据强度不匹配——若是承重论据，承重论据不应是未核验文献。`(b)` §1.2 二维区分表对 IMO SOLAS/MARPOL/SOPEP 的引用虽然诚实标注未核验，但 §1.2 末段据此断言"三者的目标函数与本想法的『诚实呈现无知』都不重合"——该断言依赖"IMO 决策书是人类事后填表"这一未经核验的定性判断，若 IMO 决议后续版本含有机器可读的 confidence 字段，落点收窄论据需要重写。

### 维度 2 — 证据链效度：3/5

**真实优点。** `pipeline-design-spec-2026-07-19.md` §2.1 的 8 步 YAML 契约在字段命名上做了显式追踪：步骤 1 / 4 / 5 / 6 / 7 共 5 步直接复用既有 schema（侦察 §4 改名建议全部采纳，例如 `downgrade_reasons` → `step_degradation_reasons`、`trace_alignment_score` → `trajectory_dtw_aggregate`、`calibration_check` 补齐为四件套含 `kendall_tau`），§2.2 表格对 `ignorance_class` / `origin` / `explicit_known_unknowns` / `counter_signal` / `reason_for_inconclusive` 五个易混字段做了正交性切割（语义分家，三者命名不重叠）——这种"命名不重叠"的纪律在 r2-review 维度二的整体批评论调下是一种实操回应。降级 DAG（§2.2）给出了 INSUFFICIENT 传全部下游 ≤ MEDIUM、LOW 只传直接后继 ≤ MEDIUM 的两条规则，并形式化为 `grade(S_{i+1}) ≤ ceil_upstream_grade(grade(S_i))`、`ceil(x) = MEDIUM if x == INSUFFICIENT or x == LOW else x`——形式化层闭合。

**真实问题。** (a) **§2.3 hard checkpoint 存在逻辑裂缝**。硬约束的 4 个合取项之一是 `NOT any(validation_arms.red_flag)`；但 §2.1 步骤 6 的 violation_handling 又规定"`validation_arms 全空 (校验臂协议未配置) → 标 INSUFFICIENT 继续, 触发整体 hard checkpoint 中『校验臂无标红』合取项的失败`"——空 validation_arms 在 `NOT any(red_flag)` 上为 vacuously true（永真），与"触发『校验臂无标红』合取项失败"互相矛盾——同一文档的契约层对同一状态有两种相反的判定。这是 §2.1 与 §2.3 之间的内部不一致，应在阶段 5 实施前闭合。(b) **校验臂零实现造成 cascading INSUFFICIENT**。asset-mapping §3.3 第 6 行明示"工程实现 0（GB 50151 / NUREG-CR-7002 / SFPE 在 dev/backend 全仓 grep 0 命中）"；若校验臂始终未配置，步骤 6 始终 INSUFFICIENT → 步骤 7 上限 ≤ MEDIUM（H4 传导）→ 步骤 7 因 kendall_tau 无法计算（无校验臂参照排序）会再触发 `kendall_tau < 0.5` 的 INSUFFICIENT → 步骤 8 接收 ≥3 个 INSUFFICIENT 上游 → `insufficient_step_count >= 4` 强制终简报 INSUFFICIENT。整条流水线在当前实现状态下结构性必然失败——`hard checkpoint` 的 `insufficient_step_count <= 3` 与 `5/8 grade ≥ MEDIUM` 两个合取项几乎不可能同时满足。换言之：**契约能闭合，但只在"校验臂实现完成"前提下闭合**；当前实现状态使契约的闭合性悬空。(c) 步骤 6 在判定中扮演的角色是"校验臂结果如实呈现 + 由 step_7 在 H4 框架下处理"——但 H4 框架要求 kendall_tau ≥ 0.5 与校验臂参照排名相关，校验臂未实现时 H4 量化无法执行；步骤 6 的角色清晰但其上游（校验臂实现）与下游（H4 量化）都不可得，**步骤 6 在契约层清楚、在实施层落空**。

### 维度 3 — 统计/协议严谨性：3/5

**真实优点。** Hard checkpoint 设计为单一布尔 `GO = (steps_completed == 8) AND (count(grade ∈ {HIGH, MEDIUM}) >= 5) AND (NOT any(validation_arms.red_flag)) AND (insufficient_step_count <= 3)`（§2.3 第 1 条）——4 个合取项均为可观测、可枚举、可写测试断言的纯布尔量。呈报规则按合取项失败原因逐条标定（"流程不完整" / "证据强度不足" / "物理闸门标红" / "降级过度"）并配对升级阶梯（直接报人 / 标 MEDIUM 步列出供人增补检索 / 由人决定否决还是降级为参考 / 触发振荡检测或转 fallback）——呈报粒度与升级动作一一对应，不存在"失败原因不明"的灰色地带。振荡检测触发条件双轨（任一步 R/S 动作 ≥ 2 次且累计 ≥ 2 步 OR insufficient_step_count ≥ 4）覆盖了"退步振荡"与"降级泛滥"两类典型失效模式，触发后 fallback 路径明确（终简报 grade 强制 INSUFFICIENT + 决策简报末尾追加 fallback paper 建议）。

**真实问题。** (a) **回退条款动作词抽象、不可执行**。§2.3.2 三选一矩阵中步骤 4 的 R 动作写为"候选空 → step_3 放宽召回"——"放宽召回"在文档全篇没有操作化定义（是降相似度阈值？换检索后端？改写 keywords？），步骤 5 的 R 动作写为"提示策略生成参考工程夹逼"——"工程夹逼"同样没有操作化定义（哪个规范条文？哪组数值约束？）。两条 R 动作因此**在实施层不可证伪**，可能在流水线运行时被静默地"自由发挥"。`(b)` **回退条款缺少步骤 7 失败的兜底**。§2.3.2 表中步骤 7 的三选一动作只有"I（标 INSUFFICIENT 继续）"——当 step_7 INSUFFICIENT 时其下游只有 step_8 一个汇集点，但若 step_7 INSUFFICIENT 同时伴随 step_6 INSUFFICIENT（cascading 情形见维度 2(b)），两步叠加会使 §2.3 hard checkpoint 的 `5/8 grade ≥ MEDIUM` 与 `insufficient_step_count <= 3` 同时失守——`升级阶梯总论` 的"返工一次仍失败 → NO-GO"会触发，但返工的"修改后重跑"动作没有指向——是回到 step_4 重生成？回到 step_1 重 Intake？没有写到。`(c)` Hard checkpoint 第 1 条 `steps_completed == 8` 与步骤 8 violation_handling 第 1 条"任何中间步 output 缺失 → 标 INSUFFICIENT 继续, decision_brief_markdown 必含『流水线不完整』提示"在概念上重复但未统一——若步骤 1 缺失则 steps_completed=1 而非 0，"流水线不完整"提示和 `步骤 8 INSUFFICIENT` 都会同时产出，呈报是否会重复？`count(grade ∈ {HIGH, MEDIUM})` 是否计入 `INSUFFICIENT` 的步骤 8 自身？文档未澄清。

### 维度 4 — 工程可行性：3/5

**真实优点。** `asset-mapping-2026-07-19.md` §3.3 的 4 项改造档位（low / low / low / medium）经 `stage4-code-audit.md` 独立代码级复核（line 33-100）后**全部维持**——证据来自：(i) `FactorLedgerDraft.factors[].confidence: 'high' | 'medium' | 'low'` 在 service / spec 两处保留（line 404/428/452 spec 断言不变）；(ii) `Report` 实体 `result` 字段是 `text` 类型，无 migration；(iii) `m3-decision.contract.spec.ts:25,94` 仅断言 `reportId + downloadUrl`；(iv) `ReportService` 下游 controller/module 仅构造路径无字段绑定；(v) `get_file_tree` 全仓搜 `synthesis-report` / `SynthesisReport` 0 命中（确认新建无冲突）；(vi) `dossier-repository.service.ts:84-93` 的 ENOENT→null 降级形态已存在、调用方编排层判空逻辑已就位（line 142-148）。§3.1 矩阵的 48 格计数（✅ 11 / 🟡 3 / 🟠 33 / ❌ 1）与其内嵌的诚实声明（"18 个 🟠 集中于新建步骤的全行无既有资产复用面——这是新建步骤的必然结果，非既有资产流失信号"）使得 4 项改造的真实触点 = 1–2 个文件（`decision-report.service.ts` 必须改 + `synthesis-report.service.ts` 可选新建）这一结论可被代码实证。

**真实问题。** (a) **stage4-code-audit §1 标注的关键风险未被阶段 2/3 文档吸收**。复核报告 §1 "被低估的风险"段明示：`summary.fallbackUsed`（bool）聚合到 4 档时需要**额外判断逻辑**（fallback=true 未必等于 INSUFFICIENT——可能仅为模型切换），这条业务规则 Stage 2.1 YAML 契约**未明确**——若需在 `DecisionSummary` 实体加字段，cost tier 应升至 **medium**。回查 `pipeline-design-spec-2026-07-19.md` §2.1 步骤 5 output_schema，`summary.fallbackUsed` 字段确实不存在于契约字段集（步骤 5 输出是 `factor_ledger_entries` / `trajectory_dtw_aggregate` / `scores.percentile_hit` / `protocol_failures` / `confidence_grade` / `step_degradation_reasons`），但 stage4-code-audit 的复核基于现有 Policysim 代码（`summary.fallbackUsed` 是 Policysim 现有字段，不是本评估包新加的字段）——这意味着**新加的 `confidence_grade` 与 Policysim 现有 `summary.fallbackUsed` 之间的聚合规则必须由阶段 5 实施者自己定**，契约层没给。这一缺口直接影响步骤 5 字段改造是否会破坏现有 schema：若聚合规则用 fallbackUsed 单 bool 不足以判 4 档、需要再加字段（stage4-code-audit §1 末句假设的反例），那 `buildReportPayload` 的 3 档→4 档显式映射需要更多数据来源——这与"维持 low"的判定产生内在张力。`(b)` **新建 Agent 工作量未在 4 项改造中体现**。§3.3 末尾自承"该评估包的最大工程负担是新建 Agent 主体代码（Intake / Decomposition / Retrieval / Synthesis），而非改 Policysim 既有代码"——4 项改造聚焦"既有代码改造量"，但 4 个 Agent 本身（§3.2 步骤 1/2/3/8）每个都是"完全新建"或"部分新建"，工作量为"约 150–250 行 service"或更高；§3.3 第 5 项"步骤 5 字段新增"实际是触发整个流水线跑通的前置（否则 4 个 Agent 即使实现也无落脚点），工作量在 §3.3 表中列为 low 但其下游工作量未被纳入同一张表。`(c)` 步骤 5 `confidence_grade` 字段新增是 4 项改造中**唯一被多次代码层验证为"维持 low"** 的（line 44、line 89-90 双重确认），但 stage4-code-audit §1 末句的"如果规则需在 DecisionSummary 实体加字段"是明示的**上调风险**——评估包未给该风险的兜底方案。

### 维度 5 — 诚实边界：4/5

**真实优点。** §2.2 "已知 / 推断 / 无知"三档判定规则表对机器可判 vs 必须人判做了显式切割——IGNORED 档位的"机器判『未编码』易，『判该编码』难"是诚实的认识论声明；`IRREVERSIBILITY 约束`（"档位判定一旦落盘, 不可被同一步骤内部 upgrade，升级需经下一轮 pipeline 重跑, 由人拍板位确认"）是对"步骤内自圆其说"的明确隔离。§2.1 步骤 8 violation_handling 第 2 条"`insufficient_step_count >= 4` → 终简报 grade 强制 INSUFFICIENT + 人拍板位突出『流程本身不完备』"与 §2.2 终简报 markdown 骨架的"人拍板位"四复选框（候选排序是否采纳 / 无知清单是否补检索 / 校验臂任一 red_flag 是否升级为否决 / 终简报 grade 是否接受 → 决定 GO / 降级 / NO-GO）配合，在终点把决策权完整交还给人——四复选框各自对应一个降级维度，与 §2.3 硬约束 4 个合取项一一映射，"AI 只动嘴"在终点被诚实尊重。asset-mapping §0 先行诚实声明（"『八角色』是设计目标非现状"+"校验臂 + Multi-Judge 在 Policysim 仓内零实现"）是难得的预防性反误导设计，避免下游误读现状。

**真实问题。** (a) **三档判定规则的"必须人判"边界在阶段 5 之前没对齐**。`pipeline-design-spec-2026-07-19.md` 附录 A 修订记录末明示"§2.2 三档判定规则的『必须人判』边界需要阶段 5 终裁时引入人拍板位模板对齐"——这是一个被诚实承认的待闭合缺口，意味着当下评估包对人拍板的承诺是"骨架已就位、人拍板模板未对齐"。`ignorance_triple` 字段在 `report.service.ts` 轻量备选路径是建议落点（§3.3 备选段），但其字段命名（`{ known, inferred, unknown }`）与 §2.2 IGNORED 档位命名（`IGNORED` 而非 `UNKNOWN`）有一字之差——IGNORED 在情报分析传统（Heuer 1999）里是"已识别但被忽略"的语义，与朴素英文 UNKNOWN 的"未知"不同；这是命名 vs 语义的潜在张力，会影响人拍板位能否真的"判该编码是否合理"。(b) **"AI 只动嘴"在步骤 4 Generation Agent 处张力明显**。Generation Agent 输出 `candidate_strategies[]`——这是**生成**新候选策略，不是单纯"动嘴描述既有选项"；idea §1 表格对步骤 4 的描述是"策略生成 → 候选策略池"，其输出是开题 §1.3 generation 语义的承接。`pipeline-design-spec-2026-07-19.md` §2.1 步骤 4 output_schema 给出 `risk_hint` 字段（"生成策略被拒的原由"），这一字段的存在隐含 Generation 步骤**会产出可被否决的策略**——这是合理的诚实（开题 H1/H3 终点靠专家裁定），但 Generation Agent 在产物层的"动嘴"含义比 Synthesis Agent 的"动嘴"更宽：Synthesis 是"汇总既有产物为决策简报"（无新内容生成），Generation 是"产生新候选"（有新内容生成）。文档未对此做命名或边界切割，会被审稿人或工程实施方读为"动嘴宽口径解释"。

---

## 四、引用抽查记录（≥3 条新论断）

| # | 论断 | 出处 | 文档内自洽性 | 核验状态标注诚实性 |
|---|---|---|---|---|
| 1 | **"5 邻居均无降级协议"** | `adjacent-work-positioning-2026-07-19.md` §1.1 四维对比表 | 表格内 5 邻居 (d) 列均为 ❌——表内自洽；但结论"在 5 邻居中均未占位"依赖证据强度（摘要级 vs 全文级） | 附录 A 限制声明自承 4 篇为摘要级证据 + Biomni 计划已批准摘要级——标注**基本诚实**，但 §1.1 主表未在每行重复"摘要级"标记，易让读者误判为全文核验 |
| 2 | **"八角色实为 6 角色"** | `asset-mapping-2026-07-19.md` §0 先行诚实声明 + §3.1 步骤 4 单元格脚注 | 与 §3.1 步骤 4 行的"✅ 直接复用"+"八角色扩位仅改 seed（成本 low）"自洽；与开题 v1.3.1 §2.1 的"八类角色"表述存在版本差异（开题是设计目标、评估包是现状盘点）——这是合理的内部不一致，但应在阶段 5 评估包引用时点明 | §0 标注**完全诚实**，并在 §3.1 用 🟡 标识 + 脚注解释"扩位仅改 seed"——优于常规 |
| 3 | **"校验臂在 Policysim 仓内零实现"** | `asset-mapping-2026-07-19.md` §3.1 步骤 6 + §3.3 第 6 行 | stage4-code-audit §1/§6 两次确认"全文 `red_flag`/`validation_arms` 0 命中"——交叉证据闭合；与 §3.1 步骤 7 行的"multi-judge panel / adjudicator 生产模块 0 实现（仅 ab-judge.ts 离线脚本）"组合自洽 | 标注**完全诚实**——给出全仓 grep 结果 + 离线身份实证（import 拓扑）+ 文件级证据（`ab-judge.ts` Paratera provider 依赖）三层 |
| 4 | **"summary.fallbackUsed→confidence_grade 聚合规则未在 Stage 2.1 YAML 明文"** | `stage4-code-audit.md` §1 风险段末句 + §6 总评警示 | 回查 `pipeline-design-spec-2026-07-19.md` §2.1 步骤 5 output_schema 字段集确实不含 `summary.fallbackUsed`——stage4-code-audit 的诊断**与文档实际内容一致**；但 stage4-code-audit 同时假设"如果不需在实体加字段，则维持 low"——该假设本身在文档中无独立证据支持 | stage4-code-audit 的标注**诚实且谨慎**——既指出风险、又明示假设前提；问题在于评估包阶段 2/3 未对该风险给出吸收路径，应在阶段 5 前闭合 |

**抽查结论**：3 条核心论断的文档内自洽性均成立；1 条复核附件标记的风险在评估包中**未被消化**，属于评估包的内部缺口（详见第五节严重问题清单 [严重-4]）。

---

## 五、致命问题计数

**致命问题数：0**（五维均 ≥3；无任何一维落入 ≤2 区间）。

---

## 六、严重问题清单

### 严重级（6 条）

| 编号 | 等级 | 问题 | 证据 | 可执行修法 |
|---|---|---|---|---|
| [严重-1] | 严重 | §2.3 hard checkpoint 合取项 `NOT any(validation_arms.red_flag)` 与 §2.1 步骤 6 violation_handling 对 `validation_arms 全空` 给出相反判定 | `pipeline-design-spec-2026-07-19.md` §2.1 步骤 6 violation 第 2 条 + §2.3 hard checkpoint 第 3 条 | 二选一：(a) §2.1 步骤 6 全空时改写 hard checkpoint 触发条件为"validation_arms 存在且任一 red_flag==true 才失败"；(b) §2.1 步骤 6 全空时改写为"标 INSUFFICIENT 且 hard checkpoint 自动失败" |
| [严重-2] | 严重 | Hard checkpoint `5/8 grade ≥ MEDIUM` 与 `insufficient_step_count <= 3` 在"校验臂零实现"前提下**结构性必然同时失守**——契约闭合性悬空 | asset-mapping §3.3 第 6 行"工程实现 0" + §2.3 第 2/4 合取项 + §2.1 步骤 7 kendall_tau 阈值 | 在阶段 5 前补 §2.3 兜底条款："若校验臂未实现且 MVE 阶段 N=1 内仍未上线，则 hard checkpoint 第 3 合取项不适用、降级为评审提示项" |
| [严重-3] | 严重 | §2.3.2 回退条款 R 动作在步骤 4/5 的描述词"放宽召回""工程夹逼"无操作化定义，**不可证伪** | `pipeline-design-spec-2026-07-19.md` §2.3.2 步骤 4/5 R 动作行 | 在 §2.3.2 矩阵脚注加操作化定义：步骤 4 R = "将 `knowledgeBaseQuery.keywords` 扩展为包含相邻 3 个 disasterType 关键词的并集（上限 30 词）"；步骤 5 R = "触发 `protocol_failures` 中列出的工程规范号 → 步骤 4 的 risk_hint 字段强制包含对应规范条款" |
| [严重-4] | 严重 | stage4-code-audit §1 标记的 `summary.fallbackUsed→confidence_grade` 聚合规则风险**未被阶段 2/3 文档吸收**——契约层无明文规则，可能引发 cost tier 上调与 schema 破坏 | `stage4-code-audit.md` §1 末段假设反例 + `pipeline-design-spec-2026-07-19.md` §2.1 步骤 5 output_schema 字段集无 `fallbackUsed` | 阶段 5 前在 §2.1 步骤 5 加聚合规则脚注："若 `summary.fallbackUsed==true` 且 `factor.confidence == 'low'` 出现 ≥3 条 → confidence_grade ≤ LOW；其他情形 → 维持各步 grade 聚合"（规则示例，待 stage5 评审拍板） |
| [严重-5] | 严重 | §1.3 先验 2 的承重论据（Cooke method + Morgan-Henrion 1990）核验状态为 `[未核验-需复核]`，但被用于"data / model / expert 三档分类"与 HIGH ≈ data-confirmed / MEDIUM ≈ model-derived 等关键映射的承重论据 | `adjacent-work-positioning-2026-07-19.md` §1.3 表格先验 2 行 (c) 列 + 表格 [未核验-需复核] 标注 + §2.2 IRREVERSIBILITY 约束 | 在阶段 5 前完成核验：要么联网核验 Cooke method 现行版本与 Morgan-Henrion 1990 第 2 版（如有）、要么将该映射退为"启发性参照"（同开题 v1.3.1 §2.4 对 Chen 2026 的处置） |
| [严重-6] | 严重 | §1.2 切线收尾断言"IMO / FAA / Phillips-Goodrich-Wenger 2009 三者的目标函数与本想法的『诚实呈现无知』都不重合"依赖未经核验的 IMO 决策书定性（人类事后填表） | `adjacent-work-positioning-2026-07-19.md` §1.2 末段断言 + 二维区分表 IMO 行 `[未核验-需复核：具体决议编号]` | 阶段 5 前查 imo.org IMODOCS 复核 MSC.1/Circ.1568 / A.1075(28) 现行版本；若 IMO 决议含机器可读 confidence 字段，则 §1.2 落点陈述须重写 |

### 一般级（4 条）

| 编号 | 等级 | 问题 | 证据 | 可执行修法 |
|---|---|---|---|---|
| [一般-1] | 一般 | §2.3 hard checkpoint 第 1 条 `steps_completed == 8` 与 §2.1 步骤 8 violation_handling 第 1 条"流水线不完整"提示存在概念重复，呈报是否会重复未澄清 | `pipeline-design-spec-2026-07-19.md` §2.3 第 1 合取项 + §2.1 步骤 8 violation 第 1 条 | 在 §2.3 呈报规则顶部加优先级表："不完整提示 ⊂ grade=INSUFFICIENT；`steps_completed==8` 失败时 grade 强制 INSUFFICIENT；不重复呈报" |
| [一般-2] | 一般 | §1.1 主表对 5 邻居均判定 ❌ 无降级协议，但摘要级证据占 4/5——证据强度与判定力度不匹配 | `adjacent-work-positioning-2026-07-19.md` §1.1 主表 + 附录 A 限制声明 | 在 §1.1 主表每行右侧加核验状态徽章（[摘要级]/[全文级]），让读者一眼判定证据强度 |
| [一般-3] | 一般 | §3.3 4 项改造档位评估聚焦"既有代码改造量"，但 §3.3 末段自承"评估视角的差别"——4 个新建 Agent 的工作量未在同一张表 | `asset-mapping-2026-07-19.md` §3.3 末段 + §3.2 | 在 §3.3 加附表"4 个新建 Agent 工作量分项估计"：每项行数 / 复用面 / 单测用例数 |
| [一般-4] | 一般 | §2.2 IGNORED 档位在文档主体使用但 §3.3 备选路径建议命名 `unknown`——命名 vs 语义的潜在张力 | `pipeline-design-spec-2026-07-19.md` §2.2 IGNORED 档 + `asset-mapping-2026-07-19.md` §3.3 备选段 `unknown` | 统一命名：在 §3.3 备选段改 `unknown` 为 `ignored`，与 Heuer 1999 情报分析传统对齐；或在 §2.2 加 IGNORED/UNKNOWN 命名差异脚注 |

### 瑕疵级（2 条）

| 编号 | 等级 | 问题 | 证据 | 可执行修法 |
|---|---|---|---|---|
| [瑕疵-1] | 瑕疵 | §2.2 表格"必须人判"列对 KNOWOWN 档位写"—"——可能误读为"无需人参与"而非"无需人额外判" | `pipeline-design-spec-2026-07-19.md` §2.2 判定规则表 | 改"—"为"无（数据自带）" |
| [瑕疵-2] | 瑕疵 | 评估包三份文档各自的"修订记录"末段均标注"评审状态：未评审（阶段 4 红队评审的输入材料）"——本评审完成后未在文档中闭环 | `adjacent-work-positioning-2026-07-19.md` / `pipeline-design-spec-2026-07-19.md` / `asset-mapping-2026-07-19.md` 附录 A 末行 | 阶段 5 前在本评审文件链接处加一行响应 |

---

## 七、5 条最优先修改建议（每条 ≤3 句）

1. **闭合 hard checkpoint 逻辑裂缝**：[严重-1]+[严重-2] 合并——在 §2.1 步骤 6 violation_handling 与 §2.3 hard checkpoint 之间加 6 行一致性声明，明确"validation_arms 全空"在两处的判定如何收敛；并加 §2.3 兜底条款"校验臂未实现时 hard checkpoint 第 3 合取项降级为评审提示项"，避免契约闭合性悬空。

2. **操作化步骤 4/5 R 动作词**：[严重-3]——把"放宽召回"改为"将 `knowledgeBaseQuery.keywords` 扩展为相邻 3 个 disasterType 关键词并集（上限 30 词）"；把"工程夹逼"改为"`protocol_failures` 中列出的规范号 → 步骤 4 的 `risk_hint` 强制包含对应规范条款"，两条 R 动作即可被测试断言。

3. **吸收 stage4-code-audit §1 的 fallbackUsed 聚合风险**：[严重-4]——阶段 5 前在 §2.1 步骤 5 output_schema 脚注加聚合规则草案（fallbackUsed=true + factor.confidence='low' ≥3 条 → grade ≤ LOW；其他情形 → 维持 grade 聚合），避免 cost tier 因聚合规则悬空而暗升。

4. **核验两条承重论据并明确降级**：[严重-5]+[严重-6]——阶段 5 前联网核验 Cooke method 现行版本与 Morgan-Henrion 1990（§1.3 先验 2 承重论据），并复核 imo.org IMODOCS MSC.1/Circ.1568 / A.1075(28) 现行版本（§1.2 落点收尾论据）；未核验则按 Chen 2026 先例降为"动机性参照"，避免承重论据悬空。

5. **补 §3.3 4 个新建 Agent 工作量分项表**：[一般-3]——在 §3.3 末段加附表，列出 Intake / Decomposition / Retrieval / Synthesis 4 个 Agent 的行数估计、复用面、单测用例数（参考 §3.2 与 stage4-code-audit §2 synthesis-report.service.ts 的 150–250 行估算），让工程可行性评估的"既有代码 vs 新建 Agent"两个视角合并在同一证据面。

---

## 八、附录：stage4-code-audit.md 要点摘录

复核报告关键结论（引用 `prompt-exports/stage4-code-audit.md` 第 6 节总评表）：

| 改造点 | 标注档位 | 复核档位 | 决策 |
|---|---|---|---|
| 5 decision-report 字段新增 | low | low | 维持 |
| 6 校验臂降级传导 | low | low | 维持 |
| 7 judge INSUFFICIENT 机制 | low | low | 维持 |
| 8 synthesis-report 新建 service | medium | medium | 维持 |

**4 项改造档位均不被低估，0 项上调，0 项下调。**

复核报告核心证据：
- `buildReportPayload()` (line 229–257, 29 行单函数) 输出经 `JSON.stringify` 透传到 `Report.result`（JSON 字段），schema 不变
- `FactorLedgerDraft.factors[].confidence: 'high' | 'medium' | 'low'` 3 档内部类型在 service / spec 两处都仍存在（spec line 404/428/452 不需更新）
- `Report` 实体 `result` 字段是 `text` 类型，无 migration
- `decision-report.service.spec.ts` / `m3-decision.contract.spec.ts` / `osint.contract.spec.ts` / `dossier-repository.service.spec.ts` / `ab-judge.spec.ts` / `report.service.spec.ts` 共 6 份 spec、~1200 项测试——4 项改造中**没有任何一项触发现有 spec 的连锁更新**

**复核报告唯一警示**：`summary.fallbackUsed`（bool）→ `confidence_grade`（4 档）的聚合规则**必须在 Stage 2.1 YAML 契约层明确**（fallback=true 未必等于 INSUFFICIENT——可能仅为模型切换）。若需在 `DecisionSummary` 实体加字段，改造点 5 的 cost tier 应升至 medium。当前评估**假设** YAML 契约可在不增实体字段的前提下完整定义规则——这一假设未被阶段 2/3 文档吸收，是本评审 [严重-4] 的直接来源。

**复核报告未涉及但本评审指出的扩展**：复核报告聚焦"既有代码改造量"（4 项），未覆盖"4 个新建 Agent 主体代码工作量"——后者是 asset-mapping §3.3 末段自承的"评估包最大工程负担"，应在阶段 5 前补分项估计（[一般-3]）。

---

*文档版本：v1.0（2026-07-19，独立评审子代理生成；输入为任务约束允许的 8 份文件，未引用 r2-review.md 的具体措辞；五维均 ≥3，0 fatal）。*
