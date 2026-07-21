# CDS4WorldCup Public Site AI + Market Upgrade Spec

> **Date**: 2026-06-12  
> **Audience**: AIwork / implementation agents  
> **Status**: ready for implementation  
> **Scope**: GitHub Pages public site only (`site/`, `scripts/`, `tests/`, `wiki/` progress note)  
> **Primary goal**: make the public site feel like an AI-assisted World Cup path analysis product, while keeping source discipline and plain Chinese for football fans.

## 0. Current Problems

The site has improved, but the current public experience still has five gaps:

1. **Team click expectation mismatch has mostly been fixed, but must be protected**  
   Homepage/team-list cards should open `site/team.html?team=<slug>` and show that one team's professional analysis. Do not regress to showing the full team list after a team click.

2. **Market snapshot is missing**  
   `site/data/team-details.json` currently shows market snapshot as `snapshot_unavailable`. This makes the external-reference section look weak, especially because the project already knows how to use Polymarket.

3. **The detail page contains developer-facing update text**  
   The following type of content must not appear on a visitor-facing page:
   - "后续更新"
   - "每场比赛后，不用重写页面"
   - `artifacts/team-cards/*.md`
   - `data/processed/market_public_snapshot.json`
   - `python3 scripts/build_site_data.py`

4. **The site looks like a data dashboard, not an AI analysis product**  
   Visitors should quickly understand: this is not just a static table; it is an AI-assisted, multi-perspective analysis system. However, do not advertise Kimi, Xiaomi, MiMo, or any vendor.

5. **Future updates need to be modular**  
   After every match, we should update data artifacts and rerun scripts. The implementer should not hand-edit HTML for every match.

## 1. Non-Negotiable Product Rules

### 1.1 Public Language

Use plain Chinese that football fans understand. Avoid academic or English-heavy phrasing.

Good:

- "这队凭什么能冲冠军？"
- "最怕哪种比赛？"
- "外界怎么看它？"
- "接下来先盯什么？"
- "只代表外界怎么看，不是投注建议。"

Avoid:

- "Epistemic tension"
- "baseline suite"
- "agentic long-horizon pipeline"
- "public AI baseline calibration"

### 1.2 Public Branding Boundary

Do **not** mention these on the public site:

- Kimi
- 小米 / Xiaomi
- MiMo
- MiMo Code Long-Horizon

Allowed public wording:

- "AI 多视角推演"
- "300 个独立视角"
- "公开模型群体参考"
- "外部模型参考"
- "多派别判断"

Use "AI" deliberately. The current site hides the AI nature too much. The goal is not to name the vendor; the goal is to make the visitor understand this is AI-assisted analysis.

### 1.3 Source Policy

Follow `docs/source-policy.md`.

- Green Source: official schedule, results, rankings, verifiable stats. Can support factual claims.
- Yellow Source: market snapshots, media summaries, aggregations. Can indicate external consensus or attention.
- Red Source: external model reasons and unverifiable predictions. Can be reference/baseline only.

Public UI must repeat this boundary in simple language:

> 市场和外部模型只代表外界怎么看，不是我们的事实依据，也不是投注建议。

### 1.4 Forbidden Betting / Investment Language

Do not output:

- 投注建议
- 买 / 卖 / sell / buy
- ROI / PnL / Sharpe / Kelly
- 仓位
- 低估 / 高估 / 正期望 / value bet

If raw source text contains those words, sanitize them before public JSON:

- "低估" -> "外界没有充分反映"
- "高估" -> "外界看得过热"
- "value" -> "外部判断分歧"

## 2. Target Visitor Experience

The public site should tell a clear story:

1. **Pick a team**  
   "你支持的队，夺冠到底要过哪几关？"

2. **See professional analysis for that one team**  
   The detail page should answer:
   - 这队凭什么能冲冠军？
   - 最怕哪种比赛？
   - 外界怎么看它？
   - 接下来先盯什么？

3. **Feel the AI analysis system behind it**  
   Add a visible "AI 多视角推演" module. It should show that many independent perspectives looked at the tournament, but it should not claim those perspectives are facts.

4. **See useful charts**  
   Use lightweight, static-friendly charts: CSS bars, compact dot matrix, faction cards, reference comparison bars. Do not add a heavy chart library unless there is a strong reason.

5. **Trust the boundary**  
   The visitor should understand what is fact, what is external reference, and what is entertainment/reference.

## 3. Market Snapshot Plan

### 3.1 What The Market Snapshot Is

Use Polymarket only as a Yellow Source external-reference snapshot.

It should answer:

- "外界现在给这支队多少热度？"
- "市场看法和公开模型群体参考差多少？"

It must **not** answer:

- "该不该买？"
- "有没有收益空间？"
- "哪个队被低估？"

