# P2.1 IO Specification — Evidence Input Layer

> Created: 2026-07-03
> Scope: IO contract for `papers/p07-signal-fusion/` under the
> P1+P2 mainline (Roadmap §6, §8). This file replaces the
> "12-data-source fusion" framing. The producer here does **not** own
> decision fusion; it produces **evidence-ledger-shaped rows** that the
> downstream ledger consumes.
>
> Pair with:
> - `../../../framework/schemas/data-contracts.md` §10 (canonical `signal_evidence_entry`)
> - `../../../framework/schemas/experiment-pitfalls.md` §5 (PIT-401..PIT-408)
> - `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §8

## 0. Role and non-goals

| Role | In / Out |
|------|----------|
| IN  | Raw observations from `cds-keyperson` datasources (12 active + 1 inactive). |
| OUT | `signal_evidence_entry` rows consumed by the P1+P2 `evidence_ledger_entry` schema. |
| OUT | Side-channel bias-detection rows consumed by the P1.2 settlement audit trail. |
| OUT | Ablation logs that justify the inclusion/exclusion of any source group. |
| OUT | `experiments/`, `state/`, `logs/`, `wiki/`, `paper/` artifacts. |

**Non-goals (Roadmap §8):**

- Do not claim a "novel fusion algorithm" in the paper framing (PIT-401).
- Do not output free-text forecast as a Brier input — that is the
  P1.2 side's job to re-anchor (PIT-302, PIT-406).
- Do not route P11 free-text traces into the ledger as observable
  signals (PIT-207, PIT-408).
- Do not silently include the `polymarket` datasource (PIT-403).

## 1. Producer ↔ consumer contract

```
+----------------------+      signal_evidence_entry     +----------------------+
|  cds-keyperson data  | ─────────────────────────────► |  P1+P2 ledger        |
|  sources (12 active) |                                |  (evidence_ledger_   |
|  + bias detector     | ──── bias_detection rows ────► |   entry consumer)    |
|                      |                                |                      |
|                      | ◄── settlement audit ───────── |  P1.2 settlement     |
+----------------------+                                +----------------------+
```

The contract has three properties the downstream ledger **requires**:

1. **Source independence** is declared per row, not inferred downstream.
2. **Conflict discovery** is a first-class output (rows of conflicting
   evidence, not silently merged).
3. **Freshness** carries both an absolute timestamp and a window relative
   to the indicator's natural period.

If any of these three are missing in a row, the row is treated as
`un_settleable` and excluded from the downstream Brier aggregate.

## 2. `signal_evidence_entry` schema (producer-side)

This is the row that P2.1 emits. It mirrors `data-contracts.md §10`
verbatim plus four producer-side extensions.

```json
{
  "signal_id": "SIG-P12P-042",
  "exp_id": "P12P",
  "datasource_id": "geopolitics|finance|macro|energy|sanctions|news|aviation|academic|wikipedia|weather|sports|...",
  "datasource_status": "active",
  "signal_type": "confirmed_fact|weak_evidence|missing_data|source_failure",
  "lens_weight": 0.18,
  "recency_weight": 0.92,
  "observed_at": "2026-07-02T12:00:00Z",
  "freshness_window": "P1D",
  "freshness_ratio": 0.5,
  "scenario": "base|downside|upside|null",
  "scenario_text": "OPEC+ holds; refinery margins compress",
  "numeric_forecast": null,
  "ts_ingested": "2026-07-03T08:00:00Z",

  "source_independence": 2,
  "independence_class": "primary|secondary|tertiary",
  "supporting_signals": ["SIG-P12P-041"],
  "contradicting_signals": ["SIG-P12P-038"],
  "audit_trace": [
    {"tool": "fetch|hash|score|calibrate",
     "input_sha256_prefix": "ab12...",
     "output_sha256_prefix": "cd34...",
     "ts": "2026-07-03T07:59:00Z",
     "agent": "P2.1-worker"}
  ]
}
```

### 2.1 Field-level rules

| Field | Required | Rule | Source pitfall |
|-------|:--------:|------|----------------|
| `signal_id` | yes | `SIG-P12P-<NNN>`, NNN zero-padded, monotonic within a run. | — |
| `exp_id` | yes | Always `"P12P"`. | DST-12 |
| `datasource_id` | yes | Must be one of the 12 active datasource ids. | PIT-403 |
| `datasource_status` | yes | Always `"active"`; any other value rejects the row. | PIT-403 |
| `signal_type` | yes | Enum only: `confirmed_fact|weak_evidence|missing_data|source_failure`. | PIT-408, DST-14 |
| `lens_weight` | yes | `[0, 1]`; produced by the fusion chain. | — |
| `recency_weight` | yes | `[0, 1]`; produced by `signal_normalizer.py`. | — |
| `observed_at` | yes | ISO-8601 UTC, **strictly <=** `ts_ingested`. | — |
| `freshness_window` | yes | ISO-8601 duration; indicator's natural period. | PIT-203 |
| `freshness_ratio` | yes | `age / freshness_window`; `> 1.0` ⇒ downstream flag. | PIT-203 |
| `scenario` | no | One of `base|downside|upside` or `null` when no scenario applies. | — |
| `scenario_text` | yes-if-scenario | Free text if `scenario != null`; never used as a probability. | PIT-012, PIT-302 |
| `numeric_forecast` | yes-if-bridge | Numeric `[0, 1]` if downstream Brier consumer; else `null`. | PIT-302, PIT-406 |
| `source_independence` | yes | Integer >= 1; PIT-202 only binds for `factor_type: authority` downstream. | PIT-202 |
| `independence_class` | yes | One of `primary|secondary|tertiary`. | — |
| `supporting_signals` | yes | Non-empty array unless `signal_type: source_failure`. | DST-2 |
| `contradicting_signals` | yes | May be empty **only** if `missing_prerequisites` is non-empty downstream. | PIT-201, PIT-408 |
| `audit_trace` | yes | Array of objects with `tool` and `*_sha256_prefix`. | PIT-206, DST-11 |

### 2.2 Validator expressions (run before each iteration ships)

```bash
# 2.2.1 — datasource_status must be "active"
jq -c 'select(.datasource_status != "active")' \
  experiments/signals/*.jsonl

# 2.2.2 — signal_type in 4-value enum
jq -c 'select((.signal_type |
  inside(["confirmed_fact","weak_evidence","missing_data","source_failure"]) | not))' \
  experiments/signals/*.jsonl

# 2.2.3 — freshness_window and freshness_ratio present
jq -c 'select(.freshness_window == null or .freshness_ratio == null)' \
  experiments/signals/*.jsonl

# 2.2.4 — audit_trace is structured
jq -c 'select(.audit_trace | type != "array"
  or any(.[]; .tool == null or (.input_sha256_prefix == null and .output_sha256_prefix == null)))' \
  experiments/signals/*.jsonl

# 2.2.5 — numeric_forecast absent ⇒ row is un_settleable downstream
jq -c 'select(.numeric_forecast == null) | {signal_id, settleable: false}' \
  experiments/signals/*.jsonl
```

A non-empty result from any of 2.2.1 / 2.2.2 / 2.2.4 is a **PIT-403 /
PIT-408 / PIT-206 hit** and the iteration is not done.

## 3. Datasource grouping (predetermined, locked)

The 12 active datasources are partitioned into three evidence groups.
The grouping is **predetermined** (PIT-006): do not regroup mid-run.

| Group | Name | Datasources | Independence floor | Notes |
|-------|------|-------------|:------------------:|-------|
| A | Market Signals | `finance`, `macro`, `energy` | 2 | Numeric-first; preferred `numeric_forecast` source. |
| B | Event Intelligence | `geopolitics`, `sanctions`, `news`, `aviation` | 2 | Time-sensitive; smallest `freshness_window`. |
| C | Reference Knowledge | `academic`, `wikipedia`, `weather`, `sports` | 1 | Stable but slow-moving; primary source for `confirmed_fact`. |
| — | INACTIVE | `polymarket` | n/a | Excluded by `datasource_status != "active"` filter. |

The grouping is mirrored in `state/progress.json` `predetermined_config`
and in `wiki/decisions/datasource-selection.md`. Any change requires
writing a new decision file before the run.

## 4. Conflict discovery output

When two or more rows disagree on the same fact, the producer emits
both rows **and** a conflict summary row. The summary is the
`signal_evidence_entry` shape with `signal_type: "weak_evidence"`,
`source_independence = count of distinct sources`, and
`contradicting_signals` listing every disagreeing row.

| Trigger | Conflict row emitted? |
|---------|:--------------------:|
| Same `signal_type: confirmed_fact`, different direction | yes |
| Numeric forecast within `numeric_forecast ± 0.20` window, different scenario | yes |
| `source_failure` from a primary datasource | yes (downgrades dependent rows) |
| Single source only | no (not a conflict) |

The downstream ledger uses the conflict summary to populate
`contradicting_evidence[]` (Roadmap §6.3 schema). PIT-201 prevents
the ledger from accepting an entry with both
`contradicting_evidence=[]` and `missing_prerequisites=[]`.

## 5. Freshness contract

`freshness_ratio = (ts_ingested - observed_at) / freshness_window`

| Indicator family | `freshness_window` default | Stale threshold |
|------------------|----------------------------|----------------:|
| `finance`, `energy` price ticks | `PT15M` | `> 1.0` |
| `news`, `geopolitics`, `sanctions`, `aviation` | `PT1H` | `> 1.0` |
| `macro`, `weather` | `PT6H` | `> 1.0` |
| `academic`, `wikipedia`, `sports` | `P7D` | `> 1.0` |

A row with `freshness_ratio > 1.0` is **not** discarded; it is flagged
with `stale: true` so the ledger can include it as
`contradicting_evidence` (a stale source frequently contradicts
current state).

## 6. Bias-detection output

The Calibrator output is exposed as a **side-channel row** rather than
embedded in `signal_evidence_entry`. Shape:

```json
{
  "bias_signal_id": "BSIG-P12P-007",
  "exp_id": "P12P",
  "method": "ratio_threshold",
  "significance_tested": false,
  "scenario_a": "base", "scenario_b": "upside",
  "ratio": 2.4,
  "threshold": 2.0,
  "verdict": "over_optimism",
  "ts": "2026-07-03T08:00:00Z",
  "audit_trace": [{"tool": "calibrate",
    "input_sha256_prefix": "...", "output_sha256_prefix": "...",
    "ts": "...", "agent": "P2.1-worker"}]
}
```

`significance_tested: false` is **mandatory** (PIT-402). The paper
framing is "over_optimism flagged (ratio ≥ 2.0× threshold, no
significance test)" — never "p < 0.05".

## 7. Output files

| Path | Purpose | Format |
|------|---------|--------|
| `experiments/signals/<run_id>.jsonl` | All `signal_evidence_entry` rows for one run. | JSONL |
| `experiments/conflicts/<run_id>.jsonl` | Conflict summary rows. | JSONL |
| `experiments/calibrator/<run_id>.jsonl` | `bias_signal_*` rows. | JSONL |
| `experiments/ablation/<group>_<run_id>.jsonl` | Per-group ablation outputs. | JSONL |
| `experiments/mc_inventory.json` | Row counts per condition, per group. | JSON |
| `state/findings.jsonl` | Findings + pitfall hits + avoidance reports. | JSONL |
| `state/iteration_log.jsonl` | Per-iteration summary with `preflight_pass`. | JSONL |

## 8. Cross-experiment handoff

| Consumer | Consumes | Required fields |
|----------|----------|-----------------|
| `papers/p1p2-evidence-ledger/` | `signal_evidence_entry` rows | `supporting_signals`, `contradicting_signals`, `source_independence`, `freshness_ratio`, `audit_trace` |
| `papers/p08-market-calibration/` | `bias_signal_*` rows + `numeric_forecast` | `numeric_forecast` is `[0, 1]`; `bias_signal_*` carries `significance_tested: false` |
| `state/findings.jsonl` | Pitfall hits + avoidance | All §10 fields from `data-contracts.md` |

## 9. Open questions (do NOT implement before the answer is frozen)

| # | Question | Why deferred |
|---|----------|--------------|
| Q1 | Should `supporting_signals` include cross-group corroborations or stay within-group? | Affects `source_independence` semantics. |
| Q2 | When a row's `scenario_text` is later converted to a probability, who owns the conversion? | Belongs in P1.2 (anchor table). |
| Q3 | Do we keep the original `cds-keyperson` Calibrator ratio threshold or expose a multi-axis bias? | Roadmap §8 says "evidence topology, not feature fusion". |

These are listed for tracking; resolving them is **out of scope** for
this configuration pass (Roadmap §10 近期执行清单 — first do the
configuration, then design the ablation).

## 10. Cross-references

- `data-contracts.md` §10 — canonical `signal_evidence_entry` shape.
- `data-contracts.md` §12 — validator commands (extended in §2.2 above).
- `experiment-pitfalls.md` §5 — PIT-401..PIT-408.
- Roadmap §8 — "P7 降级为输入模块，除非升级成 evidence topology".
- `state/task_spec.md` — milestones for this directory.
- `wiki/concepts/signal-to-evidence-contract.md` — narrative version.
- `wiki/decisions/2026-07-03-evidence-input-configuration.md` — the
  decision that this io_spec implements.