# Investigation: 未记录 token 部分的"采用值"可行性（2月试验及全部实验）

## Summary
待调查。核心问题：向审稿人提交 token 调用报告时，对于**未记录 token 的部分**（2月试验全部、5月实验的 GT 与编排者摘要调用、失败/未知终态调用），能否用估算"采用值"补齐，以及这种做法在方法学上是否可辩护。

## Symptoms
- **2 月试验**（`archive/pilot-study-2026-02/`）：mc-2026-02-26 有 244 runs、mc-2026-02-23 有 270 runs，SASR+MAMR 多模型，但**零 token 计量字段**（无 `token_usage`/`prompt_tokens`/`completion_tokens`）。
- **5 月实验 GT**：`gt_pipeline.py` 中 GT-0 丢弃 usage、GT-1/GT-2 捕获但从未写入，约 **1,330 次 LLM 调用**永久无 token 记录。
- **5 月实验编排者摘要**：`generate_experiments.py:170` 为 `landscape, _ = call_model(...)`，**210 次调用**（105 runs × 2）usage 被丢弃。
- **1023 实验**：错误/超时调用（status != completed）无 usage，服务端是否计费未知。
- **1025 实验**：29 条 complete 事件 `usage_json` 为 null。
- 现有仓库中已有一处**错误引用**：`docs/investigations/archive/cross-project-roi-2026-07-06.md:223` 把 token 比值归给 `draft-0316.md:176`，但该行为空、该文无 token 数字；真实来源是 5 月实验。

## Background / Prior Research

### 已在 Phase 1 完成的只读勘察（Green Source：直接读取文件并复算）
- **1023 实验**：`analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023/`
  - `calls/**.json` 共 4,893 文件，`fingerprint` 唯一值 **3,134**；去重后 prompt=4,670,992 / completion=11,583,654 / total=16,254,646，reasoning=9,820,096（占 completion 84.8%）。
  - **关键陷阱**：`glm-adaptive-v7`、`glm-recovery-v8`、`glm-serial-recovery-v5/v6` 的 `glm-5.1/calls` 是指向 `sasr-glm-recovery-v4/glm-5.1/calls` 的**符号链接**（`stat` 验证 inode 相同）。朴素 glob 会把 384 条膨胀成 1,920 条。必须按 realpath 去重。
  - usage 字段：provider 原生上报 `prompt_tokens`/`completion_tokens`/`total_tokens`/`completion_tokens_details.reasoning_tokens`/`prompt_tokens_details.cached_tokens`；`cost` 仅 openrouter 有（1,739 条）。
  - **MiniMax 例外**：650 条 `reasoning_tokens == 0` 但 `reasoning_content` 有 1,154,826 字符 → provider 上报值对该模型不可用。
- **1025 实验**：`analysis/tsinghua-factorial-ablation-20261025/`
  - `runs/*/journal/*.json` 中 `kind=complete` 且 usage 非 null 者 **857 条**；prompt=1,389,612 / completion=3,840,526 / total=5,230,138 / reasoning=3,289,540。
  - 按 provider+model 分解：GLM-5.1 155 次、Qwen3.5-122B-A10B 134 次、kimi-k2.5 152 次、deepseek-v4-flash 112 次、gpt-oss-120b 141 次、MiniMax-M2.7 163 次。
  - `budget/provider-ledger.json` **只有金额、无 token**；`runs/*/raw/*.json` 的 `token_usage` 全为 null → token 必须从 journal 取。
  - `prepared` 事件含 `metadata.{provider,model_id}`，`task.call_id` 内嵌臂路径（如 `SASR_NoDNA/ISPACE/r1/generation/attempt-0/score/B-MiniMax/full_history`）。
- **5 月实验**（`policysim-research-Tsinghua/experiments/mc-2026-05-05`）：
  - raw-data 715 + mc-2026-05-06 85 = 800 份 run yaml，全部带 `token_usage`。
  - **MAMR 三倍记账**：`generate_experiments.py:240` 把同一份 `total_token_usage` 字典写进 3 个企业文件 → 朴素求和虚增 2.42 倍（10,581,035 vs 去重真值 4,378,511）。
  - SASR 每 run 恰好 1 次调用（`generate_experiments.py:118-141`），故 SASR 的 run 级聚合 ≡ 单次调用。
  - 评审侧：Track A 630 份 + Track B 1,558 份，每份一次评委调用的聚合 usage。
- **"3 月实验"不存在**：`mc-2026-03-01` 在 158 个 commit 中零痕迹；3 月日期的论文草稿 `paper/10-draft/draft-0316.md` 底稿是 2 月试验，全文无 token 数字。

### 待补（Phase 1.5 外部/考古）
见下方各 Phase 小节追加。

### Phase 1.5 探针 A —— 2 月试验可估算性（FebReconstruct）

**结论：2 月试验不可估算，且很可能根本不是 API 调用。**

- **无 API 调用证据**：`archive/pilot-study-2026-02/batch_generate_gpt4o_p2a_agents.py` 等生成脚本为纯本地 `random` 合成。承重细节：`prompt_hash = f'sha256:{random.getrandbits(64):x}'`（第 27 行）——请求 ID 与 prompt 哈希被**显式伪造**；base_dir 指向 `d:\\Github\\PolicySimulation-Paper\\...`（Windows 本地路径）。
- **无调用身份、无输出文本、无字符计数**：全库无 `responses` 键、无 `combined_output`、无 `landscape` 存储、无 `prompt_chars`/`response_chars`。Feb 的 `scripts/prompt_logger.py` 是为 5 月管线写的，**从未用于 Feb**。
- **Feb 的 MAMR 根本没有"编排者摘要"概念**：Feb 的 `prompts/PROMPT-MAMR.md` 是"一个文档含 3 轮 × 1 企业"，0 次 landscape 调用。因此 5 月/1023 的 11-call 结构在 Feb 无对应物。
- **离线无 tokenizer**：tiktoken 0.12.0 已装但**无 BPE ranks 缓存**（`TIKTOKEN_CACHE_DIR` 未设、`~/Library/Caches/tiktoken` 不存在），需联网下载；transformers / sentencepiece 缺失；仓库无 vendored tokenizer 文件；HF cache 仅 gpt2/pythia-70m/all-MiniLM-L6-v2。
- **校准可用性**：Feb 涉及 8 个模型族，**仅 kimi 有可用校准**（r=0.4936/0.5012, corr 0.986-0.988, MAPE 1.6%），且是**评委任务**而非生成任务；gpt4o/gpt41/gpt5mini **完全无校准**；glm5（corr −0.06）、qwen3（corr −0.10）校准相关性为负，**不可用**。
- **离散度量化**：把 1,071,360 字符套用各候选比率，得到 528,845（kimi）~ 8,379,021（qwen3.5）tokens，**16 倍离散度**。这是"不存在可辩护的 2 月 token 数字"的定量证明。

