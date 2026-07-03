# Experiment Configuration Orchestration Plan

> Date: 2026-07-03  
> Scope: Configure experiment directories to match the AutoResearch roadmap, with uniform wiki, prompts, state files and input/output specs.

## Objective

Prepare the active experiment directories so small agents can run them safely under the AutoResearch protocol:

- `papers/p12-judge-calibration`
- `papers/p1p2-evidence-ledger` (new mainline directory)
- `papers/p08-market-calibration`
- `papers/p07-signal-fusion`
- P11 remains closed as a source dataset; no new P11 mainline config beyond closure.

## Dispatch Strategy

Small models are assigned narrow, file-scoped tasks:

1. **Pitfalls and shared contracts**: read roadmap/materials and create shared pitfalls + data-contract docs.
2. **P12 config**: align P12 state/wiki/prompts/specs with shared contracts.
3. **P1+P2 mainline config**: create evidence-ledger directory with state/wiki/prompts/specs.
4. **P1.2 config**: align market-calibration directory as settlement/calibration layer.
5. **P2.1 config**: align signal-fusion directory as evidence-input layer.

Each worker must:

- read this plan plus the roadmap,
- edit only its assigned directory and explicitly allowed shared docs,
- write files that are readable by a fresh agent,
- avoid implementation claims unless there is code/data,
- record known pitfalls and non-goals,
- preserve existing experiment data and paths.

## Shared Deliverables

- `../../framework/schemas/experiment-pitfalls.md`
- `../../framework/schemas/data-contracts.md`
- per-experiment `state/io_spec.md`
- per-experiment `wiki/index.md` or updates
- per-experiment `claude-prompt.md` and `mimo-prompt.md` if missing or stale
- per-experiment `state/task_spec.md` updated only when needed

## Verification Checklist

- All active experiment dirs have `state/task_spec.md`, `state/progress.json`, `state/io_spec.md`.
- All active experiment dirs have `logs/`, `wiki/index.md`, `experiments/`, and `paper/` or an explicit note why not.
- Prompts tell agents to use AutoResearch state files, do not ask user questions, and obey Roadmap scope.
- JSON files parse with `jq`.
- No existing raw data or experiment result is moved.
