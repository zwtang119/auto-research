# 跨项目 ROI：研究资产如何帮助 3 个开发项目 + 顶刊机会再评估

日期：2026-07-06
方法：rp-investigate-cli + 直接文件读取 3 个项目 + pair investigator (session 4AEFE752) 独立 ROI 评估
新输入：3 个兄弟项目（Policysim-v0.2 / cds4polymarket / policysim-research-Tsinghua）
上游报告：`docs/investigations/rethink-2026-07-06-zh.md`（auto-research 自身的顶刊 KILL verdict + G3 methods paper 为唯一活跃目标）

---

## 一、收敛结论（先给判断）

**用户问的是一个比"顶刊"更聪明的优化目标：研究资产能否反向赋能 3 个开发项目 + 顺便看是否产生新顶刊机会。这个角度是前几轮完全忽略的。**

**关键发现**：
1. **policysim-research-Tsinghua 是 4 项目中最成熟的论文资产**——mc-2026-05-05 实验完成，4 假设全部通过（d=1.19, IRR=1.56, p<1e-37），正在论文撰写阶段。
2. **auto-research 的 judge calibration / Brier / evidence ledger 资产可以作为 Tsinghua 论文的方法论验证层**——这是前几轮完全没看到的顶刊新方向（不是 auto-research 自己发顶刊，而是给 Tsinghua 论文加方法论杠杆）。
3. **跨项目协同反模式已经在发生**——cds4polymarket 的 `prompt_provenance_service.py` 已被 policysim-research-Tsinghua 借鉴（2026-06-10）；已有 `cds4polymarket/docs/investigations/evidence-chain-readability-retro-2026-06-10.md` 跨项目审计报告发现两项目共享"LLM prompt 不持久化"反模式。
4. **最高 ROI 转移 = G3 dual-ledger bridge 扩展到 policysim-research-Tsinghua**——把 evidence_ledger_entry × factor_ledger_entry 桥接扩展到 Tsinghua 的 ODD/protocol schema，作为 Tsinghua 论文的"证据可复现性"附录。

**收敛**: auto-research 的研究资产**不再追求自己发顶刊**（前几轮 KILL verdict 仍成立），而是**作为方法论验证层反哺 policysim-research-Tsinghua 论文**——这是新的顶刊杠杆路径。

---

## 二、3 项目当前状态摘要

### 1. Policysim-v0.2（CDS-EDK 应用开发）

| 维度 | 状态 |
|---|---|
| 仓库 | TypeScript/NestJS + TypeORM + Vue/React + pnpm monorepo |
| 版本 | 0.2.3 (2026-06-08) — Decision/Emergency 模块持久化、角色守卫 |
| 当前 | **术语统一**：Policysim → CDS-EDK、M3-α/β/γ → H1/H2/H3（2026-07-01）|
| 北极星 | "让复杂决策先在机器中运行，再在现实中执行"——AI-Native 决策控制面 |
| 是否研究院 | 否——应用开发，H0-H4 五层架构对齐课程五 |
| 痛点（推断） | 验证证据链（cds-collab-guard 已蒸馏 35 session 教训）、production reliability |

### 2. cds4polymarket（Kimi 世界杯 + 因子校准研究+应用）

| 维度 | 状态 |
|---|---|
| 仓库 | Python（calibration_lib.py、ab-test/、cds-runtime-kb/、apps/） |
| 关键资产 | **calibration_lib.py**（3 absolute + 3 pairwise + Drift + PASS/WARNING/STOP）、factor-ledger-and-decision-sentinel 概念、Kimi 300-agent 世界杯实验 |
| 已发现的反模式 | LLM prompt 不持久化（与 policysim-research-Tsinghua 同源缺陷，见 cross-project retro）|
| 痛点 | Vault 不存 prompt、Kimi 因子池动态校准方案设计中、Codability 300 项标注已 pivot 到 Reason Recoverability Gate |

### 3. policysim-research-Tsinghua（学术研究，最成熟）

