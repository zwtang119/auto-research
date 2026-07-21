# Decision Co-Scientist 开题工作包（交接文档）

> 状态：**开题·暂停待资源**（2026-07-19，用户决策：终裁 GO 附条件——选题、开题、Nature 标准实验方案全部交付，未投入 MVE 实施资源；规划资产归档保留，重启入口见 §4。2026-07-20 用户裁定统一状态表述，此前误写"已关闭"）
> 本目录是「医学 AI 自动科研方法论 → CDS 决策科学」方向从选题到开题的完整工作包，2026-07-18 晚至 07-19 经 goal 模式迭代完成。
>
> **🎯 给陌生读者：先读 [`PROJECT-BRIEF.md`](PROJECT-BRIEF.md)**——单文档自足的项目简报（背景、简版文献综述、设计、结论、下一步，经陌生人读者测试修订）。本 README 是面向项目内部的手册。

---

## 1. 这是什么

候选论文方向 **Decision Co-Scientist**（工作名）：把 Co-Scientist/Robin 式「假设生成→锦标赛→进化→元评审」闭环移植到 PolicySim 多智能体应急决策推演，用真实灾害档案（Factor Ledger 结算）做现实锚校准。

**当前结论**：方向判定 **GO（附条件）**。开题报告经两轮独立红队评审通过（R2：4/3/4/3/5，0 致命）；选题评价管线第二趟终裁：**首选 NeurIPS D&B，IJCAI/AAAI 主会备选，Nature ComSci 暂不够格**。Nature 标准实验方案已交付（`docs/plans/decision-coscientist-experiment-2026-07-19.md` v2）。**项目于 2026-07-19 关闭**：用户决策不再投入实施资源；全部规划资产归档于本目录、`docs/plans/` 与 `docs/reviews/`。

## 2. 文件地图

| 文件 | 内容 |
|---|---|
| `proposal-decision-coscientist.md` | **开题报告 v1.3.1**（第 0 章为给非专业读者的导读；正文为学术版；含四层评估结构、H1–H4、预注册统计方案、18–22 周进度与回退条款、64 条已核验文献、术语表） |
| `topic-eval-top-journal-2026-07-19.md` | **选题终裁 memo（第二趟管线）**：Q1/Q2/Q3 + C1–C7 逐条评分、venue 建议、7 条修正清单、拒绝条款 |
| `topic-eval-explained-em-audience-2026-07-19.md` | **选题思路与顶刊可行性说明（正式汇报体）**：选题怎么想出、凭什么说新、离顶刊还差什么；含 AI/医学基础概念解释与术语表 |
| `q1-novelty-and-theory.md` | Q1：LEAR / arXiv 2509.21868 / self-play 综述全文精读与区分；novelty 收窄为四点；α-Rank 替代 Elo、多样性 D 的设计修正 |
| `q2-abm-validation-and-citations.md` | Q2：ABM 验证谱系定位（POM×输出验证×history-friendly；calibration-as-fitness 两个真新成分）；SLALOM 对话；15 条引用核验 + LQS 分级 |
| `q3-validation-arm-selection.md` | Q3：非 LLM 校验臂选型（GB 50151 泡沫闸门 + ETE 疏散模型 + 水力下界），含协议草案与验证先例 |
| `q4-gulei-anchor-encoding.md` | Q4：古雷锚试编码评估（需适配可 fork，不触发 kill；sim 侧三个可观测性缺口清单） |
| `q5-second-case-selection.md` | Q5：第二锚选定（主选郑州 7·20 负锚、备选天津港 8·12；Jaipur/大连如实排除；去污设计） |
| `anchors/gulei-2015-0406.factors.yaml` | 古雷 9 条因子编码（四类俱全、双挂钩、区间锚） |
| `anchors/settlement_record.template.disaster.yaml` | 灾害域适配版结算模板 |
| `anchors/anchor-pool-pipeline.md` | 锚池建设流水线（六步法 + AI 自动化分层 Tier 0–4 + 医学文献背书映射 + 预案库矿线）；2026-07-19 同步 F1 宽类轨道（台风首选/地震备选）、F2 决策行动锚源金矿、Buncefield F4① 归档/镜像修正 |
| `source-inventory-2026-07-19.md` | **数据可行性附件**（2026-07-19 定向盘点）：灾害参数/后果/决策行动三层机读金矿 + 两轮网络复测 + 硬约束清单 + 最终采集指引（境内直连） |
| `anchor-authenticity-and-corpus-2026-07-19.md` | **锚真实性与语料扩容调研**（2026-07-19）：古雷/郑州双锚官方真实性核验 + 中国官方调查报告语料扩容盘点 + 国际候选评估；推荐结构「2 深 + 1–2 国外对照 + 1 宽类」；驱动 `anchors/anchor-pool-pipeline.md` §1 候选列表增补（Katrina 众院首选洪涝对照 / CSB West Fertilizer 首选化工对照 / 响水 3·21 备选锚上调） |
| `reviews/r1-review.md` / `r2-review.md` | 两轮独立评审（评审子代理未接触作者侧材料） |
| `reviews/r1-response.md` / `r2-response.md` | 逐条回应记录 |
| `idea-decision-pipeline-2026-07-19.md` | **想法备忘录（项目关闭后用户补充，未评审）**：决策流水线——把 CDS 决策科学拆成 Agent 负责的流水线步骤，面对从未见过的风险仍能走完决策流程 |
| `sources/` | 下载核验用的原文 PDF（LEAR、2509.21868、SLALOM、Grimm、Axtell 等） |

