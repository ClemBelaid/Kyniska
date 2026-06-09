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
from src.core.check_for_process import check_couple




def frst_process(mire, screen, xm, ym, xo, yo):
    """ Entrées: la mire , l'écran un dico avec ses paramètres(origine, vecteur normal vn et vecteurs directeurs u1 et u2), les 2 points de la mire avec lesquels 
     on va faire le fixing et les 2 points fixés de l'écran.
        Sorties:La mire obtenue après la translation et la rotation  les points xm, ym après la transformation et la liste des points de la mire transformés"""
    
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
    

    lst_xmire_fin = {}
    for id, x_mire in lst_xmire_trs.items() :
         x_mire = np.array(x_mire)
         x_mire_rote = mat_rot @ (x_mire - xm_trs) + xm_trs
         lst_xmire_fin[id]= x_mire_rote.tolist()
    
    xm_rote= xm_trs
    
    #ym_trs = np.array(ym_trs)
    ym_rote= mat_rot @ (ym_trs - xm_trs) + xm_trs

    ######################################
    points = list(lst_xmire_fin.values())
    ids = list(lst_xmire_fin.keys())

    return (Mire(points, ids=ids, alignes=mire.alignes), xm_rote , ym_rote, lst_xmire_fin)

def scd_process(mire, screen, lst_xmr_fin, xm, ym, xo, yo):
    
    vn = screen["normal"]
    u1 = screen["u1"]
    u2 = screen["u2"]
    
    points = mire.points

    yo_xo = yo - xo
    yo_xo = yo_xo[0] * screen["u1"] + yo_xo[1] * screen["u2"]
    ym_xm = ym - xm

    b = np.linalg.norm(yo_xo)
    c = np.linalg.norm(ym_xm)
    a = np.sqrt(c**2 - b**2)

    # Calcul de l'angle phi entre le vecteur ym_xm et l'écran
    ym_xm = ym - xm
    sin_phi = np.dot(ym_xm, vn)
    ym_xm[2] = 0
    cos_phi = np.linalg.norm(ym_xm)
    phi = np.arctan2(sin_phi, cos_phi)

    angle = theta - phi
    mat_rot = calcul_matrice_rotation(axis, -angle)

    angle_inv = -(theta + phi)
    mat_rot_inv = calcul_matrice_rotation(axis, -angle_inv)

    # -----------------------------------------
    # Rotation finale de toute la mire
    # -----------------------------------------
    lst_fin = {}

    for id, pt in lst_xmr_fin.items():

        pt = np.array(pt)
        pt_rot = mat_rot @ (pt - xm) + xm
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
        pt_rot_inv = mat_rot_inv @ (pt - xm) + xm
        lst_fin_inv[id] = pt_rot_inv.tolist()

    points_inv = list(lst_fin_inv.values())
    ids_inv = list(lst_fin_inv.keys())

    mire_fin_inv = Mire(
        points_inv,
        ids = ids_inv,
        alignes = mire.alignes
    )

    best_ym = mat_rot @ (ym - xm) + xm
    best_ym_inv = mat_rot_inv @ (ym - xm) + xm

    return mire_fin, mire_fin_inv, xm, best_ym, best_ym_inv
    

def thd_process(mire,screen,obs,xm,ym,N):
    """ Entrées: la mire , l'écran un dico avec ses paramètres(origine, vecteur normal vn et vecteurs directeurs u1 et u2), l'observation référence , les 2 points de la mire obtenus après frst et scd process 
     et N pour la discrétisation de l'intervalle des angles.
        Sorties:la mire à la position qui colle le mieux avec l'observation référence , l'angle obtenu et l'erreur  """
    
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    
    ym_xm = ym - xm

    eps = 1e-4

    best_rms = np.inf
    best_mire = None
    best_angle = None
    axis = ym_xm / np.linalg.norm(ym_xm)

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
            best_mire = new_mire
            best_angle = agl

        if rms < eps:
            break

    return (best_mire, best_rms, best_angle)
           

def app_proc(mire,obs,screen,xo,yo): 
    """ Entrées: la mire , l'observation référence ,  l'écran un dico avec ses paramètres(origine, vecteur normal vn et vecteurs directeurs u1 et u2), les 2 points 
    fixés de l'observation 
        Sorties:la pose de la mire qui colle le mieux avec l'observation référence , les candidats xm et ym qui donnent cette meilleure pose l'angle obtenu, l'erreur et l'angle  """   
    pts_items = list(mire.pts.items())
    d_obs = np.linalg.norm(yo - xo)
    best_score = np.inf
    best_mire = None
    best_xm = None
    best_ym = None
    best_agl = 0

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
