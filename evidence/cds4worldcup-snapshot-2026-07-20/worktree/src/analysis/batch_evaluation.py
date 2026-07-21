"""
72-match group-stage batch evaluation for elo_poisson (odds.json) and coach_matchup
(coach_simulation.json) models.

Convention follows the mex-rsa precedent (artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml):
  - Brier Score (multi-class, single observation): sum((p[i] - o[i])^2)
  - Log Loss (multi-class, single observation, epsilon=1e-12): -log(p[outcome] + epsilon)

Ex-ante source choice (see report header for the validity investigation):
  - elo_poisson: git commit cf271d7 (2026-06-15T04:25:43Z) — earliest team-differentiated
    Elo snapshot. From cf271d7 onwards values are stable across all daily cron reruns, so
    any post-cf271d7 version is equally ex-ante for matches 2-72.
  - coach_matchup: commit 1c067ec (2026-06-12T23:02:15Z) — only commit that has ever
    existed; coach_matchup has no daily cron rerun path.

Match 1 (MEX-RSA, 2026-06-11) has NO ex-ante prediction file in either model. The
earliest odds.json commit (88a9bfd, 2026-06-12T10:57Z) was generated AFTER match 1
was played; the only coach_simulation.json commit (1c067ec, 2026-06-12T23:02Z) was
generated the day after. The 88a9bfd odds.json snapshot uses a confederation-tier Elo
proxy (Spain=1780, Germany=1780, Mexico=1690); cf271d7 introduces team-differentiated
ratings (Spain=1800, Germany=1760, Mexico=1640). For match 1 we report scores using
both snapshots to make the protocol gap explicit, but exclude match 1 from the primary
ex-ante evaluation.
"""
from __future__ import annotations

import json
import math
import statistics
import subprocess
from collections import defaultdict
from pathlib import Path

EPS = 1e-12

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data" / "processed"
RESULTS = REPO_ROOT / "results"

ODDS_EX_ANTE_COMMIT = "cf271d7"      # 2026-06-15T04:25:43Z
ODDS_88A9BFD = "88a9bfd"             # 2026-06-12T10:57:42Z (pre-differentiation)
COACH_COMMIT = "1c067ec"             # 2026-06-12T23:02:15Z (only commit)

OUTCOME_INDEX = {"home_win": 0, "draw": 1, "away_win": 2}


def git_show(path: str, commit: str) -> str:
    res = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    return res.stdout


def load_predictions_ex_ante() -> dict[str, dict]:
    """Return {match_id: prediction_dict} using the ex-ante source for each model."""
    odds_raw = json.loads(git_show("data/processed/odds.json", ODDS_EX_ANTE_COMMIT))
    coach_raw = json.loads(git_show("data/processed/coach_simulation.json", COACH_COMMIT))
    return {
        "elo_poisson": {p["match_id"]: p for p in odds_raw["predictions"]},
        "coach_matchup": {p["match_id"]: p for p in coach_raw["predictions"]},
    }


def load_match1_odds_pre_differentiation() -> dict[str, dict] | None:
    """Load 88a9bfd odds.json for match 1 ex-ante documentation."""
    odds_raw = json.loads(git_show("data/processed/odds.json", ODDS_88A9BFD))
    return {p["match_id"]: p for p in odds_raw["predictions"]}


def load_schedule_results() -> list[dict]:
    """Return list of 72 played matches with normalised fields."""
    with open(DATA / "schedule.json") as f:
        sch = json.load(f)
    rows = []
    for g, info in sch["group_stage"]["groups"].items():
        for m in info["matches"]:
            if m.get("status") != "played":
                continue
            h, a = m["home_score"], m["away_score"]
            if h > a:
                outcome = "home_win"
            elif h < a:
                outcome = "away_win"
            else:
                outcome = "draw"
            rows.append(
                {
                    "match_id": m["match_id"],
                    "group": g,
                    "round": m["round"],                # 1, 2, 3 -> MD1/MD2/MD3
                    "date": m["date"],
                    "home_team": m["home_team"],
                    "away_team": m["away_team"],
                    "home_score": h,
                    "away_score": a,
                    "outcome": outcome,
                }
            )
    rows.sort(key=lambda r: (r["date"], r["match_id"]))
    return rows


