#!/usr/bin/env python3
"""
numeric_odds.py — Elo + Poisson 数值预测基线 (M4)

纯 stdlib 实现。读取赛程和球队注册表，基于 Elo 预期得分 + 泊松分布
计算每场比赛的胜/平/负概率。

来源等级: Red（模型输出，非事实）

用法: python3 scripts/numeric_odds.py
输出: data/processed/odds.json
"""

import csv
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.poisson import poisson_prob, compute_match_probs_from_lambdas
from src.utils.constants import BASE_GOALS, HOME_ADVANTAGE, MAX_GOALS, LAMBDA_MIN, LAMBDA_MAX

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE_PATH = ROOT / "data" / "processed" / "schedule.json"
REGISTRY_PATH = ROOT / "data" / "processed" / "team_registry.csv"
SIGNALS_PATH = ROOT / "data" / "processed" / "kimi_baseline_signals_matrix.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "odds.json"

# ── Elo 配置 ──────────────────────────────────────────────
# 基于联合会的初始 Elo（rough proxy，非实际 FIFA 排名）
ELO_BASE_BY_CONFED = {
    "UEFA": 1700,
    "CONMEBOL": 1690,
    "CAF": 1570,
    "AFC": 1550,
    "CONCACAF": 1550,
    "OFC": 1460,
}

# Kimi 覆盖的强队额外加分（kimi-aggregation + champion/top3 的队伍普遍更强）
# 分三档：高概率（>10%）、中概率（3-10%）、低概率（<3%）
KIMI_HIGH_BONUS = 100
KIMI_MID_BONUS = 60
KIMI_LOW_BONUS = 30

# 非 Kimi 覆盖的队伍基础分
KIMI_UNCOVERED_ADJUST = 0

# 东道主额外加分（主场优势体现在 Elo 中）
HOST_NATIONS = {"Mexico", "Canada", "United States"}
HOST_BONUS = 60

# 泊松模型参数已移至 src/utils/constants.py


def load_team_registry():
    """读取 team_registry.csv，返回 {canonical_team: row_dict}"""
    teams = {}
    with open(REGISTRY_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            teams[row["canonical_team"]] = row
    return teams


def load_kimi_probabilities():
    """读取 kimi_baseline_signals_matrix.csv，返回 {canonical_team: probability}"""
    probs = {}
    if not SIGNALS_PATH.exists():
        return probs
    with open(SIGNALS_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("has_kimi_data") == "True" and row.get("kimi_probability"):
                try:
                    probs[row["canonical_team"]] = float(row["kimi_probability"])
                except (ValueError, TypeError):
                    pass
    return probs


def assign_elo(team_name, team_info, kimi_probs=None):
    """基于联合会 + Kimi 概率分层 + 是否东道主，分配初始 Elo"""
    confed = team_info.get("confederation", "UEFA")
    elo = ELO_BASE_BY_CONFED.get(confed, 1550)

    # Tier-based differentiation using Kimi baseline probability
    if kimi_probs and team_name in kimi_probs:
        prob = kimi_probs[team_name]
        if prob >= 10.0:
            elo += KIMI_HIGH_BONUS
        elif prob >= 3.0:
            elo += KIMI_MID_BONUS
        else:
            elo += KIMI_LOW_BONUS
    elif team_info.get("source_status") == "kimi-aggregation":
        # kimi-aggregation team without probability data — mid tier
        elo += KIMI_MID_BONUS

    # 东道主
    if team_name in HOST_NATIONS:
        elo += HOST_BONUS

    return elo


def elo_expected_score(rating_a, rating_b):
    """计算 A 对 B 的预期得分（0~1）"""
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))





def compute_match_probs(home_elo, away_elo, is_home_host=False):
    """
    基于 Elo 差 + 泊松分布计算胜/平/负概率。

    Returns: (home_win, draw, away_win, exp_goals_home, exp_goals_away)
    """
    # 主队 Elo（加主场优势）
    home_elo_adj = home_elo + 65  # 固定主场 Elo 加成
    if is_home_host:
        home_elo_adj += 30  # 东道主额外加成

    # 预期得分
    e_home = elo_expected_score(home_elo_adj, away_elo)
    e_away = 1.0 - e_home

    # 转换为泊松 lambda（预期进球数）
    lam_home = BASE_GOALS * (e_home / 0.5) * HOME_ADVANTAGE
    lam_away = BASE_GOALS * (e_away / 0.5)

    # 限制 lambda 在合理范围
    lam_home = max(LAMBDA_MIN, min(LAMBDA_MAX, lam_home))
    lam_away = max(LAMBDA_MIN, min(LAMBDA_MAX, lam_away))

    # 泊松分布 → 胜/平/负
    p_home_win, p_draw, p_away_win = compute_match_probs_from_lambdas(
        lam_home, lam_away, MAX_GOALS
    )

    return (
        round(p_home_win, 4),
        round(p_draw, 4),
        round(p_away_win, 4),
        round(lam_home, 3),
        round(lam_away, 3),
    )


