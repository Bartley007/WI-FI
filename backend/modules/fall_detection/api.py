"""Backend entry point for fall detection. backend/api/routes.py calls replay() for GET /api/fall_detection/replay.

Default: return the file written by evaluation code through backend.shared.export.write_replay.
Replace it with live inference if this module should compute results on request.
"""
from backend.shared.export import read_replay

MODULE = "fall_detection"


def replay() -> dict | None:
    return read_replay(MODULE)
