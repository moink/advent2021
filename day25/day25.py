import contextlib
import collections
import copy
import functools
import itertools
import math
import re
import statistics

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import advent_tools

SOUTH_FACING = 2

EAST_FACING = 1
EMPTY = 0

def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    data = advent_tools.PlottingGrid.from_file(
        {'.' : EMPTY, '>' : EAST_FACING, 'v': SOUTH_FACING}
    )
    # data.show()
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    # data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    print(data)
    return data


def run_part_1(data):
    old_data = np.zeros_like(data.grid)
    count = 0
    while (old_data != data.grid).any().any():
        count += 1
        old_data = data.grid.copy()
        move_one_step(data, EAST_FACING, 1)
        move_one_step(data, SOUTH_FACING, 0)
        # data.show()
    return count


def move_one_step(data, direction, axis):
    east_facing = data.grid == direction
    empty = data.grid == EMPTY
    moved_right = np.roll(east_facing, 1, axis)
    can_move = moved_right & empty
    do_move = np.roll(can_move, -1, axis)
    data.grid[can_move] = direction
    data.grid[do_move] = EMPTY


def run_part_2(data):
    pass


if __name__ == '__main__':
    main()
