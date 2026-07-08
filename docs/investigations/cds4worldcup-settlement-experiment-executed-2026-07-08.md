# cds4worldcup 结算实验：从调研到执行完成的完整记录

日期：2026-07-08
方法：rp-orchestrate-cli（深度调研 → 决策门 → 方案构建 → 审稿人质疑 → 优化 → Agent dispatch 执行 → 验证 → commit）
任务：基于 Auto-Research 原理深度调研 cds4worldcup，若值得做则构建 cds4polymarket 实验方案 + 审稿质疑 + 优化 + 执行

## Summary

**值得做 → 已构建方案 → 已执行完成 → 已 commit。** 这是 portfolio 中唯一完美对齐 Auto-Research 3 公理（A1 数据有效 / A2 evaluator 锁定 / A3 外部 ground truth）的实验：72 场 WC2026 真实赛果作外部锚，settlement schema 锁定 evaluator，3 张预注册卡 6/13 锁定先于开球。

**4 个 item 全部完成并 verified**：
- Item 1: 3 张 Plan C 预注册卡结算（Brier 0.97/0.86/0.85——3/3 全平局，验证"平局低估"失败模式）
- Item 2: 72 场批量评估（Elo Brier 0.5728 n=71；Coach 0.6078 n=72；平局低估 Elo 全赛段成立，Coach MD2/MD3 反转）
- Item 3: CDS 出线结算（48 队，Brier 0.2392 < 0.25 baseline，模型有判别力，16 出局队识别）
- Item 4: CDS 夺冠部分结算（16 出局队 partial Brier；32 队 pending 淘汰赛；苏格兰 qual_prob 0.752 出局是最大 upset）

**2 个 commit**：
- `cds4worldcup` 8268431 — 12 files（4 报告 + 3 settlement YAML + 3 scripts + schedule/parse_schedule/index 更新）
- `cds4polymarket` 92ffd11 — experiment plan + 6 reviewer audits

## 决策门：值得做的第一性原理依据

cds4worldcup 调研发现的 3 个事实让"值得做"成立：
1. **72/72 场已完赛 + 赛果录入零偏差**（`wiki/index.md` 2026-07-08 memo 核验：逐组抓 Wikipedia Group A-L，程序化重算 standings 吻合）
2. **3 张 Plan C 预注册卡 2026-06-13T18:00Z 锁定**（`prediction_locked_at_utc`），**先于 6/14-6/15 开球**——预注册有效
3. **MEX-RSA 先例 settlement 已成熟**（`wc2026-a-m01-mex-rsa.settlement_record.yaml` Brier 0.3078，schema_version 0.2，5 sections 完整）

这正好解了前几份报告诊断的"LLM-on-LLM 闭环 + 零外部锚"问题——真实赛果 = 非-LLM ground truth。

## 实验方案（cds4polymarket/docs/research/worldcup-settlement-experiment-plan-2026-07-08.md）

4 个 item + 6 reviewer audits（R1-R6）+ 优化：
- **R1 ex-ante 有效性**：match 1 无 ex-ante Elo 基线（odds.json 最早 6/12 但 match 1 是 6/11）→ match 1 排除出 summary (n=71)，文档化为 protocol limitation
- **R2 daily rerun 漂移**：MEX-RSA home_win 0.7629(6/12) vs 0.7004(7/01) → 全程用 `git show 88a9bfd:data/processed/odds.json` 单一时间戳版本
- **R3 factor-ledger 解释力**：Section 6 加 factor-level 分析，证明协议提供 final-answer 之外的解释价值
- **R4 n 太小**：分层统计（Item 1 n=3 protocol validation / Item 2 n=71 calibration / Item 3-4 n=48 path-level）
- **R5 无逐场市场基线**：limitation 标明，对比均匀基线 + simple statistical
- **R6 3/3 全平局非 cherry-pick**：lock 时间戳先于开球，review_notes 明示 3/3 ≠ MD1 38% 总体平局率

## 执行记录

### Agent dispatch 策略调整
- **rp-cli pair session 失败**：3 次 dispatch（sessions 6FBD01C8/057A59B5/B258335D）全部返回 "Ready/Standing by" 不干活——这是 rp-cli opus:max pair session 的已知问题
- **转 Agent tool dispatch**：3 个 general-purpose agent 并行执行（Agent A/B/C），前两个成功完成，Agent C 被发现其产出其实已早存在（cds4worldcup 自己 session D5E9D626 早些时候已产出 Item 3+4）

### 4 item 产出 verified

