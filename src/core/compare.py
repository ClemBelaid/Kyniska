import os
curr_dir = os.path.dirname(__file__) # Current directory
#
import matplotlib.pyplot as plt
from src.core.geometry import build_basis
from src.core.process import app_proc
from src.core.process import frst_process
from src.core.process import scd_process
from src.core.mire import Mire 
from src.core.observation import Observation 
from src.core.animation import animate_rotation

from src.core.labelisation import labeliser_points

from src.core.transformation import calcul_matrice_rotation

import numpy as np

# Save animation to GIF?
SAVE_GIF = False

#--------------------------------
# 3D scene -- Data
#--------------------------------

mire = Mire.load_json("Mire_init") # Notre mire initiale (non-rotée) et l'algo va déterminer cette rotation qui colle avec les observations de obs_ref
mire_rot = Mire.load_json("Mire_rot") # La mire tournée et translatée ayant servi à calculer obs_ref
obs_ref = Observation.load_json("obs_ref")
obs_pts = obs_ref.points

##################################################
# Création de l'écran
vn = np.array([0,0,1])
u1,u2=build_basis(vn)
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

###################################################
#Reconstruction des points 2D dans le repère monde: ils se retrouveront alors bien sur l'écran
obs_3d = np.array([
    screen["origin"] + p[0]*u1 + p[1]*u2
    for p in obs_pts
]) 

# Sélection des points (xo, yo) de référence sur l'observation
xo = obs_ref.points[0]
yo = obs_ref.points[1]

# Calcul du meilleur angle par rotation de la mire
(bst_mire, bst_xm, bst_ym, bst_score, bst_agl) = app_proc(mire, obs_ref, screen, xo, yo)

# Animation de la rotation de la mire
# Attention : il faut donner comme argument la mire après le second process, pas bst_mire !


#bst_xm = mire.points[0]
#bst_ym = mire.points[1]
#bst_agl = 0

(mire_1, xm_rote, ym_rote, lst_xm) = frst_process(mire, screen, bst_xm, bst_ym, xo, yo)
(mire_2, mire_2_inv, xm2_rote, ym2_rote, ym2_rote_inv) = scd_process(mire_1, screen, lst_xm, xm_rote, ym_rote, xo, yo)
(data, data_proj) = animate_rotation(mire_2, obs_3d, screen, xm2_rote, ym2_rote, xo, yo, bst_agl)
(data, data_proj) = animate_rotation(mire_2_inv, obs_3d, screen, xm2_rote, ym2_rote_inv, xo, yo, bst_agl)


# Impression des résultats (meilleur angle, meilleur scolre)
best_frame = int(bst_agl/np.pi*180)
print("Best angle:", best_frame)
print("Best score:", bst_score)
print("Best xm = ", bst_xm)
print("Best ym = ", bst_ym)
print("Vrai xm = ", mire.points[0])
print("Vrai ym = ", mire.points[1])


# Labélisation des points projetés de la mire
meilleurs_points_projetes = data_proj[best_frame]

# Remarque importante : on part du principe que data et data_proj contiennent 360 lignes (pour chaque angle variant d'1 degré)
# Mais si on modifie le nombre d'angles, il faut peut-être modifier un peu cette structure ...

labels_finaux = labeliser_points(meilleurs_points_projetes, obs_3d)
print("Correspondances trouvées :", labels_finaux)

# Comparaison des erreurs entre la "meilleure mire calculée" et la mire initiale de référence 
print(bst_mire.points - mire_rot.points)
