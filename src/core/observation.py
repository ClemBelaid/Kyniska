import json
import numpy as np

class Observation:
    def __init__(self, points2d, alignes = None, ids=None, v=None):
        """
        Crée une observation 2D.

        points2d : points (n,2)
        ids : optionnel
        v : vecteur normal au plan
        """
        self.points = np.array(points2d, dtype=float)
        self.ids = ids
        self.v = v
        self.alignes = alignes

    def __len__(self):
        """
        Renvoie le nombre de points observés.
        """
        return len(self.points)

    def __str__(self):
        return f"Mire with {len(self.points)} points"
    
    def draw(self, ax=None):
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
        plt.xlabel("x")
        plt.ylabel("y")
        if self.v :
            plt.title("Projection selon le plan normal au vecteur : (" + str(self.v[0]) + "," + str(self.v[1]) + "," + str(self.v[2]) + ")")

        return ax

    def copy(self):
        """
        Renvoie une copie indépendante.
        """
        obj = Observation(
            self.points.copy(),
            None if self.ids is None else self.ids.copy(),
            self.v
        )
        obj.alignes = None if self.alignes is None else self.alignes.copy()
        return obj

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
        alignes = []

        for pt in data["points"]:
            ids.append(pt["id"])
            points.append([pt["u"], pt["v"]])

        return cls(points, ids)

    def ajouterBruit(self, posRatio, negRatio):
        """
        Crée une observation 2D bruitée.
        points2d : points (n,2)
        pos : float (entre 0 et 1) du pourcentage (?) de bruit positif
            0 = aucun bruit positif, 1 = autant de bruit positif que de vraies billes (par ex ?)
        neg : float (entre 0 et 1) du pourcentage (?) de bruit négatif
            0 = aucun bruit négatif, 1 = image entièrement vidée ?
        ids : optionnel
        """
        observ_copy = self.copy()
        np.random.seed(42)

        # On calcul le nombre de billes à supprimer (faux négatifs)
        # Suppression aléatoire -> à voir, cela peut être modifié également ?
        nbFauxNeg = len(self)*negRatio
        for i in range(nbFauxNeg):
            k = np.random.randint(0, len(self))
            # Je pense qu'on ne peut pas générer directement nbFauxNeg nombres aléatoires dans [0, n-1]
            # Car il y aurait un risque de doublons et donc pas le bon nombre de billes supprimées
            np.delete (self.points, k)

        # Genère nbFauxPos points de dimension 3 aléatoires
        nbFauxPos = len(self)*posRatio
        newPoints = np.random.rand(nbFauxPos, 3)

        # Tailles s aléatoires ?
        #s = np.random.rand(nbFauxPos)*60 + 30

        self.points.append(newPoints)

