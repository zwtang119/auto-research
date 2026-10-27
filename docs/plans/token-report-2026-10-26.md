# Plan: Token 调用报告（分阶段交付）

> 2026-10-26 立项。基于 `docs/investigations/token-report-imputation-feasibility-2026-10-26.md` 的调查裁定。
> 用户裁定：1023 与 1025 实验仍在运行，**先做除此之外的 token 调用**，实验完毕后**追加**，最后出整体报告。

## 交付目标

向审稿人提交一份**分层 token 调用报告**（仅 token，不含金额），覆盖全部已执行实验，并附可离线复现的台账。

## 不可协商的约束

1. **只新建文件，不改动任何现有代码或实验目录**。1023/1025 正在运行，全程不得写入 `analysis/tsinghua-baseline-audit-20261022/` 与 `analysis/tsinghua-factorial-ablation-20261025/`。
2. **五级状态落在字段级**：measured / reconstructed-imputed / partial / not-applicable / unknown。同一条调用可同时是 measured completion + unknown reasoning。禁止把缺失或来源未知改写成零，禁止把估算改写成实测。
3. **禁止用不匹配分母、共享副本或任意分摊支撑比较结论**。
4. 任何数字必须能被离线脚本从冻结输入重算。
5. `policysim-research-Tsinghua` 仓库**本阶段只读**：11.3× 的更正以"更正登记表"交付，不直接改写他仓文件。

## 分层裁定（已定，无须再议）

| 情形 | 层级 |
|---|---|
| 1023/1025 provider 原生 usage | measured |
| 5月 raw + evaluation | measured（共享 usage 去重属确定性重建） |
| 5月 GT-2/GT-1 | completion: reconstructed-imputed；prompt: partial |
| 5月 GT-0 | partial（50 次为设计调用数，实际物理调用数 unknown） |
| 5月 MAMR 编排者 210 次 | reconstructed-imputed（1023 同任务锚点） |
| 2月试验 | 已证实本地合成: N/A；来源未明: unknown |
| error/pending/null-usage | unknown（null ≠ 0） |
| MiniMax reasoning_tokens=0 | provider 字段 measured；reasoning 分解 unknown |

## 已定数字（Green Source，已复核）

- 5月生成（去重、匹配3模型）：SASR **808,076** / MAMR **3,101,262**
- 5月评估：Track A SASR 2,135,216 / MAMR 2,630,591；Track B SASR 1,166,393 / MAMR 3,367,854；合计 9,300,054
- 5月 MAMR 朴素求和 9,303,786 → **虚增 3.00 倍**（同一 total_token_usage 写入3个企业文件）
- 头条比值：原 **11.3283× 撤回**；主报 **3.8378×**（共同企业产出单位）／辅报 **11.5135×**（架构 episode 单位）
- 编排者跨期锚点估算 **742,055**（舍入均值版 749,714，差 7,659 待解释并冻结一个版本）
- GT-2 kimi 可见 completion 估算 **1,060,348**（敏感性 1,037,174–1,084,582，**非置信区间**）
- GT-2 minimax 主表只报可见字符 **2,132,512**；原生 completion 与隐藏 reasoning unknown；代理 1,058,844 / 含隐藏思维 3,507,421 仅进情景表
- 2月：02-23+02-26 共 514 份生成产物为已证实本地合成 → N/A；02-19 provenance unknown；02-21 混合补齐

## 工作项

### [ ] Item 1 — 5月实验抽取引擎与字段级台账（可复现）
**目标**：建立 `analysis/token-imputation-audit-20261026/` 包，写出离线抽取脚本，产出 5月实验的字段级 call-ledger。
**Done when**：
- `manifest.json`（来源路径、SHA-256、纳入排除规则、共享 usage 关系、快照时刻）
- `call-ledger.csv`（每行一个调用/一次计量单元，字段含 stage/condition/model/source_path/source_hash/shared_group_id/dedup_key/status/measured-vs-imputed 标志/estimator_id/lower/upper/interval_type）
- `estimators.yaml` + `calibration.csv`（每个估算式的系数来源、校准对象、适用域、chars 定义、模板处理、隐藏 reasoning 处理）
- `reproduce.py`（离线、无网络、无 API、从冻结输入重算全部采纳数字；自检：共享 usage 不重复计入、原生小计与源记录一致、真实重试未被哈希折叠、表中比值可由同一 ledger 重算）
- 5月五情景 S0–S4 的 `scenarios.csv` 与 `summary.md`
- 包内 `README.md` + `CHANGELOG.md`
**边界**：不碰 1023/1025 目录；不写 policysim-research-Tsinghua。

