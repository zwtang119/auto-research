## Goal
按 state/task_spec.md 的 Milestone 顺序自动完成 M1→M5（实验），然后走论文阶段 M6→M9。
每完成一个里程碑：更新 progress.json 的 completed_milestones，追加 findings.jsonl 和 iteration_log.jsonl。
全程零交互——遇到阻塞写到 state/blocked.md。

## 工作方式
1. 先读 state/task_spec.md 和 state/progress.json，找到第一个未完成 milestone
2. milestones 与 Quality Gate 映射：
   - M1-M2 → 基础搭建（提取 SignalFusionEngine、Gulei 场景数据采集）
   - M3 → **Gate 2 (Experiment)**：4 条件 × 100 MC 推演 = 400 runs
   - M4 → 消融实验（逐组移除数据源，各 50 runs，ANOVA）
   - M5 → 偏差检测验证（Calibrator 混淆矩阵，准确率 ≥ 80%）
   - M6 → **Gate 3 (Structure)**：LaTeX 编译通过
   - M7 → Deep Improvement：≥6 figures + ≥10 tables
   - M8 → **Gate 4 (Final Review)**：多轮同行评审
   - M9 → 零 LaTeX 报错
3. 连续 2 次卡住 → 换策略（记录到 state/directions_tried.json）
4. 所有进度通过 state/ 文件传递，logs/ 三流记录

## 实验设计

**4 条件（各 100 runs）**:
- Condition A: 无外部数据（LLM-only 基线）
- Condition B: 原始未融合数据（12 源 unstructured）
- Condition C: 融合信号（lens weights + 3-scenario forecast）
- Condition D: 融合信号 + 偏差诊断（C + calibrator 输出）

**消融**（Condition C，各 50 runs）:
- Full(12 源) → 移除 Group A → 移除 Group B → 移除 Group C
- 度量：Δ 历史吻合度, resource utilization, response time

**成功标准**:
- 融合信号 > 原始数据，p < 0.05
- ≥1 个数据源组移除导致决策质量下降 ≥20%
- Calibrator 偏差检测准确率 ≥ 80%
- 论文编译零报错

## 依赖
- cds-keyperson SignalFusionEngine：../../cds-keyperson/src/backend/services/（只读）
  - signal_normalizer.py (48 行) + fusion_engine.py (71 行) + forecaster.py (62 行) + calibrator.py (86 行) + forecast_pipeline.py (160 行)
- 12 个数据源：../../cds-keyperson/src/backend/datasources/（只读，polymarket 标记 INACTIVE 跳过）
- LLM（DeepSeek-V4）：通过 ../../cds-keyperson/.env 读取

## 已知限制（task_spec.md 已记录）
- SignalFusionEngine 总计 267 行（+pipeline 427 行），算法简单（recency 线性插值 + 方向加权）
- Forecaster 输出文本描述而非数值概率，与 Brier/Log Loss 校准不直接兼容
- Calibrator 仅 2.0x 比率偏差检测，无统计检验
- 旧版 Group D（emergency/environment/culture）已废弃，使用修订后的 3 组（A/B/C）

## 数据源分组（修订版，与 progress.json 一致）
- Group A "Market Signals"：finance(YahooFinance+Binance), macro(WorldBank), energy(Energi) → 5 sources
- Group B "Event Intelligence"：geopolitics(GDELT+IFRCGO), sanctions(OFAC), news(RSS), aviation(OpenSky+Celestrak) → 7 sources
- Group C "Reference Knowledge"：academic(OpenAlex), wikipedia, weather(OpenMeteo), sports(TheSportsDB) → 4 sources
