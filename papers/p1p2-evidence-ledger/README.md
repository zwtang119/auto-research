# P1+P2 Evidence Ledger — 证据结构化 Agent 决策主线

> 主线目标：在灾害应急多 Agent 决策中，把 RAG、信号融合、因子提取、外部结算连接到一份**可验证的证据账本**，使每个关键 claim 都可被独立检验、审计并结算。
> 创建日期：2026-07-03  
> 协议：Deli_AutoResearch（控制论版本）  
> 路线图：`../docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §6  
> 数据合约：`../framework/schemas/data-contracts.md` §8（`evidence_ledger_entry`）  
> 陷阱清单：`../framework/schemas/experiment-pitfalls.md` §3（PIT-201..PIT-208）

## 1. 三句话回答

1. **要做什么**：在 Gulei / Polymarket 等应急与结算场景上，写出第一条 `evidence_ledger_entry`，演示因子提取、矛盾证据、时效性与可结算性四条核心 invariant 都能命中。
2. **不做什么**：不是另一个 RAG benchmark，不是又一个多源信号融合 demo，也不是在 P2.1 输出之后做语义聚合。证据账本是**决策的契约**，不是流水线。
3. **如何停**：Day 14 五人格 review 中位分 ≥ 6.5 且 P1.2 settlement 通道存在；否则退回 P12 短论文路线，不再在大结构上赌。

## 2. 入口

| 想看 | 路径 |
|------|------|
| 任务规格 | `state/task_spec.md` |
| 当前进度 | `state/progress.json` |
| 已尝试方向 | `state/directions_tried.json` |
| 累积发现 | `state/findings.jsonl` |
| 迭代日志 | `state/iteration_log.jsonl` |
| 输入输出合约 | `state/io_spec.md` |
| 工作日志 | `logs/work.jsonl` |
| 编排日志 | `logs/orchestrator.jsonl` |
| 心跳日志 | `logs/heartbeat.jsonl` |
| 论文大纲 | `paper/outline.md` |
| 启动 prompts | `claude-prompt.md`、`mimo-prompt.md` |
| 知识库索引 | `wiki/index.md` |

## 3. 与已有目录的关系

| 目录 | 角色 |
|------|------|
| `papers/p07-signal-fusion/` | evidence **input** layer：把多源信号变成 `signal_evidence_entry` 后再喂入本目录 |
| `papers/p08-market-calibration/` | settlement / calibration layer：消费 `evidence_ledger_entry` 的 `settlement_rule` 与 `observed_outcome`，输出 `settlement_record` 与 Brier/Log Loss |
| `legacy/p11-closed-v5-minimax-m3/` | 反例与样本来源：free-text reasoning trace **不是** evidence（见 PIT-207、PIT-408）|
| `papers/p12-judge-calibration/` | 平行赛道：本目录的 factor quality 评估借用 P12 的 blind/pairwise/neighborhood 协议 |

本目录 **不移动** 上述目录的文件，不吞并它们的实验数据；只在 `state/` 和 `experiments/ledger/` 下新增。

## 4. 核心反题（与历史路线对话）

| 旧路线 | 本主线的反题 |
|--------|------------|
| "P1 = 接入知识库效果更好" | "P1+P2 = 每个关键判断都落到 factor ledger" |
| P2.1 = 12 数据源融合 | P2.1 在本主线中只承担 evidence input：算法本身不在论文卖点 |
| P8 = 预测市场校准 LLM Agent | P1.2 = belief update with settlement evidence，**不是** 知识写回 |
| P11 = 主论文大修 | P11 仅为反例：free-text trace 不能进 ledger |

## 5. 失败信号（写在 `state/blocked.md` 的条件）

- 任一 invariant（PIT-201..PIT-206）连续 2 轮被绕开且无人修复。
- 30 条手工 `evidence_ledger_entry` 中 `un_settleable_ratio > 0.4` 且无解释。
- `confidence_delta_distribution` 方差为 0（在 `experiments/belief_update_stats.json`）。
- `audit_trace` 不可结构化，至少 20% 行降级为自由文本。

## 6. 非目标

- 不做 RAG 通用系统综述；不与 LangChain / LlamaIndex 直接对照。
- 不在 Day 1-2 阶段就接入真实 Gulei 应急 API。
- 不修改 P2.1 或 P1.2 内的 harness；本目录只读取 `experiments/` 下的产物。
- 不请求用户任何决策；所有 ambiguous case 写入 `state/blocked.md` 或 `state/findings.jsonl`。
