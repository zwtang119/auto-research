#!/usr/bin/env python3
"""
generate_path_cards.py — Plan A1: 48 队薄切片路径卡生成器

用法: python3 scripts/generate_path_cards.py
输出: artifacts/team-cards/<team_slug>.md + artifacts/team-cards/README.md + data/processed/kimi_baseline_signals_matrix.csv
"""

import csv
import json
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.slug import slugify
from src.utils.kimi import group_kimi_by_team, compute_signals, build_section_9

TEAM_REGISTRY = ROOT / "data" / "processed" / "team_registry.csv"
KIMI_INVENTORY = ROOT / "data" / "processed" / "kimi_agent_inventory.csv"
KIMI_AGG = ROOT / "data" / "raw" / "kimi" / "kimi_300_unpacked" / "wc2026_aggregation.json"
OUTPUT_DIR = ROOT / "artifacts" / "team-cards"
SIGNALS_CSV = ROOT / "data" / "processed" / "kimi_baseline_signals_matrix.csv"

TODAY = str(date.today())

# ── 读取数据 ──────────────────────────────────────────

def load_team_registry():
    teams = []
    with open(TEAM_REGISTRY, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            teams.append(row)
    return teams

def load_kimi_inventory():
    agents = []
    with open(KIMI_INVENTORY, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            agents.append(row)
    return agents

def load_kimi_aggregation():
    with open(KIMI_AGG, encoding="utf-8") as f:
        return json.load(f)

# ── 聚合数据查找 ──────────────────────────────────────────

def get_team_aggregation(agg, team_en, team_zh):
    """从 all_teams 和 top8 获取球队聚合数据"""
    # 先用中文名匹配（aggregation 用中文）
    for t in agg.get("all_teams", []):
        if t["team"] == team_zh or t["team"] == team_en:
            return t
    for t in agg.get("top8", []):
        if t["team"] == team_zh or t["team"] == team_en:
            return t
    return None

# ── 生成路径卡 ─────────────────────────────────────────

def generate_card(team, kimi_by_team, agg):
    slug = slugify(team["canonical_team"])
    zh = team["zh_name"]
    en = team["en_name"]
    conf = team["confederation"]
    group = team.get("group", "")
    coverage = team["coverage_status"]
    has_kimi = coverage == "champion/top3"

    # Kimi 数据
    kimi_agents = kimi_by_team.get(zh, [])
    team_agg = get_team_aggregation(agg, en, zh)
    kimi_prob = team_agg.get("probability", "N/A") if team_agg else "N/A"
    kimi_votes = team_agg.get("raw_votes", "N/A") if team_agg else "N/A"

    signals = compute_signals(team, kimi_agents, kimi_prob)

    # 薄切片路径卡内容
    lines = []
    lines.append(f"# Championship Path Simulation Card: {zh} ({en})\n")
    lines.append(f"> **类型**: path-card-mvp-a1")
    lines.append(f"> **状态**: thin-slice")
    lines.append(f"> **日期**: {TODAY}")
    lines.append(f"> **team_slug**: `{slug}`\n")

    # ── 1. Team Profile ──
    lines.append("## 1. Team Profile\n")
    lines.append("```yaml")
    lines.append(f"team: {zh} ({en})")
    lines.append(f"team_slug: {slug}")
    lines.append(f"confederation: {conf}")
    lines.append(f"group: {group}")
    lines.append("tier: unassigned")
    lines.append("tier_status: pending_data_gate")
    lines.append("path_type: unassigned")
    lines.append("path_type_status: unassigned")
    lines.append(f"kimi_baseline_signals:")
    for s in signals:
        lines.append(f"  - {s}")
    if not signals:
        lines.append("  - none_yet")
    lines.append("source_status:")
    if has_kimi:
        lines.append("  green_sources: []")
        lines.append(f"  yellow_sources: [kimi-aggregation]")
        lines.append(f"  red_sources: [kimi-300-agent-reasons]")
        lines.append("  coverage: partial")
    else:
        lines.append("  green_sources: []")
        lines.append("  yellow_sources: []")
        lines.append("  red_sources: []")
        lines.append("  coverage: thin")
    lines.append("```\n")

    if not has_kimi:
        lines.append(f"> ⚠️ **数据缺口**: {zh} 未出现在 Kimi 300 Agent 预测中。本卡为薄切片占位，数据待补充。\n")

    # ── 2. Championship Thesis ──
    lines.append("## 2. Championship Thesis\n")
    if has_kimi and kimi_prob != "N/A":
        lines.append(f"> 如果 {zh} 夺冠，最可能是因为 `<待分析>`，并且 `<关键阻力>` 被 `<待分析>` 破解。\n")
        lines.append(f"Kimi 聚合概率: {kimi_prob}%（{kimi_votes} 票）。\n")
    else:
        lines.append(f"> 如果 {zh} 夺冠，最可能是因为 `<待分析>`，并且 `<关键阻力>` 被 `<待分析>` 破解。\n")
        lines.append("待数据补充后填写。\n")

    # ── 3. Primary Obstacles ──
    lines.append("## 3. Primary Obstacles\n")
    lines.append("| 阻力 | 类型 | 为什么重要 | 可判定代理 |")
    lines.append("|---|---|---|---|")
    if has_kimi:
        lines.append("| `<待分析>` | `<type>` | | |")
    else:
        lines.append("| `<数据不足>` | | | |")
    lines.append("")

    # ── 4. Required Breakthroughs ──
    lines.append("## 4. Required Breakthroughs\n")
    lines.append("| 突破 | 发生阶段 | 最低条件 | 失败信号 |")
    lines.append("|---|---|---|---|")
    lines.append("| `<待分析>` | | | |")
    lines.append("")

    # ── 5. Black Swan Helpers ──
    lines.append("## 5. Black Swan Helpers\n")
    lines.append("| 黑天鹅 | 受益机制 | 是否可观测 | 备注 |")
    lines.append("|---|---|---|---|")
    lines.append("| `<待分析>` | | | |")
    lines.append("")

    # ── 6. Miracle Package ──
    lines.append("## 6. Miracle Package\n")
    lines.append("```yaml")
    lines.append("minimum_conditions_count: unassigned")
    lines.append("conditions:")
    lines.append("  - condition: <待分析>")
    lines.append("    type: <type>")
    lines.append("    observable_proxy: <待分析>")
    lines.append("    settlement_rule: <待分析>")
    lines.append("```\n")

    # ── 7. Path Simulation Notes ──
    lines.append("## 7. Path Simulation Notes\n")
    lines.append("```yaml")
    lines.append("simulation_status: not_run_yet")
    lines.append("championship_path_count: null")
    lines.append("dominant_path_pattern: null")
    lines.append("dominant_failure_node: null")
    lines.append("bracket_dependency: null")
    lines.append("black_swan_dependency: null")
    lines.append("penalty_dependency: null")
    lines.append("injury_sensitivity: null")
    lines.append("```\n")

    # ── 8. Factor Ledger Candidates ──
    lines.append("## 8. Factor Ledger Candidates\n")
    lines.append("| factor_id | factor_name | relation | observable_proxy | settlement_rule | source |")
    lines.append("|---|---|---|---|---|---|")
    lines.append("| | | | | | |\n")

    # ── 9. Marginalia Notes ──
    lines.append(build_section_9(kimi_agents, kimi_prob, TODAY))

    # ── 10. Update Log ──
    lines.append("## 10. Update Log\n")
    lines.append("| 日期 | 阶段 | 更新 | 影响 |")
    lines.append("|---|---|---|---|")
    lines.append(f"| {TODAY} | pre-tournament | 初始薄切片版本 | MVP-A1 |")
    lines.append("")

    # ── 11. Current Interpretation ──
    lines.append("## 11. Current Interpretation\n")
    if has_kimi:
        lines.append(f"**最可信路径**: 待分析。Kimi 聚合概率 {kimi_prob}%。")
        lines.append(f"**最不可信叙事**: 待分析。")
        lines.append(f"**最值得赛中监控的信号**: 待分析。")
        lines.append(f"**如果夺冠，哪些赛前判断有价值**: 待分析。")
    else:
        lines.append(f"**数据不足**: {zh} 未被 Kimi 300 Agent 预测覆盖。")
        lines.append(f"本卡为薄切片占位，等待补充数据后填写。")
    lines.append("")

    return "\n".join(lines), slug, signals, has_kimi, kimi_prob

# ── 主流程 ─────────────────────────────────────────────

def main():
    print("Loading data...")
    teams = load_team_registry()
    agents = load_kimi_inventory()
    agg = load_kimi_aggregation()

    print(f"Teams: {len(teams)}, Kimi agents: {len(agents)}")

    kimi_by_team = group_kimi_by_team(agents)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 生成 48 张卡
    cards_info = []
    for team in teams:
        card_content, slug, signals, has_kimi, kimi_prob = generate_card(team, kimi_by_team, agg)
        card_path = OUTPUT_DIR / f"{slug}.md"
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(card_content)
        cards_info.append({
            "slug": slug,
            "team": team["canonical_team"],
            "zh_name": team["zh_name"],
            "confederation": team["confederation"],
            "group": team.get("group", ""),
            "has_kimi": has_kimi,
            "kimi_prob": kimi_prob,
            "signals": ";".join(signals) if signals else "none",
        })
        status = "✅ Kimi" if has_kimi else "📋 thin/missing"
        print(f"  {team['zh_name']:8s} ({team['en_name']:20s}) → {slug}.md  {status}")

    # 生成 kimi_baseline_signals_matrix.csv
    print(f"\nGenerating kimi_baseline_signals_matrix.csv...")
    with open(SIGNALS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["team_slug", "canonical_team", "zh_name", "confederation", "group",
                         "has_kimi_data", "kimi_probability", "kimi_baseline_signals", "path_type", "tier"])
        for c in cards_info:
            writer.writerow([
                c["slug"], c["team"], c["zh_name"], c["confederation"], c["group"],
                c["has_kimi"], c["kimi_prob"], c["signals"], "unassigned", "unassigned"
            ])

    # 生成 README
    readme = f"""# 48 队薄切片夺冠路径卡

> **类型**: Plan A1 产出
> **日期**: {TODAY}
> **总数**: {len(cards_info)} 队

## 覆盖情况

- Kimi 覆盖: {sum(1 for c in cards_info if c['has_kimi'])} 队
- thin/missing: {sum(1 for c in cards_info if not c['has_kimi'])} 队
- path_type: 全部 unassigned（等待 A2 数据派生分类）

## 文件列表

| 球队 | 文件 | Kimi 数据 | 信号 |
|------|------|-----------|------|
"""
    for c in sorted(cards_info, key=lambda x: (not x['has_kimi'], x['zh_name'])):
        data_icon = "✅" if c['has_kimi'] else "📋"
        readme += f"| {c['zh_name']} | [{c['slug']}.md]({c['slug']}.md) | {data_icon} | {c['signals']} |\n"

    readme += f"""
## 用法

每张卡遵循 `docs/path-card-template.md` 的 11 节结构。

薄切片版本只填写：
- Team Profile（基本信息 + 数据覆盖状态）
- Marginalia Notes（Kimi reason 摘要，如有）
- Update Log

其余字段保持 `<待分析>` 占位，等待后续阶段填充。
"""
    with open(OUTPUT_DIR / "README.md", "w", encoding="utf-8") as f:
        f.write(readme)

    print(f"\n✅ Done: {len(cards_info)} cards generated in {OUTPUT_DIR}")
    print(f"✅ Signals matrix: {SIGNALS_CSV}")
    print(f"✅ README: {OUTPUT_DIR / 'README.md'}")

if __name__ == "__main__":
    main()
