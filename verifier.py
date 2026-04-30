from src.core import Observation
import numpy as np 
import sys

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 4:   # Au moins 2 trucs(original et résultat de l'identification) à comparer (a)
        print("Usage: program <nb>  <original_1> <resultat_1>, etc....\n"
              " - <nb> : Le nombre de billes "
              " - <original_1> : La projection vérité-terrain (tous les points identifiés correctement)\n"
              " - <resultat_1> : Le résultat obtenu à partir d'un algorithme d'identification ",
            file=sys.stderr)
        sys.exit(1)

    else:
        n = len(sys.argv)
        nb_pt = int(sys.argv[1])
        lst_nb_bon = []
        for i in range(1, n/2):
            p_original = Observation.load_json(sys.argv[2*i])
            p_identif = Observation.load_json(sys.argv[2*i+1])
            nb_bon = 0
            for j in range(len(p_identif.ids)) :
                # Idée : créer un dictionnaire de points : (id, coordonnées)
                if p_identif.points[j] == p_original.points[j] :
                    nb_bon += 1
            lst_nb_bon.append(nb_bon) 
        print("Taux de réussite dans les identifications: ")
        for i in range(2, n-1):
           print(f" cliché_{i-1} : Taux de bons identifiés :  {(lst_nb_bon[i-2]/nb_pt)*100:.2f}%")
          
        
                  
                
                
            