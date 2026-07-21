# 世界杯算法比较实证论文方案（先发散后聚焦）

> 日期：2026-07-20 ｜ 状态：v1.1（设计评审后修订：依赖重排 G1→G0→协议→OSF、市场基线降级路径写死、预注册定位收窄）｜ 评审记录：见文末 ｜ 上游决策：用户 Up-front 访谈 2026-07-20（主线=T1 算法比较实证；目标=域内现实区间；n 分层声明；kimi 溯源待验证）
> 证据仓库：`cds4worldcup`（**已封存，只读证据，任何分析不得直接操作该仓库**，用户指令 2026-07-20）｜ 先例模板：`docs/plans/decision-coscientist-experiment-2026-07-19.md`（闸门结构 + 预注册纪律）

## Goal

以 2026 世界杯为天然实验场，写一篇**多算法同台比较实证论文**：在同一套 ex-ante 冻结、公开可审计的预测资产上，比较 5 类方法（统计模型 / 阵型蒙特卡洛 / 路径空间枚举 / LLM 群体信号 / 预测市场）的校准度与区分度结构差异。卖点不是"谁赢了"，而是**罕见的全公开审计链 + 真 ex-ante 预测 + 诚实的结构性负结果**。

## Background

**证据资产清单（已全部核实，附出处；均指 `cds4worldcup` 内路径）**：

- **逐场预测（n=104 潜力）**：Elo+Poisson（`odds.json`，ex-ante commit `88a9bfd`，R1/R2 瑕疵在案）与 Coach 对位模型（`coach_simulation.json`，commit `1c067ec` 零漂移）。小组赛 72 场已结算：Elo Brier 0.5728 / 硬选 54.9%（n=71），Coach 0.6078 / 59.7%（n=72），均匀基线 0.6667（`results/2026-07-08-group-stage-72-match-evaluation.md`）。淘汰赛 32 场预测存在但**未结算**。
- **队伍级预测（n=48）**：CDS 路径空间引擎（Elo/Bradley-Terry bracket 枚举，`src/cds/championship.py`），ex-ante 2026-07-01。结算 n=46：**93.5% 夺冠质量压在出局队**，头号热门塞内加尔 4.39% 止步 32 强（`results/2026-07-18-cds-championship-knockout-settlement.md`）。
- **kimi LLM 群体信号**：300 persona agent × 10 派别；`kimi_agent_inventory.csv`（300 行）在库；首页前五自 2026-06-12 至 07-19 **逐字节冻结**（git 全史核实），前五中四进四强。项目自定级 Red Source；上游生成规则在 gitignored 的 `worldcup-kimi/`，**溯源完整性待验证**。
- **市场基线**：Polymarket 快照 77 个 commit（2026-06-12 → 07-19 每日），覆盖 45 队夺冠 outright——未结算的时间序列资产。
- **协议资产**：Green/Yellow/Red 来源分级、ex-ante 有效性判定（R1/R2）、因子账本结算。
- **内部诊断**：`docs/investigations/system-running-state-and-paper-readiness-2026-06-20.md` 判定项目 "site-driven, not paper-driven"，本计划显式补上预注册闭环。

**n 的分层声明（用户已确认）**：逐场级 n=104 可做统计推断；队伍级 n=48 夺冠概率 = 单届赛事（tournament-level n=1），只做描述性校准分析；市场每日序列做时间序列描述。

**选题发散记录（已聚焦，一行备案）**：候选 T1 算法比较实证 / T2 LLM 群体智能 / T3 审计协议方法论 / T4 过度分散负结果 / T5 因子账本，经 C1–C5 评分与用户裁定：主线=T1，T3 并入方法章节，T4 并入结果章节，T2 挂 G1 闸门决定升降级，T5 降为结果章一节案例分析（n=4，标注局限）。

## Approach

**核心科学问题**：在完全相同的事前信息与冻结纪律下，五类预测方法的**概率结构**（集中度、平局校准、质量分散）如何系统性不同？哪类结构差异对应实际结算优势？

