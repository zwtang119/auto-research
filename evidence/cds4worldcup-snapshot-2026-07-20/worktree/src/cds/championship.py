"""Championship path conditional probability engine (CDS Layer 2).

Computes per-team championship probabilities by walking the knockout bracket
from R32 through the Final, using Elo-based Bradley-Terry head-to-head
probabilities at each round.

Key formula:  P(i beats j) = elo_i / (elo_i + elo_j)
where elo_i is the Bradley-Terry parameter from ``elo-proxy.json``.

For third-place composite slots, the opponent is probability-weighted across
candidate groups' most likely 3rd-place teams.  For winner/loser propagation
slots (W73, RU101, etc.), the expected opponent Elo is computed from all
teams that could reach that match position.
"""

from __future__ import annotations

import json
import math
import re
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import csv

from src.cds.knockout_bracket import (
    ROUND_ORDER,
    PathNode,
    build_bracket_paths,
    parse_slot,
)

# Re-export round order for convenience
ROUND_ORDER_MAP = ROUND_ORDER

# Team name → Chinese name mapping
TEAM_NAME_ZH = {
    "Algeria": "阿尔及利亚", "Argentina": "阿根廷", "Australia": "澳大利亚",
    "Austria": "奥地利", "Belgium": "比利时", "Bosnia and Herzegovina": "波黑",
    "Brazil": "巴西", "Canada": "加拿大", "Cape Verde": "佛得角",
    "Colombia": "哥伦比亚", "Croatia": "克罗地亚", "Curaçao": "库拉索",
    "Czech Republic": "捷克", "Côte d'Ivoire": "科特迪瓦",
    "DR Congo": "刚果民主共和国", "Ecuador": "厄瓜多尔", "Egypt": "埃及",
    "England": "英格兰", "France": "法国", "Germany": "德国",
    "Ghana": "加纳", "Haiti": "海地", "Iran": "伊朗", "Iraq": "伊拉克",
    "Japan": "日本", "Jordan": "约旦", "Mexico": "墨西哥",
    "Morocco": "摩洛哥", "Netherlands": "荷兰", "New Zealand": "新西兰",
    "Norway": "挪威", "Panama": "巴拿马", "Paraguay": "巴拉圭",
    "Portugal": "葡萄牙", "Qatar": "卡塔尔", "Saudi Arabia": "沙特阿拉伯",
    "Scotland": "苏格兰", "Senegal": "塞内加尔", "South Africa": "南非",
    "South Korea": "韩国", "Spain": "西班牙", "Sweden": "瑞典",
    "Switzerland": "瑞士", "Tunisia": "突尼斯", "Turkey": "土耳其",
    "United States": "美国", "Uruguay": "乌拉圭", "Uzbekistan": "乌兹别克斯坦",
}


def team_zh(name: str) -> str:
    """Return Chinese name for a team, falling back to original if not found."""
    return TEAM_NAME_ZH.get(name, name)

# Rounds that count toward championship (exclude third_place)
CHAMPIONSHIP_ROUNDS = [
    "round_of_32",
    "round_of_16",
    "quarterfinal",
    "semifinal",
    "final",
]

# Slot regexes (duplicated from knockout_bracket to avoid tight coupling)
_RE_WINNER = re.compile(r"^W(\d+)$")
_RE_LOSER = re.compile(r"^RU(\d+)$")
_RE_THIRD = re.compile(r"^3([A-L]+)$")
_RE_POS = re.compile(r"^([12])([A-L])$")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class PathProbability:
    """Per-round probability node for a single bracket path."""

    round: str
    match_id: str
    opponent_slot: str
    opponent_team: Optional[str]
    conditional_win_prob: float
    cumulative_prob: float
    probability_source: str = "elo_poisson"


@dataclass
class TeamChampionship:
    """Championship analysis result for one team."""

    team: str
    group: str
    championship_prob: float
    championship_path_count: int
    dominant_path_pattern: str
    dominant_failure_node: str
    bracket_dependency: str
    black_swan_dependency: str = "not_assessed"
    penalty_dependency: str = "not_assessed"
    injury_sensitivity: str = "not_assessed"
    simulation_status: str = "run_complete"
    path_nodes: list[PathProbability] = field(default_factory=list)
    simulation_meta: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Elo / Bradley-Terry helpers
