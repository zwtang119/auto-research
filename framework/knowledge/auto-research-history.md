# AutoResearch Framework History

> **Scope**: framework-level evolution. Per-paper histories live in each
> `papers/<N>-<topic>/state/iteration_log.jsonl`.

## 2026-07-03 — Monorepo bootstrap

**Event**: auto-research/ promoted from a multi-paper workspace to a
**framework monorepo**.

**Why**:
- Victor Chen reference site (`victorchen96.github.io`) mirrors the
  Deli_AutoResearch long-horizon protocol.
- User wanted the framework to outlive any single paper.
- 14 active files referenced cross-paper content (data-contracts,
  pitfalls) — proof of cross-paper need.
- 0 active scripts reusable across papers — proof that premature full
  scaffold would be empty bins.

**Decisions bound this session**:

| Decision | Rationale | Source |
|---|---|---|
| Single monorepo | Minimal disruption to P12 progress; framework shares one `git log` over time | user Q1 |
| Active papers under `papers/`, closed under `legacy/` | Lifecycle visible from path; R3 | rename-proposal §3 |
| Framework-level dirs only when ≥2 papers need them | YAGNI; the promotion rule locked in §3 of restructure-blueprint | user Q2 |
| R1 Single-Source-of-Truth | Closure-time copy-in: a paper must own its inputs before closing; deprecated sources can be retired | FRAMEWORK-RULES R1 + per-paper `state/source-of-truth.md` |
| Use Deli_AutoResearch convention | State-file skeleton already matched; constraint #2 zero-interaction already in `R6`; §9 engineering constraints validated by 9 unit tests + manifest guard | user Q4 |
| Heartbeat watchdog: deferred | User explicitly opted against heartbeat for Day 1; re-evaluate at first stall | user (c) |
| website hub (GitHub Pages): future | Not in scope this turn; user has not built `<owner>.github.io` yet | user §1 |

**Execution milestones**:

- 9 directory renames (active ↔ legacy split)
- 31 active-scope files `sed`-patched for old-paths → new-paths
- 3 runtime scripts in P12 had path-arithmetic fixed
- 9 / 9 P12 unit tests GREEN post-rename
- `OBSOLETE.md` at repo root for cite-restoration
- `docs/portfolio/FRAMEWORK-RULES.md` written (7 rules)
- `papers/README.md` written (active + closed tables)
- `papers/p12-judge-calibration/state/source-of-truth.md` written (closure checklist)
- `framework/{README, schemas/{data-contracts, experiment-pitfalls}, knowledge/auto-research-history}/` created (minimal scaffold)
- 14 schema path references rewritten (depth-aware across papers/, docs/, framework/)
- 0 broken refs after rewrite (verified by `readlink -f`)

## Open questions / next actions

- [ ] User build `<owner>.github.io` and link `website/` content to it (Day-1+)
- [ ] Decide whether to apply `claude-prompt.md` SKILL reference per paper (Day-2+ if any paper agent drifts)
- [ ] At first P12 stall (3+ consecutive iterations with 0 new findings), enable heartbeat L2
- [ ] At M8 closure, execute the 7-step source-of-truth plan in
      `papers/p12-judge-calibration/state/source-of-truth.md`

## Risk register (today)

| Risk | Status |
|---|---|
| P12 reads P11 from `legacy/` — fragile cross-folder dep | Mitigated by R1 + `source-of-truth.md` plan |
| 9 dirs moved; paper cites pre-rename | Mitigated by `OBSOLETE.md` (root) for 9 old paths |
| Framework scaffold may be too thin | Mitigated by promotion rule; first cross-paper need will trigger expansion |
| Heartbeat not enabled | Accepted by user; trade-off faster Day-1 M2 vs no auto-restart |
