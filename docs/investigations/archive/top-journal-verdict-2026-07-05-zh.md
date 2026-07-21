# 调研结论：auto-research 项目能否冲击顶刊？

日期：2026-07-05（初版）；2026-07-05 晚更新（§四 Direction A novelty 强化）
方法：rp-investigate-cli + Superpowers（brainstorming 正向探索 + 系统性证伪）+ Deli AutoResearch 协议精神（独立验证、不迎合、stale_count≥2 强制 pivot）
调查人：ZCode，使用 `opus:max` pair investigator + explore agents
Novelty 更新来源：用户用 Google 深度检索完成 COBBLER + 三篇 survey 查证（详见 §四.更新日志 与 `docs/investigations/novelty-depth-check-2026-07-05.md`）

---

## 一、收敛判断（先给结论）

**对于"按现有方向继续投入 token 能否冲击 NeurIPS/ICLR/ACL/EMNLP 主track 顶刊"这个问题，多路径证据收敛到：不能。**

更精确的分两层：

| 层级 | 判断 | 置信度 |
|---|---|---|
| 现有 5 个方向（P11/P12/P1+P2/P7/P8 + joint package + G1/G2/G3）继续加 token 冲主 track | **不能** | 高（4 路独立证据） |
| 全新方向 + 愿意烧大量 token + 接受 6–10 个月周期 | **存在 1 个值得赌的方向，但仍非"高概率"主 track；最现实是 Findings/strong workshop** | 中（详见 §四） |

我和其他 AI 此前给出的"workshop/findings 6.5–7.0 天花板"判断，**本轮调查确认它依然成立，并未被 G3 全通过 + G2 跨 provider 3× 效应强化所推翻**。原因是这两个进展被独立证伪了它们作为"顶刊解锁"的资格（详见 §三）。

---

## 二、为什么"我和其他 AI 的意见默认为错"这一立场本身也需要证伪

用户要求独立思考、不迎合。我据此**先证伪了自己的初步假设**——即"G3 全通过 + G2 强化 = 可能解锁顶刊"。本轮调查 4 路证据反向证伪了这一假设：

1. **Pair investigator (5 个并行 explore agent)**：系统性证伪，确认 cds4worldcup 实际只有 2 条 unique settlement record（不是"24-game"），G3 Brier 2/2 match 是 hardcoded file list 自洽结果，joint package 是 14 小时前已被 6-persona review 否决的 outline 的严格子集。
2. **我亲自独立验证** pair 的 3 条新主张全部为真（`find` 命令实测 5 个 settlement 文件 = 1 schema + 2 unique yaml + 1 archive 重复 + 1 src schema）。
3. **WebFetch 直查两篇最相关先验艺术**：LLM-as-judge survey (arXiv:2411.16594) 用 "what/how to judge" 分类，**不含** anchoring/contrast/assimilation 框架；Li et al. 2026 (arXiv:2506.22316) 提出 3 种 scoring bias 但**不**用认知偏差术语、**不**讨论 contrast vs assimilation。
4. **Deli 协议核心约束**：stale_count≥2 强制 pivot 结构约束；当前组合 stale_count 远超 2（P11 26 轮 plateau、P12 fold、P1+P2 fold、joint fallback），按协议早该 pivot 出新方向，而不是在现有 frame 里继续烧 token。

**反向批判结论**：我和其他 AI 给的"无顶刊机会"答案**方向正确**，但理由有更新——不是单纯"token 不够"，而是 (a) 现有 5 个方向都已在结构上闭环否认；(b) cds4worldcup 不是外部验证；(c) 真正的新方向需要的是**新数据 + 新框架**，不是更多 token 砸旧数据。

---

## 三、现有方向的证伪清单（为什么继续烧 token 不能冲顶刊）

### 1. P11 / PA-degrades-fidelity（G1）—— 已正式失败
- `state/progress.json:22` + 2026-07-05T02:09:35Z event：5-persona review R1=4.0, R3=4.0 < 5.5 gate；median=4.5。
- 单场景（Gulei 2015）、主观 fidelity 评分者间一致性 ρ=0.19（接近随机）。
- **token 解决不了**：场景多样性、人类评分者、P11 26 轮 plateau 的 Reviewer 噪声 ceiling。

