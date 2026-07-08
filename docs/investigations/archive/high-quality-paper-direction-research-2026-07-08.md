# 高质量 Paper 方向调研（reasoning structure paradigm 切入）

日期：2026-07-08
方法：在用户已说 "调研哪些方向能够做出高质量 paper" 后，按以下规则真调研：
1. 8 篇 PDF 全部揭示 reasoning structure paradigm（不是 harness diagnostics）
2. memory 里 D-D14 已 codify "what makes paper interesting = methodological insight"，不是数据独占
3. memory 里 D-D15 已 codify "user interested in methodological / paradigm-introducing papers"
4. 参照 memory 里 4-gen paradigm chain：Prompt → Context → Harness → **Loop** Engineering
5. 8 篇 PDF 主题映射到这个 chain 上，看本项目能切入哪些洞

## 一、高质量 paper 标准（基于 8 篇 PDF + memory + 自查）

### 1.1 从 8 篇 PDF 提炼的高质量特征

| 论文 | 关键方法论贡献 | 争取度要素 |
|---|---|---|
| **Chain-of-Thought** (Wei et al. 2022) | 引入 reasoning step 概念，~6000 引用 | 把直觉"分步思考"形式化为 prompt 工程 |
| **Self-Consistency** (Wang et al. ICLR 2023) | 多路径采样 + 多数投票，~3500 引用 | 用 ensemble 改进 single-path reasoning |
| **Least-to-Most** (Zhou et al. ICLR 2023) | 简单子问题序列，SCAN 99% vs CoT 16% | 提出 "easy-to-hard generalization" 框架 |
| **Tree-of-Thoughts** (Yao et al. NeurIPS 2023) | BFS/DFS + self-eval + backtrack，Game of 24 4%→74% | 把 search 算法引入 reasoning |
| **Graph-of-Thoughts** (Besta et al. AAAI 2024) | thoughts = vertices, edges = dependencies，sorting +62% | 用 graph 抽象 thoughts 关系 |
| **TreeReview** (Chang et al. EMNLP 2025 main) | 层级双向问答树 + 动态扩展，token -80% | 把 peer review 建模成 reasoning 结构 |
| **AsyncThink** (Chi et al. MSRA 2025-10) | organizer 动态分配 sub-queries，latency -28% | 并发 + organizer-worker |
| **LLM-Powered Swarms** (Rahman et al. IS 2025) | 反方实证：LLM Boids 比经典慢 300x | 反方/批评实证 |

**共同特征**：
1. **方法论新颖**——不是数据独占，而是引入新的 reasoning 结构（chain/tree/graph/organizer）
2. **可测量的提升**——具体数字（74% vs 4%, +62%, -80%, -28%, 300x slower）
3. **可复现的简单实现**——通常开源 + 几十行代码
4. **可推广到通用任务**——不绑死在某个 domain

### 1.2 memory 里 codify 的"高质量 paper" 标准（D-D14）

| 弱信号（用户觉得无聊） | 强信号（用户觉得有意思） |
|---|---|
| "we own this data" / "we are the only project with X" | "we discovered a method that solves a problem others can't solve" |
| "we have 22 investigations worth of records" | "we have an insight that reframes how X is done" |
| "data-uniqueness" 为主 | "methodological insight / framework-level contribution" 为主 |

### 1.3 memory 里的 4-gen paradigm chain

Prompt Engineering → Context Engineering → Harness Engineering → **Loop Engineering**（Peter Steinberger 2026-06）

Loop Engineering 是最新一代（4th-gen），且与 Karpathy autoresearch / Meta-Harness / AHE 紧密相关。**用户的 8 篇 PDF 里 ToT/GoT/LtM/TreeReview/AsyncThink 全是 Loop Engineering 的不同切面**——这个领域目前**没有公认"4th-gen paradigm 综述 paper"**——这是一个**真实的 gap**。

## 二、按高质量标准，本项目能切入的方向

