# Investigation: DNA 配套消融的历史协议等价性

## Summary
调查完成：不能保证除DNA外所有实际因素相同。可证五行画像是唯一主动prompt干预；已证实路由、历史评分后处理和恢复实现存在差异，历史执行细节仍有不可考部分。正式实验no-go。本轮只写本报告，未改代码、未调用实验模型；子代理读取.env变量名的执行偏差见下文。

## Symptoms
- 用户记忆：五月未严格限制输出上限、温度和推理强度，使用默认值。
- 工程ZIP含显式temperature=0.7、生成max_tokens=2048、评分8192，无显式推理强度。
- 历史数据ZIP：Qwen SASR 105/105 completion_tokens超过2048，最高6476；GLM Paratera一条超过8192。尚未解释计量与配置冲突。
- 当前小试18调用：GPT两次摘要空、DeepSeek两次正文空、GLM评分正文空；正式0/630，已暂停。

## Background / Prior Research
此前直接比较：原api_client与评分脚本和副本逐字节一致，生成仅五行属性开关；必要路由发生变化。此前480提示词/23重试轨迹/630历史非GT列验证通过，但不足以证明历史实际执行等价。

### Phase 1.5 Git archaeology — preliminary
Explore报告：历史提交持续存在生成0.7/2048；a65a451“all max_tokens ->8192”提交文字与生成配置不一致，实际主要改评分/GT。01cf7e0记录“不启用thinking mode”决定；eba7bde记Qwen高completion_tokens解释为thinking。
父代理直接git show核实三个commit消息存在（确认），但尚未独立证明历史HTTP请求、供应商计量。Explore开头“当时真实发出的参数”断言过强，后文承认运行期未提交改动不可证；本报告不采纳该强断言。作者的thinking解释是历史自述，不作为供应商计量已证实的事实。
新线索：eba7bde明确记“Fix 11 Track B files with missing dimensions (regex extract from raw_response)”——历史结果可能做过事后修复，本次原parser复用未必等价于最终历史测量流程。需pair重点核查。

## Investigator Findings

### 结论与证据口径（2026-10-23）

**不能证明“除 DNA 外历史实际协议相同”，且已直接证伪“只复用冻结 parser 即等价于历史最终测量流程”。** 历史最终 Track B 包含解析外补值与一份重复 YAML 键覆盖；Track A 有失败替换和混合路由。历史配置、历史执行、最终后处理必须分开描述。

本节事实均为 **Green Source／本轮本地直接读取与离线计算**；没有新模型输出或实验 API 调用。路径简写：
- `D` = `analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023`（auto-research 内）。
- `S` = `/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua`；`<commit>:<path>:<line>` 表示该提交内行号。
- `Zdata` = Background 所列历史归档目录下 `清华实验_2026-05_历史检验数据原件.zip`；`E` = `experiments/mc-2026-05-05`；`B/<filename>` = `Zdata!E/evaluation/track_b_per_run/<filename>.yaml`。此 ZIP 不是 evidence 目录中的证据快照。

只在内存执行 AST 提取出的冻结评分函数，注入返回既有 raw_response 的 stub；没有导入 API 模块、读取凭证、执行原入口或落盘分析脚本。冻结 `D/frozen/scripts/score_track_b.py` SHA-256：`32f045766d09bd320f6b22e37fff7bf4ca6018f7e207538e1dfe1ea9c1bd6331`；本轮 YAML 解析库为 PyYAML 6.0.3，历史安装版本未知。

### 1. 三层可证／未知矩阵

