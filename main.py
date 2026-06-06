from src.core.compare import function
from src.core.geometry import build_basis
from src.core.mire import Mire
from simulate import simulate
import numpy as np

vn = np.array([0,0,1])
u1,u2 = build_basis(vn)
origin = np.array([
        0.,
        0.,
        0.
    ])
screen = {
        "origin": origin,
        "normal": vn,
        "u1": u1,
        "u2": u2
    }

mire = Mire.load_json("vrMire") # Notre mire initiale (non-rotée) et l'algo va déterminer cette rotation qui colle avec les observations de obs_ref

somme_score = 0
somme_taux_corrects = 0
for i in range(100):
    print(i)
    print(somme_score/100, somme_taux_corrects/100)
    simulate(screen)
    score, taux_corrects = function(mire, screen)
    somme_score += score
    somme_taux_corrects += taux_corrects