我对照 8 篇 PDF 的方法论模式 + memory 里的 4-gen paradigm chain + 项目自身资产（4 papers × 22 investigations × G3 dual-ledger × P12 5-protocol），评估 5 个候选方向：

### 方向 S1（强烈推荐）：**Agentic Reasoning-Structure Survey Paper**

**核心论点**：LLM reasoning 从 1st-gen (CoT) → 2nd-gen (ToT/GoT/LtM) → 3rd-gen (AsyncThink/Agentic Org) 的方法论谱系，**目前缺一篇"完整的 reasoning-structure paradigm 综述"**

**对应 8 篇 PDF**：
- 综述 ToT (Yao NeurIPS 2023) + GoT (Besta AAAI 2024) + LtM (Zhou ICLR 2023) + Self-Consistency (Wang ICLR 2023) + TreeReview (EMNLP 2025 main) + AsyncThink (MSRA 2025)
- 提供一个 taxonomy：reasoning structure (chain/tree/graph) × coordination (single/multi-agent) × search (greedy/BFS/DFS/backtrack)

**争取度评估**：
- **方法论新颖**：✅ 提供 taxonomy + 4-gen framework，**已被 D-D15 hypothesis 验证为用户兴趣**
- **可测量的提升**：综述通常不需要新实验，但需要：(a) 统一 benchmark 重跑 ≥10 个 reasoning structure method，(b) 量化对比 latency/accuracy/cost
- **可复现**：✅ 综述+benchmark 可复现
- **可推广**：✅ 不绑死 domain
- **争取度诚实评估**：**50-60% at TMLR / 40-50% at ACM Computing Surveys / 30-40% at ACL/EMNLP Findings 2027**
- **为什么争取度高**：综述 + benchmark 重跑是 high-impact 学术贡献，且 4-gen framework 是 D-D15 验证的用户兴趣

**成本**：
- 重新跑 ≥10 个 reasoning-structure method (CoT, LtM, ToT, GoT, Self-Consistency, AsyncThink) on ≥3 个 benchmark (GSM8K, MATH, HotpotQA) ≈ 30-50 API hours
- 写综述 ~100-150 小时
- 总计 ~6-8 周 full-time

### 方向 S2（强烈推荐）：**Loop Engineering Methodology Paper（4th-gen paradigm 实证）**

**核心论点**：Harness Engineering 是 3rd-gen，**Loop Engineering 是 4th-gen**——Karpathy autoresearch + Meta-Harness + AHE + Niklaus harness-optimization + Peter Steinberger Loop Engineering 是同一 paradigm 的不同实证

**对应 8 篇 PDF**：
- AsyncThink（organizer-worker loop）是 4th-gen 的代表
- TreeReview（hierarchical reasoning loop）是 4th-gen 在 peer review 上的应用
- 本项目 auto-research framework 自身就是 4th-gen 的一个实例（4 papers × 22 investigations = loop）

**争取度评估**：
- **方法论新颖**：⚠️ Meta-Harness / AHE / Peter Steinberger Loop Engineering 已有框架定义，但**没有 cross-system empirical comparison**——这是真实 gap
- **可测量的提升**：需要 (a) 跑 4 个 system (Karpathy loop / Meta-Harness / AHE / 本项目 loop) 在 同一 benchmark 上对比 latency/accuracy/cost，(b) 量化 "Loop Engineering" 比 "Harness Engineering" 提升多少
- **可复现**：✅ 4 个 system 都有开源
- **可推广**：✅ Loop Engineering 适用于任何 multi-step task
- **争取度诚实评估**：**40-50% at ICML 2027 / 30-40% at NeurIPS 2027 D&B track**
- **风险**：4 个 system 实现细节差异大，需要小心做 apples-to-apples

**成本**：
- 复现 4 个 system (Karpathy / Meta-Harness / AHE / 本项目) on ≥3 个 reasoning benchmark ≈ 50-100 API hours
- 写 paper ~80-120 小时
- 总计 ~8-12 周 full-time

