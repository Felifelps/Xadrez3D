from OpenGL.GL import *
from .mesh import Mesh

class BoardModel(Mesh):
    def __init__(self, rotation_speed=10, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.rotation_speed = rotation_speed

        self.texture_paths = [
            'assets/board/chess_board1.png',
            'assets/board/chess_board2.png',
            'assets/board/chess_board3.png',
        ]

        self.texture_ids = [self.load_texture(path) for path in self.texture_paths]

        self.current_texture_index = 0

        super().__init__(
            obj_path='assets/board/board.obj',
            texture_path=self.texture_paths[0],
            pos=pos,
            rot=rot,
            scale=scale,
        )
        

    def keyboard(self, key, x, y):
        if key == "t":
            self.current_texture_index = (self.current_texture_index + 1) % len(self.texture_paths)
            self.texture_id = self.texture_ids[self.current_texture_index]

        return super().keyboard(key, x, y)
