# 决策流水线评估包终裁 memo — 2026-07-19

> **2026-07-19 更正注记**：宽类（2 深案 + 1 宽类 N≥60）路径已补充（台风首选 IBTrACS v04r01 + CMA 最佳路径 + 省级响应通告 + EM-DAT 后果；地震备选 USGS FDSN），不改 H1/H2；决策行动锚源清单（mem.gov.cn / 省厅逐日爬取、IFRC GO actions_taken、NWS api.weather.gov CAP、NTSB CAROL、CSB PDF 等）已核实，可使 §5.5 步骤 3 检索不为空。

> **本文档为 2026-07-19 评估包组成部分，引用已冻结的开题报告 v1.3.1（`auto-research/docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md`）与项目简报 v1.3（`PROJECT-BRIEF.md`），但不修改它们。** 评估包包括 4 份本目录已有文件：阶段 1 邻近工作定位、阶段 2 流水线设计规范 v1.1、阶段 3 资产映射、阶段 4 红队评审；本 memo 是第 5 份。评估包自身为 §16 决策路径方法论的一次新实例化。
>
> 引用版本：开题 v1.3.1（冻结）/ PROJECT-BRIEF v1.3（冻结）/ 流水线设计规范 **v1.1**（含红队严重-1/2/3 最小补丁，含 GO_L0/GO_L1 分级）/ 红队评审 v1.0（4/3/3/3/4，fatal=0）。
>
> 关键假设：横州六蓝（2026-07）官方报告可得性是**未知量**——列入假设而非事实；若走查前报告未公开，最小验证案例按 fallback 规则降为下一个 ≥2026-07-19 后新风险。

---

## §5.1 4 视角评审

### 视角 1 — 工程应用方（能否 deploy 到 PolicySim 生产？）

**可以分阶段部署，首版必走 GO_L0**。阶段 3 资产映射 §3.3 + 阶段 4 代码复核给出"真实代码改动仅 1–2 个文件"的工程底线：`decision-report.service.ts` 单文件单函数加 `confidence_grade` + `step_degradation_reasons` 两个 JSON 字段（不触发 Report 实体 migration、6 份 spec 0 连锁更新）；可选新建 `synthesis-report.service.ts`（medium）或走轻量备选（low）。**端到端成本量级**：每步 schema 校验 ≤1 token；主步骤单次 100–500 token LLM 推理；8 步纸面走查单案例估 1.5k–3k token。**关键工程风险**：校验臂与 Multi-Judge 在 Policysim 仓内零实现——v1.1 §2.3 GO_L0/L1 分级正是为回应此风险，**首版生产必走 L0**，L1 须等校验臂 end-to-end 实跑后不可逆升级。

### 视角 2 — 项目方（课题五知识库建设？）

**部分服务，主要受益是"流程知识"维度而非"案例知识"维度**。课题五 4 deliverables（P2 Factor Ledger 校准闭环 / P1 RAG 注入 / P11 内心独白→角色一致性 / P8 市场校准）在评估包中均不被直接改动——开题 v1.3.1 §0–§5 与 PROJECT-BRIEF v1.3 的 P2/P1 通道仍按原节奏推进。评估包的真正服务点是把 idea §2"案例知识会缺席、流程知识不缺席"升格为可工程化的流程知识载体：步骤 2 `explicit_known_unknowns`（4 字段：claim / why_unknown / what_would_resolve / confidence_default）与步骤 8「已知-推断-无知清单」段落是流程知识的最小可沉淀单元；与课题三知识库 API 边界通过 `knowledgeBaseQuery.keywords` 复用 seed 字段、步骤 3 `analogies` / `physical_parameters` / `regulatory_constraints` 三个新数组 + `retrieval_coverage_gaps` 缺口报告实现"案例知识 vs 流程知识"分工——**流程知识落 8 步契约、案例知识落知识库 API**，评估包不发明新知识图谱、不重做 P1/P2 通道。

### 视角 3 — 论文 reviewer（「方法论协议」贡献能否支撑 short paper？）

