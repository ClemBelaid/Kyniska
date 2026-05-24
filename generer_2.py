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

    # Pour l'instant je dis que a1 = 0°, a2 = 30°, a3 = -30°
    #v1 = np.array([0,0,1])
    v2 = np.array([0, 0, 1])
    #v3 = np.array([0, -0.5, np.sqrt(3)/2])


    # En fait, il faudrait créer 6 projections :
    # Une vérité-terrain (GT) + une projection "anonyme" pour chaque angle/vecteur de porjection
    # Pour la GT, il faut enregistrer directement les identifiants de chaque point au moment de les projeter
    # Et pour les projections "anonymes" il faut enregistrer des IDs "random"
    # ou bien négatifs (pour se souvenir qu'ils représentent une valeur fausse/indéterminée)
    tht = np.pi/6 # angle de 10 degrés
    phi = tht # peu importe c'est pour tester 
    #mat1 = np.array([[np.cos(tht),0,np.sin(tht),30],[0,1,0,0],[-np.sin(tht),0,np.cos(tht),0],[0,0,0,1]]) # rotation et translation de la mire (frst_process simulé artficiellement)
    axis = vrMire.points[0] - vrMire.points[1]
    axis = axis / np.linalg.norm(axis)
    mat_rot = calcul_matrice_rotation(axis , tht)
    xm = vrMire.points[0]
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
    ])
    u1, u2 = build_basis(v2)
    
    origin = np.array([
    0.,
    0.,
    0.
    ])
    screen = {
    "origin": origin,
    "normal": v2,
    "u1": u1,
    "u2": u2
    }
    """mat = np.array([
    [1, 0, 0, 0],
    [0,1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ])"""

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
    vrMire.save_json("Mire_tr")

    # mire tournée utilisée seulement pour créer les observations
    mir_rot = Mire(points, ids=ids, alignes=vrMire.alignes)

    obs_ref = proj.project_mire_to_plane(mir_rot, screen)
    obs_ref.save_json("obs_ref")
    