import ModulePage from '../../components/ModulePage.jsx'

// Page for this module. Owner: edit freely. Add your own JSX per stage with the `stages` prop, e.g. stages={{ evaluation: <MyChart /> }}.
// `zone` values must exist in `zones` in meta.js to appear on the landing floor plan.
export default function SpaceProximitySensing() {
  return (
    <ModulePage
      id="space_proximity_sensing"
      summary="Which zone is the target in, and roughly how close to the WiFi device?"
      renderFrame={(f) => (
        <div className="big">{f.zone} <span className="sm">proximity {f.proximity ?? 'unknown'}, confidence {Math.round(f.confidence * 100)}%</span></div>
      )}
    />
  )
}
