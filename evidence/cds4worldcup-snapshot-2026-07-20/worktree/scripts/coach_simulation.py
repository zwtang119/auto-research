#!/usr/bin/env python3
"""
coach_simulation.py — 教练+球员对位模型 (WI-CM.5 + WI-CM.6)

Phase select-xi: 基于身价启发式选择每队×每种阵型的首发XI (WI-CM.5)
Phase simulate:  蒙特卡洛阵型采样 + 位置对位引擎 + Poisson模拟 (WI-CM.6)

用法:
  python3 scripts/coach_simulation.py --phase=select-xi [--method=heuristic|llm]
  python3 scripts/coach_simulation.py --phase=simulate

输出:
  data/processed/coach_formations.json   (Phase select-xi)
  data/processed/coach_simulation.json   (Phase simulate)

来源等级: Red（模型输出，非事实）
"""

import argparse
import json
import math
import os
import random
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Path setup ─────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.utils.poisson import compute_match_probs_from_lambdas  # noqa: E402
from src.utils.constants import BASE_GOALS, HOME_ADVANTAGE, MAX_GOALS, LAMBDA_MIN, LAMBDA_MAX  # noqa: E402


def _load_env():
    """Load .env file from project root into os.environ (zero deps)."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("\"'")
                if key and key not in os.environ:
                    os.environ[key] = value


_load_env()

FORMATION_POSITIONS = ROOT / "config" / "formation_positions.json"
FORMATION_DISTS = ROOT / "config" / "formation_distributions.json"
SQUADS = ROOT / "data" / "processed" / "transfermarkt_squads.json"
SCHEDULE = ROOT / "data" / "processed" / "schedule.json"
XI_OUTPUT = ROOT / "data" / "processed" / "coach_formations.json"
SIM_OUTPUT = ROOT / "data" / "processed" / "coach_simulation.json"

# ── Model constants (centralized in src/utils/constants.py) ─
MC_SAMPLES = 20

# ── Position mappings ──────────────────────────────────────
# Formation-specific codes → canonical codes for player matching
CODE_NORMALIZE = {
    "LCB": "CB", "RCB": "CB",
    "LWB": "LB", "RWB": "RB",
}

# Any code → position group (covers both formation and transfermarkt codes)
CODE_TO_GROUP = {
    "GK": "GK",
    "CB": "DEF", "LB": "DEF", "RB": "DEF",
    "LCB": "DEF", "RCB": "DEF", "LWB": "DEF", "RWB": "DEF",
    "DM": "MID", "CM": "MID", "AM": "MID", "LM": "MID", "RM": "MID",
    "CF": "ATT", "LW": "ATT", "RW": "ATT", "SS": "ATT",
}


# ── Helpers ────────────────────────────────────────────────
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ════════════════════════════════════════════════════════════
#  WI-CM.5 — XI Selection
# ════════════════════════════════════════════════════════════

def select_xi_heuristic(players, formation_slots):
    """Greedy market-value heuristic: for each slot, pick the best available
    player matching position_code → normalized code → position_group fallback."""

    # Sort once by value descending
    pool = sorted(players, key=lambda p: p.get("market_value_eur", 0), reverse=True)
    used = set()
    xi = []

    for slot in formation_slots:
        code = slot["position_code"]
        group = slot["position_group"]
        norm = CODE_NORMALIZE.get(code, code)
        chosen = None

        # 1) Exact position_code
        for p in pool:
            if p["name"] not in used and p.get("position_code") == code:
                chosen = p
                break

        # 2) Normalized code (LCB→CB etc.)
        if chosen is None and norm != code:
            for p in pool:
                if p["name"] not in used and p.get("position_code") == norm:
                    chosen = p
                    break

        # 3) Position-group fallback (any DEF/MID/ATT/GK player)
        if chosen is None:
            for p in pool:
                if p["name"] not in used:
                    if CODE_TO_GROUP.get(p.get("position_code", "")) == group:
                        chosen = p
                        break

        # 4) Extreme fallback — any remaining player
        if chosen is None:
            for p in pool:
                if p["name"] not in used:
                    chosen = p
                    break

        if chosen is None:
            xi.append({"name": "(missing)", "position_code": code,
                        "market_value_eur": 0})
            continue

        used.add(chosen["name"])
        xi.append({
            "name": chosen["name"],
            "position_code": code,
            "market_value_eur": chosen.get("market_value_eur", 0),
            "age": chosen.get("age"),
            "club": chosen.get("club", ""),
        })

    return xi


# ── LLM integration (minimal OpenAI-compatible client) ──────

_LLM_URL = "https://api.minimax.chat/v1/chat/completions"


def _llm_call(prompt, api_key, timeout=60):
    """Minimal OpenAI-compatible chat completion via urllib."""
    model_name = os.environ.get("MINIMAX_MODEL", "MiniMax-M3")
    payload = json.dumps({
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a JSON-only response system. Never output reasoning, thinking, or explanation. Output ONLY valid JSON. No other text."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
        "max_tokens": 4000,
    }).encode("utf-8")

    req = urllib.request.Request(
        _LLM_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            return body["choices"][0]["message"]["content"]
        except (urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
            if attempt == 2:
                raise
            print(f"    LLM retry {attempt + 1}/3: {exc}")

    return ""  # unreachable


def select_xi_llm(team_name, formation, players, formation_slots):
    """LLM-based XI selection with heuristic fallback."""
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        return select_xi_heuristic(players, formation_slots)

    # Build prompt
    slot_lines = [f"  Slot {s['slot']}: {s['position_code']} ({s['position_group']})"
                  for s in formation_slots]
    top_players = sorted(players, key=lambda p: p.get("market_value_eur", 0),
                         reverse=True)[:30]
    p_lines = [f"  {p['name']} | {p.get('position_code', '?')} | "
               f"€{p.get('market_value_eur', 0):,} | Age {p.get('age', '?')}"
               for p in top_players]

    prompt = (
        f"Select the best starting XI for {team_name} in a {formation} formation.\n\n"
        f"Positions:\n" + "\n".join(slot_lines) + "\n\n"
        f"Players (top 30 by value):\n" + "\n".join(p_lines) + "\n\n"
        f"Return a JSON array of 11 objects: "
        f'[{{"name": "...", "position_code": "..."}}]\n'
        f"position_code must match the slot code above."
    )

    try:
        raw = _llm_call(prompt, api_key)
        # Strip markdown fences if present
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        # Extract JSON array from response (model may output reasoning before JSON)
        # Use bracket balancing to find the actual top-level JSON array
        stripped = raw.strip()
        if stripped.startswith("["):
            raw = stripped
        else:
            depth = 0
            found = False
            for i, ch in enumerate(stripped):
                if ch == "[":
                    depth += 1
                    if not found:
                        json_start = i
                        found = True
                elif ch == "]":
                    depth -= 1
                    if found and depth == 0:
                        raw = stripped[json_start:i + 1]
                        break
            else:
                pass  # let json.loads handle the original error
        xi_list = json.loads(raw.strip())
        if not isinstance(xi_list, list) or len(xi_list) != 11:
            raise ValueError(f"Expected 11 players, got {len(xi_list)}")

        # Enrich with market value from player pool
        name_val = {p["name"]: p for p in players}
        result = []
        for entry in xi_list:
            name = entry.get("name", "")
            p = name_val.get(name, {})
            result.append({
                "name": name,
                "position_code": entry.get("position_code", ""),
                "market_value_eur": p.get("market_value_eur", 0),
                "age": p.get("age"),
                "club": p.get("club", ""),
            })
        return result

    except Exception as exc:
        print(f"  ⚠️  LLM fallback for {team_name} {formation}: {exc}")
        return select_xi_heuristic(players, formation_slots)


def run_select_xi(method="heuristic"):
    """Phase select-xi: build XI cache for all teams × used formations."""
    formations = load_json(FORMATION_POSITIONS)["formations"]
    dists = load_json(FORMATION_DISTS)
    squads_data = load_json(SQUADS)["teams"]

    use_llm = method == "llm" and bool(os.environ.get("MINIMAX_API_KEY"))
    select_fn = select_xi_llm if use_llm else select_xi_heuristic

    teams_out = {}
    n_teams = n_forms = n_players = 0

    for team_name, team_info in squads_data.items():
        players = team_info.get("players", [])
        if not players:
            continue

        team_dist = dists.get("teams", {}).get(team_name, dists.get("default", {}))
        team_out = {}

        for form_name, prob in team_dist.items():
            if prob <= 0 or form_name not in formations:
                continue

            slots = formations[form_name]["positions"]
            xi = select_fn(team_name, form_name, players, slots) if use_llm \
                else select_xi_heuristic(players, slots)

            team_out[form_name] = {"formation": form_name, "xi": xi}
            n_forms += 1
            n_players += len(xi)

        if team_out:
            teams_out[team_name] = team_out
            n_teams += 1

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "llm" if use_llm else "heuristic",
        "stats": {"teams": n_teams, "formations": n_forms, "total_selections": n_players},
        "teams": teams_out,
    }
    save_json(output, XI_OUTPUT)

    print(f"✅ select-xi: {n_teams} teams × {n_forms} formations = {n_players} selections")
    print(f"   → {XI_OUTPUT}")
    return output


# ════════════════════════════════════════════════════════════
#  WI-CM.6 — Matchup Engine + Monte Carlo Simulation
# ════════════════════════════════════════════════════════════

def group_value(xi_players, group):
    """Sum of log(market_value_eur + 1) for XI players in a position group."""
    total = 0.0
    for p in xi_players:
        if CODE_TO_GROUP.get(p.get("position_code", "")) == group:
            total += math.log(p.get("market_value_eur", 0) + 1)
    return total


def compute_lambdas(home_xi, away_xi):
    """Position-group matchup → λ for both teams.

    Step 1  group_value = Σ log(mv+1) per group
    Step 2  attack_ratio = att_A / (att_A + def_B)
    Step 3  λ = BASE × (ratio/0.5) × (0.7 + 0.3 × mid_ratio) × HOME_ADVANTAGE
    """
    att_h = group_value(home_xi, "ATT")
    def_h = group_value(home_xi, "DEF")
    mid_h = group_value(home_xi, "MID")

    att_a = group_value(away_xi, "ATT")
    def_a = group_value(away_xi, "DEF")
    mid_a = group_value(away_xi, "MID")

    d1 = att_h + def_a
    atk_r_h = att_h / d1 if d1 > 0 else 0.5

    d2 = att_a + def_h
    atk_r_a = att_a / d2 if d2 > 0 else 0.5

    d3 = mid_h + mid_a
    mid_r = mid_h / d3 if d3 > 0 else 0.5

    lam_h = BASE_GOALS * (atk_r_h / 0.5) * (0.7 + 0.3 * mid_r) * HOME_ADVANTAGE
    lam_a = BASE_GOALS * (atk_r_a / 0.5) * (0.7 + 0.3 * (1 - mid_r))

    return max(LAMBDA_MIN, min(LAMBDA_MAX, lam_h)), max(LAMBDA_MIN, min(LAMBDA_MAX, lam_a))


def confidence(hw, draw, aw, lam_h, lam_a):
    mx = max(hw, draw, aw)
    gd = abs(lam_h - lam_a)
    if mx > 0.50 and gd > 0.5:
        return "high"
    if mx > 0.40 and gd > 0.3:
        return "medium"
    return "low"


def get_dist(team, distributions):
    return distributions.get("teams", {}).get(team, distributions.get("default", {}))


def sample_formation(dist, rng):
    names = [f for f, p in dist.items() if p > 0]
    weights = [dist[f] for f in names]
    return rng.choices(names, weights=weights, k=1)[0]


def simulate_match(home, away, xi_cache, distributions, rng):
    """Monte Carlo: sample N formation pairs, compute matchup, average."""
    home_dist = get_dist(home, distributions)
    away_dist = get_dist(away, distributions)

    samples = []
    for _ in range(MC_SAMPLES):
        hf = sample_formation(home_dist, rng)
        af = sample_formation(away_dist, rng)

        h_entry = xi_cache.get(home, {}).get(hf)
        a_entry = xi_cache.get(away, {}).get(af)
        if not h_entry or not a_entry:
            continue

        h_xi, a_xi = h_entry["xi"], a_entry["xi"]
        if len(h_xi) < 11 or len(a_xi) < 11:
            continue

        lam_h, lam_a = compute_lambdas(h_xi, a_xi)
        hw, d, aw = compute_match_probs_from_lambdas(lam_h, lam_a, MAX_GOALS)

        samples.append({
            "home": hf, "away": af,
            "home_win": round(hw, 4), "draw": round(d, 4), "away_win": round(aw, 4),
            "lam_home": round(lam_h, 3), "lam_away": round(lam_a, 3),
        })

    if not samples:
        return None

    n = len(samples)
    avg_hw = sum(s["home_win"] for s in samples) / n
    avg_d = sum(s["draw"] for s in samples) / n
    avg_aw = sum(s["away_win"] for s in samples) / n

    # Normalize
    tot = avg_hw + avg_d + avg_aw
    if tot > 0:
        avg_hw /= tot
        avg_d /= tot
        avg_aw /= tot

    avg_lh = sum(s["lam_home"] for s in samples) / n
    avg_la = sum(s["lam_away"] for s in samples) / n

    return {
        "home_win": round(avg_hw, 4),
        "draw": round(avg_d, 4),
        "away_win": round(avg_aw, 4),
        "expected_goals_home": round(avg_lh, 3),
        "expected_goals_away": round(avg_la, 3),
        "confidence": confidence(avg_hw, avg_d, avg_aw, avg_lh, avg_la),
        "formation_samples": samples,
    }


def run_simulate():
    """Phase simulate: predict all group-stage matches via Monte Carlo."""
    xi_data = load_json(XI_OUTPUT)
    distributions = load_json(FORMATION_DISTS)
    schedule = load_json(SCHEDULE)

    xi_cache = xi_data.get("teams", {})
    rng = random.Random(42)
    predictions = []

    # Group stage
    for group, gdata in schedule["group_stage"]["groups"].items():
        for match in gdata["matches"]:
            home, away = match.get("home_team"), match.get("away_team")
            if not home or not away:
                continue
            if home not in xi_cache or away not in xi_cache:
                continue

            result = simulate_match(home, away, xi_cache, distributions, rng)
            if not result:
                continue

            predictions.append({
                "match_id": match["match_id"],
                "model": "coach_matchup",
                "home_team": home,
                "away_team": away,
                "home_win": result["home_win"],
                "draw": result["draw"],
                "away_win": result["away_win"],
                "expected_goals_home": result["expected_goals_home"],
                "expected_goals_away": result["expected_goals_away"],
                "confidence": result["confidence"],
                "formation_samples": result["formation_samples"],
                "source_level": "red",
                "source_note": "模型模拟输出，非事实。基于身价代理 + 泊松分布。",
            })

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": "coach_matchup",
        "model_description": (
            "教练对位模型。使用 Transfermarkt 身价做位置对位评估，"
            "蒙特卡洛阵型采样 + 泊松分布计算胜/平/负概率。来源等级: Red（模型输出）。"
        ),
        "total_matches_predicted": len(predictions),
        "mc_samples": MC_SAMPLES,
        "predictions": predictions,
    }
    save_json(output, SIM_OUTPUT)

    print(f"✅ simulate: {len(predictions)} matches predicted")
    print(f"   → {SIM_OUTPUT}")
    _validate(output)
    return output


def _validate(output):
    """Check output meets WI-CM.6 criteria."""
    issues = []
    for p in output["predictions"]:
        s = p["home_win"] + p["draw"] + p["away_win"]
        if abs(s - 1.0) > 0.01:
            issues.append(f"  {p['match_id']}: sum={s:.4f}")
        if p.get("source_level") != "red":
            issues.append(f"  {p['match_id']}: source_level={p.get('source_level')}")

    n = output["total_matches_predicted"]
    if n < 60:
        issues.append(f"  Only {n}/72 group matches (need ≥60)")

    if issues:
        print("⚠️  Validation issues:")
        for i in issues:
            print(i)
    else:
        print("✅ Validation passed: probabilities sum ≈ 1.0, all red source, ≥60 matches")


# ════════════════════════════════════════════════════════════
#  Main
# ════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Coach + Matchup Model (WI-CM.5 + WI-CM.6)")
    parser.add_argument("--phase", required=True,
                        choices=["select-xi", "simulate"],
                        help="Phase to run")
    parser.add_argument("--method", default="heuristic",
                        choices=["heuristic", "llm"],
                        help="XI selection method (default: heuristic)")
    args = parser.parse_args()

    if args.phase == "select-xi":
        run_select_xi(method=args.method)
    else:
        run_simulate()


if __name__ == "__main__":
    main()