**能支撑，venue 候选有 2 个高对口 + 1 个备选**。评估包贡献落点（阶段 1 §1.1–§1.3 落点陈述）已收窄为"应急决策方法论的流程固化 + 步骤级降级协议显式化"——这是一篇方法论短文（methodology / protocol short paper, 4–6 页）的形态而非实证长文。venue 候选（来自 `prompt-exports/stage5-recon-venues.md`）：(a) **ISCRAM 2026** AI for Crisis Management track（2025 已核验，2026 CFP 未发布——首要高对口）；(b) **JASSS short comm**（OA、滚动、2–4 月审稿、严格同行评审）——若允许期刊投稿，本 venue 最强候选；(c) 备选 AAAI-27 student abstract（~2026-08 截稿）。**PoliSim@CHI 2026/2027 workshop 按"未确认存在"对待**（侦察多次 WebSearch 未命中 CHI 2025 任何 PoliSim 工作坊列表），不作为选项 2 首选——评估包 §5.4 选项 2 走 ISCRAM/JASSS 双轨而非 PoliSim@CHI。novelty 收窄纪律（开题 v1.3.1 §2.5 R1-N1 与阶段 1 §1.1–§1.3 三重限定）保证 short paper 不滑入 AFlow/ADAS/EvoAgent 的 workflow 进化红海。

### 视角 4 — 学术价值（5 年后 durable identity 是什么？）

**durable identity = "SOP 范式 + LLM 步骤级降级协议 + 已知-推断-无知清单三档"的三者耦合点**。阶段 1 §1.1–§1.3 三条先验（ROC 2002 + Avizienis 2004 分布式系统降级 / Lichtenstein-Fischhoff-Phillips 1982 + Morgan-Henrion 1990 决策科学 calibration / Heuer 1999 + Rumsfeld 2002 情报分析已知-无知）各自沉淀 20–40 年但**耦合进 8 步 Agent 流水线显式契约**这一点在文献中未占位——这是 5 年后仍可能被人引的部分（区别于某个具体 LLM 工具或某个具体应急场景的工程实现）。**两个次级 identity** 也值得标注：v1.1 §2.3 的 GO_L0/GO_L1 双级 hard checkpoint 是首个把"校验臂未实现"显式分级为评审提示项的工程协议（vs 此前只有 1 级全开/全关）；v1.1 §2.1 步骤 6 的 `arms_executed: bool` 三态消解了空集 vacuous truth 误判，可被其他 LLM 决策流水线参考。**风险**：durable identity 取决于两条承重论据能否核验——阶段 1 §1.3 先验 2 的 Cooke method + Morgan-Henrion 1990 现行版本与 §1.2 末段 IMO 决策书的定性（人类事后填表）若核验失败，durable identity 需退为"启发性参照"而非"承重论据"（详见 §5.6 严重-5/6）。

---

## §5.2 12+ Path 分类（A / B / C / D 强制四分类全填实）

