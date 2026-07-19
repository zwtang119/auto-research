#!/usr/bin/env python3
"""P8 M1.5 — Brier Score + Log Loss calculator for prediction-market calibration.

Implements the `settlement_record.scores.{brier, log_loss, baseline_difference}`
contract from `cds4polymarket/experiments/worldcup-2026-factor-calibration/schemas/settlement_record.schema.yaml`.

Formulas
--------
For a binary outcome o ∈ {0, 1} and predicted probability p ∈ [0, 1]:

    Brier(p, o) = (p - o)²
    LogLoss(p, o) = -[o * log(p) + (1 - o) * log(1 - p)]

For a multi-outcome prediction (n classes with probabilities p_1..p_n
and one-hot outcome o_1..o_n):

    Brier_multi(p, o) = Σ_i (p_i - o_i)²
    LogLoss_multi(p, o) = -Σ_i o_i * log(p_i)

The aggregate is the mean over N predictions.

Baseline-difference is computed against an arbitrary set of baselines
(e.g. Polymarket market consensus, naïve 0.5, or a previous version).

Usage
-----
CLI:
    python3 experiments/calc_brier.py \\
        --input experiments/settlement_predictions.jsonl \\
        --output experiments/settlement_records.jsonl \\
        --baseline "market_consensus"

Programmatic:
    from experiments.calc_brier import compute_brier, compute_log_loss, build_settlement_record
    b = compute_brier([0.7, 0.3, 0.6], [1, 0, 1])

Input format (JSONL, one row per prediction)
-------------------------------------------
{"record_id": "SR-P12E-001", "exp_id": "P12E", "event_id": "PMKT-2026-WTI-Q3",
 "factor_id": "F-P1P2-001", "claim_id": "C-P1P2-007",
 "predicted_p": 0.65, "observed_outcome": 1,
 "source": "numeric",  # numeric | anchor | text-extract
 "judge_id": "judge-m3-gold-L", "gold_set_version": "v3-frozen-2026-07-01",
 "ts_predicted": "2026-07-01T00:00:00Z",
 "baseline_predictions": {"market_consensus": 0.55, "naive_0.5": 0.5}}
"""
from __future__ import annotations
import argparse
import json
import math
import sys
from pathlib import Path
from typing import Iterable

P8_ROOT = Path(__file__).resolve().parent.parent
EXPERIMENTS = P8_ROOT / "experiments"


def compute_brier(predicted: list[float], observed: list[int]) -> tuple[float, list[float]]:
    """Return (aggregate_brier, per_row_brier_components).

    predicted[i] is the predicted probability (single class).
    observed[i] is the binary outcome ∈ {0, 1}.

    For multi-class, flatten using one-vs-rest before calling.
    """
    if len(predicted) != len(observed):
        raise ValueError(f"length mismatch: predicted={len(predicted)} observed={len(observed)}")
    if not predicted:
        return float("nan"), []
    components = []
    for p, o in zip(predicted, observed):
        if not (0.0 <= p <= 1.0):
            raise ValueError(f"predicted_p={p} outside [0,1]")
        if o not in (0, 1):
            raise ValueError(f"observed_outcome={o} not in {{0, 1}}")
        components.append((p - o) ** 2)
    return sum(components) / len(components), components


def compute_log_loss(predicted: list[float], observed: list[int],
                     eps: float = 1e-15) -> tuple[float, list[float]]:
    """Return (aggregate_log_loss, per_row_components).

    Clips predicted probabilities to [eps, 1-eps] to avoid log(0).
    """
    if len(predicted) != len(observed):
        raise ValueError(f"length mismatch: predicted={len(predicted)} observed={len(observed)}")
    if not predicted:
        return float("nan"), []
    components = []
    for p, o in zip(predicted, observed):
        if not (0.0 <= p <= 1.0):
            raise ValueError(f"predicted_p={p} outside [0,1]")
        if o not in (0, 1):
            raise ValueError(f"observed_outcome={o} not in {{0, 1}}")
        p_clip = min(max(p, eps), 1.0 - eps)
        components.append(-(o * math.log(p_clip) + (1 - o) * math.log(1 - p_clip)))
    return sum(components) / len(components), components


def compute_brier_multiclass(probs_list: list[list[float]], outcome_indices: list[int]) -> float:
    """Multi-class Brier: Σ_i (p_i - o_i)² averaged across rows.

    probs_list[r] is a list of class probabilities for row r (sums to 1.0).
    outcome_indices[r] is the index of the true class for row r.
    """
    if len(probs_list) != len(outcome_indices):
        raise ValueError("length mismatch")
    if not probs_list:
        return float("nan")
    total = 0.0
    for probs, true_idx in zip(probs_list, outcome_indices):
        n = len(probs)
        if abs(sum(probs) - 1.0) > 1e-6:
            raise ValueError(f"probabilities do not sum to 1.0: sum={sum(probs)}")
        for i, p in enumerate(probs):
            o = 1.0 if i == true_idx else 0.0
            total += (p - o) ** 2
    return total / len(probs_list)


