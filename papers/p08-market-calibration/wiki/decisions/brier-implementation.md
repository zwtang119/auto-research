# Brier 计算实现

> **类型**：decision | **状态**：accepted | **日期**：2026-07

## 决策
实现 `calc_brier.py`（~50 行）用于自动计算 Brier Score。当前 Schema 已定义，YAML 中有手工值，Python 计算函数不存在。

## 设计方案
- 输入：预测概率列表 + 实际结果列表
- 输出：Brier Score（0-1）+ Log Loss
- 支持按领域、按事件类型分组统计

## 相关页面
- [[concepts/brier-score]]: Brier Score 定义
