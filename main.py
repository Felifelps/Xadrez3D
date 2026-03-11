from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *
from game import *
from models import *
from utils import *
from graphics.camera_app import OpenGLCameraApp


class App(OpenGLCameraApp):

    def __init__(self):
        super().__init__("Xadrez3D")

        self.board_model = BoardModel()

        self.game = Game(
            on_reset=self.reset_game,
            on_move=self.update_pieces_meshes
        )

        self.game.reset()

    @property
    def objects(self):
        return [
            self.board_model,
            *list(self.piece_meshes.values()),
            *self.highlight_meshes,
        ]

    def reset_game(self):
        self.checkmate = False
        self.hovered_piece = None
        self.selected_piece = None
        self.piece_meshes = {}
        self.highlight_meshes = []

        self.update_pieces_meshes()

    def update_pieces_meshes(self):
        new_meshes = {}

        for piece in self.game.get_all_pieces():

            if piece.id in self.piece_meshes:
                mesh = self.piece_meshes[piece.id]
            else:
                template = PIECE_MESH_DATA[piece.symbol]
                piece_colors = PIECE_COLORS[piece.color]

                on_click = lambda p=piece: self.handle_piece_click(p)

                mesh = PieceModel(
                    obj_path=template.get("obj_path"),
                    scale=template.get("scale"),
                    rot=template.get("rot"),
                    colors=piece_colors,
                    on_click=on_click,
                )

                mesh.offset = template.get("pos_delta", (0, 0, 0))

            mod = 1 if piece.color == 1 else -1

            mesh.rot[1] *= mod

            pos = convert_piece_pos(*piece.pos)
            for i in range(3):
                pos[i] += mesh.offset[i]

            mesh.pos = pos

            print(piece, piece.pos, mesh.pos)
            new_meshes[piece.id] = mesh

        self.piece_meshes = new_meshes

        self.centralizing_camera = True

    def handle_piece_click(self, piece):
        self.highlight_meshes.clear()

        if self.selected_piece and self.selected_piece.color != piece.color:
            return self.handle_move(self.selected_piece.pos, piece.pos)

        if self.checkmate or piece.color != self.game.current_player:
            return

        self.selected_piece = piece

        for pos in piece.get_legal_moves():

            target = not isinstance(self.game.get_piece(*pos), Empty)
            on_click = lambda p=pos: self.handle_move(piece.pos, p)

            highlight = HighlightModel(
                target=target,
                pos=convert_piece_pos(*pos, base_y=0.07),
                on_click=on_click,
            )

            self.highlight_meshes.append(highlight)

    def handle_move(self, start, end):
        try:
            self.game.move(start, end)
            print(self.game)
            self.centralizing_camera = True
        except InCheckException as e:
            print(e)
        except CheckmateException as e:
            self.checkmate = True
            print(e)
        except ChessException as e:
            print(e)
        finally:
            self.clear_selection()

    def clear_selection(self):
        self.selected_piece = None
        self.highlight_meshes.clear()

    def centralize_camera(self):
        self.modifier = -1 if self.game.current_player == 0 else 1
        return super().centralize_camera()

    def display(self):
        super().display()

        for object in self.objects:
            object.draw()

    def keyboard(self, key, x, y):
        key = key.decode("utf-8")

        if key == "u":
            self.game.undo()

        if key == 'r':
            self.game.reset()

        if key == "w":
            self.camera_phi += 5
        if key == "a":
            self.camera_theta -= 5
        if key == "s":
            self.camera_phi -= 5
        elif key == "d":
            self.camera_theta += 5

        self.camera_phi = max(10, min(80, self.camera_phi))
        self.camera_theta %= 360

        if key == "c":
            self.centralizing_camera = True

        for object in self.objects:
            object.keyboard(key, x, y)

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        if state == GLUT_DOWN:
            if button == 3:
                self.camera_distance -= 0.1
            elif button == 4:
                self.camera_distance += 0.1

            self.camera_distance = max(2.0, min(self.camera_distance, 3.0))

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            ray_origin, ray_direction = make_ray_from_mouse(x, y)

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

    def passive_motion(self, x, y):
        ray_origin, ray_direction = make_ray_from_mouse(x, y)

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
