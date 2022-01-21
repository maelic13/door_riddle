from itertools import combinations
from functools import partial
from multiprocessing import cpu_count, Pool
from typing import List, TypeVar

import chess
import numpy as np


T = TypeVar("T")


def get_solutions(check_piece: chess.Piece, positions: list[chess.Board]) -> List[chess.Board]:
    solutions = list()
    for board in positions:
        for sq in chess.SQUARES:
            if board.piece_at(sq) == check_piece:
                if len(board.attackers(check_piece.color, sq)):
                    break
        solutions.append(board)
    return solutions


def get_batches(positions: List[T], num_batches: int) -> List[List[T]]:
    batch_size = int(len(positions) / num_batches)
    batches = [positions[i * batch_size:(i + 1) * batch_size] for i in range(num_batches)]
    batches[0] += positions[num_batches * batch_size:]
    return batches


def get_all_possible_positions(num_pieces: int) -> np.ndarray:
    which = np.array(list(combinations(range(64), num_pieces)))
    grid = np.zeros((len(which), 64), dtype="int8")
    grid[np.arange(len(which))[None].T, which] = 1
    return grid


def convert_to_boards(positions: np.ndarray, piece: chess.Piece) -> List[chess.Board]:
    converted = list()
    for position in positions:
        board = chess.Board()
        board.clear_board()
        for square, occupied in zip(chess.SQUARES, position):
            if occupied:
                board.set_piece_at(square, piece)
        converted.append(board)
    return converted


if __name__ == "__main__":
    piece = chess.Piece(chess.QUEEN, chess.Color(chess.WHITE))
    cpus = cpu_count()

    boards = convert_to_boards(get_all_possible_positions(8), piece)
    possible_positions = get_batches(boards, cpus)

    with Pool(processes=cpus) as pool:
        found_solutions = pool.map(partial(get_solutions, piece), possible_positions)
    found_solutions = [item for sublist in found_solutions for item in sublist]

    # for solution in found_solutions:
    #     print(solution)

    print(f"{len(found_solutions)} solutions found!")
