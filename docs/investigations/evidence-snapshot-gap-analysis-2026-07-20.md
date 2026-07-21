# Investigation: 证据快照缺口分析——哪些信息需要补入分析副本

> 日期：2026-07-20 ｜ 调查对象：`auto-research/evidence/cds4worldcup-snapshot-2026-07-20/`（以下简称**证据快照**；命名约定见 MANIFEST 与本文 §命名）
> 上游：开题报告 `docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms.md` v1.0、计划 `docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md` v1.1

## Summary

证据快照可支撑论文分析，但需向**分析副本**补入 4 类信息：① KO103/KO104 赛果（已 Green Source 核验：西班牙 1–0 阿根廷 a.e.t.；英格兰 6–4 法国）；② ex-ante 版本提取——漂移问题比预想更广，**`odds.json` 与 `cds_qualification.json` 均为 07-19 漂移版**，两者都须从 bundle 提取赛前版；③ kimi 溯源备忘录（聚合层已 21/21 精确复算，生成层版本不可考）；④ 增补日志 CHANGELOG 框架。oracle 的两条断言（意大利队过滤、cds4polymarket 关联）经 pair 证伪；pair 的一条断言（结算 JSON 缺失）经本人复核证伪——快照完整。

## Symptoms（已自查确认的缺口，作为调查输入）

1. **决赛与季军赛结果缺失**：`worktree/data/processed/schedule.json` 的 KO103（法 vs 英，季军赛 07-18）与 KO104（西 vs 阿，决赛 07-19）status=scheduled，未录入比分。
2. **无淘汰赛逐场预测**：`odds.json`（elo_poisson）与 `coach_simulation.json` 均仅 72 场小组赛预测——开题报告 v1.0 的 n=104 口径须修正为 n=72(71)。
3. **odds.json 工作区版本为漂移版**（generated_at 2026-07-19，R2 实锤）：ex-ante 评估版必须从 bundle 提取 commit `88a9bfd`。
4. **kimi 生成元数据部分可考**：`data/raw/kimi/kimi_300_unpacked/` 含 plan.md（生成规则）、wc2026_aggregation.json（聚合公式"信心加权归一化"、metadata date 2026-06-05）、42 个派别文件；模型版本不可考。
5. **paper-readiness 诊断文档未提交**：`docs/investigations/system-running-state-and-paper-readiness-2026-06-20.md` 在原仓库为 untracked，引用证据等级需标注。
6. **市场快照 schema 已核实**：45 队，字段 probability/raw_yes_price/market_slug/question + unmapped_markets；77 个日度 commit（2026-06-12→07-19）。

## Hypotheses（待 pair 验证或证伪）

- H-a：除上述 6 项外，快照内还存在其他影响论文分析的数据缺口（如：cds_qualification 的结算完整性、因子账本覆盖率、source-policy 版本一致性）。
- H-b：kimi 聚合公式（信心加权归一化）可用 `kimi_agent_inventory.csv` 300 行精确复算 wc2026_aggregation.json 的 all_teams 概率——若可复算，kimi 信号的可复现性论证成立；若不可，存在未文档化权重。
- H-c：bundle 中提取的 `88a9bfd` 版 odds.json 与 72 场结算报告所用版本一致（交叉核验 R2 处置可行性）。

## Background / Prior Research

**Phase 1.5 外部查证（Green Source：Wikipedia，2026-07-20 本人直接核验）**：

- **决赛 KO104**：西班牙 1–0 阿根廷（加时，Torres 106'），2026-07-19，MetLife 球场。[2026 FIFA World Cup final (Wikipedia)](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_final)。冠军 = 西班牙（队史第二冠）。
- **季军赛 KO103**：英格兰 6–4 法国，2026-07-18，Miami Gardens。[2026 FIFA World Cup knockout stage (Wikipedia)](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_knockout_stage) 对阵图确认（explore 代理曾报出来源分歧，经本人直接核验对阵图消解）。
- **半决赛**：西班牙 2–0 法国（07-14）；阿根廷 2–1 英格兰（加时，07-15）。
- **基准率关键事实（喂给开题报告 §7.1）**：Wikipedia 淘汰赛页明确记载——**本届是世界杯史上首次 FIFA 排名前四球队全部进入四强**。这意味着任何"重仓热门"的信号（市场、FIFA 排名、kimi）在今年都会"命中"4/4——"前五中四"的基准率论证有了直接文献锚点：本届热门进四强是常态事件，不能作为技能证据。
- kimi 前五对照实际成绩：西班牙（#1, 23.82%）冠军、阿根廷（#3, 19.59%）亚军、法国（#2, 23.56%）四强、英格兰（#5, 5.2%）第四、葡萄牙（#4, 6.56%）16 强负于西班牙。仅作描述，不入技能论证。

