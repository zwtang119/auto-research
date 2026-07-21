"""
Knockout bracket path graph builder for CDS pipeline (WI-PAN.4).

Parses ``site/data/schedule.json``'s ``knockout`` section and builds a
complete bracket DAG showing every team's possible path from group stage
through to the final.

Three slot reference types are resolved:

1. **Position + Group**: ``1A`` = group A winner, ``2B`` = group B runner-up
2. **Composite Third-Place Sets**: ``3ABCDF`` = best 3rd-placed from {A,B,C,D,F}
3. **Winner/Loser Propagation**: ``W73`` = winner of KO73, ``RU101`` = loser of KO101
"""

from __future__ import annotations

import csv
import json
import re
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# Canonical round ordering for deterministic sort order.
ROUND_ORDER: dict[str, int] = {
    "round_of_32": 0,
    "round_of_16": 1,
    "quarterfinal": 2,
    "semifinal": 3,
    "third_place": 4,
    "final": 5,
}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class PathNode:
    """A single match node in a team's knockout bracket path.

    Attributes
    ----------
    round :
        Knockout round identifier (``"round_of_32"``, ``"round_of_16"``,
        ``"quarterfinal"``, ``"semifinal"``, ``"final"``, ``"third_place"``).
    match_id :
        Match identifier from schedule.json (e.g. ``"KO75"``).
    opponent_slot :
        Human-readable description of who the team could face.
    is_deterministic :
        ``True`` when the opponent is fixed by group position alone
        (e.g. ``"2B"``); ``False`` when it depends on match results or
        third-place rankings.
    """

    round: str
    match_id: str
    opponent_slot: str
    is_deterministic: bool


# ---------------------------------------------------------------------------
# Slot parsing
# ---------------------------------------------------------------------------

_SLOT_RE_WINNER = re.compile(r"^W(\d+)$")
_SLOT_RE_LOSER = re.compile(r"^RU(\d+)$")
_SLOT_RE_THIRD = re.compile(r"^3([A-L]+)$")
_SLOT_RE_POS = re.compile(r"^([12])([A-L])$")


def parse_slot(slot: str) -> dict:
    """Parse a slot reference string into a typed descriptor.

    Returns one of:

    * ``{"type": "winner", "match_num": int}``
    * ``{"type": "loser",  "match_num": int}``
    * ``{"type": "third_place", "pool_groups": list[str]}``
    * ``{"type": "position_group", "position": int, "group": str}``

    Raises :class:`ValueError` for unrecognised formats.
    """
    m = _SLOT_RE_WINNER.match(slot)
    if m:
        return {"type": "winner", "match_num": int(m.group(1))}

    m = _SLOT_RE_LOSER.match(slot)
    if m:
        return {"type": "loser", "match_num": int(m.group(1))}

    m = _SLOT_RE_THIRD.match(slot)
    if m:
        return {"type": "third_place", "pool_groups": list(m.group(1))}

    m = _SLOT_RE_POS.match(slot)
    if m:
        return {
            "type": "position_group",
            "position": int(m.group(1)),
            "group": m.group(2),
        }

    raise ValueError(f"Unknown slot format: {slot}")


def _is_deterministic(slot: str) -> bool:
    """True when the opponent is fixed by group position alone."""
    return parse_slot(slot)["type"] == "position_group"


def _short_slot(slot: str) -> str:
    """Compact slot label for inline descriptions."""
    info = parse_slot(slot)
    if info["type"] == "third_place":
        return f"3rd({''.join(info['pool_groups'])})"
    return slot


