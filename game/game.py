from contextlib import contextmanager

from .utils import *
from .exceptions import *
from .piece import *


class Game:

    def __init__(self, on_reset=lambda: None, on_move=lambda: None):
        self.on_reset = on_reset
        self.on_move = on_move

    def reset(self):
        self.moves = {}
        self.current_move_index = 0

        self.last_double_pawn = None
        self.current_player = 1

        self.kings = {
            0: King(color=0),
            1: King(color=1),
        }

        self.board: list[list[Piece]] = [
            [Rook(0), Knight(0), Bishop(0), Queen(0), self.kings[0], Bishop(0), Knight(0), Rook(0)],
            [Pawn(0) for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Empty() for _ in range(8)],
            [Pawn(1) for _ in range(8)],
            [Rook(1), Knight(1), Bishop(1), Queen(1), self.kings[1], Bishop(1), Knight(1), Rook(1)],
        ]

        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                piece.x = x
                piece.y = y
                piece.game = self

        self.on_reset()

    def get_piece(self, x, y):
        return self.board[x][y]

    def get_all_pieces(self):
        pieces = []
        for row in self.board:
            for p in row:
                if not isinstance(p, Empty):
                    pieces.append(p)
        return pieces

    def get_king_pos(self, color):
        return self.kings[color].pos

    def change_player(self):
        self.current_player = 1 - self.current_player

    def is_attacked_by(self, x, y, attacker_color):

        for piece in self.get_all_pieces():

            if piece.color != attacker_color:
                continue

            if piece.can_move_to(x, y):
                return True

        return False

    def is_in_check(self, color):
        kx, ky = self.get_king_pos(color)
        return self.is_attacked_by(kx, ky, 1 - color)

    def has_legal_moves(self, color):

        for piece in self.get_all_pieces():

            if piece.color != color:
                continue

            for x in range(8):
                for y in range(8):

                    target = self.get_piece(x, y)

                    if target.color == color:
                        continue

                    if not piece.can_move_to(x, y):
                        continue

                    with self.simulate_move(piece.pos, (x, y)):
                        if not self.is_in_check(color):
                            return True

        return False

    def is_checkmate(self, color):

        if not self.is_in_check(color):
            return False

        return not self.has_legal_moves(color)

    @contextmanager
    def simulate_move(self, start, end):

        sx, sy = start
        ex, ey = end

        piece = self.board[sx][sy]
        captured = self.board[ex][ey]

        old_piece_pos = (piece.x, piece.y)
        old_captured_pos = None
        old_last_double = self.last_double_pawn

        if not isinstance(captured, Empty):
            old_captured_pos = (captured.x, captured.y)
            captured.x = -1
            captured.y = -1

        self.board[ex][ey] = piece
        self.board[sx][sy] = Empty()

        piece.x, piece.y = ex, ey

        yield

        self.board[sx][sy] = piece
        self.board[ex][ey] = captured

        piece.x, piece.y = old_piece_pos

        if old_captured_pos:
            captured.x, captured.y = old_captured_pos

        self.last_double_pawn = old_last_double

    def undo(self):
        move = self.moves.get(self.current_move_index - 1, None)

        if not move:
            return

        self.current_move_index -= 1
        piece, target, start, end = move

        sx, sy = start
        ex, ey = end

        self.board[sx][sy] = piece
        self.board[ex][ey] = target

        piece.x, piece.y = start
        target.x, target.y = end

        self.on_move()
        self.change_player()

    def move(self, start, end):

        validate_pos(start)
        validate_pos(end)

        sx, sy = start
        ex, ey = end

        piece = self.get_piece(sx, sy)
        target = self.get_piece(ex, ey)

        if piece.color != self.current_player:
            raise InvalidMoveException("Não é sua vez")

        if target.color == piece.color:
            raise InvalidMoveException("Não pode capturar peça da mesma cor")

        if self.handle_castle(piece, start, end):
            return

        if self.handle_en_passant(piece, start, end):
            return

        if not piece.can_move_to(ex, ey):
            raise InvalidMoveException("Movimento inválido para essa peça")

        with self.simulate_move(start, end):
            puts_in_check = self.is_in_check(self.current_player)
        
        if puts_in_check:
            raise InvalidMoveException("Movimento ilegal: deixa o rei em cheque")

        self.board[sx][sy] = Empty()
        self.board[ex][ey] = piece

        piece.x, piece.y = ex, ey
        piece.has_moved = True

        self.handle_promotion(piece, end)

        if isinstance(piece, Pawn) and abs(ex - sx) == 2:
            self.last_double_pawn = (ex, ey)
        else:
            self.last_double_pawn = None

        self.moves[self.current_move_index] = (piece, target, start, end)
        self.current_move_index += 1

        self.on_move()

        self.change_player()

        if self.is_checkmate(self.current_player):
            raise CheckmateException("Xeque-mate")

        if self.is_in_check(self.current_player):
            raise InCheckException("Está em cheque")

    def handle_promotion(self, piece, end):

        if not isinstance(piece, Pawn):
            return

        ex, ey = end

        if (piece.color == 1 and ex == 0) or (piece.color == 0 and ex == 7):

            promoted = Queen(piece.color)
            promoted.x, promoted.y = ex, ey
            promoted.game = self

            self.board[ex][ey] = promoted

    def handle_en_passant(self, piece, start, end):

        if not isinstance(piece, Pawn):
            return False

        sx, sy = start
        ex, ey = end

        target = self.get_piece(ex, ey)

        if sy == ey:
            return False

        if not isinstance(target, Empty):
            return False

        if self.last_double_pawn != (sx, ey):
            return False

        with self.simulate_move(start, end):

            self.board[sx][ey] = Empty()

            if self.is_in_check(self.current_player):
                return False

        self.board[sx][ey] = Empty()

        self.board[ex][ey] = piece
        self.board[sx][sy] = Empty()

        piece.x, piece.y = ex, ey
        piece.has_moved = True

        self.on_move()

        self.last_double_pawn = None
        self.current_player = 1 - self.current_player

        return True

    def handle_castle(self, piece, start, end):

        if not isinstance(piece, King):
            return False

        sx, sy = start
        ex, ey = end

        if abs(ey - sy) != 2:
            return False

        if piece.has_moved:
            raise InvalidMoveException("Rei já se moveu")

        if self.is_in_check(piece.color):
            raise InvalidMoveException("Não pode rocar em cheque")

        if ey > sy:
            rook = self.board[sx][7]
            rook_target = 5
            between = [5, 6]
        else:
            rook = self.board[sx][0]
            rook_target = 3
            between = [1, 2, 3]

        if not isinstance(rook, Rook) or rook.color != piece.color:
            raise InvalidMoveException("Roque inválido")

        if rook.has_moved:
            raise InvalidMoveException("Torre já se moveu")

        for c in between:
            if not isinstance(self.board[sx][c], Empty):
                raise InvalidMoveException("Caminho bloqueado")

        step = 1 if ey > sy else -1

        with self.simulate_move(start, (sx, sy + step)):
            if self.is_in_check(piece.color):
                raise InvalidMoveException("Rei passaria por cheque")

        with self.simulate_move(start, end):
            if self.is_in_check(piece.color):
                raise InvalidMoveException("Rei terminaria em cheque")

        self.board[sx][sy] = Empty()
        self.board[ex][ey] = piece
        piece.x, piece.y = ex, ey

        self.board[sx][rook.y] = Empty()
        self.board[sx][rook_target] = rook
        rook.x, rook.y = sx, rook_target

        piece.has_moved = True
        rook.has_moved = True

        self.on_move()

        self.current_player = 1 - self.current_player
        self.last_double_pawn = None

        return True

    def __str__(self):
        result = "    0  1  2  3  4  5  6  7\n"

        for i, row in enumerate(self.board):
            result += f"{i} | "
            for piece in row:
                result += f"{piece} "
            result += "|\n"

        return result
    