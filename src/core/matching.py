from .mire import Mire
from .observation import Observation
from .geometry import calculBirapport
import numpy as np
import itertools

def detecter_quadruple_alignes_observation(obs: Observation, eps=0):
    """
    Fonction détectant et inscrivant un quadruplet de billes alignées
    dans une observation.

    Args:
        obs : une observation de la classe Observation
        eps : seuil de tolérance, 0 pour exact

    Returns:
        (int, array-like) : nombre de quadruplets détectés
        + liste des 4-uplets d'identifiants
    """
    n = len(obs.points)
    points = np.asarray(obs.points)

    nb_4uplets = 0
    liste_4uplets = []

    for i in range(n):
        for j in range(i + 1, n):

            pi, pj = points[i], points[j]
            alignes = [pi, pj]

            for k in range(j + 1, n):
                pk = points[k]

                u = pj - pi
                v = pk - pi

                if abs(u[0] * v[1] - u[1] * v[0]) <= eps:
                    alignes.append(pk)

            if len(alignes) >= 4:
                nb_4uplets += 1
                liste_4uplets.append(tuple(alignes[:4]))

    return nb_4uplets, liste_4uplets


def identification(m, p1, p2, p3, epsilon = 0.01):
    """
    Entrée : une mire m, trois projections différentes p1, p2, p3
    Sortie : Identification des points 2D de chaque projection en les associant à leurs IDs
    """
    listeBR = []

    for q in m.alignes:
        (ida,idb,idc,idd) = q
        (a,b,c,d) = (m.points[ida], m.points[idb], m.points[idc], m.points[idd])
        listeBR.append(calculBirapport(a,b,c,d))

    print("listeBR = ", listeBR)

    p1_alignes = detecter_quadruple_alignes_observation(p1, 4)[1]
    p2_alignes = detecter_quadruple_alignes_observation(p2, 4)[1]
    p3_alignes = detecter_quadruple_alignes_observation(p3, 4)[1]

    p_ids_candidats = []
    p_ids1 = []
    p_ids2 = []

    for q in p1_alignes:
        (a,b,c,d) = q
        print("p1")
        print(a,b,c,d)
        n = calculBirapport(a,b,c,d)
        print("birapport = ", n)
        for i in range(len(listeBR)):
            if abs(n - listeBR[i]) <= epsilon :
                candidat = m.alignes[i]
                print("candidat =", candidat)
                p_ids_candidats.append(candidat)

    for q in p2_alignes:
        (a,b,c,d) = q
        print("p2")
        print(a,b,c,d)
        n = calculBirapport(a,b,c,d)
        print("birapport = ", n)
        for i in range(len(listeBR)):
            if abs(n - listeBR[i]) <= epsilon :
                candidat = m.alignes[i]
                print("candidat =", candidat)
                if np.any(np.all(candidat == p_ids_candidats, axis=1)):
                    p_ids.append(candidat)
                else:
                    p_ids_candidats.append(candidat)

    return p_ids
