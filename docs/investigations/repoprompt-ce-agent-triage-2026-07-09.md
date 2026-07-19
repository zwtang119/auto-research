# RepoPrompt CE Agent Triage — 2026-07-09

## Summary
Three symptoms investigated against upstream issues #413 (App Translocation recovery) and #424 (CLI PATH hardening + no-space path migration). Only one symptom warrants a new upstream issue.

---

## Evidence Gathered

| Source | Finding |
|--------|---------|
| `gh api issues/413` | Fix targets `ManagedCLIPathPolicy.classifySymlink()` — stale translocated managed targets are now `.managedStale` (repaired), not `.unmanaged` (refused) |
| `gh api issues/424` | Fixes Codex startup delay, moves CE CLI links to `~/RepoPrompt`, grandfather-recognizes legacy/Classic paths, improves executable discovery diagnostics, adds Sentry breadcrumbs |
| `git log` local clone | #413 merged at v1.0.24 (c255548d); #424 merged at v1.0.26 (5bc088ef) |
| `/usr/local/bin/rp-cli` | → `/Applications/RepoPrompt CE.app/Contents/MacOS/repoprompt-mcp` ✅ valid |
| `discovery.json` | `"command": "/Applications/RepoPrompt CE.app/Contents/MacOS/repoprompt-mcp"` ✅ correct |
| Installed app bundle | CFBundleShortVersionString = **1.0.24** |
| `v1.0.26` tag | Contains merged fixes for both #413 and #424 |

---

## Per-Symptom Verdict

### (a) Symlink previously pointed at deleted `/Applications/RepoPrompt.app/` (old name migration drift)
**Verdict: ALREADY COVERED by #413**

The root cause is AppTranslocation creating a symlink to a randomized path, then the app moved to /Applications making it dangling. #413's `classifySymlink` fix explicitly handles this by recognizing stale translocated managed targets as `.managedStale` and repairing them. Current `/usr/local/bin/rp-cli` is valid and pointing correctly — the fix is working. **Do not file new issue.**

### (b) CE managed files (discovery.json, repoprompt_ce_cli) drift to AppTranslocation UUID paths
**Verdict: ALREADY COVERED by #413**

This is the exact symptom #413 was written to fix. `discovery.json` currently shows the correct `/Applications/` path, consistent with #413 having repaired the translocated state. **Do not file new issue.**

### (c) Installed CE binary is 1.0.24 but source tag v1.0.26 contains merged fixes for both #413 and #424 — stale bundle
**Verdict: NEW ISSUE WORTH FILING**

The installed app bundle is at 1.0.24; source is at 1.0.26. A stale bundle means:
- #413 fix is present (v1.0.24 has it), but user still hit translocation issues historically
- #424 fix is **absent** — user is on v1.0.24 but #424 landed in v1.0.26
- Root cause: the installed bundle was not refreshed after the v1.0.26 release, likely due to auto-update failure or manual install path confusion

**Recommended new issue**: "CE bundle version staleness — installed binary 1.0.24 but latest is 1.0.26, causing missing CLI PATH/diagnostics fixes". Tags: `bug`, `installer`, `auto-update`.

---

## Confidence

| Symptom | Confidence |
|---------|------------|
| (a) Symlink drift | **High** — exact match to #413 root cause |
| (b) CE files translocation | **High** — #413 is the exact fix |
| (c) Stale bundle | **Medium** — circumstantial (installed version vs source); needs user's confirmation of update mechanism failure |

---

## Output File
`/Users/tangzw119/Documents/GitHub/auto-research/docs/investigations/repoprompt-ce-agent-triage-2026-07-09.md`
