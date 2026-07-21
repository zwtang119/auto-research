# Critique: Homepage Optimization Spec Review Plan

> **Review of**: `docs/plans/homepage-optimization-spec-review-2026-06-12.md`
> **Date**: 2026-06-12
> **Scope**: Plan quality, not spec quality — does this plan reliably guide an implementer?

---

## 1. Top 3 Under-Specified Seams

**Seam A — Data contract between Phase B and Phase D is undefined.** The plan lists B7 ("扩展 `build_site_data.py` 产出 `matches.json` 和 `odds.json`") but never specifies the JSON schemas. An implementer must guess field names, nesting depth, and how `panorama.json` (Phase D6) relates to the existing `homepage.json` 12-key contract. Without this contract, B and D can be built in parallel (as the plan suggests) only to discover they don't connect.

**Seam B — Phase A6 assumes the competing spec completes without conflict.** A6 says "按升级计划的 Task 1-11 完成" the `public-site-ai-market-upgrade` spec. But that spec may extend `site/`, `portal.css`, and `build_site_data.py` in ways that collide with Phase B's architecture choices (e.g., new CSS variables, modified JSON keys). The plan has no reconciliation step between A6 output and B1-B8 design.

**Seam C — Phase C4 hand-waves the API execution environment.** The plan correctly identifies M7's architecture problem (spec §17.1: MiMo can't spawn 300 API calls) and recommends "Python batch," but C1 (`api_client.py`) doesn't specify: where do API keys come from? GitHub Actions secrets? Local env? How does `daily_orchestrator.py` run — on GitHub Actions (2h timeout, no GPU) or Mac mini (availability SLA)? The §17.2 cost analysis (L2: ~1,500 runs/day) is presented but the plan defers the L-level decision to an open question, leaving C4's scope undetermined.

---

## 2. Specificity Balance

**Over-specified (tactical choices the implementation agent should own):** Phase A's seven tasks read like implementation tickets with acceptance criteria. A1 ("修复 `portal.css:1334-1377`") is a ~10-line CSS fix — specifying line numbers in a plan adds maintenance burden without aiding execution. A3 ("补全禁用词列表") is similarly granular. These should be a single "fix all P0/P1 bugs" work item; the implementation agent can discover specifics from the investigation reports.

**Under-specified (dropped useful framing):** The plan correctly identifies the spec's §17 contradictions (⚠️ 1-7) but then recommends only "修订正文" without saying which contradictions *block* execution vs. which are cosmetic. For example: ⚠️ 4 (§7.7 vs §17.1 — MiMo can't do 300 runs) is a blocking architecture contradiction that must be resolved before Phase C starts, while ⚠️ 2 (zero-dependency vs D3/Plotly) is a design clarification that the implementer can resolve at D-time. The plan treats them equally.

Also dropped: the spec's §2 reference-project analysis (policysim batch patterns, cds4polymarket Arena class, institute-one VaultWriter) is genuinely useful implementation guidance. The plan dismisses the entire spec but these patterns could directly inform C1-C8. An implementer would benefit from a "keep these §2 patterns" note.

---

## 3. Contradictions & Missing Dependencies

- **Phase D dependency diagram is misleading.** The plan says D "可以 B 完成后用 mock 数据先行," but D6 (build pipeline integration) and D7 (navigation integration) require C's aggregation output and A6's completed `site/` state. The actual critical path is A → B → C → D; D can prototype with mocks but cannot ship without C.

- **B8 (wiki match pages) conflicts with Marginalia protocol.** The plan notes (⚠️ 3) that the spec's `wiki/teams/`, `wiki/players/`, `wiki/matches/` structure breaks the existing `wiki/concepts/`, `wiki/decisions/`, `wiki/annotations/` Marginalia layout. B8 creates 72 match pages anyway, without resolving this. `scripts/audit.py` will flag every new page as a protocol violation.

- **Phase A7 (MiMo reliability) outcome changes everything downstream.** If MiMo Campaign is fundamentally unreliable, Phases C4-C6 must be pure Python batch — a different architecture than what's assumed. The plan acknowledges this risk but doesn't define a decision gate or alternative architecture sketch.

---

## 4. Risk of Over-Planning

**Can cut or simplify:**
- Phase A's 7 individual tasks → 2 work items: "fix P0/P1 bugs (A1-A5)" and "complete competing spec (A6)." A7 (MiMo verification) is exploratory; make it a spike, not a phase gate.
- The scoring rubric (§1 five dimensions, 2-3/5 each) and the full findings table (7 ✅, 10 ❌, 7 ⚠️) are excellent *input* to the plan but redundant *inside* the plan. An implementer needs the phased tasks, not the spec evaluation that produced them. Move to an appendix or keep in the investigation doc.
- Open Questions #3 (L1-L4 voting tier) and #5 (§17 merge strategy) can be deferred — they don't block Phase A or B.

---

## 5. Questions Whose Answers Change Implementation Order

1. **Does the competing spec's remaining 10% touch `build_site_data.py` or `portal.css`?** If yes, Phase B must wait for A6 to settle the data contract and CSS variable namespace. If no, B can start immediately after A1-A5.

2. **Is MiMo Campaign fixable?** A7 determines whether M6/M7 use MiMo (simpler, less reliable) or Python batch (more engineering, more reliable). This changes Phase C from "configure MiMo modules" to "build API client + batch runner" — different skill set, different effort.

3. **What's the daily API budget?** L2 (~1,500 runs, ~$2-5/day) is sustainable; L1 (21,600 runs, ~$30-80/day) changes Phase C from a scripting task to a cost engineering task. The plan can't scope C4 without this answer.

4. **Does baseline filling (B6) reveal data quality issues?** If the 6 baselines can't be populated from existing sources, the "先数据后展示" principle means Phase D is blocked until source gaps close — and the source gap map shows 0 teams with Green Source. This may push the full plan's timeline from 12-18 weeks to "wait for qualification to finalize."
