import contextlib
import collections
import copy
import functools
import itertools
import math
import time

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
    # data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    print(data)
    return data


def run_part_1(data):
    res = 1e16
    print(math.fabs(4-3))
    for i in range(max(data)):
        can3 = (math.fabs(d-i) for d in data)
        can = sum(can3)
        if can < res:
            res = can
    return res


def run_part_2(data):
    start = time.perf_counter()
    res = 1e16
    for i in range(max(data)):
        fuel = sum(get_fuel(int(math.fabs(d-i))) for d in data)
        if fuel < res:
            res = fuel
    end = time.perf_counter()
    return res, end - start

@functools.lru_cache()
def get_fuel(dist):
    return sum(range(dist + 1))

if __name__ == '__main__':
    main()