import io
import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError
from xml.etree import ElementTree as ET

from scripts import update_profile as profile


NOW = datetime(2026, 11, 12, 14, 48, tzinfo=timezone.utc)
ROOT = Path(__file__).resolve().parents[1]


class ProfileTests(unittest.TestCase):
    def test_age_handles_calendar_boundaries(self):
        cases = [
            (date(2021, 4, 23), date(2026, 11, 12), "5 years, 6 months, 20 days"),
            (date(2024, 2, 29), date(2025, 2, 28), "1 year, 0 months, 0 days"),
            (date(2025, 1, 31), date(2025, 3, 1), "0 years, 1 month, 1 day"),
        ]
        for created, today, expected in cases:
            with self.subTest(created=created, today=today):
                self.assertEqual(profile.account_age(created, today), expected)

    def test_contribution_count_accepts_markup_spacing_and_zero(self):
        self.assertEqual(profile.parse_contributions(
            '<h2>2,741\n <span>contributions</span> in the last year</h2>'), 2741)
        self.assertEqual(profile.parse_contributions(
            '<h2>0 contributions in the last year</h2>'), 0)
        self.assertEqual(profile.parse_contributions(
            '<h2>1 contribution in the last year</h2>'), 1)

    def test_missing_contribution_count_is_not_a_zero(self):
        with self.assertRaises(ValueError):
            profile.parse_contributions('<html>Please sign in</html>')

    def test_all_pages_count_forks_separately_without_fork_stars(self):
        page_one = [{"id": i, "fork": False, "stargazers_count": 2}
                    for i in range(100)]
        responses = {
            "https://api.github.com/users/example": {
                "created_at": "2021-04-23T04:18:05Z", "followers": 19},
            "https://api.github.com/users/example/repos?type=owner&per_page=100&page=1": page_one,
            "https://api.github.com/users/example/repos?type=owner&per_page=100&page=2": [
                {"id": 100, "fork": True, "stargazers_count": 900}],
            "https://github.com/users/example/contributions":
                '<h2>2,741 contributions in the last year</h2>',
        }

        def respond(request, timeout):
            self.assertEqual(timeout, 30)
            if request.full_url.startswith("https://api.github.com/"):
                self.assertEqual(request.get_header("Authorization"), "Bearer synthetic-token")
            else:
                self.assertIsNone(request.get_header("Authorization"))
            value = responses[request.full_url]
            return io.BytesIO((value if isinstance(value, str) else json.dumps(value)).encode())

        with patch.object(profile, "urlopen", side_effect=respond):
            stats = profile.collect_stats("example", NOW, "synthetic-token")
        self.assertEqual(stats["repos"], 100)
        self.assertEqual(stats["forks"], 1)
        self.assertEqual(stats["stars"], 200)
        self.assertEqual(stats["followers"], 19)
        self.assertEqual(stats["contributions"], 2741)

    def test_refresh_failure_preserves_existing_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "assets").mkdir()
            (root / "profile.json").write_text('{"username":"example"}')
            paths = [root / "assets" / name for name in
                     ("profile-dark.svg", "profile-light.svg", "profile-dark-mobile.svg",
                      "profile-light-mobile.svg", "github-stats.json")]
            for path in paths:
                path.write_text("previous snapshot")
            with patch.object(profile, "urlopen", side_effect=URLError("offline")):
                with self.assertRaises(URLError):
                    profile.update(root)
            self.assertEqual([path.read_text() for path in paths], ["previous snapshot"] * 5)

    def test_generated_cards_escape_text_and_include_zero_statistics(self):
        config = {
            "username": "example", "header": "name<&>",
            "fields": [["OS", "A & B <test>"], ["Uptime", "{uptime}"]],
            "contact": [["Website", "example.com"]],
        }
        avatar = {"cols": 2, "rows": 1, "rgb": [0, 0, 0, 255, 255, 255]}
        stats = {"created_at": "2021-04-23T04:18:05Z", "as_of": NOW.isoformat(),
                 "repos": 0, "forks": 0, "stars": 0, "followers": 0, "contributions": 0}
        for theme in ("dark", "light"):
            with self.subTest(theme=theme):
                card = profile.render_card(config, avatar, stats, theme)
                tree = ET.fromstring(card)
                texts = " ".join(tree.itertext())
                self.assertIn("name<&>", texts)
                self.assertIn("A & B <test>", texts)
                self.assertIn("5 years, 6 months, 20 days", texts)
                self.assertIn("2026-11-12 22:48 UTC+8", texts)
                values = ["".join(node.itertext()) for node in tree.findall(
                    ".//s:text[@class='value']", {"s": "http://www.w3.org/2000/svg"})]
                self.assertEqual(values.count("0"), 3)
                self.assertIn("0 {Forks: 0}", values)
                self.assertEqual(tree.get("viewBox"), "0 0 985 560")
                self.assertNotIn("<script", card)

    def test_mobile_card_preserves_content_with_readable_intrinsic_width(self):
        config = json.loads((ROOT / "profile.json").read_text())
        avatar = json.loads((ROOT / "assets/avatar.json").read_text())
        stats = {"created_at": "2021-04-23T04:18:05Z", "as_of": NOW.isoformat(),
                 "repos": 7, "forks": 356, "stars": 5, "followers": 19, "contributions": 2741}
        card = profile.render_card(config, avatar, stats, "dark", mobile=True)
        tree = ET.fromstring(card)
        self.assertEqual(tree.get("width"), "420")
        self.assertGreater(int(tree.get("height")), 900)
        text = " ".join(tree.itertext())
        for expected in ("GPT", "ENG", "LaTeX, Markdown, HTML", "2,741", "356"):
            self.assertIn(expected, text)
        self.assertNotIn("script", [element.tag for element in tree.iter()])


if __name__ == "__main__":
    unittest.main()
