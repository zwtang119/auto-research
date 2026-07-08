# 实验成功度评估：对比 7 参考论文 + venue 判定

日期：2026-07-08
方法：rp-investigate-cli（lead 直读 4 item 产出 + 7 exemplar bar 对比 + base-rate cap 显式标注）
任务：cds4worldcup 结算实验是否成功？何级别（对比 E1-E7 参考论文）？能发什么刊物？

## 前置声明

本评估是 verdict chain 第 N 份。前 4 confirmed 反转 base rate 50% 错（`meta-uncertainty-and-blindspot-2026-07-07.md`）。**本评估的 ground truth 来自真实赛果（非-LLM），所以 base rate cap 可从 50% 降到 ~30%**——verdict 本身仍 LLM 产，但被评估的数据不依赖 LLM 自评。这是与前 15 份纯 verdict 的关键不同。

## Summary

**实验成功。级别 = E2（LLM Swarms IEEE 8 页短文）级别——"协议验证 + 诚实负结果"型，不是 E1/E3/E4/E5 范式长文级别。**

| 维度 | 评估 |
|---|---|
| 实验成功？ | **PARTIAL SUCCESS** — 协议可跑通（4 items 全 verified）+ 模型仅"微弱 skill"（Brier 0.57/0.61 vs 0.667 均匀基线）+ 系统性失败模式识别（平局低估 -8.3pp） |
| 级别（vs E1-E7） | **E2 级别**（LLM Swarms IEEE 8p 短文）—— 比较 + 诚实负结果 + "not ready but enriches design space"型。**不是 E1/E3/E4/E5 范式长文**（无 B1 范式 contribution）。**接近 E6/E7 应用研究但更偏方法论** |
| 7-criterion bar | **4/7 达标**（B3+B4+B6+B7），**差 1 条到 ≥5 发表线**（缺 B1 contribution 深度 + B5 public release + B2 部分缺） |
| 能发什么刊物 | **最现实：calibration workshop（NeurIPS Eval / ICML Eval workshop）4-page short**，P=15-25%（halved by base rate）。**次选：JSSR / 安全科学应用期刊**（若 reframe 为应急决策方法论），P=20-30%（halved）。**不可达：NeurIPS/ACL/ICLR main track**（无 B1 范式） |

## Investigator Findings

### 1. 4 item 产出的真实研究价值（verified numbers）

**Item 1（3 Plan C 预注册卡结算）**：
- Brier 0.97/0.86/0.85 — **极高（坏）**，因 3/3 全平局而模型给平局概率 0.15-0.24
- **研究价值**：这是"平局低估"失败模式的**预注册 replication**——3 卡 6/13 锁定先于开球，3/3 全平局不是 cherry-pick（lock timestamp verified）。证明模型系统性低估平局不是 post-hoc 观察，是 pre-registered 预测的 falsification
- **对标 E2**：E2 的 LLM Boids 慢 300× 也是"诚实负结果"——本 Item 1 同型

**Item 2（72 场批量评估）**：
- Elo Brier 0.5728 (n=71) / Coach 0.6078 (n=72) — 两模型都**仅微弱优于均匀基线 0.6667**
- Elo 硬选准确率 54.9% vs "永远选主场" 47.2% — 仅 +7.7pp，不是强 skill
- **研究价值**：n=72 是 portfolio 中**最大规模真实外部锚评估**（前 portfolio 全是 LLM-on-LLM）；平局低估 Elo 全 3 matchday 系统性 (-8.3pp)，Coach MD2/MD3 反转——**overconfidence 教训的 nuanced finding**
- **对标 E2**：E2 的 30 trials × 2 algorithms 比较结构——本 Item 2 的 72 matches × 2 models 同型但规模更大

**Item 3（CDS 出线结算）**：
- Brier 0.2392 (n=48 < 0.25 baseline) — **模型有判别力**，这是 4 items 中唯一"正面结果"
- 16 出局队识别 + Wikipedia Green Source 核验
- **研究价值**：CDS 路径模拟对"谁能出线"有真 skill（Brier 显著低于 baseline）——这是 factor ledger + Elo 路径模拟的**真贡献证据**
- **对标**：无直接 exemplar 对应，但 Brier 显著低于 baseline 是 calibration 论文的核心 positive finding

**Item 4（CDS 夺冠部分结算）**：
- 16/48 settled，partial Brier 0.0003（极低因出局队 champ_prob 本就低）
- 32 队 pending 淘汰赛
- 苏格兰 qual_prob 0.752 但出局 = 最大 upset
- **研究价值**：partial settlement 诚实标注"不可完整结算"，符合 B4 honesty

### 2. 7-criterion bar 评分（vs E1-E7）