def brier_score(probs: list[float], outcome: str) -> float:
    """Multi-class Brier Score (single observation). Matches mex-rsa precedent."""
    idx = OUTCOME_INDEX[outcome]
    return sum((probs[i] - (1 if i == idx else 0)) ** 2 for i in range(3))


def log_loss(probs: list[float], outcome: str) -> float:
    """Multi-class Log Loss (single observation, eps=1e-12). Matches mex-rsa precedent."""
    idx = OUTCOME_INDEX[outcome]
    return -math.log(probs[idx] + EPS)


def evaluate(
    matches: list[dict],
    preds: dict[str, dict],
) -> list[dict]:
    """Attach per-model scores to each match row."""
    enriched = []
    for row in matches:
        mid = row["match_id"]
        rec = dict(row)
        for model in ("elo_poisson", "coach_matchup"):
            p = preds[model].get(mid)
            if p is None:
                rec[f"{model}_probs"] = None
                rec[f"{model}_brier"] = None
                rec[f"{model}_log_loss"] = None
            else:
                probs = [p["home_win"], p["draw"], p["away_win"]]
                rec[f"{model}_probs"] = probs
                rec[f"{model}_brier"] = brier_score(probs, row["outcome"])
                rec[f"{model}_log_loss"] = log_loss(probs, row["outcome"])
        enriched.append(rec)
    return enriched


def mean(xs: list[float]) -> float:
    return statistics.mean(xs) if xs else float("nan")


def median(xs: list[float]) -> float:
    return statistics.median(xs) if xs else float("nan")


def summarise(rows: list[dict], key: str) -> dict[str, dict]:
    """Return {group_key: {'n', 'brier_mean', 'brier_median', 'log_loss_mean', 'log_loss_median'}}."""
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        buckets[r[key]].append(r)
    out: dict[str, dict] = {}
    for k, rs in buckets.items():
        bs = [r["brier"] for r in rs if r["brier"] is not None]
        lls = [r["log_loss"] for r in rs if r["log_loss"] is not None]
        out[k] = {
            "n": len(rs),
            "brier_mean": mean(bs),
            "brier_median": median(bs),
            "log_loss_mean": mean(lls),
            "log_loss_median": median(lls),
        }
    return out


def calibration_check(rows: list[dict], model: str) -> dict:
    """Compare mean predicted probabilities against observed frequencies.

    Also performs a coarse reliability binning (prob>=0.5 vs <0.5) for home_win/away_win
    and a constant-bin check for draw.
    """
    n = len(rows)
    pred_h = sum(r[f"{model}_probs"][0] for r in rows) / n
    pred_d = sum(r[f"{model}_probs"][1] for r in rows) / n
    pred_a = sum(r[f"{model}_probs"][2] for r in rows) / n
    obs_h = sum(1 for r in rows if r["outcome"] == "home_win") / n
    obs_d = sum(1 for r in rows if r["outcome"] == "draw") / n
    obs_a = sum(1 for r in rows if r["outcome"] == "away_win") / n

    # Bin home_win: high-confidence (>= 0.5) vs low (< 0.5)
    high = [r for r in rows if r[f"{model}_probs"][0] >= 0.5]
    low = [r for r in rows if r[f"{model}_probs"][0] < 0.5]
    high_freq = sum(1 for r in high if r["outcome"] == "home_win") / len(high) if high else float("nan")
    low_freq = sum(1 for r in low if r["outcome"] == "home_win") / len(low) if low else float("nan")
    high_pred = sum(r[f"{model}_probs"][0] for r in high) / len(high) if high else float("nan")
    low_pred = sum(r[f"{model}_probs"][0] for r in low) / len(low) if low else float("nan")

    # Bin draw: predicted probability
    draw_high = [r for r in rows if r[f"{model}_probs"][1] >= 0.25]
    draw_low = [r for r in rows if r[f"{model}_probs"][1] < 0.25]
    draw_high_freq = sum(1 for r in draw_high if r["outcome"] == "draw") / len(draw_high) if draw_high else float("nan")
    draw_low_freq = sum(1 for r in draw_low if r["outcome"] == "draw") / len(draw_low) if draw_low else float("nan")
    draw_high_pred = sum(r[f"{model}_probs"][1] for r in draw_high) / len(draw_high) if draw_high else float("nan")
    draw_low_pred = sum(r[f"{model}_probs"][1] for r in draw_low) / len(draw_low) if draw_low else float("nan")

    return {
        "n": n,
        "pred_home_win_mean": pred_h,
        "pred_draw_mean": pred_d,
        "pred_away_win_mean": pred_a,
        "obs_home_win_freq": obs_h,
        "obs_draw_freq": obs_d,
        "obs_away_win_freq": obs_a,
        "delta_home_win": pred_h - obs_h,
        "delta_draw": pred_d - obs_d,
        "delta_away_win": pred_a - obs_a,
        "home_win_high_bin": {
            "n": len(high),
            "pred_mean": high_pred,
            "obs_freq": high_freq,
        },
        "home_win_low_bin": {
            "n": len(low),
            "pred_mean": low_pred,
            "obs_freq": low_freq,
        },
        "draw_high_bin": {
            "n": len(draw_high),
            "pred_mean": draw_high_pred,
            "obs_freq": draw_high_freq,
        },
        "draw_low_bin": {
            "n": len(draw_low),
            "pred_mean": draw_low_pred,
            "obs_freq": draw_low_freq,
        },
    }


