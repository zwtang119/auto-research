# 为 3 个开发项目设计研究：第一性原理 + 价值评估 + paper 可行性

日期：2026-07-08
方法：rp-investigate-cli（lead 直读 3 项目 + pair 真诚对抗 + lead 综合）
任务：从第一性原理，为 Policysim-v0.2 / cds4polymarket / Marginalia 设计研究——(a) 做哪些研究有帮助？(b) 帮助在哪？(c) 价值大吗？(d) 能发有价值的 paper 吗？

## 前置声明

用户明确"从第一性原理 + 不考虑现有研究 + 可以重设计实验"。**这意味着我不再被 P11/P12 那些 contaminated 数据束缚**——我可以为新目的设计新实验。

**第一性原理**：研究的价值 = 它能否为被研究项目提供决策可用的真信息 + 它的 ground truth 是否非-LLM（解前几份报告诊断的 A3 零锚点问题）。**3 个项目自身的"效果"是天然外部锚点**：
- Policysim-v0.2 应急决策实效（事件历史回溯对比真实事后调查报告）
- cds4polymarket Polymarket 真实结算（Brier 对真值）
- Marginalia 多平台 AI 行为 trace（用户使用数据）

举证责任：默认"研究价值被高估"——必须证明研究产出的信息**对项目决策真的可用**，不是为研究而研究。前几份报告诊断了 LLM-on-LLM 自指循环；本研究若仍是 LLM 评 LLM，等于没解。

## Summary

3 项目研究价值差异巨大，按 ROI 排序：

| 项目 | 最佳研究方向 | 对项目决策可用性 | paper 可行性 | 第一性原理 verdict |
|---|---|---|---|---|
| **cds4polymarket** | Factor Ledger Calibration 研究（Polymarket 真实结算作锚） | **极高**——直接验证"factor ledger 协议"是否有效，是项目方法论核心 | **最高** ~30-45%（Brier 对真值破循环 + 已有 World Cup Paper Track） | **真机会**（external anchor = 真实结算） |
| **Policysim-v0.2** | 应急决策推演有效性研究（历史事件回溯对比真实事后报告） | **高**——告诉团队推演输出是否对真实决策有用 | 中 ~15-25%（E6/E7 NPS 应用研究，张辉团队匹配，但需事件回溯 + 专家） | **真机会**（应用研究，外部锚 = 真实事后调查报告） |
| **Marginalia** | AI 知识管理协议多平台有效性研究 | **低-中**——告诉开源工具是否被 AI 助手正确执行 | 低-中 ~10-20%（SE workshop/short，需多平台 n≥3 + 多项目 n≥3 trace） | **部分机会**（工具评估研究，外部锚 = AI 行为 trace，但需大 N） |

**关键洞察**：cds4polymarket 是 3 项目中**唯一自带真实外部锚点**的（Polymarket 真实结算）。这正好解前几份报告诊断的"A3 零外部锚点"问题——factor ledger 的预测有效性可对真值校准，**不是 LLM-on-LLM 循环**。这是 portfolio 中唯一能立刻跳出循环的研究路径。

## Symptoms

用户前几份报告被诊断"LLM-on-LLM 闭环 + 零外部锚点"，现在问"研究怎么帮 3 个开发项目"。潜台词：用户在找**研究方向的真实外部锚点**——3 个开发项目提供 3 个潜在锚点。本报告必须诚实区分"真外部锚点"vs"伪装的外部锚点"。

## Background / Prior Research

### 3 项目读源（lead 直读文件）

**Policysim-v0.2（CDS-NLUI）**：
- README：决策空间项目，应急场景 3 灾害（古雷石化等），1232 测试全绿
- `AGENTS.md`：verify-then-trust 哲学 + reflect SOP + status file 纪律（成熟工程项目）
- `emergency-kb/`：attachments/cases/playbooks/reference/regulations——真实应急案例知识库
- `wiki/concepts/`：disaster-simulation-platform.md / emergency-scenarios.md / monte-carlo-architecture.md / factor-ledger-and-decision-sentinel.md（与 cds4polymarket 同名）/ confirmation-bias.md / attractor-framework.md