**H-b 验证（本人直接计算，2026-07-20）——确认**：用 `kimi_agent_inventory.csv` 300 行按 plan.md 公式（信心加权归一化）复算，与 `wc2026_aggregation.json` 的 all_teams 概率 **21/21 队全部精确一致**（容差 0.05pp 内零失配；西班牙 23.82 / 法国 23.56 / 阿根廷 19.59 / 葡萄牙 6.56 / 英格兰 5.2 全部逐位吻合）。kimi 信号聚合层完全可复现，V-kimi 预审通过。

**H-c 验证（本人直接计算，2026-07-20）——确认**：从证据快照 bundle 克隆并 checkout `88a9bfd`，`odds.json` generated_at=2026-06-12T10:57:42Z、n=72；match 1 home_win=0.7629 / draw=0.1582 / away=0.0789，与 72 场评估报告引用值**逐位一致**；工作区现版（07-19 漂移版）home_win=0.7004，R2 漂移实锤。ex-ante 版本提取路径可行，V-88a 预审通过。（验证用临时克隆已清理。）

## Investigator Findings

> 调查执行者：investigator（pair 角色）| 调查日期：2026-07-20
> 调查范围：H-a 假设——除 Symptom 1–6 外，是否存在影响论文分析的其他数据缺口。
> 调查方法：4 项 fan-out explore 子探针 + 1 项主线程内交叉核验。每条结论给出 file:line 实证。

### F1 — `cds_qualification.json` 与 2026-07-08 结算报告的对齐

- **F1.1** Universe 一致性：JSON `total_teams=48`（`data/processed/cds_qualification.json:4`）↔ 结算文档 48 teams (12 groups × 4)（`results/2026-07-08-cds-qualification-settlement.md:11–62`）。**VERIFIED** — 无团队级漂移，confederation 与分组皆匹配。
- **F1.2** `qual_prob_top2` 数值漂移：JSON 在头部 `generated_at: 2026-07-19T02:49:57.749925+00:00`（`cds_qualification.json:3`），而结算报告基于 2026-07-08 的版本生成。例：Czech Republic 在 JSON 中为 `qual_prob_top2=0.8247`（`cds_qualification.json:~7`），但结算文档表格记录为 0.834（`2026-07-08-cds-qualification-settlement.md:96`，表 3）。**INCONSISTENT** — 同一团队差 ~1pp；探针测得最大漂移为 Iran +0.023（11 天延迟重新生成所致）。
- **F1.3** 关键缺口：**`cds_qualification.json` 没有任何 `qualified` / `eliminated` 布尔字段**。每个团队仅有概率字段（`qual_prob`、`qual_prob_top2`、`position_probs`、`scenarios`）+ 路径标签（`resulting_position` 含 `top2_qualified`/`3rd_may_qualify`/`eliminated`，但这是概率枚举内的标签，不是 ground-truth outcome）。**VERIFIED via file head**（`cds_qualification.json:5–60`）。
- **F1.4** 关键缺口（与 F1.3 直接相关）：结算文档显式声明"实际二元结算结果"存放在 **`results/ops/cds-settlement-2026-07-08.json`**（`2026-07-08-cds-qualification-settlement.md:6`、`269`、`272`），由 `src/cds/settlement_run.py:41` 生成；其路径亦在 `results/2026-07-08-cds-championship-partial-settlement.md:182` 被复用。
- **F1.5** **该 ops JSON 在快照中不存在**。验证：`results/` 目录仅含 7 个 markdown（无 `ops/` 子目录，见文件树）；`file_search` 全文搜 `results/ops` → 0 命中；`file_search` 搜 `settlement-2026-07-08` 找到的 12 处匹配全部为 markdown 引用，无 JSON 文件实体。**CRITICAL GAP — 论文不可直接消费**：每队 32 强/出局布尔位无法从快照直接读取。
- **F1.6** 可恢复性评估：`wiki/index.md:29` memo 声明结算脚本使用 `lots_seed=20260708` 保证确定性，且 12 小组 × 8 比分抽样经 Wikipedia Green Source 0 偏差核验（`2026-07-08-cds-qualification-settlement.md:64–66`）。在原仓库 live state 下重跑 `python3 -m src.cds.settlement_run` 可重生成 JSON，但**快照内仅冻结 `settlement_run.py` 源码，未冻结 `schedule.json` 当日字节**，因此纯快照内不可重生成。

