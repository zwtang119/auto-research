# 决策流水线设计规范——8 步 Agent 流水线 I/O 契约、降级协议与编排论证

> 本文档为 2026-07-19 评估包组成部分，**引用已冻结的开题报告 v1.3.1**（`auto-research/docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md`）与项目简报 v1.3（`PROJECT-BRIEF.md`）**但不修改它们**。本文件对应评估包阶段 2 的 4 节产出——把 `idea-decision-pipeline-2026-07-19.md` 中的 8 步想法表升级为可执行协议。AutoResearch 协议定义引用 `auto-research/docs/autoresearch/orchestrator-prompt.md` + `auto-research/framework/watchdog/README.md` 已核验沉淀，不重新发明。
>
> **字段对齐来源**：阶段 2 engineer 侦察报告 `prompt-exports/stage2-recon-schema-crosswalk.md`（5 条冲突 ≤ 10；本文采用其全部改名建议——`downgrade_reasons` → `step_degradation_reasons`、`trace_alignment_score` → `trajectory_dtw_aggregate`、`calibration_check` 补齐为四件套含 `kendall_tau`）。
>
> **编排取舍论证**：阶段 1 三节贡献落点陈述见 `adjacent-work-positioning-2026-07-19.md` §1.1–§1.3——本文件 §2.4 一句话引用 §1.1 的落点（"固定步骤集 + 显式降级协议"组合在 5 邻居中未占位）。

---

## §2.1 I/O 契约 schema（8 步每步三件套）

每步契约 = (input_schema / output_schema / 契约违反处理)。八步共复用侦察报告 §5 表中的字段集；至少 5 步直接复用既有字段名（步骤 1 / 4 / 5 / 6 / 7），不发明新词。

**强制全局字段**：`confidence_grade ∈ {HIGH, MEDIUM, LOW, INSUFFICIENT}` 为每步 output 必填；`step_degradation_reasons: list[str]` 在 grade ∈ {MEDIUM, LOW, INSUFFICIENT} 时必填（grade=HIGH 时可省略）。

### 步骤 1 — Intake Agent

```yaml
input_schema:
  payload_type: unstructured_risk_report
  required_fields: [report_text, source_tier]   # source_tier ∈ {official, media, self_reported}
  accepted_when: |                  # 即使降级也接受——Intake 是流水线入口、永不拒绝
    true                              # 不在入口处硬判，给后续步骤留存降级机会

output_schema:                       # 完全复用 Policysim seed schema 9 字段（侦察 §1.2）
  scenario_spec:
    id: string                       # 必复用: from seed
    name: string                     # 必复用
    disasterType: string             # 必复用 (e.g. "chemical-explosion")
    description: string              # 必复用
    eventChain:                      # 必复用, EventChainNode[]
      - {id, name, type, children, probability}
    defaultResources:                # 必复用, {personnel, vehicles, equipment, timeLimitHours}
      {personnel: int, vehicles: int, equipment: {foam_tons?: int, ...}, timeLimitHours: int}
    agentRoles:                      # 必复用, EmergencyAgentRole[]
      - {role, name, expertise, decisionAuthority}
    interventionDimensions:          # 必复用
      - {id, label, type, options[], min?, max?, suggested?}
    knowledgeBaseQuery:              # 必复用, {scenarioId, disasterType, keywords[]}
      {scenarioId: string, disasterType: string, keywords: string[]}
    metricProfile:                   # 必复用, EmergencyMetricDefinition[]
      - {key, label, aiField, unit, higherIsBetter, description}
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]   # 必填, Intake 自评
  step_degradation_reasons: list[str]   # 条件必填, 例: source_tier=self_reported + 字段缺失

violation_handling:
  - condition: required_field_missing(report_text)
    action: 标 INSUFFICIENT 继续 (不退回——入口无上游)
  - condition: source_tier == self_reported
    action: 标 LOW 继续 + step_degradation_reasons 追加 "未官方核实"
```

### 步骤 2 — Decomposition Agent

```yaml
input_schema:
  source_step: step_1_intake
  payload:
    scenario_spec: required
    confidence_grade: required           # 上游 grade 决定本步上限
  required_fields: [scenario_spec.id, scenario_spec.disasterType, scenario_spec.eventChain]
  accepted_when: scenario_spec.confidence_grade != INSUFFICIENT
                        # 若上游 INSUFFICIENT：本步 grade 上限 ≤ LOW（详见 §2.2 降级 DAG）

output_schema:
  sub_problems:                          # 新建, 但与 decision/dto 接口对齐（侦察 §4 末注）
    - {id: string, description: string, decision_relevance: enum[high, medium, low]}
  explicit_known_unknowns:               # 新建, 字段严格遵从侦察 §4 冲突#2 建议
    - {ku_id: string,                    # 加 ku_id 用于与 factor_id 隔离
       claim: string,                    # KU=前瞻待证, ≠counter_signal (后验反证) ≠reason_for_inconclusive (裁定失败)
       why_unknown: string,
       what_would_resolve: string,
       confidence_default: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]}
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]   # 必填
  step_degradation_reasons: list[str]   # 条件必填

violation_handling:
  - condition: input.accepted_when == false (上游 INSUFFICIENT)
    action: 跳过此步, 直接转发 step_1.scenario_spec 给 step_3, 标 step_3 input 携带 sub_problems=[] + grade ≤ LOW
  - condition: sub_problems 为空
    action: 标 INSUFFICIENT 继续 + 在降级原因中说明 "分解失败"
```

