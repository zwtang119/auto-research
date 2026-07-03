# P12 IO Specification

> Created: 2026-07-03
> Scope: P12 judge-calibration input/output contract
> Pair with `../../../framework/schemas/data-contracts.md` and `../../../framework/schemas/experiment-pitfalls.md`

This document fixes the inputs, outputs, validators and non-goals for
P12. It is the single source of truth that all prompts (`claude-prompt.md`,
`mimo-prompt.md`), state files, and experiment artefacts must obey.

`exp_id` for this directory is **`P12`** (see `data-contracts.md` §1).
All sample ids use the prefix `P12-`. All protocol run ids use
`R-P12-<protocol>-<NNN>`. Timestamps are ISO-8601 UTC.

---

## 1. Inputs

| Field | Source | Required | Pitfall |
|-------|--------|----------|---------|
| `sample_manifest.jsonl` | M1 deliverable | yes | PIT-005, PIT-105 |
| P11 raw sample files | `../legacy/p11-closed-v5-minimax-m3/experiments/...` | yes | PIT-105 |
| P11 prior-judge evidence | `../legacy/p11-closed-v5-minimax-m3/wiki/decisions/blind-judge.md`, `h1-reformulation.md`, `2026-07-03-structural-intelligence-reassessment.md` | yes | PIT-101, PIT-105 |
| Frozen protocol set | this file §3 | yes | PIT-101, PIT-106 |
| Frozen `sample_ids_ordered` list | `experiments/sample_ids_ordered.json` | yes | PIT-106 |
| Gold `ground_truth_correctness` per sample | P11 human label (imported, not invented) | yes | PIT-005 |
| Pre-registration artefact | `state/experiment_design.md` (frozen before run) | yes | PIT-006 |

### 1.1 Sample manifest invariants (PIT-005, PIT-105)

Every row in `experiments/sample_manifest.jsonl` MUST carry:

- `sample_id` matching `^P12-[0-9]{3,}$`
- `source_path` pointing to a real file in the source project
- `source_sha256_prefix` (12-char sha256 prefix of the file at import time)
- `original_condition` (one of `inner_monologue | no_think | pure_analysis`)
- `condition_visible_to_judge: false` for every imported P11 sample

The validator command (run from this directory):

```bash
jq -c 'select(.source_path and .source_sha256_prefix and .condition_visible_to_judge==false)' \
  experiments/sample_manifest.jsonl | wc -l
# must equal: wc -l < experiments/sample_manifest.jsonl
```

---

## 2. Outputs

| File | Format | Schema | Pitfall |
|------|--------|--------|---------|
| `experiments/sample_manifest.jsonl` | jsonl | `sample_manifest` (data-contracts §6) | PIT-005, PIT-105 |
| `experiments/sample_ids_ordered.json` | json | array of `sample_id` strings | PIT-106 |
| `experiments/leakage_reproduction.json` | json array | `judge_protocol_result` (data-contracts §7) | PIT-101, PIT-106 |
| `experiments/pairwise_blind_results.json` | json array | `judge_protocol_result` (data-contracts §7) | PIT-102, PIT-106 |
| `experiments/neighborhood_probe_schema.json` | json | `axis: role|fact|consequence`, original `sample_id` | PIT-104 |
| `experiments/neighborhood_probe_results.json` | json array | `judge_protocol_result` (data-contracts §7) | PIT-103, PIT-104 |
| `experiments/abstention_results.json` | json array | `judge_protocol_result` (data-contracts §7) | PIT-103 |
| `experiments/calibration_metrics.md` | markdown | per-protocol table + H1/H1c/H3/F1 verdict deltas | PIT-002, PIT-107 |
| `paper/outline.md` | markdown | abstract / method / results / limitations | G3 |
| `paper/review_round_1.md` | markdown | R1..R5 scores, median, unresolved weakness | PIT-002, PIT-107 |

### 2.1 Cross-protocol `sample_ids_ordered` (PIT-106)

All five protocol result files MUST list `sample_ids_ordered` in the
exact same order. The validator:

```bash
jq -r '.sample_ids_ordered | join(",")' experiments/*_results.json | sort -u | wc -l
# must equal 1
```

### 2.2 Required fields per `judge_protocol_result` row (data-contracts §7)

- `record_id` matching `^R-P12-(leaked|blind|pairwise|neighborhood|abstention)-[0-9]{3,}$`
- `sample_id`, `protocol`, `judge_id`, `awareness`, `score`, `score_band`
- `abstain: true` ⇒ `abstain_reason` non-empty (PIT-103, DST-8)
- `protocol: neighborhood` ⇒ `axis` non-null and in `role|fact|consequence` (PIT-104)
- `consistency_on_wrong` numeric in `[0, 1]`
- `ground_truth_correctness` boolean
- `judge_id != "self"` (DST-10, PIT-013)

### 2.3 Calibration metrics table (M6)

`experiments/calibration_metrics.md` MUST contain one row per
`(hypothesis, protocol)` combination where `hypothesis ∈ {H1, H1c, H3, F1}`.
Each row carries:

- `n` (sample count for that cell; ≥ 30 to make a directional claim — PIT-007)
- `mean_score`
- `mean_consistency_on_wrong`
- `abstain_rate`
- `verdict_delta` vs the leaked baseline
- `statistical_test` (or explicit `not_tested: true`)