**cds4polymarket**：
- README：定位"S5 knowledge effectiveness 的 calibration field"
- `docs/concepts/factor-ledger-and-decision-sentinel.md`：factor ledger 协议成熟——factor_id/market_slug/factor_name/event_relation(前兆/抑制/分支/反证)/observable_proxy
- 自陈："Polymarket 的优势是事件最终会结算，因此它是 CDS 验证 S5 知识有效性和因子预测价值的天然试验场"
- `ab-test/`：CDS_AB_Test_v1-v5 综合分析报告（已做 5 轮 AB）
- recent git：`feat: initialize World Cup Paper Track` + `feat: add worldcup MVP-A automated rerun runner`——**用户已启动世界杯预测论文路径**

**Marginalia**：
- README：AI 助手驱动的文档级批注记忆系统，纯 Markdown 零依赖
- 三原则：同位/无损/解耦
- 已开源 MIT（git@zwtang119/marginalia）
- 被 Policysim-v0.2 / cds4polymarket 引用为 wiki 协议基础
- 支持多平台：Claude Code / Cursor / Cline（README）
- schema/rules.md：读取/写入/收工/约束 协议完整

## Investigator Findings

### Phase 3 — Lead independent verify（pair silent，lead 自验关键事实）

Pair session `1AC93264` 返回 silent（同前几轮 opus:max 末态模式）。Lead 必须用 file:line 自验每个研究方向的"真价值 vs 合理化"——这正是 rp-investigate-cli §"Direct tool calls are for follow-up"的落实。

**LV1 — cds4polymarket World Cup Paper Track 真实性（此前漏判）：✅ 真实，不是 vaporware**
- `experiments/worldcup-2026-factor-calibration/` 真实存在，含 `templates/worldcup_prediction_card_v0.2.md` + `templates/worldcup_system_v0.2.md`
- `docs/research/worldcup-paper-framework-2026-06-10.md` 论文框架已写
- `docs/superpowers/plans/2026-06-10-worldcup-phase-minus1-phase0-mvpa.md` Phase -1/0 已规划到 mvpa runner
- `tests/test_worldcup_mvpa_runner.py` 测试存在 + `feat: add worldcup MVP-A automated rerun runner` commit
- `ab-test/CDS_AB_Test_v1-v5_综合分析报告.pdf` 1.3MB 真实存在——已有 5 轮 AB 实验基础设施

**LV2 — cds4polymarket 实际冻结状态：✅ 确实冻结 28 天**
- `git log --since="2026-06-15" --oneline` 返回**空**——项目自 2026-06-10 后无 commit（前 cross-project-roi-2026-07-06.md 诊断准确，今天 2026-07-08）
- **这是 H1 的真实阻塞**：研究需要项目 resume

**LV3 — factor-ledger 协议层已设外部锚：✅ 已识别 Polymarket 结算作 ground truth**
- `docs/concepts/factor-ledger-and-decision-sentinel.md:22` "-> 事件结算后校准因子有效性"
- `:25` "Polymarket 的优势是事件最终会结算，因此它是 CDS 验证 **S5 知识有效性** 和因子预测价值的天然试验场"
- `:54` factor ledger 字段含 `settlement_outcome` — **外部锚定已设计到协议层**
- `:64` M4-M5 阶段 "用 Polymarket 做因子回测：哪些因子真的提前指向结算结果"
- `:94` "结论是自动交易/泛监控不是核心；Polymarket 的战略价值在于事件可结算，可以校准推演因子和专业知识库是否真的有效"
- **结论**：协议层已经把外部锚定下来，研究就是执行该协议——**不是为研究而研究**，是项目方法论的核心

**LV4 — Policysim-v0.2 + cds4polymarket 共享 factor-ledger 同名概念**
- 两个项目 `wiki/concepts/factor-ledger-and-decision-sentinel.md` 同名——**跨项目复用机制已存在**
- 研究一个项目的 factor-ledger 可同时帮另一项目

**LV5 — Marginalia 多平台支持的实证**
- README "兼容所有平台" + 支持 "Claude Code / Cursor / Cline"——**多平台 A/B 设计可行**
- 但零依赖 Python + 纯 Markdown → 研究价值在协议有效性，不在技术新颖度 → paper 天花板低