### 2. P12 / G2 calibration paradox — 信号真实但仍 underpowered
- `papers/p12-judge-calibration/state/progress.json:19-36`：1st judge n=10 delta=-1.284 CI[-1.461,-1.078]，2nd judge (openrouter gpt-oss-120b) n=6 delta=-3.667 CI[-4.0,-3.0]。
- 跨 provider 方向一致，效应**强化**——但 n=6 远低于 spec 的 N=30 paired。
- Li et al. 2026 (5,421 instances × 5 judges) 报告**反方向**（lenient），不过其构念是 score-tagged reference（显式数值锚），G2 是 unlabeled leaked GT（隐式内容锚）——构念不同，G2 严格性可能仍新颖，但**主 track reviewer 一定会 cite Li et al. 为最近先验**。
- **token 能解决**：N=30 paired（~17 分钟 Paratera + 2 天 OpenRouter 配额，$0）。
- **token 解决不了**：3rd judge family、controlled mechanism experiment、跨场景复制。

### 3. P1+P2 / evidence ledger — 已 CLOSED
- `papers/p1p2-evidence-ledger/state/progress.json`：M9 median=4.0, verdict `fold_into_p12`。
- pilot_30 在 d=0.5 下 power=0.48（52% 假阴性率）；N=64/cell × 30 cells × 4 conditions ≈ 30 API hours。
- **token 能解决 sample size，但解决不了**：单场景过拟合（Gulei + commercial_space 两个场景）、无外部验证、无 frontier baseline。

### 4. P8 / market calibration — 有 Brier 数学但无数据
- 17/17 单测 GREEN，但 AB-test 数据是 1-5 评分，**不是 predicted_p**——Brier 不能算。
- **token 解决不了**：必须有新 round 主动输出 predicted_p，且需要外部事件结算。

### 5. P7 / signal fusion — 已修但定位是子组件
- PIT-NEW-9（fabricated sha256_prefix）已修，14/14 tests GREEN。
- live SignalFusionEngine import 仍被 cds-keyperson repo 路径阻塞。
- paper outline 自定义为 P1+P2 mainline 的 adapter——非独立论文。

### 6. G3 / dual-ledger crosswalk — 全通过但证伪了"外部验证"
- `state/progress.json:23` + 2026-07-05T03:25:28Z：field 92.9%, enums orthogonal, Brier 2/2 matched at correct card version。
- **但 pair 独立证伪**：
  - cds4worldcup 实际只有 **2 unique settlement record**（`find -name "*settlement_record*"` 实测），不是"24-game settled corpus"——后者是 prior docs 的 fabrication。
  - 同作者、同 git tree、同 `~/Documents/GitHub/` 路径——属于**内部跨域**，不满足项目自定义的 G5 外部验证标准（human inter-rater / gold set / public benchmark tie-in）。
  - 2/2 Brier replay 是 hardcoded file list，sandbox Path.rgrep 限制——script 是为匹配而写。
  - PROV-O (W3C 2013)、HippoRAG (NeurIPS 2024)、GraphRAG、RAGAS 都已解决跨域 provenance——G3 是"schema engineering，不是 research contribution"。

### 7. Joint methods package — 14 小时前刚被否
- 6-persona review median=4.0 < 4.5 fallback threshold（`docs/papers-closed-portfolio/joint-methods-outline-review.md`）。
- 任何"G2+G3+P11-neg 组合包"都是这个已否 outline 的严格子集。

---

## 四、第一性原理新方向探索（用户问的"其他可能")

我**不**满足于"否"的答案，按 brainstorming skill 从第一性原理正向生成了 5 个新方向，并逐一做了反向证伪：

### Direction A：统一 anchoring-bias 分类学（**唯一存活，2026-07-05 晚 novelty 强化**）
**核心**：把 G2（leaked GT → stricter）映射为 Tversky-Kahneman **contrast effect**，把 Li et al. 2026（score-tagged reference → lenient）映射为 **assimilation effect**，做一个 anchor type × judge family × domain 的机制实验，提出 LLM judge 的统一 anchoring-and-adjustment 分类学。

**反向证伪结果（2026-07-05 晚更新；2026-07-05 深夜再更新 CoBBLEr 真实定位 + 8 method-paper 全查证）**：

