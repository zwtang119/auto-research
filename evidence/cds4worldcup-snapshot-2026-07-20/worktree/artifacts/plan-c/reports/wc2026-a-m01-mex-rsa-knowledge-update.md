# Knowledge Update Log: wc2026-a-m01-mex-rsa

> **Match**: Mexico 2-0 South Africa (Group A, Opening Match)
> **Date**: 2026-06-11, Estadio Azteca, Mexico City
> **Settlement Date**: 2026-06-13
> **Source**: [FIFA Official Match Report](https://fdp.fifa.org/assetspublic/ce281/r12452/pdf/FullTimeMatchReport-English.pdf)

---

## 1. Pre-Match Judgments vs Reality

### 1.1 Validated Judgments

| Pre-Match Judgment | Actual Outcome | Status |
|---|---|---|
| Mexico favored to win (P=0.55) | Mexico won 2-0 | ✅ Correct |
| South Africa's attacking output would be limited | 3 total shots, 2 on target | ✅ Correct |
| Opening match has high variance potential | 3 red cards in the match | ⚠️ Partially — variance showed in discipline, not scoreline |
| Estadio Azteca home advantage is massive | 80,824 attendance, Mexico dominant | ✅ Correct |
| Mexico's opening-match curse would be broken | First WC opening win in 8 attempts | ✅ Correct |

### 1.2 Inconclusive Judgments

| Pre-Match Judgment | Actual Outcome | Status |
|---|---|---|
| Mexico would control first-half possession (>=55%) | Full-match 61%, half-time data unavailable | ❓ Inconclusive |

### 1.3 Invalidated Judgments

| Pre-Match Judgment | Actual Outcome | Status |
|---|---|---|
| Mexico would generate >= 6 corners from sustained pressure | Only 3 corners despite 16 shots | ❌ Incorrect |

---

## 2. Factor Performance Summary

### f01: Mexico First-Half Possession >= 55% (Precursor)
- **Result**: Inconclusive
- **Full-match possession**: 61%
- **Assessment**: The factor's observable proxy (first-half possession) was not available from the designated data source. The full-match aggregate strongly suggests the factor would have been supported, but the settlement protocol correctly marks this as inconclusive.
- **Learning**: Future factors should either use full-match aggregates or specify alternative data sources with half-time breakdowns.

### f02: South Africa Shots on Target <= 3 (Suppressor)
- **Result**: ✅ Supported (2 shots on target)
- **Assessment**: Excellent factor selection. South Africa was completely dominated — only 3 total attempts in 90 minutes. The suppressor correctly identified that South Africa's low attacking quality (FIFA rank #61) would be exposed at this level, especially away from home.
- **Confidence**: High. This factor is directly applicable to similar matchups where a significantly lower-ranked away team faces a host nation.

### f03: Mexico Corners >= 6 (Precursor)
- **Result**: ❌ Rejected (3 corners)
- **Assessment**: The factor failed despite Mexico's dominance in every other metric. 16 shots yielded only 3 corners, indicating:
  - Most attacks came through central channels rather than wide areas
  - South Africa's deep defensive shape funneled play centrally
  - Many shots were direct efforts rather than crosses requiring defensive intervention
- **Learning**: Corner count is not a reliable proxy for overall attacking dominance. Shot volume and possession correlate poorly with corners in matches where one team plays very deep.

---

## 3. Prediction Calibration Assessment

### Score Summary
- **Brier Score**: 0.3078 (lower is better; range 0-2 for 3-class)
- **Log Loss**: 0.5978 (lower is better)
- **Outcome**: Correct direction (home_win predicted at 0.55, home_win occurred)

### Comparison to Baseline
| Metric | Prediction | Simple Statistical Baseline | Delta |
|---|---|---|---|
| P(home_win) | 0.55 | 0.61 | -0.06 |
| Brier Score | 0.3078 | 0.2342 | +0.0736 |
| Log Loss | 0.5978 | 0.4943 | +0.1035 |

The prediction was **slightly less calibrated** than the simple statistical baseline. The 0.06 reduction in home_win probability reflected documented uncertainty about opening-match pressure effects, but Mexico's home advantage at Estadio Azteca proved even stronger than the ranking model suggested. The uncertainty discount was over-applied.

### Key Insight
The simple FIFA ranking baseline does not adjust for home advantage (documented in the prediction card). In this case, the unadjusted baseline was actually *more accurate* because the home advantage effect at Estadio Azteca (2200m altitude, 80k+ home fans, co-host nation emotion) roughly offset the opening-match pressure discount.

---

## 4. Path Card Updates

### 4.1 Mexico (Home, Group A)

**Validated Signals**:
- Home dominance is real: Mexico controlled every facet of the match (61% possession, 16-3 shots)
- Quiñones is a genuine difference-maker at this level (opening goal, hit the post later)
- Jiménez remains clinical in high-pressure moments
- Defensive discipline is a concern: Montes red card in stoppage time

**Updated Understanding**:
- Mexico's path through Group A looks comfortable based on this performance
- The opening-match curse narrative is broken, which may reduce psychological pressure in subsequent matches
- Red card risk (1 direct red in a match they dominated) suggests discipline issues under emotional pressure

### 4.2 South Africa (Away, Group A)

**Validated Signals**:
- Attacking output was minimal (3 shots, 2 on target) against top-level opposition
- Discipline collapsed under pressure (2 direct red cards: Sithole 49', Zwane 84')
- Goalkeeper Ronwen Williams kept the score respectable (only 2 conceded from 16 shots)
- Bafana Bafana's AFCON 2023 form (3rd place) did not translate to World Cup level

**Updated Understanding**:
- South Africa's path through Group A is significantly harder than pre-tournament assessment
- Playing with 9 men for extended periods will deplete the squad for subsequent matches
- The ranking gap (#15 vs #61) manifested as a real quality gap on the pitch
- South Africa's defensive structure was reasonable (only 2 goals conceded despite 16 shots) but insufficient

---

## 5. Methodological Learnings

1. **Corner count is a poor precursor factor for dominant teams against deep defenses.** Mexico earned only 3 corners despite 16 shots. Future factors should prefer shot volume or xG-related metrics over corner counts when one team is expected to dominate possession.

2. **Half-time statistics require dedicated data sources.** The FIFA official match report provides only full-match aggregates for possession. Factors requiring half-time breakdowns should specify alternative data sources (Opta, Sofascore) in their `data_sources` field.

3. **The uncertainty discount for "opening match variance" may be over-applied for true home advantages.** Mexico's Estadio Azteca advantage (altitude + crowd + co-host emotion) produced a routine win, not a high-variance upset. The simple statistical baseline, which does not model these factors, was accidentally more accurate.

4. **Red card count (3) validates the "opening match volatility" note partially**, but the volatility manifested in discipline rather than scoreline variance. The prediction correctly captured the directional outcome but the uncertainty note misidentified the source of variance.

5. **Suppressor factors (f02) outperformed precursor factors (f01, f03)** in this match. The suppressor (limiting South Africa's attacking output) was both well-chosen and well-calibrated. The precursors (possession, corners) suffered from proxy measurement issues.

---

## 6. Applicable to Future Matches

- **For Mexico's remaining Group A matches**: Expect continued dominance in possession and shots. Corner count factor should NOT be reused — Mexico's attacking pattern is centrally focused.
- **For South Africa's remaining Group A matches**: Attacking output is likely to remain low against quality opposition. Suppressor-type factors (opponent shots on target limits) are more reliable than precursor factors for South Africa's opponents.
- **For opening-match patterns**: The home advantage at Estadio Azteca is confirmed as one of the strongest in international football. The "opening match curse" narrative for Mexico is now resolved.

---

*Document generated as part of Plan C settlement for wc2026-a-m01-mex-rsa.*
*Settled at: 2026-06-13T12:00:00Z*
