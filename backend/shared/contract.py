"""Checks a replay JSON against the module's own contract (backend/modules/<module>/contract.py).

Shared code knows no field names; each module declares its own FRAME_FIELDS. General rules: docs/data-contract.md.
"""
from importlib import import_module


def frame_fields(module: str) -> list[str] | None:
    """The module's declared fields, or None if it has no contract.py."""
    try:
        return import_module(f"backend.modules.{module}.contract").FRAME_FIELDS
    except ModuleNotFoundError:
        return None


def validate_replay(module: str, payload: dict) -> list[str]:
    """Return a list of problems. Empty list means the payload follows the contract."""
    fields = frame_fields(module)
    if fields is None:
        return [f"module {module!r} has no backend/modules/{module}/contract.py"]
    frames = payload.get("frames")
    if not isinstance(frames, list) or not frames:
        return ['"frames" must be a non-empty list']
    problems = []
    last_t = None
    for i, frame in enumerate(frames):
        if "t" not in frame:
            problems.append(f"frame {i}: missing t")
            continue
        if last_t is not None and frame["t"] < last_t:
            problems.append(f"frame {i}: t goes backwards")
        last_t = frame["t"]
        for field in fields:
            if field not in frame:
                problems.append(f"frame {i}: missing {field}")
    return problems
