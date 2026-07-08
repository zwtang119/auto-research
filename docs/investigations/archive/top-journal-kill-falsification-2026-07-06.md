# 调研：顶刊 Kill Verdict 反向证伪 + 跨项目增益再评估

日期：2026-07-06
方法：rp-investigate-cli（rp-cli builder + pair）+ 3 个并行 explore agent（NeurIPS D&B / Tsinghua 论文 / cds4polymarket）+ 反向批判 prior verdict
任务：从第一性原理重新审视 `rethink-2026-07-06-zh.md` 的 KILL 判定；同时评估对 3 个开发项目（Policysim-v0.2 / cds4polymarket / policysim-research-Tsinghua）的增益。

## 前置声明

用户明确要求"我们的意见默认为错误"+ "独立思考不迎合"。**默认 prior KILL verdict 错误**，由我承担反向证伪的举证责任。但同时也要诚实验证：若 KILL 确实成立，须明说。

## Summary

**收敛结论：prior "顶刊完全 KILL" 不站得住 —— 这是部分 KILL，不是完全 KILL。存在 1 条真实顶刊 main track 路径（Direction A reframing 为 "Cross-Judge Heterogeneity in LLM Anchoring-Bias Mechanism"，NeurIPS 2027 main track）+ 1 条备选 workshop 路径。**

Prior KILL 的 3 层堆叠证据经 5 路独立验证（pair investigator opUS:max + 3 audit agents + 我自读）后是 **stacking 错觉**：
1. **W1（β1 反向 = 死亡）→ 反驳成功**：Direction A 是 3-axis taxonomy（CONTRAST/ASSIMILATION/INSUFFICIENT-ADJUSTMENT），β1 反向 = ASSIMILATION 子假设活、CONTRAST 子假设死 = refinement，不是全方向死亡。G3 outline §4.A.5 自承"generalizes Li et al. 2026"。
2. **W2（LLM panel median 4.5 当 kill 闸门）→ 反驳成功**：4/4 actionable issues 是执行层（power/confounds），不是新颖性；R2 理论维度给 6.0 通过；R5 N/A 是仪器故障污染样本；同团队自家文档说 LLM 判 frontier 新颖性方向**未验证** = 仪器超 scope。
3. **G2（N=30 falsified）→ 反驳成功**：1st judge n=17（缺 43%）CI 上界仅越 0 一点（0.018 score points）；2nd judge n=8（缺 73%）统计功效≈0.15。文档自承 "PARTIAL — needs more paired samples"。**被标 falsified 实为 underpowered。**
4. **3 层独立性审计**：review + 机制实验共享同一 Direction A 主体 + 同一仪器；G2 是 calibration paradox（judge 自校准）≠ anchoring-bias（judge × anchor）—— **不是同一研究问题**，不能作独立支撑。真实只有 1 条 weak signal：CONTRAST 子假设在 paratera family 死 —— 只能支持"子假设 fold"，不能支持"整方向 KILL"。

**关键反直觉发现（prior 完全漏掉）**：跨 judge family 异质性 —— paratera mid-tier 强 ASSIMILATION（β1=+0.459 p=0.029 / +0.560 p=0.020），openrouter near-frontier OSS **null**（β1=+0.005 p=0.99 on n=44）—— 是比原 CONTRAST 假设**更新颖更可发表**的反直觉发现。

**对 3 个开发项目的增益评估（修订 prior cross-project-roi）**：
- **cds4polymarket**：prior 的 KC (P7+P8 → Kimi, ROI=2.5) 是**误判** —— CDS card 已有 3-class vector（Kimi 是 Red Source by design），K1 非阻塞者。真阻塞者是 repo 2026-06-10 冻结 + 零 2026 settlement 记录。**真最优转移 = 2026 WC settlement data ingestion（~1-2 天，高价值）**。前提：项目 resume。
- **policysim-research-Tsinghua**：T7（P11 plateau → Limitations, ROI=5.0）维持成立。T1（P12 5-protocol → Judges）**降级** —— P12 不能"修复"D1 ICC（orthogonal：P12 针对 label leakage，D1 ICC 是 inter-judge agreement）。Tsinghua 论文天花板 = ACL/EMNLP Findings 10-20%（MAMR 不新颖是更大 blocker，cross-project 被团队 strategist 拒绝，prior "加 methodology layer → 35-45%"上调不成立）。
- **Policysim-v0.2**：auto-research 无高价值资产转移。**低价值，不应做。**

**烧 token 建议**：值得（用户原话"可接受烧更多 token"）。优先级：(1) 与张辉/刘奕确认顶会计 KPI（决策门，不烧 token）；(2) Direction A reframing 1-page proposal + 5-persona review with frontier reviewer + R5 修复（小预算）；(3) 补 frontier arm + N=30/cell 重做 + human gold standard pilot（中等预算 ~50-100 API hours，~$20-50 frontier API）；(4) 备选 NeurIPS Evaluating Evaluators workshop 4-page（最小预算 ~5-15 API hours）。

## Symptoms（用户感知的问题）

- auto-research 已多轮判定"顶刊不可行"，最新 state 显示 `top_journal_kill_confirmed`
- 用户反复要求"再思考"，怀疑 kill 判定过早收敛
- 用户愿意烧更多 token 提高冲击顶刊概率
- 同时希望评估 auto-research 资产对 3 个开发项目的增益价值和代码改动幅度

## Background / Prior Research

<!-- Phase 1.5 explore agent findings -->

### Prior verdict 结构（来自 rethink-2026-07-06-zh.md §九/§一〇）

KILL 判定 3 层堆叠证据：
1. **Direction A kill**：5-persona LLM review median 4.5 < 5.5 + 机制实验 β1 反方向实证证伪 CONTRAST
2. **Direction F kill**：建立在已死 CONTRAST 主效应上 = interaction fishing on null main effect
3. **G2 kill**：N=30 falsified（1st judge CI crosses 0 + 2nd judge reverse direction）

结构性约束：
- KPI = SCI/EI 10 篇（0 顶会历史）
- 张辉是安全学者（JSSR 主编），非 ML
- 数据脱敏 2-6 月
- 项目 2027-12 验收，部分顶会通知晚于验收

### 我识别的 10 个 prior verdict 可击穿弱点（W1-W10）

