# Decision Co-Scientist — 主题导航（dreaming D2 · B 簇 26 篇）

> 生成：2026-11-09｜覆盖 `index.json` topic=`Decision Co-Scientist` 的 26 篇，全部 `dormant`
> 性质：导航页；状态准绳以 [`CLAUDE.md`](../../CLAUDE.md) 当前活跃主线表为准。不改任何原文。

## 当前有效结论

- 方向终裁 **GO（附条件）**；开题 v1.4 + Nature 标准实验方案 v2.1 已交付，**未投入 MVE 实施资源**。统一状态表述：**开题·暂停待资源**（`README.md:3`，用户 2026-07-20 裁定；该行明确「此前误写『已关闭』」）。
- ⚠️ **状态措辞冲突**：`PROJECT-BRIEF.md:4` 仍写「已关闭（2026-07-19 晚完成一轮后关闭进化）…2026-07-19 用户决策：结束项目」。与 README:3 的纠正并存。**只标注、不裁决**，按 `CLAUDE.md:16`「开题·暂停待资源」为准绳。
- 投稿目标：首选 **NeurIPS Datasets & Benchmarks**（锚数据集 + 锦标赛基准 + 校准协议三件套）；IJCAI 2027 主会备选；AAAI 2027 时间过紧不列；Nature Computational Science 需一年以上多案例（`PROJECT-BRIEF.md:17`、`README.md:14`）。
- durable identity = 「SOP 范式 + LLM 步骤级降级协议 + 已知-推断-无知清单三档」三者耦合点（`ruling-memo-2026-07-19.md:29`）。
- 核心机制是**降级而非崩溃**：任一步失效输出显式置信度降级标记，最终简报如实呈现依据/推断/无知（`idea-decision-pipeline-2026-07-19.md:26`）。

## 权威链

| 文档 | 角色 | 状态 |
|---|---|---|
| [`README.md`](../../docs/investigations/decision-coscientist-proposal/README.md) | 项目内部手册，陌生读者先读 BRIEF | 状态口径以此为准（含 2026-07-20 纠正） |
| [`PROJECT-BRIEF.md`](../../docs/investigations/decision-coscientist-proposal/PROJECT-BRIEF.md) | 单文档自足简报（经陌生人读者测试修订） | 状态措辞与 README 冲突，见上 |
| [`proposal-decision-coscientist.md`](../../docs/investigations/decision-coscientist-proposal/proposal-decision-coscientist.md) | 开题 v1.4（F5 settleability 切割 + F1 宽类轨道 + F4 修链 + F2/F3 锚源升级） | R1、R2 两轮独立评审通过并逐条回应 |
| [`decision-coscientist-experiment-2026-07-19.md`](../../docs/plans/decision-coscientist-experiment-2026-07-19.md) | 实验方案 v2.1，Nature 标准 | **最终交付物，未执行** |
| `q1`–`q5` 备忘录 | novelty 谱系 / ABM 验证 / 非 LLM 校验臂 / 古雷因子编码 / 第二案例 | 均标「完成」（调研级） |
| `reviews/r1-*` `r2-*` | 两轮独立评审 + 逐条回应 | R2 通过满足 goal 终止条件 (a) |
| [`plan-critique-decision-coscientist-experiment-2026-07-19.md`](../../docs/reviews/plan-critique-decision-coscientist-experiment-2026-07-19.md) | 有界设计评审（批评者视角） | **未签 implementation-ready** |
| [`revision-brief-2026-07-19.md`](../../docs/investigations/decision-coscientist-proposal/revision-brief-2026-07-19.md) | 外科手术式修订原则：不动骨架、不动已通过终裁、不重写 H1/H2 | 修订纪律准绳 |

## 已验证数字（转录原文 `path:line`，未独立复算）

