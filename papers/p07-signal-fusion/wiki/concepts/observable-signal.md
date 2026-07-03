# 可观测信号

> **定义**：4 种结构化的数据质量信号类型，确保 Agent 知道每条信息的可靠性。

| 信号类型 | 置信度 | 含义 |
|------|:--:|------|
| `confirmed_fact` | 0.8-0.9 | 多源交叉验证的事实 |
| `weak_evidence` | 0.4-0.5 | 单源或弱来源信息 |
| `missing_data` | 0.3 | 该领域数据缺失 |
| `source_failure` | 0.9 | 数据源不可用（网络故障/限流） |

## 强制不变量

来自 cds-keyperson 的 Step 15k 可观测数据层：
- `source_failure` → 禁止输出负面结论
- `missing_data` → 标记 "未知"
- `weak_evidence` → 低置信度标记
- 100% 覆盖率要求

## 相关页面

- [[concepts/signal-fusion-pipeline]]: 融合管线
- [[concepts/information-quality-metrics]]: 质量度量
