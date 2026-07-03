# P1+P2 Evidence Ledger — IO Spec

> Created: 2026-07-03
> Schema: `evidence_ledger_entry` (data-contracts.md §8)
> Pitfalls: PIT-201..PIT-208 (experiment-pitfalls.md §3)
> `exp_id = P1P2`; claim id prefix `C-P1P2-`; factor id prefix `F-P1P2-`.

## 1. Required fields per `evidence_ledger_entry`

`claim_id`, `exp_id`, `factor_id`, `factor_type` (precedent|inhibitor|branch|falsifier|authority), `decision_context`, `supporting_evidence[]`, `contradicting_evidence[]`, `missing_prerequisites[]`, `source_independence` (int ≥ 1), `freshness`, `freshness_window` (ISO-8601 duration), `freshness_ratio`, `authority` (high|med|low), `applicability`, `settlement_rule`, `settleable` (bool), `observed_outcome`, `confidence_before`, `confidence_after`, `audit_trace[]`, `ts_created`.

## 2. Six validator invariants

| id | Rule |
|----|------|
| PIT-201 | not both `contradicting_evidence=[]` and `missing_prerequisites=[]` |
| PIT-202 | `factor_type: authority` ⇒ `source_independence ≥ 2` |
| PIT-203 | `freshness_ratio = age / freshness_window`; `> 1.0` ⇒ `stale: true` |
| PIT-204 | `settleable: true` ⇒ `settlement_rule` non-empty and machine-checkable |
| PIT-205 | `confidence_after ≠ confidence_before` on ≥ 80% of entries |
| PIT-206 | `audit_trace` is an array of `{tool, ts, input_sha256_prefix, output_sha256_prefix, agent}` |

## 3. Validation commands

```bash
# parse
jq . state/findings.jsonl >/dev/null
jq . state/iteration_log.jsonl >/dev/null
jq . state/progress.json >/dev/null

# ledger invariants (MUST be empty)
jq -c 'select(.contradicting_evidence==[] and .missing_prerequisites==[])' experiments/ledger/*.jsonl  # PIT-201
jq -c 'select(.factor_type=="authority" and .source_independence < 2)' experiments/ledger/*.jsonl    # PIT-202
jq -c 'select(.settleable==true and (.settlement_rule==null or .settlement_rule==""))' experiments/ledger/*.jsonl  # PIT-204
jq -c '.audit_trace[]? | select(.tool==null)' experiments/ledger/*.jsonl                            # PIT-206

# heartbeat action restricted (MUST be empty)
jq -c 'select(.action and (.action | inside(["liveness","restart","nudge"]) | not))' logs/heartbeat.jsonl
```

## 4. Output paths

| Path | Content |
|------|---------|
| `experiments/ledger/pilot_10.jsonl` | 10 handcrafted entries (M1) |
| `experiments/ledger/pilot_run.jsonl` | pilot run (M5) |
| `experiments/rejected_entries.jsonl` | entries failing any invariant |
| `experiments/aged_entries.jsonl` | entries with `freshness_ratio > 1.0` |
| `experiments/settleability_audit.json` | `total_factors / un_settleable / un_settleable_ratio` |
| `experiments/belief_update_stats.json` | `confidence_delta_distribution` stats |
| `experiments/settlement_mapping.md` | Gulei/Polymarket → `settlement_rule` (M2) |
| `experiments/pilot_power.md` | effect-size estimate before scaling (M3) |
| `experiments/baseline_design.md` | control vs treatment (M4) |
| `experiments/coverage_audit.md` | evidence coverage + conflict (M6) |

## 5. Cross-references

- `../../../framework/schemas/data-contracts.md` §8 (evidence_ledger_entry).
- `../../../framework/schemas/experiment-pitfalls.md` §3 (P1+P2 traps), §8.3 (pre-flight).
- `state/task_spec.md` §4 milestones, §5 invariants.
- `wiki/concepts/evidence-ledger-schema.md` (concept-level write-up).
- `wiki/decisions/2026-07-03-mainline-configuration.md` (why this config).
