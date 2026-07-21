# CDS4WorldCup2026 路径空间 Spec 决策

> **类型**: decision
> **状态**: active
> **日期**: 2026-06-11
> **创建日期**: 2026-06-11
> **最后更新**: 2026-06-11

## 决策

将 CDS4WorldCup2026 的主线定义为 **48 队夺冠路径推演与条件世界空间**，而不是“预测 2026 世界杯冠军”。

正式 spec 写入：

- `docs/design/specs/2026-06-11-cds4worldcup2026-path-space-spec.md`

Plan 0 复制执行计划写入：

- `docs/design/plans/2026-06-11-plan0-fork-copy-plan.md`

## 核心结构

项目采用四个 plan：

- **Plan 0**：CDS4WorldCup 分叉复制方案，迁移 CDS4Polymarket 的可复用方法、数据、知识和 fixture。
- **Plan A**：48 队夺冠路径推演主线，输出 Team Path Card 和 Path Matrix。
- **Plan B**：MVP-0 决策树，判断 Kimi / AI 群体数据是否值得进入校准扩展。
- **Plan C**：MVP1&2 兜底方案，保留原 Factor Ledger 预注册、结算和知识回写闭环。

## 决策理由

原 Kimi 因子校准方案虽然比“AI 猜冠军”更严谨，但仍可能被吸回“寻找最优预测因子”的问题框架。48 队夺冠路径推演能更贴近 CDS 的本体：输出条件空间、阻力结构、黑天鹅助力和可校准知识，而不是输出单一答案。

Plan B 保留数据门控能力，避免在 Kimi reason 质量、codability、Neff 或 adjudication yield 不成立时继续扩展错误实验。Plan C 保留 MVP1&2，确保即使 Kimi 数据不可用，CDS 协议本身仍能跑通。

## 下一步

1. 执行 Plan 0 复制并生成 copy manifest。
2. 启动 Plan A0 / A1：48 队 registry 与 48 队薄切片夺冠路径推演卡；4 队只作为深描质检样本。
3. 启动 Plan B0 / B1：Kimi reason 直觉锚定与数据可用性。
4. 准备 Plan C：复制 schema / template / fixture 后核验单场闭环。
5. 暂缓 UI / dashboard spec，待 MVP-A1 完成且 Path Card / Matrix 字段稳定后再决策。

## 执行记录

> [!memo] 2026-06-11 第一实施包已创建
>
> 来源：本轮执行。
> 上下文：根据 spec 的第一实施包，已创建 Plan A / B / C 所需目录骨架，并新增 `docs/source-policy.md`、`docs/path-card-template.md`、`docs/design/plans/2026-06-11-mvp0-data-gate-plan.md`、`artifacts/reports/mvpa1-four-team-selection.md`。下一步可执行 Plan 0 复制 Kimi 原始数据、CDS4Polymarket protocol/schema/fixture，并实施 MVP-0 数据门控脚本。

> [!memo] 2026-06-11 修正 Plan A 命名并纳入 Plan 0 复制方案
>
> 来源：用户要求将旧称修正为“夺冠路径推演”，并审阅 spec 是否明确分叉该做什么、复制什么、知识点与 Kimi 数据如何迁移、UI 是否单独建 spec，以及 Plan 0/A/B/C 是否具备实施条件。
> 上下文：主 spec 已更新为四 plan 结构，新增 Plan 0 分叉复制执行计划。当前结论是：已具备分叉 + Plan 0 + Plan A0/A1 + Plan B0/B1 + Plan C 准备条件；暂不具备完整 48 队 Markov 引擎与新前端 UI 的实施条件。

> [!memo] 2026-06-11 新增数据依赖闸门矩阵
>
> 来源：用户追问除了 `Path Type` 外，还有哪些开发项必须先做数据分析再定。
> 上下文：主 spec 已新增数据依赖闸门，明确 `tier`、初始实力参数、Markov/Monte Carlo 正式参数、Bayesian 更新权重、Factor Ledger 入账阈值、黑天鹅/阻力排行、UI/可视化、论文主张等都必须等待 Plan A0/A1、Plan C 或 Kimi recoverability gate 后再定；第一阶段只允许做 registry、source inventory、模板、copy manifest 和接口骨架。

> [!memo] 2026-06-11 Plan A 调整为 48 队全覆盖，Path Type 改为数据派生
>
> 来源：用户指出 `Path Type` 分类需要先完成 MVP-0 / 数据分析，否则容易变成无数据依据的先验分类；同时明确希望 48 支球队全做，而不是只做几支。
> 上下文：主 spec 已修正为 MVP-A1 先做 48 队薄切片路径卡，4 队仅作为深描质检样本；`Path Type` 在 MVP-A2 才基于 48 队 `path_signals` 矩阵派生，Kimi reason 只有通过 recoverability gate 后才能作为辅助。

