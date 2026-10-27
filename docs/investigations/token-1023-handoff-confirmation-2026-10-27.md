# 1023 接入交接：编排者独立复核确认

日期：2026-10-27；记录者：OpenCode gpt-6.1-sol。

## 确认来源与范围

Green Source / 操作者转达的独立核验结果：本会话最新用户消息报告，编排者已用独立 `zipfile` 读取 ledger 所指的 3,561 个源记录，并核对 active 与旧非1023行。以下记录该确认，不冒充本会话执行了外部核验，也不伪造编排者签名、执行日志或额外完成凭据。

| 核验项 | 编排者确认 |
|---|---:|
| 1023 源记录 | 3,561 |
| 有 usage 的源记录 | 3,546 |
| 原生 prompt | 5,562,036 |
| 原生 completion | 15,412,118 |
| 原生 reasoning | 13,332,709 |
| 原生 total | 20,974,154 |
| active / may | 4,319 |
| active / benchmark | 3,446 |
| active / 1025 旧快照 | 1,267 |
| active / 新1023 | 3,561 |
| 保留的旧非1023行 | 9,032 |
| 9,032 行所有原字段差异 | 0 |

**保留结论是原字段值相同，不是原CSV字节相同。** active增加了schema列，CSV整体字节不同；不得用“字节原样保留”描述合并CSV。

上述计数及原生小计与本包既有独立实现验证结果一致（`analysis/token-1023-append-20261027/verification.json:1`、`results.json:1`）。本次不重复调查或启动其他会话。该确认仅覆盖用户明确列出的源记录/usage/active计数/历史原字段，不扩展为正式采用映射的外部验收、provider执行证明或完整项目最终结算。

## 封装状态

- 已封装包：`analysis/token-1023-append-20261027/`。
- 统一报告：`docs/investigations/token-report-2026-10-27.md:1`。
- `release.py verify` 返回 PASS：38个文件的集合、尺寸及SHA-256一致。
- 封装清单SHA-256：`0ebac27b679a8dfc902c3357d58007e98a640bdd5cfb1d1cb359a0ea39a2fae9`（`analysis/token-1023-append-20261027/release-manifest.json`）。
- 本文件为封装完成后的独立交接补充，**不在上述38文件封装内**；未修改或重封既有包。包内此前“独立编排者核验待执行”的历史文字，由本补充在上述明确范围内更新，不视为全部缺口关闭。

仍为 `LIMITED_KNOWN_RESOURCE_SUBTOTAL`：15条缺usage，整体停写/无补跑凭据未补齐；1025仍仅为2026-10-26旧快照，不并入跨实验已知小计。reasoning不叠加到total，mode保持unknown。本任务未commit/push，未触碰非本次工作区修改。