# ---------------------------------------------------------------------------


def load_elo_params(path: Path) -> dict[str, float]:
    """Load Elo Bradley-Terry parameters from elo-proxy.json.

    Returns {canonical_team_name: bt_param}.
    The file uses slug names (e.g. "côte-d'ivoire") which we map to
    canonical names via a normalisation step.
    """
    with open(path) as f:
        data = json.load(f)

    raw: dict[str, float] = data.get("teams", {})
    # Normalise keys: slug → canonical
    return {_slug_to_canonical(k): v for k, v in raw.items()}


def load_qualification_probs(path: Path) -> dict[str, dict]:
    """Load qualification probabilities from cds_qualification.json.

    Returns {team: {qual_prob, position_probs: {p_1st, p_2nd, p_3rd, p_4th}, group}}.
    """
    with open(path) as f:
        data = json.load(f)

    result = {}
    for t in data.get("teams", []):
        result[t["team"]] = {
            "qual_prob": t["qual_prob"],
            "position_probs": t.get("position_probs", {}),
            "group": t.get("group", ""),
            "third_place_qual_prob": t.get("third_place_qual_prob", 0.0),
        }
    return result


# ---------------------------------------------------------------------------
# Slot → opponent Elo resolution
# ---------------------------------------------------------------------------


def _slot_to_entry_matches(
    slot: str,
) -> list[tuple[str, str]]:
    """Map a bracket slot to potential (match_id, side) entry points.

    Returns list of (match_id, "home"/"away") tuples.
    For position+group slots like "1A", returns the R32 matches where that
    slot appears.
    """
    # This is resolved by looking at the bracket — handled in the main loop
    return []


def _resolve_opponent_elo(
    slot: str,
    team: str,
    elo_params: dict[str, float],
    team_group: str,
    qual_probs: dict[str, dict],
    match_lookup: dict[str, dict],
    bracket_paths: dict[str, list[PathNode]],
    third_place_map: dict,
    cache: dict,
) -> tuple[float, Optional[str]]:
    """Resolve the expected opponent Elo and name for a bracket slot.

    Returns (expected_opponent_elo, most_likely_opponent_name).
    """
    info = parse_slot(slot)

    if info["type"] == "position_group":
        return _resolve_position_group(
            info["position"], info["group"], team, elo_params, qual_probs
        )

    if info["type"] == "third_place":
        return _resolve_third_place_slot(
            info["pool_groups"], team, team_group, elo_params, qual_probs, third_place_map
        )

    if info["type"] in ("winner", "loser"):
        return _resolve_propagation_slot(
            info["type"], info["match_num"], team, elo_params, qual_probs,
            match_lookup, bracket_paths, third_place_map, cache,
        )

    # Fallback
    avg_elo = sum(elo_params.values()) / max(len(elo_params), 1)
    return avg_elo, None


def _resolve_position_group(
    position: int,
    group: str,
    team: str,
    elo_params: dict[str, float],
    qual_probs: dict[str, dict],
) -> tuple[float, Optional[str]]:
    """Resolve opponent for a deterministic position+group slot."""
    best_team = None
    best_prob = -1.0

    for tname, tdata in qual_probs.items():
        if tname == team:
            continue
        if tdata.get("group") != group:
            continue
        pos_key = f"p_{position}{'st' if position == 1 else 'nd' if position == 2 else 'rd' if position == 3 else 'th'}"
        prob = tdata.get("position_probs", {}).get(pos_key, 0.0)
        if prob > best_prob:
            best_prob = prob
            best_team = tname

    if best_team and best_team in elo_params:
        return elo_params[best_team], best_team

    # Fallback: average of all teams in group
    group_elos = [
        elo_params[t]
        for t, d in qual_probs.items()
        if d.get("group") == group and t != team and t in elo_params
    ]
    if group_elos:
        return sum(group_elos) / len(group_elos), None

    avg = sum(elo_params.values()) / max(len(elo_params), 1)
    return avg, None