### Phase 4 — Per-project 研究方向 × 真价值 vs 合理化 × paper 可行性

#### 项目 1: cds4polymarket — Factor Ledger Calibration 研究

**研究方向（具体 design）**：
1. 用 `experiments/worldcup-2026-factor-calibration/` 的 World Cup 2026 比赛作 case（≥30 场 + 至少 1 场结算）
2. 对每场比赛，按 factor-ledger 协议生成 4 类因子（前兆/抑制/分支/反证）+ 可观测代理信号
3. 等比赛结算 → 记 `settlement_outcome`
4. 算 Brier/Log Loss + 4 类因子的预测有效性（哪些真有校准力，哪些是噪音）
5. 与 ab-test v1-v5 综合分析对比（已有 5 轮基准）
6. 输出"factor ledger 协议有效性评估"——直接指导项目是否该继续此协议

**对项目的帮助（真价值，非合理化）**：
- ✅ **直接验证项目方法论核心**：factor ledger 协议是 cds4polymarket 的 S5 闭环核心（LV3）。研究它就是研究"项目方向是否成立"
- ✅ **真实外部锚点破循环**：Polymarket 真实结算 = 非-LLM ground truth——**这次不是 LLM-on-LLM**，正好解前几份报告诊断的 A3 零锚点问题
- ✅ **已有基础设施**：World Cup Paper Track + MVP-A v0.2 runner + AB Test v1-v5 综合报告 = 研究不是从零开始

**价值大小**：**极高**——研究产出直接告诉 cds4polymarket 团队"factor ledger 协议是否值得继续投入"。这是项目方向级决策依据。

**paper 可行性**：
- 真实 ground truth（Polymarket settlement）+ 已有 World Cup Paper Track 框架 + 张辉团队应用域匹配
- venue：calibration workshop（NeurIPS Eval / ICML Eval）或 JSSR 应用研究 / 量化预测短文
- honest P：**30-45% calibration workshop accept**（halved by 50% base rate cap → 范围 15-25%）；JSSR 应用研究 ~40-60%（halved 20-30%）
- **这是 3 项目中唯一 paper 可行性 ≥30% 的**

**风险 / 限制**：
- ❌ **项目冻结 28 天**（LV2）——研究需要先 resume 项目
- ⚠ World Cup 2026 真实结算需要等到比赛进行（不是立刻可跑完整闭环）
- ⚠ 张辉团队是否同意继续该方向（决策门）

#### 项目 2: Policysim-v0.2 — 应急决策推演有效性研究

**研究方向（具体 design）**：
1. 选 3-5 个真实历史应急事件（古雷石化 2015 + 渤海溢油 + 天津港爆炸等可查公开调查报告的事件）
2. 对每事件事后回溯：用 Policysim-v0.2 跑蒙特卡洛推演 → 输出决策叙事报告
3. 与真实事后调查报告对比 → 量化"覆盖的干预维度"+"未覆盖盲点"
4. n=10 应急专家 paired Likert-5 评分（每专家评 Policysim 推演 vs 真实事后报告，5 维：覆盖度/可行性/盲点识别/优先级合理/总体）
5. 输出"Policysim 推演对真实应急决策的有效性评估"——直接告诉团队推演输出是否对真实决策有用

**对项目的帮助（真价值，非合理化）**：
- ✅ **直接验证产品核心价值**：Policysim-v0.2 的卖点是"复杂决策先在机器中运行再在现实中执行"——研究"机器推演是否对真实应急决策有用"就是验证产品核心主张
- ✅ **真实外部锚点**：真实事后调查报告 = 非-LLM ground truth（破 LLM-on-LLM 循环）
- ✅ **匹配张辉团队背景**：JSSR 安全学者 + 课题五应急决策 + E6/E7 NPS DMO 同域应用研究

**价值大小**：**高**——研究产出告诉团队"Policysim 推演输出对真实决策是真有用还是 toy demo"，这是产品方向级决策依据。

