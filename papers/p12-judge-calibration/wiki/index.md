# P12 Judge Calibration Wiki

> Maintained: 2026-07-03
> exp_id: `P12`
> Status: configured for AutoResearch; awaiting M1 sample manifest.

## Current Decision

P12 is the short-term 60-point paper candidate. It reuses P11 data
to test whether the five-protocol judge (leaked / blind / pairwise /
neighborhood / abstention) can correct the false-positive conclusions
in the H1 / H1c / H3 / F1 chain.

The configuration decision is recorded in
[`decisions/2026-07-03-p12-configuration.md`](decisions/2026-07-03-p12-configuration.md).

## Entry Points

| Role | Path |
|------|------|
| Task definition | `../state/task_spec.md` |
| IO contract | `../state/io_spec.md` |
| Progress | `../state/progress.json` |
| Findings | `../state/findings.jsonl` |
| Iteration log | `../state/iteration_log.jsonl` |
| Directions tried | `../state/directions_tried.json` |
| Pre-registration | `../state/experiment_design.md` (to be created in M2) |
| Worker prompt (Claude) | `../claude-prompt.md` |
| Worker prompt (Mimo) | `../mimo-prompt.md` |

## Concepts

- [`concepts/judge-calibration-protocol.md`](concepts/judge-calibration-protocol.md) —
  the five-protocol design and the link to data-contracts.

## Decisions

- [`decisions/2026-07-03-p12-configuration.md`](decisions/2026-07-03-p12-configuration.md) —
  scope, non-goals, gate mapping, why this configuration.

## Source Evidence (read-only for P12)

- `../../legacy/p11-closed-v5-minimax-m3/wiki/decisions/blind-judge.md`
- `../../legacy/p11-closed-v5-minimax-m3/wiki/decisions/h1-reformulation.md`
- `../../legacy/p11-closed-v5-minimax-m3/wiki/decisions/2026-07-03-structural-intelligence-reassessment.md`
- `../../legacy/p11-closed-v5-minimax-m3/state/progress.json`
- `../../legacy/p11-closed-v5-minimax-m3/experiments/`

## Key Pitfalls (from `../../../../framework/schemas/experiment-pitfalls.md` §2)

- **PIT-101** — Label leakage in judge prompts. P12 must run leaked + blind.
- **PIT-102** — Brittle consistency-on-wrong. Pairwise protocol must be conditional on `ground_truth_correctness`.
- **PIT-103** — Abstention collapse. `abstain_rate` must be > 0 on ambiguous sets.
- **PIT-104** — Neighborhood probes that are not actually neighbors. Each probe changes exactly one axis.
- **PIT-105** — Reusing P11 samples without re-anchoring. Imported samples set `condition_visible_to_judge: false`.
- **PIT-106** — Apples-to-oranges across protocols. All five share `sample_ids_ordered`.
- **PIT-107** — Five-persona review without diversity. Review rounds must use ≥ 2 distinct models.

Universal traps to keep in mind: **PIT-001** (verify every citation),
**PIT-002** (anti-inflation cap), **PIT-003** (stale → structural pivot),
**PIT-006** (pre-registration frozen), **PIT-007** (n ≥ 30 per cell),
**PIT-009** (fresh session each iteration), **PIT-010** (≤ 5 large files,
≤ 300 lines each), **PIT-011** (no user questions mid-run).

## Milestones (from `state/task_spec.md`)

| # | Milestone | Deliverable |
|---|-----------|-------------|
| M1 | Sample manifest from P11 | `experiments/sample_manifest.jsonl` |
| M2 | Reproduce label leakage | `experiments/leakage_reproduction.json` |
| M3 | Pairwise blind judge | `experiments/pairwise_blind_results.json` |
| M4 | Neighborhood probe schema | `experiments/neighborhood_probe_schema.json` |
| M5 | Small probe run | `experiments/neighborhood_probe_results.json` (≥ 30 samples) |
| M6 | Calibration metrics table | `experiments/calibration_metrics.md` |
| M7 | Paper skeleton | `paper/outline.md` |
| M8 | Five-persona review | `paper/review_round_1.md` (median ≥ 6.0 → short paper) |

## Non-goals

- No new large P11 experiment.
- No universal judge benchmark claim.
- No reliance on producer self-confidence.
- No `level=question` in any log line.
- No edits to `state/experiment_design.md` after the run starts.
