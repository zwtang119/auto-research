# 路线图 working copy 补充调研与文献核实（R2）

- 查询日期：2026-07-22
- 调研对象：`docs/roadmaps/worldcup-two-paper-roadmap-2026-07-21-working.md` v1.5（只读）
- 口径：优先 arXiv、NBER、作者主页及厂商模型卡；所有 URL 均于 2026-07-22 查询。Web Search Prime 因余额不足返回 429，故改用直接页面抓取与 arXiv 搜索页；无法直接证明的内容标为“未找到，不可考”。

## 一、§10 参考文献核实

### 1. AMW：存在 NBER 工作论文，路线图“出处 unknown”已过时

**结论：部分证伪，需更新。** 论文尚未找到期刊正式版，但已是 **NBER Working Paper 33949**（June 2025），DOI 为 **10.3386/w33949**。Alex Moehring 作者主页也将其列为 2025 Working Paper，并链接 NBER w33949。未找到可核验的 SSRN 编号或 exact-title SSRN 页面，故 SSRN 记为“未找到，不可考”。

- 准确题名：*Designing Human-AI Collaboration: A Sufficient-Statistic Approach*。
- 作者：Nikhil Agarwal、Alex Moehring、Alexander Wolitzky。
- NBER：Working Paper 33949，June 2025，DOI 10.3386/w33949。
- 单位核实：Agarwal 为 MIT Economics 的 Paul A. Samuelson Professor，并列 NBER；Wolitzky 为 MIT Economics 教授；Moehring 当前个人主页显示 Wharton School Assistant Professor。因而路线图的“MIT/NBER、Purdue、MIT”至少对 Moehring 的**当前单位**不准确；可能是论文写作时旧单位，但须按 PDF 署名日期另注，不能作为当前单位。
- 期刊版：截至查询日未在 NBER 页面或作者研究页发现期刊接受/刊发信息，故“未找到，不可考”。

证据：
- https://www.nber.org/papers/w33949 （查询 2026-07-22）
- https://doi.org/10.3386/w33949 （查询 2026-07-22）
- https://www.alexmoehring.com/research （查询 2026-07-22）
- https://www.alexmoehring.com/ （查询 2026-07-22）
- https://economics.mit.edu/people/faculty/nikhil-agarwal （查询 2026-07-22）
- https://economics.mit.edu/people/faculty/alexander-wolitzky （查询 2026-07-22）
- https://papers.ssrn.com/sol3/results.cfm?txtKey_Words=%22Designing%20Human-AI%20Collaboration%3A%20A%20Sufficient-Statistic%20Approach%22 （403，未能核验；查询 2026-07-22）

### 2. arXiv 四条逐项核实

| arXiv | 存在性 | 核实元数据 | 与路线图 §10 比对 |
|---|---|---|---|
| 2605.00420 | 存在 | *Foresight Arena: An On-Chain Benchmark for Evaluating AI Forecasting Agents*；Maksym Nechepurenko、Pavel Shuvalov；v1 2026-05-01，v2 2026-05-04 | 题名与版本正确；路线图仅写姓氏且称 first names unknown，需补全名字。 |
| 2601.22444 | 存在 | *Automating Forecasting Question Generation and Resolution for AI Evaluation*；Nikos I. Bosse、Peter Mühlbacher、Jack Wildman、Lawrence Phillips、Dan Schwarz；v1 2026-01-30，v2 2026-03-09 | 题名与 v2 正确，但“Bosse”单作者写法错误/不完整；文中约 95% 自动结算准确率与摘要一致。 |
| 2607.01661 | 存在 | *Diverse Evidence, Better Forecasts: Multi-Agent Deliberation Under Information Asymmetry*；Yuante Li、Yicheng Tao、Kate Zhang、Taozhi Wang、Gefei Gu、Yaxin Zhou；v1 2026-07-02 | **高优先标题证伪**：路线图把框架名 InfoDelphi 当成论文题名；准确题名如左。作者“Li et al.”可用但应补全。 |
| 2512.08296 | 存在 | *Towards a Science of Scaling Agent Systems*；Yubin Kim 等 20 人；v1 2025-12-09，最新 v3 2026-04-08 | 题名/作者次序基本正确，但路线图称 v2、日期 2025-12-17 已不是最新版本；应引用 v3（2026-04-08）或注明所用版本。 |