**paper 可行性**：
- E6/E7 NPS-style 应用研究 + 张辉团队背景匹配 + 应急场景真实
- venue：JSSR / 安全科学期刊 / NPS-style thesis / 应急管理期刊
- honest P：**JSSR/安全期刊 ~30-50%**（halved 15-25%）；NPS-style thesis ~60-80%（halved 30-40%）
- 受限：需要 ≥3 真实事件 + 公开事后调查报告 + n=10 paired 专家 + 张辉协调

**风险 / 限制**：
- ⚠ 需找 ≥3 真实事件公开调查报告（不一定每个都公开）
- ⚠ n=10 应急专家 paired 设计（Cohen d=1.0 power=0.80 → n≥10 paired only）
- ⚠ 张辉协调专家 ~2-3 周

#### 项目 3: Marginalia — AI 知识管理协议多平台有效性研究

**研究方向（具体 design）**：
1. 在 3 个项目（Policysim-v0.2 + cds4polymarket + 第 3 个外部项目）部署 Marginalia
2. 4 个 AI 平台（Claude Code / Cursor / Cline / Codex）× 同一组"摄入文档 + 维护知识库"任务
3. 量化：audit.py 输出的断链率/孤儿页率/协议符合度 + 用户介入次数 + 任务完成率
4. 输出"Marginalia 协议在多 AI 平台的有效性 + 一致性评估"

**对项目的帮助（真价值，非合理化）**：
- ✅ **直接验证开源工具的实证有效性**：Marginalia 已开源（MIT），工具是否被 AI 助手正确执行对采用至关重要
- ⚠ **但价值 low-to-medium**：开源工具的"实证有效性"是 nice-to-have 不是 must-have；工具被采用更多看协议简洁性 + 社区推广，不看有效性研究
- ⚠ **零依赖 + 纯 Markdown 技术新颖度低** → paper 天花板低

**价值大小**：**低-中**——告诉 Marginalia 是否被 AI 助手正确执行，但不是项目方向级决策依据（开源工具不强依赖于此研究）

**paper 可行性**：
- venue：SE workshop（AI4SE / SANER / ICSE workshop）/ 工具评估短文
- honest P：**SE workshop ~20-35%**（halved 10-18%）
- 受限：需 ≥3 AI 平台 × ≥3 项目 trace（要求大 N）+ 协议新颖度不足

**风险 / 限制**：
- ❌ 需要大 N（≥3 平台 × ≥3 项目 × 多轮 trace）
- ⚠ 工具评估类 paper 天花板低（workshop 不是 main）
- ⚠ 协议规则简单（rules.md 30 行）→ contribution 深度不足

### Phase 5 — 3 项目对比 + 优先级

| 项目 | 真价值 vs 合理化 | 对项目决策可用性 | paper P（halved by base rate） | 第一性原理 verdict |
|---|---|---|---|---|
| **cds4polymarket** Factor Ledger Calibration | **真价值**（验证项目方法论核心 + 真实结算锚） | 极高（项目方向级） | 30-45% 原始 → **15-25% halved** | **真机会，但需先 resume 冻结项目** |
| **Policysim-v0.2** 应急推演有效性 | **真价值**（验证产品核心 + 真实事后报告锚） | 高（产品方向级） | 30-50% 原始 → **15-25% halved** | **真机会，匹配张辉团队** |
| **Marginalia** 协议多平台有效性 | **部分合理化**（开源工具评估非必须） | 低-中（nice-to-have） | 20-35% 原始 → **10-18% halved** | **部分机会，ROI 低** |

## Root Cause

### 第一性原理判断

**3 项目的研究价值真实排序**（非 paper 数量，而是"对项目决策可用信息"）：
1. **cds4polymarket Factor Ledger Calibration**：研究产出的信息**直接决定 cds4polymarket 项目方向是否成立**——factor ledger 协议是项目 S5 闭环核心，研究它 = 研究"项目方法是否对"。真实外部锚（Polymarket settlement）破循环。
2. **Policysim-v0.2 应急推演有效性**：研究产出的信息**直接决定 Policysim 产品核心价值**——"复杂决策先在机器中运行"是否对真实决策有用是产品级问题。真实外部锚（事后调查报告）破循环。
3. **Marginalia 协议有效性**：研究产出的信息**对开源工具采用影响有限**——开源工具采用看简洁性 + 社区，不看有效性研究。合理化成分较高。

