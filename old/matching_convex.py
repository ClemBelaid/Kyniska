from .src.core.mire import Mire
from scipy.spatial import ConvexHull
from .src.core.observation import Observation
import cv2 
import numpy as np
import itertools

def enveloppe_convexe_3D(m):
    """
    Entrée : Une mire 3D 
    Sortie : Les identifiants des points de l'enveloppe convexe 3D de cette mire
    """
    convexHull = ConvexHull(m.points)
    # Les sommets (vertices) de convexHull sont renommés "dans l'ordre d'apparition"
    # Ils ne correspondent pas aux identifiants que l'on a nous-mêmes définis dans la mire
    ids = []
    for index in convexHull.vertices :
        pt = m.points[index]
        pid = m.getID(pt)
        ids.append(pid)
    return ids

def enveloppe_convexe_2D(o):
    """
    Entrée : Une observation 2D
    Sortie : Les identifiants des points de l'enveloppe convexe 2D de cette observation
    """
    convexHull = ConvexHull(o.points)
    # Les sommets (vertices) de convexHull sont renommés "dans l'ordre d'apparition"
    # Ils ne correspondent pas aux identifiants que l'on a nous-mêmes définis dans la mire
    ids = []
    for index in convexHull.vertices :
        pt = o.points[index]
        pid = o.getID(pt)
        ids.append(pid)
    return ConvexHull(o.points).vertices


def generer_circuits_candidats(mire_3d, obs_2d):
    #obtenir la longueur m de l'enveloppe 2D
    indices_2d = enveloppe_convexe_2D(obs_2d)
    m = len(indices_2d)

    #Construire le graphe d'adjacence 3D (qui est relié à qui sur la 'coque')
    hull3d = ConvexHull(mire_3d.points)
    adj = {i: set() for i in range(len(mire_3d.points))}
    for simplex in hull3d.simplices: #hull3d.simplices contient les faces (triangles)
        for i in range(3):
            u, v = simplex[i], simplex[(i+1)%3]
            adj[u].add(v)
            adj[v].add(u)

    #Trouver tous les circuits de longueur m via un parcour
    circuits_valides = []
    
    def dfs(start_node, current_path):
        if len(current_path) == m:
            #si le dernier point est relié au premier, le circuit est bouclé
            if start_node in adj[current_path[-1]]:
                circuits_valides.append(current_path)
            return

        for voisin in adj[current_path[-1]]:
            if voisin not in current_path:
                dfs(start_node, current_path + [voisin])

    #lancer la recherche depuis chaque point de l'enveloppe 3D
    indices_3d_hull = hull3d.vertices
    for start_node in indices_3d_hull:
        dfs(start_node, [start_node])

    #Pour chaque circuit, générer les 2m appariements (rotations + inversion)
    tous_les_candidats = []
    for circuit in circuits_valides:
        for i in range(m):
            rotation = np.roll(circuit, i).tolist()
            tous_les_candidats.append(rotation)          #sens horaire
            tous_les_candidats.append(rotation[::-1])    #sens anti-horaire
            
    return tous_les_candidats