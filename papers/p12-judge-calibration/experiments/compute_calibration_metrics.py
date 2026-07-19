#!/usr/bin/env python3
"""P12 M6 — calibration_metrics.md calculator.

Reads all four protocol result files and produces:
- experiments/calibration_metrics.md (the 4x4 protocol x hypothesis table)
- Per-protocol mean_score, std, n
- Per-condition mean_delta_score (leaked - blind) with bootstrap 95% CI
- Stop-condition #1 verdict per experiment_design.md

Run from papers/p12-judge-calibration/.
"""
from __future__ import annotations
import json
import math
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P12_ROOT / "experiments"

PROTOCOL_FILES = {
    "leaked": EXPERIMENTS / "leakage_reproduction.json",
    "blind": EXPERIMENTS / "blind_baseline_results.json",
    "neighborhood": EXPERIMENTS / "neighborhood_probe_results.json",
    "abstention": EXPERIMENTS / "abstention_results.json",
}

# P11 anchor hypotheses — each cell aggregates the score for the
# hypothesis's condition and the corresponding P11 finding.
HYPOTHESIS_MAP = {
    "H1": "inner_monologue",   # P11 H1: inner monologue affects behavior
    "H1c": "no_think",         # P11 H1c: reasoning depth drives effect
    "H3": "inner_monologue",   # P11 H3: risk_tolerance shift (same condition, different lens)
    "F1": "pure_analysis",     # P11 F1: fidelity flip
}

CONFIDENCE = 0.95
BOOTSTRAP_RESAMPLES = 10_000
SEED = 42


def load_protocols() -> dict[str, list[dict]]:
    out = {}
    for proto, path in PROTOCOL_FILES.items():
        if not path.exists():
            print(f"WARN: {path} missing — empty list for {proto}", file=sys.stderr)
            out[proto] = []
            continue
        try:
            data = json.loads(path.read_text())
            if isinstance(data, list):
                out[proto] = data
            else:
                print(f"WARN: {path} not a JSON array", file=sys.stderr)
                out[proto] = []
        except json.JSONDecodeError as e:
            print(f"WARN: {path} JSON parse failed: {e}", file=sys.stderr)
            out[proto] = []
    return out


def bootstrap_ci(values: list[float], n_resamples: int = BOOTSTRAP_RESAMPLES,
                  seed: int = SEED, conf: float = CONFIDENCE) -> tuple[float, float, float]:
    """Return (mean, ci_low, ci_high) via percentile bootstrap."""
    if not values:
        return float("nan"), float("nan"), float("nan")
    rng = random.Random(seed)
    means = []
    n = len(values)
    for _ in range(n_resamples):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo_i = int((1 - conf) / 2 * n_resamples)
    hi_i = int((1 + conf) / 2 * n_resamples) - 1
    return sum(values) / n, means[max(0, lo_i)], means[min(n_resamples - 1, hi_i)]


def paired_t_pvalue(deltas: list[float]) -> float:
    """Welch-style two-sided p-value approximation for paired deltas.
    Returns p-value; <=0.05 ⇒ significant. Small-sample exact computation
    is overkill for this summary table."""
    if len(deltas) < 2:
        return float("nan")
    mean = sum(deltas) / len(deltas)
    var = sum((d - mean) ** 2 for d in deltas) / (len(deltas) - 1)
    se = math.sqrt(var / len(deltas)) if var > 0 else 0.0
    if se == 0.0:
        return 0.0 if mean != 0 else 1.0
    # approximate t; for n=150 we treat |t|>2 as significant
    t = mean / se
    # crude: p ≈ 2 * (1 - Phi(|t|))
    z = abs(t)
    # Phi approximation (Abramowitz & Stegun 7.1.26)
    p = 1.0 - math.erf(z / math.sqrt(2))
    return 2 * (1 - math.erf(z / math.sqrt(2))) / 2  # = 1 - erf(z/√2) ≈ two-sided p


