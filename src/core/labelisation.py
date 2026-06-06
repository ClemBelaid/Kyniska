import numpy as np
from scipy.spatial.distance import cdist
from .mire import Mire
from .observation import Observation

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


def taux_labels_corrects(labels):
    taux = 0
    for x in labels.keys():
        if labels[x] == x :
            taux += 1
    return taux/len(labels)
