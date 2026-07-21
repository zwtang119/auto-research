#!/usr/bin/env python3
"""
source_gap_scanner.py — 48-Team Source Gap Scanner for CDS4WorldCup

Scans all 48 team path cards for source coverage gaps.
Replaces MiMo Sprint 1 Task T004 with deterministic, reproducible output.

Key improvements over MiMo T004:
  - Correctly parses YAML source_status from §1 of each card
  - No template-filler — each row reflects actual card content
  - Idempotent and reproducible
  - Adds excluded_from_wc flag (Italy lost UEFA playoff)

Reads:
  - artifacts/team-cards/*.md — source_status YAML from §1
  - data/processed/kimi_baseline_signals_matrix.csv — Kimi data presence
  - data/processed/team_registry.csv — confederation, group

Writes:
  - data/processed/source_gap_map.csv

Usage: python3 scripts/source_gap_scanner.py
"""

import csv
import re
import sys
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from build_site_data import build_teams_json, CARDS_DIR
from src.utils.csv_helpers import load_csv

TEAM_REGISTRY = ROOT / "data" / "processed" / "team_registry.csv"
SIGNALS_CSV = ROOT / "data" / "processed" / "kimi_baseline_signals_matrix.csv"
OUTPUT_CSV = ROOT / "data" / "processed" / "source_gap_map.csv"

# Teams confirmed NOT in 2026 WC (verified via Wikipedia API in earlier sprints)
EXCLUDED_SLUGS = {"italy"}


def parse_source_status(card_text: str) -> dict:
    """Parse source_status YAML arrays from §1 Team Profile.

    The YAML block looks like:
        source_status:
          green_sources: [public-football-knowledge]
          yellow_sources: [kimi-aggregation]
          red_sources: [kimi-300-agent-reasons]
          coverage: sufficient

    Returns dict with green_sources, yellow_sources, red_sources (lists),
    and coverage (str).
    """
    result = {
        "green_sources": [],
        "yellow_sources": [],
        "red_sources": [],
        "coverage": "unknown",
    }

    for key in ("green_sources", "yellow_sources", "red_sources"):
        match = re.search(rf'{key}:\s*\[([^\]]*)\]', card_text)
        if match:
            raw = match.group(1).strip()
            if raw:
                result[key] = [
                    s.strip().strip("'\"")
                    for s in raw.split(",")
                    if s.strip() and s.strip() not in ("none_yet",)
                ]

    cov_match = re.search(r'coverage:\s*(\w+)', card_text)
    if cov_match:
        result["coverage"] = cov_match.group(1)

    return result


def classify_gap(sources: dict, card_status: str) -> dict:
    """Classify source gap level based on parsed source counts.

    Returns dict with gap_level, gap_description, recommended_action.

    Note: "public-football-knowledge" is a generic template label added by
    generate_path_cards.py, NOT a specific verifiable Green Source per
    source-policy.md. Deep-description cards with only this label are
    still classified as high gap.
    """
    green = len(sources["green_sources"])
    yellow = len(sources["yellow_sources"])
    red = len(sources["red_sources"])

    if green > 0 and yellow > 0:
        return {
            "gap_level": "high",
            "gap_description": (
                f"无实质性 Green Source（仅 generic label "
                f"{sources['green_sources']}），实际依赖 Yellow/Red"
            ),
            "recommended_action": (
                "补充 FIFA 官方排名、近期大赛赛果、阵容名单等 Green Source"
            ),
        }
    elif green > 0:
        return {
            "gap_level": "high",
            "gap_description": (
                f"仅 generic Green Source label（{sources['green_sources']}），"
                f"无具体可复核数据源"
            ),
            "recommended_action": "补充具体可复核的 Green Source（FIFA排名、赛果、阵容）",
        }
    elif yellow > 0:
        return {
            "gap_level": "high",
            "gap_description": (
                f"无 Green Source；仅依赖 {yellow} 个 Yellow Source + "
                f"{red} 个 Red Source"
            ),
            "recommended_action": "补充 FIFA 官方排名、近期大赛赛果、阵容名单等 Green Source",
        }
    else:
        action = "补充 FIFA 排名、阵容名单、近期赛果等 Green Source"
        if card_status == "thin-slice":
            action += "；建议升级为 deep-description"
        return {
            "gap_level": "critical",
            "gap_description": "无任何来源；path card 为薄切片占位",
            "recommended_action": action,
        }


def run_scan():
    """Main scan — iterate all team cards, classify sources, write CSV."""
    print("Loading team data via build_site_data parser...")
    teams, meta = build_teams_json(strict=False)
    print(f"  {meta['deep_description_count']} deep-description, "
          f"{meta['thin_slice_count']} thin-slice")

    registry = {r["canonical_team"]: r for r in load_csv(TEAM_REGISTRY)}
    signals = {r["canonical_team"]: r for r in load_csv(SIGNALS_CSV)}

    rows = []
    for slug, team in sorted(teams.items()):
        canonical = team.get("canonical_name", "")
        zh_name = team.get("zh_name", "")
        card_status = team.get("status", "")

        reg = registry.get(canonical, {})
        confederation = reg.get("confederation", "")
        group_name = reg.get("group", "")

        # Parse source_status from raw card text
        md_path = CARDS_DIR / f"{slug}.md"
        card_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""

        sources = parse_source_status(card_text)
        gap = classify_gap(sources, card_status)

        has_kimi = canonical in signals
        is_excluded = slug in EXCLUDED_SLUGS

        rows.append({
            "team_slug": slug,
            "canonical_team": canonical,
            "zh_name": zh_name,
            "confederation": confederation,
            "group": group_name,
            "card_status": card_status,
            "has_kimi_data": has_kimi,
            "green_source_count": len(sources["green_sources"]),
            "yellow_source_count": len(sources["yellow_sources"]),
            "red_source_count": len(sources["red_sources"]),
            "coverage_status": sources["coverage"],
            "gap_level": gap["gap_level"],
            "gap_description": gap["gap_description"],
            "recommended_source_action": gap["recommended_action"],
            "excluded_from_wc": is_excluded,
        })

    # Write CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "team_slug", "canonical_team", "zh_name", "confederation", "group",
        "card_status", "has_kimi_data",
        "green_source_count", "yellow_source_count", "red_source_count",
        "coverage_status", "gap_level", "gap_description",
        "recommended_source_action", "excluded_from_wc",
    ]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Generated {OUTPUT_CSV} ({len(rows)} teams)")

    # Summary
    gap_counts = Counter(r["gap_level"] for r in rows)
    status_counts = Counter(r["card_status"] for r in rows)

    print(f"\n{'═' * 50}")
    print(f"  Source Gap Summary")
    print(f"{'═' * 50}")
    for level in ("none", "medium", "high", "critical"):
        c = gap_counts.get(level, 0)
        if c:
            print(f"  {level:10s}: {c} teams")
    print(f"  {'─' * 30}")
    for status, c in status_counts.most_common():
        print(f"  {status:20s}: {c}")

    excluded = [r for r in rows if r["excluded_from_wc"]]
    if excluded:
        print(f"\n  ⚠️  Excluded from 2026 WC:")
        for r in excluded:
            print(f"      {r['canonical_team']} ({r['zh_name']}) — "
                  f"gap={r['gap_level']}, "
                  f"sources=g{r['green_source_count']}/y{r['yellow_source_count']}/r{r['red_source_count']}")

    return rows


if __name__ == "__main__":
    run_scan()
