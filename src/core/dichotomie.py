import numpy as np
from src.core.projection import project_pt_to_plane
from src.core.transformation import calcul_matrice_rotation

def optimisation_dichotomie(pts, obs_3d, axis, xm2_rote, screen, u1, u2, tol=1e-3):
    """
    Algorithme de dichotomie (recherche ternaire) pour trouver l'angle 
    exact qui minimise l'erreur de projection de la mire.
    """
    gauche = 0.0
    droite = 360.0
    
    #Fonction interne pour calculer l'erreur maximale à un certain angle donné
    def calculer_erreur(angle_deg):
        theta_rad = np.deg2rad(angle_deg)
        mR = calcul_matrice_rotation(axis, theta_rad)
        
        pts_projetes = []
        for p in pts:
            pt_rot = mR @ (p - xm2_rote) + xm2_rote
            pt_proj = project_pt_to_plane(pt_rot, screen)
            pt_p3D = screen["origin"] + pt_proj[0]*u1 + pt_proj[1]*u2
            pts_projetes.append(pt_p3D)
            
        #Distance maximale entre la simulation et les observations réelles
        return np.max(np.linalg.norm(np.array(pts_projetes) - obs_3d, axis=1))

    #Boucle de recherche par séparation (Dichotomie/Ternaire)
    while (droite - gauche) > tol:
        m1 = gauche + (droite - gauche) / 3
        m2 = droite - (droite - gauche) / 3
        
        if calculer_erreur(m1) < calculer_erreur(m2):
            droite = m2  #L'erreur est plus petite à gauche, on élimine le tiers droit
        else:
            gauche = m1  #L'erreur est plus petite à droite, on élimine le tiers gauche
            
    return (gauche + droite) / 2

#dès qu'on a besoin de calculer l'angle par dichotomie 
# (que ce soit dans compare_test.py ou dans check_for_process.py)
#Et on l'appelle simplement comme ça
#best_angle = optimisation_dichotomie(pts, obs_3d, axis, xm2_rote, screen, u1, u2)
#print(f"Angle trouvé par dichotomie : {best_angle:.3f}°")