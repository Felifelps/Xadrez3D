from OpenGL.GL import *
from .object import Object

class PieceModel(Object):
    def __init__(
        self,
        obj_path,
        pos=(0, 0, 0),
        rot=(0, 0, 0),
        scale=(1, 1, 1),
        colors=[
            (1, 1, 1),
            (133, 12, 27),
        ],
        on_click=lambda: None
    ):

        self.colors = colors
        self.current_color_index = 0

        super().__init__(
            obj_path=obj_path,
            pos=pos,
            rot=rot,
            scale=scale,
            color=self.colors[self.current_color_index],
            on_click=on_click,
        )
        

    def keyboard(self, key, x, y):
        if key == "t":
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.base_color = self.color = self.colors[self.current_color_index]

        return super().keyboard(key, x, y)
