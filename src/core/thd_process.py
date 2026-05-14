import numpy as np 
from .transformation import calcul_matrice_rotation
from .mire import Mire 
from .projection import project_mire_to_plane
from .check_observ import check_observ


def thd_process(mire,v,obs,xm,ym,N):
    """Entrées: la mire qui a été fixée correctement,le vecteur normal au plan ,l'observation originale, 
    xm et ym qui sont sur notre axe de rotation N pour la discrétisation des angles """
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    ym_xm = ym - xm 
    eps = 1e-6
    for agl in angles:
        mR = calcul_matrice_rotation(ym_xm, agl)
        lst_pt = {}
        for id, x_mire in mire.pts.items():
            x_mire_homo = np.array(x_mire + [1])
            x_mire_trs_homo= mR @ x_mire_homo
            lst_pt[id] = (x_mire_trs_homo[:3] / x_mire_trs_homo[3]).tolist()
        points = list(lst_pt.values())
        ids = list(lst_pt.keys())
        new_mire = Mire(points, ids=ids, alignes=mire.alignes)
        observ = project_mire_to_plane(new_mire,v)
        rms = check_observ(obs,observ)
        if rms < eps :
            break 
            