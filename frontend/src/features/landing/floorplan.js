// Floor plan geometry for the landing page (SVG units, viewBox 640 x 440).
// Zone names come from the space_proximity_sensing module's own meta.js (`zones`),
// so its owner edits them there.
import { MODULES } from '../../modules/registry.js'

export const FLOOR = {
  box: { x: 30, y: 30, w: 580, h: 380 },
  router: { x: 80, y: 80 },
  node: { x: 590, y: 230 },
  fan: { x: 300, y: 100 },
  furniture: [
    { name: 'BED', x: 420, y: 50, w: 170, h: 130 },
    { name: 'SOFA', x: 50, y: 270, w: 170, h: 110 },
    { name: 'DESK', x: 430, y: 290, w: 160, h: 100 },
  ],
  door: { x: 270, w: 70 },
  zones: Object.assign({}, ...MODULES.map((m) => m.zones || {})),
}