def _resolve_third_place_slot(
    pool_groups: list[str],
    team: str,
    team_group: str,
    elo_params: dict[str, float],
    qual_probs: dict[str, dict],
    third_place_map: dict,
) -> tuple[float, Optional[str]]:
    """Resolve opponent for a third-place composite slot.

    Probability-weight across candidate groups' most likely 3rd-place teams.
    """
    # Collect candidate teams: those most likely to finish 3rd in each pool group
    candidates: list[tuple[str, float, float]] = []  # (team, p_3rd, elo)

    for g in pool_groups:
        if g == team_group:
            continue  # Can't face team from own group in this slot
        best_3rd = None
        best_p3 = 0.0
        for tname, tdata in qual_probs.items():
            if tname == team:
                continue
            if tdata.get("group") != g:
                continue
            p3 = tdata.get("position_probs", {}).get("p_3rd", 0.0)
            if p3 > best_p3:
                best_p3 = p3
                best_3rd = tname
        if best_3rd and best_3rd in elo_params:
            candidates.append((best_3rd, best_p3, elo_params[best_3rd]))

    if not candidates:
        # Fallback to all teams in pool groups
        pool_elos = [
            elo_params[t]
            for t, d in qual_probs.items()
            if d.get("group") in pool_groups and t != team and t in elo_params
        ]
        avg = sum(pool_elos) / max(len(pool_elos), 1) if pool_elos else (
            sum(elo_params.values()) / max(len(elo_params), 1)
        )
        return avg, None

    # Probability-weighted expected Elo
    total_weight = sum(c[1] for c in candidates)
    if total_weight == 0:
        total_weight = 1.0

    expected_elo = sum(c[1] * c[2] for c in candidates) / total_weight
    most_likely = max(candidates, key=lambda c: c[1])

    return expected_elo, most_likely[0]


def _resolve_propagation_slot(
    prop_type: str,  # "winner" or "loser"
    match_num: int,
    team: str,
    elo_params: dict[str, float],
    qual_probs: dict[str, dict],
    match_lookup: dict[str, dict],
    bracket_paths: dict[str, list[PathNode]],
    third_place_map: dict,
    cache: dict,
) -> tuple[float, Optional[str]]:
    """Resolve expected opponent for a winner/loser propagation slot.

    Uses the bracket structure to find all teams that could reach this
    match position, then computes expected Elo.
    """
    src_id = f"KO{match_num}"

    # Check cache — include team to avoid cross-team cache pollution (F-05)
    cache_key = f"{prop_type}:{src_id}:{team}"
    if cache_key in cache:
        return cache[cache_key]

    src_match = match_lookup.get(src_id)
    if not src_match:
        avg = sum(elo_params.values()) / max(len(elo_params), 1)
        cache[cache_key] = (avg, None)
        return avg, None

    # Find all teams whose bracket path includes this match
    # and compute expected opponent from the other side of the bracket
    home_slot = src_match["slot_home"]
    away_slot = src_match["slot_away"]

    # Collect teams that could appear on each side
    home_teams = _collect_teams_for_slot(
        home_slot, team, elo_params, qual_probs, match_lookup, bracket_paths, third_place_map, cache
    )
    away_teams = _collect_teams_for_slot(
        away_slot, team, elo_params, qual_probs, match_lookup, bracket_paths, third_place_map, cache
    )

    if prop_type == "winner":
        # We want the winner of this match — expected Elo of the stronger side
        # For the *opponent* of our team, we need to know which side our team is on
        # and take the other side
        opponent_teams = home_teams if team in [t for t, _ in away_teams] else away_teams
        if not opponent_teams:
            opponent_teams = away_teams if team in [t for t, _ in home_teams] else home_teams
    else:  # loser
        # For third-place match — loser of a match
        opponent_teams = home_teams if team in [t for t, _ in away_teams] else away_teams
        if not opponent_teams:
            opponent_teams = away_teams if team in [t for t, _ in home_teams] else home_teams

    if not opponent_teams:
        avg = sum(elo_params.values()) / max(len(elo_params), 1)
        cache[cache_key] = (avg, None)
        return avg, None

    # Probability-weighted expected Elo
    total_weight = sum(w for _, w in opponent_teams)
    if total_weight == 0:
        total_weight = 1.0

    expected_elo = sum(w * elo_params.get(t, 0) for t, w in opponent_teams) / total_weight
    best = max(opponent_teams, key=lambda x: x[1])

    result = (expected_elo, best[0])
    cache[cache_key] = result
    return result


