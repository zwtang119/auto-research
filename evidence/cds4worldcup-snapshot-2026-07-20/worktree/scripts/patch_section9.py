#!/usr/bin/env python3
"""
patch_section9.py — 增量修复 §9 Marginalia（不覆盖深描内容）

修复 generate_path_cards.py 的队名中英文不匹配 Bug 导致的
§9 Marginalia 数据丢失问题。只替换 §9，保留 §1-§8 和 §10-§11。

用法: python3 scripts/patch_section9.py
"""

import csv
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.slug import slugify
from src.utils.csv_helpers import load_csv
from src.utils.kimi import group_kimi_by_team, compute_signals, build_section_9

TEAM_REGISTRY = ROOT / "data" / "processed" / "team_registry.csv"
KIMI_INVENTORY = ROOT / "data" / "processed" / "kimi_agent_inventory.csv"
SIGNALS_CSV = ROOT / "data" / "processed" / "kimi_baseline_signals_matrix.csv"
CARDS_DIR = ROOT / "artifacts" / "team-cards"

TODAY = str(date.today())


def patch_card(card_path, new_section_9):
    """只替换 §9，保留其他所有 section"""
    text = card_path.read_text(encoding="utf-8")

    # 找到 §9 和 §10 的位置
    s9_match = re.search(r'^## 9\.\s*Marginalia Notes', text, re.MULTILINE)
    s10_match = re.search(r'^## 10\.\s*Update Log', text, re.MULTILINE)

    if not s9_match or not s10_match:
        print(f"  ⚠️ {card_path.name}: 无法定位 §9/§10 边界，跳过")
        return False

    s9_start = s9_match.start()
    s10_start = s10_match.start()

    patched = text[:s9_start] + new_section_9 + "\n" + text[s10_start:]
    card_path.write_text(patched, encoding="utf-8")
    return True




def main():
    print("Loading data...")
    teams = load_csv(TEAM_REGISTRY)
    agents = load_csv(KIMI_INVENTORY)
    kimi_by_team = group_kimi_by_team(agents)

    print(f"Teams: {len(teams)}, Kimi agents: {len(agents)}")
    print(f"Kimi groups (Chinese keys): {len(kimi_by_team)} teams")

    patched_count = 0
    signals_data = []

    for team in teams:
        slug = slugify(team["canonical_team"])
        zh = team["zh_name"]
        has_kimi = team["coverage_status"] == "champion/top3"

        # 获取该队的 Kimi agents（使用中文名查找 — 这是 Bug 修复的核心）
        kimi_agents = kimi_by_team.get(zh, [])
        kimi_prob = "N/A"

        if kimi_agents:
            # 从 agents 推算概率（简单近似：votes/300 * 100）
            kimi_prob = f"{len(kimi_agents) / 300 * 100:.2f}"

        card_path = CARDS_DIR / f"{slug}.md"
        if not card_path.exists():
            print(f"  ⚠️ {slug}.md 不存在，跳过")
            continue

        # 构建 §9 内容
        new_s9 = build_section_9(kimi_agents, kimi_prob, TODAY)

        # 增量补丁
        if patch_card(card_path, new_s9):
            patched_count += 1
            agent_count = len(kimi_agents)
            status = f"✅ {agent_count} agents" if agent_count > 0 else "📋 无 agents"
            print(f"  {zh:8s} → {slug}.md  {status}")

        # 计算信号
        signals = compute_signals(team, kimi_agents, kimi_prob)
        signals_data.append({
            "slug": slug,
            "team": team["canonical_team"],
            "zh_name": zh,
            "confederation": team["confederation"],
            "group": team.get("group", ""),
            "has_kimi": has_kimi,
            "kimi_prob": kimi_prob if kimi_prob != "N/A" else "N/A",
            "signals": ";".join(signals) if signals else "none",
        })

    # 更新 kimi_baseline_signals_matrix.csv
    # 保留原有概率数据（从聚合 JSON 获取的更准确），只更新信号列
    print(f"\nUpdating signals matrix...")
    existing_signals = {}
    try:
        with open(SIGNALS_CSV, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                existing_signals[row["canonical_team"]] = row
    except FileNotFoundError:
        pass

    with open(SIGNALS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["team_slug", "canonical_team", "zh_name", "confederation", "group",
                         "has_kimi_data", "kimi_probability", "kimi_baseline_signals", "path_type", "tier"])
        for sd in signals_data:
            # 保留原有的概率数据（从聚合 JSON 获取的更精确）
            existing = existing_signals.get(sd["team"], {})
            prob = existing.get("kimi_probability", sd["kimi_prob"])
            writer.writerow([
                sd["slug"], sd["team"], sd["zh_name"],
                sd["confederation"], sd["group"],
                sd["has_kimi"], prob, sd["signals"],
                "unassigned", "unassigned"
            ])

    print(f"\n✅ Patched {patched_count} cards")
    print(f"✅ Updated signals matrix: {SIGNALS_CSV}")

    # 统计新信号
    from collections import Counter
    all_signals = Counter()
    for sd in signals_data:
        for s in sd["signals"].split(";"):
            all_signals[s] += 1
    print(f"\nSignal distribution:")
    for sig, count in all_signals.most_common():
        print(f"  {sig}: {count}")


if __name__ == "__main__":
    main()
