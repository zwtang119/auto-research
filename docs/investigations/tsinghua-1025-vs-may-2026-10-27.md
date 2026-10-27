# 调查：1025八臂实验与五月实验的现象及可能解释

日期：2026-10-27；协调：OpenCode gpt-6.1-sol。状态：调查完成；父直接复核通过，机制仍有未识别部分。

## Summary

**结论：多轮处理包的总体增量最稳定；MA主要表现为竞争意识、其他质量维度及模型之间的权衡；显式DNA没有跨结构一致的正增益。五月到1025的MAMR评分上升，但评委与模型服务发生变化，不能将其归因为系统能力进步或DNA作用。**

从冻结逐样本数据复算五月630样本和1025修订360样本。父独立核对990样本、11880个指标字段、40组均值、24个主移除差和90对SR实际请求，全部通过；区间另直接复跑调查脚本，不冒称父独立编写bootstrap。只读既有实验与发布包，不新增实验模型调用，不修改既有统计规则。

## Symptoms

- 五月仅SASR/MAMR有DNA；1025为同期SA/MA×SR/MR×DNA/NoDNA八臂，不能直接把跨期差当DNA效应。
- 1025已有原available-case与13重评+1格式修复补充修订两套结果，须明确版本。
- 需要核对多轮优势、MA与DNA条件依赖、模型异质性，以及五月与十月基线变化。

## Background / Prior Research

本题优先使用仓库冻结数据与实际请求/协议；当前无需外部检索。对模型服务漂移只作待验证解释，不以外部知识替代逐请求证据。

## Investigator Findings

以下为pair逐样本调查；父复核范围和限制见文末。

### 2026-10-27 独立逐样本复算（调查交付；不替代原正式统计）

**结论先行。** 两期都观察到同 DNA 的 MAMR 高于 SASR；1025 同期八臂中，MR 是总体上最稳定的正增量，MA 则表现为高阶效应计数增加、但 B 总分接近抵消的维度/模型权衡，DNA 不呈现普遍正增益。五月到1025的 MAMR 上升主要集中于 DeepSeek、其次 Qwen 的 B；GPT 的 B 几乎不变。**不能据跨期变化归因 DNA、模型升级、cap 放宽或单一长度机制。** 以下明确区分“直接观察”“协议支持解释”“未验证假说”。

#### F0. 版本、来源和复算口径

为避免长路径歧义，本节引用前缀如下；`I/foo:line` 等均表示下表完整路径加后缀及行号。

| 前缀 | workspace 相对路径 |
|---|---|
| `I/` | `analysis/tsinghua-1025-vs-may-20261027/` |
| `F/` | `analysis/tsinghua-factorial-ablation-20261025/` |
| `O/` | `analysis/tsinghua-factorial-ablation-20261025/supplementary-scoring-20261027/offline-statistics/` |
| `H/` | `analysis/tsinghua-baseline-audit-20261022/historical-acceptance-20261027/verified-01/` |
| `D/` | `analysis/tsinghua-baseline-audit-20261022/dna-final-20261027/statistics/history-001/` |
| `M/` | `analysis/tsinghua-baseline-audit-20261022/D-dna-ablation-20261023/frozen/` |

