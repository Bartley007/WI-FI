# Breathing assessability gates

## Purpose

The breathing model answers whether a 10-second CSI window contains breathing
evidence. It must not be forced to make that decision when the input is poor or
another source can create a similar pattern. `inference/gating.py` wraps the
frozen model probability in an ordered, explainable decision layer.

## Ordered decision

Only the first triggered gate becomes the primary reason:

1. invalid or low-quality CSI -> `not_assessable / low_quality`
2. clear motion -> `not_assessable / motion`
3. high external Fan probability -> `not_assessable / fan`
4. calibrated stationary-periodic risk -> `not_assessable / periodic_interference`
5. unstable consecutive-window evidence -> `not_assessable / temporal_instability`
6. otherwise apply the frozen seed 123 threshold -> `breathing` or `none`

Missing optional evidence means "unavailable", not zero risk. This distinction
prevents a disconnected activity or motion-source module from silently
asserting that a window is safe.

## Implemented now

- typed and range-checked gate inputs and configuration
- fixed precedence and machine-readable reason codes
- existing dataset quality flags feeding the quality gate
- external motion and Fan probability inputs
- explicit periodic-interference and temporal-instability inputs
- conversion to the existing public `{t, status, confidence}` frame contract
- unit tests for every gate, priority, missing evidence, threshold behaviour,
  invalid scores, and frame conversion

The public confidence is a decision-margin score. It is zero at the frozen
breathing threshold and approaches one farther from the boundary. A rejected
window reports the score of the gate that rejected it.

## Deliberately not calibrated yet

The periodic-interference and temporal-instability risk producers are not yet
implemented. The K=208 analysis cannot be converted directly into a hard gate:
the official test set has already been observed, and K is confounded with
environment, user, deployment, and label. Thresholds for new risk producers
must be developed using train/validation data only.

The next experiment must report both coverage and selective performance:

- rejection rate and reason distribution
- retained breathing recall and macro-F1
- retained empty-room false-positive rate
- fraction of existing validation errors rejected
- correct predictions unnecessarily rejected

After calibration, an independent newly collected or newly declared holdout
is required for an unbiased final assessment of the updated gated system.
