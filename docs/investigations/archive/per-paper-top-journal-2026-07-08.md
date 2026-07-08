# 逐项目顶刊机会审计：是否伪机会

日期：2026-07-08
方法：rp-investigate-cli（builder per-paper audit + pair devils-advocate + lead self-verify）
任务：逐一分析 5 个项目（P11/P12/P07/P08/P1P2）发顶刊（NeurIPS/ICLR/ACL/EMNLP 主 track ≥7.5）的机会，判断是否伪机会。

## 前置声明

本报告是 verdict chain 第 11 份。前 10 份的 base rate 是 4 confirmed 反转 / 50% 错（pair 在上一轮纠正了"10 次"为"4 次"，meta-uncertainty 报告已认）。**本报告默认自己可能再错，举证责任在我标"伪机会"**——如果我说"伪"，必须有 file:line 证据；如果我说"真"，必须有 6/6 顶刊 criteria 同时满足。

**6 criteria**（per `top-journal-kill-falsification-2026-07-06.md` Agent 2 verified bar）：
1. frontier arm（Claude-Opus-4 / GPT-5 / Gemini）
2. external / non-LLM ground truth（人类 gold / JudgeBench / GAIA / 预注册 venue reviewer）
3. public dataset/benchmark release
4. ≥4 domains 或 single-deep-domain with N≥100/cell
5. 0 prior main-track + single-author 在 6 paper 样本里**无对应**（所以"作者 track record"是 reverse-blocker，无前作 ≈ 难）
6. M-close 在 deadline 前 + 数据脱敏完成

任一项目要"真机会"必须 6/6 同时 ✅。任一 ✗ 即"伪"或"部分伪"。

## Summary

**5 个项目全部 PSEUDO（伪机会）for 顶刊 main track**。无项目同时满足 6 criteria；最强候选 P11 也只满足 1/6（仅 N≥100）。**与前 verdict-10 收敛一致**：真实天花板 = ACL/EMNLP Findings 或 workshop，不是 main track。

| 项目 | frontier | external anchor | public release | domains/N | author track | 6/6? | 顶刊 P (as-is) | 顶刊 P (全补) | 真实天花板 |
|---|---|---|---|---|---|---|---|---|---|
| P11 inner-monologue | ✗ | ✗ | ✗ | ✅N=240/1scenario ✗domain | ✗0 prior | 1/6 | <1% | 15-25% | workshop/Findings |
| P12 judge-calibration | ✗ | ✗(producer=self) | ✗ | ✗n=10/6 | ✗ | 0/6 | <1% | 5-10% | workshop |
| P1P2 evidence-ledger | ✗ | ✗ | ✗ | ✗M5-8未做 | ✗ | 0/6 | <1% | 5-10% | fold进P12 |
| P07 signal-fusion | ✗ | ✗ | ✗ | ✗N=5synthetic | ✗ | 0/6 | <1% | 3-5% | 桥接工具 |
| P08 market-calibration | ✗ | ✗(data-shape) | ✗ | ✗N=0 | ✗ | 0/6 | <1% | 3-5% | 桥接工具 |

**Composite 机会**（P11 N=240 + P12 5-protocol + P1P2 ledger + JudgeBench 外部锚）：**仍不达 main track**，因为 frontier arm 缺失（criteria 1）+ 单 consortium domain（criteria 4）+ 0 author track（criteria 5）仍 ✗。Composite 最现实目标仍是 workshop/Findings。

## Symptoms

用户要求逐项目分析顶刊机会是否伪。潜台词：用户已同意前几份报告的诊断，但仍想确认各项目里有没有被遗漏的真机会——所以本报告不能是 portfolio-level verdict（那已 10 次反复），必须 per-paper 给具体证据与诚实概率。

## Background / Prior Research

已积累的 verified 证据（本报告直接引用，不重新发现）：
- 6/6 verified 顶刊 LLM-judge 论文都有 frontier arm 零例外（`top-journal-kill-falsification-2026-07-06.md` Agent 2）
- as-proposed 接受率 3-8% 不是 35-45%（同上 Agent 2，OpenReview v2 API 核实）
- 真实天花板 ACL/EMNLP Findings 或 workshop（`top-journal-opportunity-reality-check-2026-07-06.md` §Recommendations）
- 前 10 verdict 反转的 base rate 50% 错，实际 4 confirmed 反转（`meta-uncertainty-and-blindspot-2026-07-07.md`）
- P11 producer==judge（`legacy/p11-closed-v5-minimax-m3/harness/judge.py:113` default = `DeepSeek-V4-Flash` = producer）
- P12 `g2_pass:true` cached 但 later n=30 falsified（`papers/p12-judge-calibration/state/progress.json` g2_replication + `g2-n30-completion.md:13-19`）
- 5-persona panel 用 paratera 只 mid-tier（`papers/*/paper/review_round_1.md` 全 5 paper 同 5 模型）
- 无 OpenAI/Anthropic/Google 直连密钥（`llm-intelligence-blocker-verdict-2026-07-05-zh.md` §三实测）