def _collect_teams_for_slot(
    slot: str,
    exclude_team: str,
    elo_params: dict[str, float],
    qual_probs: dict[str, dict],
    match_lookup: dict[str, dict],
    bracket_paths: dict[str, list[PathNode]],
    third_place_map: dict,
    cache: dict,
    max_depth: int = 10,
) -> list[tuple[str, float]]:
    """Collect (team, probability) pairs that could occupy a bracket slot.

    For position+group slots, returns the most likely team at that position.
    For winner/loser slots, recursively resolves.
    For third-place slots, returns candidate 3rd-place teams.
    """
    if max_depth <= 0:
        return []

    info = parse_slot(slot)

    if info["type"] == "position_group":
        pos = info["position"]
        grp = info["group"]
        pos_key = f"p_{pos}{'st' if pos == 1 else 'nd' if pos == 2 else 'rd' if pos == 3 else 'th'}"
        teams = []
        for tname, tdata in qual_probs.items():
            if tdata.get("group") == grp and tname in elo_params:
                prob = tdata.get("position_probs", {}).get(pos_key, 0.0)
                if prob > 0:
                    teams.append((tname, prob))
        return teams

    if info["type"] == "third_place":
        pool_groups = info["pool_groups"]
        teams = []
        for g in pool_groups:
            for tname, tdata in qual_probs.items():
                if tdata.get("group") == g and tname in elo_params:
                    p3 = tdata.get("position_probs", {}).get("p_3rd", 0.0)
                    tpq = tdata.get("third_place_qual_prob", 0.0)
                    # Probability of being the 3rd-place team that qualifies from this pool
                    # Approximate: p_3rd * relative third_place_qual_prob
                    if p3 > 0 and tpq > 0:
                        teams.append((tname, p3 * tpq))
        return teams

    if info["type"] in ("winner", "loser"):
        src_id = f"KO{info['match_num']}"
        src_match = match_lookup.get(src_id)
        if not src_match:
            return []
        home = _collect_teams_for_slot(
            src_match["slot_home"], exclude_team, elo_params, qual_probs,
            match_lookup, bracket_paths, third_place_map, cache, max_depth - 1
        )
        away = _collect_teams_for_slot(
            src_match["slot_away"], exclude_team, elo_params, qual_probs,
            match_lookup, bracket_paths, third_place_map, cache, max_depth - 1
        )

        if info["type"] == "winner":
            # Winner — teams weighted by their probability of winning
            result = []
            for t, w in home:
                # P(team wins match) depends on expected opponent from away side
                away_elo_avg = (
                    sum(elo_params.get(a, 0) * aw for a, aw in away) / max(sum(aw for _, aw in away), 1e-9)
                    if away else sum(elo_params.values()) / max(len(elo_params), 1)
                )
                if t in elo_params:
                    team_elo = elo_params[t]
                else:
                    _avg = sum(elo_params.values()) / max(len(elo_params), 1)
                    warnings.warn(f"F-17: team '{t}' not in elo_params, using global avg {_avg:.4f}")
                    team_elo = _avg
                win_p = team_elo / max(team_elo + away_elo_avg, 1e-9)
                result.append((t, w * win_p))
            for t, w in away:
                home_elo_avg = (
                    sum(elo_params.get(h, 0) * hw for h, hw in home) / max(sum(hw for _, hw in home), 1e-9)
                    if home else sum(elo_params.values()) / max(len(elo_params), 1)
                )
                if t in elo_params:
                    team_elo = elo_params[t]
                else:
                    _avg = sum(elo_params.values()) / max(len(elo_params), 1)
                    warnings.warn(f"F-17: team '{t}' not in elo_params, using global avg {_avg:.4f}")
                    team_elo = _avg
                win_p = team_elo / max(team_elo + home_elo_avg, 1e-9)
                result.append((t, w * win_p))
            return result
        else:  # loser
            result = []
            for t, w in home:
                away_elo_avg = (
                    sum(elo_params.get(a, 0) * aw for a, aw in away) / max(sum(aw for _, aw in away), 1e-9)
                    if away else sum(elo_params.values()) / max(len(elo_params), 1)
                )
                if t in elo_params:
                    team_elo = elo_params[t]
                else:
                    _avg = sum(elo_params.values()) / max(len(elo_params), 1)
                    warnings.warn(f"F-17: team '{t}' not in elo_params, using global avg {_avg:.4f}")
                    team_elo = _avg
                lose_p = away_elo_avg / max(team_elo + away_elo_avg, 1e-9)
                result.append((t, w * lose_p))
            for t, w in away:
                home_elo_avg = (
                    sum(elo_params.get(h, 0) * hw for h, hw in home) / max(sum(hw for _, hw in home), 1e-9)
                    if home else sum(elo_params.values()) / max(len(elo_params), 1)
                )
                if t in elo_params:
                    team_elo = elo_params[t]
                else:
                    _avg = sum(elo_params.values()) / max(len(elo_params), 1)
                    warnings.warn(f"F-17: team '{t}' not in elo_params, using global avg {_avg:.4f}")
                    team_elo = _avg
                lose_p = home_elo_avg / max(team_elo + home_elo_avg, 1e-9)
                result.append((t, w * lose_p))
            return result

    return []


