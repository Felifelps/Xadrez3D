from .object import Object


class HighlightModel(Object):
    def __init__(self, target=False, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1), on_click=lambda: print("highlight_on_click")):
        super().__init__(
            obj_path="assets/highlight.obj",
            color=(0.5, 0, 0) if target else (0, 0, 0.5),
            pos=pos,
            rot=rot,
            scale=[s * 0.1125 for s in scale],
            opacity=0.5,
            on_click=on_click,
        )
