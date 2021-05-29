from typing import List, Optional
import random
from ConnectNGame.src import move
from ConnectNGame.src import board
from . import player


class RandomAi(player.Player):
    VISIBLE_CHARACTERS = [chr(i) for i in range(ord('!'), ord('~') + 1)]
    number_created = 0

    def __init__(self, name: str, piece: str, board: "board.Board") -> None:
        super().__init__(name, piece)
        self.board = board

    @staticmethod
    def create_from_itself(players: List["player.Player"], board: "board.Board") -> "player.Player":
        """
        Create player for user input
        :param board: The board for it to play
        :param players: The other players in the game
        :return: A player created from this user's input
        """
        name = f"RandomAi {len(players) + 1}"
        piece = RandomAi.get_piece(players, board.blank_char)
        return RandomAi(name, piece, board)

    @staticmethod
    def get_piece(players: List["player.Player"], blank_char: str, case_matters: bool = False) -> Optional[str]:
        result = None
        piece = random.choice(RandomAi.VISIBLE_CHARACTERS)
        cmp_piece = piece if case_matters else piece.lower()
        player_pieces = {player.piece if case_matters else player.piece.lower(): player for player in players}
        if cmp_piece not in player_pieces and cmp_piece != blank_char.lower():
            result = piece
        return result

    def get_move(self) -> "move.Move":
        while True:
            random_move = random.randint(0, self.board.num_cols - 1)
            str_random_move = str(random_move)
            int_random_move = int(random_move)
            if not self.board.is_column_full(int_random_move):
                break
        return move.Move.from_string(self, str_random_move)
