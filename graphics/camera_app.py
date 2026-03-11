from math import sin, cos, radians

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from .opengl_app import BaseOpenGLApp


class OpenGLCameraApp(BaseOpenGLApp):

    def __init__(self, window_name="Untitled"):
        super().__init__(window_name)

        self.base_camera_theta = 90
        self.base_camera_phi = 45
        self.min_camera_distance = 3
        self.max_camera_distance = 5
        self.camera_transition_rate = 0.075
        self.camera_transition_modifier = 1
        self.centralizing_camera = False

        self.camera_distance = self.min_camera_distance
        self.camera_theta = self.base_camera_theta
        self.camera_phi = self.base_camera_phi
        self.camera_y = 2
        self.camera_speed = 5

    def display(self):

        if self.centralizing_camera:
            self.centralize_camera()

        theta = radians(self.camera_theta)
        phi = radians(self.camera_phi)

        x = self.camera_distance * cos(phi) * sin(theta)
        y = self.camera_distance * sin(phi)
        z = self.camera_distance * cos(phi) * cos(theta)

        gluLookAt(
            x, y, z,
            0, 0, 0,
            0, 1, 0
        )

        return super().display()

    def centralize_camera(self):
        target_theta = self.base_camera_theta * self.modifier
        target_phi = self.base_camera_phi
        target_distance = self.min_camera_distance

        diff_theta = target_theta - self.camera_theta
        diff_phi = target_phi - self.camera_phi
        diff_distance = target_distance - self.camera_distance

        self.camera_theta += diff_theta * self.camera_transition_rate
        self.camera_phi += diff_phi * self.camera_transition_rate
        self.camera_distance += diff_distance * self.camera_transition_rate

        if (
            abs(diff_theta) < 1
            and abs(diff_phi) < 1
            and abs(diff_distance) < 0.01
        ):
            self.centralizing_camera = False
