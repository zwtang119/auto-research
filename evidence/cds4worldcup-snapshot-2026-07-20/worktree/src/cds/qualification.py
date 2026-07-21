"""Group qualification scenario simulation.

Core algorithm for computing each team's probability of advancing from the
group stage of the 2026 FIFA World Cup.

Approach (per team):
  1. Find the team's group (4 teams, 6 matches).
  2. Enumerate the team's 3 matches → 3^3 = 27 outcome scenarios.
  3. For each of the 27 scenarios, Monte-Carlo-sample the OTHER 3 group matches
     using Elo probabilities (N_SAMPLES draws per scenario).
  4. Call compute_group_standings() for each completed scenario.
  5. Aggregate to get qual_prob = P(top 2) + P(3rd & best-8-third-place).

Third-place qualification requires cross-group comparison: after computing
all 12 groups' position distributions, rank the 12 third-placed teams and
estimate the probability that each group's 3rd-place team is in the top 8.
"""

from __future__ import annotations

import json
import math
import random
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.cds.group_standings import MatchResult, Standing, compute_group_standings


def _poisson_sample(lam: float, rng: random.Random) -> int:
    """Sample from Poisson(lam) using Knuth's algorithm."""
    if lam < 0:
        return 0
    L = math.exp(-lam)
    k = 0
    p = 1.0
    while True:
        k += 1
        p *= rng.random()
        if p < L:
            break
    return k - 1

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------

# Outcome label for a single match from a team's perspective
OUTCOMES = ("W", "D", "L")

# Scenario classification labels (Chinese, per schema)
SCENARIO_SECURED = "已定出线"
SCENARIO_MUST_WIN = "必胜出线"
SCENARIO_DANGER = "危局"
SCENARIO_ELIMINATED = "已淘汰"
SCENARIO_NORMAL = "正常争夺"


@dataclass
class TeamQualification:
    """Qualification analysis for one team."""

    team: str
    group: str
    qual_prob: float
    position_probs: dict[str, float]  # p_1st, p_2nd, p_3rd, p_4th
    third_place_qual_prob: float | None
    scenarios: list[dict[str, Any]]
    key_matches: list[dict[str, Any]]
    simulation_meta: dict[str, Any]
    qual_prob_top2: float | None = None  # F-04: original top-2 probability before third-place addition


# ---------------------------------------------------------------------------
# Probability helpers
# ---------------------------------------------------------------------------


def load_odds(path: str | Path) -> dict[str, dict]:
    """Load odds.json and return {match_id: prediction_dict}."""
    with open(path) as f:
        data = json.load(f)
    return {p["match_id"]: p for p in data["predictions"]}


def load_schedule(path: str | Path) -> dict:
    """Load schedule.json."""
    with open(path) as f:
        return json.load(f)


def load_team_registry(path: str | Path) -> list[dict]:
    """Load team_registry.csv → list of dicts."""
    import csv

    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_group_schedule(schedule: dict) -> dict[str, dict]:
    """Build {group_letter: {teams: [...], matches: [...]}} from schedule.json."""
    groups = {}
    for letter, gdata in schedule["groups"].items():
        teams = [t["name"] for t in gdata["teams"]]
        matches = []
        for m in gdata["matches"]:
            matches.append(
                {
                    "match_id": m["match_id"],
                    "round": m["round"],
                    "home": m["home"],
                    "away": m["away"],
                }
            )
        groups[letter] = {"teams": teams, "matches": matches}
    return groups


# ---------------------------------------------------------------------------
# Score generation
# ---------------------------------------------------------------------------


def _typical_scorelines(outcome: str) -> list[tuple[int, int]]:
    """Return plausible scorelines for W/D/L outcome."""
    if outcome == "W":
        return [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (1, 0), (2, 1)]
    elif outcome == "D":
        return [(0, 0), (1, 1), (2, 2), (0, 0), (1, 1), (1, 1)]
    else:  # L
        return [(0, 1), (0, 2), (1, 2), (0, 3), (1, 3), (0, 1), (1, 2)]


