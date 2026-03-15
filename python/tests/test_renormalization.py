import numpy as np

from coherence.kernel.renormalization import coarse_grain, renormalize


def test_coarse_grain_block_average():
    field = np.array([1, 3, 2, 2, 0, 4], dtype=float)
    result = coarse_grain(field, scale=2)
    assert np.allclose(result, np.array([2.0, 2.0, 2.0]))


def test_renormalize_divides_by_max():
    field = np.array([1, 3, 2, 2, 0, 4], dtype=float)
    result = renormalize(field, scale=2)
    assert np.allclose(result, np.array([1.0, 1.0, 1.0]))


def test_renormalize_handles_zero_max():
    field = np.zeros(4)
    result = renormalize(field, scale=2)
    assert np.allclose(result, np.zeros(2))
