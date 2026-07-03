# Data Contracts — Unified IO Schemas

> Created: 2026-07-03
> Scope: shared JSON shapes for P12, P1+P2 evidence ledger, P1.2
> settlement, P2.1 evidence input. Pair with `experiment-pitfalls.md`
> (the matching trap ids are noted in each section).

## 1. Experiment IDs

| exp_id | directory | role | primary IO dir |
|--------|-----------|------|----------------|
| P12 | `papers/p12-judge-calibration/` | judge calibration | `experiments/` |
| P1P2 | `papers/p1p2-evidence-ledger/` (new) | evidence ledger mainline | `experiments/ledger/` |
| P12E | `papers/p08-market-calibration/` | settlement / calibration | `experiments/` |
| P12P | `papers/p07-signal-fusion/` | evidence input layer | `experiments/` |

`exp_id` is required in every schema below. Timestamps are ISO-8601
UTC. Numbers in `[0, 1]` unless `unit` says otherwise. Enums are
lowercase snake_case.

## 2. Naming conventions

| object | pattern | example |
|--------|---------|---------|
| sample id | `<exp_id>-<NNN>` | `P12-017` |
| factor id | `F-<exp_id>-<NNN>` | `F-P1P2-001` |
| claim id | `C-<exp_id>-<NNN>` | `C-P1P2-007` |
| protocol run id | `R-<exp_id>-<protocol>-<NNN>` | `R-P12-blind-002` |
| finding id | `FID-<yyyymmdd>-<NNN>` | `FID-20260703-004` |
| iteration id | `IT-<yyyymmdd>-<NNN>` | `IT-20260703-002` |
| file name | `snake_case.json` or `.jsonl`; dates as `YYYY-MM-DD` | `leakage_reproduction.json` |

## 3. `state/findings.jsonl` (one JSON object per line)

Required: `ts`, `exp_id`, `level`, `event`, `detail`, `verified`.

```json
{"ts": "2026-07-03T08:14:22Z", "exp_id": "P12",
 "level": "info|warn|error|decision", "event": "finding|abort|gate_pass",
 "detail": "one-line statement", "verified": true,
 "verified_by": "fingerprint or path",
 "pitfall_id": "PIT-101",
 "source_path": "experiments/leakage_reproduction.json",
 "mitigation": "stripped label, re-ran blind protocol"}
```

## 4. `state/iteration_log.jsonl` (one row per iteration)

```json
{"ts": "2026-07-03T08:30:00Z", "exp_id": "P12",
 "iteration_id": "IT-20260703-002", "iteration": 2, "stale_count": 0,
 "milestone": "M3", "deliverable": "experiments/pairwise_blind_results.json",
 "preflight_pass": true, "preflight_failed_ids": [],
 "unresolved_weakness": "R2 theorist: settlement rule not stated",
 "review_scores": {"R1": 6.0, "R2": 5.5, "R3": 6.5, "R4": 6.0, "R5": 5.5},
 "review_median": 6.0, "pitfall_ids_hit": ["PIT-106"]}
```

`unresolved_weakness` and `review_median` are required on review
rounds (PIT-002).

## 5. `state/progress.json`

```json
{"exp_id": "P12", "iteration": 2, "status": "running",
 "stale_count": 0, "last_seen": "2026-07-03T08:30:00Z",
 "current_milestone": "M3", "completed_milestones": ["M1", "M2"],
 "blocked": false, "block_reason": null}
```

## 6. `experiments/sample_manifest.jsonl` (P12)

Every `sample_id` must resolve to a real file with a recorded hash
prefix (PIT-005, PIT-105).

```json
{"sample_id": "P12-017", "exp_id": "P12",
 "source_project": "legacy/p11-closed-v5-minimax-m3",
 "source_path": "experiments/mc-2026-07-01-inner-monologue/raw-data/inner_monologue/ISPACE/sample_42.json",
 "source_sha256_prefix": "a3f1c0b9e2d4",
 "original_condition": "inner_monologue", "condition_visible_to_judge": false,
 "ambiguous": true, "ground_truth_correctness": false,
 "ts_imported": "2026-07-03T07:55:00Z"}
```

