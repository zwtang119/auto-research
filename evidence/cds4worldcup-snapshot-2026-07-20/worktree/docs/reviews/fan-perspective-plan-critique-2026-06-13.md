# Critique: 球迷视角站点体检计划

> **Reviewed**: `docs/plans/fan-perspective-site-review-2026-06-13.md`
> **Compared against**: Oracle export `oracle-plan-2026-06-13-095515-54c164-1463.md`
> **Date**: 2026-06-13

---

## 1. Top 3 Under-Specified Seams

**Seam A — "Done when" references opaque check IDs without content.** Every work item's completion criterion is "完成 X-01 到 X-NN 检查," but the plan itself does not contain these check items. They live exclusively in the export (e.g., H-01 = "首屏 10 秒理解度", L-02 = "grep 所有渲染字符串"). An implementer who reads only the plan cannot judge scope or completion without cross-referencing the export. **Fix**: either inline the 1-line summary of each check ID into the plan, or add a single appendix table mapping ID → one-line description.

**Seam B — "检查方法" is undefined for every work item.** The plan lists key files but never says *how* to check. The export specifies concrete methods (grep commands, browser console JS snippets like `document.querySelectorAll('.source-badge')`, Chrome DevTools viewport tests). Without this, Item 6 "语言合规检查" could be done by visual spot-check or by full `grep -ri` — radically different effort and coverage. **Fix**: for each item, name at least the primary method (grep / visual / browser console / DevTools).

**Seam C — Item 12 "差距汇总" output format is unspecified.** The plan says "完成差距清单表格（含预填充的 10 条已知差距 + 新发现项）" but doesn't define the schema. The export defines a 9-field record format (编号/维度/页面/Spec 条款/差距描述/严重度/影响范围/是否已知/证据). Without this, the aggregator must invent their own structure and the resulting report may not match what downstream consumers expect. **Fix**: either inline the 9-field schema or point to the export's §3.1.

---

## 2. Specificity Balance

**Over-specified (plan locks a choice the implementer should own):**
- Item 12 has `Size: ~30 min 文档整理` — the only item with a time estimate. Either all items should have estimates (as the export's §4.3 provides) or none should; a single estimate creates a false precision anchor.

**Dropped useful framing from the export:**
- **"当前可检" vs "未来可检" distinction** — The export dedicates §3.3 (6 items) and Appendix A (10-row table) to classifying which spec acceptance criteria can be evaluated now vs. which are deferred. The plan mentions this in prose ("标记为'未来可检'而非当前差距") but never lists the items. An implementer must re-derive this classification to avoid false-gap findings.
- **Concrete grep / console commands** — The export provides executable verification methods (e.g., `grep -in "投注\|ROI\|PnL..." site/data/*.js` and browser JS for source-badge coverage). The plan drops all of these, losing reproducibility.
- **Dependency graph** — The export has an ASCII DAG showing parallel vs. sequential work. The plan only adds one dependency (Item 12 ← Items 1–11), losing the information that Items 1/6/7/8/9/10/11 are independently parallelizable.
- **Already-closed finding index** — The export's Appendix B cross-references every prior investigation finding to its treatment in the plan (e.g., "visual-inspection #1 → ✅ 已修复 → 不再检查"). The plan drops this, so an implementer may waste time re-verifying known-fixed bugs.

---

## 3. Contradictions & Missing Dependencies

- **Work item count mismatch**: The plan says "11 个可并行/有序执行的检查任务" (line ~46 of Approach section) but defines **12** items (Items 1–12). The export correctly lists W-01 through W-11 (11 work items) plus W-11 as the aggregator — 12 total. Minor but confusing.
- **Item 7 scope gap**: Item 7 "投注措辞红线检查" lists `site/data/*.js` and `scripts/build_site_data.py` as key files, but the export's B-03 specifically checks `_sanitize_public_text` in `build_site_data.py` for missing Chinese "买/卖" replacements. The plan's file scope is correct but the "done when" doesn't mention verifying the sanitizer's coverage, which is the only actionable finding (G-SANITIZE-01).
- **Missing dependency**: Item 10 "AI 多视角模块深度检查" has no stated dependency, but the export's W-07 depends on W-05 (brand isolation scan) because A-05 checks for vendor names in faction text — the same surface V-01 through V-04 cover. Running Item 10 before Item 8 risks redundant or inconsistent grepping.

---

## 4. Risk of Over-Planning

**Sections to simplify or cut:**
- **Part 2 spec-compliance dimensions** — The plan's Background section already has a "设计规格验收标准摘要" with 6 compliance dimensions. The Approach section then lists 8 dimensions. The export further expands each to 4–7 check items. For a 体检 report (understanding-focused, not fix-focused), the 8-dimension × 35-check-item matrix is heavyweight. Consider: collapse into 3 tiers — (a) quick grep checks (language + betting + brand — all can be automated), (b) visual checks (responsive + accessibility), (c) judgment calls (AI module quality, navigation gaps). This would halve the items without losing coverage.
- **Pre-filled gap table (10 items)** — Including 10 already-known gaps in the plan is useful context but bloats the plan itself. These are findings, not work items. Better: keep a one-line summary ("10 prior gaps will carry forward") and move the full table to the eventual report template.
- **Zero-dependency dimension (Items Z-01 to Z-04)** — The plan already confirms all 4 items as ✅ in the Background ("纯静态 HTML/CSS/JS，数据预构建为 JSON"). Including a full verification work item for something already confirmed is overhead. Flag as "no-action-needed" and skip.

---

## 5. Questions That Would Change Implementation Order

| # | Question | Why it matters |
|---|---------|---------------|
| Q1 | **Is the implementer a human with browser access, or an agent running grep?** | If agent-only: all visual/interaction items (H-01 screenshot, R-01 DevTools, W-02 click-through) are blocked; grep-only items should go first. If human: visual checks are cheaper than 35-row grep scans and should lead. |
| Q2 | **Should the 10 pre-filled gaps be re-verified or carried forward as-is?** | If re-verify: Items 6–10 each contain verification work for already-known gaps. If carry-forward: ~40% of each item's scope is pre-closed, halving effort. |
| Q3 | **Is the output a narrative report (理解) or a pass/fail compliance matrix?** | The CLAUDE.md framing says "理解为主" but the export's 9-field gap schema + severity ratings lean toward compliance audit. Answer determines whether Part 2's 8-dimension grid is the right structure. |
| Q4 | **Does "球迷视角" require recruiting actual fans, or is persona-based expert review sufficient?** | The plan's 2-persona approach (普通球迷 + 数据型球迷) is expert-simulated. If actual fan testing is desired, Items 1–5 need a protocol change (task-based scenarios, think-aloud), fundamentally restructuring the work. |

---

*End of critique.*
