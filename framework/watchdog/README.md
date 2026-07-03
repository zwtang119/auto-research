# Watchdog (Deli §7)

Three-tier guardian per `Deli_AutoResearch §7` and `FRAMEWORK-RULES.md R6`.

| Layer | Form | Status (2026-07-03) | How to run |
|-------|------|---------------------|------------|
| L0    | resident shell guard | **DESIGN ONLY** (TODO); would require a wrapper process or external monitor. macOS `launchd` `KeepAlive` could fill this slot but was not configured today. | N/A |
| L1    | hourly cron | ✅ **ENABLED** | `bash framework/watchdog/hourly_patrol.sh` (read `hourly_patrol.sh` header for `crontab -e` line). |
| L2    | business-loop self-update | ✅ **ENABLED** | First-action call: `from l2_callback import heartbeat; heartbeat(state_file=Path("papers/<N>/state/progress.json"))` |

## L0 (TODO, not deployed)

A resident daemon that spawns a headless agent if heartbeat stale > 2h.
On macOS the natural slot is `~/Library/LaunchAgents/com.auto-research.watchdog.plist`
with `KeepAlive=true` and a 2h interval. **Not deployed today** because:

1. User explicitly accepted the heartbeat opt-out for Day-1 M2.
2. macOS LaunchAgent deploy requires a one-time `launchctl load -w` that the
   user must invoke — out of session scope.
3. L2 + L1 alone catch the most common failure modes (silent stall).

If/when L0 is needed, see `hourly_patrol.sh` for the contract.

## L1 (hourly_patrol.sh)

Cron-installed script that scans `papers/*/state/progress.json` for
`last_seen` staleness (>2h default, override via
`$WATCHDOG_STALE_THRESHOLD_SECONDS`). Detects:

- `stale_loop` — paper state file's `last_seen` exceeds the threshold.
- `stale_portfolio_loop` — `state/progress.json` (root level) is stale.
- `no_last_seen` — first-run state file before any L2 heartbeat.
- `bad_last_seen_format` — malformed ISO timestamp.
- `no_heartbeat_log` — `framework/watchdog/heartbeat.jsonl` missing entirely.

Outputs a JSONL line per finding to `framework/watchdog/patrol.jsonl`.

To install (one-time, per session):

```bash
crontab -e
# add this line:
0 * * * * bash /Users/tangzw119/Documents/GitHub/auto-research/framework/watchdog/hourly_patrol.sh
```

To trigger once for smoke testing:

```bash
bash framework/watchdog/hourly_patrol.sh
# inspect:
tail -10 framework/watchdog/patrol.jsonl
```

## L2 (business-loop heartbeat)

The contract: any script that claims "I am running" must call
`heartbeat()` as its first action. Currently adopted in:

- `papers/p12-judge-calibration/experiments/run_leaked_baseline.py` —
  does NOT yet call `heartbeat()`; an M3 work item adds the call.

To enable L2 in P12's M2 runner, the runner would prepend:

```python
import sys
sys.path.insert(0, str(AUTO_RESEARCH_ROOT / "framework" / "watchdog"))
from l2_callback import heartbeat
heartbeat(
    state_file=Path("papers/p12-judge-calibration/state/progress.json"),
    source="p12_M2",
    detail="leaked_baseline_runner_started",
)
```

L2 currently lives only as a documented primitive — adoption across
paper scripts is a Day-2 task.

## Heartbeat log (`heartbeat.jsonl`)

JSONL stream of all heartbeats, written by L2 callers. Cleared/archived
monthly. Example line:

```json
{"ts":"2026-07-03T16:00:00Z","source":"p12_M2","level":"liveness",
 "action":"heartbeat","detail":"leaked_baseline_runner_started"}
```

## Patrol log (`patrol.jsonl`)

JSONL stream of all L1 patrol findings. Cleared/archived monthly.
Example line (a stale loop):

```json
{"ts":"2026-07-03T16:00:01Z","level":"warn","event":"stale_loop",
 "detail":"papers/p12-judge-calibration/state/progress.json",
 "extra":"age_seconds=7500 threshold=7200"}
```

## Why three layers?

The full `Deli §7` rationale: any single layer dying can be detected and
recovered by another. L0 detects L1 dies; L1 detects L2 dies; L2 detects
business-loop dies. Today's deployment is **L1 + L2** (skips L0).
