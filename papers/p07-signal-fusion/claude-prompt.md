# P2.1 Evidence Input Layer — Claude Code 启动指令

> 新定位 (2026-07-03)：本目录是 P1+P2 主线的 evidence input layer。
> 不再以"12 数据源融合"作为论文主张。生产者发出 `signal_evidence_entry`
> 行供下游 ledger 与 P1.2 settlement 消费。

先读 MEMORY.md，再读 `state/task_spec.md`、`state/io_spec.md` 与
`wiki/decisions/2026-07-03-evidence-input-configuration.md`。

## 启动

1. 读 `state/task_spec.md` + `state/progress.json`，找第一个未完成 milestone。
2. 按 evidence input layer 视角执行 M1→M5（实验）→ M6→M9（论文）：
   - M1-M2 → 基础搭建（确认 cds-keyperson 数据源可拉取；不重写融合算法）
   - M3 → Gate 2：4 条件 × 100 MC = 400 runs；产出 `experiments/signals/*.jsonl`
   - M4 → 消融：逐组移除数据源，各 50 runs，写入 `experiments/ablation/`
   - M5 → 偏差检测 side-channel；`significance_tested: false`
   - M6 → Gate 3：LaTeX 编译
   - M7 → Deep Improvement：≥6 figures + ≥10 tables
   - M8 → Gate 4：多轮 peer review
   - M9 → 零报错
3. 每次完成更新 `state/progress.json` + `state/findings.jsonl` + `state/iteration_log.jsonl`。
4. 连续 2 次卡住 → 换策略，记录到 `state/directions_tried.json`。

## 输出契约（必读）

- 写 `signal_evidence_entry` 行（schema 见 `state/io_spec.md §2`），不是融合文本。
- 每个 row 必须带：`source_independence`、`independence_class`、`supporting_signals`、
  `contradicting_signals`、`freshness_window`、`freshness_ratio`、`audit_trace`。
- `numeric_forecast` 必须是 `[0, 1]` 或 `null`；文本预测不是概率。
- 冲突发现：发现矛盾时同时输出两行 + 一条 `weak_evidence` summary 行。
- 偏差检测走 side-channel（`bias_signal_*`），不写入 `signal_evidence_entry`。

## 约束

- **零交互**（PIT-011）。除明确的 paper-review 节点外不向用户提问。
- 状态文件是唯一真相源。
- 代码只读：`../../cds-keyperson/src/backend/services/`（267 行 chain，**作为实现细节，不作为研究主张**）+ `../../cds-keyperson/src/backend/datasources/`（12 源，polymarket INACTIVE 必须过滤）。
- **上下文管理**：~40 轮后写 `state/checkpoint.md` 并重启（PIT-010）。
- 单轮最多读 5 个大文件；单文件不超过 300 行。

## 数据源分组（3 组，predetermined）

- Group A "Market Signals"：finance(YahooFinance+Binance), macro(WorldBank), energy(Energi)
- Group B "Event Intelligence"：geopolitics(GDELT+IFRCGO), sanctions(OFAC), news(RSS), aviation(OpenSky+Celestrak)
- Group C "Reference Knowledge"：academic(OpenAlex), wikipedia, weather(OpenMeteo), sports(TheSportsDB)

## 必避陷阱

- PIT-401：不主张 novel fusion algorithm。
- PIT-402：偏差检测不写 `p < 0.05`；`significance_tested: false`。
- PIT-403：polymarket 必须排除。
- PIT-405：4 条件 × 100 runs = 400 行；运行后用 `jq` 校验行数。
- PIT-406 / PIT-302：文本预测不是概率。
- PIT-408：free-text trace 不是 signal；`signal_type` 必须落在 4 值 enum。

## 论文主张（禁止 / 允许）

- **禁止**："novel fusion algorithm"、"thin engineering paper"
- **允许**："ablation protocol for evidence coverage"、
  "bias-detection contract with `significance_tested: false`"、
  "evidence-ledger adapter for P1+P2 mainline"

## 上下文入口

- `state/task_spec.md` — 任务与 milestone
- `state/io_spec.md` — IO 契约与 validator 表达式
- `wiki/index.md` — 知识库索引
- `wiki/concepts/signal-to-evidence-contract.md` — 契约叙述版
- `wiki/decisions/2026-07-03-evidence-input-configuration.md` — 本次重新配置决策
- `paper/outline.md` — 论文大纲（按 evidence input 视角写）
- `../../../framework/schemas/experiment-pitfalls.md` §5 — P2.1 陷阱清单
