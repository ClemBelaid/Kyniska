import numpy as np 
import random
from .mire import Mire 
from .projection import project_mire_to_plane
from .projection import project_pt_to_plane
from .transformation import calcul_matrice_rotation
from .geometry import perpendicular_vector
from .check_observ import check_observ



def frst_process(mire,v,xo,yo):
    """ Entrées: la mire , le vecteur normal du plan écran et les 2 points fixés de l'écran
        Sorties:La mire obtenue après la translation et la rotation  les points xm, ym """
    eps = 1e-2
    #On fixe 2 points dans l'observation: nos xo et yo les 2 premiers points par exemple 
    
    #On suppose que d(xo,yo)>0 (xo et yo ne sont pas trop proches)
    #prendre 2 points au hasard de notre mire 
    id1, id2 = random.sample(mire.ids, 2)
    xm= mire.pts[id1]
    ym = mire.pts[id2]
    xp = project_pt_to_plane(xm,v)
    yp = project_pt_to_plane(ym,v)
    d=np.linalg.norm(yp - xp)
    d_fx = np.linalg.norm(yo - xo)
    while d==0 or d > d_fx:
        id1, id2 = random.sample(mire.ids, 2)
        xm= mire.pts[id1]
        ym = mire.pts[id2]
        xp = project_pt_to_plane(xm,v)
        yp = project_pt_to_plane(ym,v)
        d=np.linalg.norm(yp - xp)
    #A ce stade on a un couple (xm,ym) candidat potentiel à la projection de (xo,yo)
    #On applique alors la translation de vecteur xpxo à la mire 
    xp_xo = xo - xp 
    mat_trs = np.array([[1,0,0,xp_xo[0],[0,1,0,xp_xo[1]],[0,0,1,50],[0,0,0,1]]])
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
    yp_prim = project_pt_to_plane(ym_trs,v)
    yo_xo = yo-xo
    ypp_xo = yp_prim - xo 
    u_xmxo= np.cross(yo_xo,ypp_xo)
    cos_a = np.dot(yo_xo,ypp_xo) / (np.linalg.norm(yo_xo) * np.linalg.norm(ypp_xo))
    a = np.arccos(cos_a)
    mat_rot = calcul_matrice_rotation(u_xmxo,a)
    ###########################################################
    lst_xmire_fin = {}
    for id, x_mire in lst_xmire_trs :
         x_mire_homo= np.array(x_mire + [1])
         x_mire_rote_homo= mat_rot @ x_mire_homo
         lst_xmire_fin[id]= (x_mire_rote_homo[:3] / x_mire_rote_homo[3]).tolist()
    ###################################
    xm_homo = np.array(xm_trs + [1])
    xm_rote_homo= mat_rot @ xm_homo
    xm_rote=  xm_rote_homo[:3] /  xm_rote_homo[3] 
    
    ym_homo = np.array(ym_trs + [1])
    ym_rote_homo= mat_rot @ ym_homo
    ym_rote =  ym_rote_homo[:3] /  ym_rote_homo[3]
    ######################################
    points = list(lst_xmire_fin.values())
    ids = list(lst_xmire_fin.keys())

    return (Mire(points, ids=ids, alignes=mire.alignes), xm_rote , ym_rote, lst_xmire_fin)



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

def thd_process(mire,v,obs,xm,ym,N):
    """Entrées: la mire qui a été fixée correctement,le vecteur normal au plan ,l'observation originale, 
    xm et ym qui sont sur notre axe de rotation N pour la discrétisation des angles """
    angles = np.linspace(0, 2*np.pi, N, endpoint=False)
    ym_xm = ym - xm 
    eps = 1e-6
    for agl in angles:
        mR = calcul_matrice_rotation(ym_xm, agl)
        lst_pt = {}
        for id, x_mire in mire.pts.items():
            x_mire_homo = np.array(x_mire + [1])
            x_mire_trs_homo= mR @ x_mire_homo
            lst_pt[id] = (x_mire_trs_homo[:3] / x_mire_trs_homo[3]).tolist()
        points = list(lst_pt.values())
        ids = list(lst_pt.keys())
        new_mire = Mire(points, ids=ids, alignes=mire.alignes)
        observ = project_mire_to_plane(new_mire,v)
        rms = check_observ(obs,observ)
        if rms < eps :
            break 
"""Après ça serait bien d'avoir des fonctions d'affichage de mire et de plan pour mieux visualiser le truc """