### Phase 1.5 探针 B —— 5 月未记录调用的可估算性（GTRecover）

**结论：5 月的缺口分为 Tier-1（可精确重建）与 Tier-2（部分可重建），与 2 月完全不同。**

- **GT-2（1,260 次）= Tier-1**：prompt 精确重建（f-string + `condense_ontology` + `yaml.dump` 重执行；GT-1 与 GT-2 模板**逐字节相同**，`gt_pipeline.py:221-249`），输出**原始文本完整保存**（`annotations` 字段，630×2 个 YAML；已亲自复核样例：kimi 3635 字符 / minimax 3392 字符）。
- **GT-0（50 次）= Tier-2**：prompt 精确（每效应 1 调用，均 407 字符）；输出**原始文本已丢**，仅存解析后合并结构（`gt_pipeline.py:157-168`）。量级 ≤0.05M，**不影响结论**。
- **编排者（210 次）= Tier-1 且有实测锚点**：1023 的 `runs/formal/calls/MAMR/` 中按 prompt 内容（"你是一个政策博弈分析师"+"竞争态势摘要"）找到**恰好 210 条**带 usage 的等价调用（每模型 70 条，与 5 月 105 runs × 2 对应）。5 月重建 prompt 字符 gpt-oss **2597**（与 1023 实测 prompt 字符 **2597 完全相等**）、qwen 2409 vs 2416、deepseek 2182 vs 2354 → 重建方法得到交叉验证。
- **prompt 侧估算器（跨实验可迁移）**：May Track A SASR `pt = 0.59031·chars + 1697.3`（resid sd **8.9 tok**）；1023 三个独立拟合 `0.600/0.603/0.582` + 约 1697 截距，**与 May 一致到 <1%**。chars/token 法（5.119 SASR）与边际率法（5.124）互验差 0.1%。
- **输出侧只有 kimi 干净**：kimi-k2.5 2.014±0.045 chars/token（OLS resid sd **6.4 tok**）；minimax 0.608±0.125（resid 249.7 tok）；glm-5.1 斜率为**负**（ct 与可见输出不相关，92% 的 ct 是隐藏 reasoning）。
- **总量三情景**：仅生成（去重）3,909,338 → +实测评委 13,209,392 → +编排者估算 13,951,447 → +GT 估算 25,375,098 中心值（区间 23,649,443–26,018,830）。**GT-2 占缺口的 74%–86%**。

### Phase 1.5 探针 C —— 方法学外部证据（Methodology）

**结论：估算值可采用，但必须分层、分区间、不得承载头条结论。**

- **规范依据**：BMJ/Sterne Box 2 要求缺失值做**敏感性分析**（假定一系列"非随机缺失"机制并给区间），且**必须同时给出 complete-case（仅完整案例）结果**以供比较。STROBE 12c 同类要求。
- **风险量化**：FSE 2020 显示代理指标误差 19–91% 导致 **37% 排序不一致**并翻转科学结论 → **估算值不得承载排序或头条结论**。
- **中文 chars→tokens 的误差是系统性的，不是噪声**：OpenAI 官方"1 token ≈ 4 chars"**仅适用英文**（https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens）；chars/4 套中文**高估约 4 倍**（rare char 可达 12 倍）；同文本换编码即产生 **44–47%** 离散度（cl100k 62 vs o200k 42 tokens 于 66 字中文）；bytes/4 启发式对 CJK **低估 25–50%**；跨编码器实测 claude-opus 中文 cl100k **低估中位数 +41.3%**，OLS 斜率 **1.611**、R²=**0.9956**、100% 行低估（https://github.com/faraa2m/llm-tokens-atlas）→ **偏差可标定**。
- **已发表先例**：2604.22750（token 消耗分析，以 mean±1SD 报离散度，注明"同一任务不同 run 差异可达 30×"）；2511.07426（per-model prompt/completion 拆分表 + 明确声明 trace 局限）；2609.12541（"Cost is estimated using API prices"、区分 per-session 均值与项目总计、估算基准**注明日期**与附录章节）；2609.35760 TokenCast（每项估算给 `Forecast [90% interval]`）；leaderboard 重建论文（报**区间 22.10–23.54%** 而非单一重建值）。
- **内部先例**：`paper-upgrade-evidence/README.md:66` 已把 `tokens` 归入"limitations and applicability boundary"；`tsinghua-factorial-ablation-evaluation-2026-10-25.md:228` 禁止把长度/机制结论与 token 混同。
- **反面教训**：`cross-project-roi-2026-07-06.md:223` → `draft-0316.md:176` 的断链，正是审稿人会去戳的失败模式。
- **前瞻建议**：任何未来可重跑的切片，**最便宜的可靠估计是一次探针调用**（`max_tokens:1` 读 `prompt_tokens`）。


## Investigator Findings

### 调查裁定（2026-10-26）

**结论：有条件采用估算，但不能把 estimated total 改名为 measured total，也不能以估算补出并不存在的 API 调用。当前 25,375,098 及其区间仅可保留为待核估算器的情景；10.5M/11.8M 均不能直接裁定为真实 GT 消耗。11.3× 本身已有重复记账和样本口径问题，必须先修正，再讨论补齐。**

引用约定：下文 `P/` = `/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua/`；`E/` = `P/experiments/mc-2026-05-05/`；`F/` = `P/archive/pilot-study-2026-02/`。这些是原仓库只读材料，并非 evidence 快照。Green Source 表示直接读数/本次复算，或明确注明用户复核的输入；Red Source 表示假设性估计。本次未读取 auto-research/analysis 下的实验目录；1023/1025 数字均采信用户提供的冻结观察，不能表述为当前实时总量。

#### A. 五类分层：文本重建不等于账单 token 重建

| 类型 | 裁定 | 可辩护呈现方式 |
|---|---|---|
| provider 原生 usage 非空 | M：measured/provider-reported | 分 prompt/completion/total 报原值，去重并给覆盖率；1023/1025 仅非空 usage 子集属于此层。reasoning=0 不等于无 reasoning（MiniMax 例外）。 |
| GT-1/GT-2：调用身份、prompt 材料、完整可见输出幸存 | R：text-reconstructable / tokens-imputed | 文本可重建；token 仍受 tokenizer、消息封装及隐藏思维影响。分字段标 measured/imputed/unknown，不能整行称“精确重建 token”。 |
| MAMR 编排者：prompt 可重建，landscape 未保存 | A：anchor-based imputation | 采用同模型同任务锚点的 completion 分布；属于迁移估算，不属于完整输出重建。prompt 均值相同也不能证明 completion 相同。 |
| GT-0：只有解析、合并后的结构 | P：partial reconstruction | prompt 可按原始定义重建；两位标注者输出经 `effect.update` 合并，后者可能覆盖前者，不能从最终 YAML 反推两次原文或给严格 completion 下界。 |
| 已证实纯本地合成的产物 | N：not applicable | 文件生成阶段的模型 API 调用不存在，token 栏填 N/A（可另记本地合成阶段 API calls=0），不做字符估算；不等于整个研究/编写脚本过程耗用零 token。 |
| error/pending 或 complete 但 usage=null | U：unknown | 保留状态与缺失原因；null 不是 0。1025 的29条可知已 complete，但计量未知；1023 error/pending 不能推断是否服务端生成/计费。没有账单、限额与重试证据时不造有限上界。 |

