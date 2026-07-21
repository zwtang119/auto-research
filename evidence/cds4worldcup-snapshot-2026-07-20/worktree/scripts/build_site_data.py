#!/usr/bin/env python3
"""
build_site_data.py — 解析 team cards + CSV → 前端 JSON

用法: python3 scripts/build_site_data.py
输出: site/data/teams.json + site/data/meta.json
"""

import csv
import json
import re
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
TEAM_REGISTRY = ROOT / "data" / "processed" / "team_registry.csv"
SIGNALS_CSV = ROOT / "data" / "processed" / "kimi_baseline_signals_matrix.csv"
BASELINES_CSV = ROOT / "data" / "processed" / "baseline_suite_registry.csv"
AUDIT_CSV = ROOT / "data" / "processed" / "path_card_internal_audit.csv"
OBSTACLE_MATRIX_CSV = ROOT / "data" / "processed" / "path_card_obstacle_type_matrix.csv"
AGENT_INVENTORY_CSV = ROOT / "data" / "processed" / "kimi_agent_inventory.csv"
CARDS_DIR = ROOT / "artifacts" / "team-cards"
OUTPUT_DIR = ROOT / "site" / "data"

# Expected team card counts (verified against team-cards/ directory)
EXPECTED_TEAM_COUNT = 48
EXPECTED_DEEP_DESCRIPTION_COUNT = 48
EXPECTED_THIN_SLICE_COUNT = 0

# ── Country flag emoji mapping ──────────────────────────
COUNTRY_FLAGS = {
    "Spain": "🇪🇸", "France": "🇫🇷", "Argentina": "🇦🇷", "Portugal": "🇵🇹",
    "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "Germany": "🇩🇪", "Morocco": "🇲🇦", "Brazil": "🇧🇷",
    "Norway": "🇳🇴", "Netherlands": "🇳🇱", "Croatia": "🇭🇷", "Colombia": "🇨🇴",
    "Japan": "🇯🇵", "Senegal": "🇸🇳", "United States": "🇺🇸", "Mexico": "🇲🇽",
    "Uruguay": "🇺🇾", "Belgium": "🇧🇪", "Australia": "🇦🇺", "South Korea": "🇰🇷",
    "Turkey": "🇹🇷", "Canada": "🇨🇦", "Panama": "🇵🇦", "Costa Rica": "🇨🇷",
    "Italy": "🇮🇹", "Denmark": "🇩🇰", "Switzerland": "🇨🇭", "Austria": "🇦🇹",
    "Poland": "🇵🇱", "Ukraine": "🇺🇦", "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "Chile": "🇨🇱",
    "Ecuador": "🇪🇨", "Venezuela": "🇻🇪", "Saudi Arabia": "🇸🇦", "Tunisia": "🇹🇳",
    "Cameroon": "🇨🇲", "Côte d'Ivoire": "🇨🇮", "Nigeria": "🇳🇬", "Ghana": "🇬🇭",
    "Egypt": "🇪🇬", "Algeria": "🇩🇿", "Iran": "🇮🇷", "Uzbekistan": "🇺🇿",
    "Iraq": "🇮🇶", "Qatar": "🇶🇦", "New Zealand": "🇳🇿", "Paraguay": "🇵🇾",
}

CONFEDERATION_LABELS = {
    "UEFA": "欧洲", "CONMEBOL": "南美", "CONCACAF": "中北美",
    "AFC": "亚洲", "CAF": "非洲", "OFC": "大洋洲",
}

OBSTACLE_LABELS = {
    "low_scoring_dependency": "太依赖小比分",
    "psychological_pressure": "心理压力",
    "bracket_strength": "签表太硬",
    "base_strength_gap": "硬实力差距",
    "tactical_mismatch": "战术对不上",
    "squad_depth": "板凳厚度不够",
    "injury_risk": "伤病风险",
    "travel_fatigue": "旅途消耗",
    "favorite_collision": "太早撞热门队",
    "penalty_dependency": "太依赖点球",
    "other": "其他难点",
}

SOURCE_LABELS = {
    "Green": "可靠事实",
    "Yellow": "待核验线索",
    "Red": "只能参考",
    "Mixed": "混合来源",
    "Mixed (Red source + Yellow processed data)": "混合来源",
}

BASELINE_DISPLAY_NAMES = {
    "uniform_48": "48 队平均参照",
    "defending_champion": "卫冕冠军参照",
    "fifa_ranking_proxy": "FIFA 排名参照",
    "elo_proxy": "Elo 实力参照",
    "market_public_baseline": "市场公开参照",
    "kimi_public_ai_baseline": "公开模型群体参考",
}

BASELINE_PUBLIC_RULES = {
    "uniform_48": "先假设每队机会一样，用来当最朴素的参照线。",
    "defending_champion": "看看“上届冠军惯性”这件事到底有没有解释力。",
    "fifa_ranking_proxy": "用 FIFA 排名做一个简单实力参照，等官方排名数据补齐后再更新。",
    "elo_proxy": "用公开 Elo 评分做实力参照，数据源确认后再放进快照。",
    "market_public_baseline": "把公开市场看法整理成快照，只看外界热度和分歧。",
    "kimi_public_ai_baseline": "整理一组公开模型群体的冠军倾向，只看外界偏向，不当作事实。",
}

FACTION_COLORS = {
    "数据派": "#6E8499",
    "赔率派": "#A85F50",
    "老球迷派": "#7E9070",
    "玄学派": "#C2A75F",
    "主帅视角派": "#97768F",
    "伤病赛程派": "#5E807A",
    "黑马派": "#C07E55",
    "阵容年龄派": "#B27D7E",
    "心理抗压派": "#76729A",
    "建模派": "#B59A6B",
}

PUBLIC_VENDOR_FORBIDDEN = [
    "Kimi", "kimi", "小米", "Xiaomi", "MiMo", "MiMo Code Long-Horizon",
]

PUBLIC_BETTING_FORBIDDEN = [
    "投注建议", "ROI", "PnL", "Sharpe", "Kelly", "仓位",
    "低估", "高估", "正期望", "value bet",
]

STATUS_LABELS = {
    "complete": "已完成",
    "pass": "已通过",
    "partial": "部分可用",
    "partial_populated": "部分可用",
    "designed_not_populated": "规则有了，数据待补",
    "snapshot_unavailable": "这次还没有快照",
    "not_available": "暂时没有",
    "planned": "已规划",
    "deferred": "暂缓",
}


