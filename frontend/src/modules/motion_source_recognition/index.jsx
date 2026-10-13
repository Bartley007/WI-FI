import ModulePage from '../../components/ModulePage.jsx'
import { ProbBars } from '../../components/charts.jsx'

// Page for this module. Owner: edit freely.
// Everything for this module's frontend lives in this folder: meta.js, plan.js, data/replay.json and this page.
// Put extra components, charts and images here too.
// Add your own JSX per stage with the `stages` prop, e.g. stages={{ evaluation: <MyChart /> }}.
export default function MotionSourceRecognition() {
  return (
    <ModulePage
      id="motion_source_recognition"
      summary="Which kind of source is moving: Human, Pet, IRobot or Fan? Unknown when evidence is weak."
      renderFrame={(f) => (
        <div>
          <div className="big">{f.label} <span className="sm">confidence {Math.round(f.confidence * 100)}%</span></div>
          <ProbBars probs={f.probs} highlight={f.label} />
        </div>
      )}
    />
  )
}
