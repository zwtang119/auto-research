# Framework

> **AutoResearch framework layer** — cross-paper reusable rules, schemas,
> and knowledge. **Paper-specific content** lives at
> `papers/<N>-<topic>/framework/` instead (see
> [`docs/portfolio/framework-top-level-build-plan-2026-07-03.md`](../docs/portfolio/framework-top-level-build-plan-2026-07-03.md) §"Promotion rule").

## Layout

| Subdir | What | When to use |
|---|---|---|
| `schemas/` | Cross-paper data shapes and pitfalls | Already used by ≥1 paper (P7/P8/P12/P1+P2). Currently: [`data-contracts.md`](schemas/data-contracts.md) and [`experiment-pitfalls.md`](schemas/experiment-pitfalls.md). |
| `knowledge/` | Framework-level knowledge (evolution log, conventions) | One file: [`auto-research-history.md`](knowledge/auto-research-history.md). |
| `skills/` | (not yet created) | Wait until a second skill beyond `Deli_AutoResearch` emerges. |
| `prompts/` | (not yet created) | Wait until ≥2 papers share a prompt template. |
| `scripts/` | (not yet created) | Wait until a cross-paper script exists (currently 0). |
| `runbooks/` | (not yet created) | Wait until a writeable SOP emerges from repeated ops. |

## Rule of promotion

From `docs/portfolio/restructure-blueprint-2026-07-03.md` §3 (locked):

1. **Default**: paper-specific content lives at
   `papers/<N>-<topic>/framework/<x>/`.
2. **Promote**: when a piece becomes used by ≥2 papers, move it here.
3. **Irreversible**: once promoted, no un-promotion. (Avoids drift between
   paper-local copy and framework-level canonical.)

## Cross-references

- [`docs/portfolio/FRAMEWORK-RULES.md`](../docs/portfolio/FRAMEWORK-RULES.md) — 7 framework rules including Single-Source-of-Truth (R1) and Zero-Interaction (R6).
- [`docs/portfolio/aliases.md`](../docs/portfolio/aliases.md) — paper-code ↔ directory mapping.
- [`docs/portfolio/rename-proposal-2026-07-03.md`](../docs/portfolio/rename-proposal-2026-07-03.md) — namespace rationale.
- [`docs/portfolio/naming-audit-2026-07-03.md`](../docs/portfolio/naming-audit-2026-07-03.md) — human-misunderstanding audit (7 risk classes).
- `~/.claude/skills/Deli_AutoResearch/SKILL.md` — long-horizon protocol SKILL
  that the framework aligns with (see R6 in FRAMEWORK-RULES.md).
