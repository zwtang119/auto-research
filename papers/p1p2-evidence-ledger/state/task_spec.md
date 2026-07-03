# P1+P2 Evidence Ledger — Task Spec

> Created: 2026-07-03  
> Priority: high-ceiling mainline paper candidate  
> Anchor: roadmap §6 (`docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md`)  
> Schema: `evidence_ledger_entry` (`../../../framework/schemas/data-contracts.md` §8)  
> Pitfalls: PIT-201..PIT-208 (`../../../framework/schemas/experiment-pitfalls.md` §3)

## 1. Goal

Specify, prototype, and validate an **evidence ledger** that converts
agent decisions in emergency-response scenarios into structured,
auditable, and settleable claims. Each claim must expose its
supporting evidence, contradicting evidence, missing prerequisites,
source independence, freshness, authority, applicability, and a
machine-checkable settlement rule.

## 2. Core Research Question

> In disaster-response multi-agent decision making, can a structured
> evidence ledger connect RAG retrieval, multi-source signal fusion,
> factor extraction and external settlement into a verifiable decision
> substrate — replacing free-text reasoning traces as the primary
> substrate for downstream evaluation?

## 3. Paper Framing

- Target venue: NeurIPS / ICML / ICLR (workshop or main track depending on evidence strength).
- Working title: *Evidence-Structured Agent Decision Making for Emergency Response*.
- Chinese title: *面向应急响应的证据结构化 Agent 决策*.
- Contribution shape (anti-PIT-401 / anti-thinning):
  1. A 14-field `evidence_ledger_entry` schema with six validator-enforced invariants.
  2. A 2-week pilot showing directional improvement on a Gulei-class scenario.
  3. A settlement bridge to prediction-market / Polymarket outcomes with Brier / Log Loss.

## 4. Milestones

| # | Milestone | Deliverable | Auto-verifiable |
|---|-----------|-------------|----------------|
| M1 | Schema + 10 handcrafted entries | `experiments/ledger/pilot_10.jsonl`, `wiki/concepts/evidence-ledger-schema.md` | schema validates (6 invariants); n == 10 |
| M2 | Gulei / Polymarket settlement mapping | `experiments/ledger/settlement_mapping.md` | ≥ 30 claims have `settleable: true` |
| M3 | Pilot effect-size estimate | `experiments/pilot_power.md` | effect size recorded; planned N documented |
| M4 | Baseline vs evidence-ledger comparison design | `experiments/baseline_design.md` | control arm + treatment arm + pre-registered metrics |
| M5 | Pilot run (small N) | `experiments/ledger/pilot_run.jsonl`, `experiments/belief_update_stats.json` | confidence_delta_distribution variance ≠ 0; no PIT-202/203 hit |
| M6 | Evidence coverage / conflict audit | `experiments/coverage_audit.md` | every entry has `contradicting_evidence` OR `missing_prerequisites` |
| M7 | Settleability audit | `experiments/settleability_audit.json` | `un_settleable_ratio ≤ 0.4` |
| M8 | Paper outline (G3 structural gate) | `paper/outline.md` | abstract → method → results → limitations |
| M9 | Five-persona review (G5) | `paper/review_round_1.md` | R1..R5 persona scores; use ≥2 distinct reviewer models when available; median ≥ 6.5 to continue |
| M10 | Go/no-go decision (Day 12-14) | `state/decisions/2026-07-17-go-no-go.md` | explicit; `stale_count` recorded |

## 5. Invariants (one line each; full table in `state/io_spec.md` §3)

1. **PIT-201**: not both `contradicting_evidence=[]` and `missing_prerequisites=[]`.
2. **PIT-202**: `factor_type: authority` ⇒ `source_independence ≥ 2`.
3. **PIT-203**: `freshness_ratio = age / freshness_window`; `> 1.0` ⇒ `stale: true`.
4. **PIT-204**: `settleable: true` ⇒ non-empty, machine-checkable `settlement_rule`.
5. **PIT-205**: `confidence_after ≠ confidence_before` on at least 80% of entries.
6. **PIT-206**: `audit_trace` is an array of objects with `tool` and a `*_sha256_prefix`.

## 6. Success Criteria

- Validator passes on all pilot entries; 0 PIT-violations in `experiments/rejected_entries.jsonl`.
- `un_settleable_ratio ≤ 0.4` for ≥ 30 settleable claims (M2).
- Day 14 review median ≥ 6.5; if not, fold into P12 short-paper route.
- At least one external settlement source (Polymarket, Gulei public outcome, or historical) maps onto the claim set.

## 7. Data Sources

| Source | Role | Used by |
|--------|------|---------|
| Gulei 2022 incident report (open-source) | scenario + ground truth | M2, M5 |
| Polymarket / cds4polymarket artifacts | external settlement oracle | M2, M7 |
| P1.1 reasoning traces | **counter-example** (free text is not evidence) | M6 (anti-pattern check) |
| P2.1 signal rows | evidence input adapter | M5 |
| P1.2 Brier/Log Loss pipeline | settlement calibration | M7, M9 |

## 8. Stale Rules

- `stale_count ≥ 2`: pivot a **structural** constraint (e.g., relax
  validator or change scenario); do not retune the prompt.
- `stale_count ≥ 4`: write `state/blocked.md`, freeze automation, and
  hand off to a human review before re-opening.
- Direction diversity: every new attempt must differ from all prior
  `directions_tried` entries on at least one axis (hypothesis, method,
  data source, evaluation metric).

## 9. Quality Gates (paper-writing skill group)

| Gate | Minimum for this mainline |
|------|---------------------------|
| G1 Literature | LSN-style references on factor model, evidence-aware decision making, settlement markets; verified at most every 20 entries (PIT-001) |
| G2 Experiment | Hypothesis, control, statistical test, ≥ 30 cells per claim OR bootstrap CI (PIT-007) |
| G3 Structure | `paper/outline.md` complete with abstract/method/results/limitations |
| G4 Figures | At least one audit-trail table and one coverage-vs-conclusion figure |
| G5 Review | Five reviewer personas; use ≥2 distinct reviewer models when available; first round ≤ 7.0; +1.5 max per round |

## 10. Non-goals

- No universal RAG benchmark claim.
- No leaderboard comparison with LangChain / LlamaIndex.
- No daily human-in-the-loop checkpoints; zero-interaction only
  (PIT-011); escalation path is `state/blocked.md`.
- No edits to P2.1 / P1.2 / P11 internal files; this directory is
  read-only against siblings except for `experiments/ledger/` and
  `state/`.
