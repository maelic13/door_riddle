from time import time
from typing import List

import numpy as np

from sudoku.board import Board
from sudoku.move import Move


class SudokuSolver:
    @classmethod
    def solve_board(cls, board: Board) -> Board:
        valid_moves = cls._sort_moves(board.valid_moves())
        for move in valid_moves:
            board.make_move(move)
            board = cls.solve_board(board)
            if board.win():
                return board
            board.unmake_last_move()
        return board

    @classmethod
    def _sort_moves(cls, moves: List[Move]) -> List[Move]:
        counter = dict()
        for move in moves:
            if move.square not in counter:
                counter[move.square] = 1
                continue
            counter[move.square] += 1
        return sorted(moves, key=lambda x: counter[x.square])


if __name__ == "__main__":
    task_board = Board(np.array((
        (6, None, None, None, 7, 1, 4, None, None),
        (1, 8, 5, None, None, 9, 2, None, None),
        (None, 4, None, 2, 5, None, 9, None, 8),
        (5, None, 8, None, 3, None, None, None, 4),
        (None, 7, 3, None, None, None, 6, None, 1),
        (None, None, None, None, None, None, None, None, None),
        (2, 3, 4, 9, 1, None, None, 7, 6),
        (8, None, None, None, None, 7, 1, None, 9),
        (7, 1, None, 6, 8, 3, None, None, None))))

    task_board2 = Board(np.array((
        (6, 9, 2, 8, 7, 1, 4, 5, 3),
        (1, 8, 5, 3, 4, 9, 2, 6, 7),
        (3, 4, 7, 2, 5, 6, 9, 1, 8),
        (5, 6, 8, 1, 3, 2, 7, 9, 4),
        (4, 7, 3, 5, 9, 8, 6, 2, 1),
        (9, 2, 1, 7, 6, 4, 3, 8, 5),
        (2, 3, 4, 9, 1, 5, 8, 7, 6),
        (8, 5, 6, 4, 2, 7, 1, 3, 9),
        (7, 1, 9, 6, 8, 3, 5, 4, 2))))

    start = time()
    solution = SudokuSolver.solve_board(task_board)
    end = time()
    print(solution)
    print(solution == task_board2)

    print(f"Execution time: {end - start} s.")
