# Factor Ledger 因子账本

> **定义**：从推演数据中自动提取"关键因子"（哪些决策节点改变了事件走向）的系统化数据库，支持预注册（事前声明因子）和结算（事后验证因子）。

## 四类因子

| 类型 | 定义 | 示例 |
|------|------|------|
| **前兆因子** | 事前能预警的信号 | "WTI 价格跌破 $60" |
| **抑制因子** | 能阻止事件恶化的措施 | "OPEC+ 宣布减产" |
| **分支因子** | 导致走向分叉的决策点 | "美联储加息 vs 降息" |
| **反证因子** | 事后证明判断错误的信号 | "地缘冲突未如预期升级" |

## 当前状态

⚠️ 设计文档完整（cds4polymarket concept doc 81行），**Python 代码 0 行实现**。需在实验中按设计评估因子。

## 预注册与结算协议

来自 cds4worldcup 的成熟协议：
- YAML 格式：`factor_id/origin/event_relation/observable_proxy/settlement_rule`
- Multi-Judge 裁决框架（4角色：证据/校准/怀疑/知识裁判）

## 相关页面

- [[concepts/prediction-market-calibration]]: 校准方法论
- [[decisions/factor-evaluation]]: 评估方法决策
