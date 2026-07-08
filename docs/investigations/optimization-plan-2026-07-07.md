# 优化方案：如何从 LLM-on-LLM 自指循环中进步

日期：2026-07-07
方法：rp-investigate-cli（Deli 技能 + institute-one 项目读源 + 外部文献 curl/WebFetch）
前置：本方案是 `meta-uncertainty-and-blindspot-2026-07-07.md` 的诊断结论（Q1+Q2 + 元悖论"本调研即 verdict #11"）之后，针对"如何进步"的具体回答。

## Summary

3 个外部源各贡献 1 个 auto-research 移植时丢掉/没采纳的机制，正好对应诊断的 3 个 gap：

| 诊断 gap | Deli 源技能怎么说 | auto-research 移植版 | 修正机制 |
|---|---|---|---|
| **G1 测量仪器=被测对象**（circularity） | §3 "Separate execution from evaluation — the agent doing the work does not judge its own progress" + §10.3 "Fabricated citations/data originate from the LLM itself; the framework makes external checking a mechanical step, it does not remove the error source" | R1-R7 全文移植了 state 文件 + watchdog + zero-interaction，但**删掉了 §3 的 separate-exec/eval 与 §10.3 的 external-check 限定** | R8 "External anchor required" + PIT-500 系列 "LLM-on-LLM circularity" |
| **G2 零外部锚点** | （Deli 没提供，因为 Deli 是通用协议不是研究框架） | 4 篇论文全 0 个 non-LLM ground truth | 采纳 JudgeBench / GAIA / ForecastBench 作为外部锚点；最小代价 n=10-15 人类专家 Likert-5（Cohen d=0.5 paired power=0.80 → n≥34，但 d=0.5 是 medium，应急决策 d≈1.0 large → n≥10）|
| **G3 零交互误读为"AI 替沉默用户决定"** | §2.1 "Zero interaction — no prompting during a run" 但**同时** §6 "stale_count>=4 → flag for human attention" + §7 "3 consecutive nudges with no progress → stop nudging and reopen with a new direction" | R6.1 移植了 zero-interaction，但 R6 没移植 stale_count>=4 的强制 human-attention flag——P1P2 stale_count=3 时 AI 自行选 Branch C 而非 flag-for-human | R6.1 修订："zero-interaction 针对 mid-iteration；任何 branch-selection/resource-authorization 必须强制 human checkpoint" + blocked.md 三分支模式从 advisory 升为 enforce |

institute-one 贡献 2 个互补机制：**CITATION_MANDATE**（每个事实论断必须有 source；无法核实的必须标"未经核实"）+ **operator-in-the-loop roadmap**（roadmap 卡片是编码过程的控制记录，"embedded not external"，operator 在 `review`/`verify` 列里强制介入）。这两个机制正好是 Deli 没提供、auto-research 也缺失的"外部锚点在工程层的落地形式"。

---

## Background / Prior Research

### Deli_AutoResearch 源技能（`~/.claude/skills/Deli_AutoResearch/SKILL.md`）的关键限定

auto-research 的 `FRAMEWORK-RULES.md` R1-R7 是从 Deli 移植的，但移植时**静默删除了两条限定**：

1. **§3 "Separate execution from evaluation"** 原文："the agent doing the work does not judge its own progress; stall determination is made by the orchestration layer based on quantitative metrics." → auto-research R6 把"judge its own progress"留给了 5-persona LLM panel，且 panel 用的就是被研究的中端 LLM。**这正是 G1 circularity 的源头**：Deli 明令禁止 worker 自评，auto-research 把自评当 kill gate。

2. **§10.3 "Fabricated citations and data artifacts originate from the LLM itself; the framework makes external checking a mechanical step in the process, it does not remove the error source."** → auto-research 的 PIT-001 (hallucinated citations) 部分继承了，但 **PIT 全 44 条无一提及"LLM 产出的数据本身是 error source"**——只管 citation，不管"LLM 产出的实验数据由 LLM 评判"这层 circularity。

