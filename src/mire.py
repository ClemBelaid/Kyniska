from src.observation import Observation
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
                "a": int(q[0]), # IDs des points alignés, ici représentés par des int
                "b": int(q[1]), # A voir si on décide que les IDs sont finalement des chars
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

        #data.get("name", "mire")
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
    
    # Voir si on en fait pas une méthode de classe... ?
    def perpendicular_vector(self, v):
        if v[1] == 0 and v[2] == 0:
            if v[0] == 0:
                raise ValueError('zero vector')
            else:
                return np.cross(v, [0, 1, 0])
        return np.cross(v, [1, 0, 0])

    def project_mire_to_plane(self, v):
        """
        Projette une mire 3D sur un plan et renvoie une Observation indexée.

        Paramètres
        ----------
        mire : Mire
            Mire contenant les points 3D.

        v : array-like (3,)
            Vecteur normal du plan.

        Retour
        ------
        Observation
            Points projetés en 2D avec les ids de la mire.
            Sert de base pour générer ensuite des observations
            bruitées / non indexées.
        """

        # Nombre de billes n
        n = len(self.points)

        # Origine O' du plan
        #o_prime = (0,0,0)

        # Calcul des coordonnées du plan
        d = 0   # d gère la hauteur du plan
        if (v[2] == 0):
            if(v[0] == 0):
                xx, zz = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
                yy = 0
            else:
                # Si c = 0, on a juste ax + by = 0 <=> ax = -by <=> x = -by/a
                yy = np.meshgrid(np.linspace(0,1,20))
                xx = -v[1]*yy/v[0]
        else:
            xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
            zz = (-v[0] * xx - v[1] * yy - d) * 1. / v[2] # z = (-ax -by)/c

        # Calcul de deux vecteurs directeurs (u1, u2) du plan, orthogonaux à v
        u1 = self.perpendicular_vector(v) 
        u2 = np.cross(v, u1)   # u2 est orthogonal à la fois à v et à u1
        
        observ = []

        for pt in self.points:
            # Vecteur u des coordonnées de la bille
            u = (pt[0], pt[1], pt[2])

             # Vecteur u_proj projeté dans le plan 2D de vecteur normal v 
            u_prime = np.dot(u,v)/np.dot(v,v)*v
            w = u - u_prime
            observ.append((np.dot(u1, w), np.dot(u2,w)))
        
        return Observation(observ, v, self.ids)
