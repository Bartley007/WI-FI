"""Write and read a module's replay output. Used by each module's api.py and by evaluation scripts."""
import json

from .contract import validate_replay
from .paths import frontend_data_file, outputs_dir


def write_replay(module: str, payload: dict, bundle: bool = False) -> None:
    """Validate and save backend/modules/<module>/outputs/replay.json.

    With bundle=True the same file is also written into the frontend module folder, so the website shows it even
    without the backend. One call updates both sides.
    """
    problems = validate_replay(module, payload)
    if problems:
        raise ValueError("replay does not follow the module contract:\n  " + "\n  ".join(problems))
    text = json.dumps(payload, indent=1)
    out = outputs_dir(module)
    out.mkdir(parents=True, exist_ok=True)
    (out / "replay.json").write_text(text)
    if bundle:
        target = frontend_data_file(module)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)


def read_replay(module: str) -> dict | None:
    """Return the saved replay, or None if the module has not exported one yet."""
    path = outputs_dir(module) / "replay.json"
    return json.loads(path.read_text()) if path.exists() else None
