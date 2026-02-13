from OpenGL.GL import *
from .mesh import Mesh

class BoardModel(Mesh):
    def __init__(self, rotation_speed=10, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.rotation_speed = rotation_speed
        self.textures = [
            'assets/board/chess_board1.png',
            'assets/board/chess_board2.png',
            'assets/board/chess_board3.png',
        ]
        self.current_texture_index = 0

        super().__init__(
            obj_path='assets/board/board.obj',
            texture_path=self.textures[self.current_texture_index],
            pos=pos,
            rot=rot,
            scale=scale,
        )
        

    def keyboard(self, key, x, y):
        if key == "t":
            self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
            self.texture_id = self.load_texture(self.textures[self.current_texture_index])

        return super().keyboard(key, x, y)
