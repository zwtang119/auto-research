# Cross-Project Pitfall Wiki — Plan (NOT executed)

> **Status**: PLAN ONLY. Do not execute until user explicitly signs off.
> **Created**: 2026-07-03
> **Author**: AUTO agent (in response to user request)
> **Memory reference**: `notes.md` of session `ses_0d97c9d65ffetVZWgKZgNV91CC` carries the locked decisions.
> **Past-attempt note**: A first draft of `pitfalls-and-recoveries.md` was written in a prior turn but rolled back per user "目前不要执行". This plan supersedes that abandoned draft.

---

## 0. The user's request (verbatim, three turns collapsed)

> 我计划阅读/Users/tangzw119/Documents/GitHub下的各个项目的开发文档，找到遇到的坑。看看本项目是否会踩到。这是一个长期任务。请你做好准备（比如提前压缩内存）等。我强烈建议你做一个踩坑笔记。方便后续各个项目继承。这个踩坑笔记应当在/Users/tangzw119/Documents/GitHub/wiki中。同时，也可以写一个各个项目的优点（供后续开发借鉴，不过似乎太多了？），也放在/Users/tangzw119/Documents/GitHub/wiki中。请你规划一下，看看怎么做才是恰到好处的。

Three asks:
1. Read sibling-project docs under `/Users/tangzw119/Documents/GitHub/`,
   find pitfalls, check whether auto-research has/will hit them.
2. Write a **pitfall-catalog notebook**, committed (long-term maintained)
   at `/Users/tangzw119/Documents/GitHub/wiki/`.
3. (Optional) Cross-project **strengths** reference — user expressed doubt
   ("似乎太多了?"),**recommended to skip** per user-confirmed Q&A in prior turn.

The user's repeated phrasing signals:
- This is **long-term**, not a single-session task.
- Memory should be **compressed** before we start (avoid context bloat).
- Single, easy-to-find notebook location (not scattered docs).
- Don't go overboard with the optional strengths section.

---

## 1. Locked design decisions (from prior Q&A)

| # | Decision | Rationale | Source |
|---|---|---|---|
| D1 | Output location: `/Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md` (top-level file, **not** a subdir) | Wiki's single-entry rule: `index.md` is the only entry; everything else is reachable from it. A top-level file + 1-line entry in `index.md` honors this rule. A new subdir (`pitfalls/`) would create a second-tier "entry" feel. | user (Q2 round-1) |
| D2 | **Skip** strengths/strengths-reference section | User flagged "似乎太多了" → confirmed skip via Q3 | user |
| D3 | Multi-Phase reading; Phase 1 = **薄扫 / thin scan** of top docs only | Avoid context explosion; long-term task; max 2–3 projects per session start | user (Q3 round-1) |
| D4 | PIT ID format = `PI-NNN` (zero-padded). Status marks: 🔴 已踩 / 🟡 未踩但暴露 / 🟢 防御已布 / ⚪ 未评估 | Mirrors existing wiki decisions/concepts taxonomy; easy grep | design |
| D5 | Each entry ≤ 80 lines; cross-link instead of inlining large blocks | Wiki is browsable, not a thesis | design |
| D6 | PIT must cite source `path#section` or `git sha`; no orphan entries | Provenance is enforceable later | design |

---

## 2. Scope

### 2.1 Phase list

| Phase | Reading depth | Output | Approx time |
|---|---|---|---|
| **Phase 0** (DONE) | None — curated 2 PITs from in-session memory | None — file not written (rolled back) | n/a |
| **Phase 1** | Thin scan: `README.md` / `CLAUDE.md` (when present) / `AGENTS.md` (when present) / `docs/index.md` for **15+ sibling projects** | 30–60 PIT entries (3–6 per project), auto-research exposure re-evaluated from ⚪ → 🔴 / 🟡 / 🟢 | 3–5 sessions |
| **Phase 2** | Mid-deep: open project-local `docs/investigations/`, `docs/postmortem/`, `CHANGELOG.md`, `experiments/` READMEs | Add cross-project recurring patterns; consolidate duplicates | 2–3 sessions |
| **Phase 3** | Deep dive on top 3 most-leveraged sources (e.g. cds4polymarket, Policysim-v0.2, Marginalia) | Add 5–10 cross-cutting "meta-PITs" (e.g. protocol-vs-implementation divergence) | 2–3 sessions |
| **Phase 4** | maintenance, no new reading | Refresh ⚪ → 🔴/🟡/🟢 per current auto-research code | 1 session, can repeat |

