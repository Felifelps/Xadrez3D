

def validate_pos(pos):
    assert type(pos) in [tuple, list] and len(pos) == 2, 'Wrong pos'
    assert all((value > 0 and value < 8 for value in pos))


class Board:
    def __init__(self):
        self.reset_board()
    
    def reset_board(self):
        self.pieces: list[Piece] = [
            [Rook(color=0), Knight(color=0), Bishop(color=0), Queen(color=0), King(color=0), Bishop(color=0), Knight(color=0), Rook(color=0)],
            [Pawn(color=0) for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Pawn(color=1) for _ in range(8)],
            [Rook(color=1), Knight(color=1), Bishop(color=1), Queen(color=1), King(color=1), Bishop(color=1), Knight(color=1), Rook(color=1)],
        ]

        for x in range(8):
            for y in range(8):
                piece = self.pieces[x][y]
                piece.x, piece.y = x, y
                piece.board = self

    def move(self, start, end):

        validate_pos(start)
        validate_pos(end)

        sx, sy = start
        ex, ey = end

        piece = self.pieces[sx][sy]

        piece.can_move_to(ex, ey)

        self.pieces[sx][sy] = Empty()
        self.pieces[ex][ey] = piece

        piece.x, piece.y = ex, ey

    def __str__(self):
        result = ""
        for row in self.pieces:
            result += "| "
            for piece in row:
                result += str(piece) + " "
            result += "|\n"
        return result

class Piece:
    symbol = "-"
    def __init__(self, color = 1):
        self.board = None
        self.x = 0
        self.y = 0
        self.color = color

    def can_move_to(self, x, y):
        pass

    def __str__(self):
        return f"{self.symbol}{self.color}"

class Pawn(Piece):
    symbol = 'p'
    def can_move_to(self, x, y):
        pass

class Rook(Piece):
    symbol = 'r'
    def can_move_to(self, x, y):
        pass

class Knight(Piece):
    symbol = 'k'
    def can_move_to(self, x, y):
        pass

class Bishop(Piece):
    symbol = 'b'
    def can_move_to(self, x, y):
        pass

class Queen(Piece):
    symbol = 'Q'
    def can_move_to(self, x, y):
        pass

class King(Piece):
    symbol = 'K'
    def can_move_to(self, x, y):
        pass

class Empty(Piece):
    symbol = "·"
    def __init__(self):
        super().__init__(color='·')

    def can_move_to(self, x, y):
        raise Exception("Cant move from nowhere")



print(Board())