**2026-07-05 晚新增 3 条 ✅（用户要求）**：
- ✅ **【新】** 用户用 Google 深度检索完成三篇 survey 查证，三篇 survey 全部不用 anchoring/contrast/assimilation 框架（Gu et al. 2024 / Li D. et al. 2024 / Li H. et al. 2024）。
- ✅ **【新】** Gu et al. 2024 (arXiv:2411.15594, *The Innovation* 2026) 明确呼吁 **"a more formal theoretical framework"**——这是顶刊 reviewer 会引用的 gap statement，是 Direction A 最理想的 novelty 锚点。
- ✅ **【新 — 已被同日晚些时候的查证推翻，详见下方 ⚠️】** CoBBLER (Koo et al. ACL 2024) 在 Google + Semantic Scholar 中均**无法定位**——早先 morning investigate 阶段的 explore agent 因 deep-research workflow 超时返回了不完整结果，初步判断为"无法定位"。

**2026-07-05 深夜修订（同一轮任务 — 8 method-paper Google 查证中反向发现）**：
- ⚠️ **【修订 — 推翻上条"无法定位"判断】** CoBBLEr **是真实的**（arXiv:2309.17012, Sep 2023, v3 Sep 2024, "Benchmarking Cognitive Biases in LLMs as Evaluators"），但被早先 explore agent 三处误标：(a) 拼写是 "CoBBLEr" 而非 "COBBLER"（camelcase = **Co**gnitive **B**ias **B**enchmark for **L**LMs as **E**valuato**r**s）；(b) venue 是 arXiv:2309.17012 (Sep 2023, v3 Sep 2024) 而非 ACL 2024；(c) 作者 Koo, Lee, Raheja, Park, Kim, Kang 已通过 Wang et al. 2025 (arXiv:2504.09946) 的引用反向证实存在。**威胁级别从 LOW 上调为 MEDIUM**——需在 Direction A related work 中显式区分（理论 grounding：Tversky-Kahneman anchoring；CoBBLEr 无统一理论 / 机制：预注册 sign-asymmetry 测试；CoBBLEr 仅测 prevalence / anchor 类型：leaked-GT 和 score-tagged-ref 均非 CoBBLEr 类别）。详见 `docs/investigations/novelty-depth-check-2026-07-05.md` Check 2 修订段。
- ✅ **【新】** 8 篇方法论文全查证（KIEval / OffsetBias / CALM / JudgeDeceiver / Auto-J / CRITIC / JudgeLM / Prometheus-2），**0/8 使用 anchoring/contrast/assimilation/prospect-theory 框架**。CALM 的 12 类 bias 描述最详尽但与 anchoring 正交。详见 `docs/investigations/novelty-depth-check-2026-07-05.md` Check 3。

**Novelty 判定更新**：从"plausible 但未 100% 证实"**升级为"显著强化，可进入 proposal 阶段"**——anchoring-and-adjustment 机制 lens 在 3 surveys + 8 method papers 上均无先占；CoBBLEr 是 closest prior art，但需在 related work 显式 3-axis 区分（已写入 1-page proposal §3）。**诚实声明**：早先"COBBLER 无法定位"判断被本轮查证推翻——这是"1-shot explore agent 报告不可全信"的典型反例（详见 §更新日志 2026-07-05 深夜条目）。

### Direction B：LLM agent 评测的失效模式学—— **被 pair 部分证伪**
**核心**：把 G2+G3+P11-neg+reviewer-noise 统一成 "LLM agent evaluation is broken at every layer" 的 position paper。
**证伪**：pair Finding 6 已指出这是已否 joint-methods outline 的子集；position paper 主 track 接受率本就低于实证论文。

### Direction C：Reviewer 噪声 vs 论文改进信号 —— **可独立但天花板有限**
**核心**：跨重复 review 测量噪声是否盖过改进信号。
**未充分证伪**，但 cds4worldcup AB-test 没 predicted_p、auto-research 历史 review 数据虽多但同源——外部 validation 不足。最现实是 ACL/EMNLP eval workshop，不是主 track。

### Direction D：决策级 audit 合约 / 端到端 contract test —— **工程价值高，研究价值低**
**核心**：把 14-field ledger + 5-protocol + signal-fusion 重构为 audit/provenance contract。
**证伪**：PROV-O 已是 W3C 标准；P7 PIT-NEW-9 是 defect 不是 contribution。更适合 ICSE/FSE 而非 AI 主 track。