| 维度 | 状态 |
|---|---|
| 定位 | **学术研究项目**（论文撰写中，不是软件开发） |
| 实验 | **mc-2026-05-05 全管线完成** |
| 4 假设 | **全部 PASS**：H1 d=1.19 IRR=1.56 p<1e-37 / H1a +0.61 p<1e-80 / H2 Shannon 6.46 vs 5.52 / H3 11.3x token / H4 3/3 models consistent |
| 3 层架构 | Generators (deepseek/gpt-oss/qwen) / GT Annotators (minimax+kimi κ=0.56) / Judges (Track A glm-5.1, Track B kimi+minimax) |
| 条件 | MAMR（多 Agent 多轮，实验组）vs SASR（单 Agent 单轮，基线） |
| 当前阶段 | **论文撰写** + Methodology Disclosure 已写 + Prompt Provenance 已修 |
| 已借鉴 | cds4polymarket 的 `prompt_provenance_service.py`（2026-06-10）|

---

## 三、auto-research 研究资产盘点（已确认状态）

| 资产 | 状态 | 价值 |
|---|---|---|
| **Direction A anchoring-bias** | **FOLDED**（review median 4.5 < 5.5 + 机制实验 β1 反方向证伪）| 作 G3 论文 Appendix A 否定结果 |
| **G2 calibration paradox** | **FALSIFIED at N=30**（前 N=6 cherry-picked）| 作方法论教训 |
| **G3 dual-ledger bridge** | **OUTLINE WRITTEN**（92.9% field coverage + 100% Brier replay）| 唯一活跃投稿目标，ACL/EMNLP Findings 25-35% |
| **P12 5-protocol judge calibration** | CLOSED as standalone，**但方法论仍可用** | leaked/blind/pairwise/neighborhood/abstention 5 协议 |
| **P1+P2 evidence ledger** | 14-field schema + 6 PIT invariants + power analysis | 方法学输出（即便作 standalone paper 已 fold）|
| **P8 Brier/log-loss calc** | 17/17 tests GREEN，但无 predicted_p 数据 | 工具可直接复用 |
| **P7 signal-to-ledger adapter** | PIT-NEW-9 fixed，audit chain 真实 | 14/14 tests GREEN |
| **Deli AutoResearch 协议** | framework-level | 已部分应用到 cds-collab-guard |

---

## 四、候选研究→项目转移（ROI 矩阵）

| # | 候选转移 | 源（auto-research）| 目标项目 | 价值 (1-10) | 代码改动 (1-10) | ROI | 集成路径 |
|---|---|---|---|---:|---:|---:|---|
| T1 | **P12 5-protocol judge calibration** | P12 | policysim-research-Tsinghua Judges（Track A/B）| **9** | 4 | **2.25** | 加进 score_track_b.py：blind/leaked/neighborhood 作为 Track B 的扩展协议；论文"Judge Reliability"小节 |
| T2 | **G3 dual-ledger 扩展桥** | G3 | policysim-research-Tsinghua ODD/protocol schema | **8** | 5 | **1.60** | 把 G3 crosswalk 扩展到 factor_ledger_entry × evidence_ledger_entry × Tsinghua protocol；论文"Reproducibility"附录 |
| T3 | **P1+P2 PIT invariants (PIT-201..208)** | P1+P2 | 全 3 项目（共享验证库）| 6 | 5 | 1.20 | 抽取为 framework/scripts/pit_validator.py，各项目 schema 适配 |
| T4 | **P8 Brier/log-loss calc** | P8 | cds4polymarket ab-test/ | 5 | 2 | **2.50** | 直接 drop-in：抄 `calc_brier.py` + 17 tests 进 cds4polymarket/calibration_lib.py |
| T5 | **PIT-NEW-9 audit-chain utility** | P7 | 全 3 项目（共享工具）| 4 | 2 | 2.00 | 抽取 sha256-prefix 工具为 framework/scripts/audit_chain.py |
| T6 | **P7 signal-to-ledger adapter** | P7 | cds4polymarket factor pool | 4 | 6 | 0.67 | 需要 cds4polymarket 有 signal source；目前无 |
| T7 | **P11 26-round review plateau 数据** | P11 | policysim-research-Tsinghua 论文 Limitations | 5 | 1 | **5.00** | 文字引用 P11 plateau 作为 reviewer-noise 证据 |
| T8 | **Deli AutoResearch 协议扩展** | framework | cds4polymarket（cds-collab-guard 已部分应用）| 6 | 3 | 2.00 | 把 Deli 协议的 L0/L1 心跳扩展到 cds4polymarket 的工作流 |

