#!/usr/bin/env python3
"""
parse_schedule.py — Parse FIFA World Cup 2026 schedule into structured JSON.

Reads:
  - data/ops/mimo_outputs/wiki-wc2026-draw.json (group compositions from Wikipedia)
  - Raw FIFA fixture data (embedded from fifa.com/scores-fixtures)

Outputs:
  - data/processed/schedule.json

Usage:
  python3 scripts/parse_schedule.py
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAW_JSON = ROOT / "data" / "ops" / "mimo_outputs" / "wiki-wc2026-draw.json"
SCHEDULE_CSV = ROOT / "data" / "processed" / "team_registry.csv"
OUTPUT_JSON = ROOT / "data" / "processed" / "schedule.json"

# ── Venue registry ───────────────────────────────────────
VENUES = {
    "Mexico City": {
        "stadium": "Estadio Azteca",
        "fifa_name": "Mexico City Stadium",
        "city": "Mexico City",
        "country": "Mexico",
        "timezone": "America/Mexico_City",
        "region": "Central",
    },
    "Guadalajara": {
        "stadium": "Estadio Akron",
        "fifa_name": "Guadalajara Stadium",
        "city": "Guadalajara",
        "country": "Mexico",
        "timezone": "America/Mexico_City",
        "region": "Central",
    },
    "Monterrey": {
        "stadium": "Estadio BBVA",
        "fifa_name": "Monterrey Stadium",
        "city": "Monterrey",
        "country": "Mexico",
        "timezone": "America/Monterrey",
        "region": "Central",
    },
    "Toronto": {
        "stadium": "BMO Field",
        "fifa_name": "Toronto Stadium",
        "city": "Toronto",
        "country": "Canada",
        "timezone": "America/Toronto",
        "region": "Eastern",
    },
    "Vancouver": {
        "stadium": "BC Place",
        "fifa_name": "BC Place Vancouver",
        "city": "Vancouver",
        "country": "Canada",
        "timezone": "America/Vancouver",
        "region": "Western",
    },
    "Los Angeles": {
        "stadium": "SoFi Stadium",
        "fifa_name": "Los Angeles Stadium",
        "city": "Inglewood, CA",
        "country": "United States",
        "timezone": "America/Los_Angeles",
        "region": "Western",
    },
    "San Francisco Bay Area": {
        "stadium": "Levi's Stadium",
        "fifa_name": "San Francisco Bay Area Stadium",
        "city": "Santa Clara, CA",
        "country": "United States",
        "timezone": "America/Los_Angeles",
        "region": "Western",
    },
    "Seattle": {
        "stadium": "Lumen Field",
        "fifa_name": "Seattle Stadium",
        "city": "Seattle, WA",
        "country": "United States",
        "timezone": "America/Los_Angeles",
        "region": "Western",
    },
    "Dallas": {
        "stadium": "AT&T Stadium",
        "fifa_name": "Dallas Stadium",
        "city": "Arlington, TX",
        "country": "United States",
        "timezone": "America/Chicago",
        "region": "Central",
    },
    "Houston": {
        "stadium": "NRG Stadium",
        "fifa_name": "Houston Stadium",
        "city": "Houston, TX",
        "country": "United States",
        "timezone": "America/Chicago",
        "region": "Central",
    },
    "Kansas City": {
        "stadium": "Arrowhead Stadium",
        "fifa_name": "Kansas City Stadium",
        "city": "Kansas City, MO",
        "country": "United States",
        "timezone": "America/Chicago",
        "region": "Central",
    },
    "Atlanta": {
        "stadium": "Mercedes-Benz Stadium",
        "fifa_name": "Atlanta Stadium",
        "city": "Atlanta, GA",
        "country": "United States",
        "timezone": "America/New_York",
        "region": "Eastern",
    },
    "Miami": {
        "stadium": "Hard Rock Stadium",
        "fifa_name": "Miami Stadium",
        "city": "Miami Gardens, FL",
        "country": "United States",
        "timezone": "America/New_York",
        "region": "Eastern",
    },
    "Boston": {
        "stadium": "Gillette Stadium",
        "fifa_name": "Boston Stadium",
        "city": "Foxborough, MA",
        "country": "United States",
        "timezone": "America/New_York",
        "region": "Eastern",
    },
    "Philadelphia": {
        "stadium": "Lincoln Financial Field",
        "fifa_name": "Philadelphia Stadium",
        "city": "Philadelphia, PA",
        "country": "United States",
        "timezone": "America/New_York",
        "region": "Eastern",
    },
    "New Jersey": {
        "stadium": "MetLife Stadium",
        "fifa_name": "New York/New Jersey Stadium",
        "city": "East Rutherford, NJ",
        "country": "United States",
        "timezone": "America/New_York",
        "region": "Eastern",
    },
}

# Map alternative city names to canonical keys
CITY_ALIASES = {
    "San Francisco": "San Francisco Bay Area",
    "New York/New Jersey": "New Jersey",
}

# ── FIFA country code → canonical team name ──────────────
FIFA_CODE_MAP = {
    "MEX": "Mexico", "RSA": "South Africa", "KOR": "South Korea", "CZE": "Czech Republic",
    "CAN": "Canada", "BIH": "Bosnia and Herzegovina", "QAT": "Qatar", "SUI": "Switzerland",
    "BRA": "Brazil", "MAR": "Morocco", "HAI": "Haiti", "SCO": "Scotland",
    "USA": "United States", "PAR": "Paraguay", "AUS": "Australia", "TUR": "Turkey",
    "GER": "Germany", "CUW": "Curaçao", "CIV": "Côte d'Ivoire", "ECU": "Ecuador",
    "NED": "Netherlands", "JPN": "Japan", "SWE": "Sweden", "TUN": "Tunisia",
    "BEL": "Belgium", "EGY": "Egypt", "IRN": "Iran", "NZL": "New Zealand",
    "ESP": "Spain", "CPV": "Cape Verde", "KSA": "Saudi Arabia", "URU": "Uruguay",
    "FRA": "France", "SEN": "Senegal", "IRQ": "Iraq", "NOR": "Norway",
    "ARG": "Argentina", "ALG": "Algeria", "AUT": "Austria", "JOR": "Jordan",
    "POR": "Portugal", "COD": "DR Congo", "UZB": "Uzbekistan", "COL": "Colombia",
    "ENG": "England", "CRO": "Croatia", "GHA": "Ghana", "PAN": "Panama",
}

# Reverse lookup: team name -> FIFA code (for backfilling KO team slots from names).
CODE_LOOKUP = {name: code for code, name in FIFA_CODE_MAP.items()}

# ── Knockout stage verified results (Green Source: Wikipedia knockout_stage page) ──
# Entered 2026-07-18 (R32→SF, 30 matches) + 2026-07-19 (final/third-place pending).
# match_num -> (home_team, away_team, home_score, away_score, result_note)
# Scores are 90-min (or aet) regulation scores; penalties noted in result_note.
KO_RESULTS = {
    # Round of 32 (73-88)
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
    # Round of 16 (89-96)
    89: ("Canada", "Morocco", 0, 3, ""),
    90: ("Paraguay", "France", 0, 1, ""),
    91: ("Brazil", "Norway", 1, 2, ""),
    92: ("Mexico", "England", 2, 3, ""),
    93: ("Portugal", "Spain", 0, 1, ""),
    94: ("United States", "Belgium", 1, 4, ""),
    95: ("Argentina", "Egypt", 3, 2, ""),
    96: ("Switzerland", "Colombia", 0, 0, "Switzerland won 4-3 on penalties"),
    # Quarterfinals (97-100)
    97: ("France", "Morocco", 2, 0, ""),
    98: ("Spain", "Belgium", 2, 1, ""),
    99: ("Norway", "England", 1, 2, "after extra time"),
    100: ("Argentina", "Switzerland", 3, 1, "after extra time"),
    # Semifinals (101-102)
    101: ("Spain", "France", 2, 0, ""),
    102: ("Argentina", "England", 2, 1, ""),
}

# Knockout matches still pending as of generation: teams resolved from SF
# results but match not yet played. match_num -> (home_team, away_team).
# KO103 third-place (RU101 vs RU102 = France vs England) and KO104 final
# (W101 vs W102 = Spain vs Argentina).
KO_PENDING_TEAMS = {
    103: ("France", "England"),   # third place
    104: ("Spain", "Argentina"),  # final
}

# ── Group compositions from Wikipedia draw ───────────────
# Positions: 1 = Pot 1 seed, 2 = Pot 2, 3 = Pot 3, 4 = Pot 4
GROUPS = {
    "A": ["MEX", "RSA", "KOR", "CZE"],
    "B": ["CAN", "BIH", "QAT", "SUI"],
    "C": ["BRA", "MAR", "HAI", "SCO"],
    "D": ["USA", "PAR", "AUS", "TUR"],
    "E": ["GER", "CUW", "CIV", "ECU"],
    "F": ["NED", "JPN", "SWE", "TUN"],
    "G": ["BEL", "EGY", "IRN", "NZL"],
    "H": ["ESP", "CPV", "KSA", "URU"],
    "I": ["FRA", "SEN", "IRQ", "NOR"],
    "J": ["ARG", "ALG", "AUT", "JOR"],
    "K": ["POR", "COD", "UZB", "COL"],
    "L": ["ENG", "CRO", "GHA", "PAN"],
}

# ── Matchday pairing patterns ────────────────────────────
# Each matchday has 2 matches per group with specific position pairings
MD_PAIRINGS = {
    1: [(1, 2), (3, 4)],  # 1st vs 2nd, 3rd vs 4th
    2: [(1, 3), (4, 2)],  # 1st vs 3rd, 4th vs 2nd
    3: [(4, 1), (2, 3)],  # 4th vs 1st, 2nd vs 3rd
}


def resolve_city(raw_city: str) -> str:
    """Map FIFA city display name to canonical venue key."""
    return CITY_ALIASES.get(raw_city, raw_city)


def get_position(group_teams: list, code: str) -> int:
    """Get 1-indexed position of a team in its group."""
    return group_teams.index(code) + 1


def get_round(home_pos: int, away_pos: int) -> int:
    """Determine matchday (1-3) from position pairing."""
    pairing = (home_pos, away_pos)
    for md, pairs in MD_PAIRINGS.items():
        if pairing in pairs:
            return md
    raise ValueError(f"Unknown position pairing: {pairing}")


def get_match_in_round(round_num: int, home_pos: int, away_pos: int) -> int:
    """Get match number within the round (1 or 2)."""
    pairs = MD_PAIRINGS[round_num]
    pairing = (home_pos, away_pos)
    return pairs.index(pairing) + 1


def get_global_match_num(round_num: int, match_in_round: int) -> int:
    """Get match number within group (1-6)."""
    return (round_num - 1) * 2 + match_in_round


def parse_draw_json():
    """Parse Wikipedia draw JSON to extract and validate group compositions."""
    if not DRAW_JSON.exists():
        print("⚠️  Draw JSON not found, using hardcoded group data")
        return GROUPS

    with open(DRAW_JSON, encoding="utf-8") as f:
        data = json.load(f)

    wikitext = data["parse"]["wikitext"]["*"]
    parsed_groups = {}

    # Extract group tables from the Final draw section
    # Pattern: | A1 || ''{{#invoke:flag|fb|MEX}}''
    # or:      | A2 || {{#invoke:flag|fb|RSA}}
    group_pattern = re.compile(
        r"\|\s*([A-L])(\d)\s*\|\|\s*'*\{\{#invoke:flag\|fb\|(\w+)\}\}",
    )
    for m in group_pattern.finditer(wikitext):
        group_letter, pos, code = m.group(1), int(m.group(2)), m.group(3)
        if group_letter not in parsed_groups:
            parsed_groups[group_letter] = [None] * 4
        parsed_groups[group_letter][pos - 1] = code

    # Validate
    for g in "ABCDEFGHIJKL":
        if g not in parsed_groups:
            print(f"⚠️  Group {g} not found in draw data, using fallback")
            return GROUPS
        if None in parsed_groups[g]:
            print(f"⚠️  Group {g} incomplete, using fallback")
            return GROUPS
        if parsed_groups[g] != GROUPS[g]:
            print(f"ℹ️  Group {g}: draw={parsed_groups[g]} vs hardcoded={GROUPS[g]}")
            # Use parsed data as authoritative

    print(f"✅ Parsed all 12 groups from draw JSON")
    return parsed_groups


# ── Raw FIFA fixture data ────────────────────────────────
# Format: (date, home_code, away_code, group, venue_city, kickoff_display, status, [home_score, away_score])
# source: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/scores-fixtures
# Times are displayed in viewer timezone (likely US Eastern); kickoff_display captures FIFA.com output.
GROUP_FIXTURES: list = [
    # ── Matchday 1 ──
    # Group A
    ("2026-06-11", "MEX", "RSA", "A", "Mexico City", None, "played", 2, 0),
    ("2026-06-12", "KOR", "CZE", "A", "Guadalajara", None, "played", 2, 1),
    # Group B (results entered 2026-06-18, Green Source; backfilled to source 2026-07-08)
    ("2026-06-12", "CAN", "BIH", "B", "Toronto", "19:00", "played", 1, 1),
    ("2026-06-13", "QAT", "SUI", "B", "San Francisco Bay Area", "19:00", "played", 1, 1),
    # Group C
    ("2026-06-13", "BRA", "MAR", "C", "New Jersey", "22:00", "played", 1, 1),
    ("2026-06-14", "HAI", "SCO", "C", "Boston", "01:00", "played", 0, 1),
    # Group D
    ("2026-06-13", "USA", "PAR", "D", "Los Angeles", "01:00", "played", 4, 1),
    ("2026-06-14", "AUS", "TUR", "D", "Vancouver", "04:00", "played", 2, 0),
    # Group E
    ("2026-06-14", "GER", "CUW", "E", "Houston", "17:00", "played", 7, 1),
    ("2026-06-14", "CIV", "ECU", "E", "Philadelphia", "23:00", "played", 1, 0),
    # Group F
    ("2026-06-14", "NED", "JPN", "F", "Dallas", "20:00", "played", 2, 2),
    ("2026-06-15", "SWE", "TUN", "F", "Monterrey", "02:00", "played", 5, 1),
    # Group G
    ("2026-06-15", "BEL", "EGY", "G", "Seattle", "19:00", "played", 1, 1),
    ("2026-06-16", "IRN", "NZL", "G", "Los Angeles", "01:00", "played", 2, 2),
    # Group H
    ("2026-06-15", "ESP", "CPV", "H", "Atlanta", "16:00", "played", 0, 0),
    ("2026-06-15", "KSA", "URU", "H", "Miami", "22:00", "played", 1, 1),
    # Group I
    ("2026-06-16", "FRA", "SEN", "I", "New Jersey", "19:00", "played", 3, 1),
    ("2026-06-16", "IRQ", "NOR", "I", "Boston", "22:00", "played", 1, 4),
    # Group J
    ("2026-06-17", "ARG", "ALG", "J", "Kansas City", "01:00", "played", 3, 0),
    ("2026-06-17", "AUT", "JOR", "J", "San Francisco Bay Area", "04:00", "played", 3, 1),
    # Group K
    ("2026-06-17", "POR", "COD", "K", "Houston", "17:00", "played", 1, 1),
    ("2026-06-18", "UZB", "COL", "K", "Mexico City", "02:00", "played", 1, 3),
    # Group L
    ("2026-06-17", "ENG", "CRO", "L", "Dallas", "20:00", "played", 4, 2),
    ("2026-06-17", "GHA", "PAN", "L", "Toronto", "23:00", "played", 1, 0),

    # ── Matchday 2 ── (results: Wikipedia Group A–L pages, Green Source, 2026-07-08)
    # Group A
    ("2026-06-18", "CZE", "RSA", "A", "Atlanta", "16:00", "played", 1, 1),
    ("2026-06-19", "MEX", "KOR", "A", "Guadalajara", "01:00", "played", 1, 0),
    # Group B
    ("2026-06-18", "SUI", "BIH", "B", "Los Angeles", "19:00", "played", 4, 1),
    ("2026-06-18", "CAN", "QAT", "B", "Vancouver", "22:00", "played", 6, 0),
    # Group C
    ("2026-06-19", "SCO", "MAR", "C", "Boston", "22:00", "played", 0, 1),
    ("2026-06-20", "BRA", "HAI", "C", "Philadelphia", "00:30", "played", 3, 0),
    # Group D
    ("2026-06-19", "USA", "AUS", "D", "Seattle", "19:00", "played", 2, 0),
    ("2026-06-20", "TUR", "PAR", "D", "San Francisco Bay Area", "03:00", "played", 0, 1),
    # Group E
    ("2026-06-20", "GER", "CIV", "E", "Toronto", "20:00", "played", 2, 1),
    ("2026-06-21", "ECU", "CUW", "E", "Kansas City", "00:00", "played", 0, 0),
    # Group F
    ("2026-06-20", "NED", "SWE", "F", "Houston", "17:00", "played", 5, 1),
    ("2026-06-21", "TUN", "JPN", "F", "Monterrey", "04:00", "played", 0, 4),
    # Group G
    ("2026-06-21", "BEL", "IRN", "G", "Los Angeles", "19:00", "played", 0, 0),
    ("2026-06-22", "NZL", "EGY", "G", "Vancouver", "01:00", "played", 1, 3),
    # Group H
    ("2026-06-21", "ESP", "KSA", "H", "Atlanta", "16:00", "played", 4, 0),
    ("2026-06-21", "URU", "CPV", "H", "Miami", "22:00", "played", 2, 2),
    # Group I
    ("2026-06-22", "FRA", "IRQ", "I", "Philadelphia", "21:00", "played", 3, 0),
    ("2026-06-23", "NOR", "SEN", "I", "New Jersey", "00:00", "played", 3, 2),
    # Group J
    ("2026-06-22", "ARG", "AUT", "J", "Dallas", "17:00", "played", 2, 0),
    ("2026-06-23", "JOR", "ALG", "J", "San Francisco Bay Area", "03:00", "played", 1, 2),
    # Group K
    ("2026-06-23", "POR", "UZB", "K", "Houston", "17:00", "played", 5, 0),
    ("2026-06-24", "COL", "COD", "K", "Guadalajara", "02:00", "played", 1, 0),
    # Group L
    ("2026-06-23", "ENG", "GHA", "L", "Boston", "20:00", "played", 0, 0),
    ("2026-06-23", "PAN", "CRO", "L", "Toronto", "23:00", "played", 0, 1),

    # ── Matchday 3 ── (results: Wikipedia Group A–L pages, Green Source, 2026-07-08)
    # Group A
    ("2026-06-25", "CZE", "MEX", "A", "Mexico City", "01:00", "played", 0, 3),
    ("2026-06-25", "RSA", "KOR", "A", "Monterrey", "01:00", "played", 1, 0),
    # Group B
    ("2026-06-24", "SUI", "CAN", "B", "Vancouver", "19:00", "played", 2, 1),
    ("2026-06-24", "BIH", "QAT", "B", "Seattle", "19:00", "played", 3, 1),
    # Group C
    ("2026-06-24", "SCO", "BRA", "C", "Miami", "22:00", "played", 0, 3),
    ("2026-06-24", "MAR", "HAI", "C", "Atlanta", "22:00", "played", 4, 2),
    # Group D
    ("2026-06-26", "TUR", "USA", "D", "Los Angeles", "02:00", "played", 3, 2),
    ("2026-06-26", "PAR", "AUS", "D", "San Francisco Bay Area", "02:00", "played", 0, 0),
    # Group E
    ("2026-06-25", "ECU", "GER", "E", "New Jersey", "20:00", "played", 2, 1),
    ("2026-06-25", "CUW", "CIV", "E", "Philadelphia", "20:00", "played", 0, 2),
    # Group F
    ("2026-06-25", "TUN", "NED", "F", "Kansas City", "23:00", "played", 1, 3),
    ("2026-06-25", "JPN", "SWE", "F", "Dallas", "23:00", "played", 1, 1),
    # Group G
    ("2026-06-27", "NZL", "BEL", "G", "Vancouver", "03:00", "played", 1, 5),
    ("2026-06-27", "EGY", "IRN", "G", "Seattle", "03:00", "played", 1, 1),
    # Group H
    ("2026-06-27", "URU", "ESP", "H", "Guadalajara", "00:00", "played", 0, 1),
    ("2026-06-27", "CPV", "KSA", "H", "Houston", "00:00", "played", 0, 0),
    # Group I
    ("2026-06-26", "NOR", "FRA", "I", "Boston", "19:00", "played", 1, 4),
    ("2026-06-26", "SEN", "IRQ", "I", "Toronto", "19:00", "played", 5, 0),
    # Group J
    ("2026-06-28", "JOR", "ARG", "J", "Dallas", "02:00", "played", 1, 3),
    ("2026-06-28", "ALG", "AUT", "J", "Kansas City", "02:00", "played", 3, 3),
    # Group K
    ("2026-06-27", "COL", "POR", "K", "Miami", "23:30", "played", 0, 0),
    ("2026-06-27", "COD", "UZB", "K", "Atlanta", "23:30", "played", 3, 1),
    # Group L
    ("2026-06-27", "PAN", "ENG", "L", "New Jersey", "21:00", "played", 0, 2),
    ("2026-06-27", "CRO", "GHA", "L", "Philadelphia", "21:00", "played", 2, 1),
]

# ── Knockout stage fixture data ──────────────────────────
# Format: (match_num, date, slot_home, slot_away, round, venue_city, kickoff_display)
# match_num: FIFA global match number (73-104)
# slot format: "1A" = group winner A, "2B" = runner-up B, "3ABCDF" = best 3rd from those groups,
#              "W73" = winner of match 73, "RU101" = loser of match 101
KNOCKOUT_FIXTURES: list = [
    # ── Round of 32 (Matches 73-88) ──
    (73, "2026-06-28", "2A", "2B", "round_of_32", "Los Angeles", "19:00"),
    (74, "2026-06-29", "1E", "3ABCDF", "round_of_32", "Houston", "17:00"),
    (75, "2026-06-29", "1F", "2C", "round_of_32", "Boston", "20:30"),
    (76, "2026-06-30", "1C", "2F", "round_of_32", "Monterrey", "01:00"),
    (77, "2026-06-30", "1I", "3CDFGH", "round_of_32", "Dallas", "17:00"),
    (78, "2026-06-30", "2E", "2I", "round_of_32", "New Jersey", "21:00"),
    (79, "2026-07-01", "1A", "3CEFHI", "round_of_32", "Mexico City", "01:00"),
    (80, "2026-07-01", "1L", "3EHIJK", "round_of_32", "Atlanta", "16:00"),
    (81, "2026-07-01", "1D", "3BEFIJ", "round_of_32", "Seattle", "20:00"),
    (82, "2026-07-02", "1G", "3AEHIJ", "round_of_32", "San Francisco Bay Area", "00:00"),
    (83, "2026-07-02", "1H", "2J", "round_of_32", "Los Angeles", "19:00"),
    (84, "2026-07-02", "2K", "2L", "round_of_32", "Toronto", "23:00"),
    (85, "2026-07-03", "1B", "3EFGIJ", "round_of_32", "Vancouver", "03:00"),
    (86, "2026-07-03", "2D", "2G", "round_of_32", "Dallas", "18:00"),
    (87, "2026-07-03", "1J", "2H", "round_of_32", "Miami", "22:00"),
    (88, "2026-07-04", "1K", "3DEIJL", "round_of_32", "Kansas City", "01:30"),

    # ── Round of 16 (Matches 89-96) ──
    (89, "2026-07-04", "W73", "W75", "round_of_16", "Houston", "17:00"),
    (90, "2026-07-04", "W74", "W77", "round_of_16", "Philadelphia", "21:00"),
    (91, "2026-07-05", "W76", "W78", "round_of_16", "New Jersey", "20:00"),
    (92, "2026-07-06", "W79", "W80", "round_of_16", "Mexico City", "00:00"),
    (93, "2026-07-06", "W83", "W84", "round_of_16", "Dallas", "19:00"),
    (94, "2026-07-07", "W81", "W82", "round_of_16", "Seattle", "00:00"),
    (95, "2026-07-07", "W86", "W88", "round_of_16", "Atlanta", "16:00"),
    (96, "2026-07-07", "W85", "W87", "round_of_16", "Vancouver", "20:00"),

    # ── Quarterfinals (Matches 97-100) ──
    (97, "2026-07-09", "W89", "W90", "quarterfinal", "Boston", "20:00"),
    (98, "2026-07-10", "W93", "W94", "quarterfinal", "Los Angeles", "19:00"),
    (99, "2026-07-11", "W91", "W92", "quarterfinal", "Miami", "21:00"),
    (100, "2026-07-12", "W95", "W96", "quarterfinal", "Kansas City", "01:00"),

    # ── Semifinals (Matches 101-102) ──
    (101, "2026-07-14", "W97", "W98", "semifinal", "Dallas", "19:00"),
    (102, "2026-07-15", "W99", "W100", "semifinal", "Atlanta", "19:00"),

    # ── Third place (Match 103) ──
    (103, "2026-07-18", "RU101", "RU102", "third_place", "Miami", "21:00"),

    # ── Final (Match 104) ──
    (104, "2026-07-19", "W101", "W102", "final", "New Jersey", "19:00"),
]

ROUND_LABELS = {
    "round_of_32": "Round of 32",
    "round_of_16": "Round of 16",
    "quarterfinal": "Quarterfinal",
    "semifinal": "Semifinal",
    "third_place": "Third Place",
    "final": "Final",
}


def build_group_stage(groups: dict) -> list:
    """Build all 72 group stage match objects from fixture data + group compositions."""
    matches = []

    for fixture in GROUP_FIXTURES:
        date_str = fixture[0]
        home_code = fixture[1]
        away_code = fixture[2]
        group = fixture[3]
        raw_city = fixture[4]
        kickoff = fixture[5]
        status = fixture[6]
        home_score = fixture[7] if len(fixture) > 7 else None
        away_score = fixture[8] if len(fixture) > 8 else None

        city = resolve_city(raw_city)
        group_teams = groups[group]
        home_pos = get_position(group_teams, home_code)
        away_pos = get_position(group_teams, away_code)
        round_num = get_round(home_pos, away_pos)
        match_in_round = get_match_in_round(round_num, home_pos, away_pos)
        match_num = get_global_match_num(round_num, match_in_round)

        match_id = f"{group}{match_num}-{home_code}-{away_code}"

        venue_info = VENUES.get(city, {})
        match_obj = {
            "match_id": match_id,
            "fifa_match_num": None,  # FIFA doesn't number group stage matches publicly
            "group": group,
            "round": round_num,
            "date": date_str,
            "kickoff_display": kickoff,
            "venue_city": city,
            "venue_stadium": venue_info.get("stadium", city),
            "venue_country": venue_info.get("country", ""),
            "home_team": FIFA_CODE_MAP.get(home_code, home_code),
            "away_team": FIFA_CODE_MAP.get(away_code, away_code),
            "home_code": home_code,
            "away_code": away_code,
            "status": status,
        }
        if status == "played" and home_score is not None:
            match_obj["home_score"] = home_score
            match_obj["away_score"] = away_score

        matches.append(match_obj)

    return matches


def build_knockout_stage() -> list:
    """Build all 32 knockout stage match objects.

    For matches played through the semi-finals (R32 16 + R16 8 + QF 4 + SF 2 = 30),
    the actual home/away teams and scores are filled from ``KO_RESULTS`` (Green
    Source: Wikipedia 2026 FIFA World Cup knockout_stage page, verified
    2026-07-18). The final (KO104) and third-place (KO103) keep
    ``status="scheduled"`` but have their teams resolved from the semi-final
    results (per ``KO_PENDING_TEAMS``) for site display. Slot references are
    preserved in ``slot_home``/``slot_away`` for auditability.
    """
    matches = []

    for fixture in KNOCKOUT_FIXTURES:
        match_num = fixture[0]
        date_str = fixture[1]
        slot_home = fixture[2]
        slot_away = fixture[3]
        round_key = fixture[4]
        raw_city = fixture[5]
        kickoff = fixture[6]

        city = resolve_city(raw_city)
        venue_info = VENUES.get(city, {})

        match_id = f"KO{match_num}"

        match_obj = {
            "match_id": match_id,
            "fifa_match_num": match_num,
            "round": round_key,
            "round_label": ROUND_LABELS[round_key],
            "date": date_str,
            "kickoff_display": kickoff,
            "venue_city": city,
            "venue_stadium": venue_info.get("stadium", city),
            "venue_country": venue_info.get("country", ""),
            "slot_home": slot_home,
            "slot_away": slot_away,
        }

        # Fill actual teams/scores from verified KO results (Green Source) when available.
        if match_num in KO_RESULTS:
            home, away, hs, as_, note = KO_RESULTS[match_num]
            match_obj["home_team"] = home
            match_obj["away_team"] = away
            match_obj["home_code"] = FIFA_CODE_MAP.get(home, CODE_LOOKUP.get(home))
            match_obj["away_code"] = FIFA_CODE_MAP.get(away, CODE_LOOKUP.get(away))
            match_obj["status"] = "played"
            match_obj["home_score"] = hs
            match_obj["away_score"] = as_
            if note:
                match_obj["result_note"] = note
        elif match_num in KO_PENDING_TEAMS:
            home, away = KO_PENDING_TEAMS[match_num]
            match_obj["home_team"] = home
            match_obj["away_team"] = away
            match_obj["home_code"] = FIFA_CODE_MAP.get(home, CODE_LOOKUP.get(home))
            match_obj["away_code"] = FIFA_CODE_MAP.get(away, CODE_LOOKUP.get(away))
            match_obj["status"] = "scheduled"  # teams resolved from SF results; match not yet played
        else:
            match_obj["home_team"] = None
            match_obj["away_team"] = None
            match_obj["home_code"] = None
            match_obj["away_code"] = None
            match_obj["status"] = "scheduled"

        matches.append(match_obj)

    return matches


def build_venues_list() -> dict:
    """Build the venue registry for the schedule output."""
    return {city: info for city, info in VENUES.items()}


def main():
    print("🏆 Parsing FIFA World Cup 2026 schedule...")

    # Parse group compositions from draw data
    groups = parse_draw_json()

    # Validate group fixtures against group compositions
    for fixture in GROUP_FIXTURES:
        home_code, away_code, group = fixture[1], fixture[2], fixture[3]
        group_teams = groups[group]
        if home_code not in group_teams:
            print(f"⚠️  {home_code} not in Group {group} ({group_teams})")
        if away_code not in group_teams:
            print(f"⚠️  {away_code} not in Group {group} ({group_teams})")

    # Build schedule
    group_matches = build_group_stage(groups)
    knockout_matches = build_knockout_stage()
    venues = build_venues_list()

    # Verify counts
    if len(group_matches) != 72:
        raise ValueError(f"Expected 72 group matches, got {len(group_matches)}")
    if len(knockout_matches) != 32:
        raise ValueError(f"Expected 32 knockout matches, got {len(knockout_matches)}")

    # Verify each group has exactly 6 matches
    from collections import Counter
    group_counts = Counter(m["group"] for m in group_matches)
    for g in "ABCDEFGHIJKL":
        if group_counts[g] != 6:
            raise ValueError(f"Group {g} has {group_counts[g]} matches (expected 6)")

    # Verify each group's round distribution
    for g in "ABCDEFGHIJKL":
        round_counts = Counter(m["round"] for m in group_matches if m["group"] == g)
        if round_counts[1] != 2:
            raise ValueError(f"Group {g} MD1: {round_counts.get(1, 0)} matches")
        if round_counts[2] != 2:
            raise ValueError(f"Group {g} MD2: {round_counts.get(2, 0)} matches")
        if round_counts[3] != 2:
            raise ValueError(f"Group {g} MD3: {round_counts.get(3, 0)} matches")

    # Build output
    schedule = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "fifa.com/scores-fixtures + wikipedia draw (2025-12-05)",
        "timezone_note": (
            "Kickoff times (kickoff_display) are as displayed on FIFA.com in the viewer's "
            "timezone (likely US Eastern). Convert to venue local time using the venue timezone."
        ),
        "venues": venues,
        "group_stage": {
            "groups": {},
        },
        "knockout_stage": knockout_matches,
        "summary": {
            "total_matches": 104,
            "group_stage_matches": 72,
            "knockout_stage_matches": 32,
            "groups": 12,
            "teams": 48,
            "group_letters": list("ABCDEFGHIJKL"),
            "matchday_dates": {
                "1": "2026-06-11 to 2026-06-18",
                "2": "2026-06-18 to 2026-06-24",
                "3": "2026-06-24 to 2026-06-28",
            },
            "knockout_dates": {
                "round_of_32": "2026-06-28 to 2026-07-04",
                "round_of_16": "2026-07-04 to 2026-07-07",
                "quarterfinal": "2026-07-09 to 2026-07-12",
                "semifinal": "2026-07-14 to 2026-07-15",
                "third_place": "2026-07-18",
                "final": "2026-07-19",
            },
        },
    }

    # Organize group matches by group
    for g in "ABCDEFGHIJKL":
        group_team_codes = groups[g]
        group_team_names = [FIFA_CODE_MAP[c] for c in group_team_codes]
        group_match_list = [m for m in group_matches if m["group"] == g]
        group_match_list.sort(key=lambda m: m["round"])
        schedule["group_stage"]["groups"][g] = {
            "teams": [
                {"position": i + 1, "code": code, "name": name}
                for i, (code, name) in enumerate(zip(group_team_codes, group_team_names))
            ],
            "matches": group_match_list,
        }

    # Write output
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)

    played = sum(1 for m in group_matches if m["status"] == "played")
    scheduled = sum(1 for m in group_matches if m["status"] == "scheduled")
    ko_played = sum(1 for m in knockout_matches if m["status"] == "played")
    ko_scheduled = sum(1 for m in knockout_matches if m["status"] == "scheduled")
    print(f"✅ Generated {OUTPUT_JSON}")
    print(f"   Group stage: {len(group_matches)} matches ({played} played, {scheduled} scheduled)")
    print(f"   Knockout stage: {len(knockout_matches)} matches ({ko_played} played, {ko_scheduled} scheduled)")
    print(f"   Total: {len(group_matches) + len(knockout_matches)} matches")


if __name__ == "__main__":
    main()
