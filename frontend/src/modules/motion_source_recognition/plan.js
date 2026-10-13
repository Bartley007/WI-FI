// Plan for this module. Edit freely: add, remove or reword items, and move `s` from 'planned' to 'doing' to 'done'.
// Starting text follows the team proposal.
const p = (t, s = 'planned') => ({ t, s })

export default {
  preprocessing: [
    p("Read HDF5, metadata and official splits; keep user, environment, device and session ids"),
    p("Quality checks on CSI amplitude; normalisation fitted on training data only"),
    p("Train and test split by whole recording batches, so neighbouring segments never cross sets"),
  ],
  training: [
    p("Time-series statistics with a tree model as the baseline"),
    p("MiniRocket and a light 1D convolutional model for comparison"),
  ],
  experiments: [
    p("Choose the final model by minority-class recognition, compute cost and cross-environment stability"),
    p("If minority-class batches are too few, repeat over several grouped splits and report mean and std"),
  ],
  evaluation: [
    p("Macro-F1, per-class recall, rejection rate and false rejection of known classes"),
    p("Confusion matrix for Human, Pet, Robot and Fan, focus on Human vs Fan and Pet vs Human"),
    p("Output class and confidence for the other modules; low confidence gives Unknown (a decision state, not a training class)"),
  ],
}
