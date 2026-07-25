# Paper A 论文骨架（章节结构 + 每节要点 + 图表落位）

> 日期：2026-07-25 ｜ 状态：v0.1 骨架（待用户确认后填内容）
> 开题底座：`docs/investigations/worldcup-algorithms-proposal/proposal-worldcup-algorithms-v2.md`（H1–H5 + PIV + A1–A5 模块，权威科学设计）
> 执行计划：`docs/plans/worldcup-algorithms-comparison-paper-2026-07-20.md`（W1–W8 + G0/G1/G2 闸门）
> 证据层：`evidence/cds4worldcup-timestamp-anchors-2026-07-25/`（EVIDENCE-CHAIN、TOP4 核验卡、截图 22 张、双锚收据）
> 注意：2026-07-20 旧提纲（本目录 `worldcup-paper-outline-and-supplements-2026-07-20.md`）的 11 周进度与 venue 映射仍有效；其"校准结构差异"卖点已被 v2 的"协议为一等贡献"框架吸收——本骨架以 v2 为准，旧提纲的 IMRaD 要点与 venue 分析可继续引用。

## 0. 题目与一句话

**推荐题目（v2 对齐）**：
> **Audit-Chain-Anchored Reconciliation: A Protocol for Verifiable Multi-Forecaster Evaluation, Applied to Five Sealed Forecasts of the 2026 FIFA World Cup**
> （审计链锚定的对账协议：一种可验证的多预测者评估协议，应用于 2026 世界杯五份封存预测）

**一句话（Check 1 句式，全文四处一致）**：我们提出 audit-chain-anchored multi-forecaster reconciliation protocol，以 git 冻结 + 来源分级 + 统一结算 + OSF 分析协议冻结 + 协议完整性向量五件套，把多源事前预测升格为可复现的同台评估对象，并将协议完整性状态作为与预测分数并列的一等评估字段。

**主语纪律**：主语永远是协议，不是"我们拥有五份独家预测"（v2 §7.0 禁用表述对照表逐项执行）。

## 1. 贡献声明（4 条，与 H1–H5 映射）

| # | 贡献 | 对应假设 | 证据载体 |
|---|---|---|---|
| C1 | 协议五件套 + PIV 八字段：协议完整性作为一等评估字段 | H5 | PIV 标注表（五预测者 × 八字段） |
| C2 | 逐场层校准结构差异：RPS 主指标 + 分解诊断 + 偏差方向签名 | H1、H2 | 72(71) 场结算表、reliability 图 |
| C3 | 路径枚举引擎的 rank-vs-mass 分裂（描述性失败模式案例） | H3 | 分轮次淘汰质量表 |
| C4 | LLM 群体信号 vs 市场共识的 asymmetric evidence 诊断 + 悬念句（Paper B 预注册载体） | H4 | 截面相关、偏离方向表、H4-ii 悬念句 |

## 2. IMRaD 骨架

### Abstract（≤250 词）
- 协议主张 + 五预测者同台 + 关键数字（RPS/Brier 反转的分量解释、93.5% 质量错配、21/21 复算）+ OSF/证据链声明
- 禁忌：无"首个"、无 pre-registered（赛后冻结的是分析协议）、无"我们预测中了"

### 1. Introduction
- **开头 hook（一段，唯一允许出现"猜中"的位置）**：前五名单覆盖全部四强（引用 TOP4 核验卡数字），随即声明"本文不以命中为证据"——基准率（史上首次 FIFA 前四全进四强）+ 快照敏感性（0.19pp 漂移）两句话消毒
- 问题：多源事前预测的可信同台评估缺协议；一次性 benchmark 的三种死法（快照漂移、预注册缺位、来源渗漏——各举本文实例）
- 贡献 4 条；阅读路线

### 2. Related Work
- 足球预测谱系（Dixon-Coles → ML）、proper scoring rules 与分解、预测市场与群体智慧、LLM 预测与 LLM 群体（Foresight Arena / Prophet Arena / ForecastBench / InfoDelphi）
- **占位防御**（v2 §2.6 + stage1 评审 CRITICAL 项）：2026 新 prior art 逐一 crosswalk——Polymarket-v1、Counterfactual Brier、Yates decomposition、Hyndman reconciliation（显式 disambiguation）、InfoDelphi
- W5 系统文献检索结果在此落地（**硬闸门，未完成前本节约谈占位**）

### 3. The Protocol（方法核心章）
- 3.1 五件套定义（git 冻结 / 来源分级 / 统一结算 / OSF 冻结 / PIV）
- 3.2 PIV 八字段定义表 + fail-loud 处置规则 + 同覆盖归一化规则
- 3.3 审计链规格：commit 级寻址、bundle 复现入口、服务端时间戳的角色（git 日期自声明 → bot commit 不可倒签 → Actions/Events/Gmail 三级服务端证据）
- 3.4 与既有实践的关系：OSF 预注册、GJP、forecast reconciliation 的边界（Check 4 缺口句）

### 4. Data：五份封存预测与证据链
- 4.1 五预测者画像（P1 Elo+Poisson / P2 Coach 混合 / P3 路径空间 / P4 kimi 群体 / P5 市场；覆盖 39/21 队的分母纪律）
- 4.2 证据保全与封存协议：快照→bundle→校验和→第三方锚（OTS/FreeTSA）；封存升级（branch protection）；破口披露（引用锚更正、每日漂移、PIV 新实例）
- 4.3 已知瑕疵处置（R1–R5 + 市场快照漂移新实例；ex-ante 版本提取规则 `88a9bfd`）
- **图 S1–S7 中 S4（Gmail）/S5（Actions）/S7（Wayback）在本节作证据链展示**

