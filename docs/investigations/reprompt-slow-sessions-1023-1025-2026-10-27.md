# 调查：1023/1025 系列会话耗时过长的原因（GPT 思考慢？）

日期：2026-10-27
数据来源：RepoPrompt CE 本地会话存档（非证据快照，为运行时数据）
`~/Library/Application Support/RepoPrompt CE/Workspaces/Workspace-auto-research-8F6D506A-2895-4725-BDEE-A8288FFB1DB4/AgentSessions/`

## Summary

1023/1025 两条实验线从 2026-10-23 22:39 到 2026-10-27 15:31 共约 4 天挂钟时间，其中**大头是等待用户/过夜挂机与后台实验运行，不是 GPT 思考**。在工具记录 100% 保留的会话中，模型思考/生成仅占活跃时间的 4%–31%，工具执行占 69%–96%。GPT（`gpt-6.1-sol` / `gpt-6-astra`，均开 `effort=high` thinking）的真实影响是**长尾延迟**：单次回复前的思考中位数 9–26 秒（与 GLM 同量级），但 p90 可达 135 秒至十几分钟，多次叠加会明显拉长单个 turn 的体感。

## Symptoms

- 用户感知：10/23、10/25 两条线"用了很久"，怀疑 GPT 思考慢。
- 11 个会话跨 4 天（2026-10-23 → 2026-10-27），单会话挂钟最长 65h55m（AF79E34A）。
- 单个 turn 常见 10–70 分钟才有一次回复。

## Background / Prior Research

无需外部检索。数据为本机 RepoPrompt CE 会话存档：

- 索引：`AgentSessions/AgentSessionIndex.json`（含 `coveredTurnDurationSeconds`、`interActiveIntervalGapSeconds`、`agentModelRaw`、`acpModelParameterSelections` 等字段）
- 会话详情：`AgentSessions/AgentSession-<UUID>.json`（`transcript.turns[].responseSpans[].activities[]` 带逐活动时间戳）

时间口径校准（已验证）：`coveredTurnDurationSeconds + ΣinterActiveIntervalGapSeconds ≈ 挂钟跨度`，即：
**挂钟 = 活跃（covered） + 空档（gap，等待用户/挂机）**。

## Investigator Findings

> 本次由主 agent 直接完成（数据为本地运行时存档，无需 pair/explore 委派）；所有数字均由脚本从上述 JSON 复算。

### 1. 11 会话总览

| ID 前缀 | 名称 | 模型 | 挂钟 | 活跃 | 空档(≈等用户) | 工具调用 | 工具记录保留率 |
|---|---|---|---|---|---|---|---|
| AF79E34A | 1023:DNA 消融正式实验启动 | gpt-6-astra | 65h55m | 39h55m | 25h59m | 579 | 2% |
| B796E6F4 | 总 token 数量的估算 | gpt-6.1-sol | 50h06m | 31h27m | 18h38m | 449 | 9% |
| 4A7B4FD2 | 1023-2 | gpt-6.1-sol | 22h38m | 6h23m | 16h14m | 514 | 14% |
| 422AD44D | 调查：1025八臂与五月实验对比 | gpt-6.1-sol | 22h09m | 15h58m | 6h11m | 85 | 11% |
| 65BF2688 | 1025 动态共享队列并发升级 | gpt-6-astra | 16h55m | 3h06m | 13h48m | 113 | 12% |
| 01249BDC | 1025 实验后续步骤分析 | gpt-6.1-sol | 13h33m | 6h44m | 6h48m | 252 | 100% |
| C8B53C93 | 清华 1023/1025 清洁交付执行计划 | mimo-v2.6-pro | 7h36m | 5h51m | 1h44m | 497 | 6% |
| CEC6003B | 1025-3 | gpt-6.1-sol | 5h36m | 1h48m | 3h47m | 99 | 12% |
| 2C0A8EB9 | W2 历史接入与正式统计准备 | gpt-6.1-sol | 1h35m | 58m11s | 37m24s | 108 | 100% |
| C9E7D543 | W1 DNA final acceptance | gpt-6.1-sol | 1h10m | 1h00m | 9m56s | 118 | 100% |
| A51E36F8 | token-consumption-handoff | glm-5.3 | 19m11s | 19m08s | 0m02s | 44 | 100% |

（422AD44D 与 4A7B4FD2 为 fork 关系，早期时间线重叠，统计时勿直接相加。）

### 2. 活跃时间拆分（仅工具记录 100% 保留的会话，证据最硬）

| 会话 | 模型 | 活跃 | 模型思考/生成 | 工具执行 | 思考中位 | 思考最长 |
|---|---|---|---|---|---|---|
| 01249BDC | gpt-6.1-sol | 6h44m | 14m47s (**4%**) | 6h29m (96%) | 9s | 227s |
| 2C0A8EB9 | gpt-6.1-sol | 58m11s | 18m06s (31%) | 40m07s (69%) | 21s | 471s |
| C9E7D543 | gpt-6.1-sol | 1h00m | 8m43s (14%) | 51m30s (86%) | 26s | 135s |
| A51E36F8 | glm-5.3 | 19m08s | 13m23s (70%) | 5m45s (30%) | 18s | 175s |

关键样本：01249BDC（13h33m 挂钟、252 次工具调用）**96% 活跃时间是工具执行**，GPT 思考只占 4%。

