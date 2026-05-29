from src.core.mire import Mire
import src.core.generation as gen 
import src.core.projection as proj
from src.core.geometry import build_basis
import numpy as np
import sys

from src.core.transformation import calcul_matrice_rotation

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: program <vrai_mire.json> <nb points>\n"
              " - <vrai_mire.json> : le json de la vrai mire faite manuellement }\n",
              file=sys.stderr)
        sys.exit(1)

    vrMire = Mire.load_json(sys.argv[1])

    # Configuration du vecteur de projection et de l'angle
    v2 = np.array([0, 0, 1])
<<<<<<< HEAD:generer_2.py
    tht = np.pi/12  # angle de 30 degrés
    phi = tht 
    
    # On gère le cas où vrMire.points est une liste ou un dictionnaire
    if hasattr(vrMire, 'points') and isinstance(vrMire.points, list):
        liste_points_base = vrMire.points
    else:
        liste_points_base = list(vrMire.pts.values())
        
    xm = np.array(liste_points_base[0])
    if len(liste_points_base) > 1:
        # CONVERSION EN NUMPY ARRAY ICI POUR ÉVITER LE TYPEERROR
        axis = np.array(liste_points_base[0]) - np.array(liste_points_base[1])
    else:
        axis = np.array([1.0, 0.0, 0.0])
        
    axis = axis / np.linalg.norm(axis)
    mat_rot = calcul_matrice_rotation(axis, tht)

    mat_tr = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 20],
        [0, 0, 0, 1]
=======
    #v3 = np.array([0, -0.5, np.sqrt(3)/2])


    # En fait, il faudrait créer 6 projections :
    # Une vérité-terrain (GT) + une projection "anonyme" pour chaque angle/vecteur de porjection
    # Pour la GT, il faut enregistrer directement les identifiants de chaque point au moment de les projeter
    # Et pour les projections "anonymes" il faut enregistrer des IDs "random"
    # ou bien négatifs (pour se souvenir qu'ils représentent une valeur fausse/indéterminée)
    tht = np.pi/6 # angle de 10 degrés
    phi = tht # peu importe c'est pour tester 
    #mat1 = np.array([[np.cos(tht),0,np.sin(tht),30],[0,1,0,0],[-np.sin(tht),0,np.cos(tht),0],[0,0,0,1]]) # rotation et translation de la mire (frst_process simulé artficiellement)
<<<<<<< HEAD
    axis = vrMire.points[2] - vrMire.points[4]
=======
    axis = vrMire.points[2] - vrMire.points[5]
>>>>>>> afa77c6 (Rien de nouveau)
    axis = axis / np.linalg.norm(axis)
    mat_rot = calcul_matrice_rotation(axis , tht)
    xm = vrMire.points[2]
    """mat_rot = np.array([
    [np.cos(phi), -np.sin(phi), 0, 0],
    [np.sin(phi),  np.cos(phi), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ])"""
    mat_tr = np.array([
    [1,0, 0, 0],
    [ 0 ,1, 0, 0],
    [0, 0, 1,20 ],
    [0, 0, 0, 1]
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae:old/generer_2.py
    ])
    
    u1, u2 = build_basis(v2)
    
    origin = np.array([0., 0., 0.])
    screen = {
        "origin": origin,
        "normal": v2,
        "u1": u1,
        "u2": u2
    }

<<<<<<< HEAD:generer_2.py
    # =======================================================
    # RÉCUPÉRATION DU NOMBRE DE POINTS EN PARAMÈTRE VIA L'ENTRÉE STANDARD
    # =======================================================
    try:
        nb_points_demande = int(sys.argv[2])
    except (IndexError, ValueError):
        nb_points_demande = len(liste_points_base)

    lst_pts_tr = {}
    lst_pts_rote = {}
    points_initiaux_bruts = []

    np.random.seed(42)  # Pour que ce soit toujours les mêmes points aléatoires
    for i in range(nb_points_demande):
        if i < len(liste_points_base):
            x_vec = np.array(liste_points_base[i])
            current_id = i
        else:
            # On génère des points supplémentaires aléatoires dans l'espace du cube
            x_vec = np.random.uniform(0.0, 30.0, 3)
            current_id = i
        # ON SAUVEGARDE LE POINT BRUT ICI (Avant la rotation !)
        points_initiaux_bruts.append(list(x_vec))
            
        x_rot = mat_rot @ (x_vec - xm) + xm 
        lst_pts_rote[current_id] = x_rot.tolist()
        x_rot_h = np.array([x_rot[0], x_rot[1], x_rot[2], 1.0])
        x_tr_h = mat_tr @ x_rot_h
        lst_pts_tr[current_id] = x_tr_h[:3].tolist()
    
    points_projetes = list(lst_pts_tr.values())
    ids_projetes = list(lst_pts_tr.keys())
    ids_initiaux = [i for i in range(nb_points_demande)]
    
    # =======================================================
    # SAUVEGARDE DES OBJETS
    # =======================================================
    # On utilise DIRECTEMENT la nouvelle liste propre 'points_initiaux_bruts' ici !
    nouvelle_mire_brute = Mire(points_initiaux_bruts, ids=ids_initiaux, alignes=vrMire.alignes)
    nouvelle_mire_brute.save_json("Mire_tr")

    # Mire tournée utilisée seulement pour créer les observations correspondantes
    mir_rot = Mire(points_projetes, ids=ids_projetes, alignes=vrMire.alignes)
    obs_ref = proj.project_mire_to_plane(mir_rot, screen)
    obs_ref.save_json("obs_ref")
    
    print(f"[SUCCESS] Génération réussie de {nb_points_demande} points dans 'Mire_tr' !")

   
=======
    lst_pts_tr = {}
    lst_pts_rote = {}

    for id, x_mire in vrMire.pts.items():
        #1ère transformation : rotation selon l'axe ym_xm
        x_vec = np.array(x_mire)
        x_rot = mat_rot @ (x_vec - xm) + xm 
        lst_pts_rote[id] = x_rot.tolist()
        x_rot_h = np.array([x_rot[0],x_rot[1],x_rot[2],1.0])
        x_tr_h= mat_tr @ x_rot_h
        lst_pts_tr[id] = x_tr_h[:3].tolist()
        
    points = list(lst_pts_tr.values())
    ids = list(lst_pts_tr.keys())
    # mire originale sauvegardée
    vrMire.save_json("Mire_init")

    # mire tournée utilisée seulement pour créer les observations
    mir_rot = Mire(points, ids=ids, alignes=vrMire.alignes)
    mir_rot.save_json("Mire_rot")

    obs_ref = proj.project_mire_to_plane(mir_rot, screen)
    obs_ref.save_json("obs_ref")
    
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae:old/generer_2.py
