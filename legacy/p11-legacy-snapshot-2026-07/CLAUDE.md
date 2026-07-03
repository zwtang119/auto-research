# P11 Inner Monologue → RoleDNA 角色一致性验证

> **论文管线**：P11 | **模型**：DeepSeek-V4 | **AutoResearch 协议**：Deli_AutoResearch
> **状态**：M1 complete, M2 in progress | **目标会议**：ACL 2027 / EMNLP 2027

## 快速进入

1. 读 `wiki/index.md` 了解本实验知识库全貌
2. 读 `state/task_spec.md` 了解实验任务规格与假设
3. 读 `state/progress.json` 了解当前进度

## Marginalia 知识库

本实验使用 Marginalia 边注系统。知识库位于 `wiki/`。

### 每次对话开始时
- 读取 `wiki/index.md` 了解知识库全貌

### 对话中遇到以下情况时
- 讨论了新概念或机制 → 在 `wiki/concepts/` 创建页面
- 做了实验决策 → 在 `wiki/decisions/` 记录
- 发现与已有知识的关系 → 用 `[[wikilink]]` 链接

### 完成实质工作后
- 更新 `wiki/index.md`（如有新页面）
- 在相关页面添加批注：`> [!memo] YYYY-MM-DD 内容`
- 更新 `state/progress.json`

## 三原则
- 同位：记忆附着在知识点旁边，读知识点即读记忆
- 无损：保留原话，不经过 Embedding 压缩
- 解耦：纯 Markdown 文件，独立于任何平台

## 核心数据资产

| 资产 | 状态 | 位置 |
|------|------|------|
| 实验脚本（3个） | ✅ M1 完成 | `scripts/*.py` |
| 主实验（150 runs） | 🔄 M2 进行中 | 待运行 |
| LLM Judge 评分 | ⏳ M3 待启动 | `scripts/llm_judge_scoring.py` |
| 统计分析 | ⏳ M4 待启动 | `scripts/statistical_analysis.py` |
