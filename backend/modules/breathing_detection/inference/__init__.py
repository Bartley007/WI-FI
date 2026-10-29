"""Inference and decision gating for breathing detection."""

from .gating import (
    GateConfig,
    GateDecision,
    GateInputs,
    GateReason,
    decide_breathing_status,
)

__all__ = [
    "GateConfig",
    "GateDecision",
    "GateInputs",
    "GateReason",
    "decide_breathing_status",
]
