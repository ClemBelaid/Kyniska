from src.core import Mire
import src.core.generation as gen 
import src.core.projection as proj
import numpy as np
import sys

from transformation import calcul_matrice_rotation

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: program <type mire> <nb points> <a1> <a2> <a3> ...\n"
              " - <type mire> : {pave | cone tronque | }\n"
              " - <nb points> : un nombre \n"
              " - <a1> : un angle (en degrés) \n"
              " - <a2> : un angle (en degrés) \n"
              " - <a3> : un angle (en degrés) ",
            file=sys.stderr)
        sys.exit(1)

    nb_pts = int(sys.argv[2])
    if(sys.argv[1] == "pave"):
        m = gen.generer_cube(nb_pts)
    
    if(sys.argv[1] == "cone tronque"):
        m = gen.generer_cone_tronque(nb_pts)
    
    if(sys.argv[1] == "cone tronque creux"):
        m = gen.generer_cone_tronque_creux(nb_pts)
    
    m.save_json("newMire")

    # Pour l'instant je dis que a1 = 0°, a2 = 30°, a3 = -30°
    #v1 = np.array([0,0,1])
    v2 = np.array([0, 0.5, np.sqrt(3)/2])
    #v3 = np.array([0, -0.5, np.sqrt(3)/2])


    # En fait, il faudrait créer 6 projections :
    # Une vérité-terrain (GT) + une projection "anonyme" pour chaque angle/vecteur de porjection
    # Pour la GT, il faut enregistrer directement les identifiants de chaque point au moment de les projeter
    # Et pour les projections "anonymes" il faut enregistrer des IDs "random"
    # ou bien négatifs (pour se souvenir qu'ils représentent une valeur fausse/indéterminée)
    tht = np.pi/18 # angle de 10 degrés
    phi = tht # peu importe c'est pour tester 
    #mat1 = np.array([[np.cos(tht),0,np.sin(tht),30],[0,1,0,0],[-np.sin(tht),0,np.cos(tht),0],[0,0,0,1]]) # rotation et translation de la mire (frst_process simulé artficiellement)
    mat = calcul_matrice_rotation([0,0,1], tht)
    mat1 = np.eye(4)
    mat1[:3,:3] = mat
    mat1[:3,3] = [30,0,0]
    mat2 = np.array([
    [np.cos(phi), -np.sin(phi), 0, 0],
    [np.sin(phi),  np.cos(phi), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
    ])
    lst = {}
    for id, x_mire in m.pts.items():
        x_mire_homo= np.array(x_mire + [1])
        x_mire_trs_homo1= mat1 @ x_mire_homo
        #x_mire_trs_homo2= mat2 @  x_mire_trs_homo1
        lst[id] = (x_mire_trs_homo1[:3] / x_mire_trs_homo1[3]).tolist()
    points = list(lst.values())
    ids = list(lst.keys())
    mir=Mire(points, ids=ids, alignes=m.alignes)
    obs_ref = proj.project_mire_to_plane(mir,v2)
    obs_ref.save_json("obs_ref")

    """(p1,p1_fake) = proj.project_mire_to_plane(m, v1)
    p1.save_json("proj_0_deg")
    p1_fake.save_json("proj_0_deg_pour_ident")
    (p2,p2_fake) = proj.project_mire_to_plane(m, v2)
    p1.save_json("proj_30_deg")
    p2_fake.save_json("proj_30_deg_pour_ident")
    (p3,p3_fake) = proj.project_mire_to_plane(m, v3)
    p3.save_json("proj_moins_30_deg")
    p3_fake.save_json("proj_moins_30_deg_pour_ident")"""