# Investigation: Code Review Findings + Live Site Loading Failure

## Summary

The live site at https://zwtang119.github.io/cds4worldcup/ is **completely broken** — all sections show "正在加载..." loading messages because `homepage.js` has a JavaScript SyntaxError that prevents the entire script from executing. The root cause is a corrupted `escapeHtml()` function introduced by commit 253f02f.

## Symptoms

- Homepage shows 5 "正在加载..." messages instead of rendered content
- `正在加载球队入口...`, `正在加载当前进度...`, `正在加载夺冠难点...`, `正在加载外部参照...`, `正在加载更新记录...`
- Team detail pages also affected (team-detail.js has the same SyntaxError)

## Root Cause

### The `escapeHtml()` SyntaxError (P0 — Site-Breaking)

**Files:** `site/js/homepage.js:413`, `site/js/team-detail.js:285`

The frontend agent's edit corrupted the `escapeHtml()` function. The previous commit (40be253) had correct HTML entity replacements:

```javascript
// BEFORE (correct — from commit 40be253)
.replace(/&/g, "&amp;")
.replace(/</g, "&lt;")
.replace(/>/g, "&gt;")
.replace(/"/g, "&quot;")
.replace(/'/g, "&#039;");
```

Our commit (253f02f) corrupted them to:

```javascript
// AFTER (broken — from commit 253f02f)
.replace(/&/g, "&")      // no-op: replaces & with &
.replace(/</g, "<")       // no-op: replaces < with <
.replace(/>/g, ">")       // no-op: replaces > with >
.replace(/"/g, "")        // SYNTAX ERROR: three consecutive """ 
.replace(/'/g, "&#039;"); // only this one survived correctly
```

The `&quot;` → `""` transformation created three consecutive double-quote characters `"""`, which JavaScript cannot parse:
- First `"` opens the replacement string
- Second `"` closes it (empty string `""`)  
- Third `"` starts a NEW unterminated string
- The `)` is consumed into the string → `SyntaxError: missing ) after argument list`

**Verified with:** `node --check site/js/homepage.js` → SyntaxError at line 413

**Impact:** The entire `homepage.js` script fails to load. `initHomepage()` never executes. All loading placeholder messages remain visible. The catch error handler also never runs (it's part of the same broken script).

### How the Corruption Happened

The agent was tasked with updating `escapeHtml()` to allow "AI" and "Agent" in public text. The original intent was to stop replacing `AI` → `模型` and `Agent` → `模型样本`. But the agent also stripped the HTML entity names from the escape function's replacements, treating them as vendor terms to sanitize. The `&amp;`, `&lt;`, `&gt;`, `&quot;` strings were NOT vendor terms — they were the CORRECT escape sequences.

## Code Review Findings — Re-evaluated

### ✅ Confirmed Issues

| # | Finding | Severity | Real? | Notes |
|---|---------|----------|-------|-------|
| 1 | `escapeHtml()` SyntaxError | **P0-CRITICAL** | ✅ YES | Site-breaking. Corrupts both homepage.js and team-detail.js. |
| 2 | `escapeHtml()` no-op for `&`, `<`, `>` | **P0** | ✅ YES | Even after fixing SyntaxError, `&`/`<`/`>` replacements are no-ops → XSS vulnerability. |
| 3 | `"value"` sanitization overly broad | P1 | ✅ YES | Line 553 in build_site_data.py replaces ALL "value" occurrences. |
| 4 | `slugToTeamName()` only maps 4 teams | P1 | ✅ YES | External reference chart shows raw slugs for non-mapped teams. |
| 5 | `_validate_public_text_boundary()` never called | P1 | ✅ YES | Defined but unused at runtime. Inline checks have different forbidden lists. |
| 6 | `fetch_market_snapshot.py` minimal tests | P1 | ✅ YES | Only 2 happy-path tests. |

### ❌ Not Real Issues / Display Artifacts

| # | Finding | Verdict | Notes |
|---|---------|---------|-------|
| 7 | CSS missing @media wrapper | **Pre-existing** | The orphaned responsive rules existed BEFORE our commit. Not introduced by us. |
| 8 | Dot grid 60 vs spec 30 | P2 (cosmetic) | The code caps at 60, spec says 30. Minor visual difference. |
| 9 | Italy 0% probability | P2 (data) | Valid data — Italy didn't qualify. Display concern, not a bug. |
| 10 | Internal "kimi" variable names | P2 (cleanup) | Internal only, doesn't affect public output. |

### 🔄 Severity Adjustments

- Finding #1 (SyntaxError): **Upgraded from P0 to P0-CRITICAL** — this is not just an XSS risk, it's a site-breaking parse error
- Finding #2 (no-op escapes): **Stays P0** — XSS vulnerability even after SyntaxError is fixed
- Finding #5 (unused validation): **Downgraded from P1 to P2** — the inline checks DO catch vendor terms, just with a different list

## Recommended Fixes

### Fix 1: Restore `escapeHtml()` in both JS files (CRITICAL)

Replace the broken escapeHtml in both `site/js/homepage.js` and `site/js/team-detail.js`:

```javascript
function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
```

This restores the original correct implementation from commit 40be253.

### Fix 2: Fix `"value"` sanitization (P1)

In `scripts/build_site_data.py`, change the `"value"` replacement to only match betting-context phrases, not all occurrences of "value".

### Fix 3: Extend `slugToTeamName()` (P1)

Add all 48 team slugs to the map, or build the lookup from the loaded data.

## Investigation Log

### Phase 1 - SyntaxError Discovery
**Hypothesis:** The loading failure is caused by a JavaScript error preventing script execution
**Findings:** `node --check` confirms SyntaxError at line 413 in homepage.js and line 285 in team-detail.js
**Evidence:** `.replace(/"/g, """)` has three consecutive double-quote characters
**Conclusion:** Confirmed — this is the root cause of the loading failure

### Phase 2 - Escape Function Comparison
**Hypothesis:** The escapeHtml function was corrupted by our commit
**Findings:** Previous commit (40be253) had correct `&amp;`/`&lt;`/`&gt;`/`&quot;` replacements. Our commit (253f02f) stripped the entity names.
**Evidence:** `git show 40be253:site/js/homepage.js | grep -A 8 "function escapeHtml"` shows correct code
**Conclusion:** Confirmed — our commit introduced the corruption

### Phase 3 - Live Site Verification
**Hypothesis:** The live site is serving the broken code
**Findings:** `curl -s https://zwtang119.github.io/cds4worldcup/js/homepage.js | node --check /dev/stdin` confirms SyntaxError on live site
**Evidence:** Live homepage-data.js has `build_date: 2026-06-11` and includes ai_perspectives data. Live homepage.js has the broken escapeHtml.
**Conclusion:** Confirmed — the GitHub Pages deployment completed and is serving broken code

### Phase 4 - Code Review Re-evaluation
**Hypothesis:** Some review findings may be display artifacts
**Findings:** escapeHtml SyntaxError is REAL and CRITICAL. The "no-op" issue is also real but secondary to the SyntaxError. CSS orphaned rules are pre-existing.
**Evidence:** node --check, hex dump analysis, git diff comparison
**Conclusion:** 6 findings confirmed, 1 upgraded to CRITICAL, 2 downgraded, 1 pre-existing

## Preventive Measures

1. **Always run `node --check` on JS files** before committing — this would have caught the SyntaxError
2. **Don't let agents edit escape/security functions** without human review — these are critical code paths
3. **Add a CI check** that validates JS syntax: `node --check site/js/*.js`
4. **Test the actual rendered page** after changes, not just the data pipeline — the Python tests passed but the site was broken
