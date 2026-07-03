# `<think>` 标签格式决策

> **类型**：decision | **状态**：accepted | **日期**：2026-07

---

## 背景

DeepSeek-V4 原生支持 `<think>` 标签，但需要对内容格式做规范，确保 LLM Judge 能可靠解析。

## 决策

- **Mode B**：`<think>(角色内心独白)</think>` —— 角色沉浸式第一人称
- **Mode C**：`<think>纯逻辑分析</think>` —— 风险评估、资源约束
- 标签内容包围在 `(` 和 `)` 中以区分于 XML 标记

## 相关页面

- [[concepts/inner-monologue-methodology]]: 内心独白方法论