| 分类 | 问题 | 本项目语境下的具体内容 | ROI 判断 |
|---|---|---|---|
| **A. Fix existing data**（评估包本身修订） | 6 严重问题中未被打补丁覆盖的 | **[严重-5]** Cooke method + Morgan-Henrion 1990 承重论据联网核验（1–2 人日）——HIGH/MEDIUM/LOW/INSUFFICIENT 4 档与 data/model/expert 三档映射的承重依据；**[严重-6]** IMO MSC.1/Circ.1568 / A.1075(28) 决议现行版本查 imo.org IMODOCS（0.5 人日）——§1.2 落点收尾论据；**[一般-1]** §2.3 hard checkpoint 第 1 条与 §2.1 步骤 8 violation 第 1 条呈报优先级表（0.25 人日）；**[一般-4]** §3.3 备选段 `unknown` → `ignored` 统一命名（0.1 人日） | **高 ROI**（约 2–3 人日，闭合 4 条评估包内部缺口；其中 [严重-5] 是 GO 前置条件） |
| **B. New paper with existing data**（用评估包写 short paper） | 评估包能否直接支撑方法论短文 | **ISCRAM 2026 AI for Crisis track**（首推，需 4–6 页 methodology 改写 + §1.3 承重论据核验）；**JASSS short comm**（备选，若允许期刊路径则更对口，2–4 月审稿周期）；**AAAI-27 student abstract**（保底，~2026-08 截稿）——三选一并附"评估包 v1.1 → 投稿稿 v0.1"映射表 | **中-高 ROI**（4–6 人日改写 + 1–2 人日核验；可与 A 并行） |
| **C. Re-run**（重做某些探索） | 阶段 1 摘要级证据是否需补全文级精读 | **AFlow / ADAS / EvoAgent** 三篇 arXiv §1 + §5 Related Work 全文精读（2 人日偏紧，1 人日完成度若 <50% 则 Biomni 已降为摘要级，AFlow 优先 ADAS 次之）——为 §1.1 四维对比表每行加核验状态徽章（[摘要级]/[全文级]，回应 [一般-2]）；**EvoAgent 标题歧义**（arXiv 2406.14228 v1 vs v2 复核 0.25 人日） | **中 ROI**（2.25 人日；不阻塞 GO 路径但提升 novelty 论证强度） |
| **D. Restart**（换思路） | 是否放弃固定 8 步改 hybrid 或动态编排 | **Hybrid 按场景族路由**（4 族：工业事故 / 自然灾害 / 公共卫生 / 城市生命线——阶段 1 §1.2 落点已确认的分类；族内仍固定 8 步；外层族路由决策本身是新增不透明点，与"AI 只动嘴"硬约束张力，v1.1 §2.4 论证表已说明 hybrid 不作为首推）；**完全动态**（直接落 AFlow/ADAS 红海，novelty 趋零）——两条都不推荐重启 | **极低 ROI**（novelty 价值 < §1.1 落点论证所得；与开题 §2.3c 区分已被 v1.1 §2.4 表格锁定） |

**推荐**：A + B 并行（A 闭合评估包内部缺口、B 把评估包升格为投稿稿）；C 选 1 篇 AFlow 全文精读 + EvoAgent 标题复核即可（不补全三篇）；D 不推荐。

---

## §5.3 Gate 4 评分（7 项）

| 优先级 | 检查项 | 标记 | 一句证据 |
|---|---|---|---|
| 🔴 P0-1 | 评估包文档完整性 | ✅ | 阶段 1/2/3/4 四份均达 done-when（2958/5k 内/2500 内/172 行 ≤规定字数；8 步契约三件套齐全；8×6 矩阵 48 格填实） |
| 🔴 P0-2 | 评估包可读性 | ✅ | 8 步表非专业读者可复述（idea §1 原表 + v1.1 §2.1 8 个 YAML 契约字段名直接复用 seed）；降级 DAG 1 页可画 |
| 🔴 P0-3 | 红队评审通过 | ✅ | **4 / 3 / 3 / 3 / 4**，fatal = 0；6 严重 + 4 一般 + 2 瑕疵，严重-1/2/3 已 v1.1 闭环 |
| 🟡 P1-1 | 方法论一致性 | ✅ | v1.1 响应严重-1/2/3 后与开题 v1.3.1 §5.3/§5.4 H4 + §16.1 hard checkpoint + AutoResearch 协议不矛盾；Q3/Q4 schema 字段 5/8 步直接复用 |
| 🟡 P1-2 | 诚实边界 | 🟡 | idea §5 五条均得对策（§2.4 编排取舍表回应 1；§2.3 错误传播回应 2；§2.2 IRREVERSIBILITY + 终简报"流程性建议"措辞回应 3；§1.1–§1.3 落点收窄回应 4；§2.1 步骤 3 + §3.2 步骤 3 检索缺口回应 5）；但 [严重-5/6] 两条承重论据未核验（见 §5.6） |
| 🟢 P2-1 | 写作清晰度 | ✅ | 三份文档均含"修订记录"附录 + 限制声明 + 评估包内引用互链（adjacent ↔ design ↔ asset-mapping ↔ redteam） |
| 🟢 P2-2 | 资产接口清晰度 | ✅ | asset-mapping §3.1 矩阵 11 ✅ / 3 🟡 / 33 🟠 / 1 ❌ 计数自洽 + §3.3 4 项改造档位与 stage4-code-audit 复核档位完全一致（0 上调 0 下调） |

