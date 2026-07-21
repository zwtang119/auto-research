# Critique: 全景审阅 + CDS 推演 + 管线整合 Plan

> **Reviewed:** `docs/plans/panoramic-review-cds-pipeline-2026-06-12.md`
> **Date:** 2026-06-12
> **Scope:** WI-PAN.1–11, CDS 两层引擎、前端渐进披露、每日管线整合

---

## 1. Top 3 Under-Specified Seams

### 1A. FIFA Tiebreaker Engine (WI-PAN.2) — H2H Mini-League Rules Ambiguous

WI-PAN.2 states the ranking order as "积分 > 净胜球 > 进球数 > H2H > 抽签" and calls for "3 队同分的 H2H 迷你联赛" tests. This is the most mechanically complex WI in the plan, yet the spec is one sentence. **Critical gaps:**

- **H2H scope ambiguity:** When 3+ teams are tied, FIFA 2026 rules recompute GD/GF/H2H within the *mini-league of tied teams only*, then fall back to overall GD/GF if still tied. The plan doesn't specify whether the engine must handle this nested fallback or just flat overall-then-H2H. The test mention of "3 队同分 H2H 迷你联赛" implies nested, but the stated order ("积分 > 净胜球 > 进球数 > H2H") reads as *overall* GD/GF *then* H2H — which is **not** the FIFA order for multi-team ties.
- **Fair-play / drawing-of-lots:** FIFA's actual tiebreaker continues through fair-play points and finally lots. The plan truncates at H2H > 抽签, omitting fair-play. An implementer must decide: hard-code fair-play (data dependency on discipline stats not yet in the pipeline), or treat it as draw?
- **4th-place team in 4-team tie:** With 48 teams in 12 groups, 3-way ties are common but 4-way is possible. No test case mentioned.

**Impact:** Wrong tiebreaker logic silently corrupts all 48 teams' qualification probabilities downstream. This is the load-bearing seam.

### 1B. Bracket Slot Parsing (WI-PAN.4) — Slot Vocabulary Undefined

The plan says `knockout_bracket.py` must parse "1A/2B/3ABCDF → W73/W74 等模式". Looking at `schedule.json`, the actual slot vocabulary is richer than implied:

- Group qualifiers: `1A`, `2A`, `2B`, `1C`, `2F`, `1E`, `2C`… (position + group letter)
- Best third-place: `3ABCDF`, `3EGHJK`, `3ABCDL` — compound group sets whose mapping depends on *which* third-place teams qualify, per FIFA's inter-group balancing table
- Winner propagation: `W73`, `W74`… `W90` (winner of match N)

The plan doesn't specify:
- Whether `knockout_bracket.py` must resolve the third-place slot logic (which third-place teams from which groups go to which R32 matches), or just pass through the literal slot labels. This is a FIFA-published mapping table — deterministic but non-trivial.
- How to handle the tree: `W73` feeds into `slot_home` of an R16 match. The plan says "返回每队从小组出线到决赛的所有路径节点" but doesn't specify the output data structure. Is it a DAG? A list of paths per team? Adjacency list?

**Impact:** Without the third-place mapping table, the bracket engine can't enumerate *any* team's path deterministically — it can only produce a partial bracket for the 24 known group qualifiers (1st/2nd), leaving all third-place slots unresolved.

### 1C. Championship Layer's Conditional Probability Inputs (WI-PAN.5) — Unspecified Dependency

WI-PAN.5 says it consumes "出线概率 + 淘汰赛 bracket + 每轮对手三信号概率" to build a conditional probability tree. But:
- Each knockout round opponent is probabilistic (depends on who wins prior rounds). Computing per-round "三信号概率" requires the coach model to have already simulated *hypothetical* matchups for teams that haven't been paired yet. The plan doesn't specify whether WI-PAN.5 calls the Elo engine directly for these hypothetical matchups, or depends on pre-computed coach data.
- The plan says CDS can "降级运行" on Elo alone, but doesn't specify what "降级" means structurally for the championship tree: does it use Elo probabilities at every node? Does it only fill Elo-based paths and leave coach slots as null?

**Impact:** An implementer must decide the probability source per tree node — this changes the architecture of `cds_path_simulation.py --layer=championship` significantly.

---

## 2. Specificity Balance

### Over-Specified

- **WI-PAN.6 UI details:** Dictates `coachMap[match_id]` key structure (`home_win/draw/away_win/confidence/expected_goals_*`), the accent color for coach bars, and "查看更多" expand behavior. These are front-end implementation decisions the agent should own. The schema alignment with `oddsMap` is architecturally relevant, but the CSS color choice is not.
- **WI-PAN.8 line references:** Pins to `homepage.js:296` and specific CSS class names (`ref-fill-ai`, `ref-fill-market`). Line references rot. The structural intent (3-bar chart from 2-bar) suffices.

