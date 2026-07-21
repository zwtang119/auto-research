# AIwork Research Spec: Path Card Audit + Baseline Suite

> **类型**: research-execution-spec
> **状态**: ready-for-aiwork
> **日期**: 2026-06-11
> **执行者**: AIwork
> **范围**: 研究审计，不做前端实现，不修改 `docs/references/`

## 1. 目标

本 spec 让 AIwork 执行两条独立研究线：

1. **Path Card Internal Audit**：审计 21 支深描球队路径卡，判断 CDS 自身产物是否具备区分力、可结算性和来源边界。
2. **Baseline Suite Design**：预注册朴素基线与外部 baseline 的构造方式，为赛后或阶段性校准准备比较框架。

这两条线不是为了证明 CDS 比 Kimi 更准，而是为了回答：

> CDS4WorldCup 当前产出的知识对象，是否比普通叙事更可审计、更可结算、更能暴露自身失败条件？

## 2. 非目标

- 不做冠军推荐。
- 不输出投注建议、赔率价值、仓位或收益率。
- 不把 Kimi 概率作为 CDS 事实输入。
- 不把 Kimi reason 直接升格为 Factor Ledger 因子。
- 不做前端页面实现。
- 不读取、引用、复制或提交 `docs/references/` 下任何文件。
- 不修改 `specs/` 或 `docs/design/specs/` 中既有 spec，除非用户另行要求。

## 3. 必读上下文

执行前阅读：

- `CLAUDE.md`
- `wiki/index.md`
- `docs/source-policy.md`
- `docs/design/specs/2026-06-11-cds4worldcup2026-path-space-spec.md`
- `docs/path-card-template.md`
- `artifacts/team-cards/README.md`
- 21 张 `artifacts/team-cards/*.md` 中状态为 `deep-description` 的路径卡
- `data/processed/team_registry.csv`
- `data/processed/kimi_baseline_signals_matrix.csv`
- `artifacts/reports/plan-c-protocol-validation.md`（若已存在）

禁止读取：

- `docs/references/**`
- `data/raw/**`

如需 Kimi 汇总字段，只使用已处理后的 `data/processed/kimi_baseline_signals_matrix.csv`。

## 4. Source Policy 约束

严格遵守 `docs/source-policy.md`：

- Green Source 才能作为事实输入。
- Kimi probability / ranking / reason 只能作为 public AI baseline、候选线索或 Marginalia。
- 市场/赔率只能作为外部 baseline 或描述性参照，不做投注建议。
- Factor Ledger 候选必须有 `observable_proxy`、`settlement_rule`、时间窗口和来源。

## 5. Research Line A: Path Card Internal Audit

### 5.1 核心问题

审计 21 张深描路径卡是否存在以下问题：

- 不同球队的阻力类型是否有真实区分度。
- 高频阻力是结构性恒常，还是模板化填充。
- `Required Breakthroughs` 是否具体到球队机制。
- `Black Swan Helpers` 是否过度同质化。
- `Miracle Package` 中多少条件可赛后结算。
- §11 Current Interpretation 是否和 §3-§6 的结构一致。

### 5.2 输入

- `artifacts/team-cards/*.md`
- `data/processed/team_registry.csv`
- `data/processed/kimi_baseline_signals_matrix.csv`

只纳入 `> **状态**: deep-description` 的 21 张路径卡。

### 5.3 输出

创建：

- `artifacts/reports/path-card-internal-audit.md`
- `data/processed/path_card_internal_audit.csv`
- `data/processed/path_card_obstacle_type_matrix.csv`

可选创建脚本：

- `scripts/audit_path_cards.py`

### 5.4 CSV 字段

`path_card_internal_audit.csv` 每队一行：

```csv
team_slug,canonical_team,zh_name,status,primary_obstacle_count,required_breakthrough_count,black_swan_helper_count,miracle_condition_count,settleable_condition_count,placeholder_count,source_boundary_notes,overall_audit_status
```

字段解释：

- `settleable_condition_count`：Miracle Package 中有清楚 observable proxy 和 settlement rule 的条件数量。
- `placeholder_count`：仍包含 `<待分析>`、`<数据不足>` 或空白关键字段的数量。
- `source_boundary_notes`：记录 Kimi baseline 是否被正确降级为外部参照。
- `overall_audit_status`：`pass` / `pass_with_notes` / `needs_revision`。

`path_card_obstacle_type_matrix.csv` 每队一行，列为阻力类型：

```csv
team_slug,canonical_team,base_strength_gap,bracket_strength,squad_depth,injury_risk,travel_fatigue,tactical_mismatch,psychological_pressure,low_scoring_dependency,penalty_dependency,favorite_collision,other
```

