# Judge Calibration Protocol

> Concept page · 2026-07-03 · exp_id `P12`
> Pair with `../../../../framework/schemas/data-contracts.md` §6-7 and
> `../../../../framework/schemas/experiment-pitfalls.md` §2.

## 1. Problem statement

P11 measured role-conditioned LLM behaviour with a single judge that
saw the condition label. Three pathologies followed:

1. **Label leakage** — the judge used `inner_monologue / no_think /
   pure_analysis` as a feature, inflating effect sizes.
2. **Brittle consistency** — paraphrases of a known-bad answer kept
   high scores because consistency was reported unconditional on
   correctness.
3. **Silent abstention** — the judge was forced to score every sample
   even when the question was ambiguous, so noisy outputs were
   averaged into the verdict.

P12 fixes this with a **frozen five-protocol** evaluation set run on
the same ordered sample list. The contribution is the protocol set
and the metrics that come out of it, not a new benchmark.

## 2. The five protocols

All five protocols share one `sample_ids_ordered` list (PIT-106). All
five emit rows of the `judge_protocol_result` shape (data-contracts §7).

| # | Protocol | `awareness` | What the judge sees | Required fields |
|---|----------|-------------|---------------------|-----------------|
| 1 | `leaked` | `leaked` | Original P11 output **and** the condition label. | `score`, `score_band` |
| 2 | `blind` | `blind` | Original P11 output with the condition label stripped. `condition_visible_to_judge: false` in the manifest. | `score`, `score_band` |
| 3 | `pairwise` | `pairwise` | Two outputs for the same `sample_id`; judge returns a preference + confidence. | `paraphrase_id`, `ground_truth_correctness`, `consistency_on_wrong` |
| 4 | `neighborhood` | `blind` | A probe that mutates exactly one axis of the original. | `axis: role|fact|consequence`, original `sample_id` referenced |
| 5 | `abstention` | `blind` | Judge may return `abstain: true` with a non-empty `abstain_reason`. | `abstain`, `abstain_reason` |

## 3. The five metrics

The metrics all live in `experiments/calibration_metrics.md` (M6) and
are reported per `(hypothesis, protocol)` cell.

| Metric | Formula | Threshold for "calibrated" |
|--------|---------|----------------------------|
| `mean_score` | mean of `score` over the cell | n/a — for context |
| `consistency_on_wrong` | `mean(score | not correct)` | ≤ 0.5 (PIT-102) |
| `abstain_rate` | `count(abstain=true) / n` | > 0 on any cell with `ambiguous_count > 0` (PIT-103) |
| `verdict_delta` | `verdict(protocol) - verdict(leaked)` | reported; sign and magnitude interpreted against the hypothesis |
| `effect_size` | Cohen's d on score, or `n` with bootstrap CI | needs `n ≥ 30` per cell (PIT-007) |

The headline claim of P12 is whether `verdict_delta` flips the
leaked-protocol conclusion for at least one of `H1, H1c, H3, F1` after
applying blind + pairwise + neighborhood + abstention together.

## 4. The four hypotheses under test

| id | Original P11 claim | What P12 actually tests |
|----|--------------------|--------------------------|
| H1 | inner_monologue beats no_think | Does the leaked-vs-blind verdict_delta flip? |
| H1c | inner_monologue beats no_think on reasoning depth | Does pairwise consistency-on-wrong survive blind re-anchoring? |
| H3 | risk_tolerance → risk-taking shift is robust | Do neighborhood probes on `consequence` axis keep the verdict stable? |
| F1 | pure_analysis beats inner_monologue on group emergence vocab | Does the abstention rate on ambiguous group-emergence questions change the verdict? |

H1 is the canonical label-leakage case (PIT-101). H1c is the canonical
consistency-on-wrong case (PIT-102). H3 is the canonical neighborhood
case (PIT-104). F1 is the canonical abstention case (PIT-103).

## 5. Why five, not one

A single judge cannot separate leakage from consistency from abstention.
The protocol set is **decomposed** so that each pathology is tested
by exactly one protocol:

- `leaked → blind` separates the leakage component.
- `blind → pairwise` (with `ground_truth_correctness` conditioning)
  separates the consistency component.
- `blind → neighborhood` (with single-axis mutation) separates the
  generalisation component.
- `blind → abstention` (with `abstain_rate` and `abstain_reason`
  quality) separates the forced-scoring component.

Reporting only `leaked` and `blind` (PIT-106) hides the latter two
failure modes; reporting all five on the same ordered sample list makes
the contributions additive.

## 6. Cross-protocol invariants

These are checked by the validator (io_spec §7).

- All five result files share the same `sample_ids_ordered` (PIT-106).
- Every row carries `judge_id` and `judge_id != "self"` (PIT-013, DST-10).
- `abstain=true` ⇒ `abstain_reason` non-empty (PIT-103, DST-8).
- `protocol: neighborhood` ⇒ `axis` non-null and in enum (PIT-104, DST-?).
- Every imported P11 sample row has `condition_visible_to_judge: false`
  (PIT-105, DST-9).

## 7. Cross-references

- `state/io_spec.md` — exact validator commands and required fields.
- `state/task_spec.md` — milestones and success criteria.
- `../../../../framework/schemas/data-contracts.md` §6-7 — schema.
- `../../../../framework/schemas/experiment-pitfalls.md` §2 — trap ids.
- `../../docs/roadmaps/2026-07-03-topic5-autoresearch-roadmap.md` §5
  — the P12 fast-paper route that this protocol set implements.
- `wiki/decisions/2026-07-03-p12-configuration.md` — why this
  protocol set was chosen.