**P0 三项全 ✅**——按 §16.5 规则"红队 5 维均 ≥3 + 0 fatal"通过；P1-2 一项 🟡（待 §5.6 严重-5/6 处置闭合后转 ✅）；P2 两项 ✅。

---

## §5.4 三选项终裁

### 选项 1 — GO + hard checkpoint（推荐）

- **触发条件**：评估包 fatal = 0 + 6 严重问题已 v1.1 补丁闭环（[严重-1/2/4] 已闭，[严重-3] 操作化待 8 步 Agent 实施时细化，[严重-5] 走查前联网核验） + §5.5 最小验证走查通过 GO_L0 单一布尔。
- **Fallback**：`insufficient_step_count ≥ 4` 或振荡检测触发 → 终简报 grade 强制 INSUFFICIENT + 决策简报追加"建议转 fallback paper"（v1.1 §2.3.4）→ 评估包本体不废弃，转入选项 2 路径。
- **时间预算**：**2–3 人日**（§5.5 纸面走 8 步 + 1 案例对照；横州六蓝若官方报告不可得则换下一案例，估时不增）。
- **拒选理由（本选项不选时的代价）**：(a) 跳过首次"未知风险纸面走查"机会，novelty 论证永远停在协议层；(b) 校验臂零实现下的契约闭合性只能在 GO_L0 下被走查验证（v1.1 §2.3 L0/L1 分级正是为 GO_L0 走查而设），不走查则该分级无实证；(c) 8 步 YAML 契约在评估包阶段未走过真实 schema 实例化，6 严重问题中 [严重-3] 的 R 动作操作化只能在 Agent 实施时细化，纸面走查可暴露更多操作化缺口。

### 选项 2 — 降级为方法论 short paper

- **触发条件**：选项 1 走查中 `insufficient_step_count ≥ 4` 或硬约束第 3 项（校验臂全空 arms_executed=false）在 L0 豁免代价三件外仍无法收敛；或人方判断"工程时机不成熟但方法论已自洽"。
- **Fallback**：ISCRAM 2026/JASSS/AAAI-27 三 venue 投递均被拒 → 选项 3 NO-GO（本项目方向关闭）。
- **时间预算**：**4–6 人日**（评估包改写为 4–6 页方法论稿 + §1.3 承重论据联网核验 1–2 人日 + 投稿格式适配 0.5 人日）。
- **拒选理由（本选项不选时的代价）**：(a) 放弃评估包已就绪的工程证据（48 格矩阵 + 4 项改造 + code-audit 复核），把它们压缩为协议论文读者不可复现；(b) 跳过来自"校验臂零实现 → GO_L0 走查"这条诚实路径的独特贡献，方法论短文读者看不到"在工程未实跑约束下如何分级"的工程智慧；(c) 走查机会成本：6 个月后横州六蓝若成为已发表案例，本评估包的"首例纸面走查"窗口作废。

### 选项 3 — NO-GO（§16.6 禁选）

- **触发条件**：**不应触发**——评估包 fatal = 0 + 红队 4/3/3/3/4 不支持 NO-GO 评分 + 6 严重问题已 v1.1 闭环；NO-GO 须评估包 ≤2 维评分才合规。
- **Fallback**：无（项目方向关闭）。
- **时间预算**：N/A。
- **拒选理由**：§16.6 明确"不要选 3——它就是问题"；且本评估包 fatal=0 不是边界情况，选 3 等于把已完成工作归零，触发 §16.7「doomed loop」。

