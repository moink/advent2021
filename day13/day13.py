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
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    max_x = max(int(line.split(",")[0]) for line in data[0])
    max_y = max(int(line.split(",")[1]) for line in data[0])
    grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for line in data[0]:
        x, y = line.split(",")
        grid[int(y), int(x)] = 1
    folds = []
    for line in data[1]:
        equation = line.split()[-1]
        axis, pos = equation.split("=")
        if axis == "x":
            folds.append((1, int(pos)))
        else:
            folds.append((0, int(pos)))
    return grid, folds


def fold_grid(grid, axis, pos):
    if axis == 0:
        grid1 = grid[0: pos, :]
        # print(grid1)
        grid2 = grid[pos + 1:, :]
        # print(grid2)
    else:
        grid1 = grid[:, 0: pos]
        # print(grid1)
        grid2 = grid[:, pos + 1:]
        # print(grid2)
    new_grid2 = np.flip(grid2, axis=axis)
    result = grid1 | new_grid2
    # print(result)
    return result


def run_part_1(data):
    grid, folds = data
    grid = fold_grid(grid, folds[0][0], folds[0][1])
    return grid.sum().sum()
    # grid = fold_grid(grid, folds[1][0], folds[1][1])
    return grid

def run_part_2(data):
    grid, folds = data
    for axis, pos in folds:
        grid = fold_grid(grid, axis, pos)
    plt.imshow(grid)
    plt.show()
    return grid


if __name__ == '__main__':
    main()