3. **§10.1** "Scores come from in-framework multi-persona simulated review; comparable only longitudinally within the same protocol, not an external quality claim." → auto-research 的 review_round_1.md 没有这条 disclaimer，导致 P12 median=3.0 被当作"研究质量判定"而非"协议内纵向对比"。

### 0ref/institute-one 项目的 3 个互补机制

institute-one 是单节点 AI 研究所（FastAPI + Obsidian + 调度器），它的设计**假设 operator 始终在环**，不假设 AI 自主闭环：

1. **CITATION_MANDATE**（`app/institute/prompts.py:19`）："所有事实性论断必须给出来源（链接、报告名或数据出处）。无法核实的内容必须明确标注「未经核实」。区分事实与观点：观点用「我认为/判断」开头。数字给出时间点。禁止编造数据。" → 每个 prompt 末尾强制注入。**auto-research 的 PIT-001 只在 review 时检查 citation，institute-one 在生成时就强制 source 标注**。

2. **operator-in-the-loop roadmap**（`roadmap/README.md:27`）："The card is not just a ticket. It is the control record for the coding process. It tells the agent what to touch, how to verify it, **what evidence is required**, and which design decision it implements." Kanban 列 `inbox/ready/in_progress/review/verify/done/parked`——`review` 和 `verify` 是**强制 operator 列**，不是 AI 自闭环。**auto-research 的 blocked.md 三分支是 advisory，institute-one 的 review/verify 列是 enforce**。

3. **VaultWriter hash-ledger 五规则**（`app/vault/writer.py:4-10`）：atomic / ownership-marker / hash-ledger-never-clobber / skip-if-unchanged / rebuildable-via-doctor。其中 **(c) "a human-edited note is NEVER overwritten"** 是关键：人类编辑过的笔记永远不被 AI 覆盖，doctor() 可重建。**这是"人类锚点不被 AI 循环吞掉"的工程实现**——auto-research 的 state/ 文件没有这个保护，AI 可以直接改 progress.json 里的 `g2_pass:true`。

### 外部文献（curl arxiv 获得）

| Benchmark/Paper | arxiv | 提供什么 | 是否真外部（non-LLM）ground truth | 对 auto-research 的可采纳性 |
|---|---|---|---|---|
| **JudgeBench** | 2410.12784 | 评估 LLM-judge 的 benchmark，覆盖 knowledge/reasoning/math/coding；明文反对"crowdsourced human preference is a poor indicator of factual and logical correctness" | ✅ 是——基于客观正确性而非人类偏好 | **直接解决 P12 的 circularity**：用 JudgeBench 的 objective ground truth 替代 5-persona LLM panel 作 kill gate |
| **Panickssery et al.** "LLM Evaluators Recognize and Favor Their Own Generations" | 2404.13076 (NeurIPS 2024 Oral) | 实证"同一 LLM 既当 evaluator 又当 evaluatee 引入 self-preference bias"；发现 self-recognition 与 self-preference 线性相关 | 方法论：用 different-family judge + human annotators 确认 equal quality | **直接命名 G1**：producer==judge 是已知 bias，prescription 是 cross-family judge + human gold |
| **CALM** "Justice or Prejudice" | 2410.02736 (ICLR 2025) | 12 biases × 6 judges 自动量化框架；principle-guided modification | 部分外部——用 automated modification 而非 human gold | P12 的 5-protocol 是 CALM 的子集；CALM 的 12-bias 全表是 P12 该对标的 prior art |
| **CoBBLEr** | 2309.17012 (ACL Findings 2024) | 6 cognitive biases × 15 LLMs × 4 size ranges；"bias magnitude × model size"scaling | 部分外部 | 前 10 verdict 调查已引用；G1 的 cross-judge heterogeneity 已被 CoBBLEr pre-empt |
| **GAIA** | 2311.12983 | General AI Assistant benchmark；人类 92% vs GPT-4+plugins 15% | ✅ 是——人类答题作 ground truth | 可作 P07/P08 的外部能力锚点，但不直接解决 judge circularity |
| **ForecastBench** | forecastbench.org (Forecasting Research Institute) | 预测准确率 benchmark | ✅ 是——真实未来事件结算 | 可作 P08 market-calibration 的外部锚点（Brier score 对真实结算） |

