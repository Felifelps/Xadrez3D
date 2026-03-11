from OpenGL.GL import *
from .object import Object
from constants import BOARD_TEXTURES


class BoardModel(Object):
    current_texture_index = 0

    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):

        self.texture_paths = BOARD_TEXTURES

        self.texture_ids = [self.load_texture(path) for path in self.texture_paths]
        BoardModel.current_texture_index = 0

        super().__init__(
            obj_path='assets/board/board.obj',
            texture_path=self.texture_paths[0],
            pos=pos,
            rot=rot,
            scale=scale,
        )

    def keyboard(self, key, x, y):
        if key == "t":
            BoardModel.current_texture_index += 1 
            BoardModel.current_texture_index %= len(self.texture_paths)

            self.texture_id = self.texture_ids[BoardModel.current_texture_index]

        return super().keyboard(key, x, y)
