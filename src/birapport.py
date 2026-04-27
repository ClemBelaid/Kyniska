from src.mire import Mire
from src.observation import Observation
import numpy as np
import itertools

# Gérer le cas où nc = nb ou bien nd = nb (division par zéro)
def calculBirapport(a, b, c, d):
    """
    Entrée : points en 3D
    Sortie : birapport (a,b,c,d)
    """
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    nc = np.linalg.norm(c)
    nd = np.linalg.norm(d)
    return (nc-na)/(nc-nb)*(nd-na)/(nd-nb) 

def detecter_quadruple_alignes_observation(obs: Observation, nb=4):
    """
    Fonction detectant et inscrivant un quadruler de billes alignees dans une observation.
    Args:
        obs : une observation de la classe Observation
        nb : nombre de bille alignee a detecter pour la generalisation ca ne mange pas de pains.
    Returns:
        (int, (Array like)) : nombre de quaddruplet detecter + liste des 4-uplet de ids
    """

# Supposons que l'objet mire contient une liste des points *alignés* qui sont donc CONNUS à l'avance !!
# Avec des birapports DIFFERENTS (sinon aucun intérêt !!)
# Par exemple : [(0,1,2,3), (4,5,6,7)]
def identification(m, p1, p2, p3, epsilon = 0):
    """
    Entrée : une mire m, trois projections différentes p1, p2, p3
    Sortie : Identification des points 2D de chaque projection en les associant à leurs IDs
    """
    listeBR = [] # Liste des birapports de la mire

    for q in m.alignes:
        (ida,idb,idc,idd) = q
        (a,b,c,d) = (m.points[ida], m.points[idb], m.points[idc], m.points[idd])
        listeBR.append(calculBirapport(a,b,c,d))

    p1_alignes = detecter_quadruple_alignes_observation(p1, 4)
    #p2_alignes = detecter_quadruple_alignes_observation(p2, 4)
    #p3_alignes = []

    p_ids = []

    for q in p1_alignes:
        (a,b,c,d) = q
        n = calculBirapport(a,b,c,d)
        for i in range(len(listeBR)):
            if abs(n - listeBR[i]) <= epsilon :
                (ida, idb, idc, idd) = m.alignes(i)
                p_ids.extend(([ida, a], [idb, b], [idc, c], [idd, d])) 
    
    return p_ids
