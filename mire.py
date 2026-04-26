import json
import numpy as np
import math

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
    @staticmethod
    def perpendicular_vector(v):
            if v[1] == 0 and v[2] == 0:
                if v[0] == 0:
                    raise ValueError('zero vector')
                else:
                    return np.cross(v, [0, 1, 0])
            return np.cross(v, [1, 0, 0])

    """def project_mire_to_plane(self, v):
        
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
        

        # Nombre de billes n
        n = self.points.length()
        n_norm = np.sqrt(sum(n**2))

        # Origine O' du plan
        o_prime = (1,1,0)

        # Calcul des coordonnées du plan
        d = 0   # d gère la hauteur du plan
        xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
        zz = (-v[0] * xx - v[1] * yy - d) * 1. / v[2] # z = (-ax -by)/c

        # Calcul de deux vecteurs directeurs (u1, u2) du plan, orthogonaux à v
        u1 = self.perpendicular_vector(v) 
        u2 = np.cross(v, u1)   # u2 est orthogonal à la fois à v et à u1
        
        observ = []

        for pt in self.points:
            # Vecteur u des coordonnées de la bille
            u = (pt["x"], pt["y"], pt["z"])

             # Vecteur u_proj projeté dans le plan 2D de vecteur normal v 
            u_prime = np.dot(u,v)/np.dot(v,v)*v
            u_proj = u - u_prime

            w = u_proj - o_prime # Remarque : cette ligne n'est peut-être pas nécessaire ? 
            observ.append((np.dot(u1, w), np.dot(u2,w)))
        
        return Observation(observ, self.ids)"""
    

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
        n = self.__len__()
        #n_norm = np.sqrt(sum(n**2))
        
        # Origine O' du plan
        o_prime = (1,1,0)

        # Calcul des coordonnées du plan
        #d = 0   # d gère la hauteur du plan
        """xx, yy = np.meshgrid(np.linspace(0,1,20), np.linspace(0,1,20))
        zz = (-v[0] * xx - v[1] * yy - d) * 1. / v[2] # z = (-ax -by)/c"""

        # Calcul de deux vecteurs directeurs (u1, u2) du plan, orthogonaux à v
        u1 = Mire.perpendicular_vector(v) 
        u2 = np.cross(v, u1)   # u2 est orthogonal à la fois à v et à u1
        
   
        R_list = [] #liste de matrices de rotation 
        thetas = np.radians([-30,0,30 ]) # rotation selon l'axe x(intuition:"Hochement de tête de haut en bas"))
        for theta in thetas:
            R=np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0,np.sin(theta),np.cos(theta)]])
            R_list.append(R)
        cliches2D_3=[]
        vect_projetés_dans_le_2D=[]
        for R in R_list:
            X_cam = (R @ self.points.T).T
            observ = []
            for u in X_cam:
                    
                    # Vecteur u_proj projeté dans le plan 2D de vecteur normal v 
                    u_prime = np.dot(u,v)/np.dot(v,v)*v
                    u_proj = u - u_prime
                    vect_projetés_dans_le_2D.append(u_proj)
                    w = u_proj - o_prime #vecteur w qui va de o_prime vers u_proj 
                    """observ.append((np.dot(u1, w), np.dot(u2,w))) ajout_commentaire : on se place dans le cas orthornormé""" 
                    #cas non orthonormé:
                    a11 = np.dot(u1, u1)
                    a12 = np.dot(u1, u2)
                    a22 = np.dot(u2, u2)

                    b1 = np.dot(w, u1)
                    b2 = np.dot(w, u2)
                    det = a11 * a22 - a12 * a12
                    a = (b1 * a22 - b2 * a12) / det
                    b = (b2 * a11 - b1 * a12) / det
                    observ.append((a, b))
            cliches2D_3.append(Observation(observ, self.ids))
        return cliches2D_3, vect_projetés_dans_le_2D

    
      
            