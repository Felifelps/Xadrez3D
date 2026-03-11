from OpenGL.GL import *
from PIL import Image
import numpy as np


class Mesh:
    def __init__(
        self,
        obj_path,
        texture_path=None,
    ):
        self.load_obj(obj_path)

        self.texture_path = texture_path
        self.texture_id = self.load_texture(texture_path)

    def load_obj(self, path):
        vertex = []
        texcoords = []
        normals = []

        faces_v = []
        faces_vt = []
        faces_vn = []

        with open(path, "r", encoding="utf-8") as f:
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
                    faces_v.append([face_v[0], face_v[1], face_v[2]])
                    faces_vt.append([face_vt[0], face_vt[1], face_vt[2]])
                    faces_vn.append([face_vn[0], face_vn[1], face_vn[2]])

                    faces_v.append([face_v[0], face_v[2], face_v[3]])
                    faces_vt.append([face_vt[0], face_vt[2], face_vt[3]])
                    faces_vn.append([face_vn[0], face_vn[2], face_vn[3]])

        self.vertex = vertex
        self.texcoords = texcoords
        self.normals = normals
        self.faces_v = faces_v
        self.faces_vt = faces_vt
        self.faces_vn = faces_vn

        xs = [v[0] for v in vertex]
        ys = [v[1] for v in vertex]
        zs = [v[2] for v in vertex]

        self.bbox_min = (min(xs), min(ys), min(zs))
        self.bbox_max = (max(xs), max(ys), max(zs))

        self.__compute_contiguous_arrays()

    def load_texture(self, path):
        if not path:
            return None

        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGB").tobytes()

        width, height = img.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            img_data
        )

        return texture_id

    def compute_normal(self, a, b, c):
        ab = np.subtract(b, a)
        ac = np.subtract(c, a)
        n = np.cross(ab, ac)
        return n / np.linalg.norm(n)

    def __compute_contiguous_arrays(self):
        verts = []
        norms = []
        uvs = []

        for fv, fvt, fvn in zip(self.faces_v, self.faces_vt, self.faces_vn):
            for i in range(3):
                verts.append(self.vertex[fv[i]])

            if any(n is None for n in fvn):
                v0 = self.vertex[fv[0]]
                v1 = self.vertex[fv[1]]
                v2 = self.vertex[fv[2]]
                face_normal = self.compute_normal(v0, v1, v2)
                norms.extend([face_normal, face_normal, face_normal])
            else:
                for i in range(3):
                    norms.append(self.normals[fvn[i]])

            for i in range(3):
                index = fvt[i]
                if not index:
                    break
                uvs.append(self.texcoords[index])

        self.va_vertices = np.ascontiguousarray(verts, dtype=np.float32)
        self.va_normals  = np.ascontiguousarray(norms, dtype=np.float32)
        self.va_uvs = np.ascontiguousarray(uvs, dtype=np.float32)

        self.va_vertices_flat = self.va_vertices.flatten()
        self.va_normals_flat  = self.va_normals.flatten()
        self.va_uvs_flat = self.va_uvs.flatten()

        self.vertex_count = len(verts)
