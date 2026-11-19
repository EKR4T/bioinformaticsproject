from django.test import SimpleTestCase

from . import engine


class EngineTests(SimpleTestCase):
    def test_examples_use_known_mutations(self):
        for e in engine.EXAMPLES:
            known, unknown = engine.resolve(e["mutations"])
            self.assertEqual(unknown, [], e["label"])

    def test_parse_accepts_spaces_and_case(self):
        tokens = engine.parse_mutations("KATG s315t\nrpoB S450L, fabG1_c-15t")
        known, unknown = engine.resolve(tokens)
        self.assertEqual(known, ["katG_S315T", "rpoB_S450L", "fabG1_c-15t"])
        self.assertEqual(unknown, [])

    def test_mdr_profile_is_called_resistant(self):
        calls = {r["drug"]: r["call"] for r in engine.predict(["katG_S315T", "rpoB_S450L"])}
        self.assertEqual(calls["INH"], "R")
        self.assertEqual(calls["RIF"], "R")

    def test_no_mutations_is_susceptible_for_first_line(self):
        calls = {r["drug"]: r["call"] for r in engine.predict([])}
        for d in ["INH", "RIF", "EMB"]:
            self.assertEqual(calls[d], "S")


class ViewTests(SimpleTestCase):
    def test_pages(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/model/").status_code, 200)
        r = self.client.get("/", {"mutations": "katG_S315T, bogus_X1Y"})
        self.assertContains(r, "bogus_X1Y")
        self.assertContains(r, "Resistant")

    def test_api(self):
        r = self.client.post("/api/predict", {"mutations": ["rpoB_S450L"]}, content_type="application/json")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["recognised"], ["rpoB_S450L"])
        self.assertEqual(len(data["predictions"]), 13)
        bad = self.client.post("/api/predict", "not json", content_type="application/json")
        self.assertEqual(bad.status_code, 400)
