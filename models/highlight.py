from .mesh import Mesh


class HighlightModel(Mesh):
    def __init__(self, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), on_click=lambda: print("highlight_on_click")):
        super().__init__(
            obj_path="assets/highlight.obj",
            color=(0, 0, 0.5),
            pos=pos,
            rot=rot,
            scale=[s * 0.1 for s in scale],
            on_click=on_click,
        )
