# 2026-07-03 — Settlement Layer Configuration

> **Type**: decision | **Status**: accepted | **Date**: 2026-07-03
> **Scope**: `papers/p08-market-calibration/` only; sibling directories are reconfigured by concurrent agents
> **Trigger**: `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md §7`

## Context

The 2026-07-03 topic-5 roadmap (`docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md §7`) demotes P8 / P1.2 from a standalone "prediction market calibration of LLM agents" mainline into the **external settlement / calibration layer** of the new P1+P2 evidence-ledger mainline. The original P1.2 framing competed with P12 for the same contribution space and required Brier/Log Loss code that does not exist yet. The new role makes P1.2 a producer of `settlement_record` rows that the P1+P2 ledger joins against `evidence_ledger_entry.observed_outcome`.

This directory (`papers/p08-market-calibration/`) is reconfigured to match that role. The configuration plan is `docs/autoresearch/2026-07-03-experiment-configuration-plan.md`; the IO contract is `state/io_spec.md`; the pitfalls are `framework/schemas/experiment-pitfalls.md §4`.

## Decision

Reconfigure this directory as the **settlement / calibration layer** for P1+P2. The deliverable artefacts are:

1. `state/io_spec.md` — IO contract aligned with `settlement_record` schema (`data-contracts.md §9`).
2. `wiki/concepts/settlement-calibration-layer.md` — narrative explaining the layer's role.
3. `wiki/decisions/2026-07-03-settlement-layer-configuration.md` — this decision.
4. `wiki/index.md` — refreshed to reflect the new positioning.
5. `claude-prompt.md`, `mimo-prompt.md` — entry points updated for the layer.
6. `paper/outline.md` — outline for a layer paper, framed as settlement plumbing rather than a novel calibration method.

## Non-goals (do NOT do in this reconfiguration pass)

1. **Do not implement Brier code.** `calc_brier.py` is M1.5 in `state/task_spec.md` and requires its own configuration pass with a unit-test target. This pass writes the spec, not the code.
2. **Do not rewrite `state/task_spec.md` milestones into P1+P2-shape.** The milestones M1-M9 stay; the milestone narrative changes from "standalone calibration paper" to "settlement layer that supports the P1+P2 mainline". M1.5 (Brier calculator) and M6-M9 (paper phases) are unchanged in number.
3. **Do not edit any other experiment directory.** P12, P1+P2 (new mainline), and P2.1 are configured by concurrent agents. Touching them risks write conflicts.
4. **Do not move files under `cds4polymarket/` or `cds4worldcup/`.** Both are read-only sources.
5. **Do not change the M2 single-human-checkpoint rule.** It is preserved. After M2 the worker runs zero-interaction.
6. **Do not claim a Factor Ledger implementation.** The 81-line design doc is unchanged; `state/implementation_status.md` (already present) keeps reporting 0 code lines until M3 work actually writes them.
7. **Do not lead the paper with "we built a novel calibration method".** The contribution is the settlement contract; calibration is the means.
8. **Do not claim "17 rounds of A/B testing" as a paper sentence.** The directory count is 27, the version range is v02-v16 = 15 versions (PIT-307). The paper must use the count it can defend.
9. **Do not weaken or expand the Gold-H/M/L drift claim without updating `state/calibration_lib_audit.md`.** Three anchors detect a constant offset only (PIT-305).
10. **Do not introduce text-extract Brier inputs into the headline aggregate.** They go in `brier_text_extract_only` separately (PIT-302, DST-15).

## Pitfalls acknowledged (from `experiment-pitfalls.md §4`)

- **PIT-301** — never claim Factor Ledger exists; only `state/implementation_status.md` knows the design-vs-code truth.
- **PIT-302** — headline Brier accepts `numeric | anchor` only; `text-extract` is separate.
- **PIT-303** — single M2 checkpoint; no `level=question` after.
- **PIT-304** — Polymarket pull capped at 5 events/domain until retry/backoff is added.
- **PIT-305** — gold-set audit must record the limit; expand or weaken the claim.
- **PIT-306** — writeback `before.json` is frozen first; `after.json` carries its hash.
- **PIT-307** — directory count, not "17 rounds" claim.
- **PIT-308** — no ANOVA with n<3 per cell; report directional consistency only.

## Cross-references

- `state/io_spec.md` — IO contract produced by this decision
- `wiki/concepts/settlement-calibration-layer.md` — narrative explanation
- `docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md §7` — roadmap source
- `framework/schemas/data-contracts.md §9` — `settlement_record` schema
- `framework/schemas/experiment-pitfalls.md §4` — P1.2 pitfalls
- `docs/autoresearch/2026-07-03-experiment-configuration-plan.md` — orchestration plan
- `state/task_spec.md` — milestones (unchanged in number; reframed in narrative)
- `claude-prompt.md`, `mimo-prompt.md` — entry points updated
- `paper/outline.md` — outline produced by this decision

## Stop condition

This reconfiguration pass ends when `state/io_spec.md`, `wiki/index.md`, `wiki/concepts/settlement-calibration-layer.md`, this decision file, the two prompts, and `paper/outline.md` are written and parseable. After that, the worker waits for the next milestone (M1.5: Brier calculator) to be scheduled.