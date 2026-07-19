#!/usr/bin/env python3
"""Unit tests for `adapter_signal_to_ledger.py`.

Covers:
  - signal_type → bucket mapping (confirmed_fact → supporting, others → contradicting)
  - independence_class resolution (primary/secondary/tertiary)
  - PIT-403: INACTIVE datasources rejected
  - PIT-403 / PIT-408: polymarket datasource rejected
  - PIT-302 / PIT-406: supporting without numeric_forecast flagged as rejected
  - group_by_claim builds supporting/contradicting arrays
  - CLI: end-to-end JSONL → JSONL pipeline

Run from papers/p07-signal-fusion/:
    python3 experiments/test_adapter_signal_to_ledger.py
"""
from __future__ import annotations
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

P7_ROOT = Path(__file__).resolve().parent.parent
ADAPTER = P7_ROOT / "experiments" / "adapter_signal_to_ledger.py"


def _good_signal(signal_type: str = "confirmed_fact", datasource_id: str = "energy",
                 status: str = "active", numeric_forecast: float | None = 0.5,
                 signal_id: str = "SIG-P12P-001") -> dict:
    return {
        "signal_id": signal_id,
        "exp_id": "P12P",
        "datasource_id": datasource_id,
        "datasource_status": status,
        "signal_type": signal_type,
        "lens_weight": 0.18,
        "recency_weight": 0.92,
        "observed_at": "2026-07-02T12:00:00Z",
        "scenario": "base",
        "scenario_text": "OPEC+ holds; refinery margins compress",
        "numeric_forecast": numeric_forecast,
        "ts_ingested": "2026-07-03T08:00:00Z",
    }


class TestAdaptSignalRow(unittest.TestCase):

    def test_confirmed_fact_goes_to_supporting(self):
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(signal_type="confirmed_fact"), scenario="gulei")
        self.assertEqual(m["bucket"], "supporting")
        self.assertEqual(m["independence_class"], "primary")
        self.assertFalse(m["rejected"])

    def test_weak_evidence_goes_to_contradicting(self):
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(signal_type="weak_evidence"), scenario="gulei")
        self.assertEqual(m["bucket"], "contradicting")
        self.assertEqual(m["independence_class"], "secondary")

    def test_missing_data_goes_to_contradicting(self):
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(signal_type="missing_data"), scenario="gulei")
        self.assertEqual(m["bucket"], "contradicting")
        self.assertEqual(m["independence_class"], "tertiary")

    def test_source_failure_goes_to_contradicting(self):
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(signal_type="source_failure"), scenario="gulei")
        self.assertEqual(m["bucket"], "contradicting")
        self.assertEqual(m["independence_class"], "tertiary")

    def test_pit403_inactive_datasource_rejected(self):
        from adapter_signal_to_ledger import adapt_signal_row
        with self.assertRaises(ValueError) as cm:
            adapt_signal_row(_good_signal(status="inactive"), scenario="gulei")
        self.assertIn("datasource_status", str(cm.exception))

    def test_pit403_polymarket_datasource_rejected(self):
        from adapter_signal_to_ledger import adapt_signal_row
        with self.assertRaises(ValueError) as cm:
            adapt_signal_row(_good_signal(datasource_id="polymarket"), scenario="gulei")
        self.assertIn("forbidden", str(cm.exception))

    def test_pit302_supporting_without_numeric_forecast_rejected(self):
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(numeric_forecast=None), scenario="gulei")
        self.assertTrue(m["rejected"])
        self.assertIn("PIT-302", m["reject_reason"])

    def test_pit_new_9_snippet_sha256_is_real_hash(self):
        """PIT-NEW-9: snippet_sha256_prefix must be a real SHA256, not fabricated padding.

        Regression test: prior code used `sig_id.replace('SIG-','')[:12].ljust(12,'_')`
        which produced strings ending with underscores (fabricated). The fix hashes
        the canonical signal content (signal_id + scenario + scenario_text + numeric_forecast)
        and truncates to 12 hex chars.
        """
        import re
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(), scenario="gulei")
        # Must be exactly 12 hex chars (not 12 of anything-else)
        self.assertEqual(len(m["snippet_sha256_prefix"]), 12)
        self.assertRegex(m["snippet_sha256_prefix"], r"^[0-9a-f]{12}$",
                          "snippet_sha256_prefix must be real SHA256 hex; got "
                          f"{m['snippet_sha256_prefix']!r}")
        # Must NOT be ljust-padded
        self.assertNotIn("_", m["snippet_sha256_prefix"],
                          "fabricated padding detected (PIT-NEW-9 not fixed)")

    def test_snippet_sha256_deterministic_and_content_sensitive(self):
        """PIT-NEW-9 defense: same input → same hash; different content → different hash."""
        from adapter_signal_to_ledger import adapt_signal_row
        # Use a signal with a different numeric_forecast so the diff below actually differs
        sig = _good_signal(numeric_forecast=0.85)
        h1 = adapt_signal_row(sig, scenario="gulei")["snippet_sha256_prefix"]
        h2 = adapt_signal_row(sig, scenario="gulei")["snippet_sha256_prefix"]
        self.assertEqual(h1, h2, "hash must be deterministic for audit chain")
        # Change numeric_forecast to a clearly different value
        sig_diff = dict(sig); sig_diff["numeric_forecast"] = 0.42
        self.assertNotEqual(sig["numeric_forecast"], sig_diff["numeric_forecast"],
                             "test bug: numeric_forecast not actually changed")
        h3 = adapt_signal_row(sig_diff, scenario="gulei")["snippet_sha256_prefix"]
        self.assertNotEqual(h1, h3, "hash must be content-sensitive to detect tampering")
        # Change scenario
        h4 = adapt_signal_row(sig, scenario="mimo_integration")["snippet_sha256_prefix"]
        self.assertNotEqual(h1, h4, "hash must be scenario-sensitive")

    def test_pit302_contradicting_without_numeric_forecast_allowed(self):
        """Contradicting signals don't need numeric_forecast (they are negative evidence)."""
        from adapter_signal_to_ledger import adapt_signal_row
        m = adapt_signal_row(_good_signal(signal_type="weak_evidence", numeric_forecast=None), scenario="gulei")
        self.assertFalse(m["rejected"])

    def test_invalid_signal_type_raises(self):
        from adapter_signal_to_ledger import adapt_signal_row
        with self.assertRaises(ValueError):
            adapt_signal_row(_good_signal(signal_type="conjecture"), scenario="gulei")