def _sample_scoreline(
    outcome: str,
    expected_goals_home: float = 1.5,
    expected_goals_away: float = 1.0,
    rng: random.Random | None = None,
) -> tuple[int, int]:
    """Sample a realistic scoreline for a given outcome.

    Uses a Poisson model centered on expected goals, then adjusts to match
    the desired outcome (W/D/L).
    """
    if rng is None:
        rng = random.Random()

    if expected_goals_home < 0.3:
        expected_goals_home = 0.3
    if expected_goals_away < 0.3:
        expected_goals_away = 0.3

    # Try Poisson first, retry if outcome doesn't match
    for _ in range(20):
        hg = _poisson_sample(expected_goals_home, rng)
        ag = _poisson_sample(expected_goals_away, rng)
        if outcome == "W" and hg > ag:
            return (hg, ag)
        elif outcome == "D" and hg == ag:
            return (hg, ag)
        elif outcome == "L" and hg < ag:
            return (hg, ag)

    # Fallback: pick from typical scorelines
    scorelines = _typical_scorelines(outcome)
    return rng.choice(scorelines)


# ---------------------------------------------------------------------------
# Core simulation
# ---------------------------------------------------------------------------

# Number of Monte Carlo samples for the OTHER 3 matches per scenario
N_MC_SAMPLES = 200

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


def _outcome_for_team(
    match: dict, team: str, outcome: str
) -> tuple[str, str, str]:
    """Determine home/away and W/D/L perspective for a team in a match.

    Returns (home, away, result_from_home_perspective) where result is 'W','D','L'.
    """
    if match["home"] == team:
        return (match["home"], match["away"], outcome)
    else:
        # Team is away; flip W↔L
        flipped = {"W": "L", "D": "D", "L": "W"}[outcome]
        return (match["home"], match["away"], flipped)


