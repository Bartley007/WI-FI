import ModulePage from '../../components/ModulePage.jsx'

// Page for this module. Owner: edit freely. Add your own JSX per stage with the `stages` prop, e.g. stages={{ evaluation: <MyChart /> }}.
export default function HumanActivityRecognition() {
  return (
    <ModulePage
      id="human_activity_recognition"
      summary="Which normal activity is the person doing, and how stable is the estimate?"
      renderFrame={(f) => (
        <div>
          <div className="big">{f.activity} <span className="sm">confidence {Math.round(f.confidence * 100)}%</span></div>
          <p className="sm">{f.stable ? 'Stable' : 'Transition or weak evidence'}</p>
        </div>
      )}
    />
  )
}
