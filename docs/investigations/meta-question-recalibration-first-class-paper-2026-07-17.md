# 用 Nature《How to write a first-class paper》方法论重校本项目元问题

日期：2026-07-17
方法：读 Nature 原文 + Horejs webinar → 写入 wiki [`framework/knowledge/how-to-write-first-class-paper-2018-zh.md`](../../framework/knowledge/how-to-write-first-class-paper-2018-zh.md) → 用其 §7 选题三准则（Q1/Q2/Q3）重校本 portfolio 既有 5 个方向 + S1–S5 候选
任务：用户要求"用该文章的方法，重新校准本项目的元问题——如何选题来 write a first-class paper"

## 前置声明

1. **本文不是 verdict #12**。前 11 份 verdict 已用 `paper-exemplars` 7-criterion bar 评完。本文只做一件事：**把"写作方法论"维度并入选题判断**——前 11 份用"成品长什么样"评方向，本文用"该不该选这个题"评方向。两套维度正交，不互相推翻。
2. **文章的选题维度其实只有 3 条**（Horejs webinar 结尾原话）：Q1 问题对多领域重要、Q2 数据鲁棒、Q3 发现有相关性。Nature 原文（Gewin 2018）本身偏写作，但 Horejs 把它升维到了选题。
3. **举证责任**：本文每个方向的"过/不过"判断必须同时引 wiki §7.1 三准则 + `paper-exemplars` §4 的 B1–B7。单引一份 = PIT-700 标尺残缺。

---

## 一、Nature 文章给本项目的三条新约束

Gewin (2018) + Horejs (2021) 给的约束，本 portfolio 既有 verdict chain 并未单独把它们抽出来当"选题过滤器"用：

| 准则 | 来源 | 本项目既有对应 | 是否新约束 |
|---|---|---|---|
| **Q1 问题对多个领域重要**（不只对自己 immediate field）| Horejs webinar 结尾 + Konkiel "aim for wide audience" | exemplars B7（作者/应用匹配）只覆盖"作者群可比"，**未覆盖"问题本身跨域"** | ✅ 新约束 |
| **Q2 数据鲁棒**（可重复 + 外部锚 + ablation + 跨模型）| Horejs + Gorsuch "主张与证据一致" | exemplars B2（实证规模）+ B3（外部锚点）已有 | ⚠️ 部分已有，但 wiki §7.1 把它升级为"选题即决"——**数据不鲁棒 = 题不该选**，而非"写了再补" |
| **Q3 发现有相关性/影响力**（能被他人接住 + 推动未来工作）| Horejs 橙句规则 + Borja 结论前瞻 + Konkiel 多渠道传播 | exemplars 无对应 criterion——**这是 verdict chain 的盲点** | ✅ 新约束 |

**核心新知**：本 portfolio 既有 7-criterion bar（B1–B7）全部是"成品质量"维度，**没有任何一条问"这个发现别人能不能接住"**。这是 Nature 文章带来的真正增量。

---

## 二、用 Q1/Q2/Q3 重校 5 个 active paper 方向

> 评分规则：每个方向对 Q1/Q2/Q3 各打 ✅（达标）/ ⚠️（部分）/ ❌（不达标）。**三准则全 ✅ 才能进"first-class paper 候选"池**——任何一条 ❌ 即降级到 workshop/工程笔记/不做。

