#!/usr/bin/env bash
# Install the L1 hourly patrol as a user-level crontab entry.
#
# Idempotent: re-running replaces the existing auto-research-watchdog line.
# Does NOT overwrite unrelated crontab entries.
set -euo pipefail

AUTO_ROOT="/Users/tangzw119/Documents/GitHub/auto-research"
SCRIPT="$AUTO_ROOT/framework/watchdog/hourly_patrol.sh"
MARKER="auto-research-watchdog"
CRON_LINE="0 * * * * bash $SCRIPT # $MARKER"

if [ ! -f "$SCRIPT" ]; then
  echo "FATAL: $SCRIPT not found" >&2
  exit 2
fi
chmod +x "$SCRIPT"

TMP=$(mktemp)
trap "rm -f $TMP" EXIT
crontab -l > "$TMP" 2>/dev/null || true
# Remove any existing auto-research-watchdog line
grep -v "$MARKER" "$TMP" > "$TMP.out" || true
mv "$TMP.out" "$TMP"
# Append new line
echo "$CRON_LINE" >> "$TMP"
crontab "$TMP"

echo "Installed crontab line:"
echo "  $CRON_LINE"
echo
echo "To verify:"
echo "  crontab -l | grep auto-research-watchdog"
echo
echo "To uninstall:"
echo "  crontab -l | grep -v auto-research-watchdog | crontab -"
