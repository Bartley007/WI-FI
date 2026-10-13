"""Run from the repository root.

    python -m backend.api                              all modules on port 8000
    python -m backend.api --port 9000                  another port
    python -m backend.api --only fall_detection        just your own module while you develop
"""
import argparse

from . import routes
from .server import serve

parser = argparse.ArgumentParser(prog="python -m backend.api")
parser.add_argument("--port", type=int, default=8000)
parser.add_argument("--only", nargs="+", metavar="MODULE", help="serve only these module folders")
args = parser.parse_args()

if args.only:
    routes.MODULES = routes.discover(args.only)
    missing = set(args.only) - set(routes.MODULES)
    if missing:
        raise SystemExit(f"no such module: {', '.join(sorted(missing))}")
serve(args.port)
