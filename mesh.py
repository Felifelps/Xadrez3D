from OpenGL.GL import *
from PIL import Image
import numpy as np
from utils import compute_normal
import os

class Mesh:
    def __init__(self, obj_path, pos=(0,0,0), rot=(0,0,0), scale=1):
        vertex, texcoords, normals, faces_v, faces_vt, faces_vn = self.load_obj(obj_path)

        self.vertex = vertex
        self.texcoords = texcoords
        self.normals = normals
        self.faces_v = faces_v
        self.faces_vt = faces_vt
        self.faces_vn = faces_vn

        self.pos = list(pos)
        self.rot = list(rot)
        self.scale = scale
        self.center = self.compute_center()

        verts = []
        norms = []

        for fv, fvn in zip(self.faces_v, self.faces_vn):
            for i in range(3):
                verts.append(self.vertex[fv[i]])

                if fvn[i] is not None:
                    norms.append(self.normals[fvn[i]])
                else:
                    norms.append((0,0,1))  # fallback

        self.va_vertices = np.array(verts, dtype=np.float32)
        self.va_normals  = np.array(norms, dtype=np.float32)
        self.vertex_count = len(verts)

        print("Min:", np.min(vertex, axis=0))
        print("Max:", np.max(vertex, axis=0))
        print("Center:", self.center)


    def compute_center(self):
        verts = np.array(self.vertex, dtype=float)
        center = np.mean(verts, axis=0)   # (cx, cy, cz)
        return center

    @classmethod
    def load_texture(cls, path):
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)  # IMPORTANTÍSSIMO no OpenGL
        img_data = img.convert("RGB").tobytes()

        width, height = img.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

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

    def draw(self):
        glPushMatrix()

        glDisable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1)

        glTranslatef(*self.pos)
        glTranslatef(*(-self.center))
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)
        glTranslatef(*self.center)
        glScalef(self.scale, self.scale, self.scale)

        # ---- DESENHO OTIMIZADO ----
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, self.va_vertices)
        glNormalPointer(GL_FLOAT, 0, self.va_normals)

        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        # ----------------------------

        glPopMatrix()


    @classmethod
    def load_obj(cls, path):
        vertex = []
        texcoords = []
        normals = []

        faces_v = []
        faces_vt = []
        faces_vn = []

        with open(path, "r") as f:
            for line in f:
                if line.startswith("v "):                     # posição
                    _, x, y, z = line.split()
                    vertex.append((float(x), float(y), float(z)))

                elif line.startswith("vt "):                 # UV
                    _, u, v, _ = line.split()
                    texcoords.append((float(u), float(v)))

                elif line.startswith("vn "):                 # normal
                    _, nx, ny, nz = line.split()
                    normals.append((float(nx), float(ny), float(nz)))

                elif line.startswith("f "):                  # face
                    parts = line.split()[1:]
                    
                    # parse v/vt/vn
                    face_v = []
                    face_vt = []
                    face_vn = []
                    
                    for p in parts:
                        indices = p.split('/')
                        
                        # pode ter formatos diferentes:
                        # v
                        # v/vt
                        # v//vn
                        # v/vt/vn
                        
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
                    
                    # Triangulação de QUAD (1,2,3,4 → 1-2-3 e 1-3-4)
                    if len(face_v) == 3:
                        faces_v.append(face_v)
                        faces_vt.append(face_vt)
                        faces_vn.append(face_vn)

                    elif len(face_v) == 4:
                        # tri 1: 0, 1, 2
                        faces_v.append([face_v[0], face_v[1], face_v[2]])
                        faces_vt.append([face_vt[0], face_vt[1], face_vt[2]])
                        faces_vn.append([face_vn[0], face_vn[1], face_vn[2]])

                        # tri 2: 0, 2, 3
                        faces_v.append([face_v[0], face_v[2], face_v[3]])
                        faces_vt.append([face_vt[0], face_vt[2], face_vt[3]])
                        faces_vn.append([face_vn[0], face_vn[2], face_vn[3]])

        vertex = np.array(vertex, dtype=float)

        center = np.mean(vertex, axis=0)
        vertex -= center   # centraliza na origem

        max_range = np.max(np.ptp(vertex, axis=0))
        vertex /= max_range  # deixa com escala ~1.0


        return vertex, texcoords, normals, faces_v, faces_vt, faces_vn


    def load_texture(self, path):
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGB").tobytes()

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB,
            img.width, img.height, 0,
            GL_RGB, GL_UNSIGNED_BYTE, img_data
        )

        return tex_id

    def keyboard(self, key, x, y): pass
    def special_keys(self, key, x, y): pass
    def mouse(self, button, state, x, y): pass
    def motion(self, x, y): pass
    def passive_motion(self, x, y): pass


class Visualizable(Mesh):
    def __init__(self, obj_path, rotation_speed=10, pos=(0, 0, 0), rot=(0, 0, 0), scale=1):
        super().__init__(obj_path, pos, rot, scale)
        self.rotation_speed = rotation_speed
        self.turn_left = False
        self.turn_right = False
        self.tilt_up = False
        self.tilt_down = False

    def keyboard(self, key, x, y):
        key = key.decode("utf-8")
        if key == "a": self.rot[1] += self.rotation_speed
        if key == "d": self.rot[1] -= self.rotation_speed
        if key == "w": self.rot[0] += self.rotation_speed
        if key == "s": self.rot[0] -= self.rotation_speed

        return super().keyboard(key, x, y)