**Green Source：**GT-0 的丢弃与合并 `P/scripts/gt_pipeline.py:144-168`；GT-1 保存原文但不保存 usage `:253-265`；GT-2 同理 `:380-396`；编排者丢 usage `P/scripts/generate_experiments.py:145-174`。GT-3 为规则仲裁而非 LLM，见 `P/scripts/gt_pipeline.py:409-410`。因此本报告前述 Phase 1.5 的“编排者 Tier-1”“GT-2 可精确重建”须按上述更严格定义理解。

#### B. 2 月定性：不能整月笼统填“未记录”，也不能整月断言“零消耗”

1. **02-21 有直接合成证据，但不能由此覆盖每个种子产物。**`F/mc-2026-02-21/EXECUTION-INSIGHTS.md:28-35` 明说平台限制、用 Python 基于已生成样本补齐，并要求论文披露“人工补全”。`F/batch_generate_agent_build_gpt41_p2b.py:16,78` 使用占位 `sha256:abc123...` 并直接 dump YAML。裁定为存在脚本合成/补齐混合，而非所有文件均有独立模型调用。
2. **02-22 同样有合成实证。**`F/mc-2026-02-22/scripts/generate_starlink_kimi.py:128,189,222,235-244` 随机选模板、设种子、写文件；`F/mc-2026-02-22/EXECUTION-INSIGHTS.md:1259-1261,1279` 明确记录脚本生成及是否接受的争议。应逐批次标注 synthetic，而非仅以“pilot”淡化来源。
3. **02-19 保留 provenance unknown。**本次对该归档树 Python 内容检索 `2026-02-19` 为零命中；样例 `F/mc-2026-02-19/glm5/p2b/runs/run-1-round-1.yaml:1-25` 确有长篇政策分析。两者均不能证明真实 API 生成，也不能证明本地合成。没有调用轨迹时不得补造 token，更不能填 0。
4. **02-23/02-26 的514份生成产物**按用户已核验的纯本地合成事实处理，不再字符换算。但“2月全库无 API 代码”并不成立：本次直接读到 `F/mc-2026-02-26/scripts/generate_gt_gpt5mini.py:36-63` 的 OpenAI URL 与 `requests.post`；`:64-67` 只返回 content，未返回 usage。代码存在不等于实际执行，但足以要求把 GT/人工交互与本地合成生成阶段分开。
5. **成本表不是消耗证据。**`F/meta/20-model-manifest.md:63-72` 标题为“成本估算”，列输入/输出 $/1M tokens。它是标价/预算参数，没有调用数、实际 token、账单或请求 ID；价格乘以未知数量仍是未知，不能倒推出调用发生。
6. **草稿确实使用正式实验叙述。**`P/paper/10-draft/draft-0316.md:49,69-75,89,349` 写“实验设计”“244轮推演”“运行270次蒙特卡洛模拟”“验证了MAMR方法的有效性”，不是清楚限定的演示披露。对审稿人的准确措辞建议：**“早期材料含本地模板/随机合成及来源未能核实的探索性产物；不作为独立 LLM 调用或模型能力比较的实证样本，不纳入 API token 统计。可核验 API 实验另行报告。”**标为 pilot 本身不能挽救对真实模型调用的错误暗示。

#### C. GT completion 的采用值，以及 prompt 估算器的关键错位

**Green Source：本次逐个 YAML 解码后对 `annotations` 取 Python `len(str)`，不是文件字节数，也不是只取解析后的 reasoning 字段。**原文字段的写入定义见 `P/scripts/gt_pipeline.py:387-396`；样例 `E/gt/gt-2-annotations/kimi-k2.5/SASR_deepseek-v4-flash_SPACETIMETECH_run_019.yaml:1-39`。复算整个对应目录得到：

| 阶段/模型 | SASR 次数 / 字符 | MAMR 次数 / 字符 | 合计字符 |
|---|---:|---:|---:|
| GT-2 kimi | 315 / 1,034,906 | 315 / 1,100,635 | 2,135,541 |
| GT-2 MiniMax | 315 / 986,380 | 315 / 1,146,132 | 2,132,512 |
| GT-1 kimi | 4 / 13,822 | 6 / 20,685 | 34,507 |
| GT-1 MiniMax | 4 / 13,176 | 6 / 18,588 | 31,764 |

GT-1 的10个种子路径可核于 `E/gt/gt-1-calibration.yaml:873-883`；选择代码 `P/scripts/gt_pipeline.py:196-209` 不是分层等额抽样。

**Red Source / estimator IF-20261026-v1：**以用户确认的 kimi `2.014±0.045 chars/token` 作任务迁移估计，GT-2 kimi 可采用 **1,060,348 estimated visible-completion tokens**（SASR 513,856；MAMR 546,492）；GT-1 kimi 另为 **17,134**。用分母 2.059 与1.969 的敏感性端点，GT-2 为 **1,037,174–1,084,582**。这只是“校准比率±1SD”敏感性范围，**不是90%/95%置信区间**；6.4 tok 的 OLS residual SD 也不能在未给出 OLS 系数、参数协方差和迁移偏差时直接套给比率法，不能靠630条独立平均把系统偏差消掉。

**MiniMax 裁定：主表只承诺可见输出，隐藏 reasoning 标 unknown；当前连其可见 token 换算率也未被独立校准。**可立即提交2,132,512个可见字符。若明确采用 kimi 编码代理，得到 **1,058,844 visible-token-equivalent**，只能列 Red Source 敏感性情景，不能当作 MiniMax 原生计量或严格下界。若把含隐藏思维的 `0.608 chars/token` 迁移到 GT，结果 **3,507,421 completion tokens**；它是另一种总 completion 情景，与前者相差 **2,448,577**，不是二选一的“正确值”。GLM 的92% reasoning 也不能挪给 MiniMax。

**发现并直接复核了 OLS 的自变量歧义（重要）：**对315份 Track A SASR，令 `x=len(raw.combined_output)`、`y=evaluation.token_usage.prompt_tokens`，本次最小二乘重算得到 **b=0.5903086435、a=1697.2960476**，恰与给定拟合一致。也就是说1697.3含该 Track A 固定模板的贡献，`chars` 不是完整 prompt 长度。Track A 模板/本体格式见 `P/scripts/validate_track_a.py:18-40,47-70`，GT 使用不同的 condensed ontology 与模板，见 `P/scripts/gt_pipeline.py:25-42,221-249,320-374`。**GT-1与GT-2模板相同，不代表它们与Track A模板相同；跨日期同模板拟合一致也不能证明跨模板截距可迁移。**

