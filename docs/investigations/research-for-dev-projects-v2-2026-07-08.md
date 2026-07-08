# 重答 3 项目研究方向（Auto-Research 方法视角）+ 文档清理记录

日期：2026-07-08
方法：rp-investigate-cli（前答 `research-for-dev-projects-2026-07-08.md` 的深化 + Q4 文档清理执行）
任务：(1-3) 再次答 3 项目研究方向，从 Auto-Research 方法视角；(4) 整理文档

## 前置声明（这次与前答的关键不同）

前答 `research-for-dev-projects-2026-07-08.md` 我评估了"什么研究对项目有用"，但**漏了用户明确要求的"基于 Auto-Research 的方法"**——这意味着研究设计本身应是 Karpathy/Deli 式迭代实验 loop（提出假设→跑→评估→保留/舍弃），不是一次性的对比研究。

**Auto-Research 方法 vs 普通研究的区别**（基于 `karpathy-loop-harness-2026-07-07.md` 验证的 Karpathy `program.md`）：
1. **evaluator 锁定**：评估器不可被研究对象修改（Karpathy `evaluate_bpb` 客观 metric，agent 只改 `train.py`）
2. **状态文件 append-only**：`results.tsv` 永不覆盖，新 verdict 只追加
3. **迭代探索**：多次 propose-evaluate-keep/discard，不是一次性实验
4. **停止条件 + budget cap**

因此本次每个项目的"研究"必须是能跑迭代 loop 的设计——而不是一次比较研究。这是前答的关键缺失。

## Q1: Policysim-v0.2 — 应急决策推演有效性

### Auto-Research 方法视角的新 design

**研究对象**：Policysim 蒙特卡洛推演输出（决策叙事报告）对真实应急决策的有效性
**evaluator 锁定**：真实事后调查报告 + n≥10 应急专家 paired Likert-5（金标冻结，非-LLM）
**迭代 loop**：
1. 选历史事件 E（古雷 2015 / 渤海溢油 / 天津港 / 苏州燃气等）
2. Policysim 跑推演 → 输出报告 R_E
3. 对比 R_E vs 真实事后调查报告 I_E → 量化覆盖度/盲点/可行性
4. n=10 专家 paired 评 R_E 与 I_E
5. **迭代**：若 Policysim 漏维度 → 改 prompt/schema/知识库 → 重跑同 E → 再评
6. 直到推演覆盖度 ≥ 阈值 或 stale_count ≥ 3
7. **跨事件验证**：第 N 事件的推演用第 1..N-1 事件学到的 schema 改进

### 帮助在哪（vs 前答更具体）
前答只说"验证产品核心价值"——本答具体到**迭代 schema 改进**：每次跑事件 → 专家反馈 → 改 `emergency-kb/schema` 与 `monte-carlo-architecture` → 重跑。研究的产出直接沉淀为 Policysim 的 schema v2/v3——**研究 = 产品迭代**，不是论文附产品。

### 价值大小
**高**——研究产出的 schema 改进直接进 `emergency-kb/` 和 `wiki/concepts/`。Policysim 团队会用这些改进（不是"看论文后参考"，而是"迭代本身就是产品开发"）。**这是真价值不是合理化**。

### paper 可行性
- E6/E7 NPS-style 应用研究 + 张辉 JSSR 匹配
- 题目候选："Iterative Schema Refinement for Emergency-Response Simulation: A Pre-Registered Case-Study Series on 5 Historical Incidents"
- honest P：JSSR/安全期刊 30-50%（halved 15-25%）；NPS-style thesis 60-80%（halved 30-40%）
- 前答一致，但 design 更扎实（迭代而非一次比较）

## Q2: cds4polymarket — Factor Ledger Calibration

### Auto-Research 方法视角的新 design（最有 Auto-Research 味道）

