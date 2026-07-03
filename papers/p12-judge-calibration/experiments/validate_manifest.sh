#!/usr/bin/env bash
# P12 M1 manifest guard. Run from .../papers/p12-judge-calibration/.
# Exits 0 iff PIT-005, PIT-105, PIT-106 invariants hold for the manifest
# AND the manifest matches the frozen sample_ids_ordered list.
#
# Implements state/io_spec.md §7.1 + §7.2 + §7.3 in a single shell guard
# so it can run between iterations (framework §9 rule 3).
set -euo pipefail

cd "$(dirname "$0")/.."

M=experiments/sample_manifest.jsonl
F=experiments/sample_ids_ordered.json
D=state/experiment_design.md

# Pre-registration artefact MUST exist before any results file is written
# (io_spec §7.8, PIT-006).
[ -f "$D" ] || { echo "FAIL: $D missing (PIT-006 violation)"; exit 1; }

[ -f "$M" ] || { echo "FAIL: $M missing"; exit 1; }
[ -f "$F" ] || { echo "FAIL: $F missing"; exit 1; }

# io_spec §7.1: json parse
jq . "$M" >/dev/null      || { echo "FAIL: $M not valid jsonl"; exit 1; }
jq . "$F" >/dev/null      || { echo "FAIL: $F not valid json"; exit 1; }

# n == 450
N=$(wc -l < "$M" | tr -d ' ')
[ "$N" = "450" ]          || { echo "FAIL: n=$N, expected 450"; exit 1; }

# io_spec §7.2: PIT-105 every row has path + 12-hex sha + blind-by-default
PASS=$(jq -c 'select(.source_path and .source_sha256_prefix and .condition_visible_to_judge==false)' "$M" | wc -l | tr -d ' ')
[ "$N" = "$PASS" ]        || { echo "FAIL: PIT-105 only $PASS/$N rows blind"; exit 1; }

# PIT-106: sample_ids_ordered matches manifest row order exactly
ORDER=$(jq -r '.sample_id' "$M" | paste -sd , -)
FROZEN=$(jq -r '.[]' "$F" | paste -sd , -)
[ "$ORDER" = "$FROZEN" ]  || { echo "FAIL: sample_ids_ordered != manifest order"; exit 1; }

# id integrity: P12-001 .. P12-450 with no gaps
EXPECTED=$(seq -f "P12-%03g" 1 450 | paste -sd , -)
[ "$FROZEN" = "$EXPECTED" ] || { echo "FAIL: sample_ids_ordered is not contiguous P12-001..P12-450"; exit 1; }

echo "OK: 450 rows, PIT-105 + PIT-106 invariants hold, pre-registration present"
