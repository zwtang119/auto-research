# Framework Top-Level Build Plan (2026-07-03)

> Decide: build `framework/` all at once vs incrementally.

## Recommendation

**Minimal scaffold now; expand lazily.** Concrete proposal:

```
framework/                                     # NEW top-level
├── README.md                                  # explain it
├── schemas/                                   # docs/portfolio/{data-contracts,
│   ├── experiment-pitfalls.md                 #   experiment-pitfalls}.md moved
│   └── data-contracts.md                      #   in (already canonical)
└── knowledge/                                 # cross-paper knowledge
    └── auto-research-history.md               # framework evolution log

(DEFERRED until first need:)
├── skills/                                    # wait for a second skill beyond
│                                              # Deli_AutoResearch (currently only 1)
├── prompts/                                   # wait until ≥2 papers share a prompt
├── scripts/                                   # wait until build_sample_manifest.py
│                                              # or similar is used in 2+ papers
└── runbooks/                                  # wait for a writeable SOP
```

## Why minimal-not-full

Evidence (measured just now):
- `papers/*/state/*.md`, `papers/*/CLAUDE.md` referencing cross-paper
  assets: **14 files** reference `data-contracts.md` / `experiment-pitfalls.md`.
- Files invoking Deli skill directly: **2 files** (P7 CLAUDE.md, P8 CLAUDE.md).
- Currently reusable cross-paper code: **0 files**. (Only `build_sample_manifest.py`
  in P12 is script-shaped, and it's P11-path-resolving, paper-specific.)

So the *real* cross-paper need today is **schemas + knowledge + framework-rules**.
That maps to exactly the 2 dirs I'm proposing to create now.

## Why not defer everything

`docs/portfolio/FRAMEWORK-RULES.md` exists but lives in `docs/portfolio/`
which mixes framework rules with portfolio snapshots. Pulling the rules
up into `framework/` makes the namespace honest. The other schemas
move because they're already used by 14 files.

## Promotion rule (locked-in)

From `docs/portfolio/restructure-blueprint-2026-07-03.md` §3:

1. **Default** — paper-specific stuff stays under `papers/<N>/framework/`.
2. **Promote** — only when used by ≥2 papers.
3. **Irreversible** — once promoted, no un-promotion.

This rule has *never been triggered* yet (zero reusable items in 0 papers).
That's signal: do not pre-build empty bins.

## Concrete minimal-scaffold steps (Day 0 evening / Day 1 morning)

| # | Action | File | Outcome |
|---|---|---|---|
| 1 | `mkdir -p framework/{schemas,knowledge}` and `framework/README.md` | framework/README.md | 3 entries |
| 2 | Move `framework/schemas/data-contracts.md` → `framework/schemas/data-contracts.md` | (same content) | one find-rename |
| 3 | Move `framework/schemas/experiment-pitfalls.md` → `framework/schemas/experiment-pitfalls.md` | (same content) | one find-rename |
| 4 | Update 14 file references: `framework/schemas/data-contracts.md` → `framework/schemas/data-contracts.md` and `../../framework/schemas/experiment-pitfalls.md` → `framework/schemas/experiment-pitfalls.md` | sed-batch across active papers + docs | 14 sed replacements |
| 5 | Update `docs/portfolio/FRAMEWORK-RULES.md` internal cross-refs to point to `framework/...` (the R1 doc reflects the eventual home) | FRAMEWORK-RULES.md | a few link updates |
| 6 | Write `framework/knowledge/auto-research-history.md` as the *change-log* of the framework itself | framework/knowledge/auto-research-history.md | 1 file |
| 7 | Update `OBSOLETE.md` if needed (it should NOT mention the move from `docs/portfolio/` → `framework/`, because both live in this repo; just note in CHANGELOG.md) | root CHANGELOG.md or just the audit trail | 1 sentence |

After this, framework/ has **5 files** (1 README + 2 schemas + 1 history + the
implicit empty dirs `skills/`, `prompts/`, `scripts/`, `runbooks/` if I want
to pre-stage them as placeholder `.gitkeep`-only — *or* I don't stage them
at all and let them appear naturally).

## Decision my recommendation

**Build steps 1, 4, 6 right now.** That's it.
- 1 README
- 2 docs-moves (with auto-rewrite of references)
- 1 history log
- `framework/{skills,prompts,scripts,runbooks}/` not created yet — they
  appear when first needed.

**Total**: 4 new directories (`framework/`, `framework/schemas/`,
`framework/knowledge/`, plus their `.gitkeep`s if you want them), 4 new
files, ~14 sed references rewritten. Estimated 20 minutes wall time.

**Then** P12 M2 can run as normal. framework/ stays minimal until M2's
results tell us what to promote.

## When to *expand* framework/

After M2 results land, observe:
- Did M2 generate any helper script that other protocols/papers could reuse?
  → if yes, promote to `framework/scripts/`.
- Did M2 discover a prompt template (judge prompt, pre-registration
  reminder) that P7/P8/P11 will need?
  → if yes, promote to `framework/prompts/`.
- Did M2 surface a *new* watch (e.g. specific stall pattern) that requires
  a watchdog beyond what Deli_AutoResearch provides?
  → if yes, write `framework/skills/autoresearch-extension/SKILL.md`.

Each promotion is one committed event with evidence. By M3/M4 we'll know
concretely whether the bigger scaffold earns its keep.