def determine_confidence(home_win, draw, away_win, elo_diff):
    """
    置信度分级：
    - high: Elo 差距大（>200）且概率差异明显
    - medium: Elo 差距适中（100~200）
    - low: Elo 差距小（<100）或概率接近
    """
    max_prob = max(home_win, draw, away_win)
    if abs(elo_diff) > 200 and max_prob > 0.50:
        return "high"
    elif abs(elo_diff) > 100 and max_prob > 0.40:
        return "medium"
    else:
        return "low"


def build_factors(home_team, away_team, home_info, away_info,
                  elo_diff, lam_home, lam_away):
    """生成因子列表，解释概率来源"""
    factors = []

    # Elo 差距
    if abs(elo_diff) > 150:
        stronger = home_team if elo_diff > 0 else away_team
        factors.append(f"{stronger} Elo 优势显著 (+{abs(elo_diff)})")
    elif abs(elo_diff) > 80:
        stronger = home_team if elo_diff > 0 else away_team
        factors.append(f"{stronger} 有一定 Elo 优势 (+{abs(elo_diff)})")

    # 联合会差异
    h_confed = home_info.get("confederation", "?")
    a_confed = away_info.get("confederation", "?")
    if h_confed != a_confed:
        factors.append(f"跨联合会: {h_confed} vs {a_confed}")

    # 东道主优势
    if home_team in HOST_NATIONS:
        factors.append(f"东道主主场 ({home_team})")

    # 进球预期
    if lam_home > 2.0:
        factors.append(f"主队预期进球较高 ({lam_home})")
    if lam_away > 2.0:
        factors.append(f"客队预期进球较高 ({lam_away})")

    if not factors:
        factors.append("两队实力接近，基线模型区分度低")

    return factors


def main():
    # 读取数据
    with open(SCHEDULE_PATH, encoding="utf-8") as f:
        schedule = json.load(f)

    teams_info = load_team_registry()
    kimi_probs = load_kimi_probabilities()

    # 为所有球队分配 Elo（使用 Kimi 概率分层）
    elo_ratings = {}
    for name, info in teams_info.items():
        elo_ratings[name] = assign_elo(name, info, kimi_probs)

    # 遍历比赛
    results = []
    processed = 0
    skipped = 0

    # 小组赛
    for group_letter, group_data in schedule["group_stage"]["groups"].items():
        for match in group_data["matches"]:
            home = match["home_team"]
            away = match["away_team"]

            if not home or not away:
                skipped += 1
                continue

            home_elo = elo_ratings.get(home, 1550)
            away_elo = elo_ratings.get(away, 1550)
            is_host = home in HOST_NATIONS

            hw, d, aw, lam_h, lam_a = compute_match_probs(
                home_elo, away_elo, is_host
            )

            elo_diff = home_elo - away_elo
            confidence = determine_confidence(hw, d, aw, elo_diff)
            factors = build_factors(
                home, away,
                teams_info.get(home, {}),
                teams_info.get(away, {}),
                elo_diff, lam_h, lam_a,
            )

            results.append({
                "match_id": match["match_id"],
                "model": "elo_poisson",
                "home_team": home,
                "away_team": away,
                "home_win": hw,
                "draw": d,
                "away_win": aw,
                "expected_goals_home": lam_h,
                "expected_goals_away": lam_a,
                "confidence": confidence,
                "factors": factors,
                "source_level": "red",
                "source_note": "模型模拟输出，非事实。基于 Elo 代理 + 泊松分布。",
            })
            processed += 1

    # 淘汰赛（仅当 home/away 已确定时才预测）
    for match in schedule.get("knockout_stage", []):
        home = match.get("home_team")
        away = match.get("away_team")

        if not home or not away:
            skipped += 1
            continue

        home_elo = elo_ratings.get(home, 1550)
        away_elo = elo_ratings.get(away, 1550)
        is_host = home in HOST_NATIONS

        hw, d, aw, lam_h, lam_a = compute_match_probs(
            home_elo, away_elo, is_host
        )

        elo_diff = home_elo - away_elo
        confidence = determine_confidence(hw, d, aw, elo_diff)
        factors = build_factors(
            home, away,
            teams_info.get(home, {}),
            teams_info.get(away, {}),
            elo_diff, lam_h, lam_a,
        )

        results.append({
            "match_id": match["match_id"],
            "model": "elo_poisson",
            "home_team": home,
            "away_team": away,
            "home_win": hw,
            "draw": d,
            "away_win": aw,
            "expected_goals_home": lam_h,
            "expected_goals_away": lam_a,
            "confidence": confidence,
            "factors": factors,
            "source_level": "red",
            "source_note": "模型模拟输出，非事实。基于 Elo 代理 + 泊松分布。",
        })
        processed += 1

    # 写入输出
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": "elo_poisson",
        "model_description": (
            "基线数值预测模型。使用联合会代理 Elo + 主场优势 + "
            "泊松分布计算胜/平/负概率。来源等级: Red（模型输出）。"
        ),
        "total_matches_predicted": processed,
        "total_matches_skipped": skipped,
        "elo_ratings": {k: v for k, v in sorted(elo_ratings.items(), key=lambda x: -x[1])},
        "predictions": results,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated {OUTPUT_PATH}")
    print(f"   Predicted: {processed} matches")
    print(f"   Skipped: {skipped} (no team assigned yet)")
    print(f"   Elo range: {min(elo_ratings.values())} – {max(elo_ratings.values())}")


if __name__ == "__main__":
    main()
