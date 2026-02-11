from math import sin, cos, radians

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from models import Mesh, Board, Tower

WIDTH, HEIGHT = 800, 600
CLEAR_COLOR = (0.1, 0.1, 0.1, 1.0)

class App:
    def __init__(self):
        self.__init_opengl()
        self.camera_distance = 2.5
        self.camera_theta = 0
        self.camera_y = 1.5
        self.camera_speed = 5

        self.objects: list[Mesh] = [
            Board(),
            Tower(pos=(-0.875, 0, -0.875), scale=0.25),
            Tower(pos=(-0.625, 0, -0.625), scale=0.25),
            Tower(pos=(-0.375, 0, -0.375), scale=0.25),
            Tower(pos=(-0.125, 0, -0.125), scale=0.25),
            Tower(pos=(0.875, 0, 0.875), scale=0.25),
            Tower(pos=(0.625, 0, 0.625), scale=0.25),
            Tower(pos=(0.375, 0, 0.375), scale=0.25),
            Tower(pos=(0.125, 0, 0.125), scale=0.25),
        ]

    def __init_opengl(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow("Xadrez3D")

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
        glutKeyboardFunc(lambda key, x, y: self.__keyboard(key, x, y))
        glutMouseFunc(lambda button, state, x, y: self.__mouse(button, state, x, y))
        glutSpecialFunc(lambda key, x, y: self.__special_keys(key, x, y))
        glutMotionFunc(lambda x, y: self.__motion(x, y))
        glutPassiveMotionFunc(lambda x, y: self.__passive_motion(x, y))

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        theta = radians(self.camera_theta)

        x = self.camera_distance * sin(theta)
        z = self.camera_distance * cos(theta)

        gluLookAt(
            x, self.camera_y, z,
            0, 0, 0,
            0, 1, 0
        )

        for object in self.objects:
            object.draw()

        glutSwapBuffers()

    def __reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        gluPerspective(45, w / float(h), 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)

    def __keyboard(self, key, x, y):
        key = key.decode("utf-8")

        if key == 'a':
            self.camera_theta += self.camera_speed
        if key == 'd':
            self.camera_theta -= self.camera_speed

        self.camera_theta %= 360

        

        for object in self.objects:
            object.keyboard(key, x, y)

        glutPostRedisplay()

    def __special_keys(self, key, x, y):
        for object in self.objects:
            object.special_keys(key, x, y)

        glutPostRedisplay()

    def __mouse(self, button, state, x, y):
        for object in self.objects:
            object.mouse(button, state, x, y)

        glutPostRedisplay()

    def __motion(self, x, y):
        for object in self.objects:
            object.motion(x, y)

        glutPostRedisplay()

    def __passive_motion(self, x, y):
        for object in self.objects:
            object.passive_motion(x, y)

        glutPostRedisplay()

    def run(self):
        glutMainLoop()

if __name__ == '__main__':
    app = App()
    app.run()
