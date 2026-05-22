from .mire import Mire
from .observation import Observation
from .transformation import *
import numpy as np
import itertools

def find_2points(m, p):
    """
    Entrée : Une mire 3D m, une projection 2D p
    Sortie : Deux points A et B de la mire
    """
    # On sélectionne deux points au hasard de la projection 
    a = p.points[0]
    b = p.points[1]
    dist = np.linalg.norm(a, b)

    for comb in itertools.combinations(m.points, 2):
        (u,v) = comb
        # Axe de rotation défini dans le référentiel mire
        axe = v - u 
        hypothenuse = np.linalg.norm(axe)
        if hypothenuse < dist:
            continue
        for ang in range(360):
            # Il faut écrire une fonction de rotation pour la mire prenant en paramètres un angle et un axe
            mR = calcul_matrice_rotation(axe, ang)

            # On reprojette selon le vecteur v de la projection p
            # On vérifie tous les points (méthode des moindres carrés)
            # Il faut que la nouvelle projection p' et la projection p se "superposent" bien
            # Ie pour chaque point (identifié) de p', s'il y a un point (non-identifié) de p "pas très loin"
            # (dans un cercle de rayon epsilon), alors on dit que ce point p correspond au point p' : ça donne l'identification

