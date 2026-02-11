import numpy as np
from OpenGL.GL import *

def compute_normal(a, b, c):
    ab = np.subtract(b, a)
    ac = np.subtract(c, a)
    n = np.cross(ab, ac)
    n = n / np.linalg.norm(n)
    return n

def ray_intersect_aabb(origin, direction, box_min, box_max):
    tmin = -1e9
    tmax =  1e9

    for i in range(3):
        if direction[i] != 0:
            t1 = (box_min[i] - origin[i]) / direction[i]
            t2 = (box_max[i] - origin[i]) / direction[i]

            tmin = max(tmin, min(t1, t2))
            tmax = min(tmax, max(t1, t2))

    if tmax >= max(0, tmin):
        return True, tmin

    return False, None
