# 内心独白方法论

> **定义**：通过让 LLM Agent 在 DeepSeek-V4 原生 `<think>` 标签中暴露内部思考过程，实现角色行为一致性的可观测与可验证。

---

## 三种实验模式

| 模式 | 描述 | `<think>` 内容 |
|------|------|---------------|
| **Mode A (baseline)** | 当前 PolicySim 默认 | 无 `<think>` 标签 |
| **Mode B (inner_monologue)** | 角色沉浸式内心独白 | 第一人称担忧、判断、决策动机 |
| **Mode C (pure_analysis)** | 纯逻辑分析 | 风险评估、资源约束、行动优先级 |

## DeepSeek-V4 原生 `<think>` 支持

DeepSeek-V4 是 PolicySim 引擎绑定的模型，原生支持 `<think>` 标签。这是选择 DeepSeek-V4 作为基线实验模型的核心原因——不需要额外的 prompt engineering。

## 控制指令注入位置

控制指令追加在第一轮用户消息末尾，不修改 Agent 系统提示词。

## 已知限制

效果是概率性的——未触发的轮次自动成为自然对照组。

## 相关页面

- [[concepts/role-consistency]]: RoleDNA 5维基因
- [[concepts/hypotheses]]: H1-H3 研究假设
- [[decisions/think-tag-format]]: `<think>` 标签格式决策
- [[comparisons/mode-comparison]]: 三种模式对比
