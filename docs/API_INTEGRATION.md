# API integration

How a module result gets from Python to the website.

## Request flow

```text
React page -> src/api/replay.js -> GET /api/<module>/replay -> backend/api/routes.py
           -> backend/modules/<module>/api.py replay() -> outputs/replay.json
```

If the backend is not running, or has no output for that module yet, `src/api/replay.js` uses the bundled
`frontend/src/modules/<module>/data/replay.json`. Each page shows which source it used (`backend` or `bundled`).

## Configuration

| Where | Setting | Meaning |
|---|---|---|
| `frontend/.env.local` | `VITE_BACKEND_URL=http://localhost:8000` | Turn on reading from the backend. Unset means bundled files only |
| shell | `CSI_DATA_ROOT=/path/to/data` | Where the CSI-Bench files are, read by `backend/shared/paths.py` |
| shell | `python -m backend.api --port 9000` | Run the backend on another port |
| shell | `python -m backend.api --only fall_detection` | Serve only your own module while you develop |

`npm run dev` at the repository root starts both sides and sets `VITE_BACKEND_URL` for you.

## Backend routes

All routes are listed in the `ROUTES` table in `backend/api/routes.py`.

| Method | Route | Returns |
|---|---|---|
| GET | `/api/health` | `{"ok": true}` |
| GET | `/api/modules` | Module folder names found under `backend/modules/` |
| GET | `/api/<module>/replay` | The module's replay JSON, or 404 `no output yet` |

The server allows CORS, because the website runs on another port.

## Website routes

All routes are listed in `frontend/src/app/router.jsx`. The router is `HashRouter`, so addresses look like `/#/module/fall_detection` and the built files work from any static host.

| Route | Page |
|---|---|
| `/#/` | Landing page with the floor plan (`features/landing`) |
| `/#/module/<module>` | One module page; created automatically for every folder in `src/modules/` |
| `/#/fusion` | Fusion and improvement (`features/fusion`) |

## Add or change a module

1. Add the same folder name under `backend/modules/` and `frontend/src/modules/`. Nothing else needs editing: the backend finds `api.py`, the website finds `meta.js`.
2. Write `backend/modules/<module>/contract.py` with the module's `FRAME_FIELDS`, and `summarize` in the frontend `meta.js`. No shared file lists module fields.
3. Run `npm test`: it checks both sides of the module and its bundled data.
4. If it feeds the fusion rules, set `role` in `meta.js` and extend `features/fusion/rules.js`.

## Replay format

See [data-contract.md](data-contract.md).