### 3. 模型思考延迟分布（"工具结果→下一条助手消息"，剔除剪枝假间隔 >3600s）

| 模型 | 样本 | 中位 | p75 | p90 | 均值 |
|---|---|---|---|---|---|
| glm-5.3 | 33 | 17.6s | 28.8s | 44.2s | 24.3s |
| gpt-6.1-sol | 330 | 10.2s | 28.8s | **134.6s** | 118.8s |
| gpt-6-astra | 60 | 3.6s | 164.8s | **822.7s** | 246.3s |

结论：GPT 中位延迟并不慢（10s vs GLM 18s），**慢在长尾**：p90 达 2 分钟（sol）到十几分钟（astra）。全部 GPT 会话都开了 `effort=high` thinking（`acpModelParameterSelections`），放大了长尾。

### 4. "30–90 分钟才回复"的真相

多个会话存在看似 1900s–5463s 的"结果→回复"间隔，但这些会话工具记录保留率仅 2%–14%（retention 剪枝，`frozenDetailedToolTailLimit`）。这些长间隔内是**被剪掉的中间工具调用链**（状态轮询、测试、数据处理），不是模型干想。100% 保留的会话中"结果→回复"最长仅 471s。

### 5. 其他真实耗时来源（会话消息原文佐证）

- 后台实验本身跑数小时："1025 八条件消融实验已恢复…预计还需 4–7 小时"（CEC6003B，17:19 发出，31 分钟后回复）；GLM 15 块、1200+ 请求；360 份 PDF（7,255 页）生成。
- 流程阻塞：Paratera HTTP 403、macOS"文稿文件夹"权限拦截、配置故障整批作废重跑、预算确认点等待用户授权（AF79E34A/65BF2688 消息原文）。
- 等用户/过夜：空档最大 25h59m（AF79E34A）、18h38m（B796E6F4）、16h14m（4A7B4FD2），含 32389s（≈9h）、40922s（≈11.4h）整夜空档。

## Investigation Log

### Phase 1-2 - 数据源定位
**Hypothesis:** 对话 ID 属于某个本地会话存储。
**Findings:** 不在 OpenCode DB、不在 Codex；命中 RepoPrompt CE auto-research 工作区 AgentSessions 存档。
**Evidence:** `AgentSessionIndex.json`（135 条，11 个 ID 全部命中，其中 C8B53C93 为本次调查会话的 parentSessionID）。
**Conclusion:** 确认。

### Phase 3 - 时间口径校准
**Hypothesis:** turn 时长之和 = 活跃时间。
**Findings:** turn 求和会因 fork/并行重复计数（422AD44D 求和 77h > 挂钟 22h）；权威口径为 coveredTurnDuration + gaps ≈ wall（误差 <0.1%）。
**Evidence:** 各会话 `coveredTurnDurationSeconds` 与 `interActiveIntervalGapSeconds` 交叉验证。
**Conclusion:** 确认，采用索引口径。

### Phase 4 - 活跃时间拆分
**Hypothesis:** GPT 思考是耗时主因。
**Findings:** 100% 保留会话中思考占 4%–31%，工具执行 69%–96%；GPT 长尾 p90 135–823s 但中位仅 3.6–10.2s。
**Evidence:** 见上表 2、表 3（逐活动时间戳复算）。
**Conclusion:** 假设部分成立（长尾）、大部分证伪（主体耗时）。

## Root Cause

1. **主因（≈挂钟的 50%–85%）：等待**——等用户回复/授权、过夜挂机、后台实验运行。1023/1025 是 4 天跨度的多阶段实验交付，物理上就不可能"快"。
2. **次因（活跃时间的 69%–96%）：工具执行**——2300+ 次工具调用（bash 测试套件 30–150s/次、数据统计、PDF 生成）。
3. **GPT 的真实贡献：长尾思考**。`gpt-6.1-sol`/`gpt-6-astra` 均以 `effort=high` thinking 运行，p90 思考延迟 135s/823s，个别 turn 一次思考+长报告 2–8 分钟，叠加几十个 turn 后体感明显。但中位延迟与 GLM 相当（10s vs 18s），**不是每次回复都慢**。
4. **感知放大器**：retention 剪枝把几十分钟的工具链折叠成"一次很久才来的回复"，让人误以为模型在长时间思考。

## Recommendations

1. 判断"慢"时分开看：挂钟≠模型慢。用 `coveredTurnDurationSeconds`（活跃）与 `interActiveIntervalGapSeconds`（空档）拆分，见 `AgentSessionIndex.json`。
2. 对汇报/总结类 turn 降 thinking：`acpModelParameterSelections` 中 `effort=high` 仅留给攻坚 turn，汇报 turn 用 medium/low，可显著削 p90 长尾。
3. 重尾工具任务（如 01249BDC 的 252 次调用）应保持非 GPT 快模型跑批，GPT 留给分析/决策 turn。
4. 大空档（>1h）多为等待用户授权（预算确认点、权限）——预先给授权边界可消除最长的等待。

## Preventive Measures

- 会话级计时看板：新会话开始时记录 firstActivityAt，长任务按"等待/活跃"分账汇报，避免用挂钟误判模型性能。
- 后台实验类工作流设置自动轮询+唤醒（`autoWakeOnOversightUpdates`），减少人工 check-in 造成的空档。
- 长周期实验（4 天级）拆成明确的里程碑会话，每段独立计时。
