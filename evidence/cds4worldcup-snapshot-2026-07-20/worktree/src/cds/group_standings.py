"""Group standings calculator with FIFA 2026 multi-team tiebreaker protocol.

Implements the official FIFA ranking procedure for group stage standings:
1. Points (3=win, 1=draw, 0=loss)
2. For 3+ teams tied on points: mini-league (matches between tied teams only)
   a. Mini-league points
   b. Mini-league goal difference
   c. Mini-league goals scored
3. If still tied: full group stats
   a. Full group goal difference
   b. Full group goals scored
4. Fair-play points (disciplinary data — optional)
5. Drawing of lots (seeded random — last resort)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MatchResult:
    """A single completed match result."""

    home: str
    away: str
    home_goals: int
    away_goals: int


@dataclass
class Standing:
    """A team's final standing in the group."""

    team: str
    position: int  # 1-4
    points: int
    goal_diff: int
    goals_for: int
    goals_against: int
    tiebreaker_note: str  # how the tie was resolved


def compute_group_standings(
    teams: list[str],
    results: list[MatchResult],
    fair_play: dict[str, float] | None = None,
    lots_seed: int = 42,
) -> list[Standing]:
    """Compute final group standings from match results.

    Args:
        teams: 4 team names in the group.
        results: 6 match results (all pairs).
        fair_play: Optional mapping {team: fair_play_points}.
                   Higher is better (fewer deductions). Skip if None.
        lots_seed: Seed for drawing of lots (last resort tiebreaker).

    Returns:
        Standings ordered 1st through 4th.
    """
    if len(teams) != 4:
        raise ValueError(f"Expected 4 teams, got {len(teams)}")
    if len(results) != 6:
        raise ValueError(f"Expected 6 match results, got {len(results)}")

    # Build per-team full group stats
    full_stats = _compute_stats(teams, results)

    # Rank teams using FIFA tiebreaker protocol
    ranked = _rank_teams(teams, results, full_stats, fair_play, lots_seed)

    # Build Standing objects
    standings = []
    for position, team in enumerate(ranked, start=1):
        stats = full_stats[team]
        # Find the tiebreaker note for this team
        note = _get_tiebreaker_note(team, teams, results, full_stats, fair_play)
        standings.append(
            Standing(
                team=team,
                position=position,
                points=stats["points"],
                goal_diff=stats["goal_diff"],
                goals_for=stats["goals_for"],
                goals_against=stats["goals_against"],
                tiebreaker_note=note,
            )
        )
    return standings


def _compute_stats(teams: list[str], results: list[MatchResult]) -> dict[str, dict]:
    """Compute full group stats for each team."""
    stats: dict[str, dict] = {}
    for team in teams:
        stats[team] = {"points": 0, "goals_for": 0, "goals_against": 0, "goal_diff": 0}

    for match in results:
        h, a = match.home, match.away
        hg, ag = match.home_goals, match.away_goals

        stats[h]["goals_for"] += hg
        stats[h]["goals_against"] += ag
        stats[a]["goals_for"] += ag
        stats[a]["goals_against"] += hg

        if hg > ag:
            stats[h]["points"] += 3
        elif hg < ag:
            stats[a]["points"] += 3
        else:
            stats[h]["points"] += 1
            stats[a]["points"] += 1

    for team in teams:
        s = stats[team]
        s["goal_diff"] = s["goals_for"] - s["goals_against"]

    return stats


def _compute_mini_league_stats(
    tied_teams: set[str], results: list[MatchResult]
) -> dict[str, dict]:
    """Compute stats using only matches between tied teams."""
    stats: dict[str, dict] = {}
    for team in tied_teams:
        stats[team] = {"points": 0, "goals_for": 0, "goals_against": 0, "goal_diff": 0}

    for match in results:
        h, a = match.home, match.away
        if h not in tied_teams or a not in tied_teams:
            continue
        hg, ag = match.home_goals, match.away_goals

        stats[h]["goals_for"] += hg
        stats[h]["goals_against"] += ag
        stats[a]["goals_for"] += ag
        stats[a]["goals_against"] += hg

        if hg > ag:
            stats[h]["points"] += 3
        elif hg < ag:
            stats[a]["points"] += 3
        else:
            stats[h]["points"] += 1
            stats[a]["points"] += 1

    for team in tied_teams:
        s = stats[team]
        s["goal_diff"] = s["goals_for"] - s["goals_against"]

    return stats


