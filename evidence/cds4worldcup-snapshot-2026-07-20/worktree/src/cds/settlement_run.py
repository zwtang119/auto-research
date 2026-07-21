"""Settlement helper for CDS qualification + championship (group-stage phase).

Produces a single JSON artifact with:
  - per-group final standings (1st-4th)
  - list of advanced teams (top 2 + best 8 third-place)
  - list of eliminated teams (16)
  - per-team actual vs predicted qualification/championship outcomes
  - qualification Brier (48 teams)
  - partial championship Brier (16 eliminated teams)

This is read-only: it consumes existing data/processed/{schedule,cds_qualification,
cds_championship}.json plus data/processed/team_registry.csv and writes a JSON
artifact under results/ops/ for downstream report generation.

The actual group standings are computed from the 72 played matches using the
existing src.cds.group_standings.compute_group_standings (FIFA 2026 multi-team
tiebreaker protocol). Third-place rankings follow FIFA's published rule:
8 of 12 third-placed teams advance; ranking criterion is points → GD → GF →
goals scored in all group matches → fair-play (we do not model fair-play for
the settled actual).

Usage (from project root):
    python3 -m src.cds.settlement_run
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from src.cds.group_standings import MatchResult, Standing, compute_group_standings

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_PATH = PROJECT_ROOT / "data" / "processed" / "schedule.json"
QUAL_PATH = PROJECT_ROOT / "data" / "processed" / "cds_qualification.json"
CHAMP_PATH = PROJECT_ROOT / "data" / "processed" / "cds_championship.json"
REGISTRY_PATH = PROJECT_ROOT / "data" / "processed" / "team_registry.csv"
OUTPUT_PATH = PROJECT_ROOT / "results" / "ops" / "cds-settlement-2026-07-08.json"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_schedule() -> dict:
    with open(SCHEDULE_PATH) as f:
        return json.load(f)


def _load_qual() -> dict:
    with open(QUAL_PATH) as f:
        return json.load(f)


def _load_champ() -> dict:
    with open(CHAMP_PATH) as f:
        return json.load(f)


def _load_registry() -> dict[str, str]:
    """Return {en_name: confederation} from team_registry.csv."""
    out: dict[str, str] = {}
    with open(REGISTRY_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["en_name"]] = row["confederation"]
    return out


def _build_group_results(schedule: dict) -> dict[str, list[MatchResult]]:
    """Return {group_letter: [6 MatchResult]} for every group."""
    out: dict[str, list[MatchResult]] = {}
    groups = schedule["group_stage"]["groups"]
    for letter in sorted(groups):
        matches = [
            MatchResult(
                home=m["home_team"],
                away=m["away_team"],
                home_goals=int(m["home_score"]),
                away_goals=int(m["away_score"]),
            )
            for m in groups[letter]["matches"]
        ]
        # Sanity: only operated on played matches
        for m in matches:
            assert m.home_goals is not None and m.away_goals is not None
        if len(matches) != 6:
            raise ValueError(f"Group {letter} has {len(matches)} matches, expected 6")
        out[letter] = matches
    return out


def _group_teams(schedule: dict) -> dict[str, list[str]]:
    """Return {group_letter: [4 team names]}."""
    groups = schedule["group_stage"]["groups"]
    return {
        letter: [t["name"] for t in groups[letter]["teams"]]
        for letter in sorted(groups)
    }


# ---------------------------------------------------------------------------
# Standings / qualifier computation
# ---------------------------------------------------------------------------


@dataclass
class GroupOutcome:
    letter: str
    standings: list[dict]  # [{team, position, points, gd, gf, ga, note}]
    top2: list[str]        # 1st, 2nd
    third: str             # 3rd-placed
    fourth: list[str]


def _compute_all_group_outcomes(schedule: dict) -> dict[str, GroupOutcome]:
    group_results = _build_group_results(schedule)
    teams_by_group = _group_teams(schedule)
    out: dict[str, GroupOutcome] = {}
    for letter in sorted(group_results):
        teams = teams_by_group[letter]
        results = group_results[letter]
        # Use a fixed lots seed for determinism. Fair-play data unavailable.
        standings: list[Standing] = compute_group_standings(
            teams, results, lots_seed=20260708
        )
        sdicts = [
            {
                "team": s.team,
                "position": s.position,
                "points": s.points,
                "gd": s.goal_diff,
                "gf": s.goals_for,
                "ga": s.goals_against,
                "note": s.tiebreaker_note,
            }
            for s in standings
        ]
        # Top 2 = position 1 and 2. 3rd = first team with position 3.
        top2 = [s.team for s in standings if s.position in (1, 2)]
        third = next(s.team for s in standings if s.position == 3)
        fourth = [s.team for s in standings if s.position == 4]
        out[letter] = GroupOutcome(
            letter=letter, standings=sdicts, top2=top2, third=third, fourth=fourth
        )
    return out


def _rank_thirds(outcomes: dict[str, GroupOutcome]) -> list[tuple[str, str, dict]]:
    """Return [(group, team, standing_dict)] sorted by FIFA best-3rd ranking.

    FIFA ranks 3rd-placed teams by (descending):
      1. points
      2. goal difference
      3. goals scored
      4. goals conceded (ascending — lower is better)
      5. fair-play (not modelled here — no equality expected to remain)
      6. drawing of lots (deterministic via position 3's standing order)

    Note: When two 3rd-placed teams are still tied after points/GD/GF/GA, FIFA's
    actual protocol uses fair-play then drawing of lots. We do not model
    fair-play; if a tie remains we break by drawing order from the group's
    own tiebreaker note (which already incorporated mini-league logic). That is
    consistent with the deterministic seed used at the group-standings call.
    """
    rows: list[tuple[str, str, dict]] = []
    for letter, o in outcomes.items():
        third_row = next(s for s in o.standings if s["position"] == 3)
        rows.append((letter, third_row["team"], third_row))
    # Sort: points DESC, gd DESC, gf DESC, ga ASC
    rows.sort(
        key=lambda r: (-r[2]["points"], -r[2]["gd"], -r[2]["gf"], r[2]["ga"])
    )
    return rows


@dataclass
class QualifierResult:
    advanced: list[str]          # 32 teams
    eliminated: list[str]        # 16 teams
    best_eight_thirds: list[tuple[str, str]]  # [(group, team)]
    per_group_top2: dict[str, list[str]]
    per_group_third: dict[str, str]
    per_group_fourth: dict[str, str]


def _determine_qualifiers(outcomes: dict[str, GroupOutcome]) -> QualifierResult:
    top2_set: set[str] = set()
    per_group_top2: dict[str, list[str]] = {}
    per_group_third: dict[str, str] = {}
    per_group_fourth: dict[str, str] = {}

    for letter, o in outcomes.items():
        per_group_top2[letter] = o.top2
        per_group_third[letter] = o.third
        # 4th = the one team with position 4 (only ever one)
        fourth_team = next(s["team"] for s in o.standings if s["position"] == 4)
        per_group_fourth[letter] = fourth_team
        top2_set.update(o.top2)

    # Best 8 third-placed teams
    ranked_thirds = _rank_thirds(outcomes)
    best_eight = ranked_thirds[:8]
    worst_four = ranked_thirds[8:]

    advanced = list(top2_set) + [t for _, t, _ in best_eight]
    advanced_set = set(advanced)
    # All 48 teams minus 32 advanced = 16 eliminated
    all_teams = sorted({t for _, o in outcomes.items() for s in o.standings for t in [s["team"]]})
    eliminated = [t for t in all_teams if t not in advanced_set]

    return QualifierResult(
        advanced=sorted(advanced),
        eliminated=sorted(eliminated),
        best_eight_thirds=[(g, t) for g, t, _ in best_eight],
        per_group_top2=per_group_top2,
        per_group_third=per_group_third,
        per_group_fourth=per_group_fourth,
    )


# ---------------------------------------------------------------------------
# Brier scores
# ---------------------------------------------------------------------------


def _brier(probs: Iterable[float], outcomes: Iterable[int]) -> tuple[float, list[float]]:
    """Return (mean_brier, per_observation_scores)."""
    per = [(p - o) ** 2 for p, o in zip(probs, outcomes)]
    n = len(per)
    mean = sum(per) / n if n else 0.0
    return mean, per


def _build_per_team_rows(
    qual_data: dict,
    champ_data: dict,
    qualifiers: QualifierResult,
) -> list[dict]:
    """Per-team settlement row combining actual outcome + predicted probabilities."""
    advanced_set = set(qualifiers.advanced)
    qual_by_team = {t["team"]: t for t in qual_data["teams"]}
    champ_by_team = {t["team"]: t for t in champ_data["teams"]}
    rows: list[dict] = []
    for team in sorted(qual_by_team):
        q = qual_by_team[team]
        c = champ_by_team.get(team, {})
        actual_qual = 1 if team in advanced_set else 0
        rows.append(
            {
                "team": team,
                "group": q["group"],
                "actual_qualified_top2_or_best3": actual_qual,
                "qual_prob_top2_pred": q.get("qual_prob_top2"),
                "qual_prob_pred_total": q.get("qual_prob"),
                "championship_prob_pred": c.get("championship_prob"),
                "brier_qual_top2": (q.get("qual_prob_top2") - actual_qual) ** 2
                if q.get("qual_prob_top2") is not None else None,
                "brier_championship_partial": (c.get("championship_prob")) ** 2
                if (team not in advanced_set and c.get("championship_prob") is not None)
                else None,
            }
        )
    return rows


def _aggregate_by(rows: list[dict], key: str, score_key: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    grouped: dict[str, list[dict]] = {}
    for r in rows:
        grouped.setdefault(r[key], []).append(r)
    for k, items in grouped.items():
        scores = [r[score_key] for r in items if r[score_key] is not None]
        out[k] = {
            "n": len(items),
            "n_settled": len(scores),
            "mean_score": sum(scores) / len(scores) if scores else None,
        }
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    schedule = _load_schedule()
    qual_data = _load_qual()
    champ_data = _load_champ()
    registry = _load_registry()

    outcomes = _compute_all_group_outcomes(schedule)
    qualifiers = _determine_qualifiers(outcomes)

    # Qualification Brier on top2 qual_prob_top2 (single binary outcome)
    rows = _build_per_team_rows(qual_data, champ_data, qualifiers)
    qual_brier, _ = _brier(
        [r["qual_prob_top2_pred"] for r in rows if r["qual_prob_top2_pred"] is not None],
        [r["actual_qualified_top2_or_best3"] for r in rows if r["qual_prob_top2_pred"] is not None],
    )
    qual_total = [r["qual_prob_top2_pred"] for r in rows if r["qual_prob_top2_pred"] is not None]

    # Partial championship Brier on the 16 eliminated teams only
    champ_scores = [r["brier_championship_partial"] for r in rows if r["brier_championship_partial"] is not None]
    partial_champ_brier = sum(champ_scores) / len(champ_scores) if champ_scores else None

    # Aggregations
    by_group = _aggregate_by(rows, "group", "brier_qual_top2")
    by_group_champ = _aggregate_by(rows, "group", "brier_championship_partial")

    # Confederation-level
    rows_with_conf = [{**r, "confederation": registry.get(r["team"], "UNKNOWN")} for r in rows]
    by_confederation = _aggregate_by(rows_with_conf, "confederation", "brier_qual_top2")
    by_confederation_champ = _aggregate_by(rows_with_conf, "confederation", "brier_championship_partial")

    artifact = {
        "generated_at_utc": "2026-07-08T00:00:00Z",
        "settlement_scope": "group_stage_72_matches_complete_2026-06-11_to_2026-06-27",
        "qualification": {
            "n_advanced": len(qualifiers.advanced),
            "n_eliminated": len(qualifiers.eliminated),
            "best_eight_thirds": [
                {"group": g, "team": t} for g, t in qualifiers.best_eight_thirds
            ],
            "advanced_teams": qualifiers.advanced,
            "eliminated_teams": qualifiers.eliminated,
            "per_group": {
                letter: {
                    "standings": o.standings,
                    "top2": o.top2,
                    "third": o.third,
                    "fourth": next(s["team"] for s in o.standings if s["position"] == 4),
                }
                for letter, o in outcomes.items()
            },
            "brier": {
                "mean": qual_brier,
                "n": len(qual_total),
                "by_group": by_group,
                "by_confederation": by_confederation,
            },
        },
        "championship_partial": {
            "scope": "16 group-stage-eliminated teams only",
            "n_settled": len(champ_scores),
            "brier_mean": partial_champ_brier,
            "by_group": by_group_champ,
            "by_confederation": by_confederation_champ,
            "pending_note": (
                "32 teams (top 2 of each group + best 8 of 12 third-placed teams) remain "
                "in the knockout bracket. Their championship_prob cannot be settled until "
                "the tournament concludes."
            ),
        },
        "per_team_rows": rows_with_conf,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(artifact, f, indent=2)

    # Summary print for the agent log
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Qualification Brier (top2 48-team): {qual_brier:.4f}")
    print(f"Championship partial Brier (16 eliminated): {partial_champ_brier:.4f}")
    print(f"Advanced: {len(qualifiers.advanced)}, Eliminated: {len(qualifiers.eliminated)}")
    print(f"Eliminated teams: {qualifiers.eliminated}")


if __name__ == "__main__":
    main()
