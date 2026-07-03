# 课题五 AutoResearch 新路线图

> 日期：2026-07-03  
> 目标：优先写出 60 分可发表论文；若出现清晰结构性突破，再冲击更高分论文。  
> 基准：`Towards a Science of Scaling Agent Systems` 是 100 分级参照，不作为短期硬目标。  
> 本路线图替代 `topic5-research-directions.md` 中关于 P11 为 Tier 1 主线的旧判断；旧文档保留为历史规划。

## 1. 总判断

本项目当前最大的瓶颈不是实验数量，而是选题与执行闭环。P11 内心独白已经产生有价值结果，但继续修补主论文的边际收益低。新的主线应从“让 Agent 多想 / 多说”转为“让 Agent 的证据、判断、校准和回写可验证”。

更新后的路线：

1. **P11 快速收口**：作为负结果、方法论案例和 P12 数据来源，不再作为主论文大修。
2. **P12 Judge 校准优先启动**：最适合快速形成 60 分短论文或 workshop 论文。
3. **P1+P2 合并为高上限主线**：以 evidence-structured emergency decision intelligence 为核心，而不是单独证明 RAG 或信号融合。
4. **P8 作为外部结算层并入主线**：用 prediction market / historical settlement 提供 Brier、Log Loss、factor settlement 与写回验证。
5. **P7/P2.1 仅在升级为 evidence topology 后继续**：普通 signal fusion 不足以支撑优秀论文。

## 2. AutoResearch 执行原则

本路线图必须尽量使用 AutoResearch 提效，但要使用它的“控制论版本”，而不是让 agent 无限尝试。

### 2.1 必须采用的状态文件协议

根目录维护 portfolio 层状态：

- `state/task_spec.md`：组合目标、里程碑、成功标准。
- `state/progress.json`：当前主线、迭代号、停滞计数、活跃任务。
- `state/findings.jsonl`：跨项目发现，append-only。
- `state/directions_tried.json`：已尝试方向，防止认知循环。
- `state/iteration_log.jsonl`：每次迭代的结果摘要。
- `logs/orchestrator.jsonl`、`logs/work.jsonl`、`logs/heartbeat.jsonl`：三类日志分离。

每个子项目继续保留自己的 `state/`、`logs/`、`wiki/`、`paper/` 与 `experiments/`。根目录只做组合决策，不吞并子项目证据。

### 2.2 停滞与 pivot 规则

- 单个方向连续 2 轮无新发现，或审稿分数 / 关键指标下降：`stale_count += 1`。
- `stale_count >= 2`：必须 pivot 结构约束，不能只改 prompt 或写法。
- `stale_count >= 4`：停止自动循环，写明 blocked reason，不再消耗实验预算。
- 单轮 work agent 最多读 5 个大文件；单文件超过 300 行时只读相关片段。
- 每轮必须有可验证产物：数据文件、分析文件、论文段落、审稿记录或决策文档。

### 2.3 论文写作 Gate

采用 AutoResearch paper-writing skill group 的五类分工：

| 子技能 | 用途 | 本项目对应 |
|---|---|---|
| Literature Survey | 文献搜索、引用分级、DBLP/来源核查 | P12 与 P1+P2 的相关工作 |
| Paper Structure & Logic | 论文结构、claim 链、摘要结论对齐 | 每条论文线的核心叙事 |
| Experiment Design | 假设、变量、对照、统计检验 | P12 viability 与 P1+P2 主实验 |
| Figures & Tables | 高信息密度图表 | 消融、校准、factor ledger、settlement |
| Peer Review Simulation | 五人格评审、弱项路由 | 每个里程碑后的停/走判断 |

Gate 采用适配版：

| Gate | 最低要求 | 用途 |
|---|---|---|
| Gate 1 Literature | 关键文献覆盖；新近文献与正式版本核查；避免堆引用 | 防止故事落后 |
| Gate 2 Experiment | 明确 hypothesis、control、stat test、最小样本 | 防止只写概念 |
| Gate 3 Structure | LaTeX 可编译或 markdown 结构完整；abstract-conclusion 对齐 | 防止散文式 paper |
| Gate 4 Figures | 至少有核心表/图支撑 claim | 防止无图无证据 |
| Gate 5 Review | R1-R5 五类 reviewer 中位分；binding weakness 必须路由 | 防止自嗨 |

## 3. 项目组合排序

| Rank | 方向 | 当前状态 | 决策 |
|---|---|---|---|
| 1 | **P12 Judge 校准** | 根目录尚无独立目录；证据来自 P11 label leakage 与外部文献 | 新建为短期主任务 |
| 2 | **P1+P2 Evidence RAG + Factor Ledger** | P1/RAG 仍在规划；P2.1 signal fusion 有初始化 state | 作为高上限主论文设计 |
| 3 | **P8 / P1.2 Market calibration** | `p1.2-market-calibration_*` 已初始化 | 改为 settlement/calibration layer |
| 4 | **P7 / P2.1 Signal fusion** | `p2.1-signal-fusion_*` 已初始化 | 仅作为 evidence topology 的输入层 |
| 5 | **P11 Inner monologue** | Mimo 与 Minimax-M3 均有完整数据和 synthesis | 收口，不再大修主线 |