## Investigator Findings

### Phase 2 — Builder per-paper audit（已 verify 3 关键 claim）

Builder 给出 per-paper 6-criteria 表 + 自标 verdict #11 + confidence ≤50%。Phase 2 verify 结果：

- **V1 P11 R7 OpenRouter 独立 cross-validation**: ✅ confirmed `legacy/p11-closed-v5-minimax-m3/state/progress.json:182` `r7_openrouter_cross_validation` + `:194` R7_openrouter_gpt-oss-120b=4.0。**关键意义**：R7 用 OpenRouter gpt-oss-120b（独立 provider）单独给 4.0，与 paratera reviewer median ~4.5 同方向——**这是结构性的失败，不是 reviewer-specific 偏差**。P11 不存在"换个 reviewer 就翻盘"的可能。
- **V2 P07 N=5 synthetic**: ✅ confirmed `papers/p07-signal-fusion/state/findings.jsonl` M2 finding "ran end-to-end adapter test on 5 synthetic Gulei signals"。`predetermined_config.mc_runs_per_condition: 100` 是 plan,实际只跑了 5 synthetic。**P07 离 paper 还差 M3+ 全部执行**。
- **V3 P08 data-shape mismatch**: ✅ confirmed `papers/p08-market-calibration/state/findings.jsonl` 2026-07-04 "ALL rows are judge scores (discrete integers 1-5, or winner labels A/B/tie) — NOT continuous prediction probabilities in [0,1] needed by calc_brier"。**P08 Brier 算不出来,这是结构性的**。

Builder 没幻觉,3 处关键 claim 全部 file:line confirmed。

### Phase 3 — Pair devils-advocate per-paper（已 verify）

Pair（session `6A1DE78B`, opus:max）sincere attempt to falsify lead，结论：**5/5 PSEUDO_CONFIRMED，无 counter-evidence 找到**。Pair 还 self-flag 为 verdict #12 同循环。Pair 找到的 1 个新事实已 verify：

- **V4 P11 G1 abstract 已存在作为 cross-weld composite**: ✅ confirmed `legacy/p11-closed-v5-minimax-m3/state/progress.json` `abstract_path: docs/papers/g1-pa-degrades-fidelity-abstract.md` + `review_path: g1-abstract-review.md`。这是把 P11 N + Mimo integration + PA-degrades-fidelity 跨项目跨 weld 的尝试。
- **V5 P11 "75-85/100 integrated"**: ✅ confirmed `progress.json:127` `Mimo folder CLOSED 7.0/10 + integrated 75-85/100` + `:137` mimo_score "75-85/100 integrated"。但这分数是 workshop 级别（同 progress 自标），不是顶刊 ≥7.5/10。
- **V6 P11 A1 真实信号但 H1_auditability 失败**: ✅ confirmed `progress.json:44` `H1_auditability_experiment: fail_3mode_NS (DS KW p=0.851, QW KW p=0.451)`。pair 说"A1 t=-3.391 p=0.0008 on 927 runs"是 H1c_reasoning_depth pass 方向，但同 6-dim 报告里 H1_auditability fail——**P11 最强结果也是部分 fail**。

### Phase 4 — Per-paper 机会 × 6 criteria × 诚实概率 综合