### 3.2 Where The Data Comes From

Polymarket currently exposes a "World Cup Winner" event with many Yes/No markets.

Known discovery result from 2026-06-12:

- Event title: `World Cup Winner`
- Event slug: `world-cup-winner`
- Example market:
  - Question: `Will Spain win the 2026 FIFA World Cup?`
  - Slug: `will-spain-win-the-2026-fifa-world-cup-963`
  - `outcomes`: `["Yes", "No"]`
  - `outcomePrices`: `["0.1695", "0.8305"]`

Interpretation:

- Use the `Yes` price as probability.
- Convert `0.1695` to `16.95%`.
- Store the snapshot time.
- Store the original event slug and market slugs for auditability.

### 3.3 What The User Needs To Do

The user should not hand-edit JSON.

The only thing the user may need to provide once is the Polymarket event slug if automatic discovery fails:

```bash
POLYMARKET_EVENT_SLUG=world-cup-winner python3 scripts/fetch_market_snapshot.py
python3 scripts/build_site_data.py
```

If the script can auto-discover `world-cup-winner`, no user action is needed.

### 3.4 Implementation Task: `scripts/fetch_market_snapshot.py`

Add a zero-dependency Python script:

```bash
python3 scripts/fetch_market_snapshot.py
```

Optional environment variables:

- `POLYMARKET_EVENT_SLUG` default: `world-cup-winner`
- `POLYMARKET_SEARCH_QUERY` default: `FIFA World Cup 2026 winner`
- `MARKET_SNAPSHOT_OUT` default: `data/processed/market_public_snapshot.json`

Data source:

- Prefer `https://gamma-api.polymarket.com/public-search?q=FIFA+World+Cup+2026+winner&limit=20`
- Find event whose slug is `world-cup-winner`
- If discovery fails, try event slug lookup if there is a stable Gamma endpoint available
- If still failing, exit non-zero with a plain explanation; do not create fake data

Output schema:

```json
{
  "status": "available",
  "source": "polymarket_gamma_public_search",
  "event_slug": "world-cup-winner",
  "event_title": "World Cup Winner",
  "last_fetched_at": "2026-06-12T00:00:00Z",
  "display_rule": "只代表外界怎么看，不作为事实依据。",
  "teams": {
    "spain": {
      "probability": 16.95,
      "market_slug": "will-spain-win-the-2026-fifa-world-cup-963",
      "question": "Will Spain win the 2026 FIFA World Cup?",
      "raw_yes_price": 0.1695
    }
  }
}
```

Team mapping:

- Use `data/processed/team_registry.csv` and/or `data/processed/team_name_map.csv`.
- Parse questions like `Will Spain win the 2026 FIFA World Cup?`.
- Map English team names to our slugs.
- Handle known aliases:
  - `USA`, `United States` -> `united-states`
  - `Turkiye`, `Türkiye`, `Turkey` -> `turkey`
  - `Ivory Coast`, `Côte d'Ivoire` -> `côte-divoire`
  - `South Korea`, `Korea Republic` -> `south-korea`

Do not include placeholder markets such as `Team AM`, `Team AI`, `Any Other Team` unless they can be mapped safely. Unmapped rows should go into an `unmapped_markets` array for audit, not into public team probabilities.

### 3.5 Build Integration

`scripts/build_site_data.py` already reads:

```text
data/processed/market_public_snapshot.json
```

Keep that contract.

Improve it if needed:

- Include `event_slug`, `event_title`, `last_fetched_at`.
- In team detail, market reference should show:
  - probability if available
  - last fetched date
  - "待核验线索"
  - "只代表外界怎么看，不是投注建议"

### 3.6 GitHub Actions

Add an optional scheduled workflow only if it can be done safely:

- Run once every 6 hours or once daily.
- Fetch market snapshot.
- Build site data.
- Deploy Pages.

Do not commit on every schedule run unless the project already has a safe pattern. Prefer Pages build artifact deployment over bot commits. If uncertain, leave a documented manual command first.

## 4. Remove Developer-Facing Detail Page Content

### 4.1 Remove From `site/team.html`

Delete the whole visitor-facing section:

```html
<section class="section detail-panel update-contract">
  ...
</section>
```

### 4.2 Remove From `site/js/team-detail.js`

Remove:

- `updateRule`
- `updateSteps`
- `renderUpdateContract(...)`
- call to `renderUpdateContract(...)`

### 4.3 Remove From Public JSON If Not Needed

`build_public_team_details_json()` currently includes `update_contract`. This is useful for internal docs but should not be shipped in public detail payload unless another internal consumer needs it.

Recommended:

- Remove `update_contract` from `site/data/team-details.json`.
- Put update instructions in a developer doc instead, not the visitor page.