## 3. 关键判断链（一屏速览）

1. **能映射**：医学 AI 自动科研 13 要素中 6 条缺失即贡献空间；映射有三个断点（真值硬度、统计合法性、judge 效度）→ 详见 `../medical-ai-to-cds-mapping-2026-07-18.md`（v3）
2. **novelty 成立（全文级核查）**：LEAR（GECCO 2025）与 2509.21868 均不覆盖；calibration-as-fitness 收窄为三重限定组合（自然语言策略 × 历史外部真值 × 生成性闭环）
3. **理论地基**：judge 属持久性噪声源——Youden J>0、误判率 ≪10%（285B 实测）、α-Rank 替代裸 Elo、多样性 D 门槛、选择伪影对照、B4 回忆对照臂
4. **锚可建**：古雷 9 因子已编码（官方调查报告锚）；郑州负锚三要素全满分 sim 侧零成本；锚池流水线（Tier 0–4）+ 预案库行动空间矿线已设计
5. **卡点唯一**：G2 统计合法性（LLM 采样 std=0 问题）未解——W1–W4 go/no-go
6. **venue**：NeurIPS D&B（三件套：锚数据集+锦标赛基准+校准协议）首选；IJCAI 2027 备选；PoliSim@CHI workshop 降级出口

## 4. 若未来重启：入口（按优先级）

0. **执行蓝图**：`docs/plans/decision-coscientist-experiment-2026-07-19.md`（Nature 标准，经 builder + 设计评审 v2；MVE 在 W12–W14，四个 go/no-go 闸门）——重启时以此为据
1. **MVE 最小证据链**：古雷单场景 C0 vs C2 端到端试点（锦标赛+进化+校验臂+锚对照），兼作成本试跑与 G2 探针——估 4–6 周，是 GO 的硬前提
2. G2 统计合法性工作（LHS+种子+版本钉死；不过则按预写条款转方法短文）
3. 郑州因子编码（1 人日）+ Buncefield 第三锚（跨辖区）
4. 跨底座复现（DeepSeek-V4 + 开源模型）
5. 资产发布包（锚数据集、fork schema、锦标赛协议、校验臂代码、预案语料库）
6. 专家 panel 招募（≥3 名，盲评需要）

## 5. 与其他方向的关系（防重复建设）

- **C1（AI 研究系统过程 trace）**：唯一在轨顶刊方向，互补并行；本方向建设过程持续为其供 trace
- **Tsinghua `ideas/09`（古雷回顾性验证）**：三轴切割（09=事后政策调整/效应本体/十年尺度；本方向=现场处置策略/因子结算/56 小时尺度），资源紧张时按预写条款合并
- **P1+P2 合并规划**：本方向已实质接替其主干位置
- **evolution-medical-ai**：医学文献情报源（`references/papers/` + `docs/investigations/ai-scientist-papers-review-2026-07-18.md`）

## 6. 本次会话还修正了

- `../medical-ai-to-cds-mapping-2026-07-18.md` 参考文献 #10：LEAR 作者 "Gurkan, A." → "Gurkan, C." 并换 ACM 正式 DOI（Q2 核验发现的勘误）

### 2026-07-19 后续修订

- **场景清单纠错**：「企业洪水」为合成调试场景（无真实数据），全部正式文件（PROJECT-BRIEF、详版说明、开题报告 §5.1）改为「古雷、郑州两个历史场景 + 广西横州洪水（六蓝水库溃坝，2026-07）真实案例（零污染锚储备）」；合成场景仅作开发调试。
- **sources/ 补充**：Co-Scientist、Robin 两篇 Nature 官方全文 PDF + self-play 综述 PDF（来自 evolution-medical-ai/references，可了结 R1 评审 E7 挂起的 Robin 88%/61% 引用核验）。
- **兄弟仓库评估结论**（2026-07-19，三+七仓库逐一深挖）：cds4worldcup 的结算 schema 三件套与防泄漏治理为最有价值资产（已补登 §8 外部资产）；cds4polymarket/ab-test 有实验治理方法论与外交预测断言账本，但无统计机器；evolution-medical-ai 除文献 PDF 外无价值（mock demo）；0ref 下 institute-one、Mammalia-tree、MiMo-Code、MiroFish、deputy-agent、A2UI、skill 七仓库对项目硬能力（分布统计、α-Rank、judge 校准、G2、锚分离）均无帮助，仅 MiMo-Code 的评审聚合机械与 skill/Frontier-Engineering 的任务契约可作设计阅读。