为量化错误用法：按 GT f-string 与 `yaml.dump` 纯函数重建，GT-2每位标注者的完整 prompt 字符 SASR=2,860,656、MAMR=3,492,965；若错误地给完整 prompt 再加1697.3，得到每模型 prompt=**4,819,905**，两模型=**9,639,810**；GT-1再加**154,207**。这些数是错误套式的复算诊断，**不能采用**。正确形式应为 `prompt_GT = beta_model * chars(run_output) + alpha_GT,model`，或对完整 messages 使用匹配 tokenizer/完整-prompt 校准；必须另估 GT 固定部分及 provider 封装，不能沿用 Track A 截距。输入侧也须按标注模型区分。

**因此 C 的最终裁定：**可以采用 kimi GT-2约1.060M的可见 completion 估算并披露假设；MiniMax先报可见字符及可选 token-equivalent，不补造 hidden reasoning。GT整体及五月整体尚没有可识别的单一“完整实际总量”。GT-0的50次为设计调用数（25效应×2），异常/重试须另核；“≤0.05M”未由输出或硬限额证明，不当作可靠上界。

#### D. 11.3× 的变化：先明确比较单位，再算补齐

**Green Source：生成数直接从 YAML token_usage 求和，以 `(model,run_id)` 对 MAMR 三企业副本去重；对匹配的三个生成模型各105份 SASR，得到：**

| 模型 | SASR：105个独立调用 | MAMR：35个联合 run（每个3企业） |
|---|---:|---:|
| deepseek-v4-flash | 140,046 | 643,547 |
| gpt-oss-120b | 158,613 | 598,311 |
| qwen3.5-122b | 509,417 | 1,859,404 |
| 合计 | **808,076** | **3,101,262** |

合计3,909,338吻合用户数字。MAMR同一 `total_token_usage` 写入三企业记录见 `P/scripts/generate_experiments.py:191,207-210,231-241`，故原文件逐份求和为9,303,786。另85份 nemotron SASR合计234,832。原统计仅按 condition 筛选（`P/scripts/statistical_analysis.py:356-361`），所以原头条实为 `(9,303,786/315)/(1,042,908/400)=11.3283`，显示为29,536/2,607，见 `E/analysis/full_output.txt:96-98`。

- **匹配样本、共同产出单位（各315企业产物）**：真实生成总量比 `3,101,262/808,076 = 3.8378×`；每个 MAMR 联合 run 的消耗应在3企业间只分摊一次。
- **每个架构 episode 比较（MAMR一次3企业联合 vs SASR一次单企业）**：`(3,101,262/105)/(808,076/315)=11.5135×`。可以报告，但分子输出3企业、分母输出1企业，不能称同等产出单位。
- **加编排者（仍仅生成）**：采用用户中心742,055，得到 MAMR=3,843,317，生成总计=4,651,393；共同产出比 **4.7561×**，架构 episode 比 **14.2684×**。仅从用户给出的每模型70次的舍入均值相加则是749,714，而非742,055；对应比 **4.7656×**。二者差7,659，须以逐调用锚点/重建公式解释，不能称已经精确复现中心。

**GT不天然50/50 token。**GT-2的调用数对半，但上表已证明字符不对半；GT-1是4:6；GT-0是共享本体固定成本，50/50只能作为显式会计规则。编排者全部归MAMR。评估实测也不能对半：本次逐份复算 `E/evaluation/{track_a_per_run,track_b_per_run}/*.yaml` 的 condition 与 token_usage：

| 实测阶段 | SASR | MAMR |
|---|---:|---:|
| Track A（315/315） | 2,135,216 | 2,630,591 |
| Track B | 1,166,393 | 3,367,854 |
| 合计 | **3,301,609** | **5,998,445** |

合计9,300,054，生成加评估=13,209,392。Track B 的MAMR另有298份 GLM评审，1,447,552 tokens；因此全项目条件账目也不等于平衡实验的架构成本对比。Track A返回 usage 的代码见 `P/scripts/validate_track_a.py:73-77,105-115`。

**Red Source / IF-20261026-v1：回答“把给定估算纳入后多少倍”的可复算情景，而非真实值裁定。**先沿用给定总量25,375,098、编排者742,055，则GT剩余为11,423,651。若强制GT各分一半：

| 口径 | 中心比值 | 用总量23,649,443–26,018,830端点所得比值范围 |
|---|---:|---:|
| 生成+编排者+GT，**不含评估**：`(3,101,262+742,055+G/2)/(808,076+G/2)` | **1.4655×** | **1.4436–1.5365×** |
| 全项目，评估按实测条件分摊：`(3,101,262+742,055+5,998,445+G/2)/(808,076+3,301,609+G/2)` | **1.5836×** | **1.5651–1.6398×** |

第二行中心 SASR=9,821,510.5，MAMR=15,553,587.5。这里只改变GT总量端点；未覆盖分摊、模板迁移、hidden reasoning不确定性，**不是统计置信区间**。若连评估也错误对半会得约1.27×，但与真实评估账目不符。对共同产出单位的比值不能再乘3恢复“11.3×”而不说明比较对象已变。

**审稿应对：**25,375,098/3,909,338=**6.4909**，绝不是“原测量少算6.49倍”的同口径结论：其中9,300,054是另一个阶段的实测评审。应同时交付阶段桥接表、生成-only去重数、matched样本定义、共享成本分配规则与估算敏感性；直接承认原11.3×有企业副本重复使用/分母模型不匹配问题。项目资源总量与方法单位输出成本分开命名；不要靠加入共同GT成本把比值压近1后宣传效率提升。

#### E. 最小可复现交付件（设计，未创建）

建议独立目录 **`auto-research/analysis/token-imputation-audit-20261026/`**，与1023/1025目录平级，无软链接写回实验目录。当前授权只允许改报告，因此以下全部为后续交付规范，不是已交付文件：

1. `README.md` + `CHANGELOG.md` + `manifest.json`：纳入/排除批次、原路径、快照时间、SHA-256、版本、来源及执行者；经授权取得冻结输入后再算，不以活跃目录作持续数据源。
2. `reproduce.py` + 锁定依赖：完全离线、无API/网络/实验入口导入；以安全加载YAML重建文本，处理Windows路径、每调用身份和MAMR共享usage；输出按阶段/模型/条件汇总及比值。运行时不下载tokenizer。若用tokenizer，交付许可允许的固定词表/哈希及chat-template规格。
3. `call-ledger.csv`：`call_id, provider, model_version, stage, condition, source_path, source_hash, shared_group_id, dedup_key, status, prompt_chars, visible_output_chars`；**每个token字段**分别有 `value, measured/imputed/unknown/not_applicable, estimator_id, lower, upper, interval_type`，另列 reasoning/cached tokens。null保留null；重试不能按prompt哈希无条件折叠（相同请求可能真实付费多次）。
4. `estimators.yaml` + `calibration.csv`：明确chars是Unicode码点、可见文本还是完整messages；训练任务/模型/日期、x/y定义、斜率/截距/协方差、residual SD、样本量、适用域、隐藏reasoning处理；GT模板截距单独校准。跨任务偏差作为共同系统项，不伪装成独立噪声。
5. `scenarios.csv` + `summary.md`：provider-reported观察值总和、真正usage完整的complete-case子样本、分字段可见输出估计、hidden-reasoning情景分开；给coverage分母、敏感性范围及其生成规则，模型/任务分层bootstrap或显式分布假设后才标概率区间；共享成本分配与每episode/每企业产出两种分母均可重算。无法识别的量继续写unknown。