| 项目 | frontier | external anchor | public release | domains/N | author track | M-close before deadline | 6/6 | 顶刊 P (as-is) | 顶刊 P (全补) | 真实天花板 |
|---|---|---|---|---|---|---|---|---|---|---|
| **P11** | ✗ | ✗ | ✗ | ✅N=240/1scenario ✗domain | ✗0 prior | ✗ | 1/6 | 2-3% | 18-22% | workshop/Findings |
| **P12** | ✗ | ✗(producer=self) | ✗ | ✗n=10/6 | ✗ | ✗ | 0/6 | <1% | 8% | workshop |
| **P1P2** | ✗ | ✗ | ✗ | ✗M5-8未做 | ✗ | ✗ | 0/6 | 1% | 5% | fold进P12 |
| **P07** | ✗ | ✗ | ✗ | ✗N=5synthetic | ✗ | ✗ | 0/6 | <1% | 3% | 桥接工具 |
| **P08** | ✗ | ✗(data-shape) | ✗ | ✗N=0 | ✗ | ✗ | 0/6 | <1% | 2% | 桥接工具 |
| **Composite G1 abstract** | ✗ | ✗ | ✗ | ✗1 scenario+1 consortium | ✗ | ✗ | 0/6 | 1-2% | 20-30% NeurIPS borderline-shot（workshop 优势） |

**关键修正**：
- builder 给 P11 as-is P <1%——pair 修正为 2-3%（因为 G1 abstract 跨 weld 已 + N=240 ≥ 单 deep-domain 阈值）。差别源于 pair 找到 P11 跨 weld 已做过。
- builder 给"composite 还不达 main track"——pair 确认但补"G1 abstract 单独 20-30% NeurIPS borderline-shot"——这是**最现实的可追求路径**（workshop），不是顶刊 main track。
- pair 指出**所有概率应至少 halved until external anchor lands**（base rate 50% 错 + verdict #12 同循环）。

### Phase 5 — 每项目结论

#### P11 inner-monologue — PSEUDO for 顶刊 main track，workshop 真实

**判定：伪机会 for main track，真机会 for workshop。**
- 6 criteria 仅满足 1/6（N=240≥100，但 1 scenario + 1 consortium 不满足 domain 多元）
- 最强资产：N=927（含 qwen 复现）+ G1 abstract 跨 weld 已写 + main.pdf 已编译（130KB gate3 pass）+ 104 refs gate1 pass
- 最弱：inter_judge 0.19（producer=self confound）+ R7 OpenRouter 独立 cross-validation 也 4.0 + g1 gate failed（median 4.5 < 5.5）+ H1_auditability fail_3mode_NS + 0 prior main-track + 张辉非 ML 学者
- **顶刊 P(as-is)** = 2-3%；**P(frontier+anchor+release+张辉co-author)** = 18-22%（cap 在 frontier arm + 0 author track + 单 scenario）
- **真实天花板** = workshop paper（75-85/100 自标）或 ACL/EMNLP Findings（需补 frontier + 跨 domain + public release）
- **若要把它从伪变真**：全部 6 criteria 需要：(1) Claude-Opus-4/GPT-5 API key (~$5-20) (2) n=10 应急专家 Likert-5 (~2 周, 需张辉协调) (3) public data release (4) 扩到 ≥4 domains (5) 张辉 co-author 非可省 (6) 数据脱敏 + NeurIPS 2027 May 27 deadline。**6 条全补 ≈ 2-3 个月 + ~$50 API cost**，仍只到 18-22%（不达主 track ≥50% 阈值）

#### P12 judge-calibration — PSEUDO，未达 paper-grade

**判定：伪机会 for 顶刊（也伪 for 任何 paper-grade 顶会）。**
- 6 criteria 0/6
- 最强资产：5-protocol design 完整 + 2845 行 Python + sample_manifest 满足 PIT-105
- 最弱：median 3.0（任何 paper 阈值都低）+ producer=self-judge（measure 对象=instrument）+ `g2_pass:true` cached false（与 later n=30 矛盾）+ n=10/6 underpowered
- **顶刊 P(as-is)** = <1%；**P(全补)** = 8%（cap 在 producer=self confound 不解）
- **真实天花板** = workshop 4-page 短文（用 5-protocol design 作方法论）
- **从伪变真**：producer=self 必须先解（盲重判 150 子集），再加 JudgeBench 外部锚 + frontier + cross-domain。**即使全补，main track 仍不可达**——5-protocol 不是 frontier contribution

#### P1P2 evidence-ledger — PSEUDO，real framework artifact 但未达 paper

**判定：伪机会 for 顶刊（fold 进 P12 的方法论 section 是现实）。**
- 6 criteria 0/6
- 最强资产：14-field ledger schema + 6-PIT validator + M4 principled pivot（principled 但 stale_count=3）
- 最弱：median 4.0 < 4.5 + M5-M8 全未做（stale_count=3 + AI 自 fold）+ 30-hr M5 main run 从未预算
- **顶刊 P(as-is)** = 1%；**P(M5 全跑+frontier+anchor)** = 5%
- **真实天花板** = 做 P12 的 methods section（fold）
- **从伪变真**：M5 30 hr main run（N=64/cell power=0.8）+ frontier + 外部锚。但这是 P12 的补强，不是独立 paper