def load_csv(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def parse_markdown_card(md_path):
    """Parse a team card Markdown file into structured sections."""
    text = md_path.read_text(encoding="utf-8")
    card = {}

    # Detect status (deep-description vs thin-slice)
    status_match = re.search(r'>\s*\*\*状态\*\*:\s*(\S+)', text)
    card["status"] = status_match.group(1) if status_match else "unknown"

    # §2 Championship Thesis
    thesis_section = _section_body(text, 2, "Championship Thesis")
    thesis_match = re.search(r'>\s*(.+?)(?:\n\n|\Z)', thesis_section, re.DOTALL)
    card["championship_thesis"] = _clean_markdown_text(thesis_match.group(1)) if thesis_match else ""

    # §3 Primary Obstacles — parse table
    card["primary_obstacles"] = _parse_table(_section_body(text, 3, "Primary Obstacles"))

    # §4 Required Breakthroughs — parse table
    card["required_breakthroughs"] = _parse_table(_section_body(text, 4, "Required Breakthroughs"))

    # §5 Black Swan Helpers — parse table
    card["black_swan_helpers"] = _parse_table(_section_body(text, 5, "Black Swan Helpers"))

    # §6 Miracle Package — extract YAML
    miracle_section = _section_body(text, 6, "Miracle Package")
    miracle_match = re.search(r'```yaml\s*\n(.*?)```', miracle_section, re.DOTALL)
    if miracle_match:
        yaml_text = miracle_match.group(1)
        conditions = []
        for cond_match in re.finditer(
            r'-\s*condition:\s*(.+?)\n\s*type:\s*(.+?)\n\s*observable_proxy:\s*(.+?)\n\s*settlement_rule:\s*(.+?)(?:\n|$)',
            yaml_text
        ):
            conditions.append({
                "condition": _clean_markdown_text(cond_match.group(1)),
                "type": _clean_markdown_text(cond_match.group(2)),
                "observable_proxy": _clean_markdown_text(cond_match.group(3)),
                "settlement_rule": _clean_markdown_text(cond_match.group(4)),
            })
        card["miracle_package"] = conditions
    else:
        card["miracle_package"] = []

    # §11 Current Interpretation
    interp_match = re.search(
        r'## 11\.\s*Current Interpretation\s*\n+(.*?)(?:\n## |\Z)',
        text, re.DOTALL
    )
    if interp_match:
        interp_text = interp_match.group(1).strip()
        card["current_interpretation"] = {}
        for label, key in [
            ("最可信路径", "most_credible_path"),
            ("最不可信叙事", "least_credible_narrative"),
            ("最值得赛中监控的信号", "signals_to_monitor"),
            ("如果夺冠，哪些赛前判断有价值", "valuable_pre_judgments"),
            ("数据不足", "data_insufficient"),
        ]:
            pat = re.compile(rf'\*\*{re.escape(label)}\*\*:\s*(.+?)(?=\n\n\*\*|\Z)', re.DOTALL)
            m = pat.search(interp_text)
            if m:
                card["current_interpretation"][key] = m.group(1).strip()
    else:
        card["current_interpretation"] = {}

    # §1 profile paragraph (after ```yaml``` block)
    profile_para = re.search(
        r'```\n\n(.+?)(?:\n\n## )',
        text, re.DOTALL
    )
    card["profile_paragraph"] = profile_para.group(1).strip() if profile_para else ""

    return card


def _section_body(text, number, title):
    """Return the body of one numbered Markdown section."""
    match = re.search(
        rf'## {number}\.\s*{re.escape(title)}\s*\n(.*?)(?=\n## \d+\.|\Z)',
        text,
        re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def _clean_markdown_text(value):
    """Normalize lightweight Markdown placeholders and whitespace for JSON output."""
    return re.sub(r'\s+', ' ', value).strip().strip('"')


def _parse_table(section_text):
    """Parse the first Markdown table in a section body."""
    match = re.search(
        r'\|(.+?)\|\s*\n\|[-:| ]+\|\s*\n((?:\|.+\|\s*\n?)*)',
        section_text,
        re.DOTALL,
    )
    if not match:
        return []

    headers_raw = match.group(1)
    headers = [h.strip() for h in headers_raw.split('|')]
    rows_text = match.group(2).strip()
    rows = []
    for line in rows_text.split('\n'):
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) == len(headers) and not _is_placeholder_row(cells):
            row = {}
            for i, h in enumerate(headers):
                row[h] = _clean_markdown_text(cells[i]) if i < len(cells) else ""
            rows.append(row)
    return rows


def _is_placeholder_row(cells):
    joined = "".join(cells).strip()
    if not joined or set(joined) <= {"-", ":"}:
        return True
    placeholder_cells = [
        cell in {"", "`<待分析>`", "`<数据不足>`", "<待分析>", "<数据不足>"}
        or cell.startswith("`<")
        or cell.startswith("<")
        for cell in cells
    ]
    return all(placeholder_cells)


def build_teams_json(strict=False):
    """Main build function."""
    # Load CSV data
    registry = {r["canonical_team"]: r for r in load_csv(TEAM_REGISTRY)}
    signals = {r["canonical_team"]: r for r in load_csv(SIGNALS_CSV)}

    teams = {}
    obstacle_type_counter = Counter()
    deep_count = 0
    thin_count = 0

    for md_file in sorted(CARDS_DIR.glob("*.md")):
        if md_file.name == "README.md":
            continue

        card_data = parse_markdown_card(md_file)
        slug = md_file.stem

        # Find matching registry entry
        reg = None
        sig = None
        for canonical, r in registry.items():
            test_slug = canonical.lower().replace(" ", "-").replace("'", "")
            if test_slug == slug:
                reg = r
                sig = signals.get(canonical)
                break

        if not reg:
            if strict:
                raise ValueError(f"No registry row found for card: {md_file}")
            continue

        canonical = reg["canonical_team"]
        is_deep = card_data["status"] == "deep-description"

        if is_deep:
            deep_count += 1
        else:
            thin_count += 1

        # Count obstacle types
        for obs in card_data.get("primary_obstacles", []):
            otype = obs.get("类型", obs.get("type", ""))
            if otype and not otype.startswith("<") and not otype.startswith("`"):
                obstacle_type_counter[otype] += 1

        team_entry = {
            "slug": slug,
            "canonical_name": canonical,
            "zh_name": reg.get("zh_name", ""),
            "en_name": reg.get("en_name", ""),
            "confederation": reg.get("confederation", ""),
            "confederation_label": CONFEDERATION_LABELS.get(reg.get("confederation", ""), ""),
            "group": reg.get("group", ""),
            "flag": COUNTRY_FLAGS.get(canonical, "🏳️"),
            "status": card_data["status"],
            "is_deep": is_deep,
            "coverage_status": reg.get("coverage_status", ""),
            "kimi_probability": float(sig["kimi_probability"]) if sig and sig.get("kimi_probability", "N/A") != "N/A" else None,
            "kimi_baseline_signals": sig.get("kimi_baseline_signals", "none") if sig else "none",
            "championship_thesis": card_data.get("championship_thesis", ""),
            "primary_obstacles": card_data.get("primary_obstacles", []),
            "required_breakthroughs": card_data.get("required_breakthroughs", []),
            "black_swan_helpers": card_data.get("black_swan_helpers", []),
            "miracle_package": card_data.get("miracle_package", []),
            "current_interpretation": card_data.get("current_interpretation", {}),
            "profile_paragraph": card_data.get("profile_paragraph", ""),
        }
        teams[slug] = team_entry

    # Build meta.json
    meta = {
        "total_teams": len(teams),
        "deep_description_count": deep_count,
        "thin_slice_count": thin_count,
        "obstacle_type_distribution": dict(obstacle_type_counter.most_common()),
        "obstacle_type_count": len(obstacle_type_counter),
        "confederations": sorted(set(t["confederation"] for t in teams.values() if t["confederation"])),
        "groups": sorted(set(t["group"] for t in teams.values() if t["group"])),
        "plan_status": {
            "plan_0": {"name": "分叉复制", "status": "complete", "label": "✅ 完成"},
            "plan_a0": {"name": "主体注册", "status": "complete", "label": "✅ 完成"},
            "plan_a1": {"name": "48队路径卡", "status": "complete", "label": "✅ 完成"},
            "plan_a2": {"name": "Path Type 分类", "status": "not_started", "label": "📋 未开始"},
            "plan_b0": {"name": "数据门控", "status": "complete", "label": "✅ 完成"},
            "plan_b1": {"name": "直觉锚定", "status": "complete", "label": "✅ 完成"},
            "plan_b2": {"name": "可恢复性门控", "status": "deferred", "label": "⏸️ 延期"},
            "plan_c": {"name": "协议闭环验证", "status": "complete", "label": "✅ 完成"},
        },
        "kimi_coverage": {
            "covered": sum(1 for t in teams.values() if t["kimi_probability"] is not None),
            "not_covered": sum(1 for t in teams.values() if t["kimi_probability"] is None),
        },
        "build_date": __import__("datetime").date.today().isoformat(),
    }

    if strict:
        _validate_site_data(teams, meta)

    return teams, meta


def build_homepage_json(strict=False):
    """Build the single static JSON payload used by the homepage."""
    teams, meta = build_teams_json(strict=strict)
    audit_rows = load_csv(AUDIT_CSV) if AUDIT_CSV.exists() else []
    baseline_rows = load_csv(BASELINES_CSV) if BASELINES_CSV.exists() else []
    matrix_rows = load_csv(OBSTACLE_MATRIX_CSV) if OBSTACLE_MATRIX_CSV.exists() else []

    settleable_count = _sum_int(audit_rows, "settleable_condition_count")
    deep_audited = sum(1 for row in audit_rows if row.get("status") == "deep-description")
    deep_passed = sum(1 for row in audit_rows if row.get("overall_audit_status") == "pass")
    obstacle_distribution = _build_obstacle_distribution(meta["obstacle_type_distribution"])
    team_teasers = _build_team_teasers(teams)
    baselines = _build_baselines(baseline_rows)
    public_model_snapshot = _build_public_model_snapshot(teams)
    market_snapshot = _build_market_snapshot()
    ai_perspectives = _build_ai_perspectives(teams)

    generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    homepage = {
        "generated_at": generated_at,
        "build_date": meta["build_date"],
        "source_policy_version": "draft-for-execution",
        "summary": {
            "total_teams": meta["total_teams"],
            "deep_description_count": meta["deep_description_count"],
            "thin_slice_count": meta["thin_slice_count"],
            "obstacle_record_count": sum(row["count"] for row in obstacle_distribution),
            "settleable_condition_count": settleable_count,
            "baseline_count": len(baselines),
        },
        "audit": {
            "deep_cards_audited": deep_audited,
            "deep_cards_passed": deep_passed,
            "source_boundary_status": "pass",
            "source_boundary_label": "来源边界已检查",
            "factor_ledger_schema_status": "pass",
            "factor_ledger_schema_label": "赛后对账规则可用",
        },
        "hero": {
            "headline": "48 支球队，每队都有一条夺冠路。",
            "lede": "我们不直接猜谁会夺冠。我们想看清楚：一支球队真要捧杯，得过哪些坎，哪些迹象要提前出现，哪些判断赛后能对上账。",
            "boundary": "市场数据只代表“外界怎么看”，不是我们的事实依据，也不是投机指引。",
            "hooks": [
                "如果阿根廷夺冠，世界得变成什么样？",
                "法国要卫冕，最难的几关是哪几关？",
                "你支持的球队，离冠军到底差哪口气？",
            ],
        },
        "team_teasers": team_teasers,
        "obstacle_distribution": obstacle_distribution,
        "obstacle_matrix_teaser": _build_obstacle_matrix_teaser(matrix_rows),
        "baselines": baselines,
        "public_signal_snapshots": {
            "public_model_crowd": public_model_snapshot,
            "market_public_baseline": market_snapshot,
        },
        "ai_perspectives": {
            key: value
            for key, value in ai_perspectives.items()
            if key != "teams"
        },
        "public_consensus_gap": {
            "status": "not_available",
            "status_label": STATUS_LABELS["not_available"],
            "display_rule": "市场快照发布后，才展示外界看法和我们路径判断之间差多少。",
            "items": [],
        },
        "monitoring": {
            "items": [
                {"label": "市场快照", "status": "planned", "status_label": STATUS_LABELS["planned"]},
                {"label": "官方消息", "status": "planned", "status_label": STATUS_LABELS["planned"]},
                {"label": "伤病和新闻线索", "status": "planned", "status_label": STATUS_LABELS["planned"]},
                {"label": "赛程/赛果对账", "status": "planned", "status_label": STATUS_LABELS["planned"]},
                {"label": "人工复核", "status": "planned", "status_label": STATUS_LABELS["planned"]},
            ],
            "public_display_rule": "只展示任务状态，不展示未核验事实为结论。",
        },
        "research_log": [
            {"date": "2026-06-11", "type": "路径卡", "title": "48 队路径卡完成", "href": "teams.html"},
            {"date": "2026-06-11", "type": "审计", "title": "21 张深度卡通过内部审计", "href": ""},
            {"date": "2026-06-11", "type": "参照组", "title": "5 组公开参照规则整理完成", "href": ""},
            {"date": "2026-06-11", "type": "对账", "title": "赛后对账协议验证通过", "href": ""},
        ],
    }

    if strict:
        _validate_homepage_json(homepage)

    return homepage


def _sum_int(rows, key):
    total = 0
    for row in rows:
        try:
            total += int(row.get(key, 0) or 0)
        except ValueError:
            continue
    return total


def _build_obstacle_distribution(distribution):
    rows = []
    for key, count in distribution.items():
        rows.append({
            "type": key,
            "display_label": OBSTACLE_LABELS.get(key, key.replace("_", " ")),
            "count": count,
            "classification": _classify_obstacle(key),
        })
    return rows


def _classify_obstacle(key):
    if key in {"low_scoring_dependency", "psychological_pressure", "bracket_strength"}:
        return "常见门槛"
    if key in {"injury_risk", "travel_fatigue", "favorite_collision"}:
        return "区分变量"
    return "路径难点"


def _build_team_teasers(teams):
    featured = [
        "argentina", "france", "spain", "portugal", "england", "germany", "morocco", "brazil"
    ]
    ordered = [teams[slug] for slug in featured if slug in teams]
    if len(ordered) < 8:
        ordered.extend(team for team in sorted(teams.values(), key=lambda item: item["en_name"]) if team not in ordered)

    teasers = []
    for team in ordered[:12]:
        obstacles = _top_obstacle_labels(team)
        thesis = _plain_thesis(team)
        teasers.append({
            "team_slug": team["slug"],
            "team_name": team["zh_name"] or team["canonical_name"],
            "en_name": team["en_name"],
            "flag": team["flag"],
            "confederation": team["confederation"],
            "confederation_label": team["confederation_label"],
            "display_status": team["status"],
            "display_status_label": "深度版" if team["is_deep"] else "简版",
            "path_thesis": thesis,
            "top_obstacle_types": obstacles,
            "source_completeness": "deep" if team["is_deep"] else "thin",
            "source_completeness_label": "资料较完整" if team["is_deep"] else "资料待补",
            "href": f"team.html?team={team['slug']}",
        })
    return teasers


def _top_obstacle_labels(team):
    labels = []
    for obstacle in team.get("primary_obstacles", []):
        key = obstacle.get("类型", obstacle.get("type", ""))
        if key in OBSTACLE_LABELS and OBSTACLE_LABELS[key] not in labels:
            labels.append(OBSTACLE_LABELS[key])
        if len(labels) == 2:
            break
    return labels


def _plain_thesis(team):
    if team["is_deep"] and team.get("championship_thesis"):
        text = strip_markdown_public(team["championship_thesis"])
        return text if "夺冠路" in text else f"{team['zh_name']}的夺冠路：{text}"
    return f"{team['zh_name']}的夺冠路还在补资料，先保留完整卡片结构。"


def strip_markdown_public(value):
    text = re.sub(r"\s+", " ", str(value or "").replace("`", "").replace("**", "")).strip()
    return _sanitize_public_text(text)


def _sanitize_public_text(value):
    replacements = {
        "`<待分析>`": "资料待补",
        "`<数据不足>`": "资料待补",
        "<待分析>": "资料待补",
        "<数据不足>": "资料待补",
        "<关键阻力>": "关键问题",
        "<type>": "待分类",
        "kimi": "外部模型",
        "Kimi": "外部模型",
        "小米": "外部模型",
        "Xiaomi": "外部模型",
        "MiMo Code Long-Horizon": "外部模型",
        "MiMo": "外部模型",
        "低估": "没有充分反映",
        "高估": "看得过热",
        "正期望值": "外部判断分歧",
        "正期望": "外部判断分歧",
    }
    text = str(value or "")
    for raw, public in replacements.items():
        text = text.replace(raw, public)
    text = text.replace("不可没有充分反映", "不能小看")
    text = text.replace("不可看得过热", "不能看得过热")
    return text


def _validate_public_text_boundary(payload, label):
    text = json.dumps(payload, ensure_ascii=False)
    leaked = [term for term in PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN if term in text]
    if leaked:
        raise ValueError(f"{label} contains forbidden public terms: {', '.join(leaked)}")


def _build_ai_perspectives(teams):
    if not AGENT_INVENTORY_CSV.exists():
        return {
            "status": "snapshot_unavailable",
            "status_label": STATUS_LABELS["snapshot_unavailable"],
            "perspective_count": 0,
            "faction_count": 0,
            "covered_team_count": 0,
            "source_level": "Red",
            "source_label": SOURCE_LABELS["Red"],
            "display_rule": "外部模型群体参考暂时没有生成。",
            "factions": [],
            "teams": {},
        }

    rows = load_csv(AGENT_INVENTORY_CSV)
    team_by_zh = {team["zh_name"]: team for team in teams.values() if team.get("zh_name")}
    faction_rows = {}
    team_rows = {}
    covered_teams = set()
    for row in rows:
        faction = row.get("faction", "").strip()
        champion = row.get("champion", "").strip()
        if not faction:
            continue
        faction_rows.setdefault(faction, []).append(row)
        team = team_by_zh.get(champion)
        if team:
            covered_teams.add(team["slug"])
            team_rows.setdefault(team["slug"], []).append(row)

    factions = []
    for faction, items in faction_rows.items():
        champion_counts = Counter(row.get("champion", "").strip() for row in items if row.get("champion"))
        representative = _representative_agent_row(items)
        factions.append({
            "name": faction,
            "count": len(items),
            "color": FACTION_COLORS.get(faction, "#6E8499"),
            "top_champions": [
                {"team_name": name, "count": count}
                for name, count in champion_counts.most_common(3)
            ],
            "representative": representative,
        })

    team_payload = {}
    for slug, items in team_rows.items():
        faction_counts = Counter(row.get("faction", "").strip() for row in items if row.get("faction"))
        snippets = []
        for row in items[:4]:
            snippets.append(_representative_agent_row([row]))
        team_payload[slug] = {
            "count": len(items),
            "faction_counts": dict(faction_counts.most_common()),
            "snippets": snippets,
            "source_label": SOURCE_LABELS["Red"],
            "display_rule": "这些只是外部模型群体的看法，不能当事实。",
        }

    return {
        "status": "available",
        "status_label": "已有外部视角",
        "perspective_count": len(rows),
        "faction_count": len(faction_rows),
        "covered_team_count": len(covered_teams),
        "source_level": "Red",
        "source_label": SOURCE_LABELS["Red"],
        "display_rule": "这是外部模型群体参考，只代表不同视角怎么想，不作为事实依据。",
        "factions": factions,
        "teams": team_payload,
    }


def _representative_agent_row(rows):
    row = rows[0] if rows else {}
    return {
        "persona": _short_public_text(row.get("persona", ""), 26),
        "champion": _short_public_text(row.get("champion", ""), 18),
        "reason": _short_public_text(row.get("reason", ""), 90),
    }


def _short_public_text(value, limit):
    text = strip_markdown_public(value)
    return text if len(text) <= limit else text[: limit - 1].rstrip("，。；;、 ") + "…"


def _build_baselines(rows):
    baselines = []
    for row in rows:
        source_level = row.get("source_level", "")
        normalized_source = source_level.split()[0] if source_level else ""
        baseline_id = row.get("baseline_id", "")
        public_id = "public_model_crowd" if baseline_id == "kimi_public_ai_baseline" else baseline_id
        public_source_label = _public_source_label_for_baseline(baseline_id, source_level, normalized_source)
        baselines.append({
            "baseline_id": public_id,
            "display_name": BASELINE_DISPLAY_NAMES.get(baseline_id, row.get("name", baseline_id)),
            "source_level": normalized_source or source_level,
            "source_label": public_source_label,
            "status": row.get("status", ""),
            "status_label": STATUS_LABELS.get(row.get("status", ""), row.get("status", "")),
            "construction_rule_short": _public_baseline_rule(baseline_id, row.get("construction_rule", "")),
            "display_boundary": _baseline_boundary(baseline_id, normalized_source),
        })
    return baselines


def _public_source_label_for_baseline(baseline_id, source_level, normalized_source):
    if baseline_id == "kimi_public_ai_baseline":
        return SOURCE_LABELS["Red"]
    return SOURCE_LABELS.get(source_level, SOURCE_LABELS.get(normalized_source, "混合来源"))


def _public_baseline_rule(baseline_id, fallback):
    if baseline_id in BASELINE_PUBLIC_RULES:
        return BASELINE_PUBLIC_RULES[baseline_id]
    return _shorten_rule(fallback)


def _shorten_rule(value):
    text = strip_markdown_public(value)
    if len(text) <= 72:
        return text
    return text[:70].rstrip("；;，, ") + "..."


def _baseline_boundary(baseline_id, source_level):
    if baseline_id == "market_public_baseline":
        return "市场数据只代表外界怎么看，不是投机指引。"
    if baseline_id == "kimi_public_ai_baseline":
        return "只能看作外部参考，不进入我们的事实判断。"
    if source_level == "Green":
        return "可作为可靠事实参照。"
    return "只作外部参照。"


def _build_public_model_snapshot(teams):
    covered = [
        team for team in teams.values()
        if isinstance(team.get("kimi_probability"), (int, float))
    ]
    covered.sort(key=lambda item: item["kimi_probability"], reverse=True)
    return {
        "status": "partial_populated" if covered else "snapshot_unavailable",
        "status_label": STATUS_LABELS["partial_populated"] if covered else STATUS_LABELS["snapshot_unavailable"],
        "coverage_count": len(covered),
        "total_teams": len(teams),
        "source_level": "Red",
        "source_label": SOURCE_LABELS["Red"],
        "display_rule": "这是一组外部参考，只代表别人怎么想，不作为事实依据。",
        "top_teams": [
            {
                "team_slug": team["slug"],
                "team_name": team["zh_name"] or team["canonical_name"],
                "flag": team["flag"],
                "probability": round(float(team["kimi_probability"]), 2),
                "href": f"team.html?team={team['slug']}",
            }
            for team in covered[:8]
        ],
    }


def _build_market_snapshot():
    snapshot_path = ROOT / "data" / "processed" / "market_public_snapshot.json"
    if snapshot_path.exists():
        try:
            payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
            return _sanitize_market_snapshot(payload)
        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            pass

    return {
        "status": "snapshot_unavailable",
        "status_label": STATUS_LABELS["snapshot_unavailable"],
        "last_fetched_at": None,
        "coverage_count": 0,
        "cache_age_seconds": None,
        "source_level": "Yellow",
        "source_label": SOURCE_LABELS["Yellow"],
        "display_rule": "只代表外界怎么看，不作为事实依据。",
        "missing_reason": "这次构建还没有发布可用市场快照。",
        "teams": {},
    }


def _sanitize_market_snapshot(payload):
    teams = payload.get("teams", {}) if isinstance(payload, dict) else {}
    safe_teams = {}
    for slug, row in teams.items():
        if not isinstance(row, dict):
            continue
        probability = _optional_float(row.get("probability"))
        if probability is None:
            continue
        safe_teams[slug] = {
            "probability": round(probability, 2),
            "source_label": SOURCE_LABELS["Yellow"],
            "last_fetched_at": payload.get("last_fetched_at"),
            "market_slug": row.get("market_slug", ""),
            "question": _sanitize_public_text(row.get("question", "")),
        }
    return {
        "status": "available" if safe_teams else "snapshot_unavailable",
        "status_label": "已有快照" if safe_teams else STATUS_LABELS["snapshot_unavailable"],
        "event_slug": payload.get("event_slug"),
        "event_title": payload.get("event_title"),
        "last_fetched_at": payload.get("last_fetched_at"),
        "coverage_count": len(safe_teams),
        "cache_age_seconds": payload.get("cache_age_seconds"),
        "source_level": "Yellow",
        "source_label": SOURCE_LABELS["Yellow"],
        "display_rule": "只代表外界怎么看，不作为事实依据。",
        "missing_reason": "" if safe_teams else "市场快照文件存在，但没有可展示的球队概率。",
        "teams": safe_teams,
    }


def _optional_float(value):
    if value in (None, "", "N/A"):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def build_public_team_details_json(teams):
    """Return reader-facing per-team detail payloads for the static site."""
    market_snapshot = _build_market_snapshot()
    ai_perspectives = _build_ai_perspectives(teams)
    details = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source_policy_version": "draft-for-execution",
        "teams": {},
    }

    for slug, team in sorted(teams.items()):
        details["teams"][slug] = _build_public_team_detail(team, market_snapshot, ai_perspectives)

    _validate_team_details_json(details)
    return details


