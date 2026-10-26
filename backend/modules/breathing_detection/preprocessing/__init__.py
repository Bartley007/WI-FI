"""Breathing detection: Data reading, quality checks, splits and features."""
from .data import BreathingDataset, BreathingSample, DataValidationError
from .features import FEATURE_NAMES, PeriodicityFeatureConfig, extract_periodicity_features
from .temporal import (
    TEMPORAL_FEATURE_NAMES,
    TOP_VARIANCE_FEATURES,
    INTERPOLATED_FEATURES,
    extract_interpolated_subcarriers,
    extract_temporal_statistics,
    extract_top_variance_subcarriers,
)
from .cache import TemporalCache, build_temporal_cache, load_temporal_cache

__all__ = [
    "BreathingDataset",
    "BreathingSample",
    "DataValidationError",
    "FEATURE_NAMES",
    "PeriodicityFeatureConfig",
    "extract_periodicity_features",
    "TEMPORAL_FEATURE_NAMES",
    "extract_temporal_statistics",
    "TOP_VARIANCE_FEATURES",
    "INTERPOLATED_FEATURES",
    "extract_interpolated_subcarriers",
    "extract_top_variance_subcarriers",
    "TemporalCache",
    "build_temporal_cache",
    "load_temporal_cache",
]
