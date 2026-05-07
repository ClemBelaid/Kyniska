from src.core import Mire
import src.core.generation as gen 
import src.core.projection as proj
import numpy as np
import sys

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
    v1 = np.array([0,0,1])
    v2 = np.array([0, 0.5, np.sqrt(3)/2])
    v3 = np.array([0, -0.5, np.sqrt(3)/2])


    # En fait, il faudrait créer 6 projections :
    # Une vérité-terrain (GT) + une projection "anonyme" pour chaque angle/vecteur de porjection
    # Pour la GT, il faut enregistrer directement les identifiants de chaque point au moment de les projeter
    # Et pour les projections "anonymes" il faut enregistrer des IDs "random"
    # ou bien négatifs (pour se souvenir qu'ils représentent une valeur fausse/indéterminée)
    
    (p1,p1_fake) = proj.project_mire_to_plane(m, v1)
    p1.save_json("proj_0_deg")
    p1_fake.save_json("proj_0_deg_pour_ident")
    (p2,p2_fake) = proj.project_mire_to_plane(m, v2)
    p1.save_json("proj_30_deg")
    p2_fake.save_json("proj_30_deg_pour_ident")
    (p3,p3_fake) = proj.project_mire_to_plane(m, v3)
    p3.save_json("proj_moins_30_deg")
    p3_fake.save_json("proj_moins_30_deg_pour_ident")