### **建议选项 1 GO，理由：评估包 fatal=0 + 6 严重问题已 v1.1 闭环 + 唯一前置风险（横州官方报告可得性）可通过 hard checkpoint 转选项 2 降级吸收，不构成阻塞性未知量。**

---

## §5.5 若 GO 的最小验证设计

**案例**：横州六蓝（2026-07，晚于底座训练截止）作为首选；**关键假设：横州六蓝官方报告可得性未知**，若走查前未公开则降级为下一个 ≥2026-07-19 后新风险（不含 7/19 当日及之前已公开案例，避免训练污染）——此 fallback 不增时间预算，因纸面走查不依赖报告字段级精确值。

**流程**：8 步纸面走查（**不实跑 PolicySim**）。v1.1 §2.1 八份 YAML 契约即八张表，依次填入：(1) Intake → 通报文本 + `source_tier` 自评 → `scenario_spec`；(2) Decomposition → `sub_problems` + `explicit_known_unknowns` 4 字段；(3) Retrieval → 检索 OSINT dossier（手填）→ `analogies` / `physical_parameters` / `regulatory_constraints` + `retrieval_coverage_gaps`；(4) Generation → `candidate_strategies` 含 `option_combination` + `risk_hint`；(5) Simulation → `factor_ledger_entries` + `trajectory_dtw_aggregate` + `protocol_failures`；(6) Validation → `arms_executed: bool` 三态之一 + `validation_arms`（**校验臂未实现时 arms_executed=false、validation_arms=[]**，v1.1 §2.1 步骤 6 violation 状态 a）；(7) Judge → `calibration_check` 四件套（kendall_tau 无法计算时按 INSUFFICIENT 走 v1.1 §2.1 步骤 7 violation 第 1 条）；(8) Synthesis → `decision_brief_markdown` 七段 + `worst_upstream_grade` + `insufficient_step_count`。

**度量（三件）**：
1. **每步 confidence_grade** 4 档分布（HIGH/MEDIUM/LOW/INSUFFICIENT 计数）+ 降级次数（v1.1 §2.2 DAG 形式化 `ceil_upstream_grade` 传播规则的实际触发次数）；
2. **`insufficient_step_count`** 终汇点（v1.1 §2.1 步骤 8 output_schema）；
3. **与"单体协商"版本逐段对比**——以开题 v1.3.1 描述的"八角色三轮协商"作为对照组，由人用 v1.1 §2.2 终简报 markdown 模板"已知-推断-无知清单"段落判定：8 步版本是否在"诚实呈现无知"维度上更准确（v1.1 §2.2 IRREVERSIBILITY 约束防止"步骤内自圆其说"）。

**判定（GO_L0 单级）**：v1.1 §2.3 hard checkpoint 在校验臂未实现下走 GO_L0 单一布尔（校验臂零实现场景的 L1→L0 降级已闭合 [严重-2]）：

```
GO_L0 = (steps_completed == 8)
  AND (count(grade ∈ {HIGH, MEDIUM}) >= 5)        # L1 与 L0 同
  AND (NOT any(validation_arms.red_flag))         # L0 下 vacuous true, 有意豁免
  AND (insufficient_step_count <= 4)              # L0 比 L1 多容忍 1 步
```

**判定规则**：
- GO_L0 通过 → 走查成立；评估包机制在工程未实跑约束下得到首次实证；可选入选项 1 继续（GO_L0→GO_L1 升级条件：校验臂协议实现 + `kendall_tau_n_pairs ≥ 10` 稳定计算 + 阶段 5 终裁 memo 重审）。
- GO_L0 不通过（任一合取项失败）→ 按 v1.1 §2.3 呈报规则标失败原因（流程不完整 / 证据强度不足 / 降级过度）；升级阶梯 = (a) 修改后重跑纸面走查、(b) 接受降级结果转选项 2 短文、(c) NO-GO（仅当返工一次仍失败）。
- 振荡检测触发（任一 R/S 动作 ≥ 2 次且累计 ≥ 2 步 OR `insufficient_step_count ≥ 4`）→ 终简报 grade 强制 INSUFFICIENT + 追加 fallback paper 建议 → 转选项 2。