## 4. P11 收口路线

### 4.1 决策

P11 不再追求 main conference 级主论文。它的最佳用途是：

- P12 的 judge calibration 案例库。
- P1+P2 主论文中的反例 / appendix。
- workshop 或短论文：“inner monologue 是 process signal，不是 fidelity lever”。

### 4.2 两日任务

1. 冻结 P11 新实验，除非是 P12 需要的小样本复核。
2. 整理五个可复用结果：
   - H1 blind 后失败。
   - label leakage 导致 false positive。
   - H1c reasoning depth 通过。
   - H3 risk_tolerance 到 risk-taking 稳健。
   - pure analysis 在 group emergence vocabulary 上超过 inner monologue。
3. 在 P11 state 中记录 `CLOSED_AS_MAINLINE_REUSED_FOR_P12`。
4. 将 P11 paper 目标改为 workshop / appendix / method case，不再进入 8.5 循环。

### 4.3 停止条件

如果 P11 的新修改不能直接服务 P12 或 P1+P2，不做。

## 5. P12 快速论文路线

### 5.1 论文问题

> 如何校准 LLM judge，使它不被标签泄漏、自信幻觉、错误一致性和不当弃答机制误导？

建议题目方向：

> Calibrating LLM Judges for Agent Reliability: Blind Pairwise Evaluation, Neighborhood Probes, and Abstention-Aware Scoring

中文描述：

> 面向 Agent 可靠性的 LLM 裁判校准：盲评、邻域探针与弃答感知评分。

### 5.2 最小可行实验

使用 P11 现有样本，不开大规模新实验：

1. **Label leakage test**：对比显式 condition 标签 vs blind judge。
2. **Pairwise blind test**：同一输出成对比较，减少绝对分漂移。
3. **NCB-style neighborhood probes**：围绕角色行为、事实前提、决策后果生成邻域问题。
4. **Consistency-on-wrong**：同一错误在 paraphrase 下是否稳定复现。
5. **Abstention-aware score**：允许 judge 标记 insufficient evidence，而不是强行评分。

### 5.3 3-6 天 Gate

| 天数 | 产物 | Gate |
|---|---|---|
| Day 1 | P12 task dir + task_spec + sample manifest | 样本可复现 |
| Day 2 | blind / leaked / pairwise judge harness | 能复现 P11 label leakage |
| Day 3 | neighborhood probe schema + 小样本结果 | 至少 30-50 个样本 |
| Day 4 | calibration metrics 表 | 能区分 false positive 与 stable signal |
| Day 5 | 4 页短文结构 | 贡献清楚 |
| Day 6 | 五人格 review | 中位分 >= 6.0 则写短论文；否则并入 P1+P2 |

### 5.4 成功标准

- 能清楚复现：label-aware judge 高估某个 condition。
- blind / pairwise / neighborhood probe 至少一种方法能显著降低 false positive。
- 有一张核心表：不同 judge protocol 对 H1/H1c/H3/F1 的结论差异。
- R2 theorist 不再能说“只是工程清洗”，因为有明确 reliability metric。

## 6. P1+P2 高上限主线

### 6.1 论文问题

> 在灾害应急多 Agent 决策中，是否可以通过结构化证据账本，把 RAG、信号融合、因子提取、外部结算连接成可验证的决策智能？

建议题目方向：

> Evidence-Structured Agent Decision Making for Emergency Response

中文描述：

> 面向应急响应的证据结构化 Agent 决策。

### 6.2 关键变化

不要把 P1 写成“接入知识库后效果更好”。这太像应用工程。

应改成：

> Agent 的每个关键判断都必须落到 factor ledger：有哪些支持证据、冲突证据、缺失前提、来源独立性、时效性、权威性、适用条件，以及可结算的验证规则。

### 6.3 最小 schema

每条决策 / claim 至少包含：

- `claim_id`
- `decision_context`
- `supporting_evidence[]`
- `contradicting_evidence[]`
- `missing_prerequisites[]`
- `source_independence`
- `freshness`
- `authority`
- `applicability`
- `factor_type`
- `settlement_rule`
- `observed_outcome`
- `confidence_before`
- `confidence_after`
- `audit_trace`

### 6.4 与已有目录的关系

- `papers/p07-signal-fusion`：作为 evidence input layer，不单独主打 feature fusion。
- `papers/p08-market-calibration`：作为 settlement/calibration layer，补 Brier/Log Loss 与 factor evaluability。
- P11：作为 “free-text reasoning trace 不足以承担证据结构” 的反例。

