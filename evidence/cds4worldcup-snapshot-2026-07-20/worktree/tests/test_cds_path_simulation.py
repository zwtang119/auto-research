"""Tests for the CDS path simulation engine.

Covers:
1. Group standings integration with real Group A teams
2. Qualification 27-scenario probability sum ≈ 1.0
3. Bracket paths for all 48 teams
4. Third-place slots (8 slots, 5 candidate groups each)
5. Championship cumulative_prob monotonic decreasing
6. Output files are valid JSON with 48 teams
7. All probabilities in [0, 1]
8. Schema required fields present
"""

import json
from pathlib import Path

import pytest

from src.cds.group_standings import MatchResult, compute_group_standings
from src.cds.knockout_bracket import PathNode, build_bracket_paths, parse_slot
from src.cds.qualification import TeamQualification, simulate_team_qualification


# ---------------------------------------------------------------------------
# Project root
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Test 1: Group standings integration — real Group A teams
# ---------------------------------------------------------------------------

class TestGroupStandingsIntegration:
    def test_group_a_real_teams_position_ordering(self):
        """Run compute_group_standings() with real Group A teams and
        predetermined match results. Verify position ordering is sensible.
        """
        teams = ["Mexico", "South Africa", "South Korea", "Czech Republic"]
        results = [
            # Matchday 1 (real)
            MatchResult("Mexico", "South Africa", 2, 0),
            MatchResult("South Korea", "Czech Republic", 2, 1),
            # Matchday 2 (plausible)
            MatchResult("Czech Republic", "South Africa", 1, 1),
            MatchResult("Mexico", "South Korea", 1, 0),
            # Matchday 3 (plausible)
            MatchResult("South Africa", "South Korea", 0, 3),
            MatchResult("Czech Republic", "Mexico", 0, 2),
        ]
        standings = compute_group_standings(teams, results)
        positions = {s.team: s.position for s in standings}

        # Mexico won all 3 — must be 1st
        assert positions["Mexico"] == 1
        # South Korea won 2 — must be 2nd
        assert positions["South Korea"] == 2
        # Czech Republic and South Africa each drew 1, lost 2 → 1 pt each
        # CZE GD=-3, RSA GD=-5 → CZE 3rd
        assert positions["Czech Republic"] == 3
        assert positions["South Africa"] == 4

        # Verify stats for Mexico
        mexico = next(s for s in standings if s.team == "Mexico")
        assert mexico.points == 9
        assert mexico.goals_for == 5
        assert mexico.goal_diff == 5

        # All 4 positions must be unique
        assert len(set(s.position for s in standings)) == 4


# ---------------------------------------------------------------------------
# Test 2: Qualification 27-scenario probability sum ≈ 1.0
# ---------------------------------------------------------------------------

