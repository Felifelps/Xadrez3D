import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from mesh import Mesh, Visualizable

WIDTH, HEIGHT = 800, 600
CLEAR_COLOR = (0.1, 0.1, 0.1, 1.0)


class App:
    def __init__(self):
        self.objects: list[Mesh] = []
        self.__init_opengl()

        # Carrega objeto
        obj = Visualizable("Rainha.obj")
        self.objects.append(obj)

    def __init_opengl(self):
        # Inicialização correta do GLUT (obrigatório no Windows)
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow(b"Xadrez3D")

        # OpenGL básico
        glClearColor(*CLEAR_COLOR)
        glEnable(GL_DEPTH_TEST)

        # Iluminação
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glShadeModel(GL_SMOOTH)

        glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.2, 0.2, 0.2, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 10.0, 10.0, 1.0))

        # Callbacks
        glutDisplayFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__keyboard)
        glutSpecialFunc(self.__special_keys)
        glutMouseFunc(self.__mouse)
        glutMotionFunc(self.__motion)
        glutPassiveMotionFunc(self.__passive_motion)

    def __reshape(self, w, h):
        if h == 0:
            h = 1

        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / float(h), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def __keyboard(self, key, x, y):
        for obj in self.objects:
            obj.keyboard(key, x, y)
        glutPostRedisplay()

    def __special_keys(self, key, x, y):
        for obj in self.objects:
            obj.special_keys(key, x, y)
        glutPostRedisplay()

    def __mouse(self, button, state, x, y):
        for obj in self.objects:
            obj.mouse(button, state, x, y)
        glutPostRedisplay()

    def __motion(self, x, y):
        for obj in self.objects:
            obj.motion(x, y)
        glutPostRedisplay()

    def __passive_motion(self, x, y):
        for obj in self.objects:
            obj.passive_motion(x, y)
        glutPostRedisplay()

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Câmera básica
        glTranslatef(0.0, 0.0, -5.0)

        for obj in self.objects:
            obj.draw()

        glutSwapBuffers()

    def run(self):
        glutMainLoop()


if __name__ == "__main__":
    app = App()
    app.run()
