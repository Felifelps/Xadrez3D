from OpenGL.GL import *

class Piece:
    def __init__(self, color, pos=(0, 0, 0), rot=(0, 0, 0), scale=1):
        self.piece_color = color
        self.pos = list(pos)
        self.rot = list(rot)
        self.scale = scale
        
    def put_color(self):
        if self.piece_color == 'white':
            color = [0.9, 0.9, 0.9, 1.0]
        else:
            color = [0.1, 0.1, 0.1, 1.0]
        
        glColor3f(color[0], color[1], color[2])
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0)
        
    def draw(self):
        pass
    
    def keyboard(self, key, x, y): pass
    def special_keys(self, key, x, y): pass
    def mouse(self, button, state, x, y): pass
    def motion(self, x, y): pass
    def passive_motion(self, x, y): pass

