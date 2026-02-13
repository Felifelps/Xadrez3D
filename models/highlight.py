from .mesh import Mesh


class HighlightModel(Mesh):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(
            obj_path="assets/highlight.obj",
            color=(0, 0, 0.5),
            pos=pos,
            rot=rot,
            scale=[s * 0.1 for s in scale]
        )