## 7. `judge_protocol_result` (P12)

One record per `(sample_id, protocol)`. All five protocols must
share `sample_ids_ordered` (PIT-106).

```json
{"record_id": "R-P12-blind-002", "exp_id": "P12",
 "sample_id": "P12-017", "protocol": "leaked|blind|pairwise|neighborhood|abstention",
 "judge_id": "judge-claude-opus-4", "awareness": "blind|leaked|pairwise",
 "score": 0.42, "score_band": "low|med|high",
 "abstain": false, "abstain_reason": null,
 "paraphrase_id": null, "ground_truth_correctness": false,
 "consistency_on_wrong": 0.18, "axis": "role|fact|consequence|null",
 "ts": "2026-07-03T08:10:00Z"}
```

Required when `abstain: true`: `abstain_reason` (PIT-103). Required
when `protocol: neighborhood`: `axis` (PIT-104).

## 8. `evidence_ledger_entry` (P1+P2)

Originates in roadmap §6.3; adds audit-trail and freshness
requirements (PIT-201, PIT-202, PIT-203, PIT-204, PIT-205, PIT-206).

```json
{"claim_id": "C-P1P2-007", "exp_id": "P1P2",
 "factor_id": "F-P1P2-001", "factor_type": "precedent|inhibitor|branch|falsifier|authority",
 "decision_context": "Gulei evacuation: shelter-in-place vs relocate",
 "supporting_evidence": [{"source_id": "S-001", "snippet_sha256_prefix": "9b1c...",
   "observed_at": "2026-06-28T10:00:00Z", "independence_class": "primary|secondary|tertiary"}],
 "contradicting_evidence": [{"source_id": "S-014", "snippet_sha256_prefix": "7e0a...",
   "observed_at": "2026-06-29T11:00:00Z", "independence_class": "primary"}],
 "missing_prerequisites": [],
 "source_independence": 2,
 "freshness": "2026-06-29T11:00:00Z", "freshness_window": "P1D", "freshness_ratio": 4.0,
 "authority": "high|med|low", "applicability": "Gulei-class petrochemical event within 24h",
 "settlement_rule": "if observed wind shift > 30 deg within 6h then factor_confirmed=true",
 "settleable": true,
 "observed_outcome": {"label": "confirmed|refuted|partial|unobserved",
                      "ts": "2026-06-30T00:00:00Z", "value": 1},
 "confidence_before": 0.55, "confidence_after": 0.78,
 "audit_trace": [{"tool": "search|judge|extract|hash", "ts": "2026-07-03T08:00:00Z",
   "input_sha256_prefix": "ab12...", "output_sha256_prefix": "cd34...", "agent": "worker-1"}],
 "ts_created": "2026-07-03T08:05:00Z"}
```

Invariants (validator enforces):
- `factor_type: authority` ⇒ `source_independence >= 2` (PIT-202).
- not both `contradicting_evidence=[]` and `missing_prerequisites=[]`
  (PIT-201).
- `freshness_ratio = age / freshness_window`; `> 1.0` ⇒ `stale: true`
  (PIT-203).
- `settleable: true` ⇒ `settlement_rule` non-empty and machine-checkable
  (PIT-204).
- `audit_trace` is an array of objects with `tool` and at least one
  `*_sha256_prefix` (PIT-206).
- `source_type: free_text_trace` requires `trace_grounded: true` and
  `grounding_source_id` (PIT-207).

## 9. `settlement_record` (P1.2)

Brier/Log Loss input. Headline Brier accepts `source: numeric` or
`source: anchor` only; `text-extract` is reported separately
(PIT-302, PIT-305, PIT-306, PIT-307).

```json
{"record_id": "SR-P12E-017", "exp_id": "P12E",
 "event_id": "PMKT-2026-WTI-Q3",
 "factor_id": "F-P1P2-001", "claim_id": "C-P1P2-007",
 "predicted_p": 0.65, "observed_outcome": 1,
 "source": "numeric|anchor|text-extract",
 "judge_id": "judge-m3-gold-L", "gold_set_version": "v3-frozen-2026-07-01",
 "brier_component": 0.1225, "log_loss_component": 0.4308,
 "ts_predicted": "2026-07-01T00:00:00Z", "ts_observed": "2026-07-03T00:00:00Z",
 "baseline_sha256_prefix": "9f00..."}
```

