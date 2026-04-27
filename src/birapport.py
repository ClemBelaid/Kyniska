from mire import Mire
from observation import Observation
import numpy as np
import itertools
#from observation import Observation ---> Une fois que la classe Observation sera créée

# Entrée : points en 3D
# Sortie : birapport (a,b,c,d)
# Gérer le cas où nc = nb ou bien nd = nb (division par zéro)
def calculBirapport(a, b, c, d):
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    nc = np.linalg.norm(c)
    nd = np.linalg.norm(d)
    return (nc-na)/(nc-nb)*(nd-na)/(nd-nb) 

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
    n = len(obs.points2d)
    points = np.asarray(obs.points2d)

    nb_4uplets = 0
    liste_4uplets = []

    for i in range(n):
        for j in range(i + 1, n):

            pi, pj = points[i], points[j]
            alignes = [i, j]

            for k in range(j + 1, n):
                pk = points[k]

                # nb : on ne s'embête pas avec les sqrt,
                # les normes sont au carré
                u = pj - pi
                v = pk - pi

                # produit vectoriel 2D nul <=> alignement
                if abs(u[0] * v[1] - u[1] * v[0]) <= eps:
                    alignes.append(k)

            if len(alignes) >= 4:
                nb_4uplets += 1
                liste_4uplets.append(tuple(alignes[:4]))

    return nb_4uplets, liste_4uplets


# Supposons que l'objet mire contient une liste des points *alignés* qui sont donc CONNUS à l'avance !!
# Avec des birapports DIFFERENTS (sinon aucun intérêt !!)
# Par exemple : [(0,1,2,3), (4,5,6,7)]
def identification(m, p1, p2, p3):
    """
    Entrée : une mire m, trois projections différentes p1, p2, p3
    Sortie : Identification des points 2D de chaque projection en les associant à leurs IDs
    """
    listeBR = [] # Liste des birapports

    p1_ids = []

    for q in m.alignes:
        # Comment récupérer les points quand on a la liste des IDs ?
        (ida,idb,idc,idd) = q
        (a,b,c,d) = (m.points[ida], m.points[idb], m.points[idc], m.points[idd])
        listeBR.append(calculBirapport(a,b,c,d))

    p1_alignes = []
    # Détecter les points alignés de la projection p1 !!
    # Sinon ça n'a pas de sens de calculer un birapport sur des points non-alignés
    # Donc pas besoin de faire de la combinatoire sur tous les points de p1

    for q in p1_alignes:
        (a,b,c,d) = q
        n = calculBirapport(a,b,c,d)
        for i in range(len(listeBR)):
            if(n == listeBR[i]): # On a trouvé un birapport qui correspond
                (ida, idb, idc, idd) = m.alignes[i] # On récupère le quadruplet d'IDs ayant un tel birapport
                # Essayer d'écrire ces 4 lignes en une seule (code + propre)
                p1_ids.append([int(ida), a])
                p1_ids.append([int(idb), b])
                p1_ids.append([int(idc), c])
                p1_ids.append([int(idd), d])
    
    return p1_ids
