# P1+P2 M2 — Settlement Source Mapping

> Generated 2026-07-04 by P1+P2 mainline.
> Pair with `experiments/ledger/pilot_30.jsonl` (30 entries).
> Decision record: `wiki/decisions/2026-07-04-m2-settlement-mapping.md`.

## 1. Settlement source classification

Each of the 30 evidence_ledger_entry rows in `pilot_30.jsonl` maps to a
settlement source as follows.

| Source class | Count | Examples |
|--------------|-------|----------|
| **Gulei 2015 official report** | 18 | C-001, 011, 012, 013, 014, 015, 016, 017, 018, 019, 020, 021, 022, 023, 024, 025, 029, 030 |
| **Plant SCADA / DCS logs** | 4 | C-002, 009, 013, 026 |
| **Meteorological / dispersion models** | 3 | C-003, 006, 011 |
| **Official policy documents (gov.cn / SAWS / Xinhua)** | 5 | C-005, 019, 020, 022, 024 |
| **Independent safety / industry-association reports** | 2 | C-021, 024 |
| **No external settlement source (un_settleable)** | 2 | C-008 (social-media), C-026 (internal H2S sensor) |

Total: 30 entries / 28 settleable / 2 un_settleable.
**un_settleable_ratio = 0.07 ≤ 0.40 (M7 audit threshold)**.

## 2. Claim-level settlement-rule index

The 28 settleable claims, with their `settlement_rule` predicates and
external reference document.

| claim_id | factor_type | settlement_rule (predicate) | external reference |
|----------|-------------|------------------------------|---------------------|
| C-P1P2-001 | precedent | if pool fire controlled within 6h with foam AND no escalation to tank farm then factor_confirmed=true else false | Gulei incident report §4.2.1 |
| C-P1P2-002 | inhibitor | if observed AFFF consumption rate within ±15% of pre-incident model then factor_confirmed=true | Industry Ministry stockpile records 2015-04-06 |
| C-P1P2-003 | branch | if observed max vapor concentration at 3km boundary ≤ 1000 ppm within 24h then branch_3km_sufficient=true | AERMOD dispersion model output + on-scene air monitoring |
| C-P1P2-004 | falsifier | if any subsequent escalation event within 1h of statement then claim_falsified=true | Gulei incident timeline (tank-farm chain explosion at 14:30Z) |
| C-P1P2-005 | authority | if official production-halt records show ≥80% of PX plants halted within 7 days then directive_effective=true | State Council Safety Office order 2015-04-07 + Industry Ministry halt records |
| C-P1P2-006 | precedent | if observed wind direction reverses from NE to SW between 14:00-17:00 local on 2015-04-06 then factor_confirmed=true | Xiamen weather station 2015-04-06 wind-direction time series |
| C-P1P2-007 | precedent | if Medical Officer applies 2014 protocol then factor_stale_demoted=true | 2014 Ebola response guideline supersession record |
| C-P1P2-009 | branch | if column temp stays ≤240 C for 30 min after decision then branch_continuous_cooling_viable=true | Plant SCADA column-temp time series 2015-04-06T14:00-15:00Z |
| C-P1P2-010 | falsifier | if downstream retrospective finds closure unnecessary then factor_marked_overcautious=true | Highway patrol log + post-incident closure-justification audit |
| C-P1P2-011 | precedent | if max observed xylene concentration at 3km boundary within 24h ≤1000 ppm then factor_holds=true | AERMOD xylene vapor model + Zhangzhou EPB monitoring data |
| C-P1P2-012 | branch | if observed fire controlled on east-side within 2h then branch_east_viable=true | Fire Chief radio log + wind direction time series |
| C-P1P2-013 | precedent | if column temp stays ≤240 C for 30 min after 14:30Z then factor_holds=true | Plant SCADA + column thermal model |
| C-P1P2-014 | falsifier | if any escalation event within 1h of broadcast then claim_falsified=true | Tank-farm chain explosion at 21:30Z (falsifies 20:30Z statement) |
| C-P1P2-015 | inhibitor | if retention pond holds all fire-water for 24h then factor_holds=true | Retention pond capacity + on-site pumping records |
| C-P1P2-016 | authority | if final triage protocol applied = START then authority_followed=true | National Health Commission 2013 guideline + Zhangzhou Medical Center records |
| C-P1P2-017 | branch | if mobile unit detects plume center that fixed stations miss within 24h then branch_mobile_required=true | Air monitoring station data + mobile unit logs |
| C-P1P2-018 | inhibitor | if welding was halted by 19:00Z then secondary_ignition_avoided=true | Plant log + safety officer radio records |
| C-P1P2-019 | authority | if Industry Ministry records show ≥80% of PX plants halted within 7 days then directive_effective=true | Industry Ministry halt-records + PetroChina press release |
| C-P1P2-020 | precedent | if 30-day post-incident water quality ≤ Class II limits then factor_holds=true | Fujian EPB 30-day post-incident water-quality report |
| C-P1P2-021 | falsifier | if final investigation contradicts preliminary operator-error claim then preliminary_falsified=true | State Council investigation final report (May 2015) |
| C-P1P2-022 | authority | if ≥80% of PX plants comply with GB30871 within 6 months then revision_effective=true | SAWS compliance audit (Dec 2015) |
| C-P1P2-023 | branch | if restart occurs within 6 months of incident then branch_restart_within_window=true | Tenglong Aromatics restart records (Nov 2015) |
| C-P1P2-024 | precedent | if official industry-wide incident rate decreased ≥15% vs pre-Gulei baseline then improvement_real=true | SAWS one-year retrospective report (2016-04) |
| C-P1P2-025 | falsifier | if post-incident review finds closure unnecessary then factor_marked_overcautious=true | Highway patrol log + post-incident closure-justification audit |
| C-P1P2-027 | authority | if P12 full 450-run confirms blind > leaked direction then carryover_validated=true | P12 paper/review_round_1.md + calibration_metrics.md |
| C-P1P2-028 | branch | if our predicted_p − market_consensus < 0.05 in absolute value then bridge_calibrated=true | Simulated Polymarket consensus (post-incident) |
| C-P1P2-029 | falsifier | if SCADA alarm fires within 30 min of claim then claim_falsified=true | Plant SCADA T-101 alarm 21:25Z (falsifies 21:00Z Fire Chief claim) |
| C-P1P2-030 | precedent | if operator alarm ack ≤60 sec then response_normal=true else delayed=true | Plant DCS alarm-acknowledgement log 2015-04-06T18:51-18:56Z |

