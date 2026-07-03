# AutoResearch 运行材料

本目录保存组合级 AutoResearch 参考和运行提示。

## 文件

| 文件 | 说明 |
|---|---|
| `bootstrap-skills.md` | 将 AutoResearch framework 与 paper-writing skill 安装为 Mimo skills 的提示词 |
| `orchestrator-prompt.md` | WorkBuddy / orchestrator 执行 AutoResearch 协议的提示词 |

## 本项目采用的关键规则

- 状态写入文件，不依赖聊天记忆。
- 每个任务有 `state/task_spec.md`、`progress.json`、`findings.jsonl`、`directions_tried.json`、`iteration_log.jsonl`。
- 两轮停滞后必须换结构约束，而不是继续调 prompt。
- 工作 agent 与验证 / 审稿 agent 分离。
- 每轮必须产生可验证产物。
- 五人格 review 使用中位数，不用平均数虚高。

## 根目录状态

组合级状态在：

- `state/task_spec.md`
- `state/progress.json`
- `state/findings.jsonl`
- `state/directions_tried.json`
- `state/iteration_log.jsonl`

子项目状态仍保存在各自目录下，不迁移。
