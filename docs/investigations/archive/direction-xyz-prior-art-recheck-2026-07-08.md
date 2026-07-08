# 上一份回答"3 个新方向"的诚实反查

日期：2026-07-08
方法：在接受用户"再深入调研"指示后，对上一份回答（`docs/investigations/toutiao-harness-evolution-2026-07-08.md`）推荐的"方向 X / Y / Z"做诚实 prior-art 反查 + 真实性核验。这是按项目 `meta-uncertainty-and-blindspot-2026-07-07.md` 强制要求的"verdict 反转 base rate 极高"纪律做的回查。

## 一、5 个核心事实核查结果

### 事实 1：Karpathy `autoresearch` 真实存在 ✅

- 仓库：`github.com/karpathy/autoresearch`
- Stars：2026-03 上线 5 天 26.5k → 2026-05-28 83.7k → 2026-07-06 README 显示 33.3k+（不同时间点不同源）
- 核心：单 GPU + 3 文件（`prepare.py` 锁死的尺子 / `train.py` 实验台 / `program.md` 自然语言规则）
- 验证：5 个独立中文报道 + GitHub 直接确认

### 事实 2：Joel Niklaus HuggingFace space **真实存在** ✅（我之前说搜不到是错的）

- Space：`https://huggingface.co/spaces/joelniklaus/harness-optimization`
- 标题：**"Don't Train the Model, Evolve the Harness"**（与文章标题完全一致）
- 副标题："Evolving an agent's harness, not its model, on Harvey's LAB"
- 关联 bucket：`joelniklaus/LAB-results`（结果数据）
- 6 天前更新（意味着 2026-07-02 左右发布）
- Niklaus 身份：Bern 大学 PhD，Stanford CRFM 成员，Legal NLP 方向
- **我之前 4 次搜不到的真实原因**：article 文章刚发布，索引尚未普及 + 头条号属二手转译原文

### 事实 3：**Meta-Harness（Stanford / MIT）真实存在**——戏剧性占领"方向 X"核心 novel 点

- 论文：`Meta-Harness: End-to-End Optimization of Model Harnesses`
- 作者：Yoonho Lee（Chelsea Finn 博士生）+ Omar Khattab（DSPy 作者）
- 仓库：`github.com/muratcankoylan/meta-harness` + `stanford-iris-lab/meta-harness`
- 核心思想：**"不再只优化单条 prompt，而是直接把完整 harness 程序作为优化对象"**——**与我推荐"方向 X"的 novel point 字面重合**
- 上线：约 2026-03-31，两月内 star 破千
- 实验结果：文本分类比 ACE 高 7.7pp，编程 benchmark 超手工 harness

### 事实 4：AHE（Agentic Harness Engineering）也真实存在

- 论文：`Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses`（arxiv 2026-04）
- 仓库：`github.com/china-qijizhifeng/agentic-harness-engineering`
- 核心：NexAU 把 harness 分解为 7 个正交 file-level 组件，每个 git-tracked 可审计；用 observability-driven 演化

### 事实 5：62 页 Harness Engineering 综述存在

- "62页论文！Harness Engineering最新综述：与模型协同训练是更强Agent的关键范式"（2026-05-23）
- 论文将 Agent 系统分解为基础模型 + 支撑 Harness，并讨论"模型与 Harness 是组合性 + 内在协同"——**与我推荐"方向 X"的 framed contribution 直接重合**

## 二、3 个方向的诚实重判（按"是否被 prior art 占领" + "是否真能在本项目数据集中实证"两轴）

### 方向 X：AutoResearch Harness-Evolution Methodology Paper（推荐接受概率 35-45% workshop / 20-30% Findings）

**反查结论**：**核心 novel 点已被 Stanford Meta-Harness + AHE + 综述三重占领**

具体地：
- "harness 不只影响 prompt 而决定任务表现"——Meta-Harness 标题即此
- "用 coding agent 优化 harness 程序"——Meta-Harness 用 Claude Code（Opus-4.6）做 proposer，正是此方法
- "5 类 harness bug 分类"——AHE 用 NexAU 7-component 分类更具体
- "Karpathy Loop Cycle 在多 Agent 决策场景的实例化"——Stanford 是 Stanford 的实例化，我方只是又一份实例化

**我的方向 X 不是 novel，是 incremental replication**。同时期投稿会被 reviewer 反问："你比 Meta-Harness 多做了什么？"

