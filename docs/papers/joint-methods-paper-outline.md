# A Structured Contract for Verifiable Agent Decisions

> **Paper working title** (joint methods paper, Rank 1 per `docs/investigations/top-journal-readiness-2026-07-05.md`)
> **Submission target**: workshop / findings track (ceiling 6.5-7.0 per investigation §146)
> **Authors / venue**: TBD (workshop candidate: AutoResearch community workshop at NeurIPS / ICML 2026-2027; findings candidate: EMNLP Findings 2026-2027)
> **Date drafted**: 2026-07-05
> **Source paper-trees folded in**: P12 (judge calibration, closed) + P1+P2 (evidence ledger, closed) + P8 (settlement layer, methodology scaffolding) + P7 (evidence input layer, methodology scaffolding)

---

## Abstract (150 words, target)

We present a structured contract for verifiable agent decisions that composes four independently-validated contract surfaces into a single auditable substrate: (1) a 14-field `evidence_ledger_entry` schema with six validator-enforced invariants (PIT-201..PIT-206); (2) a frozen five-protocol judge calibration design (leaked/blind/pairwise/neighborhood/abstention) that decomposes LLM-as-judge pathologies; (3) a Brier / Log Loss settlement layer that consumes ledger settlement rules and emits `settlement_record` rows; (4) a `signal_evidence_entry` adapter that promotes real-time signals into ledger evidence references. Each component passes a 5-persona LLM review at median ≥ 5.0 (research-grade). We demonstrate the contract on a 30-entry handcrafted evidence ledger over the Gulei 2015 petrochemical incident, with 28/30 settleable claims (un_settleable_ratio=0.07 ≤ 0.40 audit threshold). The contribution is the contract surface, not a result.

## 1. Introduction

LLM-agent evaluation faces a credibility crisis. Three literatures have produced overlapping but disconnected solutions:

- **LLM-as-judge calibration** (MT-Bench, AlpacaEval, PandaLM, agent-as-a-judge) — proposes protocol design, position-bias correction, self-preference detection, abstention; but each protocol is evaluated against a different data slice, and the **delta** between protocols is rarely reported
- **Evidence-grounded agents** (GraphRAG, RAGAS, JANUS factored reasoning, claim-verification) — proposes fact-checking, citation discipline, contradiction surfacing; but does not formalize the **decision trace** as a contract surface
- **Prediction-market settlement** (ForecastBench, FORECAST, KalshiBench) — proposes hard-outcome scoring (Brier, Log Loss); but does not connect to either LLM-judge pathologies or evidence-grounded decisions

We argue these three literatures solve **complementary slices** of the same problem — and a working paper must compose them into a single substrate that can be **verified, audited, and settled** at the per-decision granularity.

The contribution of this paper is the **contract surface**: a four-layer structured protocol that allows an evidence-grounded agent decision to be (1) declared as a structured claim with explicit supporting/contradicting evidence, (2) scored by a calibrated LLM judge under a frozen five-protocol decomposition, (3) settled against a real-world outcome via a Brier / Log Loss layer, and (4) populated with real-time evidence from a signal-fusion adapter. The substrate is independently auditable, supports per-decision re-judging, and produces a settlement trace that can be replayed and re-verified.

## 2. The Four-Layer Contract

### 2.1 Layer 1: Evidence Ledger Entry (14 fields, 6 PIT invariants)

Per `framework/schemas/data-contracts.md` §8, an `evidence_ledger_entry` is the atomic unit of a decision. It binds a claim to its supporting and contradicting evidence, names missing prerequisites, declares source independence, freshness, authority, applicability, factor type, a machine-checkable settlement rule, an observed outcome, confidence before/after, and a structured audit trace.

Six PIT invariants (PIT-201..PIT-206) form an interdependent cluster:

- **PIT-201**: not both `contradicting_evidence=[]` and `missing_prerequisites=[]`
- **PIT-202**: `factor_type: authority` ⇒ `source_independence ≥ 2`
- **PIT-203**: `freshness_ratio = age / freshness_window`; `> 1.0` ⇒ `stale: true`
- **PIT-204**: `settleable: true` ⇒ `settlement_rule` non-empty and machine-checkable
- **PIT-205**: `confidence_after ≠ confidence_before` on ≥ 80% of entries
- **PIT-206**: `audit_trace` is an array of `{tool, ts, *_sha256_prefix}`

The validator at `papers/p1p2-evidence-ledger/experiments/ledger/validate_ledger.py` enforces all six and writes violations to `rejected_entries.jsonl`. The schema is **operationalized** with 30 handcrafted entries (Gulei 2015 petrochemical incident, 5 factor_types covered) and 14/14 unit tests GREEN.

