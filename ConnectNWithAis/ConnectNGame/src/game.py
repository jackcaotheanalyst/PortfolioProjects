from typing import List, Optional
from .players import player
from .board import Board
from .players import human_player
from .players import random_ai
from .players import simple_ai


class Game(object):

    @staticmethod
    def create_game_from_file(path_to_file: str) -> "Game":
        """
        create a game from the specified configuration file
        :param path_to_file: the follow holding the configuration
        :return: a game setup up based on the configuration file
        """
        with open(path_to_file) as config_file:
            config = {}
            for line in config_file:
                line = line.strip()
                if line:
                    var, value = line.split(':')
                    var = var.strip()
                    value = value.strip()
                    try:
                        value = int(value)  # type: ignore[assignment]
                    except ValueError:
                        pass
                    config[var] = value
            num_rows = int(config['num_rows'])
            num_cols = int(config['num_cols'])
            board = Board(num_rows, num_cols, config['blank_char'])
            return Game(board, config['num_pieces_to_win'])  # type: ignore[arg-type]

    def __init__(self, board: Board, num_pieces_to_win: int,
                 players: Optional[List["player.Player"]] = None) -> None:

        self.cur_player_turn = 0
        self.board = board
        self.num_pieces_to_win = num_pieces_to_win
        self.someone_won: bool = False
        if players is not None:
            self.players: List[player.Player] = players
        else:
            self.players = []
            for num in range(2):
                self.setup_player(Game.setup_player_type(num))

    @property
    def cur_player(self) -> "player.Player":
        """
        :return: the player whose turn it is
        """
        return self.players[self.cur_player_turn]

    @property
    def num_players(self) -> int:
        """
        :return: The number of players in the game
        """
        return len(self.players)

    @property
    def is_tie_game(self) -> bool:
        """
        Check if the game ended ina tie.
        Can only be safely called after checking if someone won the game
        :return: if the game ended in a tie
        """
        return self.board.is_full

    @staticmethod
    def setup_player_type(player_num: int) -> str:
        """
        Create the players for this game
        :return: the type of player
        """
        player_types = ["human", "random", "simple"]
        while True:
            print(f"Choose the type for Player {player_num + 1}")
            player_type = input(f"Enter Human or Random or Simple: ").strip().lower()
            if player_type != "":
                if any(i.startswith(player_type) for i in player_types):
                    break
                else:
                    print(f"{player_type} is not one of Human or Random or Simple. Please try again.")
            else:
                print(f"{player_type} is not one of Human or Random or Simple. Please try again.")
        return player_type

    def setup_player(self, player_type: str) -> None:
        if "human".startswith(player_type):
            self.players.append(human_player.HumanPlayer.create_from_user_input(self.players, self.board.blank_char))
        elif "random".startswith(player_type):
            self.players.append(random_ai.RandomAi.create_from_itself(self.players, self.board))
        elif "simple".startswith(player_type):
            self.players.append(simple_ai.SimpleAI.create_from_itself(self.players, self))
        else:
            return None

    def play(self) -> None:
        """
        Play a game of ConnectN to completion
        :return: None
        """
        while True:
            print(self.board)
            player_move = self.cur_player.take_turn(self.board)
            if player_move.ends_game(self):
                int_player_move_row = int(player_move.row)
                int_player_move_column = int(player_move.column)
                self.someone_won = self.is_part_of_win(int_player_move_row, int_player_move_column)
                break
            self.change_turn()
        self.declare_winner_or_tie()

    def is_game_over(self) -> bool:
        """
        :return: whether the game is over
        """
        return self.someone_won or self.is_tie_game

    def is_part_of_win(self, row: int, column: int) -> bool:
        """
        Check if the given piece is part of a win
        :param row:
        :param column:
        :return:
        :side effect: modifies someone_won
        """
        if self.board.contains_blank_character(row, column):
            raise ValueError(f'{row},{column} contains a blank space')

        return self.board.count_max_matches(row, column) >= self.num_pieces_to_win

    def change_turn(self) -> None:
        """
        Change the turn to the next player in line
        :return:
        """
        self.cur_player_turn = (self.cur_player_turn + 1) % self.num_players

    def declare_winner_or_tie(self) -> None:
        """
        Print out who won the game or if it was a tie
        :return:
        """
        print(self.board)
        if self.someone_won:
            print(f'{self.cur_player} won the game!')
        else:
            print('Tie Game.')
