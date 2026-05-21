<<<<<<< HEAD
from core import Observation
=======
from src.core import Observation
>>>>>>> origin/main
import numpy as np 
import sys

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 4:   # Au moins 2 trucs(original et résultat de l'identification) à comparer (a)
        print("Usage: program <nb>  <original_1> <resultat_1>, etc....\n"
              " - <nb> : Le nombre de billes "
              " - <original_1> : {Le cliché original}\n"
              " - <resultat_1> : le résultat lié à cet original obtenu avec l'algo d'identification ",
            file=sys.stderr)
        sys.exit(1)
    else:
        n=len(sys.argv)
        nb_pt = int(sys.argv[1])
        lst_nb_bon = []
        for i in range(2,n-1):
            p_original=Observation.load_json(sys.argv[i])
            p_identif =Observation.load_json(sys.argv[i+1])
            eps = 1e-6 #Je pars du principe que les points sont rangés dans l'ordre: Le 1er point du fichier par exemple est forcément celui d'indice 0 et pas autre chose
            nb_bon = 0
            for j in range (nb_pt):
                if np.linalg.norm(p_original.points[i] - p_identif.points[i]) < eps:
                    nb_bon+=1
            lst_nb_bon.append(nb_bon) 
        print("Taux de réussite dans les identifications: ")
        for i in range(2,n-1):
           print(f" cliché_{i-1} : Taux de bons identifiés :  {(lst_nb_bon[i-2]/nb_pt)*100:.2f}%")
          
        
                  
                
                
            