from OpenGL.GL import *

from .mesh import Mesh


class Object(Mesh):
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
        super().__init__(obj_path, texture_path)

        self.on_click = on_click

        self.color = list(color)
        self.base_color = list(color)

        self.pos = list(pos)
        self.base_pos = list(pos)

        self.rot = list(rot)
        self.base_rot = list(rot)

        self.scale = list(scale)
        self.base_scale = list(scale)

        self.opacity = opacity
        self.base_opacity = opacity

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

        glRotatef(self.rot[0], 1, 0, 0)
        glRotatef(self.rot[1], 0, 1, 0)
        glRotatef(self.rot[2], 0, 0, 1)

        glScalef(*self.scale)

        glTranslatef(-self.center[0], -self.center[1], -self.center[2])

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

        return self.ray_intersect_aabb(ray_origin, ray_dir, world_min, world_max)

    def ray_intersect_aabb(self, origin, direction, box_min, box_max):
        tmin = -1e9
        tmax =  1e9

        for i in range(3):
            if direction[i] != 0:
                t1 = (box_min[i] - origin[i]) / direction[i]
                t2 = (box_max[i] - origin[i]) / direction[i]

                tmin = max(tmin, min(t1, t2))
                tmax = min(tmax, max(t1, t2))

        if tmax >= max(0, tmin):
            return True, tmin

        return False, None

    def keyboard(self, key, x, y):
        pass

    def special_keys(self, key, x, y):
        pass

    def mouse(self, button, state, x, y):
        pass

    def motion(self, x, y):
        pass

    def passive_motion(self, x, y):
        pass

    def on_hover(self, is_hovered):
        value = 1.5 if is_hovered else 1
        self.color = [v * value for v in self.base_color]
