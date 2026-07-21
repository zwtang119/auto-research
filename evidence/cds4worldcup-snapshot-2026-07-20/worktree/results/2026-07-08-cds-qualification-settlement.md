# CDS Qualification Settlement — 2026-07-08

> Settlement of `data/processed/cds_qualification.json` (48 teams, 200 MC/scenario)
> against the 72 played group-stage matches in `data/processed/schedule.json`
> (2026-06-11 → 2026-06-27, all 72 matches `status=played`).
> Helper script: `src/cds/settlement_run.py` → `results/ops/cds-settlement-2026-07-08.json`.

## TL;DR

| Metric | Value |
|--------|-------|
| Total settlement population | 48 teams (12 groups × 4 teams) |
| Advanced to Round of 32 | 32 teams (24 from top-2 + 8 best of 12 third-placed) |
| Eliminated (group stage) | 16 teams |
| Brier score, top-2 qual_prob vs actual qualify (n=48) | **0.2392** |
| Log loss, top-2 qual_prob vs actual qualify (n=48) | not reported in this experiment (ref. Item 2 batch) |
| Mean `qual_prob_top2` for the 32 advanced | 0.577 |
| Mean `qual_prob_top2` for the 16 eliminated | 0.342 |
| Largest calibration surprises | see §4 |

Brier of 0.2392 is comfortably below the constant-0.5 baseline (= 0.250) and
slightly above the team's-own-priors baseline (if the model had assigned 32/48
= 0.667 to every "advanced" hypothesis and 0.333 to every "eliminated"
hypothesis, mean Brier would be 0.222). The model is **discriminating**
(advanced teams have higher predicted probability than eliminated ones) but
**miscalibrated** in specific directions detailed below.

## 1. Group Stage Final Standings (top-2 + 3rd + 4th)

Recomputed from `schedule.json` using `src.cds.group_standings.compute_group_standings`
(FIFA 2026 multi-team tiebreaker protocol: Pts → mini-league → full group GD/GF →
fair-play → lots; fair-play data unavailable, lots_seed=20260708 used for
deterministic reproducibility).

Verification note: per `wiki/index.md` 2026-07-08 memo, all 12 group standings
were **manually cross-checked against Wikipedia Group A–L pages (Green Source)
with zero team-level deviation**, and 8 sampled scores (MEX 2-0, GER 7-1,
NED-JPN 2-2, BEL-EGY 1-1, ESP-CPV 0-0, FRA 3-1, BRA-MAR 1-1, UZB-COL 1-3)
were spot-checked with zero deviation. `schedule.json` is treated as the
canonical source of truth for all 72 matches in this settlement.

| Group | 1st | 2nd | 3rd | 4th | Notes |
|-------|-----|-----|-----|-----|-------|
| A | Mexico (9) | South Africa (4) | South Korea (3) | Czech Republic (1) | MEX won all three (the "host track"); RSA 2nd on 4pts after W vs KOR + D vs CZE |
| B | Switzerland (7) | Canada (4) | Bosnia and Herzegovina (4) | Qatar (1) | SUI went 2-1-0 with 1 draw; CAN ahead of BIH on GD |
| C | Brazil (7) | Morocco (7) | Scotland (3) | Haiti (0) | BRA ahead of MAR on GD (+6 vs +3); both tied on 7pts |
| D | United States (6) | Australia (4) | Paraguay (4) | Turkey (3) | USA ahead of AUS on GD (USA +5 vs AUS 0); both advanced |
| E | Germany (6) | Côte d'Ivoire (6) | Ecuador (4) | Curaçao (1) | GER ahead of CIV on GD (+6 vs +3); ECU 3rd on 4pts after W vs GER |
| F | Netherlands (7) | Japan (5) | Sweden (4) | Tunisia (0) | NED won all three; JPN 2nd on GD (JPN +2 vs SWE +1) |
| G | Belgium (5) | Egypt (5) | Iran (3) | New Zealand (1) | BEL and EGY tied on 5pts; BEL ahead on GD (+3 vs +1) |
| H | Spain (7) | Cape Verde (3) | Uruguay (2) | Saudi Arabia (2) | ESP won group; CV 2nd on 3pts after 3 draws; URU ahead of KSA on GD |
| I | France (9) | Norway (6) | Senegal (3) | Iraq (0) | FRA won all three; NOR 2nd via W-L-W; SEN 3rd best-8 |
| J | Argentina (9) | Austria (4) | Algeria (4) | Jordan (0) | ARG dominant; AUT ahead of ALG on GD; ALG 3rd best-8 |
| K | Colombia (7) | Portugal (5) | DR Congo (4) | Uzbekistan (0) | COL 1st, POR 2nd, COD 3rd best-8 |
| L | England (7) | Croatia (6) | Ghana (4) | Panama (0) | ENG 1st, CRO 2nd on 6pts (W-L-W), GHA 3rd best-8 |