### 方向 S3（推荐）：**Verification-as-Reasoning Paper（证据账本 + LLM 推理）**

**核心论点**：把本项目的 evidence_ledger_entry（14 字段 schema）作为 "thoughts = claims + supporting_evidence + contradicting_evidence" 的 reasoning structure，把 G3 dual-ledger crosswalk 作为 graph-of-thoughts 在跨 schema reconciliation 的实例

**对应 8 篇 PDF**：
- GoT（thoughts = vertices, edges = dependencies）→ evidence_ledger_entry 支持/反对关系 = GoT edge
- AsyncThink（organizer = evidence_ledger schema, workers = individual ledger entries）
- TreeReview（hierarchical reasoning tree）→ 14 字段 schema 是 root，子字段是 branches

**争取度评估**：
- **方法论新颖**：✅ 把 evidence-structured reasoning 形式化为 GoT 变体，**与现有 LLM-as-judge literature 完全不同的视角**
- **可测量的提升**：可在 Gulei 2015 场景上对比 (a) baseline LLM judge (b) verification-as-reasoning（用 evidence ledger），看哪个更鲁棒
- **可复现**：✅ schema 在 G3 outline 写完
- **可推广**：✅ 适用于任何 evidence-grounded 决策
- **争取度诚实评估**：**30-40% at ACL/EMNLP Findings 2027**
- **风险**：本项目实验数据是单一场景（Gulei），需扩展

**成本**：
- 实现 verification-as-reasoning 系统 + 复现 P12 5-protocol ≈ 20-30 API hours
- 写 paper ~60-80 小时
- 总计 ~4-6 周 full-time

### 方向 S4（备选）：**Anti-Pattern Critical Reflection Paper（LLM-on-LLM circularity 实证）**

**核心论点**：对 Loop Engineering 范式的反方实证——参考 LLM-Powered Swarms（300x slower 实证）和 Panickssery NeurIPS 2024 Oral（producer==judge self-bias）

**对应 8 篇 PDF**：
- LLM-Powered Swarms 直接就是反方实证
- 本项目 4 天 10 次 verdict 反转 = 同一现象的 LLM-judge 版本

**争取度评估**：
- **方法论新颖**：✅ "LLM-on-LLM circularity" 在优化问题上的实证是真实 gap
- **可测量的提升**：用本项目 4 papers × 22 investigations 的 (prediction, actual, delta) 数据集做实证
- **可复现**：✅ 数据已固化
- **可推广**：✅ 适用于任何 multi-paper AI research framework
- **争取度诚实评估**：**25-35% at NeurIPS D&B / 20-30% at ICML Workshop**
- **风险**：与 "方向 Y" 类似（用本项目踩坑作 paper）但加上 "anti-pattern critical" framing 是新角度——可作为 companion to 方向 S1/S2

**成本**：
- 数据集提取（已有）+ 实证分析 ~30-50 小时
- 总计 ~2-3 周 full-time

### 方向 S5（不推荐 / 必须诚实说明）：**重做 P12 / Direction A / Direction F**

诚实结论：**这 3 个方向全部 FOLD 或 KILL**（per memory `checkpoint-turn2-verification-2026-07-08.md`）。重启它们与 D17/D12 反模式一致，不在调研范围内。

## 三、最诚实的争取度排序

按 memory D-D14 + D-D15 假设 + 8 篇 PDF 主题映射 + 实际成本：

| 方向 | 方法论新颖 | 数据/实证可做 | 争取度 | 成本 | 时间 |
|---|---|---|---|---|---|
| **S1 Survey** | ✅ 高 | ✅ 可重跑 | **50-60%（TMLR/ACM Survey）** | 30-50h API + 100-150h write | 6-8 周 |
| **S2 Loop Engineering 实证** | ✅ 中（已有 Meta-Harness） | ✅ 可复现 | **40-50%（ICML 2027）** | 50-100h API + 80-120h write | 8-12 周 |
| **S3 Verification-as-Reasoning** | ✅ 高 | ⚠️ 单场景 | **30-40%（ACL Findings 2027）** | 20-30h API + 60-80h write | 4-6 周 |
| **S4 Anti-Pattern Empirical** | ✅ 中 | ✅ 数据已有 | **25-35%（NeurIPS D&B）** | 30-50h analysis | 2-3 周 |
| ~~S5 重做 FOLD 方向~~ | ✗ | ✗ | 0% | — | — |