If any cell has `n < 30`, the table MUST say so in the row footnote
(PIT-007).

---

## 3. Frozen protocol set (PIT-101, PIT-104, PIT-106)

All five protocols share the same `sample_ids_ordered`:

1. **`leaked`** — judge prompt contains the original condition label.
2. **`blind`** — judge prompt has the condition label stripped; `condition_visible_to_judge: false`.
3. **`pairwise`** — judge sees two outputs of the same `sample_id` (paraphrased or model-A vs model-B) and returns a preference; tied to `consistency_on_wrong` (PIT-102).
4. **`neighborhood`** — judge sees a probe that mutates exactly one axis (`role|fact|consequence`) of the original; tied to `axis` field (PIT-104).
5. **`abstention`** — judge may return `abstain: true` with `abstain_reason`; the metric is `abstain_rate` plus the residual score on non-abstained items (PIT-103).

The prompt template for each protocol is recorded in
`wiki/concepts/judge-calibration-protocol.md` and MUST NOT be edited
mid-run (PIT-006, PIT-009).

---

## 4. Pre-registration (`state/experiment_design.md`)

Before any run, `state/experiment_design.md` MUST be written and frozen
(PIT-006). It must contain:

- The hypothesis under test (one of H1, H1c, H3, F1 reframed as a calibration claim).
- The primary metric and its range.
- The pre-registered `n` per cell.
- The frozen `sample_ids_ordered` list (or its generator rule).
- The frozen judge model list.
- The stop condition: which `effect_size` or `delta_score` would constitute evidence.

After the run, this file is read-only. A surprise finding is logged
to `state/findings.jsonl` and becomes a follow-up experiment, not a
re-framing of the original.

---

## 5. Logs

Three log files, one role each (data-contracts §11):

- `logs/work.jsonl` — per-step actions of the worker agent.
- `logs/orchestrator.jsonl` — orchestrator decisions (restart, nudge, escalate).
- `logs/heartbeat.jsonl` — watchdog liveness checks; `action` restricted to
  `liveness | restart | nudge` (PIT-004).

`level: question` is **forbidden** in any log line (PIT-011).
P12 has zero human checkpoints.

---

## 6. Review rounds (PIT-002, PIT-107)

Every `paper/review_round_*.md` file MUST:

- List the five persona scores (R1..R5) and the median.
- Carry an `unresolved_weakness` string.
- List `reviewer_models: [string, ...]` and reject the round if all
  entries are the same model (PIT-107).
- Apply the anti-inflation cap: first round ≤ 7.0, +1.5 max per round.

---

## 7. Validation commands (run from this directory)

```bash
# 7.1 — JSON / JSONL parse
jq . state/findings.jsonl >/dev/null
jq . state/iteration_log.jsonl >/dev/null
jq . state/progress.json >/dev/null
jq . experiments/sample_manifest.jsonl >/dev/null

# 7.2 — sample manifest: every row has path + hash prefix + blind-by-default
jq -c 'select(.source_path and .source_sha256_prefix and .condition_visible_to_judge==false)' \
  experiments/sample_manifest.jsonl | wc -l

# 7.3 — protocols share sample_ids_ordered
jq -r '.sample_ids_ordered | join(",")' experiments/*_results.json | sort -u | wc -l

# 7.4 — abstention rows have non-empty abstain_reason (MUST be empty)
jq -c 'select(.abstain==true and (.abstain_reason==null or .abstain_reason==""))' \
  experiments/*_results.json

# 7.5 — neighborhood rows carry axis (MUST be empty)
jq -c 'select(.protocol=="neighborhood" and (.axis==null or (.axis | inside(["role","fact","consequence"]) | not)))' \
  experiments/*_results.json

# 7.6 — judge_id is never "self" (MUST be empty)
jq -c 'select(.judge_id=="self")' experiments/*_results.json

# 7.7 — heartbeat: action restricted (MUST be empty)
jq -c 'select(.action and (.action | inside(["liveness","restart","nudge"]) | not))' \
  logs/heartbeat.jsonl

# 7.8 — pre-registration exists before any *_results.json
test -f state/experiment_design.md
```

Any non-zero output from the "MUST be empty" commands is a PIT-block;
the iteration is not done until the trap is cleared.

---

## 8. Non-goals

- No new large-scale P11 experiment (task_spec §"Non-goals").
- No universal "best judge" claim — the contribution is the protocol
  set, not a leaderboard.
- No reliance on producer self-confidence; `judge_id` is always a
  distinct agent (PIT-013, DST-10).
- No prompts that ask the user a question during a run (PIT-011).
- No edits to `state/experiment_design.md` after the run starts
  (PIT-006).

---

## 9. Cross-references

- `data-contracts.md` §3 (findings), §4 (iteration log), §5 (progress),
  §6 (sample manifest), §7 (judge protocol result), §11 (logs), §12 (validators).
- `experiment-pitfalls.md` §1 universal traps, §2 P12 traps, §6 prompt
  anti-patterns, §7 data-shape traps, §8.2 P12 pre-flight checklist.
- `state/task_spec.md` — milestones, success criteria, stale rules.
- `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §5 P12 fast
  paper route.
- `wiki/concepts/judge-calibration-protocol.md` — the protocol design.
- `wiki/decisions/2026-07-03-p12-configuration.md` — why this
  configuration was chosen.