def describe_slot(slot: str, match_lookup: dict[str, dict]) -> str:
    """Return a human-readable description of a slot reference.

    Parameters
    ----------
    slot :
        Raw slot string from schedule.json (e.g. ``"W75"``, ``"3ABCDF"``).
    match_lookup :
        ``{match_id: match_dict}`` for resolving winner/loser references.
    """
    info = parse_slot(slot)

    if info["type"] == "position_group":
        label = "winner" if info["position"] == 1 else "runner-up"
        return f"{label} of Group {info['group']}"

    if info["type"] == "third_place":
        groups = ",".join(info["pool_groups"])
        return f"best 3rd-placed team from Groups {groups}"

    if info["type"] == "winner":
        src_id = f"KO{info['match_num']}"
        src = match_lookup.get(src_id)
        if src:
            h = _short_slot(src["slot_home"])
            a = _short_slot(src["slot_away"])
            return f"winner of {src_id} ({h} vs {a})"
        return f"winner of {src_id}"

    if info["type"] == "loser":
        src_id = f"KO{info['match_num']}"
        src = match_lookup.get(src_id)
        if src:
            return f"loser of {src_id} ({src['round_label']})"
        return f"loser of {src_id}"

    return slot  # pragma: no cover


# ---------------------------------------------------------------------------
# Forward-tracing through the bracket
# ---------------------------------------------------------------------------


