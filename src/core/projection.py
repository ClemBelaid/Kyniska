import numpy as np
from src.core.geometry import perpendicular_vector
from src.core.observation import Observation


def project_pt_to_plane(pt, screen):
    """
    Projection orthogonale d'un point 3D sur le plan écran.
    Retourne les coordonnées 2D dans la base écran.
    """

    vn = screen["normal"]
    u1 = screen["u1"]
    u2 = screen["u2"]
    origin = screen["origin"]

    pt = np.array(pt)

    # vecteur depuis l'origine du plan
    vec = pt - origin

    # composante normale
    proj_normal = np.dot(vec, vn) / np.dot(vn, vn) * vn

    # projection orthogonale 3D sur le plan
    proj3d = pt - proj_normal

    # coordonnées écran
    x = np.dot(proj3d - origin, u1)
    y = np.dot(proj3d - origin, u2)

    return np.array([x, y])
        
def project_mire_to_plane(mire, screen):
    """
    Projette une mire 3D sur le plan écran
    et renvoie une Observation indexée.
    """

    vn = screen["normal"]
    u1 = screen["u1"]
    u2 = screen["u2"]
    origin = screen["origin"]

    observ = {}

    for pid, pt in mire.pts.items():

        pt = np.array(pt)

        # vecteur depuis l'origine du plan
        vec = pt - origin

        # composante normale
        proj_normal = np.dot(vec, vn) / np.dot(vn, vn) * vn

        # projection 3D sur le plan
        proj3d = pt - proj_normal

        # coordonnées 2D dans la base écran
        x = np.dot(proj3d - origin, u1)
        y = np.dot(proj3d - origin, u2)

        observ[pid] = (x, y)

    points = list(observ.values())
    ids = list(observ.keys())

    return Observation(points, ids=ids, v=vn)


      



       
    
               