**最高 ROI = T7（P11 review plateau → Tsinghua 论文 Limitations，ROI=5.0）**——0 代码改动 + 引用证据。
**第二高 = T4（P8 Brier → cds4polymarket，ROI=2.5）**——17/17 tests 直接复用。
**第三高 = T1（P12 5-protocol → Tsinghua Judges，ROI=2.25）**——对论文方法论价值最大。

---

## 五、新顶刊方向：cross-project methodology validation paper

**Direction K（新，前几轮完全没看到）**：**"Multi-project methodology validation for LLM-agent decision evaluation"** — 把 auto-research 的 judge calibration + Brier + evidence ledger + PIT invariants 作为**shared methodology layer**，在 3 个独立项目（policysim-research-Tsinghua mc-2026-05-05 / cds4polymarket Kimi 世界杯 / CDS-EDK 部署）中验证其有效性。

**为什么这是新方向**：
1. 前 6 轮调研**完全没考虑** auto-research 资产作为姊妹项目的 methodology layer
2. policysim-research-Tsinghua mc-2026-05-05 的 4 假设全部通过是**最强的实证基底**（d=1.19）
3. 跨项目验证 = 真实多场景验证（解锁前几轮判定的"场景多样性"卡点）
4. 已有跨项目协同先例（prompt_provenance_service 借鉴）—— 不是空中楼阁

**诚实评估**：

| 维度 | Direction K 评估 |
|---|---|
| 新颖性 | shared methodology layer + cross-project validation = NeurIPS/ICLR Datasets & Benchmarks 风格 |
| 实证基底 | **强**——基于 Tsinghua 4 假设 d=1.19 + cds4polymarket Kimi 世界杯 + CDS-EDK 部署 |
| 场景多样性 | **3 独立项目**（解锁前几轮卡点）|
| 外部验证 | 部分满足——3 项目跨 domain，但同一团队（同前几轮的"内部跨域"风险）|
| frontier baseline | 仍是中端模型（与 LLM 智力判定一致：non-blocking）|
| 主 track 接受概率 | ~15-25%（NeurIPS D&B 或 ACL Findings）|
| 最现实天花板 | ACL Findings 7.0-7.5（与 G3 methods paper 同档）|
| 关键风险 | (a) 项目组认可；(b) 3 项目其实同一团队 = "internal cross-domain" 而非真外部；(c) 论文作者署名协调 |

**反向批判**：
1. **3 项目同属张辉团队 / 同一 git 工作区** = 内部跨域，前几轮已证伪 cds4worldcup 不能作外部验证；同样地，3 项目也不能算外部验证。
2. **Direction K = "G3 methods paper 的扩展版"**，前几轮已判定 G3 是 ACL/EMNLP Findings 7.0-7.5，不是主 track。
3. **Tsinghua 论文已有自己的撰写计划**，强行加 cross-project 方法论层可能 delay 投稿。

**证伪结论**：Direction K 是 **G3 methods paper 的自然扩展**，不构成新的主 track 路径。但它**显著提高 G3 methods paper 的实证厚度**——把 G3 从"双账本桥接方法论"升级为"多项目共享方法论层"，使 Findings 接受概率从 25-35% 提升到 **35-45%**。

---

## 六、给用户的建议（按优先级）

### 立即可做（高 ROI，不烧 token）

1. **T7（ROI=5.0）**：在 policysim-research-Tsinghua 论文 Limitations 引用 P11 的 26-round review plateau 作为"reviewer noise"证据——0 代码改动。
2. **T4（ROI=2.5）**：把 P8 的 `calc_brier.py` + 17 tests 复制到 cds4polymarket/calibration_lib.py——drop-in，~2 小时。
3. **T1（ROI=2.25）**：与 Tsinghua 论文作者（张辉团队）讨论在 score_track_b.py 加 P12 5-protocol（至少 blind/leaked）作为 Track B 扩展——这能直接强化论文的"Judge Reliability"节。

