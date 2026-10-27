# Token 论文核算：采用集主表、资源账附录、历史估算另列

日期：2026-10-27；冻结核算版本：paper-accounting-v1；执行者：OpenCode gpt-6.1-sol。

**论文主表仅为1023正式采用与1025侧车有效关联共5,220条，native total=32,261,917；不是全资源或全项目最终消耗。** 五月只另列冻结历史匹配范围，不伪称所有历史均获论文采用。三个层次不能相加：采用集嵌套于资源账，历史估算不是新增原生usage。

Green Source：下文 `B/` = `analysis/token-paper-accounting-20261027/`。数字由冻结 `B/inputs/active-ledger.csv:1` 直接复算，`B/input-lock.json:1` 列来源/hash；输入是既有分析冻结，不是 evidence/ 证据快照。不读实验活动源、不重采集、不运行旧包脚本、不发API、不改旧包或高引用区。采用凭据沿用已验证冻结绑定，并非本轮重新执行parser或原协议有效性试验。

## 1. 主表：论文采用集（Green Source）

筛1023 `adoption=adopted`；1025 `sidecar_adoption` 为 `sidecar-adopted` 或 `sidecar-format-repaired-original-call`。Green Source：`B/paper-ledger.csv:1`、`B/paper-table.csv:1`、`B/mapping.csv:1`、`B/summary.json:1`。

| experiment | 记录 | prompt (known/n) | completion (known/n) | total (known/n) | reasoning (known/n) |
|---|---|---|---|---|---|
| 1023 | 3360 | 5,320,782 (3360/3360) | 14,851,291 (3360/3360) | 20,172,073 (3360/3360) | 12,847,207 (3360/3360) |
| 1025 | 1860 | 3,257,386 (1860/1860) | 8,832,458 (1860/1860) | 12,089,844 (1860/1860) | 7,658,471 (1860/1860) |
| 两实验合计 | 5220 | 8,578,168 (5220/5220) | 23,683,749 (5220/5220) | 32,261,917 (5220/5220) | 20,505,678 (5220/5220) |

所选每行四字段均为measured且非空。reasoning独立展示、不额外加到total；原生0不证明无思考，reasoning大于completion照录，不凭差额推断可见输出或跨provider语义。记录不是统一的HTTP发送数。原22个跨run重复call_id保留于资源账；新account_id包括experiment/run/call_id/attempt/archive/hash，不能按call_id或fingerprint合并。

### 1.1 按 experiment / stage / provider / model / condition

