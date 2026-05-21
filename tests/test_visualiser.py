import unittest
import sys
import os
from unittest.mock import patch

# --- CONFIGURATION DES CHEMINS ---
chemin_actuel = os.path.dirname(os.path.abspath(__file__))
racine_projet = os.path.normpath(os.path.join(chemin_actuel, '..'))

if racine_projet not in sys.path:
    sys.path.insert(0, racine_projet)

# Importation de la nouvelle fonction principale
<<<<<<< HEAD
from src.core.visualiser6 import visualiser_3D
=======
from src.core.visualiser5 import visualiser_3D
>>>>>>> d23e5b5 (Plusieurs modifs liés à generer.py et le nouveau fichier compare2.py maintenant les commandes à exécuter sont python generer.py forme nb_pts et python -m src.core.compare2)

class TestVisualiseurV5(unittest.TestCase):
    
    @patch('matplotlib.pyplot.show')  # Évite d'ouvrir la fenêtre de dialogue pendant le test
    def test_visualiser_3d_chargement_json(self, mock_show):
        """ Vérifie que le visualiseur charge correctement les deux fichiers JSON de generer.py """
        mire_json = os.path.join(racine_projet, 'newMire.json')
        obs_json = os.path.join(racine_projet, 'obs_ref.json')
        
        # Le test passe si la fonction s'exécute sans lever d'exception
        if os.path.exists(mire_json) and os.path.exists(obs_json):
            try:
                visualiser_3D(mire_json_path=mire_json, ecran_json_path=obs_json)
                execution_reussie = True
            except Exception as e:
                print(f"\n❌ Le visualiseur a planté : {e}")
                execution_reussie = False
            
            self.assertTrue(execution_reussie)
        else:
            print("\n⚠️ Fichiers JSON de test manquants, lance generer.py d'abord.")

if __name__ == '__main__':
    unittest.main()