# ---------------------------------------------------------------------------
# Team-name helpers
# ---------------------------------------------------------------------------

_SLUG_OVERRIDES = {
    "côte-d'ivoire": "Côte d'Ivoire",
    "dr-congo": "DR Congo",
    "bosnia-and-herzegovina": "Bosnia and Herzegovina",
    "south-africa": "South Africa",
    "south-korea": "South Korea",
    "new-zealand": "New Zealand",
    "cape-verde": "Cape Verde",
    "czech-republic": "Czech Republic",
    "united-states": "United States",
    "saudi-arabia": "Saudi Arabia",
}


def _slug_to_canonical(slug: str) -> str:
    """Convert a slug like 'côte-d'ivoire' to canonical 'Côte d'Ivoire'."""
    if slug in _SLUG_OVERRIDES:
        return _SLUG_OVERRIDES[slug]
    # Default: title-case each segment
    return " ".join(s.capitalize() for s in slug.replace("-", " ").split())


# ---------------------------------------------------------------------------
# Main simulation
# ---------------------------------------------------------------------------


def compute_championship_paths(
    team_filter: str | None = None,
    group_filter: str | None = None,
) -> list[TeamChampionship]:
    """Compute championship probabilities for all (or filtered) teams.

    Args:
        team_filter: If set, only compute for this team.
        group_filter: If set, only compute for teams in this group.

    Returns:
        List of TeamChampionship results.
    """
    project_root = Path(__file__).resolve().parent.parent.parent

    # --- Load data ---
    qual_path = project_root / "data" / "processed" / "cds_qualification.json"
    elo_path = project_root / "data" / "processed" / "baselines" / "elo-proxy.json"
    tp_path = project_root / "config" / "third_place_mapping.json"
    schedule_path = project_root / "site" / "data" / "schedule.json"

    print("[CDS-Championship] Loading data...")
    qual_data = load_qualification_probs(qual_path)
    elo_params = load_elo_params(elo_path)

    with open(tp_path) as f:
        third_place_map = json.load(f)

    with open(schedule_path) as f:
        schedule = json.load(f)

    knockout = schedule["knockout"]
    match_lookup = {m["match_id"]: m for m in knockout}

    # Build bracket paths
    print("[CDS-Championship] Building bracket paths...")
    bracket_paths = build_bracket_paths(
        schedule_path=str(schedule_path),
        third_place_map_path=str(tp_path),
    )

    # Build team → group mapping
    team_group = {t: d["group"] for t, d in qual_data.items()}

    # Filter teams
    teams = list(qual_data.keys())
    if team_filter:
        teams = [t for t in teams if t == team_filter]
    elif group_filter:
        teams = [t for t in teams if team_group.get(t) == group_filter.upper()]

    if not teams:
        print("[CDS-Championship] No teams to simulate.")
        return []

    print(f"[CDS-Championship] Computing championship paths for {len(teams)} teams...")

    results: list[TeamChampionship] = []
    cache: dict = {}  # Shared cache for propagation slot resolution

    for i, team in enumerate(teams):
        print(f"  [{i+1}/{len(teams)}] {team}...", end=" ", flush=True)

        result = _compute_team_championship(
            team=team,
            team_group=team_group.get(team, ""),
            qual_data=qual_data.get(team, {}),
            elo_params=elo_params,
            bracket_paths=bracket_paths,
            match_lookup=match_lookup,
            third_place_map=third_place_map,
            qual_probs=qual_data,
            cache=cache,
        )
        results.append(result)
        print(f"championship_prob={result.championship_prob:.4f}")

    # Global normalization: ensure all championship probs sum to 1.0
    total = sum(tc.championship_prob for tc in results)
    if total > 0:
        for tc in results:
            tc.championship_prob = tc.championship_prob / total

    return results


