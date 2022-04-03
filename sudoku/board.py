from copy import copy
import numpy as np

from sudoku.move import Move
from sudoku.sector_id import SectorId


class Board:
    def __init__(self, board: np.ndarray) -> None:
        self._current_board = board
        self._move_history = list()
        self._root = copy(board)

    @staticmethod
    def empty() -> "Board":
        empty_board = np.array((
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None),
            (None, None, None, None, None, None, None, None, None)))
        return Board(empty_board)

    @property
    def root(self):
        return Board(self._root)

    def filled(self) -> bool:
        flat_board = [item for sublist in self._current_board for item in sublist]
        return None not in set(flat_board)

    def valid(self) -> bool:
        return self.all_rows_valid() and self.all_columns_valid() and self.all_sectors_valid()

    def win(self) -> bool:
        return self.filled() and self.valid()

    def valid_moves(self):
        moves = self.possible_moves()
        valid_moves = list()

        for move in moves:
            self.make_move(move)
            if self.valid():
                valid_moves.append(move)
            self.unmake_last_move()
        return valid_moves

    def possible_moves(self):
        possible_moves = list()
        for row_index in range(9):
            for column_index in range(9):
                if self._current_board[row_index][column_index] is not None:
                    continue
                possible_moves += [Move(row_index, column_index, x) for x in range(1, 10)]
        return possible_moves

    def make_move(self, move: Move) -> bool:
        if self._current_board[move.row][move.column] is not None:
            return False

        self._move_history.append(move)
        self._current_board[move.row][move.column] = move.number
        return True

    def unmake_last_move(self) -> bool:
        if not self._move_history:
            return False

        move = self._move_history.pop()
        self._current_board[move.row][move.column] = None
        return True

    def column(self, column_index: int) -> np.ndarray:
        return np.array(tuple(x[column_index] for x in self._current_board))

    def row(self, row_index: int) -> np.ndarray:
        return np.array(self._current_board[row_index])

    def sector(self, sector_id: SectorId) -> np.ndarray:
        row_index, column_index = SectorId.get_starting_indices(sector_id)
        return np.array((
            self._current_board[row_index][column_index:column_index + 3],
            self._current_board[row_index + 1][column_index:column_index + 3],
            self._current_board[row_index + 2][column_index:column_index + 3]))

    def all_columns_valid(self) -> bool:
        return np.all([self.column_valid(x) for x in range(9)])

    def all_rows_valid(self) -> bool:
        return np.all([self.row_valid(x) for x in range(9)])

    def all_sectors_valid(self) -> bool:
        return np.all([self.sector_valid(x) for x in SectorId])

    def column_valid(self, row_index: int) -> bool:
        filled_numbers_in_column = [x for x in self.column(row_index) if x is not None]
        return len(filled_numbers_in_column) == len(set(filled_numbers_in_column))

    def row_valid(self, row_index: int) -> bool:
        filled_numbers_in_row = [x for x in self.row(row_index) if x is not None]
        return len(filled_numbers_in_row) == len(set(filled_numbers_in_row))

    def sector_valid(self, sector_id: SectorId) -> bool:
        flat_sector = [item for sublist in self.sector(sector_id) for item in sublist]
        filled_numbers_in_sector = [x for x in flat_sector if x is not None]
        return len(filled_numbers_in_sector) == len(set(filled_numbers_in_sector))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            raise NotImplementedError
        return np.all(self._current_board == other._current_board)

    def __repr__(self):
        string = " --- --- --- --- --- --- --- --- ---\n"
        for row_index in range(9):
            row_numbers = tuple(x if x is not None else " " for x in self.row(row_index))
            string += "| {} | {} | {} | {} | {} | {} | {} | {} | {} |\n".format(*row_numbers) \
                      + " --- --- --- --- --- --- --- --- ---\n"
        return string


if __name__ == "__main__":
    brd = Board.empty()
    brd.make_move(Move(0, 0, 9))
    brd.make_move(Move(7, 7, 9))
    brd.make_move(Move(8, 8, 9))
    print(brd)
    print(brd.valid())
    print(brd.filled())
    print(brd.win())