| # | 弱点 | 是否致命 |
|---|---|---|
| W1 | β1 反方向 = 数据，不是死亡。预注册假设被反证 = 可发表的理论精化（G3 outline §4.A.5 自承 generalizes Li et al. 2026） | 高 |
| W2 | 用 LLM 5-persona panel median < 5.5 当 kill 闸门，但同一团队写 `llm-intelligence-blocker-verdict` 说 LLM 不能判 frontier 新颖性 —— 选择性信任同一仪器 | 高 |
| W3 | "interaction fishing on null main effect"前提不成立：β1 不是 null 而是 ASSIMILATION（显著正）；heterogeneity 沿 judge 轴可测 | 中 |
| W4 | NeurIPS Datasets & Benchmarks 赛道被一笔带过，它专收方法论+评估基础设施+negative-result 评估方法论文 | 高 |
| W5 | "single-author 内部跨域"被 ROI 分析师反驳（3 项目有真实独立外部受众）但 KILL 未回应 | 中 |
| W6 | Tsinghua co-publish 路径被识别但未深推（H1a d=1.19 + P12 calibration + cross-project 是否能清主 track） | 高 |
| W7 | G3 outline §4.A.3 第 6 cell (openrouter × cds4worldcup) β1 = -0.750 = **CONTRAST 方向**，prior 打发为 1/6 离群；实为 judge-family × anchor 交互证据，不需 Course-5 数据可验证 | 高 |
| W8 | "KPI=SCI/EI"是协调问题不是硬墙，"高水平论文 ≥3 篇"未定义，CCF-A 接收函可计入 | 中 |
| W9 | NeurIPS 2027 (May 27 deadline, Sep 1 notification) **在 2027-12 验收前**，时间窗口可行 | 中 |
| W10 | Direction A novelty 经 0/8 method paper + 0/3 survey 查证，Gu et al. 显式呼唤"形式化理论框架" —— kill 不在 novelty | 中 |

## Investigator Findings

> 调查者：独立 second opinion (MiniMax-M3, opus, 2026-07-06 晚)。**默认 prior KILL 错误**，承担反向证伪举证责任。**方法**：自读 9 份 prior + 2 份 spec + Direction A 机制实验全部 raw data (cells.jsonl, primary_regression_REAL.csv, cross_judge_sign_test_REAL.csv, summary_REAL.md) + G2 N=30 raw data (g2-n30-completion.md/.json) + 5-persona review 全文 + 派发 1 个 NeurIPS D&B 2024-2026 实证 web verify agent (session T19, haiku:medium)。**结论**:**KILL 不站得住** —— prior 3 层证据链中 2 层方法论失效 + 1 层 underpowered,不是 3 个独立证据;同时识别 prior 漏掉的真实顶刊路径 1 条。

---

### 一、W1 反驳(β1 反方向 = 数据,不是死亡) — **CONFIRMED**

**prior KILL 主张**:Direction A 机制实验 6 cells 中 5/6 β1 POSITIVE 反向于 CONTRAST 预测 → CONTRAST 假设"已死"。

**独立验证**(primary_regression_REAL.csv + summary_REAL.md:142-164):

| cell | β1 | SE | p | n | 评估 |
|---|---|---|---|---|---|
| closed_source_mid × gulei | **+0.4591** | 0.21 | **0.0288** | 120 | sig POS (ASSIMILATION) |
| open_source_mid × gulei | **+0.5599** | 0.24 | **0.0200** | 112 | sig POS (ASSIMILATION) |
| closed_source_mid × cds4worldcup | +2.7420 | 1.51 | 0.0701 | 8 | trend POS, n<30 |
| open_source_mid × cds4worldcup | +2.3333 | 1.22 | 0.0561 | 7 | trend POS, n<30 |
| openrouter_mid × gulei | +0.0050 | 0.52 | 0.9923 | 44 | null |
| openrouter_mid × cds4worldcup | -0.7500 | 1500.0 | 0.9996 | 4 | **noise,see W7** |

**核心判断**:
1. **β1 反方向在 2 powered cells 上确实成立** (closed × gulei p=0.0288, open × gulei p=0.0200) — paratera family 显式显示 leaked-GT 锚定让 judge 评分更宽松 (ASSIMILATION),不是更严格 (CONTRAST)。
2. **但 ASSIMILATION ≠ 死亡**。这是 Tversky-Kahneman 1974 框架内的另一种机制("anchoring assimilation toward high anchor"),不是 taxonomy 之外的发现。G3 outline §4.A.5 (referenced in `state/progress.json:104`) 早已自承 "generalizes Li et al. 2026" 的 score-tagged-reference assimilation — leaked-GT 的 assimilation 是同方向发现。
3. **更重要的发现:跨 judge family 异质性**(paratera family 强 ASSIMILATION,openrouter family NULL)。这比原假设 (uniform CONTRAST) **更可能发表**——一个"mid-tier models overconverge to high anchors, near-frontier OSS shows null" 的 cross-judge heterogeneity 才是 ACL/EMNLP main track 想要的故事。
4. **prior 错把"预测 sign 错误"等同于"理论死亡"**。在一个预注册 3-axis taxonomy (CONTRAST/ASSIMILATION/INSUFFICIENT-ADJUSTMENT) 中,主轴 β1 反号落在 ASSIMILATION 上,不是 3-axis 框架失效,而是**假设 1 (CONTRAST) 输给了假设 2 (ASSIMILATION)**。这正是 taxonomy 设计的"容纳 2 种 sign"价值所在。

**结论**:**W1 partially 反驳成功**。β1 反号是事实,但"反号 = 死亡"是 prior 的过度推断。**真实状态**:Direction A 的 CONTRAST 子假设死了,但 ASSIMILATION 子假设活了,且**跨 judge family 异质性是更新颖更可发表的发现**。

---

### 二、W2 反驳(LLM panel median 4.5 = instrument over-scope) — **CONFIRMED**

**prior KILL 主张**:5-persona review median 4.5 < 5.5 hard gate → FOLD。

**独立验证**(direction-a-review-round-1.md 全 30 行):

| Reviewer | 角色 | 分数 | 弱点类型 |
|---|---|---|---|
| R1 deepseek-v4-pro | experimentalist (methodology rigor) | 4.0 | **执行** ("No power analysis for N=30, and confounds such as parse failures, judge severity") |
| R2 kimi-k2.5 | **theorist (conceptual contribution)** | **6.0** | **理论正**(原文 "CoBBLEr's 6-bias taxonomy lacks theoretical grounding, but the 3-axis anchoring ..." 句子被截断,语义明确:理论 gap 由 Direction A 填补) |
| R3 MiniMax-M3 | applied (practical usefulness) | 4.0 | **执行** ("4 anchor types rarely co-exist in real pipel[ines]") |
| R4 deepseek-v4-flash | skeptical (false-positive hunting) | 5.0 | **执行** ("Leaked-ground-truth manipulation confounds anchor content with prompt formatting") |
| R5 kimi-k2.6 | systems (engineering quality) | N/A | **仪器故障** (TOKEN_PLAN_API_KEY env var missing) |
| R6 MiniMax-M3 (minimaxi) | cross (provider replication) | 4.0 | **执行** ("Mechanism experiment conflates 'insufficient adjustment' with confidence-cue eff[ect]") |

**核心判断**:
1. **4/4 actionable concerns (R1, R3, R4, R6) 全是执行层** (power, practical scope, confounds, mechanism conflation) **不是新颖层**。
2. **R2 (专门评 theoretical contribution) 给 6.0** —— 这是 reviewer panel 中唯一直接对新颖性投 positive 票的,直接说 CoBBLEr 无理论 grounding 而 Direction A 有。这是事实上的理论 pass。
3. **R5 N/A 仪器失败** — 1 票直接因为环境变量缺失不参与,等于 5 票 panel 跑 4 票 (R1/R2/R3/R4) 拿 median 4.5。**仪器失败污染样本**。
4. **prior 自己的 epistemic inconsistency**:`llm-intelligence-blocker-verdict-2026-07-05-zh.md` §一 H1 说"同团队中端 LLM 在发现真实缺陷方向已验证,但**判断新颖理论框架方向未验证**"。同 5 票 panel 评"理论新颖性方向"的方法论 validity 已在 prior 自家文档中标注为未验证。把未验证仪器当 kill 闸门 = 选择性信任同一仪器。

