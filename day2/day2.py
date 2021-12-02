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
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    return data


def run_part_1(data):
    depth = 0
    pos = 0
    for line in data:
        direction, str_step = line.split()
        step = int(str_step)
        if direction == "forward":
            pos = pos + step
        elif direction == "up":
            depth = depth - step
        elif direction == "down":
            depth = depth + step
        else:
            raise RuntimeError
    return depth * pos


def run_part_2(data):
    depth = 0
    pos = 0
    aim = 0
    for line in data:
        direction, str_step = line.split()
        step = int(str_step)
        if direction == "forward":
            pos = pos + step
            depth = depth + aim * step
        elif direction == "up":
            aim = aim - step
        elif direction == "down":
            aim = aim + step
        else:
            raise RuntimeError
    return depth * pos


if __name__ == '__main__':
    main()