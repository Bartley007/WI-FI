"""Backend entry point for space & proximity sensing. backend/api/routes.py calls replay() for GET /api/space_proximity_sensing/replay.

Default: return the file written by evaluation code through backend.shared.export.write_replay.
Replace it with live inference if this module should compute results on request.
"""
from backend.shared.export import read_replay

MODULE = "space_proximity_sensing"


def replay() -> dict | None:
    return read_replay(MODULE)
