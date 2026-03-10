from OpenGL.GL import *
from .mesh import Mesh

class Piece(Mesh):
    pass

class RookModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(1, 1, 1)):
        super().__init__(obj_path="assets/rook/rook.obj", pos=pos, rot=rot, scale=[s * 0.25 for s in scale])

class KnightModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(0.2, 0.2, 0.2)):
        super().__init__(obj_path="assets/knight/knightSimple.obj", pos=pos, rot=rot, scale=scale)

class BishopModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(0.2, 0.2, 0.2)):
        super().__init__(obj_path="assets/bishop/bishop.obj", pos=pos, rot=rot, scale=scale)

class PawnModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(0.075, 0.075, 0.075)):
        super().__init__(obj_path="assets/pawn/pawn.obj", pos=pos, rot=rot, scale=scale)

class KingModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(0.02, 0.02, 0.02)):
        super().__init__(obj_path="assets/king/king.obj", pos=pos, rot=rot, scale=scale)

class QueenModel(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=(0.02, 0.02, 0.02)):
        super().__init__(obj_path="assets/queen/queen.obj", pos=pos, rot=rot, scale=scale)