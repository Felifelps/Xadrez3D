from OpenGL.GL import *
from ..mesh import Mesh

class Piece(Mesh):
    def __init__(self, color, pos, **kwargs):
        super().__init__(obj_path=None, **kwargs)
        self.color = color   
        self.pos = pos 
    def put_color(self):
        if self.color == 'white':
            glColor3f(0.9, 0.9, 0.9)
        else:
            glColor3f(0.1, 0.1, 0.1)
    def draw(self):
        pass

