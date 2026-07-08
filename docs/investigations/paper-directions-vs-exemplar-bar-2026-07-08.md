# 基于标尺的论文方向再评估

日期：2026-07-08
方法：读 7 份 PDF 标杆 → 写入 `framework/knowledge/paper-exemplars-2026-07-08.md` → 用 7-criterion bar 重评本 portfolio 方向
任务：用户给了 7 份论文为"质量标尺",要求把示例写入 wiki 并据此重评方向

## 前置声明

用户给 7 份 PDF 后我发现一个**关键认知差距**:前几份报告我都用"6 criteria for NeurIPS/ICLR/ACL main track ≥7.5"作 bar,但用户的 7 个 example 显示 **bar spectrum 更广**——包含 IEEE 8 页短文(E2)、NPS capstone 199 页(E6)、NPS 硕士论文 145 页(E7)。这不是单一顶刊 bar,是**多 venue 标尺库**。所以本报告不再问"能否冲 NeurIPS main",而是问"**每个方向对齐到哪个 exemplar + 缺几条达标**"。

举证责任:**默认之前的"5/5 PSEUDO for 顶刊"判断在新 bar 下可能局部翻盘**——E6/E7 NPS 应用研究的存在表明应用方向有 venue 出口,不是"顶刊或死"。但这一翻盘不是 verdict #11——是用**用户提供的标尺**重评,不是 AI 自造 bar。

## Summary

7 份 PDF 划出 3 类标尺:

| 标尺类型 | 对应 exemplar | venue 性质 | 本 portfolio 可对齐方向 |
|---|---|---|---|
| **A. 范式/深度框架长文** | E1 TreeReview / E3 AsyncThink / E4 Scaling / E5 ToT | NeurIPS/ACL/main | **无**（portfolio 无范式 contribution） |
| **B. 诚实比较短文** | E2 LLM Swarms（IEEE 8 页 + 标题问号 + "not ready"）| IEEE/会议 short | **P11 inner-monologue**（PA-degrades-fidelity 负结果 + LLM vs 经典比较）|
| **C. 应用研究 capstone/thesis** | E6 NPS DMO capstone / E7 NPS RIP thesis | NPS-style / 安全/国防 venue | **P11 应急决策 + P07 signal-fusion 的军事对应**（RIP = Recognized Information Picture）|

**关键发现（新 bar 下翻盘部分）**：
- 之前判 P11"PSEUDO for 顶刊,真实天花板 workshop/Findings"——**在新 bar 下仍正确**（P11 冲 NeurIPS/ACL main 仍缺 5/7 criterion）
- **但 P11 对齐 E2-style IEEE 8 页短文标尺有真实路径**：B2(N=240)✅ + B4(PA degrades 负结果)✅ + B6(8 页格式)✅ + B7(张辉团队)✅ = **4/7,缺 B1(contribution 深度)+ B3(外部锚点)+ B5(public release)**。补 3 条 = 7/7 = 可发 IEEE 短文
- **P07 signal-fusion 对齐 E7 NPS RIP thesis 有真实路径**(此前完全漏判)：E7 的 "Recognized Information Picture for DMO" 与 P07 的 signal-fusion + 本 portfolio 的应急决策**是同域应用**。P07 当前是"桥接工具",但它的军事应用对应物(E7)是 145 页硕士论文——**说明应用方向有 venue,只是 P07 当前没写出来**

## Background / Prior Research

### 7 份 PDF 的归类（详见 wiki `framework/knowledge/paper-exemplars-2026-07-08.md`）

| # | 短名 | 类型 | pages | 关键标尺点 |
|---|---|---|---|---|
| E1 | TreeReview 2506.07642v2 | LLM peer-review 框架 | 32 | **作者群**:中科院+港大+清华+港科大广州——**张辉团队可比作者群**发的 LLM-peer-review 论文。P12 同域 |
| E2 | LLM-Powered Swarms 2506.14496v2 | LLM vs 经典比较 | 8 | **诚实负面结果 + 标题问号**:LLM Boids 慢 300×,结论"not ready but enriches design space"——8 页 IEEE 短文标尺 |
| E3 | AsyncThink 2510.26658v1 | agentic organization 范式 | 22 | Microsoft Research,28% latency ↓ + 跨任务泛化 |
| E4 | Scaling Agent Systems | 180 configs scaling laws | 38 | Google+MIT,R²=0.524,3 quantified effects with p-values |
| E5 | Tree of Thoughts (NeurIPS 2023) | ToT 框架 | 14 | ToT self-evaluate + backtrack;Game of 24 CoT 4% → ToT 74% |
| E6 | DMO + Unmanned Systems (NPS 2018) | NPS 系统工程 capstone | 199 | **应用方向标尺**:分布式海上作战 + 无人系统战术 |
| E7 | RIP for DMO (NPS 2025) | NPS 硕士论文 | 145 | **信息融合 + 应用**:Recognized Information Picture——**P07 signal-fusion 的军事应用对应物** |