def simulate_team_qualification(
    team: str,
    group_letter: str,
    group_data: dict,
    odds_map: dict[str, dict],
    n_mc_samples: int = N_MC_SAMPLES,
    rng_seed: int = 42,
) -> TeamQualification:
    """Simulate qualification probability for a single team.

    Args:
        team: Team name.
        group_letter: Group letter (A–L).
        group_data: {"teams": [...], "matches": [...]} for the group.
        odds_map: {match_id: {home_win, draw, away_win, expected_goals_*}}.
        n_mc_samples: Monte Carlo samples for other matches per scenario.
        rng_seed: Random seed.

    Returns:
        TeamQualification with probabilities and scenario analysis.
    """
    rng = random.Random(rng_seed)
    teams = group_data["teams"]
    matches = group_data["matches"]

    # Split matches: team's matches vs other matches
    team_matches = [m for m in matches if team in (m["home"], m["away"])]
    other_matches = [m for m in matches if team not in (m["home"], m["away"])]

    # --- Phase 1: enumerate 3^3 = 27 scenarios for the team's matches ---
    # Weighted position counts: position -> total weighted probability
    weighted_position_counts: dict[int, float] = {}
    scenario_results: list[dict] = []  # per-scenario aggregation

    # For key_matches impact calculation (weighted)
    win_qual_weight: dict[int, float] = {}  # match_idx -> qual weight when winning
    lose_qual_weight: dict[int, float] = {}
    win_total_weight: dict[int, float] = {}
    lose_total_weight: dict[int, float] = {}

    for scenario_idx in range(27):
        # Decode scenario_idx into 3 outcomes (base-3)
        outcomes = []
        tmp = scenario_idx
        for _ in range(3):
            outcomes.append(OUTCOMES[tmp % 3])
            tmp //= 3

        # Compute Elo probability of this outcome combination
        scenario_prob = 1.0
        for mi, m in enumerate(team_matches):
            pred = odds_map.get(m["match_id"], {})
            p_hw = pred.get("home_win", 0.4)
            p_dr = pred.get("draw", 0.3)
            p_aw = pred.get("away_win", 0.3)

            # Get probability of the team's outcome in this match
            if m["home"] == team:
                if outcomes[mi] == "W":
                    scenario_prob *= p_hw
                elif outcomes[mi] == "D":
                    scenario_prob *= p_dr
                else:
                    scenario_prob *= p_aw
            else:
                # Team is away: W means away_win, L means home_win
                if outcomes[mi] == "W":
                    scenario_prob *= p_aw
                elif outcomes[mi] == "D":
                    scenario_prob *= p_dr
                else:
                    scenario_prob *= p_hw

        # Track per-scenario qualification
        qual_in_scenario = 0
        total_in_scenario = 0

        for mc_run in range(n_mc_samples):
            # Build all 6 match results
            all_results: list[MatchResult] = []

            # Team's 3 matches (fixed outcomes)
            for mi, m in enumerate(team_matches):
                home, away, result = _outcome_for_team(m, team, outcomes[mi])

                # Get expected goals from odds
                pred = odds_map.get(m["match_id"], {})
                exp_h = pred.get("expected_goals_home", 1.5)
                exp_a = pred.get("expected_goals_away", 1.0)

                # Adjust expected goals based on outcome to bias Poisson
                if result == "W":
                    exp_h_adj = max(exp_h, 1.2)
                    exp_a_adj = min(exp_a, 0.8)
                elif result == "L":
                    exp_h_adj = min(exp_h, 0.8)
                    exp_a_adj = max(exp_a, 1.2)
                else:
                    exp_h_adj = exp_h * 0.85
                    exp_a_adj = exp_a * 0.85

                hg, ag = _sample_scoreline(result, exp_h_adj, exp_a_adj, rng)
                all_results.append(MatchResult(home=home, away=away, home_goals=hg, away_goals=ag))

            # Other 3 matches (Monte Carlo sampled from Elo probabilities)
            for m in other_matches:
                pred = odds_map.get(m["match_id"], {})
                p_hw = pred.get("home_win", 0.4)
                p_dr = pred.get("draw", 0.3)
                p_aw = pred.get("away_win", 0.3)
                exp_h = pred.get("expected_goals_home", 1.3)
                exp_a = pred.get("expected_goals_away", 1.1)

                # Sample outcome
                r = rng.random()
                if r < p_hw:
                    oth_outcome = "W"  # home wins
                elif r < p_hw + p_dr:
                    oth_outcome = "D"
                else:
                    oth_outcome = "L"  # home loses

                hg, ag = _sample_scoreline(oth_outcome, exp_h, exp_a, rng)
                all_results.append(
                    MatchResult(home=m["home"], away=m["away"], home_goals=hg, away_goals=ag)
                )

            # Compute standings
            standings = compute_group_standings(teams, all_results, lots_seed=rng.randint(0, 10**6))

            # Find our team's position
            team_pos = None
            for s in standings:
                if s.team == team:
                    team_pos = s.position
                    break

            if team_pos is None:
                continue

            # Weight this observation by scenario probability
            w = scenario_prob / n_mc_samples
            weighted_position_counts[team_pos] = weighted_position_counts.get(team_pos, 0.0) + w
            total_in_scenario += 1

            # Top 2 = direct qualification
            if team_pos in (1, 2):
                qual_in_scenario += 1

            # Track key match impacts (weighted)
            for mi, m in enumerate(team_matches):
                if outcomes[mi] == "W":
                    win_total_weight[mi] = win_total_weight.get(mi, 0.0) + w
                    if team_pos in (1, 2):
                        win_qual_weight[mi] = win_qual_weight.get(mi, 0.0) + w
                elif outcomes[mi] == "L":
                    lose_total_weight[mi] = lose_total_weight.get(mi, 0.0) + w
                    if team_pos in (1, 2):
                        lose_qual_weight[mi] = lose_qual_weight.get(mi, 0.0) + w

        scenario_results.append(
            {
                "outcomes": outcomes,
                "scenario_prob": scenario_prob,
                "qual_count": qual_in_scenario,
                "total_count": total_in_scenario,
                "qual_rate": qual_in_scenario / total_in_scenario if total_in_scenario > 0 else 0.0,
            }
        )

    # Position probabilities (sum should ≈ 1.0)
    total_weight = sum(weighted_position_counts.values())
    p_1st = weighted_position_counts.get(1, 0.0) / total_weight if total_weight > 0 else 0.0
    p_2nd = weighted_position_counts.get(2, 0.0) / total_weight if total_weight > 0 else 0.0
    p_3rd = weighted_position_counts.get(3, 0.0) / total_weight if total_weight > 0 else 0.0
    p_4th = weighted_position_counts.get(4, 0.0) / total_weight if total_weight > 0 else 0.0
    qual_prob = p_1st + p_2nd  # Direct qualification (top 2)

    # --- Phase 2: Classify scenarios ---
    scenarios = _classify_scenarios(
        team, team_matches, scenario_results, qual_prob
    )

    # --- Phase 3: Key matches impact ---
    key_matches_list = _compute_key_matches(
        team_matches, win_qual_weight, lose_qual_weight, win_total_weight, lose_total_weight, team
    )

    return TeamQualification(
        team=team,
        group=group_letter,
        qual_prob=round(qual_prob, 4),
        position_probs={
            "p_1st": round(p_1st, 4),
            "p_2nd": round(p_2nd, 4),
            "p_3rd": round(p_3rd, 4),
            "p_4th": round(p_4th, 4),
        },
        third_place_qual_prob=None,  # filled in cross-group phase
        scenarios=scenarios,
        key_matches=key_matches_list,
        simulation_meta={},  # filled by caller
    )


