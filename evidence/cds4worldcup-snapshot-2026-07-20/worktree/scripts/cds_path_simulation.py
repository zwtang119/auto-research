#!/usr/bin/env python3
"""CDS Path Simulation Engine.

Usage:
    python3 scripts/cds_path_simulation.py --layer=qualification
    python3 scripts/cds_path_simulation.py --layer=qualification --team=Brazil
    python3 scripts/cds_path_simulation.py --layer=qualification --group=A

Outputs:
    data/processed/cds_qualification.json  (48 teams, per cds_qualification.schema.yaml)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.cds.qualification import (
    N_MC_SAMPLES,
    TeamQualification,
    add_third_place_to_qual_prob,
    build_group_schedule,
    compute_third_place_qual_probs,
    load_odds,
    load_schedule,
    load_team_registry,
    simulate_team_qualification,
)
from src.cds.championship import (
    TeamChampionship,
    championship_to_dict,
    compute_championship_paths,
)

# Paths (relative to project root)
SCHEDULE_PATH = PROJECT_ROOT / "site" / "data" / "schedule.json"
ODDS_PATH = PROJECT_ROOT / "site" / "data" / "odds.json"
TEAM_REGISTRY_PATH = PROJECT_ROOT / "data" / "processed" / "team_registry.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "cds_qualification.json"
CHAMPIONSHIP_OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "cds_championship.json"


def run_qualification_layer(
    team_filter: str | None = None,
    group_filter: str | None = None,
    n_mc_samples: int = N_MC_SAMPLES,
) -> list[dict]:
    """Run the qualification simulation layer.

    Args:
        team_filter: If set, only simulate this team.
        group_filter: If set, only simulate teams in this group.
        n_mc_samples: Monte Carlo samples per scenario.

    Returns:
        List of qualification dicts conforming to cds_qualification.schema.yaml.
    """
    print(f"[CDS] Loading data...")
    schedule = load_schedule(SCHEDULE_PATH)
    odds_map = load_odds(ODDS_PATH)
    teams_data = load_team_registry(TEAM_REGISTRY_PATH)
    group_schedule = build_group_schedule(schedule)

    # Build team → group mapping
    team_group = {}
    for row in teams_data:
        team_group[row["canonical_team"]] = row["group"]

    # Determine which teams to simulate
    all_teams = [row["canonical_team"] for row in teams_data]
    if team_filter:
        all_teams = [t for t in all_teams if t == team_filter]
    elif group_filter:
        all_teams = [t for t in all_teams if team_group.get(t) == group_filter.upper()]

    if not all_teams:
        print("[CDS] No teams to simulate. Check filter.")
        return []

    print(f"[CDS] Simulating qualification for {len(all_teams)} teams "
          f"({n_mc_samples} MC samples per scenario)...")

    qualifications: list[TeamQualification] = []
    start_time = time.time()

    for i, team in enumerate(all_teams):
        group_letter = team_group.get(team)
        if not group_letter:
            print(f"[CDS] WARNING: No group for {team}, skipping")
            continue

        group_data = group_schedule.get(group_letter)
        if not group_data:
            print(f"[CDS] WARNING: No schedule for group {group_letter}, skipping {team}")
            continue

        print(f"  [{i+1}/{len(all_teams)}] {team} (Group {group_letter})...", end=" ", flush=True)
        t0 = time.time()

        qual = simulate_team_qualification(
            team=team,
            group_letter=group_letter,
            group_data=group_data,
            odds_map=odds_map,
            n_mc_samples=n_mc_samples,
            rng_seed=42 + hash(team) % 10000,
        )
        qualifications.append(qual)
        elapsed = time.time() - t0
        print(f"qual_prob={qual.qual_prob:.3f} ({elapsed:.1f}s)")

    total_elapsed = time.time() - start_time
    print(f"[CDS] Simulation complete in {total_elapsed:.1f}s")

    # Cross-group third-place comparison
    print("[CDS] Computing third-place qualification probabilities...")
    compute_third_place_qual_probs(qualifications)
    add_third_place_to_qual_prob(qualifications)

    # Convert to output format
    now = datetime.now(timezone.utc)
    results = []
    for q in qualifications:
        entry = {
            "team": q.team,
            "group": q.group,
            "qual_prob": q.qual_prob,
            "qual_prob_top2": q.qual_prob_top2,  # F-04: original top-2 probability
            "scenarios": q.scenarios,
            "position_probs": q.position_probs,
            "third_place_qual_prob": q.third_place_qual_prob,
            "key_matches": q.key_matches,
            "simulation_meta": {
                "run_at_utc": now.isoformat(),
                "probability_source": "elo_poisson",
                "group_matches_completed": 0,
                "total_outcomes_enumerated": 27,
            },
        }
        results.append(entry)

    # Sort by group then qual_prob descending
    results.sort(key=lambda x: (x["group"], -x["qual_prob"]))

    return results


def main():
    parser = argparse.ArgumentParser(
        description="CDS Path Simulation Engine"
    )
    parser.add_argument(
        "--layer",
        required=True,
        choices=["qualification", "championship"],
        help="Simulation layer to run",
    )
    parser.add_argument(
        "--team",
        default=None,
        help="Simulate only this team (by canonical name)",
    )
    parser.add_argument(
        "--group",
        default=None,
        help="Simulate only this group (A-L)",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=N_MC_SAMPLES,
        help=f"Monte Carlo samples per scenario (default: {N_MC_SAMPLES})",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: data/processed/cds_qualification.json)",
    )

    args = parser.parse_args()

    if args.layer == "qualification":
        results = run_qualification_layer(
            team_filter=args.team,
            group_filter=args.group,
            n_mc_samples=args.samples,
        )

        if not results:
            print("[CDS] No results produced.")
            sys.exit(1)

        output_path = Path(args.output) if args.output else OUTPUT_PATH
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_data = {
            "schema_version": "0.1",
            "schema_type": "cds_qualification",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_teams": len(results),
            "teams": results,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\n[CDS] Output written to {output_path}")
        print(f"[CDS] {len(results)} teams, schema_version=0.1")

        # Quick summary
        quals = [r["qual_prob"] for r in results]
        print(f"[CDS] qual_prob range: {min(quals):.3f} – {max(quals):.3f}")
        high = [r["team"] for r in results if r["qual_prob"] >= 0.8]
        low = [r["team"] for r in results if r["qual_prob"] < 0.3]
        print(f"[CDS] High confidence (≥0.8): {len(high)} teams")
        print(f"[CDS] Low confidence (<0.3): {len(low)} teams")

    elif args.layer == "championship":
        champ_results = compute_championship_paths(
            team_filter=args.team,
            group_filter=args.group,
        )

        if not champ_results:
            print("[CDS] No championship results produced.")
            sys.exit(1)

        output_path = Path(args.output) if args.output else CHAMPIONSHIP_OUTPUT_PATH
        output_path.parent.mkdir(parents=True, exist_ok=True)

        now = datetime.now(timezone.utc)
        teams_data = [championship_to_dict(tc) for tc in champ_results]

        output_data = {
            "schema_version": "0.1",
            "schema_type": "cds_championship",
            "generated_at": now.isoformat(),
            "total_teams": len(teams_data),
            "teams": teams_data,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"\n[CDS] Championship output written to {output_path}")
        print(f"[CDS] {len(teams_data)} teams, schema_version=0.1")

        # Quick summary
        probs = [t["championship_prob"] for t in teams_data]
        print(f"[CDS] championship_prob range: {min(probs):.6f} – {max(probs):.6f}")
        top5 = sorted(teams_data, key=lambda x: -x["championship_prob"])[:5]
        print("[CDS] Top 5:")
        for t in top5:
            print(f"  {t['team']:25s} {t['championship_prob']:.4f}")


if __name__ == "__main__":
    main()
