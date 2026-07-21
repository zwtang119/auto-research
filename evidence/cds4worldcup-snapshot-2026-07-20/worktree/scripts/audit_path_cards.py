#!/usr/bin/env python3
"""
audit_path_cards.py — Path Card Internal Audit for CDS4WorldCup

审计 21 张深描球队路径卡，生成：
  - data/processed/path_card_internal_audit.csv
  - data/processed/path_card_obstacle_type_matrix.csv

用法: python3 scripts/audit_path_cards.py
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
OUTPUT_AUDIT_CSV = ROOT / "data" / "processed" / "path_card_internal_audit.csv"
OUTPUT_MATRIX_CSV = ROOT / "data" / "processed" / "path_card_obstacle_type_matrix.csv"

# Canonical obstacle type taxonomy from path-card-template.md
OBSTACLE_TYPES = [
    "base_strength_gap",
    "bracket_strength",
    "squad_depth",
    "injury_risk",
    "travel_fatigue",
    "tactical_mismatch",
    "psychological_pressure",
    "low_scoring_dependency",
    "penalty_dependency",
    "favorite_collision",
    "other",
]

# Placeholder patterns
PLACEHOLDER_PATTERNS = [
    "<待分析>", "`<待分析>`", "<数据不足>", "`<数据不足>`",
    "<待填充>", "<TBD>", "TBD", "N/A",
]


def count_placeholders(card_data: dict) -> int:
    """Count placeholder fields across §3-§6."""
    count = 0
    for section_key in ["primary_obstacles", "required_breakthroughs",
                        "black_swan_helpers", "miracle_package"]:
        items = card_data.get(section_key, [])
        if not items:
            # Empty section counts as one placeholder
            count += 1
            continue
        for row in items:
            for v in row.values():
                if any(p in str(v) for p in PLACEHOLDER_PATTERNS):
                    count += 1
                    break
    return count


def count_settleable_conditions(miracle_package: list) -> int:
    """Count conditions with clear observable_proxy AND settlement_rule."""
    count = 0
    for cond in miracle_package:
        proxy = cond.get("observable_proxy", "").strip()
        rule = cond.get("settlement_rule", "").strip()
        has_proxy = proxy and not any(p in proxy for p in PLACEHOLDER_PATTERNS)
        has_rule = rule and not any(p in rule for p in PLACEHOLDER_PATTERNS)
        if has_proxy and has_rule and len(proxy) > 4 and len(rule) > 4:
            count += 1
    return count


def extract_obstacle_types(obstacles: list) -> Counter:
    """Extract obstacle type counts from §3 table."""
    counter = Counter()
    for obs in obstacles:
        otype = obs.get("类型", obs.get("type", "")).strip()
        if otype and not any(p in otype for p in PLACEHOLDER_PATTERNS):
            if otype in OBSTACLE_TYPES:
                counter[otype] += 1
            else:
                counter["other"] += 1
        elif otype:
            counter["other"] += 1
    return counter


def check_source_boundary(card_text: str) -> str:
    """Check if Kimi data is correctly demoted to Red Source in §9."""
    notes = []
    # Check §9 for Red Source marker
    if "Red Source" in card_text:
        notes.append("Kimi correctly demoted to Red Source")
    else:
        notes.append("⚠️ No Red Source marker found in §9")

    # Check §8 Factor Ledger — should be empty at this stage
    section8 = re.search(
        r'## 8\.\s*Factor Ledger Candidates\s*\n(.*?)(?=\n## \d+\.|\Z)',
        card_text, re.DOTALL
    )
    if section8:
        s8_text = section8.group(1).strip()
        data_rows = [line for line in s8_text.split('\n')
                     if line.strip().startswith('|')
                     and not all(c in '|-: ' for c in line)]
        if len(data_rows) <= 1:
            notes.append("§8 Factor Ledger empty (correct)")
        else:
            notes.append("§8 Factor Ledger has entries")

    return "; ".join(notes) if notes else "no issues found"


def determine_audit_status(placeholder_count, settleable_ratio, source_ok):
    """Determine overall audit status: pass / pass_with_notes / needs_revision."""
    issues = []
    if placeholder_count > 5:
        issues.append("high_placeholder_count")
    if settleable_ratio < 0.5:
        issues.append("low_settleability")
    if not source_ok:
        issues.append("source_boundary_risk")

    if not issues:
        return "pass"
    elif len(issues) == 1 and issues[0] != "source_boundary_risk":
        return "pass_with_notes"
    else:
        return "pass_with_notes" if len(issues) <= 2 else "needs_revision"


def run_audit(include_thin_slice=False):
    """Main audit function. Returns (audit_rows, matrix_rows, obstacle_type_counts).

    Args:
        include_thin_slice: If True, also audit thin-slice cards (replaces MiMo T003).
    """
    print("Building team data from existing parser...")
    teams, meta = build_teams_json(strict=False)

    registry = {r["canonical_team"]: r for r in load_csv(TEAM_REGISTRY)}
    signals = {r["canonical_team"]: r for r in load_csv(SIGNALS_CSV)}

    if include_thin_slice:
        target_teams = teams
        print(f"Auditing all {len(teams)} cards (deep + thin-slice)")
    else:
        target_teams = {slug: t for slug, t in teams.items() if t["is_deep"]}
        print(f"Found {len(target_teams)} deep-description cards")

    all_obstacle_types = Counter()
    team_obstacle_types = {}
    audit_rows = []
    matrix_rows = []

    for slug, team in sorted(target_teams.items()):
        obstacles = team.get("primary_obstacles", [])
        breakthroughs = team.get("required_breakthroughs", [])
        black_swan_helpers = team.get("black_swan_helpers", [])
        miracle_package = team.get("miracle_package", [])

        # Obstacle type extraction
        obs_types = extract_obstacle_types(obstacles)
        team_obstacle_types[slug] = obs_types
        all_obstacle_types.update(obs_types)

        # Placeholder count
        card_data_for_ph = {
            "primary_obstacles": obstacles,
            "required_breakthroughs": breakthroughs,
            "black_swan_helpers": black_swan_helpers,
            "miracle_package": miracle_package,
        }
        placeholder_count = count_placeholders(card_data_for_ph)

        # Settleable conditions
        settleable_count = count_settleable_conditions(miracle_package)
        miracle_count = len(miracle_package)

        # Source boundary check
        md_path = CARDS_DIR / f"{slug}.md"
        card_text = md_path.read_text(encoding="utf-8") if md_path.exists() else ""
        source_notes = check_source_boundary(card_text)
        source_ok = "correctly" in source_notes or "empty (correct)" in source_notes

        # Overall status
        settleable_ratio = settleable_count / miracle_count if miracle_count > 0 else 0

        # For thin-slice cards, override status to thin_slice_expected
        if not team.get("is_deep", True):
            status = "thin_slice_expected"
        else:
            status = determine_audit_status(placeholder_count, settleable_ratio, source_ok)

        canonical = team.get("canonical_name", "")
        zh_name = team.get("zh_name", "")

        audit_rows.append({
            "team_slug": slug,
            "canonical_team": canonical,
            "zh_name": zh_name,
            "status": team.get("status", ""),
            "primary_obstacle_count": len(obstacles),
            "required_breakthrough_count": len(breakthroughs),
            "black_swan_helper_count": len(black_swan_helpers),
            "miracle_condition_count": miracle_count,
            "settleable_condition_count": settleable_count,
            "placeholder_count": placeholder_count,
            "source_boundary_notes": source_notes,
            "overall_audit_status": status,
        })

        matrix_row = {"team_slug": slug, "canonical_team": canonical}
        for otype in OBSTACLE_TYPES:
            matrix_row[otype] = obs_types.get(otype, 0)
        matrix_rows.append(matrix_row)

    # Write audit CSV
    OUTPUT_AUDIT_CSV.parent.mkdir(parents=True, exist_ok=True)
    audit_fields = [
        "team_slug", "canonical_team", "zh_name", "status",
        "primary_obstacle_count", "required_breakthrough_count",
        "black_swan_helper_count", "miracle_condition_count",
        "settleable_condition_count", "placeholder_count",
        "source_boundary_notes", "overall_audit_status",
    ]
    with open(OUTPUT_AUDIT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=audit_fields)
        writer.writeheader()
        writer.writerows(audit_rows)
    print(f"✅ Generated {OUTPUT_AUDIT_CSV}")

    # Write matrix CSV
    matrix_fields = ["team_slug", "canonical_team"] + OBSTACLE_TYPES
    with open(OUTPUT_MATRIX_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=matrix_fields)
        writer.writeheader()
        writer.writerows(matrix_rows)
    print(f"✅ Generated {OUTPUT_MATRIX_CSV}")

    deep_count_actual = sum(1 for r in audit_rows if r["status"] == "deep-description")
    thin_count_actual = sum(1 for r in audit_rows if r["status"] == "thin-slice")
    print(f"\n── Audit Coverage: {deep_count_actual} deep + {thin_count_actual} thin-slice = {len(audit_rows)} total ──")

    # Summary stats
    print(f"\n── Obstacle Type Distribution (across {deep_count_actual} deep cards) ──")
    for otype, count in all_obstacle_types.most_common():
        pct = count / deep_count_actual * 100
        label = "UNIVERSAL" if pct >= 60 else "DIFFERENTIATING" if pct >= 20 else "RARE"
        print(f"  {otype}: {count} ({pct:.0f}%) [{label}]")

    total_obstacles = sum(all_obstacle_types.values())
    deep_in_target = sum(1 for t in target_teams.values() if t.get("is_deep"))
    avg_obstacles = total_obstacles / deep_in_target if deep_in_target else 0
    print(f"\n  Total obstacle entries: {total_obstacles}")
    print(f"  Average per team: {avg_obstacles:.1f}")

    total_conditions = sum(r["miracle_condition_count"] for r in audit_rows)
    total_settleable = sum(r["settleable_condition_count"] for r in audit_rows)
    print(f"\n── Miracle Package Settleability ──")
    print(f"  Total conditions: {total_conditions}")
    print(f"  Settleable: {total_settleable}")
    if total_conditions:
        print(f"  Ratio: {total_settleable / total_conditions:.1%}")

    status_counts = Counter(r["overall_audit_status"] for r in audit_rows)
    print(f"\n── Audit Status ──")
    for status, count in status_counts.most_common():
        print(f"  {status}: {count}")

    return audit_rows, matrix_rows, all_obstacle_types


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Path card audit for CDS4WorldCup")
    parser.add_argument("--all", action="store_true",
                        help="Include thin-slice cards (replaces MiMo Sprint 1 T003)")
    args = parser.parse_args()
    run_audit(include_thin_slice=args.all)