- **来源标记**：输入文件身份、请求记录、离线算术核验为 **Green Source**；生成文本、LLM 评分及其所有均值/差值/区间为 **Red Source**，不是现实政策效果或人工 ground truth。下列数值表统一继承本段 Red Source 标记：五月冻结 commit `1fab155a7ec77b275e9340263ea659c684a4b6ef`；1025 补充修订冻结 payload SHA-256 `b3ed4dda001f6093502b6236cf4cd80178be294335c3e4d52a449b6a087d0f9e`。版本记录见 `H/authority.json:3-13`、`O/provenance.json:1`；后者逐项列出13重评、1格式修复以及1066份不变有效评分。
- **五月主源不是1023实验结果**：按 `H/formal630.csv` 和 `H/evaluation_bindings.csv` 选取历史归档的630份原生成、1890份原评分，核对 ZIP member hash、归档 hash，并逐对象确认属于 `D/period-input.json` 的 `original_evaluations`。工程 ZIP SHA 为 `93e87d41de8d63c3efe38343d079709a87b0968470b6e5b540f1bcdab07482b8`，数据 ZIP SHA 为 `ca96a010eb21d2ee48e1b1553c501fb87cbe59b04d3995747195ed23db0547de`。绑定/复算代码：`I/recompute.py:70-124`；每份评分 member 路径及 hash：`I/sample-sources.csv:2-1891`。
- **1025主源为补充修订**：从原1080份评分及14份绑定 sidecar 重新算360样本，而不是照抄 `analysis.json`。逐一验证 `input_sha256 == full_history_sha256`，复算 A/B 后核对 adopted `analysis_view`；`I/recompute.py:126-180`。保留原 available-case（A有效355、B有效351），不把缺失当0，不拿修订CI贴到原点估计上；`I/recompute.py:260-271`、`I/result.json:1-15`。
- **公式**：A=`effect_counts.second_order + third_order`（1025另与 SO/TO `appeared` 标签交叉核对）；B=两评委各自有效数值维度均值后等权平均。五月按原 loader 每评委及双评委结果取3位小数；本批五维整数评分下不改变所报均值。维度旁路 D1…D5 仅在两评委该维都存在时取均值，缺维保留NA；不回写主B。全文字符数=`len(combined_output)`，末轮=`len(responses[-1])`，不是token数。见 `I/recompute.py:100-116`、`:155-178`。
- **样本量/权重**：五月每模型×企业×条件35，SASR/MAMR各315（模型分层各105）；1025每格5，每臂45（模型分层各15），八臂360。完整格下 pooled mean 与3模型×3企业九格等权点估计一致。原available-case仍先格内有效样本均值再九格等权。
- **区间边界**：下列95% bootstrap CI均为探索性、条件于这3个模型/3家企业，无多重比较校正、无等价检验。同期按模型内 replicate 整块重抽，八臂和三企业一起移动；跨期两期独立抽样，五月SASR格内重抽、MAMR三企业批次同抽，1025整块同抽；不按跨期同名 `run_id` 配对。PCG64/seed=20261027/10000 draws/linear quantile；`I/recompute.py:193-259`。既有结果已足够，不再扩展大规模bootstrap。

#### F1. 同 DNA 跨期现象：MAMR上升，SASR的B总体近乎不动

**直接观察（Red Source）**，Δ=1025−五月。整体每期/每条件 n=315→45。

| 条件 | 五月A | 1025 A | ΔA [95% CI] | 五月B | 1025 B | ΔB [95% CI] |
|---|---:|---:|---:|---:|---:|---:|
| SASR_DNA | 4.1333 | 4.7333 | 0.6000 [0.2254, 0.9968] | 2.9905 | 2.9978 | 0.0073 [-0.0889, 0.1076] |
| MAMR_DNA | 6.4540 | 7.9333 | 1.4794 [1.0349, 1.9079] | 3.6014 | 3.8933 | 0.2919 [0.2032, 0.3735] |

来源：`I/cross-period.csv:2-17`、`I/group-means.csv:2-17`；父协调者已独立复核两期10个整体A/B均值，与本调查结果零失配。

**模型分层（每期/每条件 n=105→15）**：

| 模型 | 条件（均有DNA） | A：五月→1025 | ΔA | B：五月→1025 | ΔB |
|---|---|---:|---:|---:|---:|
| GPT | SASR | 4.3524→4.4667 | 0.1143 | 3.0914→3.0267 | -0.0648 |
| GPT | MAMR | 5.6571→7.3333 | 1.6762 | 3.8338→3.8467 | 0.0129 |
| DeepSeek | SASR | 4.0095→4.7333 | 0.7238 | 2.9924→3.0733 | 0.0810 |
| DeepSeek | MAMR | 6.1714→8.4000 | 2.2286 | 3.4257→4.0533 | 0.6276 |
| Qwen | SASR | 4.0381→5.0000 | 0.9619 | 2.8876→2.8933 | 0.0057 |
| Qwen | MAMR | 7.5333→8.0667 | 0.5333 | 3.5448→3.7800 | 0.2352 |

- MAMR的B增量并不均匀：GPT +0.0129（CI −0.1343, +0.1529），DeepSeek +0.6276（+0.4057, +0.8105），Qwen +0.2352（+0.1676, +0.3029）。GPT区间跨0不等于“已证明无变化”，也不能仅以一显著一不显著证明模型差异。逐模型数据及CI见 `I/cross-period.csv:7-9`、`:15-17`。
- **同 DNA 的 MAMR−SASR**：五月A=2.3206、B=0.6110；1025 A=3.2000、B=0.8956。1025 A的2.8000/B的0.8533是 `MAMR_DNA−SASR_NoDNA`，不是本项同DNA对角。见 `I/mamr-sasr-gains.csv:2-17`、`I/factorial-contrasts.csv:30`、`:146`。不能将对角差增长解释为DNA效应，亦未由此识别跨期机制。