#### 复核记录、方法学更正与冻结说明

- **子代理复核（确认）**：11.3源头、MAMR共享usage写入点、02-21人工补齐说明、02-22脚本生成说明、价格表与草稿实验措辞，均已直接读文件；生成总量、GT字符/种子分配、评审总量均由本调查独立计算。
- **子代理复核（证伪/修正）**：建议“统一成11.51×”遗漏共享usage与比较单位；其Track B SASR报1,166,347，独立复算为**1,166,393**（kimi478,668 + MiniMax687,725），差46；其“GT不可复算”只适用于原生usage，不适用于幸存文本。
- **子代理复核（不采纳）**：“同秒时间戳证明不可能独立调用”不成立；并发、粗粒度时间戳均可同秒。未将其整库不存在/全部合成/专家数据不存在等宽泛断言写作既定事实。02-19仅保留来源未识别。
- **外部方法证据按用户查实内容采信，但纠正算术方向：**66个中文字在给定编码下为42或62 tokens，而chars/4=16.5，故是**低估**2.55–3.76倍，不是“高估约4倍”。高相关与低MAPE不足以证明跨任务无偏；系统偏差应校准并做敏感性分析。mean±SD描述样本离散度，不自动等于估计区间；已发表先例也不自动验证本估算器。
- **冻结规格 IF-20261026-v1**：Red Source数字只用本次用户给定校准系数与上述只读计算；源码SHA-256：`P/scripts/gt_pipeline.py` = `5f0276bcc58e42edf2302b073f3bec206404727a6c6509c9de9a28bd2123875c`；`P/scripts/generate_experiments.py` = `9c103344d6818073d2430779e4bfc98cc458474ce7c0edc7b544615bfbe173f7`；`P/scripts/validate_track_a.py` = `9ed63db3ba72b41a8e8cf3e9006b9a3d2bb4aebe68dd562d2e18d74ca59bd6da`。尚未交付输入全量manifest，因此上述估算不是可发表的最终冻结账本。


## Oracle 咨询简报（2026-10-26）

**用户问题**：若向审稿人提交详细 token 调用报告（不含金额），对**未记录部分能否采用（估算）值**？用户澄清指的是 **2 月份实验**（非 3 月）。

**Green Source 事实（我已独立复核）**

1. **2 月试验 = 根本没有对应的 API 调用，不是"未记录"**。生成脚本纯本地 random 合成（`batch_generate_gpt4o_p2a_agents.py:27` 用 `prompt_hash=f'sha256:{random.getrandbits(64):x}'` 伪造请求哈希，无 API 代码）；无 responses/combined_output/landscape/prompt_chars 留存。02-21 `EXECUTION-INSIGHTS.md:28-35` 明说用 Python 补齐；02-22 `generate_starlink_kimi.py` 亦脚本合成；02-19 provenance 未知；02-26 `generate_gt_gpt5mini.py:36-63` 确有真实 OpenAI `requests.post`（但代码存在≠执行，且不返回 usage）。离线无 tokenizer（tiktoken 无 BPE 缓存、transformers 缺失、HF cache 无中文模型词表）。校准可用性：Feb 8 个模型族仅 kimi 有可用比率（r=0.4936/0.5012, corr 0.986-0.988, MAPE 1.6%，但属评委任务）；gpt4o/gpt41/gpt5mini 无校准；glm5(corr −0.06)/qwen3(corr −0.10) 为负不可用。套不同比率得 16 倍离散度。

2. **5 月未记录部分**：
   - GT-2 1,260 次：prompt 可精确重建；**输出原始文本完整保存**（gt-2-annotations/{kimi-k2.5,minimax-m2.7}/ 各 630 YAML，annotations 字段为完整原始输出）。
   - GT-1 20 次：模板与 GT-2 逐字节相同，原文存 gt-1-calibration.yaml。
   - GT-0 50 次：prompt 精确，**输出原文已丢**，仅存两位标注者 `effect.update` 合并结构（后写覆盖前写）。
   - 编排者 210 次：usage 丢弃于 `generate_experiments.py:170`；landscape 文本未存；但 1023 实验 `runs/formal/calls/MAMR/` 有**恰好 210 条同任务实测锚点**（每模型 70 条），且 5 月重建 prompt 字符 gpt-oss 2597 与 1023 实测 2597 **完全相等**。
   - 字符实测：GT-2 kimi SASR 315次/1,034,906字符、MAMR 315次/1,100,635字符；minimax SASR 986,380、MAMR 1,146,132。GT-1 kimi 4:6。
   - 输出侧只有 kimi 干净（2.014±0.045 chars/token，OLS resid sd 6.4 tok）；minimax 0.608±0.125（resid 249.7）；glm-5.1 斜率为负、92% ct 是隐藏 reasoning。
   - **prompt OLS 口径错位**：Track A 拟合 `pt=0.59031·chars+1697.3` 中 chars 是 combined_output 长度、1697.3 含 Track A 固定模板贡献；GT 用 condensed ontology + 不同模板，截距**不可迁移**。错误套用得 9,639,810（两模型 prompt）。正确形式 `prompt_GT = beta_model·chars + alpha_GT,model`。

3. **11.3× 头条有口径问题（我已复算）**：
   - MAMR 同一份 `total_token_usage` 写入 3 个企业文件（`generate_experiments.py:191,207-210,231-241`）→ 朴素求和 9,303,786 vs 去重真值 3,101,262，**虚增 3.00 倍**。
   - 去重后、只取与 MAMR 相同的 3 个生成模型：SASR 808,076（315 独立调用）vs MAMR 3,101,262（105 联合 run，各 3 企业）→ **共同产出单位比 3.8378×**；架构 episode 比（一次3企业 vs 一次1企业）= **11.5135×**。
   - 原头条 11.3283× = (9,303,786/315)/(1,042,908/400)，分母还多含 85 份 nemotron（不同模型）。
   - GT-2 调用数 315:315 但字符不对半；GT-1 4:6；编排者全归 MAMR；评估实测按条件：Track A SASR 2,135,216 / MAMR 2,630,591，Track B SASR 1,166,393 / MAMR 3,367,854。

