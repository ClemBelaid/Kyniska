import numpy as np

def perpendicular_vector(v):
    if v[1] == 0 and v[2] == 0:
        if v[0] == 0:
            raise ValueError('zero vector')
        else:
            return np.cross(v, [0, 1, 0])
    return np.cross(v, [1, 0, 0])


def build_basis(v):
    v = np.array(v, dtype=float)
    v = v / np.linalg.norm(v)

    ref = np.array([1.0, 0.0, 0.0])

    # si trop colinéaire, changer de référence
    if abs(np.dot(ref, v)) > 0.9:
        ref = np.array([0.0, 1.0, 0.0])

    u1 = np.cross(v, ref)
    u1 = u1 / np.linalg.norm(u1)

    u2 = np.cross(v, u1)
    u2 = u2 / np.linalg.norm(u2)

    return u1, u2
