from src.core.mire import Mire
from src.core.generation import (
    generer_cube,
    generer_cone_tronque,
    generer_cone_tronque_creux
)
 

import numpy as np
import sys



if __name__ == "__main__":
    argc = len(sys.argv)
    if argc == 1 :
        print("Usage: generation + sauvegarde de la mire"
              "program <nom_mire> <nb_billes > \n"
              " - <nom_Mire> : la forme qu'on veut de la mire"
               "- <nb_billes > : le nombre de billes qu'on souhaite",
              file=sys.stderr)
        sys.exit(1)


    if argc == 3 :
        np.random.seed(42)
        nom_mire = sys.argv[1]
        nb_billes = int(sys.argv[2])
        a, b, c = np.random.uniform(
        -np.pi/6,
        np.pi/6,
        3
        )

        if nom_mire == "cube":

            vrMire = generer_cube(
            nb_billes=nb_billes,
            largeur=200,
            longueur=200,
            hauteur=200
            )

        elif nom_mire == "cone_tronque":

            vrMire = generer_cone_tronque(
            nb_billes=nb_billes,
            rayon_base=100,
            rayon_sommet=40,
            hauteur=250
            )

        elif nom_mire == "cone_tronque_creux":

            vrMire = generer_cone_tronque_creux(
            nb_billes=nb_billes,
            rayon_base=100,
            rayon_sommet=40,
            hauteur=250
            )
        
        vrMire.save_json("vrMire")


    
    
   
