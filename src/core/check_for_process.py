import numpy as np
import random
import itertools
from src.core.observation import Observation 
from src.core.mire import Mire
from src.core.projection import project_pt_to_plane

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
    """ Remarque : éventuellement cette fonction sera supprimée pour être intégrée directement dans la grosse boucle for
    qui englobera tout le processus (on itère ce processus sur chaque couple de billes de la mire)"""

    # Distance des points "témoins" y0 et x0
    d_obs = np.linalg.norm(np.array(yo - xo))

    if np.linalg.norm(yo - xo) < 1e-8: # Erreur sur y0 et x0
        return None

    for (id1,id2) in itertools.combinations(mire.ids.tolist(), 2):
        xm = np.array(mire.pts[id1])
        ym = np.array(mire.pts[id2])
        dm = np.linalg.norm(ym - xm)
        if dm < d_obs:
            continue
        else:
            break

    return (xm,ym)