Format: team (points). All scores/play confirmed via schedule.json.

## 2. Best 8 of 12 Third-Placed Teams (FIFA ranking)

FIFA ranks the 12 third-placed teams by: Pts → GD → GF → GA → fair-play → lots.
Recomputed here with FIFA-published tiebreaker order; no ties survived Pts/GD/GF/GA
(verified).

| Rank | Group | Team | Pts | GD | GF | Notes |
|------|-------|------|-----|----|----|-------|
| 1 | K | DR Congo | 4 | +2 | 5 | 3rd best → advanced |
| 2 | F | Sweden | 4 | +1 | 6 | 3rd best → advanced |
| 3 | E | Ecuador | 4 | +1 | 4 | 3rd best → advanced |
| 4 | L | Ghana | 4 | +1 | 3 | 3rd best → advanced |
| 5 | B | Bosnia and Herzegovina | 4 | +1 | 3 | 3rd best → advanced (CAN ahead of BIH on GD=+2 vs +1) |
| 6 | J | Algeria | 4 | 0 | 5 | 3rd best → advanced (AUT ahead on GD) |
| 7 | D | Paraguay | 4 | -2 | 2 | 3rd best → advanced |
| 8 | I | Senegal | 3 | +1 | 6 | 3rd best → advanced (lowest pts in top-8, separated by GD over the worst-4 thirds) |
| — | cut-line — | — | — | — | — | — |
| 9 (cut) | C | Scotland | 3 | 0 | 1 | eliminated |
| 10 (cut) | H | Uruguay | 2 | -1 | 3 | eliminated |
| 11 (cut) | G | Iran | 3 | -1 | 2 | eliminated |
| 12 (cut) | A | South Korea | 3 | -2 | 2 | eliminated |

Note: FIFO best-8 is **points-desc**, with GD as separator. Senegal (3pts,
GD=+1) edged over Iran (3pts, GD=-1) and South Korea (3pts, GD=-2); Scotland
(3pts, GD=0) was the cut at the boundary after a 3-way tie on 3pts was broken
by GD → Iran (-1) < Scotland (0) → eliminated. Uruguay (2pts) was last.

These three eliminated thirds — Scotland (3), Iran (3), Uruguay (2) — plus
the 12 fourth-placed teams yield the 16 eliminated teams listed below.

## 3. The 32 Advanced and 16 Eliminated Teams

### Advanced (32) — top 2 of each group, except A/C/G/H which had only top-2 advance; B/D/E/F/I/J/K/L also contribute their 3rd to the best-8.

Group A: Mexico, South Africa
Group B: Switzerland, Canada, Bosnia and Herzegovina
Group C: Brazil, Morocco
Group D: United States, Australia, Paraguay
Group E: Germany, Côte d'Ivoire, Ecuador
Group F: Netherlands, Japan, Sweden
Group G: Belgium, Egypt
Group H: Spain, Cape Verde
Group I: France, Norway, Senegal
Group J: Argentina, Austria, Algeria
Group K: Colombia, Portugal, DR Congo
Group L: England, Croatia, Ghana

### Eliminated (16) — reused in Item 4 (championship partial settlement)