**研究对象**：factor-ledger 协议（前兆/抑制/分支/反证 4 类因子）对 Polymarket 真实结算的预测有效性
**evaluator 锁定**：Polymarket 真实结算（`settlement_outcome` 字段，factor-ledger 协议已有，外部非-LLM）
**迭代 loop（这就是 Karpathy 模式的直接落地）**：
1. 对每场 World Cup 2026 比赛 M_i，按 factor-ledger 协议生成 4 类因子 + 可观测代理信号
2. 等比赛结算 → 记 `settlement_outcome`
3. 算 Brier/Log Loss + per-类因子预测有效性
4. **迭代**：若某类因子预测力 < 阈值 → 改 factor-ledger schema（如加新因子类 / 改可观测代理定义）→ 重测下一批比赛
5. 直到因子有效性 ≥ 阈值 或 stale_count ≥ 3
6. **最终输出**：factor-ledger 协议 v2（已校准）+ Brier 量化 + 是否真有校准力的 verdict

### 帮助在哪（vs 前答更具体）
前答说"验证项目方法论核心"——本答具体到**迭代 factor-ledger schema 改进**：研究产出的 schema v2 直接回写到 `docs/concepts/factor-ledger-and-decision-sentinel.md`——**研究 = 协议演进**，不是论文附产品。**且 evaluator 是真实结算，完美匹配 Karpathy evaluator-lock 公理（A2）**——这是本 portfolio 唯一完美对齐 Auto-Research 方法的方向。

### 价值大小
**极高**——cds4polymarket 项目自陈 "factor ledger 是 S5 知识有效性的核心闭环"。研究产出 = 协议 v2 = 项目下一步方向。**且项目已有 World Cup Paper Track + MVP-A v0.2 runner + AB Test v1-v5 基础设施**（`research-for-dev-projects-2026-07-08.md` LV1 verified）。这不是从零开始。

### paper 可行性
- calibration workshop NeurIPS Eval / ICML Eval
- 题目候选："Factor Ledger Calibration: An Iterative Auto-Research Loop for Knowledge-Effectiveness Verification on Polymarket"
- honest P：**3 项目最高**——calibration workshop 30-45%（halved 15-25%）
- 完美 evaluator-lock + 真实 ground truth + 已有基础设施
- **关键阻塞**：项目冻结 28 天（`research-for-dev-projects-2026-07-08.md` LV2 verified），需先 resume

## Q3: Marginalia — 协议多平台有效性

### Auto-Research 方法视角的新 design

**研究对象**：Marginalia 协议（schema/rules.md）被不同 AI 助手执行的一致性 + 有效性
**evaluator 锁定**：`audit.py` 输出的断链率/孤儿页率/协议符合度（脚本化，非-LLM）
**迭代 loop**：
1. 在 ≥3 项目（Policysim/cds4polymarket/第 3 个外部）部署 Marginalia
2. 4 AI 平台（Claude/Cursor/Cline/Codex）× 同一组"摄入 + 维护"任务
3. audit.py 跑 → 量化断链率/孤儿页率/协议符合度
4. **迭代**：若某平台协议符合度 < 阈值 → 改 rules.md 让协议更明确 → 重测
5. 跨平台收敛或 stale_count ≥ 3

### 帮助在哪
前答说"验证开源工具实证有效性"——本答具体到**协议规则的迭代明确化**：研究产出的 rules.md v2 直接回写到 Marginalia repo。**但价值仍低-中**——开源工具有效性是 nice-to-have，协议简洁性 + 社区推广更重要。

### 价值大小
**低-中**——rules.md 当前仅 30 行，迭代改进上限有限。研究产出对项目决策影响小（开源工具采用不太看有效性研究）。

### paper 可行性
- SE workshop（AI4SE/SANER）
- honest P：20-35%（halved 10-18%）
- 工具评估类天花板低 + 大 N 要求（≥3 平台 × ≥3 项目）
- **同前答判定**：合理化成分较高，不优先

## Q1-3 对比表（最终版）

| 项目 | Auto-Research 完美对齐 | evaluator 锁定 | 迭代产出回写项目 | 价值 | paper P（halved） | verdict |
|---|---|---|---|---|---|---|
| **cds4polymarket** Factor Ledger | ✅✅ 完美（真实结算=locked evaluator） | ✅ settlement_outcome | ✅ factor-ledger schema v2 → docs/concepts/ | **极高** | 15-25% NeurIPS Eval | **强推 #1** |
| **Policysim-v0.2** 应急推演 | ✅ 较好（事后报告=anchor） | ✅ 真实事后调查 + n=10 专家 | ✅ emergency-kb schema v2 → wiki/concepts/ | **高** | 15-25% JSSR | **推 #2** |
| **Marginalia** 协议有效性 | ⚠ 部分（audit.py 脚本化） | ✅ audit.py 输出 | ⚠ rules.md v0.4（仅 30 行） | **低-中** | 10-18% SE workshop | 不优先 |

