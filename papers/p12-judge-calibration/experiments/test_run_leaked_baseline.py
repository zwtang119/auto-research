"""P12 M2 leaked-baseline script tests.

Confirms the smoke test (--dry-run --limit N) emits records that pass
`state/io_spec.md` §7 invariants on the `judge_protocol_result` schema.

Smoke test does NOT exercise the real `api_client.call_model` path.
For real-M2 validation: set DEEPSEEK_API_KEY + run without --dry-run.

Run from .../papers/p12-judge-calibration/:
    python -m unittest experiments.test_run_leaked_baseline -v
"""
from __future__ import annotations
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = P12_ROOT / "experiments" / "run_leaked_baseline.py"
OUT_RESULT = P12_ROOT / "experiments" / "leakage_reproduction.json"


def _import_runner():
    """Load run_leaked_baseline.py as a module without executing main().

    Lets us call internal helpers (aggregate_score, make_record) directly.
    """
    spec = importlib.util.spec_from_file_location("rlb", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run_dry(n: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run", "--limit", str(n)],
        cwd=str(P12_ROOT), capture_output=True, text=True, timeout=30,
    )


class TestRunLeakedBaseline(unittest.TestCase):

    def test_dry_run_emits_correct_row_count(self):
        r = _run_dry(7)
        self.assertEqual(r.returncode, 0, f"stderr: {r.stderr}")
        rows = json.loads(OUT_RESULT.read_text())
        self.assertEqual(len(rows), 7)

    def test_records_match_judge_protocol_result_schema(self):
        r = _run_dry(3)
        self.assertEqual(r.returncode, 0)
        rows = json.loads(OUT_RESULT.read_text())
        id_pat = re.compile(r"^R-P12-leaked-\d{3}$")
        for row in rows:
            self.assertRegex(row["record_id"], id_pat)
            self.assertEqual(row["protocol"], "leaked")
            self.assertEqual(row["awareness"], "leaked")
            self.assertNotEqual(row["judge_id"], "self")
            self.assertGreaterEqual(row["score"], 1.0)
            self.assertLessEqual(row["score"], 5.0)
            self.assertIn(row["score_band"], {"low", "mid", "high"})
            self.assertFalse(row["abstain"])
            self.assertIn("sample_id", row)

    def test_sample_ids_match_frozen_order(self):
        r = _run_dry(10)
        self.assertEqual(r.returncode, 0)
        rows = json.loads(OUT_RESULT.read_text())
        frozen = json.loads((P12_ROOT / "experiments" / "sample_ids_ordered.json").read_text())[:10]
        self.assertEqual([r["sample_id"] for r in rows], frozen)

    def test_aggregate_score_handles_empty_dict(self):
        mod = _import_runner()
        score, empty = mod.aggregate_score({})
        self.assertEqual(score, 0.0)
        self.assertTrue(empty)
        # When malformed scores are returned by the judge, the row should
        # be flagged as abstained in the output.
        score2, empty2 = mod.aggregate_score({"risk_tolerance_consistency": 4.0})
        self.assertEqual(score2, 4.0)
        self.assertFalse(empty2)

    def test_make_record_marks_abstained_when_empty(self):
        mod = _import_runner()
        sample = {"sample_id": "P12-001"}
        rec = mod.make_record(
            sample=sample, idx=1, score=0.0, parsed={"scores": {}},
            cond_label="no_think", judge_id="deepseek-v4-pro", dt_ms=100,
            abstained=True, abstain_reason="empty_scores_dict",
        )
        self.assertTrue(rec["abstain"])
        self.assertEqual(rec["abstain_reason"], "empty_scores_dict")
        self.assertEqual(rec["score"], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
