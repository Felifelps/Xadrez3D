from OpenGL.GL import *
from .mesh import Mesh

class Piece(Mesh):
    pass

class RookModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(1, 1, 1)):
        super().__init__(obj_path="assets/rook/rook.obj", pos=pos, rot=rot, scale=[s * 0.25 for s in scale])

class KnightModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(1, 1, 1)):
        super().__init__(obj_path="assets/knight/knight.obj", pos=pos, rot=rot, scale=scale)