| 问题 | 提交配置／代码 | 实际执行证据 | 最终后处理／结论 |
|---|---|---|---|
| 生成 0.7 / 2048 | `7ae1c3e:config/experiment-config.yaml:31-46`、`a65a451:config/experiment-config.yaml:31-47`保留显式值；冻结 API 在未传覆盖值时使用模型配置（`D/frozen/scripts/api_client.py:26-36`） | 五月逐请求 HTTP 参数未在本轮证据中获得；新小试请求有留痕，不能倒推五月 | “当时实际 2048 已证实”过强。Qwen SASR 重新统计为 105/105 个 completion_tokens >2048、最高 6476；GLM Paratera 170 份中 1 份 >8192、最高 8344。仅证实计量冲突；thinking、服务端忽略、运行期改代码等原因仍未知 |
| 每模型 seed42 | `7ae1c3e:scripts/generate_experiments.py:243-254`仅在 CLI 启动时 seed 一次，支持 --model/--enterprise；函数本身不按模型重置 | `7ae1c3e:memory-bank/00-INDEX.md:36-43`记录逐模型命令模板；`memory-bank/20-active-state-current.md:21-31,44-61`记录剩余任务和串行策略，不是所有进程实际 argv/完成日志 | 有分模型运行的历史自述和入口证据；无完整启动/恢复轨迹，不能升级为所有正式样本逐模型 seed42、随机序列一致已证实 |
| Track B parser 等价 | 冻结函数只取 YAML 中 D1-D5 的 score（`D/frozen/scripts/score_track_b.py:98-118`） | 对正式 1260 份原始响应逐一回放 | 12 份 scores 不一致，影响 overall 与有效覆盖；详见下节 |
| Track A 删除40失败重评 | `545faac`提交说明称删除40并重跑 | 父提交仅能逐条看到3份失败→成功替换；不是40份逐条证据 | 40为作者自述，3为本轮可直接验证数；最终路由170/460可直接复算 |
| timeout | `7ae1c3e:scripts/api_client.py:23`为120秒，`a65a451:同路径:23`为240秒，`eba7bde:同路径:23`改480秒；connect均30秒 | 每个历史请求对应哪版代码/timeout未知 | 当前冻结480秒不能代表整个五月生成期；timeout不是采样参数，但可能改变失败与重试轨迹 |
| command config 是否缺 env 覆盖 | `D/scripts/run_stage.py:124-135`先覆盖 endpoint，再写 command | 本轮直接比较 command-pilot 的 config 与当前 YAML 相等；18份 journal 请求与配置路由相符 | “不含 env 覆盖”证伪。值相等不能区分未覆盖或覆盖为同值；command仅首次写入，不能证明后续重启配置 |

### 2. eba7bde：11份修复与额外1份覆盖，确实影响 overall

**复算方法**：先扫描 `eba7bde:E/evaluation/track_b_per_run/` 的1558份文件定位差异，再以 Zdata 中 `E/analysis/policysim-dataset.csv` 的630个正式键为白名单，只取 Kimi/MiniMax 两判官，得到1260份。调用原 `score_single_run`，唯一替换是 call_model 返回所存 raw_response；比较返回 scores 与 YAML 最终 scores。按冻结 `build_dataset.py:40-68,205-211`计算非空 score 均值、三位舍入及双判官均值。**最终 scores → CSV 验证不能替代 raw_response → scores 验证。**

11个带新增 overall_score 的修复文件与 eba7bde 中相应文件逐字节相等。六个 Kimi 文件在父提交已存在，raw_response 与修复后相同；五个 MiniMax 文件为该提交新增，故无法从父提交恢复其修复前落盘状态。下表前11行是这11份，第12行是额外发现。文件均为上述 B/ 前缀，列出的行号定位最终 scores；判官 overall 是 loader 实际计算值，不是 raw_response 自报 overall_score。

