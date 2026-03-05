from math import sin, cos, radians

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from models import *
from game import *

WIDTH, HEIGHT = 800, 600
CLEAR_COLOR = (0.1, 0.1, 0.1, 1.0)

PIECE_MESH_DATA = {
    "r": {
        "obj_path": "assets/rook/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "k": {
        "obj_path": "assets/rook/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "b": {
        "obj_path": "assets/rook/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "Q": {
        "obj_path": "assets/rook/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "K": {
        "obj_path": "assets/rook/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "p": {
        "obj_path": "assets/rook/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
}

class App:
    def __init__(self):
        self.base_camera_theta = 90
        self.min_camera_distance = 2
        self.max_camera_distance = 5
        self.is_moving = False

        self.camera_distance = self.min_camera_distance
        self.camera_theta = self.base_camera_theta
        self.camera_y = 1.5
        self.camera_speed = 5

        self.__init_opengl()

        self.board_model = BoardModel()
        self.game: Game = Game(on_reset=self.on_reset_game)
        self.game.reset()

    def on_reset_game(self):
        self.checkmate = False
        self.hovered_piece = None
        self.selected_piece = None
        self.piece_meshes = {}
        self.highlight_meshes = []

        for piece in self.game.get_all_pieces():
            color = piece.color if piece.color == 1 else 0.25

            self.piece_meshes[piece] = Mesh(
                **PIECE_MESH_DATA[piece.symbol],
                pos=convert_piece_pos(*piece.pos),
                color=(color, color, color),
                on_click=lambda p=piece: self.handle_piece_click(p)
            )

    def handle_piece_click(self, piece):
        print("Clicou em", piece)
        self.highlight_meshes.clear()

        if self.selected_piece and self.selected_piece.color != piece.color:
            self.handle_move(self.selected_piece.pos, piece.pos, piece)
            return

        if self.checkmate or piece.color != self.game.current_player:
            return

        self.clear_selection()

        self.selected_piece = piece

        for pos in piece.get_legal_moves():

            highlight = HighlightModel(
                target=self.game.get_piece(*pos).color == 1 - self.selected_piece.color,
                pos=convert_piece_pos(*pos),
                on_click=lambda p=pos: self.handle_move(piece.pos, p, self.game.get_piece(*pos))
            )
    
            self.highlight_meshes.append(highlight)

    def handle_move(self, start, end, target_piece):
        try:
            self.game.move(start, end)
            self.piece_meshes.pop(target_piece, "It was empty")

            self.clear_selection()
        except InCheckException:
            self.clear_selection()
        except CheckmateException:
            self.checkmate = True
            self.clear_selection()
        except ChessException as e:
            print(e)

    def clear_selection(self):
        self.selected_piece = None
        self.highlight_meshes.clear()

    @property
    def objects(self):
        return list(self.piece_meshes.values()) + self.highlight_meshes

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
        glutCloseFunc(quit)

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        self.__position_camera()

        self.board_model.draw()

        for piece in self.game.get_all_pieces():
            self.piece_meshes[piece].pos = convert_piece_pos(*piece.pos)
            self.piece_meshes[piece].draw()

        for highlight_mesh in self.highlight_meshes:
            highlight_mesh.draw()

        glutSwapBuffers()
        glutPostRedisplay()

    def __position_camera(self):
        if not self.is_moving:
            modifier = -1 if self.game.current_player == 0 else 1
            target_theta = self.base_camera_theta * modifier

            self.camera_theta += (target_theta - self.camera_theta) * 0.075

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

        if key == 'r':
            self.game.reset()

        if key == "m":
            self.is_moving = not self.is_moving

        if self.is_moving:
            if key == 'a':
                self.camera_theta += self.camera_speed
            if key == 'd':
                self.camera_theta -= self.camera_speed

        self.camera_theta %= 360

        self.board_model.keyboard(key, x, y)

        for piece_mesh in self.piece_meshes.values():
            piece_mesh.keyboard(key, x, y)

        glutPostRedisplay()

    def __special_keys(self, key, x, y):
        for piece_mesh in self.piece_meshes.values():
            piece_mesh.special_keys(key, x, y)

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

            for object in self.objects:
                hit, dist = object.intersect_ray(ray_origin, ray_direction)

                if hit and dist < min_dist:
                    clicked = object
                    min_dist = dist

            if clicked:
                clicked.on_click()

        glutPostRedisplay()

    def __make_ray_from_mouse(self, mouse_x, mouse_y):
        # Pegando matrizes OpenGL atuais
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)

        # Inverte Y da tela: OpenGL usa origem no canto inferior
        mouse_y = viewport[3] - mouse_y - 1

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
        for piece_mesh in self.piece_meshes.values():
            piece_mesh.motion(x, y)

        glutPostRedisplay()

    def __passive_motion(self, x, y):
        ray_origin, ray_direction = self.__make_ray_from_mouse(x, y)

        hovered = None
        min_dist = 1e9

        for obj in self.objects:
            hit, dist = obj.intersect_ray(ray_origin, ray_direction)
            if hit and dist < min_dist:
                hovered = obj
                min_dist = dist

        if hovered != self.hovered_piece:
            if self.hovered_piece:
                self.hovered_piece.on_hover(False)

            if hovered:
                hovered.on_hover(True)

            self.hovered_piece = hovered

        glutPostRedisplay()

    def run(self):
        glutMainLoop()

if __name__ == '__main__':
    app = App()
    app.run()
