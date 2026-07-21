#!/usr/bin/env python3
"""Backfill 30 played knockout-stage results into schedule.json's knockout_stage.

Source: Wikipedia 2026 FIFA World Cup knockout_stage page (Green Source, 2026-07-18).
Cross-checked: finalist pair (Spain vs Argentina, 2026-07-19) vs Final page.

This patches `home_team`/`away_team`/`home_code`/`away_code`/`status`/`home_score`/
`away_score` for the 30 KO matches played through the semi-finals (R32 16 + R16 8 +
QF 4 + SF 2). The final (KO104) and third-place (KO103) remain `scheduled` with
team slots resolved from the semi-final losers/winners where possible.

Idempotent: re-running only updates fields, never duplicates. Slot references
(`slot_home`/`slot_away`) are preserved unchanged for auditability.
"""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SCHED = REPO / "data" / "processed" / "schedule.json"

# team code map (subset needed for KO teams)
CODE = {
    "South Africa": "RSA", "Canada": "CAN", "Germany": "GER", "Paraguay": "PAR",
    "Brazil": "BRA", "Japan": "JPN", "Netherlands": "NED", "Morocco": "MAR",
    "Côte d'Ivoire": "CIV", "Norway": "NOR", "France": "FRA", "Sweden": "SWE",
    "Mexico": "MEX", "Ecuador": "ECU", "England": "ENG", "DR Congo": "COD",
    "Belgium": "BEL", "Senegal": "SEN", "United States": "USA",
    "Bosnia and Herzegovina": "BIH", "Spain": "ESP", "Austria": "AUT",
    "Portugal": "POR", "Croatia": "CRO", "Switzerland": "SUI", "Algeria": "ALG",
    "Australia": "AUS", "Egypt": "EGY", "Argentina": "ARG", "Cape Verde": "CPV",
    "Colombia": "COL", "Ghana": "GHA",
}

# KO results: match_num -> (home, away, hs, as, note)
# From Wikipedia 2026 FIFA World Cup knockout_stage page (Green Source, 2026-07-18).
# Penalties/aet noted; scores are 90-min (or aet) regulation scores.
KO_RESULTS = {
    73: ("South Africa", "Canada", 0, 1, ""),
    74: ("Germany", "Paraguay", 1, 1, "Paraguay won 4-3 on penalties"),
    75: ("Brazil", "Japan", 2, 1, ""),
    76: ("Netherlands", "Morocco", 1, 1, "Morocco won 3-2 on penalties"),
    77: ("Côte d'Ivoire", "Norway", 1, 2, ""),
    78: ("France", "Sweden", 3, 0, ""),
    79: ("Mexico", "Ecuador", 2, 0, ""),
    80: ("England", "DR Congo", 2, 1, ""),
    81: ("Belgium", "Senegal", 3, 2, "after extra time"),
    82: ("United States", "Bosnia and Herzegovina", 2, 0, ""),
    83: ("Spain", "Austria", 3, 0, ""),
    84: ("Portugal", "Croatia", 2, 1, ""),
    85: ("Switzerland", "Algeria", 2, 0, ""),
    86: ("Australia", "Egypt", 1, 1, "Egypt won 4-2 on penalties"),
    87: ("Argentina", "Cape Verde", 3, 2, "after extra time"),
    88: ("Colombia", "Ghana", 1, 0, ""),
    89: ("Canada", "Morocco", 0, 3, ""),
    90: ("Paraguay", "France", 0, 1, ""),
    91: ("Brazil", "Norway", 1, 2, ""),
    92: ("Mexico", "England", 2, 3, ""),
    93: ("Portugal", "Spain", 0, 1, ""),
    94: ("United States", "Belgium", 1, 4, ""),
    95: ("Argentina", "Egypt", 3, 2, ""),
    96: ("Switzerland", "Colombia", 0, 0, "Switzerland won 4-3 on penalties"),
    97: ("France", "Morocco", 2, 0, ""),
    98: ("Spain", "Belgium", 2, 1, ""),
    99: ("Norway", "England", 1, 2, "after extra time"),
    100: ("Argentina", "Switzerland", 3, 1, "after extra time"),
    101: ("Spain", "France", 2, 0, ""),
    102: ("Argentina", "England", 2, 1, ""),
}

# Final + third-place: resolve teams from SF results (still scheduled/pending final)
# KO103 third-place: RU101 (France) vs RU102 (England) -> teams known, match today 2026-07-18
# KO104 final: W101 (Spain) vs W102 (Argentina) -> teams known, match 2026-07-19
KO_PENDING_TEAMS = {
    103: ("France", "England"),   # third place, 2026-07-18
    104: ("Spain", "Argentina"),  # final, 2026-07-19
}


def main():
    with SCHED.open() as f:
        s = json.load(f)
    ko = s["knockout_stage"]
    updated = 0
    for m in ko:
        num = m["fifa_match_num"]
        if num in KO_RESULTS:
            home, away, hs, as_, note = KO_RESULTS[num]
            m["home_team"] = home
            m["away_team"] = away
            m["home_code"] = CODE.get(home)
            m["away_code"] = CODE.get(away)
            m["status"] = "played"
            m["home_score"] = hs
            m["away_score"] = as_
            if note:
                m["result_note"] = note
            updated += 1
        elif num in KO_PENDING_TEAMS:
            home, away = KO_PENDING_TEAMS[num]
            m["home_team"] = home
            m["away_team"] = away
            m["home_code"] = CODE.get(home)
            m["away_code"] = CODE.get(away)
            # status remains "scheduled"; teams resolved for display
    # update summary
    played = sum(1 for m in ko if m["status"] == "played")
    s["summary"]["knockout_stage_matches"] = len(ko)
    s["summary"]["knockout_played"] = played
    with SCHED.open("w") as f:
        json.dump(s, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated} KO matches to played (R32+R16+QF+SF).")
    print(f"Knockout played: {played}/32 (final + 3rd-place still scheduled with teams resolved).")


if __name__ == "__main__":
    main()
