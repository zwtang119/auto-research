# Token 统一报告：1023 冻结接入与 replacement

日期：2026-10-27；执行者：OpenCode gpt-6.1-sol。

**结论：1023 离线接入完成，交付限定的已知资源小计；不是全项目最终结算。** 1025 活动树未读取、未更新，仅保留 2026-10-26 旧快照供查阅，不并入下面跨实验已知资源小计。旧包及源实验只读；未发实验 API、未控制实验进程。

Green Source：本报告事实与确定性算术来自 `analysis/token-1023-append-20261027/source-manifest.json:1`、`results.json:1`、`verification.json:1`；以下简写 `B/` 均指 `analysis/token-1023-append-20261027/`。这是分析冻结包，不是 evidence/ 证据快照。

## 1. 两种 1023 口径

四项 token 列均为原生已知小计，括号为 known/记录分母；缺失不填 0，reasoning 不另加到 total。全部 mode 与 semantic_state=unknown；MiniMax 原生 reasoning=0 不代表没有思考。

| 视图 | 物理请求记录 / 记录的 HTTP hook | prompt | native completion | native reasoning | native total | 状态 |
|---|---:|---:|---:|---:|---:|---|
| 正式采用调用（含消费摘要） | 3360 / 3360 | 5,320,782 (3360/3360) | 14,851,291 (3360/3360) | 12,847,207 (3360/3360) | 20,172,073 (3360/3360) | measured |
| 正式实验全部资源 | 3425 / 3425 | 5,360,480 (3413/3425) | 14,888,312 (3413/3425) | 12,870,178 (3413/3425) | 20,248,792 (3413/3425) | partial-native |
| 1023 全部已知资源（加 pilot/diagnostic） | 3561 / 3561 | 5,562,036 (3546/3561) | 15,412,118 (3546/3561) | 13,332,709 (3546/3561) | 20,974,154 (3546/3561) | partial-native |
| 未进入正式采用的资源 | 201 / 201 | 241,254 (186/201) | 560,827 (186/201) | 485,502 (186/201) | 802,081 (186/201) | partial-native |

Green Source：`B/results.json:1`。HTTP hook 是客户端记录，不是 provider 执行/计费收据。采用账与资源账是嵌套视图，不能相加。3,360 = 1,260 生成轮次（SASR 315 + MAMR 945）+ 210 被采用请求消费的摘要 + 1,890 评分；正式全部资源为 3,425（生成 1,312 + 摘要 210 + 评分 1,903）。

全资源比采用账多 201 条：52 条未采用正式生成、13 条正式评分错误、120 条 pilot、16 条 compatibility diagnostic。已知 native total 差 802,081，但另有 15 条 usage 缺失，不能把这项差额称完整浪费量。13 条正式评分错误中一条仍有原生 usage，已保留。相同fingerprint可能是独立重复实验或恢复重发，不将236条重复额外记录一概称retry；未采用生成不被机械归因为错误。Green Source：`B/ledger-1023.csv:1`、`B/missing-usage.json:1`。

### 正式采用：stage / provider / model

