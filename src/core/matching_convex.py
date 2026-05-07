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

# A retravailler
def estimate_camera(match):
    obj_pts = np.array([points_3d[i] for i, _ in match], dtype=np.float32)
    img_pts = np.array([points_2d[j] for _, j in match], dtype=np.float32)

    # Dummy camera intrinsics (replace with real ones)
    K = np.eye(3)

    success, rvec, tvec = cv2.solvePnP(obj_pts, img_pts, K, None)

    return success, rvec, tvec

best_match = None
best_error = float('inf')

# A retravailler
for match in candidates:
    success, rvec, tvec = estimate_camera(match)
    
    if not success:
        continue

    # Reproject and compute error
    obj_pts = np.array([points_3d[i] for i, _ in match], dtype=np.float32)
    img_pts = np.array([points_2d[j] for _, j in match], dtype=np.float32)

    projected, _ = cv2.projectPoints(obj_pts, rvec, tvec, np.eye(3), None)
    projected = projected.squeeze()

    error = np.linalg.norm(projected - img_pts)

    if error < best_error:
        best_error = error
        best_match = match