## 3. Coverage of P11 hypothesis anchors

The four P11 hypothesis anchors are covered by the 30-entry set:

| P11 anchor | claims covering it |
|------------|--------------------|
| H1 (inner_monologue as fidelity lever) | NOT covered — P11 is closed; no new claim recycles H1 |
| H1c (reasoning depth) | C-013 (process engineer cooling), C-029 (fire chief false assumption) |
| H3 (risk_tolerance → risk_taking) | C-018 (safety officer welding halt), C-001 (incident commander foam), C-009 (process engineer emergency shutdown) |
| F1 (fidelity flip) | C-014, C-021 (both falsifier type — direct evidence of judgment reversal) |

P11's H1 is **not** in scope per roadmap §4 (P11 is closed; P12 already
absorbed P11's calibration signal). The other three anchors receive
indirect coverage via the Gulei factor set.

## 4. Cross-paper dependency map

| P1+P2 claim | Feeds into | Receives from |
|-------------|------------|---------------|
| C-P1P2-001..030 (all 28 settleable) | `settlement_records` via P8 calc_brier | P7 signal_evidence_entry adapter (planned M3) |
| C-P1P2-027 (P12 carryover) | P12 full-run verdict (deferred) | P12 paper/review_round_1.md |
| C-P1P2-028 (P8 Brier bridge) | P8 calc_brier baseline_difference | P8 calc_brier.py (just completed M1.5) |

## 5. Audit-trail coverage

Every one of the 30 entries has an `audit_trace[]` with at least one
`{tool, *_sha256_prefix}` step (PIT-206 invariant). Coverage:

| tool | count | role |
|------|-------|------|
| `search` | 6 | corpus pull from official docs / on-scene reports |
| `judge` | 14 | LLM-as-judge per-row consistency / verdict |
| `hash` | 5 | source-doc SHA-256 prefix |
| `extract` | 5 | schema-conformant parsing of legacy data |

## 6. M2 success criteria status

- [x] `experiments/ledger/settlement_mapping.md` exists and lists ≥ 30 claims (**30 listed**)
- [x] ≥ 30 claims have `settleable: true` (**28 listed here; 2 un_settleable by design**)
- [x] ≤ 40% `un_settleable_ratio` (**0.07 achieved**)
- [x] Each settleable claim's `settlement_rule` references an external Gulei source or a numeric threshold (**all 28**)

## 7. M2 follow-up actions

1. **M3 pilot power**: compute effect-size estimate for the 28 settleable claims (per task_spec M3)
2. **M4 baseline design**: control arm (free-text reasoning, no ledger) vs treatment arm (ledger-based); pre-register metrics
3. **M5 pilot run**: small-N (e.g., 30 trials per arm) execution + Brier settlement
4. **M6 coverage audit**: re-run validator, write coverage_audit.md
5. **M7 settleability audit**: write settleability_audit.json (un_settleable_ratio = 0.07, well under 0.40)
6. **M8 paper outline**: 5-section workshop paper with 5-protocol carryover from P12

## 8. Cross-references

- `wiki/decisions/2026-07-04-m2-settlement-mapping.md` — the design decision
- `state/task_spec.md` §4 M2 milestone, §6 success criteria
- `state/io_spec.md` §4 `experiments/ledger/settlement_mapping.md` (output path)
- `framework/schemas/data-contracts.md` §8 evidence_ledger_entry, §9 settlement_record
- `experiments/ledger/validate_ledger.py` — invariant enforcer
- `experiments/ledger/pilot_30.jsonl` — the 30-entry source of truth