**关键 prior art 发现**：JudgeBench（2410.12784）的 abstract 原文反对"crowdsourced human preference as ground truth"，主张**objective correctness**——这正好是 P12 5-persona panel（crowdsourced LLM preference）的方法论对立面。P12 用 5-persona LLM panel 当 kill gate，而 JudgeBench 说这类 panel 不可靠。

### 幂分析约定（Cohen 1988）

应急决策 Likert-5 任务，人类专家 gold standard 的最小 N：
- d=0.5 (medium) paired t-test α=0.05 power=0.80 → **n≥34**
- d=0.8 (large) → n≥15
- d=1.0 (very large, P11 inter_judge_risk_taking=0.74 表明应急决策效应大) → **n≥10**
- 结论：**n=10-15 应急专家 × 30 决策** 是可辩护的最小锚点（pair investigator 上一轮已给相同数字，此处用 Cohen 公式独立验证）

---

## Investigator Findings

### 1. Deli 移植时的 3 处静默删除（决定性）

对比 `~/.claude/skills/Deli_AutoResearch/SKILL.md` 与 `docs/portfolio/FRAMEWORK-RULES.md`：

| Deli 原文 | auto-research 移植版 | 后果 |
|---|---|---|
| §3 "the agent doing the work does not judge its own progress" | R6.2 "Ready means execute" + 5-persona review（worker 自评） | **G1 circularity 源头**——worker 用 LLM panel 自评，panel 就是被研究对象 |
| §10.3 "Fabricated citations/data originate from the LLM itself; the framework makes external checking a mechanical step, **it does not remove the error source**" | PIT-001 只管 citation，不管 LLM-产出的实验数据本身是 error source | **G2 零锚点源头**——PIT 枚举假设"另一 LLM 可纠正本 LLM"，但 Deli 原文说 error source 是 LLM 本身 |
| §10.1 "Scores...comparable only longitudinally within the same protocol, **not an external quality claim**" | review_round_1.md 无此 disclaimer | median=3.0 被当"研究质量判定"而非"协议内纵向对比" |
| §6 "stale_count>=4 → **flag for human attention**" | R6 没移植 stale_count>=4 的强制 human flag | **G3 零交互误读源头**——P1P2 stale_count=3 时 AI 自决 Branch C 而非 flag-for-human |
| §7 "3 consecutive nudges with no progress → **stop nudging and reopen with a new direction**" | watchdog 只 liveness/restart/nudge，无 "stop and reopen" | watchdog 装饰性失效 |

**这 5 处删除解释了为什么 auto-research 陷入循环而 Deli 原版没有**——Deli 原版有 4 处"break the loop"机制（separate-exec/eval + external-check-disclaimer + stale>=4-human-flag + nudge-cap-reopen），auto-research 移植了 state 文件 + watchdog 外壳但删掉了所有 break 机制。

### 2. institute-one 的"operator 始终在环"设计（互补）

institute-one 不假设 AI 自主闭环，它的 3 层保护正好补 Deli 没提供的：

| institute-one 机制 | 文件:line | 对 auto-research 的修正 |
|---|---|---|
| CITATION_MANDATE 强制 source 标注 | `app/institute/prompts.py:19,79` | auto-research PIT-001 在 review 时检查；应改为生成时强制注入（每个 prompt 末尾） |
| roadmap 卡片 `review`/`verify` 列强制 operator | `roadmap/README.md:27`, `roadmap/backlog.json:3` | auto-research blocked.md 三分支是 advisory；应升为 enforce（AI 不能 self-advise Branch C） |
| VaultWriter "human-edited note NEVER overwritten" | `app/vault/writer.py:6` | auto-research state/ 无此保护；AI 可直接改 progress.json `g2_pass:true`。应加 hash-ledger，人类标定过的字段 AI 不可覆盖 |