| experiment | stage | provider | model | condition | 记录 | prompt (known/n) | completion (known/n) | total (known/n) | reasoning (known/n) |
|---|---|---|---|---|---|---|---|---|---|
| 1023 | evaluation | openrouter | moonshotai/kimi-k2.5 | MAMR | 315 | 783,403 (315/315) | 356,572 (315/315) | 1,139,975 (315/315) | 314,467 (315/315) |
| 1023 | evaluation | openrouter | moonshotai/kimi-k2.5 | SASR | 315 | 389,956 (315/315) | 509,922 (315/315) | 899,878 (315/315) | 536,993 (315/315) |
| 1023 | evaluation | paratera | GLM-5.1 | MAMR | 315 | 1,120,627 (315/315) | 4,997,896 (315/315) | 6,118,523 (315/315) | 4,693,554 (315/315) |
| 1023 | evaluation | paratera | GLM-5.1 | SASR | 315 | 702,715 (315/315) | 4,217,750 (315/315) | 4,920,465 (315/315) | 3,902,859 (315/315) |
| 1023 | evaluation | paratera | MiniMax-M2.7 | MAMR | 315 | 775,001 (315/315) | 365,123 (315/315) | 1,140,124 (315/315) | 0 (315/315) |
| 1023 | evaluation | paratera | MiniMax-M2.7 | SASR | 315 | 389,331 (315/315) | 319,489 (315/315) | 708,820 (315/315) | 0 (315/315) |
| 1023 | generation | openrouter | deepseek/deepseek-v4-flash | MAMR | 315 | 211,183 (315/315) | 693,312 (315/315) | 904,495 (315/315) | 665,231 (315/315) |
| 1023 | generation | openrouter | deepseek/deepseek-v4-flash | SASR | 105 | 53,287 (105/105) | 128,107 (105/105) | 181,394 (105/105) | 103,716 (105/105) |
| 1023 | generation | openrouter | openai/gpt-oss-120b | MAMR | 315 | 254,195 (315/315) | 501,789 (315/315) | 755,984 (315/315) | 180,271 (315/315) |
| 1023 | generation | openrouter | openai/gpt-oss-120b | SASR | 105 | 68,703 (105/105) | 132,845 (105/105) | 201,548 (105/105) | 42,360 (105/105) |
| 1023 | generation | paratera | Qwen3.5-122B-A10B | MAMR | 315 | 192,217 (315/315) | 1,762,249 (315/315) | 1,954,466 (315/315) | 1,615,194 (315/315) |
| 1023 | generation | paratera | Qwen3.5-122B-A10B | SASR | 105 | 53,386 (105/105) | 443,310 (105/105) | 496,696 (105/105) | 403,430 (105/105) |
| 1023 | orchestrator | openrouter | deepseek/deepseek-v4-flash | MAMR | 70 | 97,355 (70/70) | 26,956 (70/70) | 124,311 (70/70) | 19,176 (70/70) |
| 1023 | orchestrator | openrouter | openai/gpt-oss-120b | MAMR | 70 | 129,659 (70/70) | 101,645 (70/70) | 231,304 (70/70) | 83,176 (70/70) |
| 1023 | orchestrator | paratera | Qwen3.5-122B-A10B | MAMR | 70 | 99,764 (70/70) | 294,326 (70/70) | 394,090 (70/70) | 286,780 (70/70) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | MAMR_DNA | 45 | 32,906 (45/45) | 131,191 (45/45) | 164,097 (45/45) | 111,800 (45/45) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | MAMR_NoDNA | 45 | 30,366 (45/45) | 141,459 (45/45) | 171,825 (45/45) | 124,436 (45/45) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | MASR_DNA | 15 | 8,713 (15/15) | 29,587 (15/15) | 38,300 (15/15) | 26,807 (15/15) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | MASR_NoDNA | 15 | 8,222 (15/15) | 24,072 (15/15) | 32,294 (15/15) | 22,516 (15/15) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | SAMR_DNA | 45 | 49,118 (45/45) | 122,987 (45/45) | 172,105 (45/45) | 100,520 (45/45) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | SAMR_NoDNA | 45 | 50,493 (45/45) | 139,786 (45/45) | 190,279 (45/45) | 109,836 (45/45) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | SASR_DNA | 15 | 8,713 (15/15) | 26,372 (15/15) | 35,085 (15/15) | 22,663 (15/15) |
| 1025 | generation | openrouter | deepseek/deepseek-v4-flash | SASR_NoDNA | 15 | 8,143 (15/15) | 28,637 (15/15) | 36,780 (15/15) | 24,822 (15/15) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | MAMR_DNA | 45 | 38,531 (45/45) | 71,652 (45/45) | 110,183 (45/45) | 28,756 (45/45) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | MAMR_NoDNA | 45 | 36,236 (45/45) | 75,534 (45/45) | 111,770 (45/45) | 30,438 (45/45) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | MASR_DNA | 15 | 10,432 (15/15) | 20,210 (15/15) | 30,642 (15/15) | 6,414 (15/15) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | MASR_NoDNA | 15 | 9,793 (15/15) | 19,153 (15/15) | 28,946 (15/15) | 7,209 (15/15) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | SAMR_DNA | 45 | 66,173 (45/45) | 86,837 (45/45) | 153,010 (45/45) | 27,109 (45/45) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | SAMR_NoDNA | 45 | 67,276 (45/45) | 82,626 (45/45) | 149,902 (45/45) | 22,376 (45/45) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | SASR_DNA | 15 | 10,443 (15/15) | 19,253 (15/15) | 29,696 (15/15) | 6,490 (15/15) |
| 1025 | generation | openrouter | openai/gpt-oss-120b | SASR_NoDNA | 15 | 9,806 (15/15) | 18,137 (15/15) | 27,943 (15/15) | 4,225 (15/15) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | MAMR_DNA | 45 | 29,380 (45/45) | 245,336 (45/45) | 274,716 (45/45) | 226,150 (45/45) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | MAMR_NoDNA | 45 | 27,358 (45/45) | 252,039 (45/45) | 279,397 (45/45) | 231,795 (45/45) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | MASR_DNA | 15 | 8,202 (15/15) | 58,169 (15/15) | 66,371 (15/15) | 52,726 (15/15) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | MASR_NoDNA | 15 | 7,627 (15/15) | 60,927 (15/15) | 68,554 (15/15) | 54,890 (15/15) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | SAMR_DNA | 45 | 39,093 (45/45) | 225,919 (45/45) | 265,012 (45/45) | 205,735 (45/45) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | SAMR_NoDNA | 45 | 38,921 (45/45) | 223,258 (45/45) | 262,179 (45/45) | 200,239 (45/45) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | SASR_DNA | 15 | 8,202 (15/15) | 60,534 (15/15) | 68,736 (15/15) | 55,116 (15/15) |
| 1025 | generation | paratera | Qwen3.5-122B-A10B | SASR_NoDNA | 15 | 7,627 (15/15) | 59,796 (15/15) | 67,423 (15/15) | 53,983 (15/15) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | MAMR_DNA | 45 | 111,223 (45/45) | 113,965 (45/45) | 225,188 (45/45) | 125,387 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | MAMR_NoDNA | 45 | 117,606 (45/45) | 105,085 (45/45) | 222,691 (45/45) | 120,219 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | MASR_DNA | 45 | 55,224 (45/45) | 97,413 (45/45) | 152,637 (45/45) | 104,733 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | MASR_NoDNA | 45 | 55,188 (45/45) | 95,246 (45/45) | 150,434 (45/45) | 101,496 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | SAMR_DNA | 45 | 133,966 (45/45) | 102,392 (45/45) | 236,358 (45/45) | 113,783 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | SAMR_NoDNA | 45 | 143,501 (45/45) | 111,794 (45/45) | 255,295 (45/45) | 120,807 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | SASR_DNA | 45 | 54,358 (45/45) | 92,333 (45/45) | 146,691 (45/45) | 100,344 (45/45) |
| 1025 | score | openrouter | moonshotai/kimi-k2.5 | SASR_NoDNA | 45 | 56,491 (45/45) | 83,515 (45/45) | 140,006 (45/45) | 89,029 (45/45) |
| 1025 | score | paratera | GLM-5.1 | MAMR_DNA | 45 | 159,634 (45/45) | 683,785 (45/45) | 843,419 (45/45) | 641,652 (45/45) |
| 1025 | score | paratera | GLM-5.1 | MAMR_NoDNA | 45 | 166,118 (45/45) | 724,956 (45/45) | 891,074 (45/45) | 682,902 (45/45) |
| 1025 | score | paratera | GLM-5.1 | MASR_DNA | 45 | 100,013 (45/45) | 594,195 (45/45) | 694,208 (45/45) | 549,026 (45/45) |
| 1025 | score | paratera | GLM-5.1 | MASR_NoDNA | 45 | 99,868 (45/45) | 593,172 (45/45) | 693,040 (45/45) | 548,678 (45/45) |
| 1025 | score | paratera | GLM-5.1 | SAMR_DNA | 45 | 183,181 (45/45) | 704,344 (45/45) | 887,525 (45/45) | 661,425 (45/45) |
| 1025 | score | paratera | GLM-5.1 | SAMR_NoDNA | 45 | 193,396 (45/45) | 785,348 (45/45) | 978,744 (45/45) | 741,154 (45/45) |
| 1025 | score | paratera | GLM-5.1 | SASR_DNA | 45 | 99,021 (45/45) | 606,823 (45/45) | 705,844 (45/45) | 563,241 (45/45) |
| 1025 | score | paratera | GLM-5.1 | SASR_NoDNA | 45 | 101,138 (45/45) | 567,999 (45/45) | 669,137 (45/45) | 522,207 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | MAMR_DNA | 45 | 110,397 (45/45) | 52,474 (45/45) | 162,871 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | MAMR_NoDNA | 45 | 116,302 (45/45) | 53,776 (45/45) | 170,078 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | MASR_DNA | 45 | 55,216 (45/45) | 47,611 (45/45) | 102,827 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | MASR_NoDNA | 45 | 55,169 (45/45) | 44,921 (45/45) | 100,090 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | SAMR_DNA | 45 | 132,490 (45/45) | 68,992 (45/45) | 201,482 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | SAMR_NoDNA | 45 | 142,089 (45/45) | 62,015 (45/45) | 204,104 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | SASR_DNA | 45 | 54,317 (45/45) | 45,730 (45/45) | 100,047 (45/45) | 0 (45/45) |
| 1025 | score | paratera | MiniMax-M2.7 | SASR_NoDNA | 45 | 56,362 (45/45) | 46,581 (45/45) | 102,943 (45/45) | 0 (45/45) |
| 1025 | summary | openrouter | deepseek/deepseek-v4-flash | MAMR_DNA | 10 | 14,180 (10/10) | 2,980 (10/10) | 17,160 (10/10) | 1,259 (10/10) |
| 1025 | summary | openrouter | deepseek/deepseek-v4-flash | MAMR_NoDNA | 10 | 14,758 (10/10) | 3,992 (10/10) | 18,750 (10/10) | 2,682 (10/10) |
| 1025 | summary | openrouter | openai/gpt-oss-120b | MAMR_DNA | 10 | 18,438 (10/10) | 19,542 (10/10) | 37,980 (10/10) | 18,025 (10/10) |
| 1025 | summary | openrouter | openai/gpt-oss-120b | MAMR_NoDNA | 10 | 18,595 (10/10) | 12,683 (10/10) | 31,278 (10/10) | 10,255 (10/10) |
| 1025 | summary | paratera | Qwen3.5-122B-A10B | MAMR_DNA | 10 | 13,471 (10/10) | 44,503 (10/10) | 57,974 (10/10) | 43,351 (10/10) |
| 1025 | summary | paratera | Qwen3.5-122B-A10B | MAMR_NoDNA | 10 | 13,902 (10/10) | 40,822 (10/10) | 54,724 (10/10) | 39,765 (10/10) |