| stage | provider | model | 请求记录 | prompt | native completion | native reasoning | native total | 状态 |
|---|---|---|---:|---:|---:|---:|---:|---|
| evaluation | openrouter | moonshotai/kimi-k2.5 | 630 | 1,173,359 (630/630) | 866,494 (630/630) | 851,460 (630/630) | 2,039,853 (630/630) | measured |
| evaluation | paratera | GLM-5.1 | 630 | 1,823,342 (630/630) | 9,215,646 (630/630) | 8,596,413 (630/630) | 11,038,988 (630/630) | measured |
| evaluation | paratera | MiniMax-M2.7 | 630 | 1,164,332 (630/630) | 684,612 (630/630) | 0 (630/630) | 1,848,944 (630/630) | measured |
| generation | openrouter | deepseek/deepseek-v4-flash | 420 | 264,470 (420/420) | 821,419 (420/420) | 768,947 (420/420) | 1,085,889 (420/420) | measured |
| generation | openrouter | openai/gpt-oss-120b | 420 | 322,898 (420/420) | 634,634 (420/420) | 222,631 (420/420) | 957,532 (420/420) | measured |
| generation | paratera | Qwen3.5-122B-A10B | 420 | 245,603 (420/420) | 2,205,559 (420/420) | 2,018,624 (420/420) | 2,451,162 (420/420) | measured |
| orchestrator | openrouter | deepseek/deepseek-v4-flash | 70 | 97,355 (70/70) | 26,956 (70/70) | 19,176 (70/70) | 124,311 (70/70) | measured |
| orchestrator | openrouter | openai/gpt-oss-120b | 70 | 129,659 (70/70) | 101,645 (70/70) | 83,176 (70/70) | 231,304 (70/70) | measured |
| orchestrator | paratera | Qwen3.5-122B-A10B | 70 | 99,764 (70/70) | 294,326 (70/70) | 286,780 (70/70) | 394,090 (70/70) | measured |

采用依据：630 个 raw 的 1,260 个响应正文逐字唯一匹配物理 calls；210 个摘要逐字关联三个被采用企业请求；评分按 manifest/cache/adoption/input SHA-256/evaluation usage 关联，1,890 个评分输入与采用 raw 字节相同、输出正文出现在评分请求中。54 个 judge×condition×生成模型×企业单元各 35 个评分。Green Source：`B/adoption-bindings.json:1`、`B/adopted-cells.json:1`、`B/adoption-hash-checks.json:1`；实现 `B/append1023.py` 的 adopt、独立实现 `B/verify.py`。这是采用身份与计量核验，不是评分正确性或原 parser 全量重跑验收。

## 2. 统一总表（保留历史原值）

Green Source：`B/unified-table.csv:1`、`B/unified-summary.json:1`。每个实验/stage/provider/model 一行；token 数值为 native_known_subtotal，不含估算。M=全部记录有原生值，P=部分原生，U=无原生；各字段单独给 known/分母。U含原始partial/not-applicable等无原生值状态，细分沿用ledger，不作原生测量；`unknown` 不改成零。

调用 basis：A=1023 realpath 物理请求记录，记录的 http_sends 均为 1；H=历史 physical_calls 字段可用时的和，非新发送验证；R=只有记录数、物理调用数 unknown。五月 MAMR 105 行是 joint-run-meter，不能当 105 次 HTTP；1025 旧行是旧 complete 记录而非最终调用分母。历史 provider 只是旧归档配置/标注，不补造逐调用路由。