**关键新增洞察 vs 前答**：
1. **cds4polymarket 是唯一完美对齐 Auto-Research 方法**——真实结算 = Karpathy evaluator-lock 的天然等价物。这不是研究用到了 Auto-Research，是研究领域本身就是 Auto-Research loop。
2. **Policysim 与 cds4polymarket 共享 factor-ledger 同名概念**（前答 LV4 verified）——研究 cds4polymarket 的 factor-ledger schema v2 可**跨项目回写**到 Policysim `wiki/concepts/factor-ledger-and-decision-sentinel.md`，一份研究两个项目受益。
3. **3 个方向的迭代产出都直接回写项目 schema**——这正是 Auto-Research 方法的产物纪律，不是"论文写完就丢"。
4. **Marginalia 仍低 ROI**——rules.md 太短（30 行），迭代上限有限。

## Q4: 文档清理记录（已执行）

### 已清理（2026-07-08）

**保留 current（6 canonical docs）**：
- `meta-uncertainty-and-blindspot-2026-07-07.md`（元诊断，49KB）
- `optimization-plan-2026-07-07.md`（修正方案，21KB）
- `karpathy-loop-harness-2026-07-07.md`（外部 prior art，23KB）
- `paper-directions-vs-exemplar-bar-2026-07-08.md`（7-criterion bar 重评，18KB）
- `first-principles-redesign-feasibility-2026-07-08.md`（第一性原理，21KB）
- `research-for-dev-projects-2026-07-08.md`（3 项目研究 v1，26KB）

**新建**：
- `INDEX.md`（本目录导航：canonical 6 + reference 1 + archived 22）
- `research-for-dev-projects-v2-2026-07-08.md`（本文件，Auto-Research 方法深化版）

**归档至 `archive/`（22 stale docs）**：详见 `INDEX.md` §Archived。包含 4 次 confirmed 反转 verdict chain（verdict #1/#2/#3/#9/#10/per-paper）+ 中间产物（Direction A 系列、llm-blocker、orchestrated-assessment、toutiao 重叠、high-quality-paper-direction 重叠）。**不删除**，按 R7 cite-restoration 保留作 audit trail。

### 为什么这样清理

1. **22 份 stale verdict 形成的循环本身就是元诊断的证据**（`meta-uncertainty-and-blindspot-2026-07-07.md` 诊断的"4 confirmed 反转"），删除会抹除诊断自己 proof。改用 archive 保留 provenance 但标 superseded。
2. **6 份 canonical 互相引用形成闭环**：meta-diagnosis 提出 problem → optimization-plan 给修正 → karpathy 给外部 prior art → paper-directions 用 bar 重评 → first-principles 答能否 → research-for-dev 转 dev 项目实践。任何 future 工作从这 6 份进入即可。
3. **INDEX.md 让任何人 5 秒内知道当前态**——不需要读 25 份 stale。

## Recommendations

### 给用户的 4 问直接答案（最终版）

**Q1 Policysim-v0.2**：Auto-Research 迭代 loop——选 ≥5 真实历史应急事件， Policysim 推演 vs 真实事后调查报告 + n=10 专家 paired，迭代改 emergency-kb schema。**帮助=迭代产出回写项目 schema**；**价值高**；**paper JSSR 15-25% halved**。

**Q2 cds4polymarket**：Auto-Research 完美对齐——factor-ledger 协议对 World Cup 2026 真实结算作 Brier 校准，迭代改 factor-ledger schema。**帮助=演进项目核心协议**；**价值极高**；**paper 3 项目最高 NeurIPS Eval 15-25% halved**。**阻塞=项目冻结 28 天需先 resume**。