1023采用包含生成轮次、实际消费摘要与持久化评分，而非全部formal请求。1025侧车1,860 = 原有效采用1,846 + 13补测有效评分 + 1原调用的本地格式修复关联；**不叠加原有效集，不覆盖原主结果**。本地format repair不增加API发送，不将事后补测/修复改称原协议预注册完整结果。失败、被替代/未采用生成仍在资源附录；没有从主表剔除后就抹去资源。

## 2. 五月：冻结历史匹配范围，不是全部历史论文采用（Green Source）

固定历史批次为 `mc-2026-05-05`；限定 `experiment=may`、`scope=balanced`、stage属于generation/track_a/track_b；逐条身份冻结于 `B/historical-scope.json:1`，与主采用集另表存储 `B/historical-matched-ledger.csv:1`，不混入5,220分母。生成限定deepseek-v4-flash、gpt-oss-120b、qwen3.5-122b三个模型；Track A为已保存GLM/GLM-coding评估，Track B为Kimi/MiniMax评估。该范围沿用旧账平衡比较标记，**没有新增历史逐条论文采用裁定，也不是全部历史资源/失败重试完整清单**。scope之外170条nemotron生成、298条额外GLM评估、GT和编排等保留资源层。

| stage | condition | 记录 | prompt (known/n) | completion (known/n) | total (known/n) | reasoning (known/n) |
|---|---|---|---|---|---|---|
| generation | MAMR | 105 | 796,746 (105/105) | 2,304,516 (105/105) | 3,101,262 (105/105) | — (0/105) |
| generation | SASR | 315 | 186,544 (315/315) | 621,532 (315/315) | 808,076 (315/315) | — (0/315) |
| track_a | MAMR | 315 | 1,064,095 (315/315) | 1,566,496 (315/315) | 2,630,591 (315/315) | — (0/315) |
| track_a | SASR | 315 | 687,952 (315/315) | 1,447,264 (315/315) | 2,135,216 (315/315) | — (0/315) |
| track_b | MAMR | 630 | 1,445,980 (630/630) | 474,322 (630/630) | 1,920,302 (630/630) | — (0/630) |
| track_b | SASR | 630 | 746,226 (630/630) | 420,167 (630/630) | 1,166,393 (630/630) | — (0/630) |

