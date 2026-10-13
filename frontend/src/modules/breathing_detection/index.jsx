import ModulePage from '../../components/ModulePage.jsx'

// Page for this module. Owner: edit freely. Add your own JSX per stage with the `stages` prop, e.g. stages={{ evaluation: <MyChart /> }}.
export default function BreathingDetection() {
  return (
    <ModulePage
      id="breathing_detection"
      summary="Is there a stable breathing pattern? 'Not assessable' when motion, a fan or low quality gets in the way."
      renderFrame={(f) => (
        <div className="big">{f.status.replace('_', ' ')} <span className="sm">confidence {Math.round(f.confidence * 100)}%</span></div>
      )}
    />
  )
}
