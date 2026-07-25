# cutoff-recheck-b — 模型训练截止日外部事实核查（复核 B）

- 日期：2026-07-22
- 执行者：截止复核代理B
- 复核对象：`analysis/roadmap-v12-scan/model-cutoff-scan.md`（前次核查，下称"前次"）
- 来源优先级：HuggingFace 官方组织模型卡 → 官方技术报告/arXiv → OpenRouter 模型页 → 官方 GitHub；第三方聚合站一律不作为定论依据。
- 证据等级四档：**语料公开**（训练语料有公开清单/可下载，可独立验证）/ **官方模型卡声明**（官方页面或官方技术报告明示 cutoff）/ **仅第三方**（只有聚合站或第三方论文转引）/ **不可考**（无任何来源）。

---

## 1. Kimi-K2.5（moonshotai/Kimi-K2.5）

**结论：官方未公布训练数据截止日 → 不可考。前次淘汰判定维持。**

查过的官方页面（逐一核对全文，均无 cutoff 字段）：

- HF 官方模型卡 <https://huggingface.co/moonshotai/Kimi-K2.5>：仅称 "built through continual pretraining on approximately 15 trillion mixed visual and text tokens atop Kimi-K2-Base"，全文无 knowledge cutoff / data cutoff 字样。卡上注明技术报告为 arXiv:2602.02276（Kimi K2.5: Visual Agentic Intelligence）。
- 官方 GitHub <https://github.com/MoonshotAI/Kimi-K2.5>：与 HF 卡同文，无 cutoff。
- OpenRouter 模型页 <https://openrouter.ai/moonshotai/kimi-k2.5>：页面只有路由/价格/用量信息，无 cutoff。

第三方说法（互相矛盾，不可采信）：

- puter.com 开发者页称 "knowledge cutoff date of Jan 2025"（<https://developer.puter.com/ai/moonshotai/kimi-k2.5/>，无出处）；
- 第三方论文 arXiv:2604.18576 附录称 "Kimi-K2.5 (knowledge cutoff 2025-06-30)"（未给出处）；
- llm-stats 标注 "not specified"；therouter.ai 标注 "Training data cutoff: Not publicly disclosed"。

**附：Kimi K2 复核**（前次记 "~2025-03，厂家声明（弱）"，依据第三方论文 arXiv:2512.14754）：

- HF 官方模型卡 <https://huggingface.co/moonshotai/Kimi-K2-Instruct> 全文无 cutoff（仅 "Pre-trained a 1T parameter MoE model on 15.5T tokens"）。
- 官方渠道均无截止日；前次的 2025-03 仅第三方论文转引 → 降级为**仅第三方**；就实验前提（截止日可证明 < 2026-06）而言与"不可考"等效，淘汰判定维持。

**证据等级判定：不可考（K2.5）；仅第三方（K2 的 2025-03）。**

---

## 2. MiniMax-M2.7（MiniMaxAI/MiniMax-M2.7，附 M2 / M2.5）

**结论：M2.7 / M2.5 / M2 官方均未公布训练数据截止日 → 不可考。前次对 M2 的"不可考"判定维持，并扩展确认至 M2.5、M2.7。**

查过的官方页面（逐一核对全文，均无 cutoff 字段）：

- HF 官方模型卡 <https://huggingface.co/MiniMaxAI/MiniMax-M2.7>：全文为能力/评测/部署说明，无训练数据时间范围、无 cutoff。
- MiniMax 官方产品页 <https://www.minimax.io/models/text/m27>（2026-07-21 更新）：同样无 cutoff。
- OpenRouter 模型页 <https://openrouter.ai/minimax/minimax-m2.7>：仅简介与路由信息，无 cutoff。
- HF 官方模型卡 <https://huggingface.co/MiniMaxAI/MiniMax-M2.5>：无 cutoff（有 RL 训练细节，但无预训练数据时间范围）。
- HF 官方模型卡 <https://huggingface.co/MiniMaxAI/MiniMax-M2>：无 cutoff。

**证据等级判定：不可考（M2 / M2.5 / M2.7 全系列）。**

---

## 3. gpt-oss-120b（复核前次"截止 2024-06"）