#### F2. 1025同期八臂：MR最稳定，MA/DNA的含义依赖条件

先列各臂直接均值（每臂n=45；修订版，Red Source）：

| 臂 | A | B | 全文字符均值 | 末轮字符均值 |
|---|---:|---:|---:|---:|
| SASR_NoDNA | 5.1333 | 3.0400 | 919.82 | 919.82 |
| SASR_DNA | 4.7333 | 2.9978 | 843.20 | 843.20 |
| SAMR_NoDNA | 7.3111 | 3.8817 | 4455.87 | 1760.91 |
| SAMR_DNA | 6.8000 | 3.8600 | 4071.29 | 1651.24 |
| MASR_NoDNA | 4.4222 | 3.0133 | 872.00 | 872.00 |
| MASR_DNA | 4.9778 | 2.9689 | 876.87 | 876.87 |
| MAMR_NoDNA | 7.7556 | 3.8111 | 3363.31 | 1080.56 |
| MAMR_DNA | 7.9333 | 3.8933 | 3112.58 | 1007.09 |

来源：`I/group-means.csv:10-17`。因子记号 `a=SA/MA`、`r=SR/MR`、`d=NoDNA/DNA`；**指标A**与**因子a/组件C_A**不可混淆。

**主移除差**均以完整 `MAMR_DNA` 为起点，分别减去 `SAMR_DNA`、`MASR_DNA`、`MAMR_NoDNA`，不是跨其他水平平均的主效应：

| 主移除差 | A [95% CI] | B [95% CI] | 原available-case A / B（CI=NA） |
|---|---:|---:|---:|
| C_A：MA−SA，固定MR/DNA | 1.1333 [0.6444, 1.6444] | 0.0333 [-0.0711, 0.1289] | 1.1889 / 0.0267 |
| C_R：MR−SR，固定MA/DNA | 2.9556 [2.3778, 3.5339] | 0.9244 [0.8511, 1.0000] | 2.9778 / 0.9244 |
| C_D：DNA−NoDNA，固定MA/MR | 0.1778 [-0.2889, 0.6222] | 0.0822 [-0.0200, 0.1733] | 0.1778 / 0.0822 |

来源：`I/factorial-contrasts.csv:2-4`、`:118-120`；原版逐样本重建见 `I/recompute.py:260-271`、`I/result.json:175`起。修订并未翻转这三项总体方向，但“原CI缺失”必须保留。

**条件依赖与交互（Red Source）**：

1. **总体MR simple差四项A/B皆正，四项各自CI均排除0**：固定(a,d)=(SA,NoDNA)/(SA,DNA)/(MA,NoDNA)/(MA,DNA)，A增量=2.1778/2.0667/3.3333/2.9556，B=0.8417/0.8622/0.7978/0.9244。是总体层结论，不是每个模型每一格皆正（如GPT SAMR_NoDNA−SASR_NoDNA的A=−0.3333、CI跨0）。来源：`I/factorial-contrasts.csv:22-25`、`:51-54`、`:138-141`。
2. **DNA没有普遍正增益**：DNA−NoDNA在SASR/SAMR/MASR/MAMR下A=−0.4000/−0.5111/+0.5556/+0.1778，B=−0.0422/−0.0217/−0.0444/+0.0822。总体A只有MASR此项探索性CI排除0；B四项均跨0。不应写“DNA无效”，而应写“本样本不支持跨结构一致的正增益”。来源：`I/factorial-contrasts.csv:26-29`、`:142-145`。
3. **平均主效应与主移除不是同一量**：跨另两因子水平平均，a/r/d在指标A上的主效应=+0.2778/+2.6333/−0.0444，在B上=−0.0232/+0.8565/−0.0065。指标A的AR交互=1.0222 [0.5333,1.5444]、AD=0.8222 [0.4889,1.1556]；这是平均difference-in-differences（不是回归±1编码系数），表明MA相对差依赖轮数与DNA水平。但三阶ARD=−0.2667 [−1.4444,1.0222]，总体B的二阶/三阶交互均未排除0；不支持强“三组件协同”叙事。来源：`I/recompute.py:193-209`、`I/factorial-contrasts.csv:5-17`、`:121-133`。