### 中期（需要协调）

4. **T2（ROI=1.6）**：G3 crosswalk 扩展到 Tsinghua protocol schema，作为论文 Reproducibility 附录——把 G3 methods paper 和 Tsinghua 论文形成协同。
5. **T3（ROI=1.2）**：抽取 PIT-201..208 为 framework/scripts/pit_validator.py 共享验证库——长期为 3 项目提供 invariant 检查。

### 顶刊策略

6. **不要试图让 auto-research 自己发顶刊主 track**（前几轮 KILL verdict 仍成立）。
7. **pivot 策略**：把 auto-research 的方法论资产**作为 policysim-research-Tsinghua 论文的方法论验证层**。Tsinghua 论文本身有 d=1.19 的强效应，加上 auto-research 的 5-protocol calibration + dual-ledger bridge + PIT invariants，把 Tsinghua 论文从"results paper with weak methodology"升级为"results paper with strong methodology"。
8. **Tsinghua 论文天花板**：单独发表 = SCI Q1（JSSR/Fire）；加 auto-research 方法论层 = **可能 ACL/EMNLP Findings 7.0-7.5**（25-35% → 35-45%）。仍非主 track ≥7.5。

### 不该做

9. **不要**为 Direction K 单独写新论文——它是 G3 + Tsinghua 协同的副产品，不是独立路径。
10. **不要**把 3 项目当成"外部验证"——它们同属张辉团队，前几轮已证伪 cds4worldcup 不能作外部验证，同理 3 项目也不能。
11. **不要**在 Tsinghua 论文投稿前 burn token 做 Direction K 实验——T1/T4/T7 已足够。

---

## 七、收敛判断（用户问的"意见收敛"）

| 问题 | 收敛判断 | 置信度 |
|---|---|---|
| auto-research 自己发顶刊主 track | **不能**（前几轮 KILL 仍成立）| 高 |
| auto-research 资产能帮助 3 个开发项目吗 | **能，T7/T4/T1 三个高 ROI 转移立即可做** | 高 |
| 是否产生新顶刊机会 | **Direction K** = G3 扩展 + Tsinghua 论文方法论杠杆，**不是新主 track 路径，但提高 G3 接受概率 25-35%→35-45%** | 中 |
| 最高 ROI 单一转移 | **T7**（P11 plateau → Tsinghua 论文 Limitations，ROI=5.0，0 代码改动）| 高 |
| 对 Tsinghua 论文的影响 | 从"results paper with weak methodology"升级为"results paper with strong methodology"，天花板从 SCI Q1 → ACL/EMNLP Findings | 中 |

---

## 八、Investigator Second Opinion（Pair Falsification）

<!-- pair session 4AEFE752 返回后追加 -->

---

## 九、诚实局限声明

1. **我没有 read Tsinghua 论文初稿**——`paper/10-draft/` 目录存在但我未读，无法判断方法论层是否真的缺。
2. **我没有 read cds4polymarket 的 Kimi 世界杯当前状态**——是否仍在进行、是否已发论文未知。
3. **我没有 read CDS-EDK 的 production metrics**——T8 的 ROI 评估基于推论。
4. **Pair second opinion 待返回**——ROI 数值可能被 pair 修正。
5. **3 项目同团队的"内部跨域"风险**未被定量评估——前几轮已证伪 cds4worldcup，同理推论。

---

## 十、交叉引用

