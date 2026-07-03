# P-directory Rename Proposal (Draft 2026-07-03)

> **Status**: EXECUTED 2026-07-03. See `OBSOLETE.md` (root) for old→new redirect.
> Authoritative mapping table is now in §6 below; the audit report is at `docs/portfolio/naming-audit-2026-07-03.md`.
> **Author**: AutoResearch coordinator, based on `docs/portfolio/aliases.md`.
> **Decision owner**: User (you). The actual `git mv` calls require your sign-off.

## 1. Why rename

Current directory namespace leaks *three* orthogonal metadata dimensions into a
single path token: paper-line code (P1.1/P1.2/P2.1/P12), agent backend (`-mimo`
vs `_minimax-m3`), and route node (1.1 vs 1.2). Aliases (`docs/portfolio/aliases.md`)
exist only because the namespace itself is ambiguous.

Per `MEMORY.md` §Architecture decisions (2026-07-03): user has confirmed that
going forward the only scheduling agent is `minimax-m3`; therefore the per-agent
suffix (`-mimo` vs `_minimax-m3`) is infrastructure detail that should NOT
appear in paper-citable paths. Models actually invoked (DeepSeek-V4-Flash,
Kimi-K2.5, Qwen) live inside `wiki/` metadata, not in paths.

## 2. Academic-normative rationale

| Issue in current layout | Norm violated | Reference |
|---|---|---|
| One paper line → 3 different filenames (`p1.1-inner-monologue` / `-mimo` / `_minimax-m3`) differing in punctuation | Single concept → single representation | ISO/IEC 11179 |
| Paper code (P11) ≠ directory version (1.1) → need `aliases.md` | Identifier locality in metadata registry | W3C DCAT, VCAP |
| Agent backend suffix visible in path | Separation of *platform* / *sample* metadata | MIAME (genomics), BIOSHARE |
| Lifecycle invisible from path | Versioning + archival conventions | RFC 3339, W3C DCAT |
| `~/Documents/GitHub/policysim-research-Tsinghua` outside repo | Reproducibility locator ungrouped | FAIR Principles R1.1 |

## 3. Proposed mapping

| Current | Proposed | Rationale |
|---|---|---|
| `p1.1-inner-monologue/` | `p11-inner-monologue/legacy-snapshot-2026-07/` | Parent is a non-git M1 snapshot bundle with mixed content. Mark as legacy, dated. |
| `p1.1-inner-monologue-mimo/` | `p11-inner-monologue/closed-v5-mimo/` | CLOSED 7.0/10; bring under P11 namespace, status + version suffix. |
| `p1.1-inner-monologue_minimax-m3/` | `p11-inner-monologue/closed-v5-minimax-m3/` | CLOSED; same treatment as mimo. |
| `p1.2-market-calibration_minimax-m3/` | `p08-market-calibration/` | Active entry point for P8. Paper code (P8) becomes path. |
| `p1.2-market-calibration-mimo/` | `p08-market-calibration/legacy-init-2026-07/` | Initialized but inactive; legacy-suffix. |
| `p2.1-signal-fusion_minimax-m3/` | `p07-signal-fusion/` | P7 active entry point. |
| `p2.1-signal-fusion-mimo/` | `p07-signal-fusion/legacy-init-2026-07/` | Inactive. |
| `p1-p2-evidence-ledger/` | `p1p2-evidence-ledger/` | Hyphen → no separator between adjacent digits (matches `P1P2` reading). |
| `p12-judge-calibration/` | (no rename) | Already compliant. |

`policysim-research-Tsinghua` outside repo: out of scope for this draft; listed as §7 follow-up.

## 4. Naming schema

```
p<N>{-subtopic}/                       for ACTIVE projects
p<N>{-subtopic}/legacy-init-YYYY-MM/   for initialized but inactive
p<N>{-subtopic}/closed-v<N>-{agent}/   for closed project snapshots
p<N>{-subtopic}/legacy-snapshot-YYYY-MM/  for non-versioned mix-bags
```

- `N` is the paper-code integer (1, 2, 7, 8, 11, 12), no dot.
- For combined codes (`P1+P2`) write `p1p2-`.
- Separator: single hyphen `-` throughout; no underscores, no dots inside names.
- `agent` only appears in `closed-vN-` paths because it's a *historical* marker
  (which agent wrote the closure). For LIVE paths, agent is implementation
  detail and lives in `state/writer.json`.