### 6.5 两周 Gate

| 周期 | 产物 | 停/走标准 |
|---|---|---|
| Day 1-2 | factor ledger schema + 10 条手工样例 | 专家/agent 能读懂；字段不空泛 |
| Day 3-5 | Gulei 或 Polymarket settlement 映射 | 至少 30 个 claim/factor 可结算 |
| Day 6-8 | baseline vs evidence-ledger 对照实验设计 | control 清楚，不依赖 judge 单点评分 |
| Day 9-11 | 小样本 pilot | 方向性改善或错误暴露明确 |
| Day 12-14 | 五人格 review + paper outline | 中位分 >= 6.5 继续；否则退回 P12 短论文 |

## 7. P8 / P1.2 的新定位

P1.2 原来是“预测市场校准 LLM Agent”。现在应降维为 P1+P2 的外部结算层，同时保留独立短论文可能。

### 必做修复

1. 实现自动 Brier / Log Loss 计算。
2. 明确 event selection 人工 checkpoint 只保留一次。
3. 把 Factor Ledger 从概念文档推进到最小可用 JSON/CSV。
4. 将 “knowledge writeback” 改写为 “belief update with settlement evidence”，避免像记忆写回的产品功能。

### 独立成文条件

只有当它能证明以下一点时，P1.2 才单独写：

> prediction market settlement 可以稳定校准 agent 的 factor-level belief update。

否则并入 P1+P2。

## 8. P7 / P2.1 的新定位

P2.1 不应再以“12 数据源融合”作为主贡献。原因是现有 SignalFusionEngine 只有 267 行，算法是 recency + direction weighting，容易被评审认为是薄工程。

继续条件：

- 输出不再是 fused text，而是 evidence ledger entries。
- 每个 source group 的贡献用 source independence / conflict discovery / freshness improvement 衡量。
- Ablation 不只看“决策质量分数”，还看 evidence coverage、conflict detection、settlement accuracy。

如果做不到，就只作为 P1+P2 的输入模块。

## 9. 目录组织规范

根目录只保留组合级入口：

```text
auto-research/
├── README.md
├── topic5-research-directions.md          # 历史路线图
├── docs/
│   ├── roadmaps/                          # 新路线图
│   ├── portfolio/                         # 项目组合索引
│   ├── investigations/                    # 调研报告
│   └── autoresearch/                      # AutoResearch 协议/运行材料
├── state/                                 # portfolio 层 AutoResearch 状态
├── logs/                                  # portfolio 层日志
├── legacy/p11-legacy-snapshot-2026-07*/                 # P11 历史/收口
├── p1.2-market-calibration*/              # P8 / settlement layer
├── p2.1-signal-fusion*/                   # P7 / evidence input layer
└── victorchen96.github.io/                # AutoResearch 参考资料
```

暂不移动实验目录内部文件。内部路径可能被 harness、LaTeX、wiki 引用，强行迁移收益低、风险高。

## 10. 近期执行清单

### 本周

1. 新建 P12 目录与 AutoResearch state。
2. 冻结 P11 主线，写 closure status。
3. 从 P11 抽取 judge calibration 样本 manifest。
4. 运行 P12 3-6 天 viability probe。

### 下周

1. 若 P12 成功：写 4-6 页短论文，目标 workshop / findings-style。
2. 同时设计 P1+P2 factor ledger schema。
3. 将 P1.2 的 Brier/Log Loss 自动计算补齐。
4. 将 P2.1 输出改造成 evidence ledger input。

### 两周后

1. P12 中位 review >= 6.0：进入短论文打磨。
2. P1+P2 pilot 中位 review >= 6.5：作为主论文继续。
3. 两者都失败：停 AutoResearch，重新做选题，而不是继续堆实验。

## 11. 反通胀规则

- 第一轮 review 上限 7.0。
- 每轮最大涨幅 +1.5。
- 必须保留至少 1 个 unresolved weakness。
- 中位分优先于平均分。
- R2 theorist 或 R1 experimentalist 的 binding weakness 必须先处理。
- 外部引用、实验数字、数据文件必须可追溯；发现错误时分数可以下降。

## 12. 最终建议

当前最理性的策略不是继续悲观，也不是被乐观建议带着跑，而是把项目变成一个可停止、可 pivot、可验证的组合系统：

- **P11：收口。**
- **P12：快速试，能写就写。**
- **P1+P2+P8：作为真正高上限主线。**
- **P7：降级为输入模块，除非升级成 evidence topology。**

这一路线最大化 AutoResearch 的优势：快速并行阅读、自动复核、审稿驱动、状态文件闭环；同时限制它的弱点：无限循环、虚高评分、路径振荡和无证据扩写。