### 5. Results
- 5.1 逐场层（H1/H2，统计推断层）：RPS 主指标表 + 配对 bootstrap + BH；Murphy/Yates 分解；**硬选-Brier 反转作为分量结构表征**（插图，不当标题）；偏差方向签名（P1 平局低估 vs P2 反向）
- 5.2 队伍层（H3，描述层）：质量分布表（93.5% 错配）、冠军 log score、top-5 mass；rank-vs-mass 分裂案例
- 5.3 kimi vs 市场（H4）：截面相关三档判定、偏离方向表（阿根廷↑/葡萄牙↓ ex post 全对，**仅描述**）、同池重归一 ensemble、H4-ii 悬念句（= Paper B 预注册假设，与路线图 §2 咬合措辞一致）
- 5.4 PIV 标注结果（H5）：五预测者 × 八字段全表；协议分 × 预测分并列读法；**图 S3（B6b）/S6（B8 修正史）在此作 PIV 实例展示**
- 5.5 因子账本次要案例（A5，n=4 局限声明 + 4/104 覆盖率 + ledger 状态不一致登记）

### 6. Discussion
- 协议的可迁移性（保险/法律/医学 evidence→factor→settlement；POMDP 组件分解归属）
- 结构性边界（v2 §6 七条全保留：单届、n=72 power、市场不对称强、结果污染边界）
- 负面结果的读法（P3 过度分散、平局低估——失败模式是协议诊断力的证据，不是项目的耻辱）

### 7. Data Availability（硬资产节）
- 引用锚 `923e23a`（GitHub 公开后）+ Zenodo DOI（embargo，待归档）+ bundle 复现指令 + 校验和 + 锚定收据索引
- 声明：赛前无第三方网页存档（阴性披露）；服务端记录 400 天窗口；OSF 边界（作者已见部分结果）

## 3. 图表落位总表

| 编号 | 内容 | 类型 | 位置 |
|---|---|---|---|
| 图 1 | 协议五件套架构图 | 方法示意图 | §3.1 |
| 图 2 | 审计链时间轴（6-05 kimi 元数据 → 6-11 建仓 → 6-12 CDS → 6-13 冻结 → 7-19 结算 → 7-25 锚定） | 证据链示意 | §3.3/§4.2 |
| 图 3 | reliability diagram（P1/P2 分量对比） | 结果图 | §5.1 |
| 图 4 | 偏差方向签名（MD1/2/3 分层） | 结果图 | §5.1 |
| 图 5 | 夺冠质量分布（分轮次淘汰质量） | 结果图 | §5.2 |
| 图 6 | kimi vs 市场散点 + 偏离标注 | 结果图 | §5.3 |
| 表 1 | PIV 五预测者 × 八字段 | 核心表 | §5.4 |
| 表 2 | 五预测者总览（覆盖/n/任务层） | 数据表 | §4.1 |
| 表 3 | RPS/Brier/LogLoss + 检验 | 结果表 | §5.1 |
| 图 S1 | C12 首页（前五名单公开展示） | 补充截图 | §Intro/§4 |
| 图 S2 | B7b+B7c 双联（前五名单行级 + Red 纪律标注） | 补充截图 | §4.1 |
| 图 S3 | B6b（ef30658 西班牙 0.0484 行级） | 补充截图 | §5.2/§5.4 |
| 图 S4 | E2（Gmail 6-11 时间戳） | 补充截图 | §4.2 |
| 图 S5 | A1（Actions 148 条全景） | 补充截图 | §4.2 |
| 图 S6 | B8（875748b 修正史，主动披露） | 补充截图 | §5.4 |
| 图 S7 | C14（Wayback 第三方存档） | 补充截图 | §4.2 |
| 附 A | EVIDENCE-CHAIN 文档 + 校验和 + 锚定收据 | 补充材料 | §7 |
| 附 B | TOP4 核验卡（含基准率披露） | 补充材料 | §Intro 脚注引用 |
| 附 C | 破口披露（MANIFEST-ADDENDUM §2） | 补充材料 | §7 |

## 4. 写作闸门（挂接既有计划）

| 闸门 | 内容 | 阻塞关系 |
|---|---|---|
| W5 | 系统文献检索（Check 4 生死关） | **阻塞 §2 与定题** |
| G2 | 第三方一键复算（bundle → 关键数字） | 阻塞所有数字进稿 |
| V-kimi/V-88a | 管线验证（21/21 复算、ex-ante 提取） | 已通过预审，正式复算入稿前复核 |
| 外部盲审 κ≥0.6 | PIV 外部生存测试（stretch） | 失败 → PIV 降内部应用（预写路径，不影响 H1–H4） |
| Zenodo embargo | 证据包归档 + DOI | 投稿前必须（建议提前） |

## 5. 措辞禁忌速查（继承 v2 §7.0 + 路线图 §3.2）

- 禁："首个世界杯 LLM benchmark"、"pre-registered predictions"、"我们预测中了冠军/四强"（结果章节）、"kimi 证明了"
- 许（限定位置）："前五中四"（引言 hook + 附录 B，带基准率披露）、"描述性亮点"、"审计链"
- 必：每个数字可回溯到 commit/复算脚本；每条时间主张分层（自声明/服务端/第三方）