**评估协议冻结（收窄定位，替代"预注册"表述）**：赛事已结束且部分结果作者已知——已见过的数字包括：72 场两模型结算全套指标、n=46 夺冠结算、kimi 前五与四强对照。**未计算**的只有：淘汰赛 32 场结算、市场序列重构与同台对照。因此 OSF 冻结物定位为**分析协议**（指标、纳排、主对照、多重比较规则 + 已知/未知边界声明），不是预测预注册；论文如实披露该边界。

**分析模块**：
1. **统一结算管线**：全部预测者（Elo、Coach、CDS 路径、kimi 信号、市场、均匀/FIFA 排名朴素基线）同一 ex-ante 规则结算。逐场级报 RPS（主）/Brier/LogLoss（辅）+ 校准曲线；队伍级报 Brier + 质量分布描述。淘汰赛 32 场首次结算。
2. **市场基线同台（队伍级限定）**：Polymarket 是夺冠 outright，无逐场 W/D/A——**市场只进队伍级对照，不做逐场映射反推**（与项目 R5 局限一致，论文中声明）；逐场基线 = 均匀 + 永远主场 + FIFA 排名。市场日度序列另作时间线描述。
3. **校准结构差异**：Elo 平局低估（−8.3pp，无 Dixon-Coles）vs Coach 平局高估 vs CDS 过度分散 vs 市场/kimi 集中——偏差的方向与结构是结果主线。
4. **kimi 信号 vs 市场**：相关性/领先-滞后——独立信息还是市场共识复述（节制处理为一节；T2 是否升级独立贡献由 G1 决定）。
5. （案例分析，不单列模块）因子账本 4 场深案例：标量分之外的解释力，标注 n=4 局限。

**证据保全（用户硬约束）**：`cds4worldcup` 封存。分析在独立工作区，只用只读导出副本；论文 Data Availability 指向原仓库公开 commit 哈希 + Zenodo 归档 DOI。

**统计纪律**：逐场主指标 RPS 预声明；模型两两比较配对 bootstrap CI + 效应量，BH 校正（比较族在 G1 后锁定——kimi 降级则族从 5 变 4）；队伍级与市场时间线仅描述不检验；爆冷/偏差分析标注探索性。

## Work Items

按周编号。**硬 go/no-go：W1 末 G1（kimi 溯源）、W2 末 G0（证据封存）、W4 末 G2（管线可复现）。顺序依据：导出完整性依赖溯源结论，协议族依赖 kimi 定级。**

### Phase A：溯源、封存与协议（W1–W2，关键路径）

| # | 内容 | 验收 | 决策点 |
|---|---|---|---|
| W1-1 | kimi 溯源验证：确认 `worldcup-kimi/` 上游可访问性。判定清单（达到才算一等公民）：persona/prompt 生成规则、聚合权重算法、模型版本、时间戳链，四项可文档化 ≥3 项；不可访问则基于 `kimi_agent_inventory.csv` 逆向重建并声明局限 | 溯源备忘录（按清单逐项判定） | **W1 末 G1**：kimi 定为一等对照 or 描述性一节；T2 升降级 |
| W1-2 | 市场快照 schema 审计（只读抽查副本前先做本项）：77 快照字段一致性、缺口清单、概率刻度 | schema 备忘录 + 序列缺口表 | 缺口大 → 模块 2 降为端点对比（赛前 vs 决赛前），市场退出主推断族 |
| W1-3 | 只读导出：git bundle（全史）+ 数据文件副本 + commit 清单哈希 + **条件性 kimi 上游捕获**（G1 结论决定入包范围）+ 决赛结果确认（缺则以 FIFA/Wikipedia Green Source 补齐并记录） | 导出 manifest 逐项可重建；原仓库零写入 | **W2 末 G0**：导出不完整阻断 |
| W2-1 | 分析协议 v1（指标/纳排/主对照/**比较族按 G1 结论锁定**/多重比较/分层 n 声明/已知数字边界声明） | 内部评审通过 | — |
| W2-2 | OSF 冻结分析协议 + 时间戳 | 公开 OSF 链接 | 冻结后才允许跑 W3 统一结算 |

