# P12 Judge Calibration M1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Pre-register the P12 judge-calibration experiment by writing `state/experiment_design.md`, generating `experiments/sample_manifest.jsonl` from P11 v5 A-runs (3 standard conditions × 50 runs × 3 enterprises = 450 samples), and freezing `experiments/sample_ids_ordered.json`. No judge invocation.

**Architecture:** A pure-data pre-registration step. Single Python builder script reads P11 yaml headers (no LLM calls), emits deterministic JSONL + JSON, validators live in shell and re-execute from `state/io_spec.md` §7. Outputs match the `sample_manifest` schema referenced by `state/io_spec.md` §1.1 and `data-contracts.md` §6.

**Tech Stack:** Python 3 (stdlib + `yaml`); `jq` for validators; no third-party deps beyond `pyyaml` (already used by P11). Scripts invoked from `papers/p12-judge-calibration/` working dir.

## Global Constraints

[Project-wide requirements binding EVERY task — version floors, dependency limits, naming and copy rules, platform requirements, exact values.]

- `exp_id` for P12 is **P12**. Sample id prefix: **P12-NNN**. Protocol run-id prefix: **R-P12-<protocol>-<NNN>**. (`state/io_spec.md` §1.)
- `original_condition` enumerated as exactly `inner_monologue | no_think | pure_analysis`. (`state/io_spec.md` §1.1.) — 750 A-runs minus the 300 `output_only`/`explicit_audit` ones = 450.
- `condition_visible_to_judge` MUST be `false` for every imported P11 sample (PIT-105).
- `sample_ids_ordered.json` is frozen once. All M2-M5 protocols iterate it in identical order (PIT-106).
- `state/experiment_design.md` is frozen at end of M1 (PIT-006); later edits route to `state/findings.jsonl`.
- Every script ≤ 300 lines (framework §9 engineering #1).
- All P11 imports carry `source_path` (absolute, relative to repo root) and `source_sha256_prefix` (12-char sha256 of file at import time).
- No LLM calls in M1. No judge invocation. No `experiments/*_results.json` writes.
- Working directory for ALL scripts and validators: `/Users/tangzw119/Documents/GitHub/auto-research/papers/p12-judge-calibration`.
- P11 source root used by imports: `../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/` (post-restructure).

---

## Task Decomposition

Three files, two test files, four validators. Each task produces a test-gated deliverable.

### Task 1: `state/experiment_design.md` (pre-registration, no code)

**Covers:** PIT-006, frozen pre-registration per `state/io_spec.md` §4.

**Files:**
- Create: `state/experiment_design.md`

**Interfaces:**
- Consumes: `state/task_spec.md`, `state/io_spec.md`, the P11 v5 metadata at `../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/metadata.json`, P12 `state/directions_tried.json`, P12 `wiki/concepts/judge-calibration-protocol.md`.
- Produces: a markdown file with all five required sections (`io_spec.md` §4).

- [ ] **Step 1: Write the design doc**

Write `papers/p12-judge-calibration/state/experiment_design.md` containing, in order:
- **§Hypothesis**: Calibration claim — `H_cal: When the same P11 sample is judged under (leaked, blind, pairwise, neighborhood, abstention), the leaked-vs-blind mean score delta is non-zero for ≥ 1 of the 3 standard conditions at α=0.05; otherwise the protocols are equivalent (null).`
- **§Primary metric**: `delta_score = leaked_score - blind_score` per sample; reported mean and 95% CI per condition.
- **§n per cell**: 150 per condition (3 enterprises × 50 runs/cell, parsed from filename pattern `^<condition>_<enterprise>_runNNN\.yaml$`).
- **§Sample set**: P11 v5 A-runs at `../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/` filtered to `original_condition ∈ {inner_monologue, no_think, pure_analysis}`. Excluded: `output_only`, `explicit_audit` (deferred to M3/M5 as transfer material).
- **§Frozen sample IDs order**: outer loop `condition` (`inner_monologue → no_think → pure_analysis`), inner loop `enterprise` (`ISPACE → LANDSPACE → SPACETIMETECH`, alphabetical ascending), inner `run_id` ascending (`001..050`).
- **§Frozen judge model list**: `DeepSeek-V4-Flash` (after P11 closure, this is the surviving in-house judge; `Kimi-K2.5` deferred as second judge in M3 to keep M2 cost down — per `directions_tried.json:directions[1].status: rejected_initially` rationale about not running a large benchmark in M2).
- **§Stop conditions**:
  - Direction pivot (structure): if `stale_count >= 2`, drop pairwise and abstention protocols and run only (leaked, blind, neighborhood).
  - Hard stop: `stale_count >= 4` → fold into P1+P2 methodology per `state/task_spec.md` "Stale Rules".
  - Effect-size early stop: if `|delta_score| < 0.05` AND 95% CI width `< 0.1` in all three conditions, end M2 with "no leakage effect" verdict.
- **§Pre-registration lock**: declare this file is now read-only; future findings append to `state/findings.jsonl`.

Constraints on the doc:
- ≤ 200 lines.
- Use the existing frontmatter style `> Created: 2026-07-03` borrowed from `state/io_spec.md` and `state/task_spec.md`.
- No new directories or files beyond this one in M1.

- [ ] **Step 2: Verify presence and PIT-006 invariant**

Run:
```bash
test -f papers/p12-judge-calibration/state/experiment_design.md && \
  head -1 papers/p12-judge-calibration/state/experiment_design.md | grep -q '^# P12' && \
  grep -q '## §Hypothesis' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §Primary metric' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §n per cell' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §Sample set' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §Frozen sample IDs order' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §Frozen judge model list' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §Stop conditions' papers/p12-judge-calibration/state/experiment_design.md && \
  grep -q '## §Pre-registration lock' papers/p12-judge-calibration/state/experiment_design.md
```
Expected: exit 0.

- [ ] **Step 3: Commit (deferred)**

Per user instruction "NEVER commit unless the user explicitly asks" — do NOT commit at this task. The `experiments/` outputs in Tasks 2-3 are also uncommitted. The session ends with a dirty working tree per framework §5.

---

### Task 2: `experiments/build_sample_manifest.py` + `experiments/test_build_sample_manifest.py` (TDD: RED → GREEN)

**Covers:** PIT-005, PIT-105, PIT-106 invariants in `state/io_spec.md` §1.1, §3, §7.2-7.3.

**Files:**
- Create: `experiments/build_sample_manifest.py`
- Create: `experiments/test_build_sample_manifest.py`
- Modify: `state/progress.json` (increment iteration, append a work log entry — optional, deferred)

**Interfaces:**
- Consumes: P11 v5 yaml files at `../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/` (path is relative to P12 working dir).
- Produces:
  - `experiments/sample_manifest.jsonl` — exactly 450 rows, one per P11 sample.
  - `experiments/sample_ids_ordered.json` — list of 450 sample_id strings in frozen execution order.

Row schema (matches `data-contracts.md` §6 and `state/io_spec.md` §1.1):
```json
{
  "sample_id": "P12-NNN",                      // zero-padded NNN ∈ [001, 450]
  "source_path": "legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/<file>.yaml",
  "source_sha256_prefix": "<first 12 hex chars of sha256 of file content at import>",
  "original_condition": "inner_monologue|no_think|pure_analysis",
  "original_enterprise": "ISPACE|LANDSPACE|SPACETIMETECH",
  "original_run_id": "001..050",                // string, zero-padded, as in filename
  "producer_model": "DeepSeek-V4-Flash",        // from metadata.json
  "judge_model_planned": "DeepSeek-V4-Flash",
  "condition_visible_to_judge": false,
  "imported_at": "2026-07-03T<HH:MM:SS>+08:00"
}
```

Sample id generation (frozen order):
- Outer loop `original_condition` in this order: `inner_monologue`, `no_think`, `pure_analysis`.
- Inner loop `original_enterprise` alphabetical: `ISPACE`, `LANDSPACE`, `SPACETIMETECH`.
- Inner loop `original_run_id` ascending `001..050` (numeric sort, not lexicographic).
- Assign `sample_id = f"P12-{counter:03d}"` with `counter` starting at 1.

This ordering is identical to the `sample_ids_ordered.json` array.

- [ ] **Step 1 (RED): Write the failing test**

`papers/p12-judge-calibration/experiments/test_build_sample_manifest.py`:

```python
import json, hashlib, os, re, subprocess, sys
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent          # .../papers/p12-judge-calibration/
P11_ROOT = (P12_ROOT.parent / "p1.1-inner-monologue"
                          / "legacy/p11-closed-v5-minimax-m3")
P11_A_YAML = P11_ROOT / "experiments" / "h5-emergence" / "A" / "yaml"


def _script_path():
    return P12_ROOT / "experiments" / "build_sample_manifest.py"


def _run():
    # Run from P12 working dir, write into experiments/.
    return subprocess.run(
        [sys.executable, str(_script_path())],
        cwd=str(P12_ROOT), capture_output=True, text=True, timeout=60,
    )


def test_script_runs_and_writes_files():
    out = _run()
    assert out.returncode == 0, f"script failed: {out.stderr}"
    assert (P12_ROOT / "experiments" / "sample_manifest.jsonl").exists()
    assert (P12_ROOT / "experiments" / "sample_ids_ordered.json").exists()


def test_manifest_row_count_is_450():
    out = _run()
    assert out.returncode == 0
    n = sum(1 for _ in open(P12_ROOT / "experiments" / "sample_manifest.jsonl"))
    assert n == 450, f"expected 450 rows, got {n}"


def test_every_row_passes_PIT_105_PIT_005_invariants():
    out = _run()
    assert out.returncode == 0
    manifest_path = P12_ROOT / "experiments" / "sample_manifest.jsonl"
    bad = []
    pat = re.compile(r"^P12-\d{3,}$")
    for line in open(manifest_path):
        row = json.loads(line)
        if not pat.match(row.get("sample_id", "")):
            bad.append(("bad_sample_id", row))
        if not row.get("source_path"):
            bad.append(("missing_source_path", row))
        if not row.get("source_sha256_prefix"):
            bad.append(("missing_sha", row))
        if row.get("condition_visible_to_judge") is not False:
            bad.append(("not_blind", row))
        if row.get("original_condition") not in {"inner_monologue", "no_think", "pure_analysis"}:
            bad.append(("bad_condition", row))
    assert not bad, f"PIT-blocked rows: {bad[:3]} (total {len(bad)})"


def test_sample_ids_ordered_matches_manifest_order():
    out = _run()
    assert out.returncode == 0
    manifest_path = P12_ROOT / "experiments" / "sample_manifest.jsonl"
    frozen_path = P12_ROOT / "experiments" / "sample_ids_ordered.json"
    manifest_ids = [json.loads(line)["sample_id"]
                    for line in open(manifest_path)]
    frozen_ids = json.loads(frozen_path.read_text())
    assert manifest_ids == frozen_ids, "frozen list must match manifest row order"


def test_sample_id_prefix_is_P12_NNN_with_no_gaps():
    out = _run()
    assert out.returncode == 0
    frozen_path = P12_ROOT / "experiments" / "sample_ids_ordered.json"
    frozen_ids = json.loads(frozen_path.read_text())
    expected = [f"P12-{i:03d}" for i in range(1, 451)]
    assert frozen_ids == expected


def test_sha_prefix_is_12_lowercase_hex_chars():
    out = _run()
    assert out.returncode == 0
    manifest_path = P12_ROOT / "experiments" / "sample_manifest.jsonl"
    bad = []
    for line in open(manifest_path):
        sha = json.loads(line)["source_sha256_prefix"]
        if not re.fullmatch(r"[0-9a-f]{12}", sha or ""):
            bad.append(sha)
    assert not bad, f"bad sha prefixes (first 3): {bad[:3]}"


def test_source_path_points_to_real_files():
    out = _run()
    assert out.returncode == 0
    manifest_path = P12_ROOT / "experiments" / "sample_manifest.jsonl"
    bad = []
    for line in open(manifest_path):
        row = json.loads(line)
        # source_path is repo-relative; resolve from auto-research root
        repo_root = P12_ROOT.parent.parent
        full = repo_root / row["source_path"]
        if not full.exists():
            bad.append(str(row["source_path"]))
    assert not bad, f"missing source files (first 3): {bad[:3]}"
```

- [ ] **Step 2 (Verify RED): Run the test, confirm it fails with `FileNotFoundError`**

Run: `pytest experiments/test_build_sample_manifest.py -v 2>&1 | head -30`
Expected: every test fails, errors stating `build_sample_manifest.py` does not exist OR `sample_manifest.jsonl` does not exist.

(If using a venv without pytest, run `python -m unittest experiments/test_build_sample_manifest.py` after adjusting — see Step 1 note below.)

**Note on test framework**: if `pytest` is not installed in the user's env, change tests to a single class `class TestManifest(unittest.TestCase)` with `def test_*` methods. Both frameworks are acceptable. The simpler choice for portability is `unittest`. Use whichever is in `p11.virtualenv` or system Python. Decide from `python -c "import pytest"` and the user's env. Prefer **`unittest` stdlib** to avoid an extra dep at the project root; adapt the test file accordingly.

- [ ] **Step 3 (GREEN): Write `experiments/build_sample_manifest.py`**

```python
#!/usr/bin/env python3
"""P12 M1 sample-manifest builder.

Reads P11 v5 A-yaml files at
  ../legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/
filters to 3 standard conditions (inner_monologue, no_think, pure_analysis),
emits experiments/sample_manifest.jsonl + experiments/sample_ids_ordered.json
in the frozen order described in state/experiment_design.md §§.

No LLM calls. Idempotent: running twice yields byte-identical output
(other than imported_at timestamp) provided the source files are unchanged.
"""
from __future__ import annotations
import hashlib, json, re, sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# --- Paths ---
P12_ROOT = Path(__file__).resolve().parent.parent
AUTO_ROOT = P12_ROOT.parent.parent                 # .../auto-research
P11_ROOT = (AUTO_ROOT / "p1.1-inner-monologue"
                      / "legacy/p11-closed-v5-minimax-m3")
P11_A_YAML = P11_ROOT / "experiments" / "h5-emergence" / "A" / "yaml"
P11_METADATA = P11_ROOT / "experiments" / "h5-emergence" / "metadata.json"

EXPERIMENTS = P12_ROOT / "experiments"
MANIFEST_PATH = EXPERIMENTS / "sample_manifest.jsonl"
FROZEN_PATH = EXPERIMENTS / "sample_ids_ordered.json"

STANDARD_CONDITIONS = ["inner_monologue", "no_think", "pure_analysis"]
ENTERPRISES_ALPHA = ["ISPACE", "LANDSPACE", "SPACETIMETECH"]

TZ_UTC8 = timezone(timedelta(hours=8))
NOW = lambda: datetime.now(TZ_UTC8).strftime("%Y-%m-%dT%H:%M:%S+08:00")


FILENAME_RE = re.compile(r"^(?P<cond>[^_]+)_(?P<ent>[A-Z0-9]+)_run(?P<rid>\d{3})\.yaml$")


def sha12(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def build_rows():
    rows = []
    counter = 0
    for cond in STANDARD_CONDITIONS:
        for ent in ENTERPRISES_ALPHA:
            for rid_int in range(1, 51):
                rid = f"{rid_int:03d}"
                fname = f"{cond}_{ent}_run{rid}.yaml"
                full = P11_A_YAML / fname
                if not full.exists():
                    # skip silently when a cell is short — log and continue
                    print(f"warn: missing {fname}", file=sys.stderr)
                    continue
                counter += 1
                sample_id = f"P12-{counter:03d}"
                rel = full.relative_to(AUTO_ROOT)
                rows.append({
                    "sample_id": sample_id,
                    "source_path": str(rel),
                    "source_sha256_prefix": sha12(full),
                    "original_condition": cond,
                    "original_enterprise": ent,
                    "original_run_id": rid,
                    "producer_model": "DeepSeek-V4-Flash",
                    "judge_model_planned": "DeepSeek-V4-Flash",
                    "condition_visible_to_judge": False,
                    "imported_at": NOW(),
                })
    return rows


def main():
    EXPERIMENTS.mkdir(parents=True, exist_ok=True)
    rows = build_rows()
    with MANIFEST_PATH.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with FROZEN_PATH.open("w", encoding="utf-8") as f:
        json.dump([r["sample_id"] for r in rows], f, ensure_ascii=False, indent=2)
    print(f"wrote {len(rows)} rows -> {MANIFEST_PATH}")
    print(f"wrote {len(rows)} ids -> {FROZEN_PATH}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4 (Verify GREEN): Run tests**

Run: `python -m unittest experiments/test_build_sample_manifest.py -v 2>&1 | tail -25`
Expected: 7 tests, all pass.

- [ ] **Step 5: Run io_spec §7.1 + §7.2 validators by hand**

From `papers/p12-judge-calibration/`:
```bash
jq . experiments/sample_manifest.jsonl >/dev/null && echo "7.1 OK"
N=$(wc -l < experiments/sample_manifest.jsonl)
M=$(jq -c 'select(.source_path and .source_sha256_prefix and .condition_visible_to_judge==false)' experiments/sample_manifest.jsonl | wc -l)
test "$N" = "$M" && echo "7.2 OK (n=$N)"
```
Expected: both lines print `OK`.

- [ ] **Step 6: Append one finding to `state/findings.jsonl` (PIT-006 supplement)**

Append (do NOT replace):
```jsonl
{"ts":"<import time>","source":"m1","level":"info","finding":"P12 M1 sample manifest frozen: 450 samples (3 conditions × 3 enterprises × 50 runs), all condition_visible_to_judge=false, source_sha256_prefix=12hex","details":{"manifest_path":"experiments/sample_manifest.jsonl","frozen_ids_path":"experiments/sample_ids_ordered.json","n":450}}
```

Validate: `jq . state/findings.jsonl >/dev/null` → exit 0.

---

### Task 3: `experiments/validate_manifest.sh` (io_spec §7.1, §7.2 dumpable as reusable CI guard)

**Covers:** io_spec §7.1 + §7.2 machine-checkable per the framework §9 engineering rule #3 "Validation must run between iterations".

**Files:**
- Create: `experiments/validate_manifest.sh`
- Modify: none

- [ ] **Step 1: Write the guard**

```bash
#!/usr/bin/env bash
# P12 M1 manifest guard. Run from .../papers/p12-judge-calibration/.
# Exits 0 iff PIT-005, PIT-105 invariants hold for sample_manifest.jsonl.
set -euo pipefail

cd "$(dirname "$0")/.."
M=experiments/sample_manifest.jsonl
F=experiments/sample_ids_ordered.json

[ -f "$M" ] || { echo "FAIL: $M missing"; exit 1; }
[ -f "$F" ] || { echo "FAIL: $F missing"; exit 1; }

jq . "$M" >/dev/null                                              || { echo "FAIL: $M not valid jsonl"; exit 1; }
jq . "$F" >/dev/null                                              || { echo "FAIL: $F not valid json"; exit 1; }

N=$(wc -l < "$M" | tr -d ' ')
test "$N" = "450"                                                 || { echo "FAIL: n=$N, expected 450"; exit 1; }

PASS=$(jq -c 'select(.source_path and .source_sha256_prefix and .condition_visible_to_judge==false)' "$M" | wc -l | tr -d ' ')
test "$N" = "$PASS"                                               || { echo "FAIL: PIT-105 only $PASS/$N rows blind"; exit 1; }

ORDER=$(jq -r '.sample_id' "$M" | paste -sd , -)
FROZEN=$(jq -r '.[]' "$F" | paste -sd , -)
test "$ORDER" = "$FROZEN"                                         || { echo "FAIL: sample_ids_ordered != manifest order"; exit 1; }

echo "OK: 450 rows, PIT-105 + PIT-106 invariants hold"
```

- [ ] **Step 2: Make executable + dry-run**

Run: `chmod +x experiments/validate_manifest.sh && bash experiments/validate_manifest.sh`
Expected: prints `OK: 450 rows, PIT-105 + PIT-106 invariants hold` and exits 0.

- [ ] **Step 3: Negative test (sanity: temp-modified manifest should fail)**

```bash
cp experiments/sample_manifest.jsonl /tmp/manifest.bak
echo '{"sample_id":"P12-bogus","source_path":"x","condition_visible_to_judge":true}' >> experiments/sample_manifest.jsonl
bash experiments/validate_manifest.sh; rc=$?
mv /tmp/manifest.bak experiments/sample_manifest.jsonl
test "$rc" = "1" || { echo "FAIL: guard should have rejected the bad row"; exit 1; }
echo "guard rejects bad rows ✓"
```

Expected: guard exits non-zero on the bad row, and the final echo prints.

---

### Task 4: Update `state/io_spec.md` and `state/task_spec.md` for the post-restructure P11 path

**Covers:** §11 note from checkpoint: P12 docs reference the OLD `../legacy/p11-closed-v5-minimax-m3/` path, which no longer resolves. This is a doc sweep, not a runtime-blocking fix, but flagged in checkpoint §5.

**Files:**
- Modify: `state/io_spec.md`
- Modify: `state/task_spec.md`
- Modify: `wiki/index.md`

**Constraints:**
- Only update the 5 P11 path references in P12 docs (io_spec, task_spec, wiki/index already shows the wiki/decisions references). Do NOT change semantics, schema, or section structure.
- Do NOT touch the `state/directions_tried.json`, `state/progress.json`, or `state/findings.jsonl`.

- [ ] **Step 1: In `state/io_spec.md`, replace the OLD path with NEW**

Edit:
```
../legacy/p11-closed-v5-minimax-m3/experiments/...
```
to:
```
../legacy/p11-closed-v5-minimax-m3/experiments/...
```
Apply to lines 22 and 23 (P11 raw sample files + P11 prior-judge evidence block).

- [ ] **Step 2: In `state/task_spec.md`, same replacement**

Apply to lines 53-57 (Data Sources block).

- [ ] **Step 3: In `wiki/index.md`, same replacement**

Apply to lines 43-47 (the P11 cross-reference list).

- [ ] **Step 4: Validate the new paths resolve**

Run from `papers/p12-judge-calibration/`:
```bash
test -d ../legacy/p11-closed-v5-minimax-m3/experiments && echo "path resolves ✓"
test -f ../legacy/p11-closed-v5-minimax-m3/wiki/decisions/blind-judge.md && echo "blind-judge decision doc found ✓"
```

- [ ] **Step 5: Re-run guard**

Run: `bash experiments/validate_manifest.sh`
Expected: still `OK`.

---

### Task 5: Final state snapshot (no judge runs)

**Covers:** Framework §9 rule #3 (validation between iterations) + §5 (state always up to date).

- [ ] **Step 1: Append a final M1 work log entry**

Append one JSONL line to `state/findings.jsonl`:
```jsonl
{"ts":"<now>","source":"m1","level":"decision","finding":"P12 M1 closed: pre-registration, manifest (450 rows), and frozen sample ids committed locally. Zero judge calls performed. Awaiting M2 (leaked baseline).","n_samples":450}
```

- [ ] **Step 2: Verify zero M2-M5 artefacts exist**

From `papers/p12-judge-calibration/`:
```bash
test ! -f experiments/leakage_reproduction.json && echo "no M2 artifact ✓"
test ! -f experiments/pairwise_blind_results.json && echo "no M3 artifact ✓"
test ! -f experiments/neighborhood_probe_schema.json && echo "no M4 artifact ✓"
test ! -f experiments/neighborhood_probe_results.json && echo "no M5 artifact ✓"
test ! -f experiments/calibration_metrics.md && echo "no M6 artifact ✓"
```

- [ ] **Step 3: Final guard + summary printout**

Run: `bash experiments/validate_manifest.sh`
Expected: `OK: 450 rows, PIT-105 + PIT-106 invariants hold`.

Print a one-line summary to stderr:
```
P12 M1 closed: 450 samples pre-registered. Next: M2 leaked_baseline.
```

---

## Acceptance for M1

- `state/experiment_design.md` exists; all 9 §-headings present and recognized by `head -1` greps.
- `experiments/build_sample_manifest.py` is idempotent and ≤ 100 lines.
- `experiments/test_build_sample_manifest.py` runs and shows 7/7 pass.
- `experiments/sample_manifest.jsonl` contains exactly 450 rows, every row PIT-105 clean.
- `experiments/sample_ids_ordered.json` lists `P12-001..P12-450` in identical order to the manifest.
- `experiments/validate_manifest.sh` is executable, returns 0 on the canonical artifact, and returns ≠ 0 on a tampered copy.
- No `experiments/*_results.json` exists. No LLM calls made. No judge runs.
- `state/io_spec.md`, `state/task_spec.md`, `wiki/index.md` references the POST-restructure P11 path.
- All `experiments/*.py` files ≤ 300 lines (framework §9 #1).

## Self-Review

- **Spec coverage (§1.1 invariants)**: every invariant is exercised by at least one unit test (PIT-005 rows, PIT-105 blind, PIT-106 order match, sha prefix shape, sample id regex). ✓
- **Placeholders**: zero `TBD`/`fill in details`/`similar to` markers in this plan. Every block contains executable code. ✓
- **Type consistency**: `sample_id` is `P12-NNN` everywhere; `source_path` is always `auto-research`-relative (so the test's `repo_root / row["source_path"]` arithmetic holds for both local and CI); `original_run_id` is the zero-padded string used in filenames (no leading-zero ambiguity). ✓
- **No drift from prior code**: P12 already declares `exp_id=P12` and the 5 protocols; the manifest row schema matches `data-contracts.md` §6 fields referenced in `io_spec.md`. No rename of any schema field. ✓
- **Out-of-scope reminder**: The 2 EXTRA conditions (`output_only`, `explicit_audit`) are explicitly excluded from M1 per the user's chosen option (3 standard conditions). They are noted in design doc §Sample Set and held for M3/M5. ✓
- **Cleanup of Track A**: 6 v5 path repairs were already committed in the parent commit (this session's earlier turn). They are NOT a Task in this plan. ✓
- **Commit policy**: User has not requested a commit. Per CLAUDE.md / global safety, no commits. Working tree will remain dirty. ✓
