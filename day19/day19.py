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

ALL_AXES = (0, 1, 2)

SIZE = 1000

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
    result = []
    for chunk in data:
        result.append([])
        for line in chunk[1:]:
            result[-1].append(
                np.asarray
                ([int(num_str) for num_str in (re.findall(r'-?[0-9]+', line))])
            )
    return result


def all_orientations(grid):
    for dir_x, dir_y in itertools.permutations(range(3), 2):
        for sign_x, sign_y in itertools.product((-1, 1), (-1, 1)):
            x_vec = np.zeros((3,))
            y_vec = np.zeros((3,))
            x_vec[dir_x] = sign_x
            y_vec[dir_y] = sign_y
            z_vec = np.cross(x_vec, y_vec)
            new_grid = []
            for line in grid:
                new_grid.append(np.asarray((
                    np.dot(x_vec, line),
                    np.dot(y_vec, line),
                    np.dot(z_vec, line),
                )))
            yield new_grid


def find_all_distances(grid1, grid2):
    return([tuple(vec2 - vec1) for vec1, vec2 in itertools.product(grid1, grid2)])


def shift_beacons(grid, shift):
    return {tuple((beacon - shift).astype(int)) for beacon in grid}


def manhattan_distance(shift1, shift2):
    return sum(abs(s2 - s1) for s1, s2 in zip(shift1, shift2))


def run_part_1(data):
    unknown = set(range(1, len(data)))
    to_evaluate = collections.deque([0])
    grids = {0: {tuple(beacon) for beacon in data[0]}}
    shifts = [(0, 0, 0)]
    while unknown:
        i = to_evaluate.pop()
        unknown = set(range(len(data))).difference(grids.keys())
        for j in unknown:
            for grid in all_orientations(data[j]):
                 distances = find_all_distances(grids[i], grid)
                 for shift, count in collections.Counter(distances).items():
                     if count >= 12:
                        grids[j] = shift_beacons(grid, shift)
                        to_evaluate.append(j)
                        shifts.append(tuple(shift))
    all_beacons = {beacon for grid in grids.values() for beacon in grid}
    return max(manhattan_distance(shift1, shift2) for shift1, shift2 in itertools.combinations(shifts, 2))

def run_part_2(data):
    pass


if __name__ == '__main__':
    main()