def _compute_team_championship(
    team: str,
    team_group: str,
    qual_data: dict,
    elo_params: dict[str, float],
    bracket_paths: dict[str, list[PathNode]],
    match_lookup: dict[str, dict],
    third_place_map: dict,
    qual_probs: dict[str, dict],
    cache: dict,
) -> TeamChampionship:
    """Compute championship probability for a single team.

    Instead of parsing PathNode.opponent_slot (human-readable), we trace
    the bracket from raw schedule data to get raw slot references.
    """
    team_elo = elo_params.get(team, 1.0)
    qual_prob = qual_data.get("qual_prob", 0.5)
    position_probs = qual_data.get("position_probs", {})

    # --- Build raw entry points from schedule ---
    # For each qualifying position, find the R32 match and side
    knockout = list(match_lookup.values())
    slot_index: dict[str, list[tuple[str, str]]] = {}
    for m in knockout:
        for side in ("slot_home", "slot_away"):
            slot_index.setdefault(m[side], []).append((m["match_id"], side))

    # Collect entry points: list of (match_id, team_side, position_label, weight)
    entry_points: list[tuple[str, str, str, float]] = []

    # 1st place entry
    for mid, side in slot_index.get(f"1{team_group}", []):
        w = position_probs.get("p_1st", 0.5)
        entry_points.append((mid, side, "1st", w))

    # 2nd place entry
    for mid, side in slot_index.get(f"2{team_group}", []):
        w = position_probs.get("p_2nd", 0.3)
        entry_points.append((mid, side, "2nd", w))

    # 3rd place entry — check all third-place slots that include this group
    for slot, entries in slot_index.items():
        try:
            info = parse_slot(slot)
        except ValueError:
            continue
        if info["type"] == "third_place" and team_group in info["pool_groups"]:
            for mid, side in entries:
                p3 = position_probs.get("p_3rd", 0.0)
                tpq = qual_data.get("third_place_qual_prob", 0.0)
                w = p3 * tpq  # Simplified weight
                entry_points.append((mid, side, "3rd", w))

    if not entry_points:
        # Fallback — no entry found
        return TeamChampionship(
            team=team, group=team_group, championship_prob=0.0,
            championship_path_count=0, dominant_path_pattern="no_entry",
            dominant_failure_node="none", bracket_dependency="none",
            path_nodes=[], simulation_meta={
                "run_at_utc": datetime.now(timezone.utc).isoformat(),
                "probability_source": "elo_poisson",
                "qualification_prob_used": qual_prob,
                "paths_enumerated": 0,
            },
        )

    # --- Build downstream graph (winner propagation) ---
    downstream: dict[str, list[tuple[str, str]]] = {}  # match_id → [(child_mid, child_side)]
    for m in knockout:
        num = m["match_id"].replace("KO", "")
        w_ref = f"W{num}"
        for other in knockout:
            if other["match_id"] == m["match_id"]:
                continue
            if other["slot_home"] == w_ref:
                downstream.setdefault(m["match_id"], []).append((other["match_id"], "slot_home"))
            if other["slot_away"] == w_ref:
                downstream.setdefault(m["match_id"], []).append((other["match_id"], "slot_away"))

    # --- Trace each entry point to final ---
    all_path_results: list[tuple[float, list[PathProbability], list[tuple[str, str]]]] = []

    for entry_mid, entry_side, pos_label, pos_weight in entry_points:
        # DFS to find all paths from this entry to the final
        raw_paths = _trace_raw_paths(entry_mid, entry_side, match_lookup, downstream)

        for raw_path in raw_paths:
            # raw_path: list of (match_id, team_side, opp_raw_slot)
            path_prob_nodes: list[PathProbability] = []
            cumulative = 1.0

            for match_id, team_side, opp_raw_slot in raw_path:
                match = match_lookup[match_id]
                round_name = match["round"]
                if round_name not in CHAMPIONSHIP_ROUNDS:
                    continue

                # Resolve opponent Elo from raw slot
                opp_elo, opp_name = _resolve_opponent_elo(
                    slot=opp_raw_slot,
                    team=team,
                    elo_params=elo_params,
                    team_group=team_group,
                    qual_probs=qual_probs,
                    match_lookup=match_lookup,
                    bracket_paths=bracket_paths,
                    third_place_map=third_place_map,
                    cache=cache,
                )

                win_prob = team_elo / max(team_elo + opp_elo, 1e-9)
                win_prob = max(0.01, min(0.99, win_prob))
                cumulative *= win_prob

                path_prob_nodes.append(PathProbability(
                    round=round_name,
                    match_id=match_id,
                    opponent_slot=opp_raw_slot,
                    opponent_team=opp_name,
                    conditional_win_prob=round(win_prob, 4),
                    cumulative_prob=round(cumulative, 6),
                    probability_source="elo_poisson",
                ))

            if path_prob_nodes:
                all_path_results.append((cumulative * pos_weight, path_prob_nodes, raw_path))

    # --- Aggregate results ---
    total_champ_prob = sum(p for p, _, _ in all_path_results)
    # F-03: Clamp to [0,1] as safety net against probability > 1.0
    # NOTE: this is a temporary fix; full solution requires computing paths
    # under the full probability law (inclusion-exclusion over overlapping paths).
    # With the F-05 cache fix, P>1.0 should occur much less frequently.
    total_champ_prob = min(1.0, max(0.0, total_champ_prob))

    # Find dominant path (highest weighted prob)
    if all_path_results:
        best_idx = max(range(len(all_path_results)), key=lambda i: all_path_results[i][0])
        best_prob, best_path, best_raw = all_path_results[best_idx]
    else:
        best_path = []
        best_raw = []

    # Dominant failure node
    biggest_drop_node = ""
    biggest_drop = 0.0
    if len(best_path) > 0:
        prev_cum = qual_prob
        for pn in best_path:
            drop = prev_cum - pn.conditional_win_prob
            if drop > biggest_drop:
                biggest_drop = drop
                round_title = pn.round.replace("_", " ").title()
                opp_desc = team_zh(pn.opponent_team) if pn.opponent_team else pn.opponent_slot
                biggest_drop_node = (
                    f"{round_title} vs {opp_desc} "
                    f"(win_prob {pn.conditional_win_prob:.2f}, "
                    f"cumulative {pn.cumulative_prob:.4f})"
                )
            prev_cum = pn.cumulative_prob

    # Dominant path pattern
    pattern_parts = []
    for pn in best_path:
        round_short = _round_short(pn.round)
        opp = team_zh(pn.opponent_team) if pn.opponent_team else pn.opponent_slot
        pattern_parts.append(f"{round_short}:{opp}")
    dominant_pattern = " → ".join(pattern_parts) if pattern_parts else "no_path"

    path_count = len(all_path_results)

    # Bracket dependencies from raw slots
    dependencies = set()
    for _, _, opp_raw in best_raw:
        try:
            info = parse_slot(opp_raw)
        except ValueError:
            continue
        if info["type"] == "third_place":
            dependencies.add(
                f"32强对手取决于 {opp_raw} "
                f"（小组 {','.join(info['pool_groups'])}）"
            )
        elif info["type"] in ("winner", "loser"):
            # Find which round this match is in
            for pn in best_path:
                if pn.opponent_slot == opp_raw:
                    dependencies.add(f"{_round_chinese(pn.round)}对手: {opp_raw}")
                    break

    bracket_dep = "；".join(dependencies) if dependencies else "none"

    now = datetime.now(timezone.utc)
    return TeamChampionship(
        team=team,
        group=team_group,
        championship_prob=round(total_champ_prob, 6),
        championship_path_count=path_count,
        dominant_path_pattern=dominant_pattern,
        dominant_failure_node=biggest_drop_node or "none",
        bracket_dependency=bracket_dep,
        black_swan_dependency="not_assessed",
        penalty_dependency="not_assessed",
        injury_sensitivity="not_assessed",
        simulation_status="run_complete",
        path_nodes=best_path,
        simulation_meta={
            "run_at_utc": now.isoformat(),
            "probability_source": "elo_poisson",
            "qualification_prob_used": qual_prob,
            "paths_enumerated": path_count,
        },
    )


