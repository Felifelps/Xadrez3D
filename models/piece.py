from OpenGL.GL import *
from .mesh import Mesh

class Piece(Mesh):
    def __init__(self, obj_path, pos=(0, 0, 0), rot=(0, 0, 0), scale=1):
        super().__init__(
            obj_path,
            pos=pos,
            rot=rot,
            scale=scale,
        )
