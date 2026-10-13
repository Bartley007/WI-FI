"""Backend entry point for motion source recognition. backend/api/routes.py calls replay() for GET /api/motion_source_recognition/replay.

Default: return the file written by evaluation code through backend.shared.export.write_replay.
Replace it with live inference if this module should compute results on request.
"""
from backend.shared.export import read_replay

MODULE = "motion_source_recognition"


def replay() -> dict | None:
    return read_replay(MODULE)