| 实验 | stage | provider / model | 记录 / 调用 | basis | prompt | native completion | native reasoning | native total | P/C/R/T状态 |
|---|---|---|---:|:---:|---:|---:|---:|---:|:---:|
| 1023 | evaluation | openrouter / moonshotai/kimi-k2.5 | 651 / 651 | A | 1,213,212 (651/651) | 907,531 (651/651) | 899,146 (651/651) | 2,120,743 (651/651) | M/M/M/M |
| 1023 | evaluation | paratera / GLM-5.1 | 663 / 663 | A | 1,890,133 (652/663) | 9,519,655 (652/663) | 8,880,157 (652/663) | 11,409,788 (652/663) | P/P/P/P |
| 1023 | evaluation | paratera / MiniMax-M2.7 | 653 / 653 | A | 1,201,631 (650/653) | 706,847 (650/653) | 0 (650/653) | 1,908,478 (650/653) | P/P/P/P |
| 1023 | generation | openrouter / deepseek/deepseek-v4-flash | 493 / 493 | A | 314,209 (492/493) | 883,070 (492/493) | 818,411 (492/493) | 1,197,279 (492/493) | P/P/P/P |
| 1023 | generation | openrouter / openai/gpt-oss-120b | 445 / 445 | A | 341,213 (445/445) | 670,548 (445/445) | 237,860 (445/445) | 1,011,761 (445/445) | M/M/M/M |
| 1023 | generation | paratera / Qwen3.5-122B-A10B | 433 / 433 | A | 253,188 (433/433) | 2,271,213 (433/433) | 2,078,750 (433/433) | 2,524,401 (433/433) | M/M/M/M |
| 1023 | orchestrator | openrouter / deepseek/deepseek-v4-flash | 73 / 73 | A | 101,424 (73/73) | 28,338 (73/73) | 20,334 (73/73) | 129,762 (73/73) | M/M/M/M |
| 1023 | orchestrator | openrouter / openai/gpt-oss-120b | 77 / 77 | A | 142,673 (77/77) | 113,392 (77/77) | 94,411 (77/77) | 256,065 (77/77) | M/M/M/M |
| 1023 | orchestrator | paratera / Qwen3.5-122B-A10B | 73 / 73 | A | 104,353 (73/73) | 311,524 (73/73) | 303,640 (73/73) | 415,877 (73/73) | M/M/M/M |
| 1025 旧快照* | 1025_journal | openrouter / deepseek/deepseek-v4-flash | 173 / ? | R | 141,279 (163/173) | 406,268 (163/173) | 358,848 (163/173) | 547,547 (163/173) | P/P/P/P |
| 1025 旧快照* | 1025_journal | openrouter / moonshotai/kimi-k2.5 | 229 / ? | R | 428,711 (228/229) | 532,489 (228/229) | 584,554 (228/229) | 961,200 (228/229) | P/P/P/P |
| 1025 旧快照* | 1025_journal | openrouter / openai/gpt-oss-120b | 193 / ? | R | 201,050 (188/193) | 302,212 (188/193) | 113,700 (188/193) | 503,262 (188/193) | P/P/P/P |
| 1025 旧快照* | 1025_journal | paratera / GLM-5.1 | 229 / ? | R | 653,076 (225/229) | 3,182,902 (225/229) | 2,961,369 (225/229) | 3,835,978 (225/229) | P/P/P/P |
| 1025 旧快照* | 1025_journal | paratera / MiniMax-M2.7 | 231 / ? | R | 429,763 (231/231) | 266,406 (231/231) | 0 (231/231) | 696,169 (231/231) | M/M/M/M |
| 1025 旧快照* | 1025_journal | paratera / Qwen3.5-122B-A10B | 212 / ? | R | 151,583 (203/212) | 988,839 (203/212) | 905,053 (203/212) | 1,140,422 (203/212) | P/P/P/P |
| benchmark | benchmark-generation | unknown / deepseek-v4-flash | 18 / ? | R | 1,683 (18/18) | 86,271 (18/18) | — (0/18) | 87,954 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / deepseek-v4-pro | 18 / ? | R | 1,683 (18/18) | 94,036 (18/18) | — (0/18) | 95,719 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / glm-5.1 | 18 / ? | R | 1,730 (18/18) | 74,241 (18/18) | — (0/18) | 75,971 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / kimi-k2.5 | 18 / ? | R | 1,748 (18/18) | 23,468 (18/18) | — (0/18) | 25,216 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / kimi-k2.6 | 18 / ? | R | 1,748 (18/18) | 36,180 (18/18) | — (0/18) | 37,928 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / mimo-v2.5-pro | 18 / ? | R | 6,310 (18/18) | 49,698 (18/18) | — (0/18) | 56,008 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / minimax-m2.7 | 18 / ? | R | 2,051 (18/18) | 32,535 (18/18) | — (0/18) | 34,586 (18/18) | M/M/U/M |
| benchmark | benchmark-generation | unknown / qwen3.6-plus | 18 / ? | R | 1,840 (18/18) | 84,423 (18/18) | — (0/18) | 86,263 (18/18) | M/M/U/M |
| benchmark | benchmark-judge | unknown / deepseek-v4-flash | 493 / ? | R | — (0/493) | — (0/493) | — (0/493) | — (0/493) | U/U/U/U |
| benchmark | benchmark-judge | unknown / deepseek-v4-pro | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | U/U/U/U |
| benchmark | benchmark-judge | unknown / glm-5.1 | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | U/U/U/U |
| benchmark | benchmark-judge | unknown / kimi-k2.5 | 493 / ? | R | — (0/493) | — (0/493) | — (0/493) | — (0/493) | U/U/U/U |
| benchmark | benchmark-judge | unknown / kimi-k2.6 | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | U/U/U/U |
| benchmark | benchmark-judge | unknown / mimo-v2.5-pro | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | U/U/U/U |
| benchmark | benchmark-judge | unknown / minimax-m2.7 | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | U/U/U/U |
| benchmark | benchmark-judge | unknown / qwen3.6-plus | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | U/U/U/U |
| may | generation | openrouter / gpt-oss-120b | 140 / ? | R | 366,370 (140/140) | 390,554 (140/140) | — (0/140) | 756,924 (140/140) | M/M/U/M |
| may | generation | openrouter / nemotron-3-super | 170 / 170 | H | 143,888 (170/170) | 325,285 (170/170) | — (0/170) | 469,173 (170/170) | M/M/U/M |
| may | generation | paratera / deepseek-v4-flash | 140 / ? | R | 355,369 (140/140) | 428,224 (140/140) | — (0/140) | 783,593 (140/140) | M/M/U/M |
| may | generation | paratera / qwen3.5-122b | 140 / ? | R | 261,551 (140/140) | 2,107,270 (140/140) | — (0/140) | 2,368,821 (140/140) | M/M/U/M |
| may | gt0 | paratera / kimi-k2.5 | 25 / ? | R | — (0/25) | — (0/25) | — (0/25) | — (0/25) | U/U/U/U |
| may | gt0 | paratera / minimax-m2.7 | 25 / ? | R | — (0/25) | — (0/25) | — (0/25) | — (0/25) | U/U/U/U |
| may | gt1 | paratera / kimi-k2.5 | 10 / 10 | H | — (0/10) | — (0/10) | — (0/10) | — (0/10) | U/U/U/U |
| may | gt1 | paratera / minimax-m2.7 | 10 / 10 | H | — (0/10) | — (0/10) | — (0/10) | — (0/10) | U/U/U/U |
| may | gt2 | paratera / kimi-k2.5 | 630 / 630 | H | — (0/630) | — (0/630) | — (0/630) | — (0/630) | U/U/U/U |
| may | gt2 | paratera / minimax-m2.7 | 630 / 630 | H | — (0/630) | — (0/630) | — (0/630) | — (0/630) | U/U/U/U |
| may | gt3 | unknown / not-applicable | 1 / 0 | H | — (0/1) | — (0/1) | — (0/1) | — (0/1) | U/U/U/U |
| may | orchestrator | openrouter / gpt-oss-120b | 70 / ? | R | — (0/70) | — (0/70) | — (0/70) | — (0/70) | U/U/U/U |
| may | orchestrator | paratera / deepseek-v4-flash | 70 / ? | R | — (0/70) | — (0/70) | — (0/70) | — (0/70) | U/U/U/U |
| may | orchestrator | paratera / qwen3.5-122b | 70 / ? | R | — (0/70) | — (0/70) | — (0/70) | — (0/70) | U/U/U/U |
| may | track_a | glm-coding / glm-5.1-coding | 460 / 460 | H | 1,206,758 (460/460) | 2,219,974 (460/460) | — (0/460) | 3,426,732 (460/460) | M/M/U/M |
| may | track_a | paratera / glm-5.1 | 170 / 170 | H | 545,289 (170/170) | 793,786 (170/170) | — (0/170) | 1,339,075 (170/170) | M/M/U/M |
| may | track_b | paratera / glm-5.1 | 298 / 298 | H | 730,375 (298/298) | 717,177 (298/298) | — (0/298) | 1,447,552 (298/298) | M/M/U/M |
| may | track_b | paratera / kimi-k2.5 | 630 / 630 | H | 1,098,123 (630/630) | 223,582 (630/630) | — (0/630) | 1,321,705 (630/630) | M/M/U/M |
| may | track_b | paratera / minimax-m2.7 | 630 / 630 | H | 1,094,083 (630/630) | 670,907 (630/630) | — (0/630) | 1,764,990 (630/630) | M/M/U/M |