#### F3. SR负对照：请求相同，不能把负差归因提示词或agent数量

**直接观察（Green Source请求核验；Red Source评分差）**：SASR与MASR同DNA水平下，3模型×5重复×3企业×2水平共90对首轮实际 `prepared.task.request_json`，解析后的完整body（messages/model/temperature）全部相等，`route_json`逐对相等；90对输出文本无一相同。不只是静态模板“看起来相同”，也不只是比较可能带依赖ID的request hash。核验代码 `I/check_protocol.py:30-55`，全配对表 `I/sr-request-pairs.csv:2-91`；第一对实际请求见 `F/runs/formal-v31-360-20261026-r2/journal/00000253.json:1` 与 `.../00000274.json:1`（完整路径逐行保存在CSV）。静态 SR 分支也没有MA/SA措辞区别：`F/scripts/design.py:115-127`。

- NoDNA下MASR−SASR的A=−0.7111 [−1.2444,−0.2000]；DNA下A=+0.2444 [−0.3111,+0.7556]。B分别−0.0267/−0.0289，两区间均跨0。来源：`I/factorial-contrasts.csv:18-19`、`:134-135`。
- **解释边界**：这里SR的“MA标签”没有落实为不同的信息交换处理，因此负差不是纯agent数处理的因果证据，也不能归于提示差异。temperature=0.7且输出不同，**可与生成随机波动相容**；还存在评委采样、执行时序、后端变化等未分离来源。现有输出不能证明是“偶然评分采样”单独造成：未固定相同文本反复盲评分，也未做同期交错的同body重复采样分解。探索性多重比较和每格仅5重复进一步限制其诊断强度。

#### F4. 总分接近抵消，不等于维度或模型没有变化

**直接观察（Red Source）**：D1=causal chain，D2=strategy rationality，D3=effect coverage，D4=competition awareness，D5=time horizon；各维先取双评委平均，再按样本汇总。

| 对比 | D1 | D2 | D3 | D4 | D5 | B总差 |
|---|---:|---:|---:|---:|---:|---:|
| 同期C_A：MAMR_DNA−SAMR_DNA | -0.1778 | -0.1556 | 0.0111 | 0.8444 | -0.3556 | 0.0333 |
| 同期C_R：MAMR_DNA−MASR_DNA | 0.4000 | 1.4333 | 0.4778 | 1.3444 | 0.9667 | 0.9244 |
| 跨期MAMR_DNA：1025−五月 | 0.2516 | 0.3492 | 0.2865 | 0.3175 | 0.2548 | 0.2919 |

来源：直接相减 `I/group-means.csv:2`、`:10`、`:12`、`:14`。以上均为描述性维度差，未新增维度显著性检验。

- C_A的B总差仅+0.0333，却是D4 +0.8444被D5 −0.3556、D1 −0.1778、D2 −0.1556等抵消；较准确表述是“竞争意识评分增加、其他维度有所权衡”，不是“MA不改变质量”。C_R则五维均正，尤以D2/D4较大。
- C_A有模型异质性：GPT/DeepSeek/Qwen的A=+2.4667/+0.7333/+0.2000，B=−0.1800/−0.1133/+0.3933。GPT的A增加但B下降，Qwen的B增加；总体平均不能代替每个模型。来源：`I/factorial-contrasts.csv:31`、`:60`、`:89`、`:147`、`:176`、`:205`。
- 跨期MAMR的五维整体均上升，但分层集中：DeepSeek D4 +0.8571、D2/D5各+0.6810；GPT各维变动很小。Kimi和MiniMax各自MAMR均值跨期增量分别+0.4152/+0.1686；双评委同向不意味着已排除共享偏差或服务变化。来源：`I/group-means.csv:2`、`:4`、`:6`、`:10`、`:18`、`:26`。
- **缺维例外必须披露**：1025 DeepSeek/rep-5/SAMR_NoDNA/LANDSPACE的Kimi D4=None，其主B-Kimi=4.75按四个有效维度取均值，双评委B=4.275；因此不能称“全部1080评分完整五维”，1080还包含A，本批B评分是720份（719份五维、1份四维）。调查维度表在该样本D4保留NA，其余四维照计；SAMR_NoDNA的D4因此n=44，其他维n=45，五维旁路完整行n=44，不把各维均值平均冒充既有主B。原文件 `F/runs/formal-v31-360-20261026-r2/scores/0cc7486710f546cf354ae50472165bbd888c66cfec8e90c215e127a2b8a5b8f4.json:1`；`I/result.json:145-170`、`I/recompute.py:175-178`。

