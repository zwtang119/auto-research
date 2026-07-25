# 三个 2026 代开源模型训练数据截止日官方来源复核（复核代理 A）

- 日期：2026-07-22
- 执行者：截止复核代理 A
- 范围：DeepSeek-V4-Pro / DeepSeek-V4-Flash、GLM-5.1、Qwen3.5-122B-A10B；外加 OpenRouter 是否提供 training cutoff 的元问题。
- 方法：只采信官方来源（HuggingFace 官方组织模型卡 → 官方技术报告（arXiv/官方博客/官方文档站）→ OpenRouter 官方 API/页面 → 官方 GitHub）。技术报告 PDF 已下载全文并 grep `cutoff` / `cut-off` / `data up to` / `as of 20xx` 等关键词。第三方聚合站一律不作证据。

---

## 1. DeepSeek-V4-Pro 与 DeepSeek-V4-Flash

**结论：未找到官方来源记载训练数据截止日。**

查过的官方页面：

- HuggingFace 官方模型卡 <https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro>（V4-Pro 与 V4-Flash 共用同一模型卡，Flash 页面同源）：全文无截止日。与训练数据相关的唯一原文：
  > "We pre-train both models on more than **32T** diverse and high-quality tokens, followed by a comprehensive post-training pipeline."
- 官方技术报告 arXiv:2606.19348（"DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence"，v1 提交 2026-04-26，<https://arxiv.org/abs/2606.19348>）：PDF 全文下载后 grep `cutoff` / `cut-off` / `knowledge cut` / `data up to` / `as of 20` / `until 20` / `through 20` —— **0 命中**。§4.1 Data Construction 仅有：
  > "On top of the pre-training data of DeepSeek-V3, we endeavor to construct a more diverse and higher-quality training corpus with longer effective contexts."
  即只说"在 V3 语料之上扩充"，未给时间边界。
- OpenRouter 官方 API（`https://openrouter.ai/api/v1/models`，2026-07-22 实查）：`deepseek/deepseek-v4-pro` 与 `deepseek/deepseek-v4-flash` 的 `knowledge_cutoff` 字段均为 `null`。
- 官方 GitHub（github.com/deepseek-ai，模型卡所引 inference/encoding 仓库）：未见截止日声明。

前次核查的 "late 2025" 说法：本次未在任何官方来源找到对应记载，维持"仅第三方"定性。

**证据等级判定：仅第三方**（官方模型卡、技术报告、OpenRouter、GitHub 全部沉默）。

**2026-06 后赛事回放判定：不可用**——无法以官方来源证明 cutoff < 2026-06。

---

## 2. GLM-5.1

**结论：未找到官方来源记载训练数据截止日。**

查过的官方页面：

- HuggingFace 官方模型卡 <https://huggingface.co/zai-org/GLM-5.1>：全文无截止日；仅指向官方博客与 GLM-5 技术报告：
  > "📖 Check out the GLM-5.1 [blog](https://z.ai/blog/glm-5.1) and GLM-5 [Technical report](https://arxiv.org/abs/2602.15763)."
- 官方博客 <https://z.ai/blog/glm-5.1>：全文（含全部脚注）无截止日，只有 benchmark 与能力描述。
- 官方技术报告 arXiv:2602.15763（"GLM-5: from Vibe Coding to Agentic Engineering"，v1 2026-02-17 / v2 2026-02-24，注意该报告是 **GLM-5** 的报告，GLM-5.1 无独立技术报告）：PDF 全文 grep `cutoff` / `cut-off` 等 —— **0 命中**。
- 官方文档站 <https://docs.z.ai/guides/llm/glm-5.1>：模型规格页仅有 Context Length 200K、Maximum Output Tokens 128K、模态、能力列表与调用示例，**无 knowledge/training cutoff 字段**。
- OpenRouter 官方 API（2026-07-22 实查）：`z-ai/glm-5.1` 的 `knowledge_cutoff` 为 `null`。
- 官方 GitHub（github.com/zai-org/GLM-5，模型卡所引）：未见截止日声明。

前次核查的 "2025-11" 说法：本次未在任何官方来源找到对应记载，维持"仅第三方"定性。

**证据等级判定：仅第三方**（官方全部沉默；且 GLM-5.1 连独立技术报告都没有，可引的官方文本比 DeepSeek-V4 更少）。

**2026-06 后赛事回放判定：不可用**——无法以官方来源证明 cutoff < 2026-06。

---

## 3. Qwen3.5-122B-A10B

**结论：未找到官方来源记载训练数据截止日；前次核查"无公开截止日"成立。**