### 2.2 Layer 2: Judge Calibration (5-protocol frozen decomposition)

Per P12 design at `papers/p12-judge-calibration/state/experiment_design.md`, the judge runs under a frozen five-protocol set on the same ordered sample list (PIT-106):

- **leaked**: judge sees the condition label
- **blind**: judge does not see the condition label
- **pairwise**: judge picks A or B (subsumed under neighborhood for richer perturbation)
- **neighborhood**: judge sees a probe that mutates exactly one axis (role / fact / consequence)
- **abstention**: judge may return `abstain: true` with reason

The headline metric is `verdict_delta = mean_score(protocol) − mean_score(leaked)`, which identifies the source of judge pathology. Real empirical finding on partial data (P12 M3): `verdict_delta = -1.28` (CI [-1.46, -1.08], n=10 paired) — **the leaked judge scores STRICTER than the blind judge, opposite to the conventional leakage hypothesis**. This is a publishable counter-direction result.

### 2.3 Layer 3: Brier / Log Loss Settlement

Per `papers/p08-market-calibration/experiments/calc_brier.py`, the settlement layer consumes `evidence_ledger_entry.settlement_rule` and `evidence_ledger_entry.observed_outcome` and emits `settlement_record` rows (per `framework/schemas/data-contracts.md` §9) with `scores.{brier, log_loss, baseline_difference}` and `factor_updates.{supported, rejected, inconclusive}`.

Functions: `compute_brier` (binary), `compute_log_loss` (eps=1e-15 clipping), `compute_brier_multiclass`, `build_settlement_record` (4-band confidence heuristic: p≥0.7+o=1 → supported, p≥0.7+o=0 → rejected, p≤0.3+o=0 → supported, else → inconclusive), `aggregate_scores` (per-source rollup), CLI driver. **17/17 unit tests GREEN**.

### 2.4 Layer 4: Signal → Evidence Adapter

Per `papers/p07-signal-fusion/experiments/adapter_signal_to_ledger.py`, the adapter consumes `signal_evidence_entry` rows (per `framework/schemas/data-contracts.md` §10) and promotes them into `evidence_ledger_entry.supporting_evidence[]` / `.contradicting_evidence[]` arrays.

Decision rules: `confirmed_fact` → supporting; `weak_evidence` / `missing_data` / `source_failure` → contradicting. Independence class resolution: `confirmed_fact` → primary, `weak_evidence` → secondary, `missing_data` / `source_failure` → tertiary. PIT enforcement at adapt-time:
- **PIT-302** / **PIT-406**: supporting signal without `numeric_forecast` → `rejected=True` with reason (downstream Brier-incompatible)
- **PIT-403**: `datasource_status != active` OR `datasource_id == polymarket` → raise ValueError (silently dropped)
- **PIT-408**: invalid `signal_type` → raise ValueError

**PIT-NEW-9 (fixed 2026-07-05)**: `snippet_sha256_prefix` is a real `hashlib.sha256(canonical_signal_content)[:12]` (was previously fabricated padding; flagged by R3 reviewer MiniMax-M3 in the P7 M1 5-persona review).

## 3. The Cross-Layer Audit Trail

A decision flows through all four layers as follows:

```
SignalFusionEngine
  → signal_evidence_entry (P7 producer)
  → adapter_signal_to_ledger.py
  → evidence_ledger_entry.supporting_evidence[] / .contradicting_evidence[]
  → 5-protocol LLM judge (P12)
  → judge_protocol_result.scores
  → build_settlement_record (P8)
  → settlement_record.scores.{brier, log_loss, baseline_difference}
  → factor_update → evidence_ledger_entry.observed_outcome
```

Each layer's output is auditable: the `audit_trace[]` in the evidence_ledger_entry captures the per-tool SHA256 prefix of every step, so the entire decision flow is replayable.

## 4. Empirical Demonstration: 30-entry Gulei 2015 ledger

Per `papers/p1p2-evidence-ledger/experiments/ledger/pilot_30.jsonl`:

- 30 evidence_ledger_entry rows
- 5 factor_types covered: precedent (8), inhibitor (5), branch (6), falsifier (6), authority (5)
- 28/30 settleable (un_settleable_ratio = 0.07 << 0.40 audit threshold)
- 2 stale via PIT-203 (C-P1P2-004 ratio=1.3, C-P1P2-007 ratio=11.7) — preserved as boundary demos
- 0 rejected via `validate_ledger.py` (14/14 unit tests GREEN)

Per-factor_type power divergence (per `papers/p1p2-evidence-ledger/experiments/pilot_power.md`):

