# P11 Inner Monologue → RoleDNA Role Consistency Validation

> **Tier 1 | 零人工 | DeepSeek-V4专属**
> 前提：PolicySim仿真引擎绑定DeepSeek-V4 + RoleDNA驱动Agent角色扮演

## Goal

Validate whether exposing agent inner monologue (character-immersed `<think>` tags) improves role-behavior consistency with assigned RoleDNA, and whether consistent role behavior leads to more realistic emergent group dynamics in emergency simulations.

## Verified Facts vs Previous Claims

> **事实核查 (2026-07-01)**：M1 已完成，脚本已创建。

| 之前声称 | 实际验证 | 影响 |
|---------|---------|------|
| "PolicySim MC Engine 绑定 DeepSeek-V4 + RoleDNA 驱动 Agent" | 已验证 - 使用 api_client.py 调用 DeepSeek-V4 | ✅ |
| "deepseek_v4_rolepaly_instruct control instruction templates 已就绪" | 已验证 - 在 CONTROL_INSTRUCTIONS 中定义 | ✅ |
| "3-mode × 50-run = 150 total runs 可在一周内完成" | 待验证 (M2) | — |
| "LLM Judge auto-scoring 零人工可行性" | 待验证 (M3) | — |

## Core Hypothesis

> H1: Inner-monologue agents show higher RoleDNA fidelity scores than no-think agents.
> H2: Pure-analysis agents show logically cleaner but less-characteristic decisions.
> H3: Higher role consistency in individual agents correlates with more realistic emergent group behavior.

## Why this is academically novel

1. Role consistency is an underexplored evaluation dimension in LLM agent research
2. Inner monologue provides the FIRST direct measurement window into agent "thoughts"
3. Closes the loop with cds-keyperson's Role DNA framework: does 5-dimension gene profiling actually control behavior?
4. Process-level transparency (think tags) + output-level explainability (DecisionTrace) = complete "AI decision transparency" thesis

## Experimental Design

**3 modes × Gulei scenario × 50 MC runs each = 150 total runs**

```
Mode A (baseline): No think tags — current PolicySim default
Mode B (inner_monologue): <think>(角色内心独白)</think> before each decision
Mode C (pure_analysis): <think>纯逻辑分析, no inner monologue</think> before each decision
```

**Control instruction** (appended to first-round user message):
```
Mode B: 【角色沉浸要求】在你的思考过程（<think>标签内）中，请遵守以下规则：...
Mode C: 【思维模式要求】在你的思考过程（<think>标签内）中，请遵守以下规则：...
```

## Evaluation Dimensions

| Dimension | Method | Auto-verifiable |
|-----------|--------|:--:|
| RoleDNA Fidelity (5 dimensions) | LLM Judge scores each agent's behavior against assigned RoleDNA | ✅ |
| Decision Quality (6 metrics) | Same baseline as P1/P2 (伤亡/财产/环境/泡沫/时间/人力) | ✅ |
| Emergent Realism | Multi-Judge: does group interaction resemble real emergency patterns? | ✅ |
| Think-tag Trigger Rate | Regex count of `<think>` tags per agent-round | ✅ |
| Role Consistency-RoleDNA Correlation | Spearman's ρ between fidelity scores and RoleDNA parameters | ✅ |

## Success Criteria

- [ ] Mode B (inner_monologue) RoleDNA fidelity > Mode A (no think) by ≥ 0.5 on 5-point scale (p<0.05)
- [ ] Mode B decision quality non-inferior to Mode A (inner monologue doesn't degrade decisions)
- [ ] Think-tag trigger rate ≥ 85% in Mode B (probabilistic but high)
- [ ] Spearman's ρ between RoleDNA risk_tolerance and agent cautiousness behavior ≥ 0.4

## Milestones

| # | Milestone | Deliverable | Est. | Status |
|---|-----------|-------------|------|--------|
| M1 | Integrate deepseek_v4 inner_monologue instruction into PolicySim | 1 modified prompt template | 1 week | ✅ Completed |
| M2 | Run 3-mode × 50-run experiment (150 total) | 150 simulation logs | 1-2 weeks | 🔄 In Progress |
| M3 | LLM Judge auto-scoring (RoleDNA fidelity + emergent realism) | scores.jsonl | 1 week | ⏳ Pending |
| M4 | Statistical analysis + paper writing + submit | complete LaTeX | 2-3 weeks | ⏳ Pending |

## Quality Gates (paper-writing skill)

| Gate | Description | Required For | Corresponding Milestone | Auto-verifiable |
|------|-------------|-------------|------------------------|:--:|
| Gate 2: Experiment | Clear hypothesis, statistical test (p<0.05), ≥3 trials | Phase 1 exit | M3 (LLM Judge scoring) | ✅ |
| Gate 3: Structure | Compiles, ≤300 lines/file, abstract-conclusion alignment | Phase 2 exit | M4 (paper draft) | ✅ |
| Gate 4: Final Review | Blocking multi-round review, score trajectory tracked | Submission ready | M4 (submit) | ✅ |

## Paper Target

- **Title**: *Inner Monologue as a Window into Multi-Agent Reasoning: Validating Role Consistency in Emergency AI Systems*
- **Venue**: ACL 2027 / EMNLP 2027
- **Merge option**: Combine with P3 (explainability) for "AI Decision Transparency" mega-paper (§11-B of topic5-research-directions.md)

## Data Sources

- PolicySim MC engine (Gulei scenario)
- cds-keyperson Role DNA framework (5-dimension behavior genes)
- deepseek_v4_rolepaly_instruct (control instruction templates)
- No external APIs needed

## Known Limitation

- Effect is probabilistic (not 100% think-tag trigger). This is handled by reporting trigger rate and using non-triggered rounds as natural control group.
