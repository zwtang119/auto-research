# Token 统一报告：1025 replacement 完成与1023缺失说明

日期：2026-10-27；执行者：OpenCode gpt-6.1-sol。

**所列范围接入完成；仍是已知原生资源小计，不是无缺口的全项目最终消耗。** `complete` 仅指本次接入工作完成。新1025替代旧1025全部1,267行，五月/benchmark/新1023的11,326行逐字段保留。原实验、旧分析包、旧报告只读；本轮无API、进程启停、commit/push。

Green Source：以下 `B/` = `analysis/token-1025-append-20261027/`；事实/计数/算术来自 `B/source-manifest.json:1`、`B/results.json:1`、`B/verification.json:1`。`source.zip::path:line` 指本分析冻结包成员（不是 evidence/ 证据快照）。历史估算另标 Red Source / item1-v1 / estimator，不混入原生数。

## 1. 接入结果及口径

各token列是native known subtotal；括号known/账本记录分母；缺失永不写0。native reasoning独立展示，**不额外加到total**。mode/semantic_state=unknown；MiniMax原生reasoning=0不能证明无思考。采用账是资源账的嵌套视图，不能相加。

| 视图 | 记录 | prompt | native completion | native total | native reasoning | 状态 |
|---|---|---|---|---|---|---|
| 1025资源全集（含22本地失败） | 1911 | 3,277,206 (1876/1911) | 8,864,237 (1876/1911) | 12,141,443 (1876/1911) | 7,689,934 (1876/1911) | partial-native |
| 主run全部资源 | 1874 | 3,243,222 (1863/1874) | 8,766,631 (1863/1874) | 12,009,853 (1863/1874) | 7,594,516 (1863/1874) | partial-native |
| 补测/恢复全部资源 | 15 | 33,984 (13/15) | 97,606 (13/15) | 131,590 (13/15) | 95,418 (13/15) | partial-native |
| 首run本地初始化失败 | 22 | — (0/22) | — (0/22) | — (0/22) | — (0/22) | unknown/N/A |
| 原主结果采用槽位（含无效/缺失评分） | 1860 | 3,233,045 (1851/1860) | 8,746,567 (1851/1860) | 11,979,612 (1851/1860) | 7,572,670 (1851/1860) | partial-native |
| 原主结果有效采用集 | 1846 | 3,222,344 (1846/1846) | 8,733,538 (1846/1846) | 11,955,882 (1846/1846) | 7,563,053 (1846/1846) | measured |
| 补充侧车有效采用关联集 | 1860 | 3,257,386 (1860/1860) | 8,832,458 (1860/1860) | 12,089,844 (1860/1860) | 7,658,471 (1860/1860) | measured |

Green Source：`B/results.json:1`、`B/adoption-coverage.json:1`、`B/adoption-bindings.json:1`。三个“采用”口径有意分开：

- **原主结果采用槽位1,860** = 720被接受生成 + 60被消费摘要 + 1,080原评分槽位。评分含9个transport_error和5个completed但无效；9个无usage，不能抹掉。known total=11,979,612，覆盖1,851/1,860。
- **原主结果有效采用集1,846** = 720+60+1,066有效评分，usage全覆盖，native total=11,955,882。有效性沿用冻结 `analysis_value` 是否非null；本轮验证身份/输入/正文/usage，不冒充原parser重跑或评分语义正确性验收。
- **侧车有效采用关联集1,860** = 720+60+1,066原有效评分+13补测有效评分+1原请求的本地format-repaired关联，usage全覆盖，native total=12,089,844。格式修复只插入两个单引号；**没有第16次补测**，也不是原协议新测量。不覆盖原主结果，不将事后补测改称预注册完整结果。
- 资源账保留原run的所有1,874条及15补测；首run另22条本地错误。资源全集比原主槽位多51条，比侧车有效关联多51条，但两组“多出”不是同一集合；不能只按数差称为重试/浪费。
- 主run：734生成（其中3条configuration-invalidated）、60摘要、1,080评分；补测：15评分，13成功/2个403。原configuration-invalidated 3条均保留（一条有usage、两条403无usage），新的replacement namespace也保留，不能按fingerprint删除。

### 1.1 1025按stage / provider / model：资源全集

Green Source：`B/stage-provider-model.json:1`。记录不是经独立收据确认的HTTP发送数；本地失败包含在记录分母，详见§3。

