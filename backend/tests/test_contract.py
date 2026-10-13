import unittest

from backend.shared.contract import frame_fields, validate_replay


class ContractTest(unittest.TestCase):
    def test_valid_replay_has_no_problems(self):
        frames = [{"t": 0, "fall_score": 0.1, "state": "normal"}, {"t": 5, "fall_score": 0.9, "state": "alert"}]
        self.assertEqual(validate_replay("fall_detection", {"frames": frames}), [])

    def test_missing_field_is_reported(self):
        problems = validate_replay("fall_detection", {"frames": [{"t": 0}]})
        self.assertTrue(any("fall_score" in p for p in problems))

    def test_time_must_not_go_backwards(self):
        frames = [{"t": 5, "fall_score": 0, "state": "normal"}, {"t": 1, "fall_score": 0, "state": "normal"}]
        self.assertTrue(any("backwards" in p for p in validate_replay("fall_detection", {"frames": frames})))

    def test_unknown_module_and_empty_frames(self):
        self.assertIsNone(frame_fields("nope"))
        self.assertTrue(validate_replay("nope", {"frames": []}))
        self.assertTrue(validate_replay("fall_detection", {"frames": []}))


if __name__ == "__main__":
    unittest.main()
