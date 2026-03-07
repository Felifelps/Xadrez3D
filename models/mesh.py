from OpenGL.GL import *
from PIL import Image
import numpy as np
from utils import *

class Mesh:
    def __init__(
        self,
        obj_path,
        texture_path=None,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        color=(1, 1, 1),
        scale=(1, 1, 1),
        opacity=1,
        on_click=lambda: None,
    ):
        vertex, texcoords, normals, faces_v, faces_vt, faces_vn = load_obj(obj_path)

        self.texture_id = self.load_texture(texture_path)
        self.vertex = vertex
        self.texcoords = texcoords
        self.normals = normals
        self.faces_v = faces_v
        self.faces_vt = faces_vt
        self.faces_vn = faces_vn
        self.opacity = opacity

        self.on_click = on_click

        self.pos = list(pos)
        self.rot = list(rot)
        self.color = list(color)
        self.base_color = list(color)
        self.scale = list(scale)
        self.center = self.__compute_center()

        xs = [v[0] for v in vertex]
        ys = [v[1] for v in vertex]
        zs = [v[2] for v in vertex]

        self.bbox_min = (min(xs), min(ys), min(zs))
        self.bbox_max = (max(xs), max(ys), max(zs))

        self.__compute_contiguous_arrays()

    def __compute_contiguous_arrays(self):
        verts = []
        norms = []
        uvs = []

        for fv, fvt, fvn in zip(self.faces_v, self.faces_vt, self.faces_vn):
            for i in range(3):
                verts.append(self.vertex[fv[i]])

            if any(n is None for n in fvn):
                v0 = self.vertex[fv[0]]
                v1 = self.vertex[fv[1]]
                v2 = self.vertex[fv[2]]
                face_normal = compute_normal(v0, v1, v2)
                norms.extend([face_normal, face_normal, face_normal])
            else:
                for i in range(3):
                    norms.append(self.normals[fvn[i]])

            for i in range(3):
                index = fvt[i]
                if not index:
                    break
                uvs.append(self.texcoords[index])

        self.va_vertices = np.ascontiguousarray(verts, dtype=np.float32)
        self.va_normals  = np.ascontiguousarray(norms, dtype=np.float32)
        self.va_uvs = np.ascontiguousarray(uvs, dtype=np.float32)

        self.va_vertices_flat = self.va_vertices.flatten()
        self.va_normals_flat  = self.va_normals.flatten()
        self.va_uvs_flat = self.va_uvs.flatten()

        self.vertex_count = len(verts)

    def __compute_center(self):
        verts = np.array(self.vertex, dtype=float)
        center = np.mean(verts, axis=0)
        return center

    @classmethod
    def load_texture(cls, path):
        if not path:
            return None

        img = Image.open(path)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        img_data = img.convert("RGB").tobytes()

        width, height = img.size

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            img_data
        )

        return texture_id

    def draw(self):
        glPushMatrix()

        glColor4f(self.color[0], self.color[1], self.color[2], self.opacity)

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)
        else:
            glDisable(GL_TEXTURE_2D)

        glTranslatef(*self.pos)
        glTranslatef(*(-self.center))
        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)
        glTranslatef(*self.center)
        glScalef(*self.scale)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        if self.texture_id:
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glTexCoordPointer(2, GL_FLOAT, 0, self.va_uvs_flat)

        glVertexPointer(3, GL_FLOAT, 0, self.va_vertices_flat)
        glNormalPointer(GL_FLOAT, 0, self.va_normals_flat)

        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)

        if self.texture_id:
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()

    def intersect_ray(self, ray_origin, ray_dir):
        min_x, min_y, min_z = self.bbox_min
        max_x, max_y, max_z = self.bbox_max

        px, py, pz = self.pos
        sx, sy, sz = self.scale

        world_min = (
            px + min_x * sx,
            py + min_y * sy,
            pz + min_z * sz,
        )

        world_max = (
            px + max_x * sx,
            py + max_y * sy,
            pz + max_z * sz,
        )

        return ray_intersect_aabb(ray_origin, ray_dir, world_min, world_max)

    def keyboard(self, key, x, y): pass
    def special_keys(self, key, x, y): pass
    def mouse(self, button, state, x, y): pass
    def motion(self, x, y): pass
    def passive_motion(self, x, y): pass

    def on_hover(self, is_hovered):
        value = 1.5 if is_hovered else 1
        self.color = [v * value for v in self.base_color]
