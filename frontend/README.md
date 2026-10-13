# Frontend

React + Vite website. The architecture, who edits what, and the shared files are in the repository [README](../README.md).

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # static files in dist/
```

```text
src/
  main.jsx          entry point
  app/              router.jsx (all routes), Layout.jsx (navigation)
  api/              replay.js (data loading: backend first, bundled file as fallback)
  components/       charts.jsx, ModulePage.jsx (page template for a module), ui.jsx
  features/         landing/ (floor plan), fusion/ (rules.js, content.js, page)
  modules/          one folder per module, found by registry.js
  styles/           global.css
```

Set `VITE_BACKEND_URL` in `.env.local` (see `.env.example`) to read from the backend.
