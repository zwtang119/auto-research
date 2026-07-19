#!/usr/bin/env python3
"""P1+P2 M1 — Validator for `evidence_ledger_entry` JSONL files.

Enforces the 6 PIT invariants from `framework/schemas/data-contracts.md` §8
plus 2 supplementary checks (required-fields, JSON parse). Writes any
violations to `experiments/rejected_entries.jsonl` and exits non-zero
if any invariant fails.

Run from papers/p1p2-evidence-ledger/:
    python3 experiments/ledger/validate_ledger.py [--input PATH]

If --input omitted, validates all *.jsonl in experiments/ledger/.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent.parent
LEDGER_DIR = P12_ROOT / "experiments" / "ledger"
REJECTED = LEDGER_DIR / "rejected_entries.jsonl"
AGED = LEDGER_DIR / "aged_entries.jsonl"


REQUIRED_FIELDS = {
    "claim_id", "exp_id", "factor_id", "factor_type",
    "decision_context", "supporting_evidence", "contradicting_evidence",
    "missing_prerequisites", "source_independence",
    "freshness", "freshness_window", "freshness_ratio",
    "authority", "applicability",
    "settlement_rule", "settleable", "observed_outcome",
    "confidence_before", "confidence_after",
    "audit_trace", "ts_created",
}

VALID_FACTOR_TYPES = {"precedent", "inhibitor", "branch", "falsifier", "authority"}
VALID_AUTHORITY = {"high", "med", "low"}


def check_invariants(entry: dict) -> list[str]:
    """Return list of invariant-id violations (empty list = all pass)."""
    violations = []

    # Required fields
    missing = REQUIRED_FIELDS - set(entry.keys())
    if missing:
        violations.append(f"REQ_FIELDS: missing {sorted(missing)}")
        return violations  # can't check further

    # PIT-201: not both contradicting_evidence=[] and missing_prerequisites=[]
    if not entry["contradicting_evidence"] and not entry["missing_prerequisites"]:
        violations.append("PIT-201: contradicting_evidence=[] AND missing_prerequisites=[]")

    # PIT-202: authority ⇒ source_independence >= 2
    if entry["factor_type"] == "authority" and entry["source_independence"] < 2:
        violations.append(
            f"PIT-202: factor_type=authority requires source_independence >= 2, got {entry['source_independence']}"
        )

    # PIT-204: settleable=true ⇒ non-empty settlement_rule
    if entry["settleable"] and not entry["settlement_rule"]:
        violations.append("PIT-204: settleable=true requires non-empty settlement_rule")

    # PIT-205: confidence_before != confidence_after
    if entry["confidence_before"] == entry["confidence_after"]:
        violations.append(
            f"PIT-205: confidence_before == confidence_after == {entry['confidence_before']}"
        )

    # PIT-206: audit_trace is non-empty array of {tool, *_sha256_prefix}
    if not isinstance(entry["audit_trace"], list) or not entry["audit_trace"]:
        violations.append("PIT-206: audit_trace must be non-empty array")
    else:
        for i, step in enumerate(entry["audit_trace"]):
            if "tool" not in step:
                violations.append(f"PIT-206: audit_trace[{i}] missing 'tool'")
            if not any(k.endswith("_sha256_prefix") for k in step):
                violations.append(f"PIT-206: audit_trace[{i}] missing any '*_sha256_prefix' field")

    # Type checks
    if entry["factor_type"] not in VALID_FACTOR_TYPES:
        violations.append(f"TYPE: factor_type={entry['factor_type']} not in {VALID_FACTOR_TYPES}")
    if entry["authority"] not in VALID_AUTHORITY:
        violations.append(f"TYPE: authority={entry['authority']} not in {VALID_AUTHORITY}")
    if not isinstance(entry["source_independence"], int) or entry["source_independence"] < 1:
        violations.append(f"TYPE: source_independence must be int >= 1, got {entry['source_independence']}")
    for v_field in ("confidence_before", "confidence_after"):
        v = entry[v_field]
        if not isinstance(v, (int, float)) or not (0.0 <= v <= 1.0):
            violations.append(f"TYPE: {v_field} must be float in [0,1], got {v}")
    if not isinstance(entry["freshness_ratio"], (int, float)) or entry["freshness_ratio"] < 0:
        violations.append(f"TYPE: freshness_ratio must be non-negative, got {entry['freshness_ratio']}")

    # claim_id / factor_id pattern
    if not re.match(r"^C-P1P2-\d{3}$", entry["claim_id"]):
        violations.append(f"ID: claim_id={entry['claim_id']} does not match ^C-P1P2-NNN$")
    if not re.match(r"^F-P1P2-\d{3}$", entry["factor_id"]):
        violations.append(f"ID: factor_id={entry['factor_id']} does not match ^F-P1P2-NNN$")

    return violations


def check_stale(entry: dict) -> bool:
    """PIT-203: freshness_ratio > 1.0 ⇒ stale (separate file for the audit)."""
    return entry.get("freshness_ratio", 0) > 1.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, default=None,
                    help="Single JSONL file to validate. Defaults to all *.jsonl in experiments/ledger/.")
    ap.add_argument("--workdir", type=Path, default=LEDGER_DIR,
                    help="Where to write rejected_entries.jsonl and aged_entries.jsonl (default: experiments/ledger/).")
    args = ap.parse_args()
    workdir = args.workdir
    workdir.mkdir(parents=True, exist_ok=True)
    global REJECTED, AGED
    REJECTED = workdir / "rejected_entries.jsonl"
    AGED = workdir / "aged_entries.jsonl"

    targets = [args.input] if args.input else sorted(p for p in LEDGER_DIR.glob("*.jsonl")
                                                  if p.name not in ("rejected_entries.jsonl", "aged_entries.jsonl"))
    if not targets:
        print(f"FATAL: no JSONL files found in {LEDGER_DIR}", file=sys.stderr)
        return 2

    total = 0
    rejected = 0
    n_stale = 0
    invariant_counts = {}
    rejected_rows = []
    aged_rows = []

    for path in targets:
        if not path.exists():
            print(f"FATAL: {path} missing", file=sys.stderr)
            return 2
        for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            total += 1
            try:
                entry = json.loads(raw)
            except json.JSONDecodeError as e:
                rejected += 1
                rejected_rows.append({"line_no": line_no, "source_file": str(path),
                                      "raw": raw[:200], "violations": [f"PARSE: {e}"]})
                continue

            vs = check_invariants(entry)
            if vs:
                rejected += 1
                rejected_rows.append({"line_no": line_no, "source_file": str(path),
                                      "claim_id": entry.get("claim_id"),
                                      "violations": vs})
                for v in vs:
                    key = v.split(":")[0]
                    invariant_counts[key] = invariant_counts.get(key, 0) + 1
            if check_stale(entry):
                n_stale += 1
                aged_rows.append({"claim_id": entry["claim_id"],
                                  "freshness_ratio": entry["freshness_ratio"],
                                  "freshness_window": entry["freshness_window"]})

    if rejected_rows:
        REJECTED.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rejected_rows) + "\n")
    if aged_rows:
        AGED.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in aged_rows) + "\n")

    print(f"Validated {total} entries across {len(targets)} file(s)")
    print(f"  rejected: {rejected}")
    print(f"  stale (PIT-203 freshness_ratio>1): {n_stale}")
    if invariant_counts:
        print(f"  violations by invariant:")
        for k, v in sorted(invariant_counts.items()):
            print(f"    {k}: {v}")
    if rejected_rows:
        print("  detailed violations:")
        for r in rejected_rows[:10]:  # cap at 10 to avoid flooding stdout
            cid = r.get("claim_id", "(parse error)")
            for v in r["violations"]:
                print(f"    [{cid}] {v}")
        if len(rejected_rows) > 10:
            print(f"    ... and {len(rejected_rows) - 10} more (see rejected_entries.jsonl)")
    print(f"  rejected_entries file: {REJECTED if rejected_rows else '(not written — all passed)'}")
    print(f"  aged_entries file:     {AGED if aged_rows else '(not written — no stale)'}")

    return 0 if rejected == 0 else 1


if __name__ == "__main__":
    sys.exit(main())