import json
import numpy as np

class Mire:
    def __init__(self, points, alignes = None, ids = None):
        """
        Crée une mire 3D utilisant un dictionnaire pour le stockage.
        
        data_dict : dictionnaire {id: [x, y, z]}
        alignes : liste de quadruplets d'IDs (a, b, c, d) de points alignés
        """
        points = np.asarray(points, dtype=float)

        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("Les points doivent être des triplets")

        n = len(points)

        if ids is None:
            ids = np.arange(n)
        else:
            ids = np.asarray(ids)
            if len(ids) != n:
                raise ValueError("ids et points doivent avoir la même longueur")

        # Construction du dictionnaire
        self.pts = {int(i): points[k].tolist() for k, i in enumerate(ids)}

        self.alignes = alignes if alignes else []

    @property
    def points(self):
        """Retourne un array numpy (n,3) pour garder la compatibilité avec les calculs."""
        if not self.pts:
            return np.array([])
        return np.array(list(self.pts.values()), dtype=float)

    @property
    def ids(self):
        """Retourne la liste des identifiants des billes."""
        return list(self.pts.keys())

    def __len__(self):
        return len(self.pts)

    def __str__(self):
        return f"Mire with {len} points"

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
        return Mire(self.points.copy(), ids=self.ids.copy(), alignes=[list(q) for q in self.alignes])

    def save_json(self, filename):
        """Sauvegarde la mire en JSON en parcourant le dictionnaire."""
        data_to_save = {
            "name": filename,
            "points": [],
            "alignes": []
        }

        # On itère directement sur le dictionnaire
        for id, pt in self.pts.items():
            data_to_save["points"].append({
                "id": int(id),
                "x": float(pt[0]),
                "y": float(pt[1]),
                "z": float(pt[2])
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

        ids = []
        points = []

        # Reconstruction des tableaux ids et poinds
        for pt in content["points"]:
            ids.append(pt["id"])
            points.append([pt["x"], pt["y"], pt["z"]])

        # Reconstruction du tableau alignés
        alignes = [
            [q["a"], q["b"], q["c"], q["d"]] 
            for q in content.get("alignes", [])
        ]

        return cls(points, ids, alignes)

    def getID(self, coords):
        """
        Entrée : Un triplet de coordonnées (x,y,z).
        Sortie : L'identifiant du point ayant ces coordonnées.
        """
        for id, pt in self.pts.iteritems():
            if pt == coords:
                return id