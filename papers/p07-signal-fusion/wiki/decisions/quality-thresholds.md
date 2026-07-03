# 质量阈值设定
> **类型**：decision | **状态**：accepted

## 决策
- Recency 衰减：7天半衰期
- 方向加权系数：1.2（单方向一致）
- 比率偏差：2.0x（超出历史均值标记为偏差）
- 信号置信度阈值：confirmed ≥0.8, weak ≤0.5, missing ≤0.3

## 相关页面
- [[concepts/information-quality-metrics]]: 质量度量