### F2 — `artifacts/plan-c/factor-ledger/` 覆盖率

- **F2.1** 现有条目：仅 4 个 yaml（`wc2026-a-m01-mex-rsa.factors.yaml`、`wc2026-b-m02-qat-sui.factors.yaml`、`wc2026-c-m01-bra-mar.factors.yaml`、`wc2026-f-m01-ned-jpn.factors.yaml`），全部为小组赛 A1/B2/C1/F1。**VERIFIED**。
- **F2.2** 期望 vs 实际：`data/processed/schedule.json:2394–2398` 声明 104 场（72 小组 + 32 淘汰）。覆盖率 **4/104 (3.85%)**，缺口 100——其中 0/32 淘汰赛，4/72 小组赛（剩余 68 小组未覆盖）。**VERIFIED**。
- **F2.3** 项目自身表述：`artifacts/reports/plan-c-protocol-validation.md:9,97–99,110–112` 明示只跑 MVP2 规模（3–5 场 rolling matches），并称"only 4 fixtures"，将 104 场列为后续目标。**覆盖率低与项目自述一致**。
- **F2.4** 隐藏的状态同步缺陷：3 个 ledger（B2-QAT-SUI、C1-BRA-MAR、F1-NED-JPN）因子仍标记为 `pending` / `tracking`，但对应的 `settlement_record.yaml` 已存在。**仅 MEX-RSA 一个 ledger 三因子 `complete`**（`wc2026-a-m01-mex-rsa.factors.yaml:25–100`），其余 9 因子处于 settlement-after-ledger 但 ledger 未更新状态的不一致。**CRITICAL** —— 若下游分析把这些 ledger 视为"未结算"则会少算 3 场，视为"已结算"则与 yaml 头部声明不符。
- **F2.5** `artifacts/plan-c/predictions/` 同样稀缺：MEX-RSA 缺对应 prediction_card（被 `wc2026-a-m01-mex-rsa.factors.yaml:2–4` 反向引用回 fixtures 目录），其余 3 个 ledger 有 1:1 配对的 prediction_card。**MINOR GAP**。

### F3a — 团队路径卡的非 WC2026 团队（"需要 40 队过滤器"声明验证）

- **F3a.1** 活跃卡片数：**48 个**，与 WC2026 实际参赛数完全相等（详见 `artifacts/team-cards/` 根目录：A=4、B=3、C=7、D=1、E=3、F=1、G=2、H=1、I=2、J=2、M=2、N=3、P=3、Q=1、S=8、T=2、U=3，合计 48）。**VERIFIED — 无缺失**。
- **F3a.2** `_archived/` 10 团队：cameroon、chile、costa-rica、denmark、**italy**、nigeria、poland、ukraine、venezuela、wales（来自 `artifacts/team-cards/_archived/` 文件树）。**VERIFIED**。
- **F3a.3** Italy（探针举例）确实在 `_archived/italy.md` 而非根目录活跃卡。Italy 在 UEFA 附加赛出局未晋级 WC2026，分类正确。
- **F3a.4** "需要 40 队过滤器"声明：**REFUTED**。数据集已通过 `_archived/` 子目录**显式分区**为 48/10，无过滤需求。该声明的来源可能是探针看到的 `_archived/` 子目录被误判为"混入"——实际上命名空间隔离已完备。

### F3b — `kimi_300_unpacked/` 与 `cds4polymarket` 仓库的连接

