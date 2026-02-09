from OpenGL.GL import *
from .mesh import Mesh

class Board(Mesh):
    def __init__(self, rotation_speed=10, pos=(0, 0, 0), rot=(0, 0, 0), scale=1):
        super().__init__(
            obj_path='assets/board.obj',
            texture_path='assets/chess.png',
            pos=pos,
            rot=rot,
            scale=scale,
        )
        self.rotation_speed = rotation_speed

    def keyboard(self, key, x, y):
        key = key.decode("utf-8")

        if key == "a": self.rot[1] -= self.rotation_speed
        if key == "d": self.rot[1] += self.rotation_speed
        if key == "w": self.rot[2] += self.rotation_speed
        if key == "s": self.rot[2] -= self.rotation_speed

        return super().keyboard(key, x, y)
