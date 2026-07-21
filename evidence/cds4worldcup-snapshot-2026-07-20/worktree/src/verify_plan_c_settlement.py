"""
Multi-class Brier Score + Log Loss verification for Plan C settlement.

Usage:
    python3 src/verify_plan_c_settlement.py

Computes scores for the 3 Plan C prediction cards (qat-sui, bra-mar, ned-jpn)
and verifies against the values written to settlement_record.yaml.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class MatchScore:
    match_id: str
    p_home: float
    p_draw: float
    p_away: float
    actual_outcome: str  # "home_win" | "draw" | "away_win"
    # baseline probabilities
    b_home: float
    b_draw: float
    b_away: float


def brier(p_home: float, p_draw: float, p_away: float, actual: str) -> float:
    """Multi-class Brier Score (single observation)."""
    o = {"home_win": 0, "draw": 1, "away_win": 2}[actual]
    p = [p_home, p_draw, p_away]
    return sum((p[i] - (1 if i == o else 0)) ** 2 for i in range(3))


def log_loss(p_home: float, p_draw: float, p_away: float, actual: str, eps: float = 1e-12) -> float:
    """Multi-class Log Loss (single observation)."""
    o = {"home_win": 0, "draw": 1, "away_win": 2}[actual]
    p = [p_home, p_draw, p_away]
    return -math.log(p[o] + eps)


# Plan C prediction cards vs actual outcomes
MATCHES = [
    # Prediction: home=0.15 draw=0.24 away=0.61, baseline: 0.18/0.25/0.57
    MatchScore("wc2026-b-m02-qat-sui", 0.15, 0.24, 0.61, "draw",
               0.18, 0.25, 0.57),
    # Prediction: home=0.50 draw=0.26 away=0.24, baseline: 0.49/0.25/0.26
    MatchScore("wc2026-c-m01-bra-mar", 0.50, 0.26, 0.24, "draw",
               0.49, 0.25, 0.26),
    # Prediction: home=0.49 draw=0.26 away=0.25, baseline: 0.53/0.25/0.22
    MatchScore("wc2026-f-m01-ned-jpn", 0.49, 0.26, 0.25, "draw",
               0.53, 0.25, 0.22),
]


def main() -> None:
    print(f"{'match_id':<28} {'brier_p':>9} {'ll_p':>8} {'brier_b':>9} {'ll_b':>8} "
          f"{'Δbrier':>9} {'Δll':>8}")
    print("-" * 90)
    for m in MATCHES:
        bp = brier(m.p_home, m.p_draw, m.p_away, m.actual_outcome)
        lp = log_loss(m.p_home, m.p_draw, m.p_away, m.actual_outcome)
        bb = brier(m.b_home, m.b_draw, m.b_away, m.actual_outcome)
        lb = log_loss(m.b_home, m.b_draw, m.b_away, m.actual_outcome)
        print(f"{m.match_id:<28} {bp:>9.4f} {lp:>8.4f} {bb:>9.4f} {lb:>8.4f} "
              f"{bp - bb:>+9.4f} {lp - lb:>+8.4f}")

    # Sanity asserts (round to 4 dp as in the YAMLs)
    expected = {
        "wc2026-b-m02-qat-sui": (0.9722, 1.4271, 0.9198, 1.3863),
        "wc2026-c-m01-bra-mar": (0.8552, 1.3471, 0.8702, 1.3863),
        "wc2026-f-m01-ned-jpn": (0.8502, 1.3471, 0.8918, 1.3863),
    }
    for m in MATCHES:
        bp = round(brier(m.p_home, m.p_draw, m.p_away, m.actual_outcome), 4)
        lp = round(log_loss(m.p_home, m.p_draw, m.p_away, m.actual_outcome), 4)
        bb = round(brier(m.b_home, m.b_draw, m.b_away, m.actual_outcome), 4)
        lb = round(log_loss(m.b_home, m.b_draw, m.b_away, m.actual_outcome), 4)
        ebp, elp, ebb, elb = expected[m.match_id]
        assert bp == ebp, f"{m.match_id} brier_p {bp} != {ebp}"
        assert lp == elp, f"{m.match_id} ll_p {lp} != {elp}"
        assert bb == ebb, f"{m.match_id} brier_b {bb} != {ebb}"
        assert lb == elb, f"{m.match_id} ll_b {lb} != {elb}"
    print("\nAll assertions passed.")


if __name__ == "__main__":
    main()