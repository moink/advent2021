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


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    data = process_input(data)
    low_points = find_low_points(data)
    print('Part 1:', run_part_1(data, low_points))
    print('Part 2:', run_part_2(data, low_points))


def process_input(data):
    result = np.zeros((len(data), len(data[0])), dtype=int)
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            result[i, j] = int(char)
    return result


def run_part_1(data, low_points):
    low_values = data[low_points]
    return sum(low_values) +len(low_values)


def find_low_points(data):
    # is the number less than the one on its left?
    xdiff = np.diff(data, axis=1)
    d1 = np.pad(xdiff, ((0, 0), (1, 0)),
                "constant", constant_values=((0, 0), (-1, 0))) < 0
    # is the number less than the on on its left?
    d2 = np.pad(xdiff, ((0, 0), (0, 1)),
                "constant", constant_values=((0, 0), (0, 1))) > 0
    # is the number less than the one above it?
    ydiff = np.diff(data, axis=0)
    d3 = np.pad(ydiff, ((1, 0), (0, 0)),
                "constant", constant_values=((-1, 0), (0, 0))) < 0
    # is the number less than the one below it?
    d4 = np.pad(ydiff, ((0, 1), (0, 0)),
                "constant", constant_values=((0, 1), (0, 0))) > 0
    low_points = d1 & d2 & d3 & d4
    return low_points


def run_part_2(data, low_points):
    y_coords, x_coords = np.where(low_points)
    basin_sizes = []
    for x, y in zip(x_coords, y_coords):
        # print(x, y, data[y, x])
        in_basin = get_basin(data, x, y)
        basin_sizes.append(len(in_basin))
    return math.prod(sorted(basin_sizes, reverse=True)[0:3])


def get_basin(data, start_x, start_y):
    max_y, max_x = data.shape
    in_basin = {(start_y, start_x)}
    not_evaluated = collections.deque([(start_y, start_x)])
    while not_evaluated:
        y, x = not_evaluated.pop()
        if x - 1 >= 0:
            new_pos = (y, x - 1)
            maybe_add_to_basin(data, in_basin, new_pos, not_evaluated)
        if x + 1 < max_x:
            new_pos = (y, x + 1)
            maybe_add_to_basin(data, in_basin, new_pos, not_evaluated)
        if y - 1 >= 0:
            new_pos = (y - 1, x)
            maybe_add_to_basin(data, in_basin, new_pos, not_evaluated)
        if y + 1 < max_y:
            new_pos = (y + 1, x)
            maybe_add_to_basin(data, in_basin, new_pos, not_evaluated)
    return in_basin


def maybe_add_to_basin(data, in_basin, new_pos, not_evaluated):
    if new_pos not in in_basin:
        if data[new_pos] != 9:
            in_basin.add(new_pos)
            not_evaluated.append(new_pos)


if __name__ == '__main__':
    main()