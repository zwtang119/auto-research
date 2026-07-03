# P2.1 Signal Fusion — Evidence Input Layer

> New role after 2026-07-03 roadmap: evidence input layer for the P1+P2 evidence-ledger mainline.

This directory no longer treats "12-source signal fusion" as the main paper contribution. Its job is to convert multi-source observations into `signal_evidence_entry` rows with source independence, conflict discovery, freshness, and audit trace fields.

## Entry Points

- `state/task_spec.md` — original milestone plan, now interpreted through the evidence-input role.
- `state/io_spec.md` — binding IO contract for `signal_evidence_entry`.
- `wiki/decisions/2026-07-03-evidence-input-configuration.md` — reconfiguration decision.
- `wiki/concepts/signal-to-evidence-contract.md` — producer-consumer contract.
- `claude-prompt.md` / `mimo-prompt.md` — worker prompts.
- `paper/outline.md` — optional evidence-input paper outline.

## Hard Boundaries

- No claim of a novel fusion algorithm.
- No use of free-text forecasts as Brier probabilities.
- `polymarket` datasource remains inactive and must be excluded.
- Bias detection is a side-channel with `significance_tested: false`.
- This directory emits evidence rows; P1+P2 owns ledger decisions.
