# 角色一致性

> **定义**：Agent 在推演中的行为与其 RoleDNA 5维行为基因的匹配程度。

---

## RoleDNA 五维行为基因

| 维度 | 字段 | 含义 | 评分 |
|------|------|------|:--:|
| **风险偏好** | `risk_tolerance` | 冒险 vs 保守 | 1-5 |
| **时间偏好** | `time_preference` | 短期 vs 长期 | 1-5 |
| **市场权力** | `market_power` | 资源控制力 | 1-5 |
| **政策敏感度** | `policy_sensitivity` | 对政策信号响应 | 1-5 |
| **协同风格** | `coordination_style` | 合作 vs 竞争 | 1-5 |

## LLM Judge 评分

LLM Judge 对每轮每个 Agent 各评估 5 个维度（1-5分），取均值作为 Fidelity Score。

## 相关页面

- [[concepts/inner-monologue-methodology]]: 内心独白方法论
- [[concepts/hypotheses]]: H1 Fidelity 假设
- [[decisions/judge-selection]]: LLM Judge 选型
