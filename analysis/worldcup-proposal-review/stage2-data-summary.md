# Stage 2 数据摘要：足球预测 / LLM forecasting / 概率预测校准 文献与趋势分析

- **生成日期**：2026-07-21
- **配套数据**：`analysis/worldcup-proposal-review/stage2-literature-table.csv`（37 行，全部经联网核实，verified 37/37 = 100%；无 unverified 条目）
- **核实方式**：arXiv API 批量核验（15 条）、GitHub API（4 个仓库，含 commit 时间线）、Preprints.org 全文抓取（经 r.jina.ai）、大学官网新闻、Thinking Machines 官网、出版商页面；语义学者/OpenAlex 引用计数 API 均被限流（429），引用数未系统采集，已在表中以版本状态替代。
- **分析工具**：data-analysis skill 工作流（DuckDB SQL；skill 沙箱脚本路径 `/mnt/skills/...` 在本机不存在，按 skill 规范以本地 DuckDB 等价执行：年份/domain/type/relevance 分布、交叉表、关键词频次）。
- **基线对照**：v1.3 §2 + §10 参考文献 13 条；W6 备忘录 §2 占位风险表；F2/F3 prior art 清单。

---

## (i) 关键研究趋势

1. **领域重心三年三迁**：2024"LLM 能否预测"（Halawi NeurIPS 2024）→ 2025"动态无污染 live 基准"（ForecastBench ICLR 2025、Prophet Arena）→ 2026"结算层与训练侧"（Polymarket-v1 链上结算档案、Foresight Arena 链上 commit-reveal、RL/verbalized 校准训练）。年份分布呈明显指数化：2024 年 4 条、2025 年 7 条、2026 年 24 条（占 65%）。
2. **评分规则方法学复兴**：2026 年出现 Yates 协方差分解重排（arXiv:2603.05544，2026-06-22 v2）、Murphy 分解在 live 市场的实证应用（arXiv:2605.03310）、Foresight Arena 的 Alpha Score、ForecastBench 团队的 Brier Index 方法学更新（2026）——"单一总分 → 分解诊断"是明确的范式信号，直接支持 v2 §5 把 Brier 拆为校准/区分分量。
3. **2026 世界杯催生 6+ 个直接竞品，但存在"结算空窗"**：三个 GitHub artifact（WorldCupBench / worldcup-predictor-2026 / ai-world-cup）的最后一次提交分别为 2026-06-12 / 06-30 / 06-11，**截至 2026-07-21 无一发布赛后总结算**；学术侧 Hartvég v1（2026-07-10）明确"赛后评估为 future work"。联网未检出任何已完成赛后 LLM 世界杯预测结算的同行评审论文。这是 v2 的窗口期证据。
4. **"LLM vs 市场/人群共识"成为 2025–2026 热点**：AlDahoul（consensus bias）、Wisdom of the Silicon Crowd、Royal Society 2026（accuracy–correlation effect）、AIA Forecaster（LLM+market ensemble）、Merger-arb ICML 2026（Brier 超市场 24%）。v1.3 H4 落在拥挤赛道，必须以"赛前冻结同日截面 + 覆盖分母诚实"差异化。
5. **评估协议完整性开始被指标化**：Hartvég 的 SVS/THR（结构效度/幻觉率）、Foresight Arena 的 commit-reveal 协议与 power analysis（区分 α*=0.02 需 ~350 个已结算预测）、Bosse 的自动 resolution 准确率（95%）——协议维度从脚注升格为可计算字段，为 v2 的 Protocol Integrity Vector 提供文献土壤（也提供小样本辩护引证）。

## (ii) 方法论创新点（可作 v2 §3/§5 锚点）

| 锚点 | 来源 | v2 用法 |
|---|---|---|
| Murphy 分解拆分 Brier = 校准 + 区分 | arXiv:2605.03310；经典 Murphy 1973 | §5 主指标 RPS + Brier 分解分量 + reliability diagram |
| Yates 重排：方差失配 / 相关赤字 / 大样本校准三非负项 | arXiv:2603.05544 v2 2026-06-22 | §5 指标定义的理论更新引证 |
| Commit-reveal 冻结 + power analysis 小样本阈值 | arXiv:2605.00420 | §5.5 冻结纪律与 n=72 推断力的诚实边界引证 |
| 信息不对称消融（同质证据 → herding） | arXiv:2607.01661 (InfoDelphi) | H4 升级：从"是否可区分"到"何种 asymmetric evidence 缺位" |
| LLM ensemble 聚合 = 人群智慧复现 | arXiv:2402.19379 (Silicon Crowd) | §2.5 P4 的最直接先验；H4 判定规则参照 |
| 反事实 Brier（IPW 构造反事实验证集） | Keogh & van Geloven, Epidemiology 2024 | §5 replay/反事实评估的跨域借用声明 |
| Brier 作 RL 可验证奖励 | arXiv:2607.00164；Mantic 2026-03 | §2.5 训练侧校准新谱系 |

