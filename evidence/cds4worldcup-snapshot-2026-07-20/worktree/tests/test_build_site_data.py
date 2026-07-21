import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_site_data.py"

spec = importlib.util.spec_from_file_location("build_site_data", SCRIPT)
build_site_data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_site_data)


PUBLIC_VENDOR_FORBIDDEN = build_site_data.PUBLIC_VENDOR_FORBIDDEN
PUBLIC_BETTING_FORBIDDEN = build_site_data.PUBLIC_BETTING_FORBIDDEN


def json_dump(value):
    return json.dumps(value, ensure_ascii=False)


def assert_public_payload_clean(testcase, payload):
    text = json_dump(payload)
    for term in PUBLIC_VENDOR_FORBIDDEN + PUBLIC_BETTING_FORBIDDEN:
        testcase.assertNotIn(term, text)


class BuildSiteDataTests(unittest.TestCase):
    def test_parse_deep_card_sections_do_not_bleed_into_each_other(self):
        card = build_site_data.parse_markdown_card(ROOT / "artifacts" / "team-cards" / "spain.md")

        self.assertEqual(card["status"], "deep-description")
        self.assertEqual(len(card["primary_obstacles"]), 6)
        self.assertEqual(card["primary_obstacles"][0]["类型"], "low_scoring_dependency")
        self.assertFalse(any(row.get("阻力") == "突破" for row in card["primary_obstacles"]))
        self.assertFalse(any(row.get("阻力") == "---" for row in card["primary_obstacles"]))

        self.assertEqual(len(card["required_breakthroughs"]), 4)
        self.assertEqual(card["required_breakthroughs"][0]["发生阶段"], "小组赛")
        self.assertEqual(len(card["black_swan_helpers"]), 4)
        self.assertEqual(len(card["miracle_package"]), 3)

    def test_build_outputs_expected_counts_and_obstacle_types(self):
        teams, meta = build_site_data.build_teams_json(strict=True)

        self.assertEqual(len(teams), 48)
        self.assertEqual(meta["deep_description_count"], 48)
        self.assertEqual(meta["thin_slice_count"], 0)
        self.assertEqual(meta["kimi_coverage"]["covered"], 21)
        self.assertEqual(meta["kimi_coverage"]["not_covered"], 27)
        self.assertIn("bracket_strength", meta["obstacle_type_distribution"])
        self.assertNotIn("---", meta["obstacle_type_distribution"])
        self.assertNotIn("发生阶段", meta["obstacle_type_distribution"])

    def test_build_homepage_json_has_plain_chinese_public_contract(self):
        homepage = build_site_data.build_homepage_json(strict=True)

        self.assertEqual(homepage["summary"]["total_teams"], 48)
        self.assertEqual(homepage["summary"]["deep_description_count"], 48)
        self.assertEqual(homepage["summary"]["settleable_condition_count"], 89)

        self.assertIn("team_teasers", homepage)
        self.assertGreaterEqual(len(homepage["team_teasers"]), 8)
        self.assertEqual(homepage["team_teasers"][0]["display_status_label"], "深度版")
        self.assertIn("夺冠路", homepage["team_teasers"][0]["path_thesis"])
        self.assertTrue(homepage["team_teasers"][0]["href"].startswith("team.html?team="))

        self.assertIn("obstacle_distribution", homepage)
        obstacle_labels = {row["display_label"] for row in homepage["obstacle_distribution"]}
        self.assertIn("太依赖小比分", obstacle_labels)
        self.assertIn("签表太硬", obstacle_labels)

        self.assertIn("baselines", homepage)
        baseline_labels = {row["display_name"] for row in homepage["baselines"]}
        self.assertIn("市场公开参照", baseline_labels)
        self.assertIn("公开模型群体参考", baseline_labels)
        self.assertNotIn("Kimi AI 参考", baseline_labels)
        self.assertEqual(homepage["summary"]["baseline_count"], 6)
        baseline_text = json_dump(homepage["baselines"])
        self.assertNotIn("P = 1/odds", baseline_text)
        self.assertNotIn("overround", baseline_text)
        self.assertIn("外界热度和分歧", baseline_text)

        market_status = homepage["public_signal_snapshots"]["market_public_baseline"]["status"]
        self.assertIn(market_status, ["available", "snapshot_unavailable"])
        if market_status == "available":
            self.assertIn("teams", homepage["public_signal_snapshots"]["market_public_baseline"])
            self.assertGreater(len(homepage["public_signal_snapshots"]["market_public_baseline"]["teams"]), 0)
        self.assertIn("public_model_crowd", homepage["public_signal_snapshots"])
        self.assertEqual(homepage["public_signal_snapshots"]["public_model_crowd"]["coverage_count"], 21)
        self.assertNotIn("kimi_public_ai", homepage["public_signal_snapshots"])
        self.assertEqual(homepage["public_consensus_gap"]["status"], "not_available")

        self.assertIn("ai_perspectives", homepage)
        ai = homepage["ai_perspectives"]
        self.assertEqual(ai["perspective_count"], 300)
        self.assertEqual(ai["faction_count"], 10)
        self.assertEqual(ai["covered_team_count"], 21)
        self.assertEqual(ai["source_label"], "只能参考")
        self.assertGreaterEqual(len(ai["factions"]), 10)
        assert_public_payload_clean(self, homepage)

    def test_public_site_payload_removes_internal_reference_fields(self):
        teams, meta = build_site_data.build_teams_json(strict=True)
        public_teams = build_site_data.build_public_teams_json(teams)
        public_meta = build_site_data.build_public_meta_json(meta)

        self.assertEqual(len(public_teams), 48)
        self.assertNotIn("kimi_coverage", public_meta)

        text = json_dump({"teams": public_teams, "meta": public_meta})
        forbidden_terms = [
            "Kimi", "kimi",
            "coverage_status", "kimi_probability", "kimi_baseline_signals",
            "profile_paragraph", "current_interpretation",
            "<待分析>", "<关键阻力>", "<type>",
        ]
        for term in forbidden_terms:
            self.assertNotIn(term, text)

    def test_public_team_details_have_reader_facing_analysis_without_update_contract(self):
        teams, _ = build_site_data.build_teams_json(strict=True)
        details = build_site_data.build_public_team_details_json(teams)

        self.assertEqual(len(details["teams"]), 48)
        argentina = details["teams"]["argentina"]
        self.assertEqual(argentina["detail_href"], "team.html?team=argentina")
        self.assertIn("analysis", argentina)
        self.assertIn("opening", argentina["analysis"])
        self.assertGreaterEqual(len(argentina["analysis"]["sections"]), 3)
        self.assertIn("obstacle_chart", argentina["charts"])
        self.assertIn("public_reference_chart", argentina["charts"])
        self.assertNotIn("update_contract", details)
        text = json_dump(details)
        for leaked in ["后续更新", "每场比赛后", "artifacts/team-cards", "data/processed", "scripts/build_site_data.py"]:
            self.assertNotIn(leaked, text)

        reference = argentina["public_references"]["public_model_crowd"]
        self.assertEqual(reference["status"], "available")
        self.assertIsInstance(reference["probability"], float)
        market_status = argentina["public_references"]["market_snapshot"]["status"]
        self.assertIn(market_status, ["available", "snapshot_unavailable"])
        if market_status == "available":
            self.assertIsInstance(argentina["public_references"]["market_snapshot"].get("probability"), float)

        self.assertIn("ai_perspective", argentina)
        assert_public_payload_clean(self, details)


if __name__ == "__main__":
    unittest.main()
