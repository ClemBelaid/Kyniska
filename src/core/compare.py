import os
curr_dir = os.path.dirname(__file__) # Current directory
#
from src.core.geometry import build_basis
from src.core.process import app_proc
from src.core.mire import Mire 
from src.core.observation import Observation 
from src.core.animation import animate_rotation
from src.core.labelisation import labeliser_points
import numpy as np

# Save animation to GIF?
SAVE_GIF = False

#--------------------------------
# 3D scene -- Data
#--------------------------------

mire = Mire.load_json("newMire") #notre mire non roté et l'algo va déterminer cette rotation qui colle avec les observations de obs_ref
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

# Calcul du meilleur angle par rotation de la mire
xo =  obs_ref.points[0]
yo = obs_ref.points[1]
(bst_mire, bst_xm, bst_ym, bst_score, bst_agl) = app_proc(mire, obs_ref, screen, xo, yo)

# Animation de la rotation de la mire
# Attention : il faut donner comme argument la mire initiale, pas bst_mire !
(data, data_proj) = animate_rotation(mire, obs_3d, screen, bst_xm, bst_ym, bst_agl)

bst_index = int(bst_agl/np.pi*180)

# Labélisation des points projetés de la mire
meilleurs_points_projetes = data_proj[bst_index]

# Remarque importante : on part du principe que data et data_proj contiennent 360 lignes (pour chaque angle variant d'1 degré)
# Mais si on modifie le nombre d'angles, il faut peut-être modifier un peu cette structure ...

labels_finaux = labeliser_points(meilleurs_points_projetes, obs_3d)
print("Correspondances trouvées :", labels_finaux)
