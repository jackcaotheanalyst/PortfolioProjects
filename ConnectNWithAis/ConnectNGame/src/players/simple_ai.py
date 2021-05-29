from typing import List, Optional
import random
from . import player
from ConnectNGame.src import move
from ConnectNGame.src import game


class SimpleAI(player.Player):
    VISIBLE_CHARACTERS = [chr(i) for i in range(ord('!'), ord('~') + 1)]

    def __init__(self, name: str, piece: str, simple_game: "game.Game") -> None:
        super().__init__(name, piece)
        self.game = simple_game

    @staticmethod
    def create_from_itself(players: List["player.Player"], simple_game: "game.Game") -> "player.Player":
        """
        Create player for user input
        :param simple_game: the game for it to play
        :param players: The other players in the game
        :return: A player created from this user's input
        """
        name = f"SimpleAi {len(players) + 1}"
        piece = SimpleAI.get_piece(players, simple_game.board.blank_char)
        return SimpleAI(name, piece, simple_game)

    @staticmethod
    def get_piece(players: List["player.Player"], blank_char: str, case_matters: bool = False) -> Optional[str]:
        result = None
        piece = random.choice(SimpleAI.VISIBLE_CHARACTERS)
        cmp_piece = piece if case_matters else piece.lower()
        player_pieces = {player.piece if case_matters else player.piece.lower(): player for player in players}
        if cmp_piece not in player_pieces and cmp_piece != blank_char.lower():
            result = piece
        return result

    def get_move(self) -> "move.Move":
        opponent = (self.game.cur_player_turn + 1) % len(self.game.players)
        opponent_piece = self.game.players[opponent].piece
        pieces = [self.piece, opponent_piece]
        for piece in pieces:
            for col in range(self.game.board.num_cols):
                if not self.game.board.is_column_full(col):
                    int_move = col
                    row = self.game.board.add_piece_to_column(piece, int_move)
                    str_move = str(int_move)
                    if self.game.is_part_of_win(row, int_move):
                        self.game.board.erase_piece_from_column(int_move)
                        return move.Move.from_string(self, str_move)
                    self.game.board.erase_piece_from_column(int_move)
                else:
                    continue
        while True:
            random_move = random.randint(0, self.game.board.num_cols - 1)
            str_random_move = str(random_move)
            int_random_move = int(random_move)
            if not self.game.board.is_column_full(int_random_move):
                break
        return move.Move.from_string(self, str_random_move)