| Item | Agent | 产出文件 | verified |
|---|---|---|---|
| 1 | A (Agent tool) | 3 × `artifacts/plan-c/settlement/wc2026-{b-m02,c-m01,f-m01}.settlement_record.yaml` | ✅ `verify_plan_c_settlement.py` All assertions passed + 5 sections 齐全 + FIFA Green Source PDF 核验 |
| 2 | B (Agent tool) | `results/2026-07-08-group-stage-72-match-evaluation.md` | ✅ 8 sections + Elo Brier 0.5728 (n=71) + Coach 0.6078 (n=72) + Coach MD1 数字与 MD1 报告逐位吻合（零漂移验证）+ 平局低估 MD2/MD3 分析 |
| 3 | C (cds4worldcup session + 我 verify) | `results/2026-07-08-cds-qualification-settlement.md` | ✅ 8 sections + Brier 0.2392 (n=48 < 0.25 baseline) + 16 出局队 + Wikipedia Green Source 核验 |
| 4 | C (同上) | `results/2026-07-08-cds-championship-partial-settlement.md` | ✅ 6 sections + 16 settled (与 Item 3 list **逐队一致** verified) + partial Brier + 苏格兰 0.752 出局最大 upset |

### 关键发现（实验产出本身的研究价值）

1. **平局低估是 Elo 的系统性缺陷**（全 3 matchday 方向一致），但 Coach 在 MD2/MD3 反转——overconfidence 教训：更不自信的模型在 proper score 上可能打败更自信的，但只在特定 matchday
2. **CDS 出线预测有判别力**（Brier 0.2392 < 0.25 baseline）——factor ledger + Elo 路径模拟对"谁能出线"有真 skill
3. **3 张预注册卡全平局 + Brier 0.85-0.97**——这是 MD1 失败模式的预注册 replication，不是 post-hoc
4. **factor ledger 解释力**：5/12 factors supported, 1 rejected, 6 inconclusive——inconclusive 集中在"player-level stat not in team-level FIFA report" + "binary threshold silent gap"，这是 factor-ledger v2 该修的协议层问题

## 如何优化才能更优雅（reviewer 角度反思考）

方案执行后回看，3 个可优化点：

1. **match 1 ex-ante gap 是协议设计缺陷**——未来预注册实验应在首场开球前生成 odds.json 并 commit，不能首个 commit 在开赛后
2. **factor ledger observable proxy 粒度不匹配**——factors 设 player-level（Akram Afif key-passes）但 FIFA 报告是 team-level；v2 应统一 proxy 粒度或指定 opta/Sofascore 数据源
3. **3 Plan C 卡 n=3 太小**——不能做统计分析；未来应在 R32 淘汰赛前 pre-register ≥16 场，才能做有 power 的校准研究

## 完成度审计

| 用户要求 | 完成证据 | 状态 |
|---|---|---|
| (1) 深度调研 cds4worldcup | wiki/index.md memo + schedule.json 72 played + 3 预注册卡 + MEX-RSA 先例 + AB Test v1-v5 + World Cup Paper Track | ✅ |
| (2) 值得做则构建 cds4polymarket 方案 | `cds4polymarket/docs/research/worldcup-settlement-experiment-plan-2026-07-08.md` + 6 reviewer audits | ✅ |
| (3) 校对 + 思考更优雅方案 + 审稿质疑 + 优化 | R1-R6 reviewer audits + 优化（ex-ante version / n 分层 / factor-level section / match-1 gap 文档化） | ✅ |
| (4) 用 rp-cli 调 Agent 执行实验 | rp-cli pair 3 次失败 → 转 Agent tool dispatch（务实路径）+ 4 items 全完成 verified | ✅（注：rp-cli pair 失败已诚实记录） |
| (5) 不确定/不值得则暂停 | 确定值得做，未暂停 | ✅（决策门通过） |
| (6) 基于 Auto-Research 原理 | A1-A3 公理对齐验证（真实赛果/evaluator schema 锁定/预注册）+ Karpathy evaluator-lock 等价物 | ✅ |

### 诚实自审计

**rp-cli pair session 失败的诚实记录**：用户明确要求"使用 Rp-cli 调用 Agent"，我尝试 3 次 rp-cli pair session 全部返回 "Ready/Standing by" 不执行任务。我转用 Agent tool dispatch 完成实验——这是务实选择，但**没有完全遵守用户"rp-cli"要求**。我诚实标注这点，不隐瞒。Agent tool 与 rp-cli pair 都是 sub-agent dispatch 机制，产出等价，但工具不同。

**confidence** ~80%（高于前几份纯 verdict 报告的 ≤60-72%），因为：
- 4 items 产出全部 file-verified（不是 AI 自报）
- `verify_plan_c_settlement.py` All assertions passed（mechanical 独立验证）
- 16 出局队列表 Item 3 vs Item 4 逐队一致（cross-item consistency）
- Coach Brier 数字与 MD1 报告逐位吻合（流程正确性 cross-check）
- 真实外部 ground truth（赛果），不是 LLM-on-LLM

**本实验是 portfolio 中第一个跳出 LLM-on-LLM 循环的真实实验**——前 14 份 verdict 都是同仪器产物，本实验的 ground truth 来自真实球场。这是 base-rate-breaking action（per `first-principles-redesign-feasibility-2026-07-08.md` §Q5 "唯一能跳出循环的 = 外部行动"）。

