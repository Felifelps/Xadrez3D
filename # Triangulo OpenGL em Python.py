# Triangulo OpenGL em Python
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

# Inicializa a janela
def init():
    glClearColor(0.2, 0.0, 0.0, 0.0)  # Cor de fundo
    glColor3f(1.0, 0.0, 0.0)         # Cor do triângulo
    glPointSize(5.0)

# Função de desenho
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 0.0)  # vermelho
    glVertex3f(-0.5, -0.5, 0.0)
    
    glColor3f(0.0, 1.0, 0.0)  # verde
    glVertex3f(0.5, -0.5, 0.0)
    
    glColor3f(0.0, 0.0, 0.0)  # azul
    glVertex3f(0.0, 0.5, 0.0)
    glEnd()
    
    glutSwapBuffers()

# Configuração principal
glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(600, 600)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Triangulo OpenGL")
init()
glutDisplayFunc(draw)
glutMainLoop()
