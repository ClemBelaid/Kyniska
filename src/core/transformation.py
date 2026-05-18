from .mire import Mire
from .observation import Observation
from math import *
<<<<<<< HEAD
#import cv2
=======
import cv2
>>>>>>> origin/main
import numpy as np
import itertools


def calcul_matrice_rotation(v, angle):
    """
<<<<<<< HEAD
    Entrée : Un vecteur v qui correspond à l'axe de rotation, et un angle en radians 
    Sortie : La matrice de rotation correspondante (selon la formule de Rodrigues)
    """
    v = np.array(v, dtype=float)
    vNorm = np.linalg.norm(v)
    if vNorm < 1e-6:
        raise ValueError("Rotation axis too small")
=======
    Entrée : Un vecteur v qui correspond à l'axe de rotation, et un angle en degrés
    Sortie : La matrice de rotation correspondante (selon la formule de Rodrigues)
    """
    vNorm = np.linalg.norm(v)
    if(vNorm < 1e-6 ):
        print("Rotation direction cannot be a null (or even small) vector!")
        # Attention : il faudrait plutôt écrire raise ValueError(...) ou quelque chose comme ça
        return None
>>>>>>> origin/main

    X = v[0] / vNorm
    Y = v[1] / vNorm 
    Z = v[2] / vNorm

<<<<<<< HEAD
    C = np.cos(angle)
    S = np.sin(angle)
=======
    vRad = pi * angle / 180
    C = np.cos(vRad)
    S = np.sin(vRad)
>>>>>>> origin/main
    OmC = 1 - C

    XS = X * S
    YS = Y * S
    ZS = Z * S

    XxY = X * Y
    XxZ = X * Z
    YxZ = Y * Z

    # Creating the final rotation matrix
    mR = np.zeros((3,3))

    mR[0][0] = X * X * OmC + C
    mR[0][1] = XxY * OmC - ZS
    mR[0][2] = XxZ * OmC + YS
    mR[1][0] = XxY * OmC + ZS
    mR[1][1] = Y * Y * OmC + C
    mR[1][2] = YxZ * OmC - XS
    mR[2][0] = XxZ * OmC - YS
    mR[2][1] = YxZ * OmC + XS
    mR[2][2] = Z * Z * OmC + C

    return mR


<<<<<<< HEAD
#def calcul_matrice_translation(v):
=======
def calcul_matrice_translation(v):
>>>>>>> origin/main