单元格为该类型在该队 §3 中出现次数。

### 5.5 报告结构

`artifacts/reports/path-card-internal-audit.md` 包含：

1. Executive Summary
2. Input Scope
3. Deep Card Coverage
4. Obstacle Type Distribution
5. Constraint Classification
6. Settleability Audit
7. Source Boundary Audit
8. Findings
9. Recommended Fixes
10. Next Research Implications

### 5.6 关键分类

报告必须把低熵/高频字段分为三类，而不是简单判定为“无信息量”：

| 分类 | 定义 | 例子 |
|---|---|---|
| `universal_constraint` | 几乎所有球队都面对，但仍是世界杯路径的结构性边界 | bracket strength, injury risk |
| `differentiating_variable` | 能区分不同球队夺冠路径，应进入后续 taxonomy 候选 | low scoring dependency, penalty dependency |
| `template_noise` | 高频出现但缺少球队特异机制、observable proxy 或 settlement rule | 泛泛而谈的心理压力 |

### 5.7 验收标准

- 只审计 21 张 deep-description 卡。
- 报告明确列出三类字段：普遍约束、区分变量、模板噪声。
- 至少列出 5 个可执行修订建议。
- 不把 Kimi reason 写入 Factor Ledger。
- 不输出投注建议。

## 6. Research Line B: Baseline Suite Design

### 6.1 核心问题

在比较 Kimi、市场和 CDS 之前，先预注册外部 baseline：

> 如果一个极简 baseline 已经解释了公开共识，那么 Kimi 和 CDS 分别新增了什么信息？

### 6.2 Baseline 列表

必须设计以下 baseline：

| baseline_id | 名称 | 用途 |
|---|---|---|
| `uniform_48` | 48 队均匀分布 | 无信息 baseline |
| `defending_champion` | 上届冠军自动续约 | recency bias baseline |
| `fifa_ranking_proxy` | FIFA ranking proxy | 单因子实力 baseline |
| `elo_proxy` | Elo proxy | 单因子实力 baseline，若数据源可得 |
| `market_public_baseline` | 市场公开 baseline | 外部共识，不做投注建议 |
| `kimi_public_ai_baseline` | Kimi public AI baseline | AI crowd baseline |

### 6.3 输出

创建：

- `artifacts/reports/baseline-suite-design.md`
- `data/processed/baseline_suite_registry.csv`

可选创建脚本：

- `scripts/build_baseline_suite.py`

### 6.4 Registry 字段

`baseline_suite_registry.csv`：

```csv
baseline_id,name,input_sources,source_level,construction_rule,calibration_window,settlement_metric,status,notes
```

要求：

- `source_level` 必须是 Green / Yellow / Red / Mixed。
- `market_public_baseline` 必须标注“不用于投注建议”。
- `kimi_public_ai_baseline` 必须标注 Red Source / public AI baseline。
- 如果数据暂不可得，`status=designed_not_populated`，不要伪造数据。

### 6.5 阶段性校准设计

不要只写“等冠军产生后算 Brier”。必须设计阶段性 checkpoint：

| checkpoint | 可结算问题 |
|---|---|
| post_group_stage | baseline mass 是否仍留在存活球队上 |
| round_of_16 | Top8/强队路径是否被淘汰 |
| quarterfinal | baseline 是否集中于仍存活强队 |
| final | 冠军概率分布最终 settlement |

注意：

- 小组赛阶段不宣称证明谁“更准”。
- 阶段性结果只作为 path survival / mass loss 诊断。

### 6.6 验收标准

- baseline registry 覆盖 6 类 baseline。
- 明确每个 baseline 的 source policy 等级。
- 明确哪些 baseline 当前只是 design，不填值。
- 不报告 ROI、PnL、Sharpe、Max Drawdown。
- 不把 baseline suite 写成冠军预测产品。

## 7. 推荐执行顺序

1. 运行/编写路径卡解析脚本。
2. 生成 `path_card_internal_audit.csv`。
3. 生成 `path_card_obstacle_type_matrix.csv`。
4. 写 `path-card-internal-audit.md`。
5. 写 `baseline_suite_registry.csv`。
6. 写 `baseline-suite-design.md`。
7. 运行：

```bash
python3 scripts/audit.py --root wiki/
python3 scripts/verify.py --root wiki/
python3 -m unittest discover -s tests -v
```

如果没有新增 wiki 页面，仍需记录验证结果。

## 8. 完成后回报格式

AIwork 完成后请回报：

- 新增/修改文件列表。
- 每个报告的一句话结论。
- 是否有 source-policy 风险。
- 是否有待用户决策的问题。
- 验证命令及输出摘要。
