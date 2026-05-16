import numpy as np 
import random
from .mire import Mire 
from .geometry import perpendicular_vector
from .projection import project_mire_to_plane
from .projection import project_pt_to_plane
from .transformation import calcul_matrice_rotation
from .geometry import perpendicular_vector
from .check_for_process import check_observ
from .check_for_process import check_couple



def frst_process(mire,vn,xo,yo):
    """ Entrées: la mire , le vecteur normal du plan écran et les 2 points fixés de l'écran
        Sorties:La mire obtenue après la translation et la rotation  les points xm, ym """
    eps = 1e-2
    u1 = perpendicular_vector(vn)
    u2=np.cross(u1,vn)
    random.seed(0)
    
    #On suppose que d(xo,yo)>0 (xo et yo ne sont pas trop proches)
    #prendre 2 points au hasard de notre mire 
    
    (xm,ym)=check_couple(mire,vn,xo,yo)
    xp = project_pt_to_plane(xm, vn)
    yp = project_pt_to_plane(ym, vn)
    #A ce stade on a un couple (xm,ym) candidat potentiel à la projection de (xo,yo)
    #On applique alors la translation de vecteur xpxo à la mire 
    xp_xo = xo - xp 
    trs_3d = xp_xo[0]*u1 + xp_xo[1]*u2 + 50*vn/np.linalg.norm(vn)
    mat_trs = np.array([
    [1,0,0,trs_3d[0]],
    [0,1,0,trs_3d[1]],
    [0,0,1,trs_3d[2]],
    [0,0,0,1]
    ])
    """Le 50 totalement arbitraire juste pourque la mire ne se retrouve collé au plan écran mais bien au dessus de ce plan """
    ################################################
    lst_xmire_trs = {}
    for id, x_mire in mire.pts.items():
        x_mire_homo = np.array(x_mire + [1])
        x_mire_trs_homo= mat_trs @ x_mire_homo
        lst_xmire_trs[id] = (x_mire_trs_homo[:3] / x_mire_trs_homo[3]).tolist()
    #On considère maintenant notre ym_prim translaté ayant fixé la projection de xm sur xo=xp
    # Il faut récupérer xm et ym transformés par la translation et la rotation  car il nous serviront pour le second_process 
    ###################################################################
    xm_homo = np.array(xm + [1])
    xm_trs_homo= mat_trs @ xm_homo
    xm_trs =  xm_trs_homo[:3] /  xm_trs_homo[3] 
    
    ym_homo = np.array(ym + [1])
    ym_trs_homo= mat_trs @ ym_homo
    ym_trs =  ym_trs_homo[:3] /  ym_trs_homo[3] # Pour revenir en 3D 
    
    ######################################################################
    
    yp_prim = project_pt_to_plane(ym_trs,vn)
    yo_xo = yo-xo
    ypp_xo = yp_prim - xo 
    yo_xo_3d = yo_xo[0]*u1 + yo_xo[1]*u2
    ypp_xo_3d = ypp_xo[0]*u1 + ypp_xo[1]*u2
    
    ##################################################
    
    u = yo_xo_3d / np.linalg.norm(yo_xo_3d)
    v= ypp_xo_3d / np.linalg.norm(ypp_xo_3d)
    u_xmxo = np.cross(u, v)
    cos_a = np.clip(np.dot(u, v), -1.0, 1.0)
    sin_a = np.linalg.norm(u_xmxo)
    a = np.arctan2(sin_a, cos_a)
    
    norm_u = np.linalg.norm(u_xmxo)
    if norm_u < 1e-8:
        mat_rot = np.eye(3)
    else:
        u_xmxo = u_xmxo / norm_u
        mat_rot = calcul_matrice_rotation(u_xmxo, a)
    
    ###########################################################
    lst_xmire_fin = {}
    for id, x_mire in lst_xmire_trs.items() :
         x_mire = np.array(x_mire)
         x_mire_rote = mat_rot @ (x_mire - xm_trs) + xm_trs
         lst_xmire_fin[id]= x_mire_rote.tolist()
    ###################################
    #xm_trs = np.array(xm_trs)
    xm_rote= xm_trs
    
    #ym_trs = np.array(ym_trs)
    ym_rote= mat_rot @ (ym_trs - xm_trs) + xm_trs
   
    ######################################
    points = list(lst_xmire_fin.values())
    ids = list(lst_xmire_fin.keys())

    return (Mire(points, ids=ids, alignes=mire.alignes), xm_rote , ym_rote, lst_xmire_fin)



def scd_process(mire,vn,lst_xmr_fin,xm,ym,xo,yo):
    """Entrées: la mire , le vecteur normal au plan écran ,la liste des points de la mire après le first_process, les points 
    xm et ym obtenues après translation et rotation  de la mire, xo et yo les points fixés de l'écran
       Sorties : la mire roté pour que p(ym)=yp soit égale à yo """
    ym_xm = ym - xm
    yo_xo = yo - xo #un vecteur 2D qu'il faut mettre en 3D avec le repère (u1 ,u2 ) de l'écran 
    u1 = perpendicular_vector(vn)
    u2 = np.cross(vn, u1)
    vect = yo_xo[0]*u1 + yo_xo[1]*u2 
    u = ym_xm/ np.linalg.norm(ym_xm)
    v = vect / np.linalg.norm(vect)
    #vecteur ortho au plan P vertical contenant tous ces points et autour duquel 
    #la rotation doit se faire
    axis = np.cross(u, v)
    sin_a = np.linalg.norm(axis)
    cos_a = np.clip(np.dot(u, v), -1.0, 1.0)
    a = np.arctan2(sin_a, cos_a)
    if sin_a < 1e-8:
        mat_rot = np.eye(3)
    else:
        axis = axis / sin_a
        mat_rot = calcul_matrice_rotation(axis, a)
 
   
    lst_fin = {}
    for id, x_mire in lst_xmr_fin.items():
         x_mire= np.array(x_mire)
         x_mire_rote= mat_rot @ (x_mire - xm) + xm
         lst_fin[id]= x_mire_rote.tolist()
    ##############################
    
    xm_rote= xm
   
    
    ym_rote= mat_rot @ (ym -xm) + xm
 
    #################################

    points = list(lst_fin.values())
    ids = list(lst_fin.keys())

    return (Mire(points, ids=ids, alignes=mire.alignes), xm_rote , ym_rote, lst_fin)

def thd_process(mire,v,obs,xm,ym,N):
    """Entrées: la mire qui a été fixée correctement,le vecteur normal au plan ,l'observation originale, 
    xm et ym qui sont sur notre axe de rotation N pour la discrétisation des angles """
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    ym_xm = ym - xm

    eps = 1e-4

    best_rms = np.inf
    best_mire = None
    best_angle = None

    for agl in angles:


        axis = ym_xm / np.linalg.norm(ym_xm)
        mR = calcul_matrice_rotation(axis, agl)

        lst_pt = {}

        for id, x_mire in mire.pts.items():
            x_mire = np.array(x_mire)

            x_mire_rote = mR @ (x_mire - xm) + xm

            lst_pt[id] = x_mire_rote.tolist()

        points = list(lst_pt.values())
        ids = list(lst_pt.keys())

        new_mire = Mire(points, ids=ids, alignes=mire.alignes)

        observ = project_mire_to_plane(new_mire, v)

        rms = check_observ(obs, observ)

        if rms < best_rms:
            best_rms = rms
            best_mire = new_mire
            best_angle = agl

        if rms < eps:
            break

    return (best_mire, best_rms, best_angle)
           
"""Après ça serait bien d'avoir des fonctions d'affichage de mire et de plan pour mieux visualiser le truc """