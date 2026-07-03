# 2026-07-03 — P12 Configuration Decision

> Status: accepted
> Owner: P12 worker agent
> Pair with `state/task_spec.md`, `state/io_spec.md`,
> `wiki/concepts/judge-calibration-protocol.md`,
> `../task_spec.md` (root portfolio), and
> `../../docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §5.

## 1. Decision

Configure P12 as a **3-6 day judge-calibration viability probe** with
the following fixed properties:

1. **exp_id = `P12`**, sample prefix `P12-`, protocol id prefix
   `R-P12-<protocol>-<NNN>`, finding id prefix `FID-20260703-<NNN>`.
2. **Five frozen protocols**: `leaked`, `blind`, `pairwise`,
   `neighborhood`, `abstention`. The set is fixed for the whole run
   (PIT-006). Adding a sixth protocol is a new experiment, not an edit.
3. **Reused evidence**: P11 raw samples and P11 prior-judge decisions
   (blind-judge, h1-reformulation, structural-intelligence reassessment).
   No new large P11 run.
4. **Zero human checkpoints** (PIT-011). The P1.2 M2 exception does not
   apply here.
5. **Pre-registration first**: `state/experiment_design.md` is written
   and frozen before the first judge call (PIT-006).
6. **Stop rules**: `stale_count >= 2` ⇒ drop to minimal reproducibility
   (smaller cell sizes, drop neighborhood). `stale_count >= 4` ⇒ stop
   and fold into P1+P2 (task_spec §"Stale Rules").
7. **Five-persona review** at M8: R1..R5, median used (not mean), first
   round ≤ 7.0, ≥ 1 unresolved weakness must remain (PIT-002, PIT-107).

## 2. Why this configuration

- **Roadmap §5 names P12 as the short-term 60-point paper candidate.**
  The fast route requires reusing P11 data, not running a new
  benchmark. Reusing is the cheapest way to demonstrate the protocol
  set works on a real false-positive chain (H1, H1c, H3, F1).
- **The data-contracts already define `judge_protocol_result` and
  `sample_manifest`.** P12 does not need a new schema. It only needs
  to populate them and to enforce the P12-specific invariants in
  `io_spec.md` §7.
- **The pitfalls log already enumerates PIT-101..107.** P12's
  configuration closes each one by binding it to a validator
  command. There is no "we'll handle it later" gap.
- **The 3-6 day window is the right size for a viability probe.** It
  is short enough to be reversible, long enough to reproduce
  PIT-101 and to detect at least one of PIT-102..105.

## 3. Scope

In scope:

- M1 sample manifest re-anchored from P11 with `condition_visible_to_judge: false`.
- M2 leaked + blind judge re-run on the same `sample_ids_ordered`.
- M3 pairwise blind on a 30-50 sample subset.
- M4 neighborhood probe schema with one axis per probe.
- M5 neighborhood + abstention runs (≥ 30 samples each, or explicit abort).
- M6 calibration metrics table per (hypothesis, protocol).
- M7 paper outline with abstract, method, results, limitations.
- M8 five-persona review round.

Out of scope (P12 non-goals):

- New large P11 experiment.
- Universal "best judge" benchmark or leaderboard.
- Reliance on producer self-confidence (DST-10, PIT-013).
- Mid-run edits to `state/experiment_design.md` (PIT-006).
- Mid-run edits to the five-protocol set (PIT-006, PIT-101).
- Engagement of the user (PIT-011).

## 4. Gate mapping (from `experiment-pitfalls.md` §9)

| Gate | P12 blockers | Closed by |
|------|--------------|-----------|
| G1 Literature | PIT-001, PIT-307, PIT-407 | paper `## Related Work`; verify every citation with `source_path`. |
| G2 Experiment | PIT-101, PIT-102, PIT-103, PIT-104, PIT-105, PIT-106, PIT-005, PIT-006, PIT-007 | io_spec §1-3, validator §7. |
| G3 Structure | — | paper outline has abstract / method / results / limitations. |
| G4 Figures | PIT-001 | one comparison table in `experiments/calibration_metrics.md`. |
| G5 Review | PIT-002, PIT-103, PIT-107, PIT-204 | review round records median + unresolved weakness + diverse models. |
| A1 State | PIT-001, PIT-003, PIT-005, PIT-009, PIT-010, PIT-206, PIT-405 | state files + pre-flight checklist. |
| A2 Stall | PIT-003, PIT-008, PIT-010, PIT-011, PIT-303 | stale_count rules + no-question rule. |
| A3 Watchdog | PIT-004, PIT-009, PIT-011 | `heartbeat.jsonl` action restriction + fresh sessions. |

## 5. Success criteria (from `state/task_spec.md`)

A run is "successful" only if all of the following hold:

- M1..M6 produce real artefacts (no placeholder files).
- `experiments/calibration_metrics.md` shows at least one cell where
  the leaked-protocol verdict does **not** survive the
  blind/pairwise/neighborhood/abstention combination.
- `paper/review_round_1.md` has a median ≥ 6.0 with ≥ 1 unresolved
  weakness.
- No validator in `state/io_spec.md` §7 returns a non-empty "MUST be
  empty" result.

If `stale_count >= 4` or the M8 median < 6.0, the run is folded into
P1+P2 methodology; P12 does not ship a paper on its own.

## 6. Risks and explicit non-actions

| Risk | Mitigation | Why we are NOT doing more |
|------|------------|---------------------------|
| P11 samples are too few for n ≥ 30 per cell | Use a 30-sample minimum and report cell size in every row | We are not running new P11 samples (task_spec non-goal). |
| Single judge model dominates verdict | Force ≥ 2 distinct models in M8 review (PIT-107) | We are not running a multi-judge panel for the protocols themselves (out of scope for 3-6 day probe). |
| "Consistency" metric drifts back to unconditional | `consistency_on_wrong` is gated on `ground_truth_correctness` (PIT-102) | We are not building a generic judge library; the contribution is the protocol set. |
| `abstain_rate == 0` silently | Validator flags any cell with `ambiguous_count > 0` and `abstain_rate == 0` (PIT-103) | We are not adding automated abstention training. |
| User gets pinged mid-run | Prompts forbid `level=question` and forbid "ask the user before submitting" (PIT-011, PAP-1) | We are not adding a checkpoint even if a cell looks bad. |

## 7. Cross-references

- `state/task_spec.md` — milestones and quality gates.
- `state/io_spec.md` — inputs, outputs, validators, non-goals.
- `wiki/concepts/judge-calibration-protocol.md` — the five protocols and metrics.
- `wiki/index.md` — entry points and pitfall summary.
- `../../docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §5 — P12 fast paper route.
- `../../../../framework/schemas/data-contracts.md` — schemas.
- `../../../../framework/schemas/experiment-pitfalls.md` §1, §2, §6, §7, §8.2 — trap list and pre-flight.
- `../../docs/autoresearch/2026-07-03-experiment-configuration-plan.md` — per-experiment shared-deliverable checklist.