- **F3b.1** `data/raw/kimi/kimi_300_unpacked/` 内容（45 文件）：1 个 `plan.md`（5 阶段 300-agent 跨 10 派别执行方案）、1 个 `wc2026_data.md`（111 行数据基础）、1 个 `wc2026_aggregation.json`（Top8 概率聚合 + raw agent reasons）、42 个派别 JSON。**VERIFIED**。
- **F3b.2** Grep 矩阵（不区分大小写，跨 `data/raw/kimi/` 全树）：
  | 关键词 | 命中 | 备注 |
  |---|---|---|
  | `cds4polymarket` | **0** | — |
  | `polymarket-research` | **0** | — |
  | `pm-agent` / `pm_research` | **0 / 0** | — |
  | `github.com` | **0** | — |
  | `tangzw119` | **0** | — |
  | `polymarket` | 1 | `wc2026_aggregation.json:1146`，一处"Polymarket 显示法国真实胜率"中文 reasoning，引用的是**预测市场 Polymarket** 而非 cds4polymarket 仓库 |
  | `factor_ledger` / `prediction_card` / `settlement_record` / `schema.yaml` | **0 / 0 / 0 / 0** | — |
- **F3b.3** 反向验证：`artifacts/fixtures/cds4polymarket/`（如 `factor-ledger/wc2022-g-arg-ksa.factors.yaml`、`predictions/mvpa/wc2026-a-m01-mex-rsa.v0.2.prediction_card.yaml`）多处显式将 kimi 列为 `red_sources_excluded_from_model` 并设 `max_kimi_derived_*` 预算旋钮（典型 3/1 或 0/0）。
- **F3b.4** **VERDICT: NO UPSTREAM→DOWNSTREAM CONNECTION**。依赖箭头是**反向单向下行**：`cds4polymarket → kimi (excluded)`，仅作 source-policy 引证与预算设上限用。kimi 上游文件本身对 cds4polymarket 仓库零感知，零数据导入，零 schema 共享。**该 oracle 声明 REFUTED**。

### F4 — `docs/source-policy.md` 与结果文档版本一致性

- **F4.1** `docs/source-policy.md:3–4` 标注 `状态: draft-for-execution`、`日期: 2026-06-11`（早于所有结算文档 27–37 天）。
- **F4.2** 5 份结果文档对 source-policy 的引用（路径 `docs/source-policy.md`，无版本号）：
  - `results/2026-06-18-matchday1-prediction-evaluation.md:92`
  - `results/2026-07-08-cds-championship-partial-settlement.md:153`
  - `results/2026-07-08-cds-qualification-settlement.md:199, 247`
  - `results/2026-07-08-group-stage-72-match-evaluation.md:278, 308`
  - `results/2026-07-18-cds-championship-knockout-settlement.md:151`
  无版本冲突——**所有引用皆不带版本号**，可解析到同一文件。
- **F4.3** 自承修订需求：`results/2026-07-08-group-stage-72-match-evaluation.md:278` 明示"**需 source-policy 修订**"以纳入 Opta/Sofascore/FotMob 等黄源补半场/球员级统计缺口。**当前 `source-policy.md` 未含这些黄源示例**（其 Yellow Source 示例仅 4 类：媒体赛前分析、汇总表、新闻伤病、Kimi 尚未核验事实条目——见 `source-policy.md:38–52`）。**INCONSISTENT** —— 结果文档已识别需修订，源策略文档未跟进。
- **F4.4** `source-policy.md` 仍是 draft-for-execution 状态，与"draft 之后 1 个月内被 5 份结算文档广泛引用"的成熟度不匹配。**MINOR GAP**——建议下次修订时同步升 status（如 `ratified-v1.0`）。

### 结论摘要

| ID | 严重度 | 一句话结论 |
|----|--------|-----------|
| F1.3 | HIGH | `cds_qualification.json` 缺 `qualified`/`eliminated` 布尔字段 |
| F1.5 | **CRITICAL** | 引用 4 次的 `results/ops/cds-settlement-2026-07-08.json` 在快照内不存在 |
| F1.2 | MEDIUM | `qual_prob_top2` 数值漂移（JSON 比结算日新 11 天） |
| F2.2 | MEDIUM | factor-ledger 覆盖率 4/104 (3.85%)——与项目 MVP2 声明一致但与论文 n=104 口径差距大 |
| F2.4 | **CRITICAL** | 3/4 ledger 处于"settlement 已写但 ledger 因子仍 pending"的状态不一致 |
| F3a.4 | NONE | "需要 40 队过滤器"声明 REFUTED——48/10 已通过 `_archived/` 显式分区 |
| F3b.4 | NONE | "kimi 与 cds4polymarket 有连接"声明 REFUTED——依赖箭头反向，kimi 上游零感知 |
| F4.3 | MINOR | `source-policy.md` 自 2026-06-11 起 draft-for-execution，未跟进结算文档识别出的 Opta/Sofascore 黄源修订需求 |

