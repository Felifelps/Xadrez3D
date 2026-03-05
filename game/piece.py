from . import ChessException
from models.mesh import Mesh

class Piece:
    symbol = "-"

    def __init__(self, color = 1):
        self.game = None
        self.x = 0
        self.y = 0
        self.color = color
        self.has_moved = False

    @property
    def pos(self):
        return self.x, self.y

    def can_move_to(self, x, y):
        raise NotImplementedError()

    def __str__(self):
        return f"{self.symbol}{self.color}"

    def is_path_clear_line(self, x1, y1, x2, y2):
        if x1 == x2:
            step = 1 if y2 > y1 else -1
            for y in range(y1 + step, y2, step):
                if not isinstance(self.game.get_piece(x1, y), Empty):
                    return False
            return True

        if y1 == y2:
            step = 1 if x2 > x1 else -1
            for x in range(x1 + step, x2, step):
                if not isinstance(self.game.get_piece(x, y1), Empty):
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
            if not isinstance(self.game.get_piece(x, y), Empty):
                return False

            x += step_x
            y += step_y

        return True

    def get_legal_moves(self):
        moves = []
        for x in range(8):
            for y in range(8):
                if (x, y) == (self.x, self.y):
                    continue

                if not self.can_move_to(x, y):
                    continue

                target = self.game.get_piece(x, y)
                if isinstance(target, Empty) or target.color != self.color:
                    moves.append((x, y))

        return moves

class Pawn(Piece):
    symbol = 'p'

    def can_move_to(self, x, y):
        direction = 1 if self.color == 0 else -1
        start_row = 1 if self.color == 0 else 6

        dx = x - self.x
        dy = abs(y - self.y)

        target = self.game.get_piece(x, y)

        self.game.last_double_pawn = (x, y)

        if dy == 0 and dx == direction and isinstance(target, Empty):
            return True

        if dy == 0 and dx == 2 * direction and self.x == start_row:
            mid_x = self.x + direction
            if isinstance(self.game.get_piece(mid_x, y), Empty) and isinstance(target, Empty):
                return True

        if dy == 1 and dx == direction and target.color in (0, 1) and target.color != self.color:
            return True

        self.game.last_double_pawn = None

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
