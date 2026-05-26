import os
curr_dir = os.path.dirname(__file__) # Current directory
#
import matplotlib.pyplot as plt
from matplotlib import animation
from src.core.geometry import build_basis
from src.core.process import app_proc
from src.core.transformation import calcul_matrice_rotation
from src.core.mire import Mire 
from src.core.observation import Observation 
from src.core.animation import animate_rotation
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
# Tout ce qui concerne l'écran : origine, vect normal et vect directeurs
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

(bst_mire, bst_xm , bst_ym , bst_score , bst_agl ) = app_proc(mire,obs_ref,screen,obs_ref.points[0],obs_ref.points[1])

animate_rotation(bst_mire, obs_3d, screen, bst_xm, bst_ym)
plt.show()