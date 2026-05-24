import cv2 
import numpy as np
from scipy.spatial.distance import cdist

from .mire import Mire
from .observation import Observation

def estimate_camera(points3d, points2d):
    """
    Estime la position et l'orientation de la caméra via OpenCV (solvePnP).
    """
    # Dummy camera intrinsics (à remplacer par les vrais un jour)
    K = np.eye(3)

    # Conversion dans le bon format pour OpenCV
    points3d = np.asarray(points3d, dtype=np.float32)
    points2d = np.asarray(points2d, dtype=np.float32)

    # Rvec = Rotation vector, tvec = translation vector
    success, rvec, tvec = cv2.solvePnP(points3d, points2d, K, None)
    
    return success, rvec, tvec


def labeliser_points(points_projetes: np.ndarray, points_observes: list) -> dict:
    """
    Associe chaque point projeté (virtuel) à l'observation (réelle) la plus proche.
    """
    labels = {}
    
    # 1. Calcul de toutes les distances d'un coup avec scipy
    distances = cdist(points_projetes, points_observes)
    
    # 2. Association au plus proche
    for i in range(len(points_projetes)):
        index_plus_proche = int(np.argmin(distances[i]))
        labels[i] = index_plus_proche
        
    return labels


def validate_camera(points3d, points2d, rvec, tvec):
    """
    Vérifie le calcul en reprojetant les points et génère le dictionnaire de correspondances.
    """
    # Reprojection des points 3D sur le capteur 2D
    points3d = np.asarray(points3d, dtype=np.float32)
    projected, _ = cv2.projectPoints(points3d, rvec, tvec, np.eye(3), None)
    projected = projected.squeeze()
    
    #
    #On utilise la fonction pour créer le dictionnaire final
    correspondances = labeliser_points(projected, points2d)
    
    return correspondances