import json
import numpy as np

class Mire:
    def __init__(self, points, alignes=None, ids=None):

        points = np.asarray(points, dtype=float)

        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("Les points doivent être des triplets")

        if ids is None:
            ids = np.arange(len(points))
        else:
            ids = np.array(ids)

        self.pts = {
            int(i): points[k].tolist()
            for k, i in enumerate(ids)
        }
        self.ids = list(self.pts.keys())

        self.alignes = alignes if alignes else []

    def __len__(self):
        return len(self.pts)

    def __str__(self):
        return f"Mire with {len(self)} points"
    
    @property
    def points(self):
        return np.array(list(self.pts.values()), dtype=float)

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

        with open(filename, "r") as f:
            content = json.load(f)

        ids = []
        points = []

        for pt in content["points"]:
            ids.append(pt["id"])
            points.append([pt["x"], pt["y"], pt["z"]])

        alignes = []

        for q in content.get("alignes", []):
            alignes.append([
            q["a"],
            q["b"],
            q["c"],
            q["d"]
        ])

        return cls(points, alignes=alignes, ids=ids)
