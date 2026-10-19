# Local test results

Date: 2026-10-19  
Environment: local macOS CPU, Python 3.13, no full csi-bench download

## Automated checks

| Check | Result |
|---|---|
| Ruff format | passed |
| Ruff static checks | passed |
| Mypy | passed |
| Bandit | passed |
| Module B tests | 40 passed |
| Repository contract tests | 13 passed |
| Committed HDF5 fixture | loaded and trained |
| Subset extraction test | passed |

## Synthetic fixture experiment

The experiment uses only the committed fixture:

- 16 HDF5 samples
- four classes
- 8 train / 4 validation / 4 test
- 232 features × 24 frames
- three seeds: 42, 43, 44
- 50 epochs, early stopping patience 5

| Model | Accuracy mean ± std | Macro-F1 mean ± std |
|---|---:|---:|
| `cnn_1d` | 1.00 ± 0.00 | 1.00 ± 0.00 |
| `cnn_transformer` | 1.00 ± 0.00 | 1.00 ± 0.00 |

Reproduce:

```bash
python3 backend/modules/human_activity_recognition/scripts/evaluate_local_fixture.py \
  --epochs 50 --seeds 42,43,44
```

## Interpretation

- The local result confirms that HDF5 loading, split isolation, normalisation, both model forward/backward paths, checkpointing, prediction and replay export work.
- The fixture is intentionally separable and synthetic. A perfect result does **not** establish real-world performance and must not be reported as a csi-bench benchmark.
- Real evaluation remains pending on the Module B-only subset extracted by `prepare_local_subset.py`.
