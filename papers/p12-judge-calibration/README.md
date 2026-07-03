# P12 Judge Calibration

P12 是当前组合路线中的短期优先任务：用 P11 的 label leakage、blind judging、pairwise judging 和 neighborhood probes，形成一个可快速验证的 LLM judge 校准方法。

## 目标

在 3-6 个有效工作日内回答：

> blind / pairwise / neighborhood / abstention-aware judge protocol 能否纠正 P11 中出现的 false-positive 结论？

## 入口

- 任务定义：`state/task_spec.md`
- 进度：`state/progress.json`
- 发现：`state/findings.jsonl`
- 方向历史：`state/directions_tried.json`
- 迭代日志：`state/iteration_log.jsonl`

## 数据来源

主要复用：

- `../legacy/p11-closed-v5-minimax-m3/experiments/`
- `../legacy/p11-closed-v5-minimax-m3/wiki/decisions/blind-judge.md`
- `../legacy/p11-closed-v5-minimax-m3/wiki/decisions/2026-07-03-structural-intelligence-reassessment.md`

## 非目标

- 不重新大规模跑 P11。
- 不把 P12 做成无穷 meta-evaluation。
- 不依赖 producer model 的自报 confidence。
