import itertools
from typing import List, Iterator


class BoardError(Exception):
    pass


class ColumnOutOfBoundsError(BoardError):
    pass


class ColumnFullError(BoardError):
    pass


class EmptySpotError(BoardError):
    pass


class Board(object):

    def __init__(self, num_rows: int, num_cols: int, blank_char: str) -> None:
        self.contents = [[blank_char for col in range(num_cols)] for row in range(num_rows)]
        self.blank_char = blank_char
        self._number_of_pieces_in_columns = [0] * self.num_cols

    @property
    def num_rows(self) -> int:
        """
        :return: the number of rows in the board
        """
        return len(self.contents)

    @property
    def num_cols(self) -> int:
        """
        :return: the number of columns in the board
        """
        return len(self.contents[0])

    @property
    def is_full(self) -> bool:
        """
        :return: whether the board is full or not
        """
        return all(
            (space != self.blank_char for row in self for space in row)
        )

    def is_column_in_bounds(self, column: int) -> bool:
        """
        :param column: the column to check
        :return: whether column is in bounds or not
        """
        return 0 <= column < self.num_cols

    def is_column_full(self, column: int) -> bool:
        """
        :param column: the column to check
        :return: Whether column is full or not
        """
        return self._number_of_pieces_in_columns[column] >= self.num_rows

    def contains_blank_character(self, row: int, column: int) -> bool:
        """
        Checks whether row,col contains a blank character
        :param row:  row to check
        :param column: column to check
        :return: whether row,col contains a blank character or not
        """
        return self.contents[row][column] == self.blank_char

    def add_piece_to_column(self, piece: str, column: int) -> int:
        """
        add the piece to the specified column
        :param piece: the piece to add. Should only be a single character
        :param column: the column to add the piece to
        :return: the row the piece was added to
        :raises: ValueError if piece is not a single character
        :raises: ColumnFullError if the column played in is full
        :raises: ColumnOutOfBondsError if the column selected is out of bounds
        """
        if len(piece) != 1:
            raise ValueError(f'Piece may only be a single character but is actually {piece}')
        elif not self.is_column_in_bounds(column):
            raise ColumnOutOfBoundsError(
                f'Your column needs to be between 0 and {self.num_cols - 1} but is actually {column}.')
        elif self.is_column_full(column):
            raise ColumnFullError(f'You cannot play in {column} because it is full.')
        else:
            row = self._number_of_pieces_in_columns[column]
            self.contents[row][column] = piece
            self._number_of_pieces_in_columns[column] += 1
            return row

    def erase_piece_from_column(self, column: int) -> None:
        row = self._number_of_pieces_in_columns[column] - 1
        self.contents[row][column] = self.blank_char
        self._number_of_pieces_in_columns[column] -= 1

    def get_piece_at(self, row: int, column: int) -> str:
        """
        Get the piece at row,col
        :param row: row index
        :param column:  column index
        :return: the piece at row, col
        """
        return self[row][column]

    def count_max_matches(self, row: int, col: int) -> int:
        """
        The maximum number of uninterrupted matches going either horizontally, vertically,
        or diagonally from row,col
        :param: row: the row to check
        :param: col: the column to check
        :return: The maximum number of uninterrupted matches going either horizontally, vertically,
        or diagonally from row,col
        """
        return max(self.count_matches_horizontally(row, col),
                   self.count_matches_vertically(row, col),
                   self.count_matches_in_left_diagonal(row, col),
                   self.count_matches_in_right_diagonal(row, col))

    def count_matches_horizontally(self, row: int, col: int) -> int:
        """
        Count the number of uninterrupted matches to the piece at row,col moving horizontally
        :param: row: the row to start at
        :param: col: the column to start at
        :return: the number of matches to the piece at row,col moving horizontally
        """
        return self._count_matches_forwards_and_backwards(row, col, 0,1)

    def count_matches_vertically(self, row: int, col: int) -> int:
        """
        Count the number of uninterrupted matches to the piece at row,col moving vertically
        :param: row: the row to start at
        :param: col: the column to start at
        :return: the number of matches to the piece at row,col moving vertically
        """
        return self._count_matches_forwards_and_backwards(row, col, 1,0)

    def count_matches_in_right_diagonal(self, row: int, column: int) -> int:
        """
        Count the number of uninterrupted matches to the piece at row,col in this direction
            X
          X
        X
        :param row: the row of the spot to check
        :param column: the column of the spot to check
        :return: the number of uninterrupted matches to the piece at row,col
        """
        return self._count_matches_forwards_and_backwards(row, column, -1, 1)

    def count_matches_in_left_diagonal(self, row: int, column: int) -> int:
        """
        Count the number of uninterrupted matches to the piece at row,col in this direction
        X
          X
            X
        :param row: the row of the spot to check
        :param column: the column of the spot to check
        :return: the number of uninterrupted matches to the piece at row,col
        """
        return self._count_matches_forwards_and_backwards(row, column, 1, 1)

    def _count_matches_forwards_and_backwards(self, row_start: int, column_start: int,
                                              row_step: int, column_step: int) -> int:
        """
        Count the number of pieces matching the piece at row_start, column_start
        Going both forward (row_step, column_step) and backwards (-row_step, -column_step)
        :param row_start: the row of the spot to check
        :param column_start: the column of the spot to check
        :param row_step: how much to advance the row by in each iteration of the search
        :param column_step: how much to advance the column by in each iteration of the search
        :return: whether or not there is a win involving the piece at row_start, column_start
        """
        piece = self.get_piece_at(row_start, column_start)

        if piece == self.blank_char:
            raise EmptySpotError(f'There is no piece at {row_start},{column_start}')

        pieces_in_a_row_forward = self._count_num_pieces_in_a_row_within_range(piece, row_start, column_start,
                                                                               row_step, column_step)

        pieces_in_a_row_backward = self._count_num_pieces_in_a_row_within_range(piece, row_start, column_start,
                                                                                -row_step, -column_step)

        pieces_in_a_row = 1 + pieces_in_a_row_forward + pieces_in_a_row_backward  # + 1 for the piece itself
        return pieces_in_a_row

    def _count_num_pieces_in_a_row_within_range(self, piece: str, row_start: int, col_start: int, row_step: int,
                                                col_step: int) -> int:
        """
        Count the number of pieces in a row that match piece within (row_start,column_start)
        Note that the piece at row_start, column_start is not counted
        :param piece: the piece to match
        :param row_start: what row to start on
        :param col_start: what column to start on
        :param row_step: how much the row should advance by
        :param col_step: how much the column should advance by
        :return: the number of pieces in a row that match piece
        """
        if row_step == 0 and col_step == 0:
            raise ValueError('row_step and col_step cannot both be 0')

        pieces_in_a_row = 0
        # advance one element
        row_start = row_start + row_step
        col_start = col_start + col_step

        # locate the end of the range
        row_end = self.num_rows if row_step >= 0 else -1
        col_end = self.num_cols if col_step >= 0 else -1

        # generate the range of values
        row_range = itertools.repeat(row_start) if row_step == 0 else range(row_start, row_end, row_step)
        column_range = itertools.repeat(col_start) if col_step == 0 else range(col_start, col_end, col_step)

        for row, col in zip(row_range, column_range):  # go through the range
            if self.get_piece_at(row, col) == piece:  # count matches
                pieces_in_a_row += 1
            else:  # stop counting on first mismatch
                break
        return pieces_in_a_row

    def __iter__(self) -> Iterator[List[str]]:
        """
        Iterate through the rows
        :return:
        """
        yield from self.contents

    def __getitem__(self, index: int) -> List[str]:
        """
        Get the index row of the board
        :param index: the index of the row to get
        :return: the indexth row of the board
        """
        return self.contents[index]

    def column_iterate(self) -> Iterator[List[str]]:
        """
        Allow iteration through the columns
        :return:
        """
        yield from zip(*self.contents)

    def __repr__(self) -> str:
        sep = ' ' * max(len(str(self.num_rows - 1)), len(str(self.num_cols - 1)))
        column_headers = sep * 2 + sep.join([str(i) for i in range(self.num_cols)])
        rep = [str(pos) + sep + sep.join(row) for pos, row in enumerate(reversed(self.contents))]
        rep.insert(0, column_headers)
        return '\n'.join(rep)

    def __str__(self) -> str:
        return repr(self)