def _classify_scenarios(
    team: str,
    team_matches: list[dict],
    scenario_results: list[dict],
    overall_qual_prob: float,
) -> list[dict]:
    """Classify the 27 scenarios into schema-compliant scenario groups.

    Each scenario is weighted by its Elo probability (scenario_prob).
    """
    # Group scenarios by classification
    secured = []  # qual_rate = 1.0
    must_win_scenarios = []  # all wins → always qualify
    danger = []  # qual_rate in [0.2, 0.5]
    eliminated = []  # qual_rate = 0.0
    normal = []  # everything else

    for sr in scenario_results:
        qr = sr["qual_rate"]
        if qr >= 0.999:
            secured.append(sr)
        elif qr <= 0.001:
            eliminated.append(sr)
        elif 0.2 <= qr <= 0.5:
            danger.append(sr)
        else:
            normal.append(sr)

    # Check "must-win": if all 3 matches are W, does team always qualify?
    all_wins_scenario = None
    for sr in scenario_results:
        if sr["outcomes"] == ["W", "W", "W"]:
            all_wins_scenario = sr
            break

    must_win_trigger = None
    if all_wins_scenario and all_wins_scenario["qual_rate"] >= 0.99:
        must_win_trigger = "赢下全部剩余比赛 → 确保前二出线"
        # Move all-wins from its current category to must-win
        if all_wins_scenario in secured:
            secured.remove(all_wins_scenario)
        elif all_wins_scenario in normal:
            normal.remove(all_wins_scenario)
        must_win_scenarios.append(all_wins_scenario)

    result = []

    if must_win_scenarios:
        prob = sum(sr["scenario_prob"] for sr in must_win_scenarios)
        result.append(
            {
                "label": SCENARIO_MUST_WIN,
                "trigger": must_win_trigger or "赢下全部剩余比赛 → 确保前二出线",
                "resulting_position": "top2_qualified",
                "prob": round(prob, 4),
            }
        )

    if secured:
        prob = sum(sr["scenario_prob"] for sr in secured)
        result.append(
            {
                "label": SCENARIO_SECURED,
                "trigger": "已确保出线（所有结果都是前二）",
                "resulting_position": "top2_qualified",
                "prob": round(prob, 4),
            }
        )

    if danger:
        prob = sum(sr["scenario_prob"] for sr in danger)
        triggers = _describe_danger_triggers(team, team_matches, danger)
        result.append(
            {
                "label": SCENARIO_DANGER,
                "trigger": triggers,
                "resulting_position": "3rd_may_qualify",
                "prob": round(prob, 4),
            }
        )

    if eliminated:
        prob = sum(sr["scenario_prob"] for sr in eliminated)
        triggers = _describe_eliminated_triggers(team, team_matches, eliminated)
        result.append(
            {
                "label": SCENARIO_ELIMINATED,
                "trigger": triggers,
                "resulting_position": "eliminated",
                "prob": round(prob, 4),
            }
        )

    if normal:
        prob = sum(sr["scenario_prob"] for sr in normal)
        result.append(
            {
                "label": SCENARIO_NORMAL,
                "trigger": "出线取决于具体赛果",
                "resulting_position": "top2_qualified",
                "prob": round(prob, 4),
            }
        )

    # Ensure at least one scenario
    if not result:
        result.append(
            {
                "label": SCENARIO_NORMAL,
                "trigger": "出线取决于具体赛果",
                "resulting_position": "top2_qualified",
                "prob": round(overall_qual_prob, 4),
            }
        )

    return result