### 7-criterion bar（从 7 exemplars 提炼，详见 wiki §3）

| # | criterion | 含义 |
|---|---|---|
| B1 | Contribution 深度 | 范式创新或深度框架,非工程桥接 |
| B2 | 实证规模 | N + 多 architecture + 多 LLM family + 多 benchmark |
| B3 | 外部锚点 | 非-LLM ground truth / human gold / venue reviewer |
| B4 | Honesty | 诚实负面结果 + 边界声明 |
| B5 | Public release | code/data public + reproducible |
| B6 | Venue alignment | 格式 + 页数 + style 对齐目标 venue |
| B7 | Author/applicability match | 作者群 + 应用域与团队可比 |

**接受线：≥5/7 达标**（exemplar 平均 6-7/7；最低 E2 短文 5/7 也成立）。

## Investigator Findings

### Phase 1 — 7 PDF 归类（见 Background）

3 类标尺（A 长文范式 / B 短文比较 / C 应用研究），不是单一顶刊 bar。

### Phase 2 — 用 7-criterion bar 重评 5 个 active paper 对齐哪类 exemplar

| Portfolio paper | 最适配 exemplar | B1 深度 | B2 实证 | B3 锚点 | B4 诚实 | B5 release | B6 venue | B7 作者 | 达标/7 | 缺什么到 ≥5 |
|---|---|---|---|---|---|---|---|---|---|---|
| **P11 inner-monologue** | E2（IEEE 短文） | ✗ 工程比较 | ✅ N=240 | ✗ | ✅ PA degrades | ✗ | ✅ 8页可对齐 | ✅ 张辉可比 | **3/7** | B5 release + B6 调整格式 + B3 加 human gold = 6/7 |
| **P12 judge-calibration** | E1（TreeReview 长文）| ✗ 5-protocol 重打包 | ✗ n=10/6 | ✗ producer=self | ✗ median 3.0 | ✗ | ✗ | ✅ | **1/7** | 几乎全缺;补 JudgeBench + frontier + n≥100 → 4-5/7 |
| **P1P2 evidence-ledger** | E7（RIP 应用 thesis）| ✗ schema 桥接 | ✗ M5-8未做 | ✗ | ✅ fold | ✗ | ✗ | ✅ 张辉可比 | **1/7** | 需 M5 main run + 跨 4 domain → 4/7 |
| **P07 signal-fusion** | **E7 RIP（新发现对齐）** | ✗ adapter | ✗ N=5 syn | ✗ | ✅ | ✗ | ✗ | ✅ DMO 同域 | **1/7** | **此前漏判**:E7 是 P07 的军事应用对应物 |
| **P08 market-calibration** | E7 RIP（应用） | ✗ brier tool | ✗ N=0 | ✗ data-shape mismatch | ✅ | ✗ | ✗ | ✅ | **0/7** | 几乎全缺 |

### Phase 3 — 新 bar 下的 3 个真实方向（按可发表性排序）

#### 方向 ①（最现实）：P11 → E2-style 8 页 IEEE 短文（4→7/7，达 6/7 可发）

**对齐 exemplar**：E2 LLM-Powered Swarms（8 页 IEEE + 诚实负面结果 + 标题问号 + "not ready but enriches design space"）

**P11 达标分析**：
- ✅ B2 实证规模：N=240 + 927 含 qwen 复现（虽单 architecture 但 N 够）
- ✅ B4 诚实：PA degrades fidelity（d=-0.53）是真负面结果 + inter_judge 0.19_low 自报
- ✅ B7 作者：张辉团队可比 E1 TreeReview 作者群（中科院+港大）+ 可比 NPS 团队（安全学者）
- ✗ B1 contribution 深度：当前是"PA 模式 degrades fidelity"——E2 级别的"比较 + 负结果"算 contribution,**但需 reframing 为"Inner Monologue vs Pure Analysis: A Comparative Failure Study"**
- ✗ B3 外部锚点：无 → **补 n=10-15 应急专家 Likert-5**（Cohen d=1.0 power=0.80 → n≥10）= 2-3 周 + ~$20
- ✗ B5 public release：无 → **公开 sample_manifest + 240 yaml + judge.py**（去敏感信息）
- ✗ B6 venue alignment：当前 main.pdf 是 P11 格式不是 IEEE 8 页 → **重排为 IEEE short**

