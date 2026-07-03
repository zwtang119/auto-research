# 知识写回闭环

> **定义**：推演产生的知识（因子、效应、策略）通过结构化写回沉淀到知识库，在下一次推演中注入——形成"推演→评估→写回→改善"的正反馈循环。

## 闭环流程

```
推演产生因子 → Factor Ledger 记录 → Brier 校准 → 知识写回
    → 再次推演（注入上轮知识）→ before/after 对比 → 量化改善幅度
```

## 评估指标

- 知识写回前后的 Brier Score 变化
- 因子可结算率（事件结算后有多少因子被验证正确）
- 知识注入是否减少了"重复发现已知因子"

## 相关页面

- [[concepts/factor-ledger]]: Factor Ledger 因子账本
- [[concepts/prediction-market-calibration]]: 校准方法论