| stage | provider | model | 记录 | prompt | native completion | native total | native reasoning | P/C/T/R状态 |
|---|---|---|---|---|---|---|---|---|
| generation | openrouter | deepseek/deepseek-v4-flash | 261 | 206,272 (251/261) | 659,158 (251/261) | 865,430 (251/261) | 560,659 (251/261) | partial-native/partial-native/partial-native/partial-native |
| generation | openrouter | openai/gpt-oss-120b | 245 | 248,690 (240/245) | 393,402 (240/245) | 642,092 (240/245) | 133,017 (240/245) | partial-native/partial-native/partial-native/partial-native |
| generation | paratera | Qwen3.5-122B-A10B | 250 | 166,989 (241/250) | 1,190,975 (241/250) | 1,357,964 (241/250) | 1,085,221 (241/250) | partial-native/partial-native/partial-native/partial-native |
| score | openrouter | moonshotai/kimi-k2.5 | 367 | 733,513 (363/367) | 810,440 (363/367) | 1,543,953 (363/367) | 885,415 (363/367) | partial-native/partial-native/partial-native/partial-native |
| score | paratera | GLM-5.1 | 366 | 1,102,369 (360/366) | 5,260,622 (360/366) | 6,362,991 (360/366) | 4,910,285 (360/366) | partial-native/partial-native/partial-native/partial-native |
| score | paratera | MiniMax-M2.7 | 362 | 726,029 (361/362) | 425,118 (361/362) | 1,151,147 (361/362) | 0 (361/362) | partial-native/partial-native/partial-native/partial-native |
| summary | openrouter | deepseek/deepseek-v4-flash | 20 | 28,938 (20/20) | 6,972 (20/20) | 35,910 (20/20) | 3,941 (20/20) | measured/measured/measured/measured |
| summary | openrouter | openai/gpt-oss-120b | 20 | 37,033 (20/20) | 32,225 (20/20) | 69,258 (20/20) | 28,280 (20/20) | measured/measured/measured/measured |
| summary | paratera | Qwen3.5-122B-A10B | 20 | 27,373 (20/20) | 85,325 (20/20) | 112,698 (20/20) | 83,116 (20/20) | measured/measured/measured/measured |

### 1.2 有效采用小计（stage / provider / model）

Green Source：`B/adopted-stage-provider-model.json:1`；原主槽位分组也在同一机器文件中。

#### 原主结果有效集

| stage | provider | model | 记录 | prompt | native completion | native total | native reasoning | P/C/T/R状态 |
|---|---|---|---|---|---|---|---|---|
| generation | openrouter | deepseek/deepseek-v4-flash | 240 | 196,674 (240/240) | 644,091 (240/240) | 840,765 (240/240) | 543,400 (240/240) | measured/measured/measured/measured |
| generation | openrouter | openai/gpt-oss-120b | 240 | 248,690 (240/240) | 393,402 (240/240) | 642,092 (240/240) | 133,017 (240/240) | measured/measured/measured/measured |
| generation | paratera | Qwen3.5-122B-A10B | 240 | 166,410 (240/240) | 1,185,978 (240/240) | 1,352,388 (240/240) | 1,080,634 (240/240) | measured/measured/measured/measured |
| score | openrouter | moonshotai/kimi-k2.5 | 353 | 713,420 (353/353) | 782,904 (353/353) | 1,496,324 (353/353) | 852,471 (353/353) | measured/measured/measured/measured |
| score | paratera | GLM-5.1 | 355 | 1,086,209 (355/355) | 5,183,405 (355/355) | 6,269,614 (355/355) | 4,838,194 (355/355) | measured/measured/measured/measured |
| score | paratera | MiniMax-M2.7 | 358 | 717,597 (358/358) | 419,236 (358/358) | 1,136,833 (358/358) | 0 (358/358) | measured/measured/measured/measured |
| summary | openrouter | deepseek/deepseek-v4-flash | 20 | 28,938 (20/20) | 6,972 (20/20) | 35,910 (20/20) | 3,941 (20/20) | measured/measured/measured/measured |
| summary | openrouter | openai/gpt-oss-120b | 20 | 37,033 (20/20) | 32,225 (20/20) | 69,258 (20/20) | 28,280 (20/20) | measured/measured/measured/measured |
| summary | paratera | Qwen3.5-122B-A10B | 20 | 27,373 (20/20) | 85,325 (20/20) | 112,698 (20/20) | 83,116 (20/20) | measured/measured/measured/measured |

#### 补充侧车有效关联集

| stage | provider | model | 记录 | prompt | native completion | native total | native reasoning | P/C/T/R状态 |
|---|---|---|---|---|---|---|---|---|
| generation | openrouter | deepseek/deepseek-v4-flash | 240 | 196,674 (240/240) | 644,091 (240/240) | 840,765 (240/240) | 543,400 (240/240) | measured/measured/measured/measured |
| generation | openrouter | openai/gpt-oss-120b | 240 | 248,690 (240/240) | 393,402 (240/240) | 642,092 (240/240) | 133,017 (240/240) | measured/measured/measured/measured |
| generation | paratera | Qwen3.5-122B-A10B | 240 | 166,410 (240/240) | 1,185,978 (240/240) | 1,352,388 (240/240) | 1,080,634 (240/240) | measured/measured/measured/measured |
| score | openrouter | moonshotai/kimi-k2.5 | 360 | 727,557 (360/360) | 801,743 (360/360) | 1,529,300 (360/360) | 875,798 (360/360) | measured/measured/measured/measured |
| score | paratera | GLM-5.1 | 360 | 1,102,369 (360/360) | 5,260,622 (360/360) | 6,362,991 (360/360) | 4,910,285 (360/360) | measured/measured/measured/measured |
| score | paratera | MiniMax-M2.7 | 360 | 722,342 (360/360) | 422,100 (360/360) | 1,144,442 (360/360) | 0 (360/360) | measured/measured/measured/measured |
| summary | openrouter | deepseek/deepseek-v4-flash | 20 | 28,938 (20/20) | 6,972 (20/20) | 35,910 (20/20) | 3,941 (20/20) | measured/measured/measured/measured |
| summary | openrouter | openai/gpt-oss-120b | 20 | 37,033 (20/20) | 32,225 (20/20) | 69,258 (20/20) | 28,280 (20/20) | measured/measured/measured/measured |
| summary | paratera | Qwen3.5-122B-A10B | 20 | 27,373 (20/20) | 85,325 (20/20) | 112,698 (20/20) | 83,116 (20/20) | measured/measured/measured/measured |

