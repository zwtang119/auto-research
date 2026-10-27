# 1023 DNA 消融：报告层数据适配器设计（方案，未实施）

日期：2026-10-26；作者：gpt-6-astra（只读调研 + 方案）。状态：**仅方案，未实施**。
父计划：`docs/plans/tsinghua-dna-ablation-2026-10-23.md`（PDF/HTML 交付目标见 `:123`、`:147`）。
本方案不修改、不写入 `analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023/`（该目录由另一执行会话正在写入）。

## 0. 定位与非目标

**目标**：把已冻结的"生成输出 + 三评委评分 + 原始调用记录"组装成 630 份人类可读的单样本报告（HTML+PDF）与汇总统计，且**不重新调用任何模型、不改写任何判定、不丢失任何原始留痕**。

非目标（硬边界）：

- 不新增/重跑任何模型调用；不"修复"任何评分。
- 不把思考内容当作判定依据；思考只作过程留痕。
- 不虚构 GT；本次无 GT，报告不出现 GT 栏位。
- 不写回运行目录；适配器只读运行目录，产物写到新分析副本。

实施位置（待批准后建立）：`analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/`，自带 `CHANGELOG.md`；产物在其 `out/` 下。

## 1. 输入清单（Green Source：本轮实测）

| 用途 | 路径 | 规模 | 已验证 |
|---|---|---|---|
| 冻结生成输出 | `D-dna-ablation-20261023/runs/formal/raw-data/{SASR,MAMR}/{model}/{enterprise}/run_XXX.yaml` | 630 | 各评分目录 `inputs/` 副本与之逐文件 SHA-256 相同 |
| GLM 评分 | `glm-adaptive-v7/glm-5.1/evaluation/` | 339（持续增长） | `input_sha256` 全部与冻结输入匹配 |
| Kimi 评分 | `sasr-scoring-v3/kimi-k2.5/evaluation/`（SASR 315）＋`mamr-scoring-v1/kimi-k2.5/evaluation/`（MAMR 315） | 630 | 同上 |
| MiniMax 评分 | `minimax-scoring-v1/evaluation/` | 630 | 同上 |
| 原始调用（含完整 prompt / 响应 / 思考 / usage） | 各 `*/calls/*.json` | GLM 286+、Kimi 430、MiniMax 630 | — |
| 技术替代映射 | 各 `*/adoption.json`、`*/adoptions/*.json` | 6 处 | logical↔physical、original/replacement 哈希齐全 |

冻结参考件在 `D-dna-ablation-20261023/frozen/`（`config/experiment-config.yaml`、`protocol/40-effect-list-v2.yaml`、`scripts/score_track_b.py` 等）。

## 2. 规范键（canonical key）

目标：`{condition}|{model}|{enterprise}|{run_id:03d}|{judge}`，`condition ∈ {SASR, MAMR}`。

实测三种原生键：

| 评委 | 原生键示例 | 字段可用性 |
|---|---|---|
| GLM / Kimi | `SASR\|deepseek-v4-flash\|ISPACE\|9\|glm-5.1` | evaluation 内已含 `condition/model/enterprise/run_id/judge` |
| MiniMax | `minimax-m2.7/SASR/deepseek-v4-flash/ISPACE/run_002` | 同样含上述字段，仅 `key` 写法不同 |

规则：**以 evaluation 内的结构化字段为准重建 canonical key，不解析 `key` 字符串**；`run_id` 统一零填充到 3 位，与 `run_XXX.yaml` 对齐。重建后必须与冻结输入路径一一对应（315×2 全覆盖），否则报错退出。

## 3. 采用集去重（最容易出错的地方）

GLM 存在 6 个 evaluation 目录，构成**继承链**而非独立批次。实测重叠：v7∩v6=336、v5∩v4=66、v3∩v2=18、v4∩v2=18、v6∩v5=88。

规则：

1. 采用集 = **最新权威目录**（当前 `glm-adaptive-v7/glm-5.1/evaluation/`）的全量；其余目录只作历史留痕。
2. **禁止把各目录文件数相加**（会得到 323→339 这类重复计数）。
3. 同一 canonical key 在多个目录出现时，必须**逐字节比对 evaluation 内容**；不一致即报错并列出冲突。当前实测无冲突，此断言需固化进适配器。

## 4. 技术替代（tech01）处理

6 处映射给出 `logical_key ↔ physical_key` 与 `original/replacement` 路径、哈希、规则（"sole tech01; 原错误保留; 不再 tech02"）。

报告规则：

- 展示的是 **replacement 的响应**（该样本的唯一采用结果）。
- original 的失败类型与"服务端终态未知"必须作为**诊断标签显式呈现**，不得隐藏或静默合并。
- 物理请求数 ≠ 逻辑采用数，差额必须能被 tech01 映射逐条解释。

## 5. 思考原文归一化

| 来源 | 字段 | 实测覆盖率与长度 |
|---|---|---|
| Paratera（GLM / MiniMax / 部分生成） | `message.reasoning_content` | GLM 264/264，均 47,309 字符（最大 120,061）；MiniMax 630/630，均 1,833 |
| OpenRouter（Kimi） | `message.reasoning` ＋ `reasoning_details` | SASR 90/115、MAMR 92/315，均 3.3k–4.3k 字符 |
| 生成侧 | `reasoning_content` 与 `reasoning` 并存 | MAMR 385 / 799 份 |

