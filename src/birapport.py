from mire import Mire
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