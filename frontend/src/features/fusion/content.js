// Text content of the fusion page. Edit the lists in place.
// Rules shown here mirror src/features/fusion/rules.js and proposal section 4.8.
export const RULES = [
  ['Motion source: Human probability is high', 'Enable the human activity and fall detection interpretation'],
  ['Motion source: Fan probability is high', 'Lower the trust of breathing detection reading a periodic signal as breathing'],
  ['Fall detection: consecutive high fall scores', 'Combine with quality and time consistency into suspected fall or alert'],
  ['Space and proximity: spatial confidence is low', 'Keep the other outputs, show location as Unknown'],
  ['All valid module evidence is weak', 'Output Uncertain, never force an activity, breathing or empty-room conclusion'],
]

export const CHECKS = [
  ['Interface consistency', 'Fields complete, each module can start and stop alone, errors are recovered'],
  ['Time consistency', 'False alarms and delay: single window vs consecutive-window rule'],
  ['Uncertainty', 'Share of Unknown / Uncertain outputs and the false rejection of known classes'],
  ['Run time', 'Preprocessing, per-module inference, end-to-end replay latency and resources'],
  ['End-to-end correctness', 'Only where synchronised joint labels exist. Otherwise interface and scenario demo only'],
]

// Draft suggestions. Edit in place; `area` groups the cards.
export const IDEAS = [
  { area: 'Fusion', t: 'Check how often the Human gate in motion source recognition blocks a correct fall alert, and tune the 0.6 gate on validation data', why: 'A wrong gate hides real falls or lets pets trigger alerts' },
  { area: 'Fusion', t: 'Share one confidence convention (calibrated probability) across modules before comparing thresholds', why: 'In the current data format fall detection reports a score while motion source and space report probabilities' },
  { area: 'Data', t: 'Record a small synchronised set in one room (human, fan, pet walking, a staged fall) with consent', why: 'Gives a joint ground truth for end-to-end numbers, which the public subsets cannot' },
  { area: 'Data', t: 'Report each module on unseen users, rooms and devices next to its in-distribution score', why: 'Models may learn the room or device, not the motion' },
  { area: 'Models', t: 'Keep one baseline and one main model per module, and keep a single model if fusion inside a module gives no clear gain', why: 'Compute and schedule limit from the proposal' },
  { area: 'Models', t: 'Prefer conservative thresholds for fall detection and report recall, precision and false alarms together', why: 'Missed falls and false alarms both create false safety' },
  { area: 'System', t: 'ESP32 real-time adapter as an optional extension after the offline replay is stable', why: 'Listed as an extension goal, not required for the core result' },
  { area: 'System', t: 'Continuous distance regression, exact trajectories, pet breathing: leave as future work', why: 'Out of scope for this stage' },
]

