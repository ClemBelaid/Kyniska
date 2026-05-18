from .mire import Mire
from .observation import Observation
import cv2 
import numpy as np

def estimate_camera(points3d, points2d):
    """
    Entrée :
    Sortie : 
    """
    # Dummy camera intrinsics (replace with real ones)
    K = np.eye(3)

    # Making sure the arrays are in the right format expected by cv2
    points3d = np.asarray(points3d, dtype=np.float32)
    points2d = np.asarray(points2d, dtype=np.float32)

    # Rvec = Rotation vector, tvec = translation vector
    success, rvec, tvec = cv2.solvePnP(points3d, points2d, K, None)
    return success, rvec, tvec


def validate_camera(points3d, points2d, rvec, tvec):
    """
    Entrée :
    Sortie :
    """
    # Reproject and compute error
    points3d = np.asarray(points3d, dtype=np.float32)
    projected, _ = cv2.projectPoints(points3d, rvec, tvec, np.eye(3), None)
    projected = projected.squeeze()
    chercher_points_correspondants(projected, points2d)