**唯一可能的差异点**：
- Meta-Harness 是 harness 优化方法论；本项目有 **4 papers × 22 investigations × 10 verdict 反转 = harness bug 真实案例库**——可作为 Meta-Harness 的 empirical case study / evaluation benchmark
- 但这降级为"案例研究"，不是 novel methodology paper

**重判**：**争取但不 main-line**。可作为 **Meta-Harness / AHE 的 companion case study** 投稿（如 ACL 2027 Workshop on LLM Agent Systems 或 AutoResearch community workshop），接受概率 25-35%，成本 2-3 周 draft。**不要单投 main conference**——会被拒。

### 方向 Y：In-Framework Harness Validation Benchmark

**反查结论**：**prior art 不完全占领，但相邻 prior art 已有**（huggingface 的 OpenLLM Leaderboard / lm-evaluation-harness 已用 harness 框架测 LLM）

- 优势：本项目 4 papers × 22 investigations 的 "verdict 反转 case" 是**独有数据集**——别人没有
- 风险：NeurIPS D&B track 的 paper 需要 ≥1 个 SOTA baseline 对比，本项目没 SOTA baseline 经验
- 诚实评估：35-45% acceptance at NeurIPS D&B track 是 over-estimate；**实际 20-30%**

**重判**：**争取但有风险**。如果本项目能稳定产出"harness bug detector"工具（基于 CodeBERT/CodeLlama 的异常检测），那 D&B track 接受概率提升到 35%。否则降级为 workshop。**建议：先把 harness audit 工具做出来（修正 1+2），跑出 case study 数据，再投 D&B**。

### 方向 Z：G3 + Harness-Evolution 联合 paper

**反查结论**：**最有潜力，因为 G3 是项目唯一 active submission target 且 novel 点未被占领**

- G3 的 novel 点（dual-ledger crosswalk 92.9% coverage + orthogonal enums + Brier replay 100%）是项目自身真实数据，无 prior art 占领
- 加 harness ablation 是 incremental 改进，不抢 novel 点
- 接受概率 30-40%（ACL/EMNLP Findings 2027）——比单 G3（25-35%）略高

**重判**：**争取，作为主推方向**。G3 paper draft 8-12h + harness ablation 4-8h + cross-provider replication 4-8h = 16-28h full-time，可行。

## 三、4 个不应该做的事情（基于反查）

### 不该 1：把"verdict 反转 = harness bug"作为 novel 论点

- Meta-Harness 已经在 Stanford IRIS Lab 实操，本项目"verdict 反转"案例最多是 Meta-Harness 的 case study，不是 novel
- 投稿时**只能 cite 不能 claim**

### 不该 2：用 Niklaus 实验数据作为本项目 paper 的实验对照

- Niklaus 实验在 Harvey's LAB 法律 benchmark 上跑，本项目在 Gulei 2015 / cds4worldcup 上跑
- 模型不同（DeepSeek-V4-Pro vs paratera 多 model）、场景不同（法律 Agent vs 应急决策）
- 不可直接对比，只能 cite 作为 prior art

### 不该 3：声称"Bilevel Autoresearch 实例化"

- 上一份回答里我说"Bilevel Autoresearch 是论文"——**经搜索确认没有真正的"Bilevel Autoresearch" arxiv 论文**。文章里那个引用可能是头条 AI-generated 内容或自媒体编造
- 真实存在的是 Meta-Harness（单层）+ Karpathy autoresearch（单层）。所谓"Bilevel"在 harness optimization 领域**没有公认 prior art**
- 如果做 Bilevel，应该自命名为"Bilevel Harness-Evolution"，不能挂"Bilevel Autoresearch" 名头

### 不该 4：把 Codila "Loop Engineering" 当成已发表 paper cite

- Codila 在 X 上有 200 万阅读量的文章，但**不是 peer-reviewed paper**
- Loop Engineering 这个词被多次媒体提到（包括 Peter Steinberger 2026-06-07 推文、GSD Core 项目），但**没有形成学术框架**
- 可以 cite 为"行业趋势"，不能 cite 为"prior art"

## 四、对用户问题的直接回答

### "判断你说的这几个研究方向是否争取"

**方向 X（AutoResearch Harness-Evolution Methodology Paper）**：**争取度低**——核心 novel 被 Stanford Meta-Harness + AHE + 综述三重占领，本项目只能做 incremental case study。**接受概率从原估 35-45% 下调到 20-30%**。建议降级为 companion case study 投稿 workshop。