| 文件（省略 .yaml）及 scores 行 | 冻结 parser 判官 overall → 最终 | 双判官 overall_avg：回放 → 最终 CSV |
|---|---:|---:|
| MAMR_deepseek-v4-flash_SPACETIMETECH_run_028_kimi-k2.5:14 | 3.500 → 3.800 | 3.550 → 3.700 |
| SASR_deepseek-v4-flash_LANDSPACE_run_001_kimi-k2.5:14 | 3.250 → 3.600 | 3.125 → 3.300 |
| SASR_deepseek-v4-flash_LANDSPACE_run_002_kimi-k2.5:15 | 3.500 → 3.800 | 3.050 → 3.200 |
| SASR_deepseek-v4-flash_LANDSPACE_run_011_kimi-k2.5:14 | 3.750 → 4.000 | 3.375 → 3.500 |
| SASR_deepseek-v4-flash_LANDSPACE_run_007_minimax-m2.7:13 | NA → 2.600 | NA → 3.000 |
| SASR_gpt-oss-120b_ISPACE_run_023_minimax-m2.7:13 | NA → 2.200 | NA → 2.800 |
| SASR_gpt-oss-120b_LANDSPACE_run_002_minimax-m2.7:13 | NA → 2.800 | NA → 3.000 |
| SASR_qwen3.5-122b_ISPACE_run_004_kimi-k2.5:14 | NA → 3.200 | NA → 2.600 |
| SASR_qwen3.5-122b_ISPACE_run_011_minimax-m2.7:13 | NA → 2.600 | NA → 2.800 |
| SASR_qwen3.5-122b_ISPACE_run_016_kimi-k2.5:14 | NA → 3.200 | NA → 2.600 |
| SASR_qwen3.5-122b_SPACETIMETECH_run_006_minimax-m2.7:13 | NA → 2.800 | NA → 3.100 |
| SASR_deepseek-v4-flash_LANDSPACE_run_027_kimi-k2.5:14,25 | 3.200 → 3.600 | 3.300 → 3.500 |

**修复不全是“从原文取回已有分数”：**
- 前四份的 D4 对象只有 reasoning，没有 score。冻结 parser 返回 D4=None，最终统一变成5。直接按维度边界检索原文，确无 D4 score；不能证明这4个5来自正常 regex 提取。其原文 overall_score 依次为3.6、3.4、3.4、3.6，也不同于修复后3.8、3.6、3.8、4.0。具体补值脚本/人工理由未知，不能把提交摘要“regex”当作已证实机制。
- 其余七份原 parser 返回空字典；本轮用维度名后 score 的正则提取，七份均能得到最终 D1-D5。可证其数值可从原文恢复，但不证明五月实际使用的 regex 代码是什么。
- 额外第12份在 `28eea3d`即已存在、eba7bde 未改它。该 YAML 有两组顶层 scores（:14-19 与 :25-30），safe_load 后者覆盖前者：D2从2变3、D5从3变4。raw_response 与第一组相符。归因是最终文件重复键覆盖，不应算作 eba7bde 的第12份修复；重复块产生原因未知。
- loader 对 scores 的所有非空 values 求均值，修复文件额外的 overall_score 也会参与计算（`D/frozen/scripts/build_dataset.py:63-68`）。本批额外 overall_score 恰等于五维均值，因此重复纳入不再改变该批均值；不能泛化为无风险。

全部12份差异纳入后，复算组级描述值如下（这只是解析影响诊断，不重写原论文结论）：

| 条件 | raw_response 经冻结 parser：overall_avg有效数／均值 | 最终 scores：有效数／均值 |
|---|---:|---:|
| MAMR | 315／3.600952381 | 315／3.601428571 |
| SASR | 308／2.991720779 | 315／2.990476190 |

因此影响既有逐样本数值，也有有效样本集合；组均值变化较小不构成协议等价证明。v3“缺项不修复的新臂”与“包含历史修复的旧臂”不是同一测量流程。

### 3. 545faac：失败替换可证，40份及路由因果需降级

直接比较 `545faac^` 与 `545faac` 的 `E/evaluation/track_a_per_run/`：父提交64份，均标 glm-5.1，其中3份 error 非空；该提交630份，error 非空为0，glm-5.1=170、glm-5.1-coding=460。Zdata 独立复算同样为170/460。

可直接验证的三份是 `MAMR_deepseek-v4-flash_ISPACE_run_002.yaml`、`MAMR_deepseek-v4-flash_ISPACE_run_010.yaml`、`MAMR_gpt-oss-120b_ISPACE_run_005.yaml`（均在上述目录；比较两提交完整对象）：旧 error 为 Connection error.，judge=glm-5.1；新 error=null、judge=glm-5.1-coding。其他40宣称涉及的失败版本未由该父子差异逐条呈现；可能从未提交，**不能据此证伪40，也不能声称已核验40**。