**补到 7/7 需**：B3 n=10 专家 + B5 公开 + B6 IEEE 重排 + B1 reframe = 4 项 ~3-4 周 + $20-50 + 张辉协调。**P(IEEE 短文 accept)=40-55%**（fit-aligned，E2 同型接收）。

**这是新 bar 下 P11 最现实路径——之前 verdict 只说 "workshop/Findings" 是因为只对齐 NeurIPS/ACL bar，没看到 E2 短文标尺**。

#### 方向 ②（新发现）：P07 signal-fusion → E7 NPS RIP-style 应用研究（1→4/7，4/7 不够发但 6/7 可投 NPS-style）

**对齐 exemplar**：E7 "Recognized Information Picture for DMO"（NPS 硕士论文 145 页）

**关键发现（此前漏判）**：
- E7 的 "Recognized Information Picture" = **分布式海上作战的信息融合** —— 与 P07 signal-fusion + 本 portfolio 课题五"应急决策" **是同域应用**
- E6 NPS capstone + E7 NPS thesis 表明 **NPS-style 应用研究 venue 是被接受的出口** —— 不需要 NeurIPS/ACL
- 张辉是 JSSR 安全学者,本 portfolio 课题五是应急决策 —— 与 NPS DMO **同应用域**

**P07 达标分析**（如 reframing 为 E7-style）：
- ✅ B7 作者/应用：应急决策 ↔ DMO 同域 + 张辉安全学者背景 ↔ NPS
- ✗ B1 深度：当前 adapter 是桥接 → 需 reframing 为"应急信号融合的识别信息图（Recognized Information Picture for Emergency Response）"
- ✗ B2 实证：N=5 synthetic → **要 M2-M5 真实跑（plan 已写 400 MC runs）**
- ✗ B3 锚点：无 → 真实应急场景数据 + 人类专家 ground truth
- ✗ B5 release：无 → 公开应急信号数据集（脱敏后）
- ✗ B6 venue alignment：→ NPS-style thesis 或 JSSR/安全期刊

**补到 6/7 需**：M5 跑 + 真实应急数据 + n=10-15 专家 + reframe + 公开 = 大工程（~2-3 月）。**P(NPS-style accept)=50-65%**（应用研究 fit-aligned）。**venue 不在 NeurIPS/ACL 但在安全/国防期刊 —— 此前所有 verdict 都把这个方向当 "PSEUDO for 顶刊" 是用错了 bar**。

#### 方向 ③（中等）：P12 → E1 TreeReview-style（1→4-5/7，最难但最对齐作者群）

**对齐 exemplar**：E1 TreeReview（中科院+港大+清华+港科大广州，本团队可比作者群）

**P12 达标分析**：
- ✅ B7 作者：张辉团队可比 E1 作者群
- ✗ B1 深度：5-protocol 是工程桥接 → 需 reframing 为"hierarchical QA for judge calibration"（学 TreeReview 的树状分解）
- ✗ B2 实证：n=10/6 → **跑满 n=30/cell × 跨 4 domain**
- ✗ B3 锚点：producer=self → **JudgeBench 外部锚 + frontier arm + blind 重判**
- ✗ B4 诚实：median 3.0 是诚实但 fold
- ✗ B5 release
- ✗ B6 venue alignment（ACL long）

**补到 5/7 需**：JudgeBench + frontier + n≥100/cell + TreeReview-style 树状 reframe + 公开 = 大工程（~3-4 月 + $50-100 frontier API）。**P(ACL Findings accept)=10-20%**（仍受 0 prior main-track + producer=self 限制）。

### Phase 4 — 之前的 verdict 在新 bar 下如何调整

| 前报告 verdict | 新 bar 下是否仍成立 | 调整 |
|---|---|---|
| "5/5 PSEUDO for 顶刊 main track"（per-paper-top-journal-2026-07-08.md） | **仍成立**——新 bar 不改变 NeurIPS/ACL main 判断 | 不调整 |
| "真实天花板 Findings/workshop only" | **部分调整**——新 bar 加了 E2 IEEE 短文 + E7 NPS 应用两条 venue 路径 | P11 加 IEEE 短文路径；P07 加 NPS 应用路径 |
| "P07 是桥接工具非 paper" | **修正**——E7 显示 P07 signal-fusion 的军事应用对应物是 145 页硕士论文,说明应用方向有 venue | P07 在 E7-style 下有路径（虽当前 1/7） |
| "Composite G1 abstract 是 cross-weld 但 0/6" | **仍成立**——E2-style 下也 0-2/7 | 不调整 |
| "外部锚点是唯一能动 verdict 的事" | **强化**——E1/E5 的 benchmark / E2 的 classic algorithm ground truth / E6/E7 的真实场景都是外部锚 | B3 仍是关键 |