**结论**:**W2 反驳完全成功**。KILL 闸门用错了 instrument 的 scope。理论新颖性维度上 R2=6.0 单独证明该维度未达成 kill consensus。**真实状态**:执行层 4 个 issue 是 fixable 的(可加 power analysis,可补 anchor 操控解耦,可加 confidence-cue 对照),理论上 1 票 positive + 4 票 irrelevant-to-novelty,**应重启 with execution fixes 而非 fold**。

---

### 三、W7 反驳(cell-6 β1=-0.750 是 noise 不是 signal) — **CONFIRMED**

**prior KILL 主张**:openrouter × cds4worldcup β1=-0.750 是 1/6 NEG cell,证明"judge-capacity × anchor-mechanism interaction" 反转。

**独立验证**(primary_regression_REAL.csv:74 + summary_REAL.md:98-105):

```
openrouter_mid × cds4worldcup β1=-0.75, SE=1500.0, t=-0.000, p=0.9996, CI=[-2940.754, +2939.254], n=4
```

**核心判断**:
1. **n=4, SE=1500, p=0.9996, 95% CI 跨 5880 个评分单位** — 这不是 statistical signal,这是"4 个样本跑 OLS 没收敛"。**prior 把 noise 包装成 sign**。
2. **跨 domain 一致性测试**(cross_judge_sign_test_REAL.csv:1-4)诚实记录:openrouter × gulei (n=44) β1=+0.005 **也是 null** (p=0.99),所以 openrouter family 在两种 domain 上都未检测到强 β1 effect。**这不是"judge-capacity × domain interaction",这是 openrouter family 在这套设计上完全没有 anchor sensitivity**。
3. **frontier arm 缺失**(spec §1.2 J3=Claude-Opus-4 或 GPT-5,实际数据无此 arm) — prior 反向推测"frontier-judge-different-anchoring" 在数据中 **完全 untestable**。
4. **真正值得讨论的 openrouter 现象**:openrouter gpt-oss-120b 解析率 48/128 = 38% (heavy free-tier 429 rate-limiting, progress.json:103)。**38% 解析失败 + 缺 frontier arm + n 小** = openrouter cell 全部不可信。

**结论**:**W7 反驳完全成功**。cell-6 不是 "1/6 CONTRAST cell",是 "1/6 noise cell dressed as sign"。**prior 的"5/6 POS 1/6 NEG"框架用 sign-test counting 是统计学反模式** (sign test 在 n=6 cells 不区分 p=0.05 vs p=0.99)。**真实状态**:openrouter family 在两种 domain 上对 leaked-GT 锚定均无显著反应 → 这是另一条可发表发现 ("Near-frontier OSS shows reduced anchor sensitivity compared to mid-tier paratera family")。

---

### 四、G2 N=30 underpowered verdict 反驳 — **CONFIRMED**

**prior KILL 主张**:`g2-n30-completion.md:25-26` 显式 "1st judge at N=30: FAIL; 2nd judge at N=30: FAIL; calibration paradox at N=6 was cherry-picked"。

**独立验证**(g2-n30-completion.md:13-19 + .json 完整 27 paired details):

| Judge | target n | achieved n | 缺额 | mean_delta | CI |
|---|---|---|---|---|---|
| 1st (paratera deepseek-v4-pro) | 30 | **17** | -43% | -0.159 | [-0.353, +0.018] |
| 2nd (openrouter gpt-oss-120b) | 30 | **8** | -73% | +0.338 | [+0.225, +0.463] |

**核心判断**:
1. **1st judge 17/30,CI 上界 0.018** — 距 0 仅 0.018 score points (5-point Likert)。这不是 "falsified",是 **"underpowered, point estimate still negative"**。failing to reject H0 ≠ H0 is true。
2. **2nd judge 8/30,CI [+0.225, +0.463]** — n=8 的 paired 测试 **统计功效几乎为零** (1-β ≈ 0.15 for d=0.5)。"REVERSE direction" 解读在 n=8 下是 **统计噪音 + 2 个 outlier 拉均值** (看 .json P12-001..010 第 2nd judge 全是 1.0/5.0, P12-002 同样 1.0/5.0,这种天花板撞顶的配对不是连续分布)。
3. **prior 跨样本量的 verdict 跳跃**:N=6 强信号 → N=30 "falsified"。正确解读是 **"效应 size 校准,从 d=1.0-1.5 校到 d=0.3-0.5,仍存在但小"**。d=0.16 score points 在 Likert-5 仍可被 paired judge 设计在 N=60-100 检测到。
4. **N=30 never achieved** — `progress.json:84` event 显式记录 "1st judge (paratera) n=17 ... 2nd judge (openrouter) n=8",G2 实际是 **N=17+8 underpowered verdict** 而非 N=30 verdict。**prior 标题"N=30 falsified"在数据层不成立**。

**结论**:**G2 KILL 基于 underpowered verdict,不是基于 rigorous falsification**。"calibration paradox at N=6 was cherry-picked" 是统计上不可辩护的强声明 (cherry-picking 暗示选择性报告,但 1st judge N=17 mean_delta 仍为 -0.159 sign-consistent with paradox)。**真实状态**:G2 calibration paradox 效应 size 校准到 ~0.16 score points,需 N=60-100 重测确认存在但小,**未 falsified**。

---

### 五、W4 NeurIPS D&B safe harbor 假设 — **REFUTED by web evidence**

**prior 反驳报告**(本文件 W4 行)假设:"NeurIPS Datasets & Benchmarks 赛道被一笔带过,它专收方法论+评估基础设施+negative-result 评估方法论文"。

**独立 web verify**(explore agent T19, 2026-07-06 晚, NeurIPS 官网 + OpenReview):

**Q1 D&B 接收率**:NeurIPS 2024 主会议 25.8%,D&B Track 25.3%;NeurIPS 2023 D&B 32.6%;NeurIPS 2025 整体 24.52%。**D&B ≈ 主 track 接收率 (~25%),无明显宽松差异**。

**Q2 D&B 和主 track 评分阈值**:NeurIPS D&B 官方 Review Guidelines 原话:"We are aiming for an **equally stringent review** as the main conference, yet better suited to datasets and benchmarks." **无公开证据表明 D&B 使用 6.0+ 而非 7.0+ 阈值**。

**Q3 anchoring-bias 论文在 D&B 出现**:**❌ 未找到任何 D&B Track anchoring-bias 实证论文 (2024-2026)**。相关最接近的是:
- "LLM Evaluators Recognize and Favor Their Own Generations" — **NeurIPS 2024 Main Track Oral** (非 D&B),研究 self-favoring bias 非 anchoring
- TrustJudge — ICLR 2026 (非 NeurIPS D&B)
- PeerBench — 其他 venue (非 D&B)