历史匹配计量共2,310条，native total=11,761,840。其中生成SASR315个单企业meters、MAMR105个joint-run meters（315企业产物），MAMR三个企业共享usage只计一次；不能把三个副本当独立发送。历史reasoning保持unknown，不用1023/1025新值回填。GT/摘要缺失不变；native范围本身并不完整覆盖论文流水线成本。

### 2.1 历史匹配按stage / provider / model / condition

| experiment | stage | provider | model | condition | 记录 | prompt (known/n) | completion (known/n) | total (known/n) | reasoning (known/n) |
|---|---|---|---|---|---|---|---|---|---|
| may | generation | openrouter | gpt-oss-120b | MAMR | 35 | 293,187 (35/35) | 305,124 (35/35) | 598,311 (35/35) | — (0/35) |
| may | generation | openrouter | gpt-oss-120b | SASR | 105 | 73,183 (105/105) | 85,430 (105/105) | 158,613 (105/105) | — (0/105) |
| may | generation | paratera | deepseek-v4-flash | MAMR | 35 | 299,368 (35/35) | 344,179 (35/35) | 643,547 (35/35) | — (0/35) |
| may | generation | paratera | deepseek-v4-flash | SASR | 105 | 56,001 (105/105) | 84,045 (105/105) | 140,046 (105/105) | — (0/105) |
| may | generation | paratera | qwen3.5-122b | MAMR | 35 | 204,191 (35/35) | 1,655,213 (35/35) | 1,859,404 (35/35) | — (0/35) |
| may | generation | paratera | qwen3.5-122b | SASR | 105 | 57,360 (105/105) | 452,057 (105/105) | 509,417 (105/105) | — (0/105) |
| may | track_a | glm-coding | glm-5.1-coding | MAMR | 145 | 518,806 (145/145) | 772,710 (145/145) | 1,291,516 (145/145) | — (0/145) |
| may | track_a | glm-coding | glm-5.1-coding | SASR | 315 | 687,952 (315/315) | 1,447,264 (315/315) | 2,135,216 (315/315) | — (0/315) |
| may | track_a | paratera | glm-5.1 | MAMR | 170 | 545,289 (170/170) | 793,786 (170/170) | 1,339,075 (170/170) | — (0/170) |
| may | track_b | paratera | kimi-k2.5 | MAMR | 315 | 725,444 (315/315) | 117,593 (315/315) | 843,037 (315/315) | — (0/315) |
| may | track_b | paratera | kimi-k2.5 | SASR | 315 | 372,679 (315/315) | 105,989 (315/315) | 478,668 (315/315) | — (0/315) |
| may | track_b | paratera | minimax-m2.7 | MAMR | 315 | 720,536 (315/315) | 356,729 (315/315) | 1,077,265 (315/315) | — (0/315) |
| may | track_b | paratera | minimax-m2.7 | SASR | 315 | 373,547 (315/315) | 314,178 (315/315) | 687,725 (315/315) | — (0/315) |