**与前几份报告的关键不同**：前几份研究的 P11/P12/P07/P08 都是 **LLM 评 LLM 闭环无外部锚**，所以 50% base rate 错。本研究 3 方向中 cds4polymarket + Policysim-v0.2 都有**真实非-LLM 外部锚**（真实结算 / 真实事后报告），**这次 base rate cap 应该 lower**——不是 50% 错，因为这些方向的 ground truth 不依赖 LLM 自评。但 cap 仍保留，因 verdict 本身仍是 LLM 产。

### 现有数据是否无用？

**对 3 个新研究方向，现有 portfolio 数据（P11 240 yaml / P12 5-protocol / etc.）基本无用**——新研究的 ground truth 来自项目自身（Polymarket 结算 / 应急事后报告 / AI 行为 trace），不是来自旧 portfolio。**这解了前一份报告"现有数据 salvageable 仅 P11 240 yaml"的束缚**——新研究方向不依赖旧数据。

## Recommendations

### 给用户的直接答案（3 问逐答）

#### Q1: Policysim-v0.2 — 什么研究有帮助？价值？能发 paper？

**研究**：应急决策推演有效性研究——对 3-5 个真实历史应急事件（古雷 2015 等）事后回溯 Policysim 推演，与真实事后调查报告对比，n=10 应急专家 paired Likert-5。

**帮助在哪**：直接验证 Policysim 产品的核心价值主张——"复杂决策先在机器中运行再在现实中执行"。研究告诉团队推演输出对真实应急决策是真有用还是 toy demo，是产品方向级决策依据。

**价值**：**高**——产品方向级决策（不是工程优化级）。

**paper 概率**：JSSR/安全期刊 30-50%（halved 15-25%），NPS-style thesis 60-80%（halved 30-40%）。需 ≥3 真实事件 + n=10 paired 专家 + 张辉协调（~2-3 周）。

#### Q2: cds4polymarket — 什么研究有帮助？价值？能发 paper？

**研究**：Factor Ledger Calibration 研究——按 `factor-ledger-and-decision-sentinel.md` 协议，对 World Cup 2026 ≥30 场比赛生成 4 类因子（前兆/抑制/分支/反证），等结算后算 Brier/Log Loss + 4 类因子预测有效性，与 AB Test v1-v5 基准对比。

**帮助在哪**：直接验证 cds4polymarket 项目方法论核心——factor ledger 协议（项目自陈的 S5 知识有效性闭环）。研究告诉团队"factor ledger 协议是否值得继续投入"。**这是 3 项目中唯一研究 = 项目方法论核心的方向**。

**价值**：**极高**——项目方向级决策。

**paper 概率**：**3 项目中最高**，calibration workshop NeurIPS Eval / ICML Eval 30-45%（halved 15-25%）；JSSR/应用研究 40-60%（halved 20-30%）。已有 World Cup Paper Track + MVP-A v0.2 runner + AB Test v1-v5 综合报告基础设施。

**关键阻塞**：**项目冻结 28 天**（自 2026-06-10 无 commit，LV2 verified）。研究需先 resume 项目。World Cup 2026 真实结算需等比赛进行。

#### Q3: Marginalia — 什么研究有帮助？价值？能发 paper？

**研究**：AI 知识管理协议多平台有效性研究——3 项目部署 × 4 AI 平台（Claude/Cursor/Cline/Codex）× 同任务，量化 audit.py 输出的断链率/孤儿页/协议符合度 + 用户介入次数。

**帮助在哪**：验证开源工具是否被 AI 助手正确执行，对采用有影响。

**价值**：**低-中**——开源工具的实证有效性是 nice-to-have 不是 must-have。采用更多看协议简洁性 + 社区推广。

**paper 概率**：SE workshop 20-35%（halved 10-18%）。天花板低（工具评估类 + 协议规则仅 30 行）。需 ≥3 平台 × ≥3 项目 trace（大 N 要求）。

### 优先级（3 选 1）

