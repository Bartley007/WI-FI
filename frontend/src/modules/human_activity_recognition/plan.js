// Plan for this module. Edit freely: add, remove or reword items, and move `s` from 'planned' to 'doing' to 'done'.
// Starting text follows the team proposal.
const p = (t, s = 'planned') => ({ t, s })

export default {
  preprocessing: [
    p("Read HumanActivityRecognition HDF5, metadata and official splits; keep user, environment, device ids"),
    p("Check label definitions before training; map to standing, sitting, walking or lying only when the data supports it"),
    p("Normalisation fitted on training data only; subcarrier trimming or zero padding with valid_length"),
  ],
  training: [
    p("1D-CNN baseline for local temporal features"),
    p("CNN-Transformer for longer-range changes"),
    p("Keep time order and source metadata during training"),
  ],
  experiments: [
    p("Does the complex model really help on confusable activities, not just add size"),
    p("Three seeds, mean and std"),
  ],
  evaluation: [
    p("Macro-F1, per-class precision and recall, confusion matrix of the five official activities"),
    p("OOD results across user, environment and device; transitions, low quality input and class imbalance analysed separately"),
    p("Output: activity, confidence and stability; uncertain during transitions"),
  ],
}
