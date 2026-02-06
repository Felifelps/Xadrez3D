import numpy as np

def compute_normal(a, b, c):
    ab = np.subtract(b, a)
    ac = np.subtract(c, a)
    n = np.cross(ab, ac)
    n = n / np.linalg.norm(n)
    return n