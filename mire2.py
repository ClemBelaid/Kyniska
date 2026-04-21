def generer_cone_tronque(cls, nb_billes, rayon_base=100.0, rayon_sommet=50.0, hauteur=30.0):
    points = []
    for _ in range(nb_billes):
        z = np.random.uniform(0, hauteur)
        rayon_max_z = rayon_base + (z / hauteur) * (rayon_sommet - rayon_base)
        r = rayon_max_z * np.sqrt(np.random.uniform(0, 1))
        theta = np.random.uniform(0, 2 * np.pi)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        points.append([x,y,z])
    return cls(points)
