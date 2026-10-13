# Team handoff

Who edits what. The rule: **work on your own branch and edit only your own folders**. Changes to shared files go through the whole team.

## Module owners (five modules)

You own two folders, one on each side:

```text
backend/modules/<module>/          preprocessing/  training/  experiments/  evaluation/  outputs/  api.py
frontend/src/modules/<module>/     meta.js  plan.js  data/replay.json  index.jsx
```

Your work flows in one direction:

```text
data -> preprocessing -> training -> experiments -> evaluation -> write_replay() -> outputs/replay.json
                                                                                       |
                                                              backend API  ->  your module page and the landing floor plan
```

1. Do the four stages in `backend/modules/<module>/`. Each stage has its own folder, matching the four stages shown on your page.
2. At the end of evaluation, call `backend.shared.export.write_replay("<module>", payload, bundle=True)`. It rejects a payload that breaks your module's contract, saves `outputs/replay.json`, and also writes the copy bundled with the website, so one call updates both sides.
3. Your fields live in `backend/modules/<module>/contract.py`. The text shown for one frame on the landing page is `summarize` in your `meta.js`. Both are yours to change.
4. Keep `plan.js` honest: move items from `planned` to `doing` to `done`.
5. Edit `index.jsx` to add your own charts per stage with `stages={{ evaluation: <MyChart /> }}`. Do not import backend code from React.

Develop on your own: `python -m backend.api --only <module>` serves just your module. Run `npm test` before a merge request: it checks that both sides of your module are complete and that your bundled data follows your contract.

The only reader of your fields outside your folders is fusion. If you rename a field it uses, tell the fusion owner.

## Frontend members

- Shared UI: `frontend/src/components/` (charts, page template, small UI parts) and `frontend/src/app/` (layout, router).
- Landing page and floor plan: `frontend/src/features/landing/`.
- Fusion and improvement page: `frontend/src/features/fusion/` (rules in `rules.js`, text in `content.js`).
- API client: `frontend/src/api/replay.js`. Pages never call `fetch` themselves.

## Backend and integration members

- Routes: `backend/api/routes.py` (the route table), `backend/api/server.py`.
- Contract checks and export helpers: `backend/shared/`. They know no module fields; each module declares its own in `contract.py`.
- Tests: `backend/tests/`. Add a test when you change a route or the contract.

## Fusion

The fusion rules are the transparent rules from the proposal (section 4.8). They currently run in the browser (`frontend/src/features/fusion/rules.js`) on each module's replay. If fusion moves to the backend, keep the same input and output shape and update `docs/API_INTEGRATION.md`.

## Before opening a merge request

```bash
npm run check      # backend tests, then a frontend build
```

Do not commit `.env.local`, `node_modules`, `dist`, the CSI-Bench data, or large model files.
