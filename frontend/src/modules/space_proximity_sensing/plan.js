// Plan for this module. Edit freely: add, remove or reword items, and move `s` from 'planned' to 'doing' to 'done'.
// Starting text follows the team proposal.
const p = (t, s = 'planned') => ({ t, s })

export default {
  preprocessing: [
    p("Pick labels from Localization and ProximityRecognition that fit the prototype room"),
    p("Zone and proximity are trained and checked separately, since labels are not joint"),
  ],
  training: [
    p("Simple classifier baseline for zones"),
    p("Compare with a small MLP or another light model; proximity as a classification problem"),
  ],
  experiments: [
    p("Accuracy, stability across environments and deployment cost"),
    p("Keep location unknown or proximity uncertain when confidence is low"),
  ],
  evaluation: [
    p("Macro-F1 for zones and for the four distance levels, per-class recall, one confusion matrix each"),
    p("Effect of user, environment and device changes"),
    p("Continuous distance, exact trajectories and multi-person localisation are out of scope"),
  ],
}
