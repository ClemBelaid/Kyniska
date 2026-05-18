import unittest
import numpy as np
import sys
import os

# --- CONFIGURATION DES CHEMINS ---
# On remonte d'un cran pour trouver la racine 'Kyniska'
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
racine_projet = os.path.normpath(os.path.join(chemin_actuel, '..'))

#On ajoute la racine au système pour que 'from src.core...' fonctionne
if racine_projet not in sys.path:
    sys.path.insert(0, racine_projet)

#importation de la fonction à tester
from src.core.visualiser4_mire import get_coords

class TestVisualiseur(unittest.TestCase):
    
    def test_get_coords_dict_3d(self):
        """ Vérifie l'extraction X, Y, Z depuis ton format DICTIONNAIRE """
        # On simule le format que tu as (index: [x, y, z])
        test_dict = {
            0: [10.0, 20.0, 30.0], 
            1: [40.0, 50.0, 60.0]
        }
        
        x, y, z = get_coords(test_dict, is_2d=False)
        
        # On vérifie que les valeurs extraites sont correctes
        self.assertEqual(z[0], 30.0)
        self.assertEqual(z[1], 60.0)
        self.assertIsInstance(x, np.ndarray)

    def test_get_coords_2d_forcing(self):
        """ Vérifie que le Z est bien mis à 0 quand on est en mode observation (2D) """
        # Même si on met un Z à 999, is_2d=True doit le transformer en 0
        test_dict = {0: [10.0, 20.0, 999.0]}
        
        x, y, z = get_coords(test_dict, is_2d=True)
        
        self.assertEqual(z[0], 0.0)
        self.assertEqual(len(x), 1)

if __name__ == '__main__':
    unittest.main()