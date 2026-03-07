from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *


class BaseOpenGLApp:

    def __init__(self, window_name="Untitled"):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow(window_name)

        glClearColor(*CLEAR_COLOR)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_TEXTURE_2D)

        glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.2, 0.2, 0.2, 1.0))

        glLightfv(GL_LIGHT0, GL_POSITION, (0, -5, -5, 1))

        glutDisplayFunc(lambda: self.__display())
        glutReshapeFunc(lambda w, h: self.__reshape(w, h))
        glutKeyboardFunc(lambda key, x, y: self.keyboard(key, x, y))
        glutMouseFunc(lambda button, state, x, y: self.mouse(button, state, x, y))
        glutPassiveMotionFunc(lambda x, y: self.passive_motion(x, y))
        glutCloseFunc(quit)

    def __reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluPerspective(45, w / float(h), 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        self.display()

        glutSwapBuffers()
        glutPostRedisplay()

    def display(self):
        pass

    def keyboard(self, key, x, y):
        pass

    def mouse(self, button, state, x, y):
        pass

    def passive_motion(self, x, y):
        pass

    def run(self):
        glutMainLoop()