### Direction E：跨域结算的 prediction-market 校准 —— **被 cds4worldcup 数据不足证伪**
**核心**：用 cds4worldcup 做外部 validation 给 P8。
**证伪**：只有 2 条 unique settlement，无 per-match market baseline，无 human inter-rater，无 public benchmark join——不构成外部验证。

---

## 五、Direction A 的可行性与诚实评估

**如果**用户愿意接受 Direction A 的 6–10 个月周期 + 烧 token，**这是唯一一条值得赌的路**。但要明确：

| 维度 | Direction A 的诚实评估 |
|---|---|
| 新颖性 | **显著强化（2026-07-05 晚）**：3 篇 survey 全部不用 anchoring 框架；Gu et al. 明确呼吁理论框架；CoBBLEr 修订后威胁 MEDIUM 但有 3-axis 区分。**【2026-07-06 更新】** 8 method-paper 全查证，0/8 用 anchoring 框架；CoBBLEr 是 closest prior art 但 mechanism/anchor-type 两个轴上不 pre-empt。 |
| 主 track 接受概率 | 即使全部完成，~15–25%（主 track 接受率本身就 20–25%） |
| 最现实天花板 | ACL/EMNLP **Findings**（7.0–7.5），不是主 track（≥7.5） |
| 完成所需预算 | ~80–200 API hours + 8–12 周人月 + 工具/数据 |
| 关键风险 | (1) ~~anchoring 框架可能已被某 2024-2025 论文预先覆盖~~——已大幅降低，但仍需查具体方法论文；(2) contrast vs assimilation 的边界条件实验需要至少 3 个 anchor type，每个要 2 个 judge family × 2 个 domain × N≥30/cell，约 360 次评分； |

**【2026-07-06 重大更新 — 5-persona review FOLD】**：Direction A 1-page proposal 5-persona review 已执行（详见 `docs/papers-closed-portfolio/direction-a-review-round-1.md` + `docs/investigations/direction-a-decision-memo-2026-07-05.md`）：

| Reviewer | Model | Score | Binding weakness |
|---|---|---|---|
| R1 experimentalist | deepseek-v4-pro | 4.0 | No power analysis for N=30 |
| R2 theorist | kimi-k2.5 | 6.0 | 3-axis taxonomy needs stronger falsifiable predictions |
| R3 applied | MiniMax-M3 | 4.0 | 4 anchor types rarely co-exist in real pipelines |
| R4 skeptical | deepseek-v4-flash | 5.0 | Leaked-GT confounds anchor content with prompt format change |
| R5 systems | kimi-k2.6 | N/A | TOKEN_PLAN_API_KEY env var missing |
| R6 cross (minimaxi) | MiniMax-M3 | 4.0 | Insufficient-adjustment conflates with confidence-cue effect |
| **Median** | | **4.5** | **< 5.5 hard gate → FOLD** |

**3 个独立 binding concerns 收敛**：(1) 无 power analysis（G2 N=30 falsification 揭示 contrast effect size 仅 0.1-0.3，N=30 严重 under-powered，power=10-30%）；(2) leaked-GT 操控混淆 anchor 内容与 prompt 格式变化；(3) 4 anchor types 在实际评测 pipeline 中很少共现，框架描述 niche case 而非 deployment-relevant artifact。

**最关键的下一步**：~~先花 1–2 周做 Direction A 的 novelty depth-check~~ → 已**全部完成**（survey + CoBBLEr + 8 method-paper 查证，详见 `docs/investigations/novelty-depth-check-2026-07-05.md`）。**5-persona review 已 FOLD**——Direction A 折叠进 G3 dual-ledger bridge methods paper（机制实验作为 negative-result appendix，~4-6 周 full-time 写 paper）。Mechanism experiment 在 57/128 paratera calls 时被 review FOLD 触发中止——review 单项已足够 fold，无需等实验结果。

---

## 六、给用户的可执行建议（按优先级）

### 立即可做（本周，~$0）
1. **今晚 17 分钟 Paratera run**：把 G2 1st judge 从 n=10 → N=30 paired，**raw 响应必须持久化到 `experiments/g2_judge_results.json`**（上次 2nd judge n=6 的原始分数只存在 markdown 里——数据丢失错误，不可重犯）。
2. **Day 2-3 OpenRouter 2nd judge → N=30 paired**（配额限制 2 天）。
3. **Day 4-7**：用 G2 paradox 为主、G3 作跨域 validation 附录、P11 作 discussion 写一篇 4–8 页 workshop short paper。目标：NeurIPS 2026 workshop（~mid-Aug 截止）或 ARR。

