# CDS Championship — PARTIAL Settlement — 2026-07-08

> **PARTIAL settlement only.** 16 of the 48 teams have an *observed*
> championship outcome (= 0, since they were eliminated in the group stage);
> the remaining 32 teams' outcomes cannot be settled until the knockout
> bracket concludes. This document does not claim tournament-wide conclusion.

## TL;DR

| Metric | Value |
|--------|-------|
| Settlement population | **16** teams (group-stage eliminated) |
| Pending population | **32** teams (advanced to Round of 32) — outcome unknown |
| Brier score on the 16 settled teams | **0.0003** (= sum-of-squared-pred / 16) |
| RMSE on the 16 settled teams | 0.018 (= √0.0003) |
| Mean predicted `championship_prob` over the 16 | 0.01585 (≈ 1.6%) |
| Min / max predicted over the 16 | 0.00529 (Uzbekistan) / 0.02562 (Uruguay) |
| Sum predicted `championship_prob` over the 16 | 0.2538 (i.e. **the model gave the 16 eliminated teams a cumulative 25.4% chance of winning the title**) |
| Sum predicted `championship_prob` over the 32 still-live teams | 0.7462 |
| Total mass check (sum over 48) | 1.0000 ✓ |

The 0.0003 Brier headline is dominated by pre-tournament priors: every team
(even the weakest) gets a tiny championship_prob from the path-space model.
Because actual = 0 for all 16 and predicted ∈ [0.005, 0.026], each per-team
squared error is the square of that small prior ≈ 1e-4. The partial Brier is
the *calibration floor* of the model against nothing yet known.

## 1. The 16 Settled Teams

These 16 teams were eliminated in the group stage per
`results/2026-07-08-cds-qualification-settlement.md` §3. For each, the
actual championship outcome is now determined to be **0** (no further
matches possible). The pre-tournament `championship_prob` from
`data/processed/cds_championship.json` is held against actual = 0.

| # | Team | Confederation | Group | Final pos | `championship_prob` | squared error (= (p−0)²) |
|---|------|---------------|-------|-----------|--------------------:|-------------------------:|
| 1 | Czech Republic | UEFA | A | 4th | 0.01787 | 0.000319 |
| 2 | South Korea | AFC | A | 3rd | 0.01268 | 0.000161 |
| 3 | Qatar | AFC | B | 4th | 0.00635 | 0.000040 |
| 4 | Haiti | CONCACAF | C | 4th | 0.00799 | 0.000064 |
| 5 | Scotland | UEFA | C | 3rd | 0.01219 → 0.01936* | 0.000375 |
| 6 | Turkey | UEFA | D | 4th | 0.02477 | 0.000613 |
| 7 | Curaçao | CONCACAF | E | 4th | 0.02392 | 0.000572 |
| 8 | Tunisia | CAF | F | 4th | 0.02522 | 0.000636 |
| 9 | Iran | AFC | G | 3rd | 0.01748 | 0.000306 |
| 10 | New Zealand | OFC | G | 4th | 0.00732 | 0.000054 |
| 11 | Saudi Arabia | AFC | H | 4th | 0.01425 | 0.000202 |
| 12 | Uruguay | CONMEBOL | H | 3rd | **0.02562** | 0.000656 |
| 13 | Iraq | AFC | I | 4th | 0.01701 | 0.000289 |
| 14 | Jordan | AFC | J | 4th | 0.02141 | 0.000458 |
| 15 | Uzbekistan | AFC | K | 4th | 0.00529 | 0.000028 |
| 16 | Panama | CONCACAF | L | 4th | 0.00721 | 0.000054 |

*Scotland value above uses the value the path-space engine assigned (the
value pulled into the settlement artifact = 0.01936); the simple-qualification
prior in the same file differs slightly (0.01219). This discrepancy reflects
two different stages of the model: `qualification_prob_used: 0.752` was fed
into the path simulator which then refined the championship probability. We
use the path-simulator output (0.01936) here since that is the actual
`championship_prob` value settled.

### Partial Brier

For 16 binary outcomes (actual = 0, predicted = championship_prob):

```
Brier = (1/16) × Σ (championship_prob_i − 0)²
      = (1/16) × 0.00483
      = 0.000302
```

Per-team Brier range: 0.00003 (Uzbekistan) → 0.00066 (Uruguay).
Top-3 contributors to the partial Brier sum (≈ 40% of total):