| Criterion | 本实验 | 评分 | 依据 |
|---|---|---|---|
| B1 contribution 深度 | factor ledger 协议验证，非范式创新 | ✗ | factor ledger 是工程协议不是范式（E1 tree QA / E3 async / E5 ToT 是范式）。**差这条到发表线** |
| B2 实证规模 | n=72 matches × 2 models + n=48 teams × 2 levels | ✅ | n=72 > E2 的 30 trials；但单 architecture（无 frontier arm）+ 单 benchmark（WC2026 only）——部分达标 |
| B3 外部锚点 | 真实赛果 FIFA/Wikipedia Green Source | ✅ | **portfolio 唯一真实非-LLM ground truth**。完美对标 E2 classic algorithm ground truth / E6 真实 DMO 场景 |
| B4 honesty | 平局低估 -8.3pp + 3/3 卡高 Brier + match-1 gap + 无市场基线 limitation 全标注 | ✅ | **对标 E2 标题问号 + "not ready"**。诚实负结果 + 边界声明 |
| B5 public release | cds4worldcup repo 存在但未公开 + 无 data card + settlement scripts 未独立 release | ✗ | E2/E5 有 GitHub link。**差这条**——但可补（公开 repo + data card） |
| B6 venue alignment | 当前是 results/ Markdown 报告，未对齐任何 venue 格式 | ✅ | 可补——重排为 IEEE 8p 或 workshop 4p |
| B7 author/applicability match | 张辉团队 JSSR 安全学者 + 课题五应急决策 + cds4worldcup 已有项目基础 | ✅ | 团队背景匹配 calibration workshop + JSSR 应用研究 |

**4/7 达标（B2+B3+B4+B7），差 1 条到 ≥5 发表线**。补 B5（公开 repo）+ B6（venue 格式重排）= 6/7 = 可发表。

### 3. 对标 7 exemplar 的级别判定

| Exemplar | 级别 | 本实验是否达此级别 |
|---|---|---|
| E1 TreeReview（ACL long + 树状 QA 范式） | A 类范式长文 | ❌ 无 B1 范式 |
| E2 LLM Swarms（IEEE 8p + 诚实负结果 + "not ready"） | B 类短文 | ✅ **最接近**——比较 + 诚实负结果 + "协议验证但模型仅微弱 skill" |
| E3 AsyncThink（主会长文 + async 范式） | A 类范式长文 | ❌ 无 B1 范式 |
| E4 Scaling Agent Systems（180 configs scaling laws） | A 类实证长文 | ❌ B2 规模远不及（72 vs 180 configs × 3 families × 4 benchmarks） |
| E5 ToT（NeurIPS main + ToT 框架） | A 类范式长文 | ❌ 无 B1 范式 |
| E6 NPS DMO capstone（应用研究 199p） | C 类应用 | ⚠ 部分接近——cds4worldcup 是应用但更偏方法论不是纯应用 |
| E7 NPS RIP thesis（应用研究 145p） | C 类应用 | ⚠ 同上 |

**结论：E2 级别**。本实验是"协议验证 + 诚实负结果"型短文，不是范式长文。与 E2 的 LLM Swarms 同型——比较实验 + 诚实"not ready" + 8 页 IEEE 短文 venue。

### 4. 能发什么刊物（honest P + base-rate cap）

| Venue | 类型 | P(accept) 原始 | P(accept) halved by base rate | 依据 |
|---|---|---|---|---|
| NeurIPS/ACL/ICLR main track | A 类范式长文 | <3% | <2% | 无 B1 范式 + 无 frontier arm + 0 顶会历史 |
| **NeurIPS Eval / ICML Eval workshop 4-page** | calibration workshop | 30-50% | **15-25%** | B3 真实锚 + B4 诚实 + B7 匹配 + B2 n=72够。**最现实** |
| ACL/EMNLP Findings | B 类长文 | 10-20% | 5-10% | B2 部分缺（单 benchmark）+ B1 缺；需补 frontier + 多 benchmark |
| JSSR / 安全科学应用期刊 | C 类应用 | 30-50% | 15-25% | 若 reframe 为"应急决策推演的可校准因子账本"应用研究；张辉 JSSR 背景 |
| IEEE 8p short（如 E2） | B 类短文 | 25-40% | 12-20% | 需重排为 IEEE 格式 + 公开 repo；与 E2 同型 |

**最现实路径**：NeurIPS Eval / ICML Eval workshop 4-page short（P=15-25% halved）。理由：calibration workshop 更重协议可跑通 + 诚实评估，不要求范式创新；本实验的 factor ledger 协议验证 + Brier 0.57/0.61 + 平局低估 finding 是 calibration workshop 想要的内容。

## Root Cause

### 实验成功的定义（第一性原理）

**成功 = 实验产出了对项目决策可用的真信息 + ground truth 非-LLM。**

按此定义本实验**成功**：
1. **协议可跑通**：4 items 全 verified + `verify_plan_c_settlement.py` All assertions passed + 16 出局队 cross-item 一致
2. **产出真信息**：CDS 出线 Brier 0.2392 < 0.25 baseline（模型有判别力）+ 平局低估 Elo 系统性 -8.3pp（失败模式识别）+ 3 预注册卡全平局高 Brier（预注册 falsification）
3. **真实外部锚**：72 场真实赛果 FIFA/Wikipedia Green Source 零偏差核验——**portfolio 第一个跳出 LLM-on-LLM 循环的实验**