证据（均查询 2026-07-22）：
- https://arxiv.org/abs/2605.00420
- https://arxiv.org/abs/2601.22444
- https://arxiv.org/abs/2607.01661
- https://arxiv.org/abs/2512.08296

## 二、cutoff-hindcast 占位调查

### 1. 已出现直接占位：Hindcast（高重叠）

**发现占位。** *Hindcast: Replaying Prediction Markets to Evaluate LLM Forecasters*（arXiv:2607.14051，Xiao Ye 等，2026-07-15）直接回放已结算 Polymarket 市场，以每个市场的过去时点 t0 冻结 Reddit 检索，只允许读取 t0 前帖子，并同时相对真实结果与 t0 市场价格评分。其目标正是关闭“检索到事后报道”和“新模型训练已覆盖事件”两条泄露通道。

与 Paper B 的重叠：已结算预测市场回放、历史市场价格基准、时间截止、防泄露，方法学骨架高度重合。差异化空间：Paper B 可明确不把“又一个 hindcast benchmark”作为主贡献，而主攻 **群体规模 × 信息集** 的受控设计、V(x) 曲线、herding、跨模型家族、AMW 充分统计量检验，以及 hindcast→前瞻 Stage 2 的外部验证。Hindcast 摘要未报告 agent-count sweep、规模×信息集 factorial 或群体 herding 因果识别。

证据：
- https://arxiv.org/abs/2607.14051 （查询 2026-07-22）

### 2. 相邻占位与方法学警告

- **FutureSim**（arXiv:2605.15188）：按时间顺序重放 2026-01 至 2026-03 新闻与问题结算，让 frontier agents 预测知识截止后事件。与 Paper B 都使用真实历史时间回放，但其主问题是开放世界适应、搜索、记忆及长时程适应，不是群体规模×信息集或市场隐含概率 V(x)。
- **Simulated Ignorance Fails**（arXiv:2601.13717）：477 个问题、9 个模型显示，仅用 prompt 要模型“忘掉”已知未来不能近似真实无知；结论直接支持 Paper B 必须使用真实早截止底座，不能用提示词倒带。
- **LLMs Can Teach Themselves to Better Predict the Future**（arXiv:2502.05253）：使用在模型知识截止后结算的问题做 outcome-driven DPO，属于前瞻/训练方法占位，不是固定早截止模型对已结算事件的群体能力曲线回放。
- arXiv 关键词 `backcasting LLM predictions` 未返回结果；在本轮检索范围内，除 Hindcast/FutureSim 外，未找到与 Paper B“早截止底座 + 已结算事件 + 群体规模能力曲线”完全同构的项目，故完整同构占位为“未找到，不可考”，不能解释为不存在。

证据（均查询 2026-07-22）：
- https://arxiv.org/abs/2605.15188
- https://arxiv.org/abs/2601.13717
- https://arxiv.org/abs/2502.05253
- https://arxiv.org/search/?query=backcasting+LLM+predictions&searchtype=all&abstracts=show&order=-announced_date_first&size=50

## 三、底座截止证据抽查

### 1. gpt-oss-120b

**核实通过，但需精确措辞。** OpenAI 官方 Hugging Face 模型卡聊天模板明确写 `Knowledge cutoff: 2024-06`，同时称 117B 参数、5.1B active，可在单张 80GB GPU（如 H100/MI300X）运行。模型卡未把 2024-06 明确写作“training data cutoff”；因此路线图应称“官方模型卡/聊天模板声明的 knowledge cutoff 2024-06”，不应无保留改写为经语料审计证明的训练数据截止。

证据：
- https://huggingface.co/openai/gpt-oss-120b （查询 2026-07-22）

### 2. NVIDIA Nemotron-3-Super-120B-A12B

**截止核实通过；语料公开表述须降格。** NVIDIA 官方 NIM 文档明确写：pre-training data cutoff = June 2025，post-training data cutoff = February 2026，训练数据收集期至 2026-02-24；release date 2026-03-11；最低 GPU 要求 8×H100-80GB。故“预训练 2025-06 / 后训练 2026-02”成立。