- auto-research 顶刊 KILL verdict：`docs/investigations/rethink-2026-07-06-zh.md`
- Direction A fold chain（实证）：`state/progress.json:97-104`
- G3 methods paper outline（唯一活跃目标）：`docs/papers-closed-portfolio/g3-methods-paper-outline.md`
- 跨项目 prompt 持久化审计（已有先例）：`/Users/tangzw119/Documents/GitHub/cds4polymarket/docs/investigations/evidence-chain-readability-retro-2026-06-10.md`
- policysim-research-Tsinghua 状态：`/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua/wiki/annotations/current-state.md`
- mc-2026-05-05 实验数据：`/Users/tangzw119/Documents/GitHub/policysim-research-Tsinghua/experiments/mc-2026-05-05/`
- cds4polymarket calibration：`/Users/tangzw119/Documents/GitHub/cds4polymarket/calibration_lib.py`
- Policysim-v0.2 CDS one-pager：`/Users/tangzw119/Documents/GitHub/Policysim-v0.2/wiki/annotations/cds-one-pager-2026-06.md`

---

## Investigator Findings（独立 ROI 分析师追加，2026-07-06）

> **角色声明**：本节由独立 ROI 分析师（与前节 pair session 4AEFE752 无交集）独立产出。4 个 explore 子探针扫描 3 项目实盘状态文件后重做 ROI 矩阵。**前置声明：prior 矩阵（section 四）的 T7/T4/T1 排序我部分反驳；K-combo 应升到第一梯队。**

### 方法

- 4 个 explore 探针（read-only）：(1) Policysim-v0.2 Phase 5 阻塞；(2) cds4polymarket Kimi 世界杯状态；(3) Tsinghua 论文撰写状态；(4) 3 项目 schema 真实覆盖
- 探针全部返回实际 file:line 引用，**不是推论**
- ROI 评分：Value 1-10（10=解除 critical blocker）/Scope 1-10（10=多周重构）；ROI=Value/Scope
- 对 prior ROI 表中每行**逐条重评**，明确标"同/异/反"

### (A)+(B) 3 项目最尖锐痛点（基于探针实读）

#### Policysim-v0.2（CDS-EDK）

- **B1 阶段失锚** — 状态文件 `docs/analysis/cds-development-status.md:460-485` **无 Phase 5 heading**，roadmap 仅 4 item。`cds-strategic-control-loop.md:101` 明确指向状态源但状态源未声明 Phase 5 DoD。**Impact 9/10**：12 个 PR 全 docs/hooks-only，dev/backend 实改 1-2 处，无可对照 phase 闸门。
- **B2 KB 决策价值未实证（D5=2 = 0/36）** — 2026-07-04 clean mrp=6 rerun：3 场景 × 6 轮 × 2 arm = 36 评判中 D5=2 count = 0。LLM 拿到 KB 但**从未以"标源对照"方式引用 KB 中标准**。"信息更全≠决策更好"（v3/v16.1a/b 历史教训）未被 AB pilot 排除。**Impact 8/10**。
- **B3 P0 凭证泄露（active）** — `python -m http.server 8125` 暴露 `.env` 60h，4 个密钥必须轮换。状态 memo 2026-07-06 标 🔴。**Impact 10/10**，**auto-research 无 match**（correctly excluded）。

#### cds4polymarket（Kimi 世界杯）

- **K1 Kimi 预测缺每场概率向量（阻塞 Brier 计算）** — `worldcup-kimi/extracted_kimi_agent/wc2026_aggregation.json` 只存**队伍级投票份额**（Spain 23.82%）和**个体 confidence 标量**（0-100）；**无 home_win/draw/away_win 三分类概率向量**。`model_01_predictions.json:7,9` 直接证据：`"champion": "西班牙"` + `"confidence": 72`。**Impact 9/10**：Brier/log-loss 数学上无定义，Factor Ledger → settlement → 因子校准闭环阻塞在测量原语。
- **K2 calibration_lib.py 是 judge drift 检测，不是概率校准** — `calibration_lib.py:1-120` 显式标"AB Test Judge Stability"；Brier-ready settlement 基础设施完整（`settlement_record.schema.yaml:14-23`），但**无任何脚本对 Kimi 因子池跑概率校准**。`run_calibration.py` 只跑 judge calibration。**Impact 8/10**。
- **K3 零 2026 WC settlement 记录** — `analysis/match_level_results.csv`、`analysis/judge_adjudication_results.csv` 只有 header 无数据；`knowledge_update_log.md:19` wc2026-a-m01-mex-rsa = "pending | pending | Match not yet played"。**Impact 7/10**。

