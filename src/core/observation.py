import json
import numpy as np

class Observation:
    def __init__(self, points2d, ids=None, alignes = None, v=None):
        """
        Crée une observation 2D en utilisant un dictionnaire pour le stockage.

        points2d : tableau de points 2D
        ids : optionnel
        alignes = tableau de quadruplets alignés (optionnel)
        v : vecteur normal au plan (optionnel)
        """
        points = np.asarray(points2d, dtype=float)

        if points.ndim != 2 or points.shape[1] != 2:
            raise ValueError("Les points doivent être des couples (x,y)")

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
        self.v = v 

    @property
    def points(self):
        """Retourne un array numpy (n,2) pour l'affichage et les calculs."""
        if not self.pts:
            return np.array([])
        return np.array(list(self.pts.values()), dtype=float)

    @property
    def ids(self):
        """Retourne la liste des IDs (clés du dictionnaire)."""
        return list(self.pts.keys())

    def __len__(self):
        return len(self.pts)

    def __str__(self):
        return f"Observation with {len} points"

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
        return Observation(self.points.copy(), ids=self.ids.copy(), alignes=[list(q) for q in self.alignes], v=self.v)


    def save_json(self, filename):
        """Sauvegarde l'observation en JSON."""
        data_to_save = {
            "name": filename,
            "points": [],
            "vecteur": self.v.tolist()
        }

        for id, pt in self.pts.items():
            data_to_save["points"].append({
                "id": int(id),
                "x": float(pt[0]),
                "y": float(pt[1])
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
        """Charge une observation depuis un JSON."""
        with open(filename, "r") as f:
            content = json.load(f)

        ids = []
        points = []

        # Reconstruction des tableaux ids et points
        for pt in content["points"]:
            ids.append(pt["id"])
            points.append([pt["x"], pt["y"]])

        # Reconstruction du tableau  de quadruplets alignés
        alignes = [
            [q["a"], q["b"], q["c"], q["d"]] 
            for q in content.get("alignes", [])
        ]

        # Récupération du vecteur normal v

        v = content.get("vecteur", content.get("v"))


        return cls(points, ids, alignes, v)
    
    def ajouter_bruit_gaussien(self, ratio=0.3, sigma=2.0):

        "ratio: ratio de points affectés par le bruit et "
        "sigma l'écart-type de la loi normale"
        

        ids = self.ids
        nb = int(len(ids) * ratio)

        ids_bruites = np.random.choice(
        ids,
        nb,
        replace=False
        )

        for pid in ids_bruites:

            pt = np.array(self.pts[pid])

            bruit = np.random.normal(
            0,
            sigma,
            2
            )

            self.pts[pid] = (pt + bruit).tolist()

    def ajouter_bruit_position(self, ratio=0.2, amplitude=2.0):
        """
        Déplace aléatoirement une partie des points.

        ratio : proportion de points bruités (entre 0 et 1)
        amplitude : déplacement max en unités écran
        """

        np.random.seed(42)

        ids = self.ids
        nb = int(len(ids) * ratio)

        if nb == 0:
            return

        ids_bruites = np.random.choice(ids, nb, replace=False)

        for pid in ids_bruites:

            pt = np.array(self.pts[pid])

            dx = np.random.uniform(-amplitude, amplitude)
            dy = np.random.uniform(-amplitude, amplitude)

            self.pts[pid] = (pt + np.array([dx, dy])).tolist()

    def getID(self, coords):
        """
        Entrée : Un triplet de coordonnées (x,y,z).
        Sortie : L'identifiant du point ayant ces coordonnées.
        """
        for id, pt in self.pts.items():
            if (pt == coords).all():
                return id