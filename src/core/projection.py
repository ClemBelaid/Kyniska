import numpy as np
from .geometry import perpendicular_vector
from .observation import Observation

def project_mire_to_plane(mire, v):
    """
    Projette une mire 3D sur un plan et renvoie une Observation indexée.
    """

    n = len(mire.points)

    d = 0
    if (v[2] == 0):
        if(v[0] == 0):
            xx, zz = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
            yy = 0
        else:
            yy = np.meshgrid(np.linspace(0,1,20))
            xx = -v[1]*yy/v[0]
    else:
        xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
        zz = (-v[0] * xx - v[1] * yy - d) * 1. / v[2]

    u1 = perpendicular_vector(v)
    u2 = np.cross(v, u1)

    observ = {}
    observ_anonym={}

    for i, (pid, pt) in enumerate(mire.data.items()):
        u = np.array(pt)

        u_prime = np.dot(u,v)/np.dot(v,v)*v
        w = u - u_prime
        observ[pid]=(np.dot(u1, w), np.dot(u2,w))
        fake_id = -(i+1)
        observ_anonym[fake_id]=(np.dot(u1, w), np.dot(u2,w))
      

    return (Observation(observ,v=v),Observation(observ_anonym,v=v))

def chercher_correspond_points(p1,p2):
    """Entrées: 2 projections p1 et P2 : p1 la projection originale que l'on connait 
       p2 la projection obtenue en appliquant la rotation sur la mire 
       Sorties: Ratio de points correspondants (pour le moment)
       """
    eps = 1e-3
    score = 0
    for pt1 in p1.points:
        for pt2 in p2.points:
            d = np.linalg.norm(pt2 - pt1)
            if d < eps:
                score += 1 
    return score            
    
               