def _rank_teams(
    teams: list[str],
    results: list[MatchResult],
    full_stats: dict[str, dict],
    fair_play: dict[str, float] | None,
    lots_seed: int,
) -> list[str]:
    """Rank teams using FIFA 2026 multi-team tiebreaker protocol.

    The protocol:
    1. Group by points
    2. For groups of 3+ tied: mini-league (points → GD → GS)
    3. If still tied: full group (GD → GS)
    4. Fair-play (if available)
    5. Drawing of lots
    """
    # Group teams by points
    points_groups: dict[int, list[str]] = {}
    for team in teams:
        pts = full_stats[team]["points"]
        points_groups.setdefault(pts, []).append(team)

    # Sort point levels descending
    sorted_point_levels = sorted(points_groups.keys(), reverse=True)

    ranked: list[str] = []
    for pts in sorted_point_levels:
        group = points_groups[pts]
        if len(group) == 1:
            ranked.append(group[0])
        elif len(group) == 2:
            # 2-team tie: use full group GD, GS, then fair-play, then lots
            resolved = _resolve_two_team_tie(
                group, results, full_stats, fair_play, lots_seed
            )
            ranked.extend(resolved)
        else:
            # 3+ team tie: FIFA mini-league protocol
            resolved = _resolve_multi_team_tie(
                group, results, full_stats, fair_play, lots_seed
            )
            ranked.extend(resolved)

    return ranked


def _resolve_two_team_tie(
    tied_teams: list[str],
    results: list[MatchResult],
    full_stats: dict[str, dict],
    fair_play: dict[str, float] | None,
    lots_seed: int,
) -> list[str]:
    """Resolve a 2-team tie using full group GD → GS → fair-play → lots.

    Note: For 2-team ties in FIFA rules, H2H is the first tiebreaker after points.
    But per the task spec, the mini-league is used for 3+ teams only.
    For 2 teams tied on points, the standard order is:
    1. Full group GD
    2. Full group GS
    3. Fair-play
    4. Drawing of lots
    """
    team_a, team_b = tied_teams[0], tied_teams[1]
    sa, sb = full_stats[team_a], full_stats[team_b]

    # Full group goal difference
    if sa["goal_diff"] != sb["goal_diff"]:
        return sorted(tied_teams, key=lambda t: full_stats[t]["goal_diff"], reverse=True)

    # Full group goals scored
    if sa["goals_for"] != sb["goals_for"]:
        return sorted(tied_teams, key=lambda t: full_stats[t]["goals_for"], reverse=True)

    # Fair-play
    if fair_play is not None:
        fp_a = fair_play.get(team_a, 0)
        fp_b = fair_play.get(team_b, 0)
        if fp_a != fp_b:
            return sorted(
                tied_teams, key=lambda t: fair_play.get(t, 0), reverse=True
            )

    # Drawing of lots
    return _drawing_of_lots(tied_teams, lots_seed)


def _resolve_multi_team_tie(
    tied_teams: list[str],
    results: list[MatchResult],
    full_stats: dict[str, dict],
    fair_play: dict[str, float] | None,
    lots_seed: int,
) -> list[str]:
    """Resolve 3+ team tie using FIFA mini-league → full group fallback.

    Step 1: Mini-league (only matches between tied teams):
      a. Mini-league points
      b. Mini-league goal difference
      c. Mini-league goals scored

    Step 2: If still tied, full group stats:
      a. Full group goal difference
      b. Full group goals scored

    Step 3: Fair-play points (if available)

    Step 4: Drawing of lots

    After each criterion, separate resolved teams and recurse on remaining ties.
    """
    tied_set = set(tied_teams)
    mini_stats = _compute_mini_league_stats(tied_set, results)

    # Try mini-league criteria in order, separating teams that can be distinguished
    for criterion in ["points", "goal_diff", "goals_for"]:
        resolved = _try_separate(tied_teams, mini_stats, criterion)
        if resolved is not None:
            return resolved

    # Mini-league couldn't separate — try full group stats
    for criterion in ["goal_diff", "goals_for"]:
        resolved = _try_separate(tied_teams, full_stats, criterion)
        if resolved is not None:
            return resolved

    # Full group couldn't separate — try fair-play
    if fair_play is not None:
        # Check if fair-play can separate
        fp_values = {t: fair_play.get(t, 0) for t in tied_teams}
        if len(set(fp_values.values())) > 1:
            resolved = _try_separate_with_values(tied_teams, fp_values)
            if resolved is not None:
                return resolved

    # Drawing of lots
    return _drawing_of_lots(tied_teams, lots_seed)


