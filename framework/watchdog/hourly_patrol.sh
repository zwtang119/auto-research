#!/usr/bin/env bash
# L1 — Hourly patrol. Detects stale work loops and reports.
#
# Per Deli_AutoResearch §7, the guardian-only actions are:
#   - liveness-check
#   - restart
#   - nudge
#
# This script does liveness-check + nudge.  No write to progress.json, no
# on-behalf reporting.  All findings append to a patrol log.
#
# Install (hourly cron):
#     crontab -e
#     0 * * * * bash /Users/tangzw119/Documents/GitHub/auto-research/framework/watchdog/hourly_patrol.sh
#
# Logs to:
#     framework/watchdog/patrol.jsonl
set -euo pipefail

AUTO_ROOT="/Users/tangzw119/Documents/GitHub/auto-research"
HEARTBEAT_LOG="$AUTO_ROOT/framework/watchdog/heartbeat.jsonl"
PATROL_LOG="$AUTO_ROOT/framework/watchdog/patrol.jsonl"
STATE_GLOB="$AUTO_ROOT/papers/*/state/progress.json"
PORTFOLIO_STATE="$AUTO_ROOT/state/progress.json"
THRESHOLD_SECONDS="${WATCHDOG_STALE_THRESHOLD_SECONDS:-7200}"   # 2 hours
NOW_EPOCH=$(date +%s)
NOW_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)

mkdir -p "$(dirname "$PATROL_LOG")"
touch "$PATROL_LOG"

# Function: emit a patrol log line, dedup against the most recent
# matching (event, detail) line. DEDUP_WINDOW_SECONDS=43200 (12h) means
# the same alert fires at most twice per day, regardless of patrol
# cadence.
DEDUP_WINDOW_SECONDS="${PATROL_DEDUP_SECONDS:-43200}"

emit() {
  local level="$1"; shift
  local event="$1"; shift
  local detail="$1"; shift
  local extra="${1:-}"
  # Skip if same (event, detail) was emitted within dedup window.
  # Use jq -s (slurp) so JSONL streams are treated as arrays of objects.
  local last_ts=""
  if [ -f "$PATROL_LOG" ] && [ -s "$PATROL_LOG" ]; then
    last_ts=$(jq -rs --arg ev "$event" --arg det "$detail" \
                  '[.[] | select(.event==$ev and .detail==$det)] | last | .ts // empty' \
                  "$PATROL_LOG" 2>/dev/null || echo "")
  fi
  if [ -n "${last_ts:-}" ]; then
    local last_epoch=0
    last_epoch=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$last_ts" "+%s" 2>/dev/null || date -u -d "$last_ts" "+%s" 2>/dev/null || echo 0)
    if [ "${last_epoch:-0}" != "0" ]; then
      local delta=$((NOW_EPOCH - last_epoch))
      if [ "$delta" -lt "${DEDUP_WINDOW_SECONDS:-43200}" ]; then
        return 0
      fi
    fi
  fi
  local payload
  payload=$(jq -nc --arg ts "$NOW_ISO" --arg lvl "$level" --arg ev "$event" \
                    --arg det "$detail" --arg extra "$extra" \
                    '{ts:$ts,level:$lvl,event:$ev,detail:$det,extra:$extra}')
  echo "$payload" >> "$PATROL_LOG"
  echo "[$NOW_ISO] $level $event: $detail"
  return 0
}

# L1 rule: scan all papers/*/state/progress.json for last_seen staleness
for p in $STATE_GLOB; do
  [ -f "$p" ] || continue
  last_seen=$(jq -r '.last_seen // empty' "$p")
  if [ -z "$last_seen" ]; then
    # Treat as "never seen" — only nudge, don't alarm
    emit "info" "no_last_seen" "$p" "paper loop has not yet emitted L2 heartbeat"
    continue
  fi
  last_epoch=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$last_seen" "+%s" 2>/dev/null || \
              date -u -d "$last_seen" "+%s" 2>/dev/null || echo 0)
  if [ "$last_epoch" = "0" ]; then
    emit "warn" "bad_last_seen_format" "$p" "$last_seen"
    continue
  fi
  age=$((NOW_EPOCH - last_epoch))
  if [ "$age" -gt "$THRESHOLD_SECONDS" ]; then
    emit "warn" "stale_loop" "$p" "age_seconds=$age threshold=$THRESHOLD_SECONDS"
  fi
done

# Also check portfolio-level state
if [ -f "$PORTFOLIO_STATE" ]; then
  last_seen=$(jq -r '.last_seen // empty' "$PORTFOLIO_STATE")
  if [ -n "$last_seen" ]; then
    last_epoch=$(date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$last_seen" "+%s" 2>/dev/null || \
                date -u -d "$last_seen" "+%s" 2>/dev/null || echo 0)
    if [ "$last_epoch" != "0" ]; then
      age=$((NOW_EPOCH - last_epoch))
      [ "$age" -gt "$THRESHOLD_SECONDS" ] && \
        emit "warn" "stale_portfolio_loop" "$PORTFOLIO_STATE" "age_seconds=$age"
    fi
  fi
fi

# Heartbeat-log health: if file missing, alarm
if [ ! -f "$HEARTBEAT_LOG" ]; then
  emit "warn" "no_heartbeat_log" "$HEARTBEAT_LOG" "L2 layer may not be emitting"
fi

emit "info" "patrol_complete" "OK" "scanned_papers=$(echo $STATE_GLOB | wc -w)"
