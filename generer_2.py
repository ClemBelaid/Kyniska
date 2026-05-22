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
    tht = np.pi/32 # angle de 10 degrés
    phi = tht # peu importe c'est pour tester 
    #mat1 = np.array([[np.cos(tht),0,np.sin(tht),30],[0,1,0,0],[-np.sin(tht),0,np.cos(tht),0],[0,0,0,1]]) # rotation et translation de la mire (frst_process simulé artficiellement)
    
    mat = np.array([
    [np.cos(phi), -np.sin(phi), 0, 20],
    [np.sin(phi),  np.cos(phi), 0, 0],
    [0, 0, 1, 0],
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

    lst = {}
    for id, x_mire in m.pts.items():
        x_mire_homo= np.array(x_mire[0],x_mire[1],x_mire[2],1.)
        x_mire_trs_homo1= mat @ x_mire_homo
        #x_mire_trs_homo2= mat2 @  x_mire_trs_homo1
        lst[id] = x_mire_trs_homo1[:3].tolist()
    points = list(lst.values())
    ids = list(lst.keys())
    mir=Mire(points, ids=ids, alignes=vrMire.alignes)
    mir.save_json("Mire_tr")
    obs_ref = proj.project_mire_to_plane(mir,screen)
    obs_ref.save_json("obs_ref")
    