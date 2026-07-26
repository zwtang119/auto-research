# Investigation: Tsinghua 主力模型训练截止日可证明性复核 + 单模型充分性评估

> 日期：2026-07-22
> 触发：用户挑战 `analysis/roadmap-v12-scan/model-cutoff-scan.md` 的两条结论——(1) "Tsinghua 主力模型截止日不可考"可能不对，OpenRouter 等渠道应有资料；(2) 若 (1) 不成立，单跑 gpt-oss-120b 是否足够。要求证据优先、独立判断、不迎合。

## Summary

Q1 复核：用户的 OpenRouter 直觉有事实基础（OpenRouter 自 2026-04 起确有 `knowledge_cutoff` API 字段，342 个模型中 164 个有值），但对 Tsinghua 五个主力模型该字段全部为 null，且 HuggingFace 官方模型卡、arXiv 技术报告、官方博客均未见截止日记载——前次核查"不可考"结论**维持，且证据升级**（从"未找到"升级为"官方渠道系统性空白"）。Q2：单跑 gpt-oss-120b 不足以支撑 Paper B 的群体性结论；最小可信配置为 2 个模型（gpt-oss-120b + OLMo 3 32B），第 3 个（Llama-3.3-70B）为成本可选项。复核同时修正前次两处错误：OLMo 3 官方截止实为 2024-12（更早更有利）；Qwen3-32B 的 2024-12 无官方依据，对照档除名。

## 问题陈述（Symptoms）

- Q1：DeepSeek-V4-Pro/Flash、GLM-5.1、Qwen3.5-122B-A10B、Kimi-K2.5、MiniMax-M2.7 五个 Tsinghua 主力模型的训练数据截止日，是否存在**官方来源**（HuggingFace 官方组织模型卡 / arXiv 技术报告 / 官方文档 / OpenRouter 页面）的明确记载？前次核查（model-cutoff-scan.md）将 GLM-5.1（2025-11）与 DeepSeek-V4（late 2025）标为"仅第三方聚合站、未定位官方模型卡"，Qwen3.5 标为"无公开截止日"——该结论需复核。
- Q2：若 Q1 不成立，Paper B 实验只跑 gpt-oss-120b 单模型是否足以支撑结论？是否有必要跑 3 个模型？
- Q3（衍生）：前次核查采用"截止日 ≤2026-03 留余量"的偏好淘汰了截止 2025-11 的模型——该偏好对"回放 2026-06 后赛事"是否过度保守？（截止日早于开赛即无结果泄露；余量大小影响的是赛前信息新鲜度，不是污染。）

## Background / Prior Research

- 前次核查：`analysis/roadmap-v12-scan/model-cutoff-scan.md`（2026-07-22，含候选表与三档建议；其"局限"节自认 GLM-5.1 / DeepSeek-V4 截止日未定位官方模型卡原文）。
- Tsinghua 项目模型清单：`policysim-research-Tsinghua/config/experiment-config.yaml`（生成器 gpt-oss-120b / DeepSeek-V4-Flash / Qwen3.5-122B-A10B；裁判 MiniMax-M2.7 / Kimi-K2.5 / GLM-5.1 / DeepSeek-V4-Pro 等）。
- 待核查假设：
  - H1：OpenRouter 模型页面对上述模型给出训练截止日 → 若真，前次核查"不可考"结论错误。
  - H2：HuggingFace 官方组织（deepseek-ai / zai-org / Qwen / moonshotai / MiniMaxAI）模型卡或配套 arXiv 技术报告载明截止日 → 若真，证据等级从"第三方聚合"升为"厂家声明（官方模型卡）"。
  - H3：即使 H1/H2 为真，证据性质仍是"厂家声明"而非"语料公开可证伪"——对实验前提的影响需分级评估。

## Investigator Findings

**复核代理 A（`analysis/roadmap-v12-scan/cutoff-recheck-a.md`，2026-07-22）**