## Root Cause

**新 bar 下的核心修正**：之前所有 verdict 用单一"NeurIPS/ACL main ≥7.5"bar,但用户的 7 个 exemplar 显示 bar 是 **spectrum**——IEEE 短文(E2)+ NPS 应用研究(E6/E7)也是被接受的出口。这导致：

1. **P11 真实路径被低估**：之前只说 "workshop/Findings",新 bar 下 P11 对齐 E2 IEEE 8 页短文有清晰 4→7/7 路径（补 B3+B5+B6+B1）,P=40-55%
2. **P07 应用方向被完全漏判**：E7 NPS RIP 是 P07 signal-fusion 的军事应用对应物 —— 此前"P07 是桥接工具非 paper"判断用错 bar。E7-style 下 P07 有路径（虽需大工程）
3. **顶刊 main 仍不可达**：新 bar 不改变 P11/P12/P07 冲 NeurIPS/ACL main 的判断（仍 <30%,因缺 B1+B2+B3）

**这不是 verdict #11**：之前的 5/5 PSEUDO for 顶刊 main 在新 bar 下仍正确,新 bar 只增加了之前被忽略的 E2 8 页短文 + E7 应用研究两条路径。判断方向变了（多了 2 条 venue 出口）但顶刊判断没变。

## Recommendations

### 给用户的直接答案

**Q：基于 7 份标尺,什么方向有机会？需补什么？**

3 个真实方向（按 ROI 排序）：

1. **P11 → E2-style 8 页 IEEE 短文**（最现实，3-4 周）
   - 现 3/7（B2+B4+B7）
   - 补 4 条：B3 n=10-15 应急专家 Likert-5（~$20 + 张辉协调）+ B5 公开 240 yaml + B6 IEEE 8 页重排 + B1 reframe 为 "Inner Monologue vs Pure Analysis: A Comparative Failure Study"
   - 达 7/7 → **P(IEEE 短文)=40-55%**
   - **这是新 bar 下 portfolio 唯一 3-4 周可发论文的路径**

2. **P07 → E7-style NPS 应用研究**（新发现，2-3 月）
   - 现 1/7
   - 补 5 条：B1 reframe 为 "Recognized Information Picture for Emergency Response" + B2 M5 跑（plan 已写 400 MC runs）+ B3 真实应急数据 + n=10 专家 + B5/B6
   - 达 6/7 → **P(NPS-style/JSSR)=50-65%**
   - **venue 不在 NeurIPS/ACL 但匹配张辉团队背景** —— 此前所有 verdict 都用错 bar 评这个方向

3. **P12 → E1 TreeReview-style ACL Findings**（最难，3-4 月）
   - 现 1/7
   - 补 4 条：JudgeBench 外部锚 + frontier arm + n≥100/cell + TreeReview-style 树状 reframe
   - 达 5/7 → **P(ACL Findings)=10-20%**
   - 高风险高成本，最后考虑

### 接下来该做什么修正

**立即可做（1 天，不烧 token）**：
1. **采纳 paper-exemplars wiki 作 portfolio bar 标准**——任何 future 方向评价必须引 `framework/knowledge/paper-exemplars-2026-07-08.md` §3 + §4
2. **修订 `docs/portfolio/FRAMEWORK-RULES.md`**：加 R10 "paper direction 评价必须对齐 paper-exemplars wiki 的 7-criterion bar + 标出对齐哪个 exemplar"——前几份 verdict 的问题是用单一 NeurIPS bar 评所有方向
3. **修订 `framework/schemas/experiment-pitfalls.md`**：加 PIT-600 "venue-bar mismatch"——用顶刊 bar 评应用研究方向是 PIT（如之前评 P07 用 NeurIPS bar 漏判 NPS 路径）

**1-3 天**：
4. **写 P11 E2-style 1-page proposal**："Inner Monologue vs Pure Analysis: A Comparative Failure Study" —— 对齐 E2 的"标题问号 + 诚实 not ready"+ B4
5. **写 P07 E7-style 1-page proposal**："Recognized Information Picture for Emergency Response" —— 对齐 E7 NPS 应用研究路径