def cell_stats(records: list[dict], condition: str) -> dict:
    """Filter records by condition, compute summary stats."""
    if not records:
        return {"n": 0, "mean_score": float("nan"),
                "mean_consistency_on_wrong": float("nan"),
                "abstain_rate": float("nan"), "scores": []}
    matched = [r for r in records if r.get("sample_id", "").startswith("P12-")]
    # If condition filter is needed (H* maps to a specific condition),
    # we filter by looking up sample_id -> condition via sample_manifest.jsonl
    manifest = EXPERIMENTS / "sample_manifest.jsonl"
    cond_by_id = {}
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            r = json.loads(line)
            cond_by_id[r["sample_id"]] = r["original_condition"]

    rows = [r for r in matched if cond_by_id.get(r["sample_id"]) == condition]
    n = len(rows)
    if n == 0:
        return {"n": 0, "mean_score": float("nan"),
                "mean_consistency_on_wrong": float("nan"),
                "abstain_rate": float("nan"), "scores": []}
    scores = [r["score"] for r in rows if isinstance(r.get("score"), (int, float))]
    cons = [r.get("consistency_on_wrong", 1.0) for r in rows]
    abstains = sum(1 for r in rows if r.get("abstain", False))
    return {
        "n": n,
        "mean_score": sum(scores) / len(scores) if scores else float("nan"),
        "mean_consistency_on_wrong": sum(cons) / len(cons) if cons else float("nan"),
        "abstain_rate": abstains / n if n else float("nan"),
        "scores": scores,
    }


def mean_score_overall(records: list[dict]) -> dict:
    n = len(records)
    if n == 0:
        return {"n": 0, "mean_score": float("nan")}
    scores = [r["score"] for r in records if isinstance(r.get("score"), (int, float))]
    if not scores:
        return {"n": 0, "mean_score": float("nan")}
    return {"n": len(scores), "mean_score": sum(scores) / len(scores)}