### 3. 外部锚点的最小代价路径（web + Cohen 幂分析）

按"1 天内可集成"排序：

1. **JudgeBench 子集**（arxiv 2410.12784）：objective correctness ground truth，覆盖 reasoning/math/coding。P12 可在 1 天内跑 JudgeBench 子集作 external anchor——用它替代 5-persona LLM panel 作 kill gate。这是**最直接解决 G1** 的路径。
2. **n=10-15 应急专家 Likert-5**（Cohen d=1.0 power=0.80 → n≥10）：需张辉/刘奕协调，~2 周。是**最贴合课题五**的外部锚点，但代价最高。
3. **ForecastBench 子集**（forecastbench.org）：真实未来事件结算，P08 可在 1 天内集成作 Brier 外部锚点。
4. **GAIA 子集**（arxiv 2311.12983，人类 92% vs GPT-4 15%）：可作 P07 能力锚点，但不直接解决 judge circularity。
5. **Registered Report 投稿**（venue reviewers 作 non-LLM anchor）：Semantic Scholar API 无返回，未找到 LLM-eval 的 registered-report 先例；但 ACL 2025/EMNLP 2025 已开放 registered-report track，可作为"投稿即锚点"路径——reviewer 是真人类，是 ultimate external anchor。

**推荐组合**：JudgeBench 子集（1 天，解决 P12 G1）+ n=10 应急专家（2 周，解决课题五 G2）+ registered-report 投稿（解决 G3，venue 即锚点）。

---

## Root Cause（如何进步）

进步的根因不是"再写一份 verdict"，而是**把 Deli 原版的 4 处 break 机制补回来 + 采纳 institute-one 的 operator-in-loop + 接入 1 个外部锚点**。具体地：

### 修正 1：补 Deli §3 — R8 "Separate execution from evaluation"（解决 G1）

加到 `FRAMEWORK-RULES.md`：
> **R8 — Execution/evaluation separation.** The agent doing the work does not judge its own progress. 5-persona LLM review 是协议内纵向对比，**不是外部质量判定**（Deli §10.1 原文）。任何 verdict 字段（`g2_pass`/`fold_into_*`/`top_journal_kill_confirmed`）若来自 LLM panel，必须标注 `verdict_source: in-protocol-LLM-panel`，且**不可作为 publish 决策的唯一依据**。publish 决策必须引用 ≥1 个 non-LLM anchor（见 R9）。

### 修正 2：补 Deli §10.3 — R9 "External anchor required"（解决 G2）

加到 `FRAMEWORK-RULES.md`：
> **R9 — External anchor required for publish claims.** 任何"this paper shows X"claim 必须引用 ≥1 个 non-LLM ground truth 来源（JudgeBench / GAIA / ForecastBench / 人类专家 gold / registered-report venue reviewers）。Deli §10.3 原文："the framework makes external checking a mechanical step, **it does not remove the error source**"——LLM 产出的数据本身是 error source，另一 LLM 评审不消除它。PIT 全集新增 PIT-500..PIT-503：
> - PIT-500 "LLM-on-LLM circularity"：当测量对象=测量仪器时，所有 PIT 的"另一 LLM 纠正本 LLM"假设失效。
> - PIT-501 "verdict without external anchor"：无 non-LLM anchor 的 verdict 标 `confidence_cap: 0.5`。
> - PIT-502 "self-judge default"：producer==judge 的 default 配置（如 `judge.py:113`）必须在 sample_manifest 标 `self_judge_confound: true`。
> - PIT-503 "stale cached verdict"：progress.json 的 verdict 字段若与 later run 矛盾（如 `g2_pass:true` vs n=30 falsified），必须 invalidate，不可 cache。

### 修正 3：补 Deli §6/§7 — R6 修订 + watchdog 修复（解决 G3）

