# P1.2 Market Calibration — Settlement Layer

> New role after 2026-07-03 roadmap: external settlement / calibration layer for the P1+P2 evidence-ledger mainline.

This directory no longer leads with "prediction market calibration as a standalone agent paper." It now emits `settlement_record` rows, Brier/Log Loss inputs, and before/after settlement snapshots that make P1+P2 evidence-ledger claims externally evaluable.

## Entry Points

- `state/task_spec.md` — milestones inherited from the original P1.2 plan.
- `state/io_spec.md` — binding IO contract for `settlement_record`.
- `wiki/decisions/2026-07-03-settlement-layer-configuration.md` — reconfiguration decision.
- `wiki/concepts/settlement-calibration-layer.md` — conceptual role.
- `claude-prompt.md` / `mimo-prompt.md` — worker prompts.
- `paper/outline.md` — optional short-paper outline.

## Hard Boundaries

- No Brier implementation in this configuration pass.
- No claim that Factor Ledger exists here; P1+P2 owns it.
- No text-extract rows in headline Brier.
- M2 is the only human checkpoint.
- This directory is read-only against sibling experiments and external source repos.