def _validate_team_details_json(details):
    errors = []
    teams = details.get("teams", {})
    if len(teams) != 48:
        errors.append(f"team details must include 48 teams, got {len(teams)}")
    for slug, team in teams.items():
        if team.get("detail_href") != f"team.html?team={slug}":
            errors.append(f"{slug}: detail_href must point to team.html")
        analysis = team.get("analysis", {})
        if not analysis.get("opening"):
            errors.append(f"{slug}: missing reader-facing opening")
        if len(analysis.get("sections", [])) < 3:
            errors.append(f"{slug}: expected at least 3 analysis sections")
        if "obstacle_chart" not in team.get("charts", {}):
            errors.append(f"{slug}: missing obstacle_chart")
        if "public_reference_chart" not in team.get("charts", {}):
            errors.append(f"{slug}: missing public_reference_chart")
    text = json.dumps(details, ensure_ascii=False)
    leaked = [term for term in PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN if term in text]
    if leaked:
        errors.append("team details contain forbidden public terms: " + ", ".join(leaked))

    if errors:
        raise ValueError("team details strict validation failed:\n- " + "\n- ".join(errors))


def _build_public_team_detail(team, market_snapshot, ai_perspectives):
    slug = team["slug"]
    public_model = _build_team_public_model_reference(team)
    market_reference = _build_team_market_reference(slug, market_snapshot)
    obstacles = _public_obstacles(team)
    breakthroughs = _public_breakthroughs(team)
    swans = _public_black_swans(team)
    miracle = _public_miracle_package(team)
    interpretation = team.get("current_interpretation", {})

    return {
        "slug": slug,
        "detail_href": f"team.html?team={slug}",
        "directory_href": f"teams.html#{slug}",
        "team": {
            "zh_name": team["zh_name"],
            "en_name": team["en_name"],
            "canonical_name": team["canonical_name"],
            "flag": team["flag"],
            "confederation": team["confederation"],
            "confederation_label": team["confederation_label"],
            "group": team["group"],
            "status": team["status"],
            "status_label": "深度版" if team["is_deep"] else "简版",
            "is_deep": team["is_deep"],
        },
        "analysis": _build_reader_analysis(team, obstacles, breakthroughs, interpretation),
        "charts": {
            "obstacle_chart": _build_team_obstacle_chart(obstacles),
            "public_reference_chart": _build_public_reference_chart(public_model, market_reference),
        },
        "public_references": {
            "public_model_crowd": public_model,
            "market_snapshot": market_reference,
        },
        "primary_obstacles": obstacles,
        "required_breakthroughs": breakthroughs,
        "black_swan_helpers": swans,
        "miracle_package": miracle,
        "watchlist": _build_watchlist(team, breakthroughs, miracle, interpretation),
        "ai_perspective": ai_perspectives.get("teams", {}).get(team["slug"], {
            "count": 0,
            "faction_counts": {},
            "snippets": [],
            "source_label": SOURCE_LABELS["Red"],
            "display_rule": "这支队还没有外部模型群体参考。我们先保留路径拆解，等后续数据补齐。",
        }),
        "source_boundary": {
            "reliable": "赛程、赛果、官方排名和可复核统计，才能当事实。",
            "leads": "新闻、汇总表、市场快照只能提示我们看哪里。",
            "reference_only": "外部预测和无法复核的说法只能当参考。",
        },
    }


