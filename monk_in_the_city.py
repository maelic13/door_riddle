import numpy as np


def search(current_position: list, cost: float, visited_positions: list) -> None:
    if np.all(current_position == [4, 4]) and cost == 0:
        print("Solution found!")
        print_path(visited_positions)

    possible_moves = generate_moves(current_position, cost, visited_positions)
    for move in possible_moves:
        search(move[0], move[1], visited_positions + [[current_position, move[0]]])


def is_valid_position(position: list) -> bool:
    return 0. <= position[0] <= 4. and 0. <= position[1] <= 4.


def generate_moves(position: list, cost: float, visited_lines: list) -> list:
    moves = list()

    up_position = [position[0], position[1] - 1]
    down_position = [position[0], position[1] + 1]
    left_position = [position[0] - 1, position[1]]
    right_position = [position[0] + 1, position[1]]

    if is_valid_position(up_position) and line_not_used(position, up_position, visited_lines):
        moves.append([up_position, cost / 2.])
    if is_valid_position(down_position) and line_not_used(position, down_position, visited_lines):
        moves.append([down_position, cost * 2.])
    if is_valid_position(left_position) and line_not_used(position, left_position, visited_lines):
        moves.append([left_position, cost - 2.])
    if is_valid_position(right_position) and line_not_used(position, right_position, visited_lines):
        moves.append([right_position, cost + 2.])

    return moves


def line_not_used(position, destination, visited_lines):
    return not ([position, destination] in visited_lines or [destination, position] in visited_lines)


def print_path(visited_positions):
    print(visited_positions[::2])


if __name__ == "__main__":
    search([2, 0], 4., [[[0, 0], [1, 0]], [[1, 0], [2, 0]]])
