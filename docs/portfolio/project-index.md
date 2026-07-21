# AutoResearch 项目组合索引

> 更新日期：2026-07-03  
> 用途：让根目录一眼看清每条实验线的角色、状态和下一步。  
> 详细路线见 `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md`。

## 1. 顶层文件

| 路径 | 作用 |
|---|---|
| `README.md` | 根目录导航和当前主线 |
| `docs/roadmaps/topic5-research-directions.md` | 旧版课题五全量方向规划，保留为历史基线（2026-07-20 自根目录移入） |
| `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` | 新路线图，当前执行准绳 |
| `docs/investigations/p11-inner-monologue-paper-readiness-2026-07-03.md` | P11 readiness 调研 |
| `docs/portfolio/aliases.md` | 论文代号（P7 / P8 / P12 / P1+P2）到目录的映射 |
| `docs/autoresearch/` | AutoResearch 框架和运行材料 |
| `state/` | portfolio 层 AutoResearch 状态 |
| `logs/` | portfolio 层日志 |

## 2. 项目目录

| 目录 | 新定位 | 状态 | 下一步 |
|---|---|---|---|
| `p1.1-inner-monologue` | P11 早期版本 | 历史资产 | 不再扩展 |
| `legacy/p11-closed-v5-mimo` | P11 Mimo 版本 | 已关闭到 7.0 级 | 保留结果与 paper |
| `legacy/p11-closed-v5-minimax-m3` | P11 当前最完整版本 | 主线收口，复用给 P12 | 写 closure status，抽样本 |
| `papers/p12-judge-calibration` | P12 Judge 校准 | 新建，短期优先 | 从 P11 抽 sample manifest |
| `legacy/p08-legacy-init-2026-07` | P8 市场校准旧实现 | 初始化 | 暂不作为主入口 |
| `papers/p08-market-calibration` | P8 / settlement layer | 初始化 | 实现 Brier/Log Loss，服务 P1+P2 |
| `legacy/p07-legacy-init-2026-07` | P7 信号融合旧实现 | 初始化 | 暂不作为主入口 |
| `papers/p07-signal-fusion` | P7 / evidence input layer | 初始化 | 输出改造成 evidence ledger entries |
| `victorchen96.github.io` | AutoResearch 参考资料 | 只读参考 | 读取 framework 和 paper-writing skill |

## 3. 推荐活跃任务顺序

1. **P12 Judge Calibration**：新建目录，作为短期主任务。
2. **P11 Closure**：冻结新实验，抽取样本和方法论结果。
3. **P1+P2 Mainline Design**：factor ledger schema + evidence topology。
4. **P1.2 Settlement Layer**：Brier/Log Loss + event settlement。
5. **P2.1 Evidence Input Layer**：source independence / conflict / freshness。

## 4. 不建议做的事

- 不把 P11 继续大修成 8.5 paper。
- 不把 P2.1 写成“12 数据源融合”薄工程论文。
- 不单独追求 P1.2 市场故事，除非 settlement calibration 结果很强。
- 不在根目录继续堆散文件；新的组合级文档进 `docs/`，组合级状态进 `state/`。

## 5. 证据入口

| 主题 | 关键文件 |
|---|---|
| P11 综合判断 | `legacy/p11-closed-v5-minimax-m3/wiki/decisions/2026-07-03-comprehensive-synthesis.md` |
| P11 结构智能重评 | `legacy/p11-closed-v5-minimax-m3/wiki/decisions/2026-07-03-structural-intelligence-reassessment.md` |
| P11 主线收口 | `legacy/p11-closed-v5-minimax-m3/state/closure.md` |
| P12 任务定义 | `papers/p12-judge-calibration/state/task_spec.md` |
| P11 readiness 调研 | `docs/investigations/p11-inner-monologue-paper-readiness-2026-07-03.md` |
| P1.2 任务定义 | `papers/p08-market-calibration/state/task_spec.md` |
| P2.1 任务定义 | `papers/p07-signal-fusion/state/task_spec.md` |
| AutoResearch 框架 | `victorchen96.github.io/auto_research/framework.html` |
| Paper-writing skill | `victorchen96.github.io/auto_research/skill/paper-writing.html` |