#### policysim-research-Tsinghua（论文）

- **T1 GT 校准失败（D1 ICC ≈ 0）** — `wiki/decisions/risks-and-issues.md:31` kappa=0.56 < 0.61 阈值；`experiments/mc-2026-05-05/analysis/paper-upgrade-evidence/judge_agreement.csv:1` **Track B D1 ICC = r=0.065**（近零相关）。**Impact 9/10**：顶刊审稿人会立即问"两 judge 在 D1 上都不一致，单点 score=3.72/5.0 含义？"。威胁 H1a 整篇 validity。
- **T2 期刊未定 + 7 节全"⏳ 待开始"** — `paper/00-README.md:24-30` 全 ⏳；Nature CS/PNAS/Science Advances 结构差异大。**Impact 8/10**。
- **T3 长度混杂 + 3 层 LLM-LLM-LLM 循环验证** — MAMR 29,536 tokens vs SASR 2,607（**11.3×**）；Track A GT matching = 2.9% (`draft-0316.md:176`)。**Impact 7/10**。

### (C) 重评 ROI 矩阵（vs prior section 四）

| # | 转移 | Value | Scope | **ROI** | vs prior 排序 | 修订理由（探针证据）|
|---|------|------:|------:|------:|:--:|---|
| **KC** | **P7+P8 → cds4polymarket Kimi WC**（K1+K2 合并为"概率向量提取 → Brier 计算"管线）| **10** | 4 | **2.50** | ↑↑↑ 升到第 1 | K1 揭示**根本没有 probability vector**——prior T4 假设的"drop-in Brier calc"前提不成立；prior 完全漏掉"测量原语缺失"这一环。P7 adapter 从 Kimi faction votes 提概率三分类，P8 算 Brier/log-loss。两步串行 ~2-3 天，**解锁整个 cds4polymarket 校准闭环** |
| **T7** | **P11 plateau → Tsinghua Limitations**（0 代码改动引用）| 5 | 1 | **5.00** | = 维持 | 探针确认无变化；纯 ROI 数学冠军 |
| **T1** | **P12 5-protocol → Tsinghua Judges（Track A/B）** | **9** | 4 | **2.25** | ↑↑ 升 | 探针发现 kappa=0.56 **< 0.61 阈值** + D1 ICC=0.065，**T1 不是 nice-to-have 而是投稿前 mandatory** |
| **K3** | **P1+P2 evidence ledger → cds4polymarket factor 池** | 7 | 5 | **1.40** | ↑ 升 | KC 解 K1+K2 后，K3 因子更新机制变得可落地 |
| **B1** | **Course 5 stage-def → Policysim Phase 5 DoD** | 7 | 6 | **1.17** | — 新增 | 探针发现 Phase 5 失锚；这是 prior 矩阵没分析的维度 |
| **T2** | **G3 crosswalk → Tsinghua protocol schema** | 5 | 6 | **0.83** | ↓↓ **降** | Schema 探针发现 G3 92.9% 是 cherry-picked，**真实 AR→CWCUP 覆盖 64.3%（9/14）**；T2 实际成本高于 prior 估值 |
| **B2** | **Direction A + P1+P2 → Policysim KB D5=2 trigger** | 6 | 7 | **0.86** | ↓ 降 | Direction A **已 FOLDED**（5-persona median 4.5 < 5.5，见 `state/progress.json:97-104`），作 primary 资产不合规；只剩 P1+P2 可用，scope 涨 |
| **B3** | 凭证轮换 | 10 | n/a | **excluded** | = | 探针确认 auto-research 无 match（correctly） |

**prior 排序反驳汇总**：
- prior T7 (5.0) 仍数学最高 ✓ — 但只是 1 行引用
- prior T4 (2.5) → **我升级为 KC (2.5)**，但**含义不同**：prior T4 假设 drop-in，实际 KC 是 2 步管线
- prior T1 (2.25) → 维持 ROI，但 **Value 从 9 升到 9 更坚定**（不是 nice-to-have 而是 mandatory）
- prior T2 (1.6) → **降到 0.83**（schema 真实覆盖比 G3 自报低）
- prior T3 (1.2) → 未重测，无显著变化
- prior T6 (0.67) → 探针发现 cds4polymarket 已有 signal source（Kimi faction votes），scope 下降 → ROI 升（**未在前表，单列 P7-only ROI ~1.5**）

