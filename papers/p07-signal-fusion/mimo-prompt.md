## Goal
按 `state/task_spec.md` 的 Milestone 顺序自动完成 M1→M5（实验），然后走论文阶段 M6→M9。
本目录定位 (2026-07-03)：**evidence input layer**，生产 `signal_evidence_entry` 行供下游
`papers/p1p2-evidence-ledger/` 与 `papers/p08-market-calibration/` 消费。
每完成一个里程碑：更新 `progress.json` 的 `completed_milestones`，追加 `findings.jsonl` 和 `iteration_log.jsonl`。
全程零交互——遇到阻塞写到 `state/blocked.md`。

## 工作方式
1. 先读 `state/task_spec.md`、`state/io_spec.md`、`state/progress.json`，
   以及 `wiki/decisions/2026-07-03-evidence-input-configuration.md`，找到第一个未完成 milestone。
2. milestones 与 Quality Gate 映射：
   - M1-M2 → 基础搭建（确认 12 数据源可拉取；不重写融合算法）
   - M3 → **Gate 2 (Experiment)**：4 条件 × 100 MC 推演 = 400 runs；写 `experiments/signals/*.jsonl`
   - M4 → 消融实验（逐组移除数据源，各 50 runs，写 `experiments/ablation/`）
   - M5 → 偏差检测 side-channel（`bias_signal_*`，`significance_tested: false`）
   - M6 → **Gate 3 (Structure)**：LaTeX 编译通过
   - M7 → Deep Improvement：≥6 figures + ≥10 tables
   - M8 → **Gate 4 (Final Review)**：多轮同行评审
   - M9 → 零 LaTeX 报错
3. 连续 2 次卡住 → 换策略（记录到 `state/directions_tried.json`）。
4. 所有进度通过 `state/` 文件传递，`logs/` 三流记录。

## 实验设计（evidence input layer 视角）

**4 条件（各 100 runs）**:
- Condition A: 无外部数据（LLM-only 基线）— 验证 evidence 缺失时的下行影响
- Condition B: 原始未融合数据（12 源 unstructured）— 验证结构化的边际价值
- Condition C: 融合信号（lens weights + 3-scenario forecast）— 内部实现细节
- Condition D: 融合信号 + 偏差诊断（C + calibrator side-channel）

**消融**（Condition C，各 50 runs）:
- Full(12 源) → 移除 Group A → 移除 Group B → 移除 Group C
- 度量：freshness_ratio 分布、冲突发现数、source_independence 中位数
  （不再以"历史吻合度"为单一指标；见 `state/io_spec.md §5`）

**成功标准**:
- `signal_evidence_entry` 行通过 §2.2 的全部 validator（PIT-403/408/206/203）
- ≥1 个数据源组移除导致 downstream `source_independence` 中位数下降 ≥1
- 偏差检测 side-channel 行带 `significance_tested: false`（PIT-402）
- 论文编译零报错；论文**不主张** novel fusion algorithm（PIT-401）

## 输出契约（必读）

- 写 `signal_evidence_entry` 行，schema 见 `state/io_spec.md §2`。
- 必填字段：`source_independence`, `supporting_signals`, `contradicting_signals`,
  `freshness_window`, `freshness_ratio`, `audit_trace`。
- `numeric_forecast` ∈ `[0, 1]` 或 `null`；文本预测不是概率（PIT-302 / PIT-406）。
- `datasource_status` 必须 `"active"`；polymarket 一律过滤（PIT-403）。
- `signal_type` ∈ `{confirmed_fact, weak_evidence, missing_data, source_failure}`（PIT-408）。
- `audit_trace` 是结构化数组，每项含 `tool` + `*_sha256_prefix`（PIT-206）。

## 依赖
- cds-keyperson SignalFusionEngine：../../cds-keyperson/src/backend/services/（只读，作为实现细节）
  - signal_normalizer.py (48 行) + fusion_engine.py (71 行) + forecaster.py (62 行) + calibrator.py (86 行) + forecast_pipeline.py (160 行)
- 12 个数据源：../../cds-keyperson/src/backend/datasources/（只读，polymarket INACTIVE 跳过）
- LLM（DeepSeek-V4 / MiniMax-M3）：通过 ../../cds-keyperson/.env 读取

## 已知限制（task_spec.md 已记录，不在本次重写）
- SignalFusionEngine 总计 267 行（+pipeline 427 行），算法简单（recency 线性插值 + 方向加权）
- Forecaster 输出文本描述而非数值概率，与 Brier/Log Loss 校准不直接兼容（PIT-302）
- Calibrator 仅 2.0x 比率偏差检测，无统计检验（PIT-402）
- 旧版 Group D（emergency/environment/culture）已废弃，使用修订后的 3 组（A/B/C）

## 数据源分组（predetermined，与 progress.json 一致）
- Group A "Market Signals"：finance(YahooFinance+Binance), macro(WorldBank), energy(Energi) → 5 sources
- Group B "Event Intelligence"：geopolitics(GDELT+IFRCGO), sanctions(OFAC), news(RSS), aviation(OpenSky+Celestrak) → 7 sources
- Group C "Reference Knowledge"：academic(OpenAlex), wikipedia, weather(OpenMeteo), sports(TheSportsDB) → 4 sources

## 必避陷阱（来自 ../../framework/schemas/experiment-pitfalls.md §5）
- PIT-401：论文不主张 novel fusion algorithm
- PIT-402：偏差检测不写 `p < 0.05`
- PIT-403：polymarket 必须过滤
- PIT-404：primary metric 必须 pre-register（`experiments/primary_metric.md`）
- PIT-405：MC 输出行数必须 400
- PIT-406 / PIT-302：文本预测不是概率
- PIT-407：MemoryLayer 数量 6（不是 5）
- PIT-408：free-text trace 不是 signal
