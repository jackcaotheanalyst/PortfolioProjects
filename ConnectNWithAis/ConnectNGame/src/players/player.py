from typing import List, Any
from ConnectNGame.src import move
from ConnectNGame.src.board import Board, BoardError
import abc


class Player(object):

    @staticmethod
    def create_from_user_input(players: List["Player"], blank_char: str) -> "Player":
        ...

    @staticmethod
    def get_valid_piece(players: List["Player"], blank_char: str, case_matters: bool = False) -> str:
        ...

    @staticmethod
    def get_valid_name(players: List["Player"], case_matters: bool = False) -> str:
        ...

    def __init__(self, name: str, piece: str) -> None:
        self.name = name
        self.piece = piece

    def take_turn(self, the_board: Board) -> "move.Move":
        """
        Have the player take their turn
        :param the_board: the board to make their move on
        :return: the move the player made
        """
        while True:
            try:
                player_move = self.get_move()
                player_move.make(the_board)
            except (move.MoveError, BoardError) as error:
                print(error)
            else:
                return player_move

    @abc.abstractmethod
    def get_move(self) -> "move.Move":
        ...

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Player) and \
               self.name == other.name and \
               self.piece == other.piece

    def __ne__(self, other: Any) -> bool:
        return not self == other