## (iii) 研究空白与 v1.3 §2 需补充的具体文献方向

v1.3 §2 现有 13 条引用与本表 37 行的交集仅 3 条（Gneiting-Raftery 2007、Halawi 2024、Prophet Arena 2025），**差集 34 条**。按谱系归并，v2 §2 必须补六个方向：

1. **LLM 群体/集成预测谱系（§2.5 最大缺口）**：Schoenegger et al. 2024（Wisdom of the Silicon Crowd）、Royal Society 2026 accuracy–correlation、Iadisernia & Camassa 2025（LLM personas 宏观预测，见 arXiv:2606.13038 引文）。v1.3 讨论 P4"LLM 群体信号"却零引该谱系。
2. **Brier 分解与评分规则 2024–2026 新进展（§2.3）**：Yates 重排（2603.05544）、Murphy 分解实证（2605.03310）、评分规则综述（2504.01781）、pena.lt 2025 对 RPS 的批评性讨论。
3. **预测市场微观结构与结算层（§2.4）**：Polymarket-v1（2606.04217）、Foresight Arena（2605.00420）、Hindcast（2607.14051）、PolyBench（2604.14199）。v1.3 仅有 Wolfers-Zitzewitz 2004 一条 22 年前的文献。
4. **训练侧校准方法（§2.5 新增小节）**：ConfTuner（NeurIPS 2025）、Verifiable Rewards（2607.00164）、ADVICE（2510.10913）、Mantic/Thinking Machines（2026-03）、action-belief gap（2511.13240）。
5. **2026 世界杯直接竞品 crosswalk（§2.6 novelty 声明的承重墙）**：WorldCupBench、worldcup-predictor-2026、ai-world-cup、Hartvég、AlDahoul、ModelBall、LMU SoccerArena、Rezaei & Samadi（2606.24171）——v1.3 §2.6 自述"有限核查"，此八项正是被核查漏掉的全部。
6. **"reconciliation" 同形异义 disambiguation（F3 指定必须项）**：Hyndman 多变量层级 reconciliation（2605.17920）vs AIA supervisor reconciliation（2511.07678）vs 本项目结算对账——三个含义须在 §2 一次性切开。
7. **经典足球 ex-ante 谱系补引（§2.1）**：Dubitzky 2019 Soccer Prediction Challenge（RPS 事前提交）、Bunker 2024 综述。

**真正空白（联网未检出占位）**：把"协议完整性/审计链状态"结构化为 benchmark 一等标注字段并与 proper score 联合发表的工作，在足球预测与通用 forecasting 文献中均未发现（Hartvég 的 SVS/THR 是最接近者，但只覆盖输出结构效度，不覆盖 ex-ante 有效性/快照漂移/来源渗漏）。与 W6 终裁判断一致，该红线可守但窗口依赖"结算空窗"持续。

## (iv) 占位风险评估表

威胁等级：●●● 高 / ●● 中 / ● 低（维度：framing 重合度 × 活跃度 × 学术分量）。

| 竞品 | 威胁 | 状态（2026-07-21 核实） | v2 需要的 disambiguation（一句话） |
|---|---|---|---|
| Hartvég et al. (Preprints.org 202607.0719) | ●●● | v1 2026-07-10，非同行评审，赛后评估为其 future work | 本文不是"LLM 世界杯 benchmark"，而是同一审计链下五类**异质方法**（含统计/市场）的事后结算比较，协议完整性是一等评估轴 |
| LMU LLM SoccerArena | ●●● | 三校联合 live leaderboard，赛中每日更新，赛后论文高概率 | 本文考生含非 LLM 方法与市场基准，且全部预测赛前 git 冻结、评估协议 OSF 冻结——不是 leaderboard 而是对照实证 |
| AlDahoul et al. (SSRN 6900538) | ●●● | 预印本，主题=LLM 是否复述公众共识，与 H4 同形 | H4 不问"LLM 是否有共识偏差"（描述性），而问赛前同日截面上群体信号与市场是否统计可区分，判定规则预注册 |
| WorldCupBench | ●● | 2026-06-12 后停更，leaderboard 占位符仍为空，无赛后结算 | 本文交付的是已完成结算 + 复算验证的比较实证，非冻结后未阅卷的预测集合 |
| ModelBall / Gibbins | ●● | 作者自托管 PDF，无同行评审，n=4 模型 | 本文不做"过度自信"全称主张；只做可靠性图支持的分箱校准描述（W6 §8.2 纪律） |
| worldcup-predictor-2026 | ●● | 2026-06-30 停更，三臂设计完整但无赛后总评 | 本文差异在方法族异质性（五类考生）与审计链，不在单 LLM 多臂消融 |
| ai-world-cup | ● | 2026-06-11 停更，仅免费模型 | 同上，且工程 artifact 非学术发表 |
| ForecastBench / Prophet Arena | ●● | 持续活跃，通用 live 基准 | 本文是单赛事多方法结构差异研究，不与通用基准比规模；其 Brier Index/Murphy 分解为本文指标方法引证来源 |
| Foresight Arena | ●● | v2 2026-05-04，live 结果未发布 | 本文评估对象是"预测者"而非链上 agent；其 power analysis 反被本文引为小样本边界依据 |
| Polymarket-v1 / Hyndman reconciliation / AIA supervisor | ● | 方法近邻，非同题 | 术语 disambiguation：settlement reconciliation ≠ 层级时序 reconciliation ≠ agent 输出调和 |