### [ ] Item 2 — 2月试验逐批次定性 + 其余实验纳入口径
**目标**：2月按批次裁定 N/A / unknown / mixed；并给出除 1023/1025 外其余实验的纳入或排除决定。
**Done when**：2月每个子批次（02-19/21/22/23/26）有明确裁定与证据；一份纳入口径表覆盖 model-benchmark、legacy P11、docs/papers-closed-portfolio direction_a、cds4polymarket、papers/* 等。
**边界**：只读。

### [ ] Item 3 — 报告成稿与 11.3× 更正登记表（依赖 Item 1、2）
**目标**：出中间版 token 报告（不含 1023/1025），并给出 11.3× 更正登记表。
**Done when**：
- `docs/investigations/token-report-2026-10-26.md`（中间版，分层表 + 五情景 + 2月定性 + 纳入口径 + 1023/1025 待追加占位）
- 11.3× 更正登记表：逐条列出待改文件、行号、原文、替换文本（**不直接改他仓**）
- 1023/1025 追加操作规程（须先冻结快照再抽取，禁止直接读活动目录）
**边界**：不改 policysim-research-Tsinghua。

## 1023/1025 追加规程（待实验结束后执行）

1. 等待两个实验的完成凭据（complete 标记 + 退出码 + 停写确认）。
2. 对 calls/ 与 journal/ 取只读快照并记录 SHA-256 与时刻。
3. 用 Item 1 的同一套台账 schema 抽取，追加为新的 stage 行，**不覆盖**中间版数字。
4. 重新计算 S0–S4 与头条比值，出最终版报告。
5. 1023 抽取必须按 `os.path.realpath` 去重（5 路符号链接指向同一目录）；1025 以 journal 为准，`provider-ledger.json` 只有金额不可代替 token。

## 【重要更正】Item 1 复算推翻的三处原规格数字（编排者已独立复核）

原规格中的三个数字**无法从原始记录复现**，Item 1 复算后由编排者独立复核确认。**后续一律以更正后为准。**

| 原规格值 | 复算真值 | 性质 |
|---|---|---|
| 编排者锚点 **742,055** | **749,705**（210 条原生记录：prompt 326,778 + completion 422,927） | 742,055 不可复现。旧"舍入均值版 749,714"与原生总和也差 9；7,659 = 9（旧均值说法与原生总和之差）+ 7,650（原目标相对原生总和的下降，**原因未查明**）。prompt 长度调整诊断得 742,258.60，可解释下降 7,446.40，**仍距目标 203.60**。无原公式，不可称"舍入" |
| "GLM Track B 1,447,552 需单列" | **已包含在 9,300,054 内**，不可再加 | 排除其 1,447,552 后的**平衡评估 = 7,852,502** |
| 编排者采用"未舍入逐模型均值迁移" | 锚点按模型均值迁移（gpt-oss 3,304.3/次、qwen 5,629.9/次、deepseek 1,775.9/次） | 这是可复算的迁移口径，采纳 |

**复现命令**：`python3 analysis/token-imputation-audit-20261026/reproduce.py`（离线，11 个生成产物字节一致，自检 PASS）

**编排锚点明细（编排者独立复核，Green Source）**：

| 模型 | n | prompt | completion | 合计 | 均值/次 |
|---|---:|---:|---:|---:|---:|
| openai/gpt-oss-120b | 70 | 129,659 | 101,645 | 231,304 | 3,304.3 |
| Qwen3.5-122B-A10B | 70 | 99,764 | 294,326 | 394,090 | 5,629.9 |
| deepseek/deepseek-v4-flash | 70 | 97,355 | 26,956 | 124,311 | 1,775.9 |
| **合计** | **210** | **326,778** | **422,927** | **749,705** | — |

## 【用户复核触发 2】5 月 token "明显偏低"的归因（编排者亲自复算，Green Source）

**严格同模型同条件对比（每 run completion）**：

| 模型 | 5月 每run | 1023 每run | 差异 |
|---|---:|---:|---|
| qwen3.5-122b | 4,305 | 4,326 | **+0.5%（基本一致）** |
| deepseek-v4-flash | 800 | 1,194 | +49% |
| gpt-oss-120b | 814 | 1,299 | +60% |
| nemotron-3-super | 1,916 | 未使用（5 月独有，已 deprecated） | — |

**三个叠加原因**：

1. **分母口径不同**：5 月 SASR 400 runs（其中 85 为 nemotron，5 月独有、1023 未用，且其每 run 1,916 是 5 月三主模型中最高），1023 SASR 105 runs。5 月的"每 run 均值"看似接近，实则**在 matched-3-model 口径下 5 月 SASR 反而更低**。
2. **run 数不同**：5 月每模型 105 SASR + 105 MAMR（×3 企业 = 315）+ nemotron 85 = 400；1023 每模型 35 SASR + 35 MAMR（×3 企业）= 210 runs/模型。**任何总量对比必须先统一 run 数或统一 per-run 均值。**
3. **模型族差异真实存在**：deepseek、gpt-oss 每 run 高 49%–60%，qwen 几乎相同。**已排除 max_tokens 解释**——两期 config 的 max_tokens 完全一致（2048）。

**给审稿人的推荐口径**：matched 3 模型 × matched run 数 × per-run 均值。**禁止口径**：直接比总量（run 数、模型数、阶段数均不同）。

## 【用户复核触发】思考 token 口径裁决（编排者亲自复算，Green Source）

用户质疑："口径不对，你这里不含了思考的 token 吧？1023 单个 glm 光思考就消耗了 300～500 万 token"。

**裁决：数字没有漏算思考，但台账与报告都没有把思考拆出来呈现。这是呈现缺陷，须修复。**

**证据一：provider 上报的 `completion_tokens` 本身已含 reasoning**（不是另加字段）

| 范围 | completion | 其中 reasoning | 占比 |
|---|---:|---:|---:|
| 1023 生成 Qwen3.5-122B | 2,199,984 | 2,034,489 | 92.5% |
| 1023 生成 deepseek-v4-flash | 753,818 | 699,162 | 92.7% |
| 1023 生成 gpt-oss-120b | 647,883 | 280,547 | 43.3% |
| **1023 GLM 评分池（440 条去重）** | **6,420,409** | **5,992,757** | **93.3%** |
| 1025 journal（1215 条） | 5,548,919 | 4,803,708 | 86.6% |

用户记忆的"GLM 思考 300~500 万"命中，**当前实为 599 万**（1023 GLM 评分池，可见输出 token 仅 427,652）。

**证据二：5 月实验的 `token_usage` 亦已含思考**（虽无 reasoning 字段）。决定性证据是 completion/可见字符 比率：

| 模型 | 5 月 SASR | 1023 SASR 对照 |
|---|---:|---:|
| qwen3.5-122b | **7.82** token/字符 | **6.67** |
| gpt-oss-120b | 0.74 | 1.06 |
| deepseek-v4-flash | 0.97 | 1.46 |

qwen 两期同为 6–8 量级（纯可见输出应在 0.7–1.5），故 5 月 completion 含思考。**但 5 月源文件只有 `token_usage{prompt,completion,total}`，provider 未上报 reasoning 拆分 → 5 月各 stage 的 reasoning 只能标 unknown，不得凭空造。**

**缺陷定位**：`call-ledger.csv` 的 `reasoning_tokens_value` 列在全部 4,319 行中**为空**（generation 590 / gt0 50 / gt1 20 / gt2 1260 / gt3 1 / orchestrator 210 / track_a 630 / track_b 1558，无一非空）。

**口径纪律**：
- `completion_tokens_value` = provider 上报，**含思考**。
- `visible_completion_tokens_value` = 仅可见输出（gt1 17,134 / gt2 1,060,348 由此得出）。
- 两者是**不同口径，不可相加、不可互相冒充**。
- reasoning **不得加到 completion 之上**（会重复计算）。

**修复项（Item 4，进行中）**：A 台账补 reasoning 拆分列 + reproduce.py 新增"reasoning ≤ completion"断言；B 新增 1023/1025 四列分解附件（prompt/completion/reasoning/可见输出，带快照时刻与待重算提示）；C 报告新增"思考 token 单列"章节（含中英措辞）；D 陷阱清单补"completion 已含思考"。

## 编排者已核实的 11.3× 更正点清单（Item 3 输入）

更正对象全部位于 **policysim-research-Tsinghua 仓库**，auto-research 内无 11.3× 数字。共 **21 处**出现点：

| 类别 | 位置 |
|---|---|
| wiki | `wiki/concepts/hypotheses.md:67`、`wiki/annotations/progress-history.md:32`、`wiki/annotations/current-state.md:98`、`wiki/annotations/current-state.md:142` |
| 论文写作副本 | `paper-writing/00-GUIDE.md:57`、`paper-writing/experiments/mc-2026-05-05/README.md:20`、`paper-writing/experiments/mc-2026-05-05/analysis/full_output.txt:97`、`paper-writing/experiments/mc-2026-05-05/analysis/paper-upgrade-evidence/{README.md:27,README.md:66,claim_summary.csv:5,condition_metric_recalculation.csv:14}`、`paper-writing/experiments/mc-2026-05-05/analysis/result-landscape/enterprise_role_profiles.md:11,37,63` |
| 实验目录 | `experiments/mc-2026-05-05/{README.md:20,PLAN.md:91,VALIDATION.md:93}`、`experiments/mc-2026-05-05/analysis/paper-upgrade-evidence/{README.md:27,README.md:66,claim_summary.csv:5,condition_metric_recalculation.csv:14}`、`experiments/mc-2026-05-05/analysis/result-landscape/enterprise_role_profiles.md:11,37,63` |

**镜像副本字节一致**（已用 md5 验证 `claim_summary.csv` 与 `condition_metric_recalculation.csv` 在 `experiments/` 与 `paper-writing/` 两处相同）→ 更正必须同步两处，漏一处即产生新的口径分裂。

**注意 `current-state.md:98`（11.3x）与 `:142`（11.51x）本身已不一致** —— 这正是"两个并存口径"的证据点。更正后应统一为"主报 3.8378×（共同企业产出单位）／辅报 11.5135×（架构 episode 单位）"，并注明原 11.3x 已撤回。

**本阶段只出登记���（文件、行号、原文、替换文本），不直接改写他仓文件。**

## 进度

- [x] 调查与裁定（`docs/investigations/token-report-imputation-feasibility-2026-10-26.md`）
- [x] 计划建立（本文件）
- [x] Item 1 — 5月抽取引擎与字段级台账 → `analysis/token-imputation-audit-20261026/`（4,319 行 call-ledger、estimators、calibration、scenarios、reproduce.py、冻结 inputs.zip）
- [x] Item 2 — 2月逐批次定性 + 其余实验纳入口径（只读调查；结论已并入报告 §6、§7）
- [x] Item 3 — 中间版报告 + 更正登记表 + 追加规程 → `docs/investigations/token-report-2026-10-26.md`、`token-report-corrections-2026-10-26.{md,csv}`、`append-1023-1025-checklist.md`

## 阶段一交付状态（2026-10-26）

**验收**：`reproduce.py` 与 `verify-report.py` 均 PASS；两个脚本离线、无网络、不读活动实验目录。
**更正登记**：计划所称 21 处**实际展开 24 处**，加相关旧均值行、二月草稿措辞、direction_a 字符计数项，共 **34 项**。全部为登记表交付，**未改写 policysim-research-Tsinghua**。
**新增纳入项**：model-benchmark（实测 499,645 tokens）作为独立附录，不混入五月 ledger。
**待办（阶段二）**：1023 完成凭据出现后，按 `append-1023-1025-checklist.md` 执行：先冻结快照 → realpath 去重抽取 1023 → 以 journal 为准抽取 1025 → 追加为新 stage 行 → 重算 S0–S4 与头条比值 → 出最终版。