*1025 全部 1,267 行与 2026-10-26 safe-ledger 逐字段相同，不代表当前状态、不并入下一节小计。

### 历史估算与缺失另列

以下为 Red Source / 冻结 item1-v1 / ORCH-MEAN 历史五月摘要估算（不是五月原生测量），沿用旧 safe-ledger 的十进制值、状态及 estimator，不因本次 1023 实测而升级或删除。机器表 `B/unified-table.csv:1` 保留 estimated 列；原始估算元数据仍在 active-ledger。

| model | 估算记录 | prompt estimate | completion estimate | total estimate |
|---|---:|---:|---:|---:|
| gpt-oss-120b | 70 | 129,658.9999999999950 | 101,645.0000000000090 | 231,303.999999999990 |
| deepseek-v4-flash | 70 | 97,354.9999999999940 | 26,956.0000000000010 | 124,311.0000000000020 |
| qwen3.5-122b | 70 | 99,764.0 | 294,326.000000000010 | 394,090.000000000010 |

## 3. 跨实验已知资源小计（排除 1025）

| 范围 | 账本记录 | prompt | native completion | native reasoning | native total |
|---|---:|---:|---:|---:|---:|
| may + benchmark + 新 1023 | 11326 | 11,382,635 (6468/11326) | 23,769,729 (6468/11326) | 13,332,709 (3546/11326) | 35,152,364 (6468/11326) |