#### F5. 长度能解释一部分观测机会，但不能单独解释分数变化

**直接观察（Red Source）**：整体SASR全文均值824.45→843.20字符；MAMR全文2831.78→3112.58、末轮926.13→1007.09。MAMR分模型如下：

| 模型 | 全文字符：五月→1025 | 末轮字符：五月→1025 | 跨期A / B变化 |
|---|---:|---:|---:|
| GPT | 4075.68→4157.00 | 1390.47→1315.33 | 1.6762 / 0.0129 |
| DeepSeek | 2090.23→3026.33 | 630.39→1047.20 | 2.2286 / 0.6276 |
| Qwen | 2329.43→2154.40 | 757.52→658.73 | 0.5333 / 0.2352 |

来源：`I/group-means.csv:2-9`、`:18`、`:26`、`:34`。

- DeepSeek变长且A/B升高，但Qwen变短仍A/B升高，GPT长度近似而A上升/B近似；单一“文本更长所以更好”不成立。同期SAMR_DNA全文4071.29/末轮1651.24，均长于MAMR_DNA的3112.58/1007.09，但A反而较低（6.8 vs7.9333）、B接近（3.86 vs3.8933）；`I/group-means.csv:10`、`:14`。
- **协议支持解释**：两期评分都读全轮 `combined_output`，并非只评末轮；多轮的更多文本、迭代及上下文可能共同增加被识别到高阶效应的机会。因此观察到的是“全历史视图下MR处理包的评分增量”，不是已识别的单位token推理效率提升。历史代码 `M/scripts/validate_track_a.py:64-75`、`M/scripts/score_track_b.py:86-96`；1025 `F/scripts/score_factorial.py:33-52`；实际全文拼接逐样本由 `I/recompute.py:113`、`:151-157` 核对。
- 本调查只提供模型×臂内长度相关诊断（`I/length-diagnostics.csv:2-61`），不做“每字得分”或控制长度后的因果结论。长度是post-treatment，混合了处理路径，相关不等于中介机制。
- **不要把五月MAMR token_usage当企业输出长度**：历史源码累加三轮×三企业的9次生成及内容重试usage，整批计数复制给三企业；摘要调用usage被丢弃。不是单企业token数，也不是完整11次调用账。见 `M/scripts/generate_experiments.py:164-165`、`:179-194`、`:210-225`。故本报告主长度用原文本字符数。

#### F6. 协议/测量可比性：哪些断点已证实，哪些不能推断

下表是 **Green Source** 的配置/记录核查，不把配置名视为后端权重冻结。历史配置引用 `M/config/experiment-config.yaml:30-82`，已与五月工程ZIP对应成员逐字核对（五份代码/配置全部相同，`I/protocol-checks.json:183-218`）；它们仅作为历史协议的可定位副本，不使用1023结果作五月主数据。1025配置 `F/config/factorial.yaml:21-67` 与原实际journal路由一致（`I/protocol-checks.json:141-150`）。

| 角色 | 五月 | 1025 | 可据此说什么 |
|---|---|---|---|
| GPT生成 | OpenRouter `openai/gpt-oss-120b:free` | OpenRouter `openai/gpt-oss-120b`（非free ID） | 路由标签改变；不能直接推断质量提升 |
| DeepSeek生成 | Paratera `DeepSeek-V4-Flash` | OpenRouter `deepseek/deepseek-v4-flash` | 服务及model ID改变，跨期并非受控重跑 |
| Qwen生成 | Paratera `Qwen3.5-122B-A10B` | 同服务、同ID | 同ID仍不保证底层权重/推理后端不变 |
| A评委 | 原对象标识 `glm-5.1` 170份、`glm-5.1-coding` 460份；后者配置为glm-coding服务/model ID `glm-5.1` | 统一Paratera `GLM-5.1` | A定义相同，测量服务不恒定；不能把水平差归于生成质量 |
| B-Kimi | Paratera `Kimi-K2.5` | OpenRouter `moonshotai/kimi-k2.5` | 评委服务改变；评分漂移未被桥接校准 |
| B-MiniMax | Paratera `MiniMax-M2.7` | 同服务、同ID | 仍非锁权重或盲测校准 |

