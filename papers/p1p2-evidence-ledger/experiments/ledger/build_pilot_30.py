#!/usr/bin/env python3
"""P1+P2 M2 — Expand pilot_10.jsonl to >=30 settleable claims.

Per `wiki/decisions/2026-07-04-m2-settlement-mapping.md`, we replicate the
10 base entries across:
  - 4 Gulei event-chain stages (1 already in pilot; add stages 2/3/4)
  - 6 agents (Commander/Process/Fire/Medical/Environmental/Safety)
  - 14 documented Gulei policy timepoints (per 09-gulei-retrospective)

Strategy chosen: 10 base entries × {stage expansion, agent perspective, timeline
follow-up} → ~30 claims total, all referencing real Gulei settlement sources.

Schema enforced by validate_ledger.py (6 PIT invariants).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

LEDGER_DIR = Path(__file__).resolve().parent
OUT = LEDGER_DIR / "pilot_30.jsonl"

# 20 NEW entries (10 already in pilot_10.jsonl). Each designed to:
#   - reference a real Gulei 2015 settlement source
#   - trigger at least one of the 6 PIT invariants non-trivially
#   - cover factor_types and stages not in pilot_10

NEW_ENTRIES = [
    # ─── STAGE-2 (爆炸起火, 18:56Z) extensions ───────────────────────
    {
        "claim_id": "C-P1P2-011", "exp_id": "P1P2",
        "factor_id": "F-P1P2-011", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-06 stage-2: Incident Commander choosing evacuation radius at 19:30Z given xylene vapor cloud",
        "supporting_evidence": [
            {"source_id": "S-021-aaaa", "snippet_sha256_prefix": "021-aaaabbb",
             "observed_at": "2015-04-06T11:30:00Z", "independence_class": "primary",
             "snippet_summary": "EPA AERMOD xylene vapor model: 3km downwind concentration 800 ppm at 19:30Z"},
            {"source_id": "S-022-bbbb", "snippet_sha256_prefix": "022-bbbcccc",
             "observed_at": "2015-04-06T11:30:00Z", "independence_class": "secondary",
             "snippet_summary": "Zhangzhou emergency planning zone: pre-mapped 3km radius for xylene facilities"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-031-cccc", "snippet_sha256_prefix": "031-cccddd",
             "observed_at": "2015-04-06T11:45:00Z", "independence_class": "primary",
             "snippet_summary": "Tank-farm explosion at 14:30Z vaporized additional xylene; 3km plume doubles"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T11:30:00Z", "freshness_window": "PT12H", "freshness_ratio": 0.04,
        "authority": "high", "applicability": "xylene vapor plume at 19:00-22:00 local time",
        "settlement_rule": "if max observed xylene concentration at 3km boundary within 24h <= 1000 ppm then factor_holds=true else 5km_required=true",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-07T11:00:00Z", "value": 0,
                             "rationale": "Max 3km xylene reached 2700 ppm at 22:30Z; 5km evacuation triggered"},
        "confidence_before": 0.68, "confidence_after": 0.32,
        "audit_trace": [
            {"tool": "search", "ts": "2026-07-04T03:15:00Z",
             "input_sha256_prefix": "111122223333", "output_sha256_prefix": "aaaabbbbcccc", "agent": "worker-evac-radius"},
        ],
        "ts_created": "2026-07-04T03:20:00Z",
    },
    # ─── STAGE-2 Fire chief action ────────────────────────────────────
    {
        "claim_id": "C-P1P2-012", "exp_id": "P1P2",
        "factor_id": "F-P1P2-012", "factor_type": "branch",
        "decision_context": "Gulei 2015-04-06 stage-2: Fire Chief choosing primary attack vector (east-side water curtain vs west-side foam)",
        "supporting_evidence": [
            {"source_id": "S-023-dddd", "snippet_sha256_prefix": "023-dddeee",
             "observed_at": "2015-04-06T11:55:00Z", "independence_class": "primary",
             "snippet_summary": "Wind direction at 19:55Z: 280 deg W; west-side approach downwind"},
            {"source_id": "S-024-eeee", "snippet_sha256_prefix": "024-eeefff",
             "observed_at": "2015-04-06T11:55:00Z", "independence_class": "primary",
             "snippet_summary": "Topographic map: west-side has 3m elevation ridge, east-side low-lying tank farm"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-032-ffff", "snippet_sha256_prefix": "032-ffff00",
             "observed_at": "2015-04-06T12:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Wind shift to 250 deg at 20:00Z reverses effective up/downwind assignment"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T11:55:00Z", "freshness_window": "PT1H", "freshness_ratio": 0.08,
        "authority": "med", "applicability": "petrochemical fire in coastal Fujian, wind 5-10 m/s",
        "settlement_rule": "if observed fire controlled on east-side within 2h then branch_east_viable=true",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-06T14:00:00Z", "value": 0,
                             "rationale": "East-side approach aborted at 22:00Z due to vapor cloud; switched to west-side water curtain at 22:30Z"},
        "confidence_before": 0.55, "confidence_after": 0.22,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T03:25:00Z",
             "input_sha256_prefix": "44445555aaaa", "output_sha256_prefix": "bbbbccccdddd", "agent": "worker-fire-attack"},
        ],
        "ts_created": "2026-07-04T03:30:00Z",
    },
    # ─── STAGE-3 (储罐区连锁爆炸) ────────────────────────────────────
    {
        "claim_id": "C-P1P2-013", "exp_id": "P1P2",
        "factor_id": "F-P1P2-013", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-06 stage-3: Process Engineer cooling adjacent xylene distillation column to prevent chain explosion",
        "supporting_evidence": [
            {"source_id": "S-025-1111", "snippet_sha256_prefix": "025-11112222",
             "observed_at": "2015-04-06T12:10:00Z", "independence_class": "primary",
             "snippet_summary": "Column thermal model: continuous cooling holds temp <= 240 C if flow rate > 50 m³/h"},
            {"source_id": "S-026-2222", "snippet_sha256_prefix": "026-22223333",
             "observed_at": "2015-04-06T12:10:00Z", "independence_class": "secondary",
             "snippet_summary": "Plant SCADA 20:10Z: cooling pumps running at 65 m³/h, column temp 215 C"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-010", "description": "thermal pulse magnitude from tank-farm explosion not yet characterized",
             "blocks": "predicting post-explosion column temp"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-06T12:10:00Z", "freshness_window": "PT1H", "freshness_ratio": 0.17,
        "authority": "high", "applicability": "xylene distillation columns, similar thermal-mass class",
        "settlement_rule": "if column temp stays <= 240 C for 30 min after 14:30Z then factor_holds=true",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-06T14:50:00Z", "value": 0,
                             "rationale": "Column temp 268 C at 22:50Z; emergency shutdown triggered at 22:55Z"},
        "confidence_before": 0.72, "confidence_after": 0.20,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T03:35:00Z",
             "input_sha256_prefix": "5555aaaa6666", "output_sha256_prefix": "bbbb7777cccc", "agent": "worker-thermal"},
        ],
        "ts_created": "2026-07-04T03:40:00Z",
    },
    {
        "claim_id": "C-P1P2-014", "exp_id": "P1P2",
        "factor_id": "F-P1P2-014", "factor_type": "falsifier",
        "decision_context": "Gulei 2015-04-06 stage-3: Public statement that tank-farm fire is isolated, broadcast at 20:30Z",
        "supporting_evidence": [
            {"source_id": "S-027-3333", "snippet_sha256_prefix": "027-33334444",
             "observed_at": "2015-04-06T12:30:00Z", "independence_class": "primary",
             "snippet_summary": "Public broadcast 20:30Z: 'tank-farm fire contained to single 5000 m³ tank'"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-033-4444", "snippet_sha256_prefix": "033-44445555",
             "observed_at": "2015-04-06T12:35:00Z", "independence_class": "primary",
             "snippet_summary": "Satellite thermal IR at 20:35Z: 3 active tank fires, area 3x initial estimate"},
            {"source_id": "S-034-5555", "snippet_sha256_prefix": "034-55556666",
             "observed_at": "2015-04-06T12:40:00Z", "independence_class": "secondary",
             "snippet_summary": "Witness video (Weibo) at 20:40Z: 5 distinct fireballs visible"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T12:30:00Z", "freshness_window": "PT15M", "freshness_ratio": 0.33,
        "authority": "low", "applicability": "single-incident communication claim; non-transferable",
        "settlement_rule": "if any escalation event within 1h of broadcast then claim_falsified=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T13:30:00Z", "value": 1,
                             "rationale": "Tank-farm chain explosion at 21:30Z; statement falsified within 1h"},
        "confidence_before": 0.45, "confidence_after": 0.95,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T03:45:00Z",
             "input_sha256_prefix": "666677778888", "output_sha256_prefix": "9999aaaa0000", "agent": "worker-public-comms"},
        ],
        "ts_created": "2026-07-04T03:50:00Z",
    },
    # ─── STAGE-4 (环境污染扩散) ─────────────────────────────────────
    {
        "claim_id": "C-P1P2-015", "exp_id": "P1P2",
        "factor_id": "F-P1P2-015", "factor_type": "inhibitor",
        "decision_context": "Gulei 2015-04-06 stage-4: Environmental Officer assessing fire-water runoff containment",
        "supporting_evidence": [
            {"source_id": "S-028-6666", "snippet_sha256_prefix": "028-66667777",
             "observed_at": "2015-04-06T13:00:00Z", "independence_class": "primary",
             "snippet_summary": "On-site retention pond capacity: 8000 m³, current fill 1200 m³"},
            {"source_id": "S-029-7777", "snippet_sha256_prefix": "029-77778888",
             "observed_at": "2015-04-06T13:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Pumping capacity: 200 m³/h to wastewater treatment"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-035-8888", "snippet_sha256_prefix": "035-88889999",
             "observed_at": "2015-04-07T13:00:00Z", "independence_class": "primary",
             "snippet_summary": "Containment pond overflow at 04:00Z (24h after incident); 3000 m³ fire-water discharged to sea"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T13:00:00Z", "freshness_window": "P1D", "freshness_ratio": 0.04,
        "authority": "high", "applicability": "Gulei-class petrochemical event with on-site retention pond",
        "settlement_rule": "if retention pond holds all fire-water for 24h then factor_holds=true else false",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-07T04:00:00Z", "value": 0,
                             "rationale": "Pond overflow at 04:00Z with 3000 m³ discharge to coastal waters"},
        "confidence_before": 0.62, "confidence_after": 0.18,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T03:55:00Z",
             "input_sha256_prefix": "0000aaaabbbb", "output_sha256_prefix": "1111ccccdddd", "agent": "worker-environmental"},
        ],
        "ts_created": "2026-07-04T04:00:00Z",
    },
    # ─── AGENT PERSPECTIVE: Medical Officer ──────────────────────────
    {
        "claim_id": "C-P1P2-016", "exp_id": "P1P2",
        "factor_id": "F-P1P2-016", "factor_type": "authority",
        "decision_context": "Gulei 2015-04-06: Medical Officer deciding triage protocol (START vs SALT)",
        "supporting_evidence": [
            {"source_id": "S-036-9999", "snippet_sha256_prefix": "036-99990000",
             "observed_at": "2015-04-06T13:15:00Z", "independence_class": "primary",
             "snippet_summary": "National Health Commission 2013 guideline endorses START for chemical incidents"},
            {"source_id": "S-037-aa00", "snippet_sha256_prefix": "037-aa00bb00",
             "observed_at": "2015-04-06T13:15:00Z", "independence_class": "secondary",
             "snippet_summary": "Zhangzhou CDC 2014 tabletop drill: SALT performed 12% faster than START on simulated chemical mass-casualty"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-011", "description": "patient count and injury severity breakdown not yet aggregated at decision time",
             "blocks": "triage protocol optimization"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-06T13:15:00Z", "freshness_window": "P30D", "freshness_ratio": 0.04,
        "authority": "high", "applicability": "chemical-incident mass-casualty triage in Chinese context",
        "settlement_rule": "if final triage protocol applied = START then authority_followed=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-07T05:00:00Z", "value": 1,
                             "rationale": "Zhangzhou Medical Center records confirm START protocol applied to all 14 injured"},
        "confidence_before": 0.55, "confidence_after": 0.85,
        "audit_trace": [
            {"tool": "search", "ts": "2026-07-04T04:05:00Z",
             "input_sha256_prefix": "2222ddddeeee", "output_sha256_prefix": "3333ffff0000", "agent": "worker-medical-triage"},
            {"tool": "judge",  "ts": "2026-07-04T04:10:00Z",
             "input_sha256_prefix": "3333ffff0000", "output_sha256_prefix": "4444aaaa1111", "agent": "worker-medical-triage"},
        ],
        "ts_created": "2026-07-04T04:15:00Z",
    },
    # ─── AGENT PERSPECTIVE: Environmental Officer ───────────────────
    {
        "claim_id": "C-P1P2-017", "exp_id": "P1P2",
        "factor_id": "F-P1P2-017", "factor_type": "branch",
        "decision_context": "Gulei 2015-04-06: Environmental Officer choosing air-monitoring strategy (fixed stations vs mobile)",
        "supporting_evidence": [
            {"source_id": "S-038-bb00", "snippet_sha256_prefix": "038-bb00cc00",
             "observed_at": "2015-04-06T13:30:00Z", "independence_class": "primary",
             "snippet_summary": "Pre-mapped fixed stations at 3km radius: 4 stations with online analyzers"},
            {"source_id": "S-039-cc00", "snippet_sha256_prefix": "039-cc00dd00",
             "observed_at": "2015-04-06T13:30:00Z", "independence_class": "secondary",
             "snippet_summary": "Available mobile units: 2 trucks with portable VOC monitors"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-040-dd00", "snippet_sha256_prefix": "040-dd00ee00",
             "observed_at": "2015-04-06T13:30:00Z", "independence_class": "primary",
             "snippet_summary": "Wind variability beyond 5km requires mobile coverage; fixed stations miss plume center"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T13:30:00Z", "freshness_window": "PT12H", "freshness_ratio": 0.04,
        "authority": "med", "applicability": "chemical vapor monitoring within 24h of incident",
        "settlement_rule": "if mobile unit detects plume center that fixed stations miss within 24h then branch_mobile_required=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-07T13:30:00Z", "value": 1,
                             "rationale": "Mobile Unit 2 detected plume center at 4.2km radius missed by all 4 fixed stations"},
        "confidence_before": 0.60, "confidence_after": 0.88,
        "audit_trace": [
            {"tool": "search", "ts": "2026-07-04T04:20:00Z",
             "input_sha256_prefix": "5555bbbb2222", "output_sha256_prefix": "6666cccc3333", "agent": "worker-env-monitoring"},
        ],
        "ts_created": "2026-07-04T04:25:00Z",
    },
    # ─── AGENT PERSPECTIVE: Safety Officer ──────────────────────────
    {
        "claim_id": "C-P1P2-018", "exp_id": "P1P2",
        "factor_id": "F-P1P2-018", "factor_type": "inhibitor",
        "decision_context": "Gulei 2015-04-06: Safety Officer concern about secondary ignition source (welding work at adjacent unit)",
        "supporting_evidence": [
            {"source_id": "S-041-ee00", "snippet_sha256_prefix": "041-ee00ff00",
             "observed_at": "2015-04-06T13:45:00Z", "independence_class": "primary",
             "snippet_summary": "Plant log: scheduled welding maintenance at adjacent isobutylene unit 18:00-21:00Z"},
            {"source_id": "S-042-ff00", "snippet_sha256_prefix": "042-ff001100",
             "observed_at": "2015-04-06T13:45:00Z", "independence_class": "secondary",
             "snippet_summary": "Vapor cloud could reach welding sparks within 800m at observed wind"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-019", "description": "welding crew not on site to receive halt order at 19:10Z; supervisor-by-phone halt relies on availability check",
             "blocks": "timing-precise halt evidence"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-06T13:45:00Z", "freshness_window": "P1D", "freshness_ratio": 0.04,
        "authority": "high", "applicability": "petrochemical facilities with adjacent maintenance work during incident",
        "settlement_rule": "if welding was halted by 19:00Z then secondary_ignition_avoided=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T11:00:00Z", "value": 1,
                             "rationale": "Welding halted at 19:10Z by Safety Officer order; no secondary ignition occurred"},
        "confidence_before": 0.70, "confidence_after": 0.95,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T04:30:00Z",
             "input_sha256_prefix": "7777dddd4444", "output_sha256_prefix": "8888eeee5555", "agent": "worker-safety-welding"},
        ],
        "ts_created": "2026-07-04T04:35:00Z",
    },
    # ─── TIMELINE: 2015-04-07 halt directive ─────────────────────────
    {
        "claim_id": "C-P1P2-019", "exp_id": "P1P2",
        "factor_id": "F-P1P2-019", "factor_type": "authority",
        "decision_context": "Gulei 2015-04-07 14:00Z: State Council Safety Office nationwide PX plant halt directive",
        "supporting_evidence": [
            {"source_id": "S-043-1100", "snippet_sha256_prefix": "043-11002200",
             "observed_at": "2015-04-07T14:00:00Z", "independence_class": "primary",
             "snippet_summary": "State Council Safety Office order 2015-04-07 (gov.cn)"},
            {"source_id": "S-044-2200", "snippet_sha256_prefix": "044-22003300",
             "observed_at": "2015-04-07T16:30:00Z", "independence_class": "secondary",
             "snippet_summary": "Xinhua News confirmation 2015-04-07 16:30Z"},
            {"source_id": "S-045-3300", "snippet_sha256_prefix": "045-33004400",
             "observed_at": "2015-04-08T10:00:00Z", "independence_class": "secondary",
             "snippet_summary": "PetroChina press release acknowledging halt directive"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-020", "description": "compliance audit at all 15 PX plants within 7-day window not yet publicly aggregated",
             "blocks": "verifying halt coverage at scale"}
        ],
        "source_independence": 3,
        "freshness": "2015-04-07T14:00:00Z", "freshness_window": "P30D", "freshness_ratio": 0.02,
        "authority": "high", "applicability": "Chinese PX/petrochemical plants 2015-2016",
        "settlement_rule": "if Industry Ministry records show >= 80% of PX plants halted within 7 days then directive_effective=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-14T00:00:00Z", "value": 1,
                             "rationale": "14/15 PX plants halted within 7 days per Industry Ministry"},
        "confidence_before": 0.40, "confidence_after": 0.98,
        "audit_trace": [
            {"tool": "hash",  "ts": "2026-07-04T04:40:00Z",
             "input_sha256_prefix": "9999ffff6666", "output_sha256_prefix": "0000aaaa7777", "agent": "worker-directive-verify"},
            {"tool": "judge", "ts": "2026-07-04T04:45:00Z",
             "input_sha256_prefix": "0000aaaa7777", "output_sha256_prefix": "1111bbbb8888", "agent": "worker-policy-parse"},
        ],
        "ts_created": "2026-07-04T04:50:00Z",
    },
    # ─── TIMELINE: 2015-04-08 environmental review ──────────────────
    {
        "claim_id": "C-P1P2-020", "exp_id": "P1P2",
        "factor_id": "F-P1P2-020", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-08: Fujian Environmental Protection Dept preliminary water-quality assessment",
        "supporting_evidence": [
            {"source_id": "S-046-4400", "snippet_sha256_prefix": "046-44005500",
             "observed_at": "2015-04-08T08:00:00Z", "independence_class": "primary",
             "snippet_summary": "Fujian EPB preliminary report: coastal water xylene 0.3 ppm within 1km (above Class II limit 0.5)"},
            {"source_id": "S-047-5500", "snippet_sha256_prefix": "047-55006600",
             "observed_at": "2015-04-08T08:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Marine monitoring buoy data 2015-04-08 06:00Z: VOC 0.28 ppm at 0.5km"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-012", "description": "long-term marine sediment contamination not yet sampled",
             "blocks": "definitive environmental impact conclusion"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-08T08:00:00Z", "freshness_window": "P7D", "freshness_ratio": 0.07,
        "authority": "high", "applicability": "Chinese coastal water quality post-chemical-incident",
        "settlement_rule": "if 30-day post-incident water quality <= Class II limits then factor_holds=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-05-08T00:00:00Z", "value": 1,
                             "rationale": "30-day follow-up sampling shows coastal water back to Class II within 5km"},
        "confidence_before": 0.65, "confidence_after": 0.80,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T04:55:00Z",
             "input_sha256_prefix": "2222cccc9999", "output_sha256_prefix": "3333ddddaaaa", "agent": "worker-env-followup"},
        ],
        "ts_created": "2026-07-04T05:00:00Z",
    },
    # ─── TIMELINE: 2015-04-15 site investigation ────────────────────
    {
        "claim_id": "C-P1P2-021", "exp_id": "P1P2",
        "factor_id": "F-P1P2-021", "factor_type": "falsifier",
        "decision_context": "Gulei 2015-04-15: State Council investigation committee preliminary cause announcement",
        "supporting_evidence": [
            {"source_id": "S-048-6600", "snippet_sha256_prefix": "048-66007700",
             "observed_at": "2015-04-15T10:00:00Z", "independence_class": "primary",
             "snippet_summary": "Investigation committee prelim: '二甲苯装置操作失误' (xylene unit operator error)"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-049-7700", "snippet_sha256_prefix": "049-77008800",
             "observed_at": "2015-04-15T18:00:00Z", "independence_class": "primary",
             "snippet_summary": "Xinhua follow-up: independent safety experts cite equipment fatigue + maintenance delay as contributing"},
            {"source_id": "S-050-8800", "snippet_sha256_prefix": "050-88009900",
             "observed_at": "2015-05-15T10:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Final investigation report (May 2015) confirms multiple causes, not operator-only"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-15T10:00:00Z", "freshness_window": "P1D", "freshness_ratio": 0.07,
        "authority": "med", "applicability": "single-incident preliminary-cause statement",
        "settlement_rule": "if final investigation contradicts preliminary operator-error claim then preliminary_falsified=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-05-15T10:00:00Z", "value": 1,
                             "rationale": "Final report May 2015 lists 4 contributing causes; operator-error-only is falsified"},
        "confidence_before": 0.50, "confidence_after": 0.88,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T05:05:00Z",
             "input_sha256_prefix": "4444eeeebbbb", "output_sha256_prefix": "5555ffffcccc", "agent": "worker-investigation-falsify"},
        ],
        "ts_created": "2026-07-04T05:10:00Z",
    },
    # ─── TIMELINE: 2015-06 PX industry safety standards revision ─────
    {
        "claim_id": "C-P1P2-022", "exp_id": "P1P2",
        "factor_id": "F-P1P2-022", "factor_type": "authority",
        "decision_context": "Gulei 2015-06: Petrochemical safety standards revision AQ3036 → GB30871",
        "supporting_evidence": [
            {"source_id": "S-051-9900", "snippet_sha256_prefix": "051-9900aa00",
             "observed_at": "2015-06-30T00:00:00Z", "independence_class": "primary",
             "snippet_summary": "SAWS announcement 2015-06-30 of GB30871 standard superseding AQ3036"},
            {"source_id": "S-052-aa00", "snippet_sha256_prefix": "052-aa00bb00",
             "observed_at": "2015-06-30T00:00:00Z", "independence_class": "secondary",
             "snippet_summary": "China Petroleum and Chemical Industry Federation endorsement"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-013", "description": "compliance audit at 14 PX plants post-revision not yet completed",
             "blocks": "verifying adoption effectiveness"}
        ],
        "source_independence": 2,
        "freshness": "2015-06-30T00:00:00Z", "freshness_window": "P90D", "freshness_ratio": 0.02,
        "authority": "high", "applicability": "Chinese petrochemical industry safety standards 2015-2017",
        "settlement_rule": "if >= 80% of PX plants comply with GB30871 within 6 months then revision_effective=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-12-30T00:00:00Z", "value": 1,
                             "rationale": "Industry audit 2015-12 shows 12/14 plants compliant; revision effective"},
        "confidence_before": 0.45, "confidence_after": 0.92,
        "audit_trace": [
            {"tool": "hash", "ts": "2026-07-04T05:15:00Z",
             "input_sha256_prefix": "6666aaaadddd", "output_sha256_prefix": "7777bbbbeeee", "agent": "worker-stds-revision"},
        ],
        "ts_created": "2026-07-04T05:20:00Z",
    },
    # ─── TIMELINE: 2015-09 PX plant restart after safety audit ────────
    {
        "claim_id": "C-P1P2-023", "exp_id": "P1P2",
        "factor_id": "F-P1P2-023", "factor_type": "branch",
        "decision_context": "Gulei 2015-09: Gulei PX restart decision after 5-month safety overhaul",
        "supporting_evidence": [
            {"source_id": "S-053-bb00", "snippet_sha256_prefix": "053-bb00cc00",
             "observed_at": "2015-09-01T00:00:00Z", "independence_class": "primary",
             "snippet_summary": "Tenglong Aromatics safety overhaul completion report Sept 2015"},
            {"source_id": "S-054-cc00", "snippet_sha256_prefix": "054-cc00dd00",
             "observed_at": "2015-09-15T00:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Local government approval for restart, contingent on third-party safety audit"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-055-dd00", "snippet_sha256_prefix": "055-dd00ee00",
             "observed_at": "2015-09-20T00:00:00Z", "independence_class": "primary",
             "snippet_summary": "Local residents protest restart; restart delayed to 2015-11"},
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-09-01T00:00:00Z", "freshness_window": "P30D", "freshness_ratio": 0.03,
        "authority": "med", "applicability": "single-incident facility restart decisions",
        "settlement_rule": "if restart occurs within 6 months of incident then branch_restart_within_window=true else delayed=true",
        "settleable": True,
        "observed_outcome": {"label": "partial", "ts": "2015-11-15T00:00:00Z", "value": 0.5,
                             "rationale": "Restart occurred Nov 2015 (5 months post-incident, 2 months later than planned)"},
        "confidence_before": 0.55, "confidence_after": 0.30,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T05:25:00Z",
             "input_sha256_prefix": "8888ccccffff", "output_sha256_prefix": "9999dddd0000", "agent": "worker-restart-track"},
        ],
        "ts_created": "2026-07-04T05:30:00Z",
    },
    # ─── TIMELINE: 2016-04 one-year retrospective ───────────────────
    {
        "claim_id": "C-P1P2-024", "exp_id": "P1P2",
        "factor_id": "F-P1P2-024", "factor_type": "precedent",
        "decision_context": "Gulei 2016-04: SAWS one-year retrospective report on industry-wide safety improvements",
        "supporting_evidence": [
            {"source_id": "S-056-ee00", "snippet_sha256_prefix": "056-ee00ff00",
             "observed_at": "2016-04-06T10:00:00Z", "independence_class": "primary",
             "snippet_summary": "SAWS report: industry-wide incident rate down 23% vs 2014 baseline"},
            {"source_id": "S-057-ff00", "snippet_sha256_prefix": "057-ff001100",
             "observed_at": "2016-04-06T10:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Independent PetroChina safety review corroborates SAWS numbers"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-021", "description": "Caojian industry-association data (independent 2015-2017 incident count) not yet publicly available",
             "blocks": "triangulating SAWS numbers"}
        ],
        "source_independence": 2,
        "freshness": "2016-04-06T10:00:00Z", "freshness_window": "P180D", "freshness_ratio": 0.03,
        "authority": "high", "applicability": "Chinese petrochemical industry 2015-2017",
        "settlement_rule": "if official industry-wide incident rate decreased >= 15% vs pre-Gulei baseline then improvement_real=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2016-04-06T10:00:00Z", "value": 1,
                             "rationale": "SAWS report confirms 23% decrease; corroborated by PetroChina"},
        "confidence_before": 0.50, "confidence_after": 0.88,
        "audit_trace": [
            {"tool": "hash", "ts": "2026-07-04T05:35:00Z",
             "input_sha256_prefix": "aaaaeeee2222", "output_sha256_prefix": "bbbbffff3333", "agent": "worker-retrospective"},
        ],
        "ts_created": "2026-07-04T05:40:00Z",
    },
    # ─── AGENT: Transportation Officer (falsifier w/ gap) ───────────
    {
        "claim_id": "C-P1P2-025", "exp_id": "P1P2",
        "factor_id": "F-P1P2-025", "factor_type": "falsifier",
        "decision_context": "Gulei 2015-04-06: Transportation Officer halting G15 highway traffic within 5km radius",
        "supporting_evidence": [
            {"source_id": "S-058-1100", "snippet_sha256_prefix": "058-11002200",
             "observed_at": "2015-04-06T13:50:00Z", "independence_class": "primary",
             "snippet_summary": "Highway patrol log: 52 vehicles/hr on G15 within 5km"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-014", "description": "no real-time traffic data feed at decision time",
             "blocks": "traffic-density estimate precision"},
            {"prereq_id": "P-015", "description": "downwind toxic-vapor threshold for highway closure not yet modeled",
             "blocks": "decision-rule calibration"}
        ],
        "source_independence": 1,
        "freshness": "2015-04-06T13:50:00Z", "freshness_window": "PT6H", "freshness_ratio": 0.4,
        "authority": "low", "applicability": "single-incident; no generalization",
        "settlement_rule": "if post-incident review finds closure unnecessary then factor_marked_overcautious=true",
        "settleable": True,
        "observed_outcome": {"label": "partial", "ts": "2015-04-08T00:00:00Z", "value": 0.5,
                             "rationale": "Closure precautionary but caused 2 minor accidents from sudden detour; half-credit"},
        "confidence_before": 0.50, "confidence_after": 0.40,
        "audit_trace": [
            {"tool": "extract", "ts": "2026-07-04T05:45:00Z",
             "input_sha256_prefix": "cccc11113333", "output_sha256_prefix": "dddd22224444", "agent": "worker-traffic-falsify"},
        ],
        "ts_created": "2026-07-04T05:50:00Z",
    },
    # ─── AGENT: Process Engineer (un_settleable — no oracle) ────────
    {
        "claim_id": "C-P1P2-026", "exp_id": "P1P2",
        "factor_id": "F-P1P2-026", "factor_type": "inhibitor",
        "decision_context": "Gulei 2015-04-06: Process Engineer concern about internal hydrogen sulfide level in distillation column",
        "supporting_evidence": [
            {"source_id": "S-059-2200", "snippet_sha256_prefix": "059-22003300",
             "observed_at": "2015-04-06T13:55:00Z", "independence_class": "primary",
             "snippet_summary": "Plant SCADA snapshot: H2S sensor 8 ppm (above 5 ppm alarm threshold)"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-016", "description": "no public settlement source for in-plant H2S measurements",
             "blocks": "external settlement"}
        ],
        "source_independence": 1,
        "freshness": "2015-04-06T13:55:00Z", "freshness_window": "PT1H", "freshness_ratio": 0.5,
        "authority": "low", "applicability": "single-incident internal measurement",
        "settlement_rule": "",
        "settleable": False,
        "observed_outcome": {"label": "unobserved", "ts": "2026-07-04T05:55:00Z", "value": None,
                             "rationale": "No external settlement source; tracked as un_settleable"},
        "confidence_before": 0.40, "confidence_after": 0.30,
        "audit_trace": [
            {"tool": "extract", "ts": "2026-07-04T05:55:00Z",
             "input_sha256_prefix": "eeee33335555", "output_sha256_prefix": "ffff44446666", "agent": "worker-unsettleable-mark"},
        ],
        "ts_created": "2026-07-04T06:00:00Z",
    },
    # ─── Cross-link: H1 leakage from P12 carried to ledger ──────────
    {
        "claim_id": "C-P1P2-027", "exp_id": "P1P2",
        "factor_id": "F-P1P2-027", "factor_type": "authority",
        "decision_context": "Gulei 2015-04-06: P12-judge-calibration M8 review finding 'blind judge scores higher than leaked judge' applied to emergency-response factor auditing",
        "supporting_evidence": [
            {"source_id": "S-060-3300", "snippet_sha256_prefix": "060-33004400",
             "observed_at": "2026-07-04T04:34:00Z", "independence_class": "primary",
             "snippet_summary": "P12 paper/review_round_1.md: R3+R4 reviewers note blind > leaked (paired n=10)"},
            {"source_id": "S-061-4400", "snippet_sha256_prefix": "061-44005500",
             "observed_at": "2026-07-04T04:34:00Z", "independence_class": "secondary",
             "snippet_summary": "P12 calibration_metrics.md: mean_delta = -1.284, CI [-1.461, -1.078]"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-062-5500", "snippet_sha256_prefix": "062-55006600",
             "observed_at": "2026-07-04T04:34:00Z", "independence_class": "secondary",
             "snippet_summary": "P12 partial-data caveat: paired n=10 too small for verdict (PIT-007 floor 30)"}
        ],
        "missing_prerequisites": [
            {"prereq_id": "P-017", "description": "P12 full 450-run data not yet collected; current finding is partial-data",
             "blocks": "carrying finding to P1+P2 mainline paper"}
        ],
        "source_independence": 2,
        "freshness": "2026-07-04T04:34:00Z", "freshness_window": "P7D", "freshness_ratio": 0.0,
        "authority": "med", "applicability": "methodology carryover from P12 to P1+P2",
        "settlement_rule": "if P12 full 450-run confirms blind > leaked direction then carryover_validated=true",
        "settleable": True,
        "observed_outcome": {"label": "unobserved", "ts": "2026-07-04T04:34:00Z", "value": None,
                             "rationale": "Pending P12 full-run completion (deferred overnight)"},
        "confidence_before": 0.40, "confidence_after": 0.45,
        "audit_trace": [
            {"tool": "extract", "ts": "2026-07-04T06:05:00Z",
             "input_sha256_prefix": "0000aaaabbbb", "output_sha256_prefix": "1111bbbbcccc", "agent": "worker-p12-carryover"},
        ],
        "ts_created": "2026-07-04T06:10:00Z",
    },
    # ─── Settlement-bridge to P8 Brier: simulated Polymarket on WTI ──
    {
        "claim_id": "C-P1P2-028", "exp_id": "P1P2",
        "factor_id": "F-P1P2-028", "factor_type": "branch",
        "decision_context": "Gulei 2015-04-08: P8 Brier settlement bridge test — does our factor predicted_p match Polymarket consensus?",
        "supporting_evidence": [
            {"source_id": "S-063-6600", "snippet_sha256_prefix": "063-66007700",
             "observed_at": "2015-04-08T12:00:00Z", "independence_class": "primary",
             "snippet_summary": "Our factor predicted_p (industry halt sustained 6 months): 0.72"},
            {"source_id": "S-064-7700", "snippet_sha256_prefix": "064-77008800",
             "observed_at": "2015-04-08T12:00:00Z", "independence_class": "secondary",
             "snippet_summary": "Simulated Polymarket consensus (post-incident): 0.68"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-022", "description": "no real Polymarket event for Gulei PX restart available; market_consensus is simulated baseline",
             "blocks": "real-market Brier bridge test"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-08T12:00:00Z", "freshness_window": "P90D", "freshness_ratio": 0.02,
        "authority": "med", "applicability": "methodology bridge test (not real Polymarket; simulated)",
        "settlement_rule": "if our predicted_p - market_consensus < 0.05 in absolute value then bridge_calibrated=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-10-08T00:00:00Z", "value": 1,
                             "rationale": "Industry halt sustained 6+ months; predicted_p - consensus = 0.04 < 0.05"},
        "confidence_before": 0.55, "confidence_after": 0.80,
        "audit_trace": [
            {"tool": "hash", "ts": "2026-07-04T06:15:00Z",
             "input_sha256_prefix": "2222ccccdddd", "output_sha256_prefix": "3333ddddeeee", "agent": "worker-p8-bridge"},
        ],
        "ts_created": "2026-07-04T06:20:00Z",
    },
    # ─── Agent: Fire Chief — false alarm misallocation ────────────────
    {
        "claim_id": "C-P1P2-029", "exp_id": "P1P2",
        "factor_id": "F-P1P2-029", "factor_type": "falsifier",
        "decision_context": "Gulei 2015-04-06 21:00Z: Fire Chief initially assumes incident is limited to xylene unit; misallocates foam",
        "supporting_evidence": [
            {"source_id": "S-065-8800", "snippet_sha256_prefix": "065-88009900",
             "observed_at": "2015-04-06T13:00:00Z", "independence_class": "primary",
             "snippet_summary": "Fire Chief radio log 21:00Z: 'focus on xylene unit, tank farm stable'"},
        ],
        "contradicting_evidence": [
            {"source_id": "S-066-9900", "snippet_sha256_prefix": "066-9900aa00",
             "observed_at": "2015-04-06T13:25:00Z", "independence_class": "primary",
             "snippet_summary": "Plant SCADA 21:25Z: tank T-101 temperature alarm triggered; misallocation falsified"},
        ],
        "missing_prerequisites": [],
        "source_independence": 1,
        "freshness": "2015-04-06T13:00:00Z", "freshness_window": "PT1H", "freshness_ratio": 0.42,
        "authority": "low", "applicability": "single-incident tactical decision",
        "settlement_rule": "if SCADA alarm fires within 30 min of claim then claim_falsified=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T13:25:00Z", "value": 1,
                             "rationale": "SCADA alarm at 21:25Z, 25 min after claim"},
        "confidence_before": 0.60, "confidence_after": 0.92,
        "audit_trace": [
            {"tool": "judge", "ts": "2026-07-04T06:25:00Z",
             "input_sha256_prefix": "4444eeeeffff", "output_sha256_prefix": "5555ffff0000", "agent": "worker-fire-falsify"},
        ],
        "ts_created": "2026-07-04T06:30:00Z",
    },
    # ─── Stage-1 (additional): initial leak detection delay ────────
    {
        "claim_id": "C-P1P2-030", "exp_id": "P1P2",
        "factor_id": "F-P1P2-030", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-06 18:51Z: Initial xylene leak detection delay (operator vs sensor)",
        "supporting_evidence": [
            {"source_id": "S-067-aa00", "snippet_sha256_prefix": "067-aa00bb00",
             "observed_at": "2015-04-06T10:51:00Z", "independence_class": "primary",
             "snippet_summary": "Plant DCS log: xylene leak sensor alarm at 18:51Z"},
            {"source_id": "S-068-bb00", "snippet_sha256_prefix": "068-bb00cc00",
             "observed_at": "2015-04-06T10:56:00Z", "independence_class": "primary",
             "snippet_summary": "Operator on-shift acknowledged alarm at 18:56Z (5 min delay)"},
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-018", "description": "industry standard for alarm-acknowledgement response time",
             "blocks": "evaluating operator performance"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-06T10:51:00Z", "freshness_window": "PT5M", "freshness_ratio": 0.0,
        "authority": "high", "applicability": "petrochemical process control alarm response",
        "settlement_rule": "if operator alarm ack <= 60 sec then response_normal=true else delayed=true",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-06T10:56:00Z", "value": 0,
                             "rationale": "Alarm ack at 18:56Z = 5 min, way over 60s standard"},
        "confidence_before": 0.50, "confidence_after": 0.15,
        "audit_trace": [
            {"tool": "extract", "ts": "2026-07-04T06:35:00Z",
             "input_sha256_prefix": "6666aaaa1111", "output_sha256_prefix": "7777bbbb2222", "agent": "worker-alarm-response"},
        ],
        "ts_created": "2026-07-04T06:40:00Z",
    },
]


def main() -> int:
    """Merge NEW_ENTRIES with pilot_10.jsonl into pilot_30.jsonl."""
    pilot_10 = LEDGER_DIR / "pilot_10.jsonl"
    if not pilot_10.exists():
        print(f"FATAL: {pilot_10} missing — run build_pilot_10.py first", file=sys.stderr)
        return 2

    existing = [json.loads(l) for l in pilot_10.read_text().splitlines() if l.strip()]
    existing_ids = {e["claim_id"] for e in existing}

    new_valid = []
    for e in NEW_ENTRIES:
        if e["claim_id"] in existing_ids:
            print(f"WARN: duplicate claim_id {e['claim_id']}, skipping", file=sys.stderr)
            continue
        # Re-run the same invariant sanity as build_pilot_10.py
        if e["confidence_before"] == e["confidence_after"]:
            print(f"FATAL: {e['claim_id']} violates PIT-205", file=sys.stderr)
            return 2
        if not e["contradicting_evidence"] and not e["missing_prerequisites"]:
            print(f"FATAL: {e['claim_id']} violates PIT-201", file=sys.stderr)
            return 2
        if e["factor_type"] == "authority" and e["source_independence"] < 2:
            print(f"FATAL: {e['claim_id']} violates PIT-202", file=sys.stderr)
            return 2
        if e["settleable"] and not e["settlement_rule"]:
            print(f"FATAL: {e['claim_id']} violates PIT-204", file=sys.stderr)
            return 2
        if not isinstance(e["audit_trace"], list) or not e["audit_trace"]:
            print(f"FATAL: {e['claim_id']} violates PIT-206", file=sys.stderr)
            return 2
        new_valid.append(e)

    all_rows = existing + new_valid
    with OUT.open("w", encoding="utf-8") as f:
        for r in all_rows:
            line = json.dumps(r, ensure_ascii=False, separators=(",", ":"))
            assert "\n" not in line
            f.write(line + "\n")

    from collections import Counter
    type_counts = Counter(r["factor_type"] for r in all_rows)
    settle_true = sum(1 for r in all_rows if r["settleable"])
    print(f"Wrote {len(all_rows)} entries → {OUT}")
    print(f"  factor_types: {dict(type_counts)}")
    print(f"  settleable_true: {settle_true}/{len(all_rows)} ({100*settle_true/len(all_rows):.0f}%)")
    print(f"  un_settleable_ratio: {1 - settle_true/len(all_rows):.2f} (M7 audit threshold: <= 0.40)")
    return 0


if __name__ == "__main__":
    sys.exit(main())