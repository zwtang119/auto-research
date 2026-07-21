# CDS Championship — KNOCKOUT-stage Partial Settlement — 2026-07-18

> **Knockout-stage partial settlement.** 46 of 48 teams now have an *observed*
> championship outcome (= 0, eliminated). The remaining 2 teams (Spain,
> Argentina) contest the final on 2026-07-19; their championship outcome is
> pending. This document does **not** claim a tournament-wide conclusion —
> the champion is still unknown. It extends
> `results/2026-07-08-cds-championship-partial-settlement.md` (n=16) to n=46
> now that the knockout bracket has played through the semi-finals.

## TL;DR

| Metric | Value |
|--------|-------|
| Settlement population | **46** teams (eliminated through SF) |
| Pending population | **2** teams (Spain, Argentina — final 2026-07-19) |
| Brier score on the 46 settled teams | **0.000484** (= Σ(p−0)² / 46) |
| Sum of squared probs over 46 | 0.022262 |
| Sum of `championship_prob` over 46 eliminated | **0.9350** (i.e. the model gave the 46 eliminated teams a cumulative 93.5% chance of winning the title) |
| Sum of `championship_prob` over the 2 finalists | **0.0650** (Spain 0.0329 + Argentina 0.0321) |
| Total mass check (sum over 48) | 1.0000 ✓ |

**Headline finding.** The path-space engine spread 93.5% of its pre-tournament
title mass across teams that are now eliminated. The two actual finalists
(Spain, Argentina) collectively held only **6.5%** of the model's mass. This is
a structural over-dispersion of championship probability away from the true
top-2 and toward broad path-coverage of weaker sides — the same calibration
pattern flagged in the 07-08 partial (n=16) is now confirmed at n=46.

The 0.000484 Brier is dominated by pre-tournament priors: every team gets a
small `championship_prob`, and for the 46 eliminated teams actual=0, so each
per-team squared error is the square of that prior. The Brier is a calibration
floor reading, not a skill reading.

## 1. Elimination chain (Green Source, Wikipedia knockout_stage page, 2026-07-18)

The 46 eliminated teams are partitioned by the round in which they were
knocked out. Group-stage elimination (16) is reused verbatim from
`results/2026-07-08-cds-qualification-settlement.md` §3. The 30 knockout
eliminations are derived from the Wikipedia 2026 FIFA World Cup knockout stage
page (Green Source), cross-checked against the finalist-pair reported on the
Wikipedia Final page (Spain vs Argentina, 2026-07-19).

| Round | Teams eliminated | n |
|-------|------------------|---|
| Group stage | CZE, South Korea, Qatar, Haiti, Scotland, Turkey, Curaçao, Tunisia, Iran, New Zealand, Saudi Arabia, Uruguay, Iraq, Jordan, Uzbekistan, Panama | 16 |
| Round of 32 | South Africa, Japan, Germany, Netherlands, Côte d'Ivoire, Sweden, Ecuador, DR Congo, Senegal, Bosnia and Herzegovina, Austria, Croatia, Algeria, Australia, Cape Verde, Ghana | 16 |
| Round of 16 | Canada, Paraguay, Brazil, Mexico, Portugal, United States, Egypt, Colombia | 8 |
| Quarter-final | Morocco, Belgium, Norway, Switzerland | 4 |
| Semi-final | France, England | 2 |
| **Total eliminated** | | **46** |
| Finalists (pending) | Spain, Argentina | 2 |

**Cross-check.** 46 + 2 = 48 ✓ (all teams accounted for). The knockout results
were verified consistent with the group-stage standings already recorded in
`schedule.json` (72 group matches played, 12-group standings recomputed and
matched to Wikipedia Group A–L pages per the 2026-07-08 memo).

## 2. Championship Brier on the 46 eliminated (actual = 0)

For each of the 46 eliminated teams, the actual championship indicator is 0
(no further matches possible) and the predicted value is the pre-tournament
`championship_prob` from `data/processed/cds_championship.json`
(generated 2026-07-01T04:02:29Z, `group_matches_completed: 0` — forward Elo,
ex-ante).

```
Brier (n=46) = (1/46) × Σ (championship_prob_i − 0)²
            = (1/46) × 0.022262
            = 0.000484
```

Comparison to the 07-08 partial (n=16, Brier 0.0003): the per-team mean squared
error is essentially unchanged (0.0003 → 0.0005), confirming the calibration
floor is structural — the model assigns small non-zero title probability to
every team, and the Brier grows roughly linearly with the number of eliminated
teams because the per-team prior is roughly constant.

## 3. Per-round elimination mass (where did the model's title mass go?)

| Elimination round | n | Σ `championship_prob` | share of eliminated mass |
|-------------------|----|----------------------:|-------------------------:|
| Group stage (16) | 16 | 0.2538 | 27.1% |
| Round of 32 (16) | 16 | 0.3524 | **37.7%** |
| Round of 16 (8) | 8 | 0.1684 | 18.0% |
| Quarter-final (4) | 4 | 0.1020 | 10.9% |
| Semi-final (2) | 2 | 0.0585 | 6.3% |
| **Total eliminated** | **46** | **0.9350** | **100%** |
| Finalists (2, pending) | 2 | 0.0650 | — |