### Schema 真相（探针 4 发现 vs prior G3 自报）

| 字段组 | AR (14-field) | CWCUP (12-field) | PSIM (4-field draft) |
|---|---|---|---|
| AR 独有字段 | 7 (freshness trio, authority, applicability, audit_trace, missing_prerequisites) | — | — |
| CWCUP 独有字段 | — | 4 (origin, match_id, direction, quantified_threshold) | — |
| 共享字段 | 9 (含 confidence 范围不同：AR[0,1] vs CWCUP[0,10]) | 9 | 1 |
| **真实覆盖** | **9/14 = 64.3% AR→CWCUP** | **9/12 = 75% CWCUP→AR** | **1/14 ≈ 7% PSIM↔AR** |

**G3 自报 92.9% 是 AR-centric（13/14 AR 字段在 CWCUP 有某种映射），含语义宽松匹配（如 confidence_before[0,1] ↔ confidence_0_10[0,10] 算"匹配"）**。enum 仅 1/5 重叠（`branch` only）。任何 T2 类 schema bridge 转移的 scope 应按 64.3% 而非 92.9% 估算。

### (D) 单一最高 ROI 转移

**纯 ROI 数学冠军：T7（P11 26-round plateau → Tsinghua 论文 Limitations，ROI=5.0）**
- 0 代码改动，引用 1 段数据作为"reviewer noise"证据
- 仍成立（探针无反证）

**最大价值转移：KC（P7+P8 → cds4polymarket Kimi WC，Value=10 ROI=2.50）**
- 真实解锁 cds4polymarket 整个因子校准闭环（K1 揭示测量原语缺失 + K2 揭示工具错配）
- 2-3 天实现，对 cds4polymarket 是 milestone 级 unblock

**我推荐优先级（综合 ROI × Value × feasibility）**：

1. **T7 先做（5 分钟，0 风险）** — ROI 5.0，立即可拿
2. **KC 立项（2-3 天，最大杠杆）** — unblock cds4polymarket 主线
3. **T1 与 Tsinghua 作者协商（1 周，论文投稿前必做）** — 不是 nice-to-have

### (E) 顶刊机会（Bonus 识别）

**prior section 五的 Direction K（cross-project methodology validation）我部分同意，但探针揭示新约束**：

**支持**：
- 探针确认 K-combo 真实解锁 cds4polymarket → 外部 calibration data 可注入 Tsinghua 论文
- T1 + KC 组合可把 Tsinghua 论文方法论从"results paper with weak methodology"升级为"results paper with cross-project calibration"

**新增约束（探针发现）**：
- T1 发现 D1 ICC=0.065 ≈ 零 → **Tsinghua 论文投稿前必须先做 P12 5-protocol calibration**（blind/leaked 至少 2 协议），否则任何顶刊主 track 都会被拒
- KC 解 K1+K2 后，**cds4polymarket Kimi WC 2026 实际 settlement 数据**将是 Tsinghua 论文最强的 cross-domain 验证基底（不是 3 项目内部跨域，而是 1 个商业应用 + 1 个学术实验 + 1 个 production 部署 = 真多场景）
- **TSINGHUA H1a 论文 = 真顶刊候选，条件 = T1 + KC + T7 都做**。否则天花板 = SCI Q1；做了 = ACL/EMNLP Findings 7.0-7.5

**修正 prior 的 Direction K 评估**：
- prior 评"3 项目同团队 = 内部跨域不构成外部验证" → **反驳**：Tsinghua 是学术项目（外部用户/审稿人），cds4polymarket 是商业应用（外部用户），CDS-EDK 是 production 部署（外部用户）；3 项目有真实独立外部受众
- prior 评"Direction K 是 G3 扩展，不构成新主 track" → **部分接受但下调悲观度**：若 KC + T1 都做，Direction K 实证厚度足以撑 ACL Findings 7.0-7.5（prior 估 25-35% 接受概率 → 修到 **30-40%**）