def _trace_from_entry(
    entry_match_id: str,
    entry_side: str,
    knockout: list[dict],
    match_lookup: dict[str, dict],
    collected: list[tuple[str, str]],
) -> None:
    """Walk forward from an entry match, collecting *(match_id, team_side)* pairs.

    Follows winner-propagation edges at every round and loser-propagation
    from semifinal matches to the third-place match.  The bracket is a tree
    (no cycles), so a simple stack-based DFS suffices.

    Parameters
    ----------
    entry_match_id :
        The R32 match the team enters (e.g. ``"KO79"``).
    entry_side :
        ``"slot_home"`` or ``"slot_away"`` — which side of the match the team occupies.
    knockout :
        Full list of knockout match dicts from schedule.json.
    match_lookup :
        ``{match_id: match_dict}`` index.
    collected :
        Append-only list to receive ``(match_id, team_side)`` tuples.
    """
    stack: list[tuple[str, str]] = [(entry_match_id, entry_side)]
    visited: set[str] = set()

    while stack:
        cur_id, cur_side = stack.pop()
        if cur_id in visited:
            continue
        visited.add(cur_id)

        collected.append((cur_id, cur_side))

        cur_match = match_lookup[cur_id]
        num = cur_id.replace("KO", "")
        w_ref = f"W{num}"
        ru_ref = f"RU{num}"

        # Find downstream matches that reference winner or loser of cur
        for m in knockout:
            if m["match_id"] == cur_id:
                continue
            for side in ("slot_home", "slot_away"):
                if m[side] == w_ref:
                    # Winner propagation — team advances
                    stack.append((m["match_id"], side))
                elif m[side] == ru_ref and cur_match["round"] == "semifinal":
                    # SF loser → 3rd place match (terminal, no further tracing)
                    collected.append((m["match_id"], side))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_bracket_paths(
    schedule_path: str = "site/data/schedule.json",
    third_place_map_path: Optional[str] = "config/third_place_mapping.json",
) -> dict[str, list[PathNode]]:
    """Build knockout bracket paths for all 48 teams.

    Parameters
    ----------
    schedule_path :
        Path to the schedule JSON (must contain a ``"knockout"`` list).
    third_place_map_path :
        Optional path to a third-place mapping config.  When the file is
        absent the bracket is still built — third-place entry points are
        inferred from the slot references in the schedule itself.

    Returns
    -------
    dict[str, list[PathNode]]
        ``{team_name: [PathNode, ...]}`` for every team in the registry.
        Each list contains all possible matches across all entry points
        (1st, 2nd, or 3rd in their group).

    Notes
    -----
    * The same ``match_id`` may appear more than once when the team can
      reach it from different bracket halves (and thus face different
      opponents).  Deduplication is by ``(match_id, team_side)``.
    * Third-place entry points are identified by parsing the pool groups
      encoded in the slot strings (e.g. ``"3ABCDF"`` → groups A,B,C,D,F),
      so the optional mapping config is **not** required for enumeration.
    """
    schedule_path = Path(schedule_path)

    # -- Load schedule -------------------------------------------------------
    with open(schedule_path) as fh:
        schedule = json.load(fh)

    knockout: list[dict] = schedule["knockout"]
    match_lookup: dict[str, dict] = {m["match_id"]: m for m in knockout}

    # -- Load team registry --------------------------------------------------
    registry_path = (
        schedule_path.resolve().parent.parent.parent
        / "data"
        / "processed"
        / "team_registry.csv"
    )
    team_group: dict[str, str] = {}
    if registry_path.exists():
        with open(registry_path) as fh:
            for row in csv.DictReader(fh):
                team_group[row["canonical_team"]] = row["group"]
    else:
        warnings.warn(
            f"Team registry not found at {registry_path}; returning empty paths.",
            stacklevel=2,
        )
        return {}

    # -- (Optional) third-place mapping -------------------------------------
    # The mapping config is not required for bracket enumeration — we infer
    # third-place entry points directly from the schedule slot strings.
    # Loaded here for potential use by downstream consumers.
    if third_place_map_path:
        _tp_path = Path(third_place_map_path)
        # File may not exist yet; that's fine.
        # Future consumers can load it via json.load() when needed.

    # -- Build slot → [(match_id, side)] reverse index -----------------------
    slot_index: dict[str, list[tuple[str, str]]] = {}
    for m in knockout:
        for side in ("slot_home", "slot_away"):
            slot_index.setdefault(m[side], []).append((m["match_id"], side))

    # -- Per-team path construction ------------------------------------------
    results: dict[str, list[PathNode]] = {}

    for team, group in team_group.items():
        raw: list[tuple[str, str]] = []  # (match_id, team_side)

        # Entry path 1: group winner → slot "1{group}"
        for mid, side in slot_index.get(f"1{group}", []):
            _trace_from_entry(mid, side, knockout, match_lookup, raw)

        # Entry path 2: group runner-up → slot "2{group}"
        for mid, side in slot_index.get(f"2{group}", []):
            _trace_from_entry(mid, side, knockout, match_lookup, raw)

        # Entry path 3: third-place qualifier — find all third-place slots
        # whose pool includes this team's group.
        for slot, entries in slot_index.items():
            info = parse_slot(slot)
            if info["type"] == "third_place" and group in info["pool_groups"]:
                for mid, side in entries:
                    _trace_from_entry(mid, side, knockout, match_lookup, raw)

        # Deduplicate by (match_id, team_side) — same match from the same
        # side implies the same opponent context.
        seen: set[tuple[str, str]] = set()
        nodes: list[PathNode] = []
        for mid, side in raw:
            key = (mid, side)
            if key in seen:
                continue
            seen.add(key)

            match = match_lookup[mid]
            opp_side = "slot_away" if side == "slot_home" else "slot_home"
            opp_slot = match[opp_side]

            nodes.append(
                PathNode(
                    round=match["round"],
                    match_id=mid,
                    opponent_slot=describe_slot(opp_slot, match_lookup),
                    is_deterministic=_is_deterministic(opp_slot),
                )
            )

        # Deterministic sort: round order first, then match_id
        nodes.sort(key=lambda n: (ROUND_ORDER.get(n.round, 99), n.match_id))
        results[team] = nodes

    return results


# ---------------------------------------------------------------------------
# CLI smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    paths = build_bracket_paths()
    print(f"Bracket paths built for {len(paths)} teams\n")

    # Show a sample team's path
    for team in ("Mexico", "Argentina", "England"):
        nodes = paths.get(team, [])
        if not nodes:
            print(f"--- {team}: no path nodes ---\n")
            continue
        print(f"--- {team} ({len(nodes)} possible matches) ---")
        for n in nodes:
            det = "DET" if n.is_deterministic else "COND"
            print(f"  {n.round:16s} {n.match_id}  vs {n.opponent_slot}  [{det}]")
        print()
