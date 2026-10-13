// Finds every module folder automatically: src/modules/<module>/{meta.js, plan.js, index.jsx, data/replay.json}.
// Nobody edits this file when working on a module. To add a module, add a folder.
const metas = import.meta.glob('./*/meta.js', { eager: true })
const plans = import.meta.glob('./*/plan.js', { eager: true })
const pages = import.meta.glob('./*/index.jsx', { eager: true })
const replays = import.meta.glob('./*/data/replay.json', { eager: true })

const idOf = (path) => path.split('/')[1]
const pick = (files, id, sub) => files[`./${id}/${sub}`]?.default

export const MODULES = Object.keys(metas)
  .map(idOf)
  .map((id) => ({
    id,
    ...pick(metas, id, 'meta.js'),
    plan: pick(plans, id, 'plan.js') || {},
    Page: pick(pages, id, 'index.jsx'),
    bundled: pick(replays, id, 'data/replay.json') || null,
  }))
  .sort((a, b) => (a.order ?? 99) - (b.order ?? 99) || a.id.localeCompare(b.id))
