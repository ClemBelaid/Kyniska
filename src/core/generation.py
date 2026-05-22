from src.core.mire import Mire
import numpy as np

def generer_cone_tronque(nb_billes, ids=None,
                         rayon_base=100.0,
                         rayon_sommet=50.0,
                         hauteur=180.0):

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
                               hauteur=200.0):

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

def generer_cube(nb_billes = 8, s = 30, ids=None,
                 largeur=200.0,
                 longueur=200.0,
                 epaisseur=150.0):

    # Pour l'instant je pars du principe qu'on a 8 billes (minimum)
    points = [(0,0,0), (s,0,0), (0,s,0), (0,0,s), (s,s,0),(s,0,s),(0,s,s), (s,s,s)]

    data_dict = {i: p for i, p in enumerate(points)}
    ids = list(data_dict.keys())
    points = list(data_dict.values())

    return Mire(points, ids=ids)
"""def generer_cube(
    nb_billes,
    ids=None,
    largeur=200.0,
    longueur=200.0,
    epaisseur=150.0
):

    points = []

    n = int(np.ceil(nb_billes ** (1/3)))

    xs = np.linspace(-largeur/2, largeur/2, n)
    ys = np.linspace(-longueur/2, longueur/2, n)
    zs = np.linspace(0, epaisseur, n)

    grille = []

    for x in xs:
        for y in ys:
            for z in zs:

                xb = x + np.random.normal(0, largeur*0.02)
                yb = y + np.random.normal(0, longueur*0.02)
                zb = z + np.random.normal(0, epaisseur*0.02)

                grille.append([xb, yb, zb])

    np.random.shuffle(grille)

    points = grille[:nb_billes]

    return Mire(points, ids=list(range(nb_billes)))"""
    