def _describe_danger_triggers(
    team: str, team_matches: list[dict], danger_scenarios: list[dict]
) -> str:
    """Generate human-readable trigger for danger scenarios."""
    if not danger_scenarios:
        return "N/A"

    # Find most common pattern in danger scenarios
    loss_counts = Counter()
    for sr in danger_scenarios:
        for i, o in enumerate(sr["outcomes"]):
            if o == "L":
                opp = (
                    team_matches[i]["away"]
                    if team_matches[i]["home"] == team
                    else team_matches[i]["home"]
                )
                loss_counts[opp] += 1

    if loss_counts:
        most_dangerous = loss_counts.most_common(1)[0][0]
        return f"输给 {team_zh(most_dangerous)} → 出线危险（27 种情况中有 {len(danger_scenarios)} 种不利）"
    return f"27 种情况中有 {len(danger_scenarios)} 种 → 出线概率 20-50%"


def _describe_eliminated_triggers(
    team: str, team_matches: list[dict], elim_scenarios: list[dict]
) -> str:
    """Generate human-readable trigger for eliminated scenarios."""
    if not elim_scenarios:
        return "N/A"

    # Check if all-losses is among eliminated
    for sr in elim_scenarios:
        if sr["outcomes"] == ["L", "L", "L"]:
            return "小组赛三场全负 → 淘汰"

    # Describe worst case
    max_losses = max(sr["outcomes"].count("L") for sr in elim_scenarios)
    return f"输 {max_losses}+ 场 → 淘汰（27 种情况中有 {len(elim_scenarios)} 种）"


def _compute_key_matches(
    team_matches: list[dict],
    win_qual_weight: dict[int, float],
    lose_qual_weight: dict[int, float],
    win_total_weight: dict[int, float],
    lose_total_weight: dict[int, float],
    team: str = "",
) -> list[dict]:
    """Compute match impact: swing in qual_prob between winning and losing."""
    impacts = []
    for mi, m in enumerate(team_matches):
        w_total = win_total_weight.get(mi, 0.0)
        l_total = lose_total_weight.get(mi, 0.0)
        if w_total > 0 and l_total > 0:
            w_rate = win_qual_weight.get(mi, 0.0) / w_total
            l_rate = lose_qual_weight.get(mi, 0.0) / l_total
            impact = abs(w_rate - l_rate)
            opponent = m["away"] if m["home"] == team else m["home"]

            impacts.append(
                {
                    "match_id": m["match_id"],
                    "opponent": opponent,
                    "impact": round(impact, 4),
                }
            )

    # Sort by impact descending
    impacts.sort(key=lambda x: x["impact"], reverse=True)
    return impacts