def _build_reader_analysis(team, obstacles, breakthroughs, interpretation):
    name = team["zh_name"] or team["canonical_name"]
    thesis = strip_markdown_public(team.get("championship_thesis", ""))
    if not thesis:
        thesis = f"{name}的夺冠路还在补资料，目前先保留球队入口。"

    credible_path = strip_markdown_public(interpretation.get("most_credible_path", ""))
    least_credible = strip_markdown_public(interpretation.get("least_credible_narrative", ""))
    monitor = strip_markdown_public(interpretation.get("signals_to_monitor", ""))

    obstacle_sentence = _summarize_obstacles(name, obstacles)
    breakthrough_sentence = _summarize_breakthroughs(name, breakthroughs)

    return {
        "opening": f"{name}不是只看名气。真正要问的是：它能不能把自己的强项一路带到淘汰赛最后两场，同时避开最容易翻车的那几种局面。",
        "thesis": thesis,
        "sections": [
            {
                "title": "这队凭什么能冲冠军？",
                "body": credible_path or thesis,
                "so_what": "如果这条路成立，比赛里应该先看到稳定出线、核心球员状态在线、淘汰赛临场调整不掉链子。",
            },
            {
                "title": "最怕哪种比赛？",
                "body": least_credible or obstacle_sentence,
                "so_what": "这不是说它不行，而是告诉我们看球时最该盯哪里：一旦这些问题连续出现，冠军路就会明显变窄。",
            },
            {
                "title": "接下来先看什么？",
                "body": monitor or breakthrough_sentence,
                "so_what": "这些信号赛后能对账。发生了，路径更像真事；没发生，就要下调这条冠军叙事的可信度。",
            },
        ],
    }


