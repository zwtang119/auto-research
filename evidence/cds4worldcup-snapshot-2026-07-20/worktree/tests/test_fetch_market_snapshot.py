import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "fetch_market_snapshot.py"

spec = importlib.util.spec_from_file_location("fetch_market_snapshot", SCRIPT)
fetch_market_snapshot = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetch_market_snapshot)


class FetchMarketSnapshotTests(unittest.TestCase):
    def test_extract_team_from_question(self):
        self.assertEqual(
            fetch_market_snapshot.extract_team_name("Will Spain win the 2026 FIFA World Cup?"),
            "Spain",
        )
        self.assertEqual(
            fetch_market_snapshot.extract_team_name("Will USA win the 2026 FIFA World Cup?"),
            "USA",
        )

    def test_build_snapshot_from_public_search_payload(self):
        payload = {
            "events": [
                {
                    "title": "World Cup Winner",
                    "slug": "world-cup-winner",
                    "markets": [
                        {
                            "question": "Will Spain win the 2026 FIFA World Cup?",
                            "slug": "will-spain-win-the-2026-fifa-world-cup-963",
                            "outcomes": "[\"Yes\", \"No\"]",
                            "outcomePrices": "[\"0.1695\", \"0.8305\"]",
                        },
                        {
                            "question": "Will Any Other Team win the 2026 FIFA World Cup?",
                            "slug": "will-any-other-team-win-the-2026-fifa-world-cup",
                            "outcomes": "[\"Yes\", \"No\"]",
                            "outcomePrices": "[\"0.5\", \"0.5\"]",
                        },
                    ],
                }
            ]
        }
        name_map = {"Spain": "spain"}
        snapshot = fetch_market_snapshot.build_snapshot_from_search(payload, name_map, event_slug="world-cup-winner")

        self.assertEqual(snapshot["status"], "available")
        self.assertEqual(snapshot["event_slug"], "world-cup-winner")
        self.assertAlmostEqual(snapshot["teams"]["spain"]["probability"], 16.95)
        self.assertEqual(len(snapshot["unmapped_markets"]), 1)
        self.assertIn("只代表外界怎么看", snapshot["display_rule"])


if __name__ == "__main__":
    unittest.main()