def _trace_raw_paths(
    entry_mid: str,
    entry_side: str,
    match_lookup: dict[str, dict],
    downstream: dict[str, list[tuple[str, str]]],
) -> list[list[tuple[str, str, str]]]:
    """Trace all paths from entry to final, returning raw (match_id, team_side, opp_raw_slot) tuples.

    Returns list of paths. Each path is a list of (match_id, team_side, opp_raw_slot).
    """
    results: list[list[tuple[str, str, str]]] = []
    stack: list[tuple[str, str, list[tuple[str, str, str]]]] = [(entry_mid, entry_side, [])]

    while stack:
        cur_mid, cur_side, cur_path = stack.pop()
        match = match_lookup.get(cur_mid)
        if not match:
            continue

        opp_side = "slot_away" if cur_side == "slot_home" else "slot_home"
        opp_raw = match[opp_side]

        new_path = cur_path + [(cur_mid, cur_side, opp_raw)]

        if match["round"] == "final":
            results.append(new_path)
            continue

        # Follow winner propagation
        children = downstream.get(cur_mid, [])
        for child_mid, child_side in children:
            stack.append((child_mid, child_side, new_path))

    return results


# Removed: old _trace_paths_from_entry and _get_entry_weight replaced by _trace_raw_paths


def _round_short(round_name: str) -> str:
    """Convert round name to short form."""
    return {
        "round_of_32": "R32",
        "round_of_16": "R16",
        "quarterfinal": "QF",
        "semifinal": "SF",
        "final": "Final",
        "third_place": "3rd",
    }.get(round_name, round_name)


