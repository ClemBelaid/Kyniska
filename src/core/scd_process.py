import numpy as np 
import random
from .mire import Mire 
from .projection import project_mire_to_plane
from .projection import project_pt_to_plane
from .transformation import calcul_matrice_rotation
from .geometry import perpendicular_vector

def scd_process(mire,v,lst_xmr_fin,xm,ym,xo,yo):
    """Entrées: la mire , le vecteur normal au plan écran ,la liste des points de la mire après le first_process, les points 
    xm et ym obtenues après translation et rotation  de la mire, xo et yo les points fixés de l'écran
       Sorties : la mire roté pour que p(ym)=yp soit égale à yo """
    ym_xm = ym - xm
    yo_xo = yo - xo #un vecteur 2D qu'il faut mettre en 3D avec le repère (u1 ,u2 ) de l'écran 
    u1 = perpendicular_vector(v)
    u2 = np.cross(v, u1)
    vect = yo_xo[0]*u1 + yo_xo[1]*u2 
    w = np.cross(ym_xm,vect) #vecteur ortho au plan P vertical contenant tous ces points et autour duquel 
    #la rotation doit se faire 
    cos_a = np.dot(ym_xm,vect) / (np.linalg.norm(ym_xm) * np.linalg.norm(vect))
    a = np.arccos(cos_a)
    mat_rot = calcul_matrice_rotation(w,a)
    lst_fin = {}
    for id, x_mire in lst_xmr_fin:
         x_mire_homo= np.array(x_mire + [1])
         x_mire_rote_homo= mat_rot @ x_mire_homo
         lst_fin[id]= (x_mire_rote_homo[:3] / x_mire_rote_homo[3]).tolist()
    ##############################
    xm_homo = np.array(xm+[1])
    xm_rote_homo = mat_rot @ xm_homo
    xm_rote =  (xm_rote_homo[:3] / xm_rote_homo[3])
    ym_homo = np.array(ym+[1])
    ym_rote_homo = mat_rot @ ym_homo
    ym_rote =  (ym_rote_homo[:3] / ym_rote_homo[3])
    #################################

    points = list(lst_fin.values())
    ids = list(lst_fin.keys())

    return (Mire(points, ids=ids, alignes=mire.alignes), xm_rote , ym_rote, lst_fin)
