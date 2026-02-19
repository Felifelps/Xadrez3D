from contextlib import contextmanager


def validate_pos(pos):
    assert type(pos) in [tuple, list] and len(pos) == 2, 'Wrong pos'
    assert all(value >= 0 and value < 8 for value in pos)


class ChessException(Exception):
    pass

class Board:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.last_double_pawn = None
        self.current_player = 1

        self.kings = {
            0: King(color=0),
            1: King(color=1),
        }

        self.pieces: list[Piece] = [
            [Rook(color=0), Knight(color=0), Bishop(color=0), Queen(color=0), self.kings[0], Bishop(color=0), Knight(color=0), Rook(color=0)],
            [Pawn(color=0) for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Pawn(color=1) for _ in range(8)],
            [Rook(color=1), Knight(color=1), Bishop(color=1), Queen(color=1), self.kings[1], Bishop(color=1), Knight(color=1), Rook(color=1)],
        ]

        for x in range(8):
            for y in range(8):
                piece = self.pieces[x][y]
                piece.x, piece.y = x, y
                piece.board = self

    def get_piece(self, x, y):
        return self.pieces[x][y]

    def get_king_pos(self, color):
        return self.kings[color].pos

    def is_attacked_by(self, x, y, attacker_color):
        for row in self.pieces:
            for piece in row:
                if piece.color == attacker_color:
                    if piece.can_move_to(x, y):
                        return True
        return False

    def is_in_check(self, color):
        king_x, king_y = self.get_king_pos(color)
        enemy = 1 - color
        return self.is_attacked_by(king_x, king_y, enemy)

    @contextmanager
    def simulate_move(self, start, end):
        sx, sy = start
        ex, ey = end

        piece = self.pieces[sx][sy]
        captured = self.pieces[ex][ey]

        self.pieces[ex][ey] = piece
        self.pieces[sx][sy] = Empty()

        old_x, old_y = piece.x, piece.y
        piece.x, piece.y = ex, ey

        yield

        self.pieces[sx][sy] = piece
        self.pieces[ex][ey] = captured
        piece.x, piece.y = old_x, old_y

    def move(self, start, end):

        validate_pos(start)
        validate_pos(end)

        sx, sy = start
        ex, ey = end

        piece = self.get_piece(sx, sy)
        target = self.get_piece(ex, ey)

        if piece.color != self.current_player:
            raise ChessException("Não é sua vez")

        if any((
            self.handle_castle(piece, start, end),
            self.handle_en_passant(piece, target, start, end),
        )):
            return

        if target.color == piece.color:
            raise ChessException("Não pode capturar peça da mesma cor")

        if not piece.can_move_to(ex, ey):
            raise ChessException("Movimento inválido para essa peça")

        with self.simulate_move(start, end):
            if self.is_in_check(self.current_player):
                raise ChessException("Movimento ilegal: deixa o rei em xeque")

        self.pieces[ex][ey] = piece
        self.pieces[sx][sy] = Empty()

        piece.x, piece.y = ex, ey
        piece.has_moved = True

        self.handle_promotion(piece, end)

        self.current_player = 1 - self.current_player

        if self.is_in_check(self.current_player):
            print("⚠️ XEQUE!")

    def handle_promotion(self, piece, end):
        if not isinstance(piece, Pawn):
            return

        ex, ey = end

        if (piece.color == 1 and ex == 0) or (piece.color == 0 and ex == 7):

            promoted = Queen(piece.color)
            promoted.x, promoted.y = ex, ey
            promoted.board = self

            self.pieces[ex][ey] = promoted

    def handle_en_passant(self, piece, target, start, end):
        if not isinstance(piece, Pawn):
            False

        sx, sy = start
        ex, ey = end

        can_be_en_passant = isinstance(target, Empty) and abs(ey - sy) == 1 and ex - sx == (-1 if piece.color == 0 else 1)

        if can_be_en_passant and self.last_double_pawn == (sx, ey):
            self.pieces[sx][ey] = Empty()
            self.pieces[ex][ey] = piece
            self.pieces[sx][sy] = Empty()

            piece.x, piece.y = ex, ey
            self.last_double_pawn = None
            self.current_player = 1 - self.current_player

            return True

        return False

    def handle_castle(self, piece, start, end):
        sx, sy = start
        ex, ey = end

        # Checa se há roque
        if not (isinstance(piece, King) and abs(ey - sy) == 2):
            return False

        if self.is_in_check(piece.color):
            raise ChessException("Não pode rocar em xeque")

        # Roque pequeno
        if ey == sy + 2:
            rook = self.pieces[sx][7]

            if not isinstance(rook, Rook) or rook.color != piece.color:
                raise ChessException("Roque inválido")

            if piece.has_moved or rook.has_moved:
                raise ChessException("Rei ou torre já se moveram")

            if any(not isinstance(self.pieces[sx][c], Empty) for c in [5, 6]):
                raise ChessException("Caminho bloqueado para roque")
            
            with self.simulate_move(start, (sx, 5)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei passaria por xeque")

            with self.simulate_move(start, (sx, 6)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei terminaria em xeque")

            self.pieces[sx][sy] = Empty()
            self.pieces[sx][6] = piece
            piece.x, piece.y = sx, 6

            self.pieces[sx][7] = Empty()
            self.pieces[sx][5] = rook
            rook.x, rook.y = sx, 5

            piece.has_moved = True
            rook.has_moved = True

            self.last_double_pawn = None
            self.current_player = 1 - self.current_player
            return True

        # Roque grande
        if ey == sy - 2:
            rook = self.pieces[sx][0]

            if not isinstance(rook, Rook) or rook.color != piece.color:
                raise ChessException("Roque inválido")

            if piece.has_moved or rook.has_moved:
                raise ChessException("Rei ou torre já se moveram")

            if any(not isinstance(self.pieces[sx][c], Empty) for c in [1, 2, 3]):
                raise ChessException("Caminho bloqueado para roque")

            with self.simulate_move(start, (sx, 3)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei passaria por xeque")

            with self.simulate_move(start, (sx, 2)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei terminaria em xeque")

            self.pieces[sx][sy] = Empty()
            self.pieces[sx][2] = piece
            piece.x, piece.y = sx, 2

            self.pieces[sx][0] = Empty()
            self.pieces[sx][3] = rook
            rook.x, rook.y = sx, 3

            piece.has_moved = True
            rook.has_moved = True

            self.last_double_pawn = None
            self.current_player = 1 - self.current_player
            return True

        return False

    def __str__(self):
        order = 1 # if self.current_player == 1 else -1

        result = "    0  1  2  3  4  5  6  7\n"
        for index, row in enumerate(self.pieces[::order]):
            result += f"{index} | "
            for piece in row[::order]:
                result += piece.print() + " "
            result += "|\n"
        return result

class Piece:
    symbol = "-"

    def __init__(self, color = 1):
        self.board: Board = None
        self.x = 0
        self.y = 0
        self.color = color
        self.has_moved = False

    @property
    def pos(self):
        return self.x, self.y

    def can_move_to(self, x, y):
        raise NotImplementedError()

    def print(self):
        return f"{self.symbol}{self.color}"

    def __str__(self):
        return f"{self.symbol}{self.color}(pos={self.pos})"

    def is_path_clear_line(self, x1, y1, x2, y2):
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if not isinstance(self.board.current_playerget_piece(x1, y), Empty):
                    return False
            return True

        if y1 == y2:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if not isinstance(self.board.current_playerget_piece(x, y1), Empty):
                    return False
            return True

        return False

    def is_path_clear_diagonal(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1

        if abs(dx) != abs(dy):
            return False

        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        x, y = x1 + step_x, y1 + step_y
        while x != x2 and y != y2:
            if not isinstance(self.get_piece(x, y), Empty):
                return False

            x += step_x
            y += step_y

        return True

class Pawn(Piece):
    symbol = 'p'

    def can_move_to(self, x, y):
        direction = 1 if self.color == 0 else -1
        start_row = 1 if self.color == 0 else 6

        dx = x - self.x
        dy = abs(y - self.y)

        target = self.board.get_piece(x, y)

        self.board.last_double_pawn = (x, y)

        if dy == 0 and dx == direction and isinstance(target, Empty):
            return True

        print(self, target, dx, dy, direction, start_row)
        if dy == 0 and dx == 2 * direction and self.x == start_row:
            mid_x = self.x + direction
            if isinstance(self.board.get_piece(mid_x, y), Empty) and isinstance(target, Empty):
                return True

        if dy == 1 and dx == direction and target.color in (0, 1) and target.color != self.color:
            return True

        self.board.last_double_pawn = None

        return False


class Rook(Piece):
    symbol = 'r'

    def can_move_to(self, x, y):
        if self.x == x or self.y == y:
            return self.is_path_clear_line(self.x, self.y, x, y)
        return False

class Knight(Piece):
    symbol = 'k'
    def can_move_to(self, x, y):
        dx = abs(x - self.x)
        dy = abs(y - self.y)

        return (dx, dy) in [(1, 2), (2, 1)]

class Bishop(Piece):
    symbol = 'b'
    def can_move_to(self, x, y):
        return self.is_path_clear_diagonal(self.x, self.y, x, y)
        
class Queen(Piece):
    symbol = 'Q'
    def can_move_to(self, x, y):
        if self.x == x or self.y == y:
            return self.is_path_clear_line(self.x, self.y, x, y)
        return self.is_path_clear_diagonal(self.x, self.y, x, y)

class King(Piece):
    symbol = 'K'

    def can_move_to(self, x, y):
        dx = abs(x - self.x)
        dy = abs(y - self.y)

        return max(dx, dy) == 1


class Empty(Piece):
    symbol = "·"
    def __init__(self):
        super().__init__(color='·')

    def can_move_to(self, x, y):
        raise ChessException("Cant move from nowhere")

import os


board = Board()

while True:
    os.system('clear')
    print(board)

    start = int(input("sx: ")), int(input("sy: "))
    end = int(input("ex: ")), int(input("ey: "))

    try:
        board.move(start, end)
    except ChessException as e:
        input(e)