"""Checks that every module is complete on both sides and that its bundled website data follows its own contract.
Run `npm test` after adding or changing a module: if this passes, the module plugs in."""
import json
import unittest

from backend.api.routes import MODULES
from backend.shared.contract import frame_fields, validate_replay
from backend.shared.paths import MODULES_DIR, REPO_ROOT

FRONTEND_MODULES = REPO_ROOT / "frontend" / "src" / "modules"
STAGES = ["preprocessing", "training", "experiments", "evaluation"]


class ModulesTest(unittest.TestCase):
    def test_backend_and_frontend_have_the_same_modules(self):
        backend = {p.name for p in MODULES_DIR.iterdir() if (p / "api.py").exists()}
        frontend = {p.name for p in FRONTEND_MODULES.iterdir() if (p / "meta.js").exists()}
        self.assertEqual(backend, frontend)

    def test_backend_module_is_complete(self):
        for name in MODULES:
            with self.subTest(module=name):
                base = MODULES_DIR / name
                self.assertIsNotNone(frame_fields(name), "contract.py with FRAME_FIELDS is missing")
                for stage in STAGES:
                    self.assertTrue((base / stage).is_dir(), f"{stage}/ is missing")

    def test_frontend_module_is_complete(self):
        for name in MODULES:
            with self.subTest(module=name):
                for f in ["meta.js", "plan.js", "index.jsx", "data/replay.json"]:
                    self.assertTrue((FRONTEND_MODULES / name / f).exists(), f"{f} is missing")

    def test_bundled_replay_follows_the_contract(self):
        for name in MODULES:
            with self.subTest(module=name):
                payload = json.loads((FRONTEND_MODULES / name / "data" / "replay.json").read_text())
                self.assertEqual(validate_replay(name, payload), [])


if __name__ == "__main__":
    unittest.main()