### 步骤 3 — Retrieval Agent

```yaml
input_schema:
  source_step: step_2_decomposition
  payload:
    sub_problems: required               # 来自 step 2
    knowledgeBaseQuery: required         # 复用 seed 字段 (来自 step_1.scenario_spec)
    explicit_known_unknowns: required
  required_fields: [knowledgeBaseQuery.keywords]
  accepted_when: sub_problems 非空 OR 上游 grade != INSUFFICIENT

output_schema:
  analogies:                             # 新建, 沿用 OSINT dossier 检索接口 (Policysim dev/backend/docs/osint/dossiers)
    - {case_id: string, similarity: float, source_tier: string, summary: string}
  physical_parameters:                   # 新建
    - {parameter: string, value: any, basis: string, source_tier: string}
  regulatory_constraints:                # 新建
    - {regulation: string, clause: string, applies_when: string}
  decision_actions:                      # 新建 (F2 行动锚, 2026-07-19 实测源; 与 asset-mapping §3.2 步骤 3 对齐)
    - {action_id: string,
       actor: string,                     # 行动主体 (e.g. 国家防总/省厅/IFRC 现场协调员)
       action_type: string,               # 行动类型编码 (e.g. 启动 II 级响应/疏散/救援调度)
       action_timestamp: string,          # ISO-8601
       source_url: string,                # 必填, F2 已核验源 URL
       source_tier: enum[official, media, self_reported],
       origin: enum[mem_gov_announcement, mem_gov_investigation_report, provincial_gd, provincial_fj, provincial_zj, jma_digital_typhoon, ifrc_go_field_report, nws_cap_alert, ntsb_carol, csb_final_report, em_dat_consequence],  # F2 行动锚源枚举 (扩展自 §2.1 步骤 5 factor_ledger origin)
       summary: string,
       evidence_ref: string}              # 引用 analogies/physical_parameters/regulatory_constraints 之一
  retrieval_coverage_gaps: list[str]    # 必填, 即使检索为空也写明覆盖缺口 (idea §1 第 3 行原话)
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]
  step_degradation_reasons: list[str]

violation_handling:
  - condition: analogies AND physical_parameters AND regulatory_constraints 全部空
    action: 标 INSUFFICIENT 继续 + retrieval_coverage_gaps 必填 "检索全覆盖缺口"（核心降级点：检索为空时返回"部分类比 + 覆盖缺口报告"——idea §1 原话）
```

### 步骤 4 — Generation Agent（= 开题 M1）

```yaml
input_schema:
  source_step: step_3_retrieval
  payload:
    scenario_spec.eventChain: required   # 复用 seed 字段
    interventionDimensions: required     # 复用 seed 字段, 生成变异的白名单空间
    sub_problems: required
    retrieval_coverage_gaps: required
  required_fields: [interventionDimensions.options]
  accepted_when: interventionDimensions 非空

output_schema:
  candidate_strategies:                  # 新建, 沿用开题 §1.3 generation 语义
    - {strategy_id: string,
       option_combination: {dim_id: option_id, ...},   # 复用 interventionDimensions.id 作为 dim_id
       risk_hint: string,
       generated_by: enum[seed_template, llm_compose]}
  ignore_recommendation_rationale: string   # 生成策略被拒的原由
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]
  step_degradation_reasons: list[str]

violation_handling:
  - condition: candidate_strategies 空
    action: 退回上步 (step_3), 提示放宽 retrieval 召回, 上限 ≤ 2 次 (OS §2.3 振荡检测)
```

### 步骤 5 — Simulation Agent（= PolicySim + M2）

