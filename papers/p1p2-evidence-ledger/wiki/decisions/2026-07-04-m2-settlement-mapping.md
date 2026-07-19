# P1+P2 M2 Settlement Mapping — Decision

> **Decision date**: 2026-07-04  
> **Decision owner**: P1+P2 mainline (auto-research)  
> **Milestone**: M2 (settlement mapping to ≥30 settleable claims)  
> **Status**: selected — execution pending  
> **Anchors**: `state/task_spec.md` §4 M2, `state/io_spec.md` §4 `experiments/ledger/settlement_mapping.md`

## 1. Question

Roadmap §6.5 Day 3-5 asks: "Gulei or Polymarket settlement mapping, at least 30 claim/factor settleable."  
M2 of `state/task_spec.md` is the operational form of that ask: `experiments/ledger/settlement_mapping.md` covering ≥ 30 settleable claims.

Which settlement source(s) do we adopt, and how do we bridge the claim → settlement oracle gap?

## 2. Candidates considered

| Source | Strengths | Weaknesses | Verdict |
|--------|-----------|------------|---------|
| **Gulei 2015 official policy response** | 14 documented timepoints (2015→2025) from `09-gulei-retrospective-validation.md`; 90-citation source set; ground truth is official documents (strongest GT) | Single-incident (no generalization); some timepoints are policy-level not factor-level | **Selected as primary** |
| Polymarket / prediction-market | Real-time numeric forecast; easy Brier/Log Loss computation | Chemical-event markets illiquid; not enough factor coverage at claim granularity | **Deferred to M5 pilot expansion** |
| EIA (Energy Information Admin) | Public energy data, easy to map to refinery/fuel factors | Limited to energy-sector scope; doesn't cover emergency-response factors | **Auxiliary — kept for P1+P2 sub-scenario** |
| Cds4polymarket artifacts | Existing vendor support in framework | Same as Polymarket | **Same as Polymarket** |

## 3. Decision

**Primary settlement source: Gulei 2015 official policy response.**

Rationale (per `framework/schemas/data-contracts.md` §9 QREF-005 cite):
> "Rows are truth; vault notes are projections."

The 14 official policy timepoints are themselves a `rows-are-truth` artifact (citation-backed government documents). Mapping each Gulei factor onto one of those 14 timepoints gives the evidence ledger a primary `settlement_rule` for ~10–14 anchor claims. The remaining claims (target ≥30 settleable) need a derived oracle — which we'll construct from the Gulei retrospective report's effect ontology (already used by Policysim-v0.2).

## 4. Bridge design: factor → settlement_rule

For each of the 10 pilot_10 entries, derive a settlement_rule that names the official document or numeric threshold that would resolve the claim.

| claim_id | factor_type | settlement_rule target |
|----------|-------------|------------------------|
| C-P1P2-001 | precedent | Gulei incident report 2015 § 4.2.1 (foam application rate model) — IF actual time-to-control > 6h AND tank-farm escalated THEN factor_confirmed=false |
| C-P1P2-002 | inhibitor | Industry Ministry stockpile records 2015-04-06 → ratio of AFFF delivered to AFFF needed |
| C-P1P2-003 | branch | AERMOD dispersion model output at 3km boundary → numeric threshold |
| C-P1P2-004 | falsifier | Tank-farm explosion event timestamp 2015-04-06T14:30Z |
| C-P1P2-005 | authority | State Council Safety Office order doc (gov.cn 2015-04-07) + Industry Ministry halt records |
| C-P1P2-006 | precedent | Xiamen weather station 2015-04-06 wind-direction time series |
| C-P1P2-007 | precedent | 2014 Ebola response guideline supersession (already cited; `stale: true`) |
| C-P1P2-008 | inhibitor | Weibo sentiment — **NO formal settlement source** (marked `settleable: false` in pilot; this is intentional un_settleable) |
| C-P1P2-009 | branch | Plant SCADA column-temp time series 2015-04-06T14:00-15:00Z |
| C-P1P2-010 | falsifier | Highway patrol log + post-incident closure-justification audit |