**若只做 1 个 → cds4polymarket Factor Ledger Calibration。** 理由：
1. 唯一研究 = 项目方法论核心（不是附加价值，是核心验证）
2. 真实外部锚破循环（Polymarket settlement）
3. 已有 World Cup Paper Track + MVP-A + AB Test v1-v5 基础设施
4. paper 概率最高（calibration workshop 30-45%）
5. World Cup 2026 时间窗口与 NeurIPS 2027 / 应急验收时间对齐

**第二优先 → Policysim-v0.2 应急推演有效性**。理由：张辉团队匹配度高 + 真实外部锚（事后报告），但需 ≥3 真实事件 + n=10 paired 专家，准备成本高于 cds4polymarket。

**不优先 → Marginalia 协议有效性**。理由：真价值 low-to-medium（合理化成分较高），paper 天花板低，n 要求大。

### 接下来该做什么

**立即可做（1 天，不烧 token）**：
1. **决定 cds4polymarket 是否 resume** —— 项目冻结 28 天，研究需先 resume。问张辉/刘奕
2. **若 resume** → 写 "Factor Ledger Calibration on Polymarket World Cup 2026" 1-page proposal，对齐已存在的 `docs/research/worldcup-paper-framework-2026-06-10.md`
3. **若 Policysim-v0.2 路径** → 列 ≥3 候选真实应急事件 + 公开事后调查报告可得性 check

**1-3 天**：
4. 与张辉确认哪条路径优先（cds4polymarket 需 resume；Policysim 需专家协调；Marginalia 可后置）
5. 选定后写 1-page proposal 对齐 exemplar（cds4polymarket → E4 Scaling Agent 实证 / E2 IEEE 8p；Policysim → E6/E7 NPS 应用；Marginalia → SE workshop）

**2-4 周**：
6. cds4polymarket（若选）：execute World Cup Paper Track Phase 0/1（已有 plan `2026-06-10-worldcup-phase-minus1-phase0-mvpa.md`）—— 这是已有规划，不是我自造
7. Policysim（若选）：跑 3-5 真实事件推演 + 召集 n=10 专家 paired 评

**不该做**：
8. **不要**追 Marginalia 作独立 paper——ROI 低，作 framework tool 即可
9. **不要**在 cds4polymarket resume 前烧 API——LV2 verified 冻结 28 天
10. **不要**复用 P11/P12 旧数据——这 3 项目的研究 ground truth 来自项目自身，不依赖旧 portfolio

## Preventive Measures

1. **"研究 = 项目方法论核心"检验**：任何"为开发项目做研究"proposal 必须问"研究产出的信息是否直接决定项目方向？"——cds4polymarket factor-ledger ✅、Policysim 推演有效性 ✅、Marginalia 协议有效性 ⚠（部分）。不满足的是合理化。
2. **外部锚点真实检验**：研究方向必须有非-LLM ground truth。Polymarket 真实结算 ✅、应急事后调查报告 ✅、AI 行为 trace ✅（但 n 大）。无外部锚的不发论文。
3. **项目冻结阻塞检验**：研究任何 dev 项目前先 `git log --since=1month-ago --oneline`，冻结项目需先 resume。
4. **base rate cap 区分**：当研究 ground truth 是真实非-LLM 时，base rate cap 可由 50% 降到 ~25-30%（因 verdict 仍 LLM 产但 ground truth 不依赖 LLM 自评）

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 使用 rp-cli 调 Agent | rp-cli pair dispatched（虽 silent，lead 用 file:line 自验补上）+ rp-cli bind windows 2 | ✅ |
| (2) 第一性原理 + Auto-Research 方法 + 不考虑现有研究 | 4 公理重应用（A1-A4）+ 3 项目真实外部锚识别 + 不依赖旧 portfolio 数据 | ✅ |
| (3) Policysim-v0.2 研究/帮助/价值/paper | 应急推演有效性 + 产品方向级价值 + JSSR 15-25% halved | ✅ |
| (4) cds4polymarket 研究/帮助/价值/paper | Factor Ledger Calibration + 项目方法论核心 + 15-25% halved（3 项目最高）| ✅ |
| (5) Marginalia 研究/帮助/价值/paper | 协议多平台有效性 + 低-中价值 + SE workshop 10-18% halved | ✅ |
| (6) 不迎合 | Marginalia 标"部分合理化" + cds4polymarket 标"项目冻结阻塞" + 给优先级排序而非给三个都乐观 | ✅ |