```yaml
input_schema:
  source_step: step_4_generation
  payload:
    candidate_strategies: required
    scenario_spec.defaultResources: required           # 复用 seed 字段
    scenario_spec.metricProfile: required              # 复用 seed 字段, 模拟输出对齐 aiField
    scenario_spec.agentRoles: required                 # 复用 seed 字段
  required_fields: [candidate_strategies 非空, metricProfile.aiField 非空]
  accepted_when: candidate_strategies 非空

# 聚合规则（severity-3 修订, 不增实体字段, 回应 stage4-code-audit 警示）:
#   fallback_used (派生值, 非 Factor Ledger 实体字段, 避免 stage4-code-audit 触发的 schema 变更):
#     = any(protocol_failures[*] == "model_switched_to_fallback")
#     OR explicit step._simulation_meta.fallback_signal
#   语义声明: 「模型切换 ≠ 证据不足」
#             —— fallback_used=true 不必然等于 INSUFFICIENT, 仅做 grade 上限夹逼
#   聚合映射:
#     fallback_used=true  → confidence_grade ∈ {MEDIUM, LOW}（上限 MEDIUM, 不再升至 HIGH）
#     fallback_used=false → 无额外夹逼, 按常规证据强度评估
#   必记条目: 当 fallback_used=true, step_degradation_reasons 必含 "model_fallback_used"
#   维护承诺: 此规则在不新增 Factor Ledger 实体字段的前提下可完整定义——stage4-code-audit 警示关闭
# settleability 注释 (F5, 2026-07-19): 本项目锚数据集的「可结算 (settleable)」语义 = 因子同时满足五要件:
#   (i)   判定规则 — calibration_status 字段反映其是否已被盲评通过
#   (ii)  阈值区间 — quantified_threshold 字段
#   (iii) 反证信号 — counter_signal 字段, 后验反证, 步骤 7 验证
#   (iv)  盲评字段 — calibration_check 四件套 (gold_anchor_pass + youden_j + error_rate + kendall_tau), 步骤 7 落地
#   (v)   来源分级 — source_tier + origin 字段, §2.1 步骤 5 factor_ledger_entries 已承载
# 五要件齐备 = 「可裁定的断言」; 与 disaster-KG 描述性三元组 (LLM4TyphoonKG, github.com/2BAIHAO/LLM4TyphoonKG, 无抽取评测/无结算语义/CoT 蒸馏 7B) 显式区分.
# calibration_status 字段记录「五要件齐备度」:
#   tracking   = 模拟端已生成, 五要件尚未齐备 (缺盲评); 步骤 5 模拟结束时必刷为此值.
#   calibrated = 五要件齐备, 且经步骤 7 calibration_check 盲评通过 (gold_anchor_pass agreement_rate ≥ 85% + cohens_kappa ≥ 0.6 + youden_j > 0 + error_rate ≪ 10% + kendall_tau ≥ 0.5 / n_pairs ≥ 10).
# 维护承诺: settleability 五要件不引入 Factor Ledger 新实体字段, 全部由现有 19 字段 + H4 校准四件套承载——与 stage4-code-audit 警示保持兼容.
output_schema:                                         # 大量复用 Factor Ledger 19 字段（侦察 §2.1）
  factor_ledger_entries:
    - {factor_id: string,                              # 必复用
       event_id: string,                               # 必复用 (Q4 fork 建议改名)
       origin: enum[cds_generated, kimi_derived, human_seeded, historical_record],  # 必复用 (Q4 扩展)
       event_relation: enum[precursor, suppressor, branch, counter_signal],  # 必复用
       direction: string,                              # 必复用, 约定 "increases_/decreases_<aiField>"
       sim_hook: string,                               # 必复用
       observable_proxy: string,                       # 必复用
       quantified_threshold: string,                   # 必复用
       calibration_status: enum[tracking, calibrated], # 必复用, settleability 五要件齐备度 (F5); 步骤 5 模拟结束时刷为 tracking, 升 calibrated 需经步骤 7 calibration_check 盲评通过 (详见字段上方注释块)
       settlement_source: string}                      # 必复用
  trajectory_dtw_aggregate: float                      # 必填, 复用 proposal §5.4 "聚合 DTW 分数" 术语（侦察 §4 冲突#3）
  scores:                                              # 复用 settlement_record 字段
    percentile_hit:
      - {metric: string, anchor: any, sim_P25: float, sim_P50: float, sim_P75: float}
  protocol_failures: list[str]                         # 必复用, 例 observable_proxy_not_in_sim
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]
  step_degradation_reasons: list[str]                  # 必填, 命名遵从侦察 §4 冲突#1 改名（避免与 reason_for_inconclusive 语义重叠）

violation_handling:
  - condition: 模拟器 runtime error OR MC 推演出度异常小 (n<10)
    action: 标 INSUFFICIENT 继续, protocol_failures 必填
  - condition: percentile_hit 中所有锚都落在 [P5, P95] 之外
    action: 退回上步 (step_4), 提示策略生成参考工程夹逼
```

### 步骤 6 — Validation Agent（= 校验臂, Q3）

