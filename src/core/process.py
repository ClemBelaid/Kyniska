import numpy as np
import matplotlib as plt
import random
import matplotlib.pyplot as plt
from itertools import permutations
from src.core.mire import Mire 
from src.core.geometry import perpendicular_vector
from src.core.projection import project_mire_to_plane
from src.core.projection import project_pt_to_plane
from src.core.transformation import calcul_matrice_rotation
from src.core.geometry import perpendicular_vector
from src.core.check_for_process import check_observ
from itertools import combinations
#from src.core.check_for_process import check_couple
#from .visualiser6 import visualiser_iteration



<<<<<<< HEAD
def frst_process(mire,screen,xm,ym,xo,yo):
    """ Entrées: la mire , le plan écran(un dico avec vecteur normal, vect directeurs et origine), 2 points de la mire,et les 2 points fixés de l'écran
        Sorties: La mire obtenue après la translation et la rotation  les points xm, ym apres translation et rotation et la liste des points transformés  """
    #On suppose que d(xo,yo)>0 (xo et yo ne sont pas trop proches)
    #prendre 2 points au hasard de notre mire 
    vn=screen["normal"]
    
=======
def frst_process(mire, screen, xm, ym, xo, yo):
    """ Entrées: la mire , le vecteur normal du plan écran et les 2 points fixés de l'écran
        Sorties:La mire obtenue après la translation et la rotation  les points xm, ym """
    eps = 1e-2
   
    random.seed(0)
    
    #On suppose que d(xo,yo)>0 (xo et yo ne sont pas trop proches)
    #prendre 2 points au hasard de notre mire 
    vn=screen["normal"]
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae
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
    u = yo_xo_3d / np.linalg.norm(yo_xo_3d)
    v = ypp_xo_3d / np.linalg.norm(ypp_xo_3d)

    # FIX ORIENTATION (empêche inversion 180°)
    if np.dot(v, u) < 0:
        v = -v
        ypp_xo_3d = -ypp_xo_3d

    axis = screen["normal"]
    cos_a = np.clip(np.dot(v, u), -1.0, 1.0)
    sin_a = np.dot(np.cross(v, u), axis)

    a = np.arctan2(sin_a, cos_a)
    mat_rot = calcul_matrice_rotation(axis, a)
    
    #norm_u = np.linalg.norm(u_xmxo)
    #if norm_u < 1e-8:
    #    mat_rot = np.eye(3)
    #else:
    #    u_xmxo = u_xmxo / norm_u
    #    mat_rot = calcul_matrice_rotation(u_xmxo, a)

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

def scd_process(mire, screen, lst_xmr_fin, xm, ym, xo, yo):

    # -----------------------------------------
    # Direction écran xo -> yo remise en 3D
    # -----------------------------------------
    yo_xo = yo - xo

<<<<<<< HEAD
def scd_process(mire,screen,lst_xmr_fin,xm,ym,xo,yo):
    """Entrées: la mire , le vecteur normal au plan écran ,la liste des points de la mire après le first_process, les points 
    xm et ym obtenues après translation et rotation  de la mire, xo et yo les points fixés de l'écran
       Sorties : la mire roté pour que p(ym)=yp soit égale à yo, les points xm , ym tranformés par cette deuxième rotation et la liste des pts transformés """
