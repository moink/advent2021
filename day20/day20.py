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
    data = advent_tools.read_input_line_groups()
    data = process_input(data)
    print('Part 1:', run_part(data, 2))
    print('Part 2:', run_part(data, 50))  # 20767 is too high


def process_input(data):
    algo = [0 if char == "." else 1 for char in data[0][0]]
    grid = advent_tools.PlottingGrid.from_str(text=data[1])
    return algo, grid


def get_new_shape(shape):
    n, m = shape
    return n + 2, m + 2


def run_part(data, steps):
    algo, grid = data
    off_edges_val = 0
    for _ in range(steps):
        # grid.show()
        new_grid = advent_tools.PlottingGrid(get_new_shape(grid.grid.shape))
        n, m = grid.grid.shape
        for j in range(-1, n + 1):
            for i in range(-1, m + 1):
                nums = []
                for jj in range(j - 1, j + 2):
                    for ii in range(i - 1, i + 2):
                        if 0 <= jj < n and 0 <= ii < m:
                            val = grid.grid[jj, ii]
                        else:
                            val = off_edges_val
                        nums.append(str(val))
                lookup_val = int("".join(nums), 2)
                new_grid.grid[j + 1, i + 1] = algo[lookup_val]
        grid = new_grid
        if off_edges_val == 0:
            off_edges_val = algo[0]
        else:
            off_edges_val = algo[-1]
    grid.show()
    return grid.sum().sum()

def run_part_2(data):
    pass


if __name__ == '__main__':
    main()