```yaml
input_schema:
  source_step: step_5_simulation
  payload:
    trajectory_dtw_aggregate: required
    percentile_hit: required
    scores.anchor_distance_iqr: required     # 复用 Factor Ledger 字段 (Q4)
  required_fields: [percentile_hit, scenario_spec.metricProfile]
  accepted_when: step_5.confidence_grade != INSUFFICIENT

output_schema:                               # 沿用 Q3 三档 + 既有命名 (侦察 §3.1)
  arms_executed: bool                        # 必填 (severity-1 修订)——三态区分"未执行"/"全 PASS"/"任一 RED", 避免空集 vacuous truth 把"未实现"误读为"无标红"
  validation_arms:                           # 当 arms_executed=false 时为空列表 [], 不得被读为 vacuous PASS
    - {arm_id: enum[primary, secondary, sanity_gate],   # 必复用, Q3 三档
       red_flag: bool,                                  # 必复用
       red_flag_reason: string,                         # 必复用
       reference_trajectory: object,                    # 必复用, gate 时刻表 + 参照曲线
       sim_trajectory_dtw: float}                       # 必复用
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]
  step_degradation_reasons: list[str]        # 条件必填——arms_executed=false 或任一 red_flag 触发时必记

violation_handling:                          # 三态显式区分 (severity-1 修订)——消解硬 checkpoint 逻辑裂缝
  - state: (a) arms 未执行 / 全空（零实现或无法运行）
    condition: validation_arms 全空 OR 校验臂协议未配置 OR runtime 未启动
    action: arms_executed=false + 步骤 6 grade=INSUFFICIENT + step_degradation_reasons 记 "validation_arms not executed"
    semantics: 空 arms 不得被读为 vacuous PASS——hard checkpoint 第三合取项据此区分 "零实现" vs "真无标红"
  - state: (b) arms 执行且全 PASS
    condition: 任一 arm red_flag == false 且全部 arm 已运行
    action: arms_executed=true + 步骤 6 grade ≥ MEDIUM + 不触发降级
  - state: (c) 任一 RED
    condition: any(validation_arms.red_flag) == true
    action: arms_executed=true + 步骤 6 grade ≤ LOW + red_flag 全部保留（不退回, 校验臂结果如实呈现, 由 step_7 在 H4 框架下处理）
```

### 步骤 7 — Judge Agent（= 开题 M4）

```yaml
input_schema:
  source_step: step_6_validation
  payload:
    validation_arms: required
    factor_ledger_entries: required          # 复用 step 5 output
    candidate_strategies: required           # 复用 step 4 output
  required_fields: [validation_arms, factor_ledger_entries]
  accepted_when: step_6.confidence_grade != INSUFFICIENT

output_schema:                               # 大量复用 Factor Ledger + H4 校准四件套
  factor_updates:                            # 必复用, 三列表 (Q4 直接复用)
    supported:    [{factor_id, evidence, confidence_post}]
    rejected:     [{factor_id, evidence, confidence_post}]
    inconclusive: [{factor_id, reason_for_inconclusive}]   # 必复用, 单数, 与 step 5 degradation 语义分家
  adjudication_meta:                         # 必复用, Q4 新增
    {panel_size: int, blinded: bool, outcome_visibility: enum, inconclusive_rate_policy: string}
  adjudicator:                               # 必复用
    {status: enum[pending, supported, rejected, inconclusive],
     confidence_0_10: int,                   # 0-10 连续评分
     reason_for_inconclusive: string}
  calibration_check:                         # 必填, 严格遵从 H4 四件套 (proposal §0.2 四道关 + §3 H4)
    gold_anchor_pass: {agreement_rate: float, cohens_kappa: float},   # ≥85% + κ≥0.6
    youden_j: float,                         # >0
    error_rate: float,                       # ≪10%
    kendall_tau: float,                      # ≥0.5, 与校验臂参照排名的相关性
    kendall_tau_n_pairs: int}                 # ≥10 对
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]
  step_degradation_reasons: list[str]        # judge 失效时必填 (改为"不硬打分"——idea §5 第 5 条诚实边界)

violation_handling:
  - condition: calibration_check.kendall_tau < 0.5 OR error_rate > 10%
    action: 标 judge INSUFFICIENT 继续 (认知本步失效, 不硬打分) + step_degradation_reasons 必填
  - condition: adjudicator.status == inconclusive 占比 > 70%
    action: 触发中止信号, 等待人介入 (panel 配置错误或锚集本身不足)
```

### 步骤 8 — Synthesis Agent

