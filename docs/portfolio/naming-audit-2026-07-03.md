# Naming Audit Report — 2026-07-03

> **Auditor**: AutoResearch coordinator
> **Scope**: every directory name, file name, and identifier in the rename batch
> **Method**: each new name checked against (a) human-intuition risk, (b) academic ambiguity, (c) framework-convention match

## 1. Risk-class taxonomy

| Class | Description | Resolution |
|---|---|---|
| **R1 Agent-backend bleed** | `-minimax-m3` / `-mimo` agent name visible in citable path. Reader confuses agent with model. | Eliminated: only `legacy/p11-closed-v5-{minimax-m3,mimo}` keeps the historical marker (cite-restoration). All active paths are clean. |
| **R2 Paper-code vs route-code split** | `P11` ≠ `p1.1`. Causes `aliases.md` indirection. | Reduced: removed for active paths (`p07-`, `p08-`, `p12-`, `p1p2-`). Notes still mention route-code in `legacy/p11-closed-v5-*` as historical anchor. |
| **R3 Punctuation mix** | `.`, `-`, `_` collide in same concept (`p1.1-inner-monologue` vs `_minimax-m3`). | Eliminated for active paths (single hyphen). |
| **R4 Lifecycle invisible** | Active vs closed vs initialized not encoded. | Encoded as `closed-v5-` / `legacy-init-` / `legacy-snapshot-` suffix. |
| **R5 Agent-only-scheduler coupling** | `_minimax-m3` suffix assumes the current scheduler remains. | Off the active path; only in legacy dir names. |
| **R6 Public-path leaks internal infra** | `polysim-research-Tsinghua` outside repo. | Out of scope of this rename; flagged in `restructure-blueprint-2026-07-03.md` §7. |
| **R7 Active project hidden in legacy bag** | `p1.1-inner-monologue` (parent, no git) collides with active ACTIVE-impression. | Now `legacy/p11-legacy-snapshot-2026-07/` — clearly past. |

## 2. Per-name audit results

| New name | Risks identified | Resolved |
|---|---|---|
| `papers/p07-signal-fusion/` | P7 **was** `p2.1-signal-fusion_minimax-m3` — old readers won't find by `p2.1` | Mitigated by OBSOLETE.md redirect + aliases.md §1 alias table |
| `papers/p08-market-calibration/` | Same as above — old `p1.2-market-calibration_*` → P8 | Same |
| `papers/p12-judge-calibration/` | Was top-level `p12-judge-calibration/`. Now nested under `papers/`. Inner scripts updated. tests + guard PASS | OK |
| `papers/p1p2-evidence-ledger/` | Was `p1-p2-evidence-ledger/`. Hyphen removed; readers may find confusing | Mitigated by `OBSOLETE.md` + `aliases.md` aliases table; rationale documented in `rename-proposal-2026-07-03.md` §7 schema rule |
| `legacy/p11-closed-v5-minimax-m3/` | New name keeps `minimax-m3` agent marker — flagged in R1 | Acceptable: closed snapshots carry agent = writer signature for historical fidelity (R5 not eliminated, just demoted) |
| `legacy/p11-closed-v5-mimo/` | Same: `mimo` for the older Mimo-build snapshot | Same |
| `legacy/p11-legacy-snapshot-2026-07/` | Was the no-git parent of P11 — a mixed bag | "snapshot" status honest |
| `legacy/p08-legacy-init-2026-07/` | Was `p1.2-market-calibration-mimo` | Initialised-only, never ran. Status: legacy |
| `legacy/p07-legacy-init-2026-07/` | Was `p2.1-signal-fusion-mimo` | Same |

## 3. Open risk: in-repo cite breakage

**Status**: external paper citations (Force11 / DCAT) reference the old paths.
**Forward path**: paper authors should update bib entries; OBSOLETE.md at top
level is the canonical redirect for readers.

## 4. Verification artifacts

- P12 manifest guard (runtime): `papers/p12-judge-calibration/experiments/validate_manifest.sh` → **PASS**.
- P12 unit tests: `python -m unittest` → **9/9 PASS**.
- Full-text grep against old tokens: `p1.1-inner-monologue_minimax-m3` etc. — **0 hits in active scope** (legacy/ + 2 proposal docs + OBSOLETE.md are the only intentional holders).

## 5. Out-of-scope for this audit (flagged)

- `~/Documents/GitHub/policysim-research-Tsinghua` is outside the repo (R6).
- Internal `experiments/h5-emergence/`, `wiki/concepts/`, `state/`, `paper/` (kept as canonical P11 v5 names).
- `mimo-prompt.md` filename (deliberate: it's the prompt for the Mimo-style agent,
  even though we use minimax-m3 to dispatch it now).
- `victorchen96.github.io/` (cloned reference, not our repo).

## 6. Recommendation

Adopt the new layout. The remaining risks are either intentional (legacy/ historic markers),
acceptable (paper-cite retirement window), or out of scope (external dep on Tsinghua).