## 2. 统一主表：五月 / benchmark / 新1023 / 新1025

Green Source：`B/unified-table.csv:1`、`B/unified-summary.json:1`。每行experiment × stage × provider × model；四项原生字段状态与coverage分别给出。机器表保留估算小计、原始状态分布（含not-applicable）、status/send_state分布。这里只聚合计量元数据；不是研究效果比较。

调用basis：**J**=1025 run+完整call_id+显式attempt，prepared/pending/complete关联；pending只承诺调度，非发送收据，含本地初始化失败；补测另有hook+HTTP响应。**A**=1023存活物理calls文件，http_sends为request hook，不是provider执行收据。**H/R**=历史physical_calls有值则沿用，无值unknown；不是本轮重新验证路由/发送。五月105组MAMR共享usage计量不可当315独立调用或三倍加总；五月GT-3为N/A/physical_calls=0，不代表二月或全项目零消耗。

| 实验 | stage | provider / model | 记录 / 物理调用 | basis | prompt | native completion | native total | native reasoning | P/C/T/R状态 |
|---|---|---|---|---|---|---|---|---|---|
| 1023 | evaluation | openrouter / moonshotai/kimi-k2.5 | 651 / 651 | A | 1,213,212 (651/651) | 907,531 (651/651) | 2,120,743 (651/651) | 899,146 (651/651) | measured/measured/measured/measured |
| 1023 | evaluation | paratera / GLM-5.1 | 663 / 663 | A | 1,890,133 (652/663) | 9,519,655 (652/663) | 11,409,788 (652/663) | 8,880,157 (652/663) | partial-native/partial-native/partial-native/partial-native |
| 1023 | evaluation | paratera / MiniMax-M2.7 | 653 / 653 | A | 1,201,631 (650/653) | 706,847 (650/653) | 1,908,478 (650/653) | 0 (650/653) | partial-native/partial-native/partial-native/partial-native |
| 1023 | generation | openrouter / deepseek/deepseek-v4-flash | 493 / 493 | A | 314,209 (492/493) | 883,070 (492/493) | 1,197,279 (492/493) | 818,411 (492/493) | partial-native/partial-native/partial-native/partial-native |
| 1023 | generation | openrouter / openai/gpt-oss-120b | 445 / 445 | A | 341,213 (445/445) | 670,548 (445/445) | 1,011,761 (445/445) | 237,860 (445/445) | measured/measured/measured/measured |
| 1023 | generation | paratera / Qwen3.5-122B-A10B | 433 / 433 | A | 253,188 (433/433) | 2,271,213 (433/433) | 2,524,401 (433/433) | 2,078,750 (433/433) | measured/measured/measured/measured |
| 1023 | orchestrator | openrouter / deepseek/deepseek-v4-flash | 73 / 73 | A | 101,424 (73/73) | 28,338 (73/73) | 129,762 (73/73) | 20,334 (73/73) | measured/measured/measured/measured |
| 1023 | orchestrator | openrouter / openai/gpt-oss-120b | 77 / 77 | A | 142,673 (77/77) | 113,392 (77/77) | 256,065 (77/77) | 94,411 (77/77) | measured/measured/measured/measured |
| 1023 | orchestrator | paratera / Qwen3.5-122B-A10B | 73 / 73 | A | 104,353 (73/73) | 311,524 (73/73) | 415,877 (73/73) | 303,640 (73/73) | measured/measured/measured/measured |
| 1025 | generation | openrouter / deepseek/deepseek-v4-flash | 261 / ? | J | 206,272 (251/261) | 659,158 (251/261) | 865,430 (251/261) | 560,659 (251/261) | partial-native/partial-native/partial-native/partial-native |
| 1025 | generation | openrouter / openai/gpt-oss-120b | 245 / ? | J | 248,690 (240/245) | 393,402 (240/245) | 642,092 (240/245) | 133,017 (240/245) | partial-native/partial-native/partial-native/partial-native |
| 1025 | generation | paratera / Qwen3.5-122B-A10B | 250 / ? | J | 166,989 (241/250) | 1,190,975 (241/250) | 1,357,964 (241/250) | 1,085,221 (241/250) | partial-native/partial-native/partial-native/partial-native |
| 1025 | score | openrouter / moonshotai/kimi-k2.5 | 367 / ? | J | 733,513 (363/367) | 810,440 (363/367) | 1,543,953 (363/367) | 885,415 (363/367) | partial-native/partial-native/partial-native/partial-native |
| 1025 | score | paratera / GLM-5.1 | 366 / ? | J | 1,102,369 (360/366) | 5,260,622 (360/366) | 6,362,991 (360/366) | 4,910,285 (360/366) | partial-native/partial-native/partial-native/partial-native |
| 1025 | score | paratera / MiniMax-M2.7 | 362 / ? | J | 726,029 (361/362) | 425,118 (361/362) | 1,151,147 (361/362) | 0 (361/362) | partial-native/partial-native/partial-native/partial-native |
| 1025 | summary | openrouter / deepseek/deepseek-v4-flash | 20 / ? | J | 28,938 (20/20) | 6,972 (20/20) | 35,910 (20/20) | 3,941 (20/20) | measured/measured/measured/measured |
| 1025 | summary | openrouter / openai/gpt-oss-120b | 20 / ? | J | 37,033 (20/20) | 32,225 (20/20) | 69,258 (20/20) | 28,280 (20/20) | measured/measured/measured/measured |
| 1025 | summary | paratera / Qwen3.5-122B-A10B | 20 / ? | J | 27,373 (20/20) | 85,325 (20/20) | 112,698 (20/20) | 83,116 (20/20) | measured/measured/measured/measured |
| benchmark | benchmark-generation | unknown / deepseek-v4-flash | 18 / ? | R | 1,683 (18/18) | 86,271 (18/18) | 87,954 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / deepseek-v4-pro | 18 / ? | R | 1,683 (18/18) | 94,036 (18/18) | 95,719 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / glm-5.1 | 18 / ? | R | 1,730 (18/18) | 74,241 (18/18) | 75,971 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / kimi-k2.5 | 18 / ? | R | 1,748 (18/18) | 23,468 (18/18) | 25,216 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / kimi-k2.6 | 18 / ? | R | 1,748 (18/18) | 36,180 (18/18) | 37,928 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / mimo-v2.5-pro | 18 / ? | R | 6,310 (18/18) | 49,698 (18/18) | 56,008 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / minimax-m2.7 | 18 / ? | R | 2,051 (18/18) | 32,535 (18/18) | 34,586 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-generation | unknown / qwen3.6-plus | 18 / ? | R | 1,840 (18/18) | 84,423 (18/18) | 86,263 (18/18) | — (0/18) | measured/measured/measured/unknown/N/A |
| benchmark | benchmark-judge | unknown / deepseek-v4-flash | 493 / ? | R | — (0/493) | — (0/493) | — (0/493) | — (0/493) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / deepseek-v4-pro | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / glm-5.1 | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / kimi-k2.5 | 493 / ? | R | — (0/493) | — (0/493) | — (0/493) | — (0/493) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / kimi-k2.6 | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / mimo-v2.5-pro | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / minimax-m2.7 | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| benchmark | benchmark-judge | unknown / qwen3.6-plus | 386 / ? | R | — (0/386) | — (0/386) | — (0/386) | — (0/386) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | generation | openrouter / gpt-oss-120b | 140 / ? | R | 366,370 (140/140) | 390,554 (140/140) | 756,924 (140/140) | — (0/140) | measured/measured/measured/unknown/N/A |
| may | generation | openrouter / nemotron-3-super | 170 / 170 | H | 143,888 (170/170) | 325,285 (170/170) | 469,173 (170/170) | — (0/170) | measured/measured/measured/unknown/N/A |
| may | generation | paratera / deepseek-v4-flash | 140 / ? | R | 355,369 (140/140) | 428,224 (140/140) | 783,593 (140/140) | — (0/140) | measured/measured/measured/unknown/N/A |
| may | generation | paratera / qwen3.5-122b | 140 / ? | R | 261,551 (140/140) | 2,107,270 (140/140) | 2,368,821 (140/140) | — (0/140) | measured/measured/measured/unknown/N/A |
| may | gt0 | paratera / kimi-k2.5 | 25 / ? | R | — (0/25) | — (0/25) | — (0/25) | — (0/25) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | gt0 | paratera / minimax-m2.7 | 25 / ? | R | — (0/25) | — (0/25) | — (0/25) | — (0/25) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | gt1 | paratera / kimi-k2.5 | 10 / 10 | H | — (0/10) | — (0/10) | — (0/10) | — (0/10) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | gt1 | paratera / minimax-m2.7 | 10 / 10 | H | — (0/10) | — (0/10) | — (0/10) | — (0/10) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | gt2 | paratera / kimi-k2.5 | 630 / 630 | H | — (0/630) | — (0/630) | — (0/630) | — (0/630) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | gt2 | paratera / minimax-m2.7 | 630 / 630 | H | — (0/630) | — (0/630) | — (0/630) | — (0/630) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | gt3 | unknown / not-applicable | 1 / 0 | H | — (0/1) | — (0/1) | — (0/1) | — (0/1) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | orchestrator | openrouter / gpt-oss-120b | 70 / ? | R | — (0/70) | — (0/70) | — (0/70) | — (0/70) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | orchestrator | paratera / deepseek-v4-flash | 70 / ? | R | — (0/70) | — (0/70) | — (0/70) | — (0/70) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | orchestrator | paratera / qwen3.5-122b | 70 / ? | R | — (0/70) | — (0/70) | — (0/70) | — (0/70) | unknown/N/A/unknown/N/A/unknown/N/A/unknown/N/A |
| may | track_a | glm-coding / glm-5.1-coding | 460 / 460 | H | 1,206,758 (460/460) | 2,219,974 (460/460) | 3,426,732 (460/460) | — (0/460) | measured/measured/measured/unknown/N/A |
| may | track_a | paratera / glm-5.1 | 170 / 170 | H | 545,289 (170/170) | 793,786 (170/170) | 1,339,075 (170/170) | — (0/170) | measured/measured/measured/unknown/N/A |
| may | track_b | paratera / glm-5.1 | 298 / 298 | H | 730,375 (298/298) | 717,177 (298/298) | 1,447,552 (298/298) | — (0/298) | measured/measured/measured/unknown/N/A |
| may | track_b | paratera / kimi-k2.5 | 630 / 630 | H | 1,098,123 (630/630) | 223,582 (630/630) | 1,321,705 (630/630) | — (0/630) | measured/measured/measured/unknown/N/A |
| may | track_b | paratera / minimax-m2.7 | 630 / 630 | H | 1,094,083 (630/630) | 670,907 (630/630) | 1,764,990 (630/630) | — (0/630) | measured/measured/measured/unknown/N/A |

