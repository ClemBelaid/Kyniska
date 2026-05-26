import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from itertools import combinations
from src.core.mire import Mire 
from src.core.geometry import perpendicular_vector
from src.core.projection import project_mire_to_plane
from src.core.projection import project_pt_to_plane
from src.core.transformation import calcul_matrice_rotation
from src.core.geometry import perpendicular_vector
from src.core.check_for_process import check_observ
from src.core.check_for_process import check_couple
#from .visualiser6 import visualiser_iteration



def frst_process(mire, screen, xm, ym, xo, yo):
    """ Entrées: la mire , le vecteur normal du plan écran et les 2 points fixés de l'écran
        Sorties:La mire obtenue après la translation et la rotation  les points xm, ym """
    eps = 1e-2
   
    random.seed(0)
    
    #On suppose que d(xo,yo)>0 (xo et yo ne sont pas trop proches)
    #prendre 2 points au hasard de notre mire 
    vn=screen["normal"]
    xp = project_pt_to_plane(xm, screen)
    yp = project_pt_to_plane(ym, screen)
    #A ce stade on a un couple (xm,ym) candidat potentiel à la projection de (xo,yo)
    #On applique alors la translation de vecteur xpxo à la mire 
    xp_xo = xo - xp 
    trs_3d = xp_xo[0]*screen["u1"] + xp_xo[1]*screen["u2"] + 10*screen["normal"]
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
        x_mire_h = np.array([x_mire[0], x_mire[1], x_mire[2], 1.0])
        x_mire_trs_homo= mat_trs @ x_mire_h
        lst_xmire_trs[id] = x_mire_trs_homo[:3].tolist()

    #On considère maintenant notre ym_prim translaté ayant fixé la projection de xm sur xo=xp
    # Il faut récupérer xm et ym transformés par la translation et la rotation  car il nous serviront pour le second_process 
    ###################################################################
    xm_h = np.array([xm[0], xm[1], xm[2], 1.0])
    xm_trs_homo= mat_trs @ xm_h
    xm_trs =  xm_trs_homo[:3] 
    
    ym_h = np.array([ym[0], ym[1], ym[2], 1.0])
    ym_trs_homo= mat_trs @ ym_h
    ym_trs =  ym_trs_homo[:3] # Pour revenir en 3D 
    
    #####################################################################
    
    yp_prim = project_pt_to_plane(ym_trs,screen)
    yo_xo = yo-xo
    ypp_xo = yp_prim - xo 
    yo_xo_3d = yo_xo[0]*screen["u1"] + yo_xo[1]*screen["u2"]
    ypp_xo_3d = ypp_xo[0]*screen["u1"] + ypp_xo[1]*screen["u2"]
    
    ##################################################
    
    norm_u = np.linalg.norm(yo_xo_3d)
    norm_v = np.linalg.norm(ypp_xo_3d)

    if norm_u < 1e-8 or norm_v < 1e-8:
        raise ValueError("Vecteur nul dans frst_process")

    u = yo_xo_3d / norm_u
    v = ypp_xo_3d / norm_v
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



def scd_process(mire,screen,lst_xmr_fin,xm,ym,xo,yo):
    """Entrées: la mire , le vecteur normal au plan écran ,la liste des points de la mire après le first_process, les points 
    xm et ym obtenues après translation et rotation  de la mire, xo et yo les points fixés de l'écran
       Sorties : la mire roté pour que p(ym)=yp soit égale à yo """
    ym_xm = ym - xm
    yo_xo = yo - xo #un vecteur 2D qu'il faut mettre en 3D avec le repère (u1 ,u2 ) de l'écran 
   
    vect = yo_xo[0]*screen["u1"] + yo_xo[1]*screen["u2"]
    norm_u = np.linalg.norm(ym_xm)
    norm_v = np.linalg.norm(vect)

    if norm_u < 1e-8 or norm_v < 1e-8:
        raise ValueError("Vecteur nul dans scd_process")

    u = ym_xm / norm_u
    v = vect / norm_v
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