**新增 Critical 数据缺口（须补入分析副本）**：
1. **`results/ops/cds-settlement-2026-07-08.json`** —— 必须重跑 `src.cds.settlement_run.py` 重新生成并入快照（脚本 + seed 都在，但 schedule.json 字节已被冻结且无 .gitignore 旁路，原则上可重生成但不可"原样"恢复）。
2. **3 个 plan-c ledger 状态同步** —— B2-QAT-SUI、C1-BRA-MAR、F1-NED-JPN 的 `factors.yaml` 必须从 `pending`/`tracking` 更新为 `complete`，否则与各自的 `settlement_record.yaml` 语义冲突。

**Refuted 声明**（无需处置）：F3a.4、F3b.4。原 oracle 输出基于对 `_archived/` 子目录的视觉误判 + 对 cds4polymarket fixtures 反向引用的过度泛化。

## Root Cause

(待填 — 与 Recommendations 同步)

## Investigation Log

### Phase 1 - 快照自查（agent 本人）
**Findings:** 见 Symptoms 1–6，均已在快照副本内直接核实（python3 json 解析 + git bundle verify + gh/ls 外部核查）。
**Conclusion:** 作为调查输入确认。

## Root Cause

缺口分四类，根因各异：
1. **赛果缺口**（KO103/KO104 status=scheduled）：封存时点（07-19/20）原仓库的赛果录入流程尚未覆盖最后两场——属流程时滞，非数据丢失；以 Green Source 补齐即可（已完成核验）。
2. **版本漂移（扩大）**：`odds.json`（07-19）与 `cds_qualification.json`（2026-07-19T02:49:57Z，pair 发现 Iran qual_prob_top2 与 07-08 结算文档偏差 +0.023）均被 daily rerun 覆盖——这是项目 R2 发现的一般化：**所有 daily 重算产物都只有 bundle 历史里有 ex-ante 版**。管线必须从 bundle 提取 `88a9bfd`（odds）与 07-08 前版本（qualification）。
3. **kimi 溯源**：上游仓库不存在（2026-07-20 核查），但生成文档与原始投票存活于 gitignored 的 `data/raw/kimi/` 并进入快照——聚合层可复现（H-b 确认），生成层（模型版本、重跑同分布）永久不可考，定性为「文档部分可考的一次性 LLM 群体快照」。
4. **协议文档滞后**：`source-policy.md` 仍为 `draft-for-execution`，未吸收结算文档要求的黄源扩展（Opta/Sofascore/FotMob）——论文引用来源纪律时须注明版本。

**证伪记录**：oracle 断言「40 队过滤/意大利混入」——伪（`artifacts/team-cards/_archived/` 已隔离 10 支非参赛队）；oracle 断言「kimi 关联 cds4polymarket」——伪（依赖箭头反向，fixtures 仅将其列为排除的 red source）；pair 断言 `results/ops/cds-settlement-2026-07-08.json` 缺失——伪（快照内存在，36545 字节，pair 的 file_search 漏检）。

## Recommendations

**补入分析副本的信息清单（按优先级）**：
1. 赛果补齐：KO104 西班牙 1–0 阿根廷（a.e.t., Torres 106'）、KO103 英格兰 6–4 法国——写入分析副本 `schedule.json`，CHANGELOG 登记 Green Source 链接。
2. ex-ante 提取：`odds.json@88a9bfd` + `cds_qualification.json@≤2026-07-08` 从 bundle 提取入分析副本（V-88a 扩展为双文件）。
3. kimi 溯源备忘录：plan.md 摘要 + 聚合公式 + 21/21 复算证据 + 版本不可考声明，入分析副本 `provenance/`。
4. CHANGELOG.md 框架：分析副本根目录初始化，以上 1–3 为首批条目。
5. 开题报告 v1.2 输入：漂移扩大（qualification 也须 bundle 提取）、FIFA 前四全部进四强的基准率锚点（§7.1 强化）、kimi 前五实际成绩描述段、source-policy 版本注明。

**预防措施**：pair/oracle 断言一律经直接计算复核后方可入档（本次 4 条断言 2 条证伪 1 条漏检）；快照只做读，增补只进分析副本。

## Preventive Measures

- 分析副本的所有增补信息必须走"增补日志"（changelog），与快照原始字节分离存放，禁止就地修改 worktree。