**A评委不是随机分派**：五月SASR315份全coding，MAMR170份glm-5.1、145份coding；由原 `original_evaluations[].judge` 计数，`I/check_protocol.py:18-24`、`I/protocol-checks.json:95-103`。因此服务间样本均值之差不可当评委因果效应，跨期A只能报“各自冻结测量下的观测差”。五月唯一22项判断是MAMR/GPT/LANDSPACE/031、coding、completion_tokens=8192，但缺的是EB-003/004/005，SO10项/TO7项齐全；不能声称这项直接压低A（二+三阶）。见 `I/protocol-checks.json:104-134`。

**cap与实际行为的证据强度**：

- 五月静态 `api_client.call_model` 会传 `max_tokens`；生成/摘要配置默认2048、评分显式8192，temperature=0.7。调用链：`M/scripts/api_client.py:26-36`，`M/config/experiment-config.yaml:112-122`，`M/scripts/generate_experiments.py:122`、`:164`、`:190`，评分 `M/scripts/score_track_b.py:176-177`、`M/scripts/validate_track_a.py:188-189`。**未保存逐请求body，静态配置不能证明每次实际发送或服务遵守了cap。**
- 逐样本SASR的Qwen 105/105记录completion_tokens=2544–6476，均超过静态2048；GPT为474–1067、DeepSeek为409–1411（`I/protocol-checks.json:160-181`）。这支持“静态cap与记录usage不能等同”，不证明Qwen没有截断，也不证明其他模型均未截断；还需区分服务实际参数与usage统计口径。
- 1025原执行journal全部1874个prepared请求（生成、摘要、评分及内容尝试）body仅messages/model/temperature、temperature均0.7，**没有显式 `max_tokens`/`max_completion_tokens`**；`I/check_protocol.py:30-40`、`I/protocol-checks.json:136-155`。这是原执行范围，不将其混称为13次补评分。无显式cap不等于无限长度；完成记录stop=1861/error=2/None=11，无记录为length，但stop不保证语义完整，不能据此宣布“1025没有截断”。

**full_history、摘要与MA处理包**（Green Source协议；机制解释仍有限）：两期MAMR均使用各企业前800字符生成竞争摘要，要求200字以内但代码未硬截摘要返回；摘要仍用该生成模型，不是独立更强模型。五月 `M/scripts/generate_experiments.py:140-165`，1025 `F/scripts/generate_factorial.py:124-135`。1025 SAMR回灌自身上一轮全文，MAMR回灌跨企业压缩摘要，且轮提示措辞不同；依赖拓扑 `F/scripts/generate_factorial.py:93-101`、提示 `F/scripts/design.py:115-127`。因此C_A是**信息共享范围＋压缩＋编排＋措辞**处理包，不能称纯agent数量效应。D4上升与竞争信息共享在协议上相容，但未证明由摘要中的某条信息导致，亦未区分其他处理成分。

**特别核实：五月11个 `overall_score` 不构成额外维度或偏差来源。** 原scores中虽出现额外键，使用Fraction按原数值逐份检查，11/11恰等于D1…D5五维均值；将它作为第六个数值再平均仍严格等于原五维均值，单评委、双评委及汇总B影响均为0。见 `I/check_protocol.py:25-29`、`I/protocol-checks.json:3-94`。因此“五月B因多算一维而偏移”已被本数据证伪；不能据键数量差异制造跨期差异解释。

#### F7. 原因证据等级、复核结果与交付边界

| 等级 | 可写入结论 | 不能升级为什么 |
|---|---|---|
| **直接观察** | 修订样本下MR总体增量最稳定；MA在D4与其他维度及模型间发生抵消；DNA条件依赖；跨期MAMR增量异质 | 不是现实政策效果，不能泛化为所有模型/企业普遍规律 |
| **协议支持解释** | 全历史评分增加多轮文本的观测机会；跨企业摘要与竞争意识维度同向；服务/cap/评委变化破坏跨期受控比较 | 不能单独识别迭代、长度、信息共享、措辞的贡献；不能从断点存在反推断点造成全部差异 |
| **未验证假说** | 模型服务/后端漂移、评委严宽变化、生成与评分随机性、摘要压缩损失、时序效应可能共同作用 | 未有同文本跨期评委桥接、冻结服务重放或机制消融，不报告任何机制贡献百分比或单一根因 |
| **被排除/纠正** | 11个overall_score数值影响为0；SR实际body/route无差异；同DNA对角A=3.2而非2.8；1025尚有1份缺D4 | 不再采用“多算一维解释跨期B”“SR提示差异造成负差”“全五维无缺失”“stop证明未截断”等表述 |