def thd_process(mire,screen,obs,xm,ym,N):
    """Entrées: la mire qui a été fixée correctement,le vecteur normal au plan, l'observation originale, 
    xm et ym qui sont sur notre axe de rotation N pour la discrétisation des angles """
    
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    
    ym_xm = ym - xm

    eps = 1e-4

    best_rms = np.inf
<<<<<<< HEAD
    best_mire = None
    best_angle = None

    for agl in angles:
        axis = ym_xm / np.linalg.norm(ym_xm)
=======
    #best_mire = None
    best_angle = None
    axis = ym_xm / np.linalg.norm(ym_xm)
    for agl in angles:


        
>>>>>>> afa77c6 (Rien de nouveau)
        mR = calcul_matrice_rotation(axis, agl)

        lst_pt = {}

        for id, x_mire in mire.pts.items():
            x_mire = np.array(x_mire)

            x_mire_rote = mR @ (x_mire - xm) + xm

            lst_pt[id] = x_mire_rote.tolist()

        points = list(lst_pt.values())
        ids = list(lst_pt.keys())

        new_mire = Mire(points, ids=ids, alignes=mire.alignes)

        observ = project_mire_to_plane(new_mire, screen)

        rms = check_observ(obs, observ)

        if rms < best_rms:
            best_rms = rms
<<<<<<< HEAD
            best_mire = new_mire
=======
            #best_mire = new_mire
>>>>>>> afa77c6 (Rien de nouveau)
            best_angle = agl

        if rms < eps:
            break

<<<<<<< HEAD
    return (best_mire, best_rms, best_angle)
           
=======
    return  best_rms, best_angle
    """( best_mire,"""
    """, best_angle)"""
>>>>>>> afa77c6 (Rien de nouveau)

def app_proc(mire,obs,screen,xo,yo): 
        
    pts_items = list(mire.pts.items())
    d_obs = np.linalg.norm(yo - xo)
    best_score = np.inf
    best_mire = None
    best_xm = None
    best_ym = None
    best_agl = 0

    for (id1, xm), (id2, ym) in combinations(pts_items, 2):
        xm = np.array(xm)
        ym = np.array(ym)
         # projections des points candidats
        xp = project_pt_to_plane(xm, screen)
        yp = project_pt_to_plane(ym, screen)

        d_proj = np.linalg.norm(yp - xp)

        # conditions
        if d_proj <= 1e-8:
                continue

        if d_proj < d_obs:
                continue

        try:
                # process 1
                mire1, xm1, ym1, lst1 = frst_process(
                    mire,
                    screen,
                    xm,
                    ym,
                    xo,
                    yo
                )

        except Exception as e:
            print("Erreur process 1 sur le  couple :", id1, id2, e)
            continue

        try:
                # process 2
                mire2, xm2, ym2, lst2 = scd_process(
                    mire1,
                    screen,
                    lst1,
                    xm1,
                    ym1,
                    xo,
                    yo
                )

        except Exception as e:
            print("Erreur process 2 sur le couple :", id1, id2, e)
            continue

        try:
                # process 3
                mire3, score, agl = thd_process(
                    mire2,
                    screen,
                    obs,
                    xm2,
                    ym2,
                    360
                )

<<<<<<< HEAD
=======
                # meilleur résultat
                if score < best_score:

                    best_score = score
                    best_agl = agl
                    best_mire = mire2
                    best_xm = xm2
                    best_ym = ym2

>>>>>>> afa77c6 (Rien de nouveau)
        except Exception as e:
            print("Erreur process 3 sur le couple :", id1, id2, e)
            continue

        # meilleur résultat
        if score < best_score:
            best_score = score
            best_agl = agl
            best_mire = mire3
            best_xm = xm
            best_ym = ym

    return best_mire, best_xm, best_ym, best_score , best_agl
