#!/usr/bin/env python3
"""Unit tests for `experiments/ledger/validate_ledger.py`.

Each test writes a small synthetic JSONL containing one good entry and
one or more deliberately broken entries, then asserts that the validator:
  - accepts the good entry
  - rejects each broken entry with the expected PIT-id violation message
  - exits 0 when input is clean, exits 1 when input has violations

Run from papers/p1p2-evidence-ledger/:
    python3 -m unittest experiments/ledger/test_validate_ledger -v
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LEDGER_DIR = Path(__file__).resolve().parent
VALIDATOR = LEDGER_DIR / "validate_ledger.py"


def _write_jsonl(path: Path, entries: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False, separators=(",", ":")) + "\n")


def _good_entry() -> dict:
    return {
        "claim_id": "C-P1P2-100", "exp_id": "P1P2",
        "factor_id": "F-P1P2-100", "factor_type": "precedent",
        "decision_context": "test ctx",
        "supporting_evidence": [{"source_id": "S-x", "snippet_sha256_prefix": "abc",
                                  "observed_at": "2026-01-01T00:00:00Z", "independence_class": "primary"}],
        "contradicting_evidence": [{"source_id": "S-y", "snippet_sha256_prefix": "def",
                                     "observed_at": "2026-01-01T00:00:00Z", "independence_class": "primary"}],
        "missing_prerequisites": [],
        "source_independence": 2,
        "freshness": "2026-01-01T00:00:00Z", "freshness_window": "P1D", "freshness_ratio": 0.5,
        "authority": "high", "applicability": "test",
        "settlement_rule": "if x then y else z",
        "settleable": True,
        "observed_outcome": {"label": "confirmed", "ts": "2026-01-02T00:00:00Z", "value": 1},
        "confidence_before": 0.5, "confidence_after": 0.7,
        "audit_trace": [{"tool": "judge", "ts": "2026-01-02T00:00:00Z",
                          "input_sha256_prefix": "aa", "output_sha256_prefix": "bb", "agent": "w"}],
        "ts_created": "2026-01-02T00:00:00Z",
    }


def _run_validator(jsonl_path: Path) -> tuple[int, str]:
    """Run validator as subprocess; return (rc, stdout).

    Tests run inside a TemporaryDirectory so audit files do not pollute
    the real `experiments/ledger/` directory. We point --workdir at the
    temp dir to keep outputs contained.
    """
    workdir = jsonl_path.parent
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--input", str(jsonl_path), "--workdir", str(workdir)],
        capture_output=True, text=True, timeout=30,
    )
    return result.returncode, (result.stdout + result.stderr)


class TestValidator(unittest.TestCase):

    def test_clean_entry_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "clean.jsonl"
            _write_jsonl(p, [_good_entry()])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 0, f"validator should exit 0 on clean input; got rc={rc}\n{out}")
            self.assertIn("rejected: 0", out)

    def test_pit201_violation(self):
        """Both contradicting_evidence=[] and missing_prerequisites=[] → PIT-201."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-101"
        bad["contradicting_evidence"] = []
        bad["missing_prerequisites"] = []
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("PIT-201", out)

    def test_pit202_violation(self):
        """factor_type=authority but source_independence=1 → PIT-202."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-102"
        bad["factor_type"] = "authority"
        bad["source_independence"] = 1
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("PIT-202", out)

    def test_pit204_violation(self):
        """settleable=true but settlement_rule='' → PIT-204."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-103"
        bad["settlement_rule"] = ""
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("PIT-204", out)

    def test_pit205_violation(self):
        """confidence_before == confidence_after → PIT-205."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-104"
        bad["confidence_before"] = 0.5
        bad["confidence_after"] = 0.5
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("PIT-205", out)

    def test_pit206_violation(self):
        """audit_trace empty → PIT-206."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-105"
        bad["audit_trace"] = []
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("PIT-206", out)

    def test_pit203_stale_detection(self):
        """freshness_ratio > 1.0 → row counted as stale."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-106"
        bad["freshness_ratio"] = 5.0
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "stale.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 0)  # stale is not a hard reject
            self.assertIn("stale (PIT-203 freshness_ratio>1): 1", out)

    def test_real_pilot_10_passes(self):
        """The actual pilot_10.jsonl must pass validator with rc=0."""
        pilot = LEDGER_DIR / "pilot_10.jsonl"
        if not pilot.exists():
            self.skipTest(f"{pilot} not yet built — run build_pilot_10.py first")
        rc, out = _run_validator(pilot)
        self.assertEqual(rc, 0, f"pilot_10.jsonl should pass; got rc={rc}\n{out}")
        self.assertIn("Validated 10 entries", out)

    def test_invalid_factor_type(self):
        """factor_type not in enum → TYPE violation."""
        bad = _good_entry()
        bad["claim_id"] = "C-P1P2-107"
        bad["factor_type"] = "speculation"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("TYPE: factor_type", out)

    def test_bad_claim_id_pattern(self):
        """claim_id not matching ^C-P1P2-NNN$ → ID violation."""
        bad = _good_entry()
        bad["claim_id"] = "wrong-format"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "bad.jsonl"
            _write_jsonl(p, [_good_entry(), bad])
            rc, out = _run_validator(p)
            self.assertEqual(rc, 1)
            self.assertIn("ID: claim_id", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)