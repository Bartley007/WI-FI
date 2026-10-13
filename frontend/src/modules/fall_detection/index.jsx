import ModulePage from '../../components/ModulePage.jsx'
import { LineChart } from '../../components/charts.jsx'

// Page for this module. Owner: edit freely. Add your own JSX per stage with the `stages` prop, e.g. stages={{ evaluation: <MyChart /> }}.
export default function FallDetection() {
  return (
    <ModulePage
      id="fall_detection"
      summary="Fall or non-fall score per window, turned into a state by consecutive-window rules."
      renderFrame={(f, { frames }) => (
        <div>
          <div className="big">{f.state} <span className="sm">score {f.fall_score.toFixed(2)}</span></div>
          <LineChart points={frames.map((x) => ({ x: x.t, y: x.fall_score }))} upTo={f.t} threshold={0.8} yLabel="Fall score over time" />
        </div>
      )}
    />
  )
}
