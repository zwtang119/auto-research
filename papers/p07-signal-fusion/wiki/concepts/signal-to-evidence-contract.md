# Signal → Evidence Contract

> Created: 2026-07-03
> Scope: narrative version of `state/io_spec.md`. Defines what a
> producer-side `signal_evidence_entry` must carry so the downstream
> P1+P2 `evidence_ledger_entry` can use it without re-interpreting
> free-text reasoning.

## 1. Why this contract exists

The P1+P2 evidence-ledger mainline (Roadmap §6) rejects any entry whose
supporting evidence is free-text reasoning. P11's
`inner_monologue / no_think / pure_analysis` traces cannot be ledger
input as-is — that is the PIT-207 / PIT-408 trap.

P2.1 sits **upstream** of the ledger. It produces rows that already
satisfy the ledger invariants:

- structured, not free-text
- source-independence declared
- freshness measured, not just timestamped
- conflicts exposed, not silently merged

If a downstream ledger import script can read a P2.1 row and
materialize a ledger entry with empty `contradicting_evidence[]` and
empty `missing_prerequisites[]`, the contract failed.

## 2. Four contract clauses

### 2.1 Source independence must be declared, not inferred

Every row carries `source_independence` (integer ≥ 1) and
`independence_class` (`primary | secondary | tertiary`). Downstream
authority-factor validation (PIT-202) reads this field directly.

A producer that can only point at one source emits
`source_independence: 1` and lets the ledger mark the row as
non-authoritative. A producer with two genuinely independent sources
emits `2` and is allowed to feed authority factors.

### 2.2 Conflict discovery is a first-class output

The producer does not merge disagreeing sources into one narrative.
For every disagreement:

- Both contributing rows are emitted (each carries the other in
  `contradicting_signals`).
- A summary row is emitted with `signal_type: "weak_evidence"` and
  `source_independence = count of distinct sources`.

Downstream, the ledger imports the summary into
`contradicting_evidence[]`. This is what stops PIT-201 from firing —
the entry that pretends to be complete but lists zero contradictions
and zero missing prerequisites.

### 2.3 Freshness is ratio, not timestamp

A row that says `freshness: "2026-07-03"` on a 15-minute price tick is
not the same as on a 1-year macro indicator. The contract carries:

- `observed_at` — absolute ISO-8601 UTC.
- `freshness_window` — ISO-8601 duration matching the indicator's
  natural period.
- `freshness_ratio` — `age / freshness_window`; `> 1.0` ⇒ `stale: true`.

The ledger uses `freshness_ratio` to decide whether to include a row
as `supporting_evidence` or downgrade it to
`contradicting_evidence` (a stale source frequently contradicts
current state).

### 2.4 Bias detection is a side-channel row, not embedded

The Calibrator's `over_optimism / over_pessimism` verdict is **not**
mutated into the original `signal_evidence_entry`. Instead it is
emitted as a separate `bias_signal_*` row carrying
`significance_tested: false` (PIT-402). This keeps the producer-side
ledger row "what was observed" clean and the bias row "what the
calibrator thinks" distinct — the same separation the audit trace
enforces (PIT-206).

## 3. Signal type enum

| `signal_type` | Allowed `supporting_signals` | Allowed `contradicting_signals` |
|---------------|------------------------------|---------------------------------|
| `confirmed_fact` | non-empty | may be empty if downstream `missing_prerequisites` non-empty |
| `weak_evidence` | non-empty | non-empty |
| `missing_data` | must be empty | must be empty (carry no support, no contradiction) |
| `source_failure` | must be empty | may be empty |

This is what stops PIT-408 from firing: free-text reasoning has no
slot in this enum.

## 4. Numeric forecast handoff

The producer may emit a `numeric_forecast` in `[0, 1]` when the row
is destined for the P1.2 Brier aggregate. If the producer can only
emit a `scenario_text`, the row is forwarded as
`numeric_forecast: null`, and downstream P1.2 marks the row as
`un_settleable: true` (PIT-302, PIT-406).

The producer is **not** allowed to invent a number from text. The
P1.2 side owns the anchor table that turns text into numbers.

## 5. Audit trace

Every row carries `audit_trace` as an array of objects with `tool`
and at least one `*_sha256_prefix`. Allowed `tool` values:

- `fetch` — datasource pull.
- `hash` — sha256 prefix calculation.
- `score` — lens-weight / recency-weight calculation.
- `calibrate` — Calibrator verdict.

PIT-206 forbids the field from being a free-text comment. The trace
is what lets the audit script re-run a row and reproduce the output.

## 6. What is **not** in the contract

- The fusion algorithm. The contract talks about rows; the algorithm
  is an implementation detail inside `cds-keyperson`.
- The decision itself. The producer never claims a "decision" — only
  evidence rows.
- The judge. P12 owns judge calibration; P2.1 must never self-judge.
- The text forecast. The producer may emit text but never as a
  probability.

## 7. Worked example

Gulei scenario, 2026-07-03:

```json
{
  "signal_id": "SIG-P12P-042",
  "exp_id": "P12P",
  "datasource_id": "weather",
  "datasource_status": "active",
  "signal_type": "confirmed_fact",
  "lens_weight": 0.18,
  "recency_weight": 0.92,
  "observed_at": "2026-07-03T07:00:00Z",
  "freshness_window": "PT6H",
  "freshness_ratio": 0.17,
  "scenario": null,
  "scenario_text": null,
  "numeric_forecast": null,
  "ts_ingested": "2026-07-03T08:00:00Z",
  "source_independence": 2,
  "independence_class": "primary",
  "supporting_signals": ["SIG-P12P-040"],
  "contradicting_signals": [],
  "audit_trace": [
    {"tool": "fetch", "input_sha256_prefix": "ab12...",
     "output_sha256_prefix": "cd34...", "ts": "2026-07-03T07:55:00Z",
     "agent": "P2.1-worker"}
  ]
}
```

Downstream `evidence_ledger_entry` consumption:

- `supporting_evidence[]` ← `supporting_signals` mapped to source ids.
- `contradicting_evidence[]` ← `contradicting_signals` (empty here).
- `missing_prerequisites[]` ← not empty downstream (Group A market
  data not pulled yet) ⇒ PIT-201 does not fire.
- `freshness_ratio: 0.17` ⇒ fresh, used as `supporting_evidence`.

## 8. Failure modes the contract prevents

| Trap id | What the contract prevents |
|---------|----------------------------|
| PIT-201 | `contradicting_evidence=[]` only allowed when `missing_prerequisites` is non-empty downstream. |
| PIT-202 | Authority factors require `source_independence >= 2`; producer must declare it. |
| PIT-203 | `freshness_window` + `freshness_ratio` are required fields. |
| PIT-206 | `audit_trace` is structured, not free-text. |
| PIT-302 / PIT-406 | `numeric_forecast` is `[0, 1]` or `null`; never text-as-probability. |
| PIT-403 | `polymarket` rejected by `datasource_status` filter. |
| PIT-408 | `signal_type` is in the 4-value enum; free-text trace has no slot. |

## 9. Related pages

- `state/io_spec.md` — formal schema and validator expressions.
- `state/task_spec.md` — milestones for this directory.
- `wiki/decisions/2026-07-03-evidence-input-configuration.md` — the
  decision that locked this contract.
- `../../../../framework/schemas/data-contracts.md` §10 — canonical shape.
- `../../../../framework/schemas/experiment-pitfalls.md` §5 — matching trap ids.