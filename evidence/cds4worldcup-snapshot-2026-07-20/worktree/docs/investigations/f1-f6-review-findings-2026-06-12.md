# Investigation: F1-F6 Code Review Findings Verification

## Summary

Verified 6 non-blocking findings from the spec compliance review. **F1 is a false positive** — the CSS rules are correctly inside a `@media (max-width: 900px)` block. F2-F6 are confirmed real but low severity. None are currently breaking anything.

## Findings

### F1 — CSS Orphaned Rules: **FALSE POSITIVE** ❌

**Claim:** Lines 1347-1379 in `site/css/portal.css` have bare grid rules outside any `@media` wrapper.

**Reality:** The rules ARE inside `@media (max-width: 900px)` which opens at line 1321 and closes at line 1379. The `@media (max-width: 640px)` at line 1336 is NESTED inside the 900px block. The brace structure:

```
1321: @media (max-width: 900px) {        ← opens
1336:   @media (max-width: 640px) {      ← nested opens
1345:   }                                 ← nested closes
1347:   .hero, ... { grid-template-columns: 1fr; }  ← still inside 900px
1379: }                                   ← closes 900px
1381: @media (max-width: 640px) {        ← new separate block
```

**Conclusion:** Not a bug. The rules apply at ≤900px viewport width, which is correct responsive behavior.

**Severity:** N/A (not a real issue)

---

### F2 — `PUBLIC_BETTING_FORBIDDEN` Missing `买`/`卖`: **REAL, LOW** ✅

**Claim:** Spec section 1.4 forbids `买`, `卖`, `sell`, `buy` but code doesn't cover them.

**Evidence:**
- `PUBLIC_BETTING_FORBIDDEN` (line 106): has `投注建议`, `ROI`, `PnL`, `Sharpe`, `Kelly`, `仓位` — NO `买`/`卖`
- `_sanitize_public_text()` (lines 546-560): replaces `低估`, `高估`, `正期望` — NO `买`/`卖`
- Inline validation lists (lines 834, 1242): have `buy`, `sell`, `profit` (English) — NO Chinese `买`/`卖`
- CSV row 45 contains "买入" in reason field
- BUT: grep of `homepage.json` and `team-details.json` for "买入" returns **0 matches** — current data doesn't leak

**Root cause:** The sanitize function was designed to handle the most common betting terms from the CSV data. "买入"/"卖出" are less common and were not included. The inline validation lists use English "buy"/"sell" instead of Chinese.

**Danger level:** 🟢 LOW — not currently triggered by data
**Blast radius:** None currently — would only matter if CSV data changes
**Fix:** Add `"买": "持续看好"`, `"卖": "不再看好"` to `_sanitize_public_text()` replacements. Or add Chinese terms to `PUBLIC_BETTING_FORBIDDEN`.

---

### F3 — CI Does Not Run Unit Tests: **REAL, MEDIUM** ✅

**Claim:** `.github/workflows/ci.yml` doesn't run `python3 -m unittest`.

**Evidence:** `grep -n "unit-tests\|unittest\|test_build\|test_fetch" .github/workflows/ci.yml` returns **no matches**.

The CI runs: wiki audit/verify, sensitive file check, markdown lint, structure integrity — but NOT the Python unit tests. The `pages.yml` workflow runs `build_site_data.py` (which has internal validation) but not the test suite.

**Danger level:** 🟡 MEDIUM — regression bugs could merge without detection
**Blast radius:** The forbidden-term boundary tests (`assert_public_payload_clean`) are the primary defense against vendor/betting language leaking. Without CI enforcement, a code change could disable these checks silently.
**Fix:** Add a `unit-tests` job to `ci.yml`.

---

### F4 — `_validate_public_text_boundary()` Never Called at Runtime: **REAL, LOW** ✅

**Claim:** The function exists (line 562) but production validators use inline lists.

**Evidence:**
- `_validate_homepage_json()` (line 1224) uses inline `forbidden` list (line 1242)
- `_validate_team_details_json()` (line 815) uses inline `forbidden` list (line 834)
- `_validate_public_text_boundary()` (line 562) checks `PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN`
- Neither production validator calls `_validate_public_text_boundary()`

The inline lists are SMALLER than the canonical constants — missing `小米`, `投注建议`, `value bet`, `kimi` (lowercase).

**Mitigating factor:** Tests use `assert_public_payload_clean()` which checks the canonical constants. So the test suite catches what the runtime validators miss.

**Danger level:** 🟢 LOW — tests cover the gap
**Blast radius:** If someone adds a new forbidden term to the constants but not to the inline lists, the runtime validator won't catch it — but the test will.
**Fix:** Replace inline lists with `_validate_public_text_boundary()` calls.

---

### F5 — `_build_ai_perspectives` Doesn't Sanitize `faction`/`champion`: **REAL, LOW** ✅

**Claim:** Raw CSV values for `faction` and `champion` columns go directly into public output.

**Evidence:**
- Lines 590-591: `faction = row.get("faction", "").strip()` and `champion = row.get("champion", "").strip()` — no sanitize call
- Current factions: 数据派, 赔率派, 老球迷派, 玄学派, 主帅视角派, 伤病赛程派, 黑马派, 阵容年龄派, 心理抗压派, 建模派 — no forbidden terms
- Current champions: Chinese team names (西班牙, 法国, etc.) — no forbidden terms

**Danger level:** 🟢 LOW — current data safe
**Blast radius:** If a future CSV update introduces "Kimi" as a faction name or champion, it would leak into public JSON.
**Fix:** Add `faction = _sanitize_public_text(faction)` after line 590.

---

### F6 — `fetch_market_snapshot.py` Minimal Test Coverage: **REAL, LOW** ✅

**Claim:** Only 2 tests (happy path).

**Evidence:** `tests/test_fetch_market_snapshot.py` has 2 test methods:
- `test_extract_team_from_question` — regex happy path
- `test_build_snapshot_from_public_search_payload` — basic happy path

Missing: empty API response, malformed JSON, alias resolution, missing outcomes/prices.

**Danger level:** 🟢 LOW — plan explicitly scoped only these 2 tests
**Blast radius:** Edge cases in Polymarket API responses could cause silent failures
**Fix:** Add edge-case tests in follow-up iteration.

---

## Summary Table

| Finding | Real? | Severity | Currently Breaking? | Fix Priority |
|---------|-------|----------|-------------------|--------------|
| F1 CSS orphaned rules | ❌ FALSE POSITIVE | N/A | No | N/A |
| F2 Missing 买/卖 | ✅ Real | 🟢 Low | No (data doesn't trigger) | Next iteration |
| F3 CI no tests | ✅ Real | 🟡 Medium | No (but risk of regression) | Should fix |
| F4 Unused validator | ✅ Real | 🟢 Low | No (tests cover gap) | Next iteration |
| F5 Unsanitized faction/champion | ✅ Real | 🟢 Low | No (current data safe) | Next iteration |
| F6 Minimal test coverage | ✅ Real | 🟢 Low | No (plan scope) | Next iteration |

## Recommendations

1. **F3 is the only one worth fixing now** — add unit tests to CI. This is a 5-minute change with meaningful regression prevention.
2. F2, F4, F5 are low-risk and can be batched into a follow-up PR.
3. F1 is not a bug — no action needed.
4. F6 matches plan scope — optional follow-up.