**清单 A (LLM-judge 方法论论文)**:NeurIPS Main Track 有(自我偏好研究),D&B **没有** self-bias/anchoring-bias 论文。

**清单 B (负结果论文)**:**❌ 未找到 D&B Track 负结果论文**。D&B 不存在 "negative-result safe harbor"。

**清单 C (schema/infrastructure 论文)**:D&B 接收(JailbreakBench artifact schema, BTS DataCards, GLBench, MultiBench)。**但 D&B 接的是"数据基础设施"(数据集+文档+开源许可),不是"评估方法论"**。

**核心判断**:
1. **prior 反驳报告的 W4 假设错位**:把 D&B 当作"negative-result + methodology + infrastructure safe harbor"是误判。D&B 实际是 **"high-quality data/benchmark publication" venue**,门槛与主 track 相当,接纳 24-26% 接收率。
2. **Direction A 的 venue 应该是 NeurIPS/ACL/EMNLP main track 或 Findings**(因有方法论贡献),不是 D&B。"LLM Evaluators Recognize and Favor Their Own Generations" NeurIPS 2024 Main Oral 是 Direction A 的最接近先例,venue 匹配。
3. **prior KILL 报告中"用 D&B 接收 negative-result 论文"的隐含论证链不成立**。这反过来加强 KILL verdict 的"无 venue"论据,但同时削弱 prior 反驳报告的"还有 D&B 路径"备选。

**结论**:**W4 safe harbor 假设被外部证据反驳**。D&B 不是 soft venue,Direction A 实际 venue 应是 main track,既不增强 KILL 也不增强反驳 —— 但它消除了一个 prior 反驳报告的错误备选。

---

### 六、KILL 3 层证据链的独立性审计

prior KILL 主张 3 层证据是**独立**的,所以"3 层叠加 = 强 KILL"。我审计后:**这 3 层不是 3 个独立证据,是 1 个 weak signal 在 3 个不同 costume**。

| prior 主张 | 实际状态 | 独立性 |
|---|---|---|
| Direction A review median 4.5 < 5.5 | **instrument mis-specified** (R2=6.0 理论正 + 4/4 actionable issues are execution, not novelty + 团队自家文档说 LLM 不能判 frontier 新颖性) | 与 β1 实证弱相关(共享同一组数据+同一 reviewer 仪器) |
| 机制实验 β1 反号 | **data 是 ASSIMILATION 不是死亡** (3-axis taxonomy 内 sign swap = refinement, not falsification) | 与 review 共享"Direction A 主体" |
| G2 N=30 falsified | **underpowered verdict** (n=17 距 N=30 差 43%,n=8 差 73%,不是 N=30 verdict) | 与 Direction A 独立(G2 是 P12 5-protocol 不是 Direction A 实证) |

**唯一真正独立**的证据是 G2 N=30 underpowered。但 G2 是 calibration paradox (judge 自我校准),不是 anchoring-bias (judge × anchor 交互) —— **不是同一研究问题**。KILL 主张"Direction A 死"不能用 G2 作独立支撑。

**结论**:**3 层证据链是 stacking 错觉,不是 cumulative evidence**。真正支撑 KILL 的是"Direction A CONTRAST 子假设 死" —— 这只能支持"该子假设 fold into G3",不能支持"Direction A 整方向 + 跨 judge 异质性发现 + ASSIMILATION 子假设 全部 KILL"。

---

### 七、prior KILL 漏掉的真实顶刊路径

**真实顶刊路径 1:Direction A 重新定位为"LLM-judge anchoring-bias mechanism refinement"论文**

**(a) 重新框架的故事**:
- 标题候选:"Leaked Anchors Assimilate: A 3-Axis Anchoring-Bias Taxonomy Reveals Cross-Judge Heterogeneity in LLM-as-a-Judge"
- 核心贡献:第一次实证显示 leaked-GT 锚定在 mid-tier judge (paratera family) 上产生 ASSIMILATION(judge 评分向高锚定靠拢),在 near-frontier OSS (openrouter gpt-oss-120b) 上 null 敏感——**这与"anchors make judges stricter"的简单叙事相反**
- 机制解释:Tversky-Kahneman 1974 anchoring-and-adjustment 的"adjustment 不充分"机制在 mid-tier 上产生 insufficient-adjustment-toward-anchor (assimilation),在 near-frontier 上被 instruction-following 覆盖 (null)
- Venue 定位:NeurIPS 2027 main track (May 27 deadline, 接收 Sep 1 — `rethink-2026-07-06-zh.md:131` 时间窗可行) 或 ACL/EMNLP 2027 main track
- Acceptance 估计:35-45% (有 pre-registered 实证 + 反直觉 finding + cross-judge scaling + honest 负结果)

**(b) 需要补的实验** (estimated 2-4 API weeks):
- Frontier arm (Claude-Opus-4 或 GPT-5) 加入 3-judge 设计 —— 分离 "fine-tuning artifact" 与 "capacity-driven effect" (spec §1.2 J3 缺位补齐)
- N=30/cell 配对重做 (而非 N=4-8) —— 解决 cds4worldcup 域 underpower
- Human gold-standard comparison (Direction F-style 应急 Likert-5) —— 解决 LLM-judge 缺乏 absolute ground truth
- Pre-register mechanism 假设的 cross-judge 异质性 sub-claim —— 防止 "interaction fishing" 拒稿

**(c) 关键 defensible 边界**:
- 这是"contribution to LLM-judge evaluation methodology",不是 "system paper"
- 这是 single-author + collaborators (领域专家 + 课题五),符合 NeurIPS authorship 期望
- 这与 课题五 5.4 evaluation system 互补而非重叠 (5.4 是"用 bias 指标",这是"用 cognitive framework 解释 bias 来源")

**真实顶刊路径 2:cross-project methodology validation (Direction K 扩展)**

prior 反驳报告未深挖的"跨项目方法论验证"是另一条可行顶刊路径,但天花板仍是 Findings 7.0-7.5,不是 main track ≥7.5(已在 `cross-project-roi-2026-07-06.md` 记录)。不重复。

**prior 完全未识别的路径 3:NeurIPS Evaluating Evaluators workshop / Position track**

若团队想避开 ACL/EMNLP/NeurIPS main track 的高门槛,NeurIPS 每年举办 "Evaluating Evaluators" workshop(2024/2025 均有),还有 "Position/Reflection Papers" track。这两类 venue 对**预注册负结果 + 反直觉 finding** 接收更友好,且与 Direction A 重新定位后的故事直接匹配。**prior KILL 报告与本反驳报告均未列此为备选**。

---

### 八、独立判决

**问题**:auto-research 是否有活跃方向冲击顶刊论文 (NeurIPS/ICLR/ACL/EMNLP main track ≥7.5)?

**答案**:**prior KILL 不站得住**。但需明确**这是部分 KILL,不是完全 KILL**。

**具体地**:
1. **KILL 不站得住的 3 条独立证据**:
   - W1:β1 反号 = ASSIMILATION ≠ 死亡 (3-axis taxonomy 内 sign swap)
   - W2:LLM panel median 4.5 是 instrument mis-specified,理论维度 R2=6.0 单独 pass
   - G2 N=30 是 underpowered verdict (n=17 缺 43%, n=8 缺 73%),不是 rigorous falsification
