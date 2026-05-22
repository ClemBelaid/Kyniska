import json
import numpy as np
#import cv2
from .transformation import calcul_matrice_pose

class Mire:
    def __init__(self, points, pose = None, alignes = None, ids = None):
        """
        Crée une mire 3D utilisant un dictionnaire pour le stockage.
        
        points : une liste des points 3D de la mire
        pose : la matrice de pose de la mire par rapport au référentiel écran (monde)
        alignes : liste de quadruplets d'IDs (a, b, c, d) de points alignés
        ids : liste des identifiants des points 3D
        """
        points = np.asarray(points, dtype=float)

        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("Les points doivent être des triplets")

        if ids is None:
            ids = np.arange(len(points))
        else:
            ids = np.array(ids)

        # Construction du dictionnaire
        self.pts = {int(i): points[k].tolist() for k, i in enumerate(ids)}

        # Matrice de pose par défaut = l'identité (pour débuter)
        # Rmq : Xcam = R*Xmire + t = Mpose*Xmire
        if pose is None:
            self.pose = np.identity(4)
        else:
            self.pose = pose

        # Récupération des matrices de rotation et de translation à partir de la matrice de pose
        self.rmatrix = self.pose[0:3, 0:3]
        self.tmatrix = self.pose[0:3, 3]

        self.alignes = alignes if alignes else []

    def __len__(self):
        return len(self.pts)

    def __str__(self):
        return f"Mire with {len(self)} points"
    
    @property
    def points(self):
        return np.array(list(self.pts.values()), dtype=float)
    
    @property
    def ids(self):
        return np.array(list(self.pts.keys()), dtype=int)

    def draw(self, ax=None):
        """Affiche la mire avec matplotlib (3D)."""
        import matplotlib.pyplot as plt
        if ax is None:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection="3d")

        pts = self.points
        if pts.size > 0:
            pts = [np.append(pt, 1) for pt in pts]
            pts = [self.pose@pt for pt in pts]
            for pt in pts:
                ax.scatter(pt[0], pt[1], pt[2])

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
            "alignes": [],
            "pose": {
                "rotation" : self.rmatrix.tolist(),
                "translation" : self.tmatrix.tolist()
            }
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

        rmatrix = np.array(content["pose"]["rotation"])
        tmatrix = np.array(content["pose"]["translation"])
        pose = calcul_matrice_pose(rmatrix, tmatrix)

        return cls(points, pose, alignes, ids)

        return cls(points, alignes=alignes, ids=ids)
