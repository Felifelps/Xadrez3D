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

        glEnable(GL_LIGHTING)
        glColor3f(*self.color)

        glBegin(GL_TRIANGLES)
        for pos, normal, uv in self.vertex:
            glNormal3f(float(normal[0]), float(normal[1]), float(normal[2]))
            glTexCoord2f(float(uv[0]), float(uv[1]))
            glVertex3f(float(pos[0]), float(pos[1]), float(pos[2]))
        glEnd()

        glPopMatrix()

    @classmethod
    def load_obj(path):
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