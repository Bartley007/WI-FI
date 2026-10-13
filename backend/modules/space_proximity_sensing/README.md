# Space & proximity sensing (backend)

Output: zone and proximity level.

Everything for this module on the backend lives in this folder. Work on your own branch and edit only here.

| Folder | Put here |
|---|---|
| `preprocessing/` | Data reading, quality checks, splits and features. |
| `training/` | Model definitions and training scripts. |
| `experiments/` | Model comparison, ablations and threshold studies. |
| `evaluation/` | Metrics, confusion matrices, error analysis, and the export of outputs/replay.json. |
| `outputs/` | Generated files: `replay.json` (read by the server), checkpoints, figures. Large files stay out of git. |
| `api.py` | What the server returns for this module |
| `contract.py` | The frame fields this module promises |
| `requirements.txt` | Optional, packages only this module needs |

Frontend counterpart: `frontend/src/modules/space_proximity_sensing/`.
Export a result for the website with `backend.shared.export.write_replay("space_proximity_sensing", payload, bundle=True)`. One call updates the backend output and the copy bundled with the website.
Develop alone with `python -m backend.api --only space_proximity_sensing`.

## Frame fields

Defined in `contract.py`, besides `t` (seconds).

| Field | Meaning |
|---|---|
| `zone` | a key of `zones` in the frontend meta.js, or unknown |
| `proximity` | near, mid, far or null |
| `confidence` | 0 to 1 |