只作计量披露，不直接比较不同实验总量或宣称架构因果效应。跨期比较需统一模型/任务/阶段与输出单位；一次三企业MAMR joint episode与一次单企业SASR episode不等价。五月balanced评估排除additional-glm，不把额外GLM既包含又另加。

## 3. 资源账附录（Green Source，完整保留已有账本）

`B/resource-ledger.csv:1` 与冻结输入CSV**逐字节相同**，13,237行所有原字段/顺序不变；新映射放在独立CSV，不重写原resource字段。`B/resource-table.csv:1`按experiment/stage/provider/model/condition覆盖全部行；此处native known只取state=measured的非空值，不将历史估算混入。

| experiment | 记录 | prompt (known/n) | completion (known/n) | total (known/n) | reasoning (known/n) |
|---|---|---|---|---|---|
| 1023 | 3561 | 5,562,036 (3546/3561) | 15,412,118 (3546/3561) | 20,974,154 (3546/3561) | 13,332,709 (3546/3561) |
| 1025 | 1911 | 3,277,206 (1876/1911) | 8,864,237 (1876/1911) | 12,141,443 (1876/1911) | 7,689,934 (1876/1911) |
| benchmark | 3446 | 18,793 (144/3446) | 480,852 (144/3446) | 499,645 (144/3446) | — (0/3446) |
| may | 4319 | 5,801,806 (2778/4319) | 7,876,759 (2778/4319) | 13,678,565 (2778/4319) | — (0/4319) |
| 所列资源合计 | 13237 | 14,659,841 (8344/13237) | 32,633,966 (8344/13237) | 47,293,807 (8344/13237) | 21,022,643 (5422/13237) |

