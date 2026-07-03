# A/B 测试框架

> **定义**：cds4polymarket 的 A/B 测试系统，用于对比知识注入 vs 无知识注入的 Agent 推演质量。

## 规模

- 15+ 轮 AB 测试（v02-v16，27个实验目录）
- 6 领域 × 1 问题/领域
- Gold-H/M/L 三锚定样本用于 Judge 漂移检测

## Judge 校准

`calibration_lib.py:34-38` 定义了 3 个黄金样本（Gold-H 高质量、Gold-M 中等、Gold-L 低质量），用于周期性地检测 LLM Judge 的评分是否"跑偏"。

## 相关页面

- [[concepts/prediction-market-calibration]]: 校准方法论
- [[annotations/ab-test-rounds]]: AB 测试各轮分析
