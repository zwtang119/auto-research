# Homepage Optimization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the GitHub Pages homepage into a plain-Chinese, data-driven World Cup path portal.

**Architecture:** Extend the existing Python static data builder to emit `site/data/homepage.json`, then render the homepage with vanilla HTML/CSS/JS from that local JSON. Keep external market data as a snapshot/missing state, not a browser API call.

**Tech Stack:** Python 3 stdlib, unittest, static HTML/CSS/JS, GitHub Pages-compatible files.

---

### Task 1: Homepage Data Contract

**Files:**
- Modify: `scripts/build_site_data.py`
- Modify: `tests/test_build_site_data.py`
- Create: `site/data/homepage.json`

- [x] Add failing unittest asserting `build_homepage_json()` returns summary, team teasers, obstacle distribution, baselines, public signal snapshots, and Chinese display labels.
- [x] Implement `build_homepage_json()` from existing team data and processed CSVs.
- [x] Write `homepage.json` in `main()`.
- [x] Run `python3 -m unittest discover -s tests -v`.

### Task 2: Homepage Structure and Rendering

**Files:**
- Modify: `site/index.html`
- Create: `site/js/homepage.js`

- [x] Replace the old hard-coded homepage with semantic sections: hero, choose-team, progress, obstacles, outside-view, method, update-log.
- [x] Add `site/js/homepage.js` to fetch local `data/homepage.json`, render charts/tables/cards, escape HTML, and handle missing states.
- [x] Ensure public copy uses plain Chinese, not English-heavy technical labels.

### Task 3: Homepage Visual System

**Files:**
- Modify: `site/css/portal.css`

- [x] Add responsive layout, source tags, team teasers, CSS bar charts, CSS matrix cells, external reference cards, and mobile rules.
- [x] Preserve existing teams page styling compatibility.

### Task 4: Verification

**Files:**
- Verify generated files and local site.

- [x] Run `python3 scripts/build_site_data.py`.
- [x] Run `python3 scripts/audit.py --root wiki/`.
- [x] Run `python3 scripts/verify.py --root wiki/`.
- [x] Run `python3 -m unittest discover -s tests -v`.
- [x] Start a local HTTP server and inspect desktop/mobile via browser automation.
