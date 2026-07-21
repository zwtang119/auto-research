# Analysis Tables

> **类型**: analysis-directory
> **状态**: header-only
> **日期**: 2026-06-10
> **创建日期**: 2026-06-10
> **最后更新**: 2026-06-10

本目录存放世界杯因子校准实验的规范化分析表，由赛后 settlement artifacts 生成。

设计依据：`docs/superpowers/specs/2026-06-10-worldcup-paper-track-and-experiment-optimization-design.md` §5.2。

---

## 表文件说明

### 1. match_level_results.csv

**内容**：每场比赛一行，记录锁定时间、任务类型、CDS 概率、三方 baseline Brier 分、CDS Brier / Log Loss、来源完整度、schema 合法性和 protocol failure 数量。

**服务研究问题**：

| RQ | 用途 |
|----|------|
| RQ1 | `lock_lead_time_hours`、`schema_valid`、`protocol_failure_count` 评估预注册可执行性 |
| RQ3 | `cds_brier`、`cds_log_loss` 与 `*_baseline_brier` 比较，评估概率校准 |
| RQ4 | 与 `baseline_comparison.csv` 联合，对比 rolling protocol vs static baseline |

### 2. factor_level_results.csv

**内容**：每个因子一行，记录来源、事件关系、因子家族、可观测代理类型、阈值/结算规则完备性、裁判判定状态和知识回写动作。

**服务研究问题**：

| RQ | 用途 |
|----|------|
| RQ2 | `adjudication_status` 分布（supported / rejected / inconclusive / unadjudicable）评估因子可判定性 |
| RQ5 | 与 `judge_adjudication_results.csv` 联合，比较多裁判 vs 单裁判 |
| RQ7 | `factor_family` 分布分析哪类因子最有价值 |

### 3. protocol_failure_events.csv

**内容**：每个 protocol failure 一行，记录失败类型、严重度、发生阶段、描述、解决方案和对论文的影响评估。

**服务研究问题**：

| RQ | 用途 |
|----|------|
| RQ1 | failure 类型分布评估协议健壮性 |
| RQ6 | 与 `knowledge_update_events.csv` 联合，跟踪失败经验是否被结构化回写 |

### 4. baseline_comparison.csv

**内容**：每场比赛 × 每个 baseline 类型一行，记录 baseline 来源、任务对齐情况、概率向量、Brier / Log Loss 和锁定时可用性。

**baseline 类型**（按 §5.3）：

| baseline_type | 说明 |
|---|---|
| `simple_statistical` | 每场必有；缺 Elo/FIFA 时记录估算方法 |
| `market_odds` | 优先归档；无来源时记录 `missing_with_reason` |
| `public_ai` | 仅当任务语义一致且可提取数值概率时评分 |
| `cds_rolling` | 主实验；记录是否使用前序 knowledge update |

**服务研究问题**：

| RQ | 用途 |
|----|------|
| RQ3 | 多 baseline Brier / Log Loss 对比 |
| RQ4 | rolling protocol vs static public AI baseline |

### 5. knowledge_update_events.csv

**内容**：每次知识回写一行，记录来源比赛、更新类型（`calibration_update` / `factor_update` / `protocol_update`）、允许和禁止的后续用途、回写理由。

**服务研究问题**：

| RQ | 用途 |
|----|------|
| RQ6 | 回写类型和理由分析知识更新是否减少重复错误 |

### 6. judge_adjudication_results.csv

**内容**：每个裁判 × 每个因子一行，记录裁判 ID、verdict、置信度、使用的证据、失败标记和知识更新建议。

**裁判角色**（按 §5.6）：

| judge_id 前缀 | 角色 |
|---|---|
| `evidence_judge` | 评估因子证据 vs 阈值 |
| `calibration_judge` | 评估概率校准 |
| `skeptic_judge` | 检测 leakage / hindsight / ambiguity |
| `knowledge_judge` | 生成知识更新建议 |

**服务研究问题**：

| RQ | 用途 |
|----|------|
| RQ5 | 多裁判 disagreement rate、failure detection yield、adjudication quality |

---

## 数据生成流程

```text
settlement_record.yaml  ──┐
factor_ledger_entry.yaml ──┼──> build_analysis_tables() ──> analysis/*.csv
protocol_failure_log.md  ──┤
knowledge_update_log.md  ──┤
baseline artifacts       ──┘
```

- 生成时机：每场比赛 settlement 完成后。
- 验收：CSV 行数与 artifact 数量一致。
- 禁止：不得手动编辑已生成的 CSV 行；如需修正，回到源 YAML 重新生成。

---

## 与论文路线的关系

| 表 | A | B | C | D | E |
|----|---|---|---|---|---|
| match_level_results | ✅ | ✅ | ✅ | | ✅ |
| factor_level_results | ✅ | ✅ | | ✅ | ✅ |
| protocol_failure_events | ✅ | | | | ✅ |
| baseline_comparison | | | ✅ | | ✅ |
| knowledge_update_events | | ✅ | ✅ | | ✅ |
| judge_adjudication_results | | | | ✅ | ✅ |

---

## 相关页面

- [[worldcup-paper-track-and-experiment-optimization-design]]
- [[worldcup-factor-calibration-experiment-design]]
- [[worldcup-phase-minus1-phase0-mvpa]]
