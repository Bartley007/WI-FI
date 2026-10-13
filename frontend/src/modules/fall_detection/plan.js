// Plan for this module. Edit freely: add, remove or reword items, and move `s` from 'planned' to 'doing' to 'done'.
// Starting text follows the team proposal.
const p = (t, s = 'planned') => ({ t, s })

export default {
  preprocessing: [
    p("Read FallDetection data with the official splits; windowing and quality marks"),
    p("List hard cases the data does not cover: quick sit, lying down on purpose, strong motion, interference"),
  ],
  training: [
    p("1D-CNN baseline"),
    p("1D-CNN + LSTM for the order of changes before and after a fall"),
    p("Class weights, early stopping, repeated runs"),
  ],
  experiments: [
    p("Threshold chosen on validation data only"),
    p("Single-window score vs consecutive-window rule, with activity-change evidence from activity recognition"),
  ],
  evaluation: [
    p("Fall recall, precision and F1; false alarms and the hard cases"),
    p("Event-level recall, false alarms per hour and alert delay, only if continuous recordings exist"),
    p("State machine: normal, suspected fall, sustained high risk"),
  ],
}
