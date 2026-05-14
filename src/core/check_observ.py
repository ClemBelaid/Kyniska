import numpy as np
from .observation import Observation 



def check_observ(obs_v , obs_sim):
    """Entrées: obs_v l'observation réelle et obs_pr l'observation à tester
       Sorties: le ratio de points qui correspondent à peu près """
    ids_communs = set(obs_v.ids) & set(obs_sim.ids)
    erreurs = []
    for i in ids_communs:

        p_ref = np.array(obs_v.pts[i])
        p_sim = np.array(obs_sim.pts[i])

        d = np.linalg.norm(p_ref - p_sim)

        erreurs.append(d)
    rms = np.sqrt(np.mean(np.array(erreurs)**2)) #root mean square (racine de la moyenne des carrés)
    return rms 