**结论：确认。前次结论成立，证据等级维持"官方模型卡声明"。**

- 官方模型卡 arXiv:2508.10925（gpt-oss-120b & gpt-oss-20b Model Card, OpenAI, 2025-08-05）原文：
  > "Our model has a knowledge cutoff of June 2024."
  - HTML 版：<https://arxiv.org/html/2508.10925v1>；PDF 版 <https://arxiv.org/pdf/2508.10925> 同句（两处独立检索均命中该原句）。
- HF 官方模型卡 <https://huggingface.co/openai/gpt-oss-120b> 本身未重复 cutoff 数字，仅回引 arXiv 模型卡（"Model card" 链接指向 arXiv:2508.10925）。

**证据等级判定：官方模型卡声明（2024-06）。**

---

## 4. OLMo 3 32B（allenai/Olmo-3-1125-32B，复核"语料公开 + 数据至 2025 年中"）

**结论：语料公开属实且强于前次记载；但"数据至 2025 年中"未获官方支持——官方模型卡明示 "Date cutoff: Dec 2024"。前次的截止时间细节被推翻（实际官方声明更早），"语料公开"判定确认。**

- HF 官方模型卡 <https://huggingface.co/allenai/Olmo-3-1125-32B> 原文：
  > "These models are trained on the Dolma 3 dataset. We are releasing all code, checkpoints, and associated training details."
  > "Date cutoff: Dec 2024"（Model Description 节）
  卡内逐阶段列明语料：Stage 1 `dolma3_mix-5.5T-1125`（5.50T tokens）、Stage 2 `dolma3-dolmino-mix-1125`（2×100B）、Stage 3 `dolma3-longmino-mix-1125`（100B）。
- Ai2 官方博客 <https://allenai.org/blog/olmo3>（2025-11-20）原文：
  > "Olmo 3 is pretrained on Dolma 3, a new ~9.3-trillion-token corpus… From this pool, we construct Dolma 3 Mix, a 5.9-trillion-token (~6T) pretraining mix…"
  > "we're making every training and fine-tuning dataset available for download without any license restrictions"
- 官方 GitHub <https://github.com/allenai/dolma3> 原文：
  > "This repository contains descriptions and code necessary for reconstructing the Dolma 3 datasets."（含 Dolma 3 Mix / Dolmino / Longmino 三个数据集的构建说明与代码）
- 对"语料逐源可核查"的判定：**属实**——数据集本身可无限制下载、构建代码与配比公开，且 Ai2 提供 OlmoTrace 回溯工具；这是候选中唯一达到"语料公开"档的模型。
- 推翻点：前次"数据至 2025 年中"在官方页面中找不到任何依据，且与官方卡的 "Date cutoff: Dec 2024" 直接冲突；应以官方卡为准（截止 2024-12，比前次记载更早，对回放实验更有利）。

**证据等级判定：语料公开（官方卡另明示 Date cutoff: Dec 2024）。**

---

## 5. Qwen3-32B（复核 2024-12）与 Llama-3.3-70B（复核 2023-12）

### 5a. Qwen3-32B —— 前次结论被推翻：官方无 cutoff 声明，2024-12 仅第三方转引

- HF 官方模型卡 <https://huggingface.co/Qwen/Qwen3-32B>：全文无 cutoff（仅 "Training Stage: Pretraining & Post-training"）。
- 官方技术报告 arXiv:2505.09388（Qwen3 Technical Report）：数据章节只述 "36 trillion tokens""119 languages and dialects" 及三阶段预训练流程，无数据时间范围（经 Stanford CRFM 透明度报告 <https://crfm.stanford.edu/fmti/December-2025/company-reports/Alibaba_FinalReport_FMTI2025.html> 逐段转录其数据章节核对）。
- 官方博客 <https://qwenlm.github.io/blog/qwen3/>：无 cutoff。
- 独立学术佐证（官方未公布）：
  - arXiv:2605.21491 附录 B.2："For Qwen3 … an official pretraining knowledge cutoff is not publicly documented."
  - OpenReview 论文（id=91SrFSFNki）："No official knowledge-cutoff date for Qwen-3 is reported."
