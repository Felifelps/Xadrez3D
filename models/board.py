from OpenGL.GL import *
from .mesh import Mesh

class Board(Mesh):
    def __init__(self, rotation_speed=10, pos=(0, 0, 0), rot=(0, 0, 0), scale=1):
        self.rotation_speed = rotation_speed
        self.textures = [
            'assets/chess_board1.png',
            'assets/chess_board2.avif',
            'assets/chess_board3.jpg',
        ]
        self.current_texture_index = 0

        super().__init__(
            obj_path='assets/board.obj',
            texture_path=self.textures[self.current_texture_index],
            pos=pos,
            rot=rot,
            scale=scale,
        )
        

    def keyboard(self, key, x, y):
        key = key.decode("utf-8")

        if key == "a": self.rot[1] -= self.rotation_speed
        if key == "d": self.rot[1] += self.rotation_speed
        if key == "w": self.rot[2] += self.rotation_speed
        if key == "s": self.rot[2] -= self.rotation_speed

        if key == "t":
            self.current_texture_index = (self.current_texture_index + 1) % len(self.textures)
            self.texture_id = self.load_texture(self.textures[self.current_texture_index])

        return super().keyboard(key, x, y)