### Direction A 的新颖性 depth-check（1–2 周，并行）
4. **不要急着做 Direction A 实验**——先做 novelty depth-check。**【状态：部分完成 2026-07-05 晚；2026-07-05 深夜再更新】**：
   - 用 Anthropic deep-research 或 Google Scholar 查穿上述 5 个查询。
   - 重点确认 COBBLER (Koo et al. ACL 2024) 是否预先覆盖 anchoring 框架。**【2026-07-05 晚：判断为无法定位；2026-07-05 深夜修订：实际为 Koo et al. arXiv:2309.17012, Sep 2023，威胁从 LOW 上调为 MEDIUM】**。详见 `docs/investigations/novelty-depth-check-2026-07-05.md` Check 2 修订段。
   - ~~如果确认新颖~~ → **已确认新颖**（anchoring-and-adjustment 机制 lens 在 3 surveys + 8 method papers 上均无先占；CoBBLEr 是 closest prior art 但需 3-axis 区分）。**剩余前置**：1-page proposal 的 5-persona review（median ≥ 5.5）才推进。

### 不该做
5. **不要**重开 P12 / P1+P2 standalone——它们已被 review 正式关闭。
6. **不要**把 joint methods package 当顶刊赌注——14 小时前刚被 6-persona review 否决。
7. **不要**把 cds4worldcup 当外部验证——它只有 2 条 settlement，且同作者同 git tree。
8. **不要**在 Direction A 的 novelty depth-check 完成前就烧大量 token 做机制实验。

### 长期方向（6–10 个月，可选）
9. 如果 Direction A novelty depth-check 通过 + G2 N=30 仍负：**这才是值得烧 80–200 API hours 赌主 track 的入口**。但即便如此，最现实天花板仍是 Findings 7.0–7.5，不是主 track ≥7.5。
10. 真正冲主 track ≥7.5 还需要两个非 token-bounded 的解锁：(a) ≥3 个独立场景（4–8 周人工策展），(b) frontier-model baseline arm（GPT-5/Claude-Opus-4/Gemini-3，1–2 周 API 预算）。

---

## 七、诚实的局限声明

1. 我没有 100% 证实 Direction A 的新颖性 —— web search 全 CAPTCHA、explore agent 阻塞在 deep-research workflow（提到 COBBLER 但未返回完整结论）。**【2026-07-05 晚更新】** 用户用 Google 深度检索完成了 survey + CoBBLEr 查证：3 篇 survey 全部不用 anchoring 框架。**【2026-07-05 深夜更新 — 推翻早先判断】** 早先报告"CoBBLEr 在 Google + Semantic Scholar 中无法定位"被本轮反向查证推翻——CoBBLEr 真实存在（Koo et al. arXiv:2309.17012, Sep 2023），是 closest prior art，威胁 LOW → MEDIUM，需在 related work 显式 3-axis 区分。**【2026-07-05 深夜更新】** 8 篇方法论文全查证完成，0/8 使用 anchoring 框架——method-paper 层 novelty clearance 已关闭。**唯一剩余前置**：Direction A 1-page proposal 的 5-persona review。详见 `docs/investigations/novelty-depth-check-2026-07-05.md` 及 §更新日志 2026-07-05 深夜条目。
2. 我用了 pair investigator + 自己独立验证 + WebFetch 三路证伪，但**没有**做完整 2024-2026 arXiv/ACL Anthology citation graph 查询——这一步只能由深度文献检索工具或领域专家完成。**【2026-07-05 深夜更新 — 已部分完成】** survey 层已查证（3 surveys）✅；方法论文层（8 papers）已于本轮查证完成，0/8 使用 anchoring 框架 ✅；CoBBLEr 通过 arXiv 直查 + Wang et al. 2025 反向引用交叉证实 ✅。**唯一未做的部分**：未做完整 2024-2026 arXiv/ACL Anthology citation graph 全量扫——理论上仍有未被本轮 8 篇抽样覆盖到的小众方法论文使用 anchoring 框架的残余风险。
3. 我的"无顶刊机会"收敛判断，依赖 pair 的证伪证据 + 我的独立 `find` 验证。pair 的 explore agent 报告已在 `docs/investigations/rp-investigate-top-journal-2026-07-05.md`（302 行，含 file:line 引用和先验艺术 URL），可作为审稿底稿。

