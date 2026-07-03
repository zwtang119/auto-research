# P1.2 — IO Specification (Settlement / Calibration Layer)

> **exp_id**: `P12E`
> **Role in portfolio**: settlement / calibration layer for the P1+P2 evidence-ledger mainline
> **Scope of this file**: every artefact produced or consumed by `papers/p08-market-calibration/` after the 2026-07-03 reconfiguration
> **Source of truth**: `../../../framework/schemas/data-contracts.md` (settlement_record schema, §9); `../../../framework/schemas/experiment-pitfalls.md` (§4 P1.2 traps); `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` (§7 P8 / P1.2 new positioning)

This directory is no longer framed as a standalone "predict-then-verify the agent" experiment. It is the **external settlement layer** for the P1+P2 evidence-ledger project. The headline deliverable is a stream of `settlement_record` rows that the evidence-ledger project can join against `evidence_ledger_entry.observed_outcome`, plus a Brier/Log Loss aggregate per `factor_id`.

The files below define what this directory emits, what it accepts, what it must not do, and where the boundaries live.

## 1. Role and boundary

| Direction | P1.2 (here) does | P1.2 (here) does NOT do |
|-----------|------------------|--------------------------|
| Produces | `settlement_record` rows, Brier/Log Loss aggregates, gold-set audits, writeback before/after snapshots | Discover new factors; extract factor candidates from free-text traces; score agent reasoning quality |
| Consumes | `evidence_ledger_entry.factor_id` from the P1+P2 project; `signal_evidence_entry` from `papers/p07-signal-fusion/` (numeric only); frozen Polymarket event outcomes | Free-text reasoning traces (P11 / P2.1 text scenarios) — these must arrive as numeric `numeric_forecast` or be marked `un_settleable: true` (PIT-302, PIT-012, PIT-406) |
| Coordinates with | P12 judge calibration (provides Gold-H/M/L drift signals); P1+P2 (consumes factor ids) | Acts as the paper's sole contribution narrative — that role belongs to P1+P2 |

## 2. Output schemas (P1.2 emits)

Every output JSONL/JSON file in this directory must parse with `jq .` and conform to one of the shapes below. The contract id is the matching section in `data-contracts.md`.

### 2.1 `experiments/settlement_records.jsonl` — primary output

`settlement_record` per `data-contracts.md §9`. One row per `(factor_id, observed_outcome)` pair.

Required fields: `record_id`, `exp_id` (`P12E`), `event_id`, `factor_id`, `claim_id` (nullable when there is no P1+P2 claim yet), `predicted_p`, `observed_outcome` (0 or 1), `source`, `judge_id`, `gold_set_version`, `brier_component`, `log_loss_component`, `ts_predicted`, `ts_observed`, `baseline_sha256_prefix`.

`source` enum: `numeric | anchor | text-extract`. Headline Brier must use only `numeric` and `anchor` (PIT-302, PIT-012, DST-6). `text-extract` rows are kept in the file but reported separately; they must never enter the paper's headline number.

When a record joins against a P1+P2 ledger entry, the row also carries `claim_id` (or `null` if the settlement preceded the ledger binding). When it does not join, the row stays valid; it is a stand-alone Brier input.

### 2.2 `experiments/brier_inputs.jsonl` — typed feed for the calculator

One row per Brier input. Fields: `record_id`, `predicted_p` (in `[0,1]`), `observed_outcome` (0 or 1), `source`, `event_id`, `factor_id`, `domain`, `ts_predicted`, `ts_observed`. This is the file `calc_brier.py` (M1.5, **not implemented yet**) consumes. Until the calculator exists, this file is the hand-curated input set and is the validation target for §5.1 below.

### 2.3 `experiments/brier_summary.json` — single-file headline

Fields: `n_records`, `n_numeric_or_anchor`, `n_text_extract`, `brier_headline`, `brier_text_extract_only`, `log_loss_headline`, `log_loss_text_extract_only`, `domain_breakdown` (object keyed by domain), `ts_computed`, `code_sha256_prefix`. The two headline numbers (`brier_headline`, `log_loss_headline`) must be computed from `n_numeric_or_anchor` rows only.

### 2.4 `experiments/before_after/{before,after}.json` — writeback snapshot

