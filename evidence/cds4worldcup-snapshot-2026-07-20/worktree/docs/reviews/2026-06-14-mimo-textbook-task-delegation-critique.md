# Critique: MiMo Textbook Task Delegation Plan

**Plan:** `docs/plans/2026-06-14-mimo-textbook-task-delegation.md` · **Date:** 2026-06-14 · **Type:** review
**Verdict:** the independent conclusion (bounded 2-field probe over blanket `/goal`) is sound; three containment seams are load-bearing and unresolved, plus housekeeping cuts.

## 1. Top 3 under-specified seams

**(a) Cross-repo execution site is undecided, yet every downstream WI assumes it.** Open Q1 defers "cds4worldcup vs `policysim-research-Tsinghua` 侧运行 MiMo" to the user, but WI-1⑦ (write boundary `mimo-probe/{…}/**`), WI-2.3 (boundary exit 0), and WI-5 rollback all presuppose MiMo executes *inside* the `policysim-research-Tsinghua` working tree with that repo as cwd. If MiMo runs from `cds4worldcup` and reaches across by absolute path, the relative prefixes resolved in `mimo_boundary_check.py:48-58` anchor to the wrong root. WI-0 should state this as a blocking assumption, not leave it as a footnote.

**(b) `boundary_check` is an advisory auditor, not a guardrail — and the plan mis-describes how to retarget it.** Spot-checked `scripts/mimo_boundary_check.py`: `PROJECT_ROOT = Path(__file__).parent.parent` (line 14) is *auto-derived from the script's location*, and detection is a single `git status --short` (lines 21-24). So (i) you cannot "改 PROJECT_ROOT→policysim-research-Tsinghua" as WI-0(c) literally says — you relocate the file and edit only the prefixes; and (ii) no pre-commit/wrapper enforcement is shown. B3 already proved MiMo ignores protocol under load (mutated `campaign_state.json`/`task_queue.json`). WI-0(d)'s "dry-run exit 0" proves the script imports on an empty tree, not that containment holds. What actually gates MiMo's writes is unspecified.

**(c) `.gitignore` blinds the only detection mechanism.** WI-0(a)/(b) puts `mimo-probe/` in `.gitignore`; `boundary_check`'s sole input is `git status --short`, which omits ignored paths. A clean "OK: No changes detected" can therefore coexist with MiMo having written anywhere — the *allowed* writes are invisible, and the check can only catch forbidden writes to tracked paths. Phantom-file detection (`test -f`, WI-2.1) survives, but WI-2.3's classification assertion is partly defeated by WI-0's own gitignore. Not addressed.

## 2. Specificity balance
- **Over-specified:** WI-2.5's "runtime ≥ 30 min/领域" is a weak proxy for "didn't early-stop"; the ≥2-path fetch-attempt log (§5.4, already in the same item) is the real signal — drop the wall-clock floor.
- **Dropped framing:** no WI gates on MiMo's *own* networking quota as a precondition (Open Q3 raises it, no WI owns it). Since 02/06 were chosen *because* they're citation-dense and the baseline hit the quota wall, whether MiMo can fetch at all determines whether the probe tests citation discipline vs. tests quota.

## 3. Contradictions / missing dependencies
- **Quota vs citation gate:** WI-2.4 requires Green citations carry a resolvable URL/arXiv ID/ISBN, but Open Q3 warns MiMo may share the quota wall → the probe could be *structurally* unsatisfiable through no capability fault. Quota status must be confirmed before WI-2.4 can judge anything.
- **Baseline leakage:** WI-1⑧ copies baseline `fields/02`/`fields/06` structure into the prompt, yet WI-3 treats those same files as independent diff ground-truth. If MiMo sees the baseline, the comparison isn't blind. Unresolved.
- **WI-3 "offline stage 现在可做"** — only the *harness* is buildable now; offline verification can't start until MiMo drafts exist (external action). Sequencing blurred in the "Done when."

## 4. Over-planning risk — cut / merge
- **Cut WI-5** entirely. It restates WI-0 (the plan itself sizes it "S（并入 WI-0）"). Its one novel line — "MiMo 输出永远为候选/Red Source" — belongs in WI-1's role framing, not its own WI. The rollback argument is also already made in Approach §4.
- **Merge WI-2 ↔ WI-4.** Both enumerate the same six B3 failure modes; WI-2 = assertions, WI-4 = pass thresholds. Fold the threshold table into WI-2 and drop a work item.

## 5. Questions that reorder implementation
1. **Where does MiMo run (which repo's tree)?** → blocks WI-0/WI-1 (prefixes + cwd). Promote Open Q1 to a blocker.
2. **Is `boundary_check` advisory-only, or wired as a pre-commit/wrapper?** → changes WI-0(d)'s done-condition and whether WI-2.3 is a real gate.
3. **MiMo's networking quota before 2026-06-21?** → if MiMo also can't fetch, either defer the citation-dense 02/06 fields or the WI-2.4 Red=0/URL gate is unsatisfiable. Answer before WI-1.
4. **Does the probe get to see the baseline `fields/02`/`06`?** → determines WI-1⑧ legality and WI-3 independence.