### 4.4 Add Developer Doc Instead

Create:

```text
docs/guides/public-site-update-flow.md
```

Explain:

1. Update path cards or generated artifacts.
2. Run market snapshot script if market refresh is needed.
3. Run `python3 scripts/build_site_data.py`.
4. Run tests.
5. Deploy Pages.

This doc is for maintainers, not visitors.

## 5. AI Feeling Without Vendor Advertising

### 5.1 Homepage Module: "AI 多视角推演"

Add a homepage section near the top, after "选球队" or before "外界怎么看":

Title:

```text
300 个视角，不是一个声音。
```

Subtitle:

```text
我们把外部模型群体拆成不同视角：数据、赔率、老球迷、主帅、伤病赛程、黑马、年龄结构、心理抗压、建模和娱乐向玄学。它们只提供参考，不替我们下结论。
```

This section should not say Kimi.

### 5.2 Data Source

Use existing:

```text
data/processed/kimi_agent_inventory.csv
```

But public label should be:

```text
public_model_crowd
```

or:

```text
external_model_perspectives
```

### 5.3 Public Payload

Extend `homepage.json`:

```json
{
  "ai_perspectives": {
    "status": "available",
    "perspective_count": 300,
    "faction_count": 10,
    "covered_team_count": 21,
    "source_level": "Red",
    "source_label": "只能参考",
    "display_rule": "这是外部模型群体参考，只代表不同视角怎么想，不作为事实依据。",
    "factions": [
      {
        "name": "数据派",
        "count": 30,
        "color": "#6E8499",
        "top_champions": [
          {"team_name": "西班牙", "count": 11}
        ],
        "representative": {
          "persona": "前德甲xG数据分析师",
          "champion": "西班牙",
          "reason": "..."
        }
      }
    ]
  }
}
```

Sanitize representative reasons:

- No "Kimi".
- No "低估/高估/value".
- No betting advice.
- Keep them short: max 90 Chinese characters in UI.

### 5.4 Visual Design

Borrow the **idea** from the Kimi UI, not the branding.

Use:

- Warm paper background: `#FBF9F1`
- Ink text: `#13233A`
- Morandi faction colors:
  - `#6E8499`
  - `#A85F50`
  - `#7E9070`
  - `#C2A75F`
  - `#97768F`
  - `#5E807A`
  - `#C07E55`
  - `#B27D7E`
  - `#76729A`
  - `#B59A6B`

Component:

- 10 faction cards in responsive grid.
- Each card has:
  - faction name
  - `30 个视角`
  - 30 small dots in a 6 x 5 grid
  - dots are solid pale faction color by default
  - hover/focus shows one representative persona/reason
- No empty grey hollow circles.
- No giant numbered blocks.
- The grid should look full even before animation.

Motion:

- CSS-only stagger/fade is fine.
- Respect `prefers-reduced-motion`.
- Do not make the page feel like a game if it hurts readability.

### 5.5 Detail Page AI Module

On `team.html?team=<slug>`, add a small visitor-facing module:

Title:

```text
AI 多视角怎么看这队？
```

Content:

- Show public model probability if covered.
- Show 2-4 faction snippets for that team if available.
- Show source badge: "只能参考".
- Explain: "这些只是外部模型群体的看法，不能当事实。"

If team has no public model coverage:

```text
这支队还没有外部模型群体参考。我们先保留路径拆解，等后续数据补齐。
```

## 6. Chart Requirements

Use the chart-visualization skill conceptually, but prefer static-friendly HTML/CSS charts.

### 6.1 Homepage Charts

Required:

1. Obstacle distribution bar chart  
   Already exists. Make it visually better if needed.

2. AI perspective faction grid  
   New.

3. External reference Top 8 chart  
   Compare:
   - public model crowd probability
   - market snapshot probability if available

If market snapshot is missing, do not fake numbers. Show "市场快照待更新".

### 6.2 Team Detail Charts

Required:

1. Team obstacle chart  
   Existing.

2. External reference chart  
   Should include:
   - 48-team average line
   - public model crowd
   - market snapshot

3. Optional: "路径兑现清单"  
   A compact checklist is better than another chart if data is qualitative.

## 7. Writing Requirements

Use consulting-analysis discipline, but write in football-fan Chinese.

Each team detail page should read like:

1. **结论先行**: "阿根廷要夺冠，关键不是梅西还能不能天神下凡，而是球队能不能把他从唯一答案变成加分项。"
2. **证据/路径**: explain what must happen.
3. **看球抓手**: tell visitors what to watch next.

Avoid generic filler:

- "核心球员状态在线"
- "临场调整不掉链子"

These are acceptable as fallback, but deep teams should have sharper writing based on their path card.