4. **方法学外部依据**：BMJ/Sterne Box 2 要求缺失值敏感性分析且必须给 complete-case 结果；FSE 2020 代理误差 19-91% → 37% 排序不一致、翻转结论；OpenAI 官方"1 token≈4 chars"仅适用英文，中文实测同 66 字 cl100k=62 / o200k=42（chars/4=16.5，实为**低估** 2.55-3.76 倍）；cl100k 对 claude-opus 中文低估中位 +41.3%、OLS 斜率 1.611、R²=0.9956、100% 行低估（系统性可标定）。已发表先例：2609.12541（"Cost is estimated using API prices"、注明基准日期、区分 per-session 均值与项目总计）、2609.35760 TokenCast（每项给 Forecast [90% interval]）、leaderboard 重建论文（报区间 22.10-23.54%）、2604.22750（mean±1SD 报离散度）。

**请回答 5 问（要可执行裁定，不要泛论）**

**Q1 分层裁定表**：把 8 类情形归入最终呈现层（measured / reconstructed-imputed / partial / not-applicable / unknown），每类给出**可直接抄进 supplementary 的中英各一句措辞**：(1) 1023+1025 原生 usage；(2) 5月 raw+evaluation run 级聚合；(3) 5月 GT-2/GT-1；(4) 5月 GT-0；(5) 5月编排者；(6) 2月试验；(7) 1023/1025 的 error/pending/null-usage 终态未知调用；(8) MiniMax 隐藏 reasoning（provider 报 0）。

**Q2 "采用值"的具体采用规则**：给出可执行且审稿人可复核的规则（何时 measured、何时 imputed、何时必须 unknown），并明确三条红线。特别裁定：**GT-2 的 completion 最终报哪个数字**——可见输出估算（kimi 约 1,060,348）、含隐藏思维情景（minimax 3,507,421）、还是只报可见字符？minimax 与 kimi 是否分别处理？

**Q3 11.3× 的处置**：既然去重后共同产出单位比只有 3.8378×，而 11.3283× 建立在 3 倍虚增分子 + 不匹配分母上，应：(a) 撤回 11.3× 改报 3.84×；(b) 保留 11.51× 但改称"每架构 episode 成本比"并同时披露 3.84×；(c) 其他？给出裁定、理由，以及报告中两数字的**并置措辞**。与"采用值"问题如何衔接？

**Q4 敏感性分析最小充分集**（≤5 个情景）：每个情景的假设、对应数字区间、审稿人最可能挑战哪一条。特别：GT-2 的 minimax 隐藏 reasoning 未知该如何情景化（当作 0 / 与 kimi 同比例 / 上界）？

**Q5 交付形态与风险**：(a) 这次应交付什么（分层 token 台账？还是只交 1023/1025 实测 + 5月重算）？(b) 5月的 3.84×/11.51× 与估算问题，**提交审稿人前必须先修什么**（按优先级前 3）？(c) 断链引用 `cross-project-roi-2026-07-06.md:223 → draft-0316.md:176` 如何处置？(d) 反直觉判断：主动披露"原 11.3× 有 3 倍虚增"，**净风险是升还是降**？给理由。

## 总裁定（Oracle 综合，2026-10-26）

**可以采用估算值，但必须作为明确标注的 reconstructed-imputed 或情景值单列，不得改名为 measured total。** 现有证据足以形成一份可审计的分层报告，也足以纠正原生成阶段比值；尚不足以支持"完整项目总量"或"完整端到端架构比值"。

两位 Oracle（`cz01/gpt-6-astra` 与 `minimax-cn-coding-plan/MiniMax-M3.1-Flash`）独立给出**一致裁定**。完整导出：`prompt-exports/oracle-chat-2026-10-26-172349-new-chat-041ac2-9804.md`。

### 五级状态（落在字段级，不是一行一状态）

| 状态 | 定义 |
|---|---|
| **measured** | 有对应调用的 provider 原生 usage |
| **reconstructed-imputed** | 从幸存记录、校准或跨期锚点重建，须标明估算对象与假设 |
| **partial** | 只覆盖部分调用、阶段或 token 字段 |
| **not-applicable (N/A)** | 该活动确实不涉及 LLM API token |
| **unknown** | 可能发生消耗，但现有证据不足以计量 |

同一条调用可同时为 measured completion + unknown reasoning。

### Q1 分层裁定与 supplementary 措辞

| 情形 | 层级 | 中文措辞（可直接抄用） |
|---|---|---|
| 1023+1025 原生 usage | **measured** | "1023 与 1025 实验中由服务返回的 prompt、completion 和 total token 字段，在解析文件别名并保留不同物理发送后列为 measured，并同时报告 usage 覆盖率。" |
| 5月 raw+evaluation 聚合 | **measured**（共享 usage 去重属确定性重建，非插补） | "五月 raw 与 evaluation 中已保存的 token_usage 属于 provider-reported measured，但同一 MAMR 批次的 usage 被写入三个企业文件，因此汇总时按物理批次只计一次并报告覆盖范围。" |
| 5月 GT-2/GT-1 | completion **reconstructed-imputed**；prompt **partial** | "五月 GT-1/GT-2 的提示词与可见输出可重建，完成 token 依据模型与任务适用性作 reconstructed-imputed 并报告敏感性范围，而提示 token 在完成 GT 专用固定项校准前仅列为 partial。" |
| 5月 GT-0 | **partial** | "GT-0 的 50 次为设计调用数，由于原始输出及完整发送记录未保留，其实际 token 用量和包含失败或重试的物理调用总数未知。" |
| 5月编排者 | **reconstructed-imputed（anchor-based）** | "五月编排阶段的 token 用量依据 1023 同任务调用进行跨期估算，并非五月原生 usage；相同的 prompt 字符数不保证相同的 completion 用量。" |
| 2月试验 | 已证实合成 **N/A**；来源未明 **unknown** | "二月已核实的本地合成生成产物不适用 LLM API token 计量；来源未明、混合补齐及独立 GT 或交互阶段分别列示，不能据此推断二月整体零消耗。" |
| error/pending/null-usage | **unknown** | "error、pending 或 null-usage 不被解释为零消耗；存在原生 usage 的失败调用计入资源账，其余无法计量的已发送或发送状态不明记录保留为 unknown。" |
| MiniMax reasoning=0 | provider 字段 **measured**；reasoning 分解 **unknown** | "MiniMax 原生 reasoning_tokens 零值按原样保留，但鉴于同期存在 reasoning_content，该字段不被解释为无 reasoning，亦不据此另行叠加可能已包含在 completion 中的 token。" |

英文对应措辞见 oracle 导出文件 Q1 节。

### Q2 采用值规则与三条红线

**采用顺序**：① 同一调用的原生 usage 优先 → ② 确定性恢复（从 journal 找回 usage、去除共享 usage 副本；保留原值与变换规则）→ ③ 经适用性说明的估算单列 → ④ 仍不可识别者保留 unknown，**不强行使总表闭合**。

