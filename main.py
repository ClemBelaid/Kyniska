from mire import Mire
from birapport import * # pourquoi ça marche pas ??
import numpy as np
import matplotlib.pyplot as plt

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
    
    alignes = [[4,5,6,7]] # Le premier quadruplet a un birapport de 3, le deuxième environ 1.78
    ids = np.arange(8)

    m = Mire(pts, alignes, ids)
    m.save_json("test.json")
    m2 = Mire.load_json("test.json")
    m2.draw()

    # Attention à bien écrire v sous cette forme et pas v = (x,y,z) sinon ça bug
    v1 = np.array([0,0,1])
    p1 = m2.project_mire_to_plane(v1)
    p1.show()

    v2 = np.array([0,1,1])
    p2 = m2.project_mire_to_plane(v2)
    #p2.show()

    v3 = np.array([1,1,1])
    p3 = m2.project_mire_to_plane(v3)
    #p3.show()

    plt.show()

    print(identification(m2, p1, p2, p3))