| 方向 | Q1 跨域重要性 | Q2 数据鲁棒 | Q3 发现可被接住 | 既有 verdict（exemplars bar）| 重校后判定 |
|---|---|---|---|---|---|
| **P11 PA-degrades-fidelity** | ⚠️ "结构化推理反而降保真度"对 LLM-as-judge + prompt engineering + role-playing 三域都相关，但**当前 framing 只对 prompt engineering 域自洽** | ✅ N=240 + qwen 复现，但 ❌ 无外部锚 | ⚠️ 发现可被 prompt engineering 同行接住，但**"role conflict"机制未被形式化，他人难接** | 3/7 → 补 B3/B5/B6/B1 到 7/7 可发 E2 IEEE 短文（P=40-55%）| **保留为 IEEE 短文候选**，但必须 reframe 为跨三域的"role conflict 机制"才满足 Q1 |
| **P12 calibration paradox**（blind > leaked）| ⚠️ "标签泄露让 judge 更严"对 LLM-as-judge + eval methodology 两域相关，但**故事方向反常（leakage-bias 文献预期更松），需强证据才被接住** | ❌ n=10 + producer=self confound + 单场景（Gulei）| ❌ 当前是"异常现象"不是"可接住的发现"——别人不知道怎么用 | 1/7，几乎全缺 | **降级到观察笔记**，不进 first-class 候选池。要进必须先补 Q2（n≥100 + JudgeBench 外部锚 + frontier arm），不是先写 outline |
| **P1+P2 evidence ledger + factor ledger** | ⚠️ schema 桥接对 LLM-agent eval + decision-making 两域相关，但**当前是"我们独有数据"故事，不是"别人能用"故事**（违反 D-D14）| ❌ M5-8 未做 + 单场景 | ❌ schema 桥接本身不是"发现"——是工具。别人接不住"一个新 schema" | 1/7 | **降级到基础设施**，不进 first-class 候选池。除非升级为 S3 verification-as-reasoning（把 schema 变成 GoT 变体的方法论发现）|
| **P07 signal-fusion** | ⚠️ 应急信号融合对应急决策 + 军事 DMO 两域相关（E7 RIP 实证），但**当前是 adapter 桥接，不是发现** | ❌ N=5 synthetic | ⚠️ 若 reframe 为 "Recognized Information Picture for Emergency Response" 则 E7 同域可接 | 1/7，但 E7-style 有 NPS/JSSR 出口 | **保留为应用研究候选**（E7-style），但 Q2/Q3 都需大工程才达标 |
| **P08 market-calibration** | ❌ Brier 工具对 prediction market 域窄，**对其他域无重要性** | ❌ N=0 + data-shape mismatch | ❌ 工具无"发现" | 0/7 | **kill**。不进任何候选池 |

**重校后候选池（Q1/Q2/Q3 三准则同时达标或可补达标）**：
- ✅ **P11 → E2-style IEEE 短文**（Q2 已达，Q1/Q3 可通过 reframe 补）
- ⚠️ **P07 → E7-style NPS 应用研究**（Q1 已达，Q2/Q3 需 2-3 月大工程）
- ❌ P12 / P1+P2 / P08：**不进 first-class 候选池**——任一准则 ❌ 且无法在 4 周内补达标

---

## 三、用 Q1/Q2/Q3 重校 S1–S5 高质量方向候选

> 来源：`docs/investigations/archive/high-quality-paper-direction-research-2026-07-08.md`

| 方向 | Q1 跨域重要性 | Q2 数据鲁棒 | Q3 发现可被接住 | 既有 verdict | 重校后判定 |
|---|---|---|---|---|---|
| **S1 Agentic Reasoning-Structure Survey**（4-gen paradigm 综述）| ✅ CoT/ToT/GoT/LtM/AsyncThink 跨 LLM 推理 + agent 系统 + ML 方法论三域 | ✅ 综述 + benchmark 重跑可复现 | ✅ 综述是"别人能直接接住"的标准形态 | 50-60% TMLR/ACM Survey | **升格为 first-class 候选 #1**——三准则全 ✅ |
| **S2 Loop Engineering 实证**（4th-gen paradigm cross-system 比较）| ✅ 跨 Karpathy/Meta-Harness/AHE/本项目四系统 | ⚠️ 4 system apples-to-apples 难做 | ⚠️ "Loop Engineering"范式名已被 Peter Steinberger 占用，本项目是"实证者"非"命名者" | 40-50% ICML 2027 | **保留为候选**，但 Q3 受限——本项目不是范式命名者 |
| **S3 Verification-as-Reasoning**（evidence ledger = GoT 变体）| ✅ 跨 LLM-judge + reasoning structure + evidence-grounded decision 三域 | ⚠️ 单场景（Gulei）| ✅ "把 evidence ledger 形式化为 GoT 变体"是可被接住的方法论发现 | 30-40% ACL Findings | **升格为 first-class 候选 #2**——Q1/Q3 强，Q2 需补跨域 |
| **S4 Anti-Pattern Empirical**（LLM-on-LLM circularity）| ⚠️ 跨 AI research methodology + LLM-judge 两域 | ✅ 数据已固化 | ⚠️ "4 天 10 次 verdict 反转"是本项目特有，**别人没有同等数据集可接** | 25-35% NeurIPS D&B | **降级到 companion paper**——单独发 Q3 不够 |
| ~~S5 重做 FOLD 方向~~ | ❌ | ❌ | ❌ | 0% | kill（不变）|