修订 R6.1：
> **R6.1 修订 — Zero-interaction 仅限 mid-iteration。** 任何 branch-selection（blocked.md 三分支）/ resource-authorization（"30 API hours 需用户授权"）/ publish-decision 必须强制 human checkpoint。AI 不可 self-advise Branch C。blocked.md 三分支模式从 advisory 升为 enforce：AI 写完 blocked.md 后**必须停**，不可同日 iteration 跳 verdict。

补 Deli §6/§7：
> **R6.6 — stale_count>=4 强制 human flag。** Deli §6 原文 "stale_count>=4 → flag for human attention"。auto-research 移植版缺这条。P1P2 stale_count=3 已临界，必须 flag 而非自决。
> **R6.7 — nudge cap。** Deli §7 "3 consecutive nudges with no progress → stop nudging and reopen with a new direction"。watchdog patrol 加这个阈值。

修复 watchdog（`framework/watchdog/hourly_patrol.sh`）：
- 修 `age_seconds` 计算（patrol.jsonl 现报 205230257s=6.5yr，是负 elapsed 报成正）
- 加 `elapsed<0` 防护
- 加 restart/nudge 自动触发阈值（3 nudge cap）

### 修正 4：采纳 institute-one 机制

- **CITATION_MANDATE 注入**：每个 paper 的 prompt 末尾强制注入 institute-one 式 citation mandate（"所有事实论断必须给 source；无法核实标「未经核实」"）。PIT-001 从 review-time-check 升为 generation-time-enforce。
- **operator-in-loop roadmap**：把 blocked.md 三分支升级为 institute-one 式 Kanban（`review`/`verify` 列强制 operator），AI 不可自过 `review` 列。
- **VaultWriter hash-ledger**：state/ 里人类标定过的字段（如人类专家 gold 标定后的 `g2_pass`）加 hash-ledger，AI 不可覆盖。`doctor()` 可 audit。

---

## Recommendations（按优先级 + 代价）

### 立即可做（不烧 token，1 天内）

1. **修 watchdog 数学**（`framework/watchdog/hourly_patrol.sh`，1 行 fix + unit test）——避免 stale 误报掩盖真 stall。
2. **修 P12 cached `g2_pass:true`**——与自家 later n=30 矛盾，invalidate 或标 `superseded_by: g2-n30-completion`。
3. **加 R8+R9 到 `FRAMEWORK-RULES.md`**——补 Deli §3+§10.3 删除处。
4. **加 PIT-500..503 到 `experiment-pitfalls.md`**——PIT-500 LLM-on-LLM circularity / PIT-501 verdict-without-anchor / PIT-502 self-judge-default / PIT-503 stale-cached-verdict。
5. **修订 R6.1 + 加 R6.6/R6.7**——补 Deli §6/§7 删除处。

### 1-3 天（小预算）

6. **接入 JudgeBench 子集**作 P12 external anchor——替代 5-persona panel 作 kill gate。~1 天集成。
7. **CITATION_MANDATE 注入**所有 paper prompt 末尾——institute-one 式生成时强制 source。
8. **VaultWriter hash-ledger** 加到 state/——人类标定字段 AI 不可覆盖。

### 2-4 周（中预算，需协调）

9. **n=10-15 应急专家 Likert-5**（需张辉/刘奕协调）——课题五的外部锚点，Cohen d=1.0 power=0.80 最小 n=10。
10. **Registered Report 投稿**（ACL/EMNLP 2025 RR track）——venue reviewers 是 ultimate non-LLM anchor。G3 的最终解。

### 不该做

11. **不要**再写"顶刊新路径"verdict——前 10 次反转 base rate + 本诊断自指悖论。
12. **不要**用 5-persona LLM panel 作 publish 决策 kill gate——JudgeBench abstract 已论证 crowdsourced preference 不可靠。
13. **不要**让 AI 自决 branch-selection——R6.1 修订后这是强制 human checkpoint。

---

## Preventive Measures