=======
    d = (
        yo_xo[0] * screen["u1"]
        + yo_xo[1] * screen["u2"]
    )

    d = d / np.linalg.norm(d)

    # -----------------------------------------
    # Axe parallèle à l'écran
    # et orthogonal à xo->yo
    # -----------------------------------------
    n = screen["normal"]

    axis = np.cross(n, d)
    axis = axis / np.linalg.norm(axis)

    # -----------------------------------------
    # Recherche du meilleur angle
    # -----------------------------------------
    angles = np.linspace(np.pi, 0, 2000)

    best_err = np.inf
    best_rot = None
    best_ym = None
    best_rot_inv = None

    # Calcul de l'angle phi entre le vecteur ym_xm et l'écran
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae
    ym_xm = ym - xm
    sin_phi = ym_xm[2]
    ym_xm[2] = 0
    cos_phi = np.linalg.norm(ym_xm)
    phi = np.arctan2(sin_phi, cos_phi)

    for angle in angles:
        R = calcul_matrice_rotation(axis, angle)

        ym_rot = R @ (ym - xm) + xm

        proj = project_pt_to_plane(ym_rot, screen)

        err = np.linalg.norm(proj - yo)

        if err < best_err:
            best_err = err
            best_rot = R
            angle_inv = 2*phi + angle
            best_rot_inv = calcul_matrice_rotation(axis, -angle_inv)
            best_ym = ym_rot
            best_ym_inv = best_rot_inv @ (ym - xm) + xm

    # -----------------------------------------
    # Rotation finale de toute la mire
    # -----------------------------------------
    lst_fin = {}

    for id, pt in lst_xmr_fin.items():

        pt = np.array(pt)
        pt_rot = best_rot @ (pt - xm) + xm
        lst_fin[id] = pt_rot.tolist()

    points = list(lst_fin.values())
    ids = list(lst_fin.keys())

    mire_fin = Mire(
        points,
        ids=ids,
        alignes=mire.alignes
    )

    lst_fin_inv = {}

    for id, pt in lst_xmr_fin.items():

        pt = np.array(pt)
        pt_rot_inv = best_rot_inv @ (pt - xm) + xm
        lst_fin_inv[id] = pt_rot_inv.tolist()

    points_inv = list(lst_fin_inv.values())
    ids_inv = list(lst_fin_inv.keys())

    mire_fin_inv = Mire(
        points_inv,
        ids = ids_inv,
        alignes = mire.alignes
    )

    return mire_fin, mire_fin_inv, xm, best_ym, best_ym_inv
    

def thd_process(mire,screen,obs,xm,ym,N):
<<<<<<< HEAD
    """Entrées: la mire qui a été fixée correctement,l'écran en dico avec ses 4 attrributs : vect normal , origine et vect directeurs, les pts xm, ym bien fixés et N constante de discrétisation de l'intervalle des angles 
=======
    """Entrées: la mire qui a été fixée correctement,le vecteur normal au plan, l'observation originale, 
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae
    xm et ym qui sont sur notre axe de rotation N pour la discrétisation des angles """
    
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    
    ym_xm = ym - xm

    eps = 1e-4

    best_rms = np.inf
<<<<<<< HEAD
    #best_mire = None
    #best_angle = None
=======
    best_mire = None
    best_angle = None
    axis = ym_xm / np.linalg.norm(ym_xm)
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae

    for agl in angles:
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
            #best_mire = new_mire
            #best_angle = agl

        if rms < eps:
            break

<<<<<<< HEAD
    return  best_rms, agl
    """( best_mire,"""
    """, best_angle)"""
=======
    return (best_mire, best_rms, best_angle)
           
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae

def app_proc(mire,obs,screen,xo,yo): 
        
    pts_items = list(mire.pts.items())
    d_obs = np.linalg.norm(yo - xo)
    best_score = np.inf
    best_mire = None
    best_xm = None
    best_ym = None
    best_agl = 0
<<<<<<< HEAD

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

                # process 3
                score , agl = thd_process(
                    mire2,
                    screen,
                    obs,
                    xm2,
                    ym2,
                    360
                )

                # meilleur résultat
                if score < best_score:

                    best_score = score
                    best_agl = agl
                    best_mire = mire2
                    best_xm = xm
                    best_ym = ym

        except Exception as e:

                print("Erreur couple :", id1, id2, e)

                continue

    return best_mire, best_xm, best_ym, best_score , best_agl



=======

    for (id1, xm), (id2, ym) in permutations(pts_items, 2):
        xm = np.array(xm)
        ym = np.array(ym)

        dist = np.linalg.norm(ym - xm)

        # conditions CORRIGEES !
        if dist <= 1e-8:
            continue

        if dist < d_obs:
            continue

        try:
                # process 1
                #print("entering 1st process")
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
                #print("entering 2nd process")
                # process 2
                mire2, mire2_inv, xm2, ym2, ym2_inv = scd_process(
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
                #print("entering 3rd process")
                # process 3 - positif
                mire3, score, agl = thd_process(
                    mire2,
                    screen,
                    obs,
                    xm2,
                    ym2,
                    360
                )
                # process 3 - négatif
                mire3_inv, score_inv, agl_inv = thd_process(
                    mire2_inv,
                    screen,
                    obs,
                    xm2,
                    ym2_inv,
                    360
                )

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

        if score_inv < best_score:
            best_score = score_inv
            best_agl = agl_inv
            best_mire = mire3_inv
            best_xm = xm
            best_ym = ym

    return best_mire, best_xm, best_ym, best_score, best_agl
>>>>>>> 0356f94f014ed87ce6f511eba4ca4909eb83edae