**新增顶刊候选（prior 完全未识别）**：
- **Tsinghua H1a paper = "MAMR for policy simulation" + P12 5-protocol calibration layer + cross-project K-combo external data** → 真实目标 Nature Computational Science / PNAS Nexus / ACL Findings
- **接受概率**：30-40%（prior 估 25-35%，上调是因为 K-combo 提供了 Tsinghua 论文缺的"external validation"环节）

### 反驳 prior 矩阵的关键反例

1. **prior T6 (P7 → cds4polymarket, ROI=0.67) 完全错估** — 探针发现 cds4polymarket 已有 signal source（Kimi faction votes），scope 应从 6 降到 3-4，ROI 应升到 ~1.5。prior 把 KC 的"前置步骤"误算成 ROI 0.67。
2. **prior T4 (P8 drop-in, ROI=2.5) 误估前提交** — P8 是 Brier calc 工具，但**没有 probability vector 可 calc**。prior 完全漏掉 K1 这个 measurement primitive gap。修正后 P8-only ROI = 1.5（单独），P7+P8 串行 ROI = 2.5（合并）。
3. **prior T8 (Deli 协议 → cds4polymarket, ROI=2.0) 未在探针中验证** — 风险标记，需独立验证 cds4polymarket 是否已部分采纳 Deli 心跳。
4. **prior 完全没分析 B1（Phase 5 失锚）** — 这是 Policysim 真实 blocker，但 prior 假设"Phase 5 是已知目标"。

### Honest Limitations（独立分析师诚实声明）

1. **T1 ROI 评估基于 Tsinghua 论文作者接受 P12 5-protocol 的假设**——若作者拒绝外部协议嵌入（特别是双盲协议），T1 ROI 降到 0.5。
2. **KC ROI 评估基于 P7 adapter 能从 Kimi faction votes 提概率三分类**——这需要 Kimi 投票机制建模（Plackett-Luce 或 Dirichlet），未在探针中验证可行性。**若 P7 adapter 需先做 Kimi vote model calibration，scope 从 4 涨到 6，ROI 降到 1.67**。
3. **Direction K 顶刊评估基于 3 项目都能在投稿前完成对应 milestone**——任一延期则降级为 G3 methods paper 单发。
4. **Schema 探针未读 PSIM `dev/backend/` 完整 schema** — 7% 覆盖是 `FactorLedgerDraft` 的局部覆盖，不排除 PSIM 已有更完整 schema 未被探针发现。
5. **prior section 八 Pair Second Opinion 未返回** — 独立分析师 ROI 可能与 pair 冲突；冲突时以实际 file:line 证据为准。

### 交叉引用（本节独立）

- Direction A FOLD 证据：`state/progress.json:97-104`
- G3 92.9% 自报：`docs/papers-closed-portfolio/g3-dual-ledger-crosswalk.md`（独立探针 cross-check 实测 64.3% AR→CWCUP）
- Kimi 概率向量缺失证据：`cds4polymarket/worldcup-kimi/extracted_kimi_agent/wc2026_aggregation.json` + `model_01_predictions.json:7,9`
- Tsinghua kappa + ICC 证据：`policysim-research-Tsinghua/wiki/decisions/risks-and-issues.md:31` + `experiments/mc-2026-05-05/analysis/paper-upgrade-evidence/judge_agreement.csv:1`
- Tsinghua 论文空 section 证据：`paper/00-README.md:24-30`
- Policysim Phase 5 失锚证据：`docs/analysis/cds-development-status.md:460-485`（无 Phase 5 heading）+ `cds-strategic-control-loop.md:101`
- Policysim D5=2=0/36 证据：`docs/analysis/cds-development-status.md` 2026-07-04 memo + `docs/investigations/2026-07-03-polymarket-ab-test-lessons-for-emergency-kb.md`
- 跨项目 prompt 协同先例：`cds4polymarket/docs/investigations/evidence-chain-readability-retro-2026-06-10.md`