**代理断言复核（Green Source）**：获准的两个窄explore均已收集；主来源、35对5重复、full_history、模型路由及同期差线索经本会话直接计算/读码确认；对角误报/overall偏差证伪、D4漏检、usage账口径误解均已记录于 `I/CHANGELOG.md:7`。未验证的底层机制不进入事实结论。未以代理汇总代替原样本复算。

**交付物与复现**：

```bash
python3 -B analysis/tsinghua-1025-vs-may-20261027/recompute.py
python3 -B analysis/tsinghua-1025-vs-may-20261027/check_protocol.py
```

- `sample-metrics.csv`（990样本）、`sample-sources.csv`、`group-means.csv`、`cross-period.csv`、`mamr-sasr-gains.csv`、`factorial-contrasts.csv`、`length-diagnostics.csv` 与 `result.json` 提供字段及完整精度；`sr-request-pairs.csv`、`protocol-checks.json` 提供协议核查。14份替换评分的真实sidecar来源以 `O/provenance.json:1` 为准（`sample-sources.csv` 的overlay标记需沿该表解析，不能把其中保留的原评分hash误当新评分hash）。
- `input-hashes.json` 与 `protocol-input-hashes.json` 保存输入hash；独立复算最后逐一核对输入前后未变。承重同期点/区间与冻结统计的最大误差分别为1.7764e−15/1.3323e−15（仅先独立计算后才作对账，`I/recompute.py:227-231`）；不把旧汇总用作计算输入。
- 本调查没有新增API、没有安装、没有导入原工程执行逻辑；只在获准新辅助目录写计算产物，并仅在本报告 `Investigator Findings` 追加结论。父协调者已据直接复核结果定稿。既有 `legacy/p11-closed-v5-minimax-m3`、`papers/p12-judge-calibration/wiki/index.md`、`papers/p1p2-evidence-ledger/wiki/index.md` 等非本任务改动未触碰；不commit。

## Investigation Log

- 2026-10-27：已直接读取CLAUDE.md及AGENTS.md；工作区绑定auto-research已核对。既有三处modified不触碰。
- 初始假说：轮数/全历史评分与输出长度共同影响指标；服务/输出cap/样本量/测量版本可能不可完全比；DNA可能约束泛化也可能提供具体性；MA效应可能依赖MR与DNA。
- 工具限制：context_builder两次因 `context_builder_roots_changing` 在provider启动前被拒绝；根目录/read_file也超时。经明确workspace绑定尝试后仍失败，未继续相同重试，改为pair只读调查和父shell复核。manage_selection追加一次超时，故未声称context_builder或selection成功。
- 父先从history-001原评分和1025 combined-dataset独立算10组总体均值，逐项确认；再独立编写 `I/parent_verify.py`，从原评分＋sidecar和五月归档逐样本复核全部主要指标及分组；`I/parent-verification.json:1` 返回 `PARENT_DIRECT_CHECK_PASS`。同时直接复跑 `I/recompute.py` 与 `I/check_protocol.py`，确认来源hash、同期区间对账、路由/cap/90请求对等断言。初次parent脚本仅因外部归档不在ROOT内的路径序列化失败，未更改数据；支持绝对归档路径后通过。
- Oracle有界解释审查：export `prompt-exports/oracle-chat-2026-10-27-115955-new-chat-45f001-5a4f.md`。因selection更新超时，明确仅提供已直接核验的数字和协议摘要，不声称Oracle读到完整新证据。主lane指出MR全历史与预算绑定、负对照偏移不宜视作已分离白噪声、NoDNA只消融五属性等解释，与已读代码相符；未将Oracle当新事实来源。
- Oracle其他lane纠错：把NoDNA保留企业名称为“身份消融失败”不成立，本设计本来只删除五属性；不能用MA维度负差否认MR总体simple差；不能把90对输出不同直接确认独立无偏噪声。其余lane无可用完整分析/正确workspace证据，不采纳。无第二轮Oracle。

