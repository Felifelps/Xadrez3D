import numpy as np
from OpenGL.GL import *

def compute_normal(a, b, c):
    ab = np.subtract(b, a)
    ac = np.subtract(c, a)
    n = np.cross(ab, ac)
    n = n / np.linalg.norm(n)
    return n

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def load_shader(vs_path, fs_path):
    with open(vs_path, "r") as f:
        vs_source = f.read()
    with open(fs_path, "r") as f:
        fs_source = f.read()

    vs = compile_shader(vs_source, GL_VERTEX_SHADER)
    fs = compile_shader(fs_source, GL_FRAGMENT_SHADER)

    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program).decode())

    glDeleteShader(vs)
    glDeleteShader(fs)

    return program

def perspective_matrix(fov, aspect, near, far):
    f = 1 / np.tan(np.radians(fov) / 2)
    return np.array([
        [f/aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)


def translation_matrix(x, y, z):
    return np.array([
        [1,0,0,x],
        [0,1,0,y],
        [0,0,1,z],
        [0,0,0,1]
    ], dtype=np.float32)

def scale_matrix(s):
    return np.array([
        [s,0,0,0],
        [0,s,0,0],
        [0,0,s,0],
        [0,0,0,1]
    ], dtype=np.float32)

def rotation_matrix_x(a):
    a = np.radians(a)
    return np.array([
        [1,0,0,0],
        [0,np.cos(a),-np.sin(a),0],
        [0,np.sin(a), np.cos(a),0],
        [0,0,0,1]
    ], dtype=np.float32)

def rotation_matrix_y(a):
    a = np.radians(a)
    return np.array([
        [np.cos(a),0,np.sin(a),0],
        [0,1,0,0],
        [-np.sin(a),0,np.cos(a),0],
        [0,0,0,1]
    ], dtype=np.float32)

def rotation_matrix_z(a):
    a = np.radians(a)
    return np.array([
        [np.cos(a),-np.sin(a),0,0],
        [np.sin(a), np.cos(a),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ], dtype=np.float32)
