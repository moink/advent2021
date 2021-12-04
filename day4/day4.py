from io import StringIO

import numpy as np

import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    drawing, boards = process_input(data)
    print('Part 1:', run_part_1(drawing, boards))
    print('Part 2:', run_part_2(drawing, boards))


def process_input(data):
    drawing = [int(num) for num in data[0][0].split(",")]
    boards = []
    for grid in data[1:]:
        temp = StringIO("\n".join(grid))
        boards.append(np.loadtxt(temp, dtype=int))
    return drawing, boards


def is_winner(drawn):
    size, _ = drawn.shape
    for axis in [0, 1]:
        row_sums = drawn.sum(axis=axis)
        if (row_sums == size).any():
            return True
    return False


def score_board(board, drawn, cur_draw):
    not_called = board * (1 - drawn)
    sum = not_called.sum().sum()
    return sum * cur_draw


def run_part_1(drawing, boards):
    drawn = [np.zeros_like(boards[0])] * len(boards)
    for cur_draw in drawing:
        for board_num in range(len(boards)):
            drawn[board_num] = drawn[board_num] | (boards[board_num] == cur_draw)
            if is_winner(drawn[board_num]):
                return score_board(boards[board_num], drawn[board_num], cur_draw)
    raise RuntimeError("No winner after all drawings")


def run_part_2(drawing, boards):
    drawn = [np.zeros_like(boards[0])] * len(boards)
    no_win_yet = set(range(len(boards)))
    for cur_draw in drawing:
        for board_num in range(len(boards)):
            if board_num in no_win_yet:
                drawn[board_num] = drawn[board_num] | (boards[board_num] == cur_draw)
                if is_winner(drawn[board_num]):
                    no_win_yet.remove(board_num)
                if len(no_win_yet) == 0:
                    return score_board(boards[board_num], drawn[board_num], cur_draw)
    raise RuntimeError("Still some losing boards after all drawings")


if __name__ == '__main__':
    main()