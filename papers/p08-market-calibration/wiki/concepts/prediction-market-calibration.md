# 预测市场校准方法论

> **定义**：使用真实资金驱动的预测市场（Polymarket）作为 LLM Agent 推演的外部校准场——事件结算后即有明确对错，可验证 Agent 知识注入是否真正改善了推理质量。

## 核心创新

LLM Agent 评估是当前 AI 研究热门难题——缺乏可靠外部标准。预测市场天然是校准场：真金白银产生的概率比 AI"猜"出来的更可信。

## 实验流程

1. 知识注入 → Agent 推演 WTI 原油等事件
2. 推演结果 vs Polymarket 市场共识（Brier Score 对比）
3. 事件结算 → 因子可结算率评估
4. 知识写回 → before/after 对比
5. 6领域跨域稳健性分析

## 数据来源

cds4polymarket 的 15+ 轮 AB 测试数据（27个实验目录，v02-v16），Polymarket Gamma API。

## 相关页面

- [[concepts/brier-score]]: Brier Score 定义与计算
- [[concepts/factor-ledger]]: Factor Ledger 因子账本
- [[concepts/knowledge-writeback]]: 知识写回闭环
- [[concepts/ab-test-framework]]: A/B 测试框架
- [[concepts/cds-background]]: CDS S5 知识有效性
