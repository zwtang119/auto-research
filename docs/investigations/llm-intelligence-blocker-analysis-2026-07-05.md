# Investigation: Are the Blockers Caused by Insufficient LLM Intelligence?

Date: 2026-07-05
Method: rp-investigate-cli + falsification (both directions)

## Summary
<!-- Filled after synthesis. -->

## Symptoms (User Question)
- 当前所有卡点（顶刊冲不到、joint methods review median 4.0、G2 n=6 underpowered、G3 只有 2 条 settlement、P11 26 轮 plateau、P1+P2 fold、reviewer 噪声）是否源于使用的 LLM 智力不足？
- 当前模型：DeepSeek-V4 / Kimi-K2.5 / Qwen3.5-122B / MiniMax-M3 / gpt-oss-120b / opus:max（全部中端，无 GPT-5 / Claude-Opus-4 / Gemini-3-Pro）
- 换更高级模型能否解锁？

## Hypotheses (4-layer decomposition)

| # | Hypothesis | Test |
|---|---|---|
| H1 Reviewer intelligence | 5-persona review median=4.0 是弱 reviewer 产物（中端模型看不出方法论价值），换 frontier model 重审会翻身 | 看 review_round_1.md 的 binding weaknesses 是 concrete technical critiques 还是智力不足的误判 |
| H2 Worker intelligence | DeepSeek 199/750 parse 失败、gpt-oss 4/10 parse 失败、G2 only n=6 paired——更聪明模型会产出更干净更完整的证据 | 看 parse 失败模式 + 证据稀疏是否源于模型能力 |
| H3 Orchestration intelligence | path-selection oscillation（P12→P1+P2→joint→P11 fallback）——更聪明编排模型能避免 | 看每次 pivot 的 rationale 是模型误判还是真实 review 信号驱动 |
| H4 Structural blockers | cds4worldcup 仅 2 条 settlement、P8 无 predicted_p、场景只有 Gulei+commercial_space、无 human inter-rater | 任何模型都解决不了？ |

## Background / Prior Research

### Verified current state (from prior turn, still valid 2026-07-05 evening)
- Reviewer models: P12/P1+P2/P8/P7/G1 全部用同一组 5 个 paratera 中端模型，joint 用 6 个（+ minimaxi MiniMax-M3）
- Parse failures: P11 A2_C DeepSeek 199/750 (26.5%)；G2 2nd judge gpt-oss 4/10 (40%)
- G1 review: R1=4.0, R3=4.0 < 5.5 gate；median=4.5
- Joint methods: 6-persona median=4.0 < 4.5 fallback
- P11: 26-round plateau median 5.84-6.60

### What's NOT in prior 6 docs
前 6 份调研都把 "frontier baseline" 列为"非 token-bounded 的结构性缺口"，但**没有**任何一份问过：**reviewer 智力本身是否是瓶颈**。这是本调查的 novelty angle。

## Investigator Findings
<!-- Pair appends here. -->

## Investigation Log

### Phase 0 - Workspace Verification
**Hypothesis:** window 3 仍是 auto-research workspace.
**Findings:** rp-cli windows → window 3 workspace auto-research confirmed.
**Conclusion:** Confirmed.

## Root Cause
<!-- Filled after synthesis. -->

## Recommendations
<!-- Filled after synthesis. -->
