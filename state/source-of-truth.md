# Framework Source-of-Truth Registry

> **Created**: 2026-07-03
> **Authority**: FRAMEWORK-RULES.md **R1** (paper-owns-its-inputs) + **R8** (closure-checklist enforcement)
> **Status**: framework-level template. Each active paper MUST also have a paper-level copy at `papers/<N>/state/source-of-truth.md`.
> **Compliance basis**: 0ref QREF-005 (institute-one) Hard rule #6: "Rows are truth; vault notes are projections."

---

## 1. Why this file exists

`auto-research/` is a **multi-paper framework** that reads cross-folder inputs
(e.g. P12 reads from `legacy/p11-closed-v5-minimax-m3/...`). Without a
machine-checkable inventory of these cross-folder dependencies, **M8 closure**
becomes a manual archaeology project — reviewers cannot tell which inputs
must be materialized, which are still live, which have already been retired.

**R1 exception clause** (verbatim from FRAMEWORK-RULES.md):
> A paper may keep an external-source pointer **iff**:
> - the external directory is documented in `state/source-of-truth.md`,
> - the paper records a `last_verified_external_source: <date>` and re-verifies per iteration,
> - closing-time closure checklist has a step that materializes the snapshot.

This file is the **first two requirements** at framework level. The third
(paper-level closure checklist) is a per-paper artifact in `papers/<N>/state/`.

---

## 2. Framework-level external sources

> None registered at framework creation time (2026-07-03). This section
> is the place to add framework-wide shared sources, e.g. vendor
> repositories that multiple papers import.

| Source | Path | Type | First-verified | Last-verified | Re-verify cadence | Retire trigger |
|--------|------|------|----------------|---------------|-------------------|-----------------|
| _example_ | `framework/vendor/policysim_scripts/` | vendored SDK | YYYY-MM-DD | YYYY-MM-DD | per major upstream release | N papers still depend on it AND closure-time copy exists in each |

When the first framework-wide source is added, fill this table.

---

## 3. Paper-level cross-folder dependencies (framework view)

> This section is the **framework's mirror** of each paper's own
> `papers/<N>/state/source-of-truth.md`. The framework view shows
> cross-paper dependencies that affect multiple papers (e.g. P12 reading
> P11 v5 data). For paper-internal dependencies (e.g. P12 reading its
> own vendor copy), see the paper-level file.

| Paper | External source | Direction | Last-verified | Materialize step on M8 close |
|-------|-----------------|-----------|---------------|-------------------------------|
| p12-judge-calibration | `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/` | P11 v5 → P12 (read) | 2026-07-03 | `mkdir -p papers/p12-judge-calibration/experiments/source_data/p11_v5_A && cp -r legacy/.../experiments/h5-emergence/A/yaml/* <dst>/ && re-derive sha256` |
| p1p2-evidence-ledger | (none — standalone at M0) | — | — | — |
| p08-market-calibration | (per-paper source-of-truth.md; refer to it) | — | — | — |
| p07-signal-fusion | (per-paper source-of-truth.md; refer to it) | — | — | — |

---

## 4. Re-verification protocol (R8 enforcement)

For each row in section 3, on every iteration the owning paper MUST:

1. Check that the source path still exists (`test -e <path>` or equivalent).
2. Record `last_verified_external_source: <ISO-date>` in its
   `state/iteration_log.jsonl` entry.
3. If the path is missing or moved: **STOP**, do not retune the prompt —
   cite a pitfall id (per `experiment-pitfalls.md` §0 step 4) and raise
   to the framework owner.

The orchestrator patrol (`framework/watchdog/`) MAY add an automated
check for these paths in its `L1 hourly` sweep, per R11 (patrol
deduped) cadence.

---

## 5. M8 closure checklist (template, per paper)

When a paper reaches M8, the following MUST be executed **before** the
source can be retired / deleted / moved out of reach:

```
[ ] 1. cp -r <external-source> papers/<N>/experiments/source_data/<label>/
[ ] 2. re-derive sha256 of all copied files; store in
       papers/<N>/state/external_source_sha256.txt
[ ] 3. update sample_manifest.jsonl — swap source_path to the new location
[ ] 4. update io_spec.md and experiment_design.md references (R7 cite-restoration)
[ ] 5. re-run validate_manifest.sh — must still be OK
[ ] 6. re-run unit tests — must still be GREEN
[ ] 7. update this framework-level file (section 3 row retired) + the
       paper-level file (mark source as materialized)
[ ] 8. append level=info, source=m8_closure finding to
       papers/<N>/state/findings.jsonl
[ ] 9. only then retire the source directory (git mv to legacy if needed)
```

This checklist is **the same** at framework level and paper level. The
paper-level copy is a copy-paste; the framework-level copy is the
canonical reference.

---

## 6. R-rules cross-reference

- **R1 (paper-owns-its-inputs)**: this file is its primary mechanism.
- **R8 (closure-checklist enforcement)**: section 5 is the closure checklist
  referenced by R8's "MUST list every external source + the materialize-step
  before the legacy entry can be retired".
- **R20 (plan §7 source-project boundary)**: this file is internal to
  auto-research/, not a write into wiki/. R20 does not apply.
- **R24 (4-副产物 self-narrating pattern)**: this file is **not** a
  副产物; it is a state-skeleton file (R4 mandated). The 4-副产物
  pattern is for cross-project catalog work; state-skeleton is for
  per-paper operational continuity.

---

## 7. QREF-005 institute-one parallel (per 0ref-methodology-landscape.md)

institute-one's Hard rule #6: "Rows are truth; vault notes are projections.
Only `vault/writer.py` writes under the vault." This file is the auto-research
analog: **the state directory is truth, the wiki/ + docs/ + topic5-* are
projections**. If a projection contradicts state, **state wins**.

Concretely: if a paper's findings.jsonl says "P12 adopted v4-pro model"
and topic5-research-directions.md says "P12 still on v4-flash", the
state file is canonical — the topic5 doc is stale and must be re-derived
from state (per FRAMEWORK-RULES R7 cite-restoration + this R1 exception).

---

*Created 2026-07-03 as part of the framework-level R1+R8 closure-checklist enforcement. Next review: at first M8 closure of any paper (per the cadence in section 4).*