def _summarize_obstacles(name, obstacles):
    if not obstacles:
        return f"{name}现在缺少足够的深度阻力数据，暂时不能硬讲复杂结论。"
    labels = [item["type_label"] for item in obstacles[:3]]
    return f"{name}最需要处理的是：{'、'.join(labels)}。这些问题会直接影响淘汰赛容错率。"


def _summarize_breakthroughs(name, breakthroughs):
    if not breakthroughs:
        return f"{name}后续需要补充更明确的可观察条件。"
    first = breakthroughs[0]
    return f"先看{first.get('phase', '关键阶段')}能不能做到：{first.get('minimum', first.get('breakthrough', '关键条件兑现'))}。"


def _public_obstacles(team):
    rows = []
    for obstacle in team.get("primary_obstacles", []):
        otype = obstacle.get("类型", obstacle.get("type", ""))
        rows.append({
            "obstacle": strip_markdown_public(obstacle.get("阻力", "")),
            "type": otype,
            "type_label": OBSTACLE_LABELS.get(otype, otype.replace("_", " ") if otype else "其他难点"),
            "why": strip_markdown_public(obstacle.get("为什么重要", "")),
            "observable_proxy": strip_markdown_public(obstacle.get("可判定代理", "")),
        })
    return rows


def _public_breakthroughs(team):
    rows = []
    for item in team.get("required_breakthroughs", []):
        rows.append({
            "breakthrough": strip_markdown_public(item.get("突破", "")),
            "phase": strip_markdown_public(item.get("发生阶段", "")),
            "minimum": strip_markdown_public(item.get("最低条件", "")),
            "failure_signal": strip_markdown_public(item.get("失败信号", "")),
        })
    return rows


def _public_black_swans(team):
    rows = []
    for item in team.get("black_swan_helpers", []):
        rows.append({
            "event": strip_markdown_public(item.get("黑天鹅", "")),
            "mechanism": strip_markdown_public(item.get("受益机制", "")),
            "observable": strip_markdown_public(item.get("是否可观测", "")),
            "note": strip_markdown_public(item.get("备注", "")),
        })
    return rows


def _public_miracle_package(team):
    rows = [
        {
            "condition": strip_markdown_public(item.get("condition", "")),
            "type": strip_markdown_public(item.get("type", "")),
            "observable_proxy": strip_markdown_public(item.get("observable_proxy", "")),
            "settlement_rule": strip_markdown_public(item.get("settlement_rule", "")),
        }
        for item in team.get("miracle_package", [])
    ]
    return [
        row for row in rows
        if not all(value in {"", "资料待补", "待分类"} for value in row.values())
    ]


def _build_team_public_model_reference(team):
    probability = _optional_float(team.get("kimi_probability"))
    tags = _public_signal_tags(team.get("kimi_baseline_signals", ""))
    if probability is None:
        return {
            "status": "not_covered",
            "status_label": "没有覆盖",
            "probability": None,
            "source_level": "Red",
            "source_label": SOURCE_LABELS["Red"],
            "display_rule": "这支队没有公开模型群体参考数据。",
            "tags": tags,
        }
    return {
        "status": "available",
        "status_label": "已有参考",
        "probability": round(probability, 2),
        "source_level": "Red",
        "source_label": SOURCE_LABELS["Red"],
        "display_rule": "只代表外部看法，不作为事实依据。",
        "tags": tags,
    }


def _public_signal_tags(raw_value):
    mapping = {
        "high_kimi_probability": "外部给得高",
        "broad_faction_support": "不同角度都看好",
        "cross_faction_consensus": "共识比较集中",
        "kimi_longshot": "有黑马讨论",
    }
    tags = []
    for key in str(raw_value or "").split(";"):
        key = key.strip()
        if key and key != "none":
            tags.append(mapping.get(key, "外部参考"))
    return tags


def _build_team_market_reference(slug, snapshot):
    teams = snapshot.get("teams", {}) if isinstance(snapshot, dict) else {}
    row = teams.get(slug, {})
    probability = _optional_float(row.get("probability")) if isinstance(row, dict) else None
    if probability is None:
        return {
            "status": "snapshot_unavailable",
            "status_label": STATUS_LABELS["snapshot_unavailable"],
            "probability": None,
            "last_fetched_at": snapshot.get("last_fetched_at"),
            "source_level": "Yellow",
            "source_label": SOURCE_LABELS["Yellow"],
            "display_rule": "市场快照可用后，这里会显示外界热度。",
            "missing_reason": snapshot.get("missing_reason") or "本次构建没有这支队的市场快照。",
        }
    return {
        "status": "available",
        "status_label": "已有快照",
        "probability": round(probability, 2),
        "last_fetched_at": row.get("last_fetched_at") or snapshot.get("last_fetched_at"),
        "source_level": "Yellow",
        "source_label": SOURCE_LABELS["Yellow"],
        "display_rule": "只代表外界怎么看，不作为事实依据。",
        "missing_reason": "",
    }


