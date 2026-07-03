# P12 Paper Outline

> Status: skeleton (M7) · 2026-07-03 · exp_id `P12`
> Target: short paper (workshop / findings-style), 4-6 pages.
> Pair with `state/task_spec.md`, `state/io_spec.md`,
> `wiki/concepts/judge-calibration-protocol.md`,
> `wiki/decisions/2026-07-03-p12-configuration.md`.

## Title (working)

> Calibrating LLM Judges for Agent Reliability: Blind Pairwise
> Evaluation, Neighborhood Probes, and Abstention-Aware Scoring

## Authors / venue

- TBD (P12 worker + advisor chain).
- Target venue: workshop track (EMNLP / ACL / NeurAS findings) or
  short paper. Not a main conference.

## Abstract (placeholder — must align with conclusion at submission)

LLM-as-a-judge is the cheapest way to score agent outputs, but three
failure modes are not separated by a single judge: label leakage,
brittle consistency on known-bad answers, and forced scoring on
ambiguous cases. We present a frozen five-protocol evaluation set
(`leaked`, `blind`, `pairwise`, `neighborhood`, `abstention`) that
shares one ordered sample list and reports four metrics
(`mean_score`, `consistency_on_wrong`, `abstain_rate`, `verdict_delta`).
Re-anchoring P11 samples so the condition label is metadata not
prompt content, we show that at least one of H1 / H1c / H3 / F1
flips when the four non-leaked protocols are applied together. The
contribution is the protocol set, not a leaderboard.

## 1. Introduction

- Agents need a judge. Single judges fail in three measurable ways
  (cite PIT-101, PIT-102, PIT-103).
- The community responds with calibration, but most calibration
  papers test the judge on the producer's own confidence (DST-10,
  PIT-013). That is a confound.
- We argue for a *decomposed* protocol set and pre-registration, and
  we instantiate it on P11's H1 / H1c / H3 / F1 chain.

## 2. Related Work

- LLM-as-judge literature (Zheng et al. 2023; later surveys).
- NCB and neighborhood-style robustness.
- LLM judge calibration and abstention (cite per data-contracts §1
  and `task_spec.md` §"Quality Gates" G1).
- Avoid HARKing (PIT-006): cite only verified sources, with
  `source_path` recorded in the figure script.

## 3. Method

- 3.1 The five protocols: definitions, `awareness` values, required
  fields. Cross-ref `wiki/concepts/judge-calibration-protocol.md` §2.
- 3.2 The four metrics: formulas and thresholds. Cross-ref §3 of the
  concept page.
- 3.3 Sample re-anchoring: how P11 samples are imported with
  `condition_visible_to_judge: false` (PIT-105).
- 3.4 Pre-registration: `state/experiment_design.md` is frozen
  before the first judge call (PIT-006). The four pre-registered
  hypotheses are H1, H1c, H3, F1 (concept page §4).

## 4. Results

- 4.1 Leakage reproduction (M2). Show the leaked-vs-blind
  `verdict_delta` table.
- 4.2 Pairwise blind (M3). Show `consistency_on_wrong` per cell;
  flag any cell with `consistency_on_wrong > 0.5` (PIT-102).
- 4.3 Neighborhood (M5). Show per-axis effect sizes; flag any probe
  that mutates more than one axis (PIT-104).
- 4.4 Abstention (M5). Show `abstain_rate` per cell; flag any cell
  with `ambiguous_count > 0` and `abstain_rate == 0` (PIT-103).
- 4.5 Calibration metrics table (M6). One row per
  `(hypothesis, protocol)`. Mark cells with `n < 30` (PIT-007).

## 5. Discussion

- What flips and what does not. Which protocol carries the
  explanatory weight.
- The cost: a 5× judge budget vs a single judge. Justified by the
  decomposed failure modes.
- Limitations: reused P11 samples, single-language, single-domain.
  No claim to a universal judge.

## 6. Limitations

- Pre-registered on P11 hypotheses; not a general judge benchmark.
- Sample size per cell may be < 30; we say so in every row.
- Review diversity (PIT-107) is a soft constraint when the worker
  has access to only one model.

## 7. Reproducibility

- All artefacts under `experiments/`. Validators in
  `state/io_spec.md` §7. Pre-registration in
  `state/experiment_design.md`. Logs in `logs/`.
- Citation verification protocol (PIT-001): every numeric / citation
  claim in the paper points to a `source_path` recorded in the
  figure script.

## 8. Ethics / Use

- No human subjects beyond already-collected P11 data. P12 has zero
  human checkpoints (PIT-011).
- No PII processing beyond the P11 sample set.

## Figures / Tables (Gate 4)

- Table 1 — Per-protocol results per (H, protocol) cell with `n`.
- Table 2 — `consistency_on_wrong` per (H, protocol) cell.
- Figure 1 — `verdict_delta` from leaked to blind/pairwise/...
- Figure 2 — `abstain_rate` per cell, with `ambiguous_count`.

## Related deliverables

- `state/task_spec.md` — milestones and success criteria.
- `state/io_spec.md` — schemas and validators.
- `experiments/calibration_metrics.md` — the data behind Table 1/2
  and Figure 1/2.
- `paper/review_round_1.md` — five-persona review at M8.