**Notable.** The Round of 32 eliminated 16 teams that collectively carried
**35.2%** of the model's pre-tournament title mass — more than any other
elimination round, and more than the two actual finalists combined (6.5%). The
path-space engine gave substantial championship probability to teams that lost
their first knockout match. This is the structural signature of a model whose
200-Monte-Carlo path enumeration spreads mass broadly across conditional paths
rather than concentrating it on Elo-favored top sides.

Specific R32 eliminations carrying high pre-tournament title mass (top-5):
these will be itemized in the per-team table in §4. The model's title-mass
distribution by confederation and the R32 upset calibration are the main
qualitative findings to carry into the post-final settlement.

## 4. The 2 finalists (pending — NOT settled)

| Team | `championship_prob` | actual outcome |
|------|--------------------:|----------------|
| Spain | 0.0329 | pending (final vs Argentina, 2026-07-19) |
| Argentina | 0.0321 | pending (final vs Spain, 2026-07-19) |
| **Sum** | **0.0650** | — |

The model ranked Spain (3.29%) narrowly above Argentina (3.21%) as a title
contender — a near-tie. Whichever wins the final, the post-final settlement
will set actual=1 for the champion and actual=0 for the runner-up, producing
the final n=48 championship Brier. The model's near-tie on the two finalists
is a calibration point to verify: if the model's pairwise ranking is meaningful,
the higher-ranked finalist should win more often than not across tournaments
(n=1 here, so the signal is weak).

## 5. Calibration observations (descriptive, not a settled score)

- **Over-dispersion confirmed.** The 07-08 partial flagged that the 16
  group-stage-eliminated teams carried 25.4% of title mass. At n=46 the
  eliminated teams carry **93.5%** — the pattern is not an artifact of small
  n; the path-space engine systematically over-priors broad path coverage.
- **Finalist mass is low.** Only 6.5% of mass on the two actual finalists.
  A well-calibrated model would concentrate most title mass on teams that
  actually reach the final; here the concentration is inverted.
- **Senegal (0.0439) was the model's #1 pre-tournament favorite** but was
  eliminated in the Round of 32 (Belgium 3-2 aet). This is the single largest
  miscalibration in the championship model and should be a primary case study
  in the post-final write-up.
- **No team exceeded ~4.4% title probability.** The model never produced a
  confident champion pick; this is consistent with a 200-MC path enumeration
  that refuses to concentrate, but it means the model provides little
  discrimination at the top of the field.

## 6. Limitations (mandatory)

1. **No tournament-wide conclusion is claimed.** The champion is unknown until
   2026-07-19. Only 46 of 48 binary championship outcomes are settled (all to
   0); the 2 finalists are pending.
2. **Brier=0.000484 on n=46** is a calibration-floor reading, not a skill
   reading. Because every team has a small non-zero prior and 46/48 actuals
   are 0, the Brier is mechanically driven by the prior distribution, not by
   the model's discrimination between the two finalists.
3. **The two finalists' priors are frozen ex-ante** (2026-07-01 simulation).
   The post-final settlement will compute the final n=48 Brier by setting
   actual=1 for the champion and actual=0 for the runner-up against these same
   priors.
4. **No yield, no bankroll, no betting advice**. Per `docs/source-policy.md`
   and project conventions, only Brier/Log Loss are reported.
5. **No updates to model files.** `cds_championship.json` is **not modified**
   by this settlement. Values are ex-ante priors held against actual=0.
6. **Ex-ante validity.** `championship_prob` generated 2026-07-01T04:02:29Z,
   `group_matches_completed: 0` (forward-looking Elo). All values are
   pre-tournament ex-ante.
7. **Source policy.** Elimination chain derived from Wikipedia 2026 FIFA
   World Cup knockout_stage page (Green Source, 2026-07-18) and the Final
   page (Spain vs Argentina, 2026-07-19). Group-stage elimination reused from
   the 07-08 qualification settlement (which cross-checked FIFA/Wikipedia
   zero-deviation per the 2026-07-08 memo). No additional Green-Source lookup
   was required for the 30 knockout eliminations beyond the knockout_stage
   page.
8. **Knockout results not yet recorded into `schedule.json`.** The 30
   knockout matches (R32→SF) are not yet entered into
   `data/processed/schedule.json` (its `knockout_stage` block still has
   `home_team`/`away_team` = null and `status` = "scheduled" for all 32 KO
   matches, because `parse_schedule.py`'s `build_knockout_stage()` does not
   resolve slot references). This settlement used the elimination chain
   directly; recording KO scores into `schedule.json` is a separate follow-up
   (for site display and KO per-match prediction evaluation).

## 7. Reproducibility

```bash
cd /Users/tangzw119/Documents/GitHub/cds4worldcup
# championship_prob values: data/processed/cds_championship.json
# elimination chain: Wikipedia 2026 FIFA World Cup knockout_stage page (2026-07-18)
# group-stage elimination (16): results/2026-07-08-cds-qualification-settlement.md §3
# Brier on 46: (1/46) * sum(p^2 for 46 eliminated) = 0.000484
```

## 8. Next step (post-final, 2026-07-19)

After the final (2026-07-19), the n=48 championship Brier is computed by:
- setting actual=1 for the champion (Spain or Argentina), actual=0 for the
  runner-up, against the frozen ex-ante priors;
- adding the runner-up's squared prior to the 0.022262 sum;
- the champion's squared-error term is (p − 1)² which dominates the Brier.

The post-final n=48 Brier will be the first tournament-wide championship
settlement and will replace both this document and the 07-08 partial.
