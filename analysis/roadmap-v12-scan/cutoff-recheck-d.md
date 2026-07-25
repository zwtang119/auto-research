# 四家模型训练截止日终查（复核 D：官方完整文档补漏轮）

- 日期：2026-07-22
- 执行者：四厂终查代理
- 背景：复核 A（`cutoff-recheck-a.md`）与复核 B（`cutoff-recheck-b.md`）已核查 HF 模型卡与 arXiv 报告，四家（Qwen3.5-122B-A10B / DeepSeek-V4 系 / MiniMax-M2.7 / Kimi-K2.5）均未找到官方训练截止日。本轮按用户要求补查前一轮未覆盖或未穷尽的**官方文档站、官方 GitHub 仓库、HF 模型卡完整正文、官方技术博客**，确认无遗漏。
- 方法：HF 模型卡一律抓取 `raw/main/README.md` 全文（非渲染页元数据）grep `cutoff` / `cut-off` / `knowledge` / `training data` / `data up to` / `训练数据` / `截至` / `corpus` / `pretrain` 等关键词；官方文档站先枚举 sitemap 再逐页核对相关页面；官方技术报告取 arXiv HTML 全文 grep（含 `freshness` / `up to 20XX` / `through 20XX` / `until 20XX` / `as of 20XX` 变体）；第三方聚合站一律不作定论依据。
- 证据等级四档：语料公开 / 官方模型卡或文档声明 / 仅第三方 / 不可考。

---

## 1. Qwen3.5-122B-A10B（Qwen/Qwen3.5-122B-A10B）

**最终结论：官方渠道穷尽未找到 → 不可考。维持前一轮判定。**

本轮查过的渠道（全部无 cutoff）：

- HF 模型卡**完整正文**（raw README，92,633 字节）：唯一与训练相关的字段是 `Training Stage: Pre-training & Post-training`（第 44 行）；`knowledge` 仅命中评测表 "Knowledge" 分类行；**连预训练 token 数都未写**，更无数据时间范围。
- 官方 GitHub `QwenLM/Qwen3.5` 仓库 README（raw，11,768 字节）：grep 0 命中；News 节仅指向 `qwen.ai/blog?id=qwen3.5`；**仓库内无技术报告 PDF**（确认 Qwen3.5 无 arXiv 报告，唯一官方文本即发布博客）。
- 官方博客 <https://qwen.ai/blog?id=qwen3.5>：客户端渲染（CSR），正文不可直接抓取；前一轮已通过阿里云官方转载页 <https://www.alibabacloud.com/blog/qwen3-5-towards-native-multimodal-agents_602894> 核对全文，无截止日字段。本轮复核渲染方式未变。
- ModelScope 官方模型页 <https://modelscope.cn/models/Qwen/Qwen3.5-122B-A10B>（阿里官方渠道）：页面 JS 渲染，原始 HTML（141 KB）grep `cutoff/截止/训练数据` 0 命中。
- 前一轮已查（不重复计）：HF 卡 grep、OpenRouter API `knowledge_cutoff: null`。

**证据等级：不可考。**
**2026-06 后赛事回放判定：不可用**——无任何官方来源可证明 cutoff < 2026-06。

---

## 2. DeepSeek-V4-Pro / DeepSeek-V4-Flash（deepseek-ai/DeepSeek-V4-Pro）

**最终结论：官方渠道穷尽未找到 → 仅第三方（"late 2025" 一说无官方对应记载）。维持前一轮判定。**

本轮查过的渠道（全部无 cutoff）：

- HF 模型卡**完整正文**（raw README，13,149 字节）：`knowledge` 仅命中三处评测表分类行；与训练数据相关的唯一原文仍为：
  > "We pre-train both models on more than **32T** diverse and high-quality tokens…"
  无时间边界。
