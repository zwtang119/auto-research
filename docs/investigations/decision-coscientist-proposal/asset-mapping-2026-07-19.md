# 决策流水线资产映射——Policysim-v0.2 → 8 步流水线复用与缺口（2026-07-19）

> 本文档为 2026-07-19 评估包组成部分（阶段 3），**引用已冻结的开题报告 v1.3.1**（`proposal-decision-coscientist.md`）与项目简报 v1.3（`PROJECT-BRIEF.md`）**但不修改它们**。
>
> **事实基础**：`prompt-exports/stage3-recon-code-probe.md`（八角色实为 6 角色 / 校验臂与 Multi-Judge 在 Policysim 仓内零实现）+ `pipeline-design-spec-2026-07-19.md` §2.1–§2.4 + 字段对齐 `prompt-exports/stage2-recon-schema-crosswalk.md`。

**先行诚实声明**（防下游误读）：

- **「八角色」是设计目标非现状**——seed 当前为 6 角色（commander + 消防 / 工艺 / 医疗 / 环保 / 公安），扩 8 仅需 seed 数据调整、代码无侵入。相关格子以 🟡 标注。
- **校验臂 + Multi-Judge 在 Policysim 仓内零实现**——Q3 协议已就绪（arm_id / red_flag / reference_trajectory / sim_trajectory_dtw 命名稳定），Multi-Judge 仅 `dev/backend/scripts/ab-judge.ts` 离线实验脚本。步骤 6 / 步骤 7 涉及列以 ❌ / 🟠 标注。
- OSINT dossier 检索接口属 OSINT 子模块复用面（步骤 3 部分新建基础），未单列于 §3.1 6 列内，详见 §3.2 步骤 3 条目。

---

## §3.1 映射矩阵（8 步 × 6 类资产 + 1 列对应关系）

符号：✅ 直接复用 / 🟡 需小改（说明改什么）/ 🟠 需大改或随步骤新建（说明新建什么）/ ❌ 缺口（实现真空）。

| 步骤 | 八角色引擎 | 六维指标 | Factor Ledger | 校验臂 | §16 方法论 | 与开题 v1.3.1 M1–M5 对应 |
|---|---|---|---|---|---|---|
| 1 Intake | 🟠 步骤新建，无既有引擎面 | 🟠 步骤新建，无指标消费 | 🟠 步骤新建（新建 `scenario_spec` wrapper 与 `source_tier` 自评） | 🟠 步骤新建 | 🟠 步骤新建（§16.1 仅 hard checkpoint 间接相关） | 🟠 新增编排层 M0 前置，不在 M1–M5 序列 |
| 2 Decomposition | 🟠 步骤新建 | 🟠 步骤新建 | 🟠 步骤新建（KU 字段 `ku_id` 与 Factor Ledger `counter_signal` / `reason_for_inconclusive` 语义分家——侦察冲突 #2） | 🟠 步骤新建 | 🟠 步骤新建 | 🟠 新增编排层 |
| 3 Retrieval | 🟠 步骤新建 | 🟠 步骤新建 | 🟠 步骤新建 | 🟠 步骤新建 | 🟠 步骤新建 | 🟠 新增检索层 |
| 4 Generation | ✅ 直接复用 `emergency-scenario.handler` 三轮协商；"8 角色"扩位仅改 seed（成本 low） | 🟠 步骤不输出指标，仅消费 `interventionDimensions` | 🟡 复用 seed `interventionDimensions` 作变异空间白名单 | 🟠 步骤不直接消费校验臂 | 🟠 步骤无 §16 编排直接复用面 | ✅ = M1 |
| 5 Simulation | ✅ 复用 3-round handler（R1→R2→R3，R3 提指标） | ✅ 复用 `metricProfile.aiField` 命名（20 枚举覆盖 6 维语义） | ✅ 复用 `factor_ledger_entry` 19 核心字段（侦察 §2.1） | 🟡 不消费校验臂但需为校验臂产出 `protocol_failures` | ✅ §16.1 hard checkpoint 三合取可套用 | ✅ = M2 + M3 部分（evolution 步骤未实现） |
| 6 Validation | 🟠 校验臂独立逻辑，不走八角色 | 🟠 校验臂不输出 aiField | 🟠 校验臂不写 FL（仅调用后填 `settlement_rule`） | **❌ 工程实现 0**（GB 50151 / NUREG-CR-7002 / SFPE 在 `dev/backend` 全仓 grep 0 命中）；协议已就绪（Q3 三档 arm_id 命名稳定） | 🟡 §16.1 模板"red_flag → 标 INSUFFICIENT"可借用 | ✅ = 开题 §5.3 方法论提及（**100% 实现缺口**） |
| 7 Judge | 🟠 步骤不调用八角色 | 🟠 步骤消费 metricProfile 比较，不产出新 aiField | ✅ 复用 `factor_updates.{supported/rejected/inconclusive}` + `adjudication_meta` + `adjudicator` 四件 | **🟠 任一 arm red_flag → 本步上限 MEDIUM**（开题 §3 H4）；multi-judge panel / adjudicator 生产模块 0 实现（仅 ab-judge.ts 离线脚本） | 🟠 H4 四件套执行仅在 ab-judge.ts 跑，未入流水线 | ✅ = M4 + H4（**生产实现 0**） |
| 8 Synthesis | 🟠 步骤不调用八角色 | 🟠 步骤聚合引用，不产出新指标 | 🟠 步骤仅聚合 FL 引用 | 🟠 步骤聚合引用校验臂摘要 | ✅ §16 4 视角 + 12+ Path + Gate 4 + 3 选项骨架可复用为终简报模板 | 🟠 新增尾汇 M6 |