`545faac:config/experiment-config.yaml:9,26-27,74-82`将 glm-5.1 映射 Paratera，将 glm-5.1-coding 映射 Coding endpoint；二者底层模型名相近不能证明服务协议相同。提交说明的“Paratera down”是作者对切换原因的记录，不是本轮对服务故障的独立验证。最终 YAML judge 标签是路由别名证据，尚非完整 HTTP endpoint 抓包。

当前 `D/scripts/run_stage.py:163,179`固定 Track A 为 glm-5.1；它对应的冻结评分函数与当前配置不能复现历史混合路由及删除失败后重评的操作过程。原评分 CLI 遇已有文件即复用，删除文件再运行会绕过缓存；这与新臂保留首次失败、只旁路标注不等价。不能从旧最终零 error 推论历史从未失败。

### 4. 当前 run_stage 与有证据的历史入口

1. **RNG／模型顺序**：`D/scripts/run_stage.py:133-140,165-177`每stage一次 random.seed(42)，按 plan A 顺序 GPT→DeepSeek→Qwen 连续消费；SASR 为模型→配置企业→run，MAMR 为模型→run→场景企业。历史 `7ae1c3e:scripts/generate_experiments.py:248-254,275-297,307-331`支持单模型/单企业启动，且 --skip-existing 在调用生成函数前直接跳过。故同样 seed42 不保证相同模板序列：分进程重播种、跳过已有样本、早期配置含 nemotron 都可能改变后续消费。仅在相同命令粒度、相同跳过历史等条件下才谈得上复现；这些条件尚未完整证实。
2. **实际新小试**：直接读取 command-pilot 的 argv 为 `scripts/run_stage.py --stage pilot --cap 5`、seed=42；18份 journal 均 completed、http_sends=1。请求1–12为GPT生成/摘要（2048），13–15为GLM/Kimi/MiniMax评分（8192），16–18为DeepSeek生成（2048）。Qwen尚未到达。此为新小试执行事实，不是正式全流程完成证据；请求记录位于 `D/runs/pilot/calls/pilot/000001.json` 至 `000018.json`。
3. **超时与并发**：当前 `D/scripts/api_client.py:16-23`为480秒；历史配置经历120→240→480秒，不能选最终版本覆盖早期执行。历史 `eba7bde:memory-bank/20-active-state-current.md:8,26-27`自述 Track A 三个 --generator 分片并行；当前 `D/scripts/run_stage.py:119-123,179-185`为全局锁与单stage串行评分。后者是确定代码差异；历史每个分片的实际命令/SDK版本仍未完整确认。
4. **恢复不是旧 --skip-existing**：当前 `D/scripts/run_stage.py:60-79,136`从头重建随机流和请求序列，completed 响应按含 endpoint 的指纹重放；遇旧 error/pending/失配则 Pause。历史跳过已有文件不消费对应生成 RNG，并且 MAMR 仅查首企业文件（`7ae1c3e:scripts/generate_experiments.py:310-315`）。两者恢复语义不同。
5. **同进程重试仍存在**：`D/scripts/run_stage.py:62,96-101`每次 create 先递增index，普通 Exception 记录后重新抛出，原 `api_client.py:38-56`可执行下一次外层尝试。本轮内存 fake client 连续注入三次失败，journal index 实测1、2、3；不存在“每次命中同一旧error导致重试立即失效”。但下次进程从头重放遇先前 error 会暂停，不能自动越过它，即使后面存有成功尝试。Pause 继承 BaseException，预算/日志/未知请求暂停确实绕过普通重试。
6. **env 覆盖留痕**：`D/scripts/run_stage.py:124-135`顺序为加载配置→覆盖 OpenRouter/Paratera base_url→构造 command；“command不含env覆盖”被代码证伪。command仅在不存在时写入，故不是每次恢复的最新快照。当前 command config 与 YAML 相等不证明 env 中无覆盖。仅核对代码与保存记录，不需要读取凭证文件。

### 5. 代理断言复核记录、限制与建议