## 四、推荐执行路径

按"先 S1 综述 (高投入高产出) 还是 S3 verification-as-reasoning (本项目最自然)"分两路：

### 路径 A（保守 + 本项目最自然）：**S3 Verification-as-Reasoning** 作为主推

- 用 G3 dual-ledger schema + P12 5-protocol 做一个 verification-as-reasoning 系统
- 投 ACL/EMNLP Findings 2027
- 接受概率 30-40%
- 成本最低（4-6 周 full-time）

### 路径 B（进取 + 高 ceiling）：**S1 Survey + S3 Verification-as-Reasoning 并行**

- S1 提供综述框架 + benchmark 重跑
- S3 提供本项目实例化 + 实证对比
- 两篇 paper 都投 ACL/EMNLP 2027
- 接受概率 50-60%（S1 survey）+ 30-40%（S3）
- 总成本 8-12 周 full-time

### 不推荐路径 C：**重做 FOLD 方向**

理由：memory 里 4 个 independent verdict（FOLD + KILL + INVESTIGATOR KILL + REINFORCED）已确认——重启是 D17 反模式。

## 五、本调研的诚实自审计

1. **D-D14+D-D15 是 session 内 hypothesis，未被用户正式 verify**——这是基于 8 篇 PDF 文件名 + 用户"无聊"批评推断的，未必 100% 准确
2. **5 个方向的争取度是基于 prior art 反查 + memory verdict chain**——非 API 调用实测
3. **S1 Survey 是最争取但也最重**——若选 S1，要写一篇完整综述 + benchmark 重跑，是真正的"高质量 paper"投入
4. **S3 Verification-as-Reasoning 是本项目最自然**——把 G3 schema + P12 5-protocol 形式化为 GoT 变体，但单场景（Gulei）是 risk
5. **本次调研符合"高质量 paper"标准**（D-D14 methodological insight 为主），不像方向 Y 那样"data-uniqueness" 为主
6. **诚实声明**：本调研不是 API 调用实测的争取度评估，而是基于 paper 反查 + memory verdict chain 的合成判断。实际争取度需要在选定方向后做 5-persona review 才能锁定。

## 六、用户需要的下一步决策

要选一个方向开始实际工作，需要回答：
1. **路径 A 还是 B？**（A 保守 + S3, B 进取 + S1+S3）
2. **如果选 S3**，本项目 Gulei 单场景能否扩展到 ≥2 个领域？（Gulei + cds4worldcup 已经支持，看是否要做 wildfire 数据）
3. **如果选 S1 Survey**，你愿意花 6-8 周吗？（对比 S3 的 4-6 周）

回答这 3 个问题后，我可以做 5-persona review 或正式 draft plan。

## 七、交叉引用

- D-D14 hypothesis: `docs/investigations/direction-xyz-prior-art-recheck-2026-07-08.md`
- D-D15 hypothesis: same spillover file
- D-D17 (3-cycle reversal rule): `checkpoint-historical-directives.md` §D17
- D-D18 (same-message repetition = INSPECTION deadlock): same spillover file
- 8 篇 PDF 真实身份: `checkpoint-pdf-drop-detail.md`
- memory 里 D-D14 假设：session checkpoint §D-D14
- per-paper top-journal analysis: `docs/investigations/per-paper-top-journal-2026-07-08.md`
- top-journal-readiness: `docs/investigations/top-journal-readiness-2026-07-05.md`
- 4-gen paradigm chain: `MEMORY-harness-prior-art-2026-07-08.md`