**Q3 Marginalia**：Auto-Research 部分——多平台 audit.py 量化协议符合度，迭代改 rules.md。**帮助=明确协议**；**价值低-中**；**paper SE workshop 10-18% halved**。**不优先**。

**Q4 文档清理**：已清理——6 canonical 保留，22 stale 归档 archive/，新建 INDEX.md 导航。不删除按 R7。

### 优先级（最终版）

**cds4polymarket Factor Ledger Calibration（Auto-Research loop）** > **Policysim 应急推演（迭代 schema 改进）** > **Marginalia 协议（低 ROI）**

cds4polymarket 是 portfolio 中唯一**研究领域本身 = Auto-Research loop**的方向——真实结算 = Karpathy evaluator-lock 的天然等价物。这个方向不是"用 Auto-Research 方法做研究"，是"研究对象就是 Auto-Research loop"。

### 接下来该做什么

1. **决定 cds4polymarket 是否 resume**（冻结 28 天，问张辉/刘奕）
2. resume → write `Factor Ledger Calibration` 1-page proposal，对齐已有 `cds4polymarket/docs/research/worldcup-paper-framework-2026-06-10.md` + World Cup Paper Track Phase -1/0 plan
3. 同步 commit `docs/investigations/{INDEX.md, archive/}` 让清理生效

### 不该做

4. **不要**追 Marginalia 作独立 paper——低 ROI
5. **不要**在 cds4polymarket resume 前烧 API
6. **不要**恢复 archive/ 里的 stale verdict（它们是 4 次反转的证据，不是当前态）

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) Policysim 研究 + 帮助 + 价值 + paper | Q1 段 Auto-Research 迭代 design + schema 回写 + 15-25% halved | ✅ |
| (2) cds4polymarket 研究 + 帮助 + 价值 + paper | Q2 段 Auto-Research 完美对齐 + 3 项目最高 15-25% halved | ✅ |
| (3) Marginalia 研究 + 帮助 + 价值 + paper | Q3 段 Auto-Research 部分 + 低-中价值 + 10-18% halved | ✅ |
| (4) 整理文档 + 合并/删除/归档 | 22 归档 archive/ + 6 保留 + INDEX.md + 本文件 | ✅ |
| (5) 第一性原理 + 不考虑现有研究 | Auto-Research 方法重新 frame 3 个设计 + 不依赖旧 portfolio 数据 | ✅ |
| (6) 不迎合 | Marginalia 标"不优先" + cds4polymarket 标"项目冻结阻塞" + 不同意三个都乐观 | ✅ |

### 最终自审计

confidence ~72%（vs 前答 70%）,因为:
- Q1-3 用 Auto-Research 方法视角深化（前答漏了这层）——cds4polymarket 完美对齐 Karpathy evaluator-lock 是新洞察
- Q4 文档清理已执行 file-move verified（不是计划）
- 仍受 base rate 50% 错约束——cds4polymarket + Policysim 有真实外部锚，cap 可降到 25-30%；Marginalia 仍 50%

**唯一跳出循环 = resume cds4polymarket + 跑 World Cup 真实结算**。

## 交叉引用

- 本报告：`docs/investigations/research-for-dev-projects-v2-2026-07-08.md`
- 前答（v1）：`docs/investigations/research-for-dev-projects-2026-07-08.md`（本次深化保留 v1）
- 索引：`docs/investigations/INDEX.md`
- 元诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`
- 7-criterion bar：`framework/knowledge/paper-exemplars-2026-07-08.md`
- Karpathy evaluator-lock：`docs/investigations/karpathy-loop-harness-2026-07-07.md`
- cds4polymarket factor-ledger 协议：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/concepts/factor-ledger-and-decision-sentinel.md:22,25,54,64,94`
- cds4polymarket World Cup Paper Track：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/research/worldcup-paper-framework-2026-06-10.md`
- Policysim 应急 KB：`/Users/tangzw119/Documents/GitHub/Policysim-v0.2/emergency-kb/` + `wiki/concepts/{disaster-simulation-platform,emergency-scenarios,monte-carlo-architecture}.md`
- Marginalia 协议：`/Users/tangzw119/Documents/GitHub/Marginalia/schema/rules.md`