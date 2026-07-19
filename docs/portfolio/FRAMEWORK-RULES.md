# AutoResearch Framework Rules (2026-07-03)

> **Audience**: every paper (`papers/<N>-<topic>/`) in this monorepo.
> **Status**: binding on Day 0 (M0 of any paper). Reviewable per-iteration.
> **Source**: aligned with `Deli_AutoResearch` §2 behavioral constraints + §9 engineering constraints + the namespace choice in `docs/portfolio/rename-proposal-2026-07-03.md`.

These rules apply when this repo plays the role of *AutoResearch framework*.
Paper-specific exceptions are allowed only via explicit per-paper doc in
`papers/<N>/state/` and must state why a framework rule is relaxed.

---

## R1 — Single Source of Truth (paper-owns-its-inputs)

**Rule.** A paper directory MUST be self-contained for inputs that the paper
*depends on as evidence*. If a paper reads samples from another directory,
that data must be **copied in** before the source can be retired, deleted,
or moved out of reach.

**Why.** The framework §6 stale rules force pivots that change input sets;
per §10.1 framework scores are only comparable inside the same run, but
external reviewers and re-runs must not depend on cross-folder state that
might disappear.

**Application today.**
- `papers/p12-judge-calibration/` currently imports samples from
  `legacy/p11-closed-v5-minimax-m3/experiments/h5-emergence/A/yaml/`.
- `experiments/sample_manifest.jsonl` records `source_path` pointing there.
- **When P12 closes**, the 750 P11 v5 A-yaml must be *copied* into
  `papers/p12-judge-calibration/experiments/source_data/p11_v5_A/`
  (or a parallel p11-sample-set/ subdir) before any legacy entry is removed.

**Exception.** A paper may keep an external-source pointer **iff**:
- the external directory is documented in `state/source-of-truth.md`,
- the paper records a `last_verified_external_source: <date>` and re-verifies
  per iteration,
- closing-time closure checklist has a step that materializes the snapshot.

**Enforcement**: every paper's `state/checklist.yaml` (or
`state/closure_checklist.md`) must list each external source and the
materialization step before closure.

---

## R2 — Path discipline

**Rule.** Paths inside this repo use **single-hyphen** separators within a
component. No `.` and no `_` interleaved inside names. Lowercase per Linux
FHS. Models live in `wiki/`, not in paths.

