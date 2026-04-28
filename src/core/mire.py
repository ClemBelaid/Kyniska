import json
import numpy as np

class Mire:
    def __init__(self, points, ids=None, alignes=None):
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

        self.alignes = np.array(alignes)

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
        return Mire(self.points.copy(), self.ids.copy())

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

        return cls(points, alignes, ids)

    @classmethod
    def generer_cone_tronque(cls, nb_billes, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0):
        points = []
        for _ in range(nb_billes):

            z = np.random.uniform(0, hauteur)

            rayon_max_z = rayon_base + (z / hauteur) * (rayon_sommet - rayon_base)
            r = rayon_max_z * np.sqrt(np.random.uniform(0, 1))
            theta = np.random.uniform(0, 2 * np.pi)

            x = r * np.cos(theta)
            y = r * np.sin(theta)

            points.append([x, y, z])
        return cls(points)

    @classmethod
    def generer_cone_tronque_creux(cls, nb_billes, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0):
        points = []
        for _ in range(nb_billes):
            z = np.random.uniform(0, hauteur)
            r = rayon_base + (z / hauteur) * (rayon_sommet - rayon_base)
            theta = np.random.uniform(0, 2 * np.pi)

            x = r * np.cos(theta)
            y = r * np.sin(theta)

            points.append([x, y, z])

        return cls(points)

    @classmethod
    def generer_cube(cls, nb_billes, largeur=200.0, longueur=200.0, epaisseur=30.0):
        points = []

        for _ in range(nb_billes):
            x = np.random.uniform(-largeur / 2, largeur / 2)
            y = np.random.uniform(-longueur / 2, longueur / 2)
            z = np.random.uniform(0, epaisseur)

            points.append([x, y, z])
        return cls(points)
