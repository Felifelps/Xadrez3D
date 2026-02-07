from OpenGL.GL import *
from PIL import Image
import numpy as np
from utils import compute_normal

class Mesh:
    def __init__(
        self,
        vertex,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=1.0,
        color=(1, 1, 1),
        gl_type=GL_TRIANGLES
    ):
        self.vertex = vertex
        self.pos = list(pos)
        self.rot = list(rot)
        self.scale = scale
        self.color = list(color)
        self.gl_type = gl_type
        self.center = self.compute_center()

        print("Min:", np.min(vertex, axis=0))
        print("Max:", np.max(vertex, axis=0))
        print("Center:", self.center)


    def compute_center(self):
        verts = np.array(self.vertex, dtype=float)
        center = np.mean(verts, axis=0)   # (cx, cy, cz)
        return center

    def draw(self):
        glPushMatrix()

        glTranslatef(*self.pos)

        glTranslatef(*(-self.center))

        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)

        glTranslatef(*self.center)

        glScalef(self.scale, self.scale, self.scale)

        glColor3f(*self.color)

        glBegin(self.gl_type)
        for i in range(0, len(self.vertex), 4):
            v0 = np.array(self.vertex[i])
            v1 = np.array(self.vertex[i+1])
            v2 = np.array(self.vertex[i+2])

            normal = compute_normal(v0, v1, v2)

            glNormal3f(*normal)

            for j in range(4):
                glVertex3f(*self.vertex[i+j])
        glEnd()

        glPopMatrix()

    @classmethod
    def load_obj(cls, path):
        vertices = []
        faces = []

        with open(path, "r") as f:
            for line in f:
                if line.startswith("v "):  # vértice
                    _, x, y, z = line.split()
                    vertices.append((float(x), float(y), float(z)))

                elif line.startswith("f "):  # face
                    parts = line.split()[1:]
                    face = [int(p.split("/")[0]) - 1 for p in parts]  # indices base 0
                    faces.append(face)

        vertex_list = []
        for face in faces:
            for idx in face:
                vertex_list.append(vertices[idx])

        return vertex_list


    def keyboard(self, key, x, y): pass
    def special_keys(self, key, x, y): pass
    def mouse(self, button, state, x, y): pass
    def motion(self, x, y): pass
    def passive_motion(self, x, y): pass


class Visualizable(Mesh):
    def __init__(self, obj_file, pos=(0, 0, 0), rot=(0, 0, 0), scale=1, color=(1, 1, 1)):
        vertex = self.load_obj(obj_file)
        super().__init__(vertex, pos, rot, scale, color, gl_type=GL_QUADS)

    def keyboard(self, key, x, y):
        key = key.decode("utf-8")
        if key == "a":
            self.rot[1] -= 5
        if key == "d":
            self.rot[1] += 5
        if key == "w":
            self.rot[0] -= 5
        if key == "s":
            self.rot[0] += 5

        return super().keyboard(key, x, y)
