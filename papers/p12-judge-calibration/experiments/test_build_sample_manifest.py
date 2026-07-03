"""P12 M1 sample-manifest builder tests.

Run from the project root (.../papers/p12-judge-calibration/):

    python -m unittest experiments.test_build_sample_manifest -v

Uses unittest stdlib to avoid an extra dep at the project root.
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

P12_ROOT = Path(__file__).resolve().parent.parent
AUTO_ROOT = P12_ROOT.parent.parent    # papers/p12-judge-calibration/ → auto-research/
P11_ROOT = (AUTO_ROOT / "legacy"
                      / "p11-closed-v5-minimax-m3")
P11_A_YAML = P11_ROOT / "experiments" / "h5-emergence" / "A" / "yaml"

SCRIPT = P12_ROOT / "experiments" / "build_sample_manifest.py"
MANIFEST = P12_ROOT / "experiments" / "sample_manifest.jsonl"
FROZEN = P12_ROOT / "experiments" / "sample_ids_ordered.json"


def _run_script() -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=str(P12_ROOT), capture_output=True, text=True, timeout=60,
    )


class TestSampleManifest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run once; tests below all share the artefact.
        out = _run_script()
        if out.returncode != 0:
            raise RuntimeError(
                f"build_sample_manifest.py failed: rc={out.returncode}\n"
                f"stderr={out.stderr}"
            )

    # --- file presence -------------------------------------------------------

    def test_manifest_file_exists(self):
        self.assertTrue(MANIFEST.exists(), f"missing: {MANIFEST}")

    def test_frozen_ids_file_exists(self):
        self.assertTrue(FROZEN.exists(), f"missing: {FROZEN}")

    # --- row count ------------------------------------------------------------

    def test_manifest_has_450_rows(self):
        n = sum(1 for _ in open(MANIFEST))
        self.assertEqual(n, 450, f"expected 450 rows, got {n}")

    # --- PIT-105 / PIT-005 row invariants ------------------------------------

    def test_every_row_is_PIT_105_and_PIT_005_compliant(self):
        bad = []
        id_pat = re.compile(r"^P12-\d{3,}$")
        for line in open(MANIFEST):
            row = json.loads(line)
            if not id_pat.match(row.get("sample_id", "")):
                bad.append(("bad_sample_id", row.get("sample_id")))
                continue
            if not row.get("source_path"):
                bad.append(("missing_source_path", row.get("sample_id")))
            if not row.get("source_sha256_prefix"):
                bad.append(("missing_sha", row.get("sample_id")))
            if row.get("condition_visible_to_judge") is not False:
                bad.append(("not_blind", row.get("sample_id")))
            if row.get("original_condition") not in {
                "inner_monologue", "no_think", "pure_analysis"
            }:
                bad.append(("bad_condition", row.get("sample_id")))
            if row.get("original_enterprise") not in {
                "ISPACE", "LANDSPACE", "SPACETIMETECH"
            }:
                bad.append(("bad_enterprise", row.get("sample_id")))
        self.assertFalse(
            bad,
            f"PIT-blocked rows (first 3 of {len(bad)}): {bad[:3]}",
        )

    # --- PIT-106 frozen order match ------------------------------------------

    def test_sample_ids_ordered_matches_manifest_row_order(self):
        manifest_ids = [
            json.loads(line)["sample_id"] for line in open(MANIFEST)
        ]
        frozen_ids = json.loads(FROZEN.read_text())
        self.assertEqual(manifest_ids, frozen_ids)

    def test_sample_ids_have_no_gaps_P12_001_through_P12_450(self):
        frozen_ids = json.loads(FROZEN.read_text())
        expected = [f"P12-{i:03d}" for i in range(1, 451)]
        self.assertEqual(frozen_ids, expected)

    # --- sha prefix shape ----------------------------------------------------

    def test_sha_prefix_is_12_lowercase_hex(self):
        bad = []
        for line in open(MANIFEST):
            sha = json.loads(line)["source_sha256_prefix"]
            if not re.fullmatch(r"[0-9a-f]{12}", sha or ""):
                bad.append(sha)
        self.assertFalse(bad, f"bad sha prefixes (first 3): {bad[:3]}")

    # --- source paths exist ---------------------------------------------------

    def test_every_source_path_resolves_to_a_real_file(self):
        bad = []
        for line in open(MANIFEST):
            row = json.loads(line)
            full = AUTO_ROOT / row["source_path"]
            if not full.exists():
                bad.append(row["source_path"])
        self.assertFalse(
            bad,
            f"missing source files (first 3 of {len(bad)}): {bad[:3]}",
        )

    # --- ordering invariant: by (condition, enterprise, run_id asc) ----------

    def test_ordering_is_condition_enterprise_run_id(self):
        manifest = [json.loads(line) for line in open(MANIFEST)]
        seen = []
        for row in manifest:
            seen.append((
                row["original_condition"],
                row["original_enterprise"],
                int(row["original_run_id"]),
            ))
        expected = sorted(seen, key=lambda x: (
            {"inner_monologue": 0, "no_think": 1, "pure_analysis": 2}[x[0]],
            {"ISPACE": 0, "LANDSPACE": 1, "SPACETIMETECH": 2}[x[1]],
            x[2],
        ))
        self.assertEqual(seen, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
