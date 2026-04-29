import numpy as np
import pytest
from core.geometry import calculBirapport, perpendicular_vector


def test_perpendicular_vector():
    v = np.array([1.0, 2.0, 3.0])
    p = perpendicular_vector(v)

    assert abs(np.dot(v, p)) < 1e-10


def test_zero_vector():
    with pytest.raises(ValueError):
        perpendicular_vector(np.array([0.0, 0.0, 0.0]))


def test_birapport_known_case():
    a = np.array([0.0, 0.0])
    b = np.array([1.0, 0.0])
    c = np.array([3.0, 0.0])
    d = np.array([4.0, 0.0])

    val = calculBirapport(a, b, c, d)

    assert abs(val - (8 / 3)) < 1e-10
