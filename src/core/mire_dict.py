import json
import numpy as np

class MireDict:
    def __init__(self, data_dict=None, alignes=None):
        """
        Crée une mire 3D utilisant un dictionnaire pour le stockage.
        
        data_dict : dictionnaire {id: [x, y, z]}
        alignes : liste de quadruplets d'IDs (a, b, c, d) de points alignés
        """
        #On stocke tout dans un seul dictionnaire
        self.data = data_dict if data_dict else {}
        self.alignes = alignes if alignes else []

    @property
    def points(self):
        """Retourne un array numpy (n,3) pour garder la compatibilité avec les calculs."""
        if not self.data:
            return np.array([])
        return np.array(list(self.data.values()), dtype=float)

    @property
    def ids(self):
        """Retourne la liste des identifiants des billes."""
        return list(self.data.keys())

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return f"MireDict with {len(self.data)} points"

    def draw(self, ax=None):
        """Affiche la mire avec matplotlib (3D)."""
        import matplotlib.pyplot as plt
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        pts = self.points
        if pts.size > 0:
            ax.scatter(pts[:,0], pts[:,1], pts[:,2])

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        return ax

    def copy(self):
        """Renvoie une copie indépendante de la mire."""
        new_data = {k: list(v) for k, v in self.data.items()}
        new_alignes = [list(q) for q in self.alignes] if self.alignes else None
        return MireDict(new_data, new_alignes)

    def save_json(self, filename):
        """Sauvegarde la mire en JSON en parcourant le dictionnaire."""
        data_to_save = {
            "name": filename,
            "points": [],
            "alignes": []
        }

        # On itère directement sur le dictionnaire
        for pid, coords in self.data.items():
            data_to_save["points"].append({
                "id": int(pid),
                "x": float(coords[0]),
                "y": float(coords[1]),
                "z": float(coords[2])
            })

        for q in self.alignes:
            data_to_save["alignes"].append({
                "a": int(q[0]), "b": int(q[1]), 
                "c": int(q[2]), "d": int(q[3])
            })

        with open(filename, "w") as f:
            json.dump(data_to_save, f, indent=4)

    @classmethod
    def load_json(cls, filename):
        """Charge une mire depuis un JSON et construit le dictionnaire."""
        with open(filename, "r") as f:
            content = json.load(f)

        # Reconstruction du dictionnaire {id: [x, y, z]}
        p_dict = {
            int(pt["id"]): [pt["x"], pt["y"], pt["z"]] 
            for pt in content["points"]
        }

        # Reconstruction des alignements
        alignes = [
            [q["a"], q["b"], q["c"], q["d"]] 
            for q in content.get("alignes", [])
        ]

        return cls(p_dict, alignes)