## Root Cause / 解释分级

不存在已识别的单一根因。下列原因按“已有协议依据”与“尚待验证”分级；**已核实断点 ≠ 已确认造成分差**。直接数据表、代码和请求证据见F1–F6。

| 可能原因 | 能解释的现象 | 当前证据 / 不能越过的边界 |
|---|---|---|
| 1. 迭代、更多生成预算与更多评分材料共同起作用 | MR总体高于SR | 两期都评三轮全文，属于已核实处理包；无法分离反思、重复采样、覆盖机会和预算，不是单位token效率结论。 |
| 2. 共享竞争信息让注意力偏向对手互动 | MA的D4较高 | MAMR确实消费跨企业竞争摘要，结果与之相容；尚未追踪具体信息引用，不能证明共享是独立原因。 |
| 3. 压缩与全文回灌带来不同保留/遗忘 | SAMR更长，部分维度高于MAMR，但A较低 | SAMR自身上一轮全文对比MAMR各企业前800字符的共同摘要已确认；摘要可能损失具体性也可能去冗余，净机制未分离。 |
| 4. 指令措辞和计分目标相互作用 | 高阶效应“数量”和质量维度不完全同步 | SR要求直接列一二三阶，MR要求企业决策及新发现效应；A量覆盖、B量多维表现，不能互换，不能因A增就称整体质量增。 |
| 5. DNA既补充约束也可能锚定思路 | DNA有时正、有时负 | 五属性被开关、身份仍在已核实；“更具体”与“限制搜索空间/引入锚定”均为待内容编码的竞争假说，不能由分差直接确认。 |
| 6. 企业名称已触发预训练知识，显式DNA信息增量有限 | NoDNA也能获得较高评分 | 名称保留是设计事实；是否调用了正确企业知识、与五属性重叠程度未测。NoDNA不是无企业信息，更不是设计失败。 |
| 7. 模型对共享/压缩/身份线索的响应不同 | MA的B在GPT/DeepSeek为负、Qwen为正 | 异号点估计已核实；尚非模型交互因果确认，可能受每模型5块的波动影响。 |
| 8. 生成服务/后端或默认参数变化 | 五月到十月MAMR分数上升且模型不均匀 | GPT/DeepSeek路由变化确实存在，同ID也未锁权重；未控制重放，不知方向与贡献，不可称模型必然升级。 |
| 9. 评委变化及臂间评委构成不均 | 跨期A/B及五月MAMR−SASR差 | 五月A混合且与条件不均衡、Kimi换路由已核实；不能断言谁更严，不能把所有跨期变化归给评委。 |
| 10. 输出长度/cap、随机波动、变体抽样及执行时序 | 局部升分、负对照偏移、结果不稳定 | 长度和请求参数差异、SR同body不同输出已核实；五月实际cap/后端未知。Qwen变短仍升分，排除单一“越长越高”解释。35→5重复、新seed/设计块使抽样与时序不能忽略，但不能凭此判定异常原因。 |

**目前不能支持的归因**：去DNA导致跨期提升、付费路由必然更优、五月被cap普遍截断、多agent数量本身导致提升、DNA已证明无用、SR负对照差就是无偏随机噪声。11份overall键、缺3个EB也不能解释本次主分差。

## Recommendations

1. **当前报告写法**：主结论限定为“冻结模型评分下的多轮处理包优势和条件性”；完整披露负对照偏移、模型/维度异质性及跨期服务/评委变化。不要给机制贡献百分比。
2. **优先零API分析（建议，未新增执行）**：对90对SR差逐模型/企业/变体/实际时序拆解，检查是否少数样本或批次主导；预先说明探索性质，不把负差当固定偏差扣到MR。
3. **若另获评分授权**：按时期×臂×模型均衡抽小样本，用同一冻结评委盲化、随机次序重评，分离评分尺度漂移；复用MR文本做全文/末轮评分敏感性，但后者仍不控制生成预算。
4. **若另获生成授权**：小规模一次只改共享、压缩或DNA一项，保留预算匹配及同body重复采样；不建议仅为了追根因重跑整个八臂。除既有14份修订外，本调查不新增重评或生成。

## Preventive Measures

严格区分原协议与恢复视图、同期与跨期比较、模型评分与现实效应；不将探索性区间当多重校正检验。
