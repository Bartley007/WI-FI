import unittest

from backend.api.routes import dispatch


class RoutesTest(unittest.TestCase):
    def test_health(self):
        self.assertEqual(dispatch("GET", "/api/health"), (200, {"ok": True}))

    def test_modules_are_discovered(self):
        status, body = dispatch("GET", "/api/modules")
        self.assertEqual(status, 200)
        self.assertIn("fall_detection", body)

    def test_unknown_module_is_404(self):
        self.assertEqual(dispatch("GET", "/api/nope/replay")[0], 404)

    def test_known_module_without_output_is_404_not_500(self):
        status, body = dispatch("GET", "/api/fall_detection/replay")
        self.assertIn(status, (200, 404))
        if status == 404:
            self.assertEqual(body["error"], "no output yet")

    def test_other_methods_and_paths_are_404(self):
        self.assertEqual(dispatch("POST", "/api/health")[0], 404)
        self.assertEqual(dispatch("GET", "/elsewhere")[0], 404)


if __name__ == "__main__":
    unittest.main()
