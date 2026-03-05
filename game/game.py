from contextlib import contextmanager

from .utils import *
from .exceptions import *
from .piece import *


class Game:
    def __init__(self, on_reset=lambda: print("on_reset")):
        self.on_reset = on_reset
        self.reset()
    
    def reset(self):
        self.last_double_pawn = None
        self.current_player = 1

        self.kings = {
            0: King(color=0),
            1: King(color=1),
        }

        self.board: list[Piece] = [
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
                piece = self.board[x][y]
                piece.x, piece.y = x, y
                piece.game = self

        self.on_reset()

    def get_piece(self, x, y):
        return self.board[x][y]

    def get_all_pieces(self):
        pieces = []
        for row in self.board:
            for piece in row:
                if isinstance(piece, Empty):
                    continue
                pieces.append(piece)
        return pieces

    def get_king_pos(self, color):
        return self.kings[color].pos

    def is_attacked_by(self, x, y, attacker_color):
        for row in self.board:
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

        piece = self.board[sx][sy]
        captured = self.board[ex][ey]

        self.board[ex][ey] = piece
        self.board[sx][sy] = Empty()

        old_x, old_y = piece.x, piece.y
        piece.x, piece.y = ex, ey

        yield

        self.board[sx][sy] = piece
        self.board[ex][ey] = captured
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

        self.board[ex][ey] = piece
        self.board[sx][sy] = Empty()

        piece.x, piece.y = ex, ey
        piece.has_moved = True

        self.handle_promotion(piece, end)

        self.current_player = 1 - self.current_player

        if self.is_in_check(self.current_player):
            print("⚠️ XEQUE!")

        print("Movi", piece)

    def handle_promotion(self, piece, end):
        if not isinstance(piece, Pawn):
            return

        ex, ey = end

        if (piece.color == 1 and ex == 0) or (piece.color == 0 and ex == 7):

            promoted = Queen(piece.color)
            promoted.x, promoted.y = ex, ey
            promoted.board = self

            self.board[ex][ey] = promoted

    def handle_en_passant(self, piece, target, start, end):
        if not isinstance(piece, Pawn):
            False

        sx, sy = start
        ex, ey = end

        can_be_en_passant = isinstance(target, Empty) and abs(ey - sy) == 1 and ex - sx == (-1 if piece.color == 0 else 1)

        if can_be_en_passant and self.last_double_pawn == (sx, ey):
            self.board[sx][ey] = Empty()
            self.board[ex][ey] = piece
            self.board[sx][sy] = Empty()

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
            rook = self.board[sx][7]

            if not isinstance(rook, Rook) or rook.color != piece.color:
                raise ChessException("Roque inválido")

            if piece.has_moved or rook.has_moved:
                raise ChessException("Rei ou torre já se moveram")

            if any(not isinstance(self.board[sx][c], Empty) for c in [5, 6]):
                raise ChessException("Caminho bloqueado para roque")
            
            with self.simulate_move(start, (sx, 5)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei passaria por xeque")

            with self.simulate_move(start, (sx, 6)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei terminaria em xeque")

            self.board[sx][sy] = Empty()
            self.board[sx][6] = piece
            piece.x, piece.y = sx, 6

            self.board[sx][7] = Empty()
            self.board[sx][5] = rook
            rook.x, rook.y = sx, 5

            piece.has_moved = True
            rook.has_moved = True

            self.last_double_pawn = None
            self.current_player = 1 - self.current_player
            return True

        # Roque grande
        if ey == sy - 2:
            rook = self.board[sx][0]

            if not isinstance(rook, Rook) or rook.color != piece.color:
                raise ChessException("Roque inválido")

            if piece.has_moved or rook.has_moved:
                raise ChessException("Rei ou torre já se moveram")

            if any(not isinstance(self.board[sx][c], Empty) for c in [1, 2, 3]):
                raise ChessException("Caminho bloqueado para roque")

            with self.simulate_move(start, (sx, 3)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei passaria por xeque")

            with self.simulate_move(start, (sx, 2)):
                if self.is_in_check(piece.color):
                    raise ChessException("Rei terminaria em xeque")

            self.board[sx][sy] = Empty()
            self.board[sx][2] = piece
            piece.x, piece.y = sx, 2

            self.board[sx][0] = Empty()
            self.board[sx][3] = rook
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
        for index, row in enumerate(self.board[::order]):
            result += f"{index} | "
            for piece in row[::order]:
                result += f"{piece} "
            result += "|\n"
        return result
