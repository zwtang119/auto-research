#!/usr/bin/env python3
"""P7 M1 — signal_evidence_entry → evidence_ledger_entry.adapter.

Reads `signal_evidence_entry` rows (per framework/schemas/data-contracts.md §10)
emitted by the SignalFusionEngine, and adapts them into the two
`evidence_ledger_entry` reference-list fields (data-contracts.md §8):

    supporting_evidence[]      →  promoted from `confirmed_fact` signals
    contradicting_evidence[]   →  promoted from `weak_evidence` / `source_failure` signals

The adapter does NOT create new `evidence_ledger_entry` rows itself —
that's the consumer's job (P1+P2). It produces a *JSONL mapping file*
that the ledger builder can consume, so the per-row audit chain stays
intact (per PIT-207: source_type `free_text_trace` requires grounding).

Usage
-----
CLI:
    python3 experiments/adapter_signal_to_ledger.py \\
        --signals experiments/signals/sample_signals.jsonl \\
        --output experiments/signals_to_ledger.jsonl \\
        --scenario gulei_petrochemical

Programmatic:
    from adapter_signal_to_ledger import adapt_signal_row, group_by_claim
    refs = adapt_signal_row(signal_row, scenario="gulei")

Decision rules (per state/io_spec.md §3-4 and PIT-403/PIT-408)
----------------------------------------------------------------
- signal_type=confirmed_fact  → bucket=supporting, independence_class from datasource_status
- signal_type=weak_evidence    → bucket=contradicting, independence_class downgraded to "secondary"
- signal_type=missing_data     → bucket=contradicting (gap as negative signal)
- signal_type=source_failure   → bucket=contradicting (data quality reason)
- datasource_status != active  → REJECT (per PIT-403)
- datasource_id == polymarket  → REJECT (per PIT-403 / PIT-408: silent inclusion forbidden)
- numeric_forecast is null AND bucket=supporting  → REJECT (per PIT-302 / PIT-406:
  supporting evidence without numeric forecast is not actionable for P1.2 Brier)
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path

P7_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P7_ROOT / "experiments"

VALID_SIGNAL_TYPES = {"confirmed_fact", "weak_evidence", "missing_data", "source_failure"}
# PIT-403: do not silently include INACTIVE datasources.
VALID_DATASOURCE_STATUS = {"active"}
# PIT-403 / PIT-408: Polymarket is special-cased — must not be silently included
# (the Polymarket side is owned by P1.2 settlement layer).
FORBIDDEN_DATASOURCE_IDS = {"polymarket"}


def _classify_bucket(signal: dict) -> str | None:
    """Map signal_type → evidence_ledger_entry bucket name.

    Returns None if the signal should be rejected (returns reason via raise).
    """
    st = signal.get("signal_type")
    if st not in VALID_SIGNAL_TYPES:
        raise ValueError(f"invalid signal_type={st!r}")
    if st == "confirmed_fact":
        return "supporting"
    # weak_evidence, missing_data, source_failure all count as contradicting
    return "contradicting"


def _resolve_independence_class(signal: dict) -> str:
    """Independence class for the new evidence_ledger_entry reference.

    PIT-202: authority requires >=2 primary sources. Downgraded signals
    become secondary, not primary.
    """
    if signal.get("signal_type") == "confirmed_fact":
        return "primary"
    if signal.get("signal_type") == "weak_evidence":
        return "secondary"
    return "tertiary"


def adapt_signal_row(signal: dict, scenario: str) -> dict:
    """Adapt one signal_evidence_entry row into a ledger-ref mapping.

    Returns a dict with bucket/source_id/observed_at/independence_class/
    scenario/extra metadata. Raises ValueError for invalid input.
    """
    # PIT-403: reject INACTIVE datasources
    if signal.get("datasource_status") not in VALID_DATASOURCE_STATUS:
        raise ValueError(f"datasource_status={signal.get('datasource_status')!r} (must be 'active')")
    # PIT-403 / PIT-408: do not silently include Polymarket
    if signal.get("datasource_id") in FORBIDDEN_DATASOURCE_IDS:
        raise ValueError(f"datasource_id={signal.get('datasource_id')!r} is forbidden (P1.2 side)")

    bucket = _classify_bucket(signal)
    # PIT-302 / PIT-406: supporting evidence without numeric_forecast is
    # not actionable for P1.2 Brier — flag for downstream rejection.
    rejected = False
    reject_reason = None
    if bucket == "supporting" and signal.get("numeric_forecast") is None:
        rejected = True
        reject_reason = "PIT-302: supporting signal without numeric_forecast is not actionable"

    sig_id = signal.get("signal_id", "UNKNOWN")
    # PIT-NEW-9: snippet_sha256_prefix must be a REAL SHA256, not fabricated.
    # Hash the canonical signal content (signal_id + scenario + scenario_text + numeric_forecast);
    # truncate to 12 hex chars (matches data-contracts.md §8 12-char prefix convention).
    canonical = json.dumps(
        {
            "signal_id": sig_id,
            "scenario": scenario,
            "scenario_text": signal.get("scenario_text"),
            "numeric_forecast": signal.get("numeric_forecast"),
        },
        sort_keys=True, ensure_ascii=False, separators=(",", ":"),
    )
    sha = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:12]
    return {
        "source_id": sig_id,  # already has "SIG-" prefix per data-contracts §10
        "snippet_sha256_prefix": sha,
        "observed_at": signal.get("observed_at"),
        "independence_class": _resolve_independence_class(signal),
        "bucket": bucket,
        "scenario": scenario,
        "datasource_id": signal.get("datasource_id"),
        "lens_weight": signal.get("lens_weight"),
        "recency_weight": signal.get("recency_weight"),
        "numeric_forecast": signal.get("numeric_forecast"),
        "scenario_text": signal.get("scenario_text"),
        "rejected": rejected,
        "reject_reason": reject_reason,
    }


def group_by_claim(mappings: list[dict], claim_id: str) -> dict:
    """Group a list of signal-derived mappings into one claim's
    supporting/contradicting reference lists (skipping rejected rows).

    Returns a dict with `supporting_evidence` and `contradicting_evidence`
    arrays ready to be spliced into an evidence_ledger_entry.
    """
    out = {"claim_id": claim_id,
           "supporting_evidence": [],
           "contradicting_evidence": [],
           "rejected": []}
    for m in mappings:
        if m["rejected"]:
            out["rejected"].append({"source_id": m["source_id"], "reason": m["reject_reason"]})
            continue
        ref = {
            "source_id": m["source_id"],
            "snippet_sha256_prefix": m["snippet_sha256_prefix"],
            "observed_at": m["observed_at"],
            "independence_class": m["independence_class"],
            "snippet_summary": f"Signal {m['source_id']} from {m['datasource_id']} (lens={m['lens_weight']}, recency={m['recency_weight']})",
        }
        if m["bucket"] == "supporting":
            out["supporting_evidence"].append(ref)
        else:
            out["contradicting_evidence"].append(ref)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", type=Path, required=True,
                    help="JSONL of signal_evidence_entry rows.")
    ap.add_argument("--output", type=Path, required=True,
                    help="JSONL of per-signal adapter mappings.")
    ap.add_argument("--grouped-output", type=Path, default=None,
                    help="Optional JSON: per-claim grouped {supporting, contradicting} reference lists.")
    ap.add_argument("--scenario", type=str, default="gulei_petrochemical",
                    help="scenario tag forwarded to P1+P2 evidence_ledger_entry.scenario_text")
    ap.add_argument("--claim-id", type=str, default="C-P1P2-AUTO",
                    help="default claim_id when --grouped-output is used")
    args = ap.parse_args()

    if not args.signals.exists():
        print(f"FATAL: {args.signals} missing", file=sys.stderr)
        return 2

    mappings = []
    rejected = 0
    by_claim: dict[str, list[dict]] = {args.claim_id: []}
    for line_no, raw in enumerate(args.signals.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            signal = json.loads(raw)
            m = adapt_signal_row(signal, scenario=args.scenario)
            mappings.append(m)
            if not m["rejected"]:
                by_claim[args.claim_id].append(m)
        except ValueError as e:
            rejected += 1
            print(f"WARN line {line_no}: {e}", file=sys.stderr)
        except json.JSONDecodeError as e:
            rejected += 1
            print(f"WARN line {line_no}: JSON parse failed: {e}", file=sys.stderr)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for m in mappings:
            f.write(json.dumps(m, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Adapted {len(mappings)} signals → {args.output} (rejected={rejected})")

    if args.grouped_output:
        out = {cid: group_by_claim(ms, cid) for cid, ms in by_claim.items()}
        args.grouped_output.write_text(json.dumps(out, ensure_ascii=False, indent=2))
        n_supp = sum(len(v["supporting_evidence"]) for v in out.values())
        n_cont = sum(len(v["contradicting_evidence"]) for v in out.values())
        print(f"Grouped → {args.grouped_output} (supporting={n_supp}, contradicting={n_cont})")
    return 0


if __name__ == "__main__":
    sys.exit(main())