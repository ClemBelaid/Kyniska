import numpy as np
from core import Mire


def test_init_default_ids():
    m = Mire([[0, 0, 0], [1, 2, 3]])
    assert len(m) == 2
    assert np.array_equal(m.ids, np.array([0, 1]))


def test_init_custom_ids():
    m = Mire([[0, 0, 0], [1, 2, 3]], ids=[10, 20])
    assert np.array_equal(m.ids, np.array([10, 20]))


def test_copy_independent():
    m1 = Mire([[0, 0, 0]])
    m2 = m1.copy()

    m2.points[0, 0] = 42

    assert m1.points[0, 0] == 0
    assert m2.points[0, 0] == 42


def test_len():
    m = Mire([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
    assert len(m) == 3