Fields: `metric` (`brier_headline`), `value`, `n_records`, `gold_set_version`, `snapshot_sha256_prefix`, `ts_taken`. `before.json` is **frozen before** the writeback loop fires; `after.json` is taken after; `after.baseline_sha256_prefix == before.snapshot_sha256_prefix` (PIT-306). Until `calc_brier.py` exists, this file is a placeholder.

### 2.5 `state/calibration_lib_audit.md` — gold-set audit

Fields written into the file: `gold_set_size`, `gold_set_ids`, `judge_drift_test`, `test_limit`, `expansion_plan`. Three anchors detect a constant offset but not distribution shift; if the headline claim is "judge is calibrated", the gold set must expand (PIT-305, DST-15).

### 2.6 `state/implementation_status.md` — design-vs-code table

Fields per component: `component`, `design_lines`, `code_lines`, `tests`, `passing`. Updated on every milestone. PIT-301: do not write paper sentences that say "we have a Factor Ledger" until `design_lines > 0` and `code_lines > 0` and `tests > 0` for that component.

## 3. Input schemas (P1.2 consumes)

### 3.1 From `papers/p1p2-evidence-ledger/experiments/ledger/*.jsonl`

`evidence_ledger_entry` per `data-contracts.md §8`. P1.2 reads:

- `factor_id` (join key)
- `claim_id` (forwarded into `settlement_record.claim_id`)
- `factor_type` (used only for filtering; e.g. `authority` factors are expected to settle less often)
- `settlement_rule` (used as the **machine-checkable** rule that fires when Polymarket outcome lands; if it is non-machine-checkable, P1.2 logs `un_settleable: true` and excludes it from the headline Brier)
- `observed_outcome` (already-observed rows may short-circuit the wait for Polymarket)

Invariants enforced by the ledger are repeated here as a guardrail:

- `factor_type: authority ⇒ source_independence >= 2` (PIT-202)
- not both `contradicting_evidence=[]` and `missing_prerequisites=[]` (PIT-201)
- `freshness_ratio > 1.0 ⇒ stale: true` (PIT-203)

If any joined ledger entry fails any invariant, P1.2 logs `pitfall_hit: PIT-201|202|203` to `state/findings.jsonl` and skips the record rather than silently settling.

### 3.2 From `papers/p07-signal-fusion/experiments/signals/*.jsonl`

`signal_evidence_entry` per `data-contracts.md §10`. P1.2 consumes only:

- `signal_id` (provenance)
- `factor_id` if the signal layer already mapped to a factor (forwarded as `claim_id: null` when absent)
- `numeric_forecast` (in `[0,1]`) — **required** when the downstream consumer is the P1.2 Brier aggregate
- `signal_type` (informational; `confirmed_fact` rows are preferred for the headline Brier; `weak_evidence` and `missing_data` rows enter the file but are tagged `un_settleable: true` in §2.2)
- `datasource_status` — must be `active` (PIT-403)

Text scenarios from P2.1's Forecaster (`base/downside/upside` with no numeric probability) **must not** be reinterpreted as numeric forecasts. They must be marked `un_settleable: true` and excluded from the headline (PIT-302, PIT-406, DST-6).

### 3.3 From Polymarket (read-only)

`event_id`, `predicted_p` (market consensus at `ts_predicted`), `observed_outcome` (1 for YES resolution, 0 for NO). The endpoint is `polymarket.com` Gamma API `/events`. Each pull logs `http_status`, `attempt`, `backoff_ms`, `event_id` to `experiments/event_pull_log.jsonl` (PIT-304). Per-domain cap is **5 events** until retry/backoff is added.

## 4. Single human checkpoint (PIT-303, PIT-011)

M2 (event selection review) is the **only** place this directory engages the user. After M2 the worker must run M3-M9 with zero user questions. Workflow:

1. Worker writes `experiments/event_candidates.json` ranked by the agent's selection criteria (multi-domain coverage, sufficient liquidity, post-resolution status at selection time).
2. Worker writes `state/blocked.md` containing the single line: `M2 complete, awaiting human review of top-5 case study candidates.`
3. Human reviews the candidate list (single checkpoint, non-interactive inside the worker loop).
4. After human resolution, the worker resumes M3+ and must not log any `level: question` event.

Any `level: question` event in `logs/work.jsonl` outside M2 is a PIT-011 / PIT-303 violation.

## 5. Validation commands (run from this directory)