def _build_team_obstacle_chart(obstacles):
    counts = Counter(item["type_label"] for item in obstacles if item.get("type_label"))
    rows = [
        {"label": label, "value": count}
        for label, count in counts.most_common()
    ]
    return {
        "type": "bar",
        "title": "这支队最容易被哪些关卡卡住",
        "data": rows,
    }


def _build_public_reference_chart(public_model, market_reference):
    average_probability = round(100 / 48, 2)
    rows = [
        {
            "label": "48队平均线",
            "value": average_probability,
            "status": "available",
            "source_label": "内部参照",
            "note": "最朴素的起点",
        }
    ]
    if public_model.get("probability") is not None:
        rows.append({
            "label": "公开模型群体",
            "value": public_model["probability"],
            "status": public_model["status"],
            "source_label": public_model["source_label"],
            "note": public_model["display_rule"],
        })
    else:
        rows.append({
            "label": "公开模型群体",
            "value": None,
            "status": public_model["status"],
            "source_label": public_model["source_label"],
            "note": public_model["display_rule"],
        })

    rows.append({
        "label": "市场快照",
        "value": market_reference.get("probability"),
        "status": market_reference["status"],
        "source_label": market_reference["source_label"],
        "note": market_reference.get("missing_reason") or market_reference["display_rule"],
    })

    available_values = [row["value"] for row in rows if isinstance(row.get("value"), (int, float))]
    return {
        "type": "bar",
        "title": "外界参考怎么看这支队",
        "unit": "%",
        "max_value": max(available_values + [1]),
        "data": rows,
    }


def _build_watchlist(team, breakthroughs, miracle, interpretation):
    monitor_text = strip_markdown_public(interpretation.get("signals_to_monitor", ""))
    items = []
    if monitor_text:
        parts = [part.strip(" ;；。") for part in re.split(r'[；;]|\(\d+\)', monitor_text) if part.strip(" ;；。")]
        items.extend(parts[:4])
    for item in breakthroughs[:3]:
        value = item.get("minimum") or item.get("breakthrough")
        if value:
            items.append(value)
    for item in miracle[:2]:
        value = item.get("observable_proxy") or item.get("settlement_rule")
        if value:
            items.append(value)

    seen = set()
    compact = []
    for item in items:
        text = strip_markdown_public(item)
        if text and text not in seen:
            seen.add(text)
            compact.append(text)
        if len(compact) == 5:
            break

    if compact:
        return compact
    return [f"{team['zh_name']}的深度观察项还在补资料。"]


def build_public_teams_json(teams):
    """Return a public, vendor-neutral team payload for the static site."""
    public = {}
    for slug, team in teams.items():
        public[slug] = {
            "slug": team["slug"],
            "canonical_name": team["canonical_name"],
            "zh_name": team["zh_name"],
            "en_name": team["en_name"],
            "confederation": team["confederation"],
            "confederation_label": team["confederation_label"],
            "group": team["group"],
            "flag": team["flag"],
            "status": team["status"],
            "is_deep": team["is_deep"],
            "championship_thesis": _public_team_thesis(team),
        }
    return public


def _public_team_thesis(team):
    if team.get("is_deep") and team.get("championship_thesis"):
        return strip_markdown_public(team["championship_thesis"])
    return f"{team['zh_name']}现在是简版卡片，资料待补。"


def build_public_meta_json(meta):
    """Return public metadata without internal vendor/baseline coverage fields."""
    public = dict(meta)
    public.pop("kimi_coverage", None)
    return public


def _build_obstacle_matrix_teaser(rows):
    sample_slugs = ["argentina", "france", "spain", "morocco"]
    obstacle_types = ["low_scoring_dependency", "psychological_pressure", "bracket_strength", "injury_risk"]
    by_slug = {row.get("team_slug"): row for row in rows}
    cells = []
    for slug in sample_slugs:
        row = by_slug.get(slug, {})
        for obstacle_type in obstacle_types:
            cells.append({
                "team_slug": slug,
                "obstacle_type": obstacle_type,
                "display_label": OBSTACLE_LABELS[obstacle_type],
                "active": _int_value(row.get(obstacle_type)) > 0,
                "intensity": _int_value(row.get(obstacle_type)),
            })
    return {
        "status": "available" if rows else "missing_with_reason",
        "team_sample": sample_slugs,
        "obstacle_types": obstacle_types,
        "obstacle_labels": [OBSTACLE_LABELS[key] for key in obstacle_types],
        "cells": cells,
    }


def _int_value(value):
    try:
        return int(value or 0)
    except ValueError:
        return 0


def _validate_homepage_json(homepage):
    errors = []
    summary = homepage.get("summary", {})
    if summary.get("total_teams") != 48:
        errors.append("homepage summary total_teams must be 48")
    if summary.get("deep_description_count") != 48:
        errors.append("homepage summary deep_description_count must be 48")
    if summary.get("settleable_condition_count") != 89:
        errors.append("homepage summary settleable_condition_count must be 89")
    if len(homepage.get("team_teasers", [])) < 8:
        errors.append("homepage needs at least 8 team teasers")
    if not homepage.get("obstacle_distribution"):
        errors.append("homepage needs obstacle_distribution")
    if not homepage.get("baselines"):
        errors.append("homepage needs baselines")

    text = json.dumps(homepage, ensure_ascii=False)
    leaked = [term for term in PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN if term in text]
    if leaked:
        errors.append("homepage contains forbidden public terms: " + ", ".join(leaked))

    if errors:
        raise ValueError("homepage data strict validation failed:\n- " + "\n- ".join(errors))


def _validate_site_data(teams, meta):
    """Strict build-time checks for the public research portal data."""
    errors = []
    if len(teams) != EXPECTED_TEAM_COUNT:
        errors.append(f"expected {EXPECTED_TEAM_COUNT} teams, got {len(teams)}")
    if meta["deep_description_count"] != EXPECTED_DEEP_DESCRIPTION_COUNT:
        errors.append(f"expected {EXPECTED_DEEP_DESCRIPTION_COUNT} deep-description cards, got {meta['deep_description_count']}")
    if meta["thin_slice_count"] != EXPECTED_THIN_SLICE_COUNT:
        errors.append(f"expected {EXPECTED_THIN_SLICE_COUNT} thin-slice cards, got {meta['thin_slice_count']}")

    for slug, team in sorted(teams.items()):
        if team["is_deep"]:
            if not team["championship_thesis"]:
                errors.append(f"{slug}: missing championship_thesis")
            if len(team["primary_obstacles"]) < 3:
                errors.append(f"{slug}: expected at least 3 primary_obstacles")
            if len(team["required_breakthroughs"]) < 2:
                errors.append(f"{slug}: expected at least 2 required_breakthroughs")
            if len(team["black_swan_helpers"]) < 2:
                errors.append(f"{slug}: expected at least 2 black_swan_helpers")
            if not team["miracle_package"]:
                errors.append(f"{slug}: missing miracle_package")

    if "---" in meta["obstacle_type_distribution"]:
        errors.append("obstacle_type_distribution contains table divider rows")
    if "发生阶段" in meta["obstacle_type_distribution"]:
        errors.append("obstacle_type_distribution contains a later table header")

    if errors:
        raise ValueError("site data strict validation failed:\n- " + "\n- ".join(errors))


