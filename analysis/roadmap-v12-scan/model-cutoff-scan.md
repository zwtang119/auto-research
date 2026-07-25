# model-cutoff-scan — 世界杯回放实验开源 LLM 训练截止日核查

- 日期：2026-07-22
- 执行者：模型核查子代理
- 目的：为"训练截止日早于 2026-06（最好 ≤2026-03）的开源 LLM 做 2026 世界杯回放预测"选型。判定标准：世界杯回放要求截止日 < 2026-06；跨赛事回放要求截止日尽量早、可验证性尽量强。
- 截止证据类型三档：**语料公开**（训练语料有公开清单/文档，可独立验证）/ **厂家声明**（仅官方模型卡或第三方转引的 cutoff 声明）/ **不可考**（无官方截止日）。

## 1. 候选模型总表

| 模型 | 参数量 | 声明截止日 | 截止证据类型 | 权重链接 | 回放适用性判定 |
|---|---|---|---|---|---|
| **OLMo 3 32B** (Base/Think/Instruct) | 32B dense | 语料按快照公开（Dolma 3 Mix 5.9T tokens，2025-11-20 发布，数据至 2025 年中，可逐源核查） | **语料公开** | https://huggingface.co/allenai/Olmo-3-1125-32B | ✅ 主力候选：唯一可独立验证无 2026 世界杯内容泄露的模型；部署可行（单节点 8×GPU 或量化后更少） |
| OLMo 2 32B Instruct | 32B dense | Dolmino Mix 1124，数据至 ~2024-09/11（[arXiv 2604.15203](https://arxiv.org/html/2604.15203v1) 转引） | **语料公开** | https://huggingface.co/allenai/OLMo-2-0325-32B-Instruct | ✅ 跨赛事回放最佳（截止早 + 语料公开）；能力弱于 OLMo 3 |
| **gpt-oss-120b** | 120B MoE（A5.1B） | 2024-06（[官方模型卡 arXiv:2508.10925](https://arxiv.org/html/2508.10925v1)） | 厂家声明 | https://huggingface.co/openai/gpt-oss-120b | ✅ 主力候选：截止早、余量大；Apache 2.0，单台 80GB GPU 可跑 |
| Qwen3-235B-A22B | 235B MoE（A22B） | 2024-12（[arXiv 2605.06279](https://arxiv.org/pdf/2605.06279) 记载 Qwen3 全系 cutoff Dec 2024） | 厂家声明（第三方论文转引） | https://huggingface.co/Qwen/Qwen3-235B-A22B | ✅ 对照：能力最强的"截止 ≤2024"开源模型之一；部署需多节点 |
| Qwen3-32B | 32B dense | 2024-12（同上） | 厂家声明 | https://huggingface.co/Qwen/Qwen3-32B | ✅ 对照（单机可行档） |
| Llama-3.3-70B-Instruct | 70B dense | 2023-12（[Meta 模型卡/开发者指南](https://www.developersdigest.tech/blog/llama-3-3-70b-guide)，15T tokens） | 厂家声明 | https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct | ✅ 对照：截止最早档，跨赛事回放泄露风险最低；许可为 Llama Community License |
| DeepSeek-V3 | 671B MoE（A37B） | 2024-07（[galaxy.ai 对比页](https://blog.galaxy.ai/compare/deepseek-chat-vs-kimi-k2-5)转引官方；[自报 July 2024](https://www.softwarelitigationconsulting.com/chatgpt-o1-chain-of-thought-examples/)） | 厂家声明 | https://huggingface.co/deepseek-ai/DeepSeek-V3 | ⚠️ 对照：截止合格但 671B 部署成本高；建议走 API/托管量化版 |
| Gemma-3-27B-it | 27B dense | 2024-08（Google 声明；[arXiv 2511.12116](https://arxiv.org/pdf/2511.12116) 实测有效 cutoff ~2024-05） | 厂家声明 | https://huggingface.co/google/gemma-3-27b-it | ✅ 对照：小参数量单机可跑 |
| MiniMax-M1-80k | 456B MoE（A45.9B） | unknown（官方未公布；[llm-stats 对比页](https://llm-stats.com/models/compare/minimax-m1-40k-vs-minimax-m2.1)标注无 cutoff） | 不可考 | https://huggingface.co/MiniMaxAI/MiniMax-M1-80k | ❌ 淘汰：截止日无法证明 |
| MiniMax-M2 | 230B MoE（A10B） | unknown（同上） | 不可考 | https://huggingface.co/MiniMaxAI/MiniMax-M2 | ❌ 淘汰：截止日无法证明 |
| Kimi K2 (0711/0905) | 1T MoE（A32B） | ~2025-03（[arXiv 2512.14754 表](https://arxiv.org/html/2512.14754v1)记 Kimi-K2-0905 cutoff 2025-03；官方未明示） | 厂家声明（弱） | https://huggingface.co/moonshotai/Kimi-K2-Instruct | ⚠️ 世界杯回放勉强合格（<2026-06），但 1T 部署不现实、证据弱；不建议 |
| GLM-4.5 / GLM-4.5-Air | 355B / 106B MoE | "2025"（[crackedaiengineering 转引](https://www.crackedaiengineering.com/ai-models/zhipuai-coding-plan-glm-4-5-flash)，模糊） | 厂家声明（模糊） | https://huggingface.co/zai-org/GLM-4.5 | ⚠️ 证据太模糊，不满足可验证性要求 |
| GLM-5 / GLM-5.1 | 744B / 754B MoE（A40B） | 2025-11（[llmreference 对比页](https://www.llmreference.com/compare/glm-5/qwen3.5-397b-a17b)） | 厂家声明 | https://huggingface.co/zai-org/GLM-5（MIT） | ❌ 淘汰（世界杯回放）：截止 2025-11 距 2026-06 仅 7 个月且证据弱；不满足"≤2026-03 留余量"的偏好 |
| DeepSeek-V4-Pro / V4-Flash | 1.6T / 284B MoE | late 2025（[mindstudio](https://www.mindstudio.ai/blog/deepseek-v4-open-source-frontier-model)；2026-04-24 发布） | 厂家声明 | https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro（MIT） | ❌ 淘汰（世界杯回放）：余量过薄 + 仅厂家声明 |
| Kimi K2.5 | 1T MoE | unknown（官方未公布；[llm-stats](https://llm-stats.com/models/compare/kimi-k2.5-vs-gpt-5.5)标注未指定；2026-01-27 发布，~15T tokens 续训，[GitHub](https://github.com/MoonshotAI/Kimi-K2.5)） | 不可考 | https://huggingface.co/moonshotai/Kimi-K2.5 | ❌ 淘汰：2026 年发布、训练至 2025 年底的可能性高，且无法证明 |
| Qwen3.5 全系（含 Tsinghua 用的 Qwen3.5-122B-A10B） | 9B–397B | unknown（[llmreference](https://www.llmreference.com/compare/deepseek-v4-flash/qwen3.5-9b)标注无 cutoff；2026-02/03 发布） | 不可考 | https://huggingface.co/Qwen（Qwen3.5 系列，Apache 2.0） | ❌ 淘汰：2026 年发布且无截止日声明，无法排除 2026 年语料 |
| Mistral Small 3.1 / Large 系 | 24B–123B | 官方从未公布；第三方转引 Small 3.1 ~2024-06（[anotherwrapper](https://anotherwrapper.com/tools/llm-pricing/mistral-small-31/pixtral-large-2411)，非官方） | 不可考（仅第三方转引） | https://huggingface.co/mistralai/Mistral-Small-3.1-24B-Instruct-2503 | ❌ 淘汰：无官方截止日 |
| Xiaomi MiMo-7B（开源档） | 7B dense | unknown | 不可考 | https://huggingface.co/XiaomiMiMo/MiMo-7B-RL | ❌ 淘汰：无截止日声明 |

补充说明（闭源 API 模型，按实验设计排除）：GPT-5-mini（cutoff 2024-05）、Gemini-3-flash 等仅 API、权重不可得，不属于"开源 LLM"候选；出处 [arXiv 2509.23694 表 5](https://arxiv.org/html/2509.23694v1)。

## 2. Tsinghua 项目（policysim-research-Tsinghua）模型清单

来源：`/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua/config/experiment-config.yaml`（主配置，OpenAI 兼容接口，经 OpenRouter / paratera / DeepSeek / DashScope / MiniMax / Moonshot / 智谱 / 小米 / token-plan 九家供应商）及各实验脚本。

**生成器（generators）**
- `gpt-oss-120b`（openai/gpt-oss-120b:free，OpenRouter）— config/experiment-config.yaml:37
- `deepseek-v4-flash`（DeepSeek-V4-Flash，paratera）— :48
- `qwen3.5-122b`（Qwen3.5-122B-A10B，paratera）— :53
- `nemotron-3-super`（nvidia/nemotron-3-super-120b-a12b）— 已弃用（2026-05-06，截断+英文泄露），:42
- 备选：`glm-4.5-air`（z-ai/glm-4.5-air:free）、`hy3-preview`（tencent/hy3-preview:free）— :59, :64

**GT 标注 / 裁判（judges）**
- `minimax-m2.7`（MiniMax-M2.7，paratera）— :70
- `kimi-k2.5`（Kimi-K2.5，paratera）— :75
- `glm-5.1` / `glm-5.1-coding`（GLM-5.1，paratera / 智谱 coding 端点）— :80, :85
- `deepseek-v4-pro`（DeepSeek-V4-Pro，paratera）— :90
- `deepseek-v3.2`（DeepSeek-V3.2，paratera）— :95
- `mimo-v2.5-pro`（小米 MiMo，小米端点）— :100
- `kimi-k2.6`（token-plan）、`qwen3.6-plus`（token-plan）— :105, :110（锦标赛新模型，model-benchmark/scripts/tournament.py:626-627）

**论文撰写实验（paper-writing/experiments/mc-2026-02-23，另一批）**
- 生成器：GLM-5、Kimi、GPT-5-mini（generate_final_report.py:41-47）
- 质检/仲裁：MiniMax-M2.5（主）、Gemini-3-flash（副）（arbitration_analysis.py:289-290）

**对本实验的相关性**：Tsinghua 用的主力生成器/裁判（DeepSeek-V4 系、Qwen3.5-122B、GLM-5.1、Kimi-K2.5、MiniMax-M2.7）全部是 2025 末–2026 代模型，截止日 2025-11 或不可考——做政策仿真无碍，但直接搬来做世界杯回放**全部不合格或不可证明**（见上表淘汰档）。唯一现成合格的是 gpt-oss-120b（截止 2024-06）。

## 3. 选型建议（三档）

- **主力**：**OLMo 3 32B**（唯一语料公开、可独立证伪泄露的模型；Dolma 3 全量清单在 https://github.com/allenai/dolma3）+ **gpt-oss-120b**（截止 2024-06、余量 24 个月、单机可部署）。两者分别覆盖"可证明性最强"与"能力/部署平衡"两个极点；世界杯回放与跨赛事回放均合格。
- **对照**：**Qwen3-32B / Qwen3-235B**（截止 2024-12，能力档参考）、**Llama-3.3-70B**（截止 2023-12，最早截止档，适合跨赛事回放的保守基线）、**Gemma-3-27B**（截止 2024-08，小模型档）。
- **淘汰**：GLM-5/5.1、DeepSeek-V4 系、Kimi K2/K2.5/K2.6、Qwen3.5/3.6 系、MiniMax M1/M2/M2.5/M2.7、Mistral 全系、MiMo——原因均为截止日 ≥2025-11 余量过薄、或截止日不可考/仅模糊声明，无法满足"截止日可证明 < 2026-06"的实验前提。

## 4. 核查方法与局限

- 第一步：Grep/Glob 检索 Tsinghua 仓库（只读），模型清单以 `config/experiment-config.yaml` 为准，脚本内出现的型号逐一核对。
- 第二步：WebSearch 核实截止日；优先采用官方模型卡/arXiv 技术报告，其次 llmreference/llm-stats 等聚合站（已在表中注明转引层级）。
- 局限：llmreference/llm-stats 为第三方聚合站，其 cutoff 字段未给出官方出处时本表一律降级为"厂家声明（弱）"或"不可考"；GLM-5.1 的 2025-11、DeepSeek-V4 的 late-2025 均未能定位到官方模型卡原文，复核时建议直接查 HuggingFace 模型卡。未能找到官方截止日的字段已标 unknown，未做任何推断填充。
