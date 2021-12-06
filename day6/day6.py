import contextlib
import collections
import copy
import functools
import itertools
import math
import numpy as np
import pandas as pd
import re

import advent_tools


def main():
    # advent_tools.TESTING = True
    data = advent_tools.read_all_integers()[0]
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
    d = collections.defaultdict(int)
    for c in data:
        d[c] = d[c] + 1
    n_steps = 256
    for _ in range(n_steps):
        new_d = collections.defaultdict(int, {n-1: c for n, c in d.items()})
        zero_count = new_d.pop(-1, 0)
        new_d[6] = new_d[6] + zero_count
        new_d[8] = zero_count
        d = new_d
    return sum(d.values())
        # print(d)
        # print(collections.Counter([6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8]))

def run_part_2(data):
    pass


if __name__ == '__main__':
    main()