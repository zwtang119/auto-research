# Decision Co-Scientist 开题工作包（交接文档）

> 状态：**已暂停，等待下一阶段**（2026-07-19，用户决策：先思考，项目暂止）
> 本目录是「医学 AI 自动科研方法论 → CDS 决策科学」方向从选题到开题的完整工作包，2026-07-18 晚至 07-19 经 goal 模式迭代完成。
>
> **🎯 给陌生读者：先读 [`PROJECT-BRIEF.md`](PROJECT-BRIEF.md)**——单文档自足的项目简报（背景、简版文献综述、设计、结论、下一步，经陌生人读者测试修订）。本 README 是面向项目内部的手册。

---

## 1. 这是什么

候选论文方向 **Decision Co-Scientist**（工作名）：把 Co-Scientist/Robin 式「假设生成→锦标赛→进化→元评审」闭环移植到 PolicySim 多智能体应急决策推演，用真实灾害档案（Factor Ledger 结算）做现实锚校准。

**当前结论**：方向判定 **GO（附条件）**。开题报告经两轮独立红队评审通过（R2：4/3/4/3/5，0 致命）；选题评价管线第二趟终裁：**首选 NeurIPS D&B，IJCAI/AAAI 主会备选，Nature ComSci 暂不够格**。唯一实质卡点：零实验结果——下一步是 MVE 最小证据链试点（古雷单场景端到端），而非继续改设计。

## 2. 文件地图

| 文件 | 内容 |
|---|---|
| `proposal-decision-coscientist.md` | **开题报告 v1.3.1**（第 0 章为给非专业读者的导读；正文为学术版；含四层评估结构、H1–H4、预注册统计方案、18–22 周进度与回退条款、64 条已核验文献、术语表） |
| `topic-eval-top-journal-2026-07-19.md` | **选题终裁 memo（第二趟管线）**：Q1/Q2/Q3 + C1–C7 逐条评分、venue 建议、7 条修正清单、拒绝条款 |
| `topic-eval-explained-em-audience-2026-07-19.md` | **选题思路详版说明（面向应急管理专业读者）**：把终裁结论的推理过程完整展开——选题怎么想出、凭什么说新、离顶刊还差什么；所有 AI/医学概念就地补释，无需计算机或医学背景 |
| `q1-novelty-and-theory.md` | Q1：LEAR / arXiv 2509.21868 / self-play 综述全文精读与区分；novelty 收窄为四点；α-Rank 替代 Elo、多样性 D 的设计修正 |
| `q2-abm-validation-and-citations.md` | Q2：ABM 验证谱系定位（POM×输出验证×history-friendly；calibration-as-fitness 两个真新成分）；SLALOM 对话；15 条引用核验 + LQS 分级 |
| `q3-validation-arm-selection.md` | Q3：非 LLM 校验臂选型（GB 50151 泡沫闸门 + ETE 疏散模型 + 水力下界），含协议草案与验证先例 |
| `q4-gulei-anchor-encoding.md` | Q4：古雷锚试编码评估（需适配可 fork，不触发 kill；sim 侧三个可观测性缺口清单） |
| `q5-second-case-selection.md` | Q5：第二锚选定（主选郑州 7·20 负锚、备选天津港 8·12；Jaipur/大连如实排除；去污设计） |
| `anchors/gulei-2015-0406.factors.yaml` | 古雷 9 条因子编码（四类俱全、双挂钩、区间锚） |
| `anchors/settlement_record.template.disaster.yaml` | 灾害域适配版结算模板 |
| `anchors/anchor-pool-pipeline.md` | 锚池建设流水线（六步法 + AI 自动化分层 Tier 0–4 + 医学文献背书映射 + 预案库矿线） |
| `reviews/r1-review.md` / `r2-review.md` | 两轮独立评审（评审子代理未接触作者侧材料） |
| `reviews/r1-response.md` / `r2-response.md` | 逐条回应记录 |
| `sources/` | 下载核验用的原文 PDF（LEAR、2509.21868、SLALOM、Grimm、Axtell 等） |

## 3. 关键判断链（一屏速览）

1. **能映射**：医学 AI 自动科研 13 要素中 6 条缺失即贡献空间；映射有三个断点（真值硬度、统计合法性、judge 效度）→ 详见 `../medical-ai-to-cds-mapping-2026-07-18.md`（v3）
2. **novelty 成立（全文级核查）**：LEAR（GECCO 2025）与 2509.21868 均不覆盖；calibration-as-fitness 收窄为三重限定组合（自然语言策略 × 历史外部真值 × 生成性闭环）
3. **理论地基**：judge 属持久性噪声源——Youden J>0、误判率 ≪10%（285B 实测）、α-Rank 替代裸 Elo、多样性 D 门槛、选择伪影对照、B4 回忆对照臂
4. **锚可建**：古雷 9 因子已编码（官方调查报告锚）；郑州负锚三要素全满分 sim 侧零成本；锚池流水线（Tier 0–4）+ 预案库行动空间矿线已设计
5. **卡点唯一**：G2 统计合法性（LLM 采样 std=0 问题）未解——W1–W4 go/no-go
6. **venue**：NeurIPS D&B（三件套：锚数据集+锦标赛基准+校准协议）首选；IJCAI 2027 备选；PoliSim@CHI workshop 降级出口

## 4. 下一阶段入口（按优先级）

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