**矩阵计数**：✅ 11 / 🟡 3 / 🟠 33 / ❌ 1 = 48 格。其中 18 个 🟠（步骤 1 / 2 / 3 各 6 格）集中于"新建步骤的全行无既有资产复用面"——这是新建步骤的必然结果，非既有资产流失信号；剩余 15 个 🟠 反映既有步骤对未消费资产列。**改造真实触点见 §3.3**。

---

## §3.2 缺口清单（4 个完全 / 部分新建步骤）

### 步骤 1 — Intake Agent（**完全新建**）

- **input**：`report_text`（非结构化通报）+ `source_tier ∈ {official, media, self_reported}`；永远接受——Intake 不在入口处硬判。
- **output**：`scenario_spec`（9 字段完全复用 seed：`id` / `disasterType` / `eventChain` / `defaultResources` / `agentRoles` / `interventionDimensions` / `knowledgeBaseQuery` / `metricProfile` / `description`）+ `confidence_grade`（4 档离散）+ `step_degradation_reasons`。
- **契约违反**：`report_text` 缺失 → 标 INSUFFICIENT 继续（入口无上游，不退回）。
- **需新建**：Intake Agent 自身 + `source_tier` 自评逻辑 + `scenario_spec` wrapper 包装层（建议 nested-import 现有 seed 字段，避免发明 wrapper struct——侦察 §1.5）。**不改 Policysim 任何代码**。

### 步骤 2 — Decomposition Agent（**完全新建**）

- **input**：`scenario_spec` + 上游 `confidence_grade`（决定本步上限）。
- **output**：`sub_problems[{id, description, decision_relevance ∈ {high, medium, low}}]` + `explicit_known_unknowns[{ku_id, claim, why_unknown, what_would_resolve, confidence_default}]` + `confidence_grade` + `step_degradation_reasons`。
- **契约违反**：上游 INSUFFICIENT → 跳过本步转发；`sub_problems` 为空 → 标 INSUFFICIENT 继续。
- **需新建**：Decomposition Agent + KU 显式化协议（与 Factor Ledger `counter_signal` / `reason_for_inconclusive` 语义分家，3 者命名不重叠——侦察冲突 #2）。**不改 Policysim 任何代码**。

### 步骤 3 — Retrieval Agent（**部分新建**）

