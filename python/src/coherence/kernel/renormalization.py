from __future__ import annotations

import numpy as np


def coarse_grain(field: np.ndarray, scale: int) -> np.ndarray:
    """Block-average a 1D field into bins of length ``scale``."""
    if scale <= 0:
        raise ValueError("scale must be a positive integer")

    arr = np.asarray(field, dtype=float)
    n = arr.size // scale
    if n == 0:
        raise ValueError("scale cannot exceed field length")

    trimmed = arr[: n * scale]
    return np.mean(trimmed.reshape(n, scale), axis=1)


def renormalize(field: np.ndarray, scale: int) -> np.ndarray:
    """Coarse-grain then normalize the resulting field by its maximum value."""
    coarse = coarse_grain(field, scale)
    max_value = float(np.max(coarse))
    if max_value == 0.0:
        return coarse
    return coarse / max_value
