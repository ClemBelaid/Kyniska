from src.core.mire import Mire
import src.core.projection as proj
from src.core.geometry import build_basis
import numpy as np
import sys

from src.core.transformation import calcul_matrice_rotation


if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: applique pose  + projection "
              "program <mire.json> \n"
              " - <mire.json> : la forme qu'on veut de la mire }\n",
              file=sys.stderr)
        sys.exit(1)
    
    v2 = np.array([0, 0, 1])
    
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

    if argc == 2 :
        nom_Mire = sys.argv[1]
        vrMire = Mire.load_json(nom_Mire)
        np.random.seed(42)
        a, b, c = np.random.uniform(
        -np.pi/6,
        np.pi/6,
        3
        )
        mat_rot = np.array([
    [np.cos(b)*np.cos(c), -np.cos(b)*np.sin(c), np.sin(b), 2],
    [np.cos(a)*np.sin(c) + np.sin(a)*np.sin(b)*np.cos(c),  np.cos(a)*np.cos(c)-np.sin(a)*np.sin(b)*np.sin(c), -np.sin(a)*np.cos(b), 1],
    [np.sin(a)*np.sin(c)-np.cos(a)*np.sin(b)*np.cos(c), np.sin(a)*np.cos(c)+np.cos(a)*np.sin(b)*np.sin(c), np.cos(a)*np.cos(b), 2],
    [0, 0, 0, 1]
        ])
    
   

        lst_pts_tr = {}
    

        for id, x_mire in vrMire.pts.items():
        
            x_rot_h = np.array([x_mire[0],x_mire[1],x_mire[2],1.0])
            x_tr_h= mat_rot @ x_rot_h
            lst_pts_tr[id] = x_tr_h[:3].tolist()
        
        points = list(lst_pts_tr.values())
        ids = list(lst_pts_tr.keys())

        mir_rot = Mire(points, ids=ids, alignes=vrMire.alignes)
        mir_rot.save_json("Mir_tr")

        obs_ref = proj.project_mire_to_plane(mir_rot, screen)
        obs_ref.save_json("obs_ref")