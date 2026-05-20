#from .mire import Mire
#from .observation import Observation
from math import *

import numpy as np
import itertools


def calcul_matrice_rotation(v, angle):
    """
    Entrée : Un vecteur v qui correspond à l axe de rotation, et un angle en radians 
    Sortie : La matrice de rotation correspondante (selon la formule de Rodrigues)
    """
    v = np.array(v, dtype=float)
    vNorm = np.linalg.norm(v)
    if vNorm < 1e-6:
        raise ValueError("Rotation axis too small")

    X = v[0] / vNorm
    Y = v[1] / vNorm 
    Z = v[2] / vNorm

    C = np.cos(angle)
    S = np.sin(angle)
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


def calcul_matrice_translation(v):
    return 0

def calcul_matrice_pose(rmat, tmat):
    """
    Entrée : Les matrices de rotation et de translation (sous forme de numpy array)
    Sortie : La matrice de pose reconstruite
    """
    n = len(tmat) # 2 ou 3
    pose = np.identity(n+1)
    pose[0:n, 0:n] = rmat
    pose[0:n, n] = tmat
    
    return pose
