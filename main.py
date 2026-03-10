from math import sin, cos, radians

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from models import *

WIDTH, HEIGHT = 800, 600
CLEAR_COLOR = (0.1, 0.1, 0.1, 1.0)

class App:
    def __init__(self):
        self.camera_distance = 2.5
        self.camera_theta = 0
        self.camera_y = 1.5
        self.camera_speed = 5

        self.__init_opengl()

        positions = [
            -0.875,
            -0.625,
            -0.375,
            -0.125,
            0.875,
            0.625,
            0.375,
            0.125,
        ]

        self.objects: list[Mesh] = [
            BoardModel(),
            RookModel(pos=(positions[0], 0, positions[0])),
            KnightModel(pos=(positions[1], 0, positions[0])),
            BishopModel(pos=(positions[2], 0, positions[0])),
            KingModel(pos=(positions[3], 0, positions[0])),
            QueenModel(pos=(positions[7], 0, positions[0])),
            BishopModel(pos=(positions[6], 0, positions[0])),
            KnightModel(pos=(positions[5], 0, positions[0])),
            RookModel(pos=(positions[4], 0, positions[0])),
            PawnModel(pos=(positions[0], 0, positions[1])),
            HighlightModel(pos=(positions[1], 0, positions[1])),
        ]

    def __init_opengl(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(WIDTH, HEIGHT)
        glutCreateWindow(b"Xadrez3D")

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

        self.__position_camera()

        for object in self.objects:
            object.draw()

        glutSwapBuffers()

    def __position_camera(self):
        theta = radians(self.camera_theta)

        x = self.camera_distance * sin(theta)
        z = self.camera_distance * cos(theta)

        gluLookAt(
            x, self.camera_y, z,
            0, 0, 0,
            0, 1, 0
        )

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
        if state == GLUT_DOWN:
            if button == 3:
                self.camera_distance -= 0.1
            elif button == 4:
                self.camera_distance += 0.1

            self.camera_distance = max(2.0, min(self.camera_distance, 3.0))

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            ray_origin, ray_direction = self.__make_ray_from_mouse(x, y)

            clicked = None
            min_dist = 1e9

            for obj in self.objects:
                if isinstance(obj, BoardModel):
                    continue

                hit, dist = obj.intersect_ray(ray_origin, ray_direction)

                if hit and dist < min_dist:
                    clicked = obj
                    min_dist = dist

            if clicked:
                obj.on_click()

        glutPostRedisplay()
    
    def __make_ray_from_mouse(self, mouse_x, mouse_y):
        # Pegando matrizes OpenGL atuais
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        # Inverte Y da tela: OpenGL usa origem no canto inferior
        mouse_y = viewport[3] - mouse_y

        # Ponto no near plane
        near_point = gluUnProject(mouse_x, mouse_y, 0.0, modelview, projection, viewport)

        # Ponto no far plane
        far_point = gluUnProject(mouse_x, mouse_y, 1.0, modelview, projection, viewport)

        # Direção = far - near
        dir_vector = (
            far_point[0] - near_point[0],
            far_point[1] - near_point[1],
            far_point[2] - near_point[2]
        )

        # Normaliza direção
        length = (dir_vector[0]**2 + dir_vector[1]**2 + dir_vector[2]**2)**0.5
        dir_vector = (dir_vector[0]/length, dir_vector[1]/length, dir_vector[2]/length)

        return near_point, dir_vector

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
