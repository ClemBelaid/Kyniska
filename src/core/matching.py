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


def correspondance_projection_mire(m, p, l, epsilon):
    """
    Entrée : Une mire m, une projection p, une liste l des birapports de la mire, un critère de tolérance epsilon
    Sortie : Une liste des quadruplets de points alignés *potentiellement identifiés* dans p
    """
    # On calcule les quadruplets de points alignés dans chaque projection
    # Enregistrés sous leurs coordonnées (x,y)
    p_alignes = detecter_quadruple_alignes_observation(p, 4)[1]

    #p_ids = []

    for q in p_alignes:
        (a,b,c,d) = q
        n = calculBirapport(a,b,c,d)
        # Si le birapport fait partie des birapports connus de la mire (à epsilon près)
        for i in range(len(l)):
            if abs(n - l[i]) <= epsilon :
                # On enregistre ce quadruplet : leurs IDs d'abord puis leurs coordonnées dans p1
                p.ids.append(m.alignes[i])


# Si on part du principe que tous les points de la mire appartiennent à un quadruplet de points alignés
def annoter_birapport(m, p1, p2, p3, epsilon = 0.01):
    """
    Entrée : Une mire m, trois projections différentes p1, p2, p3 et un critère de tolérance epsilon
    Sortie : Pour chaque projection, une liste des quadruplets alignés identifiés par leur birapport,
    et une liste des coordonnées 2D correspondantes dans la projection
    """

    # Calcul des birapports de la mire
    listeBR = []
    for q in m.alignes:
        (ida,idb,idc,idd) = q
        (a,b,c,d) = (m.points[ida], m.points[idb], m.points[idc], m.points[idd])
        listeBR.append(calculBirapport(a,b,c,d))

    correspondance_projection_mire(m, p1, listeBR, epsilon)
    correspondance_projection_mire(m, p2, listeBR, epsilon)
    correspondance_projection_mire(m, p3, listeBR, epsilon)

    # Ajouter une façon de ne garder que ceux qui sont à la fois dans p1_ids, p2_ids et p3_ids (intersection) !!