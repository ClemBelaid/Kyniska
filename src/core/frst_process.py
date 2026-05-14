import numpy as np 
import random
from .mire import Mire 
from .projection import project_mire_to_plane
from .projection import project_pt_to_plane
from .transformation import calcul_matrice_rotation

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

"""Après ça serait bien d'avoir des fonctions d'affichage de mire et de plan pour mieux visualiser le truc """