- 两轮红队评分**有两组并存**：`README.md:14` 记 R2 为 `4/3/4/3/5`（0 致命）；`ruling-memo-2026-07-19.md:7` 记红队评审 v1.0 为 `4/3/3/3/4`（fatal=0）。**对象/版本不同，勿合并、勿取平均**，需回查原评审报告定版本。
- H3 预注册汇总规则：两案 ≥8 条裁定因子中 `supported ≥60%` 且无因子族系统性 rejected → 成立；`<40%` → 不成立；其间 inconclusive 并公布明细（`reviews/r1-response.md:10`）。
- 误判率必须**远低于 10%**：依据 285B 参数实验，10% 随机误判足以抹平进化全部增益（`proposal-decision-coscientist.md:36`）。
- 古雷 9 条因子完成编码，全部进 `calibration_status: tracking`，无一条因故剔除（`q4-gulei-anchor-encoding.md:19,73`）。
- 评估池：两深案合计 ≥8 条可裁定因子 + 宽类评估池 N≥60（H3 旁证）（`docs/plans/decision-coscientist-experiment-2026-07-19.md:15`）。
- 锚池推荐结构：**2 深（古雷 + 郑州）+ 1–2 国外对照 + 1 宽类**；化工对照首选 CSB West Fertilizer，洪涝对照首选 Katrina 众院报告（`anchors/anchor-pool-pipeline.md:26`）。

## 撤回与陷阱

- ❌ **评委自身不稳定**：更换 judge 模型会使评估结论从「不确定」翻转为「强」（`PROJECT-BRIEF.md:43`、`topic-eval-explained-em-audience-2026-07-19.md:28`）。生成侧与 judge 同源模型的共模噪声未讨论（`reviews/r1-review.md:53`）。
- ❌ 两篇 mem/gov.cn 直链实测 **404**（响水通报、欣佳）；引用须从栏目页或省政府批复页进入并标注迁移状态（`anchor-authenticity-and-corpus-2026-07-19.md:58`）。
- ❌ 浙江 `yjt.zj.gov.cn` 境内直连可爬、仅境外 IP 受限；**旧「只能走媒体源」结论作废**（`asset-mapping-2026-07-19.md:57`、`revision-brief-2026-07-19.md:21`）。
- ❌ Zinkevich 2007 (CFR) 页码以 DBLP **1729–1736** 为准，流传的 905–912 系印刷版本混淆（`q2-abm-validation-and-citations.md:51`）。
- ❌ 摘要级证据不能支撑「❌ 无 per-step 置信度」这类二值「明确缺失」判定（`redteam-review-2026-07-19.md:55`）。
- ❌ 复现 ≠ 解释：宏观对上不等于微观机制被验证，结论措辞限定在后果分布层（`q2:24`）。
- ❌ EvoAgent 标题歧义等 **3 条待复核项**未闭合（`adjacent-work-positioning-2026-07-19.md:7`）。
- ❌ `r1-review.md:50` 曾指出 H1「优于」无评分规则且评估锚集与适应度存在循环风险；回应见 `r1-response.md`，勿跳过直接引用结论。

## 未决

| 项 | 状态 |
|---|---|
| MVE 实施 | 未投入资源；开题·暂停待资源 |
| GO 附条件 | 条件未逐项销项 |
| implementation-ready | 未签核（plan critique / Phase 6 审查「需修订后签核」） |
| Nature ComSci | 暂不够格，需一年以上多案例 |
| PROJECT-BRIEF vs README 状态措辞 | 两处不一致，只标注待澄清 |
| E1 类后续实验 | 不在本簇，见 `governance-wiki.md` |

## 原文入口

[`docs/investigations/decision-coscientist-proposal/`](../../docs/investigations/decision-coscientist-proposal/) ｜ [`docs/plans/decision-coscientist-experiment-2026-07-19.md`](../../docs/plans/decision-coscientist-experiment-2026-07-19.md) ｜ [`docs/INDEX-DETAILS.md`](../../docs/INDEX-DETAILS.md) B 节 ｜ [`docs/index.json`](../../docs/index.json)

> 本页由 dreaming 生成，写入新目录，原文 0 改动。数字均转录并标 `path:line`，未独立复算研究结论。