**Why.** Compliance with [ISO/IEC 11179](https://en.wikipedia.org/wiki/ISO/IEC_11179)
single-concept → single-representation, plus reproducibility.

**Exceptions**: domain terms (`experiments/h5-emergence/`, `wiki/concepts/`),
vendor file names, and historical snapshot paths under `legacy/p<NN>-<status>-`
(which intentionally retain the agent marker for cite-restoration).

---

## R3 — Lifecycle suffix on legacy

**Rule.** All non-active paper-status paths live under `legacy/` with one
of these suffixes:

| Status | Suffix | Examples |
|---|---|---|
| Active | (none) | `papers/p07-signal-fusion/` |
| Initialized but inactive | `legacy-init-YYYY-MM` | `legacy/p07-legacy-init-2026-07/` |
| Closed, versioned | `closed-v<N>-{agent}` | `legacy/p11-closed-v5-mimo/` |
| Non-versioned mix-bag | `legacy-snapshot-YYYY-MM` | `legacy/p11-legacy-snapshot-2026-07/` |

**Why.** Reader can identify paper status *from the path alone*, no
`OBSOLETE.md` lookup needed.

---

## R4 — State-file skeleton (per paper)

**Rule.** Each `papers/<N>-<topic>/` MUST have, before M1 starts:

```
state/
├── task_spec.md           # goal / milestones / success criteria
├── progress.json          # {iteration, total_findings, status, stale_count,
│                          #  current_milestone, completed_milestones, …}
├── findings.jsonl         # append-only
├── directions_tried.json  # direction history
└── iteration_log.jsonl    # per-iteration summary
```

Plus when pre-registration exists:
```
state/experiment_design.md   # frozen at end of M1 (PIT-006)
```

**Why.** [Deli_AutoResearch §4](file:///Users/tangzw119/.claude/skills/Deli_AutoResearch/SKILL.md)
binding: state is the substrate; missing files ⇒ lost progress on context
compaction.

---

## R5 — Engineering constraints (per iteration)

**Rule.** Per iteration:
- ≤ 5 large files written
- no single file over 300 lines
- validation (test / compile / check) must run *between* iterations
- citation-like content verified every 20 entries, never batched
- with multiple candidate directions, prefer diversity over digging one deeper

**Why.** [Deli_AutoResearch §9](file:///Users/tangzw119/.claude/skills/Deli_AutoResearch/SKILL.md)
binding; validated across 4 prior paper tracks scoring 8.0–8.6/10.

---

## R6 — Behavioral constraints

**Rule.** When running a paper's iterations:
1. **Zero interaction**: don't prompt the user mid-iteration; ask at most one
   structured question per *milestone*, not per iteration.
2. **Ready means execute**: finishing preparation is not a checkpoint that
   needs approval; M1 close is "design + manifest + frozen IDs + tests green"
   and that is the execution. Don't ask "shall we proceed?".
3. **Persist state to files**: every iteration's outcome writes one line to
   `state/iteration_log.jsonl` and any *finding* to `state/findings.jsonl`.
4. **Callback = report-alive**: first action on a callback is to update
   progress.json, then check liveness.
5. **Guardian / worker separation**: a heartbeat patrol touches other
   tasks only via `liveness-check | restart | nudge`.

**Why.** [Deli_AutoResearch §2](file:///Users/tangzw119/.claude/skills/Deli_AutoResearch/SKILL.md)
behavioral constraints. Prevents cognitive loops, stalling, runtime
fragility — the three framework failure modes.

---

## R7 — Cite-restoration

**Rule.** When a path is renamed (R3 lifecycle suffix application), the old
path keeps an `OBSOLETE.md` stub at the same level that points to the new
location with a mapping table. The new path *must* be operational before
the old OBSOLETE.md is added (i.e. don't add redirect before the new layout
loads).

**Why.** [Force11 citation principles](https://force11.org/info/the-force11-data-citation-principles/) +
backward-compat for paper cites already in the wild.

**Application today.** `OBSOLETE.md` at repo root lists 9 old-paths → new-paths.
Legacy/ subdirs intentionally retain old-path strings inside their own
historical files (cite-restoration + git history preservation).

---

## Cross-references

- `docs/portfolio/rename-proposal-2026-07-03.md` — original namespace rationale
- `docs/portfolio/restructure-blueprint-2026-07-03.md` — Day-0 scaffold plan
- `docs/portfolio/naming-audit-2026-07-03.md` — human-risk audit
- `docs/portfolio/aliases.md` — paper-code ↔ directory mapping
- `~/.claude/skills/Deli_AutoResearch/SKILL.md` — framework source of truth


---

## Framework-level R-rule bridge (2026-07-03)

> **Source**: 24 R-rules in `~/.local/share/mimocode/memory/projects/global/MEMORY.md` (R1-R24).
> **Status**: R1-R7 are duplicated here as binding framework rules; R8-R20 are binding via global MEMORY but listed here for cross-reference. R21-R24 are working-style rules, not framework-binding.

### Cross-reference (R1-R7 here ↔ R8-R20 in global MEMORY)

| Local (here) | Global (MEMORY) | Topic |
|--------------|-----------------|-------|
| R1 | R1 (dup) | Single Source of Truth |
| R2 | R2 (dup) | Path discipline |
| R3 | R3 (dup) | Lifecycle suffix on legacy |
| R4 | R4 (dup) | State-file skeleton |
| R5 | R5 (dup) | Engineering constraints |
| R6 | R6 (dup) | Behavioral constraints |
| R7 | R7 (dup) | Cite-restoration |
| _implicit_ | **R8** | Closure-checklist enforcement (now implemented via `state/source-of-truth.md`) |
| _implicit_ | **R9** | Atomic state writes |
| _implicit_ | **R10** | Vendored function signatures are law |
| _implicit_ | **R11** | Patrol emits deduped |
| _implicit_ | **R12** | Bash `set -euo pipefail` + subshell defensive init |
| _implicit_ | **R13** | Plan self-imposed caps overridable by user |
| _implicit_ | **R14** | ls session memory dir before write |
| _implicit_ | **R15** | Verify-once-then-act |
| _implicit_ | **R16** | PIT body ≤ 80 lines (Python markers) |
| _implicit_ | **R17** | Long-file read truncation check |
| _implicit_ | **R18** | Status numeric claims require `verify:` segment |
| _implicit_ | **R19** | 🔴 needs 🩸/🟠 disambiguation |
| _implicit_ | **R20** | Plan §7 source-project boundary (R20 does NOT bind here — auto-research is the source project) |
| _not-applicable_ | R21-R24 | Working-style rules, not framework-binding |

### QREF / PIT 借鉴入口 (per wiki/0ref-methodology-landscape.md)

This file is the **paper-facing** rule book. The 6 QREF and 12 framework-level PIT are
indexed in `framework/knowledge/auto-research-history.md` §1-2 (NEW today). Per-paper
implementations should cite the QREF / PIT id when applying a borrowed pattern.

**Practical rule**: when reading this file, if a paper agent needs QREF/PIT context,
it MUST cross-reference `framework/knowledge/auto-research-history.md` §1 (QREF)
and §2 (PIT). The two-file structure follows the R24 4-副产物 self-narrating
pattern (data + meta + nav + audit-trail).

### State-skeleton anchor (per R4)

```
state/
├── task_spec.md           # goal / milestones / success criteria
├── progress.json          # iteration counter + findings count + stale_count
├── findings.jsonl         # append-only; pitfall_id field per data-contracts §3
├── directions_tried.json  # direction history
├── iteration_log.jsonl    # per-iteration summary
├── source-of-truth.md     # R1+R8 closure-checklist (NEW 2026-07-03)
└── experiment_design.md   # frozen at end of M1 (PIT-006) — only when pre-registration exists
```

The 5+1 = 6 files are the canonical state per R4 + R8. Any paper missing
`source-of-truth.md` is in R1 violation (audit log: today fixed at framework
level; per-paper copies still need paper-level writes).

---

*FRAMEWORK-RULES.md (R1-R7, 160 lines original) retained as binding rules above. This
bridge section (NEW 2026-07-03) cross-references R8-R20 in global MEMORY + QREF/PIT
index in `framework/knowledge/auto-research-history.md` §1-2. Per R24 4-副产物
pattern, this file is the 'data' (binding rules), auto-research-history.md is
the 'meta-data' (QREF/PIT context), state/source-of-truth.md is the 'audit-trail'.*
