from core import Observation
from core.matching import detecter_quadruple_alignes_observation


def test_detect_quadruplet_aligned():
    obs = Observation([
        [0, 0],
        [1, 0],
        [2, 0],
        [3, 0],
    ])

    n, lst = detecter_quadruple_alignes_observation(obs)

    assert n >= 1
    assert len(lst) >= 1


def test_no_quadruplet():
    obs = Observation([
        [0, 0],
        [1, 1],
        [2, 0],
        [3, 2],
    ])

    n, lst = detecter_quadruple_alignes_observation(obs)

    assert n == 0
    assert lst == []