**35,152,364 是异质记录范围内保存原生 total 的已知小计，不是全项目最终总量，也不是统一 HTTP 分母。** 共 6,468/11,326 行保存 native total，4,858 行无原生 total（其中 210 行有历史估算）。其中 1023 有 15 条缺 usage；五月有 joint-run 共享计量、GT 缺失/计划行及估算；benchmark judge 行未保存 usage。reasoning 仅覆盖 3,546/11,326 行。跨组 usage 覆盖与原生数分别求和，不把记录数当发送数，也不把 Red Source 估算混入 Green Source 原生值。Green Source：`B/results.json:1`。

五月原生对照保持：matched SASR 808,076；matched MAMR 3,101,262（105 组共享计量，不三倍加）；全部已知原生评估 9,300,054。新增独立验证是对冻结 safe-ledger 逐字段保留与复算，不声称本轮又读取五月原始档案。benchmark 3,446 行与五月 4,319 行均保持原值。Green Source：`B/verification.json:1`。

## 4. 结束、冻结与范围证据

- 稳定选定输入双遍检查：2026-10-27T00:14:42.058452+00:00 至 2026-10-27T00:14:51.560572+00:00（UTC）；20,512 个 realpath 文件、288,459,442 字节。两遍重新枚举集合/hash/symlink 目标一致；只去别名，不按 fingerprint 去重（重复额外 236 条全部保留）。Green Source：`B/source-manifest.json:1`、`B/results.json:1`。
- monitor/supervision 当时仍写，另存一次观察；稳定冻结不等于全树停写。排除 runtime-deps/cache/动态日志/历史材料镜像；全部冻结成员、别名及排除策略可查 manifest。Green Source：`B/monitor-observations.json:1`、`B/source-manifest.json:1`。
- GLM v12 原 status=COMPLETE_WAIT_PARENT，evaluations=630、该阶段 completed=92，host returncode=0；Kimi SASR/MAMR 各315，退出0。MiniMax物理632、completed630/error2，采用630，其中628份五维scores完整、2份空scores，保留而不按内容重发。身份与原生 usage 独立复算；不把源自评文档的 token 数作为加总输入。Green Source：`B/completion-evidence.json:1`、`B/verification.json:1`；冻结成员 `source.zip::glm-recovery-v12/glm-5.1/status.json:1`、`source.zip::minimax-scoring-v1/FINAL-ACCEPTANCE.json:1`。
- **MAMR 生成 closeout 的 host exit=2、complete_marker_exists=false**，原 status=GENERATION_ACCEPTED_END_ACCOUNT_GATE_PAUSED。本包根据采用 raw/摘要消费确认结果覆盖，不把它改成 exit=0，也不将该 marker 缺失隐藏。Green Source：`B/completion-evidence.json:1`；冻结成员 `source.zip::runs/formal/mamr-recovery18-tech01-v1/final-closeout.json:1`。
- 操作者“1023结束并授权接入”的说明单存 attestation，标记为先前会话摘要转录，不冒充逐字签名；仍无全局无补跑及明确停写凭据。pilot pending 的服务端终态未知，compatibility 02 为 error_uncertain_no_resend。Green Source：`B/operator-attestation.json:1`、`B/missing-usage.json:1`。
- 目录裁定：正式评分与恢复/technical均入资源账；pilot120、diagnostic16保留；request-profile-checks 31条及 offline-host-boundary 1条是 MockTransport夹具，32条不计。非 calls usage 候选按冻结结构审核，逐笔抄录与calls关联后不再加，review_required=0；这不是排除未记录服务端调用的证明。Green Source：`B/directory-scope.json:1`、`B/excluded-records.json:1`、`B/noncalls-audit.json:1`。
- 正式3,425条请求均省略max_tokens/max_completion_tokens；diagnostic中有对照字段，独立保留。不截断usage，不由历史config推断五月实际发送策略；本次不重做跨期因果解释。Green Source：`B/request-profiles.json:1`。
- 版本按冻结脚本/config逐文件SHA-256锁定，执行snapshot文档另列；未假设一个git commit代表全部历史执行。当前脚本hash不是历史所有调用执行代码的充分证明。Green Source：`B/source-versions.json:1`。

