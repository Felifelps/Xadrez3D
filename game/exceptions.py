
class ChessException(Exception):
    pass

class InvalidMoveException(ChessException):
    def __str__(self):
        return f"Movimento inválido: {self.args[0]}"

class InCheckException(ChessException):
    pass

class CheckmateException(ChessException):
    pass