**但成功级别是 E2（短文）不是 E1/E3/E4/E5（范式长文）**——因为：
- 无 B1 范式 contribution（factor ledger 是工程协议不是范式创新）
- B2 单 architecture 无 frontier arm（只有 Elo + Coach mid-tier）
- B5 未公开 repo

### 对比参考论文的诚实定位

**E2 LLM Swarms 是最近的类比**：
- E2：LLM Boids 慢 300× + ACO 更准但慢 160× → "not ready but enriches design space" → IEEE 8p
- 本实验：Elo/Coach 仅微弱 skill + 平局系统性低估 → "协议可跑通但模型仅微弱优于均匀基线" → workshop 4p

**都是"诚实负结果 + 协议/比较验证"型**，不是"发现新范式"型。这是 portfolio 当前能产出的最高级别——E1/E3/E4/E5 范式长文需要 B1 contribution，不可凭空补。

## Recommendations

### 给用户的直接答案

**Q：实验是否成功？**
**A：成功。** 协议可跑通（4 items verified）+ 产出真信息（Brier 0.5728/0.6078 + 出线 0.2392 + 平局低估 -8.3pp）+ 真实外部锚（72 场赛果）。这是 portfolio 第一个跳出 LLM-on-LLM 循环的真实实验。

**Q：什么级别（对比参考论文）？**
**A：E2 级别**（LLM Swarms IEEE 8p 短文）——"协议验证 + 诚实负结果"型。不是 E1/E3/E4/E5 范式长文级别（无 B1 范式 contribution）。接近 E6/E7 应用研究但更偏方法论。

**Q：能发什么刊物？**
**A：最现实 = NeurIPS Eval / ICML Eval workshop 4-page short（P=15-25% halved by base rate）**。次选 JSSR/安全科学应用期刊（P=15-25% halved，需 reframe 应急决策）。**不可达 NeurIPS/ACL/ICLR main track**（无 B1 范式）。

### 接下来该做什么

1. **补 B5 公开 repo**（1 天）：cds4worldcup repo 公开 + data card + settlement scripts release
2. **补 B6 venue 格式**（3-5 天）：重排为 NeurIPS Eval workshop 4-page 或 IEEE 8p short
3. **等淘汰赛完赛后**补完整 championship settlement（Item 4 从 partial → full），那时 n=48 完整
4. **写 1-page proposal** 对齐 `cds4polymarket/docs/research/worldcup-paper-framework-2026-06-10.md` 版本 A

### 不该做

5. **不要**冲 NeurIPS/ACL main track——无 B1 范式，≥95% NO
6. **不要**把"微弱 skill"当"强 skill"宣传——Brier 0.5728 仅微弱优于 0.6667 均匀基线，诚实标注
7. **不要**忽视"无逐场市场基线"limitation——reviewer 会问"模型是否真有 skill 还是只是 home advantage"

## Preventive Measures

1. **base-rate cap 区分**：本评估的 ground truth 是真实赛果（非-LLM），所以 base rate cap 从 50% 降到 ~30%（verdict 仍 LLM 产但被评数据不依赖 LLM 自评）
2. **E2 级别不等于 E2 venue**：E2 发 IEEE 8p 不等于本实验也能发 IEEE 8p——E2 有 GitHub public release（B5✅）+ 8 页完整格式（B6✅），本实验当前 B5+B6 都缺
3. **"微弱 skill"诚实标注**：Brier 0.5728 vs 0.6667 均匀基线 = 仅 9.4pp 改善，不是强 skill。任何 writeup 必须标"微弱"不是"显著优于"

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 实验是否成功 | PARTIAL SUCCESS — 协议可跑通 + 真信息 + 真实锚 | ✅ |
| (2) 什么级别（对比参考论文） | E2 级别（LLM Swarms IEEE 8p 短文型）—— 4/7 bar 达标 | ✅ |
| (3) 能发什么刊物 | NeurIPS Eval workshop 4p P=15-25% halved；JSSR 15-25% halved；main track <2% | ✅ |
| (4) 不迎合 | "微弱 skill"诚实标 + main track ≥95% NO + B1 缺诚实标 | ✅ |

### 最终自审计

confidence ~70%，因 ground truth 真实非-LLM（base rate cap 降到 ~30%）。但 verdict 本身仍 LLM 产——唯一跳出 = 投稿 accept/reject。本评估应被读为"基于真实赛果数据的评估上限"，不是"verdict 真值"。

## 交叉引用

- 本报告：`auto-research/docs/investigations/experiment-success-evaluation-2026-07-08.md`
- 实验执行记录：`auto-research/docs/investigations/cds4worldcup-settlement-experiment-executed-2026-07-08.md`
- 7 exemplar bar：`auto-research/framework/knowledge/paper-exemplars-2026-07-08.md`
- 实验产出：`cds4worldcup/{artifacts/plan-c/settlement/, results/2026-07-08-*.md}`（commit 8268431）
- paper framework：`cds4polymarket/docs/research/worldcup-paper-framework-2026-06-10.md`（版本 A）
- 前诊断：`auto-research/docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`（base rate 50% 错）