### 2.1 跨实验已知小计

| 范围 | 异质账本记录 | prompt | native completion | native total | native reasoning |
|---|---|---|---|---|---|
| may+benchmark+1023+1025 | 13237 | 14,659,841 (8344/13237) | 32,633,966 (8344/13237) | 47,293,807 (8344/13237) | 21,022,643 (5422/13237) |

**47,293,807仅为保存native total的已知小计**；8,344/13,237行有原生total，4,893行无原生total（含历史估算、GT计划/N/A以及22本地错误，不可全部称失败HTTP请求）。没有完整发送分母、没有总量上界；不能直接叫“全项目最终token”。原生reasoning仅覆盖5,422/13,237。五月/benchmark/1023原native total小计35,152,364加新1025已知12,141,443，守恒得到本小计；估算没有混入。

### 2.2 五月历史估算、情景和脚注（保留，不升级）

Red Source / 冻结 `item1-v1 / ORCH-MEAN`：下面十进制估算保留原字段，既不是五月原生usage，也不会随本次接入被删除。原可见completion的差额推断已撤回；mode保持unknown；不能从后来的1023/1025实测补填五月缺失。

| model | 估算记录 | prompt estimate | completion estimate | total estimate |
|---|---|---|---|---|
| gpt-oss-120b | 70 | 129658.9999999999950 | 101645.0000000000090 | 231303.999999999990 |
| deepseek-v4-flash | 70 | 97354.9999999999940 | 26956.0000000000010 | 124311.0000000000020 |
| qwen3.5-122b | 70 | 99764.0 | 294326.000000000010 | 394090.000000000010 |

