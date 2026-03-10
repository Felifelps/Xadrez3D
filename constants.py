WIDTH, HEIGHT = 800, 600
CLEAR_COLOR = (0.1, 0.1, 0.1, 1.0)

BASE_Y = 0.225

PIECE_MESH_DATA = {
    "r": {
        "obj_path": "assets/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "k": {
        "obj_path": "assets/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "b": {
        "obj_path": "assets/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
    "Q": {
        "obj_path": "assets/queen.obj",
        "rot": (0, 0, 0),
        "scale": (0.2, 0.225, 0.2)
    },
    "K": {
        "obj_path": "assets/king.obj",
        "rot": (-90, 0, 90),
        "scale": (0.015, 0.015, 0.015)
    },
    "p": {
        "obj_path": "assets/rook.obj",
        "rot": (0, 0, 0),
        "scale": (0.25, 0.25, 0.25)
    },
}

BOARD_TEXTURES = [
    'assets/board/chess_board1.png',
    'assets/board/chess_board2.png',
    'assets/board/chess_board3.png',
]

PIECE_COLORS = {
    0: (
        (0.25, 0.25, 0.25),
        (0.5, 0.4, 0.3),
        (0.6, 0.1, 0.15),
    ),
    1: (
        (1, 1, 1),
        (0.8, 0.7, 0.55),
        (0.96, 0.67, 0.94),
    ),
}

POSITIONS = [
    -0.875,
    -0.625,
    -0.375,
    -0.125,
    0.125,
    0.375,
    0.625,
    0.875,
]