### 2026-07-19 收尾

- **实验方案交付**：rp-deep-plan 全流程（Up-front 用户四问 → 双侦察 → Nature 合规与统计工具链外部调研 → builder 骨架合并 → 设计评审折入 v2），产出 `docs/plans/decision-coscientist-experiment-2026-07-19.md` 与 `docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md`。
- **项目关闭**：用户决策结束本项目，未投入实施资源；状态由「暂停」转为「关闭」。若未来重启，§4 入口与实验方案仍然有效。

### 2026-07-19 想法补充（项目关闭后）

- **决策流水线**：用户补充想法——参照 AutoResearch 协议，将 CDS 决策科学拆分为流水线、由 Agent 各管一步，使系统面对从未见过的风险仍能走完决策流程（核心机制：案例知识缺席时各步骤降级而非崩溃；无知清单 + 置信度分级如实呈现）。已记录为 `idea-decision-pipeline-2026-07-19.md`，未评审、未纳入开题报告，供重启时评估。

### 2026-07-19 决策流水线评估包（项目关闭后，平行于冻结 v1.3.1）

> 用户补充的「决策流水线」想法（idea-decision-pipeline-2026-07-19.md）经 5 阶段评估管线产出完整评估包；红队 4/3/3/3/4、fatal=0；终裁建议选项 1 GO（附 hard checkpoint），待用户拍板。所有文档为新增平行产物，不修改已冻结的开题报告 v1.3.1 与 PROJECT-BRIEF v1.3。

| 文件 | 内容 |
|---|---|
| `adjacent-work-positioning-2026-07-19.md` | 阶段 1 相邻工作定位：workflow 谱系 5 邻居 + 应急 SOP 文献 + 降级协议先验；贡献落点=流程固化+降级协议显式化 |
| `pipeline-design-spec-2026-07-19.md` | 阶段 2 设计规范（v1.1）：8 步 I/O 契约 YAML、降级 DAG、GO_L0/L1 分级 hard checkpoint、固定 8 步编排论证 |
| `asset-mapping-2026-07-19.md` | 阶段 3 资产映射：8×6 矩阵 + 缺口清单 + 4 项最小改造（真实代码改动 1-2 个文件）；如实标注 6 角色与两个零实现 |
| `redteam-review-2026-07-19.md` | 阶段 4 独立红队评审：五维 4/3/3/3/4、fatal=0、6 严重问题（v1.1 已闭环 2 条、其余已处置） |
| `ruling-memo-2026-07-19.md` | 阶段 5 终裁 memo：4 视角/12+ Path/Gate 4/三选项，建议选项 1 GO + 最小验证设计（横州六蓝纸面走 8 步） |

过程文件（中间稿，非交付物）在 `auto-research/prompt-exports/`：oracle-plan-2026-07-19-160143-a42bf4-2a67.md（总计划+执行日志）、stage1/2/3-recon-*（侦察交接）、stage4-code-audit.md（改造量复核）、stage5-recon-venues.md（venue 候选）。

### 2026-07-19 文档修订（按 revision-brief Item 4）

- **`anchors/anchor-pool-pipeline.md`**：§1 候选列表增补宽案例类轨道两行（台风首选 IBTrACS/CMA/省级响应/EM-DAT、地震备选 USGS FDSN，N≥60 旁证层）并按 F4① 将 Buncefield 行从「HSE 直链全文已验证」改为「HSE 直链 404，改用英国国家档案馆 webarchive 归档或 FABIG 镜像，Crown copyright 非商用」；§3 步骤 1 筛选增宽类准入（三层机读 + 样本量门槛），步骤 2 档案获取按 F2 补决策行动锚源金矿（mem.gov.cn 国家防总响应省厅防风响应 + JMA XML + IFRC GO actions_taken + NWS CAP + NTSB/CSB）及宽类通道；§4 Tier 1 金矿源同样按 F1/F2 扩充并以 Buncefield F4① 修正；§5 登记 `source-inventory-2026-07-19.md` 为数据可行性附件（含三层金矿 + 硬约束 + 采集指引）。
- **`anchors/anchor-pool-pipeline.md`**（按 `anchor-authenticity-and-corpus-2026-07-19.md` 修订）：§1 候选列表增补国外对照锚（Katrina 众院《A Failure of Initiative》首选洪涝对照 / CSB West Fertilizer DocumentId=694 首选化工对照；BP Texas City / Chevron Richmond / 参院 / IPET 列为可选附件）、国内化工备选锚（天津港 8·12 gov.cn PDF 实测 200 / 响水 3·21 经栏目页进入，原直链 404 标注迁移），从「已排除」行移除响水 3·21 并上调至备选锚；末尾追加推荐结构「2 深 + 1–2 国外对照 + 1 宽类」及修订注记。
- **`README.md`**：文件地图新增 `source-inventory-2026-07-19.md` 行（数据可行性附件，同步报表）并同步 `anchors/anchor-pool-pipeline.md` 行说明（标注 F1/F2/F4 本轮修订点）。