## 5. Replacement 守恒与复核

Green Source：`B/supersedes.json:1`、`B/verification.json:1`：

```text
旧 active 12,263 = may 4,319 + benchmark 3,446 + 1025旧快照 1,267 + 1023旧 3,231
新 active 12,593 = 保留 9,032 + 新 1023 3,561
旧 1023 3,231 -> 一对一 supersedes；3,229份hash不变，2份pending->completed
新物理来源 +330 = 正式后续194 + pilot/diagnostic136；状态更新不加发送
跨实验有限小计只取 11,326 行，不含1025旧快照
```

旧1023行单列 superseded-1023.csv，不参与新active求和。两条修订的旧total均空，新值分别26,968、24,124；新旧来源hash均保留。禁止将旧3,231与新3,561做ADD-only。

本会话独立实现 verify.py（不导入主提取器）从ZIP逐项核对原生字段、物理集合、采用集、54评分单元、manifest/hash、非calls抄录、replacement和全部summary；19项测试覆盖别名、同指纹多发送、错误usage、缺失、pending更新、防换ID重复源、冻结两遍新增/改动/删除/越界和reasoning语义。**未启动其他会话、未做Oracle审阅；独立编排者最终核验待执行。** 同会话独立脚本不等于外部审核签字。

复现命令（仅写新分析包/本报告；不得重新capture或运行旧包reproduce）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1023-append-20261027/append1023.py build
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1023-append-20261027/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s analysis/token-1023-append-20261027 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1023-append-20261027/report.py
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1023-append-20261027/release.py verify
```

SHA-256封装验证见 release-manifest.json；它是完整性锁，不是外部真实性签名。冻结选定输入、调用计量及限定报告已可交接；整体停写/无补跑/未保存发送完整性仍未证实，1025不在本轮结算范围。