- 前次依据 <https://arxiv.org/pdf/2605.06279>（第三方 cs.SE 论文，模型 cutoff 对比表）记 "Qwen3 全系 cutoff Dec 2024"：该文 HTML 版 404，PDF 可见片段仅称所测模型 "Knowledge cutoff spans April 2024 to January 2026"，未能核到 "Qwen3 = Dec 2024" 的原文落点；即便存在，也属第三方转引而非官方声明。
- 另有第三方调研（metehan.ai, 2026-07）指出 Qwen 维护者公开表示模型自报 cutoff 不可靠。

**证据等级判定：仅第三方（2024-12 一说）；官方层面不可考。** 相比前次的"厂家声明"**降级**——前次把第三方论文转引当成了准官方证据。注：此推翻影响前次总表中 Qwen3-235B-A22B 一行（同一来源）。

### 5b. Llama-3.3-70B-Instruct —— 前次结论确认，且来源升级为官方模型卡

- Meta 官方 HF 模型卡 <https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct> 原文：
  > "Knowledge cutoff: December 2023"（Model Information 表）
  > "Data Freshness: The pretraining data has a cutoff of December 2023."（Training Data 节）
  > "Llama 3.3 was pretrained on ~15 trillion tokens of data from publicly available sources."
- 前次引用的是第三方博客（developersdigest.tech），本次已在 Meta 官方卡找到原文，来源升级。

**证据等级判定：官方模型卡声明（2023-12）。**

---

## 6. 复核结论汇总与对前次文件的修正建议

| 模型 | 截止日 | 证据等级 | 官方 URL | 与前次差异 |
|---|---|---|---|---|
| Kimi-K2.5 | 未找到 | 不可考 | 查过 HF 卡/GitHub/OpenRouter 均无 | 维持（淘汰） |
| MiniMax-M2.7 | 未找到 | 不可考 | 查过 HF 卡/minimax.io/OpenRouter 均无 | 维持（淘汰）；M2/M2.5 同步确认不可考 |
| gpt-oss-120b | 2024-06 | 官方模型卡声明 | arxiv.org/abs/2508.10925 | 维持，确认无误 |
| OLMo 3 32B | 2024-12（官方卡 "Date cutoff: Dec 2024"） | 语料公开 | huggingface.co/allenai/Olmo-3-1125-32B | **推翻**"数据至 2025 年中"（官方声明更早）；语料公开确认 |
| Qwen3-32B | 2024-12 仅第三方；官方未公布 | 仅第三方（降级） | 官方卡/技术报告/博客均无 | **推翻**前次"厂家声明"：无官方依据 |
| Llama-3.3-70B | 2023-12 | 官方模型卡声明 | huggingface.co/meta-llama/Llama-3.3-70B-Instruct | 维持，来源由第三方博客升级为官方卡 |

**对选型结论的影响**：主力二选一（OLMo 3 32B + gpt-oss-120b）不变且 OLMo 3 证据更强；对照档中 Qwen3 系的截止日应视为"不可证明"，若实验前提要求"截止日可证明 < 2026-06"，Qwen3-32B/235B 只能作能力参考、不能作截止合规证据；Llama-3.3-70B 的 2023-12 现有官方卡原文背书，可作为最早截止档的保守基线。

## 7. 核查方法与局限

- 方法：WebSearch 定位官方页面 → FetchURL 抓取 HF 官方组织模型卡、官方博客、官方 GitHub、OpenRouter 模型页全文，人工核对是否含 cutoff 字段；官方技术报告经 arXiv 页面与第三方逐段转录（Stanford CRFM）交叉核对。
- 局限：
  1. Kimi K2.5 技术报告 arXiv:2602.02276 全文未逐页通读（HF 卡/GitHub/发布博客均无 cutoff，技术报告藏有 cutoff 声明的可能性低但未归零）。
  2. arXiv:2605.06279 仅 PDF 可读，"Qwen3 cutoff Dec 2024" 的表格落点未能逐格核到原文；不影响"非官方来源"的定性。
  3. Qwen3 技术报告数据章节经 Stanford CRFM 转录核对，未逐页通读原 PDF。
  4. MiniMax 未另查 platform.minimax.io 开发者文档全站（模型卡与产品页均无 cutoff，平台文档记载训练数据时间范围的可能性低）。
