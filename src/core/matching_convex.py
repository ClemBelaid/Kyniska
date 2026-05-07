from .mire import Mire
from scipy.spatial import ConvexHull
from .observation import Observation
import numpy as np
import itertools

def enveloppe_convexe_3D(m):
    """
    Entree : Une mire 3D 
    Sortie :
    """
    convexHull = ConvexHull(m.points)
    ids = []
    for pt in convexHull.points :
        pid = m.getID(pt)
        ids.append(pid)
    return ids

def enveloppe_convexe_2D(p):
    """
    """
    return ConvexHull(p.points).vertices
