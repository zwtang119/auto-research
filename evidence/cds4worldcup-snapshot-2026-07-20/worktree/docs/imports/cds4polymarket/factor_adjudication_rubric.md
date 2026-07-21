# Factor Adjudication Rubric

> Status: frozen-before-MVP-A
> Version: v0.1
> Last updated: 2026-06-10
> Source: spec §10 (Factor Ledger 判定协议)

---

## 1. Purpose

This rubric defines how every tracked factor in the World Cup calibration wind tunnel is adjudicated after a match concludes. It ensures post-match factor assessment is evidence-based, not impressionistic.

## 2. Required Fields for Every Tracked Factor

Each factor entering `calibration_status: tracking` must have all of the following before the match kicks off:

| Field | Description | Example |
|---|---|---|
| `observable_proxy` | What can be observed in post-match data | "opponent second-half sprint count drop" |
| `quantified_threshold` | Numeric or boolean criterion for support/rejection | "≥ 15% below first-half count" |
| `settlement_rule` | Logic mapping evidence → status | "supported if ≥ 15% drop; rejected if < 5% drop; inconclusive if data unavailable" |
| `counter_signal` | What would invalidate the factor's direction | "opponent scores first or home team red card before 30'" |
| `data_sources` | Green Sources needed for adjudication | official match event data |
| `adjudicator.required_independence` | "not the same agent/person who generated the factor" |

A factor missing any of these fields must NOT enter `calibration_status: tracking`.

## 3. Settlement States

| Status | Criterion |
|---|---|
| `supported` | Pre-match frozen `settlement_rule` evidence exists and meets the support threshold. |
| `rejected` | Pre-match frozen counter-signal or negation threshold is satisfied. |
| `inconclusive` | Evidence is missing, conflicting, threshold is inapplicable, or only the match result itself can explain the factor post-hoc. |

## 4. Confidence Scale

| Score | Meaning |
|---|---|
| 10 | Iron-clad: official match data directly confirms threshold met/not met. |
| 8–9 | Strong: official data confirms with minor ambiguity (e.g., exact minute boundary). |
| 5–7 | Moderate: evidence supports direction but requires interpretation. |
| 3–4 | Weak: evidence is indirect or partially conflicting. |
| 1–2 | Very weak: mostly post-hoc narrative, not directly observable. |
| 0 | No evidence available for adjudication. |

## 5. Adjudicator Independence

- The adjudicator must not be the same agent or person who generated the factor.
- For MVP-A (manual loop), the adjudicator can be the same human operator who ran the pre-match pipeline, but must document `adjudicator.required_independence: "same_human_different_time"` and acknowledge the conflict.
- For Phase 2+, aim for independent adjudicator.

## 6. Inconclusive Rate Policy

| Condition | Action |
|---|---|
| Inconclusive rate < 30% | Normal operation. |
| 30%–70% | Monitor. Log each inconclusive factor with `reason_for_inconclusive`. |
| > 70% for 5 consecutive matches | Trigger Factor Ledger design review. Consider transitioning to **factor taxonomy mode** (classify which sports factors are adjudicable vs. only qualitatively reviewable). |

## 7. Factor Origin Tracking

| Origin | Rules |
|---|---|
| `cds_generated` | No additional restrictions beyond rubric. |
| `kimi_derived` | Must be stripped of probability anchors before entering candidate pool. Must carry `origin: kimi_derived`. MVP max 1 per match in tracking. |
| `human_seeded` | Must still meet all rubric fields (threshold, settlement rule, counter-signal). |

## 8. Amendment Protocol

If a factor's threshold or settlement rule needs correction after lock:

1. Do NOT modify the original factor entry.
2. Append an amendment to the factor YAML with `amendment: true`, `amended_at_utc`, and the corrected fields.
3. Both original and amended versions enter adjudication.
4. Protocol failure log records `prompt_config_drift` if the correction changes the factor's direction.

---

## 9. References

- Spec §10: Factor Ledger 判定协议
- Spec §14.6: Protocol failure taxonomy
- `schemas/factor_ledger_entry.schema.yaml`: Schema definition
