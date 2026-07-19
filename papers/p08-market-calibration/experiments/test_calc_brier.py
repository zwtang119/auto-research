#!/usr/bin/env python3
"""Unit tests for `calc_brier.py`.

Covers:
  - compute_brier on binary outcomes (well-known values)
  - compute_log_loss with clipping
  - compute_brier_multiclass on one-hot outcomes
  - build_settlement_record with and without baselines
  - aggregate_scores portfolio summary
  - factor-update heuristic boundaries (p >= 0.7, p <= 0.3)
  - input length mismatch raises
  - invalid probability range raises

Run from papers/p08-market-calibration/:
    python3 experiments/test_calc_brier.py
"""
from __future__ import annotations
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P8_ROOT = Path(__file__).resolve().parent.parent
CALC = P8_ROOT / "experiments" / "calc_brier.py"


class TestPureFunctions(unittest.TestCase):

    def test_compute_brier_perfect(self):
        from calc_brier import compute_brier
        agg, comp = compute_brier([1.0, 0.0, 1.0, 0.0], [1, 0, 1, 0])
        self.assertEqual(agg, 0.0)
        self.assertEqual(comp, [0.0, 0.0, 0.0, 0.0])

    def test_compute_brier_known_value(self):
        """(0.7-1)² + (0.3-0)² + (0.6-1)² = 0.09 + 0.09 + 0.16 = 0.34; mean=0.1133..."""
        from calc_brier import compute_brier
        agg, comp = compute_brier([0.7, 0.3, 0.6], [1, 0, 1])
        self.assertAlmostEqual(agg, 0.34 / 3, places=6)
        self.assertAlmostEqual(comp[0], 0.09)
        self.assertAlmostEqual(comp[1], 0.09)
        self.assertAlmostEqual(comp[2], 0.16)

    def test_compute_brier_length_mismatch(self):
        from calc_brier import compute_brier
        with self.assertRaises(ValueError):
            compute_brier([0.5, 0.5], [1])

    def test_compute_brier_invalid_prob(self):
        from calc_brier import compute_brier
        with self.assertRaises(ValueError):
            compute_brier([1.5], [1])

    def test_compute_brier_invalid_outcome(self):
        from calc_brier import compute_brier
        with self.assertRaises(ValueError):
            compute_brier([0.5], [2])

    def test_compute_log_loss_perfect(self):
        from calc_brier import compute_log_loss
        agg, _ = compute_log_loss([1.0, 0.0], [1, 0])
        self.assertAlmostEqual(agg, 0.0, places=5)

    def test_compute_log_loss_clipping(self):
        """p=0 should be clipped to eps, not log(0) = -inf."""
        from calc_brier import compute_log_loss
        agg, comp = compute_log_loss([0.0], [0])
        self.assertTrue(math.isfinite(agg))
        self.assertTrue(math.isfinite(comp[0]))

    def test_compute_log_loss_half(self):
        """-log(0.5) ≈ 0.6931"""
        from calc_brier import compute_log_loss
        agg, _ = compute_log_loss([0.5], [1])
        self.assertAlmostEqual(agg, -math.log(0.5), places=4)

    def test_compute_brier_multiclass_one_hot(self):
        """3-class predictions where argmax == true_idx → near 0."""
        from calc_brier import compute_brier_multiclass
        agg = compute_brier_multiclass([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]], [0, 1])
        self.assertAlmostEqual(agg, 0.0, places=6)

    def test_compute_brier_multiclass_uniform(self):
        """Uniform 3-class probability [1/3, 1/3, 1/3] with true_idx=0:
        (1/3-1)² + (1/3)² + (1/3)² = 4/9 + 1/9 + 1/9 = 6/9 = 2/3
        Averaged over 1 row = 2/3.
        """
        from calc_brier import compute_brier_multiclass
        agg = compute_brier_multiclass([[1/3, 1/3, 1/3]], [0])
        self.assertAlmostEqual(agg, 2/3, places=6)

    def test_build_settlement_record_with_baseline(self):
        from calc_brier import build_settlement_record
        row = {"record_id": "SR-001", "exp_id": "P12E", "event_id": "EVT-1",
               "factor_id": "F-1", "predicted_p": 0.7, "observed_outcome": 1,
               "baseline_predictions": {"market_consensus": 0.5, "naive": 0.5}}
        rec = build_settlement_record(row, baselines=row["baseline_predictions"])
        self.assertEqual(rec["scores"]["brier"], 0.09)  # (0.7-1)²
        # baseline_diff: our_brier - baseline_brier; baseline is 0.5,1 → 0.25
        # 0.09 - 0.25 = -0.16 (we're better)
        self.assertAlmostEqual(rec["scores"]["baseline_difference"]["market_consensus"], 0.09 - 0.25, places=6)
        self.assertEqual(rec["factor_updates"]["supported"], ["F-1"])

    def test_build_settlement_record_p_high_outcome_zero_rejected(self):
        from calc_brier import build_settlement_record
        row = {"record_id": "SR-002", "factor_id": "F-2", "predicted_p": 0.9, "observed_outcome": 0}
        rec = build_settlement_record(row)
        self.assertEqual(rec["factor_updates"]["rejected"], ["F-2"])

    def test_build_settlement_record_p_low_outcome_zero_supported(self):
        from calc_brier import build_settlement_record
        row = {"record_id": "SR-003", "factor_id": "F-3", "predicted_p": 0.2, "observed_outcome": 0}
        rec = build_settlement_record(row)
        self.assertEqual(rec["factor_updates"]["supported"], ["F-3"])

    def test_build_settlement_record_p_mid_inconclusive(self):
        from calc_brier import build_settlement_record
        row = {"record_id": "SR-004", "factor_id": "F-4", "predicted_p": 0.5, "observed_outcome": 1}
        rec = build_settlement_record(row)
        self.assertEqual(rec["factor_updates"]["inconclusive"], ["F-4"])

    def test_aggregate_scores(self):
        from calc_brier import aggregate_scores, build_settlement_record
        rows = [
            {"record_id": "SR-A", "factor_id": "F-A", "predicted_p": 0.9, "observed_outcome": 1, "source": "numeric"},
            {"record_id": "SR-B", "factor_id": "F-B", "predicted_p": 0.9, "observed_outcome": 0, "source": "numeric"},
            {"record_id": "SR-C", "factor_id": "F-C", "predicted_p": 0.2, "observed_outcome": 0, "source": "anchor"},
        ]
        records = [build_settlement_record(r) for r in rows]
        agg = aggregate_scores(records)
        self.assertEqual(agg["n"], 3)
        self.assertEqual(agg["n_supported"], 2)  # A and C
        self.assertEqual(agg["n_rejected"], 1)  # B
        self.assertEqual(agg["n_inconclusive"], 0)
        self.assertEqual(set(agg["brier_per_source"].keys()), {"numeric", "anchor"})