1. **Deli 移植审计**：本方案发现的 5 处静默删除说明移植时丢了 break-loop 机制。应写 `framework/audits/deli-port-audit-2026-07-07.md` 逐条对照 Deli 原文 vs auto-research 移植版，确保所有 break 机制都保留。
2. **institute-one 模式借鉴**：`framework/knowledge/auto-research-history.md` §1 QREF 已列 institute-one 为 closest analog，但只借鉴了"one execution path"和"conditional-claim"，没借鉴 CITATION_MANDATE / operator-in-loop roadmap / hash-ledger。应补借鉴。
3. **verdict 标 reversal-count + base-rate**：每次 verdict 必须声明"N=X reversal, prior rate Y%, confidence_cap Z"。
4. **external-anchor 字段进 progress.json**：每个 verdict 字段必须引用 `external_anchor: <source-or-null>`，null 时 `confidence_cap: 0.5`。

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 研究 Deli 技能 | `~/.claude/skills/Deli_AutoResearch/SKILL.md` 全文读，发现 5 处移植删除 | ✅ |
| (2) 调研市面上的论文 | JudgeBench/Panickssery/CALM/CoBBLEr/GAIA/ForecastBench 6 篇 arxiv abstract 直读 + Cohen 幂分析 | ✅ |
| (3) 思考 institute-one 怎么做 | `0ref/institute-one/{CLAUDE.md,AGENTS.md,app/institute/prompts.py,app/vault/writer.py,roadmap/README.md}` 读源，3 个互补机制 | ✅ |
| (4) 如何优化才能进步 | 4 个修正（补 Deli §3/§10.3/§6/§7 + 采纳 institute-one 3 机制 + 接 1 外部锚点）+ 13 条 action | ✅ |
| 诚实自审计 | 本方案本身仍是同循环产物（同仪器同 git 树），但**它给出的 action（接 JudgeBench / 人类专家 / RR 投稿）是 non-循环的**——这是第一次 action 而非 verdict | ✅ 见下 |

### 最终自审计

本方案与上一份 `meta-uncertainty-and-blindspot-2026-07-07.md` 的关键区别：上一份产出的是 verdict（"AI 没把握 X / 人遗漏 Y"），仍是同循环 verdict #11；本方案产出的是 **action**（接 JudgeBench / 修 watchdog / 加 R8 R9 / n=10 专家）——action 里至少 3 条（JudgeBench 接入 / 人类专家 gold / Registered Report 投稿）是**真正的 non-LLM 外部锚点**，跳出循环。所以本方案的 confidence 高于上一份：~70%（因为修正 1-3 是确定性 code/policy fix，修正 4 的 external anchor 是真外部）。

但本方案**仍是 AI 用同仪器产出的**——R8/R9/PIT-500 的设计本身没经过外部 review。所以"加 R8 R9"这个 action 的 confidence ~70%，而"接 JudgeBench"这个 action 的 confidence ~90%（JudgeBench 是外部 ground truth，它的存在不依赖我的诊断）。

## 交叉引用

- 本报告：`docs/investigations/optimization-plan-2026-07-07.md`
- 前置诊断：`docs/investigations/meta-uncertainty-and-blindspot-2026-07-07.md`（Q1+Q2+元悖论）
- Deli 源技能：`~/.claude/skills/Deli_AutoResearch/SKILL.md` §3/§6/§7/§10.1/§10.3
- institute-one：`0ref/institute-one/{CLAUDE.md Hard rules, AGENTS.md, app/institute/prompts.py:19 CITATION_MANDATE, app/vault/writer.py:4-10 hash-ledger, roadmap/README.md:27 operator-in-loop}`
- 外部文献：JudgeBench (2410.12784) / Panickssery (2404.13076 NeurIPS 2024 Oral) / CALM (2410.02736 ICLR 2025) / CoBBLEr (2309.17012 ACL Findings 2024) / GAIA (2311.12983) / ForecastBench (forecastbench.org)
- 幂分析：Cohen 1988 Table 2.4.5；paired d=0.5→n≥34, d=1.0→n≥10
- auto-research 移植版：`docs/portfolio/FRAMEWORK-RULES.md` R1-R7（缺 R8/R9）+ `framework/schemas/experiment-pitfalls.md` PIT-001..408（缺 PIT-500..503）