47,293,807是原生total已知小计，覆盖8,344/13,237；未知不填0，无完整上界、不是全项目最终量。与主表分母不同，不称差额为重试/浪费或失败计费。1023资源缺15条usage且均不在正式采用；1025缺35条=22本地初始化失败+13网络/HTTP无usage，22本地失败不冒称provider发送。pending/hook不等于provider执行/计费收据，错误不能用后续成功usage倒填。

benchmark含生成144条原生usage、judge3302条unknown，仅资源附录，不新增论文采用断言。二月unknown/N/A不因本次主表切换变成0；二月IDE编制消耗unknown、不是命名模型API实验。原有二月逐批裁定、五月缺口、排除GLM独立并发测试与全项目范围限制沿用 `B/inputs/upstream-report.md:1`、`B/inputs/history-report.md:1`，本轮不重新调查原仓。

## 4. 历史估算/情景另列（Red Source / item1-v1）

`B/estimate-ledger.csv:1`保留已有非原生value/state/estimator/lower/upper/interval_type，逐字段关联原resource行；`B/estimate-summary.json:1`使用Decimal相加，保留输入既有十进制尾数，不伪造更高测量精度。仅ORCH-MEAN的五月编排P/C/T与KIMI-RATIO的GT可见输出代理进入此层；**没有为失败请求、reasoning或未知prompt新估算，不创建新provider差额语义**。估算共1,270个字段项，来自850个原资源记录（不能把字段项当API调用）。

| stage | model | condition | field | estimator | 记录 | 原值小计 | lower / upper |
|---|---|---|---|---|---|---|---|
| gt1 | kimi-k2.5 | MAMR | visible_completion | KIMI-RATIO | 6 | 10270.6057596822252 | 10046.1389023797954 / 10505.3326561706445 |
| gt1 | kimi-k2.5 | SASR | visible_completion | KIMI-RATIO | 4 | 6862.9592850049661 | 6712.9674599320052 / 7019.8070086338239 |
| gt2 | kimi-k2.5 | MAMR | visible_completion | KIMI-RATIO | 315 | 546492.0556107249801 | 534548.3244293345840 / 558981.7166074149075 |
| gt2 | kimi-k2.5 | SASR | visible_completion | KIMI-RATIO | 315 | 513856.0079443893298 | 502625.5463817386655 / 525599.7968511934777 |
| orchestrator | gpt-oss-120b | MAMR | completion | ORCH-MEAN | 70 | 101645.0000000000090 | None / None |
| orchestrator | gpt-oss-120b | MAMR | prompt | ORCH-MEAN | 70 | 129658.9999999999950 | None / None |
| orchestrator | gpt-oss-120b | MAMR | total | ORCH-MEAN | 70 | 231303.999999999990 | None / None |
| orchestrator | deepseek-v4-flash | MAMR | completion | ORCH-MEAN | 70 | 26956.0000000000010 | None / None |
| orchestrator | deepseek-v4-flash | MAMR | prompt | ORCH-MEAN | 70 | 97354.9999999999940 | None / None |
| orchestrator | deepseek-v4-flash | MAMR | total | ORCH-MEAN | 70 | 124311.0000000000020 | None / None |
| orchestrator | qwen3.5-122b | MAMR | completion | ORCH-MEAN | 70 | 294326.000000000010 | None / None |
| orchestrator | qwen3.5-122b | MAMR | prompt | ORCH-MEAN | 70 | 99764.0 | None / None |
| orchestrator | qwen3.5-122b | MAMR | total | ORCH-MEAN | 70 | 394090.000000000010 | None / None |