Each command must exit non-zero on a contract violation.

```bash
# 5.1 — primary output parses as JSONL
jq -c . experiments/settlement_records.jsonl >/dev/null

# 5.2 — required fields on every settlement record
jq -c 'select(.record_id and .exp_id and .event_id and .factor_id
  and (.predicted_p | type == "number") and (.observed_outcome | IN(0,1))
  and .source and .judge_id and .brier_component != null
  and .log_loss_component != null and .baseline_sha256_prefix)' \
  experiments/settlement_records.jsonl | wc -l   # must equal wc -l above

# 5.3 — headline Brier inputs are numeric or anchor (MUST be empty)
jq -c 'select(.source == "text-extract")' experiments/brier_inputs.jsonl | wc -l

# 5.4 — P2.1 rows: datasource_status must be active
jq -c 'select(.datasource_status != "active")' \
  ../papers/p07-signal-fusion/experiments/signals/*.jsonl

# 5.5 — writeback: after.baseline_sha256_prefix == before.snapshot_sha256_prefix
diff <(jq -r .snapshot_sha256_prefix experiments/before_after/before.json) \
     <(jq -r .baseline_sha256_prefix  experiments/before_after/after.json)

# 5.6 — no level=question outside M2 in work.jsonl
jq -c 'select(.level == "question")' logs/work.jsonl | wc -l

# 5.7 — heartbeat action restricted to {liveness, restart, nudge}
jq -c 'select(.action and (.action | IN("liveness","restart","nudge") | not))' \
  logs/heartbeat.jsonl
```

`5.6` and `5.7` are zero-interaction guards (PIT-011, PIT-004). `5.5` is the writeback-baseline guard (PIT-306). `5.3` enforces the headline-Brier rule (PIT-302, DST-15).

## 6. Non-goals (do NOT do these in this directory)

1. **Do not** implement `calc_brier.py` yet. This file is the spec; implementation is a separate milestone (M1.5) that requires a follow-up configuration pass and a unit-test target.
2. **Do not** claim that the Factor Ledger exists. P1.2 reads `evidence_ledger_entry.factor_id` from the P1+P2 project; it does **not** own the ledger. The factor ledger concept page here is a design pointer to the P1+P2 schema, not an implementation claim (PIT-301).
3. **Do not** lead the paper with "we built a novel prediction-market calibration method for LLM agents". The new positioning is "the external settlement layer that makes P1+P2 evidence-ledger entries evaluable". Calibration is a means, not the contribution.
4. **Do not** reframe knowledge writeback as "memory writeback" or "agent memory". The correct frame is "belief update with settlement evidence" (roadmap §7).
5. **Do not** write text-extract forecasts into the headline Brier. `text-extract` rows are reported in a separate sub-aggregate or marked `un_settleable: true` (PIT-302, DST-6, DST-15).
6. **Do not** add a second human checkpoint. M2 is the only one. Any other `level=question` event is a violation (PIT-011, PIT-303).
7. **Do not** run a Polymarket pull that exceeds 5 events per domain without first adding backoff/retry. Until retry is in, the cap is enforced manually (PIT-304).
8. **Do not** claim "judge is calibrated" on the basis of 3 gold samples. Either expand the gold set or weaken the claim (PIT-305).
9. **Do not** report cross-domain ANOVA with n < 3 per cell as a significance test. Report directional consistency only (PIT-308).
10. **Do not** move or rename any file under `cds4polymarket/` or `cds4worldcup/`. This directory is read-only on those sources.

## 7. Cross-references

- `data-contracts.md` — `settlement_record` (§9), `evidence_ledger_entry` (§8), `signal_evidence_entry` (§10), validation commands (§12).
- `experiment-pitfalls.md` — §4 P1.2 traps (PIT-301 through PIT-308); §6 prompt-level anti-patterns; §7 data-shape traps; §8 pre-flight checklist.
- Roadmap §7 — P8 / P1.2 new positioning and "settlement layer" language.
- `wiki/concepts/settlement-calibration-layer.md` — narrative explanation of this layer's role in the portfolio.
- `wiki/decisions/2026-07-03-settlement-layer-configuration.md` — the decision that produced this reconfiguration.
- `claude-prompt.md`, `mimo-prompt.md` — entry points for a worker running this directory under the AutoResearch protocol.