```yaml
input_schema:
  source_step: step_7_judge
  payload:
    全步骤 output: required (八份 contracts 全部累积)
  required_fields: 八份 contracts 全部非空
  accepted_when: 八份 contracts 全部存在 (但不要求 grade=HIGH, 详见 §2.3 hard checkpoint)

output_schema:
  decision_brief_markdown: string           # 终简报, 严格沿用 §2.2 模板 (背景/候选/校验/评分/已知-推断-无知清单/置信度摘要/人拍板位)
  worst_upstream_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]    # 上游最差等级
  insufficient_step_count: int               # INSUFFICIENT 步数 (降级 DAG 终汇点)
  confidence_grade: enum[HIGH, MEDIUM, LOW, INSUFFICIENT]        # 终简报整体 grade = worst_upstream_grade
  step_degradation_reasons: list[str]        # 合并八步全部降级原因

violation_handling:
  - condition: 任何中间步 output 缺失
    action: 标 INSUFFICIENT 继续, decision_brief_markdown 必含"流水线不完整"提示
  - condition: insufficient_step_count >= 4
    action: 终简报 grade 强制 INSUFFICIENT + 人拍板位突出"流程本身不完备"
```

---

## §2.2 无知清单与置信度降级显式协议

### 1. 「已知 / 推断 / 无知」三档判定规则（≤1 页可复述）

| 档位 | 判定证据 | 可机器判 | 必须人判 |
|---|---|---|---|
| **已知（KNOWN）** | 有官方锚值 / 物理常数 / 已公布法规条文 | ✅ 是（calibration_status == calibrated / metricProfile.aiField 有官方锚） | — |
| **推断（INFERRED）** | 有推演侧可观测 + 历史侧可类比, 但无官方锚 | ✅ 是（factor_ledger_entries.event_relation ∈ {precursor, suppressor, branch} 且 calibration_status == tracking） | — |
| **无知（IGNORED）** | 检索为空 OR counter_signal 未编码 OR adjudication 失败 | ⚠️ 部分（机器判"未编码"易, "判该编码"难） | ✅ 必须人判 ignorant_class 是否合理——这是诚实边界最后一道关 |

**IRREVERSIBILITY 约束**：档位判定一旦落盘, **不可被同一步骤内部 upgrade**（不允许"步骤内自圆其说"）。升级需经下一轮 pipeline 重跑, 由人拍板位确认。

**证据来源映射**：HIGH ≈ data-confirmed（官方锚 / 物理常数） / MEDIUM ≈ model-derived（LLM 推演 + 校验臂参照） / LOW ≈ expert-only（adjudicator panel 一致但无锚） / INSUFFICIENT ≈ no source（检索为空 / 校验臂无模型）—— 这一映射与阶段 1 §1.3 先验 2（Lichtenstein-Fischhoff-Phillips 1982 + Morgan-Henrion 1990）的 data/model/expert 三分类一致。

**与已知字段的语义区分**（回应侦察 §4 冲突#2）：`ignorance_class` 描述步骤证据状态，`origin` 字段描述因子来源——两者正交。`explicit_known_unknowns` 是前瞻待证假设（步骤 2 主动声明），与 Factor Ledger 的 `counter_signal`（后验反证）和 `reason_for_inconclusive`（裁定失败原因）三者语义不重合, 三者在每份 step output 中分别命名, 不允许合并。

### 2. 降级 DAG（1 页内可表达）

```
step1 ── confidence_grade ──> step2 ── grade ──> step3 ──> step4 ──> step5 ──> step6 ──> step7 ──> step8
   │                              │                                              │                                │
   │ INSUFFICIENT                 │ INSUFFICIENT                                  │ INSUFFICIENT                   │ worst_upstream_grade
   │   ↓ 全下游 ≤ MEDIUM           │   ↓ 全下游 ≤ MEDIUM                            │   ↓ step 7/8 ≤ LOW            │ insufficient_step_count
   │                              │                                              │                                │
   │ LOW                          │ LOW                                          │ LOW                            │ 终简报置信度摘要
   │   ↓ 只传直接后继              │   ↓ 只传直接后继                              │   ↓ 只传直接后继                │
   │                              │                                              │                                │
   │ HIGH / MEDIUM                │ HIGH / MEDIUM                                │ HIGH / MEDIUM                  │ 正常传播, 不限制下游
```

**规则**（严格遵从 §3.6a）：
- **INSUFFICIENT** 传播 ≤ MEDIUM 上限给**全部下游步骤**（不只是直接后继）。理由：INSUFFICIENT 意味着无证据源, 后续步骤无法在低证据下达到 HIGH。
- **LOW** 只传播 ≤ MEDIUM 上限给**直接后继**。理由：LOW 是"专家一致但无锚", 不阻塞再下游的累积证据恢复。
- **HIGH / MEDIUM** 正常传播, 不设上限。
- **步骤 8 报告** `(worst_upstream_grade, insufficient_step_count)` 作为降级 DAG 的终汇点——`worst_upstream_grade` 是八步中 grade 最低者（按 INSUFFICIENT < LOW < MEDIUM < HIGH 的偏序），`insufficient_step_count` 是八步中 grade==INSUFFICIENT 的步数。

