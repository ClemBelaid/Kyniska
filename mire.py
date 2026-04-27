import json
import numpy as np

class Mire:
    def __init__(self, points, ids=None):
        """
        Crée une mire 3D.

        points : liste / array de points (n,3)
        ids : identifiants des billes (optionnel)
        """
        self.points = np.array(points, dtype=float)

        if ids is None:
            self.ids = np.arange(len(points))
        else:
            self.ids = np.array(ids)

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
    
        return ax


    def copy(self):
        """
        Renvoie une copie indépendante.
        """
        return Mire(self.points.copy(), self.ids.copy())

    def save_json(self, filename):
        """
        Sauvegarde l'observation en JSON.
        """
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
        """
        Charge une observation depuis un JSON.
        """
        with open(filename, "r") as f:
            data = json.load(f)

        points = []
        ids = []

        for pt in data["points"]:
            ids.append(pt["id"])
            points.append([pt["x"], pt["y"], pt["z"]])

        return cls(points, ids, data.get("name", "mire"))
    
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
    def generer_cube(cls, nb_billes, largeur=200.0, longueur=200.0, epaisseur=30.0):
        points = []

        for _ in range(nb_billes):
            x = np.random.uniform(-largeur / 2, largeur / 2)
            y = np.random.uniform(-longueur / 2, longueur / 2)
            z = np.random.uniform(0, epaisseur)
            
            points.append([x, y, z])   
        return cls(points)

class Observation:
    def __init__(self, points2d, ids=None):
        """
        Crée une observation 2D.

        points2d : points (n,2)
        ids : optionnel
        """
        self.points = np.array(points2d, dtype=float)
        self.ids = ids

    def __len__(self):
        """
        Renvoie le nombre de points observés.
        """
        return len(self.points)

    def __str__(self):
        return f"Mire with {len(self.points)} points"
    
    def show(self, ax=None):
        """
        Affiche la mire / observation avec matplotlib.
    
        ax : axe matplotlib optionnel.
        Si None, un axe est créé.
    
        Penser à appeler plt.show() après utilisation
        pour afficher la fenêtre.
        """
        import matplotlib.pyplot as plt
    
        if ax is None:
            fig, ax = plt.subplots()
    
        ax.scatter(
            self.points[:,0],
            self.points[:,1]
        )
    
        ax.set_aspect("equal")
    
        return ax

        ax.scatter(
            self.points[:,0],
            self.points[:,1],
            self.points[:,2]
        )
    
        return ax

    def copy(self):
        """
        Renvoie une copie indépendante.
        """
        return Observation(
            self.points.copy(),
            self.ids.copy()
        )

    def save_json(self, filename):
        """
        Sauvegarde l'observation en JSON.
        """
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
        """
        Charge une observation depuis un JSON.
        """
        with open(filename, "r") as f:
            data = json.load(f)

        points = []
        ids = []

        for pt in data["points"]:
            ids.append(pt["id"])
            points.append([pt["u"], pt["v"]])

        return cls(points2d=points, ids=ids)

    def ajouterBruit(self, posRatio, negRatio):
         """
        Crée une observation 2D bruitée.

        points2d : points (n,2)
        pos : float (entre 0 et 1) du pourcentage (?) de bruit positif
            0 = aucun bruit positif, 1 = image entièrement recouverte
        neg : float (entre 0 et 1) du pourcentage (?) de bruit négatif
            0 = aucun bruit négatif, 1 = image entièrement vidée
        ids : optionnel
        """