## 8. Files To Modify

Expected files:

```text
scripts/fetch_market_snapshot.py          # new
scripts/build_site_data.py                # extend homepage/team detail payloads
tests/test_build_site_data.py             # update tests
site/index.html                           # add AI section container
site/team.html                            # remove update-contract, add AI module container
site/js/homepage.js                       # render AI perspectives + market chart
site/js/team-detail.js                    # remove developer update renderer, add AI module
site/css/portal.css                       # visual polish
docs/guides/public-site-update-flow.md    # new maintainer guide
wiki/decisions/cds4worldcup2026-path-space-spec.md # append memo
```

Do not modify:

```text
docs/references/**
schema/**
templates/**
example/**
```

Do not stage or commit:

```text
AGENTS.md
.playwright-mcp/**
```

## 9. Tests And Validation

### 9.1 Unit Tests

Run:

```bash
python3 -m unittest tests/test_build_site_data.py
```

Add test coverage for:

- `homepage["ai_perspectives"]` exists.
- `perspective_count == 300`.
- `faction_count == 10`.
- `covered_team_count == 21`.
- no public JSON contains Kimi/Xiaomi/MiMo/MiMo Code Long-Horizon.
- no public JSON contains betting/investment terms.
- `team-details.json` does not contain `update_contract`.
- `market_public_snapshot.json` sanitization works with a fixture.

### 9.2 Build

Run:

```bash
python3 scripts/build_site_data.py
```

If implementing market snapshot:

```bash
python3 scripts/fetch_market_snapshot.py
python3 scripts/build_site_data.py
```

### 9.3 Wiki

Append a memo to:

```text
wiki/decisions/cds4worldcup2026-path-space-spec.md
```

Run:

```bash
python3 scripts/verify.py --root wiki/
python3 scripts/audit.py --root wiki/
```

Current known audit issue:

- 7 P2 orphan pages may already exist.
- Do not treat existing P2 orphan pages as a blocker unless new P0/P1 appears.

### 9.4 Browser Validation

Run local server:

```bash
python3 -m http.server 8000 --directory site
```

Check:

- `http://localhost:8000/`
- `http://localhost:8000/team.html?team=argentina`
- mobile viewport around `390 x 844`

Must verify:

- no "Failed to fetch"
- homepage team cards link to `team.html?team=<slug>`
- detail page shows only one team
- no visitor-facing developer file paths
- no Kimi/Xiaomi/MiMo brand terms
- AI multi-perspective module is visible
- charts do not overflow on mobile
- no horizontal scroll

### 9.5 Online Validation After Deploy

After pushing to `main`, check:

```text
https://zwtang119.github.io/cds4worldcup/?v=<commit>
https://zwtang119.github.io/cds4worldcup/team.html?team=argentina&v=<commit>
```

## 10. Acceptance Criteria

The implementation is accepted only if all are true:

1. A team click opens a single-team professional analysis page.
2. The detail page no longer shows developer update instructions.
3. The homepage visibly communicates "AI 多视角推演" without mentioning Kimi/Xiaomi/MiMo.
4. Market snapshot can be generated by script and displayed as Yellow Source if available.
5. If market fetch fails, the site still builds and clearly says market snapshot is not available.
6. No public page gives betting advice or investment-style wording.
7. Public writing is plain Chinese and useful to football fans.
8. Future update flow is documented for maintainers, not visitors.
9. Tests pass.
10. Local and online browser checks pass.

## 11. Recommended Implementation Order

1. Remove developer update section from detail page.
2. Add market snapshot script and fixture tests.
3. Extend build data with AI perspectives.
4. Render homepage AI perspective module.
5. Render team detail AI module.
6. Polish CSS and mobile layout.
7. Rebuild site data.
8. Run tests and wiki verification.
9. Browser test locally.
10. Commit, push, verify GitHub Pages.

## 12. Notes On Assets

Useful local references exist:

```text
/Users/tangzw119/Downloads/Kimi_Agent_世界杯热力榜 UI 升级.zip
/Users/tangzw119/Downloads/Kimi_Agent_世界杯球迷人格测试.zip
/Users/tangzw119/Downloads/Kimi_Agent_为什么有些国家足球就是强.zip
/Users/tangzw119/Downloads/2026_World_Cup_White_Paper.pdf
/Users/tangzw119/Downloads/2026世界杯数据全景工作簿.xlsx
```

Use these as reference material only. Do not copy vendor branding into the public site.

If using any video/image asset from a zip:

- keep file size reasonable
- put only public-safe assets under `site/assets/`
- do not commit large raw source zips
- ensure GitHub Pages loads quickly

For this iteration, a video hero is optional. The AI perspective module and market snapshot are higher priority.

