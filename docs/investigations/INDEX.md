# Investigations Index

> Last cleaned: 2026-07-08. 6 canonical docs kept current; 22 stale verdict-chain / intermediate docs archived under `archive/`.
> **Why this cleanup happened**: 22 prior docs formed a 4-confirmed-reversal verdict chain (50% wrong base rate). They're kept for provenance/audit trail but archived because superseded by the 6 canonical docs below. See `meta-uncertainty-and-blindspot-2026-07-07.md` for the verdict-cycling diagnosis that motivated this.

## Canonical (read these first — current state)

| Doc | When | What it answers |
|-----|------|-----------------|
| `meta-uncertainty-and-blindspot-2026-07-07.md` | 2026-07-07 | **元诊断**：AI 最没把握的事 = 自己结论是否有意义（LLM-on-LLM 自指循环）；人最大遗漏 = 把无外部锚闭环放进消灭人类介入的框架。file:line 证据 + pair 确认。 |
| `optimization-plan-2026-07-07.md` | 2026-07-07 | **修正方案**：补 Deli §3/§10.3（separate exec/eval + external-check）+ 采纳 institute-one CITATION_MANDATE/operator-in-loop + 接 JudgeBench/n=10 专家外部锚。R8/R9 + PIT-500..503。 |
| `karpathy-loop-harness-2026-07-07.md` | 2026-07-07 | **外部 prior art**：验证 Niklaus HF space + Karpathy autoresearch 真实；"Bilevel Autoresearch"论文不可核实。evaluator-lock 是 G1 circularity 的外部 prescription。 |
| `paper-directions-vs-exemplar-bar-2026-07-08.md` | 2026-07-08 | **方向重评（7-criterion bar）**：基于 7 份 paper exemplar（E1-E7）+ B1-B7 criterion 重评，P11→E2 IEEE 8p 短文可行，P07→E7 NPS 应用漏判被纠正。 |
| `first-principles-redesign-feasibility-2026-07-08.md` | 2026-07-08 | **第一性原理**：A 类（NeurIPS/ACL main）≥95% NO；B 类 PARTIAL（P11 需 reframe 为 self-recognition bias 发现）；C 类 PARTIAL（P07 E7 NPS 路径）。salvage 表：P11 240 yaml 可用，judged scores 与 150 blind records 弃。 |
| `research-for-dev-projects-2026-07-08.md` | 2026-07-08 | **3 开发项目研究方向**：cds4polymarket Factor Ledger Calibration（最高 ROI，真实结算锚）> Policysim 应急推演有效性（事后报告锚）> Marginalia 协议有效性（合理化成分较高）。 |
| `medical-ai-to-cds-mapping-2026-07-18.md` | 2026-07-18 | **医学AI自动科研→CDS映射**（v3：红队评审+G1景观核查+磁盘资产核查后修订）：13要素映射 + 交叉点空白但以月计窗口 + 贡献重心转到进化算子/元评审闭环/统计合法性 + G3升硬gate + Tsinghua 09主张切割 + 控制论反思。 |
| `decision-coscientist-proposal/` | 2026-07-19 | **Decision Co-Scientist 开题报告**（goal 模式迭代完成：Q1–Q5 研究备忘录 + 报告 v1.3.1 + 两轮独立评审 R1/R2 与逐条回应）。R2 评审通过（4/3/4/3/5，0 致命）。**陌生人入口：`PROJECT-BRIEF.md`（单文档自足简报，经读者测试）**；主文档 `proposal-decision-coscientist.md`；锚编码 `anchors/gulei-2015-0406.factors.yaml`。 |

## Reference (framework-level)

- `framework/knowledge/paper-exemplars-2026-07-08.md` — **质量标尺库**：7 exemplar（E1 TreeReview/E2 LLM Swarms/E3 AsyncThink/E4 Scaling/E5 ToT/E6 NPS DMO/E7 NPS RIP）+ 7-criterion bar B1-B7 + 3 结构模板。任何方向评价必须引此文件。

## Archived (`archive/` — superseded, kept for audit trail)

22 docs forming the verdict cycle 2026-07-03 → 2026-07-08. **Do not cite as current.** Key ones:
- `top-journal-{verdict,readiness,rp-investigate}-2026-07-05*.md` — verdict #1-3, superseded
- `rethink-2026-07-06-zh.md` — verdict #4 KILL, partially superseded
- `top-journal-{kill-falsification,opportunity-reality-check}-2026-07-06.md` — verdict #9/#10, superseded by per-paper & paper-directions
- `per-paper-top-journal-2026-07-08.md` — per-paper verdict, superseded by paper-directions-vs-exemplar-bar
- `cross-project-roi-2026-07-06.md` — ROI 矩阵, superseded
- `p11-inner-monologue-paper-readiness-2026-07-03.md` — P11 readiness (P11 closed)
- `direction-a-{decision-memo,xyz-prior-art-recheck,novelty-depth-check}*.md` — Direction A 已死
- `llm-intelligence-blocker-{analysis,verdict}*.md` — 被 optimization-plan 收编
- `orchestrated-progress-assessment-2026-07-05*.md` — 被 meta-uncertainty 覆盖
- `{first-principles-top-journal-directions,post-gate-and-qlib-assessment}-2026-07-05*.md` — 1-off
- `{high-quality-paper-direction-research,toutiao-article-*,toutiao-harness-evolution}-2026-07-08.md` — 与 karpathy-loop-harness 重叠

## Why no docs were deleted (provenance rule)

Per `docs/portfolio/FRAMEWORK-RULES.md` R7 (cite-restoration), archived docs remain findable. The verdict chain itself is evidence of the LLM-on-LLM loop problem documented in `meta-uncertainty-and-blindspot-2026-07-07.md` — deleting it would erase the diagnosis's own proof.