---

## §5.6 严重问题处置表

| 编号 | 等级 | 问题（一句话） | 处置 | 一句理由 |
|---|---|---|---|---|
| [严重-1] | 严重 | §2.3 hard checkpoint `NOT any(red_flag)` 与 §2.1 步骤 6 violation 对 `validation_arms 全空` 给相反判定（空集 vacuous truth） | **已补丁 v1.1** | v1.1 §2.1 步骤 6 加 `arms_executed: bool` 三态 + §2.3 L1 第 3 合取项改写为 `arms_executed == true AND NOT any(red_flag)`，空 arms 不再被误读为无标红 |
| [严重-2] | 严重 | 校验臂零实现下 cascading INSUFFICIENT 致 `5/8 ≥ MEDIUM` 与 `insufficient_step_count ≤ 3` 结构性同时失守 | **转为 GO 前置条件** | v1.1 §2.3 引入 GO_L0/GO_L1 分级；L0 豁免第 3 合取项 + 容忍多 1 步 INSUFFICIENT + 豁免代价三件（措辞降级 / 显著标注 / insufficient_step_count ≤ 4）——闭合性悬空被走查吸收而非在评估包阶段强行闭合 |
| [严重-3] | 严重 | §2.3.2 步骤 4/5 R 动作词"放宽召回""工程夹逼"无操作化定义不可证伪 | **接受并记录** | v1.1 §2.1 步骤 5 已加 fallback_used 聚合规则；R 动作词操作化需 8 步 Agent 实施时与 schema 字段级对齐（步骤 4 R 配 keywords 扩展规则、步骤 5 R 配 protocol_failures 触发条件表），评估包不强写以避免越界定义 Agent 内部策略 |
| [严重-4] | 严重 | `summary.fallbackUsed`（bool）→ `confidence_grade`（4 档）聚合规则未在 v1.0 §2.1 明文 | **已补丁 v1.1** | v1.1 §2.1 步骤 5 顶部注释块加 `fallback_used` 派生值定义 + 聚合映射（true → grade ≤ MEDIUM + degradation_reasons 必含 `model_fallback_used`）+ 语义声明"模型切换 ≠ 证据不足"——不增实体字段 |
| [严重-5] | 严重 | §1.3 先验 2 的 Cooke method + Morgan-Henrion 1990 承重论据核验状态 `[未核验-需复核]`，但被用于 4 档与 data/model/expert 三档映射的承重论据 | **转为 GO 前置条件** | 走查前联网核验 Cooke method 现行版本与 Morgan-Henrion 1990 第 2 版；未核验则按开题 v1.3.1 §2.4 对 Chen 2026 的处置退为"启发性参照"，HIGH ≈ data-confirmed 映射退为"建议性参照"而非"承重论据" |
| [严重-6] | 严重 | §1.2 末段断言 IMO 决策书目标函数与本想法不重合，依赖未核验的 IMO 决议定性 | **接受并记录** | §1.2 已诚实标注 `[未核验-需复核]`；最坏情形 = 5 个流程化文献耦合点论证失去 1/5 支撑，剩余 4 篇（NIST IR 7601 / FEMA CPG 101 / FAA 7110.65 Ch.10 / NUREG-0654+CR-7002）均已核验，主要 novel 论证不依赖单点 IMO |

**处置后总览**：[严重-1/4] 已 v1.1 闭环（2 条），[严重-2/5] 转 GO 前置条件（2 条，走查前闭合），[严重-3/6] 接受并记录（2 条，不阻塞）。6 条均不阻塞选项 1 GO 的 hard checkpoint 触发。

---

*文档版本：v1.0（2026-07-19，pair 主笔生成；输入为阶段 1–4 评估包 + 阶段 5 venue 侦察；引用已冻结开题 v1.3.1 与 PROJECT-BRIEF v1.3 但不修改；本 memo 本身是评估包第 5 份交付物，不替用户决策，仅给三选项建议）。*