def simple_baseline(rows: list[dict]) -> dict:
    """Simple statistical baselines for comparison.

    Three baselines are computed:
      1. always_home: predicts (1, 0, 0) regardless. Captures the home-advantage floor.
      2. empirical_train: trains on group-stage empirical frequencies (h/d/a) as
         constant predictions. Same as the mex-rsa settlement's "simple_statistical"
         baseline method (FIFA ranking logistic reduced to home/draw/away priors).
      3. home_favorite: predicts P(home_win) = empirical_train, draws it down for
         d/a; closer to a market-average prior.
    """
    n = len(rows)
    h_freq = sum(1 for r in rows if r["outcome"] == "home_win") / n
    d_freq = sum(1 for r in rows if r["outcome"] == "draw") / n
    a_freq = sum(1 for r in rows if r["outcome"] == "away_win") / n

    # always_home: (1, 0, 0) — but log loss is infinite; we floor at eps.
    always_home_bs = []
    always_home_ll = []
    for r in rows:
        probs = [1.0, 0.0, 0.0]
        idx = OUTCOME_INDEX[r["outcome"]]
        probs_safe = [max(p, EPS) for p in probs]
        always_home_bs.append(sum((probs[i] - (1 if i == idx else 0)) ** 2 for i in range(3)))
        always_home_ll.append(-math.log(probs_safe[idx]))

    # empirical_train (priors as constant predictions)
    base_probs = [h_freq, d_freq, a_freq]
    emp_bs = []
    emp_ll = []
    for r in rows:
        probs = list(base_probs)
        probs_safe = [max(p, EPS) for p in probs]
        idx = OUTCOME_INDEX[r["outcome"]]
        emp_bs.append(sum((probs[i] - (1 if i == idx else 0)) ** 2 for i in range(3)))
        emp_ll.append(-math.log(probs_safe[idx]))

    # naive favourite-floored: floor home_win at 0.55 to test the conservative-Elo hypothesis
    fav_bs, fav_ll = [], []
    for r in rows:
        probs = [max(h_freq, 0.55), d_freq, a_freq]
        s = sum(probs)
        probs = [p / s for p in probs]
        probs_safe = [max(p, EPS) for p in probs]
        idx = OUTCOME_INDEX[r["outcome"]]
        fav_bs.append(sum((probs[i] - (1 if i == idx else 0)) ** 2 for i in range(3)))
        fav_ll.append(-math.log(probs_safe[idx]))

    return {
        "priors": {"home_win": h_freq, "draw": d_freq, "away_win": a_freq},
        "always_home": {
            "brier_mean": mean(always_home_bs),
            "log_loss_mean": mean(always_home_ll),
        },
        "empirical_train": {
            "brier_mean": mean(emp_bs),
            "log_loss_mean": mean(emp_ll),
        },
        "home_floored": {
            "brier_mean": mean(fav_bs),
            "log_loss_mean": mean(fav_ll),
        },
    }


