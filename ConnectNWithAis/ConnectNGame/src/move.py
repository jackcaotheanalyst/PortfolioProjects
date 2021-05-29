from typing import Optional, Any
from .players import player
from . import board
from . import game


class MoveError(Exception):
    pass


class MoveFormatError(MoveError):
    pass


class Move(object):
    @classmethod
    def from_string(cls, maker: "player.Player", str_move: str) -> "Move":
        """
        Convert the string representation of the move made by maker into a Move object
        :param maker: the player that made the move
        :param str_move: the string representation of the move
        :return: the move represented by the string
        :raises: Move FormatError if str_move does not represent an actual move
        """
        try:
            column = int(str_move)
            return Move(maker, column)
        except ValueError:
            raise MoveFormatError(f'{maker}, column needs to be an integer. {str_move} is not an integer. ')

    def __init__(self, maker: "player.Player", column: int) -> None:
        self.maker = maker
        self.row: Optional[int] = None
        self.column = column

    def make(self, the_board: "board.Board") -> None:
        """
        Make the move on the_board
        :param the_board: the board to apply the move to
        :return: None
        """
        self.row = the_board.add_piece_to_column(self.maker.piece, self.column)

    def ends_game(self, the_game: "game.Game") -> bool:
        """
        :param the_game: the game the move was made on
        :return: whether the move would end the game
        :raises: a Value error if Move.make has not been called
        """
        if self.row is None:
            raise ValueError('Move.make must be called before Move.ends_game')
        else:
            return the_game.is_part_of_win(self.row, self.column) or the_game.is_tie_game

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Move) and \
               self.maker is other.maker and \
               self.row == other.row and \
               self.column == other.column

    def __ne__(self, other: Any) -> bool:
        return not self == other
