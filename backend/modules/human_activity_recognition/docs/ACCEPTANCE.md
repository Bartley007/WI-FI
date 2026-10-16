# Acceptance checklist

## Correctness

- [x] Required replay fields remain compatible.
- [x] Stable activity ids are separate from display text.
- [x] Input shape, finite values, quality and split leakage are checked.
- [x] Both models run with deterministic seeds.
- [x] Checkpoints contain model metadata and normalisation statistics.

## Security and privacy

- [x] Raw dataset access requires `system` or `researcher`.
- [x] Replay access can use `viewer`.
- [x] Path traversal is rejected.
- [x] Secrets are referenced by environment-variable name and redacted from logs.
- [x] Input bytes, batch size, concurrency and request rate are bounded.

## Tests

- [x] Unit tests.
- [x] Contract tests.
- [x] Integration tests for HDF5 and training checkpoints.
- [x] End-to-end synthetic training and prediction.
- [x] Exception and empty-data tests.
- [x] Boundary tests.
- [x] Permission tests.
- [x] Performance smoke test.
- [ ] Real csi-bench benchmark run (requires local dataset download).

## Delivery

- [x] Interface documentation.
- [x] Environment and runbook.
- [x] Configuration reference.
- [x] Dependency list.
- [x] Migration and rollback plan.
- [x] Known limitations and unverified items.
