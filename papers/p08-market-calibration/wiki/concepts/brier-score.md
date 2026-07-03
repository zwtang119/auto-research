# Brier Score

> **定义**：预测准确度的概率评分函数。Brier = (1/N) × Σ(p_i - o_i)²，其中 p_i 是预测概率，o_i 是实际结果（0或1）。0=完美，1=全错，0.25=瞎猜。

## 当前状态

⚠️ Schema 已定义（YAML 中有手工计算值），**Python 自动计算函数不存在**。M1.5 需要实现 `calc_brier.py`（~50行）。

## 在实验中的应用

- 对比 Agent 推演概率 vs Polymarket 市场共识概率
- 事件结算后计算标准化 Brier Score
- 作为知识注入改善效果的量化指标

## 相关页面

- [[concepts/prediction-market-calibration]]: 校准方法论
- [[decisions/brier-implementation]]: 实现方案
