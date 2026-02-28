import numpy as np
from OpenGL.GL import *


POSITIONS = [
    -0.875,
    -0.625,
    -0.375,
    -0.125,
    0.875,
    0.625,
    0.375,
    0.125,
]

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

def load_obj(path):
    vertex = []
    texcoords = []
    normals = []

    faces_v = []
    faces_vt = []
    faces_vn = []

    with open(path, "r") as f:
        lines = f.read().split('\n')

    for line in lines:
        if line.startswith("v "):
            parts = line.split()
            x, y, z = parts[1:4]
            vertex.append((float(x), float(y), float(z)))

        elif line.startswith("vt "):
            parts = line.split()
            u, v = parts[1:3]
            texcoords.append((float(u), float(v)))

        elif line.startswith("vn "):
            _, nx, ny, nz = line.split()
            normals.append((float(nx), float(ny), float(nz)))

        elif line.startswith("f "):
            parts = line.split()[1:]
            
            face_v = []
            face_vt = []
            face_vn = []
            
            for p in parts:
                indices = p.split('/')
                
                vi = int(indices[0]) - 1
                face_v.append(vi)

                if len(indices) > 1 and indices[1] != '':
                    face_vt.append(int(indices[1]) - 1)
                else:
                    face_vt.append(None)

                if len(indices) == 3 and indices[2] != '':
                    face_vn.append(int(indices[2]) - 1)
                else:
                    face_vn.append(None)

            if len(face_v) == 3:
                faces_v.append(face_v)
                faces_vt.append(face_vt)
                faces_vn.append(face_vn)

            elif len(face_v) == 4:
                # Triângulo 1: v0, v1, v2
                faces_v.append([face_v[0], face_v[1], face_v[2]])
                faces_vt.append([face_vt[0], face_vt[1], face_vt[2]])
                faces_vn.append([face_vn[0], face_vn[1], face_vn[2]])

                # Triângulo 2: v0, v2, v3
                faces_v.append([face_v[0], face_v[2], face_v[3]])
                faces_vt.append([face_vt[0], face_vt[2], face_vt[3]])
                faces_vn.append([face_vn[0], face_vn[2], face_vn[3]])

    return vertex, texcoords, normals, faces_v, faces_vt, faces_vn

def convert_piece_pos(x, y):
    return POSITIONS[x], POSITIONS[y]