class TestCLI(unittest.TestCase):

    def test_cli_end_to_end(self):
        """Write a small input JSONL, run the CLI as subprocess, verify output."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "preds.jsonl"
            out = Path(tmp) / "recs.jsonl"
            agg_out = Path(tmp) / "agg.json"
            inp.write_text("\n".join([
                json.dumps({"record_id": "SR-1", "exp_id": "P12E", "event_id": "EVT-1",
                            "factor_id": "F-1", "predicted_p": 0.7, "observed_outcome": 1,
                            "source": "numeric",
                            "baseline_predictions": {"naive_0.5": 0.5}}),
                json.dumps({"record_id": "SR-2", "exp_id": "P12E", "event_id": "EVT-2",
                            "factor_id": "F-2", "predicted_p": 0.3, "observed_outcome": 0,
                            "source": "numeric"}),
                "",  # blank line should be skipped
            ]) + "\n")
            result = subprocess.run(
                [sys.executable, str(CALC), "--input", str(inp),
                 "--output", str(out), "--aggregate-output", str(agg_out)],
                capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0,
                             f"CLI rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}")
            records = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["scores"]["brier"], 0.09)
            self.assertEqual(records[1]["factor_updates"]["supported"], ["F-2"])
            agg = json.loads(agg_out.read_text())
            self.assertEqual(agg["n"], 2)
            self.assertEqual(agg["n_supported"], 2)

    def test_cli_invalid_input_propagates(self):
        """A row with bad probability should not abort the whole run; CLI prints WARN."""
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "preds.jsonl"
            out = Path(tmp) / "recs.jsonl"
            inp.write_text(json.dumps({"record_id": "SR-1", "factor_id": "F-1",
                                       "predicted_p": 1.5, "observed_outcome": 1}) + "\n")
            result = subprocess.run(
                [sys.executable, str(CALC), "--input", str(inp), "--output", str(out)],
                capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("WARN", result.stderr + result.stdout)
            self.assertEqual(len([l for l in out.read_text().splitlines() if l.strip()]), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)