- 官方文档站 api-docs.deepseek.com：枚举 sitemap 全部约 60 个 URL；逐页核对首页/快速开始、**V4 发布新闻页** <https://api-docs.deepseek.com/news/news260424>（"DeepSeek V4 Preview Release"，2026-04-24，正文仅述参数规模与 API 用法）、**Change Log** <https://api-docs.deepseek.com/updates>（含 2026-04-24 V4 条目，仅述模型名与弃用计划）——全部无 cutoff/训练数据时间字样。
- 官方 GitHub：枚举 deepseek-ai 组织全部仓库（GitHub API）——**不存在 DeepSeek-V4 仓库**（最新模型仓库止于 DeepSeek-V3.2-Exp / DeepSeek-OCR-2 等）；V4 无官方 GitHub 渠道可查。
- 前一轮已查（不重复计）：arXiv:2606.19348 技术报告 PDF 全文 grep 0 命中（§4.1 仅称"在 V3 语料之上扩充"）；OpenRouter API `knowledge_cutoff: null`。

**证据等级：仅第三方**（官方模型卡/技术报告/文档站/新闻页全部沉默）。
**2026-06 后赛事回放判定：不可用**——无法以官方来源证明 cutoff < 2026-06。

---

## 3. MiniMax-M2.7（MiniMaxAI/MiniMax-M2.7，附 M2 / M2.5）

**最终结论：官方渠道穷尽未找到 → 不可考。维持前一轮判定。**

本轮查过的渠道（全部无 cutoff）：

- HF 模型卡**完整正文**（raw README，14,902 字节）：grep 0 命中（全文为能力/评测/部署说明）。
- 官方 GitHub（枚举 MiniMax-AI 组织全部仓库后逐个核对）：
  - `MiniMax-AI/MiniMax-M2.7` README（raw，6,444 字节）：0 命中；
  - `MiniMax-AI/MiniMax-M2.5` README（raw，20,087 字节）：无 cutoff（仅一处 "tacit knowledge" 描述办公场景数据构建，与时间范围无关）；
  - `MiniMax-AI/MiniMax-M2` README（raw，13,318 字节）：0 命中。
- 开发者文档站 platform.minimaxi.com：枚举 sitemap 全部约 70 个 URL，模型相关仅 <https://platform.minimaxi.com/docs/guides/models-intro>（语言模型列表页，无 cutoff 字段）；**不存在 M2.7 专属文档页**，其余为 API 参考/计费/工具页。
- 官网 minimax.io：新闻列表 <https://www.minimax.io/news> 无 M2.7 发布稿（仅有 hailuo-23 / speech-28 条目）；M2.7 唯一官方产品页 <https://www.minimax.io/models/text/m27> 前一轮已核对全文，无 cutoff。
- 第三方说法（互相矛盾、均无出处，不可采信）：llm-bento 称 "Training Data: Up to early 2026"（<https://www.llm-bento.com/models/minimax/minimax-m27/>）；llm-stats 标注 "not specified"。
- 前一轮已查（不重复计）：OpenRouter 模型页无 cutoff。

**证据等级：不可考（官方）；第三方仅有无出处且互相矛盾的猜测。**
**2026-06 后赛事回放判定：不可用**——无公开截止日，无法证明 cutoff < 2026-06。

---

## 4. Kimi-K2.5（moonshotai/Kimi-K2.5，附 Kimi K2）

**最终结论：官方渠道穷尽未找到 → 不可考。维持前一轮判定；并关闭复核 B 遗留的两项局限。**

本轮查过的渠道（全部无 cutoff）：

- HF 模型卡**完整正文**（raw README，40,082 字节）：与训练相关的唯一原文仍为：
  > "…built through continual pretraining on approximately 15 trillion mixed visual and text tokens atop Kimi-K2-Base."
  其余 `knowledge` 命中均为评测表分类行。无时间边界。