**形式化**：`grade(S_{i+1}) ≤ ceil_upstream_grade(grade(S_i))`，其中 `ceil(x) = MEDIUM if x == INSUFFICIENT or x == LOW else x`。

### 3. 终简报 markdown 骨架模板（步骤 8 输出主结构）

```markdown
# 决策简报 —— {scenario_spec.name}（{scenario_spec.id}）

## 背景
{scenario_spec.description (≤200 字)}

## 候选
{candidate_strategies 列, 每条含 option_combination + risk_hint}

## 校验臂判定
{validation_arms 表, 每臂 arm_id / red_flag / red_flag_reason / 简注}

## 评分汇总
{factor_updates.{supported, rejected, inconclusive} 三段 + calibration_check 四件套值}

## 已知-推断-无知清单
- **已知**：{ignorance_class=KNOWN 的条目}
- **推断**：{ignorance_class=INFERRED 的条目}
- **无知**：{ignorance_class=IGNORED 的条目 + 每条无知由谁拍板确认（必人判）}

## 置信度摘要
{worst_upstream_grade = X, insufficient_step_count = N, 八步 grade 阶梯}

## 人拍板位
- [ ] 候选排序是否采纳
- [ ] 无知清单是否补检索（哪几条 KU 可由人确认）
- [ ] 校验臂任一 red_flag 是否升级为否决
- [ ] 终简报 grade 是否接受 → 决定 GO / 降级 / NO-GO
```

---

## §2.3 错误传播控制

### 1. 每步 input schema 校验规格

每步 Agent 在运行前先做 schema 校验（自动成本预估 ≤1 token/step，依赖字段名+类型检查），校验失败进入 §2.3.2 回退条款。校验清单：

| 步骤 | 必查字段 | 必查类型 | 必查值域 |
|---|---|---|---|
| 1 | report_text | string | non-empty |
| 2 | scenario_spec.{id, disasterType, eventChain} | 嵌套 | eventChain 非空 |
| 3 | knowledgeBaseQuery.keywords | string[] | non-empty |
| 4 | interventionDimensions.options | array | non-empty |
| 5 | candidate_strategies, metricProfile.aiField | 嵌套 | aiField 枚举（侦察 §1.4） |
| 6 | percentile_hit, validation_arms | 嵌套 | arm_id ∈ {primary, secondary, sanity_gate} |
| 7 | factor_ledger_entries, calibration_check | 嵌套 | kendall_tau_n_pairs ≥ 10 |
| 8 | 全八份 contracts | object | 八份皆非空 |

### 2. 每步回退条款 (IF X THEN Y，三选一)

每步 violation_handling 已嵌入 §2.1 YAML；下表汇总三选一动作的覆盖矩阵：

| 步骤 | 退回上步 (R) | 跳过此步 (S) | 标 INSUFFICIENT 继续 (I) |
|---|---|---|---|
| 1 | — | — | R 不适用（入口无上游）→ I 默认 |
| 2 | — | S（当上游 INSUFFICIENT 转 step_1 出去） | I（分解失败） |
| 3 | — | — | I（检索为空是核心降级点，idea §1 强调） |
| 4 | R（候选空 → step_3 放宽召回） | — | I（其他类型） |
| 5 | R（所有锚都离谱 → step_4） | — | I（runtime error） |
| 6 | — | — | I（校验臂未配置 / 校验臂结果如实呈现，红标不退回） |
| 7 | — | — | I（认知失效，不硬打分） |
| 8 | — | — | I（中间步缺失时仍产简报但标 INSUFFICIENT） |

### 3. 整体 hard checkpoint（单一布尔，§3.6b，分级 L1 / L0 回应 severity-2）

```
# L1（完整系统, 默认门槛）
GO_L1 = (steps_completed == 8)
  AND (count(grade ∈ {HIGH, MEDIUM}) >= 5)      # 至少 5/8 步在 MEDIUM 及以上
  AND (step_6.arms_executed == true)            # severity-1 修订——空 arms ≠ 无标红, 必须 executed
  AND (NOT any(validation_arms.red_flag))       # 校验臂无标红
  AND (insufficient_step_count <= 3)            # 步骤 8 终汇点 ≤ 3
```