以下完整保留旧报告情景，仅S0为已记录生成原生子集；S1–S3为Red Source估算/代理，S4仅失效历史诊断，不是本次总体估计、有效区间或最终结果。Green Source转录：`B/inputs/report-history.md:154–164`。


| 情景 | 数字与对象（S） | 最主要可争议假设 |
|---|---|---|
| S0 measured baseline | 生成3,909,338；共同产出3.8378×，episode 11.5135× | 只覆盖已记录生成，未包括缺失阶段 |
| S1 + ORCH-MEAN | 编排749,705；MAMR生成+编排3,850,967；两条件4,659,043；共同产出4.7656×，episode 14.2968× | 跨期同任务均值能否迁移；非实测比较 |
| S2 KIMI-RATIO | GT-2 Kimi可见completion中心1,060,348；敏感性1,037,174–1,084,582 | 共同编码/任务偏差；不能当CI |
| S3 MINIMAX-SCENARIO | **1,058,844 visible-token-equivalent**（Kimi编码代理）与 **3,507,421 completion情景**（字符/0.608）；差2,448,577 | 两者是不同对象、不是上下界；差额也不是恢复出的reasoning |
| **S4 LEGACY-DIAGNOSTIC：仅历史失效诊断** | 历史输入总量25,375,098及端点23,649,443–26,018,830；旧编排742,055；强制GT各半后，生成+编排+GT比1.4655×（1.4436–1.5365）；加实测条件评估后1.5836×（1.5651–1.6398） | GT prompt模板错位、强制各半无证据、GLM不平衡；全部是旧算法演算，非实际消耗或有效区间 |

S1原表保留742,055与749,714作为未采用对照，只用于差额审计。**S4不得进入摘要、主结果或有效区间，不是完整项目估计。** GT-2字符并不对半，GT-1种子也不对半；不能靠分摊共享GT把架构比压近一。