Nemotron-CC-v2 页面公开可见，但下载文件需登录并接受 NVIDIA Data Agreement，属于 gated/manual access；页面称含 2024–2025 八个额外 Common Crawl snapshots。该页列出 Nemotron 3 Nano 等下游模型，但**单靠该数据集页不能证明 Super-120B 的完整语料谱系或精确截止**。官方 NIM 模型卡另列 pre/post-training dataset collections，且含部分 third-party private datasets；因此“Nemotron-CC 语料公开但 gated”可成立于该数据集本身，但若路线图借此称 Super 的全部语料“公开可证伪”，证据过强，应改成“官方 cutoff + 部分训练数据集合公开/受协议门控，完整语料并非全公开”。

证据（均查询 2026-07-22）：
- https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-super-120b-a12b
- https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-super-120b-a12b.md
- https://huggingface.co/datasets/nvidia/Nemotron-CC-v2
- https://blogs.nvidia.com/blog/nemotron-3-super/ （官方公告未给 cutoff，可作交叉边界证据）

## 四、2026 竞争动态：multi-agent LLM forecasting scaling

### 1. 最接近的新竞争论文

1. **InfoDelphi / Diverse Evidence, Better Forecasts**（arXiv:2607.01661）：在 PolyGym 375 个二元预测题上操纵公共/私有证据分配，并与 single/multi-agent baselines 比较；报告 Brier 改善。它直接占据“信息不对称减少 herding”叙事，但未见 agent 数量 sweep，也没有规模×信息集完整 factorial。对 Paper B 构成信息集轴强竞争、对二维因果设计尚未完全占位。
2. **Bayesian Linguistic Forecaster**（arXiv:2604.18576，ICML AI Forecasting Workshop 2026）：用 K 个独立 trials 做 logit 聚合及分层校准，在 ForecastBench 400 题评估。它占据“多次采样/多 trial scaling + 聚合校准”，但不是多 agent 规模×信息集 factorial，也未操纵信息不对称。
3. **Towards a Science of Scaling Agent Systems**（arXiv:2512.08296 v3，2026-04-08）：260 个配置、六 benchmark、五类架构、三模型家族，系统研究 agent-system scaling，但不是专门的概率事件预测，也未以市场信息集为第二因子。它是一般 scaling 理论与实验的强先例。
4. **InfoDelphi 相邻的 oracle/resolution 工作**：arXiv 搜索返回 *Design and Evaluation of Multi-Agent AI Oracle Systems for Prediction Market Resolution*（arXiv:2605.30802），比较独立聚合与协商共识，但任务是市场**结算判定**而非事前概率预测，不能视为 Paper B 直接占位。

### 2. 占位判断

**未发现完全占位，但窗口已明显收窄。** 截至本轮可核查结果，未找到 2026 论文在概率事件预测上同时做受控的 **agent 规模 × 信息集** 二因素 factorial；最接近的是 InfoDelphi（信息集轴）与 BLF（独立 trial 数/聚合轴）分别占一半，再加一般 agent scaling 论文提供规模规律。Paper B 必须把二因素交互、预注册、跨模型家族、hindcast→前瞻复核和 herding 机制检验作为明确增量，而不能只声称“多 agent 更准”或“多样信息更好”。“未找到”仅限本轮 arXiv/网页检索，不等于不存在。

证据（均查询 2026-07-22）：
- https://arxiv.org/abs/2607.01661
- https://arxiv.org/abs/2604.18576
- https://arxiv.org/abs/2512.08296
- https://arxiv.org/abs/2605.30802
- https://arxiv.org/search/?query=%22multi-agent%22+forecasting+LLM&searchtype=all&abstracts=show&order=-announced_date_first&size=100
- https://arxiv.org/search/?query=LLM+forecasting+%22information+asymmetry%22&searchtype=all&abstracts=show&order=-announced_date_first&size=100

## 五、建议写回路线图时的最小修正（本轮未修改路线图）

1. AMW 改为 NBER Working Paper 33949（2025-06，DOI 10.3386/w33949），删除“期刊/编号 unknown”；期刊版与 SSRN 保留“未找到，不可考”。
2. 更正 arXiv:2607.01661 题名；补全 Bosse 条目的五位作者；将 scaling paper 更新到 v3（2026-04-08）。
3. B0(vi) 明确把 Hindcast arXiv:2607.14051 列作高重叠直接占位，并将贡献收紧为“群体规模×信息集、V(x)、herding、跨模型及前瞻复核”。
4. gpt-oss 用“knowledge cutoff 声明”措辞；Nemotron Super 用官方 NIM cutoff，且将“语料公开可证伪”降为“部分数据集公开但 gated，完整训练谱系并非全公开”。
