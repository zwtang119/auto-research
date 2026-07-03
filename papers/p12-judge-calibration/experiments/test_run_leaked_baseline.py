"""P12 M2 leaked-baseline script tests.

Confirms the smoke test (--dry-run --limit N) emits records that pass
`state/io_spec.md` §7 invariants on the `judge_protocol_result` schema.

Smoke test does NOT exercise the real `api_client.call_model` path.
For real-M2 validation: set DEEPSEEK_API_KEY + run without --dry-run.

Run from .../papers/p12-judge-calibration/:
    python -m unittest experiments.test_run_leaked_baseline -v
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = P12_ROOT / "experiments" / "run_leaked_baseline.py"
OUT_RESULT = P12_ROOT / "experiments" / "leakage_reproduction.json"


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