| 模型 | 官方截止日 | 核查渠道 | 证据等级 |
|---|---|---|---|
| DeepSeek-V4-Pro/Flash | 无 | HF 官方模型卡 + arXiv:2606.19348 技术报告 PDF 全文（grep `cutoff` 0 命中）+ OpenRouter | 仅第三方（"late 2025"无官方佐证） |
| GLM-5.1 | 无 | HF 模型卡 + z.ai 博客 + docs.z.ai + GLM-5 报告 arXiv:2602.15763 全文 | 仅第三方（"2025-11"无官方佐证） |
| Qwen3.5-122B-A10B | 无 | HF 模型卡 + qwen.ai 博客 + arXiv 旁证 | 不可考（Qwen3.5 无 arXiv 报告） |
| OpenRouter 元问题 | — | OpenRouter `/models` API（2026-04 起有 `knowledge_cutoff` 字段，342 模型中 164 个有值，多为闭源厂商自报） | 上述 4 条目该字段全部 `null`，网页端不展示 |

**复核代理 B（`analysis/roadmap-v12-scan/cutoff-recheck-b.md`，2026-07-22）**

| 条目 | 结论 | 证据等级 |
|---|---|---|
| Kimi-K2.5 / K2 | 无官方截止日；第三方说法互相矛盾（2025-01 vs 2025-06-30） | 不可考 |
| MiniMax-M2.7 / M2 / M2.5 | 无官方截止日（HF 卡、minimax.io、OpenRouter 均无） | 不可考 |
| gpt-oss-120b | **2024-06**，arXiv:2508.10925 原文 "Our model has a knowledge cutoff of June 2024." | 官方模型卡声明 |
| OLMo 3 32B | 语料公开属实（Dolma 3 可无限制下载、构建代码公开）；**官方卡 "Date cutoff: Dec 2024"**（修正前次"2025 年中"之误，更早更有利） | **语料公开** |
| Qwen3-32B | "2024-12"无官方出处（卡/报告/博客均无） | 降级为仅第三方——**对照档除名** |
| Llama-3.3-70B | **2023-12**，Meta 官方 HF 模型卡原文确认 | 官方模型卡声明 |

## Investigation Log

### Phase 1.5 - 官方渠道截止日核查
**Hypothesis:** H1 OpenRouter 可提供 Tsinghua 主力模型截止日；H2 HF 官方卡/arXiv 报告载明截止日。
**Findings:** H1 部分成立（OpenRouter 确有该字段）但对目标模型全为 null；H2 对五个 Tsinghua 主力模型全部不成立；对 gpt-oss-120b / OLMo 3 / Llama-3.3-70B 成立。
**Evidence:** cutoff-recheck-a.md / cutoff-recheck-b.md（含逐项 URL 与原文引句）。
**Conclusion:** 前次核查"Tsinghua 主力模型截止日不可考"**确认**；"≤2026-03 余量偏好"属过度保守（Q3）：截止日早于开赛（2026-06）即无结果泄露，余量只影响赛前信息新鲜度，不构成淘汰理由——但五模型仍因"不可考"出局，理由从"余量薄+证据弱"收紧为"证据不存在"。

## Root Cause / 结论

1. **Q1（用户挑战）不成立但方向有理**：OpenRouter 确实在 2026-04 后成为截止日信息渠道（用户直觉有事实基础），但它只是厂商自报字段的搬运工——对不公布截止日的开源模型同样空白。五个 Tsinghua 主力模型经 HF 官方卡 + arXiv 技术报告全文 + 官方博客 + OpenRouter 四路核查，截止日**系统性缺席**。结论：这批模型不能用于回放实验，与前次判定一致，证据强度升级。
2. **Q2（单模型充分性）**：不足以支撑论文结论，理由三条（见下）。但 3 个也非必需——最小可信配置为 2 个。
3. **前次扫描两处修正**：OLMo 3 官方截止 2024-12（非 2025 年中，更有利）；Qwen3 全系截止日无官方依据，从对照档除名，由 Llama-3.3-70B 递补。

## Recommendations

