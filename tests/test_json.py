import numpy as np
import matplotlib.pyplot as plt 
from mire import Mire 
from observation import Observation 

#Test ce qui est stocké est-il ce qui est récupéré ?  
if __name__ == "__main__":

    pts = [
        [0.25,0,0],
        [0.5,0,0],
        [0.75,1,0],
        [1,0.5,0.5],
        [0,0.25,0],
        [0,0.4,0],
        [0,0.75,0],
        [0,1,0]
    ]

    ids = np.arange(8)
    mire = Mire(pts, None , ids)
    mire.save_json("mire_simple.py")
    mire2= Mire.load_json("mire_simple.py")
    eps = 1e-6
    for i in range(Mire.ids):
         assert np.linalg.norm(mire.points[i] - mire2.points[i]) < eps
# Pour Observation 
    v1 = np.array([1,1,1])
    p1 = mire.perpendicular_vector(v1)
    p1.save_json("mire_projeté.json")
    p2 = Observation.load_json("mire_projeté.json")
    for i in range(p1.ids):
         assert np.linalg.norm(p1.points[i] - p2.points[i]) < eps #Tous les points projetés correspondent? 
