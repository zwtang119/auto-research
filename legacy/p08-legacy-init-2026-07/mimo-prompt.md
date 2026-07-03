## Goal
按 state/task_spec.md 的 Milestone 顺序自动完成 M1→M5，然后走论文阶段 M6→M9。
每完成一个里程碑：更新 progress.json 的 completed_milestones，追加 findings.jsonl 和 iteration_log.jsonl。

## ⚠️ 唯一的人工检查点
**M2 完成后暂停**：将 event_candidates.json 写入 state/，并在 state/blocked.md 中写 "M2 complete, awaiting human review of top-5 case study candidates"。
这是全程唯一一次等待人工，之后 M3-M9 全自动零交互。

## 工作方式
1. 先读 state/task_spec.md 和 state/progress.json，找到第一个未完成 milestone
2. 对每个 milestone：读 Deliverable + Auto-verifiable → 执行 → 自检 → 通过后写回 state
3. 连续 2 次卡住：换策略重试（记录到 state/directions_tried.json）
4. **Stale Detection**：stale_count ≥ 2 → pivot（改事件筛选标准、扩展领域）；≥ 4 → 写 state/blocked.md 标记需要人工
5. 论文阶段（M6-M9）：
   - M6 Draft：LaTeX 编译通过，≥20 篇 refs
   - M7 Deep Improvement：≥6 figures + ≥10 tables，abstract-conclusion 对齐
   - M8 Sprint：≥3 轮同行评审，记录 score trajectory
   - M9 Final：零 LaTeX 报错

## 关键约束
- 进度只通过 state/ 文件传递
- logs/ 三流日志：heartbeat / orchestrator / work
- 实验输出写入 experiments/（metrics tables、calibration results、Brier/Log Loss 计算）

## 依赖
- cds4polymarket A/B 测试数据：../../cds4polymarket/ab-test/experiments/（27 个实验目录，只读）
- 综合分析报告：../../cds4polymarket/ab-test/analysis/CDS_AB_Test_17轮综合分析报告.md（只读）
- 校准库：../../cds4polymarket/calibration_lib.py（只读）
- Judge 校准 Gold 样本：calibration_lib.py:34-38（H/M/L，3 个）
- Polymarket API：公开端点，无需额外 Key
- LLM（DeepSeek-V4）：通过 ../../cds4polymarket/.env 读取

## 已知缺口（task_spec.md 已记录，不隐藏）
- Brier/Log Loss：Schema 已有，Python 自动计算函数不存在 → M1.5 需实现 calc_brier.py (~50 行)
- Factor Ledger：设计文档完整（81 行），0 行 Python 代码 → M3 手动按设计评估
- Polymarket API：仅 /events 端点，每领域最多 5 个事件，15s 超时