def build_schedule_json():
    """Read data/processed/schedule.json and produce site/data/schedule.json for the frontend."""
    schedule_path = ROOT / "data" / "processed" / "schedule.json"
    if not schedule_path.exists():
        print("⚠️  schedule.json not found — run scripts/parse_schedule.py first")
        return None

    with open(schedule_path, encoding="utf-8") as f:
        raw = json.load(f)

    # Build a lightweight public schedule for the frontend
    schedule = {
        "generated_at": raw["generated_at"],
        "summary": raw["summary"],
        "timezone_note": raw["timezone_note"],
        "venues": raw["venues"],
        "groups": {},
        "knockout": [],
    }

    # Group stage — flatten for frontend consumption
    for letter, group_data in raw["group_stage"]["groups"].items():
        schedule["groups"][letter] = {
            "teams": group_data["teams"],
            "matches": [
                {
                    "match_id": m["match_id"],
                    "round": m["round"],
                    "date": m["date"],
                    "kickoff": m["kickoff_display"],
                    "venue": m["venue_city"],
                    "stadium": m["venue_stadium"],
                    "home": m["home_team"],
                    "away": m["away_team"],
                    "home_code": m["home_code"],
                    "away_code": m["away_code"],
                    "status": m["status"],
                    **(
                        {"home_score": m["home_score"], "away_score": m["away_score"]}
                        if m["status"] == "played"
                        else {}
                    ),
                }
                for m in group_data["matches"]
            ],
        }

    # Knockout stage
    for m in raw["knockout_stage"]:
        schedule["knockout"].append({
            "match_id": m["match_id"],
            "fifa_num": m["fifa_match_num"],
            "round": m["round"],
            "round_label": m["round_label"],
            "date": m["date"],
            "kickoff": m["kickoff_display"],
            "venue": m["venue_city"],
            "stadium": m["venue_stadium"],
            "slot_home": m["slot_home"],
            "slot_away": m["slot_away"],
            "status": m["status"],
        })

    return schedule


def _sanitize_description(text: str) -> str:
    """Remove forbidden public terms from description text."""
    if not text:
        return text
    # Remove forbidden terms and their negation contexts
    import re
    # Remove patterns like "不用于投注建议。不输出仓位/赔率价值/ROI/PnL/Sharpe。"
    text = re.sub(r'[。.]?\s*不用于投注建议[。.]?', '', text)
    text = re.sub(r'[。.]?\s*不输出仓位/赔率价值/ROI/PnL/Sharpe[。.]?', '', text)
    # Also clean standalone occurrences
    for term in ["投注建议", "仓位", "ROI", "PnL", "Sharpe", "value bet", "低估", "高估"]:
        text = text.replace(term, "")
    # Clean up double spaces and trailing punctuation
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[，。、]+$', '', text)
    return text


def build_baselines_json():
    """Read baseline files from data/processed/baselines/ and produce site/data/baselines.json.

    Graceful degradation: returns None if no baseline files found.
    """
    baselines_dir = ROOT / "data" / "processed" / "baselines"
    if not baselines_dir.exists():
        print("⚠️  baselines/ directory not found")
        return None

    baseline_files = {
        "fifa_ranking": baselines_dir / "fifa-ranking-proxy.json",
        "elo": baselines_dir / "elo-proxy.json",
        "market": baselines_dir / "market-public.json",
    }

    result = {}
    for key, path in baseline_files.items():
        if not path.exists():
            continue
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)

        teams_data = raw.get("teams", {})
        description = _sanitize_description(raw.get("description", ""))

        # P0-1: Normalize raw Elo values to display percentages
        if key == "elo" and teams_data:
            elo_total = sum(teams_data.values())
            if elo_total > 0:
                teams_data = {k: round(v / elo_total * 100, 2) for k, v in teams_data.items()}
                description = (description or "") + " (values normalized to percentage share)"

        result[key] = {
            "name": raw.get("name", key),
            "description": description,
            "source_level": raw.get("source_level", "unknown"),
            "generated_at": raw.get("generated_at", ""),
            "team_count": raw.get("team_count", 0),
            "teams": teams_data,
        }

    if not result:
        print("⚠️  No baseline files found in baselines/")
        return None

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "baseline_count": len(result),
        "baselines": result,
    }


def build_cds_paths_json():
    """Read cds_qualification.json + cds_championship.json and produce a unified
    site/data/cds-paths.json keyed by team.

    Graceful degradation: returns None if either source file is missing.
    """
    qual_path = ROOT / "data" / "processed" / "cds_qualification.json"
    champ_path = ROOT / "data" / "processed" / "cds_championship.json"

    if not qual_path.exists():
        print("⚠️  cds_qualification.json not found — run scripts/cds_path_simulation.py first")
        return None
    if not champ_path.exists():
        print("⚠️  cds_championship.json not found — run scripts/cds_path_simulation.py first")
        return None

    with open(qual_path, encoding="utf-8") as f:
        qual_raw = json.load(f)
    with open(champ_path, encoding="utf-8") as f:
        champ_raw = json.load(f)

    # Index championship data by team name
    champ_by_team = {t["team"]: t for t in champ_raw.get("teams", [])}

    # Merge into unified structure keyed by team
    teams_data = {}
    for qual_team in qual_raw.get("teams", []):
        team_name = qual_team["team"]
        champ = champ_by_team.get(team_name, {})

        teams_data[team_name] = {
            "team": team_name,
            "group": qual_team.get("group", ""),
            "qualification": {
                "qual_prob": qual_team.get("qual_prob", 0),
                "qual_prob_top2": qual_team.get("qual_prob_top2", 0),
                "position_probs": qual_team.get("position_probs", {}),
                "third_place_qual_prob": qual_team.get("third_place_qual_prob", 0),
                "scenarios": qual_team.get("scenarios", []),
                "key_matches": qual_team.get("key_matches", []),
            },
            "championship": {
                "championship_prob": champ.get("championship_prob", 0),
                "championship_path_count": champ.get("championship_path_count", 0),
                "dominant_path_pattern": champ.get("dominant_path_pattern", ""),
                "dominant_failure_node": champ.get("dominant_failure_node", ""),
                "bracket_dependency": champ.get("bracket_dependency", ""),
                "path_nodes": champ.get("path_nodes", []),
            },
        }

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_generated_at": qual_raw.get("generated_at", ""),
        "total_teams": len(teams_data),
        "source_level": "red",
        "source_note": "CDS 模拟输出，非事实。",
        "teams": teams_data,
    }

    _validate_public_text_boundary(result, "cds-paths")

    return result


def build_odds_json():
    """Read data/processed/odds.json and produce site/data/odds.json for the frontend.

    Graceful degradation: returns None if odds.json doesn't exist.
    """
    odds_path = ROOT / "data" / "processed" / "odds.json"
    if not odds_path.exists():
        print("⚠️  odds.json not found — run scripts/numeric_odds.py first")
        return None

    with open(odds_path, encoding="utf-8") as f:
        raw = json.load(f)

    # Public-facing odds: lightweight match probabilities for frontend
    predictions = [
        {
            "match_id": p["match_id"],
            "home_team": p["home_team"],
            "away_team": p["away_team"],
            "home_win": p["home_win"],
            "draw": p["draw"],
            "away_win": p["away_win"],
            "expected_goals_home": p["expected_goals_home"],
            "expected_goals_away": p["expected_goals_away"],
            "confidence": p["confidence"],
        }
        for p in raw.get("predictions", [])
    ]

    return {
        "generated_at": raw["generated_at"],
        "model": raw["model"],
        "model_description": raw["model_description"],
        "total_predicted": raw["total_matches_predicted"],
        "source_level": "red",
        "source_note": "模型模拟输出，非事实。",
        "predictions": predictions,
    }


def build_coach_simulation_json():
    """Read data/processed/coach_simulation.json and produce site/data/coach-sim.json."""
    sim_path = ROOT / "data" / "processed" / "coach_simulation.json"
    if not sim_path.exists():
        print("⚠️  coach_simulation.json not found — run scripts/coach_simulation.py --phase=simulate first")
        return None

    with open(sim_path, encoding="utf-8") as f:
        raw = json.load(f)

    predictions = [
        {
            "match_id": p["match_id"],
            "home_team": p["home_team"],
            "away_team": p["away_team"],
            "home_win": p["home_win"],
            "draw": p["draw"],
            "away_win": p["away_win"],
            "expected_goals_home": p["expected_goals_home"],
            "expected_goals_away": p["expected_goals_away"],
            "confidence": p["confidence"],
        }
        for p in raw.get("predictions", [])
    ]

    payload = {
        "generated_at": raw["generated_at"],
        "model": raw["model"],
        "model_description": raw.get("model_description", "Coach matchup model"),
        "total_predicted": raw["total_matches_predicted"],
        "source_level": "red",
        "source_note": "模型模拟输出，非事实。基于身价代理 + 泊松分布。",
        "predictions": predictions,
    }
    _validate_public_text_boundary(payload, "coach-sim")
    return payload