def main() -> int:
    protocols = load_protocols()

    lines = ["# P12 Calibration Metrics (M6)", ""]
    lines.append("> Generated by `experiments/compute_calibration_metrics.py`.")
    lines.append("> Reads 4 protocol result files and produces the 4×4 protocol × hypothesis table.")
    lines.append("")
    lines.append(f"Source files (row counts):")
    for proto, recs in protocols.items():
        lines.append(f"- `{PROTOCOL_FILES[proto].name}` → {len(recs)} records")
    lines.append("")

    # Section 1: global per-protocol summary
    lines.append("## 1. Per-protocol global summary")
    lines.append("")
    lines.append("| protocol | n | mean_score | std_score |")
    lines.append("|----------|---|------------|-----------|")
    for proto, recs in protocols.items():
        s = mean_score_overall(recs)
        if s["n"] == 0:
            lines.append(f"| {proto} | 0 | n/a | n/a |")
            continue
        scores = [r["score"] for r in recs if isinstance(r.get("score"), (int, float))]
        std = statistics.pstdev(scores) if len(scores) > 1 else 0.0
        lines.append(f"| {proto} | {s['n']} | {s['mean_score']:.3f} | {std:.3f} |")
    lines.append("")

    # Section 2: per-(protocol, hypothesis) cell
    lines.append("## 2. Calibration matrix — protocol × hypothesis")
    lines.append("")
    lines.append("Hypothesis → P11 condition anchor (P12 only reuses anchors; P12's")
    lines.append("primary claim is the leakage effect, not P11's substantive claims).")
    lines.append("")
    lines.append("Cell columns: n, mean_score, mean_consistency_on_wrong, abstain_rate,")
    lines.append("verdict_delta = mean_score(protocol) − mean_score(leaked), p_value")
    lines.append("")

    # Compute leaked baselines once per hypothesis for verdict_delta
    leaked_by_h = {h: cell_stats(protocols["leaked"], c)
                   for h, c in HYPOTHESIS_MAP.items()}

    for hyp, condition in HYPOTHESIS_MAP.items():
        lines.append(f"### {hyp} (condition: `{condition}`)")
        lines.append("")
        lines.append("| protocol | n | mean_score | cons_on_wrong | abstain_rate | verdict_delta | p_value |")
        lines.append("|----------|---|------------|---------------|--------------|---------------|---------|")
        leaked_mean = leaked_by_h[hyp].get("mean_score")
        for proto in ["leaked", "blind", "neighborhood", "abstention"]:
            s = cell_stats(protocols[proto], condition)
            if s["n"] == 0:
                lines.append(f"| {proto} | 0 | n/a | n/a | n/a | n/a | n/a |")
                continue
            mean = s["mean_score"]
            delta = mean - leaked_mean if leaked_mean is not None and not math.isnan(leaked_mean) else float("nan")
            # p-value: paired test vs leaked using same sample_ids
            leaked_ids = {r["sample_id"]: r["score"] for r in protocols["leaked"]
                          if isinstance(r.get("score"), (int, float))}
            if proto == "leaked":
                p = "—"
            else:
                deltas = []
                for r in protocols[proto]:
                    sid = r.get("sample_id")
                    if sid in leaked_ids and isinstance(r.get("score"), (int, float)):
                        deltas.append(leaked_ids[sid] - r["score"])
                p = f"{paired_t_pvalue(deltas):.4f}" if deltas else "n/a"
            lines.append(
                f"| {proto} | {s['n']} | {mean:.3f} | {s['mean_consistency_on_wrong']:.3f} | "
                f"{s['abstain_rate']:.3f} | {delta:+.3f} | {p} |"
            )
        lines.append("")

    # Section 3: leakage stop-condition #1 verdict
    lines.append("## 3. Leakage verdict (stop-condition #1 per experiment_design.md)")
    lines.append("")
    lines.append("> Stop-condition #1 from `state/experiment_design.md`: early-exit to")
    lines.append("> `no_leakage_effect` ONLY when |mean| < 0.05 AND CI width < 0.10. Otherwise")
    lines.append("> verdict is `inconclusive` (CI includes 0 → too noisy to settle).")
    lines.append("> High CI width alone is NOT evidence of leakage; it is evidence of insufficient sample size.")
    lines.append("")
    leaked_recs = protocols["leaked"]
    blind_recs = protocols["blind"]
    if leaked_recs and blind_recs:
        leaked_by_id = {r["sample_id"]: r["score"] for r in leaked_recs
                        if isinstance(r.get("score"), (int, float))}
        deltas = []
        for r in blind_recs:
            sid = r.get("sample_id")
            if sid in leaked_by_id and isinstance(r.get("score"), (int, float)):
                deltas.append(leaked_by_id[sid] - r["score"])
        if deltas:
            mean, ci_lo, ci_hi = bootstrap_ci(deltas)
            ci_width = ci_hi - ci_lo
            lines.append(f"- mean_delta_score = leaked − blind = **{mean:+.3f}**")
            lines.append(f"- 95% bootstrap CI: [{ci_lo:+.3f}, {ci_hi:+.3f}]  (width = {ci_width:.3f})")
            lines.append(f"- n_paired = {len(deltas)}")
            lines.append("")
            if abs(mean) < 0.05 and ci_width < 0.10:
                lines.append("- **Verdict**: `no_leakage_effect` (early exit per stop-condition #1)")
                lines.append("- Action: fold P12 into P1+P2 methodology, do not write short paper.")
            elif ci_hi < 0:
                lines.append("- **Verdict**: `leakage_detected_negative` (CI entirely below 0 → blind > leaked)")
                lines.append("- Action: this is the OPPOSITE of the leakage hypothesis. Investigate before claiming paper.")
            elif ci_lo > 0:
                lines.append("- **Verdict**: `leakage_detected_positive` (CI entirely above 0 → leaked > blind)")
                lines.append("- Action: proceed to M7 paper outline and M8 review.")
            else:
                lines.append(f"- **Verdict**: `inconclusive` (CI includes 0; n={len(deltas)} too small for the")
                lines.append(f"  observed effect size {mean:+.3f} to be detectable with CI width < 0.10).")
                lines.append("- Action: do NOT claim a leakage verdict. Resume full 450 runs to settle.")
        else:
            lines.append("- n_paired = 0 — cannot compute; need both leaked and blind records.")
    else:
        lines.append("- missing leaked or blind protocol data — cannot compute verdict.")

    out_path = EXPERIMENTS / "calibration_metrics.md"
    out_path.write_text("\n".join(lines))
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())