- **input**：`sub_problems` + `knowledgeBaseQuery.keywords`（seed 已存）+ `explicit_known_unknowns`。
- **output**：`analogies[]` + `physical_parameters[]` + `regulatory_constraints[]` + `decision_actions[]` + `retrieval_coverage_gaps[]` + `confidence_grade`。`decision_actions` 元素 schema 与 `pipeline-design-spec-2026-07-19.md` §2.1 步骤 3 契约对齐——每条含 `action_id` / `actor` / `action_type` / `action_timestamp` / `source_url` / `source_tier` / `origin` / `summary` / `evidence_ref`,`origin` 枚举扩 `ifrc_go_field_report` / `nws_cap_alert` / `ntsb_carol` / `csb_final_report` 等（F2 行动锚源,见下条）。
- **行动锚源（F2, 2026-07-19 实测）**:
  - mem.gov.cn 国家防总响应通告:`/xw/yjyw/`（123 页归档 2018-01 起）+ `/xw/yjglbgzdt/`（88 页 2020-07 起）,日时级时间戳静态 HTML 可爬;**2018 断档**为硬约束。
  - mem.gov.cn 调查报告栏目 `/gk/sgcc/tbzdsgdcbg/`:2003–2026 逐年归档,全文级自 2011 甬温线起。
  - 省厅:广东 `yjgl.gd.gov.cn`（实测 2020–2025）、福建 `yjt.fujian.gov.cn`（2019 起）、浙江 `yjt.zj.gov.cn`（境内直连可爬,境外 IP 限——旧「走媒体源」结论作废）。
  - JMA 防灾信息 XML（Digital Typhoon）:2012–2026 台风报文/警报发布时间线,CC BY 4.0。
  - IFRC GO API（`goadmin.ifrc.org/api/v2/`）:免 key,`field-report` 5,107 条含 `actions_taken`（主体×行动编码）;中国 69 事件多为 GDACS 自动同步条目。
  - NWS `api.weather.gov`:CAP 预警（含 Evacuation Immediate）,免 key（需 UA）。
  - NTSB CAROL（CSV/JSON）+ CSB 全本 PDF（BP Texas City,与古雷同灾种,公有领域,`https://www.csb.gov/assets/1/20/csbfinalreportbp.pdf`）。
  - ReliefWeb API:**2025-11 起需预审批 appname**（未审批返回 410）——不再作为默认落点。
  - **采集端硬约束（F7）**:境内直连,勿挂 VPN（政务站限境外 IP）。
- **契约违反**:三个数组全空 → 标 INSUFFICIENT 继续 + `retrieval_coverage_gaps` 必填"检索全覆盖缺口"（idea §1 第 3 行原话）。`decision_actions` 全空时按 F2 行动锚源逐条核验是否触及 `retrieval_coverage_gaps` 必填语义。
- **需新建**：Retrieval Agent 主体编排；**部分复用** Policysim OSINT 检索接口（`DossierRepositoryService.read(slug)` 已实现 ENOENT→null 降级形态——探查 §4.1）；降级语义在 Agent 编排层处理（`read()` 返 null → 标 LOW + `step_degradation_reasons=["dossier_not_found: ${slug}"]`），**不下沉到仓储 service**。

### 步骤 8 — Synthesis Agent（**完全新建**）

- **input**：八份 step outputs 累积。
- **output**：`decision_brief_markdown`（七段骨架：背景 / 候选 / 校验臂判定 / 评分汇总 / **已知-推断-无知清单** / 置信度摘要 / 人拍板位）+ `worst_upstream_grade` + `insufficient_step_count` + 合并 `step_degradation_reasons`。
- **契约违反**：中间 output 缺失 → 标 INSUFFICIENT 继续并在简报注明"流水线不完整"；`insufficient_step_count ≥ 4` → grade 强制 INSUFFICIENT + 触发 §16 fallback paper 流转。
- **需新建**：Synthesis Agent 主体 + 终简报渲染；已知-推断-无知渲染落到**新建** `report/services/synthesis-report.service.ts`（cost: medium）或**轻量附加**到 `report.service.ts` degraded 路径追加 `ignorance_triple` 字段（cost: low）。