### Under-Specified

- **WI-PAN.3 scenario aggregation:** "27 种聚合为 3-4 个关键情景" — what are the aggregation rules? "必胜出线" is clear (all remaining scenarios result in qualification), but "危局" and "已定" need threshold definitions (qual_prob ∈ what range?). The implementer must invent these thresholds.
- **WI-PAN.5 §7 field mapping:** The plan says championship output fills team-card §7's 8 null fields, but doesn't map which engine outputs to which fields. E.g., does `dominant_failure_node` come from the highest single-match probability drop, or the largest expected-value loss? Does `black_swan_dependency` come from §5 cross-reference or from the conditional probability tree?

---

## 3. Contradictions & Missing Dependencies

### Cross-Plan: WI-PAN.10 ↔ WI-4.3

WI-PAN.10 states: "跨计划依赖 full-upgrade WI-4.3 先实施". This is correct — WI-4.3 creates `daily-update.yml`. However:
- WI-4.3 depends on WI-3.4 (Kimi Agent) and WI-3.5 (CDS debate), per the full-upgrade plan. But the panoramic plan's CDS engine *replaces* the CDS debate concept (`cds_debate.py` → `cds_path_simulation.py`). If WI-3.5 is no longer needed, WI-4.3's dependency chain is stale. The plans should reconcile this.
- WI-PAN.10 also depends on "coach WI-CM.11" — but WI-CM.11 itself depends on WI-4.3. This creates a transitive dependency: WI-4.3 → WI-CM.11 → WI-PAN.10, which the plan's dependency diagram doesn't visualize.

### Cross-Plan: WI-PAN.6 ↔ WI-CM.8

Both plans modify `panorama.js:194` to add a new data map (`coachMap`). If WI-CM.8 (coach plan front-end integration) is implemented first, WI-PAN.6 (panoramic plan front-end) may conflict. The plan acknowledges "软依赖 WI-CM.7/8" but doesn't specify merge strategy.

### Missing: Third-Place Group Mapping Table

WI-PAN.4 needs FIFA's inter-group balancing table (which 3rd-place teams from which groups slot into which R32 matches). This is a static reference data file that doesn't exist yet and isn't listed as a dependency or a separate WI.

---

## 4. Risk of Over-Planning

- **WI-PAN.7 (CDS 路径分析面板, XL 2d):** This is the largest WI and the one most likely to be redesigned after user testing. The plan specifies three sub-components (scenario cards + path tree + Miracle Package status) in detail. Consider deferring the path tree visualization (the most visually complex piece) to a follow-up — scenario cards + §6 status alone deliver 80% of the value.
- **Factor Ledger integration (WI-PAN.11):** Generating Factor YAML for CDS outputs is metadata bookkeeping that doesn't affect user-facing functionality. The plan already notes WI-CM.10 (Factor Ledger for coach model) as "可推迟." WI-PAN.11's Factor work should get the same treatment.
- **Open Questions section declares "无":** For a plan with 11 WIs spanning two engines, a CI pipeline, and front-end integration across 3 plans, zero open questions is itself a risk signal.

---

## 5. Questions Whose Answers Would Change Implementation Order

1. **Is the 2026 format confirmed as 12 groups × 4 teams with 3rd-place advancement?** If the format or third-place rules change, WI-PAN.2 + WI-PAN.4 are the most affected and should be deferred until locked.
2. **Will the coach model (WI-CM.6) be ready before tournament start?** If not, WI-PAN.3/5 should be implemented with Elo-only from day one and the "soft dependency" treated as hard, changing the critical path.
3. **Is the path tree visualization (WI-PAN.7 sub-component b) required for MVP or can it ship after group stage ends?** If after, WI-PAN.7 drops from XL to M, and Phase C can parallel Phase B more aggressively.
4. **Does WI-3.5 (CDS debate, full-upgrade plan) still exist as a concept?** If it's superseded by this plan's CDS engine, the full-upgrade dependency tree needs updating before WI-4.3 can be correctly scoped.

---

## Summary

The plan is well-structured in its two-layer decomposition and explicit "never merge" signal discipline. The top risks are mechanical, not architectural: the FIFA tiebreaker engine (WI-PAN.2) and bracket slot parsing (WI-PAN.4) are under-specified for their deterministic-complexity level, and the cross-plan dependency graph has a stale node (WI-3.5) that should be reconciled. Cutting WI-PAN.7's path tree to post-MVP and marking Factor Ledger as deferrable would tighten the critical path from ~10d to ~6d.
