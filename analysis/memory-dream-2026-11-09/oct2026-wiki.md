# 2026-10 token / tsinghua / reprompt — 主题导航（dreaming D2 · C 簇 36 篇）

> 生成：2026-11-09｜覆盖 `index.json` 三个 2026-10 topic：token 16 + tsinghua 18 + reprompt 2 = 36 篇（active 34 / 挂起 2）
> 性质：导航页。token 数字以 [`token-accounting-wiki.md`](token-accounting-wiki.md) 为准；本页管 tsinghua / reprompt 与权威链。不改任何原文。

## 当前有效结论

- **token 核算**：论文主表 5,220 条采用集 / native total **32,261,917**；不是全项目最终消耗。生产消费交接 `WAITING_APPROVAL`（详见 [`token-accounting-wiki.md`](token-accounting-wiki.md)）。
- **1025 vs 五月**：多轮处理包总体增量最稳定；MA 主要表现为竞争意识、其他质量维度及模型间权衡；**显式 DNA 没有跨结构一致的正增益**。五月→1025 MAMR 评分上升，但评委与模型服务发生变化，**不能归因为系统能力进步或 DNA 作用**（`tsinghua-1025-vs-may-2026-10-27.md:7`）。
- **DNA 协议等价性**：不能保证除 DNA 外所有实际因素相同；已证实路由、评分后处理、恢复实现存在差异，历史细节有不可考部分 → **正式实验 no-go**（`tsinghua-dna-protocol-equivalence-2026-10-23.md:4`）。
- **视觉预检**：3 份预备 PDF 已完成离线构建、CJK 实际字体与完整可见正文检查通过；**视觉未确认**，不能称视觉通过 / Kami READY / 最终交付，**暂不据此锁版或启动 630 批量**（`tsinghua-report-visual-preflight-2026-10-27.md:5`）。
- **会话时间复算**：覆盖 33 个有实质 turn 的会话（319 去重 turn），剔除工具执行后可实测的「模型思考/生成」全项目仅 **8h52m**，占可拆解 turn 时长 27.7%、占 turn 时间区间并集 13%；约 **81%** 的 turn 时间是「折叠/挂起」。前次 11 会话调查有两处方法污染，本报告修正（`reprompt-all-sessions-model-vs-tool-time-2026-10-27.md:5,19`）。
- **clean release**：用户 2026-10-27 裁定**首版交付优先**——已验收产物独立交付，缺项标注不阻断使用，不以追加审计代替交付（`docs/progress/2026-10-27-tsinghua-clean-release-progress.md:29`）。

## 权威链（本簇最大风险：同名文档的过时状态）

| 文档 | 权威关系 |
|---|---|
| [`tsinghua-dna-ablation-2026-10-23.md`](../../docs/plans/tsinghua-dna-ablation-2026-10-23.md) | v3 **状态与参数已过时**（:5 自述）；最新执行状态以 `tsinghua-dna-ablation-handoff-2026-10-23.md` 为准（:9） |
| [`tsinghua-factorial-ablation-evaluation-2026-10-25.md`](../../docs/plans/tsinghua-factorial-ablation-evaluation-2026-10-25.md) | v3.1 **唯一权威设计**；实现仍为 v2，当前未 ready（:3, :9）；历史审计 S1/桥接等候选已被用户最终裁定取代 |
| [`tsinghua-clean-release-2026-10-27.md`](../../docs/plans/tsinghua-clean-release-2026-10-27.md) | 计划定稿，含包级并行排程；**本轮仅规划，不实施、不 commit/push**（:3） |
| [`tsinghua-1024-dna-value-identification-2026-10-27.md`](../../docs/plans/tsinghua-1024-dna-value-identification-2026-10-27.md) | 研究设计首版，**未执行**；1024 是实验代号，不回填为 2026-10-24 的预注册（:3） |
| [`tsinghua-dna-ablation-report-adapter-2026-10-26.md`](../../docs/plans/tsinghua-dna-ablation-report-adapter-2026-10-26.md) | **仅方案，未实施**（:3） |
| [`token-report-paper-accounting-2026-10-27.md`](../../docs/investigations/token-report-paper-accounting-2026-10-27.md) | 冻结核算 `paper-accounting-v1`，现行论文口径；`index.json` 标「挂起」是索引派生状态，非文档自述 |
| token 其余 9 篇 + 计划 6 篇 | 取代关系见 [`token-accounting-wiki.md`](token-accounting-wiki.md)「权威链」 |