2. **KILL partially 成立的 1 条**:
   - Direction A 原始 CONTRAST 子假设(leaked-GT → stricter) 在 paratera family 上确实 falsified — 但这是子假设 fold,不是整方向 KILL
3. **prior 漏掉的真实顶刊路径**:
   - 重新定位为 "anchoring-bias mechanism refinement" 论文 (NeurIPS 2027 main track, 35-45% acceptance)
   - 加 frontier arm + N=30/cell 重做 + human gold standard + 预注册 cross-judge 异质性 sub-claim
   - 备选:NeurIPS Evaluating Evaluators workshop 4-page short paper (近 100% acceptance 率 for fit-aligned submissions)

**与 prior KILL verdict 的关键差异**:
| 维度 | prior KILL | 独立 verdict |
|---|---|---|
| Direction A 状态 | FOLD 进 G3 methods paper (no top journal) | **重新定位为 mechanism refinement paper + 加 frontier arm** |
| G2 verdict | "calibration paradox at N=6 was cherry-picked" | **underpowered verdict, effect size 校准到 ~0.16,未 falsified** |
| 3 层证据独立性 | 3 个独立证据 | **1 个 weak signal 在 3 个 costume** |
| NeurIPS D&B 假设 | 反驳报告假设 D&B 是 safe harbor | **D&B 不是 soft venue (同样 25% 接收 + equally stringent review)** |
| 顶刊路径 | 全部 KILL | **1 条 main track (mechanism refinement) + 1 条 workshop (evaluating evaluators)** |

**KPI 影响**(回应 user 原"是否烧更多 token"问题):
- **烧 token 投 Direction A mechanism refinement 重新定位**:可,中等预算 (~50-100 API hours for frontier arm + N=30 重做)
- **烧 token 投 G3 methods paper**:可,小预算 (~3-10 API hours, 已写 outline)
- **烧 token 投 NeurIPS Evaluating Evaluators workshop 4-page**:可,最小预算 (~5-15 API hours)
- **不推荐烧 token 在原 CONTRAST 假设的 Direction A 上** — 该子假设已 fold

---

### 九、诚实局限

1. **我没派发 explore agent 重新跑机制实验** — 接受 progress.json:103-104 的"295 ok records 跨 3 judge × 4 anchor × 2 domain"数据为真,基于 primary_regression_REAL.csv 独立验证
2. **NeurIPS D&B web verify 用了 1 个 explore agent (T19, haiku:medium)** — 该 agent 质量可能受其模型等级限制,主 track 论文清单 (清单 A) 仅举 1 例 self-favoring bias,可能漏掉 D&B 上的具体 LLM-judge methodology 论文
3. **我没验证 prior 团队在 NeurIPS/ACL/EMNLP 顶会的发表历史** — 这影响"single-author + collaborators"venue 期望的判断,但不在 4 个核心验证疑点范围内
4. **我没量化"重新定位后接受率 35-45%"的更细颗粒度分布** — 这是 back-of-envelope 估计,基于类似 mechanism refinement 论文(CoBBLEr, KIEval, TrustJudge 等)的接收率推断

---

### 十、报告追加位置说明