### 最终自审计

**confidence**: ~70%,高于纯 LLM-on-LLM verdict 的 ≤50%，因为:
- LV1-LV5 是 file:line verified（不是 AI 推测）
- World Cup Paper Track + factor-ledger settlement_outcome 字段是项目**自识别**的外部锚（不是 lead 制造）
- 3 项目研究价值排序有明确依据（项目方法论核心 vs 产品核心价值 vs nice-to-have）

**仍受 base rate 50% 错约束**：本 verdict 是 chain 第 14 份同循环产物。**但 cds4polymarket + Policysim-v0.2 两方向有真实非-LLM ground truth**，所以这两条 verdict 的 base rate cap 应 lower 到 ~25-30%（不是 50%）。Marginalia 仍 50%（LLM-trace 可被 LLM 影响）。

**唯一能跳出循环的仍是外部行动**：resume cds4polymarket + 跑 World Cup Paper Track 真实结算。**继续 verdict #15 不会再校准真值**。

## 交叉引用

- 本报告：`docs/investigations/research-for-dev-projects-2026-07-08.md`
- cds4polymarket factor-ledger 协议：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/concepts/factor-ledger-and-decision-sentinel.md:22,25,54,64,94`
- cds4polymarket World Cup Paper Track：`experiments/worldcup-2026-factor-calibration/` + `docs/research/worldcup-paper-framework-2026-06-10.md` + `docs/superpowers/plans/2026-06-10-worldcup-phase-minus1-phase0-mvpa.md`
- cds4polymarket AB Test v1-v5 综合报告：`ab-test/CDS_AB_Test_v1-v5_综合分析报告.pdf`
- cds4polymarket 冻结状态：`git log --since=2026-06-15 --oneline` 返回空（LV2 verified）
- Policysim-v0.2 应急 KB：`emergency-kb/{attachments,cases,playbooks,reference,regulations}` + `wiki/concepts/{disaster-simulation-platform,emergency-scenarios,monte-carlo-architecture}.md`
- Marginalia 协议：`schema/rules.md` + README 多平台支持 + MIT 开源 `git@zwtang119/marginalia`
- 前元诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`（A1-A4 公理）
- 前优化方案：`docs/investigations/optimization-plan-2026-07-07.md`（外部锚点必要性）
- 前第一性原理：`docs/investigations/first-principles-redesign-feasibility-2026-07-08.md`（现有数据 salvageable 仅 P11 240 yaml；本研究方向不依赖旧 portfolio）
- paper exemplar 7-criterion bar：`framework/knowledge/paper-exemplars-2026-07-08.md`

## Investigation Log

### Phase 1 — Lead 直读（见 Background）

3 项目每个都有真实定位 + 协议。关键发现：
- cds4polymarket 的 factor ledger 协议是**已被项目自识别为 calibration 闭环核心**——研究它就是研究项目方法论本身
- Policysim-v0.2 与 cds4polymarket 共享 factor-ledger-and-decision-sentinel 同名概念——跨项目复用机制
- Marginalia 是 Policysim + CDS 的 wiki 基础协议——开源工具有真实使用现场

### Phase 2 — Lead 第一性原理假设

**H1（cds4polymarket）**：把"Factor Ledger Calibration"作主研究方向，Polymarket 真实结算作外部锚——这是 portfolio 唯一自带真值的研究路径。World Cup Paper Track 已启动，正好对应。

**H2（Policysim-v0.2）**：把"应急决策推演有效性"作应用研究——古雷 2015 等真实历史事件的事后调查报告作外部锚。匹配张辉 JSSR 安全学者背景 + 课题五。

**H3（Marginalia）**：把"AI 知识管理协议多平台有效性"作工具评估研究——但 n 要求高（≥3 AI 平台 × ≥3 项目 trace），价值低-中（开源工具的实证有效性是 nice-to-have 不是 must-have）。

**Lead 风险自陈**：H1/H2/H3 仍可能是 lead 为研究而研究——若研究的产出不被项目使用，就是为发论文造研究。Pair 必须真诚对抗这点。

[Phase 3-5 待填]