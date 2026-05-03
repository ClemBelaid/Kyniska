from core import observation
from core import geometry
import numpy as np

def triangulation(pt_plan1, pt_plan2,vn1, vn2, pos_plan1, pos_plan2):
    """
    Contrainte de cet algo: il faut connaitre au préalable un point appartenant à chaque plan pour avoir sa position 
    Le vecteur normal ne donnant que l'orientation du plan, une infinité de plans de différentes positions est possible

    Données: pt_plan1, pt_plan2 : des points respectivement des plans 1 et 2 
                vn1 , vn2 : des vecteurs normales des plans 1 et 2 
                pos_plan1, pos_plan2: les positions 2D du point 3D recherché respectivement sur les 
                plans 1 et 2
       Résultat : le point 3D recherché """
    #Etape1 : trouver des vecteurs directeurs pour chaque plan 
    u1 = geometry.perpendicular_vector(vn1)
    v1 = np.cross(u1,vn1)
    u2 =  geometry.perpendicular_vector(vn2)
    v2 = np.cross(u2,vn2)
    #Etape2 : Reconstruire les points 3D projections du point réel sur le plan 
    x1 = pt_plan1 + pos_plan1[0]*u1 + pos_plan1[1]*v1
    x2 = pt_plan2 + pos_plan2[0]*u2 + pos_plan2[1]*v2
    #Là on sait x= x1 + lbd1*vn1 et x = x2 + lbd2*vn2 donc x1-x2 = lbd1*vn1 - lbd2*vn2 solution de moindres carrées qui se dégage ici avec 
    # lbd = (lbd1,lbd2)
    x12 = x1 - x2 
    A=np.column_stack((vn1,vn2))
    lbd, _, _, _ = np.linalg.lstsq(A, x12, rcond=None) #lbd(la solution)= (A.T*A)^-1 * A.T * x12 solution des moindres carrées 
    return x1 + lbd[0]*vn1 #ou x2 + lbd[1]*vn2 