class TestGroupByClaim(unittest.TestCase):

    def test_group_separates_supporting_and_contradicting(self):
        from adapter_signal_to_ledger import adapt_signal_row, group_by_claim
        sigs = [
            _good_signal(signal_type="confirmed_fact", signal_id="SIG-P12P-001"),
            _good_signal(signal_type="weak_evidence", signal_id="SIG-P12P-002"),
            _good_signal(signal_type="missing_data", signal_id="SIG-P12P-003"),
        ]
        mappings = [adapt_signal_row(s, scenario="gulei") for s in sigs]
        out = group_by_claim(mappings, claim_id="C-P1P2-001")
        self.assertEqual(len(out["supporting_evidence"]), 1)
        self.assertEqual(len(out["contradicting_evidence"]), 2)
        self.assertEqual(out["supporting_evidence"][0]["source_id"], "SIG-P12P-001")
        self.assertEqual(out["claim_id"], "C-P1P2-001")

    def test_group_skips_rejected_rows(self):
        from adapter_signal_to_ledger import adapt_signal_row, group_by_claim
        good = _good_signal(signal_type="confirmed_fact", signal_id="SIG-P12P-001")
        bad = _good_signal(signal_type="confirmed_fact", signal_id="SIG-P12P-002", numeric_forecast=None)
        m_good = adapt_signal_row(good, scenario="gulei")
        m_bad = adapt_signal_row(bad, scenario="gulei")
        out = group_by_claim([m_good, m_bad], claim_id="C-P1P2-001")
        self.assertEqual(len(out["supporting_evidence"]), 1)
        self.assertEqual(len(out["rejected"]), 1)
        self.assertEqual(out["rejected"][0]["source_id"], "SIG-P12P-002")


class TestCLI(unittest.TestCase):

    def test_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "sigs.jsonl"
            out = Path(tmp) / "map.jsonl"
            grouped = Path(tmp) / "grouped.json"
            inp.write_text("\n".join([
                json.dumps(_good_signal(signal_type="confirmed_fact", signal_id="SIG-P12P-001")),
                json.dumps(_good_signal(signal_type="weak_evidence", signal_id="SIG-P12P-002")),
                json.dumps(_good_signal(signal_type="confirmed_fact", signal_id="SIG-P12P-003",
                                        numeric_forecast=None)),  # rejected
                json.dumps(_good_signal(datasource_id="polymarket")),  # rejected
                "",  # blank line
            ]) + "\n")
            result = subprocess.run(
                [sys.executable, str(ADAPTER), "--signals", str(inp),
                 "--output", str(out), "--grouped-output", str(grouped),
                 "--scenario", "gulei"],
                capture_output=True, text=True, timeout=15,
            )
            self.assertEqual(result.returncode, 0,
                             f"rc={result.returncode}\nstdout={result.stdout}\nstderr={result.stderr}")
            # 3 mappings written (1 supporting, 1 weak_evidence, 1 confirmed_fact-with-no-numeric
            # flagged rejected=True); 1 raise (polymarket ValueError skipped before write).
            # 'rejected=1' = count of m["rejected"]=True (the numeric_forecast=None one).
            self.assertIn("Adapted 3 signals", result.stdout)
            self.assertIn("rejected=1", result.stdout)
            mappings = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
            self.assertEqual(len(mappings), 3)
            non_rejected = [m for m in mappings if not m["rejected"]]
            self.assertEqual(len(non_rejected), 2)
            buckets = {m["bucket"] for m in non_rejected}
            self.assertIn("supporting", buckets)
            self.assertIn("contradicting", buckets)
            rejected_mappings = [m for m in mappings if m["rejected"]]
            self.assertEqual(len(rejected_mappings), 1)
            self.assertIn("PIT-302", rejected_mappings[0]["reject_reason"])
            grouped_data = json.loads(grouped.read_text())
            n_supp = sum(len(v["supporting_evidence"]) for v in grouped_data.values())
            n_cont = sum(len(v["contradicting_evidence"]) for v in grouped_data.values())
            self.assertEqual(n_supp, 1)
            self.assertEqual(n_cont, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)