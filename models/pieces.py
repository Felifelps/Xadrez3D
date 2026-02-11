from OpenGL.GL import *
from .mesh import Mesh

class Piece(Mesh):
    pass

class Tower(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(1, 1, 1)):
        super().__init__(obj_path="assets/tower/tower.obj", pos=pos, rot=rot, scale=[s * 0.25 for s in scale])

class Knight(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(1, 1, 1)):
        super().__init__(obj_path="assets/knight/knight.obj", pos=pos, rot=rot, scale=scale)