---

## §3.3 最小工程改造说明（4 项）

| # | 改造项 | 改什么 | 不改什么 | 成本档位（探查报告 §8） |
|---|---|---|---|---|
| **5** | decision-report 字段新增 | `monte-carlo/services/decision-report.service.ts` `buildReportPayload()`（line 195–219）新增 `confidence_grade: enum[HIGH/MEDIUM/LOW/INSUFFICIENT]` 与 `step_degradation_reasons: list[str]`（HIGH 时空数组）；`factor.confidence` 3 档→4 档显式映射在 `buildFactorLedger()` 出口 | Report 实体 schema / `ReportService.generate()` 主体 / 数据库 migration / 前端绑定（JSON 字段已能容纳） | **low** |
| **6** | 校验臂降级传导 | **描述级**：落到 §2.1 步骤 6 YAML 契约——任一 arm `red_flag=true` → 步骤 6 `confidence_grade ≤ LOW`；对应 metric 的 `step_degradation_reasons` 必填；步骤 7 看到 `calibration_check.error_rate` 时本步上限 `MEDIUM`（开题 §3 H4） | **不在 Policysim 仓内新增 validation_arms 模块**（Q3 协议未变）；不实现 GB 50151 / NUREG-CR-7002 / SFPE 工程代码（Q3 §6 + 开题 §5.3 已声明覆盖缺口） | **low**（纯契约层） |
| **7** | judge 失效 INSUFFICIENT 机制 | **描述级**：落到 §2.1 步骤 7 YAML 契约——触发 INSUFFICIENT 4 条件显式声明（H4 阈值 + Q4 `inconclusive_rate_policy` + 校验臂传导 + judge LLM 本身失败）；`step_degradation_reasons=["judge_llm_unavailable"]` 等触发模板 | 不复用 `ab-judge.ts` 的 `judgePair` 到生产流水线（实验脚本，依赖 Paratera provider，与多模型 panel 协议不直接对接）；不在 `decision-report.service.ts` 加 judge 字段 | **low**（纯契约层） |
| **8** | 终简报渲染 | 推荐落点:**新建** `dev/backend/src/modules/report/services/synthesis-report.service.ts`（约 150–250 行）+ `report.module.ts` 注册;专用服务 8 步 Synthesis Agent 输出,与现有 `report.service.ts` 平级 | 不改 `report.service.ts` 现有 CRUD/export 接口（避免回归）;不改 `pdf.service.ts`（Markdown 是 single source of truth）;不改 Report entity schema | **medium** |
| **9** | 宽类数据流扩展点（F1, 2026-07-19） | 新增宽类行动锚 `decision_actions` 流——**台风首选**:IBTrACS v04r01（`https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/`,免 key bulk,1842–至今,每周 3 更,引用 Knapp 2010/Gahtan 2024;HDX 镜像 CC BY-IGO）+ IBTrACS 内置 CMA 序列（替代原 `tcdata.typhoon.org.cn` WAF 拦脚本 468,2017 起登陆前 24h 加密 3h）+ 省级响应通告（决定时点,F2）+ EM-DAT（后果侧,行动字段已弃用）;**地震备选**:USGS FDSN（`https://earthquake.usgs.gov/fdsnws/event/1/`,免 key,PAGER 警级+ShakeMap）。**宽类用于强化 H3 旁证 N≥60**,不改 H1/H2 设计;与「横州六蓝零污染锚」并行,**不替换深案** | 不动 Policysim 任何代码;不替换深案 2 个;不复制 IBTrACS/CMA 数据到本地仓;不走境外 IP（F7） | **low**（数据流描述层,扩展 §2.1 步骤 3 `decision_actions` 契约枚举即可） |

**轻量降级备选**：步骤 8 若评审不允许新建 service，则在 `report.service.ts` `generateSimulationReportPayload()` degraded 路径中追加 `ignorance_triple: { known, inferred, unknown }` 字段 + Markdown 末尾追加一节——成本降为 **low**，但与 Simulation report 强耦合、未来 Stage 8 独立 Agent 时无法复用。

