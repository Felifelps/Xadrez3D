from OpenGL.GL import *
from OpenGL.GLU import *

class Rei:
    def __init__(self, x, z, cor=(1, 1, 1)): 
        self.x = x
        self.z = z
        self.cor = cor
        self.quadric = gluNewQuadric()
        gluQuadricNormals(self.quadric, GLU_SMOOTH)

    def desenhar(self):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glColor3fv(self.cor)

        # Tampa do corpo do Rei
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        gluDisk(self.quadric, 0, 0.5, 20, 1)
        glPopMatrix()

        # Corpo do Rei
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(self.quadric, 0.5, 0.3, 1.5, 20, 1)
        
        # Anel do Corpo
        glPushMatrix()
        glTranslatef(0, 0, 1.5)
        gluDisk(self.quadric, 0, 0.46, 20, 1)
        gluCylinder(self.quadric, 0.46, 0.46, 0.14, 20, 1)
        glTranslatef(0, 0, 0.14)
        gluDisk(self.quadric, 0, 0.46, 20, 1)
        glPopMatrix()
        
        # Cone da Cabeça
        glPushMatrix()
        glTranslatef(0, 0, 1.5)
        gluCylinder(self.quadric, 0.3, 0.44, 0.5, 20, 1)
        glTranslatef(0, 0, 0.5)
        gluDisk(self.quadric, 0, 0.44, 20, 1)
        glPopMatrix()

        # Cabeça do Rei
        glTranslatef(0, 0, 2)
        gluCylinder(self.quadric, 0.1, 0.1, 0.6, 20, 1)

        glPushMatrix()
        glTranslatef(0, 0, 0.6)
        gluDisk(self.quadric, 0, 0.1, 20, 1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, 0.3)
        glRotatef(90, 0, 1, 0)
        glTranslatef(0, 0, -0.3)
        gluCylinder(self.quadric, 0.1, 0.1, 0.6, 20, 1)
        glRotatef(180, 0, 1, 0)
        gluDisk(self.quadric, 0, 0.1, 20, 1)
        glTranslatef(0, 0, -0.6)
        glRotatef(-180, 0, 1, 0)
        gluDisk(self.quadric, 0, 0.1, 20, 1)
        glPopMatrix()

        glPopMatrix()
        glPopMatrix()