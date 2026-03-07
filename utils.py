from OpenGL.GL import *
from OpenGL.GLU import *

from constants import POSITIONS


def convert_piece_pos(x, y):
    return [POSITIONS[x], 0, POSITIONS[y]]

def make_ray_from_mouse(mouse_x: float, mouse_y: float):

    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    mouse_y = viewport[3] - mouse_y - 1

    near_point = gluUnProject(mouse_x, mouse_y, 0.0, modelview, projection, viewport)
    far_point = gluUnProject(mouse_x, mouse_y, 1.0, modelview, projection, viewport)

    dir_vector = (
        far_point[0] - near_point[0],
        far_point[1] - near_point[1],
        far_point[2] - near_point[2],
    )

    length = (dir_vector[0]**2 + dir_vector[1]**2 + dir_vector[2]**2) ** 0.5
    if length != 0:
        dir_vector = (dir_vector[0]/length, dir_vector[1]/length, dir_vector[2]/length)

    return near_point, dir_vector