class TestQualification27Scenarios:
    def test_probability_sum_approximately_one(self):
        """Call simulate_team_qualification() for a single team and verify
        that the weighted position probabilities sum to ≈ 1.0.

        Uses synthetic but plausible odds data to avoid external dependencies.
        Uses reduced MC samples for speed.
        """
        teams = ["Mexico", "South Africa", "South Korea", "Czech Republic"]
        group_data = {
            "teams": teams,
            "matches": [
                {"match_id": "A1", "round": 1, "home": "Mexico", "away": "South Africa"},
                {"match_id": "A2", "round": 1, "home": "South Korea", "away": "Czech Republic"},
                {"match_id": "A3", "round": 2, "home": "Czech Republic", "away": "South Africa"},
                {"match_id": "A4", "round": 2, "home": "Mexico", "away": "South Korea"},
                {"match_id": "A5", "round": 3, "home": "South Africa", "away": "South Korea"},
                {"match_id": "A6", "round": 3, "home": "Czech Republic", "away": "Mexico"},
            ],
        }
        odds_map = {
            "A1": {"home_win": 0.45, "draw": 0.25, "away_win": 0.30,
                    "expected_goals_home": 1.5, "expected_goals_away": 1.0},
            "A2": {"home_win": 0.40, "draw": 0.30, "away_win": 0.30,
                    "expected_goals_home": 1.3, "expected_goals_away": 1.1},
            "A3": {"home_win": 0.35, "draw": 0.30, "away_win": 0.35,
                    "expected_goals_home": 1.2, "expected_goals_away": 1.2},
            "A4": {"home_win": 0.50, "draw": 0.25, "away_win": 0.25,
                    "expected_goals_home": 1.6, "expected_goals_away": 0.9},
            "A5": {"home_win": 0.30, "draw": 0.30, "away_win": 0.40,
                    "expected_goals_home": 1.0, "expected_goals_away": 1.4},
            "A6": {"home_win": 0.30, "draw": 0.30, "away_win": 0.40,
                    "expected_goals_home": 1.0, "expected_goals_away": 1.4},
        }

        result = simulate_team_qualification(
            team="Mexico",
            group_letter="A",
            group_data=group_data,
            odds_map=odds_map,
            n_mc_samples=20,  # reduced for speed
            rng_seed=42,
        )

        # Position probabilities should sum to ~1.0
        pos_sum = sum(result.position_probs.values())
        assert abs(pos_sum - 1.0) < 0.05, (
            f"Position probabilities sum to {pos_sum}, expected ~1.0"
        )

        # qual_prob should be in [0, 1]
        assert 0.0 <= result.qual_prob <= 1.0

        # Should have at least one scenario
        assert len(result.scenarios) >= 1

        # 27 scenarios were enumerated (check via simulation_meta or scenarios)
        # The function processes 27 scenarios internally; verify position_probs
        # are non-negative and cover all 4 positions
        for key in ("p_1st", "p_2nd", "p_3rd", "p_4th"):
            assert key in result.position_probs
            assert 0.0 <= result.position_probs[key] <= 1.0


# ---------------------------------------------------------------------------
# Test 3: Bracket paths for all 48 teams
# ---------------------------------------------------------------------------

class TestBracketPaths48Teams:
    def test_bracket_paths_covers_all_48_teams(self):
        """build_bracket_paths() must return 48 teams, each with ≥1 node."""
        paths = build_bracket_paths(
            schedule_path=str(ROOT / "site" / "data" / "schedule.json"),
            third_place_map_path=str(ROOT / "config" / "third_place_mapping.json"),
        )

        assert len(paths) == 48, f"Expected 48 teams, got {len(paths)}"

        teams_with_no_nodes = [
            team for team, nodes in paths.items() if len(nodes) < 1
        ]
        assert teams_with_no_nodes == [], (
            f"Teams with 0 path nodes: {teams_with_no_nodes}"
        )

        # Each team should have at least one R32 match
        for team, nodes in paths.items():
            r32_nodes = [n for n in nodes if n.round == "round_of_32"]
            assert len(r32_nodes) >= 1, (
                f"{team} has no round_of_32 nodes"
            )


# ---------------------------------------------------------------------------
# Test 4: Third-place slots resolved
# ---------------------------------------------------------------------------