### Phase B：统一结算管线（W3–W4）

| # | 内容 | 验收 | 决策点 |
|---|---|---|---|
| W3-1 | 淘汰赛 32 场赛果核对录入（导出副本内）+ 104 场全结算 | 全结算表；与已有 72 场报告交叉一致 | — |
| W3-2 | 市场序列重构（77 快照 → 日度概率矩阵）+ 队伍级同台结算 | 市场队伍级分数 + 时间线图 | 按 W1-2 结论执行全序列或端点对比 |
| W3-3 | 队伍级 n=48 汇总（CDS vs kimi vs 市场 vs 朴素基线） | 校准描述表 + 质量分布图 | — |
| W4-1 | 管线单命令可复现 + 种子固定 | 第三方按 README 一键复算全部表格 | **W4 末 G2**：不可复现 → 降级方法短文 |

### Phase C：分析与成文（W5–W8）

| # | 内容 | 验收 |
|---|---|---|
| W5-1 | 校准结构差异（模块 3）+ kimi vs 市场（模块 4）+ 因子账本案例分析 | 结果图表冻结 |
| W6-1 | 初稿（IJF / J. Sports Analytics / PLOS ONE 三选一，按结果强度定） | 完整初稿 |
| W7-1 | 内部红队评审（用域内期刊 checklist：范围、统计报告完整性、局限披露；不用 Nature rubric） | 评审备忘录 + 修订 |
| W8-1 | Data/Code Availability（Zenodo DOI + 原仓库 commit 哈希）+ 投稿 | 投稿回执 |

## Open Questions

1. **kimi 溯源**（W1-1，G1）：上游可访问性未知；判定清单四项能文档化几项——决定比较族规模与 T2 升降级。
2. **市场序列完整性**（W1-2）：若缺口大，模块 2 降为端点对比，市场退出主推断族。
3. **决赛（2026-07-19，西班牙 vs 阿根廷）结果录入状态**：W1-3 导出时确认，缺则以 Green Source 补齐。
4. **作者署名与期刊三选一**：W6 按结果强度裁量（结果强 → IJF；协议占比高 → 方法类期刊）。

## References

- 证据（`cds4worldcup`，封存只读）：`results/2026-07-08-group-stage-72-match-evaluation.md`、`results/2026-07-18-cds-championship-knockout-settlement.md`、`docs/source-policy.md`、`docs/investigations/system-running-state-and-paper-readiness-2026-06-20.md`、`docs/design/specs/2026-06-11-aiwork-research-audit-and-baseline-spec.md`（6 基线注册表，复用不重造）
- 评分规范：`research/nature-first-class-paper/REPORT.md`、`docs/roadmaps/topic5-research-directions.md`
- 计划模板：`docs/plans/decision-coscientist-experiment-2026-07-19.md`（闸门结构、OSF 冻结、Whitaker 2021 Silver 复现标准）

## 2026-07-20 设计评审修订记录（v1.0 → v1.1）

评审（explore 子代理，仅评计划文档，未触碰封存仓库）命中并已折入：
1. **依赖重排**：G1（kimi 溯源）提前至 W1 末先于 G0；市场 schema 审计（W1-2）前移至 OSF 冻结之前；比较族在 G1 后锁定。
2. **市场逐场缺口写死**：outright 赔率不做逐场映射，市场限定队伍级对照，避免 G2 之前守卫一个未定义的计算。
3. **预注册定位收窄**：改为"分析协议冻结 + 已知/未知数字边界声明"。
4. **删减**：发散评分表压为一行备案；因子账本去模块化；W7-1 换域内 checklist；删 workshop 并行短版蔓延。
5. **补齐判定清单**：kimi 披露门槛四项清单、导出 manifest、决赛结果确认入 W1-3 验收。
