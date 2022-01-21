from itertools import combinations
from time import time
from typing import List, Tuple

import chess


def valid(board: chess.Board, chess_piece: chess.Piece) -> bool:
    for square in board.pieces(chess_piece.piece_type, chess_piece.color):
        if len(board.attackers(chess_piece.color, square)):
            return False
    return True


def get_board_from_square_numbers(position: List[int], chess_piece: chess.Piece) -> chess.Board:
    board = chess.Board()
    board.clear_board()
    for square in position:
        board.set_piece_at(square, chess_piece)
    return board


def quick_check_queen(comb: List[int]) -> bool:
    rows = list()
    files = list()
    for square in comb:
        row = square % 8
        file = int(square / 8)
        if row in rows or file in files:
            return False
        rows.append(row)
        files.append(file)
    return True


def quick_check(piece_type: chess.PieceType) -> callable:
    checks = {
        chess.QUEEN: quick_check_queen,
    }
    return checks.get(piece_type, lambda _: True)


def get_solutions_no_memory(chess_piece: chess.Piece, piece_number: int) -> Tuple[List[chess.Board], int, float]:
    def log_progress(num_positions: int, start_time: float, last_log: float) -> bool:
        if not time() - last_log > 10.:
            return False
        elapsed = time() - start_time
        speed = num_positions / elapsed
        print(f"{int(num_positions / 1000000)} millions positions checked, "
              f"{int(elapsed / 60)} minutes {int(elapsed % 60)} seconds elapsed, "
              f"{int(speed / 1000)} kpos/s.")
        return True

    start = time()
    checkpoint = time()
    solutions = list()
    positions_checked = 0
    quick_check_func = quick_check(chess_piece.piece_type)
    for comb in combinations(range(64), piece_number):
        positions_checked += 1
        if log_progress(positions_checked, start, checkpoint):
            checkpoint = time()
        if not quick_check_func(comb):
            continue
        board = get_board_from_square_numbers(comb, chess_piece)
        if valid(board, chess_piece):
            solutions.append(board)
    return solutions, positions_checked, time() - start


if __name__ == "__main__":
    piece = chess.Piece(chess.QUEEN, chess.Color(chess.WHITE))
    num_pieces = 8
    found_solutions, combinations_checked, elapsed_seconds = get_solutions_no_memory(piece, num_pieces)

    print(f"\n{combinations_checked} combinations checked, {len(found_solutions)} solutions found!")
    print(f"The procedure took {int(elapsed_seconds / 60)} minutes {int(elapsed_seconds % 60)} seconds.")

    with open("solutions.txt", "w") as save_file:
        for solved_board in found_solutions:
            save_file.write(solved_board.fen() + "\n")
