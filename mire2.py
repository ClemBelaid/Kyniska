import json
import numpy as np

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

        return cls(points, ids, data.get("name", "mire"))


def generer_cone_tronque(cls, nb_billes, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0):
    points = []
    for _ in range(nb_billes):
        z = np.random.uniform(0, hauteur)
        rayon_max_z = rayon_base + (z / hauteur) * (rayon_sommet - rayon_base)
        r = rayon_max_z * np.sqrt(np.random.uniform(0, 1))
        theta = np.random.uniform(0, 2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        points.append([x,y,z])
    return cls(points)
