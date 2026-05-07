import json
import numpy as np

class ObservationDict:
    def __init__(self, data_dict=None, v=None):
        """
        Crée une observation 2D utilisant un dictionnaire pour le stockage.
        
        data_dict : dictionnaire {id: [u, v]}
        v : vecteur normal au plan de projection
        """
        # Stockage unique : {id: [u, v]}
        self.data = data_dict if data_dict else {}
        self.v = v

    @property
    def points(self):
        """Retourne un array numpy (n,2) pour l'affichage et les calculs."""
        if not self.data:
            return np.array([])
        return np.array(list(self.data.values()), dtype=float)

    @property
    def ids(self):
        """Retourne la liste des IDs (clés du dictionnaire)."""
        return list(self.data.keys())

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f"ObservationDict with {len(self.data)} points"

    def draw(self, ax=None):
        """Affiche l'observation avec matplotlib."""
        import matplotlib.pyplot as plt
    
        if ax is None:
            fig, ax = plt.subplots()
    
        pts = self.points
        if pts.size > 0:
            ax.scatter(pts[:,0], pts[:,1])
    
        ax.set_aspect("equal")
        ax.set_xlabel("u")
        ax.set_ylabel("v")
        if self.v is not None:
            ax.set_title(f"Projection (Plan normal: {self.v})")

        return ax

    def copy(self):
        """Renvoie une copie indépendante."""
        new_data = {k: list(v) for k, v in self.data.items()}
        return ObservationDict(new_data, self.v)

    def save_json(self, filename):
        """Sauvegarde l'observation en JSON."""
        data_to_save = {
            "name": filename,
            "points": []
        }

        for pid, p in self.data.items():
            data_to_save["points"].append({
                "id": int(pid),
                "u": float(p[0]),
                "v": float(p[1])
            })

        with open(filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

    @classmethod
    def load_json(cls, filename):
        """Charge une observation depuis un JSON."""
        with open(filename, "r") as f:
            content = json.load(f)

        o_dict = {
            int(pt["id"]): [pt["u"], pt["v"]] 
            for pt in content["points"]
        }

        return cls(o_dict)

    def ajouterBruit(self, posRatio, negRatio):
        """
        Modifie l'observation en ajoutant/supprimant des points (bruit).
        """
        np.random.seed(42)
        current_ids = self.ids

        # 1. Faux Négatifs (Suppression de billes existantes)
        nb_to_remove = int(len(self) * negRatio)
        if nb_to_remove > 0 and current_ids:
            # Choix aléatoire des IDs à supprimer
            ids_to_remove = np.random.choice(current_ids, min(nb_to_remove, len(current_ids)), replace=False)
            for rid in ids_to_remove:
                del self.data[rid]

        # 2. Faux Positifs (Ajout de points "fantômisés")
        nb_to_add = int(len(self) * posRatio)
        if nb_to_add > 0:
            # On génère des IDs négatifs pour les distinguer des vraies billes
            #comme suggéré pour l'identification des bruits...
            start_id = min(self.ids) if self.ids else 0
            fake_ids = range(start_id - nb_to_add, start_id)
            
            #Génération de coordonnées 2D aléatoires (échelle arbitraire 0-3)
            new_pts = np.random.rand(nb_to_add, 2) * 3
            for fid, pt in zip(fake_ids, new_pts):
                self.data[fid] = pt.tolist()