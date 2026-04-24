from mire import Mire
import numpy as np
#from observation import Observation ---> Une fois que la classe Observation sera créée

# Entrée : points en 3D
# Sortie : birapport (a,b,c,d)
# Gérer le cas où nc = nb ou bien nd = nb (division par zéro)
def calculBirapport(a, b, c, d):
    na = np.norm(a)
    nb = np.norm(b)
    nc = np.norm(c)
    nd = np.norm(d)
    return (nc-na)/(nc-nb)*(nd-na)/(nd-nb) 

# Supposons que l'objet mire contient une liste des points *alignés* qui sont donc CONNUS à l'avance !!
# Avec des birapports DIFFERENTS (sinon aucun intérêt !!)
# Par exemple : [(0,1,2,3), (4,5,6,7)]
def identification(m, p1, p2, p3):
    """
    Entrée : une mire m, trois projections différentes p1, p2, p3
    Sortie : Identification des points 2D de chaque projection en les associant à leurs IDs
    """
    