`baseline_sha256_prefix` is required for any before/after writeback
comparison (PIT-306).

## 10. `signal_evidence_entry` (P2.1)

Restrict to the 4-value enum; `datasource_status: active` (PIT-403, PIT-408).

```json
{"signal_id": "SIG-P12P-042", "exp_id": "P12P",
 "datasource_id": "geopolitics|finance|macro|energy|sanctions|news|aviation|academic|wikipedia|weather|sports|...",
 "datasource_status": "active",
 "signal_type": "confirmed_fact|weak_evidence|missing_data|source_failure",
 "lens_weight": 0.18, "recency_weight": 0.92,
 "observed_at": "2026-07-02T12:00:00Z",
 "scenario": "base|downside|upside", "scenario_text": "OPEC+ holds; refinery margins compress",
 "numeric_forecast": null, "ts_ingested": "2026-07-03T08:00:00Z"}
```

`numeric_forecast` is required when the downstream consumer is the
P1.2 Brier aggregate (PIT-302, PIT-406). If absent, downstream treats
the row as `un_settleable: true`.

## 11. Log lines

`logs/work.jsonl`, `logs/orchestrator.jsonl`, `logs/heartbeat.jsonl`
share:

```json
{"ts": "2026-07-03T08:00:00Z", "source": "work|orchestrator|heartbeat",
 "level": "info|warn|error|decision|question", "event": "short_verb",
 "detail": "human-readable", "exp_id": "P12",
 "pitfall_id": null, "iteration_id": "IT-20260703-002"}
```

`heartbeat.jsonl` cross-task entries may only carry
`action: liveness|restart|nudge` (PIT-004). `level: question` is
forbidden outside the P1.2 M2 checkpoint (PIT-011, PIT-303).

## 12. Validation commands

Run from the experiment directory. Each command exits non-zero on a
contract violation.

```bash
# 12.1 — JSON / JSONL parse
jq . state/findings.jsonl >/dev/null
jq . state/iteration_log.jsonl >/dev/null
jq . state/progress.json >/dev/null

# 12.2 — required fields per findings row
jq -c 'select(.ts and .exp_id and .level and .event and .verified != null)' \
  state/findings.jsonl | wc -l   # must equal wc -l state/findings.jsonl

# 12.3 — sample manifest: every row has path + hash prefix
jq -c 'select(.source_path and .source_sha256_prefix)' \
  experiments/sample_manifest.jsonl | wc -l

# 12.4 — judge protocols share sample_ids_ordered
jq -r '.sample_id' experiments/*_results.json | sort | uniq -c | awk '$1==4'

# 12.5 — ledger: not both contradicting & missing empty (MUST be empty)
jq -c 'select(.contradicting_evidence==[] and .missing_prerequisites==[])' \
  experiments/ledger/*.jsonl

# 12.6 — ledger: authority requires source_independence >= 2 (MUST be empty)
jq -c 'select(.factor_type=="authority" and .source_independence < 2)' \
  experiments/ledger/*.jsonl

# 12.7 — P1.2: headline Brier inputs are numeric or anchor
jq -c 'select(.source=="text-extract")' experiments/brier_inputs.jsonl | wc -l

# 12.8 — P2.1: signal_type in enum and datasource_status == active (MUST be empty)
jq -c 'select((.signal_type | inside(["confirmed_fact","weak_evidence",
   "missing_data","source_failure"]) | not) or .datasource_status != "active")' \
  experiments/signals/*.jsonl

# 12.9 — heartbeat: action field restricted (MUST be empty)
jq -c 'select(.action and (.action | inside(["liveness","restart","nudge"]) | not))' \
  logs/heartbeat.jsonl
```

## 13. Cross-references

- `experiment-pitfalls.md` — trap ids cited above.
- Roadmap §6.3, settlement rules, evidence input → `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md`.
- Upstream state-file protocol → `victorchen96.github.io/auto_research/framework.html`.
- Portfolio milestones and gates → `state/task_spec.md` (root).
