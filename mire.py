import json
import numpy as np
import matplotlib.pyplot as plt

class Mire:
    def __init__(self, points, ids=None):
        self.points = np.array(points, dtype=float)

        if ids is None:
            self.ids = np.arange(len(points))
        else:
            self.ids = np.array(ids)

    def __len__(self):
        return len(self.points)

    def copy(self):
        return Mire(self.points.copy(), self.ids.copy())

    def save_json(self, filename):
        data = {
            "name": filename,
            "points": []
        }

        for pid, p in zip(self.ids, self.points):
            data["points"].append({
                "id": int(pid),
                "x": float(p[0]),
                "y": float(p[1]),
                "z": float(p[2])
            })

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_json(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        points = []
        ids = []

        for pt in data["points"]:
            ids.append(pt["id"])
            points.append([pt["x"], pt["y"], pt["z"]])

        return cls(points, ids)

class Observation:
    def __init__(self, points2d, ids=None):
        self.points = np.array(points2d, dtype=float)
        self.ids = ids

    def __len__(self):
        return len(self.points)

    def copy(self):
        return Observation(
            self.points.copy(),
            self.ids.copy()
        )

    def save_json(self, filename):
        data = {
            "name": filename,
            "points": []
        }

        for pid, p in zip(self.ids, self.points):
            data["points"].append({
                "id": int(pid),
                "u": float(p[0]),
                "v": float(p[1])
            })

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_json(cls, filename):
        with open(filename, "r") as f:
            data = json.load(f)

        points = []
        ids = []

        for pt in data["points"]:
            ids.append(pt["id"])
            points.append([pt["u"], pt["v"]])

        return cls(points2d=points, ids=ids)


def project_mire_to_plane(mire, plane_normal, direction=None):
    """
    Projette une mire 3D sur un plan et renvoie une Observation indexée.

    Paramètres
    ----------
    mire : Mire
        Mire contenant les points 3D.

    plane_point : array-like (3,)
        Un point du plan.

    plane_normal : array-like (3,)
        Vecteur normal du plan.

    direction : array-like (3,), optionnel
        Direction de projection.
        Si None, projection orthogonale.

    Retour
    ------
    Observation
        Points projetés en 2D avec les ids de la mire.
        Sert de base pour générer ensuite des observations
        bruitées / non indexées.
    """