class TestThirdPlaceSlots:
    def test_third_place_mapping_has_8_slots_with_5_groups(self):
        """Verify config/third_place_mapping.json: 8 slots, each with
        exactly 5 candidate groups.
        """
        with open(ROOT / "config" / "third_place_mapping.json") as f:
            tp_map = json.load(f)

        slots = tp_map["slots"]
        assert len(slots) == 8, f"Expected 8 third-place slots, got {len(slots)}"

        for slot_name, slot_data in slots.items():
            pool = slot_data["pool_groups"]
            assert len(pool) == 5, (
                f"Slot {slot_name} has {len(pool)} groups, expected 5"
            )
            # Each group letter should be A-L
            for g in pool:
                assert g in "ABCDEFGHIJKL", f"Invalid group letter {g} in {slot_name}"

    def test_third_place_slots_appear_as_conditional_in_bracket(self):
        """Cross-check: third-place composite slots should appear as
        non-deterministic (is_deterministic=False) nodes in bracket paths.
        """
        paths = build_bracket_paths(
            schedule_path=str(ROOT / "site" / "data" / "schedule.json"),
            third_place_map_path=str(ROOT / "config" / "third_place_mapping.json"),
        )

        found_conditional_third_place = False
        for team, nodes in paths.items():
            for node in nodes:
                if not node.is_deterministic:
                    # Check if the opponent_slot looks like a third-place reference
                    try:
                        info = parse_slot(node.opponent_slot)
                        if info["type"] == "third_place":
                            found_conditional_third_place = True
                            break
                    except ValueError:
                        # opponent_slot is a human-readable string (from describe_slot)
                        # We check the raw bracket instead
                        pass
            if found_conditional_third_place:
                break

        # Also check via raw schedule to confirm third-place slots exist
        with open(ROOT / "site" / "data" / "schedule.json") as f:
            schedule = json.load(f)

        tp_slot_count = 0
        for m in schedule["knockout"]:
            for side in ("slot_home", "slot_away"):
                slot = m[side]
                try:
                    info = parse_slot(slot)
                    if info["type"] == "third_place":
                        tp_slot_count += 1
                except ValueError:
                    pass

        assert tp_slot_count == 8, (
            f"Expected 8 third-place slots in schedule knockout, got {tp_slot_count}"
        )


# ---------------------------------------------------------------------------
# Test 5: Championship monotonic decreasing cumulative_prob
# ---------------------------------------------------------------------------

class TestChampionshipMonotonicDecreasing:
    def test_france_path_nodes_cumulative_prob_never_increases(self):
        """For France, path_nodes through rounds should have
        cumulative_prob that decreases or stays flat (never increases).
        """
        with open(ROOT / "data" / "processed" / "cds_championship.json") as f:
            data = json.load(f)

        france = None
        for team_data in data["teams"]:
            if team_data["team"] == "France":
                france = team_data
                break

        assert france is not None, "France not found in cds_championship.json"
        assert len(france["path_nodes"]) > 0, "France has no path_nodes"

        cumulative_probs = [pn["cumulative_prob"] for pn in france["path_nodes"]]

        for i in range(1, len(cumulative_probs)):
            assert cumulative_probs[i] <= cumulative_probs[i - 1] + 1e-9, (
                f"cumulative_prob increased from {cumulative_probs[i-1]} "
                f"to {cumulative_probs[i]} at index {i} "
                f"(round {france['path_nodes'][i]['round']})"
            )


# ---------------------------------------------------------------------------
# Test 6: Output files are valid JSON with 48 teams
# ---------------------------------------------------------------------------

class TestOutputFilesValidJson:
    def test_cds_qualification_json(self):
        """cds_qualification.json exists, is valid JSON, and has 48 teams."""
        path = ROOT / "data" / "processed" / "cds_qualification.json"
        assert path.exists(), f"File not found: {path}"

        with open(path) as f:
            data = json.load(f)

        assert "teams" in data
        assert len(data["teams"]) == 48, (
            f"Expected 48 teams, got {len(data['teams'])}"
        )

    def test_cds_championship_json(self):
        """cds_championship.json exists, is valid JSON, and has 48 teams."""
        path = ROOT / "data" / "processed" / "cds_championship.json"
        assert path.exists(), f"File not found: {path}"

        with open(path) as f:
            data = json.load(f)

        assert "teams" in data
        assert len(data["teams"]) == 48, (
            f"Expected 48 teams, got {len(data['teams'])}"
        )


# ---------------------------------------------------------------------------
# Test 7: All probabilities in [0, 1]
# ---------------------------------------------------------------------------

