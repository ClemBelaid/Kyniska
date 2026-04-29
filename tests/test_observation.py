import numpy as np
from core import Observation


def test_init():
    obs = Observation([[1, 2], [3, 4]])
    assert len(obs) == 2


def test_copy_independent():
    o1 = Observation([[1, 2]])
    o2 = o1.copy()

    o2.points[0, 0] = 99

    assert o1.points[0, 0] == 1
    assert o2.points[0, 0] == 99


def test_with_ids():
    obs = Observation([[1, 2]], ids=[7])
    assert obs.ids == [7]
