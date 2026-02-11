from .piece import Piece

class Tower(Piece):
    def __init__(self, pos=(0,0,0), rot=(0,0,0), scale=1):
        super().__init__("assets/tower.obj", pos, rot, scale)