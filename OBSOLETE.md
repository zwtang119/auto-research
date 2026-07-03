# OBSOLETE — renamed/moved 2026-07-03

This top-level layout was reorganized into the new schema on 2026-07-03.
The rename is part of the AutoResearch monorepo alignment and is documented
in:

- `docs/portfolio/rename-proposal-2026-07-03.md` (what / why / mapping)
- `docs/portfolio/restructure-blueprint-2026-07-03.md` (where / how / when)

## Where each old directory went

| Old path | New path | Notes |
|---|---|---|
| `p12-judge-calibration/` | `papers/p12-judge-calibration/` | active, renamed |
| `p1-p2-evidence-ledger/` | `papers/p1p2-evidence-ledger/` | active, simplified name |
| `p1.2-market-calibration_minimax-m3/` | `papers/p08-market-calibration/` | active |
| `p2.1-signal-fusion_minimax-m3/` | `papers/p07-signal-fusion/` | active |
| `p1.1-inner-monologue/` | `legacy/p11-legacy-snapshot-2026-07/` | parent of CLOSED v5 |
| `p1.1-inner-monologue-mimo/` | `legacy/p11-closed-v5-mimo/` | closed at 7.0 |
| `p1.1-inner-monologue_minimax-m3/` | `legacy/p11-closed-v5-minimax-m3/` | closed (git repo, history preserved) |
| `p1.2-market-calibration-mimo/` | `legacy/p08-legacy-init-2026-07/` | initialized, inactive |
| `p2.1-signal-fusion-mimo/` | `legacy/p07-legacy-init-2026-07/` | initialized, inactive |

## Why not git mv?

At the time of the rename, `auto-research/` itself was not a git repo (only the
two `p1.1-inner-monologue-*/` subprojects were). Renaming at the root level is
therefore a *new project move*, not a tracked rename — there is no history at
this level to preserve. The closed subprojects that were git repos keep their
own internal `.git/` and their commit log; we did not move files *inside* them.

## Backward compatibility

This file is the canonical redirect stub. Paper citations and external
references to the old paths should be updated. There is no symlink layer.

If a tool still resolves `../p12-judge-calibration/`, it must be updated to
`papers/p12-judge-calibration/`.

## What if you are an agent reading this?

You are looking at a renamed-out path. Walk up one level and read the
`OBSOLETE.md` file. The table above tells you the new location. Do not
silently create files at the old path.