- All lowercase per Linux/Unix [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/fhs.shtml) (§"Case sensitivity").

## 5. Backward compatibility (paper citations)

Per [Force11 Software Citation Principles](https://force11.org/info/the-force11-data-citation-principles/),
old cited paths must continue to resolve. Strategy:

1. **At execution time**: do not `git rm`; use `git mv`. Git retains history.
2. **In-tree redirects**: at every old path write an `OBSOLETE.md`:
   ```markdown
   # OBSOLETE — moved 2026-07-03

   This directory was merged into `p11-inner-monologue/closed-v5-minimax-m3/`.

   See https://github.com/<owner>/auto-research for the new path.
   A redirect stub is kept to preserve paper citations.
   ```
3. **In each affected project README.md**, prepend a pointer to the new path.
4. **`docs/portfolio/aliases.md`** becomes the *single* index; update §1's table to the new paths and add an "alias history" appendix listing old → new.

> **Note (2026-07-03)**: `auto-research/` itself is NOT a git repo (`git rev-parse` fails at the root), but each subproject IS a git repo. `git mv` therefore must run *inside each subproject's repo*, not at the auto-research root. This confines history preservation to per-subproject repositories and means the root-level moves (`p1.1-inner-monologue/` itself and any sibling `*_minimax-m3/` dirs) are **new project moves**, not renames — those still need an `OBSOLETE.md` redirect stub at the parent level even though no git history exists.

## 6. Pre-execution checklist

- [ ] Confirm `minimax-m3` is the only active scheduler (`user 2026-07-03` ✓).
- [ ] List every script that hardcodes the old paths:
      `grep -rn "p1\.1-inner-monologue\|p1\.2-market-calibration\|p2\.1-signal-fusion\|p1-p2-evidence-ledger" --include="*.py" --include="*.sh" --include="*.md" --include="*.json" --include="*.yaml"`
- [ ] For each project, run `git mv` from inside that project's repo (so its
      own commits preserve the move).
- [ ] Write `OBSOLETE.md` at every old path.
- [ ] Update `docs/portfolio/aliases.md`, `docs/portfolio/project-index.md`,
      and root `README.md`.
- [ ] Re-run M1's `experiments/validate_manifest.sh` (path-sensitive).
- [ ] Re-run all unit tests per project.
- [ ] Update `MEMORY.md` (per CLAUDE.md promoted-knowledge rule).

## 7. Out of scope for this draft

- `~/Documents/GitHub/policysim-research-Tsinghua` → separate "make
  all deps in repo" proposal (touching git submodules / vendoring).
- Renaming internal `wiki/`, `state/`, `experiments/`, `paper/`, `scripts/`,
  `logs/`, `harness/` directories — already compliant (lowercase, single
  word).
- Renaming `experiments/h5-emergence/` and similar nested paths — those
  are domain terms (P11 v5 §A), leave alone.

## 8. Why this conforms to academic norms (self-check)

| Norm | Compliance |
|---|---|
| ISO/IEC 11179 (single concept → single repr) | ✅ P11 = single namespace `p11-*` |
| FAIR R1.1 (clear data locator) | ⚠️ partial; `policysim-*-Tsinghua` external dep still breaks strict compliance — proposed next |
| Force11 citation (version + commit) | ✅ `closed-v5-{agent}` carries version + writer |
| W3C DCAT (named versioned dataset) | ✅ active vs legacy branch in path |
| MIAME (platform/sample separation) | ✅ agent vs model separated: agent in `closed-v5-` suffix, model in `wiki/` |
| IETF RFC 2119 (MUST/SHOULD) | ✅ MIGRATION uses MUST-strength redirects |

## 9. Open questions for user

1. ☐ Is `p1p2-evidence-ledger` rename OK, or keep `p1-p2-evidence-ledger`?
2. ☐ Is dropping `-mimo` paths OK, or move them under new names but keep `closed-v5-mimo` label?
3. ☐ Do you want a single PR commit for all renames, or per-project commits?
4. ☐ Should we include `OBSOLETE.md` redirect stubs, or rely solely on git history?
5. ☐ Is `policysim-research-Tsinghua` tracking in or out of this proposal?

Once these are answered, the rename can be executed via the rp-refactor-cli
flow (or a hand-tailored shell script for trivial cases).
