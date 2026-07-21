# NLUI Decision Workspace MVP

> **类型**：decision
> **状态**：planned
> **日期**：2026-06-06
**来源**：archive/cds-nlui-decision-workspace.md

---

## 背景

CDS 需要第一个可运行的 NLUI 决策工作台 MVP：用户用自然语言输入复杂决策问题，系统自动生成结构化研究 brief，并支持人工审阅后发起推演。

## 决策结果

**架构选择：**
- 以 Policysim-v0.2 为主实现仓库
- 后端新增 `decision` 模块（NestJS）
- 前端新增 `DecisionWorkspace` 页面（React 19）
- 复用现有 MonteCarloService 推演能力

**第一条闭环：**自然语言 → 研究 brief → 推演启动

## 四个任务

1. 建立后端 Decision API 契约（DTO + controller + module）
2. 实现 NL → DecisionBrief 编译与 launch 编排
3. 新增前端 Decision Workspace 页面与 API client
4. 接入 Dashboard 入口并完成手工验证

## 技术栈

NestJS 11, TypeORM, React 19, Vite, Vitest, Jest

> [!memo] 2026-06-07 本计划完整版见 archive/cds-nlui-decision-workspace.md
>
> [!memo] 2026-06-07 MVP 执行完成（demo 级别）。后端 Decision 模块（DTO + controller + service + AI 编译 + MonteCarlo launch）已接入 Policysim-v0.2。前端 DecisionWorkspace 页面已创建并挂载到 Dashboard。构建和后端测试通过。前端单测环境有预存问题（localStorage mock）需后续修复。

---

## 相关页面

- [[concepts/nlui]]: NLUI 自然语言用户界面
- [[concepts/cds]]: CDS 计算决策空间
- [[decisions/cds-business-rebuild]]: CDS 业务重构设计