**GT-2 分模型裁定**：

| 对象 | 主表采用 | 情景/附表 |
|---|---|---|
| Kimi GT-2 | 2,135,541 可见字符；**1,060,348 估算可见 completion tokens** | 2.014±0.045 chars/token → **1,037,174–1,084,582**（敏感性范围，**非置信区间**） |
| MiniMax GT-2 | **2,132,512 可见字符**；原生 completion 与隐藏 reasoning **unknown** | Kimi 编码代理 **1,058,844 visible-token-equivalent**；含隐藏思维情景 **3,507,421**（两者相差 2,448,577，**不得命名为上下界**） |

**三条红线**：
1. **不得把缺失或来源未知改写成零，也不得把估算改写成实测。**
2. **不得把校准关系迁移到不同计量对象而不重新验证。** Track A 的 `pt = 0.59031×chars + 1697.3` 中 chars 是 `combined_output`、截距含 Track A 固定模板，不能套 GT 完整 prompt（错误套用得 9,639,810）。须用 `β_model×chars(run_output) + α_GT,model` 或匹配 tokenizer。
3. **不得用不匹配分母、共享副本或任意分摊支撑比较结论。**

另须明确：中文 `chars/4` 在现有核实材料中是**低估 2.55–3.76 倍**（不是高估），且样本量增加不能消除这种系统偏差。

### Q3 11.3× 的处置

**撤回原 11.3283× 作为有效比较结论；主报共同企业产出单位 3.8378×，辅报架构 episode 单位 11.5135×。**

原公式 `(9,303,786/315)/(1,042,908/400) = 11.3283` 同时存在 MAMR 共享 usage 三倍重复计数，与 SASR 分母混入 85 份 nemotron（不同模型）两个问题。

| 比较单位 | SASR | MAMR | MAMR/SASR |
|---|---:|---:|---:|
| 315 个企业产出对应的生成 usage | 808,076 | 3,101,262 | **3.8378×** |
| 每架构 episode | 808,076/315 | 3,101,262/105 | **11.5135×** |

**并置措辞（可直接采用）**：
> 在匹配三种生成模型并去除 MAMR 共享 usage 副本后，MAMR 与 SASR 的已记录生成 token 比在共同企业产出单位下为 3.8378×，在各自架构 episode 单位下为 11.5135×；后者比较一次三企业联合生成与一次单企业生成。两项结果均不含编排摘要、GT 或评估阶段。

加入编排估算后的情景（**须标为含跨期估算的情景结果**）：编排 742,055 → MAMR 生成加编排 3,843,317 → 两条件 4,651,393 → 共同产出比 **4.7561×**、episode 比 **14.2684×**。

### Q4 敏感性分析最小充分集（5 情景）

| 情景 | 假设与数字 | 审稿人最可能挑战 |
|---|---|---|
| **S0 已记录基线** | 匹配模型 + 共享 usage 去重；生成 3,909,338；**3.8378×** / **11.5135×** | 缺失阶段是否改变结论 |
| **S1 加入编排锚点** | 742,055 → 4.7561×；舍入均值版 749,714 / 4.7656× | 跨期迁移；两算法差 7,659 |
| **S2 Kimi 可见 completion 编码敏感性** | 2.014±0.045 → **1,037,174–1,084,582**（中心 1,060,348） | 校准输出是否代表 GT 输出；范围被误当 CI |
| **S3 MiniMax 计量对象敏感性** | 1,058,844 visible-token-equivalent vs **3,507,421** 总 completion 情景，差 2,448,577 | 跨模型编码代理；重复计数 |
| **S4 历史总量与分摊规则的诊断情景** | 旧估算器 25,375,098（区间 23,649,443–26,018,830）、编排 742,055、强制 GT 各半 → 生成+摘要+GT 比 **1.4655×**（1.4436–1.5365×）；含按条件评估 **1.5836×**（1.5651–1.6398×） | GT prompt 截距错误；各半分摊无依据；额外 GLM 评估不平衡 |

**S4 只能作旧结论失效原因的诊断展示，不得进入摘要、主结果或有效区间。** GT-2 字符分布不对半、GT-1 种子为 4:6、GT-0 属共享固定成本。**不存在可辩护的"完整项目总 token 区间"。**

### Q5 交付形态与风险

**净风险判断：主动披露低于保留现有错误口径。** 原 11.3× 的重复计数与分母错配可被独立复算发现；隐去估算身份会让局部错误扩展为整份资源报告的可信度问题。披露围绕三个可检验事实：原比较有什么问题及如何纠正、哪些数值来自原生 usage 哪些来自重建、哪些缺口仍阻止完整项目结论。

**断链引用处置**（`cross-project-roi-2026-07-06.md:223 → draft-0316.md:176`）：先核对该句声称什么 → 涉及 token 的断言改引本次调查证据与最终复现表，缺证据者撤回或标待核 → 改用固定版本链接与表号/证据 ID，避免易漂移行号 → **保留纠错说明**，不要静默换链制造"原本就有依据"的印象。

**最小可复现交付件**（目录 `auto-research/analysis/token-imputation-audit-20261026/`，与 1023/1025 平级，不写回实验目录）：`manifest`、字段级 `call-ledger`、`estimators`+`calibration`、`scenarios`+`summary`、离线 `reproduce`。离线复现须检查：共享 usage 不重复计入、原生小计与源记录一致、真实重试未被哈希折叠、表中比值可由同一 ledger 重算。

### 如果只能改三件事

1. **纠正核心比值及全部派生口径**：撤回 11.3×，主报 **3.8378×**、辅报 **11.5135×**，明确仅含匹配模型的已记录生成 usage。
2. **建立字段级来源账，停止把缺失补成事实**：分开原生值/估算值/unknown；纠正"2月整体零消耗"、"MiniMax 无 reasoning"、"GT prompt 错误外推"三类断言。
3. **交付可离线复现的分层表与敏感性附录并修复引用**：固定编排估算版本；旧完整总量与强制各半结果降为诊断情景；每个最终采用数字可回溯至记录或明确估算式。

## Investigation Log

### Phase 1 - 初始摸底与问题定位
**Hypothesis:** 未记录部分可能通过"同 prompt 跨实验类比"或"字符数→token 比例"估算补齐。
**Findings:** 三类未记录缺口的性质不同：2 月试验缺**全部**计量；5 月实验缺**特定调用类别**的计量；1023/1025 缺**失败终态**的计量。这三类可用完全不同的方法处理。
**Evidence:** 见 Background 小节全部 Green Source 引用。
**Conclusion:** 需要分别评估，不能一概而论。

## Root Cause

"未记录部分能否采用值"这个问题之所以复杂，是因为**"未记录"在本次研究里其实指四种性质完全不同的缺失**，用同一套方法处理必然出错：