模型确切名称已定位为 `Qwen/Qwen3.5-122B-A10B`（Apache-2.0，image-text-to-text，122B 总参 / 10B 激活，262K 上下文）。

查过的官方页面：

- HuggingFace 官方模型卡 <https://huggingface.co/Qwen/Qwen3.5-122B-A10B>：README 全文下载后 grep `cutoff` / `cut-off` / `technical report` / `arxiv` —— **0 命中**。模型卡唯一的文献引用是博客而非论文：
  > `@misc{qwen3.5, title = {{Qwen3.5}: Towards Native Multimodal Agents}, author = {{Qwen Team}}, month = {February}, year = {2026}, url = {https://qwen.ai/blog?id=qwen3.5}}`
- 官方博客 <https://qwen.ai/blog?id=qwen3.5>：页面为客户端渲染，正文无法直接抓取；但旁证（多篇 arXiv 论文的参考文献条目，如 arXiv:2604.02022、arXiv:2604.00886 均将 Qwen3.5 引为 "Qwen Team. Qwen3.5: Towards native multimodal agents, February 2026. URL https://qwen.ai/blog?id=qwen3.5"）确认 **Qwen3.5 没有 arXiv 技术报告**，唯一官方文本即该博客。阿里云官方转载页 <https://www.alibabacloud.com/blog/qwen3-5-towards-native-multimodal-agents_602894> 亦无截止日字段。
- OpenRouter 官方 API（2026-07-22 实查）：`qwen/qwen3.5-122b-a10b` 的 `knowledge_cutoff` 为 `null`。
- 区分说明：Qwen3 系（arXiv:2505.09388，2025-05）模型卡/报告同样未在正文写截止日，但 Qwen3 时代官方对外有 "2024-12" 口径（前次核查已录）；该口径**不适用于 Qwen3.5 系**（2026-02 发布的新一代，预训练必然更新），不可移植引用。

**证据等级判定：不可考**（官方既无模型卡声明，也无技术报告可查；连第三方都没有形成一致说法）。

**2026-06 后赛事回放判定：不可用**——无公开截止日，无法证明 cutoff < 2026-06。

---

## 元问题：OpenRouter 模型页面是否提供 training cutoff 信息？

**结论：机制上有，但这 3 个模型（4 个条目）全部为空。**

- 官方博客 [April Release Spotlight](https://openrouter.ai/blog/announcements/april-release-spotlight/)（2026-04-30）明确宣布：
  > "**Knowledge cutoff dates.** LLM training cutoff dates are now available in the `/models` API, so you can programmatically check how current a model's knowledge is."
- 2026-07-22 实查 `https://openrouter.ai/api/v1/models`（342 个模型）：
  - 164 个模型填了 `knowledge_cutoff`（多为闭源厂商，如 `openai/gpt-5.5 -> 2025-12-01`、`x-ai/grok-4.20 -> 2025-09-01`、`google/gemini-3.5-flash -> 2025-01-01`）；
  - **本次核查的 4 个条目全部为 `null`**：`deepseek/deepseek-v4-pro`、`deepseek/deepseek-v4-flash`、`z-ai/glm-5.1`、`qwen/qwen3.5-122b-a10b`。API 返回原文（以 V4-Pro 为例）：`"knowledge_cutoff": null, "expiration_date": null`。
- OpenRouter 模型网页（如 <https://openrouter.ai/deepseek/deepseek-v4-pro> 及 compare 页）实际展示的字段为：Context length、Reasoning、Input/Output modalities、Providers、Pricing（input/output/cached input）、Benchmarks（Design Arena ELO、Artificial Analysis 指数）——**页面未展示 cutoff 字段**（与 API 中该字段为 null 一致）。

含义：OpenRouter 只能反映厂商自行上报的 cutoff；对不公布截止日的开源模型，OpenRouter 同样是空白，不能作为补位证据。

---

## 汇总表

| 模型 | 官方截止日 | 证据等级 | 官方 URL | 可否用于 2026-06 后回放 |
|---|---|---|---|---|
| DeepSeek-V4-Pro / V4-Flash | 未公布（"late 2025" 仅第三方） | 仅第三方 | 模型卡+报告均无（arXiv:2606.19348 全文 0 命中） | 否 |
| GLM-5.1 | 未公布（"2025-11" 仅第三方） | 仅第三方 | 模型卡/博客/docs.z.ai/GLM-5 报告（arXiv:2602.15763）均无 | 否 |
| Qwen3.5-122B-A10B | 无公开截止日 | 不可考 | 模型卡无、无 arXiv 报告（仅博客 qwen.ai/blog?id=qwen3.5） | 否 |