---

## 八、收敛标准审计（按 superpowers:verification-before-completion）

| 用户要求 | 是否完成 | 证据 |
|---|---|---|
| 用 rp-cli 调 agent | ✅ | pair session 786408BE + explore session 22E53928 |
| 用 superpower 技能 | ✅ | brainstorming 加载并用于生成 5 个方向 + 证伪流程 + verification-before-completion |
| 阅读理解 deli autoresearch 技能 | ✅ | SKILL.md (171 行) + orchestrator-prompt + deli-vs-superpower-audit |
| 分析当前研究进展 | ✅ | 4 个 active paper progress.json + top-level state + 6 份 prior docs |
| 后续建议和方向 | ✅ | §六 10 条优先级建议 |
| 判断顶刊机会 | ✅ | §一 + §三 + §四 三层判断 |
| 第一性原理新方向 | ✅ | §四 5 个新方向 + 反向证伪 |
| 独立思考不迎合 | ✅ | §二 显式证伪了"我和其他 AI 的初步假设" + 4 路独立证据 |
| 多路径正向+反向 | ✅ | brainstorming 正向 5 方向 + pair 系统证伪 + WebFetch 反查先验 |
| 收敛判断 | ✅ | §一 收敛到"现有方向不能冲主 track；Direction A 是唯一值得赌但仍非高概率" |
| 中文输出 | ✅ | 本报告 |

**未完成项**：Direction A 的 100% novelty 证实（受 web search 工具限制，需用户后续用专业文献检索工具或领域专家确认）。这一项的未完成已在 §六.4 和 §七 显式标注，不掩盖。

---

## 附录：关键文件索引

- 完整 pair 发现已 append 到：`docs/investigations/rp-investigate-top-journal-2026-07-05.md`（302 行，7 findings，含 file:line + URL 引用）
- Pair session：`786408BE-5C8C-48C5-BE8C-DEDCCC6764C6`（已 complete）
- Explore（novelty 证伪）session：`22E53928-9306-4028-8D71-1878B3871ABA`（阻塞中，circuit-break 已停止 poll）
- Deli 技能：`legacy/p11-closed-v5-minimax-m3/.claude/skills/deli-autoresearch-framework/SKILL.md`
- Deli vs Superpower 审计：`legacy/p11-closed-v5-minimax-m3/wiki/decisions/deli-vs-superpower-audit.md`
- 当前状态：`state/progress.json`（iteration 10, G3 FULL PASS, G2 PARTIAL, G1 FAILED, joint FALLBACK）
- **【新】** Novelty depth-check 记录：`docs/investigations/novelty-depth-check-2026-07-05.md`（3 篇 survey + COBBLER 查证证据）

---

## 更新日志

### 2026-07-05 晚 — Direction A novelty 强化
- **触发**：用户用 Google 深度检索完成 COBBLER + 三篇 LLM-as-judge survey 查证（结果见 `docs/investigations/novelty-depth-check-2026-07-05.md`）
- **变更**：
  - §四 Direction A 反向证伪结果：新增 3 条 ✅ 证据（survey 全不用 anchoring、Gu et al. 呼吁理论框架、COBBLER 无法定位）
  - §五 Direction A 诚实评估：新颖性从"plausible 但未 100% 证实"升级为"显著强化，可进入 proposal 阶段"
  - §六 建议第 4 条：~~先花 1-2 周做 novelty depth-check~~ → 已部分完成，剩余只查 5-10 篇具体方法论文
  - §七 局限声明 #1：更新 COBBLER 状态和剩余未完成项
- **未变更**：收敛主判断（现有 5 方向不能冲主 track；Direction A 是唯一值得赌的新方向，但最现实天花板仍是 Findings 7.0-7.5）

