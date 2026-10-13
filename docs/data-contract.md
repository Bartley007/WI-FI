# Data contract

Every module produces one JSON document, the replay JSON. The module page, the landing floor plan and the fusion page all read it.

Sources, in order: the backend (`GET <VITE_BACKEND_URL>/api/<module>/replay`, file `backend/modules/<module>/outputs/replay.json`), then the bundled `frontend/src/modules/<module>/data/replay.json`.
Write both with one call: `backend.shared.export.write_replay("<module>", payload, bundle=True)`. It validates the payload first.

```json
{
  "module": "fall_detection",
  "version": "0.1",
  "mock": true,
  "frames": [ { "t": 0, "...": "module fields" } ],
  "metrics": { "table": [ {} ], "confusion": { "labels": [], "matrix": [[]] } }
}
```

## General rules (the same for every module)

- `frames` is required and sorted by `t`, the seconds on the replay timeline. Each frame has `t` plus the module's own fields.
- Modules do not need frames at the same `t`. The landing page and the fusion page use each module's latest frame at or before the current time.
- Set `mock` to `false`, or drop it, once the data is real. Pages show a placeholder notice while it is `true`.
- `unknown` and `not_assessable` are decision states, not training classes.
- A module with missing or failing data shows as "no data". The rest keep working.

## The module's own fields

Each module declares its fields in `backend/modules/<module>/contract.py` (`FRAME_FIELDS`), and lists them in its backend README.
Changing them touches only that module's folders. The one outside reader is fusion (`frontend/src/features/fusion/rules.js`), so tell its owner.

## Optional blocks that fill the module page stages

| Key | Shape |
|---|---|
| `preprocessing` | `{ tiles: [{label, value}], table: [rows] }` |
| `training` | `{ table: [rows] }` |
| `experiments` | `{ table: [rows] }` |
| `metrics` | `{ table: [rows], confusion: { labels, matrix } }` |

Each `table` is a list of flat row objects; the keys become column headers. A missing block shows a hint on the page.
The plan checklist comes from `frontend/src/modules/<module>/plan.js`.

## Fusion rules (frontend/src/features/fusion/rules.js)

- Motion source is Human with confidence at least 0.6: activity and fall detection are used.
- Motion source is Fan: breathing evidence is trusted less.
- Fall `alert` or `suspected` is shown only when motion source passes the Human gate.
- Nothing usable: room state is Uncertain.

Fusion is a transparent demo of the expected effect. Modules use different datasets, so the combined view is not a joint ground truth.