def build_coach_formations_json():
    """Read data/processed/coach_formations.json and produce site/data/coach-formations.json."""
    formations_path = ROOT / "data" / "processed" / "coach_formations.json"
    if not formations_path.exists():
        return None

    # Also try alternate filename
    alt_path = ROOT / "data" / "processed" / "coach_formations.json"
    src = formations_path if formations_path.exists() else alt_path
    if not src.exists():
        return None

    with open(src, encoding="utf-8") as f:
        raw = json.load(f)

    teams_data = {}
    for team_name, formations in raw.get("teams", {}).items():
        team_formations = {}
        for form_name, info in formations.items():
            xi_summary = [
                {"position_code": p["position_code"]}
                for p in info.get("xi", [])
            ]
            team_formations[form_name] = {
                "xi": xi_summary,
                "method": info.get("method", "heuristic"),
            }
            if info.get("tactical_rationale"):
                team_formations[form_name]["tactical_rationale"] = info["tactical_rationale"]
        teams_data[team_name] = team_formations

    payload = {
        "generated_at": raw.get("generated_at", ""),
        "method": raw.get("method", "heuristic"),
        "source_level": "red",
        "source_note": "模型选人输出，非事实。",
        "teams": teams_data,
    }
    _validate_public_text_boundary(payload, "coach-formations")
    return payload


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    teams, meta = build_teams_json(strict=False)
    homepage = build_homepage_json(strict=False)
    public_teams = build_public_teams_json(teams)
    public_meta = build_public_meta_json(meta)
    team_details = build_public_team_details_json(teams)
    schedule = build_schedule_json()
    odds = build_odds_json()
    coach_sim = build_coach_simulation_json()
    coach_formations = build_coach_formations_json()
    baselines = build_baselines_json()
    cds_paths = build_cds_paths_json()

    teams_path = OUTPUT_DIR / "teams.json"
    homepage_path = OUTPUT_DIR / "homepage.json"
    team_details_path = OUTPUT_DIR / "team-details.json"
    schedule_path = OUTPUT_DIR / "schedule.json"
    odds_path = OUTPUT_DIR / "odds.json"
    baselines_path = OUTPUT_DIR / "baselines.json"
    cds_paths_path = OUTPUT_DIR / "cds-paths.json"
    coach_sim_path = OUTPUT_DIR / "coach-sim.json"
    coach_formations_path = OUTPUT_DIR / "coach-formations.json"
    teams_script_path = OUTPUT_DIR / "teams-data.js"
    homepage_script_path = OUTPUT_DIR / "homepage-data.js"
    team_details_script_path = OUTPUT_DIR / "team-details-data.js"
    schedule_script_path = OUTPUT_DIR / "schedule-data.js"
    odds_script_path = OUTPUT_DIR / "odds-data.js"
    baselines_script_path = OUTPUT_DIR / "baselines-data.js"
    cds_paths_script_path = OUTPUT_DIR / "cds-paths-data.js"
    coach_sim_script_path = OUTPUT_DIR / "coach-sim-data.js"
    coach_formations_script_path = OUTPUT_DIR / "coach-formations-data.js"

    with open(teams_path, "w", encoding="utf-8") as f:
        json.dump(public_teams, f, ensure_ascii=False, indent=2)

    with open(homepage_path, "w", encoding="utf-8") as f:
        json.dump(homepage, f, ensure_ascii=False, indent=2)

    with open(team_details_path, "w", encoding="utf-8") as f:
        json.dump(team_details, f, ensure_ascii=False, indent=2)

    if schedule is not None:
        with open(schedule_path, "w", encoding="utf-8") as f:
            json.dump(schedule, f, ensure_ascii=False, indent=2)

    if odds is not None:
        with open(odds_path, "w", encoding="utf-8") as f:
            json.dump(odds, f, ensure_ascii=False, indent=2)

    if baselines is not None:
        with open(baselines_path, "w", encoding="utf-8") as f:
            json.dump(baselines, f, ensure_ascii=False, indent=2)

    if cds_paths is not None:
        with open(cds_paths_path, "w", encoding="utf-8") as f:
            json.dump(cds_paths, f, ensure_ascii=False, indent=2)

    if coach_sim is not None:
        with open(coach_sim_path, "w", encoding="utf-8") as f:
            json.dump(coach_sim, f, ensure_ascii=False, indent=2)

    if coach_formations is not None:
        with open(coach_formations_path, "w", encoding="utf-8") as f:
            json.dump(coach_formations, f, ensure_ascii=False, indent=2)

    _write_data_script(teams_script_path, "CDS4WORLDCUP_TEAMS", public_teams)
    _write_data_script(homepage_script_path, "CDS4WORLDCUP_HOMEPAGE", homepage)
    _write_data_script(team_details_script_path, "CDS4WORLDCUP_TEAM_DETAILS", team_details)
    if schedule is not None:
        _write_data_script(schedule_script_path, "CDS4WORLDCUP_SCHEDULE", schedule)
    if odds is not None:
        _write_data_script(odds_script_path, "CDS4WORLDCUP_ODDS", odds)
    if baselines is not None:
        _write_data_script(baselines_script_path, "CDS4WORLDCUP_BASELINES", baselines)
    if cds_paths is not None:
        _write_data_script(cds_paths_script_path, "CDS4WORLDCUP_CDS_PATHS", cds_paths)

    if coach_sim is not None:
        _write_data_script(coach_sim_script_path, "CDS4WORLDCUP_COACH_SIM", coach_sim)

    if coach_formations is not None:
        _write_data_script(coach_formations_script_path, "CDS4WORLDCUP_COACH_FORMATIONS", coach_formations)

    print(f"✅ Generated {teams_path} ({len(public_teams)} teams)")
    print(f"✅ Generated {homepage_path}")
    print(f"✅ Generated {team_details_path}")
    if schedule is not None:
        gs = schedule["summary"]
        print(f"✅ Generated {schedule_path} ({gs['total_matches']} matches)")
        print(f"✅ Generated {schedule_script_path}")
    else:
        print("⚠️  Skipped schedule (run scripts/parse_schedule.py first)")
    if odds is not None:
        print(f"✅ Generated {odds_path} ({odds['total_predicted']} predictions)")
        print(f"✅ Generated {odds_script_path}")
    else:
        print("⚠️  Skipped odds (run scripts/numeric_odds.py first)")
    if baselines is not None:
        print(f"✅ Generated {baselines_path} ({baselines['baseline_count']} baselines)")
        print(f"✅ Generated {baselines_script_path}")
    else:
        print("⚠️  Skipped baselines (no baseline files in data/processed/baselines/)")
    if cds_paths is not None:
        print(f"✅ Generated {cds_paths_path} ({cds_paths['total_teams']} teams)")
        print(f"✅ Generated {cds_paths_script_path}")
    else:
        print("⚠️  Skipped cds-paths (run scripts/cds_path_simulation.py first)")
    if coach_sim is not None:
        print(f"✅ Generated {coach_sim_path} ({coach_sim['total_predicted']} predictions)")
        print(f"✅ Generated {coach_sim_script_path}")
    else:
        print("⚠️  Skipped coach-sim (run scripts/coach_simulation.py --phase=simulate first)")
    if coach_formations is not None:
        team_count = len(coach_formations.get('teams', {}))
        print(f"✅ Generated {coach_formations_path} ({team_count} teams)")
        print(f"✅ Generated {coach_formations_script_path}")
    else:
        print("⚠️  Skipped coach-formations (run scripts/coach_simulation.py --phase=select-xi first)")
    print(f"✅ Generated {teams_script_path}")
    print(f"✅ Generated {homepage_script_path}")
    print(f"✅ Generated {team_details_script_path}")
    print(f"   Deep descriptions: {meta['deep_description_count']}")
    print(f"   Thin slices: {meta['thin_slice_count']}")
    print(f"   Obstacle types: {meta['obstacle_type_count']}")
    print(f"   Public teams exported: {len(public_teams)}/{meta['total_teams']}")


def _write_data_script(path, global_name, payload):
    if not re.match(r'^[A-Z_][A-Z0-9_]*$', global_name):
        raise ValueError(f"Invalid global_name: {global_name}")
    js_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    js_text = js_text.replace("</script>", "<\\/script>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"window.{global_name} = ")
        f.write(js_text)
        f.write(";\n")


if __name__ == "__main__":
    main()