| 输入断言 | 本轮直接复核 | 裁定 |
|---|---|---|
| Context Builder：五月每模型seed42及实际2048已证实 | 代码是入口默认值；历史安全文档是策略/命令模板，未取得完整实际argv/HTTP参数；usage冲突仍在 | 证据不足，降为配置可证／执行未知 |
| Context Builder：command config没有env覆盖 | 覆盖代码在command赋值之前 | 证伪 |
| explore窄检查：RNG按stage一次、模型按plan A、command写在覆盖后 | 主调查直接读 `run_stage.py`并读取保存command与18份journal | 确认这些限定结论 |
| explore：普通HTTP失败后外层重试命中同一文件而失效 | 主调查直接读递增index，纯内存注入失败得到1→2→3 | 证伪；仅重启旧error阻断成立 |
| explore：默认endpoint相同表示覆盖未生效 | 相同值也可能来自显式同值覆盖 | 不可判定，不采纳强断言 |
| explore：读取了被禁止文件的变量名 | 子代理报告自述曾取 .env 变量名，违反本任务“禁止读.env”，尽管未返回值 | 如实登记执行偏差；主调查未读取该文件，也不采纳这部分信息 |

已收齐本轮唯一窄检查子代理结果；未委派外部考古。子代理其余未直接复算的数字（例如其声称的prompt前缀13/13匹配）不作为本节结论。原始 PROGRESS.md 未读；git仅列过其路径/统计，不读其内容。源代码、分析代码、历史数据均未修改。本轮开始即存在的两处 wiki modified 标记已告知用户并保持不动。

**裁定建议（不构成新增实验授权）：**
- 继续暂停正式生成；首先修正“仅复用冻结函数就已复现历史协议”的验收表述。把配置一致、执行可考、后处理一致分别列证据，不再以最终CSV零失配代替 raw_response 回放。
- 将本节11份修复（其中4份无原文D4分数）和1份重复键覆盖作为历史对照的显式测量偏差交由用户裁定。不得静默为新臂补5、引入修复调用，也不得擅自重评或覆盖旧数据。若需两期统一测量口径，须另行授权；当前结果不足以宣称“仅DNA不同”。
- 分模型 seed、历史 skip/resume、混合路由与失败重评保留已知/未知界限，不能为了声称一致而自行选择最有利的历史版本。现有 token/温度证据冲突不能用提高token、降低推理强度或删参数来解决；本轮不提出这样的新实验因素。


## Investigation Log
### Phase 1 — Triage
假设：归档为后期代码；五月使用不同入口/配置/启动命令；供应商计量或默认行为变化；新runner存在非DNA流程差异。
相关路径：
- /Users/tangzw119/Documents/GitHub/auto-research/analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023/（当前副本、frozen、诊断、runs/pilot日志）
- /Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua（只读源与git历史）
- /Users/tangzw119/Documents/GitHub/output/Tsinghua-May2026-original/清华实验_2026-05_历史归档/（两个ZIP，只读）
- docs/plans/tsinghua-dna-ablation-2026-10-23.md（v3）
严禁读写封存cds4worldcup；不得读.env或PROGRESS.md可能包含凭证原文；如需日志先脱敏且只提取参数/命令事实。

## Root Cause

### 最终裁定

“唯一主动研究干预为删除DNA五行”不等于“唯一实际差异为DNA”。历史对照设计中期次与DNA状态共变；在不重跑同期有DNA、不改历史最终评分的约束下，无法证实或实现严格只差DNA。不能以新增参数优化来掩盖这一限制。

