# Protocol Failure Log

> Status: Phase -1 smoke test complete
> Last updated: 2026-06-10

---

## Phase -1 Historical Smoke Test

### Match Selection

| Field | Value |
|---|---|
| match_id | wc2022-g-arg-ksa |
| match | Argentina vs Saudi Arabia |
| competition | 2022 FIFA World Cup, Group C |
| date | 2022-11-22 |
| result | Saudi Arabia 2-1 Argentina (away_win) |
| selection_reason | Official result unambiguous; pre-match FIFA ranking gap (#4 vs #49) provides clear statistical baseline; one of the most notable upsets in World Cup history, testing scorer under extreme surprise |

### Protocol Failure Tracking

| match_id | failure_type | status | notes |
|---|---|---|---|
| wc2022-g-arg-ksa | none | resolved | No protocol failures detected. See Go/No-Go review below. |

---

## Phase -1 Go/No-Go Review (Task 5 Step 5)

### Question 1: Can this match be scored without changing schemas?

**Answer: YES**

- All three YAML files (prediction_card, factor_ledger_entry, settlement_record) were created using the frozen schemas without modification.
- The `task_type: group_90m_wdl` semantics are unambiguous: 90-minute result classified as home_win / draw / away_win.
- Brier Score (1.3262) and Log Loss (2.4079) computed cleanly from the three-class probability vector and the actual outcome.
- No schema fields needed to be added, renamed, or removed.

### Question 2: Can each tracked factor be adjudicated from post-match evidence?

**Answer: YES**

- **Factor 1** (Saudi Arabia offside trap effectiveness): Threshold was "≥ 2 Argentina goals disallowed for offside in the first half." Post-match evidence from Wikipedia (cross-referenced with BBC Sport and FIFA reports) confirms 3 such goals. Verdict: **supported**. Adjudicator confidence: 9/10.
- **Factor 2** (Saudi Arabia early second-half goal): Threshold was "≥ 1 Saudi Arabia goal between 46'-55'." Post-match evidence confirms Al-Shehri scored in the 48th minute. Verdict: **supported**. Adjudicator confidence: 10/10.
- Both factors had clear `quantified_threshold`, `settlement_rule`, and `counter_signal` fields. Both were adjudicable using publicly available post-match data.

### Question 3: Were any Red Sources used as CDS input facts?

**Answer: NO**

- The prediction card uses only Green Sources: Wikipedia 2022 World Cup Group C page and Wikipedia 2022 World Cup seeding page.
- `kimi_public_artifact_snapshot` is listed in `red_sources_excluded_from_model`.
- The statistical baseline uses FIFA ranking data from the Wikipedia seeding page, which is a public, verifiable, non-LLM source.
- No Kimi-derived probabilities, rankings, or win rates entered the prediction or factor content.

### Question 4: Is task semantics unambiguous?

**Answer: YES**

- `task_type: group_90m_wdl` maps cleanly to the three-class probability output (home_win_90m / draw_90m / away_win_90m).
- The probabilities sum to 1.00 (0.66 + 0.25 + 0.09 = 1.00).
- The official result (Argentina 1-2 Saudi Arabia) maps unambiguously to `outcome_90m: away_win`.
- No confusion between 90-minute result and knockout advancement semantics.

---

## Go/No-Go Verdict

| Question | Result |
|---|---|
| (1) Score without schema changes? | ✅ YES |
| (2) Every factor adjudicable? | ✅ YES |
| (3) No Red Source contamination? | ✅ YES |
| (4) Task semantics unambiguous? | ✅ YES |

**Overall: GO** — Phase -1 smoke test passed. Protocol, schemas, scorer, and factor adjudication are validated for at least one historical match. The experiment may proceed to Phase 0 freeze checklist.

---

## Summary Statistics

| Metric | Value |
|---|---|
| Brier Score | 1.3262 |
| Log Loss | 2.4079 |
| Prediction | home_win=0.66, draw=0.25, away_win=0.09 |
| Actual outcome | away_win (Saudi Arabia 2-1 Argentina) |
| Baseline source | FIFA ranking logistic model (March 2022: Argentina #4, Saudi Arabia #49) |
| Baseline source URL | https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_seeding |
| Factors supported | 2/2 |
| Factors rejected | 0/2 |
| Factors inconclusive | 0/2 |
| Protocol failures | 0 |

---

## Artifacts

| File | Path |
|---|---|
| Prediction Card | `experiments/worldcup-2026-factor-calibration/predictions/phase-minus1/wc2022-g-arg-ksa.prediction_card.yaml` |
| Factor Ledger | `experiments/worldcup-2026-factor-calibration/factor-ledger/wc2022-g-arg-ksa.factors.yaml` |
| Settlement Record | `experiments/worldcup-2026-factor-calibration/settlement/wc2022-g-arg-ksa.settlement_record.yaml` |
| This Report | `experiments/worldcup-2026-factor-calibration/reports/protocol_failure_log.md` |

## Known Limitations

### Self-Referencing SHA-256 Hash (2026-06-10)

The MVP-A prediction card at `predictions/mvpa/wc2026-a-m01-mex-rsa.prediction_card.yaml` contains a `lock.sha256` field whose value (`37d7ad55564a7920abba6119f4a8f79b0bf3668dc4764c286025049cf6b0d36c`) was computed on the file content **before** the hash was written into it. Writing the hash changes the file, so the embedded hash does not match the file's actual SHA-256.

- **File's actual SHA-256**: `5dc148d478d5a20e79f284869aa9b09017faa23a1471b61f332edaf906dd0ded`
- **Embedded hash**: Pre-write snapshot (above)
- **Primary lock mechanism**: Git commit `56033f2c0008e7f94cf7f2d05e4b2d6bd56814db` (HEAD at lock time)
- **Verification method**: The file's content at that git commit should match the pre-write hash

**Resolution for future matches**: Use a detached `.sha256` companion file instead of embedding the hash inside the YAML. This avoids the circular dependency entirely.

---

## MVP-A v0.1 Superseded by v0.2 (2026-06-10)

The original MVP-A v0.1 prediction card is retained as a preflight artifact. It is superseded for official scoring because it did not preserve a fixed rendered prompt and therefore did not satisfy the prompt provenance gate. MVP-A v0.2 was generated by the automated runner before kickoff and is the official scoring artifact for `wc2026-a-m01-mex-rsa`.