- 官方 GitHub `MoonshotAI/Kimi-K2.5` README（raw master，33,956 字节）：0 命中。
- 官方技术博客 <https://www.kimi.com/blog/kimi-k2-5>（"Kimi K2.5 Tech Blog: Visual Agentic Intelligence"，468 KB 全文抽取后 grep）：0 命中。
- 官方文档站：platform.moonshot.cn 现跳转 platform.kimi.com；枚举 sitemap 后逐页核对**模型参数参考页** <https://platform.kimi.com/docs/api/models-overview>（kimi-k3/k2.7-code/k2.6/k2.5 参数对比表，仅上下文窗口与采样参数）与快速开始页——全部无 cutoff/知识截止字段。
- **Kimi K2.5 技术报告 arXiv:2602.02276 HTML 全文**（463 KB）：grep `cutoff` / `cut-off` / `freshness` / `up to 20XX` / `through 20XX` / `until 20XX` / `as of 20XX` —— **0 命中**。→ 关闭复核 B 局限 #1（"技术报告藏有 cutoff 的可能性未归零"）：现已归零。
- **Kimi K2 技术报告 arXiv:2507.20534 HTML 全文**（577 KB）：同样 0 命中。K2 的 "2025-03" 维持仅第三方定性（复核 B 已降级）。
- 第三方说法（互相矛盾，不可采信）：puter.com "Jan 2025"；arXiv:2604.18576 附录 "2025-06-30"（均无出处）。
- 前一轮已查（不重复计）：OpenRouter 模型页无 cutoff。

**证据等级：不可考。**
**2026-06 后赛事回放判定：不可用**——无公开截止日，无法证明 cutoff < 2026-06。

---

## 汇总表

| 模型 | 官方截止日 | 证据等级 | 本轮新增查证的官方渠道 | 可否用于 2026-06 后回放 |
|---|---|---|---|---|
| Qwen3.5-122B-A10B | 未公布 | 不可考 | HF raw README 全文、QwenLM/Qwen3.5 仓库、ModelScope 官方页、qwen.ai 博客（CSR，经镜像核对） | 否 |
| DeepSeek-V4-Pro / V4-Flash | 未公布 | 仅第三方 | HF raw README 全文、api-docs 全站 sitemap + V4 新闻页 + Change Log、GitHub 组织枚举（确认无 V4 仓库） | 否 |
| MiniMax-M2.7 | 未公布 | 不可考 | HF raw README 全文、M2.7/M2.5/M2 三个 GitHub 仓库、platform.minimaxi.com 全站 sitemap、minimax.io 新闻列表 | 否 |
| Kimi-K2.5 | 未公布 | 不可考 | HF raw README 全文、GitHub 仓库、kimi.com 官方技术博客、platform.kimi.com 文档站、K2.5 报告（arXiv:2602.02276）与 K2 报告（arXiv:2507.20534）HTML 全文 | 否 |

## 与前两轮的关系

- **无推翻**：四家"官方无 cutoff"的结论全部维持；Qwen3.5（不可考）、DeepSeek-V4（仅第三方）、MiniMax-M2.7（不可考）、Kimi-K2.5（不可考）的定性不变。
- **关闭的遗留局限**：复核 B 局限 #1（K2.5 技术报告未通读）与 #4（MiniMax 平台文档未全站核查）均已关闭；另确认 DeepSeek-V4 无官方 GitHub 仓库、MiniMax 官网无 M2.7 发布稿、Qwen3.5 无技术报告 PDF——即四家已不存在"尚未翻开的官方文本"。
- 未决残余（低概率，如实标注）：qwen.ai 博客为客户端渲染，正文经阿里云官方镜像核对而非原页直读；ModelScope 页面同为 JS 渲染，以原始 HTML grep 代替全文通读。两处若藏有 cutoff 声明的可能性极低（所有同源文本均无），但不为零。

## 核查方法备注

- 原始抓取件存于 `/tmp/cutoff-d/`（临时目录，含四家 HF raw README、GitHub raw README、arXiv HTML、各文档站页面）；如需复核可重新按本文 URL 抓取。
- 所有 grep 均在完整正文（非渲染摘要）上进行；命中行已逐条人工核对语义，排除评测表 "Knowledge" 分类等伪命中。