This gives **9/10 settleable** from a single Gulei source (the 1 un_settleable is C-P1P2-008 social-media, kept for `un_settleable_ratio` audit at M7).

## 5. Scale to ≥ 30

Pilot_10 has 10. To reach ≥30 settleable claims (M2 success criterion) we need ~20 more. Strategy:

1. **Replicate per-stage**: Gulei has 4 event-chain stages × ~3-4 decisions per stage = 12-16 more claims
2. **Replicate per-agent**: 6 agents (Commander / Process / Fire / Medical / Environmental / Safety) × 1-2 contested decisions each = 6-12 more
3. **Cross-link to policy timepoints**: each of 14 policy timepoints spawns 1-2 follow-up factors = 14-28 more

Target: 30-40 settleable claims by end of M2. The factor expansion is content work, not schema work — reuses the same `build_pilot_10.py` generator pattern.

## 6. Polymarket / numeric forecast path (deferred to M5)

For factors where the Gulei retrospective is too coarse (e.g., settlement_rule needs a probability), defer Polymarket numeric forecast to M5 pilot run. Example target:

> `claim_id: C-P1P2-101, settlement_rule: "predicted_p > 0.65 from Polymarket event PMKT-2026-WTI-Q3" → if observed_outcome == 1 then factor_confirmed`

This requires M5 pilot data which is not in M2 scope.

## 7. Risks and exit criteria

**Risks**:
- 14 official timepoints may not cover all factor dimensions (mitigation: derive synthetic rules from effect ontology when no official source)
- Gulei 2015 data is single-incident — generalization claim must be hedged in paper
- social-media / public-opinion factors (C-P1P2-008 type) have no settlement source — kept un_settleable for honest `un_settleable_ratio` reporting

**Exit criteria for M2 (success)**:
- `experiments/ledger/settlement_mapping.md` exists and lists ≥ 30 claims
- ≥ 30 claims have `settleable: true` in their evidence_ledger_entry
- ≤ 40% `un_settleable_ratio` (per task_spec §6)
- Each settleable claim's `settlement_rule` references either an official Gulei source or a numeric threshold

**Exit criteria for M2 (failure / pivot)**:
- Cannot reach 30 settleable claims without inventing settlement sources → `stale_count += 1` and pivot to "narrow to Gulei-only, accept n<30" (defended in paper as honest scope)

## 8. Required follow-up actions

1. Expand `build_pilot_10.py` to `build_pilot_30.py` (reuses all 10 entries + adds 20+ via stage/agent/timeline replication)
2. Each new entry must pass `validate_ledger.py` and reference a settlement source in `experiments/ledger/settlement_mapping.md`
3. Run validator; expect 30+ valid, 0 rejected
4. Append `M2_settlement_mapping_complete` finding to `state/findings.jsonl`
5. Update `state/progress.json` to iteration=2, completed_milestones+=["M2"]

## 9. Direction diversity check (Deli §6)

This direction (Gulei retrospective as primary settlement source) is structurally distinct from:
- "Polymarket as primary" (different source class, deferred)
- "EIA as primary" (different domain, energy-only)
- "synthetic oracle only" (no real-world source)

Per `state/directions_tried.json`, this is the first entry on the **settlement source** axis. Subsequent attempts must vary on at least one axis (source, granularity, oracle type) per Deli stale_rule.

## 10. References

- `state/task_spec.md` §4 M2 (milestone definition)
- `state/task_spec.md` §6 (success criteria: ≤40% un_settleable)
- `state/io_spec.md` §4 `experiments/ledger/settlement_mapping.md` (output path)
- `legacy/p11-closed-v5-mimo/state/gulei_scenario.py` (scenario reused as factor seed)
- `~/Documents/GitHub/policysim-research-Tsinghua/ideas/09-gulei-retrospective-validation.md` (14 policy timepoints, 90-citation source set)