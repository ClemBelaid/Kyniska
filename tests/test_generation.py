from core import Mire
from core.generation import (
    generer_cube,
    generer_cone_tronque,
    generer_cone_tronque_creux,
)


def test_generer_cube():
    m = generer_cube(10)
    assert isinstance(m, Mire)
    assert len(m) == 10


def test_generer_cone_tronque():
    m = generer_cone_tronque(8)
    assert isinstance(m, Mire)
    assert len(m) == 8


def test_generer_cone_tronque_creux():
    m = generer_cone_tronque_creux(6)
    assert isinstance(m, Mire)
    assert len(m) == 6