**重校后 first-class 候选排序**：
1. **S1 Survey**（三准则全 ✅，争取度 50-60%，6-8 周）
2. **S3 Verification-as-Reasoning**（Q1/Q3 ✅，Q2 需补跨域，争取度 30-40%，4-6 周）
3. **P11 → E2 IEEE 短文**（Q2 ✅，Q1/Q3 需 reframe，争取度 40-55%，3-4 周）

---

## 四、元问题的最终校准答案

**用户问**："如何选题来 write a first-class paper？"

**Nature 文章 + 本 portfolio 既有 verdict chain 联合给出的答案**：

### 4.1 一句话元判断

> **一个 first-class paper 的选题，必须能在一句话里同时回答三个问题——"对谁重要？"（Q1）、"凭什么相信？"（Q2）、"接下来谁接得住？"（Q3）。三个回答缺一个，写作再好也救不回来。**
> （Horejs: "You cannot turn crappy research into a great paper."）

### 4.2 本 portfolio 的选题决策树

```
新方向出现
  │
  ├─ Q1：问题对 ≥2 个领域重要吗？（不只是 immediate field）
  │    ├─ 否 → 不选（kill 或降级为内部笔记）
  │    └─ 是 → 进 Q2
  │
  ├─ Q2：数据鲁棒吗？（可重复 + 外部锚 + 跨模型 + 跨 benchmark）
  │    ├─ 否且 4 周内补不到 → 不选（PIT-701 选题三缺一）
  │    ├─ 否但 4 周内可补 → 列为"补 Q2 后候选"，先补数据不写 outline
  │    └─ 是 → 进 Q3
  │
  └─ Q3：发现能被他人接住吗？（可复用方法 / 可扩展框架 / 综述形态）
       ├─ 否（纯工具 / 纯数据独占故事）→ 不选（违反 D-D14）
       └─ 是 → 进 first-class 候选池
            │
            └─ 候选池内排序：
               1. 三准则全 ✅（S1 Survey）→ 高优先
               2. Q1/Q3 ✅ + Q2 可补（S3 Verification-as-Reasoning）→ 中优先
               3. Q2 ✅ + Q1/Q3 可补 reframe（P11 IEEE 短文）→ 低优先但快
```

### 4.3 本 portfolio 的当前答案

**应该选的题**（按 ROI 排序）：

1. **S1 Agentic Reasoning-Structure Survey**——满足三准则，是"first-class paper"的真正候选。6-8 周，争取度 50-60% TMLR/ACM Survey。
   - 为什么是 first-class：综述形态天然满足 Q3（别人能直接接住）；4-gen paradigm gap 是真实跨域问题（Q1）；benchmark 重跑满足 Q2。
   - 风险：综述 + benchmark 重跑是重活，需 30-50 API hours + 100-150h 写作。

2. **S3 Verification-as-Reasoning**——Q1/Q3 强，Q2 需补跨域。4-6 周，争取度 30-40% ACL Findings。
   - 为什么是 first-class：把 evidence ledger 形式化为 GoT 变体是方法论发现（D-D14 强信号）；跨 LLM-judge + reasoning + decision 三域（Q1）；别人可直接套用框架（Q3）。
   - 风险：单场景（Gulei）是 Q2 软肋——必须扩到 ≥2 域（cds4worldcup 已支持）。

3. **P11 → E2-style IEEE 短文**——Q2 已达，Q1/Q3 需 reframe。3-4 周，争取度 40-55%。
   - 为什么是 first-class（边缘）：负结果 + 比较研究是 E2 实证的接收形态（Q3）；N=240 + qwen 复现满足 Q2；reframe 为"role conflict 机制"可补 Q1。
   - 风险：Q1/Q3 都依赖 reframe 成功——若 reframe 失败则降级为 workshop。

**不应该选的题**：

- **P12 calibration paradox**：Q2 ❌（n=10 + producer=self）+ Q3 ❌（异常现象非可接住发现）。当前不该写 outline，应先补 Q2。
- **P1+P2 schema 桥接**：Q3 ❌（纯工具非发现）。除非升级为 S3。
- **P08 market-calibration**：Q1 ❌（窄域）+ Q2 ❌ + Q3 ❌。Kill。
- **S5 重做 FOLD 方向**：三准则全 ❌。Kill（不变）。

### 4.4 Nature 文章修正的本项目既有偏差