```
# L0（最小验证 / 纸面走查, 校验臂零实现, 阶段 5 §5.5 走查时启用）
# 豁免项: L1 第三合取项 (step_6.arms_executed == true)
#   —— 理由: L0 模式下校验臂协议未实现, structure 上必然 arms_executed=false, 不可作为失守判定
# 豁免代价（三件, 同时满足才允许 L0 GO）:
#   1. 终简报结论措辞强制降级为「流程性建议」（"procedure-level suggestion", 不可说"校准过的建议"）
#   2. 步骤 8 worst_upstream_grade == INSUFFICIENT 时, 人拍板位显著标注 "L0 阶段, 校验臂未实现"
#   3. insufficient_step_count ≤ 4（比 L1 的 ≤ 3 多容忍 1 步）
GO_L0 = (steps_completed == 8)
  AND (count(grade ∈ {HIGH, MEDIUM}) >= 5)
  AND (NOT any(validation_arms.red_flag))       # 在 L0 下该合取项 vacuous true, 不构成实质检查——属有意豁免
  AND (insufficient_step_count <= 4)            # L0 容忍多 1 步 INSUFFICIENT
```

```
# L0 → L1 升级条件（不可逆）
L0→L1: IF (校验臂协议实现, validation_arms 至少一次 end-to-end 实跑)
           AND (kendall_tau_n_pairs ≥ 10 已可稳定计算)
       THEN 切换至 GO_L1 布尔, L0 豁免自动失效, 阶段 5 终裁 memo 须重审
```

**呈报规则**（哪一个合取项失败报哪一项）：
1. `steps_completed < 8`：标 "**流程不完整**"，升级阶梯 = 直接报人拍板。
2. `5/8 grade ≥ MEDIUM` 不达：标 "**证据强度不足**"，升级阶梯 = 标 MEDIUM 步列出供人增补检索。
3. `validation_arms.red_flag == true`：标 "**物理闸门标红**"，升级阶梯 = 由人决定否决该候选还是降级该候选为"参考"。
4. `insufficient_step_count > 3`：标 "**降级过度**"，升级阶梯 = 触发 §2.3.4 振荡检测 / 转 fallback。

**升级阶梯总论**：任一合取项失败 → 评估包**不**自动转 GO；统一发信号给人拍板位，由人在以下三选项中选一：(a) 修改后重跑流水线 / (b) 接受降级结果, 该场景降级为"流程性建议"（§2.4 选项 2） / (c) NO-GO（§2.4 选项 3, 仅当返工一次仍失败）。

### 4. 振荡检测（自检式）

**触发条件**：在单次流水线执行中, 满足以下之一：
- 任一步骤 R（退回上步）或 S（跳过）动作 ≥ 2 次, **且**累计触发 ≥ 2 步 → 触发"**流程振荡**"告警。
- insufficient_step_count ≥ 4 → 即使未触发"流程振荡", 也自动转 fallback（终简报 grade 强制 INSUFFICIENT）。

**流转**：触发后, 步骤 8 终简报 grade 强制 INSUFFICIENT, decision_brief_markdown 的"人拍板位"中追加："**流水线振荡, 建议转 fallback paper（方法论 short paper, 不开新工程）**"。

---

## §2.4 编排范式论证

### 4×3 表（4 维 × 3 选项）

| 维度 \ 选项 | **选项 A：固定 8 步**（推荐） | **选项 B：hybrid（按场景族路由）** | **选项 C：完全动态** |
|---|---|---|---|
| **(α) novelty** | **低-中**（协议层而非架构层；阶段 1 §1.1 论证 fixed × degradation 组合在 5 邻居中未占位） | 中（族路由本身有 novelty 余地） | 高（但落入 AFlow / ADAS / EvoAgent workflow 进化搜索红海；阶段 1 §1.1 已论证此点） |
| **(β) 可解释性** | **高**（每步契约 + grade + 降级原因完整可审计, 满足高风险决策的硬要求） | 中（族路由决策本身需解释） | 低（动态图难复现, 难回滚, 违背 §16.6 误判可追溯约束） |
| **(γ) 实施成本** | **低**（步骤 4–7 大量复用 Policysim + Factor Ledger, 4 个完全新建步；与阶段 3 资产映射矩阵一致） | 中（族路由 metadata 需扩展 seed；4 族 × 8 步 = 32 个契约变体） | 高（动态图 = 自演化调度器, 工程量翻 2-3 倍, 且重做因子池分配规则） |
| **(δ) 滑向红海风险** | **低**（阶段 1 §1.1 已锁定红海边界：本想法≠workflow 进化） | 中（族路由与 Supervisor 调度部分重叠, 易被 read 为"半动态演化"） | 高（直接落 AFlow / ADAS 红海, novelty 价值逼近 0） |

### 推荐结论（引用 Stage 1 贡献落点）

**推荐选项 A：固定 8 步 + 步骤级降级**。理由一句话：阶段 1 §1.1 贡献落点陈述已锁定——"固定步骤集 + 显式降级协议"这一组合在 5 邻居中均未占位, 选 A 即守住 novelty 在协议层而非架构层, 同时保住可解释性（高风险决策硬要求）与低工程成本。

### 备选方案

