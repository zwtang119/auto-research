# 2026-07-03 Experiment Configuration Audit

## Scope

This audit verifies the agent-produced configuration pass for:

- `papers/p12-judge-calibration/`
- `papers/p1p2-evidence-ledger/`
- `papers/p08-market-calibration/`
- `papers/p07-signal-fusion/`

## Orchestration

The work was dispatched through `rp-cli` using RepoPrompt window `2` (`auto-research`). Small agents were assigned narrow, non-overlapping tasks:

1. Shared pitfalls and data contracts.
2. P12 judge-calibration configuration.
3. P1+P2 evidence-ledger mainline scaffold.
4. P1.2 settlement-layer configuration.
5. P2.1 evidence-input configuration.

Each worker was instructed to read the Roadmap, shared pitfalls, and shared data contracts; edit only its assigned directory; write specs/wiki/prompts; and avoid code implementation.

## Files Added Or Updated

Shared:

- `../../framework/schemas/experiment-pitfalls.md`
- `../../framework/schemas/data-contracts.md`
- `docs/autoresearch/2026-07-03-experiment-configuration-plan.md`

P12:

- `papers/p12-judge-calibration/state/io_spec.md`
- `papers/p12-judge-calibration/wiki/concepts/judge-calibration-protocol.md`
- `papers/p12-judge-calibration/wiki/decisions/2026-07-03-p12-configuration.md`
- `papers/p12-judge-calibration/claude-prompt.md`
- `papers/p12-judge-calibration/mimo-prompt.md`
- `papers/p12-judge-calibration/paper/outline.md`

P1+P2:

- `papers/p1p2-evidence-ledger/` full AutoResearch scaffold
- `papers/p1p2-evidence-ledger/state/io_spec.md`
- `papers/p1p2-evidence-ledger/wiki/concepts/evidence-ledger-schema.md`
- `papers/p1p2-evidence-ledger/wiki/decisions/2026-07-03-mainline-configuration.md`
- `papers/p1p2-evidence-ledger/claude-prompt.md`
- `papers/p1p2-evidence-ledger/mimo-prompt.md`
- `papers/p1p2-evidence-ledger/paper/outline.md`

P1.2:

- `papers/p08-market-calibration/state/io_spec.md`
- `papers/p08-market-calibration/wiki/concepts/settlement-calibration-layer.md`
- `papers/p08-market-calibration/wiki/decisions/2026-07-03-settlement-layer-configuration.md`
- `papers/p08-market-calibration/README.md`
- prompt and outline updates

P2.1:

- `papers/p07-signal-fusion/state/io_spec.md`
- `papers/p07-signal-fusion/wiki/concepts/signal-to-evidence-contract.md`
- `papers/p07-signal-fusion/wiki/decisions/2026-07-03-evidence-input-configuration.md`
- `papers/p07-signal-fusion/README.md`
- prompt and outline updates

## Verification Performed

- Required active-directory files checked for existence.
- Active `progress.json` and `directions_tried.json` files parsed with `jq`.
- Active `findings.jsonl` and `iteration_log.jsonl` files parsed line-by-line with `jq`.
- Agent outputs checked for scope boundaries:
  - no experiment code implemented,
  - no raw data moved,
  - no new P11 mainline experiment,
  - P1.2 explicitly avoids claiming Brier code exists,
  - P2.1 explicitly avoids claiming novel fusion algorithm.
- Relative prompt paths were corrected where they could confuse a worker launched from an experiment directory.
- P1+P2 review wording was adjusted from unrealistic "five distinct models" to "five personas; ≥2 distinct models when available."

## Residual Risks

- `experiment-pitfalls.md` is intentionally detailed and long; workers should read only the relevant experiment section plus universal traps.
- P1.2 and P2.1 `state/task_spec.md` files still reflect their original milestones; the new interpretation is supplied through `state/io_spec.md`, decision docs, prompts, and README. This preserves existing state while changing framing.
- Validation commands that reference future experiment output files will fail until those files exist; they are pre-flight checks for later milestones, not evidence of completed experiments.

## Next Action

Start P12 M1:

1. Write `papers/p12-judge-calibration/state/experiment_design.md`.
2. Generate `papers/p12-judge-calibration/experiments/sample_manifest.jsonl` from P11 samples.
3. Freeze `experiments/sample_ids_ordered.json`.
4. Do not run judge calls until M1 validators pass.