> [!memo] 2026-06-11 Plan B2 标记为局部卡点，项目主线不阻塞
>
> 来源：用户指出 Kimi reason 原文存在压缩黑话、缺主谓宾、人设独白、事实碎片和推论判断混杂的问题，普通人难以直接标注。
> 上下文：主 spec 已将 Plan B2 从 `Codability Pilot` 调整为 `Reason Recoverability Gate`，并标记为 `deferred-local-blocker`。该卡点只阻塞 Kimi reason 进入 Factor Ledger，不阻塞 Plan A1 48 队夺冠路径推演，也不阻塞 Plan C MVP1&2 协议闭环。Kimi reason 暂保留为 Red Source / Marginalia / 候选线索。

> [!memo] 2026-06-11 首页优化 spec 起草
>
> 来源：用户要求先讨论并写 spec，暂不施工。
> 上下文：在 48 队路径卡、路径卡审计、baseline suite、Plan C 协议验证、Polymarket API 能力和内部长程自动化能力边界基础上，新增 `docs/design/specs/2026-06-11-homepage-optimization-spec.md`。主页目标从静态研究说明升级为路径空间研究驾驶舱，同时继续遵守 Kimi/市场只作 public baseline 或外部共识、不作为 CDS 事实输入、不构成投注建议的边界；未投入运行的内部工具不进入主页叙事。

> [!memo] 2026-06-11 主页优化实现
>
> 来源：用户批准按首页优化 spec 施工，并要求使用中国球迷能听懂的大白话。
> 上下文：实现 `site/data/homepage.json` 构建期数据契约，重写 GitHub Pages 首页为“选球队 → 看难点 → 外界怎么看 → 方法和来源 → 更新记录”的静态页面；新增纯前端本地 JSON 渲染、CSS 条形图/矩阵、来源标签、球队入口锚点。公开页面不直接请求 Polymarket API，不展示具体长程 agent 工具品牌，不输出投注建议。

> [!memo] 2026-06-11 主页中文化和静态站验收补强
>
> 来源：用户强调公开页面要使用中国球迷能听懂的大白话。
> 上下文：将外部参照卡片中的内部公式和英文术语改为公开页面短句；把球队总览页筛选、状态、Kimi 参考、空状态等动态文案统一改为中文；保留 GitHub Pages 纯静态架构，浏览器端只读取本地 JSON，不解析 CSV，不调用外部市场 API。

> [!memo] 2026-06-11 公开站点隐藏内部参照与原始 artifacts
>
> 来源：用户指出公开首页提及 Kimi 会让访客困惑，也像在替工具打广告；同时本地 file:// 打开首页出现数据加载失败。
> 上下文：公开 GitHub Pages 改为只讲球队夺冠路、市场参考和来源边界，不展示 Kimi / AI / Agent 等内部参照名称；构建脚本输出公开版 `site/data/*.json` 和 `site/data/*-data.js` 兜底数据，直接打开 HTML 也能渲染；Pages 发布流程只发布 `site/`，不再公开 `artifacts/`、`wiki/`、`schema/`、`docs/references/`。

> [!memo] 2026-06-12 单队详情页与模块化赛后更新
>
> 来源：用户指出首页点击球队后应看到该队专业分析，而不是球队列表；同时要求补充图表、公开参考数据和赛后可更新架构。
> 上下文：新增 `site/team.html`、`site/js/team-detail.js` 与 `site/data/team-details.json`/兜底脚本；首页和球队总览页入口统一跳转到单队详情。详情页按“凭什么能冲冠军 → 最怕哪种比赛 → 接下来盯什么”写成人话，并加入难点条形图、公开模型群体参考、市场快照空状态、关键难点/突破条件/观察清单。后续每场比赛后主要更新路径卡、公开参考快照和市场快照，再重跑 `scripts/build_site_data.py`，不需要重写 HTML/CSS。

## 相关页面

- [[concepts/cds]]
- [[concepts/decision-control-plane]]
- [[decisions/cds-business-rebuild]]
- [[decisions/mimo-season-campaign-ops.md]]

> [!memo] 2026-06-11 创建 CDS4WorldCup2026 路径空间 spec 决策
>
> 来源：用户要求将 MVP-0 决策树作为 Plan B、MVP1&2 作为 Plan C 纳入新项目 spec，并输出到 `cds4worldcup` 仓库。
> 上下文：准备立即开始实施，因此先将 spec 落盘并在 wiki 中记录路线选择。

> [!memo] 2026-06-12 公开站升级边界：允许在访客页面说"AI 多视角推演"，让用户知道这是 AI 辅助分析；但不公开 Kimi / 小米 / MiMo 等厂商品牌。Polymarket 只作为 Yellow Source 市场快照，外部模型群体只作为 Red Source 参考，二者都不进入事实判断，也不输出投注建议。