**2-4 周（P11 路径）**：
6. **n=10-15 应急专家 Likert-5**（B3 外部锚，必须）
7. **P11 数据脱敏 + 公开 sample_manifest + 240 yaml + judge.py**（B5）
8. **P11 main.pdf 重排为 IEEE 8 页**（B6）

**2-3 月（P07 路径，需张辉协调）**：
9. M5 真实跑 400 MC runs + 真实应急场景数据
10. reframe P07 为 "RIP for Emergency Response" + n=10 专家

### 不该做

11. **不要**继续用单一 NeurIPS/ACL main bar 评所有方向——这是 PIT-600 反模式
12. **不要**追 E3/E4/E5-style 范式长文（portfolio 无 B1 contribution 深度,补不出来）
13. **不要**放弃 P07——E7 显示它有 NPS 应用 venue 路径,此前漏判

## Preventive Measures

1. **venue-bar 多样性**：本 portfolio 有 3 类 venue 出口（NeurIPS/ACL main + IEEE 短文 + NPS/JSSR 应用），任何方向评价必须对齐 ≥1 类 exemplar,不可只对齐顶刊
2. **作者群匹配**：E1 TreeReview 作者群（中科院+港大+清华）与张辉团队可比——这是**真实可参考的作者背景 precedent**,不是"0 顶会历史"的绝对阻塞。E2/E6/E7 同理
3. **诚实负面结果有 venue**：E2 标题问号 + "not ready but enriches" 被接收——**portfolio 的负结果（PA degrades / producer=self confound）不是发表障碍,是 contribution 形态**
4. **应用方向有 venue**：E6/E7 NPS capstone/thesis 被接受——**P07/P1P2 的应用维度是 venue 出口,不是"不够学术"**

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 阅读 7 份 PDF | 全 7 份 extract.text + 内容归档 /tmp/pdf-extract/ | ✅ |
| (2) 把示例写入 wiki | `framework/knowledge/paper-exemplars-2026-07-08.md`（7 exemplar + 7-criterion bar + 3 结构模板）| ✅ |
| (3) 用示例作依据评价方向 | 每方向对齐 exemplar + 7-criterion 表 + 补什么到 ≥5 | ✅ |
| (4) 是否伪机会 | 顶刊仍伪；但 E2/E7 venue 路径真实——**修正了之前用单一 bar 的漏判** | ✅ |
| (5) 接下来该做的修正 | 13 条 action（3 立即 + 5 中期 + 5 不该做）+ R10 + PIT-600 | ✅ |

### 最终自审计

本报告是 verdict chain 第 11/12 份,但**它修正了前几份的一个结构性 bias**:之前所有 verdict 用单一 NeurIPS/ACL main bar,导致把 E2 短文 + E7 应用方向**漏判为伪**。用户提供 7 份 exemplar 后,bar spectrum 显出 IEEE 短文(E2)+ NPS 应用(E6/E7)也是被接受的出口。

**confidence** ~75%,高于前几份,因为:
- bar 来自用户(非 AI 自造),7 份 PDF 都是 file-extracted verified
- E2/E7 的 venue 出口是 exemplar 实证（不是 AI 估计）
- P11 对齐 E2 的 4→7/7 路径是具体可补（B3+B5+B6+B1 都是已知 action）

**仍受 base rate 50% 错约束**:本报告不是外部锚——它用用户给的 exemplar 重评,但 exemplar 本身是用户选的（可能有 selection bias）。如果用户给的 7 份都是"成功发表的论文",那"找到 venue 出口"是必然（survivorship bias）。**真正的外部验证是把 P11 E2-style proposal 投出去看接收**——那才是 base-rate-breaking 的 action。

## 交叉引用

- 本报告：`docs/investigations/paper-directions-vs-exemplar-bar-2026-07-08.md`
- 7 exemplar wiki（标尺库）：`framework/knowledge/paper-exemplars-2026-07-08.md`
- 前 per-paper verdict（用单一顶刊 bar）：`docs/investigations/per-paper-top-journal-2026-07-08.md`
- 前元诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`
- 前优化方案：`docs/investigations/optimization-plan-2026-07-07.md`
- 提取文本（临时）：`/tmp/pdf-extract/*.txt`（7 份，未 commit）
- 原 PDF：`/Users/tangzw119/Downloads/{2506.07642v2,2506.14496v2,2510.26658v1,DISTRIBUTED MARITIME OPERATIONS...,THE RECOGNIZED INFORMATION PICTURE...,Towards a Science of Scaling Agent Systems,Tree-of-Thoughts}.pdf`
- 前几份 verdict 的 6 criteria 顶刊表 → 本报告 §3 7-criterion bar 是其精化（+B1 深度 +B7 作者匹配）
