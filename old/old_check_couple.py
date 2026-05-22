
def check_couple(mire,screen,xo,yo,lambda_):
    best_score = np.inf
    best_pair = None
    
    d_obs = np.linalg.norm(np.array(yo - xo))
    # Distance des points "témoins" y0 et x0
    if np.linalg.norm(yo - xo) < 1e-8: # Erreur sur y0 et x0
        return None


    for _ in range(100):

        id1, id2 = random.sample(mire.ids.tolist(), 2)

        xm = np.array(mire.pts[id1])
        ym = np.array(mire.pts[id2])

        # Distance dans la mire
        dm = np.linalg.norm(ym - xm)
        if dm < d_obs : # Critère d'exclusion : si |ym - xm| < |y0 - x0|, on passe au suivant
            continue

        xp = project_pt_to_plane(xm, screen)
        yp = project_pt_to_plane(ym, screen)

        # Distance projetée  
        d = np.linalg.norm(yp - xp)

        if d < 1e-8: # Si la distance projetée est quasi-nulle : les deux points se superposent -> exclusion
            continue

        u_obs = (yo - xo) / np.linalg.norm(yo - xo)
        u_mire = (yp - xp) / np.linalg.norm(yp - xp)

        score = abs(d - d_obs) / d_obs - lambda_ * np.dot(u_mire, u_obs)

        if score < best_score:
            best_score = score
            best_pair = (id1, id2)
    id1, id2 = best_pair
    xm = mire.pts[id1]
    ym = mire.pts[id2]
    return (xm,ym)