五月细节与范围足注保留：[旧完整报告§4–9](token-report-2026-10-26.md#4-5-月与-10231025-的可比性)；其中旧1023/1025“DEFER”仅由本报告替代，不复活已撤回的reasoning语义。matched SASR=808,076、matched MAMR=3,101,262（105组共享计量）、全部已知原生评估=9,300,054，沿用冻结保留行复算；不是本轮重读五月源档。

### 2.3 二月及历史unknown / N/A与研究范围

Green Source：冻结旧完整章节转录 `B/inputs/report-history.md:179–218`，本轮不重查原仓；二月未新增到资源账数字行。



数量与来源为 **Green Source F2（编排者已复核Item 2）**；不是Item 1 token ledger，均不得字符换算为消耗。

| 批次/活动 | 存活产物/范围（F2） | token裁定 | 证据与含义 |
|---|---|---|---|
| 02-19 | 54输出文件 | 所有token栏unknown | F/mc-2026-02-19/README.md:3仍为待执行；来源未证实，不能推定API调用或本地生成 |
| 02-21 | 2,451 + 51文件 | 指定命名模型的产物生成N/A | F/mc-2026-02-21/EXECUTION-INSIGHTS.md:28,33-35披露平台限制、人工补全、Python填充；本次采用Item 2更细批次裁定，而非旧调查笼统mixed |
| 02-22 | 250 Kimi + 990其他 + 50 + 40；GT占位及h3脚本 | N/A | F/mc-2026-02-22/EXECUTION-INSIGHTS.md:1259-1261,1279,1562,1571为脚本生成；gt_annotation_gpt4o.py:39-44为placeholder，无模型调用 |
| 02-23 | 270；过程副本270逐字节相同，只计一套 | 命名模型实验调用N/A | F/mc-2026-02-23/experiment-plan/OPERATION-LOG.md:11-45执行者Agent；CMD-P1-00*.md为IDE agent手写YAML指令，不是指定模型API实验证据 |
| 02-26 | 244 raw + 3 GT | 命名模型实验调用N/A | IDE agent/本地编制；不是命名模型API输出的已核验样本 |
| 02-26 generate_gt_gpt5mini.py | API代码存在，执行未证 | unknown | F/mc-2026-02-26/scripts/generate_gt_gpt5mini.py:36,48,62；代码不等于执行 |

F2补充裁定：二月树唯一API/provider代码在上述GT脚本；批量生成脚本伪造hash的正确位置是 **F/batch_generate_gpt4o_p2a_agents.py:17**，不是旧调查的27。已提交GT的 `gt_annotation.metadata.{annotator,timestamp,total_runs_analyzed}` 与 `effects:` schema不符合该脚本输出，文件timestamp为2026-02-25T00:00:00，与脚本datetime.now().isoformat()不符，而且不在2026-02-25 zip中，故不能归因于该脚本实际执行。此处因果裁定基于Item 2组合证据，不仅基于时间戳。

F/mc-2026-02-22/scripts/h3_cost_benefit.py:214-215的18,000/2,000是硬编码演示值，不是消耗；F/meta/20-model-manifest.md:63-72只是价格表，没有调用数或计量；F/mc-2026-02-26/prompts/PROMPT-MAMR.md没有landscape/集中摘要结构，不能迁入五月的调用结构。IDE agent编写过程可能使用tokens，但不属于命名模型实验调用；其消耗另为unknown，N/A不能概括为二月整体零消耗。

**面向审稿人的措辞：**
> 早期材料含本地模板/随机合成及来源未能核实的探索性产物；不作为独立 LLM 调用或模型能力比较的实证样本，不纳入 API token 统计。可核验 API 实验另行报告。

必须同时披露：P/paper/10-draft/draft-0316.md:49,71,75,89,349曾用“实验设计”“244轮推演”“270次蒙特卡洛模拟”等正式实验措辞，并据此作能力论断。仅改称pilot不足以消除误导；上述句子进入单独更正项。该稿没有token数，不能作为五月比值来源。


范围继承[旧报告§8](token-report-2026-10-26.md#8-纳入范围)：benchmark generation 144条原生usage、judge/tournament 3,302条无usage均保留；其他论文/封存仓/IDE编制成本不并入。独立GLM并发测试仍排除（旧脚注11发送、9实测157,199、1error+1pending；本轮未重读、不并入）；二月unknown/N/A绝非零。

## 3. 1025的结束、发送证据与35条缺失

Green Source：`B/completion-evidence.json:1`、`B/missing-usage-1025.json:1`、`B/directory-scope.json:1`：

- 用户确认“1025结束，要求接入”单独存于 `B/operator-attestation.json:1`，不是整体退出码或停写证明。
- 主run **5,638个journal事件；1,874 prepared / 1,874 pending / 1,874 complete；0未闭合；snapshot队列空、in_flight空、15 finished blocks**。journal head与 `source.zip::terminal-acceptance-20261026/acceptance.json:1` 一致；该验收的历史process_observation为空只是一时观察，不当作当前/未来保证。本轮未运行源验收器/未读取或控制进程。
- 首run **68事件、22 prepared/pending/complete，全部ModuleNotFoundError**；snapshot仍有50个生成队列项，但不在prepared集合，**不能再计50次调用**。它是已放弃的启动失败，不伪装成成功实验run。`source.zip::scripts/production.py:181`附近的lazy import在构造transport之前；`source.zip::scripts/worker.py:11–12`先factory再create。因此22项标本地初始化失败，无usage，不冒称provider发送。
- 主run记录有1,863个response envelope，8个HTTP错误状态，3个APIConnectionError仅有调度承诺/客户端错误，缺独立provider收据。**没有1,874次经独立wire收据证明的统一发送数。** 主run+补测=1,889个非本地调度/请求记录；不能凭此声称所有1,889均执行/计费。
- 补测四阶段：首执行1、continuation8、GLM来源恢复5、MiniMax来源恢复1，共15。后3阶段journal链及pending/completed hash验证；第一阶段无journal，明确以manifest+pending/response/completed三件套纳入。每条有1个request hook及HTTP状态/headers/脱敏响应，13个200、2个403。644与872各send-1/send-2独立保留；不覆盖失败，不借后续成功填失败usage。两个403是team_model_access_denied，不推断key无效或余额不足。
- **35条无usage** = 22本地ModuleNotFoundError + 主run11（4 RateLimitError、3 APIConnectionError、2 PermissionDeniedError、1 InternalServerError、1 APIStatusError）+ 补测2 PermissionDeniedError/403。对真正非本地范围为1,876/1,889有usage、13/1,889无usage；对全部记录为1,876/1,911有usage、35/1,911无usage。null不填0，也不按max_tokens、字符数或成功后续请求估算。
- 原主槽位9条无usage保留；有效采用原集1,846及侧车关联1,860各字段100%原生coverage。资源量和采用量的分母不同。

### 冻结与版本

双遍窗口 **2026-10-27T01:15:25.085704+00:00 至 2026-10-27T01:15:35.956478+00:00（UTC）**；7,593个物理文件、149,858,972字节；重新枚举选定集合/hash/alias一致，归档第一遍字节。Green Source：`B/source-manifest.json:1`。两遍非原子、不消除ABA竞态，不证明全树永久停写。

monitoring/日志另存单次hash观察 `B/monitor-observations.json:1`，既未声称仍写，也未声称停写；监控动态写入本就不等于模型调用未结束。配置、脚本、manifest、历史policy绑定/完成凭据全部冻结，逐文件hash见 `B/source-versions.json:1`；**不伪造单一历史执行commit**，当前源码hash不能证明每次历史调用执行版本。无整体exit收据，overall_exit_code保持null。

目录范围：真实补测全纳入；本地format repair无新调用；offline-tmp/i3-synthetic、i2-test夹具排除（`source.zip::scripts/test_w6.py:124–139`、`source.zip::scripts/test_w45.py:20–46`）；runtime-deps/materials不作调用。预算金额ledger/价格GET/监控/验收派生副本不是token来源；raw/score/dataset的抄录不重复相加。全部候选及目录裁定见 `B/nonjournal-audit.json:1`、`B/directory-scope.json:1`；复制汇总报告不逐一重做数值验收，不能用“review_required=0”冒充所有历史调用都已保存的证明。实际请求prepared正文及补测hook body均省略max_tokens/max_completion_tokens（`B/request-profiles.json:1`）；这是保存证据，不推断provider是否有内部限制。

## 4. 1023资源账15条缺失usage究竟是什么

Green Source：**直接从旧冻结source.zip取字节**，逐文件hash与旧ledger/manifest一致；本轮不读1023源树。详细原错误全文见 `B/missing-1023-details.json:1` / `.csv:1`，hook源码路径/行号见 `B/missing-1023-hooks.json:1`。

这些是资源账中的失败/未闭合记录，**不是正式采用3,360条的usage缺口**。正式采用的prompt/completion/total/reasoning均3,360/3,360有原生值，native total=20,172,073。资源账3,546/3,561有usage，native total=20,974,154；15条的真实token未知，既不估算，也不以成功重发倒填。

| 错误类别 | model | scope | 条数 |
|---|---|---|---|
| HTTP429 | GLM-5.1 | formal | 3 |
| HTTP500 | GLM-5.1 | formal | 3 |
| connection-error | deepseek/deepseek-v4-flash | diagnostic | 1 |
| pending-no-error-receipt | MiniMax-M2.7 | pilot | 1 |
| timeout | GLM-5.1 | formal | 4 |
| timeout | GLM-5.1 | pilot | 1 |
| timeout | MiniMax-M2.7 | formal | 2 |

按模型：GLM-5.1=11，MiniMax-M2.7=3，DeepSeek=1；按scope：formal12、pilot2、diagnostic1；按原状态：13 error、1 error_uncertain_no_resend、1 pending。原冻结字段与ZIP独立复核相同。

**具体含义：**
- 7条APITimeoutError：6条formal（GLM4、MiniMax2）和1条pilot GLM；formal错误文本“Request timed out.”，pilot只保存错误类型。客户端等待超时，没有usage，不能推断服务端已取消或从未执行。
- 3条GLM RateLimitError/HTTP429：formal，正文“当前模型服务繁忙，请稍后重试”，附fallback连接超时；这是返回错误/拒绝服务证据，不是成功推理或计费证据。
- 3条GLM InternalServerError/HTTP500：formal；其中两条为Connection error/fallback上游连接超时，一条为unexpected end of JSON input并附fallback连接超时；错误里的request id也不替代usage。
- 1条DeepSeek APIConnectionError：diagnostic，原status=error_uncertain_no_resend；只知道客户端连接异常并选择不重发，未保存provider响应。
- 1条MiniMax pilot pending：只保存请求与hook计数，**没有错误类型、完成时间或响应**；服务端终态unknown，不能编造为超时/失败/零tokens。

`http_sends=1`确认的是HTTP客户端**request hook进入**：compatibility脚本的 `event_hooks={'request':[sent]}`、评分engine的sending hook、pilot的 `real._client.event_hooks['request'].append(sent)`均在响应前记数。HTTP429/500有额外错误响应文字；其他项只有客户端异常或pending。**15条均不能仅凭hook声称provider执行，更不能据此推出计费token。**

### 逐条可读表

路径均为 `B/inputs/source-1023.zip::` 成员，JSON单行故`:1`；完整SHA与原错误全文在详细CSV/JSON。以下正文为概述，不替换原错误。

| # | scope / model | 状态 / 错误 | 冻结ZIP成员:line |
|---|---|---|---|
| 1 | diagnostic / deepseek/deepseek-v4-flash | error_uncertain_no_resend；APIConnectionError；无响应，不重发 | `compatibility-omit-max-tokens/results/calls/02.json:1` |
| 2 | formal / GLM-5.1 | error；HTTP500；连接/JSON错误及fallback连接超时 | `glm-recovery-v10/glm-5.1/calls/e920e41f73caf9584ef9ea4f1c7ee6c5fb88ebfc939e218a723b30cd9b1c2564.json:1` |
| 3 | formal / GLM-5.1 | error；HTTP500；连接/JSON错误及fallback连接超时 | `glm-recovery-v11/glm-5.1/calls/3e9dc5b8c0794377057f81d674e825aca80be73f9ccc6e63410d214950bac0f8.json:1` |
| 4 | formal / GLM-5.1 | error；Request timed out.（pilot仅存类型） | `independent-scoring-v1/calls/361f39cd7d9b719a48050142baf62b3145994f63338ac46d9223b620a766408d.json:1` |
| 5 | formal / MiniMax-M2.7 | error；Request timed out.（pilot仅存类型） | `minimax-scoring-v1/calls/479a57ed6093025089bfecc3d710f578b8045519690eb882bcb962dc3a0a490d.json:1` |
| 6 | formal / MiniMax-M2.7 | error；Request timed out.（pilot仅存类型） | `minimax-scoring-v1/calls/d0b2cb50ebb2eac5800bb24f61fe5f2dc3575ec821b54885ea3518df7b08a369.json:1` |
| 7 | pilot / MiniMax-M2.7 | pending；pending；无错误/无完成响应 | `runs/pilot-e2e-20261024-1100/calls/pilot/000064.json:1` |
| 8 | pilot / GLM-5.1 | error；Request timed out.（pilot仅存类型） | `runs/pilot-e2e-20261024-1100/calls/pilot/000087.json:1` |
| 9 | formal / GLM-5.1 | error；HTTP429；模型繁忙，fallback连接超时 | `sasr-glm-recovery-v4/glm-5.1/calls/1d0bb709425b357bed94a122463c783f2d41ce3b27c56ef851e01d21e468c398.json:1` |
| 10 | formal / GLM-5.1 | error；HTTP429；模型繁忙，fallback连接超时 | `sasr-glm-recovery-v4/glm-5.1/calls/4e2a149c760d2a610e597492f07a98a4016bee05d897b2ea56cf73080278b472.json:1` |
| 11 | formal / GLM-5.1 | error；Request timed out.（pilot仅存类型） | `sasr-glm-recovery-v4/glm-5.1/calls/66634429b22a90232df40395d2fd4c26f87fd76d778ef498072d22175967d688.json:1` |
| 12 | formal / GLM-5.1 | error；HTTP429；模型繁忙，fallback连接超时 | `sasr-glm-recovery-v4/glm-5.1/calls/b4e9563d20ea6a4bb46aebeb1242918a0e3855278b5c83d316ea20191554d396.json:1` |
| 13 | formal / GLM-5.1 | error；HTTP500；连接/JSON错误及fallback连接超时 | `sasr-glm-recovery-v4/glm-5.1/calls/e6420529206466b37c6c575b208082561d4fabe4767df94afbc48aad17389b86.json:1` |
| 14 | formal / GLM-5.1 | error；Request timed out.（pilot仅存类型） | `sasr-scoring-v2/glm-5.1/calls/0303aca7983f23cdf266a5d58914f3eb45923706ed6349ec69612cb398e39f9f.json:1` |
| 15 | formal / GLM-5.1 | error；Request timed out.（pilot仅存类型） | `sasr-scoring-v3/glm-5.1/calls/bb00c2bf4f000591869207c7ca7864eb0040b1d787841d629e2062234792a509.json:1` |

## 5. Replacement守恒、复现与限制

Green Source：`B/supersedes.json:1`、`B/superseded-1025.csv:1`、`B/verification.json:1`：

```text
旧active 12,593 = 保留11,326 + 旧1025 1,267
新active 13,237 = 保留11,326 + 新1025 1,911
保留11,326 = 五月4,319 + benchmark3,446 + 新1023 3,561
旧1025 1,267 -> 新主run 1,267条一对一同source hash；不再参与active加总
净增加644 = 主run补齐607 + 首run本地失败22 + 补测15
```

旧1267行逐字段留在superseded-1025.csv；links保留旧新身份/run/attempt/hash。保留11,326行**原有全部字段逐值相同**，只允许schema新增字段。完整attempt-qualified ID和父依赖不截断；同run同发送重复complete只计一次，冲突拒绝；不同run/attempt和相同fingerprint的独立记录不合并。pending/complete状态更新本身不增加一次发送。

离线复现（标准库，不安装、不联网、不导入实验代码、不重capture、不运行旧包脚本）：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1025-append-20261027/append1025.py build
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1025-append-20261027/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s analysis/token-1025-append-20261027 -p 'test_*.py' -v
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1025-append-20261027/report.py
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-1025-append-20261027/release.py verify
```

或运行新包 `run_checks.py` 完成build、独立verify、回归、报告和第二遍确定性比较。仅写新包/本新报告；运行日志check-run会更新，release verify会如实指出其变化，不能静默重封。封装manifest是SHA-256完整性锁，非真实性签名。

独立verify不导入append1025.py，直接从ZIP重建字段/身份/采用集合、hash链、replacement、全部小计与coverage；30项回归覆盖报告生成/统一表覆盖、release增删改/别名，以及同发送重复/冲突、不同run/attempt、request/hash/metadata篡改、父attempt、缺usage、reasoning大于completion及原生0、本地错误、双遍新增/删除/修改/别名/越界/循环。**同会话独立实现不等于外部独立审计签字**；本工作项未再派生子代理，未调用Oracle；由编排者协调并直接复核。直接复核与未验项见 `B/REVIEW.md:1`。

保留限制：本次冻结/接入只覆盖所列存活记录；没有全项目完整usage、统一HTTP发送分母、全部历史执行源码/整体exit/永久停写凭据。原parser有效性未全量重跑；二月与历史范围沿用已冻结报告裁定、不重读原仓。旧1023更细完成证据和边界继续有效，见[上一版报告§4–5](token-report-2026-10-27.md#4-结束冻结与范围证据)。所有估算/未保存usage保持其状态；不要把“接入完成”升级为“所有消耗已知”。
