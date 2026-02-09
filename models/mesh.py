from OpenGL.GL import *
from PIL import Image
import numpy as np
from utils import compute_normal

class Mesh:
    def __init__(
        self,
        obj_path,
        texture_path=None,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        color=(1, 1, 1),
        scale=1,
        gl_type=GL_TRIANGLES,
    ):
        vertex, texcoords, normals, faces_v, faces_vt, faces_vn = self.load_obj(obj_path)

        self.gl_type = gl_type
        self.texture_id = self.load_texture(texture_path)
        self.vertex = vertex
        self.texcoords = texcoords
        self.normals = normals
        self.faces_v = faces_v
        self.faces_vt = faces_vt
        self.faces_vn = faces_vn

        self.pos = list(pos)
        self.rot = list(rot)
        self.color = list(color)
        self.scale = scale
        self.center = self.__compute_center()

        self.__compute_continuous_arrays()

    def __compute_continuous_arrays(self):
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
                face_normal = compute_normal(v0, v1, v2)
                norms.extend([face_normal, face_normal, face_normal])
            else:
                for i in range(3):
                    norms.append(self.normals[fvn[i]])

            for i in range(3):
                uvs.append(self.texcoords[fvt[i]])

        # ensure contiguous float32 arrays
        self.va_vertices = np.ascontiguousarray(verts, dtype=np.float32)
        self.va_normals  = np.ascontiguousarray(norms, dtype=np.float32)
        self.va_uvs = np.ascontiguousarray(uvs, dtype=np.float32)

        # flattened versions to be safe when passing to GL
        self.va_vertices_flat = self.va_vertices.flatten()
        self.va_normals_flat  = self.va_normals.flatten()
        self.va_uvs_flat = self.va_uvs.flatten()

        self.vertex_count = len(verts)

    def __compute_center(self):
        verts = np.array(self.vertex, dtype=float)
        center = np.mean(verts, axis=0)
        return center

    @classmethod
    def load_texture(cls, path):
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

    def draw(self):
        glPushMatrix()

        glColor3f(*self.color)

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        else:
            glDisable(GL_TEXTURE_2D)

        glTranslatef(*self.pos)
        glTranslatef(*(-self.center))
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)
        glTranslatef(*self.center)
        glScalef(self.scale, self.scale, self.scale)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        if self.texture_id:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glTexCoordPointer(2, GL_FLOAT, 0, self.va_uvs_flat)

        glVertexPointer(3, GL_FLOAT, 0, self.va_vertices_flat)
        glNormalPointer(GL_FLOAT, 0, self.va_normals_flat)

        glDrawArrays(self.gl_type, 0, self.vertex_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        if self.texture_id:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

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
                if line.startswith("v "):
                    _, x, y, z = line.split()
                    vertex.append((float(x), float(y), float(z)))

                elif line.startswith("vt "):
                    _, u, v = line.split()
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

    def keyboard(self, key, x, y): pass
    def special_keys(self, key, x, y): pass
    def mouse(self, button, state, x, y): pass
    def motion(self, x, y): pass
    def passive_motion(self, x, y): pass


class Visualizable(Mesh):
    def __init__(self, obj_path, rotation_speed=10, pos=(0, 0, 0), rot=(0, 0, 0), scale=1):
        super().__init__(obj_path, pos=pos, rot=rot, scale=scale)
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
