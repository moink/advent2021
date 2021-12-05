import contextlib
import collections
import copy
import functools
import itertools
import math
import numpy as np
import pandas as pd
import re
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('Qt5Agg')

import advent_tools


def main():
    # advent_tools.TESTING = True
    data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    print(data)
    return data


def run_part_1(data):
    # min_x = min([dat[0] for dat in data] + [dat[2] for dat in data])
    # max_x = max([dat[0] for dat in data] + [dat[2] for dat in data])
    # min_y = min([dat[1] for dat in data] + [dat[3] for dat in data])
    # max_y = max([dat[1] for dat in data] + [dat[3] for dat in data])
    grid = np.zeros((1000, 1000))
    # grid = np.zeros((10, 10))
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            grid[x0, min(y0, y1):max(y0, y1)+1] += 1
            # print(f"Horizontal at x={x0} from y={y0} to {y1}")
        if y0 == y1:
            grid[min(x0, x1):max(x0, x1)+1, y0] += 1
            # print(f"Vertical at y={y0} from x={x0} to {x1}")
        # plt.imshow(grid.T)
        # plt.show()
    # print(grid.sum().sum())

    return (grid >= 2).sum().sum()

def run_part_2(data):
    # min_x = min([dat[0] for dat in data] + [dat[2] for dat in data])
    # max_x = max([dat[0] for dat in data] + [dat[2] for dat in data])
    # min_y = min([dat[1] for dat in data] + [dat[3] for dat in data])
    # max_y = max([dat[1] for dat in data] + [dat[3] for dat in data])
    grid = np.zeros((1000, 1000))
    # grid = np.zeros((10, 10))
    for x0, y0, x1, y1 in data:
        if x0 == x1:
            grid[x0, min(y0, y1):max(y0, y1) + 1] += 1
            print(f"Vertical at x={x0} from y={y0} to {y1}")
        elif y0 == y1:
            grid[min(x0, x1):max(x0, x1) + 1, y0] += 1
            print(f"Horizontal at y={y0} from x={x0} to {x1}")
        else:
            xrange, yrange = get_ranges(x0, x1, y0, y1)
            for x, y in zip(xrange, yrange):
                grid[x, y] += 1
            print(f"Diagonal with {xrange} and {yrange}")
    plt.imshow(grid.T)
    plt.colorbar()
    plt.show()
    # print(grid.sum().sum())
    return (grid >= 2).sum().sum()


def get_ranges(x0, x1, y0, y1):
    xrange = list(range(x0, x1 + 1)) or list(range(x0, x1 - 1, -1))
    yrange = list(range(y0, y1 + 1)) or list(range(y0, y1 - 1, -1))
    return xrange, yrange


if __name__ == '__main__':
    # print(get_ranges(9, 7, 7, 9))
    main()