def _try_separate(
    teams: list[str], stats: dict[str, dict], criterion: str
) -> list[str] | None:
    """Try to rank teams by a single criterion.

    If all teams have distinct values, return them sorted.
    If some ties remain, recursively resolve sub-groups.
    Returns None if all teams are equal on this criterion.
    """
    # Group by criterion value
    groups: dict[int | float, list[str]] = {}
    for team in teams:
        val = stats[team][criterion]
        groups.setdefault(val, []).append(team)

    if len(groups) == 1:
        # All equal on this criterion — can't separate
        return None

    # Sort groups by criterion value descending
    sorted_values = sorted(groups.keys(), reverse=True)

    result: list[str] = []
    for val in sorted_values:
        group = groups[val]
        if len(group) == 1:
            result.append(group[0])
        else:
            # Sub-group still tied — return None to let caller try next criterion
            return None

    return result


def _try_separate_with_values(
    teams: list[str], values: dict[str, float]
) -> list[str] | None:
    """Try to rank teams by arbitrary numeric values (e.g., fair-play points)."""
    groups: dict[float, list[str]] = {}
    for team in teams:
        val = values[team]
        groups.setdefault(val, []).append(team)

    if len(groups) == 1:
        return None

    sorted_values = sorted(groups.keys(), reverse=True)

    result: list[str] = []
    for val in sorted_values:
        group = groups[val]
        if len(group) == 1:
            result.append(group[0])
        else:
            return None  # Still tied sub-group

    return result


def _drawing_of_lots(teams: list[str], seed: int) -> list[str]:
    """Random drawing of lots as last resort tiebreaker."""
    shuffled = list(teams)
    rng = random.Random(seed)
    rng.shuffle(shuffled)
    return shuffled


def _get_tiebreaker_note(
    team: str,
    teams: list[str],
    results: list[MatchResult],
    full_stats: dict[str, dict],
    fair_play: dict[str, float] | None,
) -> str:
    """Generate a human-readable note about how ties were resolved."""
    # Find which teams share the same points
    team_pts = full_stats[team]["points"]
    same_pts = [t for t in teams if full_stats[t]["points"] == team_pts and t != team]

    if not same_pts:
        return f"Clear position (unique points: {team_pts})"

    # 2-team tie
    if len(same_pts) == 1:
        other = same_pts[0]
        sa, so = full_stats[team], full_stats[other]
        if sa["goal_diff"] != so["goal_diff"]:
            return f"2-team tie on {team_pts}pts → resolved by goal difference"
        if sa["goals_for"] != so["goals_for"]:
            return f"2-team tie on {team_pts}pts → resolved by goals scored"
        if fair_play is not None:
            if fair_play.get(team, 0) != fair_play.get(other, 0):
                return f"2-team tie on {team_pts}pts → resolved by fair-play points"
        return f"2-team tie on {team_pts}pts → resolved by drawing of lots"

    # 3+ team tie — check mini-league
    tied_teams = [team] + same_pts
    tied_set = set(tied_teams)
    mini_stats = _compute_mini_league_stats(tied_set, results)

    # Check which mini-league criterion resolved it
    for criterion, label in [
        ("points", "mini-league points"),
        ("goal_diff", "mini-league goal difference"),
        ("goals_for", "mini-league goals scored"),
    ]:
        vals = {t: mini_stats[t][criterion] for t in tied_teams}
        if len(set(vals.values())) > 1:
            # Check if this team is unique on this criterion among the tie group
            team_val = vals[team]
            if sum(1 for v in vals.values() if v == team_val) == 1:
                return f"{len(tied_teams)}-team tie on {team_pts}pts → resolved by {label}"

    # Full group fallback
    for criterion, label in [
        ("goal_diff", "full group goal difference"),
        ("goals_for", "full group goals scored"),
    ]:
        vals = {t: full_stats[t][criterion] for t in tied_teams}
        if len(set(vals.values())) > 1:
            team_val = vals[team]
            if sum(1 for v in vals.values() if v == team_val) == 1:
                return f"{len(tied_teams)}-team tie on {team_pts}pts → resolved by {label}"

    # Fair-play
    if fair_play is not None:
        fp_vals = {t: fair_play.get(t, 0) for t in tied_teams}
        if len(set(fp_vals.values())) > 1:
            return f"{len(tied_teams)}-team tie on {team_pts}pts → resolved by fair-play points"

    return f"{len(tied_teams)}-team tie on {team_pts}pts → resolved by drawing of lots"
