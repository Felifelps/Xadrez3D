from OpenGL.GL import *
from PIL import Image
import numpy as np
import os

class Mesh:
    def __init__(
        self,
        vertex,
        texture_id=None,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=1.0,
        color=(1, 1, 1)
    ):
        self.vertex = vertex
        self.texture_id = texture_id
        self.pos = list(pos)
        self.rot = list(rot)
        self.scale = scale
        self.color = list(color)

    def draw(self):
        glPushMatrix()

        glTranslatef(*self.pos)
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)

        # se tiver textura → desliga iluminação (mais simples)
        if self.texture_id is not None:
            glDisable(GL_LIGHTING)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
        else:
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_LIGHTING)
            glColor3f(*self.color)

        glBegin(GL_TRIANGLES)
        for pos, normal, uv in self.vertex:
            glNormal3f(float(normal[0]), float(normal[1]), float(normal[2]))
            glTexCoord2f(float(uv[0]), float(uv[1]))
            glVertex3f(float(pos[0]), float(pos[1]), float(pos[2]))
        glEnd()

        glPopMatrix()

    @staticmethod
    def load_texture(path):
        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img = img.convert("RGBA")
        img_data = img.tobytes()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            img.width, img.height, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, img_data
        )

        return texture_id


    @classmethod
    def load_obj_with_mtl(cls, obj_path):
        base_dir = os.path.dirname(obj_path)

        verts = []
        normals = []
        uvs = []
        faces = []
        texture_file = None

        with open(obj_path, "r") as f:
            for line in f:
                if line.startswith("mtllib"):
                    _, mtl_file = line.split()
                    texture_file = cls.parse_mtl(os.path.join(base_dir, mtl_file))

                elif line.startswith("v "):
                    _, x, y, z = line.split()
                    verts.append((float(x), float(y), float(z)))

                elif line.startswith("vn "):
                    _, x, y, z = line.split()
                    normals.append((float(x), float(y), float(z)))

                elif line.startswith("vt "):
                    parts = line.split()
                    if len(parts) == 3:
                        _, u, v = parts
                        uvs.append((float(u), float(v)))
                    elif len(parts) == 4:
                        _, u, v, w = parts
                        uvs.append((float(u), float(v)))

                elif line.startswith("f "):
                    parts = line.strip().split()[1:]
                    face = []
                    for p in parts:
                        items = p.split("/")
                        v = int(items[0]) - 1
                        t = int(items[1]) - 1 if len(items) > 1 and items[1] else -1
                        n = int(items[2]) - 1 if len(items) > 2 and items[2] else -1
                        face.append((v, t, n))
                    faces.append(face)

        vertex_list = []

        for f in faces:
            # Triangula quads
            if len(f) == 4:
                tri = [f[0], f[1], f[2], f[0], f[2], f[3]]
            else:
                tri = f

            for (vi, ti, ni) in tri:
                pos = verts[vi]
                uv = uvs[ti] if ti >= 0 else (0, 0)
                normal = normals[ni] if ni >= 0 else (0, 0, 1)
                vertex_list.append((pos, normal, uv))

        texture_id = None
        if texture_file:
            texture_id = cls.load_texture(os.path.join(base_dir, texture_file))

        return vertex_list, texture_id

    @staticmethod
    def parse_mtl(path):
        texture = None
        with open(path, "r") as f:
            for line in f:
                if line.startswith("map_Kd"):
                    _, tex = line.split()
                    texture = tex.strip()
        return texture

    def keyboard(self, key, x, y): pass
    def special_keys(self, key, x, y): pass
    def mouse(self, button, state, x, y): pass
    def motion(self, x, y): pass
    def passive_motion(self, x, y): pass