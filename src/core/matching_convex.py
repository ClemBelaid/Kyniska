from .mire import Mire
from scipy.spatial import ConvexHull
from .observation import Observation
import cv2 
import numpy as np
import itertools

def enveloppe_convexe_3D(m):
    """
    Entrée : Une mire 3D 
    Sortie : Les identifiants des points de l'enveloppe convexe 3D de cette mire
    """
    convexHull = ConvexHull(m.points)
    # Les sommets (vertices) de convexHull sont renommées "dans l'ordre d'apparition"
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
    Sortie : Les identifications des points de l'enveloppe convexe 2D de cette observation
    """
    convexHull = ConvexHull(o.points)
    ids = []
    for index in convexHull.vertices :
        pt = o.points[index]
        pid = o.getID(pt)
        ids.append(pid)
    return ids

def cyclic_permutations(lst):
    """
    Entrée : Une liste de points 3D ou 2D
    Sortie : La liste de toutes les permutations cycliques de cet ensemble de points
    """
    n = len(lst)
    return [lst[i:] + lst[:i] for i in range(n)]

def circuits_candidats(m, p):
    """
    Entrée : 
    Sortie :
    """
    convHull3D = enveloppe_convexe_3D(m)
    convHull2D = enveloppe_convexe_2D(p)
    n = len(convHull2D)
    candidats = []
    # Pour chaque circuit de taille n dans l'enveloppe convexe 3D
    for circuit in itertools.combinations(convHull3D, n):
        # On calcule toutes les permutations cycliques de ce circuit et on les ajoute aux candidats
        candidats.extend(cyclic_permutations(circuit))
    return candidats
    

# A retravailler
def estimate_camera(pts3D, pts2D):
    """
    Entrée :
    Sortie :
    """
    # Dummy camera intrinsics (replace with real ones)
    K = np.eye(3)
    success, rvec, tvec = cv2.solvePnP(pts3D, pts2D, K, None)
    return success, rvec, tvec

# A retravailler
def identification(m, p):
    """
    Entrée :
    Sortie :
    """
    candidats = circuits_candidats(m, p)
    points2D = p.points
    best_match = None
    best_error = float('inf')

    # Le tableau candidats contient une liste des circuits de l'enveloppe convexe 3D correspondant *potentiellement*
    # A l'enveloppe convexe 2D projetée
    for match in candidats:
        success, rvec, tvec = estimate_camera(match, points2D)
        
        if not success:
            continue

        # Reproject and compute error
        projected, _ = cv2.projectPoints(match, rvec, tvec, np.eye(3), None)
        projected = projected.squeeze()

        error = np.linalg.norm(projected - points2D)

        if error < best_error:
            best_error = error
            best_match = match
    
    return best_match, best_error