def build_settlement_record(row: dict, baselines: dict[str, float] | None = None) -> dict:
    """Wrap one prediction row into a settlement_record matching the schema.

    Returns a dict with `scores.{brier, log_loss, baseline_difference}` and
    `factor_updates.{supported, rejected, inconclusive}` derived from
    per-row confidence vs observed outcome.
    """
    p = row["predicted_p"]
    o = row["observed_outcome"]
    brier_agg, _ = compute_brier([p], [o])
    ll_agg, _ = compute_log_loss([p], [o])
    base_diff = {}
    if baselines:
        for name, base_p in baselines.items():
            if not (0.0 <= base_p <= 1.0):
                continue
            base_brier, _ = compute_brier([base_p], [o])
            base_diff[name] = round(brier_agg - base_brier, 6)  # negative = our model better

    # Factor-update heuristic (paper says "auto-classify"; we use confidence
    # band — overridable by reviewer):
    #   p >= 0.7 and o == 1  → supported
    #   p >= 0.7 and o == 0  → rejected
    #   p <= 0.3 and o == 0  → supported
    #   else                 → inconclusive
    if p >= 0.7 and o == 1:
        supported, rejected, inconclusive = [row["factor_id"]], [], []
    elif p >= 0.7 and o == 0:
        supported, rejected, inconclusive = [], [row["factor_id"]], []
    elif p <= 0.3 and o == 0:
        supported, rejected, inconclusive = [row["factor_id"]], [], []
    else:
        supported, rejected, inconclusive = [], [], [row["factor_id"]]

    record = {
        "record_id": row["record_id"],
        "exp_id": row.get("exp_id", "P12E"),
        "event_id": row.get("event_id"),
        "factor_id": row.get("factor_id"),
        "claim_id": row.get("claim_id"),
        "predicted_p": p,
        "observed_outcome": o,
        "source": row.get("source", "numeric"),
        "judge_id": row.get("judge_id"),
        "gold_set_version": row.get("gold_set_version"),
        "brier_component": round(brier_agg, 6),
        "log_loss_component": round(ll_agg, 6),
        "ts_predicted": row.get("ts_predicted"),
        "ts_observed": row.get("ts_observed"),
        "baseline_sha256_prefix": row.get("baseline_sha256_prefix"),
        "scores": {
            "brier": round(brier_agg, 6),
            "log_loss": round(ll_agg, 6),
            "baseline_difference": base_diff,
        },
        "factor_updates": {
            "supported": supported,
            "rejected": rejected,
            "inconclusive": inconclusive,
        },
        "protocol_failures": row.get("protocol_failures", []),
    }
    return record


def aggregate_scores(records: list[dict]) -> dict:
    """Aggregate per-record scores into portfolio-level summary.

    Returns {n, mean_brier, mean_log_loss, n_supported, n_rejected, n_inconclusive,
            brier_per_source (mean_brier per source)}.
    """
    if not records:
        return {"n": 0}
    briers = [r["scores"]["brier"] for r in records if r["scores"]["brier"] is not None]
    lls = [r["scores"]["log_loss"] for r in records if r["scores"]["log_loss"] is not None]
    n_supported = sum(len(r["factor_updates"]["supported"]) for r in records)
    n_rejected = sum(len(r["factor_updates"]["rejected"]) for r in records)
    n_inconclusive = sum(len(r["factor_updates"]["inconclusive"]) for r in records)
    by_source: dict[str, list[float]] = {}
    for r in records:
        by_source.setdefault(r.get("source", "?"), []).append(r["scores"]["brier"])
    brier_per_source = {k: round(sum(v) / len(v), 6) for k, v in by_source.items() if v}
    return {
        "n": len(records),
        "mean_brier": round(sum(briers) / len(briers), 6) if briers else None,
        "mean_log_loss": round(sum(lls) / len(lls), 6) if lls else None,
        "n_supported": n_supported,
        "n_rejected": n_rejected,
        "n_inconclusive": n_inconclusive,
        "brier_per_source": brier_per_source,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True,
                    help="JSONL of prediction rows ({predicted_p, observed_outcome, factor_id, ...}).")
    ap.add_argument("--output", type=Path, required=True,
                    help="JSONL of settlement_record rows.")
    ap.add_argument("--aggregate-output", type=Path, default=None,
                    help="Optional path to write the portfolio-level aggregate JSON.")
    ap.add_argument("--default-baseline", type=float, default=0.5,
                    help="Baseline probability used when row has no baseline_predictions (default 0.5).")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"FATAL: {args.input} missing", file=sys.stderr)
        return 2

    records = []
    n_errors = 0
    for line_no, raw in enumerate(args.input.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            row = json.loads(raw)
            baselines = row.get("baseline_predictions") or {"naive_0.5": args.default_baseline}
            rec = build_settlement_record(row, baselines=baselines)
            records.append(rec)
        except Exception as e:
            print(f"WARN line {line_no}: {type(e).__name__}: {e}", file=sys.stderr)
            n_errors += 1

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(f"Wrote {len(records)} settlement_records → {args.output} (errors={n_errors})")

    agg = aggregate_scores(records)
    if args.aggregate_output:
        args.aggregate_output.write_text(json.dumps(agg, ensure_ascii=False, indent=2))
        print(f"Wrote aggregate → {args.aggregate_output}")
    else:
        print(f"Aggregate: {json.dumps(agg, ensure_ascii=False, indent=2)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())