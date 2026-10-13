# Backend

Python side of the project. The architecture, who edits what, and the shared files are in the repository [README](../README.md).

```bash
python -m backend.api                        # from the repository root, http://localhost:8000
python -m backend.api --only fall_detection  # serve just one module while you develop
python -m unittest discover -s backend/tests -t .
```

```text
api/        routes.py (the route table), server.py (HTTP), __main__.py
shared/     contract.py (validation, reads each module's contract.py), export.py (write_replay, read_replay), paths.py
tests/      contract and route tests
modules/    one folder per module: preprocessing/ training/ experiments/ evaluation/ outputs/ api.py contract.py
```

The shared code uses only the standard library. Module-specific packages go in `modules/<module>/requirements.txt`.