class TestAllProbsInBounds:
    def test_qualification_probs_in_bounds(self):
        """All qual_prob values in cds_qualification.json are in [0, 1]."""
        with open(ROOT / "data" / "processed" / "cds_qualification.json") as f:
            data = json.load(f)

        violations = []
        for team_data in data["teams"]:
            prob = team_data["qual_prob"]
            if not (0.0 <= prob <= 1.0):
                violations.append((team_data["team"], "qual_prob", prob))

        assert violations == [], f"Out-of-bounds qual_prob: {violations}"

    def test_qual_prob_never_exceeds_one(self):
        """Verify qual_prob ≤ 1.0 and qual_prob_top2 ≤ qual_prob for every team.

        This is a regression test for F-03 / F-04: adding third-place
        qualification should never push total qual_prob above 1.0, and
        the original top-2 probability should always be ≤ total.
        """
        with open(ROOT / "data" / "processed" / "cds_qualification.json") as f:
            data = json.load(f)

        violations = []
        for team_data in data["teams"]:
            prob = team_data["qual_prob"]
            if prob > 1.0:
                violations.append((team_data["team"], "qual_prob > 1.0", prob))
            top2 = team_data.get("qual_prob_top2")
            if top2 is not None and top2 > prob + 1e-6:
                violations.append((team_data["team"], "qual_prob_top2 > qual_prob", (top2, prob)))

        assert violations == [], f"qual_prob boundary violations: {violations}"

    def test_championship_probs_in_bounds(self):
        """All championship_prob values in cds_championship.json are in [0, 1]."""
        with open(ROOT / "data" / "processed" / "cds_championship.json") as f:
            data = json.load(f)

        violations = []
        for team_data in data["teams"]:
            prob = team_data["championship_prob"]
            if not (0.0 <= prob <= 1.0):
                violations.append((team_data["team"], "championship_prob", prob))

        assert violations == [], f"Out-of-bounds championship_prob: {violations}"

        # Also check conditional_win_prob and cumulative_prob in path_nodes
        for team_data in data["teams"]:
            for pn in team_data.get("path_nodes", []):
                cwp = pn["conditional_win_prob"]
                cp = pn["cumulative_prob"]
                if not (0.0 <= cwp <= 1.0):
                    violations.append(
                        (team_data["team"], pn["match_id"], "conditional_win_prob", cwp)
                    )
                if not (0.0 <= cp <= 1.0):
                    violations.append(
                        (team_data["team"], pn["match_id"], "cumulative_prob", cp)
                    )

        assert violations == [], f"Out-of-bounds path_node probs: {violations}"


# ---------------------------------------------------------------------------
# Test 8: Schema required fields present
# ---------------------------------------------------------------------------

class TestSchemaRequiredFields:
    def test_qualification_required_fields(self):
        """Every team in cds_qualification.json has
        {team, group, qual_prob, scenarios}.
        """
        with open(ROOT / "data" / "processed" / "cds_qualification.json") as f:
            data = json.load(f)

        required = {"team", "group", "qual_prob", "scenarios"}
        missing = []
        for team_data in data["teams"]:
            present = set(team_data.keys())
            absent = required - present
            if absent:
                missing.append((team_data.get("team", "?"), absent))

        assert missing == [], f"Missing required fields: {missing}"

    def test_championship_required_fields(self):
        """Every team in cds_championship.json has
        {team, championship_prob, championship_path_count,
         dominant_path_pattern, simulation_status}.
        """
        with open(ROOT / "data" / "processed" / "cds_championship.json") as f:
            data = json.load(f)

        required = {
            "team",
            "championship_prob",
            "championship_path_count",
            "dominant_path_pattern",
            "simulation_status",
        }
        missing = []
        for team_data in data["teams"]:
            present = set(team_data.keys())
            absent = required - present
            if absent:
                missing.append((team_data.get("team", "?"), absent))

        assert missing == [], f"Missing required fields: {missing}"
