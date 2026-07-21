# Protocol Failure Log: wc2026-a-m01-mex-rsa

> **Match**: Mexico 2-0 South Africa (Group A, Opening Match)
> **Date**: 2026-06-11, Estadio Azteca, Mexico City
> **Audit Date**: 2026-06-13
> **Auditor**: AI settlement agent (automated Plan C workflow)

---

## Summary

**1 minor protocol failure detected. No critical or major failures.**

The settlement process completed successfully with all three factors adjudicated and all required artifacts generated. The one identified failure is a data availability limitation that the factor's own settlement rule already anticipated.

---

## Failure #1: Half-Time Possession Data Unavailable from Designated Source

### Details

| Field | Value |
|---|---|
| **Failure ID** | wc2026-a-m01-mex-rsa-pf01 |
| **Severity** | Minor |
| **Category** | Data availability |
| **Factor Affected** | wc2026-a-m01-mex-rsa-f01-home-possession |
| **Detected At** | Factor adjudication phase |

### Description

Factor f01 ("Mexico possession >= 55% in first half") requires first-half possession percentage for settlement. The designated data source (`fifa_match_report_wc2026_group_a`) — specifically the [FIFA Official Match Report PDF](https://fdp.fifa.org/assetspublic/ce281/r12452/pdf/FullTimeMatchReport-English.pdf) — provides only full-match aggregate possession statistics (Mexico 61%, South Africa 39%) without a half-time breakdown.

### Impact

- Factor f01 could not be definitively settled as `supported` or `rejected`.
- The factor's own `settlement_rule` field anticipated this scenario: *"inconclusive if official match statistics are unavailable or only full-match (90-minute aggregate) possession is reported without half-time breakdown."*
- The factor was settled as `inconclusive` per its own protocol, which is the correct behavior.
- No downstream artifacts were blocked; the settlement record and knowledge update log were completed normally.

### Root Cause

1. The factor's `observable_proxy` ("Mexico first-half possession percentage") requires granularity that the FIFA official match report does not provide.
2. The `data_sources` field listed only `fifa_match_report_wc2026_group_a` as the authoritative source, with no fallback.
3. The settlement rule did include the inconclusive path, but the factor design did not include an alternative data source for half-time statistics.

### Resolution

- **Immediate**: Factor settled as `inconclusive` per the predefined settlement rule. No corrective action needed for this specific settlement.
- **Recommendation for future factors**:
  1. Prefer full-match aggregate statistics as observable proxies where possible (e.g., "Mexico possession >= 55% in the full match").
  2. If half-time granularity is required, include an alternative data source in `data_sources` that provides half-time breakdowns (e.g., Opta, Sofascore, FotMob, ESPN match stats).
  3. Consider a two-tier settlement rule: primary source for definitive settlement, secondary source for corroboration.

### Status: Resolved

The failure is documented and the factor is correctly settled. No retroactive correction is needed.

---

## Checked and Confirmed: No Other Protocol Failures

The following potential failure modes were checked and confirmed clean:

### Schema Validation
- ✅ Prediction card (`wc2026-a-m01-mex-rsa.prediction_card.yaml`) validated against schema at lock time.
- ✅ Factor ledger (`wc2026-a-m01-mex-rsa.factors.yaml`) schema valid.
- ✅ Settlement record schema follows the established format (based on `wc2022-g-arg-ksa.settlement_record.yaml`).

### Red Source Contamination
- ✅ No Red Sources (kimi_public_artifact_snapshot) were used in the prediction model. The prediction card explicitly lists it under `red_sources_excluded_from_model`.
- ✅ Settlement was performed using only Green Sources (FIFA official match report, ESPN corroboration).

### Lock Integrity
- ✅ Prediction was locked at `2026-06-10T12:50:00Z`, approximately 34 hours before kickoff (`2026-06-11T23:00:00Z`). No post-kickoff information could have influenced the prediction.
- ✅ SHA256 hash and git commit recorded in prediction card.

### Data Package Integrity
- ✅ Data package ID (`wc2026-a-m01-mex-rsa-mvpa-v0.1`) is consistent across prediction card and factor ledger.
- ✅ Source cutoff UTC (`2026-06-10T12:00:00Z`) precedes lock time.

### Market Baseline
- ⚠️ Market/odds baseline was unavailable at prediction time (`status: missing_with_reason`). This is documented and expected for MVP-A manual loop. Not a protocol failure — the absence is transparently disclosed.

### Task Semantics
- ✅ `task_type: group_90m_wdl` is unambiguous. The match ended in 90 minutes (no extra time). Outcome (`home_win`) maps cleanly to the prediction categories.

### Factor Adjudication Completeness
- ✅ All 3 factors in the ledger were adjudicated:
  - f01: inconclusive (data limitation, per settlement rule)
  - f02: supported (2 <= 3 shots on target)
  - f03: rejected (3 corners, not >= 6)
- ✅ No factors were skipped or left in `pending` state without documented reasoning.

### Score Calculation
- ✅ Brier Score (0.3078) and Log Loss (0.5978) calculated correctly from prediction probabilities and actual outcome.
- ✅ Baseline comparison computed correctly using simple statistical baseline probabilities (0.61/0.25/0.14).

---

## Protocol Compliance Score

| Check | Result |
|---|---|
| Schema validation | Pass |
| Red Source exclusion | Pass |
| Lock integrity | Pass |
| Data package consistency | Pass |
| Factor adjudication completeness | Pass (1 inconclusive, documented) |
| Score calculation accuracy | Pass |
| Artifact completeness | Pass |
| **Overall** | **Pass (1 minor documented limitation)** |

---

*Document generated as part of Plan C settlement for wc2026-a-m01-mex-rsa.*
*Audit completed at: 2026-06-13T12:00:00Z*
