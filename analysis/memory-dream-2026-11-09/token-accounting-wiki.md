# Token 核算 — 当前有效口径（dreaming pilot wiki）

> 生成：2026-11-09｜方法：Anthropic《The components of agent memory》dreaming
> 覆盖：`docs/investigations/token-*.md` 10 篇（2026-10-26 ~ 10-27）
> 性质：**导航页，不是替代品**。所有数字以原文 Green Source 为准；本页不改任何原文。
> 校验：本页结论逐条回查原文 `path:line`，未做新实验、未复算账本、未调用外部模型。

## 一句话

截至 2026-10-27，**论文主表 = 5,220 条采用集 / native total 32,261,917**；任何更大的数字都是「已知原生小计」，**不是全项目最终消耗**；生产消费交接**未获批准（NO-GO）**。

## 当前有效结论

| 问题 | 答案 | 出处 |
|---|---|---|
| 论文采用集是多少 | 1023 正式采用 3,360 + 1025 侧车有效关联 1,860 = **5,220 条**；prompt 8,578,168 / completion 23,683,749 / total **32,261,917** / reasoning 20,505,678 | `docs/investigations/token-report-paper-accounting-2026-10-27.md`（冻结版本 `paper-accounting-v1`） |
| 资源账已知小计 | **47,293,807**，仅覆盖 8,344 / 13,237 行有原生 total 的记录；无完整发送分母、无总量上界 | `docs/investigations/token-report-complete-2026-10-27.md` |
| 1023 全部已知资源 | 3,561 条 / total **20,974,154**（3,546/3,561 有 usage） | `docs/investigations/token-report-2026-10-27.md` |
| 1025 资源全集 | 1,911 条 / total **12,141,443**（1,876/1,911 有 usage，含 22 条本地初始化失败） | `docs/investigations/token-report-complete-2026-10-27.md` |
| 1023 接入 | 离线接入完成；旧 1,023 的 3,231 行一对一 supersedes，单列 `superseded-1023.csv` 不参与新 active 求和 | `docs/investigations/token-report-2026-10-27.md` |
| 1025 接入 | 新 1,025 替代旧 1,025 全部 1,267 行；`complete` **仅指本次接入工作完成** | `docs/investigations/token-report-complete-2026-10-27.md` |
| 正式消费交接 | **不存在可交付的「批准版」**；候选包 `analysis/token-consumption-handoff-20261027-v1/` 为 `WAITING_APPROVAL`，verifier exit 2、`ready=false` | `docs/investigations/token-consumption-handoff-2026-10-27.md` |

**三个层次不能相加**：采用集（5,220）嵌套于资源账，历史估算是资源行的字段视图而非第四份资源。原文明确「不得把主表与附录相加」。

## 权威链（谁取代谁）

| 文档 | 角色 | 状态 |
|---|---|---|
| `token-report-2026-10-26.md`（item5-v1，49.7KB） | 暂行报告 | **部分被撤回**：§119–129 的 provider mode 判定与五月外推已撤回；自称「不是完整项目总量」 |
| `token-report-corrections-2026-10-26.md` | 更正登记表，34 项 | **只读登记，未执行替换**；权威计划称 21 处、实为 24 处 |
| `token-report-imputation-feasibility-2026-10-26.md` | 缺口可行性调查 | 有效：估算值必须分层分区间，**不得承载排序或头条结论**；2 月试验不可估算 |
| `token-readiness-recheck-2026-10-26.md` | 流程更正 | **明确撤回**旧 `ADD-only` 整批接入流程，改 replacement-view；最终发布仍 NO-GO |
| `token-report-2026-10-27.md` | 1023 接入报告 | 中间口径 35,152,364（6,468/11,326 行），已被下一份的 47,293,807 取代 |
| `token-report-complete-2026-10-27.md` | 1025 replacement | 现行资源账口径 |
| `token-report-paper-accounting-2026-10-27.md` | 论文三层核算 | **现行论文口径**（主表 / 资源账附录 / 历史估算另列） |
| `token-1023-handoff-confirmation-2026-10-27.md` | 编排者复核确认 | 仅覆盖列明的源记录与原生小计，**不扩展为正式采用映射的外部验收** |
| `token-adoption-handoff-confirmation-2026-10-27.md` | 采用集恢复核查 | 确认 32,261,917 是两采用视图合计，不是全资源账 |
| `token-consumption-handoff-2026-10-27.md` | 批准链调查 | 现行未决清单：A1–A8 全 PENDING |

