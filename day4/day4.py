import contextlib
import collections
import copy
import functools
import itertools
import math
from io import FileIO, StringIO

import numpy as np
import pandas as pd
import re

import advent_tools


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
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
    row_sums = drawn.sum(axis=1)
    # print(row_sums)
    if (row_sums == size).any():
        return True
    col_sums = drawn.sum(axis=0)
    if (col_sums == size).any():
        return True
    return False


def score_board(board, drawn, cur_draw):
    to_sum = board * (1 - drawn)
    sum = to_sum.sum().sum()
    return sum * cur_draw

def run_part_1(drawing, boards):
    drawns = [np.zeros_like(boards[0])] * len(boards)
    for cur_draw in drawing:
        for board_num in range(len(boards)):
            drawns[board_num] = drawns[board_num] | (boards[board_num] == cur_draw)
            if is_winner(drawns[board_num]):
                return score_board(boards[board_num], drawns[board_num], cur_draw)
    raise RuntimeError("No winner after all drawings")

def run_part_2(drawing, boards):
    drawns = [np.zeros_like(boards[0])] * len(boards)
    no_win_yet = set(range(len(boards)))
    for cur_draw in drawing:
        for board_num in range(len(boards)):
            if board_num in no_win_yet:
                drawns[board_num] = drawns[board_num] | (boards[board_num] == cur_draw)
                if is_winner(drawns[board_num]):
                    no_win_yet.remove(board_num)
                if len(no_win_yet) == 0:
                    return score_board(boards[board_num], drawns[board_num], cur_draw)
    raise RuntimeError("No winner after all drawings")


if __name__ == '__main__':
    main()