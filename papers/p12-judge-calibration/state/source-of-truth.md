# P12 Source-of-Truth Plan

> Created: 2026-07-03 (mandated by `docs/portfolio/FRAMEWORK-RULES.md` rule R1).
> Status: **active**, to be revised at M2 close.

## Current state

P12 currently imports its sample pool (450 P11 v5 A-yaml) from a
**cross-folder, non-self-owned source**:

```
legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/
                                            (750 yaml)
                                                │
                                                └─►  P12 reads 450 of them
                                                    (3 standard conditions ×
                                                     3 enterprises × 50 runs)
```

`experiments/sample_manifest.jsonl` records the source_path of every row;
that path is the current authority-of-location.

## Why this is fragile

The legacy directory is **historical** and may be retired, re-purposed, or
re-organized at a future milestone (a sibling paper might claim those yaml,
P11 might be revived, etc.). P12's reproducibility claim must not depend on
that other directory staying in place or staying current.

## Materialization plan (closure step)

When P12 closes (M8 end), the closure checklist MUST include this step:
**before any other closure action**:

```
1. mkdir -p papers/p12-judge-calibration/experiments/source_data/p11_v5_A/
2. cp legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/*.yaml \
     papers/p12-judge-calibration/experiments/source_data/p11_v5_A/
3. Re-derive sha256 prefix per file and update sample_manifest.jsonl:
     "source_path" → "experiments/source_data/p11_v5_A/<file>.yaml"
4. Re-run validate_manifest.sh (must still be OK)
5. Re-run python -m unittest experiments.test_build_sample_manifest
     (must still be 9/9 GREEN — both tests expect source paths to resolve)
6. Append a finding to state/findings.jsonl:
     level=info, source=p12_closure,
     finding="M8 closure: P11 v5 source materialized into self-owned dir"
7. Then, and only then, may the legacy directory move elsewhere.
```

## External deps NOT yet in scope (related but separate)

- `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/metadata.json`
  (the producer model + judges field) — same materialization rule applies,
  capture at closure.
- `wiki/decisions/blind-judge.md` from the same legacy dir — P12 cites it
  in `state/io_spec.md`. Snapshot that file into
  `papers/p12-judge-calibration/wiki/decisions/source_blind-judge.md`
  at closure.

## Required updates at closure

`state/io_spec.md` line 22 — currently `legacy/p11-closed-v5-minimax-m3/...`
must read `experiments/source_data/p11_v5_A/` after this step runs.
`state/experiment_design.md` lines 44 and 145 — same swap.

`build_sample_manifest.py` — replace `AUTO_ROOT` path resolution with the
self-owned `experiments/source_data/p11_v5_A/` directory. The unit tests
already encode `test_every_source_path_resolves_to_a_real_file`, so the
swap must preserve path resolvability.

## Why not do it now

Materializing **all** 750 yaml now would triple the repo size for a benefit
that gates on closure. The current pointer is honest (with `source_path`/
`sha256_prefix` PIT-005 record), and the legacy/ dir is short-term-stable.
Plan: do it at closure, when the paper's scope is final.

A pre-M2 dry-run is welcome if P12's M2 budget allows (≈ 30s of disk + 5
test refactor lines) but is **not required** by this rule.