规则：**按 provider 取字段，禁止写死单一字段名**；缺失即记"该次未返回思考"，不臆造、不用其他来源替代。

## 6. 已知缺口（必须显式呈现）

1. **MiniMax 2 份解析为空**（`SASR/qwen3.5-122b/ISPACE/run_032`、`SASR/qwen3.5-122b/SPACETIMETECH/run_014`）：`scores` 为空对象，按协议保留不重抽。报告须显示"该评委本次未给出五维评分"，不计入均值、不做填补。
2. **GLM evaluation 无 `raw_response`**：适配器从对应 `calls/*.json` 的 `response.choices[0].message.content` **原样补写**（只加字段，不动 `judgments`/`effect_counts`），使三评委结构一致、PDF 有统一原文入口。
3. **本次无 GT**：不设 GT 栏位；如需 GT，另立标注验证方案，不在本报告内。

## 7. 输出物

- 每样本一份 report bundle JSON（键、来源路径与哈希、完整 prompt、可见输出、思考原文、评分结构、诊断标签）。
- 每样本一份 HTML + PDF（Kami `long-doc` 中文模板）。
- 汇总：主表（父计划口径：SO+TO 与 Track B，四组：有/无 DNA × MAMR/SASR × 三生成模型）、差值与预先规定的 bootstrap 区间（10000 次，PCG64 seed=20261023，两期独立抽样、按既定格整批重采样）；不作原论文主检验的重写。

## 8. Kami 落地

- 模板：中文 `long-doc`（单样本内容多段，one-pager 不适用）；PDF 经 WeasyPrint。
- 流程：`build.py --check-content content.json` → 填模板 → `build.py --deliver filled.html content.json` 直至 READY → 逐页看图验收。
- 字体：先 `--doctor` 与 `ensure-fonts.sh`；中文衬线必须**实际绘制 CJK 字形**（缺字不报错，只会让版面变重）。
- 不能看图时，结论必须写"构建通过、视觉未确认"。
- 批量一致性：先做 **3 份样张**（SASR×1、MAMR×2，覆盖三评委）走通全流程并锁定版式，再批量。

## 9. 关键取舍：思考放哪

GLM 单份思考均值 47,309 字符（≈12k token）。全量塞进正文会让每份 PDF 膨胀到 20+ 页。

| 分层 | 内容 |
|---|---|
| 正文 | 完整 prompt、可见输出、25 条 judgment（含置信度与理由）、效应计数、诊断标签、来源键与哈希 |
| 附录（默认折叠） | 思考原文；`--with-reasoning` 生成全文版 |

默认交付折叠版；需要全量留痕时另出一套，不与默认版混放。

## 10. 验收门槛（全部从冻结数据复算）

1. 630 个输入 × 3 评委 = 1,890 条 canonical key，无重复、无缺漏。
2. 采用数：GLM 630、Kimi 630、MiniMax 630。
3. 物理请求数与逻辑采用数的差额，逐条由 6 处 tech01 ＋ 3 笔 GLM 物理错误（1 超时、2×429）＋2 份 MiniMax 空解析解释，无其他未解释项。
4. 每条 evaluation 的 `input_sha256` 与冻结输入哈希一致（实测当前 339/315/630 全部通过）。
5. 同一 canonical key 在多目录的 evaluation 内容逐字节一致。
6. 所有进入报告的数字由冻结数据复算，禁止转引项目自评文档。
7. PDF：页数符合合同、无占位符残留、CJK 字形由中文字体绘制、逐页视觉抽检通过。

## 11. 工期（供排期，非承诺）

| 阶段 | 估计 |
|---|---|
| 适配器实现 + 校验（含 §10 全部断言） | 3–5 小时 |
| 3 份样张 + Kami 版式锁定 + 视觉验收 | 1–2 小时 |
| 630 份批量生成（bundle→HTML→PDF，含抽检） | 1.5–2 小时 |
| 汇总统计与主表 | 1–2 小时 |
| **合计** | **约 6–9 小时，可与 GLM 评分并行** |

## 12. 风险与表述边界

- **等 GLM 跑完再做全量**：适配器可先实现、先用已冻结部分试制；全量批量必须在 GLM 630/630 冻结后启动。
- **长文本排版**：47k 字符思考的折叠/分页/孤行需样张验证，必要时拆附录页。
- **无 GT 的表述边界**：报告与摘要须把结论限定为"原评价口径下的描述性消融结果"，不表述为 DNA 的因果效应量。
- **跨期混杂**：五月有 DNA 与本次无 DNA 来自不同期次，差值须标注为跨期比较，不作因果归因。
- **数字纪律**：任何进入报告的统计量保留复算脚本与种子。

## 13. 待用户裁定

1. 是否批准在 `analysis/tsinghua-baseline-audit-20261022/report-adapter-20261026/` 建立实施副本（只读运行目录）。
2. 思考默认折叠版即可，还是同时交付 `--with-reasoning` 全文版（体积显著增大）。
3. GT 验证子集是否与本报告并行准备（会新增一轮标注调用与费用）。