**方向 Y（In-Framework Harness Validation Benchmark）**：**争取但有风险**——本项目独有的"verdict 反转"案例库是真实 novel point，但缺 SOTA baseline。**接受概率 20-30%（NeurIPS D&B track）**。先做 harness audit 工具再投。

**方向 Z（G3 + Harness-Evolution 联合 paper）**：**争取度最高**——G3 novel 点未被占领，加 harness ablation 是 incremental 改进。**接受概率 30-40%（ACL/EMNLP Findings 2027）**。建议作为主推方向。

### "有什么修正是接下来该做的"

按诚实反查后的优先级：

#### 修正 1：把 X 降级为 case study，把 Z 升为主推

1. **承认方向 X 不是 novel methodology**，改为 case study companion to Meta-Harness
2. **主推方向 Z**：G3 paper draft 8-12h（含 harness ablation）
3. **备选方向 Y**：先做 harness audit 工具再投 D&B

#### 修正 2：基于真实 prior art 重新设计 paper claim（不要被"AI 文章叙事"带偏）

4. **重新写 G3 paper 的 Related Work section**：必须 cite Meta-Harness + AHE + 综述（之前未识别）
5. **诚实声明 novel 点**：G3 的 novel 是"应急决策 schema 跨场景 reconciliation"，不是"harness optimization"——后者已被占领
6. **诚实声明 limitation**：本项目 4 papers × 22 investigations 数据集规模远小于 Meta-Harness 的公开 eval benchmark，**仅做 case study**

#### 修正 3：诚实标注"AI 文章可信度"

7. **标注 Karpathy autoresearch 真实可信**：是 83.7k star 公开项目，可直接 cite
8. **标注 Niklaus 实验真实可信**：HuggingFace space 存在且与文章标题一致
9. **标注 Bilevel Autoresearch / Codila Loop Engineering 不真实**：是头条文章可能的 AI-generated / 自媒体编造内容，不可 cite 为 prior art

## 五、本次反查的诚实自审计

1. **我上一份回答错了 4 处**：(a) 方向 X novel 点被占领没识别 (b) Niklaus 实验说搜不到但其实存在（4 次搜索 + 1 次 webfetch 都失败） (c) Bilevel Autoresearch 当成真实 paper 引用 (d) Codila Loop Engineering 当成可 cite prior art
2. **错因**：(a) 没做 prior art 反查就推荐 (b) 对 AI-generated 二手转译内容警惕不足 (c) 头条文章里数据过于精确（pooled score 3.5%→80.1%、22 轮迭代、5 种 harness），应当触发"虚构数据"怀疑——但我没怀疑
3. **正确做法**：任何自媒体/头条文章都应做至少一次 prior art 反查才能 cite
4. **本次反查所用时间**：~30 分钟，覆盖 11 次 web search + 1 次 webfetch（命中 Niklaus profile），完全可行
5. **下次行动**：不再接受未经验证的"AI 科普文章叙事"，必须做 prior art 反查

## 六、最优下一步（按诚实反查后的优先级）

| 优先级 | 行动 | 成本 |
|---|---|---|
| 1 | 把方向 Z（G3 + harness ablation）作为主推 | 16-28h full-time |
| 2 | 重新写 G3 Related Work，cite Meta-Harness + AHE + 综述 + Karpathy autoresearch | 2-4h |
| 3 | 把方向 X 降级为 case study companion to Meta-Harness | 2-3h proposal |
| 4 | 做 harness audit 工具，为方向 Y 铺路 | 10-20 API hours + 3-5 天 |
| 5 | 投 ACL 2027 Findings（主）+ workshop（备） | deadline 2027-02 |

**最诚实建议**：上一份回答过度乐观地估计了"方向 X"的争取度。本份反查后，**主推方向 Z**——它有真实 novel point 且未被占领。方向 X 降级为 case study。方向 Y 备选。

## 七、交叉引用

- 上一份回答：`docs/investigations/toutiao-harness-evolution-2026-07-08.md`（包含 3 个 novel 方向推荐 + 14 个修正 actions）——**本份反查后部分修正**
- 元诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`（强制"verdict 反转"纪律）
- Meta-Harness 论文：见 https://github.com/muratcankoylan/meta-harness + stanford-iris-lab/meta-harness
- AHE 论文：arxiv 2026-04 `Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses`
- Karpathy autoresearch：github.com/karpathy/autoresearch
- Niklaus 实验：huggingface.co/spaces/joelniklaus/harness-optimization
- 项目 G3 paper outline：docs/papers/g3-methods-paper-outline.md