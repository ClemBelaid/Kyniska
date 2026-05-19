from .mire import Mire
import numpy as np

"""def generer_cone_tronque(nb_billes, ids=None, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0):
    points = []
    for _ in range(nb_billes):

        z = np.random.uniform(0, hauteur)

        rayon_max_z = rayon_base + (z / hauteur) * (rayon_sommet - rayon_base)
        r = rayon_max_z * np.sqrt(np.random.uniform(0, 1))
        theta = np.random.uniform(0, 2 * np.pi)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        points.append([x, y, z])
    data_dict = {i: p for i, p in enumerate(points)}
    points = list(data_dict.values())
    ids = list(data_dict.keys())
    return Mire(points,ids=ids)

def generer_cone_tronque_creux(nb_billes, ids=None, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0):
    points = []
    for _ in range(nb_billes):
        z = np.random.uniform(0, hauteur)
        r = rayon_base + (z / hauteur) * (rayon_sommet - rayon_base)
        theta = np.random.uniform(0, 2 * np.pi)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        points.append([x, y, z])

    data_dict = {i: p for i, p in enumerate(points)}
    return Mire(data_dict, ids=ids)

def generer_cube(nb_billes, ids=None, largeur=200.0, longueur=200.0, epaisseur=30.0):
    points = []

    for _ in range(nb_billes):
        x = np.random.uniform(-largeur / 2, largeur / 2)
        y = np.random.uniform(-longueur / 2, longueur / 2)
        z = np.random.uniform(0, epaisseur)

        points.append([x, y, z])
    data_dict = {i: p for i, p in enumerate(points)}
    points = list(data_dict.values())
    ids = list(data_dict.keys())
    return Mire(points,ids=ids)"""
def generer_cone_tronque(nb_billes, ids=None,
                         rayon_base=100.0,
                         rayon_sommet=50.0,
                         hauteur=30.0):

    points = []

    for _ in range(nb_billes):

        z = np.random.uniform(0, hauteur)

        # surface du cône (PAS volume)
        t = np.random.uniform(0, 1)

        r = (1 - t) * rayon_base + t * rayon_sommet

        theta = np.random.uniform(0, 2*np.pi)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        points.append([x, y, z])

    data_dict = {i: p for i, p in enumerate(points)}
    ids = list(data_dict.keys())
    points = list(data_dict.values())

    return Mire(points, ids=ids)

def generer_cone_tronque_creux(nb_billes, ids=None,
                               rayon_base=100.0,
                               rayon_sommet=50.0,
                               hauteur=30.0):

    points = []

    for _ in range(nb_billes):

        z = np.random.uniform(0, hauteur)

        t = z / hauteur

        r = (1 - t) * rayon_base + t * rayon_sommet

        theta = np.random.uniform(0, 2*np.pi)

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        points.append([x, y, z])

    data_dict = {i: p for i, p in enumerate(points)}
    ids = list(data_dict.keys())
    points = list(data_dict.values())

    return Mire(points, ids=ids)

def generer_cube(nb_billes, ids=None,
                 largeur=200.0,
                 longueur=200.0,
                 epaisseur=30.0):

    points = []

    # on force une structure régulière + bruit léger
    for _ in range(nb_billes):

        # base quasi-grille
        x = np.random.choice(np.linspace(-largeur/2, largeur/2, int(np.sqrt(nb_billes))))
        y = np.random.choice(np.linspace(-longueur/2, longueur/2, int(np.sqrt(nb_billes))))

        z = np.random.uniform(0, epaisseur)

        # petit bruit pour éviter dégénérescence
        x += np.random.normal(0, 0.5)
        y += np.random.normal(0, 0.5)

        points.append([x, y, z])

    data_dict = {i: p for i, p in enumerate(points)}
    ids = list(data_dict.keys())
    points = list(data_dict.values())

    return Mire(points, ids=ids)
    