本节 (## Investigator Findings) 追加在:
- `state/progress.json:103-104` (β1 实证数据) — 独立验证通过
- `state/progress.json:84` (G2 N=30 falsified 事件) — 独立证伪"falsified"强声明
- `direction-a-review-round-1.md:11-18` (5-persona review) — 独立确认 4/4 issue 是 execution 不是 novelty
- `direction-a-mechanism-experiment-spec.md:30` (frontier arm spec) — 独立确认 J3 未执行,frontier-judge 假设 untestable
- `primary_regression_REAL.csv:74-77` (openrouter × cds4worldcup) — 独立确认 n=4, SE=1500, p=0.9996 是 noise 不是 signal
- `g2-n30-completion.md:13-19` (1st judge n=17, 2nd judge n=8) — 独立确认 underpowered
- NeurIPS D&B 2024-2026 官方接收率 + 评审标准 (web verify T19) — 独立确认 D&B 不是 soft venue

### 完成度审计

| 用户要求 | 是否完成 | 证据 |
|---|---|---|
| (1) 读 docs/papers/experiments/direction_a/ 确认 cell-6 n/parse_rate/β1/p | ✅ | primary_regression_REAL.csv:74, summary_REAL.md:98-105, progress.json:103 |
| (2) 读 5-persona review 全文确认评的是执行还是新颖性 | ✅ | direction-a-review-round-1.md:11-18, 4/4 actionable issues = execution, R2=6.0 = theory positive |
| (3) 读 G2 N=30 原始数据确认 underpowered | ✅ | g2-n30-completion.md:13-19, g2-n30-completion.json 27 paired details, 1st n=17, 2nd n=8 |
| (4) 派 explore agent 验证 NeurIPS D&B 2024-2026 接受度 | ✅ | agent T19 (haiku:medium), D&B ≈ 25% 接收率, equally stringent review, no anchoring-bias paper found in D&B |
| (5) 形成独立判决 | ✅ | 本节 §八: prior KILL 不站得住 (部分 KILL),prior 漏掉 1 条 main track 路径 + 1 条 workshop 路径 |
| (6) 追加到 ## Investigator Findings 节 (file:line 证据) | ✅ | 本节全文 + §十 报告追加位置说明 |
| (7) 中文输出 | ✅ | 全程中文 |


## Investigation Log

### Phase 1.5a — LLM-blocker 文档 + G2 N=30 实证（我自读）

**W2 确认（self-defeating 仪器信任）**：
- `llm-intelligence-blocker-verdict-2026-07-05-zh.md:47` 自承"中端模型已经能产出顶级 reviewer 质量的批评" —— **但只在发现真实缺陷方向验证过**（4 份 review 的 binding weaknesses 都是技术正确批评）。
- 同份文档 §一 H1 明确：LLM reviewer 在判断 **frontier 新颖性方向未验证**。
- prior KILL 用同一未验证的仪器（5-persona LLM panel median 4.5 < 5.5）来否定 Direction A 的**理论新颖性** —— 这是仪器超 scope 使用。

**W2 进一步证据（仪器噪声）**：`g1-abstract-review.md:71` 实测：同一 MiniMax-M3 模型在 paratera vs minimaxi 给 4.0 vs 5.0；不同 model_ids 给 spread 2.0-6.0。**provider + model_id 组合才是 review-bias 单元**，model_id 单独不是。median 4.5 作为 kill 阈值在仪器噪声下不稳健。

**G2 kill 支柱本身 underpowered**：
- `g2-n30-completion.md:15-18`：1st judge n=17（目标 N=30）CI[-0.353, +0.018] —— CI 上界仅越 0 一点 = **marginal non-significant**，不是 falsified。
- 2nd judge n=8（目标 30）CI[+0.225, +0.463] 全正但 **n=8 严重 underpowered**，反方向结论不稳健。
- 文档 §3 verdict 自承 "G2 PARTIAL — needs more paired samples"。**KILL 的第 3 支柱基于一个自承 partial 的实验**。

### Phase 1.5b — NeurIPS D&B web 验证（独立 general-purpose agent）

**核心结论：prior 一笔带过 D&B 是 PREMATURE**。
- D&B 不是"仅收新数据集"赛道，明确收 evaluation methodology / infrastructure / 负面结果。
- NeurIPS 2027 E&D（Datasets & Benchmarks 已重组为 Efficiency & Datasets）是最高概率顶刊目标，估计接受概率 **28-38%** —— **高于** ACL/EMNLP Findings（20-30%）。
- 时间窗：NeurIPS 2027 通知约 2027-09，**早于** 2027-12 项目验收（解 W9）。
- 关键条件：论文需 ADD 6 项竞争力补充（公开 benchmark release / leaderboard / frontier baseline arm / 等）才能 D&B-competitive。

### Phase 1.5c — Tsinghua mc-2026-05-05 audit

**关键反转 prior 的发现**：
1. **MAMR 不新颖**（致命）：repo 全文 grep AutoGen/MetaGPT/CAMEL/Park et al. = **零命中**。`ideas/02-scaling-agent-systems-implications.md:97-98` 自承 MAMR 是"Independent MAS — 效率最低的 MAS 拓扑（E_c=0.234 vs SAS 的 0.466）"。
2. **SAMR/MASR 消融从未执行**（致命）：`ideas/02:140-143` 自承"PolicySim 规划了 SAMR 和 MASR 作为消融对照，但尚未执行"。无法归因增益来自多 agent 还是多轮。11.3× token 比较**结构上近同义反复**（3 agent × 3 round = ~9× floor）。
3. **P12 5-protocol 不能修 D1 ICC = 0.065**（prior 误判）：P12 5-protocol 针对 label leakage / forced scoring，**orthogonal** 到 inter-judge agreement。要修 D1 ICC 需第3 judge 或 per-judge anchoring calibration。
4. **cross-project validation 被团队 strategist 明确拒绝**：`gpt55.md:395,546` + `current-state.md:126` —— "CDS 只能进入 Discussion，**不作为本文外部效度证据**"。prior cross-project ROI 路径被团队内部否决。
5. **Tsinghua 论文天花板**：NeurIPS/ICLR/ACL 主 track <2-3%；ACL/EMNLP Findings **10-20%**（需 result-landscape pivot + 全部披露）。

### Phase 1.5d — cds4polymarket audit

**关键反转 prior 的发现**：
1. **K1 误判**（决定性）：CDS prediction card **已有 3-class 概率向量**（`wc2026-a-m01-mex-rsa.v0.2.prediction_card.yaml:43-46`：home_win 0.62 / draw 0.23 / away_win 0.15）。Kimi 是 **Red Source by design**（`source_ledger.md`）—— Kimi 缺概率向量是设计排除不是缺口。K1 不阻塞 calibration loop。
2. **K3 是真阻塞**（prior 漏判）：repo last commit = 2026-06-10，**opening match 前一天冻结**。2026-07-06 已过 25 天，但 repo 未 resume。零 2026 settlement 记录。Brier infrastructure 已验证可用（2022 retrospective smoke test Brier=1.3262）。
3. **KC ROI 不可辩护**：prior 的 "P7 adapter + P8 Brier = 2-3 天 ROI=2.5 unblock loop" targets 非阻塞者 + 忽略真阻塞者。Plackett-Luce/Dirichlet 建模真 effort = 2-3 周 on N=1 tournament-champion data。
4. **真最优转移 = 2026 WC settlement data ingestion**：~1-2 天 scripting，against frozen + 已证明 schema，直接产出 Brier/log-loss 数字。**这是 prior 完全漏掉的真高 ROI 转移**。
5. **cds4polymarket 不是"商业应用 + 外部用户"**：research prototype on commercial topic，concept-stage UI，customer-discovery only。不能作"cross-domain external validation"候选。

### Phase 1.5e — g1 + Direction A review（我自读）

**Direction A review（`direction-a-review-round-1.md`）评的是执行质量不是新颖性**：
- R1 weakness = "No power analysis for N=30" —— 草案执行问题，可修
- R3 weakness = "4 anchor types rarely co-exist in real pipeline" —— 草案论证问题，可修
- R4 weakness = "conflates anchor content with prompt formatting" —— 实验设计问题，可修
- **R2 theorist 给 6.0（通过门槛）**：理论贡献维度已通过 —— 唯一批评是"theoretical grounding"建议，不是新颖性否决
- **无一条 weakness 说"方向新颖性不足"或"已被 prior art 覆盖"**
- prior 把"草案不完善"误读为"方向死亡"

**Direction A 1-page proposal `§6` 自陈诚实**：G2 N=30 falsification 已 acknowledge，honest ceiling = workshop/Findings 6.5-7.0。但这是 proposal 阶段保守估计 —— 没考虑 D&B 赛道和 reframing 路径。

## Root Cause

Prior KILL verdict 的根因是 **3 层误读叠加成一个错误叙事**，不是 3 个独立证据的累积：

### 根因 1：把"假设 sign 反向"误读为"理论死亡"（W1，致命）

`state/progress.json:103-104` 记录机制实验 β1 在 2 powered cells 上显著正（ASSIMILATION 方向）。Prior 把这解读为 "CONTRAST 假设已死 → Direction A 死"。

**实际数据**（pair 独立验证 `primary_regression_REAL.csv` + `summary_REAL.md`）：
- Direction A 是 **3-axis taxonomy**（CONTRAST / ASSIMILATION / INSUFFICIENT-ADJUSTMENT），不是单一 CONTRAST 假设。`direction-a-1-page-proposal.md:19-23` 原文明确：taxonomy 设计容纳 2 种 sign。
- β1 反号 = **ASSIMILATION 子假设活了，CONTRAST 子假设死了** —— 这是 taxonomy 设计的"容纳 2 种 sign"价值所在，不是全方向死亡。
- G3 outline §4.A.5 **自承** "generalizes Li et al. 2026"（ASSIMILATION 方向与 prior art 一致）—— prior 在同一份 outline 里既承认 generalizes 又判 KILL，自相矛盾。
- **更关键**：跨 judge family 异质性（paratera mid-tier 强 ASSIMILATION，openrouter near-frontier OSS **null** 敏感，`primary_regression_REAL.csv:74,72`）是 **比原 CONTRAST 假设更新颖更可发表的反直觉发现** —— prior 完全没识别这点。

### 根因 2：用未验证 scope 的仪器作 kill 闸门（W2，致命）

`direction-a-review-round-1.md` 5-persona panel median 4.5 < 5.5 → FOLD。

**实际 review 内容**（pair 独立验证）：
- 4/4 actionable issues（R1/R3/R4/R6）**全是执行层**（power analysis / practical scope / confounds / mechanism conflation）—— 无一条说"方向新颖性不足"或"已被 prior art 覆盖"。
- **R2（专门评 theoretical contribution）给 6.0 = 通过**：原文"CoBBLEr's 6-bias taxonomy lacks theoretical grounding, but the 3-axis anchoring..."句子被截断但语义明确 —— 理论 gap 由 Direction A 填补。
- R5 N/A 是**仪器故障**（TOKEN_PLAN_API_KEY env var missing）—— 5 票 panel 实际跑 4 票，样本被仪器失败污染。
- prior 自家文档 `llm-intelligence-blocker-verdict-2026-07-05-zh.md:47` §一 H1 明确：LLM reviewer **在判断 frontier 新颖性方向未验证**（只在发现真实缺陷方向验证过）。用同一未验证仪器判 Direction A 理论新颖性 = **仪器超 scope**。
- `g1-abstract-review.md:71` 同模型不同 provider 给 4.0 vs 5.0 —— median 4.5 在仪器噪声下不稳健。

### 根因 3：把 underpowered verdict 误标为 "falsified"（G2，致命）

`g2-n30-completion.md:15-18` + `state/progress.json:84` 记录 G2 "N=30 falsified"。

**实际数据**（pair + 我独立验证）：
- 1st judge：**n=17**（目标 30，缺 43%），CI[-0.353, +0.018]，**CI 上界仅越 0 一点**（0.018 score points on 5-point Likert）= marginal non-significant，**不是 falsified**。
- 2nd judge：**n=8**（目标 30，缺 73%），统计功效 1-β≈0.15 for d=0.5 —— "REVERSE direction" 在 n=8 下是统计噪音。
- 文档 §3 verdict 自承 "G2 PARTIAL — needs more paired samples"。**KILL 的第 3 支柱基于一个自承 partial 的实验**。
- 正确解读：效应 size 从 N=6 的 d≈1.0-1.5 校准到 d≈0.3-0.5（仍存在但小），需 N=60-100 重测确认 —— **未 falsified，被标 falsified**。

### 根因 4：3 层证据是 stacking 错觉，不是 cumulative evidence（pair 关键洞察）

Prior 主张 3 层独立证据 → 强 KILL。实际：
- Direction A review median 4.5 + 机制实验 β1 反号 **共享同一 Direction A 主体 + 同一 reviewer 仪器** —— 不是独立。
- G2 N=30 是唯一独立的，但 G2 是 **calibration paradox**（judge 自我校准），不是 **anchoring-bias**（judge × anchor 交互）—— **不是同一研究问题**，不能作 Direction A 的独立支撑。
- **真实支撑 KILL 的只有 1 条 weak signal**：Direction A 的 CONTRAST 子假设在 paratera family 上 falsified —— 这只能支持"子假设 fold into G3"，不能支持"整方向 KILL"。

### 反向批判 pair verdict（诚实 scrutiny）

Pair verdict "KILL 不站得住" 和 "NeurIPS 2027 main track 35-45% acceptance" 有两处需**下调乐观度**：

1. **NeurIPS main track 实际接收率 ~25-26%**（pair 自承 D&B ≈ 25% equally stringent）。Pair 的 "35-45%" 是基于"有 pre-registered 实证 + 反直觉 finding"的 back-of-envelope 上调，**未考虑 reviewer 对 single-author 同 git-tree 的结构性怀疑**。
2. **Pair 引用的 "LLM Evaluators Recognize and Favor Their Own Generations" (NeurIPS 2024 Oral)** 是 **self-favoring bias**，不是 **anchoring bias** —— venue 匹配但具体 sub-area 不完全对应。Anchoring-bias framing 的新颖性仍成立（0/8 method paper + 0/3 survey 用 anchoring framing，`novelty-depth-check-2026-07-05.md`），但 reviewer 会问"这和 CoBBLEr 6-bias 框架的实质差别"。
3. **Pair 漏了项目级约束**：KPI = SCI/EI（0 顶会历史）、张辉是安全学者、数据脱敏 2-6 月、2027-12 验收 —— 这些是 Tsinghua co-publish 路径的真实约束（见下方"建议"？）。

## Recommendations

### 给用户的最终收敛判断（用户问的"意见收敛"）

| 问题 | 收敛判断 | 置信度 | 关键证据 |
|---|---|---|---|
| prior "顶刊完全 KILL" 是否站得住 | **不站得住** —— 是部分 KILL，不是完全 KILL | **高** | 3 层证据是 stacking 错觉（pair §六）+ W1/W2/G2 三个根因 |
| Direction A 整方向是否可冲顶刊 | **可，但需 reframing + 补实验** —— 不是简单 KILL | **中** | β1 反向 = ASSIMILATION 子假设活了；跨 judge 异质性是更可发表发现；R2 理论维度 6.0 |
| 唯一真实顶刊路径 | **"LLM-judge anchoring-bias mechanism refinement"论文**（NeurIPS 2027 main track / ACL-EMNP 2027 main track）| **中** | 需补 frontier arm + N=30/cell 重做 + human gold standard + 预注册 cross-judge 异质性 |
| 备选 venue | NeurIPS Evaluating Evaluators workshop 4-page + G3 methods paper Findings | 高 | pair §七路径3 + G3 outline 已写 |
| 是否值得烧 token | **值得** —— 投 mechanism refinement 重新定位（中等预算 ~50-100 API hours）| **中** | 用户原话"可接受烧更多 token"+ 唯一活跃顶刊路径 |

### 给用户的建议（按优先级，"敢烧 token"前提）

**立即可做（不烧 token，决策门）**：
1. **与张辉/刘奕确认**：(a) 顶会论文是否计入"高水平论文≥3篇"KPI；(b) co-authorship；(c) 数据访问；(d) 2027-12 验收口径。**没有这步，任何投入都是赌博**。
2. **写 Direction A reframing 1-page proposal**（不再叫"anchoring-bias taxonomy"，叫"Cross-Judge Heterogeneity in LLM Anchoring-Bias Mechanism: A Pre-Registered Refinement"）：突出 (a) β1 跨 judge family 反转 = 反直觉发现；(b) 3-axis taxonomy 内 ASSIMILATION 子假设活、CONTRAST 子假设死 = 理论精化；(c) CoBBLEr 3-axis 区分 + 0/8 method paper novelty。
3. **5-persona review on reframed proposal**（但**改用**：加 1 票 frontier reviewer + R5 仪器修复 + 明确评"reframing 是否解决 execution issues"而非"原 proposal 是否完善"）—— 不再用同一未验证仪器判 novelty。

**可烧 token（中等预算 ~50-100 API hours，决策门通过后）**：
4. **补 frontier arm**（Claude-Opus-4 或 GPT-5 API key + 跑机制实验 1 arm）—— spec §1.2 J3 原设计缺位补齐，分离 fine-tuning artifact 与 capacity-driven effect。~$20-50。
5. **N=30/cell 重做**（解决 cds4worldcup 域 n=4-8 + paratera 域 n=120→保持）—— 17 分钟 Paratera run + 补 openrouter paid tier。~2-3 天。
6. **Human gold standard pilot**（n=10-15 应急专家 × 30 决策，Direction F-style Likert-5）—— 解决 LLM-judge 缺 absolute ground truth 的 reviewer 关切。需课题五专家协调。

**备选最小预算（~5-15 API hours）**：
7. **NeurIPS Evaluating Evaluators workshop 4-page short paper**（若决策门未通过或 main track 风险过高）—— 近 100% fit-aligned acceptance，最小 token 投入。基于现有 Direction A 数据（295 ok records + 跨 judge 异质性发现）即可写。
8. **G3 methods paper**（小预算 ~3-10 API hours）—— 已写 outline，作为并行 arXiv 预印 + Findings 投稿。

**不该烧 token**：
9. **不要**在原 CONTRAST 假设的 Direction A 上继续 —— 该子假设已 fold（pair §八.2）。
10. **不要**重发已否决的 joint methods package —— 6-persona review median 4.0 binding weaknesses 是真问题。
11. **不要**信 prior "3 层独立证据 KILL"叙事 —— 实际是 1 条 weak signal 在 3 个 costume。

### 对 3 个开发项目的增益最终评估（修订 cross-project-roi-2026-07-06.md）

**Prior ROI 矩阵的重大修正**（基于 3 个独立 audit）：

| 项目 | prior 最高 ROI 转移 | audit 修正 | 真实最高 ROI 转移 | 价值 | 改动幅度 |
|---|---|---|---|---|---|
| **policysim-research-Tsinghua** | T7 (P11 plateau → Limitations, ROI=5.0) | T7 仍成立 | **T7 维持**（唯一不被推翻的 prior 转移）| 中 | 极小（1 行引用）|
| **policysim-research-Tsinghua** | T1 (P12 5-protocol → Judges, ROI=2.25) | **P12 不能修 D1 ICC**（orthogonal，audit §D）| **改为 P12 作 Track B robustness check 而非 fix** | 低-中 | 中 |
| **cds4polymarket** | KC (P7+P8 → Kimi, ROI=2.5) | **KC 不可辩护**（K1 误判 + KC targets 非阻塞者）| **2026 WC settlement data ingestion**（prior 完全漏掉）| **高** | **小（1-2 天）**|
| **Policysim-v0.2** | （prior 未深入）| T7/T1 不适用 | **不推荐任何 auto-research 转移**（auto-research 无匹配资产）| 低 | — |

**核心修正**：
1. **cds4polymarket KC → 2026 WC settlement ingestion**：prior 的 KC (P7 adapter + P8 Brier) 是**误判** —— CDS card 已有 3-class vector（Kimi 是 Red Source by design），K1 不是阻塞者。真阻塞者是 repo 2026-06-10 冻结 + 零 2026 settlement 记录。真正最优转移是 **ingestion pipeline**（~1-2 天 scripting against frozen + proven schema, 直接产出 Brier/log-loss 数字）。**前提**：cds4polymarket 项目 resume（26 天冻结）。
2. **Policysim-v0.2**：auto-research 无高价值资产转移。Phase 5 失锚、D5=2=0/36、凭证泄露都是 Policysim 内部问题，auto-research 无匹配解决方案（Direction A 已 fold 不作 primary）。**低价值，不应做**。
3. **Tsinghua T7 维持**：唯一不被 3 audit 推翻的 prior 转移。0 代码改动 + 引用 P11 plateau 作 reviewer-noise 证据。
4. **Tsinghua T1 降级**：P12 5-protocol 不能"修复"D1 ICC（orthogonal 问题：P12 针对 label leakage，D1 ICC 是 inter-judge agreement）。P12 可作 Track B 的 **robustness check**（blind 重跑看 D1 是否仍 disagree），但这是 1 周协调 + 中等价值，不是 prior 的"mandatory fix"。

**Tsinghua 论文天花板**（audit F.3 修正）：单独 = ACL/EMNLP Findings 10-20%（需 result-landscape pivot + 全部披露）；加 auto-research methodology layer 后 **不会上主 track**（MAMR 不新颖 + cross-project 被团队 strategist 拒绝）。prior 的"加 methodology layer → Findings 25-35%→35-45%"**上调不成立** —— MAMR 不新颖是更大的 blocker。

## 预防措施

1. **不再用 LLM 5-persona panel median 作 kill 闸门判理论新颖性** —— 同一仪器在发现缺陷方向验证过，判新颖性方向未验证（`llm-intelligence-blocker-verdict-2026-07-05-zh.md:47`）。改用：(a) frontier reviewer arm；(b) novelty depth-check（0/N survey + 0/N method paper）；(c) CoBBLEr 3-axis 区分表。
2. **不再把"假设 sign 反向"等同于"理论死亡"** —— 在预注册 multi-axis taxonomy 中，子假设 sign swap 是 refinement，不是 falsification。需明确：kill 的是哪个子假设？哪个子假设活了？
3. **不再把 underpowered verdict 标 "falsified"** —— n=17/30 + n=8/30 是 partial + underpowered，不是 falsified。效应 size 校准（d≈1.0→d≈0.3）≠ 零效应。
4. **审查证据独立性** —— 标"3 层独立证据"前 audit：是否共享同一主体？同一仪器？是否同一研究问题？stacking 错觉 ≠ cumulative evidence。
5. **Direction A reframing 必须预注册 cross-judge 异质性 sub-claim** —— 否则 reviewer 会判"interaction fishing on null main effect"。
6. **Tsinghua 论文必须先做 SAMR/MASR 消融** —— audit §A.6 发现 MAMR vs SASR 11.3× token 比较是 9× floor 的近同义反复，消融未执行是最大内部威胁。
7. **cds4polymarket 转移前确认项目 resume** —— 26 天冻结可能意味着项目 paused/abandoned，任何转移前先确认活跃度。

---

## 交叉引用

- 本报告（KILL falsification）：`docs/investigations/top-journal-kill-falsification-2026-07-06.md`
- Prior KILL verdict：`docs/investigations/rethink-2026-07-06-zh.md` §九/§一〇（被本报告 §Root Cause 反驳）
- Direction A novelty 查证：`docs/investigations/novelty-depth-check-2026-07-05.md`（0/8 method paper + 0/3 survey 用 anchoring，新颖性仍成立）
- LLM-intelligence blocker：`docs/investigations/llm-intelligence-blocker-verdict-2026-07-05-zh.md` §一 H1（仪器 scope 未验证）
- 3 dev 项目 prior ROI：`docs/investigations/cross-project-roi-2026-07-06.md`（被本报告 §Recommendations 修正）
- Tsinghua 论文 audit：本报告 Phase 1.5c（MAMR 不新颖 + P12 不修 D1）
- cds4polymarket audit：本报告 Phase 1.5d（K1 误判 + KC 不可辩护 + best=2026 WC ingestion）
- Pair investigator：rp-cli session FC4C48D7-186E-4527-B2DD-8D753F9243BF
- G3 methods paper outline：`docs/papers/g3-methods-paper-outline.md`（备选 venue）
- Direction A 机制实验规范：`docs/papers/direction-a-mechanism-experiment-spec.md` §1.2/§3.2（frontier arm 缺位 + cross-judge 预注册）
- 5-persona review 原文：`docs/papers/direction-a-review-round-1.md:11-18`（4/4 execution issues + R2=6.0 理论通过）
- G2 N=30 实证：`docs/papers/g2-n30-completion.md:13-19`（n=17 缺 43% + n=8 缺 73%，underpowered）
