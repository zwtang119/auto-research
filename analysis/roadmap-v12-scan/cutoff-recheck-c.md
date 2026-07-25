# 截止日复核 C：NVIDIA Nemotron 家族（2026-07-22 实查）

核查范围：Nemotron 3 系列（Nano / Super / Ultra）、Nemotron-H、Nemotron-CC 语料，及 Tsinghua 项目已弃用的 `nemotron-3-super`。来源全部为 HuggingFace `nvidia` 官方组织模型卡原文 + NVIDIA 研究页，2026-07-22 实查。

## 家族成员表

| 型号 | 参数量 | 官方截止日（原文引句） | 证据等级 | 语料公开情况 | 权重链接 | 回放适用性判定 |
|---|---|---|---|---|---|---|
| Nemotron-3-Nano-30B-A3B-BF16 | 30B / 3.5B active（Mamba2-Transformer Hybrid MoE） | 预训练 **2025-06-25**；后训练 2025-11-28。模型卡原文："The post-training data has a cutoff date of November 28, 2025. The pre-training data has a cutoff date of June 25, 2025." | **官方模型卡声明 + 语料公开**（最高档） | 预训练语料主体发布于 Nemotron-Pre-Training-Datasets collection（CC 快照号明示：CC-MAIN-2013-20 至 CC-MAIN-2025-13；多语 2024-51/2025-08/2025-18）；样本集免申请，其余需 gated 审批 | https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16 | **适用**。cutoff 2025-06-25 < 2026-06；单机 H100/A100-80GB 可跑 BF16；NVIDIA Nemotron Open Model License 可商用 |
| Nemotron-3-Super-120B-A12B-BF16 | 120B / 12B active（LatentMoE + MTP，NVFP4 预训练） | 预训练 **2025-06**；后训练 2026-02。模型卡原文："The post-training data has a cutoff date of February 2026. The pre-training data has a cutoff date of June 2025."（数据集收集期至 2026-02-24） | **官方模型卡声明 + 语料公开** | 同 Nano：Nemotron-3 Foundation 语料（Nemotron-CC-v2/v2.1 9.13T、CC-Code-v1、Pretraining-Code 等）公开列名；后训练主体在 Nemotron-Post-Training-v3 collection（部分 gated） | https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16 | **适用但有条件**。cutoff < 2026-06 成立；BF16 最低 8×H100，单机不可行；NVFP4 变体（NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4）可单 B200/DGX Spark。注意后训练合成数据由 Kimi-K2.5/DeepSeek-V3.2 等 2026 年教师模型生成，知识污染面延至 2026-02，但距 2026-06 赛事仍有 4 个月安全边 |
| Nemotron-3-Ultra-550B-A55B-BF16 | 550B / 55B active | 预训练 **2025-09**；后训练 **2026-05**。模型卡原文："The post-training data has a cutoff date of May 2026. The pre-training data has a cutoff date of September 2025." | **官方模型卡声明**（语料称随模型开源，技术报告 https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Ultra-Technical-Report.pdf） | 基础语料同 Nemotron 3 Foundation（CC-v2/v2.1 等）；后训练含 GPT-5.5、DeepSeek-V4-Pro、"Nemotron 5.5" 等教师合成数据 | https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-BF16 | **不入选**。cutoff 虽仍 < 2026-06（2026-05，仅 1 个月安全边，过紧）；最低 8×B200 或 16×H100，标准实验室单机不可行；2026-06-04 才发布，OpenMDW-1.1 许可 |
| Nemotron-H-56B-Base-8K（另有 47B/8B） | 56B dense（Hybrid Mamba-Transformer） | 预训练 **2024-09**。模型卡原文："The pretraining data has a cutoff date of September 2024." | **官方模型卡声明** | 未公开语料（模型卡仅描述混合来源） | https://huggingface.co/nvidia/Nemotron-H-56B-Base-8K | **可用但价值低**。cutoff 最干净（2024-09）；但 base 模型、8K 上下文、NVIDIA Internal Scientific R&D 许可（仅研发用）；仅适合作为"老 cutoff 架构对照"，非主力 |
| Nemotron-CC（语料，非模型） | —（6.3T token 英文 CC 精选；v2/v2.1 至 9T+） | 语料自带 CC 快照号（v1: CC-MAIN-2013-20 ~ 2024-30；Nemotron 3 用 v2/v2.1 延伸至 CC-MAIN-2025-13），时间可证 | **语料公开**（HF gated：datasets/nvidia/Nemotron-CC 未登录返回 401，需申请；论文 arXiv:2412.11795） | 即 NVIDIA 公开语料传统的代表；Nemotron-CC-v2/v2.1/CC-Code-v1/CC-Math-v1 均在 HF `nvidia` 组织下发布（部分 gated） | https://huggingface.co/datasets/nvidia/Nemotron-CC | 作为"cutoff 可证明"的加分项：Nemotron 3 全系语料成分与快照号公开，第三方可复核 |

## Tsinghua 项目用过的 nemotron-3-super（已弃用）

- 配置：`config/experiment-config.yaml:45`，model_id `nvidia/nemotron-3-super-120b-a12b:free`（OpenRouter 免费端点）——即上表 **Nemotron-3-Super-120B-A12B 的 2026-03 新版**，不是旧 Llama-3.1-Nemotron-Super-49B。
- 弃用原因与 cutoff 无关：`experiments/mc-2026-05-05/PROGRESS.md:35` 记"60% 截断是模型本身问题（冗长输出风格）"，`docs/10-methodology/50-methodology-disclosure.md:106` 记"60% 截断 + 英文泄露，数据不可用，Phase 0 即弃用"。即弃用是免费端点输出质量问题，不构成对该模型 cutoff 资质的否定。

## 关键事实补充

- 发布节奏：Nano 2025-12-15（arXiv:2512.20848）→ Super 2026-03-11 → Ultra 2026-06-04（NVIDIA 研究页 https://research.nvidia.com/labs/nemotron/Nemotron-3/ 与 HF 模型卡一致）。
- 三款 Nemotron 3 均声明"Alongside the model, we release our final pre-training and post-training data"，但除样本集外均需 gated 审批（许可为 permissive、限训练用途）——语料公开属实但非完全免申请。
- 后训练合成数据的教师模型名单在模型卡全量披露（Nano/Super 含 gpt-oss-120b、Qwen3 系、DeepSeek-R1-0528、Kimi-K2/K2.5 等；Ultra 延伸至 GPT-5.5、DeepSeek-V4-Pro），为污染分析提供了罕见的官方清单。

## 一句选型建议

**建议入选 Nemotron-3-Nano-30B-A3B（BF16 版）入"对照档"**：与 OLMo 3 32B 同参数量级、同为官方卡声明 cutoff + 语料公开的最高证据等级，cutoff 2025-06-25 比 OLMo 3 的 2024-12 新半年、又比 Super 的 2026-02 干净，且单机 80GB 卡可跑，可作为"新架构（Hybrid Mamba-MoE）× 中等 cutoff"对照臂；Super 120B 可作 gpt-oss-120b 的同档备选主力（证据等级更高但部署成本 8×H100 或单 B200 NVFP4，且需向实验组书面说明其 2026-02 后训练面），Ultra 因部署与安全边双不合格不入选。