## 撤回与陷阱（traps，别再踩）

- ❌ 把 **47,293,807 / 35,152,364 / 32,261,917 / 20,974,154** 任一称为「全项目最终 token 消耗」或互相相加。分母不同、口径嵌套、未知不填 0。
- ❌ 把 `reasoning` 额外加到 `total`；MiniMax 原生 `reasoning=0` **不代表没有思考**（650 条 reasoning_content 有 1,154,826 字符）。
- ❌ 用旧 4,498 条 1023/1025 快照；已 superseded。旧 3,231 与新 3,561 **禁止 ADD-only 相加**。
- ❌ 用「字节原样保留」描述合并 CSV：原文保留的是**原字段值相同**，active 增加了 schema 列。
- ❌ 把 1,860 侧车关联叠加到原有效采用 1,846 条；本地格式修复**不是新增 API 调用**，事后补测不得改称原协议预注册完整结果。
- ❌ 旧 11.3283× 已撤回；主报 3.8378× / 辅报 11.5135× 仅匹配三模型已记录生成。S4、旧目标、PROVIDER-DIFFERENCE 不进入摘要或主结果。
- ❌ `direction_a` 的 `completion_tokens` 是**字符计数衍生字段**，不得重命名后补成原生 token。
- ❌ 把 22 条本地初始化失败冒称 provider 已发送请求；`pending` 只承诺调度，不是发送收据。

## 未决（不得当作已完成）

| 项 | 状态 | 出处 |
|---|---|---|
| 生产消费交接 A1–A8 | 全 PENDING：verifier 入口、代码闭包、schema 绑定、批准人身份、scope/adoption、退出码策略、停写范围、1023 superseding | `token-consumption-handoff-2026-10-27.md` |
| T2 readiness gate | 恒 NO-GO（`readiness.py` gate() 无条件返回） | 同上 |
| 1023 统计脚本 hash 冲突（B1） | 未消解：`verify.py` 实际 `bfc058dc…`/5462B 与 `STATISTICS_COMPLETE.json` 登记不一致 | 同上 |
| 估算值可用性 | 2 月试验零 token 字段、很可能不是 API 调用；5 月 GT 约 1,330 次调用永久无记录；估算不得承载头条结论 | `token-report-imputation-feasibility-2026-10-26.md` |
| 全局限制 | 未补全全项目 usage、统一 HTTP/计费分母、全部历史源码版本、整体 exit / 全树永久停写证明 | `token-report-paper-accounting-2026-10-27.md` |

## 原文入口（细节下沉，本页不复写）

- 索引：[`docs/INDEX.md`](../../docs/INDEX.md) §C、[`docs/index.json`](../../docs/index.json)
- 10 篇原文目录：[`docs/investigations/`](../../docs/investigations/)（`token-*.md`）
- 配套计划：[`docs/plans/`](../../docs/plans/)（`token-*.md` / `tsinghua-clean-release-2026-10-27.md`）
- 冻结分析包：`analysis/token-1023-append-20261027/`、`analysis/token-1025-append-20261027/`、`analysis/token-paper-accounting-20261027/`、`analysis/token-final-readiness-20261026/`

## 维护约定

- 本页由 dreaming 生成，**只在新目录写**；原文、证据快照、状态口径正文 0 改动。
- 新增 token 报告后重跑一次 dreaming：先校验本页「权威链」是否被取代，再更新数字，禁止叠加新旧口径。
- 任何数字变动必须附 Green Source `path:line`；无来源的断言标 `unconfirmed`，不进「当前有效结论」。