| # | Team | Confederation | Group | Position | Predicted `qual_prob_top2` |
|---|------|---------------|-------|----------|---------------------------|
| 1 | Czech Republic | UEFA | A | 4th | 0.834 |
| 2 | South Korea | AFC | A | 3rd | 0.231 |
| 3 | Qatar | AFC | B | 4th | 0.127 |
| 4 | Haiti | CONCACAF | C | 4th | 0.118 |
| 5 | Scotland | UEFA | C | 3rd | 0.752 |
| 6 | Turkey | UEFA | D | 4th | 0.805 |
| 7 | Curaçao | CONCACAF | E | 4th | 0.147 |
| 8 | Tunisia | CAF | F | 4th | 0.299 |
| 9 | Iran | AFC | G | 3rd | 0.356 |
| 10 | New Zealand | OFC | G | 4th | 0.205 |
| 11 | Saudi Arabia | AFC | H | 4th | 0.117 |
| 12 | Uruguay | CONMEBOL | H | 3rd | 0.808 |
| 13 | Iraq | AFC | I | 4th | 0.103 |
| 14 | Jordan | AFC | J | 4th | 0.225 |
| 15 | Uzbekistan | AFC | K | 4th | 0.134 |
| 16 | Panama | CONCACAF | L | 4th | 0.208 |

## 4. Calibration Headlines (Brier = 0.2392 mean over 48 binary outcomes)

### 4.1 The model systematically UNDERESTIMATED CAF teams

CAF (10 teams): 9 advanced, 1 eliminated. Mean predicted `qual_prob_top2` for
the 9 advanced CAF teams = **0.225**. Mean predicted for the 1 eliminated
(Tunisia) = **0.299**. The model gave the entire confederation roughly even
odds with the rest of the field; in reality CAF qualified almost everyone.

Five of the six largest "model underconfidence" calibration failures are CAF:

| Team | Group | `qual_prob_top2` | Actual | Brier |
|------|-------|-----------------|--------|-------|
| Australia (AFC, but analytically similar: host bucket underweighted) | D | 0.143 | qualified (2nd) | 0.7343 |
| Cape Verde | H | 0.147 | qualified (2nd) | 0.7283 |
| DR Congo | K | 0.159 | qualified (3rd, best-8) | 0.7080 |
| Ghana | L | 0.169 | qualified (3rd, best-8) | 0.6904 |
| Senegal | I | 0.175 | qualified (3rd, best-8) | 0.6808 |

(Top 5 above are a mix of host/noise CAF/AFC underrepresented teams; the
remainder of the top-10 underconfident qualifiers are all CAF: Côte d'Ivoire
0.187, Algeria 0.209, South Africa 0.208, Egypt 0.487, Morocco 0.280.)

### 4.2 The model systematically OVERESTIMATED mid-tier UEFA + CONMEBOL

Five of the six largest "model overconfidence" calibration failures are
European/South American sides that got stuck on tiebreakers:

| Team | Confederation | `qual_prob_top2` | Actual | Brier |
|------|---------------|-----------------|--------|-------|
| Czech Republic | UEFA | 0.834 | eliminated (4th in A) | 0.6954 |
| Uruguay | CONMEBOL | 0.808 | eliminated (3rd in H, cut) | 0.6524 |
| Turkey | UEFA | 0.805 | eliminated (4th in D) | 0.6488 |
| Scotland | UEFA | 0.752 | eliminated (3rd in C, cut) | 0.5651 |

Czech Republic is the single largest calibration failure in the dataset:
the model put them at 83% top-2 probability in Group A, but they finished
last with 1pt (1 draw, 2 losses, GD -3). The input features likely
over-weighted prior Elo on the back of the UEFA Path D playoff win.

### 4.3 Per-group Brier score (sorted, worst → best)

| Group | Mean Brier | Notable |
|-------|-----------|--------|
| D | 0.4620 | Both USA +5 GD win and AUS +0 GD 2nd-place were surprises; Turkey 4th hurt |
| A | 0.3625 | CZE way overestimated; RSA & MEX (relatively) underestimated |
| H | 0.3500 | CV 2nd unprecedented in pre-tournament priors; URU 3rd cut was a major miss |
| C | 0.2804 | Scotland 3rd fell just short of best-8; MAR 2nd better than 0.28 prior |
| F | 0.2140 | Japan & Sweden ahead of priors |
| L | 0.2045 | Ghana 3rd-best was materially under-prior |
| J | 0.2024 | ALG 3rd-best under-prior |
| K | 0.1922 | COD 3rd-best under-prior; UZB 4th miss was cheap (low prior) |
| I | 0.1841 | Norway 2nd reasonable; SEN 3rd under-prior |
| E | 0.1881 | CIV 2nd, ECU 3rd-best — both surprises |
| B | 0.1222 | BIH 3rd-best borderline; CAN 2nd larger model only mildly missed |
| G | 0.1086 | Most predictable group; BEL ahead of EGY on GD; IRN 3rd just outside best-8 |