## 已验证数字（转录原文 `path:line`，未独立复算）

- 1025 首版：360 样本 × 三格式 = **1,080 份** JSON/HTML/PDF；`5,365 文件 / 770MB`；状态 **FIRST_DELIVERY**，终验 **INCOMPLETE** 已标注（`docs/progress/2026-10-27-tsinghua-clean-release-progress.md:25`）。
- 正式生成 **0/630**，已暂停；小试 18 调用中 GPT 两次摘要空、DeepSeek 两次正文空、GLM 评分正文空（`tsinghua-dna-protocol-equivalence-2026-10-23.md:10`）。
- 用户批准 **1 份综合 + 全部 360 份逐案例** PDF 报告，可并行（`tsinghua-factorial-pdf-reports-2026-10-27.md:3`）。
- 预检 3 样张 = 旧冻结 SASR×1 + MAMR×2，每份含三评委；不读活跃 D、不消费最终 1890 数据（`tsinghua-report-visual-preflight-2026-10-27.md:9`）。
- token 关键数字（32,261,917 / 47,293,807 / 20,974,154 / 35,152,364）见 [`token-accounting-wiki.md`](token-accounting-wiki.md)，**四者不可相加**。

## 撤回与陷阱

- ❌ **「3 月实验」不存在**：`mc-2026-03-01` 在 158 个 commit 中零痕迹；3 月日期的 `draft-0316.md` 底稿是 2 月试验，全文无 token 数字（`token-report-imputation-feasibility-2026-10-26.md:32,63`）。
- ❌ **T2 恒 NO-GO 不得改/绕过**；1023 统计脚本 hash 冲突 **BLOCKED**；用户既有授权不可外推（`docs/plans/token-consumption-handoff-2026-10-27.md:12`）。token 最终门禁的提供方与可消费证明未闭合（`tsinghua-clean-release-critique-2026-10-27.md:13`）。
- ❌ `evaluation_differences` 才是分类权威，**`duplicate_differences` 已废**；有效基线列须联读 `evaluation_differences`（`tsinghua-clean-release-critique-2026-10-27.md:21`）。
- ❌ 不扫描 `latest` 猜终态；状态变化以所属执行者正式交接后直接核验为准（`tsinghua-clean-release-2026-10-27.md:22`）。
- ❌ 机器检查与目视状态分开；来源/修订映射不清、输入 hash 变化、正文/数字不一致或泄密则停问，不得猜（`tsinghua-factorial-pdf-reports-2026-10-27.md:26`）。
- ❌ 限定评审结论 ≠ implementation-ready（`tsinghua-dna-ablation-critique-2026-10-23.md:4`「需修订后签核」）。
- ❌ 1025 有原 available-case 与 13 重评 + 1 格式修复补充两套结果，须明确版本（`tsinghua-1025-vs-may-2026-10-27.md:14`）。
- ❌ `tsinghua-three-datasets-reading-order-2026-10-27.md:4` 自承 Deep Investigation 工具链未完整完成（pair admission 被阻塞），勿称全链路完成。

## 未决

| 项 | 状态 |
|---|---|
| 生产消费交接 A1–A8 / T2 gate | 全 PENDING / 恒 NO-GO（`token-accounting-wiki.md`） |
| 3 样张视觉预检 V | 部分完成，视觉未确认；不启动 630 批量 |
| DNA 正式实验 | no-go（协议不等价） |
| 1025 v3.1 实现 | 仍 v2，未 ready |
| 1023 DNA 最终收口 | W2/Open Questions 未闭合（`tsinghua-dna-final-closeout-2026-10-27.md:28`） |
| 清洁交付终验 | FIRST_DELIVERY，终验 INCOMPLETE |

## 原文入口

[`docs/investigations/`](../../docs/investigations/)（`token-*` / `tsinghua-*` / `reprompt-*`）｜ [`docs/plans/`](../../docs/plans/) ｜ [`docs/reviews/`](../../docs/reviews/) ｜ [`docs/INDEX-DETAILS.md`](../../docs/INDEX-DETAILS.md) C 节 ｜ [`docs/index.json`](../../docs/index.json)

> 本页由 dreaming 生成，写入新目录，原文 0 改动。新增报告后重跑做梦，先核对「权威链」是否被取代，禁止叠加新旧状态。