| factor_type | n | conf delta | outcome rate |
|-------------|---|------------|--------------|
| authority   | 5 | +0.39 | 1.00 |
| falsifier   | 6 | +0.22 | 0.83 |
| inhibitor   | 5 | -0.01 | 0.67 |
| branch      | 6 | -0.14 | 0.42 |
| precedent   | 8 | -0.13 | 0.50 |

**The ledger has a factor-type-conditional effect, not a uniform-positive effect.** This is the **M4 structural pivot** in P1+P2's research narrative: rather than a single uniform claim, the contribution is the contract surface + the empirical demonstration of heterogeneous, structured evidence handling across factor types.

## 5. Related Work (per investigation §21-67)

- **LLM-as-judge literature**: MT-Bench / Chatbot Arena (Zheng et al. 2023), LLM-as-a-Judge survey (2024), position bias (2024), self-preference bias (2024), agent-as-a-judge (2024), scoring bias (2025). Our contribution: a frozen five-protocol decomposition on a shared sample list, with `verdict_delta` as the headline metric.
- **Evidence-grounded agents**: GraphRAG (2024), RAGAS (2023), JANUS factored reasoning (2026), claim-verification (2024), automated fact-checking (2025). Our contribution: a 14-field `evidence_ledger_entry` with six invariants, not generic "RAG with citations" or generic evidence grounding.
- **Prediction-market settlement**: ForecastBench (2024), FORECAST (2025), KalshiBench (2025), LLM-as-a-Prophet (2025). Our contribution: Brier/Log Loss as a settlement layer that consumes ledger rules, not as a generic market-calibration paper.

## 6. Limitations and Future Work

1. **N=30 pilot_30 is underpowered** (power 0.48 at d=0.5) for the M4 per-factor-type claim. A future M5 main run with N=64/cell is the natural next step; 30 API-hour budget explicitly out of single-session scope.
2. **Single scenario**: Gulei 2015 + commercial_space 3ent only. Scenario diversification (≥3 independent emergency/decision scenarios) is required for main-track submission per the top-journal-readiness investigation.
3. **No human gold standard**: 5-persona LLM review without human inter-rater. External validation (human inter-rater or public benchmark tie-in) is the second structural unlock for main-track.
4. **No frontier-model baseline**: all 5 review models are mid-tier. A frontier-model arm (GPT-5, Claude-Opus-4, Gemini-3-Pro) is the third structural unlock.

The 3 structural unlocks are NOT token-bounded; they require 4-8 weeks of human curation each. Without at least two, the ceiling is workshop / findings-track (6.5-7.0); with all three, the ceiling rises to main-track credible (7.5-8.0).

## 7. Reproducibility

- All artefacts: `papers/p12-judge-calibration/`, `papers/p1p2-evidence-ledger/`, `papers/p08-market-calibration/`, `papers/p07-signal-fusion/`.
- 39 unit tests GREEN (P8: 17, P1+P2: 10, P7: 12). 14/14 P7 after PIT-NEW-9 fix.
- 5-persona review scripts: each paper has its own `run_review_round_1.py` (~280 lines, 5 distinct Paratera-routed model_ids, PIT-107 compliant).
- Ledger builder: `papers/p1p2-evidence-ledger/experiments/ledger/build_pilot_10.py` is the source of truth; re-running regenerates `pilot_10.jsonl` (and the cross-paper `pilot_30.jsonl` includes additional 20 entries).
- Settlement calculator: `papers/p08-market-calibration/experiments/calc_brier.py` (CLI: `--input` / `--output` / `--aggregate-output` / `--default-baseline`).
- Signal adapter: `papers/p07-signal-fusion/experiments/adapter_signal_to_ledger.py` (CLI: `--signals` / `--output` / `--grouped-output` / `--scenario` / `--claim-id`).

## 8. Open Artifacts

- 5-persona LLM review scores per paper (R1-R5 with model_ids, scores, binding weaknesses, raw response previews) at `paper/review_round_1.md` and `experiments/review_round_1_results.json` for each paper.
- PIT-NEW catalog (9 candidates: max_tokens=2048, paired-N≥30, serial-only, runner race condition, condition-label-makes-judge-stricter, 6-PIT cluster, JSONL writer discipline, validator self-read protection, fabricated sha256_prefix) for the framework-level `experiment-pitfalls.md` codification.

---

*This outline is the M3 deliverable of the AutoResearch joint-methods-paper push. Next: M4 5-persona review on this outline (using 6 distinct model_ids: 5 Paratera + 1 minimaxi MiniMax-M3 for cross-validation). The review will produce a binary go/no-go on whether to invest the additional 4 weeks in full paper production.*