## (v) 供 Stage 3 图表直接使用的数据块

### D1. 年份—数量序列（文献趋势图）

| 年份 | 条数 |
|---|---:|
| 2007 | 1 |
| 2019 | 1 |
| 2024 | 4 |
| 2025 | 7 |
| 2026 | 24 |

（2007 = Gneiting-Raftery 经典锚点；2019 = Dubitzky。若画趋势图建议 2024–2026 为主视图，经典条目作背景注记。）

### D2. domain 分布计数（谱系结构图）

| domain | 条数 | 其中高相关 |
|---|---:|---:|
| LLM预测 | 12 | 6 |
| 足球预测 | 11 | 6 |
| 校准方法 | 10 | 3 |
| 预测市场 | 4 | 2 |

### D3. 类型分布（证据等级图）

| type | 条数 |
|---|---:|
| 论文(预印本) | 15 |
| 论文(同行评审/经典) | 8 |
| 行业项目/artifact | 7 |
| 基准(含预印本) | 7 |

### D4. 占位风险分级计数（威胁热力图，仅限 10 个直接竞品/近邻）

| 威胁等级 | 数量 | 成员 |
|---|---:|---|
| ●●● 高 | 3 | Hartvég、LMU SoccerArena、AlDahoul |
| ●● 中 | 5 | WorldCupBench、ModelBall、worldcup-predictor-2026、ForecastBench/Prophet Arena（合并计）、Foresight Arena |
| ● 低 | 2 | ai-world-cup、方法近邻组（Polymarket-v1/Hyndman/AIA，合并计） |

### D5. 方法关键词 Top 频次（词频图，DuckDB 统计）

Brier 8；Elo 2；Murphy decomposition 2；RPS 2；agentic 2；fine-tuning 2；leaderboard 2（其余均 1 次，共 60+ 个独立关键词——长尾特征本身说明方法碎片化，v2 可用"协议/结算"维度做收敛叙事）。

### D6. v1.3 §2 覆盖差集（缺口图）

- 已在 v1.3：3/37（Gneiting-Raftery 2007、Halawi 2024、Prophet Arena 2025）
- 差集（v2 候选新增）：34/37，其中高相关 15 条、中相关 16 条、低相关 3 条
- 六个补引方向见 §(iii) 清单

---

## 附：核实留痕与局限

- GitHub commit 时间线（gh api）：WorldCupBench 最后提交 2026-06-12T14:32Z（`[skip ci] auto: update scores`）；worldcup-predictor-2026 最后 2026-06-29/30（knockout web arm #32）；ai-world-cup 最后 2026-06-11；Hicruben 2026-07-19 仍活跃（81 stars）。
- arXiv 版本状态（export.arxiv.org API，15 条 id_list 批量）：全部存在且版本日期与 F2/F3 登记一致；Hindcast 2607.14051 为 2026-07-15 新发。
- Hartvég 全文经 r.jina.ai 抓取确认：三层任务 + SVS/THR/Mainstream Index 指标 + "tournament not yet completed at time of study"（赛后评估未完成）。
- 引用计数：Semantic Scholar 与 OpenAlex API 均 429 限流，未采集；如需引用数维度，建议 Stage 3 前用带 API key 的 S2 批量补一次。
- 未发现项（负面结果同样记录在案）：截至 2026-07-21，未检出已完成 2026 世界杯赛后 LLM 预测结算的同行评审论文；未检出"protocol integrity 作为 benchmark 标注字段"的同名先例。