**若评审要求动态编排，则降级为选项 B（hybrid, 按场景族路由）**。实现方式：固定 4 个场景族（工业事故 / 自然灾害 / 公共卫生 / 城市生命线, 沿用阶段 1 §1.2 与 §3.1 File 1 §5.1 已确认的分类）作为路由外层, **族内仍固定 8 步**——外层是调度策略, 内层仍是步骤契约；novelty 介于 A 与 C 之间, 工程量中等, 可解释性中等。选项 C（完全动态）**不推荐**：在高风险决策场景下落入红海且失去可审计性, 工程量翻倍收益不增。

**为什么不选 hybrid 作为首推**：hybrid 引入"族路由决策"本身的可解释性缺口, 而本想法的诚实边界已经要求"AI 只动嘴"——族路由若由 LLM 决定, 等于引入新的不透明点；保留固定 8 步即保留"每一步都可被独立审计"的硬要求。

---

## 修订记录（附录 A）

- v1.0 / 2026-07-19 / pair 主笔生成
- 输入：Oracle 计划 `prompt-exports/oracle-plan-2026-07-19-160143-a42bf4-2a67.md`（阶段 2 / Generated Plan §3.1 File 2 / §3.6 算法设计 a/b） + 阶段 2 engineer 侦察 `prompt-exports/stage2-recon-schema-crosswalk.md`（5 条冲突 + 改名建议全部采纳）+ 阶段 1 `adjacent-work-positioning-2026-07-19.md` §1.1–§1.3 + `idea-decision-pipeline-2026-07-19.md` §1 §5 + 开题 v1.3.1 §5.3 §5.4 H4 + Q3 §1–§3 + Q4 §2–§3
- 待复核：阶段 5 终裁 memo 是否能在 hard checkpoint 三选项上保持一致
- 限制声明：§2.2 三档判定规则的"必须人判"边界需要阶段 5 终裁时引入人拍板位模板对齐
- 评审状态：未评审（阶段 4 红队评审的输入材料）

- v1.1 / 2026-07-19 / pair 主笔修订（红队评审 v1.0 后最小补丁）
- 修订依据：`redteam-review-2026-07-19.md` 严重问题 1/2/3（**fatal=0, 未触发返工**）
- 修订范围（最小补丁, 仅 3 处 + 本附录追加）:
  - **严重-1** 落点 §2.1 步骤 6 + §2.3 第 3 节:
    - 步骤 6 output_schema 加 `arms_executed: bool` 必填
    - 步骤 6 violation_handling 改三态 (a/b/c), 消解空集 vacuous truth 误判
    - §2.3 L1 第三合取项从 `NOT any(red_flag)` 改为 `arms_executed == true AND NOT any(red_flag)`
  - **严重-2** 落点 §2.3 第 3 节:
    - hard checkpoint 分级为 L1（完整系统, 4 合取项）/ L0（最小验证, 3 合取项 + 豁免声明）
    - 明示 L0 豁免项 + 豁免代价三件 + L0→L1 不可逆升级条件
  - **严重-3** 落点 §2.1 步骤 5 output_schema 顶部注释块:
    - 加 `fallback_used` 派生值定义（不增 Factor Ledger 实体字段）
    - 聚合映射 fallback_used=true → grade 上限 MEDIUM + step_degradation_reasons 必含 `model_fallback_used`
    - 语义声明"模型切换 ≠ 证据不足"——回应 stage4-code-audit 警示
- 未改动: §1 preamble / §2.2 全部 / §2.4 全部 / 其余 7 步契约 YAML 主体（保持字数预算不变）
- 评审状态：v1.1 仍待阶段 4 重审走读；fatal=0 未触发返工

- v1.2 / 2026-07-19 / pair 主笔最小补丁（修订简报 Item 5）
- 修订依据：`revision-brief-2026-07-19.md` F2（决策行动锚源）+ F5（settleability 切割）。
- 修订范围（仅 2 处 + 本附录追加）：
  - §2.1 步骤 3 output_schema 新增 `decision_actions[]` 字段（`origin` 枚举扩 `ifrc_go_field_report` / `nws_cap_alert` / `ntsb_carol` / `csb_final_report` / `mem_gov_announcement` / `mem_gov_investigation_report` / `provincial_gd` / `provincial_fj` / `provincial_zj` / `jma_digital_typhoon` / `em_dat_consequence` 等 F2 行动锚源）。
  - §2.1 步骤 5 output_schema 顶部新增 settleability 注释块（F5 五要件）；`calibration_status` inline 注释扩 settleability 语义，并指向新增注释块。
- 未改动：§1 preamble / §2.2 全部 / §2.3 全部 / §2.4 全部 / 其余 7 步契约 YAML 主体；v1.1 修订范围（severity-1/2/3）保持不变；保持字数预算与既有结论不变。
- 评审状态：与红队评审范围并列输入，未单独触发新一轮评审。
