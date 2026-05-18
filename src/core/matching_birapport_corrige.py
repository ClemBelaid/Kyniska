from .mire import Mire
from .observation import Observation
from .geometry import calculBirapport
import numpy as np
import itertools

def detecter_quadruple_alignes_observation(obs: Observation, eps=0.5):
    """
    Détecte les quadruplets de billes alignées en utilisant le format dictionnaire.
    
    Points clés de cette version :
    -Mapping ID/Coordonnées : Préserve l'identité des billes.
    -Tri Spatial : Indispensable pour l'invariance du birapport.
    -Robustesse : Seuil de tolérance (eps) pour absorber le bruit de détection.
    """
    #préparation des données (on travaille en vecteurs numpy)
    items = [(id_bille, np.array(pos)) for id_bille, pos in obs.points.items()]
    n = len(items)
    
    quadruplets_valides = []

    # 2 explorons toutes les paires (i, j) pour définir les droites candidates
    #utiliser combinations est plus propre que deux boucles for range...
    for (i, (id_i, pi)), (j, (id_j, pj)) in itertools.combinations(enumerate(items), 2):
        
        # Vecteur directeur de la droite définie par pi et pj
        u = pj - pi
        norm_u = np.linalg.norm(u)
        
        if norm_u < 1e-6: continue #Sécurité : points superposés

        #On cherche d'autres points sur cette droite
        #On initialise avec les deux points pivots
        alignes = [(id_i, pi), (id_j, pj)]
        
        for k, (id_k, pk) in enumerate(items):
            if k == i or k == j:
                continue
            
            v = pk - pi
            #Aire du parallélogramme (produit en croix)
            #On normalise par la distance pour que 'eps' soit cohérent en pixels
            dist_droite = abs(u[0] * v[1] - u[1] * v[0]) / norm_u
            
            if dist_droite <= eps:
                alignes.append((id_k, pk))

        # 3. Validation et stabilisation
        if len(alignes) >= 4:

            #On trie TOUJOURS par X (ou Y si vertical) pour garantir un ordre constant
            #C'est ce qui rend le matching de birapport possible plus tard
            alignes.sort(key=lambda x: (x[1][0], x[1][1]))
            
            #On génère des quadruplets uniques (4 parmi N si plus de 4 points sont alignés)
            for quad in itertools.combinations(alignes, 4):
                ids_quad = tuple(item[0] for item in quad)
                
                if ids_quad not in quadruplets_valides:
                    quadruplets_valides.append(ids_quad)

    return len(quadruplets_valides), quadruplets_valides

def correspondance_projection_mire(m, p, l, epsilon):
    """
    Identifie les quadruplets dans p en comparant leurs birapports à la liste l.
    """
    #On récupère la liste des IDs détectés
    p_alignes_ids = detecter_quadruple_alignes_observation(p, epsilon)[1]

    for q_ids in p_alignes_ids:
        #récupérons des coordonnées via les IDs pour le calcul
        pts = [p.points[i] for i in q_ids]
        n = calculBirapport(*pts)
        
        for i in range(len(l)):
            if abs(n - l[i]) <= epsilon :
                # On enregistre l'ID correspondant de la mire
                p.ids.append(m.alignes[i])

def annoter_birapport(m, p1, p2, p3, epsilon = 0.01):
    """
    Calcule les birapports de la mire et synchronise les 3 projections...
    """
    #calcul des birapports de la mire
    listeBR = []
    for q in m.alignes:
        ida, idb, idc, idd = q
        a, b, c, d = m.points[ida], m.points[idb], m.points[idc], m.points[idd]
        listeBR.append(calculBirapport(a,b,c,d))

    #Identification par projection
    correspondance_projection_mire(m, p1, listeBR, epsilon)
    correspondance_projection_mire(m, p2, listeBR, epsilon)
    correspondance_projection_mire(m, p3, listeBR, epsilon)

    #Intersection : on ne garde que les quadruplets validés par les 3 vues.!
    communs = list(set(p1.ids) & set(p2.ids) & set(p3.ids))
    p1.ids, p2.ids, p3.ids = communs, communs, communs