- ORCH-MEAN为210个五月编排推断槽位，沿用1023每模型70条锚点的均值，合计约749,705；不是五月原生usage，跨期/provider/任务漂移是共同未量化偏差，不是统计CI。旧742,055目标未复现、749,714舍入对照均不作为采用估算。
- KIMI-RATIO为GT-1/2的640条可见输出代理；不是含未知hidden reasoning的原生completion/total。lower/upper仅sensitivity-not-CI，不是消耗上下界；GT prompt模板未校准，保持partial/unknown；MiniMax主表仍unknown。
- 既有S3 MINIMAX-SCENARIO（GT2字符代理）仅历史情景：1,058,844 visible-token-equivalent与3,507,421 completion scenario是不同对象，不是上下界，不进入估算账合计。完整原情景只读保存于 `B/inputs/scenarios.csv:1`。
- S4 LEGACY-DIAGNOSTIC失效、旧强制GT对半分摊与PROVIDER-DIFFERENCE语义不启用，不进入主结果、有效区间或总量。`B/inputs/estimators.json:1`仅保存历史元数据，不表示全表每个旧estimator在此获准。

**本报告不发布measured+estimated“全项目总量”**；估算按对象/适用域分开，没有可识别的全项目误差界。

## 5. 映射、验证和发布边界

`B/mapping.csv:1`覆盖全部13,237资源行：每行resource_record（1-based数据记录）、resource_csv_line（当前CSV每条单行；独立verify检查）、account_id、原始复合身份、row SHA-256、主/历史/资源分派、估算字段与采用binding。原始source_path/archive_path/hash只作为冻结引用，脚本不打开这些活动源路径。所选paper/history原字段逐值保留，resource原CSV逐字节保留。

核算关系：paper5,220、独立history2,310与resource-only5,707构成resource行的互斥分派；估算层是资源行的字段视图，非第四份资源。不得把主表与附录相加。

```sh
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-paper-accounting-20261027/run_checks.py
PYTHONDONTWRITEBYTECODE=1 python3 analysis/token-paper-accounting-20261027/release.py verify
```

`run_checks`只从本包固定inputs运行新build/独立verify/测试，并以不同PYTHONHASHSEED两遍比较；有release锁时拒绝运行而不是静默重封。发布后仅release verify只读检查；首次seal必须显式执行，不能覆盖已有锁。锁是SHA-256完整性，不是真实性签名。

验收结果另见 `B/check-run.json:1`、`B/verification.json:1`、`B/REVIEW.md:1`。独立verify不导入生成器，重建选择/映射/原字段保留/估算与coverage，报告字节hash与表逐项核对；不是外部独立审计，也不是重跑旧parser或原始API结果有效性。

最终限制：未补全全项目usage、统一HTTP/计费发送分母、全部历史执行源码版本、整体exit/全树永久停写/未来不补跑证明。主表是批准的核算视图调整，不提升研究效果证据等级。无API/进程启停/commit/push；不输出金额或投注建议。
