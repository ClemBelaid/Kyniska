from .mire import Mire
from .observation import Observation
from .geometry import calculBirapport
import numpy as np
import itertools

import itertools
import numpy as np

def detecter_quadruplets_alignes(obs, eps=1e-6):
    """
    Fonction détectant et inscrivant un quadruplet de billes alignées
    dans une observation.

    Args:
        obs : une observation de la classe Observation
        eps : seuil de tolérance, 0 pour exact

    Returns:
       
    """

    data = list(zip(obs.ids, obs.points))

    quadruplets = []

    for quad in itertools.combinations(data, 4):

        (id1, p1), (id2, p2), (id3, p3), (id4, p4) = quad

        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)
        p4 = np.array(p4)

        u = p2 - p1
        v = p3 - p1
        w = p4 - p1

        det1 = abs(u[0]*v[1] - u[1]*v[0])
        det2 = abs(u[0]*w[1] - u[1]*w[0])

        if det1 <= eps and det2 <= eps:
            quadruplets.append((id1, id2, id3, id4))

    return quadruplets
 


def appliquer_correspondances(obs, correspondances):

    new_pts = {}

    for corr in correspondances:

        quad_proj = corr["projection"]
        quad_mire = corr["mire"]

        for pt_proj, vrai_id in zip(quad_proj, quad_mire):

            # retrouver l'id du point projeté
            for fake_id, coords in obs.pts.items():

                if np.allclose(coords, pt_proj):

                    new_pts[vrai_id] = coords

    ids = list(new_pts.keys())
    points = list(new_pts.values())

    return Observation(points, ids=ids, v=obs.v)

def correspondance_projection_mire(m, p, l, epsilon):

    p_alignes = detecter_quadruple_alignes_observation(p, 4)[1]

    correspondances = []

    for q in p_alignes:

        (a,b,c,d) = q

        n = calculBirapport(a,b,c,d)

        for i in range(len(l)):

            if abs(n - l[i]) <= epsilon:

                correspondances.append({
                    "projection": q,
                    "mire": m.alignes[i]
                })

    return correspondances

# Si on part du principe que tous les points de la mire appartiennent à un quadruplet de points alignés
def annoter_birapport(m, p1, p2, p3, epsilon=0.01):

    listeBR = []

    for (ida,idb,idc,idd) in m.alignes:

        a = m.pts[ida]
        b = m.pts[idb]
        c = m.pts[idc]
        d = m.pts[idd]

        br = calculBirapport(a,b,c,d)

        listeBR.append(br)

    map1 = correspondance_projection_mire(
        m, p1, listeBR, epsilon
    )

    map2 = correspondance_projection_mire(
        m, p2, listeBR, epsilon
    )

    map3 = correspondance_projection_mire(
        m, p3, listeBR, epsilon
    )

    return map1, map2, map3

    # Ajouter une façon de ne garder que ceux qui sont à la fois dans p1_ids, p2_ids et p3_ids (intersection) !!