# ---------------------------------------------------------------------------
# Cross-group third-place comparison
# ---------------------------------------------------------------------------


def compute_third_place_qual_probs(
    all_qualifications: list[TeamQualification],
) -> None:
    """Compute third-place qualification probabilities via cross-group comparison.

    8 of 12 third-placed teams advance. We estimate each group's 3rd-place
    team's probability of being in the top 8 by comparing p_3rd values and
    expected third-place strength across groups.

    Method: Rank groups by their teams' average Elo strength as a proxy for
    3rd-place quality. Stronger groups → stronger 3rd-place team → more likely
    to be in top 8. Simpler approach: use p_3rd probability and a heuristic
    based on group strength.
    """
    # Collect per-group 3rd-place probability
    group_p3rd = {}
    for q in all_qualifications:
        if q.group not in group_p3rd:
            group_p3rd[q.group] = q.position_probs.get("p_3rd", 0)

    # Heuristic: groups where p_3rd is spread out suggest competitive groups
    # with stronger 3rd-place teams. Groups where p_3rd is concentrated on
    # one team suggest a clear 3rd-place finisher.
    #
    # For now, use a simple proportional model:
    # If 12 groups produce 12 third-place teams, 8 advance.
    # P(3rd-team advances) ≈ rank within 12 third-place teams.
    #
    # We approximate using the team's qual_prob and p_3rd:
    # third_place_qual_prob = P(top 2) is already in qual_prob
    # We need: P(team is 3rd AND in top-8 thirds)
    #
    # Simple approach: assume each group's 3rd-place team has equal
    # chance to be in top 8 → 8/12 ≈ 0.667
    # Better: weight by group strength (average qual_prob of group's top 2)

    # F-12: precompute group average qual_prob as group strength metric
    group_avg_qual: dict[str, float] = {}
    group_counts: dict[str, int] = {}
    for q in all_qualifications:
        g = q.group
        group_avg_qual[g] = group_avg_qual.get(g, 0.0) + q.qual_prob
        group_counts[g] = group_counts.get(g, 0) + 1
    for g in group_avg_qual:
        group_avg_qual[g] /= max(group_counts.get(g, 1), 1)

    for q in all_qualifications:
        p3 = q.position_probs.get("p_3rd", 0)
        if p3 < 0.01:
            q.third_place_qual_prob = None
        else:
            # Base rate: 8 of 12 third-place teams advance
            base_rate = 8.0 / 12.0
            # F-12: Adjust by group average qual_prob as group strength proxy.
            # Stronger groups produce stronger 3rd-place teams → higher
            # probability of advancing among the best-8 thirds.
            strength_adj = 0.1 * (group_avg_qual.get(q.group, 0.5) - 0.5)
            tp_prob = max(0.0, min(1.0, base_rate + strength_adj))
            q.third_place_qual_prob = round(tp_prob, 4)


def add_third_place_to_qual_prob(
    all_qualifications: list[TeamQualification],
) -> None:
    """Add third-place qualification probability to overall qual_prob.

    qual_prob = P(top 2) + P(3rd) * P(best 8 thirds | 3rd)
    """
    for q in all_qualifications:
        p3 = q.position_probs.get("p_3rd", 0)
        tp = q.third_place_qual_prob or 0
        top2_prob = q.position_probs.get("p_1st", 0) + q.position_probs.get("p_2nd", 0)
        # F-04: preserve original top-2 probability for downstream consumers
        q.qual_prob_top2 = round(top2_prob, 4)
        q.qual_prob = round(top2_prob + p3 * tp, 4)  # total qualification probability
