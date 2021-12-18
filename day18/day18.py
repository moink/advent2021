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
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = []
    for line in data:
        result.append(eval(line))
    return result


def try_explode(pair0):
    result = []
    right = 0
    have_exploded = False
    last_num_ref = "pass"
    for pair1 in pair0:
        if isinstance(pair1, list):
            result.append([])
            for pair2 in pair1:
                if isinstance(pair2, list):
                    result[-1].append([])
                    for pair3 in pair2:
                        if isinstance(pair3, list):
                            result[-1][-1].append([])
                            for pair4 in pair3:
                                if isinstance(pair4, list):
                                    if not have_exploded:
                                        left, right = pair4
                                        exec(last_num_ref)
                                        result[-1][-1][-1].append(0)
                                        have_exploded = True
                                    else:
                                        left2, right2 = pair4
                                        result[-1][-1][-1].append([left2 + right, right2])
                                        right = 0
                                else:
                                    result[-1][-1][-1].append(pair4 + right)
                                    last_num_ref = f"result[{len(result) -1}][{len(result[-1]) -1}][{len(result[-1][-1]) -1}][{len(result[-1][-1][-1]) -1}] += left"
                                    right = 0
                        else:
                            result[-1][-1].append(pair3 + right)
                            last_num_ref = f"result[{len(result) -1}][{len(result[-1]) -1}][{len(result[-1][-1]) -1}] += left"
                            right = 0
                else:
                    result[-1].append(pair2 + right)
                    last_num_ref = f"result[{len(result) -1}][{len(result[-1]) -1}] += left"
                    right = 0
        else:
            result.append(pair1 + right)
            last_num_ref = f"result[{len(result) -1}] += left"
            right = 0
    return result


def try_split(line):

    if isinstance(line, int):
        if line >= 10:
            left = line // 2
            right = line - left
            return [left, right], True
        return line, False
    have_split = False
    result = []
    for child in line:
        if not have_split:
            new_child, have_split = try_split(child)
        else:
            new_child = child
        result.append(new_child)
    return result, have_split


def run_part_1(data):
    return calc_magnitude(sum_snailfish(data))


def sum_snailfish(data):
    result = reduce_snailfish(data[0])
    for line in data[1:]:
        result = reduce_snailfish([result, line])
    return result


def reduce_snailfish(line):
    finished = False
    while not finished:
        line, finished = try_next_step(line)
    return line


def try_next_step(line):
    new_line = try_explode(line)
    if new_line != line:
        return new_line, False
    new_line, _ = try_split(line)
    if new_line != line:
        return new_line, False
    return line, True


def calc_magnitude(expr):
    if isinstance(expr, int):
        return expr
    return 3 * calc_magnitude(expr[0]) + 2 * calc_magnitude(expr[1])


def run_part_2(data):
    return max(calc_magnitude(sum_snailfish(p)) for p in itertools.permutations(data, 2))


if __name__ == '__main__':
    main()