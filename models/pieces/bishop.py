from .base import Piece
from OpenGL.GL import *
from OpenGL.GLUT import *


class Bishop(Piece):
    def __init__(self, color, pos, rot=(0, 0, 0), scale=1):
        super().__init__(color, pos, rot, scale)

    def draw(self):
        glPushMatrix()
        glDisable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTranslatef(*self.pos)
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)
        self.put_color()
        # BASE
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(0.4, 0.1, 20, 20) 
        glPopMatrix()
        # Corpo
        glPushMatrix()
        glTranslatef(0, 0.05, 0)
        glRotatef(-90, 1, 0,0) 
        glutSolidCone(0.25, 0.8, 20, 20)
        glPopMatrix()
        # Pescoço
        glPushMatrix()
        glTranslatef(0, 0.7, 0)
        glRotatef(-90, 1, 0, 0)
        glutSolidTorus(0.05, 0.15, 10, 20)
        glPopMatrix()
        #Cabeça
        glPushMatrix()
        glTranslatef(0, 0.85, 0)
        glScalef(1.0, 1.4, 1.0)
        glutSolidSphere(0.18, 20, 20)
        glPopMatrix()
        # Bolinha do topo
        glPushMatrix()
        glTranslatef(0, 1.15, 0)
        glutSolidSphere(0.1, 20, 20)
        glPopMatrix()

        glPopMatrix()
    
    def keyboard(self, key, x, y):
        rotation_speed = 10
        key = key.decode("utf-8")
        
        if key == "a": self.rot[1] -= rotation_speed
        if key == "d": self.rot[1] += rotation_speed
        if key == "w": self.rot[2] += rotation_speed
        if key == "s": self.rot[2] -= rotation_speed
        