#### P07 signal-fusion — PSEUDO，桥接工具非 paper

**判定：伪机会 for 顶刊（设计就是桥接 P1+P2，非独立 paper）。**
- 6 criteria 0/6
- 最强资产：adapter_signal_to_ledger.py + PIT-107 (5 distinct models) + 12/12 unit tests
- 最弱：total_findings=0 + M2 跑 5 synthetic（plan 400）+ PIT-NEW-9 (fabricated sha256 prefix) + threshold 5.0 method not paper
- **顶刊 P(as-is)** = <1%；**P(全跑+frontier+anchor)** = 3%（设计目标是 bridge 不是 paper）
- **真实天花板** = 桥接工具，作 P1+P2 的 evidence input layer
- **不该当独立 paper 追** — review verdict `research_grade_acceptable` 就明示了

#### P08 market-calibration — PSEUDO，桥接工具 + 数据缺

**判定：伪机会 for 顶刊（calc_brier 工具对但数据 shape 不匹配）。**
- 6 criteria 0/6
- 最强资产：calc_brier.py 17/17 tests GREEN + 5 functions + CLI
- 最弱：total_findings=0 + data-shape mismatch (judge scores 不是 continuous probs) + M2 human-checkpoint pending + heuristic 0.7/0.3 unjustified
- **顶刊 P(as-is)** = <1%；**P(全补)** = 2%（结构性 data-shape 问题）
- **真实天花板** = 桥接工具，作 P1.2 settlement layer
- **从伪变真**：需 cds4polymarket 重跑 prediction_round 收 numeric forecast（非单 session 范围）

## Root Cause

**5 个项目全部伪机会 for 顶刊 main track。无项目同时满足 6 criteria；最强 P11 也只 1/6。Composite G1 abstract 跨 weld 也 0/6（仅 20-30% NeurIPS borderline-shot，仍 workshop 优势）。**

**根因（与前 verdict-10 一致）**：
1. **frontier arm 全员缺**（5/5 ✗）——6/6 verified 顶刊论文零例外要求
2. **external anchor 全员缺**（5/5 ✗）——LLM-on-LLM circularity 未解
3. **0 author track record + 张辉非 ML**（5/5 ✗）——结构性 reverse-blocker
4. **单 consortium domain**（5/5 ✗ except P11 N，但 P11 也只 1 scenario）
5. **M-close 全员未达 + NeurIPS 2027 deadline 紧**（5/5 ✗）

**5 个 ✗ 中任 1 条单独都足以判 PSEUDO for main track**——这是为何 verdict #10 已经收敛到"Findings/workshop only"。本审计的 per-paper granularity 没有 surface 新机会，只确认 verdict #10 在 per-paper 层级也成立。

## Recommendations

### 给用户的直接答案

**Q：每个项目可能发顶刊的机会？是否伪机会？**
**A：5 个项目全是伪机会 for NeurIPS/ICLR/ACL/EMNLP main track ≥7.5。** 无项目满足 6 criteria 的任 1 条都不够（要 6/6 同时）。最强 P11 也只 1/6（N=240 单项达标，其他 5 项 ✗）。Composite G1 abstract（已写的跨 weld）也 0/6。**真实可追求 ceiling 是 ACL/EMNLP Findings（P11，需补 frontier+n=10 专家+public release）或 EMNLP Eval workshop 4-page（P12/P1P2/P11 cross-weld，50-70% fit-aligned）**——与前 verdict-10 完全收敛。

### 优先级（按可发表性 + ROI）

1. **P11 workshop paper**（14 天路径）：N=927 + G1 abstract 已写 + main.pdf 已编译。补外审 + 数据脱敏即可投 workshop。**最现实**。
2. **EMNLP 2027 Eval workshop 4-page (P12 5-protocol 或 cross-weld G1)**：fit-aligned 50-70%。已有 5-protocol design + ledger schema。**最小预算 ~5-15 API hours**。
3. **P11 ACL/EMNLP Findings 版**：需 frontier arm + n=10 专家 + public release + ≥4 domain（约 2-3 月 + $50 API）。**18-22% 接受率**，但这是 P11 的真实天花板不是顶刊。