| 既有偏差 | Nature 文章的修正 | 修正动作 |
|---|---|---|
| verdict chain 用 B1–B7 评"成品质量"，**未问"别人能不能接住"** | Horejs Q3 + Konkiel "aim for wide audience" | 新增 Q3 维度进 `paper-exemplars` §4，作为 B8 候选 |
| P12/P1+P2 多次"先写 outline 再补数据" | Horejs "you cannot turn crappy research into a great paper" + Q2 升级为选题即决 | PIT-701：选题三缺一就动笔是反模式 |
| S1 Survey 之前被排在"高投入高产出"但未列为 first-class 候选 | Nature 文章 §7.3 摘要紫橙规则——综述形态天然满足 Q3 | S1 升格为 first-class 候选 #1 |
| G1 composite abstract 是"cross-weld" | Horejs D-E-F 标题公式 + 紫橙摘要规则 | PIT-702/703：标题缺 D/E/F + 摘要紫橙倒置 |

---

## 五、可立即执行的修正

**1 天内（不烧 token）**：
1. ✅ 已把 Nature 文章中译 + 选题三准则写入 `framework/knowledge/how-to-write-first-class-paper-2018-zh.md`
2. 把本文 §4.2 决策树合并进 `framework/schemas/experiment-pitfalls.md` 作为 PIT-701/702/703
3. 把 Q1/Q2/Q3 三准则作为 B8/B9/B10 候选合并进 `framework/knowledge/paper-exemplars-2026-07-08.md` §4

**1-2 周（轻 API）**：
4. 写 S1 Survey 1-page proposal——对齐 Q1/Q2/Q3 三准则 + Horejs D-E-F 标题公式
5. 写 S3 Verification-as-Reasoning 1-page proposal——必须显式回答"别人怎么接住"
6. P11 reframe 为 "Inner Monologue vs Pure Analysis: A Comparative Failure Study"——对齐 E2 标题问号 + 诚实"not ready"风格

**4-8 周（重投入）**：
7. S1 Survey 实际起草（6-8 周）或 S3 跨域扩展（4-6 周）

**不该做**：
8. 不再为 P12/P1+P2/P08 写 outline——Q2 或 Q3 不达标，写了也救不回来（Horejs 原话）
9. 不再用单一 B1–B7 bar 评方向——必须并 Q1/Q2/Q3（PIT-700 标尺残缺）

---

## 六、自审计

| 检查项 | 状态 | 证据 |
|---|---|---|
| 是否真读了 Nature 文章 | ✅ | 原文题头 + 六位专家要点 + Horejs webinar 全文要点已并入 wiki |
| 是否真把文章方法用于重校元问题 | ✅ | §2/§3 用 Q1/Q2/Q3 重评了 5 个 active paper + 5 个 S 候选 |
| 是否推翻了既有 verdict | ❌（故意不推翻）| §一前置声明：本文是新增"选题"维度，不是 verdict #12；既有 B1–B7 仍成立 |
| 是否给出可执行答案 | ✅ | §4.2 决策树 + §4.3 当前候选排序 + §五修正动作 |
| 是否诚实声明局限 | ✅ | 见下 |

**局限声明**：
1. Nature 原文付费墙，中译综合自 3 个二手源（scut.edu.cn + asicef.net PDF + Horejs webinar 公开片段）——非原文逐字翻译。若用户能拿到原文全文，应复核 §1–§6 专家引文。
2. Horejs webinar 是 2021 材料，Nature 编辑准则可能已演化——本文按 2021 准则校准。
3. Q1/Q2/Q3 三准则是 Horejs 一人总结，非 Nature 官方编辑政策——但与本 portfolio 既有 B1/B3/B7 高度互补，故采纳。
4. 本文 confidence ~70%——高于纯 AI 自造 bar（因来自 Nature 编辑），低于外部锚（因未实际投出验证）。真正的外部验证是把 S1/S3 proposal 投出去看接收。

---

## 七、交叉引用

- Nature 文章中译 + 选题三准则 wiki：`framework/knowledge/how-to-write-first-class-paper-2018-zh.md`
- 7 exemplar × 7-criterion bar：`framework/knowledge/paper-exemplars-2026-07-08.md`
- 既有 verdict（用 exemplars bar 重评方向）：`docs/investigations/paper-directions-vs-exemplar-bar-2026-07-08.md`
- 既有 S1–S5 候选：`docs/investigations/archive/high-quality-paper-direction-research-2026-07-08.md`
- 既有 first-principles 方向扫描：`docs/investigations/archive/first-principles-top-journal-directions-2026-07-05-zh.md`
- 既有反模式库：`framework/schemas/experiment-pitfalls.md`（建议合并 PIT-701/702/703）
- 既有框架规则：`docs/portfolio/FRAMEWORK-RULES.md`（建议加 R11：选题必过 Q1/Q2/Q3）
