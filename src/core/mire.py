import json
import numpy as np

class Mire:
    def __init__(self, points, ids=None):
        """
        Crée une mire 3D.

        points : liste / array de points (n,3)
        alignes : liste de quadruplets (a,b,c,d) de points alignés connus à l'avance
        # Si on ne les connait pas encore, on peut peut-être écrire une fonction pour les calculer...?
        ids : identifiants des billes (optionnel)
        """
        self.points = np.array(points, dtype=float)

        if ids is None:
            self.ids = np.arange(len(points))
        else:
            self.ids = np.array(ids)

        self.alignes = None

    def __len__(self):
        """
        Renvoie le nombre de points de la mire.
        """
        return len(self.points)

    def __str__(self):
        return f"Mire with {len(self.points)} points"

    def draw(self, ax=None):
        """
        Affiche la mire avec matplotlib (3D).

        ax : axe matplotlib optionnel.

        appeler plt.show() après utilisation
        pour afficher la fenêtre.
        """
        import matplotlib.pyplot as plt
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        ax.scatter(
            self.points[:,0],
            self.points[:,1],
            self.points[:,2]
        )

        plt.xlabel("x")
        plt.ylabel("y")

        return ax

    def copy(self):
        """
        Renvoie une copie indépendante.
        """
        res = Mire(self.points.copy(), self.ids.copy())
        res.alignes = None if self.alignes is None else self.alignes.copy()
        return res

    def save_json(self, filename):
        """
        Sauvegarde la mire en JSON.
        """
        data = {
            "name": filename,
            "points": [],
            "alignes" : []
        }

        for pid, p in zip(self.ids, self.points):
            data["points"].append({
                "id": int(pid),
                "x": float(p[0]),
                "y": float(p[1]),
                "z": float(p[2])
            })

        for q in self.alignes:
            data["alignes"].append({
                "a": int(q[0]),
                "b": int(q[1]),
                "c": int(q[2]),
                "d": int(q[3])
            })

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_json(cls, filename):
        """
        Charge une mire depuis un JSON.
        """
        with open(filename, "r") as f:
            data = json.load(f)

        points = []
        ids = []
        alignes = []

        for pt in data["points"]:
            ids.append(pt["id"])
            points.append([pt["x"], pt["y"], pt["z"]])

        for q in data["alignes"]:
            alignes.append([q["a"], q["b"], q["c"], q["d"]])

        obj = cls(points, ids)
        obj.alignes = alignes
        return obj