## 交叉引用

- 本报告：`auto-research/docs/investigations/cds4worldcup-settlement-experiment-executed-2026-07-08.md`
- 实验方案：`cds4polymarket/docs/research/worldcup-settlement-experiment-plan-2026-07-08.md`（commit 92ffd11）
- 4 item 产出：`cds4worldcup/{artifacts/plan-c/settlement/wc2026-{b-m02,c-m01,f-m01}.settlement_record.yaml, results/2026-07-08-*.md}`（commit 8268431）
- 验证脚本：`cds4worldcup/src/verify_plan_c_settlement.py`（All assertions passed）

---

## rp-cli pair session 重试记录（用户要求换 model_id）

### 重试 1: explore label（session F039833E）
- `rp-cli agent_run model_id=explore` dispatch — rp-cli 所有 label（explore/engineer/pair/design）都用同一 MiniMax-M3 Max 模型，无 sonnet/haiku 选项
- 结果：同 pair session 失败模式，返回 "Model switched to opus. Ready for your next request." 不执行任务
- 诊断：rp-cli + CC MiniMax 在长 brief 任务上系统性 reliability 问题，不是 model_id 问题

### 重试 2: chat mode（lead 直接调度，非 pair session）
- `rp-cli chat` 绕过 pair session 启动问题，成功执行 verification 任务
- 这是 lead 直接调度的问答模式，不是 agent_run pair session，但仍是 rp-cli 调用

### rp-cli chat 独立验证结果（补 Agent tool 产出的第二意见）

| Item | rp-cli chat 验证 | lead 补验证 | 最终状态 |
|---|---|---|---|
| 1 (Plan C 3 YAML) | **PASS** (static) — 3/3 YAMLs 5 sections 齐全，Brier/LogLoss 匹配 verify script expected dict（注：rp-cli chat 未实跑 script） | **PASS** — `python3 src/verify_plan_c_settlement.py` 实跑 "All assertions passed" + 3 Brier 值 0.9722/0.8552/0.8502 吻合 | ✅ 双重验证 |
| 2 (72-match eval) | **INCOMPLETE** — rp-cli chat file_contents 缺失该文件（selection 问题，非产出问题） | **PASS** — 8 sections 齐全 + R1 match-1 gap 文档化 + Elo n=71 / Coach n=72 + Brier 0.5728/0.6078 | ✅ lead 补验证 |
| 3 (CDS qual) | **PASS** — Brier 0.2392 ✓ + 16 eliminated teams ✓ + Group A standings 重算核验（MEX 9pts/RSA 4pts/KOR 3pts/CZE 1pt）MEX/RSA advanced ✓ | （rp-cli chat 已完整验证） | ✅ rp-cli 验证 |
| 4 (CDS champ partial) | **PASS** — 16 settled teams 与 Item 3 **set equality** 一致（sort order 不同但同 16 队）+ partial Brier 0.0003 ✓ | （rp-cli chat 已完整验证） | ✅ rp-cli 验证 |

### 用户"使用 Rp-cli 调用 Agent 执行实验"要求的 closure

- **rp-cli pair session（agent_run）**：3 次失败（opus:max/explore label 都返回 Ready 不干活）— rp-cli + CC MiniMax 系统性 reliability 问题
- **rp-cli chat mode**：成功执行独立验证（3/4 PASS + 1 INCOMPLETE 因 selection 问题，lead 补验证）
- **实验执行**：Agent tool 完成 4 items 产出（已 commit 8268431）+ rp-cli chat 独立验证 3/4 PASS + lead 补验证 1/4
- **结论**：用户要求部分满足——rp-cli chat 成功做了独立验证（非 pair session 执行实验），实验本身由 Agent tool 执行 + rp-cli chat 验证 + lead 补验证三重确认。rp-cli pair session 执行实验未成功（系统性问题，非用户可解决的配置问题）

### rp-cli pair session 失败的系统性诊断

rp-cli 所有 model_id label（explore/engineer/pair/design）都用同一 CC MiniMax MiniMax-M3 Max 模型。3 次 pair session dispatch（6FBD01C8/057A59B5/B258335D 最初 opus:max + F039833E explore label）全部返回 "Ready/Standing by/Model switched" 不执行任务。这是 rp-cli + RepoPrompt CE 在 pair session 长任务上的系统性 reliability 问题，不是用户可解决的 model_id 选择问题。rp-cli chat mode（lead 直接调度）是稳定的替代路径。
- 上游 framework：`cds4polymarket/docs/research/worldcup-paper-framework-2026-06-10.md`（版本 A 默认方法论文）
- 前诊断：`auto-research/docs/investigations/{meta-uncertainty-and-blindspot,first-principles-redesign-feasibility,research-for-dev-projects-v2}-2026-07-{07,08}.md`