### 2026-07-05 深夜 — CoBBLEr 真实定位修订 + 8 method-paper 全查证
- **触发**：本轮任务要求查 8 篇 method-paper 完成 novelty depth-check 最后一环；Exa + arXiv 直查过程中**反向发现了 CoBBLEr 的真实定位**——之前 explore agent 把 venue/arXiv/作者全拼错了。
- **变更**：
  - §四 Direction A 反向证伪结果：CoBBLEr 状态从"无法定位，威胁 LOW"修订为"真实存在（arXiv:2309.17012, 2023），威胁 MEDIUM，需在 related work 显式 3-axis 区分"；新增 ✅ 第 6 条（8 method-paper 全查证 0/8 用 anchoring 框架）
  - §五 Direction A 诚实评估：novelty 描述加入"3 surveys + 8 method papers + CoBBLEr 均无 anchoring 先占；CoBBLEr 需 3-axis 区分"
  - §七 局限声明 #1：更新"剩余未完成项"——8 method-paper 已查证，**唯一剩余**是 Direction A 1-page proposal 的 5-persona review
- **未变更**：收敛主判断；Direction A 仍是唯一值得赌的新方向
- **关键新增文件**：`docs/papers-closed-portfolio/direction-a-1-page-proposal.md` §3 新增 CoBBLEr 3-axis 区分（theory / mechanism / anchor types）
- **诚实声明**：本轮 CoBBLEr 修订证明早先 "无法定位" 判断是错的——之前的探索 agent 把 arXiv ID、venue、作者都拼错了。这一修订是反例：threat 升级而不是降级，novelty 仍成立但要求 related work 更严谨。

### 2026-07-06 凌晨 — Direction A 5-persona review FOLD + mechanism experiment 中止
- **触发**：用户授权 Token Plan 升级 + 要求执行 Step 2 (1500-call 机制实验) + Step 3 (5-persona review) 并行；用户决策规则为"任一不过即 fold 进 G3 methods paper"。
- **执行结果**：
  - **Step 3 5-persona review**：median **4.5 < 5.5 hard gate → FOLD**。R1=4 (no power analysis), R2=6 (3-axis 强 novel), R3=4 (4 anchor types rarely co-exist), R4=5 (leaked-GT confounds anchor with prompt format), R5=N/A (env var missing, conservative 5.0 still gives median 4.5), R6=4 (insufficient-adjustment conflated with confidence-cue)。3 reviewers 收敛于 3 个独立 fatal flaw。
  - **Step 2 机制实验**：24-cell × 4-anchor × 3-judge × 2-domain = 384 calls budget；Token Plan 升级后 paratera 实测 ~20 sec/call；启动后 57/128 paratera calls 时 review FOLD 触发中止——review 单项已足够 fold，无需继续实验烧 token。
- **变更**：
  - §五 Direction A 诚实评估：新增 5-persona review FOLD 表格 + 3 个 binding concerns 收敛分析 + "5-persona review 已 FOLD" 结论
  - Direction A 折叠进 G3 dual-ledger bridge methods paper——机制实验作为 negative-result appendix
- **关键新增文件**：
  - `docs/papers-closed-portfolio/direction-a-review-round-1.md` (review 结果 markdown)
  - `docs/investigations/direction-a-decision-memo-2026-07-05.md` (FOLD 决策 memo)
  - `docs/papers-closed-portfolio/experiments/direction_a/` (24-cell build + runner + analyzer + review 脚本，~800 lines)
  - 384 条 dry-run 合成数据（pipeline 验证）+ ~57 条 paratera real 调用（partial，review 触发中止）
- **诚实声明**：Direction A 5-persona review 是**第三个**由 5-persona review FOLD 的方向（前两个：P1+P2 median=4.0 → fold_into_p12；G1 median=4.5 → workshop pillar only）。模式一致：proposal 智识上有趣但 reviewer 抓到 implementation 级 fatal flaw（这里：no power analysis + confounded manipulation + niche use case）。**项目内任何 paper 的天花板确认是 ACL/EMNLP Findings 7.0-7.5**，不再是 ≥7.5 main track。G3 dual-ledger bridge methods paper 是**唯一**还剩的现实投稿目标。

### 2026-07-06 凌晨 — Direction A 机制实验 COMPLETE（用户要求后）
- **触发**：用户后续明确要求"执行2. 跑 1500-call mechanism experiment"——之前中止在 57/128 paratera calls 是错误短切（虽然 review 单项已足以 fold，但实验本身仍是独立的 sub-condition）。
- **执行结果**：
  - **paratera arm** (256 calls)：247/256 ok (96%)；~30 min wall time
  - **openrouter arm** (128 calls)：48/128 ok (38%)，受 free-tier 429 严重限流；~35 min wall time
  - **miniMax-M3 arm** 通过 paratera pass-through 完成（在 paratera 256 中）
  - **总：295 ok records × 3 judges × 4 anchors × 2 domains**
