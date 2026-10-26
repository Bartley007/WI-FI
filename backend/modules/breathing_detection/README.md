# Breathing detection (backend)

Output: breathing evidence or "not assessable".

Everything for this module on the backend lives in this folder. Work on your own branch and edit only here.

| Folder | Put here |
|---|---|
| `preprocessing/` | Data reading, quality checks, splits and features. |
| `training/` | Model definitions and training scripts. |
| `experiments/` | Model comparison, ablations and threshold studies. |
| `evaluation/` | Metrics, confusion matrices, error analysis, and the export of outputs/replay.json. |
| `outputs/` | Generated files: `replay.json` (read by the server), checkpoints, figures. Large files stay out of git. |
| `api.py` | What the server returns for this module |
| `contract.py` | The frame fields this module promises |
| `requirements.txt` | Optional, packages only this module needs |

Frontend counterpart: `frontend/src/modules/breathing_detection/`.
Export a result for the website with `backend.shared.export.write_replay("breathing_detection", payload, bundle=True)`. One call updates the backend output and the copy bundled with the website.
Develop alone with `python -m backend.api --only breathing_detection`.

## Dataset preprocessing

Install this module's dependencies into the project environment:

```bash
.venv/bin/python -m pip install -r backend/modules/breathing_detection/requirements.txt
```

Load an official split lazily (one HDF5 file is read per indexed sample):

```python
from backend.modules.breathing_detection.preprocessing import BreathingDataset

train = BreathingDataset("data/BreathingDetection", "train_id")
sample = train[0]
# project_pipeline output: [channel=1, subcarriers=K, time=300]
```

The default `project_pipeline` keeps the real 300-point window and variable
subcarrier count. Use `mode="official_reproduction"` only for a benchmark
comparison; it reproduces the authors' generic `[1, 500, 232]` padding and
clipping rule. Both modes use the downloaded official split files and
per-sample z-score normalization.

Run this module's tests with:

```bash
.venv/bin/python -m unittest discover \
  -s backend/modules/breathing_detection/tests -t . -v
```

## Interpretable periodicity baseline

The first baseline selects high-variance subcarriers and extracts 18 fixed
features covering breathing-band FFT energy and peaks, spectral entropy,
autocorrelation peaks, cross-subcarrier peak consistency, waveform agreement,
and a high-frequency motion proxy. A small balanced logistic regression keeps
the decision inspectable through its saved coefficients.

Run a short smoke experiment:

```bash
.venv/bin/python -m \
  backend.modules.breathing_detection.training.train_periodicity_baseline \
  --data-root data/BreathingDetection --max-train 400 --max-val 200
```

Omit the limits for the full train/validation run and add `--evaluate-test`
for the final test pass. The decision threshold is
selected on validation macro-F1, not the test set. Outputs are written under
the module's ignored `outputs/` directory. Small smoke-run scores are pipeline
checks only and must not be reported as final results.

The completed full-run analysis is recorded in
[`PERIODICITY_BASELINE_REPORT.md`](PERIODICITY_BASELINE_REPORT.md).

## Lightweight LSTM

The LSTM pipeline and its validation-only early stopping are implemented in
`training/train_lstm.py`. Cross-subcarrier statistics and per-sample Top-32
selection were rejected in controlled pilots. Preserving subcarrier order and
interpolating to a fixed 232-position frequency axis passed the promotion
criteria (validation macro-F1 0.8187). See
[`LSTM_PILOT_REPORT.md`](LSTM_PILOT_REPORT.md). Pilot scores are not final
full-split results.

Three complete-split seeds confirmed stable validation performance. The frozen
seed 123 candidate reached test macro-F1 0.9670 and an empty-room
false-positive rate of 0.0673. See
[`LSTM_FULL_RUN_REPORT.md`](LSTM_FULL_RUN_REPORT.md) for the full configuration,
confusion matrices, and subcarrier-count analysis.
The concentrated K=208 false positives are investigated in
[`K208_ERROR_ANALYSIS.md`](K208_ERROR_ANALYSIS.md).

### Interpolated sequence cache

Full float32 `[300,232]` arrays would use about 26 GB across all splits. The
cache stores float16 memory-mapped arrays instead (about 13 GB total) and
converts each batch back to float32 during training. It records progress every
250 samples and resumes a compatible partial build.

Build/resume train and validation caches while starting training:

```bash
.venv/bin/python -m backend.modules.breathing_detection.training.train_lstm \
  --data-root data/BreathingDetection \
  --representation interpolated \
  --cache-dir backend/modules/breathing_detection/outputs/temporal_cache \
  --build-cache
```

On later training runs, omit `--build-cache`; the completed memory-mapped cache
is loaded directly. Do not use the training script to reevaluate the frozen
model because it would train and overwrite a new checkpoint. The completed
one-way test evaluation used the read-only entry point:

```bash
.venv/bin/python -m \
  backend.modules.breathing_detection.evaluation.evaluate_lstm \
  --data-root data/BreathingDetection \
  --checkpoint backend/modules/breathing_detection/outputs/\
lstm_interpolated_full_seed123/best_model.pt \
  --cache-dir backend/modules/breathing_detection/outputs/temporal_cache \
  --output backend/modules/breathing_detection/outputs/\
lstm_interpolated_full_seed123/test_metrics.json
```

The official test result has already been observed. It must not be reused for
threshold selection, seed selection, or development of later interference
gates.

## Frame fields

Defined in `contract.py`, besides `t` (seconds).

| Field | Meaning |
|---|---|
| `status` | breathing, none or not_assessable |
| `confidence` | 0 to 1 |