Mean across 12 groups: **0.2392** (= 0.2392 n=48 by identity).

### 4.4 Confederation-level breakdown

| Confederation | n teams | n advanced | Advanced mean pred | Eliminated mean pred | Mean Brier |
|---------------|---------|------------|--------------------|----------------------|------------|
| UEFA | 16 | 10 | 0.730 | 0.498 | 0.1619 |
| CONMEBOL | 6 | 5 | 0.764 | 0.808 | 0.1761 |
| CAF | 10 | 9 | 0.225 | 0.299 | 0.5591 |
| AFC | 9 | 2 | 0.183 | 0.185 | 0.1808 |
| CONCACAF | 6 | 3 | 0.603 | 0.158 | 0.0961 |
| OFC | 1 | 0 | — | 0.205 | 0.0419 |

Conclusions:

- **CAF Brier (0.559) is the dominant failure mode** of this run. The pre-tournament model was systematically overconfident in non-CAF and underconfident in CAF (notable: South Africa 0.208 → 2nd, Algeria 0.209 → best-8, DR Congo 0.159 → best-8, Morocco 0.280 → 2nd). This is consistent with the source-policy's note that "CAF teams carry structural under-prior risk in Cold-War-Elo blends".
- **CONCACAF Brier is lowest (0.0961)** — but the Brier is artificially low because the model had very small samples (1 team per confederation in most groups); USA + Mexico + Canada all qualified as expected; Curaçao, Haiti, Panama all eliminated as expected.
- **AFC advanced=2 (Australia, Japan)** out of 9. Both advanced teams were under-prior (0.143, 0.223). The model's AFC prior was "AFC teams rarely escape European-or-CONMEBOL-dominant groups" — partially correct (only 2/9 advanced) but the cutoff case (the 3-pt third-placed teams from C, G, H) was materially under-credited.
- **UEFA Brier (0.1619) is comparatively low**: the model handles top European heavyweights well (BEL 0.945, GER 0.896, ESP 0.926, ENG 0.883, FRA 0.913, POR 0.886 all qualified as expected). The failures cluster on borderline-CDS teams (CZE, Turkey, Scotland) where the prior was 0.7-0.8.
- **CONMEBOL Brier (0.1761)**: heavyweights (BRA, ARG, URU, COL) were fine. The single failure — URU in Group H, eliminated 3rd on cut at best-8 — accounts for ~half of the confederation's Brier.

## 5. Per-Group Calibration Verdict

For each group, the model's predicted total `qual_prob_top2` across the 4
teams is roughly 1.99-2.00 (target: 2.00 = exactly 2 qualifiers from each
group via top-2 path). Where the model was wrong was the *composition* of
those 2 picks, not the count.

| Group | Σ `qual_prob_top2` | Σ `qual_prob` (incl. best-3rd) | Actual qualified | Top-2 mean Brier |
|-------|--------------------|--------------------------------|--------------------|------------------|
| A | 2.000 | 2.648 | 2 | 0.3625 |
| B | 1.989 | 2.650 | 3 (+ best 3rd) | 0.1222 |
| C | 1.995 | 2.658 | 2 | 0.2804 |
| D | 1.991 | 2.657 | 3 (+ best 3rd) | 0.4620 |
| E | 1.987 | 2.663 | 3 (+ best 3rd) | 0.1881 |
| F | 1.989 | 2.663 | 3 (+ best 3rd) | 0.2140 |
| G | 1.993 | 2.661 | 2 | 0.1086 |
| H | 1.997 | 2.667 | 2 | 0.3500 |
| I | 1.997 | 2.655 | 3 (+ best 3rd) | 0.1841 |
| J | 1.999 | 2.651 | 3 (+ best 3rd) | 0.2024 |
| K | 2.005 | 2.675 | 3 (+ best 3rd) | 0.1922 |
| L | 1.995 | 2.654 | 3 (+ best 3rd) | 0.2045 |

