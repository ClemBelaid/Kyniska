import numpy as np
from core import Mire, Observation
from core.projection import project_mire_to_plane


def test_projection_returns_observation():
    m = Mire([[0, 0, 0], [1, 0, 0]])
    obs = project_mire_to_plane(m, np.array([0, 0, 1]))

    assert isinstance(obs, Observation)


def test_projection_keeps_count():
    m = Mire([[0, 0, 0], [1, 0, 0], [2, 0, 0]])
    obs = project_mire_to_plane(m, np.array([0, 0, 1]))

    assert len(obs) == 3


def test_projection_keeps_ids():
    m = Mire([[0, 0, 0], [1, 0, 0]], ids=[5, 9])
    obs = project_mire_to_plane(m, np.array([0, 0, 1]))

    assert np.array_equal(obs.ids, np.array([5, 9]))
