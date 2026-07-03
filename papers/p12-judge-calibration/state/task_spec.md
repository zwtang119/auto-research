# P12 Judge Calibration Task Spec

> Created: 2026-07-03  
> Priority: short-term 60-point paper candidate  
> Source evidence: P11 label leakage + blind judge + structural-intelligence reassessment

## Goal

Design and validate a compact judge-calibration protocol for LLM agent outputs. The protocol should separate:

- label leakage,
- correctness vs consistency-on-wrong,
- abstention / insufficient evidence,
- neighborhood robustness,
- subjective role fidelity vs objective behavior metrics.

## Core Research Question

Can blind, pairwise, neighborhood-probe and abstention-aware judging correct false-positive conclusions in role-conditioned LLM agent evaluation?

## Milestones

| # | Milestone | Deliverable | Auto-verifiable |
|---|---|---|---|
| M1 | Sample manifest from P11 | `experiments/sample_manifest.jsonl` | file exists, references real P11 samples |
| M2 | Reproduce label leakage | `experiments/leakage_reproduction.json` | leaked vs blind deltas present |
| M3 | Pairwise blind judge | `experiments/pairwise_blind_results.json` | pairwise records count > 0 |
| M4 | Neighborhood probe schema | `experiments/neighborhood_probe_schema.json` | schema validates fields |
| M5 | Small probe run | `experiments/neighborhood_probe_results.json` | >=30 samples or explicit abort |
| M6 | Calibration metrics table | `experiments/calibration_metrics.md` | table covers H1/H1c/H3/F1 |
| M7 | Paper skeleton | `paper/outline.md` | contribution + method + result sections |
| M8 | Five-persona review | `paper/review_round_1.md` | median score and binding weaknesses |

## Success Criteria

- Reproduce at least one P11 false-positive or fragile conclusion under label-aware judging.
- Show whether blind / pairwise / neighborhood / abstention-aware protocol changes that conclusion.
- Produce a clear go/no-go decision within 3-6 active work days.
- If median review >= 6.0, proceed to short paper; otherwise fold into P1+P2 methodology.

## Quality Gates

| Gate | Requirement |
|---|---|
| Gate 1 Literature | NCB, LLM-as-KB, SimpleQA, CoT monitorability, LLM judge calibration references covered |
| Gate 2 Experiment | Hypothesis, control, metrics and at least small-N sample present |
| Gate 3 Structure | Paper skeleton has abstract, method, results, limitations |
| Gate 4 Figures/Tables | At least one core comparison table |
| Gate 5 Review | Five-persona median score and binding weakness documented |

## Data Sources

- `../legacy/p11-closed-v5-minimax-m3/wiki/decisions/blind-judge.md`
- `../legacy/p11-closed-v5-minimax-m3/wiki/decisions/h1-reformulation.md`
- `../legacy/p11-closed-v5-minimax-m3/wiki/decisions/2026-07-03-structural-intelligence-reassessment.md`
- `../legacy/p11-closed-v5-minimax-m3/state/progress.json`
- `../legacy/p11-closed-v5-minimax-m3/experiments/`

## Stale Rules

- `stale_count >= 2`: pivot from protocol complexity to minimal reproducibility.
- `stale_count >= 4`: stop and fold into P1+P2.

## Non-goals

- No large new P11 experiment.
- No universal judge benchmark claim.
- No reliance on producer self-confidence.
