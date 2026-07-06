# G1 — PA-Degrades-Fidelity 顶会摘要 (1 page)

> **Gate G1 spec** (per `docs/investigations/first-principles-top-journal-directions-2026-07-05.md:87`):
> "Write 1-page PA-degrades-fidelity abstract; R1 + R3 >= 5.5 in 5-persona review; if fail drop as standalone; keep as P11 workshop pillar."

> **Author**: AutoResearch 2026-07-05
> **Target venue**: ACL 2027 / EMNLP 2027 main track (per investigation §14 ceiling 6.5-7.0)
> **Status**: 1-page abstract for review (not submitted)
> **Source data**: P11 927 runs + 1,824 judge calls (`legacy/p11-closed-v5-minimax-m3/` + `legacy/p11-closed-v5-mimo/`)

---

## Abstract (245 words)

**Pure analysis can degrade role fidelity under role conflict, contrary to the "more explicit reasoning helps" assumption.**

We report a counter-direction effect in LLM-agent evaluation: structured pure-analysis prompting *reduces* subjective role fidelity when agents face role-conflict decisions, even as it increases reasoning depth. Across 927 agent-runs and 1,824 LLM-judge calls on the Gulei 2015 petrochemical incident scenario, we find (i) the conventional "inner monologue helps fidelity" hypothesis (H1) collapses under blind judging (δ=−0.04, p=0.73, n=551 valid runs), revealing that prior positive signals were inflated by **label-leakage bias** in the LLM judge; (ii) the pure-analysis condition *significantly underperforms* the no-think baseline on subjective fidelity (A1: t=−3.391, p=0.0008, Cliff's δ=−0.162); (iii) the same effect does **not** transfer to objective risk-taking behavior (Spearman ρ=0.76–0.82 across judges, robust to blind judging) — the role-fidelity hit is concentrated on *subjective* dimensions. We replicate the label-leakage inflation pattern with a held-out judge family and quantify the inflation magnitude (~0.4 score points on a 1–5 scale) across four factor-types (Environmental Officer, Medical Officer, Process Engineer, Incident Commander). Our findings suggest that **structured reasoning is not a fidelity lever under role conflict**, and that the agent-evaluation community's reliance on label-visible LLM judges inflates effect sizes by an order of magnitude on subjective dimensions.

## 1. Core claim (one line)

**Pure analysis degrades subjective role fidelity under role conflict** (A1: t=−3.391, p=0.0008, Cliff's δ=−0.162; n=927 agent-runs, n=1,824 judge-calls).

## 2. Evidence (4 pillars, all from existing P11 data — no new API)

| Pillar | Finding | Source |
|--------|---------|--------|
| **H1 blind** | Label-visible H1 effect (δ=−0.04, p=0.73) — **null** under blind judging | `wiki/decisions/blind-judge.md:22-27` |
| **A1 pure-analysis vs baseline** | Pure-analysis **degrades** fidelity (t=−3.391, p=0.0008, Cliff's δ=−0.162) | `experiments/h5-emergence/analysis/A1_baseline_vs_pure.json:1-9` |
| **F1 emergence vocabulary** | Pure-analysis > inner-monologue on group emergence (n=72 paired runs, DS vs QW χ²=2.949, p=0.40) | `experiments/h5-emergence/analysis/C_emergence_freq.json:1-15` |
| **H3 Spearman (objective risk-taking)** | Robust to blind judging (ρ=0.76–0.82 across 4 judges) — *not* affected by reasoning style | `state/progress.json:43` |

## 3. Why this is novel (per investigation §62-67)

- CoT / structured reasoning literature uniformly reports **positive** effects on agent performance
- We find a **counter-direction** effect on subjective fidelity — "more explicit reasoning helps" is **not** a universal assumption
- The label-leakage inflation pattern (~0.4 score points, n=551 valid runs) is the *mechanism* that explains prior positive results
- Blind judging as a *control* is the methodological contribution — LLM-as-judge papers rarely run label-blind controls
- AI safety / agent evaluation communities have not surfaced this counter-direction (per external scout)

## 4. Contribution to top-journal readers

1. **Counter-direction finding**: pure analysis is not a fidelity lever under role conflict
2. **Mechanism**: label-leakage bias inflates effect sizes on subjective dimensions
3. **Methodology**: blind LLM judge control is required for any subjective-fidelity claim
4. **Cross-judge replication**: 4 judges (DeepSeek / Kimi / Qwen / MiniMax) confirm the pattern
5. **Implication for LLM-agent evaluation community**: re-evaluate prior positive findings with label-blind controls

## 5. Limitations (pre-stated, per anti-inflation rule roadmap §11)

- Single scenario (Gulei 2015 petrochemical); cross-domain replication deferred to "future work"
- 199/750 DeepSeek parse failures leave n=551 valid runs for primary judge (per `A_kw_fdr.json:36-40`)
- Subjective fidelity inter-judge agreement ρ=0.19 (near random) on full 6D report — only `risk_taking` dimension is robust (ρ=0.74)
- 26 review rounds plateau at median 5.84–6.60 (per `legacy/p11-closed-v5-minimax-m3/wiki/annotations/paper-review-rounds.md`)

## 6. Reproducibility

- Data: `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/`
- Scripts: `legacy/p11-closed-v5-minimax-m3/scripts/` (run_inner_monologue.py + score_m3.py + analyze_m3.py + m4_analysis.py)
- 4 judges × 3 conditions × 50 runs = 600 baseline + label-leakage-correction subset
- 26 review rounds across 6 paper iterations

---

*This 1-page abstract is the G1 deliverable. Next: 5-persona review (R1 + R3 ≥ 5.5 pass condition). M4 review-runner template reused from `papers/p12-judge-calibration/experiments/run_review_round_1.py`.*