### 关键交叉点（结论性观察）

**真实代码改动仅 1–2 个文件**：
- **必须改**：步骤 5 → `decision-report.service.ts` 单文件 / 单函数改造（仅 payload 构造层）。
- **可选新建**：步骤 8 → `synthesis-report.service.ts`（cost: medium）或 `report.service.ts` 附加（同文件改动，cost: low）。
- **不动代码**：步骤 6 校验臂降级传导 + 步骤 7 judge INSUFFICIENT 机制**全部停留在 §2.1 YAML 契约层**；未来 Pipeline 实现在新建 Agent 编排层（Policysim 仓外）。
- **总触点 = 1–2 个文件**（决策报告 + 可选报告渲染服务），其余 3 项改造在契约层 + 未来 Agent 实现层（不在 Policysim 仓内）。

**4 项改造分属 4 个不同层**——决策报告 = 数据结构层、校验臂 = 契约层、judge = 契约层、终简报 = 服务层。这一分布说明该评估包的最大工程负担是**新建 Agent 主体代码**（Intake / Decomposition / Retrieval / Synthesis），而非改 Policysim 既有代码——回应 idea §5 第 1 条诚实边界：固定流水线的工程量主要在"每步独立 Agent"，而非"核心引擎改造"。这也意味着：阶段 4 红队评审维度 4（可行性）若聚焦"既有代码改造量"将得到偏乐观结论；若聚焦"新建 Agent 工作量"则需另列条目——本映射如实暴露了两个评估视角的差别。

---

## 附录 A 修订记录

- v1.0 / 2026-07-19 / Stage 3 pair 主笔生成
- 输入：`prompt-exports/stage3-recon-code-probe.md`（八角色现状 / 校验臂零实现 / multi-judge 零实现）+ `pipeline-design-spec-2026-07-19.md` §2.1–§2.4 + `prompt-exports/stage2-recon-schema-crosswalk.md` 字段对齐 + Oracle 计划 §3.1 File 3 / 阶段 3.1–3.3 + `idea-decision-pipeline-2026-07-19.md` §1 §5 + 开题 v1.3.1 §5.3 §5.4 H4 + Q3 §1–§6
- 待复核：阶段 4 红队评审维度 4（可行性）是否对 33 个 🟠 格子的"新建步骤必然结果"产生判定分歧；步骤 8 渲染落点决策（新建 vs 附加）的偏好来源人拍板
- 限制声明：本文不修改 `proposal-decision-coscientist.md` v1.3.1 / `PROJECT-BRIEF.md` v1.3，不动 Policysim-v0.2 任何代码
- v1.1 / 2026-07-19 / pair 主笔最小补丁（修订简报 Item 5）
- 修订依据:`revision-brief-2026-07-19.md` F1（宽类轨道）+ F2（决策行动锚源）+ F5（settleability 切割）+ F7（采集硬约束）。
- 修订范围（仅 3 处 + 本附录追加）：
  - §3.2 步骤 3 output 加 `decision_actions[]` 字段并 inline 指向 pipeline-design-spec §2.1 步骤 3 契约对齐;新增「行动锚源」子条目按 F2 列 mem.gov.cn / 省厅 / JMA / IFRC GO / NWS / NTSB / CSB + ReliefWeb appname 硬约束。
  - §3.2 步骤 3 契约违反行补「`decision_actions` 全空时按 F2 行动锚源逐条核验」一句;新增 F7 采集硬约束一条（境内直连,勿挂 VPN）。
  - §3.3 增登记项 #9「宽类数据流扩展点」（台风首选/地震备选,IBTrACS + CMA 序列 + 省级响应 + EM-DAT / USGS FDSN）,声明不替换深案、不动 H1/H2、不走境外 IP。
- 未改动:§1 preamble / §3.1 6 列映射 / §3.3 #5–#8 / §3.2 步骤 1/2/8 / 附录 A v1.0;保持字数预算与既有结论不变。
- 评审状态:与红队评审范围并列输入,未单独触发新一轮评审。