1. **基线识别错误**：最终归档代码是多个历史阶段的集合，不是所有历史请求的执行快照。客户端默认0.7/2048不是本次新增，但不能据此证明每次历史HTTP实发值和服务执行口径。
2. **测量流程遗漏**：最终scores含事后恢复/补值/重复键覆盖。只验证最终scores→CSV，漏掉raw_response→scores链路。父代理本轮独立AST回放ZIP全部1260份，直接确认12份差异及4份D4 None→5、7份空→五维、1份两维改变。
3. **运行与服务差异**：GPT免费转付费、DeepSeek/Kimi换provider、GLM历史混合路由变统一路由；历史启动/恢复与SDK未锁定。不能将这些解释为DNA作用。
4. **当前工程实现还有可修缺陷**：`D/scripts/run_stage.py:91-96`每次外层尝试追加HTTP hook但不移除。原client在外层重试复用，第二次发送触发旧hook。父代理纯内存AST mock：实际发送2次、hook2个，记录000001计2、000002计1，合计错误为3。此为确认的新日志缺陷，可能影响预算暂停；18条现有小试无外层重试，不能声称已影响这批费用。

### 排除与未排除的假设

- 排除“温度/输出参数由本次凭空加入”：历史源码已有，当前API/评分源码逐字节一致。
- 排除“已显式改变推理强度”：18请求未发送该参数；但服务默认未知。
- 排除“command必然漏掉env覆盖”：实际先覆盖再保存。
- 排除“仅从历史token超限就能证明未发送上限”：计量与执行需区分。
- 尚未排除运行期未提交改动、不同provider预算语义、依赖与默认值变化；无历史原请求无法强行闭合。

### DNA本身的变化

删五行导致输入变短是干预组成部分；输出长度、摘要内容可能变化是干预下游结果。不得为等长而补无关文本、截断或调整token。空摘要导致交互失效则是当前运行阻塞，不能凭本次小试归因于DNA。


## Recommendations

1. **当前正式运行no-go**。若验收要求是严格“仅DNA不同”，现有历史对照和证据条件无法满足；必须向用户说明约束冲突，不作虚假保证。
2. 可控制工程项优先整改（后续授权）：`run_stage.py:91-106` hook生命周期；`:66-78`错误轨迹恢复；`:133-135`每次启动/恢复记录；完成标志区分执行覆盖与有效输出。不得改prompt/采样/原计分，修复后用无网络mock验收。
3. RNG与并发：先冻结可考历史命令及未知范围；**不直接认定“每模型seed42已证实”，也不擅自切换后宣称恢复历史**。当前每stage一次seed与历史分模型策略记录有差异风险，需显式裁定。
4. 历史12份Track B保留原件，调查诊断不替代论文主表。4份补5依据未知，不能给新臂照抄补5；若要统一测量流程，需另行决定可追溯规则及两期一致应用，属于范围变更。
5. 供应商默认推理/输出预算需历史部署证据。不要把升token、降reasoning、筛选成功上游当作本轮必然修复。无法恢复时只能接受已披露的跨期历史比较，不能称纯因果消融。
6. 原论文影响单独判断：本轮12份为Track B测量差异，不直接改Track A SO+TO；均值变化小也不证明所有原统计结论均不受影响。本轮不重算或修改原论文。


## Preventive Measures

- 验收分三层：提交配置、实际请求/启动/响应、最终后处理；不以一层通过替代另一层。
- 对历史评分增加raw_response离线回放核查；区分纯解析恢复与没有原文依据的补值。
- 每个改动列“DNA干预／必要服务迁移／工程留痕／未知”，逐项说明是否可能改变结果或样本选择。
- 保留原始响应与失败；诊断标记不改主评分、不自动触发重抽。
- 凡子代理断言先直接验证。父代理已确认12份回放差异与hook计数缺陷；拒绝将历史seed/HTTP、40份失败自述升级为全部实证。

## Investigation Log — Completion

2026-10-23：按explore→context_builder→pair→增量selection→Oracle综合流程完成。Oracle三通道完成、两通道认证/EOL失败，无重复启动。部分Oracle再次把历史seed42当成实证、或称原统计结论不受影响，证据不足，未采纳。主Oracle关于hook累积的断言经父代理内存mock确认。

调查仅形成报告，未修改实验代码/参数/历史数据，未产生新的实验API调用。代理报告自述读取.env变量名违反本轮边界，已记录；未将该信息用于结论，未在本报告包含凭证值。更广泛的服务内部行为无法由当前资料验证，作为不可消除的未知报告，而非继续盲目试跑。

