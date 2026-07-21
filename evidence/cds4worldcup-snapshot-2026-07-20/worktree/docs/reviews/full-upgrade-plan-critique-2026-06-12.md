# Critique: Full Upgrade Plan (2026-06-12)

> [!memo] 2026-06-12 Plan review — seams, specificity, and sequencing risks

## 1. Top 3 Under-Specified Seams

**WI-0.2: Raw wikitext parsing** — The plan says "解析 `wiki-wc2026-draw.json` 提取 12 组 × 4 队" but this file is **raw Wikipedia wikitext markup** (`{{#invoke:flag|fb|MEX}}` templates, not structured JSON). There is no specification of how to extract the Final Draw table from wikitext. An implementer must choose between: (a) regex scraping the `<section begin=Result />` block, (b) a Python wikitext parser dependency, or (c) hand-curating the 48-team mapping. Each has different failure modes and maintenance burden. This is the plan's single highest-risk gap because every subsequent WI depends on correct group data.

**WI-1.3: Elo/xG data source** — "基于 FIFA 排名（或 Elo 估算）+ 近期 xG 模拟" is a two-way fork masquerading as a parenthetical. FIFA rankings are public; Elo estimations require a source. More critically, **no data source is specified for xG (expected goals)** — it appears in neither the data-flow diagram nor any fetching script. Without xG, the Poisson model has no match-level input. This should be a named WI with a defined API/scrape target.

**WI-3.1 → WI-3.4: LLM provider identity** — The plan says "Python batch 脚本 + LLM API" and references cds4polymarket's TypeScript `LLMProvider`, but never names the provider (OpenAI? Anthropic? local?). This determines whether WI-3.1 is a 20-line SDK wrapper or a multi-day multi-provider abstraction. The ~1,500 runs/day cost envelope is also unquantified — at ~4K input + 500 output tokens per run, that's ~3M tokens/day, which is $3–30 depending on provider/tier.

## 2. Specificity Balance

**Over-specified**: WI-2.1 prescribes CSS Grid layout, three-color probability bars, mobile date-aggregation view, and `portal.css` variable reuse. These are UI implementation details that should emerge from iterative development. Similarly, WI-3.5 specifies exactly 6 agent roles with names ("路径分析师/来源审计员/市场观察员/反方挑战者/历史类比师/分歧审计员") — premature for a system whose behavior should be tuned empirically.

**Under-specified**: WI-0.2's Risk note says "约 10 队可能需替换" but actual comparison shows **21 teams** differ between `team_registry.csv` and the Wikipedia draw:

| Direction | Teams |
|-----------|-------|
| In Wikipedia, NOT in registry (11) | South Africa, Czech Republic, Bosnia, Haiti, Scotland, Curaçao, Sweden, Cape Verde, DR Congo, Jordan |
| In registry, NOT in Wikipedia (10) | Chile, Costa Rica, Italy, Denmark, Poland, Ukraine, Wales, Venezuela, Nigeria, Cameroon |

Additionally, all 48 teams need group reassignment (e.g., Spain: F→H, France: C→I, Argentina: B→J). This means new `team_name_map.csv` entries, new `artifacts/team-cards/*.md` files, and new path cards — effectively a full registry rebuild, not an "M (4h)" patch job.

## 3. Contradictions & Missing Dependencies

- **WI-4.1/WI-4.2 depend on Phase 3's LLM client** — Both "news summarization" and "player injury extraction" require LLM calls, yet they're in Phase 4 with only "WI-0.3" as dependency. They actually need WI-3.1 (LLM client) completed first. Placing them in Phase 4 creates a false sense of independence.
- **WI-3.2 claims "Dependencies: 无"** — But faction configs must reference match structure (which matches, what stakes). At minimum they need the schema from WI-1.1's `schedule.json` to define per-match context templates.
- **Factual error**: Plan states "11 untracked files"; `git status` shows 10 untracked items. Minor but suggests the plan was written from memory, not from a live tree check.
- **`predictions-data.js` (123KB) is untracked with no corresponding HTML** — the plan's working-tree audit lists it but no WI addresses it. If it's orphaned, it should be cleaned in WI-0.1; if it's needed, a consumer page is missing.

## 4. Risk of Over-Planning

- **WI-3.2 (10 faction YAML configs)** is premature design. Agent voting behavior should be iterated — start with 3–4 factions, validate that LLM outputs are meaningfully different, then expand. Designing 10 fixed personas upfront assumes the prompt engineering works on first try.
- **WI-4.4 (daily report with matplotlib + report.html)** is heavy infrastructure for an initial version. A Markdown report in `results/daily/` with auto-commit would achieve the same goal with 80% less code. The HTML rendering page can come later.
- **Phase 4's daily orchestrator (WI-4.3)** can be a `Makefile` target or a 30-line shell script initially. The manifest-tracking, graceful-degradation, GitHub Actions schedule can be layered in once the pipeline is stable.

## 5. Questions That Would Change Implementation Order

1. **What is the actual scope of WI-0.2?** If 21 teams differ (not ~10), WI-0.2 is a full registry rebuild (L/1d+), not M/4h. It should be split: WI-0.2a (parse wikitext → structured draw JSON), WI-0.2b (registry rebuild + name_map + team cards), WI-0.2c (regenerate downstream).
2. **Which LLM provider?** If OpenAI-only, WI-3.1 is trivial. If multi-provider with fallback, it's the plan's stated L-size. The answer changes Phase 3's duration by 1–3 days.
3. **Is `hero-bg.mp4` (2.3MB) intentional?** It's untracked and not mentioned in any WI. If it's site content, it needs Git LFS; if not, it goes in `.gitignore`. Should be resolved in WI-0.1 to avoid bloating the repository.
4. **Is the site pre-tournament or live?** If the World Cup hasn't started, Phase 4's daily automation has nothing to automate. Phase 3 (AI pipeline) could run against historical World Cup data for validation, making it independent of live data and allowing parallel execution with Phase 2.
