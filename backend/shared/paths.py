"""Common paths. Nothing module-specific lives here."""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MODULES_DIR = REPO_ROOT / "backend" / "modules"

# Where the CSI-Bench files are on this machine. Set it in your shell, e.g.
#   export CSI_DATA_ROOT="/path/to/MotionSourceRecognition"
# The dataset is large and never goes into git.
DATA_ROOT = Path(os.environ["CSI_DATA_ROOT"]) if os.environ.get("CSI_DATA_ROOT") else None


def module_dir(module: str) -> Path:
    return MODULES_DIR / module


def outputs_dir(module: str) -> Path:
    return module_dir(module) / "outputs"


def frontend_data_file(module: str) -> Path:
    """The copy of replay.json bundled with the website, so it also works without the backend."""
    return REPO_ROOT / "frontend" / "src" / "modules" / module / "data" / "replay.json"