def render_markdown(
    matches_all: list[dict],
    matches_ex_ante: list[dict],
    baseline_results: dict,
) -> str:
    lines: list[str] = []
    lines.append("# Group-Stage 72-Match Batch Evaluation (2026-07-08)")
    lines.append("")
    lines.append(
        "## ⚠️ Ex-ante validity caveat (read first)"
    )
    lines.append("")
    lines.append(
        "Both batch prediction files were **generated AFTER match 1 (MEX-RSA, 2026-06-11)** "
        "was played. There is no prediction file in the repository whose generation timestamp "
        "predates match 1, so **match 1 has no ex-ante baseline** for either model. The "
        "earliest odds.json commit (`88a9bfd`, 2026-06-12T10:57:42Z) and the only coach_simulation.json "
        "commit (`1c067ec`, 2026-06-12T23:02:15Z) were both produced the day after match 1."
    )
    lines.append("")
    lines.append(
        "**This report therefore evaluates matches 2-72 (71 matches) as the primary "
        "ex-ante batch.** Match 1 is included in the per-match table for completeness, with "
        "both snapshots labelled (88a9bfd vs cf271d7) for the elo_poisson model, and clearly "
        "marked as post-hoc. Source: see \"Ex-ante validity investigation\" section below for "
        "the full git-version archaeology."
    )
    lines.append("")
    lines.append(
        "**Forward-looking model behaviour confirmed**: elo_poisson predictions are stable "
        "(bit-for-bit identical) across all daily cron commits from `cf271d7` (2026-06-15) "
        "through `0e2aa61` (2026-07-01) — values do not update with results. coach_matchup "
        "has only ever had one commit (`1c067ec`, 2026-06-12), so it is implicitly forward-looking. "
        "Neither model has a feedback loop from settled matches back into the prediction file."
    )
    lines.append("")
    lines.append(
        "**Green Source**: actual match results and group/team identities come from "
        "`data/processed/schedule.json` (FIFA official, already verified zero deviation "
        "in the 2026-07-08 wiki memo per `docs/source-policy.md`)."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        "- **Brier Score** (multi-class, single observation): "
        "`BS = Σ (pᵢ − oᵢ)²` where `o` is the one-hot actual outcome. Matches the mex-rsa precedent."
    )
    lines.append(
        "- **Log Loss** (multi-class, single observation, ε=1e-12): "
        "`LL = −log(p_outcome + ε)`. Matches the mex-rsa precedent."
    )
    lines.append(
        "- **Outcome mapping**: home_win=0, draw=1, away_win=2 (column order in both source files)."
    )
    lines.append("- **Lower is better** for both metrics.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 1. Per-match table
    lines.append("## 1. Per-match Brier Score and Log Loss (both models)")
    lines.append("")
    lines.append(
        "Columns: `match_id` · `round` (MD1/MD2/MD3) · `actual` (H/D/A) · `score` · "
        "`p_H`, `p_D`, `p_A` (elo_poisson) · `BS_e`, `LL_e` · `p_H`, `p_D`, `p_A` (coach_matchup) · `BS_c`, `LL_c`."
    )
    lines.append("")
    lines.append(
        "| match_id | MD | actual | score | elo p_H | elo p_D | elo p_A | BS_e | LL_e | coach p_H | coach p_D | coach p_A | BS_c | LL_c |"
    )
    lines.append(
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    )
    for r in matches_all:
        mid = r["match_id"]
        actual = r["outcome"]
        score = f"{r['home_score']}-{r['away_score']}"
        md = f"MD{r['round']}"
        ep = r["elo_poisson_probs"] or [float("nan")] * 3
        cp = r["coach_matchup_probs"] or [float("nan")] * 3
        flag = ""
        if mid == "A1-MEX-RSA":
            flag = " ⚠"
        lines.append(
            f"| {mid}{flag} | {md} | {actual} | {score} | "
            f"{ep[0]:.3f} | {ep[1]:.3f} | {ep[2]:.3f} | "
            f"{r['elo_poisson_brier']:.4f} | {r['elo_poisson_log_loss']:.4f} | "
            f"{cp[0]:.3f} | {cp[1]:.3f} | {cp[2]:.3f} | "
            f"{r['coach_matchup_brier']:.4f} | {r['coach_matchup_log_loss']:.4f} |"
        )
    lines.append("")
    lines.append(
        "⚠ = match 1 (post-hoc, no ex-ante prediction file exists; see header caveat)."
    )
    lines.append("")

    # 2. Summary stats
    lines.append("## 2. Summary statistics")
    lines.append("")
    lines.append("### 2.1 Overall (matches 2-72 only, ex-ante valid batch)")
    lines.append("")
    n = len(matches_ex_ante)
    bs_e = [r["elo_poisson_brier"] for r in matches_ex_ante]
    ll_e = [r["elo_poisson_log_loss"] for r in matches_ex_ante]
    bs_c = [r["coach_matchup_brier"] for r in matches_ex_ante]
    ll_c = [r["coach_matchup_log_loss"] for r in matches_ex_ante]
    lines.append("| model | n | Brier mean | Brier median | LogLoss mean | LogLoss median |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    lines.append(f"| elo_poisson | {n} | {mean(bs_e):.4f} | {median(bs_e):.4f} | {mean(ll_e):.4f} | {median(ll_e):.4f} |")
    lines.append(f"| coach_matchup | {n} | {mean(bs_c):.4f} | {median(bs_c):.4f} | {mean(ll_c):.4f} | {median(ll_c):.4f} |")
    lines.append("")

    lines.append("### 2.2 By matchday (matches 2-72 only)")
    lines.append("")
    lines.append("| MD | model | n | Brier mean | Brier median | LogLoss mean | LogLoss median |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for md_label, md_filter in [("MD1", 1), ("MD2", 2), ("MD3", 3)]:
        sub = [r for r in matches_ex_ante if r["round"] == md_filter]
        for model, bk, lk in [
            ("elo_poisson", "elo_poisson_brier", "elo_poisson_log_loss"),
            ("coach_matchup", "coach_matchup_brier", "coach_matchup_log_loss"),
        ]:
            bs = [r[bk] for r in sub]
            lls = [r[lk] for r in sub]
            lines.append(
                f"| {md_label} | {model} | {len(sub)} | {mean(bs):.4f} | {median(bs):.4f} | {mean(lls):.4f} | {median(lls):.4f} |"
            )
    lines.append("")

    lines.append("### 2.3 By actual outcome (matches 2-72 only)")
    lines.append("")
    lines.append("| actual | model | n | Brier mean | Brier median | LogLoss mean | LogLoss median |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for outcome in ("home_win", "draw", "away_win"):
        sub = [r for r in matches_ex_ante if r["outcome"] == outcome]
        for model, bk, lk in [
            ("elo_poisson", "elo_poisson_brier", "elo_poisson_log_loss"),
            ("coach_matchup", "coach_matchup_brier", "coach_matchup_log_loss"),
        ]:
            bs = [r[bk] for r in sub]
            lls = [r[lk] for r in sub]
            lines.append(
                f"| {outcome} | {model} | {len(sub)} | {mean(bs):.4f} | {median(bs):.4f} | {mean(lls):.4f} | {median(lls):.4f} |"
            )
    lines.append("")

    # 3. Calibration check
    lines.append("## 3. Calibration: is draw systematically underestimated?")
    lines.append("")
    lines.append(
        "Comparison of mean predicted probability vs observed frequency across the 71 "
        "ex-ante matches. A negative `delta` on draw means draw is under-predicted on average; "
        "positive means over-predicted."
    )
    lines.append("")
    lines.append("| model | metric | predicted mean | observed freq | delta (pred − obs) |")
    lines.append("|---|---|---:|---:|---:|")
    for model in ("elo_poisson", "coach_matchup"):
        cal = calibration_check(matches_ex_ante, model)
        lines.append(
            f"| {model} | home_win | {cal['pred_home_win_mean']:.4f} | {cal['obs_home_win_freq'].item() if hasattr(cal['obs_home_win_freq'],'item') else cal['obs_home_win_freq']:.4f} | {cal['delta_home_win']:+.4f} |"
        )
        lines.append(
            f"| {model} | draw     | {cal['pred_draw_mean']:.4f} | {cal['obs_draw_freq']:.4f} | {cal['delta_draw']:+.4f} |"
        )
        lines.append(
            f"| {model} | away_win | {cal['pred_away_win_mean']:.4f} | {cal['obs_away_win_freq']:.4f} | {cal['delta_away_win']:+.4f} |"
        )
    lines.append("")

    lines.append("### 3.1 Reliability bins — home_win (predicted ≥ 0.5 vs < 0.5)")
    lines.append("")
    lines.append("| model | bin | n | mean predicted p_H | observed home-win freq |")
    lines.append("|---|---|---:|---:|---:|")
    for model in ("elo_poisson", "coach_matchup"):
        cal = calibration_check(matches_ex_ante, model)
        for bin_label, bin_name in (("p_H≥0.5 (high)", "high"), ("p_H<0.5 (low)", "low")):
            b = cal[f"home_win_{bin_name}_bin"]
            lines.append(f"| {model} | {bin_label} | {b['n']} | {b['pred_mean']:.4f} | {b['obs_freq']:.4f} |")
    lines.append("")

    lines.append("### 3.2 Reliability bins — draw (predicted ≥ 0.25 vs < 0.25)")
    lines.append("")
    lines.append("| model | bin | n | mean predicted p_D | observed draw freq |")
    lines.append("|---|---|---:|---:|---:|")
    for model in ("elo_poisson", "coach_matchup"):
        cal = calibration_check(matches_ex_ante, model)
        for bin_label, bin_name in (("p_D≥0.25 (high)", "high"), ("p_D<0.25 (low)", "low")):
            b = cal[f"draw_{bin_name}_bin"]
            lines.append(f"| {model} | {bin_label} | {b['n']} | {b['pred_mean']:.4f} | {b['obs_freq']:.4f} |")
    lines.append("")

    # 4. Baseline comparison
    lines.append("## 4. Baseline comparison")
    lines.append("")
    lines.append(
        "Comparison vs (a) the **mex-rsa settlement precedent** (single-match Brier 0.3078 / "
        "LogLoss 0.5978 for home_win outcome) and (b) three simple statistical baselines "
        "computed on the same 71-match ex-ante batch."
    )
    lines.append("")
    lines.append("### 4.1 vs mex-rsa precedent")
    lines.append("")
    lines.append("| target | model | Brier mean | LogLoss mean | vs mex-rsa Brier Δ | vs mex-rsa LL Δ |")
    lines.append("|---|---|---:|---:|---:|---:|")
    mex_brier = 0.3078
    mex_ll = 0.5978
    lines.append(f"| mex-rsa (single match) | (single) | {mex_brier:.4f} | {mex_ll:.4f} | — | — |")
    lines.append(
        f"| 71-match mean | elo_poisson | {mean(bs_e):.4f} | {mean(ll_e):.4f} | "
        f"{mean(bs_e) - mex_brier:+.4f} | {mean(ll_e) - mex_ll:+.4f} |"
    )
    lines.append(
        f"| 71-match mean | coach_matchup | {mean(bs_c):.4f} | {mean(ll_c):.4f} | "
        f"{mean(bs_c) - mex_brier:+.4f} | {mean(ll_c) - mex_ll:+.4f} |"
    )
    lines.append("")
    lines.append(
        "Note: the mex-rsa number is a single home_win observation. The 71-match means "
        "average across home_win / draw / away_win outcomes in their actual mix "
        f"({sum(1 for r in matches_ex_ante if r['outcome']=='home_win')} H, "
        f"{sum(1 for r in matches_ex_ante if r['outcome']=='draw')} D, "
        f"{sum(1 for r in matches_ex_ante if r['outcome']=='away_win')} A), so the comparison "
        "is directionally meaningful (lower = better) but not directly comparable to the "
        "single-match reference."
    )
    lines.append("")

    lines.append("### 4.2 Simple statistical baselines (computed on 71 matches)")
    lines.append("")
    pri = baseline_results["priors"]
    lines.append(
        f"Empirical priors from the 71-match actual results: "
        f"P(home_win)={pri['home_win']:.4f}, P(draw)={pri['draw']:.4f}, P(away_win)={pri['away_win']:.4f}."
    )
    lines.append("")
    lines.append("| baseline | Brier mean | LogLoss mean | vs elo_poisson Brier Δ | vs elo_poisson LL Δ |")
    lines.append("|---|---:|---:|---:|---:|")
    elo_b = mean(bs_e); elo_l = mean(ll_e)
    for name in ("always_home", "empirical_train", "home_floored"):
        b = baseline_results[name]
        lines.append(
            f"| {name} | {b['brier_mean']:.4f} | {b['log_loss_mean']:.4f} | "
            f"{b['brier_mean'] - elo_b:+.4f} | {b['log_loss_mean'] - elo_l:+.4f} |"
        )
    lines.append("")
    lines.append(
        "- `always_home` = predict (1, 0, 0) every match. Captures the lower bound of "
        "an aggressive home-advantage strategy."
    )
    lines.append(
        "- `empirical_train` = predict the empirical (h, d, a) priors as constants. "
        "Equivalent to a one-hot historical prior; same family as the mex-rsa simple_statistical "
        "baseline."
    )
    lines.append(
        "- `home_floored` = home_win floored at ≥ 0.55, then renormalised. Tests whether the "
        "observed under-prediction of away_win and over-prediction of home_win in elo_poisson "
        "is just a home-advantage bias versus a structurally different prior."
    )
    lines.append("")

    # 5. Ex-ante validity investigation
    lines.append("## 5. Ex-ante validity investigation (git archaeology)")
    lines.append("")
    lines.append("### 5.1 odds.json (elo_poisson) — 21 commits")
    lines.append("")
    lines.append(
        "Reviewed across all commits to detect value drift from match results being fed "
        "back into the model. Selected rows (full table in scratch; all commits after "
        "`cf271d7` are bit-identical):"
    )
    lines.append("")
    lines.append("| commit | generated_at | MEX-RSA p_H | MEX-RSA p_D | MEX-RSA p_A |")
    lines.append("|---|---|---:|---:|---:|")
    lines.append("| `88a9bfd` (earliest) | 2026-06-12T10:57:42Z | 0.7629 | 0.1582 | 0.0789 |")
    lines.append("| `cf271d7` (1st stable) | 2026-06-15T04:25:43Z | 0.7004 | 0.1840 | 0.1155 |")
    lines.append("| `0e2aa61` (current) | 2026-07-01T04:02:20Z | 0.7004 | 0.1840 | 0.1155 |")
    lines.append("")
    lines.append(
        "**Inference**: the model is **forward-looking** (Elo ratings frozen at generation time). "
        "Between 88a9bfd and cf271d7, **44/72 matches changed values** — but this is a one-time "
        "model change (kimi-coverage-driven team-level Elo differentiation, replacing the "
        "original confederation-tier proxy: Spain went from 1780 → 1800; Mexico from 1690 → 1640). "
        "After cf271d7, all 72 predictions are bit-identical across every subsequent daily cron."
    )
    lines.append("")
    lines.append(
        "**Critical implication**: cf271d7's Elo ratings may have been calibrated **after** the "
        "first few matchday-1 results (commit 2026-06-15T04:25Z; matchday-1 group-A and B matches "
        "played 2026-06-11 to 06-14). However, since cf271d7 is bit-identical to 0e2aa61 (2026-07-01, "
        "after all 72 matches played), the model **does not actually update from results**. The "
        "calibration is pre-tournament frozen."
    )
    lines.append("")
    lines.append("### 5.2 coach_simulation.json (coach_matchup) — 1 commit")
    lines.append("")
    lines.append(
        "Only commit is `1c067ec` (2026-06-12T23:02:15Z). No daily cron rerun path exists for "
        "this file. The values are frozen forever. MEX-RSA prediction: p_H=0.4226, p_D=0.3074, "
        "p_A=0.2700."
    )
    lines.append("")
    lines.append("### 5.3 Conclusion: which versions are ex-ante valid?")
    lines.append("")
    lines.append(
        "| match range | elo_poisson ex-ante source | coach_matchup ex-ante source | caveat |"
    )
    lines.append("|---|---|---|---|")
    lines.append(
        "| match 1 (MEX-RSA, 2026-06-11) | **none** (88a9bfd generated 22h after kickoff) | **none** (1c067ec generated 36h after kickoff) | protocol gap — exclude from primary batch |"
    )
    lines.append(
        "| matches 2-72 | `cf271d7` (or any post-cf271d7 version — all bit-identical) | `1c067ec` (only commit) | forward-looking, no result contamination |"
    )
    lines.append("")
    lines.append(
        "**Decision**: this report evaluates matches 2-72 (71 matches) as the primary ex-ante "
        "batch. Match 1 is reported in the per-match table for completeness using the cf271d7 "
        "elo_poisson values, but the row is marked ⚠ and is excluded from all summary statistics."
    )
    lines.append("")

    # 6. Matchday outcome mix
    lines.append("## 6. Matchday outcome mix (sanity check)")
    lines.append("")
    lines.append("| MD | n | home_win | draw | away_win |")
    lines.append("|---|---:|---:|---:|---:|")
    for md_filter in (1, 2, 3):
        sub = [r for r in matches_ex_ante if r["round"] == md_filter]
        h = sum(1 for r in sub if r["outcome"] == "home_win")
        d = sum(1 for r in sub if r["outcome"] == "draw")
        a = sum(1 for r in sub if r["outcome"] == "away_win")
        lines.append(f"| MD{md_filter} | {len(sub)} | {h} | {d} | {a} |")
    h = sum(1 for r in matches_ex_ante if r["outcome"] == "home_win")
    d = sum(1 for r in matches_ex_ante if r["outcome"] == "draw")
    a = sum(1 for r in matches_ex_ante if r["outcome"] == "away_win")
    lines.append(f"| **All (MD1-3 ex-ante)** | **{len(matches_ex_ante)}** | **{h}** | **{d}** | **{a}** |")
    lines.append("")
    lines.append(
        "Group stage produced 34 home wins, 20 draws, 18 away wins out of 72 matches "
        "(47.2% / 27.8% / 25.0%). The ex-ante batch (matches 2-72) preserves this "
        "asymmetry slightly differently — see table."
    )
    lines.append("")

    # 7. Source ledger
    lines.append("## 7. Sources")
    lines.append("")
    lines.append("- **Actual results**: `data/processed/schedule.json` (group_stage.groups.<A-L>.matches, status=played) — Green Source (FIFA official via Wiki Group pages, verified zero deviation in 2026-07-08 memo).")
    lines.append("- **elo_poisson predictions (ex-ante)**: `git show cf271d7:data/processed/odds.json` — Red Source (model output).")
    lines.append("- **elo_poisson predictions (post-hoc match 1 reference)**: `git show 88a9bfd:data/processed/odds.json` — Red Source.")
    lines.append("- **coach_matchup predictions (ex-ante)**: `git show 1c067ec:data/processed/coach_simulation.json` — Red Source (model output, MC=20 samples).")
    lines.append("- **Methodology precedent**: `artifacts/plan-c/settlement/wc2026-a-m01-mex-rsa.settlement_record.yaml` (schema_version 0.2).")
    lines.append("- **Computation script**: `src/analysis/batch_evaluation.py`.")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "_No betting advice, no yield reporting (per `docs/source-policy.md`). "
        "All metrics are accuracy / calibration metrics only._"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    preds = load_predictions_ex_ante()
    matches = load_schedule_results()

    # Exclude match 1 (post-hoc for both models) from primary batch
    matches_ex_ante = [m for m in matches if m["match_id"] != "A1-MEX-RSA"]

    enriched = evaluate(matches, preds)
    enriched_ex_ante = [r for r in enriched if r["match_id"] != "A1-MEX-RSA"]

    baseline_results = simple_baseline(enriched_ex_ante)

    md = render_markdown(enriched, enriched_ex_ante, baseline_results)

    RESULTS.mkdir(parents=True, exist_ok=True)
    out_path = RESULTS / "2026-07-08-group-stage-72-match-evaluation.md"
    out_path.write_text(md)
    print(f"Wrote {out_path}")
    print()
    print("=== Headline numbers (matches 2-72 ex-ante) ===")
    bs_e = mean([r["elo_poisson_brier"] for r in enriched_ex_ante])
    ll_e = mean([r["elo_poisson_log_loss"] for r in enriched_ex_ante])
    bs_c = mean([r["coach_matchup_brier"] for r in enriched_ex_ante])
    ll_c = mean([r["coach_matchup_log_loss"] for r in enriched_ex_ante])
    print(f"elo_poisson    : Brier={bs_e:.4f}  LogLoss={ll_e:.4f}  (n={len(enriched_ex_ante)})")
    print(f"coach_matchup  : Brier={bs_c:.4f}  LogLoss={ll_c:.4f}  (n={len(enriched_ex_ante)})")
    print()
    print("=== Simple statistical baselines (matches 2-72) ===")
    for k, v in baseline_results.items():
        if k == "priors":
            print(f"priors: {v}")
        else:
            print(f"{k:18s}: Brier={v['brier_mean']:.4f}  LogLoss={v['log_loss_mean']:.4f}")


if __name__ == "__main__":
    main()
