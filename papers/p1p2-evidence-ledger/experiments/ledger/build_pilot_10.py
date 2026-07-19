#!/usr/bin/env python3
"""P1+P2 M1 — Author 10 handcrafted evidence_ledger_entry rows for the
Gulei petrochemical 4·6 incident.

Each row must satisfy the 6 PIT invariants (201..206) defined in
`framework/schemas/data-contracts.md` §8 and `state/io_spec.md` §2.

The 10 rows deliberately cover:
  - all 5 factor_types (precedent, inhibitor, branch, falsifier, authority)
  - both settleable=true and settleable=false
  - at least one row triggering PIT-203 (stale ratio > 1.0) for the
    freshness audit script to find
  - at least one row with factor_type=authority and source_independence=2
    so PIT-202 passes non-trivially
  - all 10 rows have confidence_before != confidence_after (PIT-205)

This script is the canonical source for `pilot_10.jsonl`; any change
to the pilot data must be made here and the file regenerated, not
hand-edited, so the audit chain stays intact.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent.parent
LEDGER_DIR = P12_ROOT / "experiments" / "ledger"
OUT = LEDGER_DIR / "pilot_10.jsonl"
LEDGER_DIR.mkdir(parents=True, exist_ok=True)


def S(prefix: str, summary: str, observed: str, klass: str) -> dict:
    """Shorthand for a source-evidence reference."""
    return {
        "source_id": f"S-{prefix}",
        "snippet_sha256_prefix": prefix,
        "observed_at": observed,
        "independence_class": klass,
        "snippet_summary": summary,
    }


def AUDIT(tool: str, ts: str, inp: str, out: str, agent: str) -> dict:
    return {"tool": tool, "ts": ts,
            "input_sha256_prefix": inp, "output_sha256_prefix": out, "agent": agent}


# 10 handcrafted entries — each one designed to test a specific invariant or
# provide a representative factor for the Gulei petrochemical scenario.

ENTRIES = [
    # ─────────────────────────────────────────────────────────────────
    # 1 — PRECEDENT: foam suppression timing (above-written sample)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-001", "exp_id": "P1P2",
        "factor_id": "F-P1P2-001", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-06 stage-1 xylene leak; Incident Commander choosing foam-vs-dry-chemical suppression",
        "supporting_evidence": [
            S("001-9b1c0a", "Industry foam-suppression manual: xylene class II flammable, AFFF 3% at 6.5 L/min/m^2 suppresses pool fire within 4h", "2015-04-06T11:30:00Z", "primary"),
            S("002-3f8e91", "Sinopec refinery incident report 2014-Q3: identical xylene pool fire suppressed by foam in 5.2h, no escalation", "2014-09-12T08:00:00Z", "secondary"),
        ],
        "contradicting_evidence": [
            S("014-7e0a9b", "On-scene fire chief radio log: wind shifted NE 35 degrees at 13:00Z; foam drift observed", "2015-04-06T13:00:00Z", "primary"),
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T11:30:00Z", "freshness_window": "P7D", "freshness_ratio": 0.04,
        "authority": "high", "applicability": "xylene-class II petrochemical pool fire, on-shore, daytime, wind < 5 m/s",
        "settlement_rule": "if pool fire controlled within 6h with foam AND no escalation to tank farm then factor_confirmed=true else false",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-07T00:00:00Z", "value": 0,
                             "rationale": "Wind shift at 13:00Z caused foam drift; pool fire escalated to tank farm at 14:30Z"},
        "confidence_before": 0.72, "confidence_after": 0.41,
        "audit_trace": [
            AUDIT("search", "2026-07-04T01:00:00Z", "ab12cd34ef56", "9988776655aa", "worker-evidence-extract"),
            AUDIT("judge",  "2026-07-04T01:05:00Z", "9988776655aa", "11223344aabb", "worker-source-independence"),
        ],
        "ts_created": "2026-07-04T01:10:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 2 — INHIBITOR: insufficient foam stock prevents full application
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-002", "exp_id": "P1P2",
        "factor_id": "F-P1P2-002", "factor_type": "inhibitor",
        "decision_context": "Gulei 2015-04-06: Logistics Officer reports only 40% of required AFFF stock on-site; cross-region replenishment ETA 8h",
        "supporting_evidence": [
            S("003-aa11bb", "On-site inventory log: 12 of 30 required AFFF drums present at 19:30Z", "2015-04-06T11:30:00Z", "primary"),
            S("004-cc22dd", "Zhangzhou emergency-mgmt dispatch log: nearest replenishment 240km away, delivery ETA 8h", "2015-04-06T12:00:00Z", "secondary"),
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-001", "description": "actual fire-area size in m^2 not yet measured", "blocks": "foam rate calculation"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-06T12:00:00Z", "freshness_window": "P1D", "freshness_ratio": 0.5,
        "authority": "med", "applicability": "Gulei-class petrochemical event within 24h, similar stockpile policy era",
        "settlement_rule": "if observed AFFF consumption rate within +/-15% of pre-incident model then factor_confirmed=true else false",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T20:00:00Z", "value": 1,
                             "rationale": "Stock ran out at 22:00Z; replenishment arrived 03:30Z next day; pre-incident model under-estimated rate by 22%"},
        "confidence_before": 0.30, "confidence_after": 0.85,
        "audit_trace": [
            AUDIT("extract", "2026-07-04T01:20:00Z", "deadbeef0001", "12345678aaaa", "worker-inhibitor-detect"),
        ],
        "ts_created": "2026-07-04T01:25:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 3 — BRANCH: choice between evacuate-3km vs evacuate-5km
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-003", "exp_id": "P1P2",
        "factor_id": "F-P1P2-003", "factor_type": "branch",
        "decision_context": "Gulei 2015-04-06 stage-2: Safety Officer deciding evacuation radius (3km vs 5km) given wind forecast NE 5-8 m/s",
        "supporting_evidence": [
            S("005-ee33ff", "EPA dispersion model AERMOD run: 3km radius sufficient for xylene vapor at observed wind", "2015-04-06T13:00:00Z", "primary"),
            S("006-114455", "Local meteorological station: wind sustained 5-8 m/s from NE for next 6h", "2015-04-06T13:30:00Z", "primary"),
        ],
        "contradicting_evidence": [
            S("015-6677aa", "Tank-farm explosion at 14:30Z produced secondary xylene release of 3x initial estimate", "2015-04-06T14:30:00Z", "primary"),
            S("016-8899bb", "Wind gust at 15:15Z reached 12 m/s, blowing vapor beyond 3km contour for 8 min", "2015-04-06T15:15:00Z", "secondary"),
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T13:00:00Z", "freshness_window": "PT6H", "freshness_ratio": 0.5,
        "authority": "high", "applicability": "downwind vapor dispersion, day-time, stable atmospheric class D",
        "settlement_rule": "if observed max vapor concentration at 3km boundary <= 1000 ppm within 24h then branch_3km_sufficient=true else branch_5km_required=true",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-07T13:00:00Z", "value": 0,
                             "rationale": "Max vapor concentration at 3km boundary reached 2800 ppm at 15:15Z; 5km evacuation was triggered"},
        "confidence_before": 0.65, "confidence_after": 0.30,
        "audit_trace": [
            AUDIT("search", "2026-07-04T01:30:00Z", "feedface0002", "abcdef012345", "worker-branch-extract"),
            AUDIT("judge",  "2026-07-04T01:35:00Z", "abcdef012345", "56789abcdef0", "worker-disagreement-check"),
        ],
        "ts_created": "2026-07-04T01:40:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 4 — FALSIFIER: claim that escalation is contained is later falsified
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-004", "exp_id": "P1P2",
        "factor_id": "F-P1P2-004", "factor_type": "falsifier",
        "decision_context": "Gulei 2015-04-06 stage-3: Communications Officer issuing public statement that escalation is contained; meanwhile tank-farm chain explosion in progress",
        "supporting_evidence": [
            S("007-cdcdcd", "Public statement broadcast at 13:50Z: 'fire under control, no further escalation expected'", "2015-04-06T13:50:00Z", "primary"),
        ],
        "contradicting_evidence": [
            S("017-efef01", "Tank-farm chain explosion at 14:30Z (40 min later) — direct falsification of containment claim", "2015-04-06T14:30:00Z", "primary"),
            S("018-0123ab", "Satellite thermal imagery at 15:00Z: 3 active tank fires, area doubled", "2015-04-06T15:00:00Z", "secondary"),
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T13:50:00Z", "freshness_window": "PT30M", "freshness_ratio": 1.3,
        "authority": "low", "applicability": "single-incident falsifier; non-transferable",
        "settlement_rule": "if any subsequent escalation event within 1h of statement then claim_falsified=true else claim_holds=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T14:30:00Z", "value": 1,
                             "rationale": "Falsified within 40 min by tank-farm chain explosion"},
        "confidence_before": 0.55, "confidence_after": 0.92,
        "audit_trace": [
            AUDIT("judge", "2026-07-04T01:50:00Z", "aaaabbbb1111", "ccccdddd2222", "worker-falsifier-detect"),
        ],
        "ts_created": "2026-07-04T01:55:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 5 — AUTHORITY: regulator directive (REQUIRES source_independence >= 2)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-005", "exp_id": "P1P2",
        "factor_id": "F-P1P2-005", "factor_type": "authority",
        "decision_context": "Gulei 2015-04-06: State Council Safety Office directive ordering all PX plants nationwide to halt production pending inspection",
        "supporting_evidence": [
            S("008-aabbcc", "State Council Safety Office order doc 2015-04-07 14:00Z (gov.cn published)", "2015-04-07T14:00:00Z", "primary"),
            S("009-ddeeff", "Xinhua News Agency confirmation report same day 16:30Z", "2015-04-07T16:30:00Z", "secondary"),
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-006", "description": "local-level compliance audit at each PX plant not yet collected at directive time", "blocks": "verifying halt coverage"}
        ],
        "source_independence": 2,
        "freshness": "2015-04-07T14:00:00Z", "freshness_window": "P30D", "freshness_ratio": 0.03,
        "authority": "high", "applicability": "all Chinese PX/petrochemical plants in 2015-2016",
        "settlement_rule": "if official production-halt records show >= 80% of PX plants halted within 7 days then directive_effective=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-14T00:00:00Z", "value": 1,
                             "rationale": "Industry Ministry records confirm 14/15 PX plants halted within 7 days"},
        "confidence_before": 0.40, "confidence_after": 0.95,
        "audit_trace": [
            AUDIT("hash",  "2026-07-04T02:00:00Z", "111122223333", "444455556666", "worker-authority-verify"),
            AUDIT("judge", "2026-07-04T02:05:00Z", "444455556666", "777788889999", "worker-policy-parse"),
        ],
        "ts_created": "2026-07-04T02:10:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 6 — PRECEDENT: terrain factor (coastal/onshore wind pattern)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-006", "exp_id": "P1P2",
        "factor_id": "F-P1P2-006", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-06: Environmental Officer assessing whether coastal/onshore wind reversal expected within 12h",
        "supporting_evidence": [
            S("010-998877", "Coastal meteorology textbook: coastal seabreeze reversal typical 14:00-17:00 local", "2014-01-01T00:00:00Z", "secondary"),
            S("011-776655", "Xiamen weather station historical April data: 73% of days show reversal between 14:00-17:00", "2014-12-31T23:59:00Z", "secondary"),
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-002", "description": "actual seabreeze timing on 2015-04-06 not yet in evidence set", "blocks": "factor confirmation"}
        ],
        "source_independence": 2,
        "freshness": "2014-12-31T23:59:00Z", "freshness_window": "P180D", "freshness_ratio": 0.65,
        "authority": "med", "applicability": "subtropical coastal sites, April, synoptic pressure gradient weak",
        "settlement_rule": "if observed wind direction reverses from NE to SW between 14:00-17:00 local on 2015-04-06 then factor_confirmed=true else false",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T15:00:00Z", "value": 1,
                             "rationale": "Wind reversal recorded at 14:45 local; factor holds"},
        "confidence_before": 0.50, "confidence_after": 0.78,
        "audit_trace": [
            AUDIT("search", "2026-07-04T02:15:00Z", "deadbeef0003", "feedface0004", "worker-terrain-precedent"),
        ],
        "ts_created": "2026-07-04T02:20:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 7 — STALE FACTOR: freshness_ratio > 1 (PIT-203 demo)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-007", "exp_id": "P1P2",
        "factor_id": "F-P1P2-007", "factor_type": "precedent",
        "decision_context": "Gulei 2015-04-06: Medical Officer citing a 2003 SARS-era quarantine protocol; protocol not updated since 2010",
        "supporting_evidence": [
            S("012-334455", "SARS-era quarantine manual 2003, last revised 2010", "2003-06-01T00:00:00Z", "primary"),
        ],
        "contradicting_evidence": [
            S("019-223344", "2014 Ebola response guideline supersedes SARS protocol for chemical-exposure scenarios", "2014-11-15T00:00:00Z", "primary"),
        ],
        "missing_prerequisites": [],
        "source_independence": 1,
        "freshness": "2003-06-01T00:00:00Z", "freshness_window": "P365D", "freshness_ratio": 11.7,
        "authority": "low", "applicability": "superseded by 2014 protocol; not applicable",
        "settlement_rule": "if Medical Officer applies 2014 protocol then factor_stale_demoted=true",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2015-04-06T18:00:00Z", "value": 1,
                             "rationale": "Medical team applied 2014 protocol; 2003 precedent marked stale in retrospective review"},
        "confidence_before": 0.45, "confidence_after": 0.15,
        "audit_trace": [
            AUDIT("search", "2026-07-04T02:30:00Z", "beadbead0005", "cafecafe0006", "worker-stale-detect"),
        ],
        "ts_created": "2026-07-04T02:35:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 8 — INHIBITOR: NOT settleable (no machine-checkable rule possible)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-008", "exp_id": "P1P2",
        "factor_id": "F-P1P2-008", "factor_type": "inhibitor",
        "decision_context": "Gulei 2015-04-06: Public Opinion Officer concerned about social-media amplification of incident imagery; no formal settlement source exists",
        "supporting_evidence": [
            S("013-9988aa", "Weibo sentiment scrape at 19:00Z: 41% of top-50 trending topics incident-related", "2015-04-06T11:00:00Z", "primary"),
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-003", "description": "no external settlement oracle for social-media impact", "blocks": "settlement"}
        ],
        "source_independence": 1,
        "freshness": "2015-04-06T11:00:00Z", "freshness_window": "PT12H", "freshness_ratio": 0.5,
        "authority": "low", "applicability": "Chinese social-media platforms in 2015",
        "settlement_rule": "",
        "settleable": False,
        "observed_outcome": {"label": "unobserved", "ts": "2026-07-04T02:40:00Z", "value": None,
                             "rationale": "No settlement source registered; tracked as un_settleable for M7 audit"},
        "confidence_before": 0.50, "confidence_after": 0.20,
        "audit_trace": [
            AUDIT("extract", "2026-07-04T02:40:00Z", "deadbeef0007", "feedface0008", "worker-unsettleable-mark"),
        ],
        "ts_created": "2026-07-04T02:45:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 9 — BRANCH: timing-dependent decision (alternate stage-3 path)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-009", "exp_id": "P1P2",
        "factor_id": "F-P1P2-009", "factor_type": "branch",
        "decision_context": "Gulei 2015-04-06 stage-3: Process Engineer choosing between continuous-cooling vs emergency-shutdown of adjacent xylene distillation column",
        "supporting_evidence": [
            S("016-aa00bb", "Distillation column thermal model: continuous cooling feasible if column temp <= 240 C", "2015-04-06T14:00:00Z", "primary"),
            S("017-cc11dd", "Plant SCADA snapshot at 14:15Z: column temp 198 C, holding steady", "2015-04-06T14:15:00Z", "primary"),
        ],
        "contradicting_evidence": [
            S("020-ee22ff", "Tank-farm explosion at 14:30Z delivered 200 C thermal pulse to column; SCADA shows 245 C at 14:35Z", "2015-04-06T14:35:00Z", "primary"),
        ],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2015-04-06T14:15:00Z", "freshness_window": "PT30M", "freshness_ratio": 0.67,
        "authority": "high", "applicability": "xylene distillation columns, similar thermal-mass class",
        "settlement_rule": "if column temp stays <= 240 C for 30 min after decision then branch_continuous_cooling_viable=true else branch_emergency_shutdown_required=true",
        "settleable": True,
        "observed_outcome": {"label": "refuted", "ts": "2015-04-06T14:50:00Z", "value": 0,
                             "rationale": "Column temp reached 268 C by 14:50Z; emergency shutdown triggered at 14:55Z"},
        "confidence_before": 0.70, "confidence_after": 0.25,
        "audit_trace": [
            AUDIT("judge", "2026-07-04T02:50:00Z", "baadf00d0009", "1234567890ab", "worker-branch-settle"),
        ],
        "ts_created": "2026-07-04T02:55:00Z",
    },
    # ─────────────────────────────────────────────────────────────────
    # 10 — FALSIFIER: confidence collapse on missing ground truth (missing_prerequisites)
    # ─────────────────────────────────────────────────────────────────
    {
        "claim_id": "C-P1P2-010", "exp_id": "P1P2",
        "factor_id": "F-P1P2-010", "factor_type": "falsifier",
        "decision_context": "Gulei 2015-04-06: Transportation Officer halting highway traffic within 5km; ground-truth on actual traffic density not yet collected",
        "supporting_evidence": [
            S("018-334466", "Highway patrol log at 12:30Z: 47 vehicles/hr counted on G15 highway within 5km radius", "2015-04-06T12:30:00Z", "primary"),
        ],
        "contradicting_evidence": [],
        "missing_prerequisites": [
            {"prereq_id": "P-004", "description": "no real-time traffic data feed at decision time; only manual patrol snapshots", "blocks": "traffic-density estimate precision"},
            {"prereq_id": "P-005", "description": "downwind toxic-vapor threshold for highway closure not yet modeled", "blocks": "decision-rule calibration"}
        ],
        "source_independence": 1,
        "freshness": "2015-04-06T12:30:00Z", "freshness_window": "PT6H", "freshness_ratio": 0.4,
        "authority": "low", "applicability": "single-incident, no generalization",
        "settlement_rule": "if downstream retrospective finds evidence-ledger predicted closure unnecessary (traffic already low) then factor_marked_overcautious=true",
        "settleable": True,
        "observed_outcome": {"label": "partial", "ts": "2015-04-08T00:00:00Z", "value": 0.5,
                             "rationale": "Closure was technically precautionary but caused 2 minor accidents from sudden detour; half-credit settlement"},
        "confidence_before": 0.55, "confidence_after": 0.42,
        "audit_trace": [
            AUDIT("extract", "2026-07-04T03:00:00Z", "f00ba7c0ffee", "deadbeef000a", "worker-falsifier-with-gap"),
            AUDIT("judge",   "2026-07-04T03:05:00Z", "deadbeef000a", "badcafe000b", "worker-gap-impact"),
        ],
        "ts_created": "2026-07-04T03:10:00Z",
    },
]


def main() -> int:
    # Sanity: every row has confidence_before != confidence_after (PIT-205)
    for i, e in enumerate(ENTRIES, 1):
        if e["confidence_before"] == e["confidence_after"]:
            print(f"FATAL row {i}: confidence_before == confidence_after violates PIT-205", file=sys.stderr)
            return 2
        # PIT-201: not both contradicting_evidence=[] and missing_prerequisites=[]
        if not e["contradicting_evidence"] and not e["missing_prerequisites"]:
            print(f"FATAL row {i}: violates PIT-201 — must declare contradicting OR missing", file=sys.stderr)
            return 2
        # PIT-202: authority requires source_independence >= 2
        if e["factor_type"] == "authority" and e["source_independence"] < 2:
            print(f"FATAL row {i}: violates PIT-202 — authority needs source_independence >= 2", file=sys.stderr)
            return 2
        # PIT-204: settleable=true requires non-empty settlement_rule
        if e["settleable"] and not e["settlement_rule"]:
            print(f"FATAL row {i}: violates PIT-204 — settleable=true requires non-empty settlement_rule", file=sys.stderr)
            return 2
        # PIT-206: audit_trace must be array
        if not isinstance(e["audit_trace"], list) or not e["audit_trace"]:
            print(f"FATAL row {i}: violates PIT-206 — audit_trace must be non-empty array", file=sys.stderr)
            return 2

    with OUT.open("w", encoding="utf-8") as f:
        lines_written = 0
        for e in ENTRIES:
            line = json.dumps(e, ensure_ascii=False, separators=(",", ":"))
            assert "\n" not in line, f"row {e['claim_id']} contains newline — would break JSONL"
            f.write(line + "\n")
            lines_written += 1
    print(f"Wrote {lines_written} entries → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())