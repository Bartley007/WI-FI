// Plan for this module. Edit freely: add, remove or reword items, and move `s` from 'planned' to 'doing' to 'done'.
// Starting text follows the team proposal.
const p = (t, s = 'planned') => ({ t, s })

export default {
  preprocessing: [
    p("Read and validate the BreathingDetection official splits", "done"),
    p("Mark low signal quality and fan-like periodic signals", "doing"),
  ],
  training: [
    p("Traditional baseline: spectral peak, autocorrelation, subcarrier consistency", "done"),
    p("One time-series model: LSTM or Transformer", "done"),
  ],
  experiments: [
    p("Window length vs response time for slow, weak signals"),
    p("Effect of motion interference, fan periodic signal and low quality"),
  ],
  evaluation: [
    p("Recall, precision and F1; empty room, motion and fan interference analysis", "doing"),
    p("Output \"not assessable\" when activity recognition sees clear motion, motion source recognition gives high Fan probability or quality is low"),
  ],
}