def _round_chinese(round_name: str) -> str:
    """Convert round name to Chinese short form."""
    return {
        "round_of_32": "32强",
        "round_of_16": "16强",
        "quarterfinal": "八强",
        "semifinal": "半决赛",
        "final": "决赛",
        "third_place": "季军赛",
    }.get(round_name, round_name)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------


def championship_to_dict(tc: TeamChampionship) -> dict:
    """Convert a TeamChampionship to schema-compliant dict."""
    return {
        "team": tc.team,
        "group": tc.group,
        "championship_prob": tc.championship_prob,
        "championship_path_count": tc.championship_path_count,
        "dominant_path_pattern": tc.dominant_path_pattern,
        "dominant_failure_node": tc.dominant_failure_node,
        "bracket_dependency": tc.bracket_dependency,
        "black_swan_dependency": tc.black_swan_dependency,
        "penalty_dependency": tc.penalty_dependency,
        "injury_sensitivity": tc.injury_sensitivity,
        "simulation_status": tc.simulation_status,
        "path_nodes": [
            {
                "round": pn.round,
                "match_id": pn.match_id,
                "opponent_slot": pn.opponent_slot,
                "opponent_team": pn.opponent_team,
                "conditional_win_prob": pn.conditional_win_prob,
                "cumulative_prob": pn.cumulative_prob,
                "probability_source": pn.probability_source,
            }
            for pn in tc.path_nodes
        ],
        "simulation_meta": tc.simulation_meta,
    }