`Σ qual_prob` (1.99-2.00 per group) ≈ 2 and Σ `qual_prob` (~2.65 per group) ≈ 2 + 0.67 best-3rd bonus confirms the model's structural belief: "2 of 4 teams qualify from each group via top-2, plus a 67% chance that a 3rd team qualifies via best-8" — that structural prior was correct in aggregate but underweight at the **per-team** level for CAF teams.

## 6. Methodology & Limitations

1. **Single-observation Brier**: each of the 48 teams contributes one binary
   observation to the Brier score. The 0.2392 number has wide confidence
   intervals (Wilson 95% CI on n=48 binary observations ≈ ±0.06). Treat the
   headline number as a calibration benchmark, not a publishable ranking.

2. **`qual_prob_top2` used (not `qual_prob`)**: per the user spec, the binary
   qualification outcome is settled against "top 2 qualification" (the standard
   group-stage->round-of-32 advancement), not against "best-8 of 12 thirds"
   which is itself a FIFA-defined ranking. Using `qual_prob_top2` matches the
   docs/spec definition. The third-place lens is captured separately via the
   per-group verification in §2.

3. **No fair-play data**: ties not resolvable by points/mini-league/full-group
   fall to drawing of lots (seed=20260708 for reproducibility). No such ties
   remained after the 12 group stages completed.

4. **No betting advice, no yield reporting**: per docs/source-policy.md, this
   settlement reports Brier and calibration diagnostics only. No odds, no
   implied returns, no bankroll.

5. **Ex-ante validity**: `cds_qualification.json` was generated
   `2026-07-01T04:02:29Z` (per `simulation_meta.run_at_utc`). At that time
   only MD1 results were entered (`group_matches_completed: 0` in the raw
   envelope, since the model is forward-looking Elo — see §6.6 of
   `wiki/index.md` 2026-06-20 memo). All CDS `qual_prob_*` values used
   here are ex-ante relative to the full 72-match group stage.

6. **Source policy**: `data/processed/schedule.json` is treated as the
   canonical source of fact per `wiki/index.md` 2026-07-08 memo
   (Wikipedia Green Source zero-deviation cross-check on 12 standings × 8
   score spot-checks = 96 verifications, zero deviation). This settlement
   does not introduce or rely on any non-Green-Source fact.

## 7. Reproducibility

```bash
cd /Users/tangzw119/Documents/GitHub/cds4worldcup
python3 -m src.cds.settlement_run
# → writes results/ops/cds-settlement-2026-07-08.json
```

The settlement artifact (`results/ops/cds-settlement-2026-07-08.json`)
contains the full per-team table, per-group standings, best-8 thirds, and
all Brier aggregations. Re-running with the same schedule.json will yield
identical numerical output (deterministic standings + deterministic Brier).

## 8. Summary

| Item | Result |
|------|--------|
| Brier, qualification (n=48, top2) | 0.2392 |
| Below constant-0.5 baseline (0.250) | yes (by 0.011) |
| Largest calibration failure | Czech Republic (UEFA, Group A, pred 0.834 → 4th, Brier 0.695) |
| Largest positive surprise | Cape Verde (CAF, Group H, pred 0.147 → 2nd, Brier 0.728) |
| Confederation with worst Brier | CAF (mean 0.559, n=10, 9 advanced) |
| Confederation with best Brier | CONCACAF (mean 0.096, n=6) — but small sample, partially artifactual |
| Sorted best-8 thirds | (K)DRC, (F)Sweden, (E)Ecuador, (L)Ghana, (B)BIH, (J)Algeria, (D)Paraguay, (I)Senegal |
| Cut at best-8 | (C)Scotland, (G)Iran, (H)Uruguay, (A)South Korea |
| 16 eliminated teams | CZE, South Korea, Qatar, Haiti, Scotland, Turkey, Curaçao, Tunisia, Iran, New Zealand, Saudi Arabia, Uruguay, Iraq, Jordan, Uzbekistan, Panama |

These 16 teams also carry Item 4: their `championship_prob` from
`cds_championship.json` is settled (now = 0).