1. **计量从未存在（2 月试验）**。`archive/pilot-study-2026-02/` 的产物是本地脚本合成——`batch_generate_gpt4o_p2a_agents.py:27` 用 `prompt_hash = f'sha256:{random.getrandbits(64):x}'` 伪造请求哈希，`mc-2026-02-21/EXECUTION-INSIGHTS.md:28-35` 明说用 Python 补齐，`mc-2026-02-22/scripts/generate_starlink_kimi.py` 亦为脚本生成。**这里没有 API 调用，因此没有 token 可估。** 根因不是"忘了记"，而是"这些数字从来不是模型产生的"。
   - 例外：`mc-2026-02-26/scripts/generate_gt_gpt5mini.py:36-63` 确有真实 OpenAI `requests.post`（且不返回 usage），但代码存在≠执行过；02-19 provenance 未知。

2. **计量存在但被丢弃（5 月 GT 与编排者）**。`gt_pipeline.py:144,150,253,380` 拿到了 usage 却从不落盘；`generate_experiments.py:170` 写成 `landscape, _ = call_model(...)`。根因是**管线设计缺陷**（usage 未纳入持久化契约），而不是数据缺失。

3. **计量存在但被复制（5 月 MAMR）**。`generate_experiments.py:191,207-210,231-241` 把同一份 `total_token_usage` 写进 3 个企业文件，**这不是缺失而是重复**——朴素求和虚增 **3.00 倍**（9,303,786 vs 真值 3,101,262）。原头条 11.3283× 正建立在这个虚增分子上，分母还混入 85 份 nemotron（不同模型）。

4. **计量存在但终态未知（1023/1025 的 error/pending/null-usage）**。这些调用**可能已在服务端计费**，但本地无 usage。根因是失败路径未保留服务端计量，且"null ≠ 0"。

由此产生一个关键区分：
- **2 月不是"缺计量"，而是"没有消耗"** → 正确处理是 **N/A**，不是 0，也不是估算。
- **5 月 GT/编排者缺计量，但调用身份、prompt 材料、输出文本（或跨期锚点）幸存** → 属于**可重建**，但重建的是 **token 估算**，不是"精确重建 token"。
- **5 月 MAMR 与 11.3× 不是缺失问题，是记账问题** → 确定性修正即可，不需要任何估算。

**方法学层面的根因**：此前把 token 记账当作"研究产出的一部分"而非"资源消耗账"，导致 usage 未被纳入持久化契约、共享 usage 未做归属建模、失败路径未保留证据。这使得**在同一份报告里，实测、重复、丢弃、未知四种状态被压平成一个数字**。

## Recommendations

按优先级：

1. **【最紧急，与估算无关】撤回并重算 5 月的 token 比值。** 撤回 11.3283×，主报共同企业产出单位 **3.8378×**、辅报架构 episode 单位 **11.5135×**，并同步修正所有派生指标（`cost_per_effect`、图表、wiki `current-state.md:98` 与 `:142` 的两个口径）。修正 MAMR 共享 usage 的三倍重复计数。**这一步不依赖任何估算，可立即执行。**

2. **【本调查的直接答复】建立五级字段级台账，停止把缺失补成事实。** measured / reconstructed-imputed / partial / not-applicable / unknown 五态落在**字段级**。具体纠正三类错误断言：2 月"整体零消耗"、MiniMax"无 reasoning"、GT prompt 套用 Track A 截距。

3. **【可辩护的采用】GT-2 分模型采用**：Kimi 可见 completion 估算 **1,060,348 tokens**（敏感性 1,037,174–1,084,582，明示为敏感性范围非置信区间）；MiniMax 主表只报 **2,132,512 可见字符**，原生 completion 与隐藏 reasoning 保持 unknown，代理值只进情景表。编排者 **742,055** 标为跨期锚点估算，并解释与舍入均值版 749,714 的 7,659 差额、冻结其中一个版本。

4. **【交付】产出可离线复现的分层包**（`auto-research/analysis/token-imputation-audit-20261026/`）：`manifest` + 字段级 `call-ledger` + `estimators`/`calibration` + `scenarios`/`summary` + 离线 `reproduce`。离线复现须自检：共享 usage 不重复计入、原生小计与源记录一致、真实重试未被哈希折叠、表中比值可由同一 ledger 重算。

5. **【修复】断链引用** `cross-project-roi-2026-07-06.md:223 → draft-0316.md:176`：改引本次调查证据与最终复现表，改用固定版本链接+表号/证据 ID，并**保留纠错说明**。

6. **【敏感性】提交 S0–S4 五情景**，其中 S4（旧总量 25,375,098 与强制各半所得 1.4655×/1.5836×）**仅作诊断展示，不得进入摘要、主结果或有效区间**。

7. **【1023/1025】** 报告须标注快照时间（两者当时均在运行），并按 realpath 去重 1023 的 5 路符号链接；1025 以 journal 为准，`provider-ledger.json` 只有金额不可代替 token。

## Preventive Measures

- **usage 必须进入持久化契约。** 任何调用点若拿到 usage 却未落盘，即为缺陷。建议在调用封装层强制"返回 usage 或显式声明丢弃原因"，并加 CI 检查：管线结束时 usage 覆盖率 < 100% 则失败（允许显式白名单）。
- **共享成本必须显式建模。** MAMR 一次联合生成被写入 3 个企业文件，说明"谁拥有这次消耗"没有定义。建议在数据结构里加 `shared_group_id` + `dedup_key`，并规定汇总时按物理批次只计一次。
- **调用身份与指纹分离。** 1023 的 1,314 个唯一请求对应 1,522 个物理记录，真实重发必须保留。建议 ledger 用 `(call_id, attempt_index, physical_key)` 而非 fingerprint 单键聚合。
- **失败路径与成功路径同等留证。** error/pending 记录必须保留请求体指纹、发送计数、终态时间，缺失 usage 写 null 而非 0；"是否已发送"要有独立字段。
- **provider 上报值原样保留 + 审计标记。** MiniMax 的 `reasoning_tokens=0` 与非空 `reasoning_content` 并存，说明 provider 字段不可轻信也不可改写。建议同时保留原生字段与派生字段，并标记 `reasoning_metering_status`。
- **下游引用必须指向可复算的产物。** 断链引用（`draft-0316.md:176`）与两个并存口径（11.3× vs 11.51×）都源于"数字进了文档但没人能重算"。建议论文中的每个派生数字都附带台账查询路径。
- **未来可重跑的切片，用一次探针调用代替估算。** provider 侧建议 `max_tokens:1` 读 `prompt_tokens`；这是最便宜可靠的估计方式，只对历史归档不可行。
- **估算器必须声明适用域并做跨任务验证。** Track A 拟合（`pt=0.59031·chars+1697.3`，chars=`combined_output`）迁到 GT 会系统性错误。建议估算器规格化：`chars` 的定义（Unicode 码点/可见文本/完整 messages）、校准对象模型与任务、截距归属的模板、隐藏 reasoning 处理、跨任务偏差作为共同系统项单列。
