# Environment and runbook

## Requirements

- Python 3.10+
- Module dependencies: `pip install -r backend/modules/human_activity_recognition/requirements.txt`
- Development checks: `pip install -r backend/modules/human_activity_recognition/requirements-dev.txt`

## Required environment variables

| Variable | Purpose | Required |
|---|---|---|
| `HAR_DATA_ROOT` or `CSI_DATA_ROOT` | csi-bench dataset root | for training with real data |
| `HAR_OUTPUT_ROOT` | checkpoints, manifests and metrics | optional; defaults to `human_activity_recognition` |
| `HAR_CONFIG` | alternate config path | optional |
| `HAR_REMOTE_ENDPOINT` | remote inference endpoint | for `remote` mode |
| `HAR_REMOTE_TOKEN` | remote bearer token | only when the endpoint requires it |

Never commit `.env.local`, tokens, dataset files, checkpoints or generated logs.

## Modes

### Local

`runtime.mode: local`. Uses local dataset and checkpoint.

### Remote

`runtime.mode: remote`. Uses `HttpTransport` with timeout, retries and classification. A missing endpoint fails before a request is sent.

### Hybrid

`runtime.mode: hybrid`. Tries remote first and falls back to local when `allow_local_fallback` is true. Degraded responses include `degraded: true` and `degradation_reason`.

## Standard checks

```bash
ruff check --config backend/modules/human_activity_recognition/pyproject.toml backend/modules/human_activity_recognition
mypy --config-file backend/modules/human_activity_recognition/pyproject.toml backend/modules/human_activity_recognition
bandit -q -r backend/modules/human_activity_recognition
python3 -m unittest discover -s backend/modules/human_activity_recognition/tests -t .
python3 -m unittest discover -s backend/tests -t .
npm --prefix frontend run build
```

## Operational limits

- Batch size, concurrency, request rate and input bytes are bounded by `runtime` config.
- Export validation happens before files are written.
- A failed module does not take down other API routes.