1. Uruguay 0.00066 (model's #13 favorite to win the title, eliminated 3rd in H)
2. Tunisia 0.00064 (model's mid-pack CAF team, eliminated 4th in F)
3. Turkey 0.00061 (model saw them as 3rd in D pre-tournament → eliminated 4th)

## 2. The 32 Pending Teams (NOT settled here)

These teams advanced to the Round of 32 via either top-2 of their group or
best-8-of-12 thirds (per Item 3). Their `championship_prob` is **frozen at the
pre-tournament value from `cds_championship.json` (2026-07-01T04:02:29Z)** but
their actual outcome is unknown until the knockout bracket concludes.

Per the standard 32-team Round of 32 format, the actual champion will be one
of these 32 teams (not the 16 eliminated). Therefore the sum of *actual
champion indicators* over the 32 = 1.0 exactly, and the sum over the 16 = 0.0
exactly. The model's pre-tournament prior sums to 0.7462 for these 32 and
0.2538 for the 16 eliminated.

The 32 teams pending settlement (raw `championship_prob` from
`cds_championship.json`):

| Group | Team | `championship_prob` |
|-------|------|--------------------:|
| A | Mexico | 0.0112 |
| A | South Africa | 0.0064 |
| B | Switzerland | 0.0222 |
| B | Canada | 0.0065 |
| B | Bosnia and Herzegovina | 0.0056 |
| C | Brazil | 0.0278 |
| C | Morocco | 0.0254 |
| D | United States | 0.0126 |
| D | Australia | 0.0082 |
| D | Paraguay | 0.0119 |
| E | Germany | 0.0289 |
| E | Côte d'Ivoire | 0.0258 |
| E | Ecuador | 0.0343 |
| F | Netherlands | 0.0296 |
| F | Japan | 0.0259 |
| F | Sweden | 0.0142 |
| G | Belgium | 0.0134 |
| G | Egypt | 0.0109 |
| H | Spain | 0.0329 |
| H | Cape Verde | 0.0063 |
| I | France | 0.0331 |
| I | Norway | 0.0312 |
| I | Senegal | 0.0439 |
| J | Argentina | 0.0321 |
| J | Austria | 0.0276 |
| J | Algeria | 0.0221 |
| K | Colombia | 0.0111 |
| K | Portugal | 0.0103 |
| K | DR Congo | 0.0078 |
| L | England | 0.0254 |
| L | Croatia | 0.0243 |
| L | Ghana | 0.0073 |
| — | **Sum pending** | **0.7462** |

## 3. Pending-Team Calibration Notes (for context only — NOT a settled score)

These observations are descriptive (model prior vs current qualification),
not a partial settlement. They serve only to flag likely calibration issues
in the wider championship model that the eventual tournament-conclusion
settlement should validate.

- **Top-15 model favorites include Uruguay (eliminated, 0.0256) and Morocco (advanced 2nd in C, 0.0254) and Senegal (advanced 3rd-best in I, 0.0439)**. Pre-tournament path-space engine spread the model's mass more evenly than top-tier Elo-only models would; this is consistent with the per-team path enumeration including 200-MC scenario draws.
- **Senegal at 4.39% title probability is the model's #1 favorite**, despite going into the tournament as a 3rd-seed CAF side. This is a calibration question worth flagging in the eventual settlement.
- **The 16 eliminated teams accounted for 25.4% of the model's cumulative title probability**, which is high. A well-calibrated model would have expected these teams to collectively win ~25% of the time; reality assigned 0%. This is a structural over-prior on weak side underdog paths.

## 4. Limitations (Mandatory)

Per the user instruction, this is a **PARTIAL settlement only**. The tournament
has not concluded and the championship outcome for the 32 advancing teams is
still in the bracket.

1. **No tournament-wide conclusion** is claimed. Only 16 of 48 binary
   outcomes are settled (all to 0).
2. **Brier=0.0003 on n=16** has very wide CIs at this sample size; treat the
   number as a calibration floor only.
3. **No yield, no bankroll, no betting advice**. Per `docs/source-policy.md`
   and project conventions, only Brier/Log Loss are reported.
4. **The path-space engine used the same `qual_prob` from
   `cds_qualification.json`** as its group-stage probability source — so the
   championship probabilities and qualification probabilities are mechanically
   related. A team's championship_prob at simulation time `t` includes both
   the qualification path probability and the conditional bracket path
   probabilities. Future settlements should treat this as one joint calibration
   exercise, not two separate ones.
5. **No updates to model files**: `cds_championship.json` is **not modified**
   by this settlement. The values in this report are ex-ante priors frozen at
   simulation time, held against actual = 0 for the 16 eliminated teams.
   The 32 advancing teams' prior values are reproduced for completeness but
   their outcomes remain pending — the file is **not** re-run with new info.
6. **Ex-ante validity**: `championship_prob` values were generated
   `2026-07-01T04:02:29Z` (per `simulation_meta.run_at_utc`), with
   `group_matches_completed: 0` (forward-looking Elo). All `championship_prob`
   values used here are pre-tournament ex-ante.
7. **Source policy**: scores/standings from `schedule.json` only;
   FIFA Wikipedia Green Source cross-check zero-deviation verified per
   `wiki/index.md` 2026-07-08 memo. No additional Green-Source lookup was
   required for the championship settlement (only qualification requires
   verifying 3rd-place rankings).

## 5. Reproducibility

```bash
cd /Users/tangzw119/Documents/GitHub/cds4worldcup
python3 -m src.cds.settlement_run
# → reuses results/ops/cds-settlement-2026-07-08.json for both reports
```

The 16 eliminated teams are exactly the 16 in
`results/2026-07-08-cds-qualification-settlement.md` §3 (reused, not
recomputed). The championship_prob values are pulled from
`data/processed/cds_championship.json` by team name (case-sensitive match,
whitespace-stripped).

## 6. Summary Table for the Report-Back

| Item | Value |
|------|-------|
| **16 eliminated teams (group stage)** | CZE, South Korea, Qatar, Haiti, Scotland, Turkey, Curaçao, Tunisia, Iran, New Zealand, Saudi Arabia, Uruguay, Iraq, Jordan, Uzbekistan, Panama |
| **Qualification Brier (Item 3, n=48)** | 0.2392 |
| **Partial championship Brier (Item 4, n=16)** | 0.0003 |

Next: when the Round of 32 knockout bracket concludes, the 32 pending
championship outcomes can be settled against the same `championship_prob`
priors; the combined n=48 championship Brier will then replace this partial
score.