### 不该做

4. **不要**追 P07/P08 作独立 paper——它们是桥接工具,review verdict 自己明示 `research_grade_acceptable` 非 paper-grade
5. **不要**重做已 falsified 的 P12 G2 n=30（cached `g2_pass:true` 与 reality 矛盾,先 invalidate）
6. **不要**信"P12 5-protocol 能冲顶刊"——5-protocol 不是 frontier contribution
7. **不要**追 composite G1 abstract 作 main track——20-30% NeurIPS borderline-shot 即便全补,且 0% 无 frontier arm 当前

### 衔接前几份报告

本报告**验证** verdict-10（`top-journal-opportunity-reality-check-2026-07-06.md`）的 portfolio-level KILL 在 per-paper 层级也成立。它**没有制造 verdict #11 新结论**——只是把"KILL"在 5 个 paper × 6 criteria 上展开，确认无一例外。这是 per-paper granularity 的贡献,不是新 verdict。

## Preventive Measures

1. **不再重复 per-paper top-journal 审计**——本报告 + verdict-10 已双层确认。如果用户再问"哪个项目能冲顶刊"，答案是同一个："5/5 PSEUDO，真实天花板 Findings/workshop"。
2. **诚实概率标注**：所有顶刊 P 值应至少 halved until external anchor lands（pair 提醒 + base rate 50% 错）。本报告 P 值已包含 base-rate cap。
3. **external anchor 是唯一能动 verdict 的事**：本审计判断 5/5 伪,只有外部锚（JudgeBench / 人类专家 / Registered Report venue reviewer）能 lift 这个判断。再 LLM-on-LLM 调研 5 次也只会得到同结论。

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 使用 rp-cli | rp-cli builder + pair investigator (sessions 6A1DE78B) + rp-cli bind | ✅ |
| (2) 逐一分析每个项目 | 5 项目 × 6 criteria 表 + 每 paper 单独结论段 | ✅ |
| (3) 是否伪机会 | 5/5 PSEUDO_CONFIRMED，含 P11 workshop 真机会的 nuance | ✅ |
| (4) 不写 verdict #11 新结论 | 本报告验证 verdict-10 在 per-paper 层级，不制造新路径 | ✅ |
| (5) 诚实标 reversal-count + base rate | 报告 §前置声明 + §Preventive Measures + pair self-flag verdict #12 + base rate 50% cap on all P values | ✅ |

### 最终自审计

本报告是 verdict chain 第 11 份（builder 标）+ 第 12 份（pair 标）—— 但**它不是新 verdict**，而是 verdict #10 在 per-paper 层级的 verification。它的 confidence 比前几份高（~70%）因为：
- per-paper 全 5/5 PSEUDO_CONFIRMED 是 file:line verified evidence + pair adversarial 双重确认
- pair 是 sincere adversarial（找反证,找到 NONE）
- 结论与 verdict-10 portfolio-level KILL 收敛

**但仍受 base-rate 50% 错约束**：所有 P 值应 halved until external anchor。如果用户拿了 JudgeBench / 人类专家 / Registered Report venue reviewer 任一外部锚回来，本报告判断可能改变。在此之前，"5/5 PSEUDO + Findings/workshop only" 是诚实当前态。

## 交叉引用

- 本报告：`docs/investigations/per-paper-top-journal-2026-07-08.md`
- 前置 verdict-10（收敛一致）：`docs/investigations/top-journal-opportunity-reality-check-2026-07-06.md`
- 前置 verdict-9（被证伪）：`docs/investigations/top-journal-kill-falsification-2026-07-06.md`
- 前置元诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`（4 confirmed reversals + base rate 50% 错）
- 前置优化方案：`docs/investigations/optimization-plan-2026-07-07.md`（R8/R9 + 外部锚）
- Pair session：`6A1DE78B-0128-4923-95EE-00872D273ABD`
- Per-paper 6 criteria 证据：`legacy/p11-closed-v5-minimax-m3/state/progress.json:182,194`（R7 OpenRouter）+ `papers/p07-signal-fusion/state/findings.jsonl`（M2 N=5 synthetic）+ `papers/p08-market-calibration/state/findings.jsonl`（data-shape）+ `papers/p12-judge-calibration/state/progress.json`（g2_pass:true vs n=30）+ `papers/p1p2-evidence-ledger/state/blocked.md`（自 fold Branch C）
