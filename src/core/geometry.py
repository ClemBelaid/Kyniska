import numpy as np

# Gérer le cas où nc = nb ou bien nd = nb (division par zéro)
def calculBirapport(a, b, c, d):
    """
    Entrée : points en 3D
    Sortie : birapport (a,b,c,d)
    """
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    nc = np.linalg.norm(c)
    nd = np.linalg.norm(d)
    return (nc-na)/(nc-nb)*(nd-na)/(nd-nb)

def perpendicular_vector(v):
    if v[1] == 0 and v[2] == 0:
        if v[0] == 0:
            raise ValueError('zero vector')
        else:
            return np.cross(v, [0, 1, 0])
    return np.cross(v, [1, 0, 0])
