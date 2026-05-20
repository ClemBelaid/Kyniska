import numpy as np
import random
from .observation import Observation 
from .mire import Mire
from .projection import project_pt_to_plane


def check_observ(obs_v, obs_sim):
    """
    Compare deux observations et retourne le RMS des distances
    entre les points ayant les mêmes IDs.
    """

    ids_communs = set(obs_v.ids) & set(obs_sim.ids)

    if len(ids_communs) == 0:
        raise ValueError("No common IDs between observations")

    erreurs = []

    for i in ids_communs:

        p_ref = np.array(obs_v.pts[i])
        p_sim = np.array(obs_sim.pts[i])

        if p_ref.shape != p_sim.shape:
            raise ValueError(f"Incompatible shapes for point {i}")

        d2 = np.linalg.norm(p_ref - p_sim)**2

        erreurs.append(d2)

    rms = np.sqrt(np.mean(erreurs))

    return rms

def check_couple(mire,screen,xo,yo,lambda_):
    best_score = np.inf
    best_pair = None
    
    for _ in range(100):

        id1, id2 = random.sample(mire.ids, 2)

        xm = mire.pts[id1]
        ym = mire.pts[id2]

        xp = project_pt_to_plane(xm, screen["normal"])
        yp = project_pt_to_plane(ym, screen["normal"])

        d = np.linalg.norm(yp - xp)

        if d < 1e-8:
            continue

        d_obs = np.linalg.norm(yo - xo)
        if np.linalg.norm(yo - xo) < 1e-8:
            continue

        u_obs = (yo - xo) / np.linalg.norm(yo - xo)
        u_mire = (yp - xp) / np.linalg.norm(yp - xp)

        score = abs(d - d_obs) / d_obs - lambda_ * np.dot(u_mire, u_obs)

        if score < best_score:
            best_score = score
            best_pair = (id1, id2)
    id1, id2 = best_pair
    xm = mire.pts[id1]
    ym = mire.pts[id2]
    return (xm,ym)