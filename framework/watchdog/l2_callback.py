#!/usr/bin/env python3
"""L2 — Business-loop heartbeat. Update self last_seen as first action.

Per Deli_AutoResearch §7 / FRAMEWORK-RULES.md R6, this is the
"first action of every callback updates its own `last_seen`" rule.

Usage:
    import sys; sys.path.insert(0, ".../auto-research/framework/watchdog")
    from l2_callback import heartbeat
    heartbeat()                                                 # first thing any business loop does
    heartbeat(state_file=Path("papers/<N>/state/progress.json"))    # explicit target

Two-tier implementation:
1. update_progress_last_seen() — updates any progress.json-like state file
2. update_heartbeat_log()       — appends to framework/watchdog/heartbeat.jsonl
                                 which is the L1 patrol's signal source
"""
from __future__ import annotations
import datetime as dt
import json
import re
import sys
from pathlib import Path

AUTO_RESEARCH_ROOT = Path(__file__).resolve().parent.parent.parent

DEFAULT_HEARTBEAT_LOG = AUTO_RESEARCH_ROOT / "framework" / "watchdog" / "heartbeat.jsonl"


def _now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# Heartbeat log retention. Archive to .<ts>.log.gz when file exceeds
# this many bytes; default 5 MiB.
HEARTBEAT_ROTATE_BYTES = 5 * 1024 * 1024


def update_progress_last_seen(state_file: Path) -> None:
    """Set `last_seen` field on a progress.json (idempotent; creates if absent).

    Uses atomic write (tempfile + os.replace) so a process death
    mid-write cannot corrupt the JSON. No-op if file does not exist
    or is not a JSON object.
    """
    import os
    import tempfile

    if not state_file.exists():
        return
    try:
        data = json.loads(state_file.read_text())
    except json.JSONDecodeError:
        return
    if not isinstance(data, dict):
        return
    data["last_seen"] = _now_iso()
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    # Atomic write: temp file in same dir, then os.replace.
    fd, tmp = tempfile.mkstemp(prefix=".lastseen.", dir=str(state_file.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tmp, state_file)
    except Exception:
        # Best-effort cleanup of leftover temp file.
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def _maybe_rotate(log_path: Path, max_bytes: int = HEARTBEAT_ROTATE_BYTES) -> None:
    """Archive `log_path` if it exceeds max_bytes. Archives to
    `log_path.parent/<basename>-<ts>.log` and starts fresh.
    """
    if not log_path.exists():
        return
    size = log_path.stat().st_size
    if size <= max_bytes:
        return
    ts = _now_iso().replace(":", "").replace("-", "")
    archive = log_path.with_name(f"{log_path.name}-{ts}.log")
    log_path.rename(archive)


def update_heartbeat_log(line: dict, log_path: Path = DEFAULT_HEARTBEAT_LOG) -> None:
    """Append a heartbeat line. L1 patrol scans this file for staleness.

    Will auto-rotate the log when it exceeds HEARTBEAT_ROTATE_BYTES.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    _maybe_rotate(log_path)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")


def heartbeat(state_file: Path | None = None,
              source: str = "unknown",
              detail: str = "",
              log_path: Path = DEFAULT_HEARTBEAT_LOG) -> None:
    """Update both a target progress.json (if given) and the heartbeat log.

    Typical use:
        heartbeat(state_file=Path("papers/<N>-<topic>/state/progress.json"),
                  source=f"{paper_code}_M{milestone}")
    """
    now = _now_iso()
    if state_file is not None:
        update_progress_last_seen(state_file)
    update_heartbeat_log({
        "ts": now,
        "source": source,
        "level": "liveness",
        "action": "heartbeat",
        "detail": detail,
    }, log_path=log_path)


if __name__ == "__main__":
    # Smoke test
    arg_state = sys.argv[1] if len(sys.argv) > 1 else None
    sfp = Path(arg_state) if arg_state else None
    heartbeat(state_file=sfp, source="cli_smoke", detail="manual run")
    print(f"heartbeat recorded at {DEFAULT_HEARTBEAT_LOG}")