1. **回放实验底座终选**：
   - 主力对：**gpt-oss-120b**（官方卡 2024-06，能力强，单机可跑）+ **OLMo 3 32B**（语料公开可证伪，官方截止 2024-12）——分别覆盖"能力档"与"可证明性金标准"，且分属 OpenAI / Ai2 两家族；
   - 可选第三：**Llama-3.3-70B**（Meta 官方 2023-12，第三家族）——预算允许时加入，支撑"跨家族稳健"句式；
   - 淘汰：DeepSeek-V4 系 / GLM-5.1 / Qwen3.5 系 / Kimi K2 系 / MiniMax 全系（截止日官方不可考）；Qwen3 系（对照档除名，截止日仅第三方）。
2. **B0 启动前**：对入选模型在 HuggingFace 官方模型卡页面存档截屏/链接，作为预注册附件（证据固定）。
3. **写作纪律**：论文中凡涉截止日的表述按三级证据分级引用——"语料公开可证伪"（OLMo）/"官方模型卡声明"（gpt-oss、Llama）/"不可考故排除"（其余），不得混用。
4. 路线图 v1.5 更新时以本报告为准替换 model-cutoff-scan.md 的三档表（含两处修正）。

---

## 追加调查（2026-07-22 第二轮）：Nemotron 系列 + 四厂官方文档终查

### Findings（Nemotron 核查，`analysis/roadmap-v12-scan/cutoff-recheck-c.md`）

| 型号 | 参数量 | 官方截止日（HF nvidia 官方卡原文） | 证据等级 | 回放判定 |
|---|---|---|---|---|
| **Nemotron-3-Nano-30B-A3B** | 30B MoE（A3B） | 预训练 2025-06-25 / 后训练 2025-11-28 | **官方卡声明 + 语料公开**（Nemotron-CC 系列含快照号，gated 需审批） | ✅ 对照档首选（与 OLMo 3 同证据级，第三家族 NVIDIA） |
| Nemotron-3-Super-120B-A12B | 120B MoE（A12B） | 预训练 2025-06 / 后训练 2026-02 | 官方卡声明 + 语料公开 | ✅ 备选主力（gpt-oss-120b 同档，部署 8×H100 或单 B200 NVFP4） |
| Nemotron-3-Ultra-550B-A55B | 550B MoE | 预训练 2025-09 / 后训练 2026-05 | 官方卡声明 | ❌ 不入选（距开赛仅 1 个月余量 + 单机不可行） |
| Nemotron-H-56B | 56B | 2024-09 | 官方卡声明 | ⚠️ 研发许可限制，慎用 |

注：Tsinghua 曾用的 nemotron-3-super 系 OpenRouter 免费端点（弃用原因是 60% 截断质量问题，与截止日无关）。

### Findings（四厂终查，`analysis/roadmap-v12-scan/cutoff-recheck-d.md`）

Qwen3.5-122B-A10B / DeepSeek-V4 系 / MiniMax-M2.7 / Kimi-K2.5：官方渠道穷尽（HF 模型卡 README 全文、官方 GitHub 仓库、官方文档站全站、arXiv 技术报告全文含 K2.5 报告 arXiv:2602.02276 与 K2 报告 arXiv:2507.20534），**均无截止日记载，维持"不可考"判定，无推翻**。四家已不存在"未翻开的官方文本"。

### 修订后的选型表（v1.5 以此为准）

- **主力对**：gpt-oss-120b（官方卡 2024-06）+ OLMo 3 32B（语料公开，2024-12）；
- **对照**：**Nemotron-3-Nano-30B**（官方卡 + 语料公开，2025-06/2025-11；NVIDIA 家族）+ Llama-3.3-70B（Meta 官方卡 2023-12）；
- **备选主力**：Nemotron-3-Super-120B（证据强于 gpt-oss 的卡声明级，部署成本高）；
- **淘汰**：DeepSeek-V4 系 / GLM-5.1 / Qwen3.5 系 / Kimi K2 系 / MiniMax 全系 / Nemotron-3-Ultra（余量过薄）/ Qwen3 系（仅第三方）。