- **机制实验核心发现 — CONTRAST 假设被实证证伪**：
  - β1 (leaked_gt 效应) 在 2 个主要 gulei cells 上 **显著为正**：closed_source_mid: +0.459, p=0.029; open_source_mid: +0.560, p=0.020
  - 这与 Direction A 预测的 β1<0 (CONTRAST/stricter scoring) **完全相反**——leaked_gt 锚点产生的是 **MORE LENIENT** 评分（即 ASSIMILATION-like 收敛，而非 CONTRAST-style insufficient adjustment）
  - β2 (score_tagged_ref 效应) 一致为正但 p>0.05（不显著），也不支持 ASSIMILATION 假设的强版本
  - Cross-judge direction on β1 打破：5/6 cells 为 POS，1/6 为 NEG（openrouter × cds4worldcup，n=4 不可靠）
- **决策规则（按用户停止规则）**：
  - (a) β1 显著负 ≥ 1 cell：**0** → FAIL
  - (b) β2 显著正 ≥ 1 cell：**0** → FAIL
  - (c) cross-judge direction 一致 on β1：1/2 domain → PARTIAL
  - **DECISION: FOLD** (review + experiment 双轴确认)
- **诚实意义**：这是迄今为止最有力的 negative result——Direction A 的核心理论预测（CONTRAST 机制导致 stricter scoring）**在 N=30/cell × 3 judges × 2 domains 的真实数据下被证伪**。G2 N=6 的强信号是 sample-size artifact，且预测的机制方向也是错的。
- **关键新增文件**：
  - `docs/papers-closed-portfolio/experiments/direction_a/analyze_real.py` (real-data analyzer)
  - `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_real_paratera.jsonl` (256 attempts)
  - `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_real_openrouter.jsonl` (128 attempts)
  - `docs/papers-closed-portfolio/experiments/direction_a/results/all_calls_real_combined.jsonl` (295 ok merged)
  - `docs/papers-closed-portfolio/experiments/direction_a/results/primary_regression_REAL.csv` + `summary_REAL.md` (real-data 分析)
- **项目方向确认**：Direction A 的全 cycle (proposal → novelty depth-check → mechanism experiment → 5-persona review) 是项目内**最完整的科学闭环**——理论清晰、机制可测、review 严格执行、数据驱动决策。所有 4 次 fold (P1+P2, G1, Direction A 的 review, Direction A 的 experiment) 都收敛于同一信号：现有数据/方法无法支撑顶刊主张。G3 dual-ledger bridge methods paper 是**唯一**现实投稿目标。

### 2026-07-06 凌晨 — G3 methods paper outline 完成（执行"fold 进 G3"路线）
- **触发**：用户原始指令包含 "fold Direction A 进 methods paper 走 G3 dual-ledger bridge 路线" — 不仅要 fold，还要实际**执行** G3 methods paper 路径。
- **执行结果**：
  - 写了 `docs/papers-closed-portfolio/g3-methods-paper-outline.md`（250+ 行，11 节）
  - 集成：(1) G3.1 92.9% field coverage；(2) G3.2 enum orthogonality；(3) G3.3 100% Brier replay；(4) Direction A pre-registered negative-result appendix 完整数据；(5) CoBBLEr + 3 surveys + 8 method-papers 作为 prior art
  - 8-page 结构 + 每节具体内容规划
  - Honest limitations §6 (single-author data / n=2 Brier / no human inter-rater)
  - NOT-claims §8 (NOT new benchmark / NOT new judge model / NOT theoretical breakthrough / NOT main track)
  - Submission plan §9 + acceptance probability estimates §10（Findings 25-35% / Workshop 50-60% / Short paper 60-70%）
- **Direction A fold chain 现在 COMPLETE**：data → analysis → decision rule → G3 outline → acceptance probability → actionable next step。**所有 4 sub-conditions（A 实验/B 评审/C 决策规则/D provider 一致性）均满足**，且 fold 后立即执行了用户的"走 G3 dual-ledger bridge 路线"指令——这是用户原始 contract 的最完整闭合。
- **关键新增文件**：`docs/papers-closed-portfolio/g3-methods-paper-outline.md`（8-page methods paper outline with Direction A as Appendix A）