### 2.2 Project list (Phase 1 surface)

From `ls /Users/tangzw119/Documents/GitHub/`, working set:

1. `cds-keyperson`           (CDS-related, large)
2. `cds4polymarket`          (CDS-related, large)
3. `cds4worldcup`            (CDS-related, large)
4. `Policysim-v0.2`          (CDS-related, large)
5. `policysim-v0.1`          (sibling sim)
6. `policysim-research-Tsinghua` (current experiment substrate; already in vendor mode)
7. `Policysim-v0.1-tsinghua` (sibling sim)
8. `Marginalia`               (knowledge-base tooling; relevant to wiki convention)
9. `Stock-Claw-OS`            (stock-trading bot; AI agent patterns)
10. `flow-island`              (game / agent sim)
11. `0ref`                     (reference collection)
12. `PaperMirror`              (paper-tracking tool; relevant to paper-writing skill)
13. `prompt-exports`           (LLM prompt archive)
14. `PolicySimulation`         (CDS-related)
15. `external_code`            (small, may be skipped after first glance)

Skip candidates (out of scope for "踩坑笔记"):
- `wiki/` itself — *target*, not source.
- `auto-research/` — that's the *consumer* of the catalog, not a sibling.

### 2.3 Out of scope

- Generic engineering postmortems (find them in `wiki/sources/` instead).
- Per-paper lessons-learned (kept inside each paper's `wiki/` per project-local convention).
- A "strengths catalog" (D2 says skip).
- Re-tooling auto-research code (this catalog is observational; fixes live in follow-up plans).

---

## 3. File-shape contract (will be applied when executed)

`/Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md`

Top-level structure (single file, ~150–250 lines):

```
# Cross-Project Pitfalls and Recoveries            (~10 lines: meta + owners + conventions)
## Top-Pitfalls-Index                                (~30 lines: table of all PITs w/ status)
## PI-NNN format                                     (~25 lines: template definition)
## PI-001 ...                                        (each entry ≤ 80 lines, body)
## ...
## Phase Log                                         (~5 lines per Phase: date + scope summary)
```

`/Users/tangzw119/Documents/GitHub/wiki/index.md`

Inject ONE line under whatever section "cross-engineering" falls (likely
"其他" or near "comparisons"). Acceptable: a 2-line block:

```md
### 🔩 工程经验
- [[pitfalls-and-recoveries]] — 跨项目踩坑笔记（auto-research 等 15 项目）
```

That is the **only** persistent index update.

---

## 4. Execution discipline (proposed)

### 4.1 Per-session discipline

When the user gives the go-ahead, the FIRST session does Phase 1 step 1
(read 3 projects' top docs). Each subsequent session:

1. Read up to **3 projects' top docs** (≤ 5 files per project). Reread
   via file_search (do NOT keep full READMEs in memory).
2. Summarize into 200-line blocks per project.
3. Convert each project block into 3–6 PITs with the schema.
4. Append to `pitfalls-and-recoveries.md` (Phase Log entry + new PITs).
5. Update `index.md` if a new section-heading lands.
6. Re-evaluate existing ⚪ → 🔴 / 🟡 / 🟢 against current
   `auto-research/` code; surface any new matches in `state/progress.json`
   by linking to the PIT entry.
7. **Memory flush at end of session**: append a 30-line "Phase N summary"
   block to `notes.md` of session `ses_0d97c9d65ffetVZWgKZgNV91CC`; then
   drop the project summaries from working memory.

### 4.2 File-system changes per Phase (cumulative)

| Phase | files affected | scope |
|---|---|---|
| 1 | `wiki/pitfalls-and-recoveries.md` (created, ≈ 60–100 lines after 1st batch) + `wiki/index.md` (1–2 lines) | minimal, reversible |
| 2 | append-only growth of pitfall file (+ ≈ 80 lines) | minimal |
| 3 | same | minimal |
| 4 | status marks refresh; no new files | minimal |

Cumulative target: end of Phase 1 file ≈ 300 lines; end of Phase 3
file ≈ 800 lines. After that, prune duplicates rather than grow further.

---

## 5. Sub-agent plan for Phase 1 step 1 (most risky to over-engineer)

If user wants parallelism later: a single **explore** subagent per
project reads its top 3 docs and emits a 50-line bulleted summary. The
main agent then condenses summaries into PIT entries. NEVER spawn a
subagent to write `pitfalls-and-recoveries.md` directly; keep the file
write in the main agent so the cross-project lens stays consistent.

But for step 1 (this session, if approved), I'll do it inline — the
first 3 projects are short. Don't dispatch agents for the first batch.

---

## 6. What I'll need from you to start

| # | Decision (some already locked) |
|---|---|
| ✅ | Output location & format (D1, D4–D6) |
| ✅ | Skip strengths section (D2) |
| ✅ | Thin-scan Phase 1 strategy (D3) |
| ☐ | **GO/NO-GO on actually creating the file in this session** |
| ☐ | If GO, **first batch size**: 3 projects (default in D3) or 1 project (most conservative)? |
| ☐ | **First batch target projects** — my suggestion (in this order, due to relevance): `policysim-research-Tsinghua`, `Policysim-v0.2`, `cds-keyperson`. User can override. |

---

## 7. What I will NOT do (boundary enforcement)

- Will not write to `/Users/tangzw119/Documents/GitHub/wiki/` without
  the explicit GO above.
- Will not modify `auto-research/` state at all in this task. Cross-checks
  against auto-research code are read-only here; live fixes belong in a
  separate plan (we already have FRAMEWORK-RULES.md tracking prevention).
- Will not write any data to `wiki/concepts/`, `wiki/decisions/`, or
  other wiki sub-dirs unless the strength catalog is approved (D2 = skip).
- Will not read every project in one session. Phase 1 batch cap is 3 projects.

---

## 8. Verification after execution (proposed)

After each Phase, verify:

```bash
ls -l /Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md
head -5  /Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md
grep -c "^### \[PI-"  /Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md   # PIT count
grep -c "^## Phase"   /Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md   # Phase count
grep -nE "pitfalls-and-recoveries" /Users/tangzw119/Documents/GitHub/wiki/index.md     # index link present
wc -l  /Users/tangzw119/Documents/GitHub/wiki/pitfalls-and-recoveries.md                # line count within envelope
```

Single-entry rule check: `index.md` contains a link to the new file.

---

## 9. Open question (for your sign-off only)

Question: when Phase 1 first batch is done (≈ 3 projects deep), do you
want me to:
- (a) **STOP and review** what got added before continuing.
- (b) **Continue autonomously** until Phase 1 finishes (~5 batches).
- (c) **Pause at every PIT entry** for individual sign-off (overkill).

Default I'd take if you say nothing: **(a) stop after first batch**.
That gives you the first 3–6 PITs at quality bar for inspection before
committing more sessions.

---

## 10. Self-check on planning fidelity

- [x] Reads scope matches user request.
- [x] Output location is single-file (per single-index rule).
- [x] No execution happened in this session beyond this plan + the
      memory flush.
- [x] Memory alignment: no orphan references to a file that doesn't
      exist (rolled back the prior write + corrected `notes.md`).
- [x] Long-term compression: phase-bounded reading cap, summary-only
      retention, REREAD via file_search rather than caching.
- [x] Verifiability: explicit `verification` block (§8) so the next
      session can assert the plan succeeded.
- [x] Stop rule: §9 asks the gating question before spinning up Phase 1.

EOF
# (Plan ends here. Below: not part of the plan file — sign-off summary.)

---

# 等你回复这一段就行

**问题清单**（已锁定的决策我都跳过了，只问真正阻塞的三条）:

- **Q1**: 可以开始吗？(默认: 等你明确 GO 才能动 `wiki/`)
- **Q2**: 第一批读几个项目？(默认: 3 个，按 `policysim-research-Tsinghua → Policysim-v0.2 → cds-keyperson` 顺序，因为这两个 policysim 跟我现在 vendor 关系最近)
- **Q3**: 第一批结束后让我继续做还是停？(默认: 停，给你 6–18 个 PIT 看完再续)

确认后我在**下一个会话轮次**就开始 Phase 1 第 1 批（不抢这次会话，强迫自己落地"先计划后执行"的纪律）。Plan 文档已经存在 `auto-research/docs/compose/plans/2026-07-03-cross-project-pitfalls-plan.md`，加上 notes.md 的事件纪要，下次会话 reload memory 就能续上。